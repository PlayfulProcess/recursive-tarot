#!/usr/bin/env python3
"""Build the Jacques Viéville (Paris, c.1650) tarot grammar from the BnF/Gallica
public-domain scan (ark btv1b10510963k). 78 card faces downloaded to images/
(odd canvases = faces, even = card backs). Trumps carry printed Roman numerals
(read from the scans); suits and courts identified by symbol/figure; pip ranks
follow the BnF folio order and are offered for correction (house style)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://tarot.recursive.eco/tarot/vieville-tarot/images"

def img(n): return f"{BASE}/c{n:02d}.jpg"

# --- 21 numbered trumps (c01..c21), read from the printed numerals on the scans
TRUMPS = [
    ("I", "Le Bateleur", "The mountebank at his table — the deck opens, as the Parisian pattern does, with the conjuror."),
    ("II", "La Papesse", "A seated, winged figure with the papal tiara — the Viéville's idiosyncratic Popess."),
    ("III", "L'Impératrice", "Enthroned with the eagle shield and a cross-staff — the Empress."),
    ("IIII", "L'Empereur", "The crowned Emperor."),
    ("V", "Le Pape", "The Pope / Hierophant."),
    ("VI", "L'Amoureux", "The Lovers, under the radiant cupid."),
    ("VII", "Le Chariot", "The Chariot."),
    ("VIII", "La Justice", "Trump VIII — named by its numeral (Justice in the Western order)."),
    ("VIIII", "L'Ermite", "The Hermit with his lantern."),
    ("X", "La Roue de Fortune", "The Wheel of Fortune."),
    ("XI", "La Force", "Trump XI — Strength."),
    ("XII", "Le Pendu", "The Hanged Man."),
    ("XIII", "La Mort", "Death — the scything skeleton (the card itself is unnamed, as usual)."),
    ("XIIII", "Tempérance", "Temperance, pouring between two vessels."),
    ("XV", "Le Diable", "The Devil."),
    ("XVI", "La Maison-Dieu", "The Tower / House of God, struck and falling."),
    ("XVII", "L'Étoile", "The Star."),
    ("XVIII", "La Lune", "The Moon."),
    ("XVIIII", "Le Soleil", "The Sun, with figures beneath."),
    ("XX", "Le Jugement", "The Judgement — the angel and the rising dead."),
    ("XXI", "Le Monde", "The World."),
]

# --- 56 suit cards (c22..c77), four suits of 14 in BnF folio order: courts then
# pips. Order of suits as photographed: Swords, Coins, Batons, Cups.
SUITS = [
    ("epees", "Épées", "Swords"),
    ("deniers", "Deniers", "Coins"),
    ("batons", "Bâtons", "Batons"),
    ("coupes", "Coupes", "Cups"),
]
RANKS = ["Roi", "Reine", "Cavalier", "Valet", "Dix", "Neuf", "Huit", "Sept",
         "Six", "Cinq", "Quatre", "Trois", "Deux", "As"]

items = []
trump_ids = []
for i, (num, name, about) in enumerate(TRUMPS):
    cid = f"trump-{i+1:02d}"
    items.append({"id": cid, "name": f"{num} · {name}", "level": 1, "category": "trump",
                  "image_url": img(i+1), "metadata": {"number": num, "arcana": "major"},
                  "sections": {"About": about}})
    trump_ids.append(cid)

suit_group_ids = []
c = 22
for skey, sfr, sen in SUITS:
    sids = []
    for r in RANKS:
        cid = f"{skey}-{c}"
        items.append({"id": cid, "name": f"{r} de {sfr}", "level": 1, "category": "suit-card",
                      "image_url": img(c), "metadata": {"suit": sen, "arcana": "minor"},
                      "sections": {"About": f"{r} of {sen}, from the Viéville pack (BnF folio order)."}})
        sids.append(cid); c += 1
    gid = f"suit-{skey}"
    items.append({"id": gid, "name": f"{sfr} · {sen}", "level": 3, "category": "axis",
                  "render_as": "pill-group", "composite_of": sids, "image_url": img(c-14),
                  "sections": {"What it is": f"The {sfr} ({sen}) suit — King, Queen, Cavalier, Valet and ten pips."}})
    suit_group_ids.append(gid)

# Le Mat (the Fool) — the unnumbered card, last in the scan (c78)
items.append({"id": "trump-mat", "name": "Le Mat (The Fool)", "level": 1, "category": "trump",
              "image_url": img(78), "metadata": {"arcana": "major"},
              "sections": {"About": "The unnumbered Fool, the wandering figure — placed last in the BnF scan."}})
trump_ids.append("trump-mat")

# emergence: the 22 atouts
items.append({"id": "axis-atouts", "name": "Les Atouts (22 Trumps)", "level": 3, "category": "axis",
              "render_as": "pill-group", "composite_of": trump_ids, "image_url": img(1),
              "sections": {"What it is": "The 22 trumps (atouts) of the Viéville — 21 numbered cards plus the unnumbered Mat."}})

grammar = {
    "name": "Jacques Viéville Tarot — Paris, c. 1650 (BnF)",
    "slug": "vieville-tarot",
    "description": "# Jacques Viéville Tarot (Paris, c. 1650)\n\n## At a glance\n\nOne of the **three oldest surviving named Tarots de Marseille-family decks**, printed in Paris around 1650 by the *maître-cartier* **Jacques Viéville** — a near-contemporary of **Jean Noblet** (whose deck this library also holds). The single known copy is at the **Bibliothèque nationale de France** and is on **Gallica** (ark:/12148/btv1b10510963k), fully public domain. Its 78 woodcut cards are shown here from the BnF scan, at high resolution.\n\n## Why it matters — the road not taken\n\nViéville's pack is the great **outlier** of the early Parisian tarots. Where Noblet sits squarely in the **C-order (Marseille)** line that became standard, Viéville's trump imagery leans toward the **Eastern/Belgian** branch: its figures face the other way, several trumps (the Popess, the Sun, the World, the Star) carry markedly different designs, and the pack is a key witness to the family that later surfaces in the **Vandenborre / 'Tarot Flamand'** decks rather than the Marseille mainstream. It shows that c. 1650 Paris held *two* competing tarot patterns at once.\n\n## What you're looking at\n\n- **22 atouts (trumps):** 21 carry printed Roman numerals (read directly from the scans here) plus the unnumbered **Mat** (Fool).\n- **56 suit cards:** four Italian suits — **Épées** (Swords), **Deniers** (Coins), **Bâtons** (Batons), **Coupes** (Cups) — each with King, Queen, Cavalier, Valet and ten pips.\n- The even-numbered canvases of the BnF scan are the cards' **patterned backs**; only the faces are shown.\n\n## Honesty notes\n\nThe trumps are identified by their **printed numerals** (the Viéville's imagery is idiosyncratic, so the name follows the deck's own number rather than the scene). Suit cards are shown in **BnF folio order**; courts are identified by figure, and **pip ranks are assigned by position and may warrant correction** — corrections welcome, as everywhere in this library.\n\n## Game, not divination\n\nLike Noblet, this is a **playing-and-trick-taking** pack from a century before tarot was attached to fortune-telling; no cartomantic meaning is native to it.\n\n## Sources\n\nBnF / Gallica (ark:/12148/btv1b10510963k), public domain; Thierry Depaulis on the early Parisian cartiers; Dummett, *The Game of Tarot*.\n\n---\n*AI-assisted first-pass: card faces from the BnF scan, trumps read from their numerals, suits/courts identified by symbol. Corrections welcome.*",
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "license": "CC-BY-SA-4.0",
    "default_view": "cards",
    "metadata": {"year": 1650, "tradition": "Tarot de Marseille family (Parisian)", "branch": "marseille", "order": "Eastern/Belgian-leaning"},
    "_source": "BnF / Gallica ark:/12148/btv1b10510963k — public domain.",
    "items": items,
}

out = os.path.join(ROOT, "tarot", "vieville-tarot")
json.dump(grammar, open(os.path.join(out, "grammar.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("wrote vieville grammar | items:", len(items), "| cards:", 78)
