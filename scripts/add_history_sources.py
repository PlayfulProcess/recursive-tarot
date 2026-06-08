# -*- coding: utf-8 -*-
"""Append a 'PROVENANCE & SOURCES' block to each deck's description, with primary
sources / historian references and the hedged game-vs-divination framing. Idempotent
(skips a deck whose description already carries the marker). Run from repo root:
    python scripts/add_history_sources.py
Then rebuild the meta:  python scripts/build_meta_grammar.py
"""
import json, os, glob

HERE = os.path.dirname(__file__)
TAROT = os.path.abspath(os.path.join(HERE, "..", "tarot"))
MARKER = "PROVENANCE & SOURCES"

SHARED = ("General scholarship: Michael Dummett, *The Game of Tarot* (1980); Decker, Depaulis & "
          "Dummett, *A Wicked Pack of Cards* (1996); Stuart Kaplan, *The Encyclopedia of Tarot*; "
          "Andrea Vitali, *Le Tarot* (letarot.it); Lothar Teikemeier, trionfi.com.")

# Hedged line for game-era decks; occult-era decks were purpose-built for divination.
HEDGE_GAME = ("Documented as a trick-taking game; there is no surviving evidence of divinatory use "
              "before the 18th century (informal cartomancy can't be wholly ruled out — see the meta's "
              "essay 'The Divination Question').")
HEDGE_DIV = ("A deck of the divinatory turn: cartomantic/esoteric tarot is first attested in the 1780s "
             "(Court de Gébelin, then Etteilla) — not a survival of an older secret tradition (see the "
             "meta's essay 'The Divination Question').")

