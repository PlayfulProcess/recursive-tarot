#!/usr/bin/env python3
"""Record WHERE each card image is used across the site, so we can spread unique cards
(never the same image twice on a page, ideally not across sibling pages) and render the
most of the library. Writes:
  - a top-level `_image_usage` array onto each deck's grammar.json (the deck's own images
    that appear in site chrome, with the pages they feed) — "metadata in the grammar";
  - a human registry at docs/plan/IMAGE-USAGE.md (with cross-page duplicate flags).
Re-run after editing any page's imagery (CLAUDE.md notes the upkeep rule). Idempotent.
Run from repo root: python scripts/audit_image_usage.py
"""
import json, os, re, glob, urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = "grammar-illustrations/"
PAGES = ["index.html"] + [p.replace(os.sep, "/") for p in glob.glob(os.path.join(ROOT, "pages", "*.html"))]
PAGES += [p.replace(os.sep, "/") for p in glob.glob(os.path.join(ROOT, "pages", "games", "*.html"))]

def page_label(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/") if os.path.isabs(p) else p

# image-path -> set of pages
usage = {}
for p in PAGES:
    fp = p if os.path.isabs(p) else os.path.join(ROOT, p)
    if not os.path.exists(fp): continue
    txt = open(fp, encoding="utf-8").read()
    for m in re.findall(r"grammar-illustrations/[^'\")\s]+\.(?:jpg|jpeg|png|gif)", txt):
        usage.setdefault(m, set()).add(page_label(p))

# group by deck (the folder right after grammar-illustrations/)
by_deck = {}
for img, pages in usage.items():
    rest = img[len(BASE):]
    deck = rest.split("/")[0] if "/" in rest else "_shared"
    by_deck.setdefault(deck, []).append((urllib.parse.unquote(rest.split("/")[-1]), sorted(pages)))

# write _image_usage onto each matching deck grammar
wrote = 0
for f in glob.glob(os.path.join(ROOT, "tarot", "*", "grammar.json")):
    slug = os.path.basename(os.path.dirname(f))
    entries = by_deck.get(slug)
    g = json.load(open(f, encoding="utf-8"))
    new = [{"image": fn, "used_on": pg} for fn, pg in sorted(entries)] if entries else None
    if g.get("_image_usage") != new:
        if new is None: g.pop("_image_usage", None)
        else: g["_image_usage"] = new
        json.dump(g, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        wrote += 1

# registry + cross-page duplicate flags
lines = ["# Image usage registry (generated — `python scripts/audit_image_usage.py`)",
         "",
         "Where each card image appears in the site chrome. Keep unique within a page, and avoid",
         "reusing the same image across sibling pages (Home / Play / About) so the library shows its",
         "range. Regenerate after editing any page's imagery.", ""]
dupes = {img: p for img, p in usage.items() if len(p) > 1}
lines.append(f"**{len(usage)} images used across {len(PAGES)} pages.** "
             f"{len(dupes)} image(s) appear on more than one page:\n")
for img, pages in sorted(dupes.items()):
    lines.append(f"- `{urllib.parse.unquote(img.split('/')[-1])}` — {', '.join(sorted(pages))}")
lines.append("\n## By deck\n")
for deck in sorted(by_deck):
    lines.append(f"### {deck}")
    for fn, pg in sorted(by_deck[deck]):
        lines.append(f"- `{fn}` → {', '.join(pg)}")
    lines.append("")
open(os.path.join(ROOT, "docs", "plan", "IMAGE-USAGE.md"), "w", encoding="utf-8").write("\n".join(lines))
print(f"_image_usage written to {wrote} grammars; {len(usage)} images, {len(dupes)} cross-page repeats; docs/plan/IMAGE-USAGE.md updated")

if __name__ == "__main__":
    pass
