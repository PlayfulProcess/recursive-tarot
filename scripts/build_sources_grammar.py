# -*- coding: utf-8 -*-
"""Build tarot/sources/grammar.json and docs/rights/IMAGE-FLAGS.md (Oct 20 2026).

Source of truth: research/sources/image-sources.json (hand-edited): one entry per place
where pictures of a deck can be found, with its holder, quality and rights as published.
This script writes:

  - tarot/sources/grammar.json: one node per source, plus three kinds of selection
    (category "selection"): one per deck, one per holder, one per rights class.
    A node sits in every selection that applies. Image only where the source entry has
    one (set only when the source's own statement says public domain, CC0 or CC BY).
  - docs/rights/IMAGE-FLAGS.md: every card image shown today whose source is
    non-commercial-only, a scan of a modern reproduction, unlicensed, weakly sourced or
    unrecorded, with the free alternative per card where one is known. Read from
    docs/rights/image-ledger.json (scripts/audit_image_rights.py).
  - one line in each deck's description linking to its selection (DECK_LINK below);
    Book T's line lives in scripts/build_book_t_deck.py, which owns that description.

Generated: never hand-edit the outputs.  --check exits 1 if a re-run would change them.
"""
import json, os, sys, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "research", "sources", "image-sources.json")
OUT = os.path.join(ROOT, "tarot", "sources", "grammar.json")
LEDGER = os.path.join(ROOT, "docs", "rights", "image-ledger.json")
FLAGS = os.path.join(ROOT, "docs", "rights", "IMAGE-FLAGS.md")
SITE = "https://tarot.recursive.eco"
VIEW = SITE + "/viewers/cards.html?src=../tarot/sources/grammar.json&item="
DECK_LINK_MARK = "**Where the pictures come from:**"
SKIP_DECK_LINK = {"book-t"}   # build_book_t_deck.py writes Book T's description

CLASS_ORDER = ["free", "open-licence", "non-commercial", "permission", "unclear", "in-copyright"]


def deck_names():
    out = {}
    for slug in os.listdir(os.path.join(ROOT, "tarot")):
        p = os.path.join(ROOT, "tarot", slug, "grammar.json")
        if os.path.exists(p) and slug != "sources":
            g = json.load(open(p, encoding="utf-8"))
            out[slug] = ((g.get("metadata") or {}).get("common_name") or g.get("name") or slug)
    return out


