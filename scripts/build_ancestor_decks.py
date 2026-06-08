# -*- coding: utf-8 -*-
"""Generate the ancestor/cousin deck grammars (Cary Sheet, Rosenwald, Noblet, Ganjifa)
as catalogue entries with provenance + honest ancestral status. Run from repo root:
    python scripts/build_ancestor_decks.py
Then rehost images + rebuild meta.
"""
import json, os
HERE = os.path.dirname(__file__); TAROT = os.path.abspath(os.path.join(HERE, "..", "tarot"))
FOOT = "\n\n---\n*AI-assisted first-pass draft, pending review by the maintainer and the Tarot History Forum. Corrections welcome via pending edit.*"
WM = "https://commons.wikimedia.org/wiki/Special:FilePath/"

DECKS = {
 "cary-sheet": dict(
   name="The Cary Sheet — Earliest Marseille Pattern (Milan, c. 1500)",
   ancestry="ancestral", tradition="Milanese woodcut / proto-Marseille (C-order)",
   cover=WM+"Tarot-cary-collection-ita-sheet-3s-c1500..jpg",
   desc=("An uncut sheet of Milanese tarot **woodcuts**, c. 1500 — the **earliest surviving evidence of the "
     "Tarot de Marseille pattern itself**, a full century before Nicolas Conver's 1760 edition. Held at the "
     "**Beinecke Rare Book & Manuscript Library, Yale** (the Cary Collection of Playing Cards). If you want the "
     "missing link between the hand-painted Italian court decks (Visconti-Sforza) and the printed Marseille "
     "standard, this is it: the same trump designs, already woodcut for mass printing.\n\nANCESTRAL STATUS: "
     "**ancestral** to the standard tarot (the printed C-order line), not an ancestor of card-playing itself.\n\n"
     "SOURCES: Beinecke Library, Yale (digitised in their collections); Michael Dummett, *The Game of Tarot* (1980)."),
   items=[("overview","The Cary Sheet","An uncut woodcut sheet showing several trumps in the Marseille arrangement, c. 1500 — the earliest witness to the pattern Conver later standardised.")]),
 "rosenwald-sheet": dict(
   name="The Rosenwald Sheet — Early Florentine (A-order), c. 1500",
   ancestry="ancestral", tradition="Florentine / A-order",
   cover=None,
   desc=("Uncut sheets of an early **Florentine (A-order)** tarot, late 15th–early 16th century, in the **National "
     "Gallery of Art, Washington** (the Lessing J. Rosenwald Collection). The NGA's open-access policy places the "
     "images firmly in the public domain — austere, woodcut, and genuinely early. A southern (A-order) counterpart "
     "to the northern C-order Cary Sheet.\n\nANCESTRAL STATUS: **ancestral** to the standard tarot (the Florentine "
     "A-order line).\n\nIMAGE: National Gallery of Art open access (nga.gov) — to be fetched. SOURCES: NGA "
     "collection; Dummett, *The Game of Tarot* (1980)."),
   items=[("overview","The Rosenwald Sheet","Uncut Florentine tarot sheets, c. 1500, at the NGA (Rosenwald Collection); the early A-order pattern.")]),
 "noblet-tarot": dict(
   name="Jean Noblet Tarot — The Oldest Surviving Tarot de Marseille (Paris, c. 1650)",
   ancestry="ancestral", tradition="Tarot de Marseille (C-order), Paris",
   cover=WM+"Jeu%20de%20tarot%20%C3%A0%20enseignes%20italiennes%20dit%20%22tarot%20Noblet%22%20-%20jeu%20de%20cartes%2C%20estampe%20-%20btv1b105109641%20(012%20of%20154).jpg",
   desc=("The **oldest surviving Tarot de Marseille**, printed in Paris c. 1650 by Jean Noblet — **110 years before "
     "Conver**. The single known copy lives at the **Bibliothèque nationale de France** and is on **Gallica** "
     "(ark:/12148/btv1b105109641), freely usable. Its siblings — the Jacques Viéville deck (ark:/12148/btv1b10510963k) "
     "and an anonymous Parisian tarot (ark:/12148/btv1b105109624) — sit right alongside it: three mid-17th-century "
     "Parisian decks just upstream of the Marseille standard.\n\nANCESTRAL STATUS: **ancestral** to the Marseille "
     "standard (the oldest extant TdM of the C-order line).\n\nSOURCES: BnF / Gallica; Thierry Depaulis."),
   items=[("overview","The Noblet Tarot","Jean Noblet's Paris deck, c. 1650 — the earliest surviving Tarot de Marseille, one known copy at the BnF (Gallica).")]),
 "ganjifa": dict(
   name="Ganjifa — Persian & Mughal Cards (the Cousin, not the Parent)",
   ancestry="cousin", tradition="Islamic-world circular cards (Persia → Mughal India)",
   cover=WM+"Ten%20Playing%20Cards%20(Ganjifa)%20LACMA%20M.2001.210.4.1-.10.jpg",
   desc=("Gorgeous **circular, hand-painted, lacquered** cards whose very name — *ganjifa* / Arabic *kanjifah* — is the "
     "**same word** as the Mamluk game. Persia from the 16th century, then richly developed in **Mughal India** "
     "(Dashavatara and other sets). **A cousin branch, NOT a parent of tarot** — it shows the Islamic-world card "
     "tradition that flourished but did *not* cross into Europe to become the four-suit pack. Filed honestly as "
     "adjacent card art, not ancestry.\n\nANCESTRAL STATUS: **cousin** — beautiful and related, but off the line that "
     "became tarot.\n\nSOURCES: LACMA open access (lacma.org); PICRYL public-domain aggregates; Ashmolean Museum."),
   items=[("overview","Ganjifa Cards","Circular lacquered Persian/Mughal cards — the same word as Mamluk *kanjifah*, a stunning cousin of the European pack, not its ancestor.")]),
}

for slug, d in DECKS.items():
    g = {
      "_grammar_commons": {"schema_version":"1.0","license":"CC-BY-SA-4.0",
        "attribution":[{"name":"PlayfulProcess","note":"AI-assisted first-pass catalogue entry; for review."}]},
      "name": d["name"], "slug": slug, "grammar_type":"custom", "creator_name":"PlayfulProcess",
      "default_view":"tree", "default_preview":"tree",
      "description": d["desc"] + FOOT,
      "metadata": {"ancestry": d["ancestry"], "tradition": d["tradition"]},
      "items": [
        {"id": iid, "name": nm, "level": 1, "category": "overview", "sort_order": i,
         **({"image_url": d["cover"]} if (i==0 and d["cover"]) else {}),
         "sections": {"What it is": txt}}
        for i,(iid,nm,txt) in enumerate(d["items"])
      ],
    }
    if d["cover"]:
        g["cover_image_url"] = d["cover"]
    os.makedirs(os.path.join(TAROT, slug), exist_ok=True)
    json.dump(g, open(os.path.join(TAROT, slug, "grammar.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("  wrote", slug, "| ancestry", d["ancestry"], "| img", bool(d["cover"]))
print("done")
