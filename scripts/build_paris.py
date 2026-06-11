#!/usr/bin/env python3
"""Build the Anonymous Parisian Tarot de Marseille grammar from the BnF/Gallica
public-domain scan (ark btv1b105109624) — the third of the three early Parisian
tarots cited in our Noblet grammar (with Noblet and Viéville). 78 card faces
(odd canvases = faces). Trumps are NAMED on the cards (read from the scans); suits
in BnF folio order: Deniers, Coupes, Bâtons, Épées."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://tarot.recursive.eco/tarot/paris-anonymous-tarot/images"
def img(n): return f"{BASE}/c{n:02d}.jpg"

TRUMPS = [
    ("I", "Le Bateleur"), ("II", "La Papesse"), ("III", "L'Impératrice"),
    ("IIII", "L'Empereur"), ("V", "Le Pape"), ("VI", "L'Amoureux"),
    ("VII", "Le Chariot"), ("VIII", "La Justice"), ("VIIII", "L'Hermite"),
    ("X", "La Roue de Fortune"), ("XI", "La Force"), ("XII", "Le Pendu"),
    ("XIII", "La Mort"), ("XIIII", "Tempérance"), ("XV", "Le Diable"),
    ("XVI", "La Maison-Dieu"), ("XVII", "L'Étoile"), ("XVIII", "La Lune"),
    ("XVIIII", "Le Soleil"), ("XX", "Le Jugement"), ("XXI", "Le Monde"),
]
SUITS = [("deniers", "Deniers", "Coins"), ("coupes", "Coupes", "Cups"),
         ("batons", "Bâtons", "Batons"), ("epees", "Épées", "Swords")]
RANKS = ["As", "Deux", "Trois", "Quatre", "Cinq", "Six", "Sept", "Huit", "Neuf",
         "Dix", "Valet", "Cavalier", "Reine", "Roi"]

items = []
trump_ids = []
for i, (num, name) in enumerate(TRUMPS):
    cid = f"trump-{i+1:02d}"
    items.append({"id": cid, "name": f"{num} · {name}", "level": 1, "category": "trump",
                  "image_url": img(i+1), "metadata": {"number": num, "arcana": "major"},
                  "sections": {"About": f"{name} (atout {num}) — the name is printed on the card."}})
    trump_ids.append(cid)

c = 22
suit_group_ids = []
for skey, sfr, sen in SUITS:
    sids = []
    for r in RANKS:
        cid = f"{skey}-{c}"
        items.append({"id": cid, "name": f"{r} de {sfr}", "level": 1, "category": "suit-card",
                      "image_url": img(c), "metadata": {"suit": sen, "arcana": "minor"},
                      "sections": {"About": f"{r} of {sen} (BnF folio order)."}})
        sids.append(cid); c += 1
    gid = f"suit-{skey}"
    items.append({"id": gid, "name": f"{sfr} · {sen}", "level": 3, "category": "axis",
                  "render_as": "pill-group", "composite_of": sids, "image_url": img(c-14),
                  "sections": {"What it is": f"The {sfr} ({sen}) suit — ten pips plus Valet, Cavalier, Reine and Roi."}})
    suit_group_ids.append(gid)

items.append({"id": "trump-mat", "name": "Le Mat (The Fool)", "level": 1, "category": "trump",
              "image_url": img(78), "metadata": {"arcana": "major"},
              "sections": {"About": "The unnumbered Fool, last in the BnF scan."}})
trump_ids.append("trump-mat")
items.append({"id": "axis-atouts", "name": "Les Atouts (22 Trumps)", "level": 3, "category": "axis",
              "render_as": "pill-group", "composite_of": trump_ids, "image_url": img(1),
              "sections": {"What it is": "The 22 named trumps — 21 numbered atouts plus the Mat."}})

grammar = {
    "name": "Anonymous Parisian Tarot — BnF (Tarot de Marseille, 17th–18th c.)",
    "slug": "paris-anonymous-tarot",
    "description": "# Anonymous Parisian Tarot de Marseille (BnF)\n\n## At a glance\n\nThe **third of the three early Parisian tarots** held at the Bibliothèque nationale de France and freely on **Gallica** (ark:/12148/btv1b105109624) — the unsigned companion to our **Jean Noblet** (c. 1650) and **Jacques Viéville** decks. Unlike the outlier Viéville, this pack sits squarely in the **C-order (Marseille)** mainstream: a fully **named** French Tarot de Marseille, every trump captioned on the card in period spelling (LE BATELEVR, LA IVSTICE, ATREMPANCE…). 78 woodcut cards, hand-coloured, shown here from the BnF scan.\n\n## Why it matters\n\nWith Noblet and Viéville, it shows that the **named, numbered Marseille pattern was already standardised in Paris a century before Nicolas Conver's 1760 Marseille** — the printed standard our library also holds. It is a clean witness to the C-order line in its Parisian form.\n\n## What you're looking at\n\n- **22 atouts (trumps):** 21 numbered + the unnumbered **Mat**, with the card names read directly from the scans.\n- **56 suit cards:** **Deniers** (Coins), **Coupes** (Cups), **Bâtons** (Batons), **Épées** (Swords), each with ten pips and four courts (Valet, Cavalier, Reine, Roi).\n\n## Honesty notes\n\nDating and maker are **uncertain** — the deck is anonymous; '17th–18th c.' follows the BnF's cautious placement and the company it keeps in the Noblet/Viéville group. The trumps are named from their printed captions; suit cards are shown in **BnF folio order** and pip ranks are assigned by position (corrections welcome).\n\n## Game, not divination\n\nA playing pack; the cartomantic readings attached to the Marseille came later, with the 18th-century occult revival.\n\n## Sources\n\nBnF / Gallica (ark:/12148/btv1b105109624), public domain; Thierry Depaulis on the Parisian cartiers; Dummett, *The Game of Tarot*.\n\n---\n*AI-assisted first-pass: faces from the BnF scan, trumps from their printed captions, suits by symbol. Corrections welcome.*",
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "license": "CC-BY-SA-4.0",
    "default_view": "cards",
    "metadata": {"year": 1700, "tradition": "Tarot de Marseille (Parisian)", "branch": "marseille", "order": "C-order"},
    "_source": "BnF / Gallica ark:/12148/btv1b105109624 — public domain.",
    "items": items,
}
out = os.path.join(ROOT, "tarot", "paris-anonymous-tarot")
json.dump(grammar, open(os.path.join(out, "grammar.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("wrote paris grammar | items:", len(items))
