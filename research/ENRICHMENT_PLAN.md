# Tarot Enrichment Plan (Jun 8 2026)

Goal: fold the `research/` library into the grammars, and add the genuinely-ancestral decks —
with **honest ancestral-status labels**. Plan only; nothing executed yet.

## Phase 0 — Reconcile (avoid double-up) ⚠️
`scripts/add_history_sources.py` already injected **generic** source blocks into each deck's
description. The `research/*.mdx` files have **richer, deck-specific** content (At a glance →
Origin → Provenance → *Game or divination?* → *The fear question* → *Counter-voices* → Sources).
**Action:** replace the generic blocks with research-derived text per deck — don't stack both.

## Phase 1 — Enrich EXISTING grammars from research (no new decks, no image fetching)
A script maps each `research/<n>-<slug>.mdx` → `tarot/<slug>/grammar.json` and writes:
- **description** ← "At a glance" + provenance + "Game or divination?" + Sources.
- a per-deck **Historiography** section ← "The fear question" (your Inquisition point, per deck) + "Counter-voices."

Mappable now: visconti-sforza(01), cary-yale(02), charles-vi(03), mantegna(04), minchiate(06),
tarocchino(07), marseille-conver(08), court-de-gebelin(09), etteilla I/II/III(10a/b/c),
oswald-wirth(11), golden-dawn(12), besancon(15).

**Meta:** supersede my generic "ON ORIGINS" with the real `00-overview` + `00b-origins` +
`00c-islamic-and-chinese` + `14-genealogy` — and rebuild the "Divination Question" essay node
from the library's own framing.

## Phase 2 — Add the ancestry layer (candidate decks) — honest dividing line
| Deck | Status | Source (PD) |
|---|---|---|
| **Mamluk** (Topkapı, c.1500) | **DIRECT ANCESTOR** — the deck Europe copied | Wikimedia Commons |
| **Cary Sheet** (Beinecke, c.1500) | **Ancestral** — earliest Marseille pattern | Beinecke, Yale |
| **Rosenwald Sheet** (NGA, ~1500) | **Ancestral** — early Florentine A-order | NGA open access |
| **Noblet** (Paris, c.1650) + Viéville + anon. Parisian | **Ancestral** — oldest surviving TdM | BnF Gallica (ark:) |
| **Ganjifa** (Persian/Mughal) | **COUSIN — label clearly**, not a parent | LACMA open access, PICRYL |
| Met Visconti (Death/Love/Hanged Man) | **Supplement** to existing Visconti | The Met open access |
| Mitelli Tarocchino (1660s) | **Supplement** to `07-tarocchino-bologna` | Wikimedia Commons |

Also already in `research/` but maybe not as grammars yet: **Sola Busca (05)**, **Tarocco
Siciliano (16)**, **RWS (13)** — decide whether each becomes its own grammar.

## Phase 3 — Images
Fetch PD images from clean sources (Wikimedia, Gallica `ark:`, NGA, LACMA, Beinecke) → R2 via the
existing `rehost-*` pattern. Record exact license + source per image (some are PD, some "open
access — verify").

## Phase 4 — Genealogy + meta
Add the new nodes to `tree-of-tarot` + the all-decks meta, carrying **ancestral-status** as
metadata (`direct-ancestor` / `ancestral` / `cousin` / `supplement`) so the viewer can show a
"By Ancestry" lens — making the **China → Islam (Mamluk) → Europe** story visible.

## Recommended sequence
1. **Phase 0 + 1** first — highest value, zero image-fetching, low risk (text from research → grammars + meta).
2. **Phase 2 candidate-ancestors catalogue** (a `candidate-ancestors.mdx` in house style: provenance + fetch URL + license + ancestral status).
3. **Phase 3 image fetch** for a first set (Mamluk + Rosenwald + Noblet) → R2, verify renders.
4. **Phase 4** wire into genealogy/meta.

## Open decisions for the maintainer
- New grammars to actually build: Mamluk (yes), Ganjifa (cousin-labelled), Cary Sheet, Rosenwald, Noblet — all? a subset?
- Sola Busca / Tarocco Siciliano / RWS — promote the research files to grammars?
- Catalogue-first (Phase 2) or image-fetch-first?
