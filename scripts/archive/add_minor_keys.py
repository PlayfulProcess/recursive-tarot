#!/usr/bin/env python3
"""add_minor_keys.py — give every Minor-Arcana item a canonical `minor_key`, the cross-deck
grouping key for minors, exactly analogous to the hand-authored `trump_key` on the majors.

A minor_key looks like `four-of-coins`, `ace-of-cups`, `knight-of-swords`: a canonical RANK +
canonical SUIT, so the 'same' card lines up across decks regardless of whether a deck calls the
suit Coins / Pentacles / Deniers or the court a Page / Knave / Fante / Valet. The per-deck
`suit`, `rank`, `number` fields are left untouched — minor_key is purely additive (like trump_key).

  python3 scripts/add_minor_keys.py            # dry-run: report keys + any unmapped tokens
  python3 scripts/add_minor_keys.py --apply     # write minor_key into the deck grammars

Run build_meta_grammar.py + check_all.py afterwards.
"""
import json, os, re, sys, glob, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GEN = {"all-decks-many-lenses", "people-of-tarot", "test"}  # generated / fixture — skip

SUITMAP = {
    "cups":"cups","coupes":"cups","coppe":"cups","hearts":"cups",
    "coins":"coins","deniers":"coins","pentacles":"coins","disks":"coins","disc":"coins",
        "denari":"coins","ori":"coins","money":"coins","diamonds":"coins",
    "swords":"swords","epees":"swords","spade":"swords","spada":"swords","spades":"swords",
    "batons":"batons","baton":"batons","wands":"batons","staves":"batons","staff":"batons",
        "clubs":"batons","bastoni":"batons","rods":"batons",
}
COURTMAP = {
    "page":"page","knave":"page","fante":"page","valet":"page","jack":"page",
        "princess":"page","panze":"page",
    "knight":"knight","cavallo":"knight","cavaliere":"knight","cavalier":"knight",
        "chevalier":"knight","horseman":"knight","prince":"knight",
    "queen":"queen","regina":"queen","reine":"queen","dame":"queen","donna":"queen",
    "king":"king","re":"king","roi":"king","koenig":"king","sota":"king",
    # Cary-Yale Visconti's extra female courts are genuinely distinct cards (it has SIX courts
    # per suit) — keep them as their own keys, never folded into page/knight.
    "damsel":"damsel","maid":"maid","horsewoman":"horsewoman",
}
PIPS = {"ace","two","three","four","five","six","seven","eight","nine","ten"}
NUMWORD = {1:"ace",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"ten"}

def is_minor(md):
    return (md.get("arcana") == "minor" or md.get("suit")
            or str(md.get("archetype","")).startswith("card:"))

def canon_suit(md, unmapped):
    raw = md.get("suit")
    if not raw:
        m = re.match(r"card:.+?-of-(.+)", str(md.get("archetype","")))
        raw = m.group(1) if m else None
    if not raw: return None
    tok = re.sub(r"[^a-z]", "", str(raw).lower())
    cs = SUITMAP.get(tok)
    if not cs: unmapped["suit"][str(raw)] += 1
    return cs

def canon_rank(md, unmapped):
    # priority: archetype rank token, then number, then rank field
    raw = None
    m = re.match(r"card:(.+?)-of-", str(md.get("archetype","")))
    if m: raw = m.group(1)
    if raw is None and isinstance(md.get("number"), int): return NUMWORD.get(md["number"])
    if raw is None and str(md.get("number","")).isdigit(): return NUMWORD.get(int(md["number"]))
    if raw is None: raw = md.get("rank")
    if not raw: return None
    tok = re.sub(r"[^a-z]", "", str(raw).split("(")[0].lower())  # 'knave (fante)' -> 'knave'
    if tok == "one": tok = "ace"
    if tok in PIPS: return tok
    if tok in COURTMAP: return COURTMAP[tok]
    unmapped["rank"][str(raw)] += 1
    return None

def main():
    apply = "--apply" in sys.argv
    unmapped = {"suit": collections.Counter(), "rank": collections.Counter()}
    keys = collections.Counter()
    per_deck = {}
    files = sorted(f for f in glob.glob(os.path.join(ROOT, "tarot", "*", "grammar.json"))
                   if os.path.basename(os.path.dirname(f)) not in GEN)
    for gp in files:
        slug = os.path.basename(os.path.dirname(gp))
        g = json.load(open(gp, encoding="utf-8"))
        added = 0
        for it in g["items"]:
            md = it.get("metadata")
            if not md or not is_minor(md): continue
            cs = canon_suit(md, unmapped); cr = canon_rank(md, unmapped)
            if not cs or not cr: continue
            mk = f"{cr}-of-{cs}"
            keys[mk] += 1
            if md.get("minor_key") != mk:
                md["minor_key"] = mk; added += 1
        per_deck[slug] = added
        if apply and added:
            json.dump(g, open(gp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # guard: a minor_key must be unique WITHIN a deck — a collision means two distinct cards were
    # wrongly merged (e.g. an extra court folded into page). Fail loud so the mapping gets fixed.
    collisions = []
    for gp in files:
        slug = os.path.basename(os.path.dirname(gp))
        seen = collections.defaultdict(list)
        for it in json.load(open(gp, encoding="utf-8"))["items"]:
            mk = (it.get("metadata") or {}).get("minor_key")
            if mk: seen[mk].append(it["id"])
        for mk, ids in seen.items():
            if len(ids) > 1: collisions.append(f"{slug}: {mk} <- {ids}")

    print(f"{'APPLIED' if apply else 'DRY-RUN'} · {len(files)} decks")
    print(f"distinct minor_keys: {len(keys)} (expect ~56 = 14 ranks × 4 suits)")
    print(f"keyed minor items: {sum(keys.values())}")
    miss = sorted(set(f"{r}-of-{s}" for r in list(PIPS)+['page','knight','queen','king']
                      for s in ['cups','coins','swords','batons']) - set(keys))
    if miss: print(f"keys with NO card in any deck: {miss}")
    for kind in ("suit","rank"):
        if unmapped[kind]:
            print(f"UNMAPPED {kind} tokens (left unkeyed — add to map): {dict(unmapped[kind])}")
    if collisions:
        print("⚠ INTRA-DECK COLLISIONS (two cards share a minor_key — fix the mapping):")
        for c in collisions: print("   " + c)
    else:
        print("intra-deck collisions: none (every minor_key is unique within its deck)")
    if not apply:
        print("\nper-deck would-add:", {k:v for k,v in per_deck.items() if v})

if __name__ == "__main__":
    main()
