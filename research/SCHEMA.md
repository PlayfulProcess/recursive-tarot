# Research Catalogue — Schema & Conventions

This is the **contract** for every research dossier in `research/`. It is written to be
read by **historians** (so they can scan, cite, and correct) and by **AI agents** (so a
machine pass can fill, link, and verify entries). One fact lives in **one place**; the
grammars (`tarot/<slug>/grammar.json`) and the generated meta are *projections* of what is
established here.

> **The discipline that makes this work:** a dossier never asserts a load-bearing claim
> without a citation key from `bibliography.bib`, and never invents a citation. If a claim
> can't be sourced, it is marked `confidence: low` and phrased as a question, not a fact.

---

## 1. The three catalogues

| Folder | One file per… | Frontmatter `type` | Drives |
|---|---|---|---|
| `research/decks/` | deck / pack / sheet | `deck` | `tarot/<slug>/grammar.json` description + per-deck sections |
| `research/people/` | person or institution | `person` \| `institution` | `tarot/people-of-tarot/grammar.json` |
| `research/cards/` | one file per deck, **card-by-card** | `cards` | per-card `sections` in that deck's grammar |

Legacy top-level `research/NN-slug.mdx` files are the **first-pass deck dossiers**. They are
being migrated/extended into `research/decks/<slug>.md` in this schema. Until a deck is
migrated, its `NN-*.mdx` remains canonical for that deck.

---

## 2. Frontmatter (YAML) — required on every file

```yaml
---
id: "etteilla-i-livre-de-thot"      # stable slug; matches the grammar slug for decks
type: "deck"                         # deck | person | institution | cards
title: "Etteilla I — Livre de Thot"
status: "verified"                   # stub | drafting | verified | needs-review
confidence: "high"                   # high | medium | low  (of the dossier as a whole)
last_updated: "2026-06-13"
maintainer_note: "AI-assisted; for maintainer + Tarot History Forum review."
# deck-only:
era: "1788–1791 (Paris)"
function: "divination"               # game | divination | esoteric | instructional | origin-myth | ancestor | cousin
order: "occult"                      # A | B | C | occult | n/a
ancestry: "descendant"               # direct-ancestor | ancestral | cousin | descendant | n/a
people: ["etteilla"]                 # ids from research/people/ (the makers/patrons/scholars)
derives_from: ["court-de-gebelin-tarot", "tarot-de-marseille-conver"]  # parent deck ids
# person/institution-only:
role_group: "occultists"             # REQUIRED for the generator: makers | patrons | occultists | scholars | institutions
summary: "One-line who-and-why for the grammar leaf."
lifespan: "1738–1791"
roles: ["cartomancer", "deck designer", "occult entrepreneur"]
made: ["etteilla-i-livre-de-thot", "etteilla-ii-egyptian"]   # deck ids this person MADE
studied: []                          # deck ids a scholar STUDIED (use instead of `made` for scholars)
features_cards: []                   # optional "deck-slug:card-id" links to specific cards
# cards-only:
deck: "etteilla-i-livre-de-thot"     # which deck this card-file documents
card_count: 78
---
```

`status` ladder: **stub** (frontmatter + TODO) → **drafting** (prose, partial sources) →
**verified** (every load-bearing claim has a citation key, web-checked) → **needs-review**
(a flagged contradiction awaiting a human).

---

## 3. Citations — the dual-recognized system

- All sources live in **`research/bibliography.bib`** (BibTeX — recognized by academics and
  trivially parsed by tools).
- In prose, cite with **`[@citekey]`** (Pandoc/academic style; also unambiguous for AI),
  optionally with a locator: `[@dummett1980, p. 67]`.
- **Quote** the source where it carries weight. Format:

  > "the four suits of the Mamluk pack are cups, coins, swords and polo-sticks" [@mayer1971]

- A new source you actually consulted on the web is added to `bibliography.bib` as a
  `@misc{web_<short>, … url=…, urldate=2026-06-13}` entry **before** you cite it. Never cite
  a key that isn't in the .bib.
