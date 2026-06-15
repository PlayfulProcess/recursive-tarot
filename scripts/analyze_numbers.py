#!/usr/bin/env python3
"""analyze_numbers.py — reproducibly answer: does each NUMBER (Ace–Ten) carry the same meaning
across suits and across decks?  Reads every deck grammar, groups the minor pips by number, and
reports the shared key (the Golden Dawn Sephirah) + the per-suit divinatory meanings, each linked
back to its grammar source (deck slug + item id).  No claims are written here that the grammars
don't contain.

  python3 scripts/analyze_numbers.py            # human report
  python3 scripts/analyze_numbers.py --evidence # also write research/synthesis/_numbers-evidence.json

Findings feed research/synthesis/numbers.json (the authored synthesis) and flag inconsistencies
for the 'rewrite the grammars if they disagree' pass.
"""
import json, os, re, sys, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
T = os.path.join(ROOT, "tarot")
RANKWORD = {"ace":1,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,
            "eight":8,"nine":9,"ten":10}
NAME = {1:"Ace",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten"}
CANON = {"cups":"Cups","coins":"Coins","pentacles":"Coins","disks":"Coins",
         "swords":"Swords","batons":"Batons","wands":"Batons","staves":"Batons","clubs":"Batons"}

def rank_suit(it):
    md = it.get("metadata") or {}
    n = md.get("number")
    suit = md.get("suit")
    arch = str(md.get("archetype") or "")
    m = re.match(r"card:(.+?)-of-(.+)", arch)
    if n is None and m: n = RANKWORD.get(m.group(1).lower())
    if not suit and m: suit = m.group(2)
    if isinstance(n, str) and n.isdigit(): n = int(n)
    cs = CANON.get(str(suit).lower()) if suit else None
    return (n if isinstance(n, int) else None), cs

def meaning(it):
    s = it.get("sections") or {}
    return (s.get("Divinatory Meaning") or s.get("Divinatory Meanings") or s.get("Reading")
            or s.get("Scene") or "")

def main():
    col = json.load(open(os.path.join(T, "_collection.json")))
    decks = [g for g in col["grammars"] if not g.get("is_meta")]
    by_num = collections.defaultdict(list)        # number -> [entry]
    for g in decks:
        try: dg = json.load(open(os.path.join(T, g["slug"], "grammar.json")))
        except Exception: continue
        for it in dg["items"]:
            md = it.get("metadata") or {}
            if md.get("arcana") != "minor" and not md.get("suit") and "card:" not in str(md.get("archetype","")):
                continue
            n, cs = rank_suit(it)
            if not n or n > 10 or not cs: continue      # pips only (courts handled elsewhere)
            by_num[n].append({"deck": g["slug"], "year": g.get("year"), "suit": cs,
                "item": it["id"], "sephirah": md.get("sephirah"),
                "gd_title": (md.get("golden_dawn_title")), "meaning": meaning(it).strip()})

    evidence = {}
    print("="*78)
    print("DO THE NUMBERS CARRY A SHARED MEANING ACROSS SUITS & DECKS?  (pips Ace–Ten)")
    print("="*78)
    for n in range(1, 11):
        ents = by_num.get(n, [])
        seph = sorted({e["sephirah"] for e in ents if e["sephirah"]})
        decks_n = sorted({e["deck"] for e in ents})
        suits_n = sorted({e["suit"] for e in ents})
        consistent = "YES — single Sephirah" if len(seph) == 1 else ("—" if not seph else f"⚠ {len(seph)} different")
        print(f"\n{NAME[n]} (n={n}) · {len(ents)} pip cards · {len(decks_n)} decks · suits {suits_n}")
        print(f"   shared key (Golden Dawn Sephirah): {seph or '(none in data)'}  → cross-suit consistent: {consistent}")
        # one Golden-Dawn-sourced reading per suit, to see if the meaning rhymes across suits
        gd = [e for e in ents if e["deck"] == "golden-dawn-book-t-tarot"]
        for e in sorted(gd, key=lambda x: x["suit"]):
            print(f"     {e['suit']:<7} [{e['deck']}#{e['item']}] {('“'+e['gd_title']+'” — ') if e['gd_title'] else ''}{e['meaning'][:90]}")
        evidence[n] = {"name": NAME[n], "sephirah": seph, "decks": decks_n, "suits": suits_n,
                       "cards": len(ents),
                       "golden_dawn": [{"suit": e["suit"], "title": e["gd_title"],
                                        "meaning": e["meaning"], "source": f"{e['deck']}#{e['item']}"}
                                       for e in sorted(gd, key=lambda x: x["suit"])]}
    # inconsistencies worth a grammar-rewrite pass
    print("\n" + "-"*78)
    print("INCONSISTENCIES (candidates for the grammar-rewrite pass):")
    flagged = 0
    for n in range(1, 11):
        seph = sorted({e["sephirah"] for e in by_num.get(n, []) if e["sephirah"]})
        if len(seph) > 1:
            print(f"   {NAME[n]}: Sephirah disagrees across decks → {seph}"); flagged += 1
    if not flagged: print("   none for pip→Sephirah (the occult layer is internally consistent).")

    if "--evidence" in sys.argv:
        out = os.path.join(ROOT, "research", "synthesis", "_numbers-evidence.json")
        json.dump({"_about": "Auto-extracted from the deck grammars by scripts/analyze_numbers.py. "
                   "Evidence for research/synthesis/numbers.json — every reading links back to <deck>#<item>.",
                   "numbers": evidence}, open(out, "w"), indent=2, ensure_ascii=False)
        print(f"\nwrote {os.path.relpath(out, ROOT)}")

if __name__ == "__main__":
    main()
