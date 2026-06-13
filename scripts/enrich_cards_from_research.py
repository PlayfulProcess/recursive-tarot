# -*- coding: utf-8 -*-
"""Enrich grammar cards with sourced research from research/cards/<slug>.md.

ADD-ONLY: injects a single new section "Research note" into each matched card
(Depicts + 'Changed from parent' delta + the card's [@…] sources + a dossier pointer).
Never removes or overwrites existing fields/sections. Idempotent (skips cards that
already have a "Research note"). Matches dossier '## <n> — <name>' blocks to grammar
items by metadata.number, then by normalized name.

  python3 scripts/enrich_cards_from_research.py            # dry-run report
  python3 scripts/enrich_cards_from_research.py --apply    # write changes
"""
import json, glob, os, re, sys, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APPLY = "--apply" in sys.argv
ONLY = [a for a in sys.argv[1:] if not a.startswith("--")]

ROMAN = {"i":1,"ii":2,"iii":3,"iiii":4,"iv":4,"v":5,"vi":6,"vii":7,"viii":8,"ix":9,"viiii":9,
         "x":10,"xi":11,"xii":12,"xiii":13,"xiiii":14,"xiv":14,"xv":15,"xvi":16,"xvii":17,
         "xviii":18,"xviiii":19,"xix":19,"xx":20,"xxi":21}

def to_int(v):
    if isinstance(v, int): return v
    if isinstance(v, str):
        t = v.strip().lower()
        if t.isdigit(): return int(t)
        if t in ROMAN: return ROMAN[t]
    return None

def strip_prefix(s):
    # remove a leading number / roman numeral + separator: "0 — Fool", "I · Le Bateleur"
    return re.sub(r"^\s*(?:\d+|[ivx]+)\s*[—\-–·.:]+\s*", "", s or "", flags=re.I)

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[*_`]", "", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\b(the|le|la|les|of|de|du|des|el|il|lo|a|au|aux)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def name_keys(s):
    """all normalized name candidates from a label like 'Le Bateleur (The Magician / Mountebank)'."""
    s = strip_prefix(s)
    keys = set()
    main = re.sub(r"\(.*?\)", " ", s)                 # name without parens
    keys.add(norm(main))
    for frag in re.findall(r"\((.*?)\)", s):          # each parenthetical
        for piece in re.split(r"[/·]| or ", frag):
            keys.add(norm(piece))
    return {k for k in keys if len(k) >= 3}

def parse_blocks(md):
    # returns list of (num|None, name, body)
    body = md.split("\n## ", 1)
    parts = re.split(r"(?m)^##\s+", md)
    out = []
    for p in parts[1:]:
        line, _, rest = p.partition("\n")
        m = re.match(r"\s*(\d+)\s*[—\-–]\s*(.*)", line)
        if m:
            num, name = int(m.group(1)), m.group(2).strip()
        else:
            num, name = None, line.strip()
        out.append((num, name, rest))
    return out

def bullet(body, *labels):
    for lab in labels:
        m = re.search(r"\*\*" + re.escape(lab) + r"[^:]*:?\*\*\s*(.*?)(?=\n-\s+\*\*|\n##|\Z)", body, re.S)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip(" .") + "."
    return ""

def cites(text):
    return sorted(set(re.findall(r"\[@([A-Za-z0-9_:-]+)\]", text)), key=str.lower)

def enrich(slug):
    dp = os.path.join(ROOT, "research", "cards", slug + ".md")
    gp = os.path.join(ROOT, "tarot", slug, "grammar.json")
    if not (os.path.exists(dp) and os.path.exists(gp)):
        return None
    g = json.load(open(gp, encoding="utf-8"))
    items = [it for it in g["items"] if not it.get("composite_of")]
    by_num, by_name = {}, {}
    for it in items:
        n = to_int((it.get("metadata") or {}).get("number"))
        if n is not None:
            by_num.setdefault(n, []).append(it)
        keys = set()
        for key in (it.get("name"), (it.get("metadata") or {}).get("french_name"),
                    (it.get("metadata") or {}).get("italian_name")):
            keys |= name_keys(key or "")
        for k in keys:
            by_name.setdefault(k, it)
    blocks = parse_blocks(open(dp, encoding="utf-8").read())
    matched, total = 0, 0
    for num, name, body in blocks:
        depicts = bullet(body, "Depicts")
        changed = bullet(body, "Changed from parent", "Changed from its parent", "Changed")
        if not (depicts or changed):
            continue                      # section/overview block, not a card
        total += 1
        it = None
        # prefer name match (handles suit/rank, FR/EN); fall back to unique number match
        for k in name_keys(name):
            if k in by_name:
                it = by_name[k]; break
        if not it and num is not None and len(by_num.get(num, [])) == 1:
            it = by_num[num][0]
        if not it:
            continue
        matched += 1
        if "Research note" in it.get("sections", {}):
            continue
        src = cites(body)
        txt = ""
        if changed:
            txt += "**What changed (vs. its parent):** " + changed + " "
        elif depicts:
            txt += depicts + " "
        if src:
            txt += "\n\n*Sources:* " + ", ".join("[@" + k + "]" for k in src) + "."
        txt += f"\n\n*Full card-by-card research:* `research/cards/{slug}.md`."
        if APPLY:
            it.setdefault("sections", {})["Research note"] = txt.strip()
    if APPLY and matched:
        json.dump(g, open(gp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return matched, total, len(items)

print(f"{'deck':32} matched/cardblocks  items   {'(APPLY)' if APPLY else '(dry-run)'}")
tot_m = 0
for dp in sorted(glob.glob(os.path.join(ROOT, "research", "cards", "*.md"))):
    slug = os.path.basename(dp)[:-3]
    if ONLY and slug not in ONLY:
        continue
    r = enrich(slug)
    if r:
        m, t, ni = r
        tot_m += m
        flag = "" if t == 0 else ("  ⚠low" if m / t < 0.6 else "")
        print(f"{slug:32} {m:3}/{t:<3}             {ni:4}{flag}")
print(f"TOTAL cards enriched: {tot_m}")