def build(data, names):
    classes, holders = data["rights_classes"], data["holders"]
    nodes = []
    for i, s in enumerate(data["sources"]):
        deck_links = ", ".join(
            f"[{names.get(d, d)}]({SITE}/viewers/cards.html?src=../tarot/{d}/grammar.json)"
            for d in s["decks"])
        node = {
            "id": s["id"],
            "name": s["title"],
            "category": "source",
            "sort_order": i,
            "keywords": ["sources", s["holder"], s["rights_class"]] + s["decks"],
            "metadata": {
                "decks": s["decks"],
                "holder": s["holder"],
                "holder_name": s["holder_name"],
                "rights_class": s["rights_class"],
                "rights_label": classes[s["rights_class"]],
                "url": s["url"],
                "checked": data["checked"],
            },
            "sections": {
                "Property rights": s["property_rights"],
                "Holder": s["holder_name"],
                "What it holds": s["holds"],
                "Quality": s["quality"],
                "Rights as published": s["rights_published"],
                "Link": f"[{s['url']}]({s['url']})",
                "Decks here": deck_links,
            },
        }
        if s.get("image"):
            node["image_url"] = s["image"]
            node["metadata"]["image_credit"] = s.get("image_credit", "")
        nodes.append(node)

    def sel(sid, name, slug, parts, about, kind, extra=None):
        m = {"slug": slug, "selection_kind": kind}
        m.update(extra or {})
        return {"id": sid, "name": name, "category": "selection", "parts": parts,
                "sections": {"About": about}, "metadata": m}

    sels = []
    by_deck = collections.OrderedDict()
    for s in data["sources"]:
        for d in s["decks"]:
            by_deck.setdefault(d, []).append(s["id"])
    for d, parts in by_deck.items():
        nm = names.get(d, d)
        sels.append(sel(
            f"sel-deck-{d}", f"Deck: {nm}", f"deck-{d}", parts,
            f"Where pictures of **{nm}** can be found, who holds them, how sharp they are, and "
            f"what their rights allow. [Open the deck]({SITE}/viewers/cards.html?src=../tarot/{d}/grammar.json).",
            "deck", {"deck_slug": d}))
    by_holder = collections.OrderedDict((h, []) for h in holders)
    for s in data["sources"]:
        by_holder[s["holder"]].append(s["id"])
    for h, parts in by_holder.items():
        if parts:
            sels.append(sel(f"sel-holder-{h}", f"Holder: {holders[h]}", f"holder-{h}", parts,
                            f"Every source held or published by **{holders[h]}**.", "holder"))
    for c in CLASS_ORDER:
        parts = [s["id"] for s in data["sources"] if s["rights_class"] == c]
        if parts:
            sels.append(sel(f"sel-rights-{c}", f"Rights: {classes[c]}", f"rights-{c}", parts,
                            f"Sources whose rights, as their holders publish them, come to: **{classes[c]}**.",
                            "rights"))
    for j, n in enumerate(sels):
        n["sort_order"] = len(nodes) + j

    desc = f"""# Sources: where the deck pictures live, and their rights

For each deck on this site: the museums, libraries and sites that hold pictures of it, how sharp
those pictures are, and **what their rights allow**, in the holder's own words where they could be
read. Each source also says plainly who holds the rights and what we may and may not do.

**Three ways in.** Selections by **deck**, by **holder** (Yale, the BnF, the Morgan, Commons…) and
by **rights** (free for any use · open licence · non-commercial only · permission needed · unclear ·
in copyright). A source can sit in several.

**Links only.** This grammar copies no pictures. A source shows an image only where its own
statement says public domain, CC0 or CC BY.

**Not legal advice.** A Commons "public domain" tag is the uploader's claim about the work, not a
grant from whoever made the scan. Checked {data['checked']}.

Every card image shown today that is non-commercial-only, a scan of a modern reproduction, or of
unclear origin is listed, card by card, with a free alternative where one is known, in
[IMAGE-FLAGS.md](https://github.com/PlayfulProcess/recursive-tarot/blob/main/docs/rights/IMAGE-FLAGS.md).

*Built by `scripts/build_sources_grammar.py` from `research/sources/image-sources.json`.*
"""
    return {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [{"name": "PlayfulProcess", "url": "https://recursive.eco",
                             "date": data["checked"],
                             "note": "Image sources for the decks: holders, quality and rights (text only; the pictures belong to their holders)"}],
        },
        "_generated": True,
        "name": "Sources: Where the Deck Pictures Live",
        "slug": "sources",
        "grammar_type": "custom",
        "provenance": "reference",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://recursive.eco",
        "default_view": "thumbnails",
        "default_preview": "thumbnails",
        "is_published": True,
        "tags": ["sources", "rights", "images", "museums", "reference"],
        "description": desc,
        "metadata": {"common_name": "Image Sources", "category": "reference"},
        "nodes": nodes + sels,
    }


# ---------------------------------------------------------------- image flags
ALT = {
    "charles-vi-tarot": "The 1844 hand-coloured lithographs (Société des bibliophiles français; Liège DONum copy, filed public domain) for all 17; Chatto 1848 engravings for Justice and the Moon. Both are copies, not photographs. No free photograph of the cards found.",
    "minchiate-florence-tarot": "None found free for commercial use; fine here with the Gallica credit.",
    "tarocco-siciliano": "Photographs of a current pack under CC BY-SA (Countakeshi, Riccardo ricceri, Wikimedia Commons). A new photograph of each card would replace the 1966 Modiano scans.",
    "oswald-wirth-tarot": "None found free for commercial use; fine here with the Gallica credit.",
    "papus-tarot-des-bohemiens": "None found free for commercial use; fine here with the Gallica credit.",
    "noblet-tarot": "None: the BnF holds the only pack.",
    "vieville-tarot": "None: the BnF holds the only pack.",
    "paris-anonymous-tarot": "None: the BnF holds the only pack.",
    "tarot-de-marseille-conver": "Trumps and aces: the Tarot World Project photographs (CC BY-SA 4.0). Pips and courts: none found free for commercial use.",
    "sola-busca-tarot": "No free set of the coloured Brera cards found. Uncoloured impressions: British Museum (CC BY-NC-SA, 4 cards), Albertina (Commons).",
    "tarocchino-bologna": "Commons scans of a Bolognese pack (to find), or John McLeod's permission.",
    "tarot-de-besancon": "A museum copy of a 1JJ pack (none found yet).",
    "belgian-tarot": "A museum copy of a Vandenborre pack (none found yet).",
    "mamluk-deck": "A credited photograph of the Topkapı pack (none found yet).",
    "etteilla-i-livre-de-thot": "Find the printing first; the BIU Santé 1791 dictionary (Etalab open licence) is a text source, not the cards.",
    "etteilla-ii-egyptian": "Find the printing first.",
    "etteilla-iii-oracle-des-dames": "Find the printing first.",
    "rider-waite-smith-pictorial-key": "The 1909 first printing on Commons (Roses & Lilies, public domain, 812-860 px); for 10 cards, the Yale copy on Commons (about 1,830 px).",
    "golden-dawn-book-t-tarot": "As Rider-Waite-Smith: the 1909 Roses & Lilies scans on Commons; the Yale copy for 10 cards.",
    "este-tarot": "Same source, sharper: Yale's IIIF full size (3,256 x 5,640 px) is free for any use under Yale's open-access policy.",
}

