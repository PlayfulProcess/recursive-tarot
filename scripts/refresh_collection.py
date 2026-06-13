# -*- coding: utf-8 -*-
"""Refresh tarot/_collection.json DERIVED fields from the actual grammar files.

The grammars are the source of truth; this re-syncs each registry entry's name, type,
items count, cover_image_url, default_preview and blurb from tarot/<slug>/grammar.json.
It PRESERVES curation (branches, deck_slugs, slug/branch/is_meta/path, top-level fields)
and only rewrites the derived fields. Idempotent.

Run from repo root:  python3 scripts/refresh_collection.py
"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COLL = os.path.join(ROOT, "tarot", "_collection.json")


def blurb_of(g):
    desc = (g.get("description") or "").strip().split("\n")[0]
    return (desc[:200] + "…") if len(desc) > 200 else desc


def main():
    c = json.load(open(COLL, encoding="utf-8"))
    changed = []
    for e in c.get("grammars", []):
        path = os.path.join(ROOT, e["path"])
        if not os.path.exists(path):
            print("  MISSING grammar:", e["path"]); continue
        g = json.load(open(path, encoding="utf-8"))
        new = {
            "name": g.get("name"),
            "type": g.get("grammar_type"),
            "default_preview": g.get("default_preview"),
            "items": len(g.get("items", [])),
            "cover_image_url": g.get("cover_image_url"),
            "blurb": blurb_of(g),
        }
        for k, v in new.items():
            if e.get(k) != v:
                changed.append(f"{e['slug']}.{k}")
                e[k] = v
    json.dump(c, open(COLL, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"refreshed {len(c['grammars'])} entries; {len(changed)} fields changed")
    for ch in changed:
        print("   ~", ch)


if __name__ == "__main__":
    main()