- **Confidence tags inline** where a single claim is shakier than the dossier overall:
  `(confidence: low — only one secondary source; primary not seen)`.

### What counts as a source (in rough order of weight)
1. **Primary objects / archives**: the cards themselves, BnF Gallica `ark:`, Beinecke,
   Topkapı, Morgan, NGA scans.
2. **The Dummett spine**: Dummett 1980; Decker–Depaulis–Dummett 1996; Dummett–McLeod 2004.
3. **Standard references**: Kaplan, *Encyclopedia of Tarot* I–IV; Mayer 1971 (Mamluk);
   Moakley 1966 (Visconti).
4. **Reputable web scholarship**: trionfi.com / Andy Pollett, The World of Playing Cards
   (wopc.co.uk), Tarot Heritage, l'Association Le Tarot, museum catalogue pages.
5. **Weak / tertiary**: general Wikipedia, blogs — usable for orientation, but a
   load-bearing claim needs something from 1–4, or it's `confidence: low`.

---

## 4. Section structure

### Deck dossier (`research/decks/<slug>.md`)
Carry forward the proven structure from `research/README.mdx`:
1. **At a glance** — one honest paragraph.
2. **Origin & dating** — what the documents show.
3. **Provenance & evidence** — surviving objects, archives, who holds them.
4. **Structure** — suits, ranks, trump order, card count; what is standard vs. peculiar.
5. **Game or divination?** — the repo's core distinction, per deck.
6. **What changed from its parent** — the diff against `derives_from`, and *why*.
7. **The fear question** — would makers/users have hidden it, read against law & Church.
8. **Counter-voices** — the "suppressed history" claim, stated fairly, then weighed.
9. **People** — who made / paid for / later studied it (link `people/` ids).
10. **Open questions / corrections owed.**
11. **Sources** — the `[@…]` keys used.

### Person / institution dossier (`research/people/<slug>.md`)
1. **At a glance** — who, when, why they matter to tarot in one paragraph.
2. **Life & context** — dates, place, trade, the milieu.
3. **What they made / did** — the decks, books, or institutions, each linked.
4. **The claim vs. the record** — myths attached to them (e.g. Gébelin's Egypt, Gringonneur
   as the Charles VI painter) stated and weighed.
5. **Connections** — teachers, rivals, successors, patrons (link other `people/` ids).
6. **How they appear in this collection** — which decks/cards should feature them.
7. **Open questions / corrections owed.**
8. **Sources.**

### Cards dossier (`research/cards/<deck-slug>.md`)
A header (deck, count, source-of-imagery), then **one block per card** in deck order:

```md
## <number> — <Card name> (<original-language name>)
- **Depicts:** … [@key]
- **Means (upright / reversed):** … (only where the tradition has meanings; a game deck has none natively)
- **Changed from parent:** what this card does that its `derives_from` predecessor did not, and *why* [@key]
- **Sources:** [@key], [@key]
- **Confidence:** high | medium | low
```

The **"Changed from parent"** line is the heart of the per-card pass — e.g. for Etteilla,
how each card departs from the Marseille trump it replaces; for RWS, how Smith's scene
departs from the pip it illustrates. Omit the line where there is no parent (root decks).

---

## 5. Linking research → grammars (the integration contract)

When a dossier reaches `status: verified`, its facts flow into the grammars:
- **Deck dossier** → the grammar `description`, a `Historiography` section, and per-deck
  `metadata` (`order`, `function`, `ancestry`, `derives_from`, `people`).
- **Cards dossier** → each card's `sections` (esp. a `What changed` / `Sources` section) and
  `keywords`.
- **People dossier** → an item in `tarot/people-of-tarot/grammar.json`, with `made` →
  the deck ids and (where specific) the card ids it should feature in.

The grammar carries the **rendered, readable** text and a `_research` pointer back to the
dossier file; the dossier carries the **evidence and quotes**. The generated meta copies
from the grammars only — it is never a source of truth and is always rebuildable by
`scripts/build_meta_grammar.py`.