def flag_of(r):
    """Return (flag, note) for a ledger row, or None when the image needs no flag."""
    deck, credit, cls = r["deck"], (r.get("credit") or ""), r["class"]
    if r["provenance"] != "record":
        return None
    if "Dal Negro" in credit:
        return ("modern reproduction", "Scanned from the Dal Negro facsimile, not the card.")
    if "David Madore" in credit:
        return ("modern reproduction", "Scanned by David Madore from the AGMüller facsimile (per the Commons credit).")
    if "bnf-scan" in cls or deck in ("vieville-tarot", "paris-anonymous-tarot"):
        return ("non-commercial only", "BnF scan: free here with the Gallica credit, a licence for any sale.")
    if deck == "este-tarot" and cls != "holder-open-access":  # Yale full size since Oct 19 2026
        return ("lower resolution than the holder's", "Yale's file is about three times sharper; rights are fine.")
    if deck == "sola-busca-tarot":
        return ("unclear scan source", "From waitesmith.org at 474 px; which exemplar is not stated.")
    if deck == "tarocchino-bologna" and "pagat" in (r.get("image_url") or "") + credit:
        return ("no licence", "Copied from pagat.com (© John McLeod), no image licence.")
    if deck == "tarocco-siciliano" and "fujutu" not in (r.get("image_url") or "").lower():
        return ("weak provenance", "A 1966 Modiano pack, filed on Commons as PD-old-70 from steve-p.org; a pack printed that recently is a weak case.")
    if deck in ("tarot-de-besancon", "belgian-tarot", "mamluk-deck"):
        return ("weak provenance", "Public-domain work; the scan's origin is thin (" + (credit[:60] or "no credit") + ").")
    if cls == "unrecorded":
        return ("unrecorded", "Nothing in the repo says which scan or printing this is.")
    if deck in ("rider-waite-smith-pictorial-key", "golden-dawn-book-t-tarot"):
        return ("printing unrecorded", "Commons credit muzendo.jp; which early printing is not recorded.")
    return None


def visconti_alt(r, card_meta):
    museum = (card_meta.get("museum") or "")
    if "Cary-Yale" in (r.get("credit") or "") or "Beinecke" in (r.get("credit") or ""):
        return "Yale IIIF (record 33220491), free for any use."
    if "Morgan" in museum:
        return ("The Morgan's own image if the card is among its 35 (MS M.630; non-commercial, unaltered, "
                "captioned); the Carrara's cards have no online images found.")
    return "None found online."


