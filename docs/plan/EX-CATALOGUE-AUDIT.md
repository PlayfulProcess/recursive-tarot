# EX-CATALOGUE audit — the "uncatalogued" cards (Jun 24 2026)

The builder flagged that Sola Busca ↔ RWS were "strikingly hard" to pair, and that ~20–33 cards are
uncatalogued. Audit result: **most of the uncatalogued cards are legitimately sui-generis, not a data
bug** — they have no standard 22-major / 4-suit equivalent to pair on. A few are real and fixed.

## What "uncatalogued" means
`scripts/build_meta_grammar.py` classifies each card as **major** (a 0–21 trump by name/number) or
**minor** (has a suit). Anything else is "unclassified" — and the Emergence Explorer can only pair
cards that share a dimension (arcana + major number, or suit + rank).

## The breakdown (233 across all grammars; 33 within the 13 historical tarot decks)
**Legitimately non-standard — should NOT be force-classified (no equivalent exists):**
- **Non-tarot grammars:** 36 Tattvas (47), Ontoject (18), Petit Lenormand (33), Anecdotes/Ys (22),
  Ma Diao money cards (16), Mamluk proto-cards (12), Ganjifa (1). These aren't tarot at all.
- **Sui-generis historical trumps:** Mantegna Tarocchi (40 — the E-series: Estates / Muses / Liberal
  Arts / Virtues / Planets / Spheres), Minchiate's *extra* trumps (23 — the 12 zodiac, 4 elements, 3
  theological virtues, the extra Papi), Cary-Yale's extra theological virtues (3 — Faith/Hope/Charity).
  These genuinely have no RWS counterpart.

**Real bugs — FIXED:**
- **Deck-cover items leaking in as cards** (`category:"overview"`): noblet, cary-sheet, rosenwald,
  ganjifa "The X Tarot/Sheet/Cards" entries. → `build_meta_grammar.py` now skips `category=="overview"`.

**Aliasable (small, optional):** Tarocchino di Bologna's "Love" → Lovers (major 6) and "The Old Man
(Time)" → Hermit (major 9) *could* be aliased so they pair; its four equal "Papa (Moor)" trumps are
genuinely sui-generis (4 equal papi, no distinct standard mapping).

## The real fix for the builder's pain is EX-SECTIONS, not more cataloguing
Sola Busca's cards ARE catalogued (it has suited minors + standard-ish trumps); the Golden-Dawn/RWS
deck is too. So they *can* pair on **arcana + major-number** (trumps) and **suit + rank** (minors).
The difficulty was the **Explorer UI** — knowing *which* dimension to pivot on. That's **EX-SECTIONS**
(a clearer dimension picker + full-text sections), the genuinely high-value next step. Cataloguing the
sui-generis cards further would be inaccurate — they are correctly "their own thing."
