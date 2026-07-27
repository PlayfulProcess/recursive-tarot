#!/usr/bin/env python3
"""Build the d'Este (Estensi) Tarocchi grammar — the 16 surviving hand-painted
Ferrarese cards, c.1450, from Yale's Beinecke / Cary Collection of Playing Cards
(PLAYING CARDS GEN 966), open-access IIIF. Card identifications are Yale's own
catalogue labels (not guessed). Face images committed to images/ (cNN.jpg, the
odd canvases of the BnF... — here the Yale manifest; even canvases are blank backs)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://tarot.recursive.eco/tarot/este-tarot/images"
def img(n): return f"{BASE}/c{n:02d}.jpg"

# (image file number, Yale label, kind, suit/arcana, note)
CARDS = [
    (1,  "King of Swords",        "court", "Swords",  "Re di Spade."),
    (3,  "Queen of Swords",       "court", "Swords",  "Regina di Spade."),
    (5,  "Cavalier of Swords",    "court", "Swords",  "Cavallo di Spade."),
    (7,  "King of Batons",        "court", "Batons",  "Re di Bastoni."),
    (9,  "Cavalier of Batons",    "court", "Batons",  "Cavallo di Bastoni."),
    (11, "Jack of Batons",        "court", "Batons",  "Fante di Bastoni."),
    (13, "King of Coins",         "court", "Coins",   "Re di Denari."),
    (15, "Queen of Cups",         "court", "Cups",    "Regina di Coppe."),
    (17, "Il Bagatto (The Magician)", "trump", "major", "The mountebank — the first trump (atout I)."),
    (19, "Il Papa (The Pope)",    "trump", "major",   "The Pope / Hierophant."),
    (21, "Temperance",            "trump", "major",   "Temperance, pouring between two vessels."),
    (23, "The Star",              "trump", "major",   "La Stella."),
    (25, "The Moon",              "trump", "major",   "La Luna."),
    (27, "The Sun",               "trump", "major",   "Il Sole."),
    (29, "The World",             "trump", "major",   "Il Mondo."),
    (31, "Il Matto (The Fool)",   "trump", "major",   "The Fool / Mat — the unnumbered wanderer."),
]

items = []
trump_ids, court_ids = [], []
for n, name, kind, suit, note in CARDS:
    cid = f"card-{n:02d}"
    meta = {"arcana": "major"} if kind == "trump" else {"suit": suit, "arcana": "minor"}
    meta["collection"] = "Beinecke Library, Yale (Cary Collection) — PLAYING CARDS GEN 966"
    items.append({"id": cid, "name": name, "level": 1, "category": kind,
                  "image_url": img(n), "metadata": meta, "sections": {"About": note}})
    (trump_ids if kind == "trump" else court_ids).append(cid)

items.append({"id": "axis-trumps", "name": "Surviving Trumps (8)", "level": 3, "category": "axis",
              "render_as": "pill-group", "composite_of": trump_ids, "image_url": img(17),
              "sections": {"What it is": "The eight trumps that survive — Bagatto, Pope, Temperance, Star, Moon, Sun, World and the Fool — out of an original sequence now mostly lost."}})
items.append({"id": "axis-courts", "name": "Surviving Court Cards (8)", "level": 3, "category": "axis",
              "render_as": "pill-group", "composite_of": court_ids, "image_url": img(1),
              "sections": {"What it is": "Eight court cards across the four Italian suits (Swords, Batons, Coins, Cups) — kings, queens, a cavalier and a jack."}})

grammar = {
    "name": "d'Este Tarocchi — The Ferrarese Fragment (c. 1450)",
    "slug": "este-tarot",
    "description": "# d'Este (Estensi) Tarocchi\n\n## At a glance\n\nAmong the **oldest surviving tarot of all** — sixteen hand-painted cards made in **Ferrara around 1450**, in the orbit of the ruling **House of Este**, contemporaries of the Milanese Visconti decks but from the *other* great early tarot court. Only **16 cards survive** (8 trumps + 8 court cards) of what was once a full pack; they are held in the **Cary Collection of Playing Cards at Yale's Beinecke Library** (PLAYING CARDS GEN 966) and shown here from Yale's open-access high-resolution scans.\n\n## Why it matters — the B-order home\n\nFerrara is the home of the **B-order** trump sequence (the Eastern branch in Dummett's A/B/C scheme). Where Milan's Visconti decks head the **C-order** line that became the Tarot de Marseille, the d'Este cards are a rare, luxurious witness to Ferrara's parallel tradition — proof that tarot's invention was not a single Milanese event but a courtly fashion shared across northern Italy in the 1440s–50s.\n\n## What survives\n\n- **8 trumps:** Il Bagatto (the Magician), Il Papa (the Pope), Temperance, the Star, the Moon, the Sun, the World, and Il Matto (the Fool).\n- **8 court cards:** kings, queens, a cavalier and a jack across Swords, Batons, Coins and Cups.\n- Card identifications are **Yale's own catalogue labels** — not guessed from iconography. The cards are unnumbered (as 15th-century hand-painted trumps were).\n\n## Game, not divination\n\nLike the Visconti decks, this is a **luxury court game** object — *trionfi*, three centuries before any divinatory use. No cartomantic meaning is native to it.\n\n## Provenance & evidence\n\nBeinecke Rare Book & Manuscript Library, Yale — Cary Collection (Mary Flagler Cary, 1967); PLAYING CARDS GEN 966; cards 140 × 78 mm; completely digitized, open access (credit: Yale University Library). Dating ('c. 1450') and the Ferrarese/Este attribution follow the standard scholarship but, as with all the early hand-painted decks, remain debated.\n\n## Sources\n\nYale Beinecke / Cary Collection catalogue; Michael Dummett, *The Game of Tarot* (1980); Thierry Depaulis on the Ferrarese decks.\n\n---\n*AI-assisted first-pass: high-resolution faces from Yale's open-access IIIF, named from Yale's catalogue. Corrections welcome.*",
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "license": "CC-BY-SA-4.0",
    "default_view": "cards",
    "metadata": {"year": 1450, "tradition": "Ferrarese hand-painted tarocchi", "branch": "roots", "order": "B"},
    "_source": "Yale Beinecke / Cary Collection of Playing Cards (PLAYING CARDS GEN 966), open access. Credit: Yale University Library.",
    "items": items,
}
out = os.path.join(ROOT, "tarot", "este-tarot")
json.dump(grammar, open(os.path.join(out, "grammar.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("wrote d'Este grammar | items:", len(items))