def flags_doc():
    if not os.path.exists(LEDGER):
        return None
    led = json.load(open(LEDGER, encoding="utf-8"))
    rows = led["rows"]
    meta = {}
    for slug in {r["deck"] for r in rows}:
        p = os.path.join(ROOT, "tarot", slug, "grammar.json")
        if os.path.exists(p):
            for n in json.load(open(p, encoding="utf-8")).get("nodes", []):
                meta[(slug, n.get("id"))] = n.get("metadata") or {}
    by_deck = collections.OrderedDict()
    for r in rows:
        f = flag_of(r)
        if f:
            by_deck.setdefault(r["deck"], []).append((r, f))
    out = [
        "# Image flags: pictures shown today that are not free for any use",
        "",
        "Generated by `scripts/build_sources_grammar.py` from `docs/rights/image-ledger.json` (the",
        f"ledger of {led.get('checked')}). Re-run after `scripts/audit_image_rights.py`. Never hand-edit.",
        "",
        "Flags: **non-commercial only** (BnF/Gallica scans: fine on this free site with the credit, a",
        "licence for anything sold) · **modern reproduction** (a scan of a printed facsimile, not the",
        "card) · **no licence** · **weak provenance** · **unrecorded** · **printing unrecorded** ·",
        "**lower resolution than the holder's**. Living artists' decks and PlayfulProcess's own are left out.",
        "The sources behind each alternative are in the `sources` grammar",
        f"({SITE}/viewers/cards.html?src=../tarot/sources/grammar.json).",
        "",
        "## Summary",
        "",
        "| Deck | Flagged images | Flag(s) | Free alternative |",
        "|---|---|---|---|",
    ]
    for d, lst in by_deck.items():
        fl = sorted({f[0] for _, f in lst})
        alt = ALT.get(d, "Per card below." if d == "visconti-sforza-tarot" else "None found.")
        out.append(f"| `{d}` | {len(lst)} | {', '.join(fl)} | {alt} |")
    for d, lst in by_deck.items():
        out += ["", f"## `{d}` ({len(lst)})", "", "| Card | Flag | Note | Free alternative |", "|---|---|---|---|"]
        for r, (fl, note) in lst:
            if d == "visconti-sforza-tarot":
                alt = visconti_alt(r, meta.get((d, r["item"]), {}))
            else:
                alt = ALT.get(d, "None found.")
            name = (r.get("name") or r["item"]).replace("|", "/")
            out.append(f"| {name} (`{r['item']}`) | {fl} | {note} | {alt} |")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- deck description links
def deck_line(slug, name):
    return (f"{DECK_LINK_MARK} who holds this deck's pictures, how sharp they are and what their "
            f"rights allow: [Sources: {name}]({VIEW}sel-deck-{slug}).")


def link_decks(slugs, names, write):
    changed = []
    for slug in slugs:
        if slug in SKIP_DECK_LINK:
            continue
        p = os.path.join(ROOT, "tarot", slug, "grammar.json")
        raw = open(p, encoding="utf-8").read()
        g = json.loads(raw)
        desc = g.get("description") or ""
        line = deck_line(slug, names.get(slug, slug))
        lines = [l for l in desc.rstrip("\n").split("\n") if not l.startswith(DECK_LINK_MARK)]
        new = "\n".join(lines).rstrip("\n") + "\n\n" + line + "\n"
        if new != desc:
            changed.append(slug)
            if write:
                g["description"] = new
                orig = json.loads(raw)
                tail = "\n" if raw.endswith("\n") else ""
                indent = next((i for i in (2, None, 1, 4)
                               if json.dumps(orig, ensure_ascii=False, indent=i) + tail == raw), 2)
                with open(p, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(json.dumps(g, ensure_ascii=False, indent=indent) + tail)
    return changed


def main():
    check = "--check" in sys.argv
    data = json.load(open(DATA, encoding="utf-8"))
    names = deck_names()
    for s in data["sources"]:
        assert s["rights_class"] in data["rights_classes"], s["id"]
        assert s["holder"] in data["holders"], s["id"]
        for d in s["decks"]:
            assert d in names, f"{s['id']}: unknown deck {d}"
    g = build(data, names)
    text = json.dumps(g, ensure_ascii=False, indent=2) + "\n"
    flags = flags_doc()
    decks = list(dict.fromkeys(d for s in data["sources"] for d in s["decks"]))
    stale = []
    if not os.path.exists(OUT) or open(OUT, encoding="utf-8").read() != text:
        stale.append(OUT)
    if flags is not None and (not os.path.exists(FLAGS) or open(FLAGS, encoding="utf-8").read() != flags):
        stale.append(FLAGS)
    stale += link_decks(decks, names, write=not check)
    if check:
        if stale:
            print("sources grammar is stale; run python scripts/build_sources_grammar.py:", stale)
            sys.exit(1)
        print("sources grammar up to date")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    if flags is not None:
        open(FLAGS, "w", encoding="utf-8", newline="\n").write(flags)
    n_src = len(data["sources"])
    print(f"wrote {OUT}: {n_src} sources, {len(g['nodes']) - n_src} selections; "
          f"flags doc; deck links updated: {len(stale) - 2 if len(stale) >= 2 else 0}")


if __name__ == "__main__":
    main()
