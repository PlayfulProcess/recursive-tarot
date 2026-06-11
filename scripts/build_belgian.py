#!/usr/bin/env python3
"""Build the Belgian (Vandenborre / 'Tarot Flamand') tarot grammar — 22 Major
Arcana from the public-domain c.1780 set on Wikimedia Commons (the 'Tarot
Belgijski' upload). Images committed to images/ and served via GitHub Pages."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://tarot.recursive.eco/tarot/belgian-tarot/images"
def img(n): return f"{BASE}/t{n:02d}.jpg"

# (A-number, numeral, name, about) — 21 numbered atouts + the unnumbered Fool (A22)
TRUMPS = [
    (1, "I", "Le Bateleur", "The mountebank — the Magician."),
    (2, "II", "Le Capitaine Fracasse", "**A Belgian substitution.** Where the Marseille has La Papesse (the Popess), the Flemish tarot puts a swaggering soldier — the *Capitaine* of farce and commedia dell'arte. Avoiding the female 'pope' sidesteps a figure the Counter-Reformation found scandalous."),
    (3, "III", "L'Impératrice", "The Empress."),
    (4, "IIII", "L'Empereur", "The Emperor."),
    (5, "V", "Bacchus", "**The second Belgian substitution.** In place of Le Pape (the Pope), the wine-god **Bacchus** rides a barrel — a playful, anticlerical swap that, with the Captain, removes both Catholic clergy from the trumps."),
    (6, "VI", "L'Amoureux", "The Lovers."),
    (7, "VII", "Le Chariot", "The Chariot."),
    (8, "VIII", "La Justice", "Justice."),
    (9, "VIIII", "L'Ermite", "The Hermit."),
    (10, "X", "La Roue de Fortune", "The Wheel of Fortune."),
    (11, "XI", "La Force", "Strength."),
    (12, "XII", "Le Pendu", "The Hanged Man."),
    (13, "XIII", "La Mort", "Death (the card itself is unnamed)."),
    (14, "XIIII", "Tempérance", "Temperance."),
    (15, "XV", "Le Diable", "The Devil."),
    (16, "XVI", "La Foudre (La Maison-Dieu)", "The Tower — here a lightning-struck tower, the 'Wrath of God'."),
    (17, "XVII", "L'Étoile", "The Star."),
    (18, "XVIII", "La Lune", "The Moon."),
    (19, "XVIIII", "Le Soleil", "The Sun."),
    (20, "XX", "Le Jugement", "The Judgement."),
    (21, "XXI", "Le Monde", "The World."),
    (22, "", "Le Fou (The Fool)", "The unnumbered Fool / Mat — the wandering jester."),
]

items = []
ids = []
for a, num, name, about in TRUMPS:
    cid = f"trump-{a:02d}"
    title = (f"{num} · {name}" if num else name)
    items.append({"id": cid, "name": title, "level": 1, "category": "trump",
                  "image_url": img(a), "metadata": {"number": num, "arcana": "major"},
                  "sections": {"About": about}})
    ids.append(cid)
items.append({"id": "axis-atouts", "name": "Les Atouts (22 Trumps)", "level": 3, "category": "axis",
              "render_as": "pill-group", "composite_of": ids, "image_url": img(5),
              "sections": {"What it is": "The 22 trumps of the Flemish tarot — the Marseille sequence with the Captain and Bacchus swapped in for the Popess and the Pope."}})

grammar = {
    "name": "Belgian Tarot — Vandenborre / 'Tarot Flamand' (Brussels, c. 1780)",
    "slug": "belgian-tarot",
    "description": "# Belgian Tarot — the Vandenborre / Flemish pattern\n\n## At a glance\n\nThe **Flemish tarot** (*Tarot flamand*), printed in Brussels in the later 18th century by makers such as **F. I. Vandenborre** and Jacques/Jean Galler. It keeps the whole **Tarot de Marseille** structure but is famous for **two substitutions** in the trumps — a quiet response to Catholic sensibilities:\n\n- **II · Le Capitaine** — a braggart soldier replaces **La Papesse** (the Popess).\n- **V · Bacchus** — the wine-god on a barrel replaces **Le Pape** (the Pope).\n\nWith both clergy gone, the deck could be sold without offence in a region pulled between Catholic and Protestant authority. It is the **Eastern/Belgian branch** of the family — the same current the earlier **Viéville** (1650) pointed toward.\n\n## What you're looking at\n\nThe **22 Major Arcana** (atouts) of the Vandenborre pattern, from the public-domain c. 1780 set on Wikimedia Commons. The 56 suit cards are not included here — clean public-domain scans of the Flemish minors have not yet been located at usable resolution; this is therefore a **trumps-only** grammar (like our Oswald Wirth), and the images are **display resolution**, not print.\n\n## Game, not divination\n\nThe Flemish tarot was a **card game**; the cartomantic readings attached to tarot belong to the later French occult tradition, not to this Brussels playing pack.\n\n## Sources\n\nWikimedia Commons 'Tarot Belgijski' set (public domain, c. 1780); Thierry Depaulis on the Belgian/Flemish cartiers; Dummett, *The Game of Tarot*. Trump identifications follow the standard Vandenborre order.\n\n---\n*AI-assisted first-pass: 22 trumps from the PD Commons set, named in the standard order with the two documented Flemish substitutions flagged. Corrections welcome.*",
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "license": "CC-BY-SA-4.0",
    "default_view": "cards",
    "metadata": {"year": 1780, "tradition": "Tarot de Marseille family (Flemish/Belgian)", "branch": "marseille", "order": "Eastern/Belgian"},
    "_source": "Wikimedia Commons 'Tarot Belgijski' (public domain, c. 1780).",
    "items": items,
}

out = os.path.join(ROOT, "tarot", "belgian-tarot")
json.dump(grammar, open(os.path.join(out, "grammar.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("wrote belgian grammar | items:", len(items))