DECKS = {
 "visconti-sforza-tarot": dict(hedge=HEDGE_GAME, prov=(
   "Hand-painted c. 1451 for the Visconti–Sforza court of Milan; the surviving cards are split across "
   "three collections — the Morgan Library & Museum (New York), the Accademia Carrara (Bergamo) and the "
   "Beinecke Rare Book & Manuscript Library (Yale). The 'Bonifacio Bembo' attribution is traditional but "
   "debated (some cards given to the 'Master of the Pierpont-Morgan-Bergamo Tarocchi'); six cards are later "
   "restorations."), src="Primary: the cards at the Morgan Library (themorgan.org) & Beinecke (Yale). Kaplan vol. I."),
 "cary-yale-visconti-tarot": dict(hedge=HEDGE_GAME, prov=(
   "The lavish 'Cary-Yale' Visconti deck, c. 1442, with six-rank courts and the theological virtues — held "
   "at the Beinecke Rare Book & Manuscript Library, Yale (the Cary Collection of Playing Cards)."),
   src="Primary: Beinecke Library, Yale (brbl-dl.library.yale.edu). Kaplan, *Encyclopedia of Tarot*."),
 "charles-vi-tarot": dict(hedge=HEDGE_GAME, prov=(
   "17 hand-painted trump cards at the Bibliothèque nationale de France (Cabinet des Estampes). Long called "
   "the 'Gringonneur'/'Charles VI' deck after a 1392 court payment, but now dated to late-15th-century Ferrara "
   "and unconnected to that payment."), src="Primary: BnF / Gallica (gallica.bnf.fr). Thierry Depaulis on the misattribution."),
 "minchiate-florence-tarot": dict(hedge=HEDGE_GAME, prov=(
   "The 97-card Florentine expansion (40+ trumps adding the zodiac, elements and virtues), 16th–18th c. "
   "Documented as a game across Tuscany."), src="Dummett & McLeod, *A History of Games Played with the Tarot Pack*; Franco Pratesi's archival studies; Vitali (letarot.it)."),
 "tarocchino-bologna": dict(hedge=HEDGE_GAME, prov=(
   "The 62-card Bolognese trick-taking game (pips 2–5 removed), 17th c., with the 'four Papi' signature. The "
   "Bologna tradition is the best-documented continuous tarot-as-game lineage."), src="Andrea Vitali, *Le Tarot* — extensive Bologna essays (letarot.it); Dummett."),
 "tarot-de-marseille-conver": dict(hedge=HEDGE_GAME, prov=(
   "Nicolas Conver's 1760 Marseille woodblock pattern — the canonical 'Tarot de Marseille,' later adopted as "
   "the occult era's reference image. Examples and the trade context are documented at the BnF."), src="Thierry Depaulis, *Tarot, jeu et magie* (BnF exhibition catalogue, 1984); BnF / Gallica."),
 "tarot-de-besancon": dict(hedge=HEDGE_GAME, prov=(
   "The Besançon variant (18th–19th c., eastern France / Switzerland) in which Juno and Jupiter replace the "
   "Papess and Pope. A game pattern of the German-speaking borderlands."), src="Depaulis; Kaplan, *Encyclopedia of Tarot*."),
 "court-de-gebelin-tarot": dict(hedge=HEDGE_DIV, prov=(
   "Where divination is invented: Antoine Court de Gébelin's 1781 plates and essay claiming the cards encode an "
   "ancient Egyptian 'Book of Thoth' — an evidence-free Romantic-era myth (hieroglyphs were not yet deciphered)."),
   src="PRIMARY: Court de Gébelin, *Le Monde Primitif*, vol. VIII (1781) — on Gallica (gallica.bnf.fr). Decker, Depaulis & Dummett, *A Wicked Pack of Cards*."),
 "etteilla-i-livre-de-thot": dict(hedge=HEDGE_DIV, prov=(
   "Among the first decks purpose-built for fortune-telling: Jean-Baptiste Alliette ('Etteilla', 1788–89), who "
   "founded a professional cartomancy practice and an Egyptian-styled system."), src="PRIMARY: Alliette, *Manière de se récréer avec le jeu de cartes nommées tarots* (1783–85). Decker, Depaulis & Dummett, *A Wicked Pack of Cards* (definitive on Etteilla)."),
 "etteilla-ii-egyptian": dict(hedge=HEDGE_DIV, prov=(
   "A later 'Grand Etteilla' edition in the Egyptian style, continuing Alliette's cartomantic system into the 19th c."),
   src="Decker, Depaulis & Dummett, *A Wicked Pack of Cards*; Kaplan, *Encyclopedia of Tarot*."),
 "etteilla-iii-oracle-des-dames": dict(hedge=HEDGE_DIV, prov=(
   "The 'Grand Etteilla III / Oracle des Dames', a 19th-c. commercial continuation of the Etteilla tradition."),
   src="Decker, Depaulis & Dummett, *A Wicked Pack of Cards*; Kaplan."),
 "oswald-wirth-tarot": dict(hedge=HEDGE_DIV, prov=(
   "22 esoteric Major Arcana: Oswald Wirth's 1889 deck (made with Stanislas de Guaita), continuing the "
   "Lévi → Continental occult synthesis."), src="PRIMARY: Oswald Wirth, *Le Tarot des imagiers du Moyen Âge* (1927). Decker & Dummett, *A History of the Occult Tarot*."),
 "golden-dawn-book-t-tarot": dict(hedge=HEDGE_DIV, prov=(
   "'Book T' — the Hermetic Order of the Golden Dawn's tarot instruction (S. L. MacGregor Mathers), with the full "
   "correspondence system (astrology, Hebrew letters, decans) and the Strength↔Justice swap that shaped the RWS."),
   src="PRIMARY: 'Book T' as published in Israel Regardie, *The Golden Dawn*. Decker & Dummett, *A History of the Occult Tarot*."),
}

def block(d):
    return ("\n\n" + MARKER + ":\n" + d["prov"] + "\n\n" + d["hedge"] + "\n\n" + d["src"] + "\n\n" + SHARED)

changed = 0
for slug, d in DECKS.items():
    p = os.path.join(TAROT, slug, "grammar.json")
    if not os.path.exists(p):
        print("  ! missing", slug); continue
    g = json.load(open(p, encoding="utf-8"))
    desc = g.get("description", "") or ""
    if MARKER in desc:
        print("  = already has sources:", slug); continue
    g["description"] = desc.rstrip() + block(d)
    json.dump(g, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    changed += 1
    print("  + sources added:", slug)
print("decks updated:", changed)
