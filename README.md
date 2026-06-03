# The recursive.eco Tarot Collection

A public-domain, scholarship-grounded set of **tarot grammars** — structured JSON
datasets, one per historical deck — plus a **genealogical meta-grammar** that maps how
the decks descend from one another. Everything here is **CC-BY-SA-4.0** and built from
**public-domain** sources (Wikimedia Commons, the BnF/Gallica, etc.).

If you are a tarot historian or collector and found this from the Tarot History Forum:
**welcome, and please correct us.** See *Contributing* below.

> **This repo is the canonical home for the tarot grammars.** Each deck lives at
> `tarot/<slug>/grammar.json` and declares this repo as its source via `_github_url`.
> The platform ([recursive.eco](https://recursive.eco)) indexes these files; edits and
> pull requests here are the authoritative source. (See *Relationship to
> recursive.eco-schemas* at the bottom.)

---

## What this is (and is not)

- **Is:** an open, machine-readable map of tarot's documentary history — each deck's
  cards with iconography, history, correspondences (where the tradition has them), and
  honest tradition notes. It renders at [recursive.eco](https://recursive.eco) as cards,
  readings, and a genealogy tree.
- **Is not:** a divination product dressed up as history. Where a deck was a **game**
  deck (Visconti, Marseille, Minchiate, Charles VI…), every card says so — divination is
  a later (post-1780s) overlay, not the deck's origin.

### Accuracy principles we try to hold
- **Public domain only.** No copyrighted decks reproduced (e.g. **Thoth, 1944** is
  referenced, never copied).
- **No forced equivalences.** Etteilla renumbered Death to 17; the Golden Dawn swapped
  Strength↔Justice; Minchiate's zodiac/element cards have *no* standard equivalent; Sola
  Busca's classical figures only *loosely* map. We mark these honestly rather than
  flattening them.
- **Game vs. divination is labelled**, per card.
- **The Tarot History Forum** (and Dummett's scholarship) is consulted for **facts**;
  no forum text is reproduced (it's author-copyrighted).
- We will be wrong about things. Corrections are the point.

---

## The decks (built so far)

| Grammar | Deck | Cards | Tradition / order |
|---|---|---|---|
| `tarot/visconti-sforza-tarot` | Visconti-Sforza | 85 | oldest near-complete (Milan, c.1451) |
| `tarot/cary-yale-visconti-tarot` | Cary-Yale (Visconti di Modrone) | 73 | six courts + theological virtues (c.1442) |
| `tarot/charles-vi-tarot` | "Charles VI" (Gringonneur) | 18 | Ferrarese / B-order (c.1450–80) |
| `tarot/minchiate-florence-tarot` | Minchiate | 106 | Florentine 97-card / A-order |
| `tarot/tarot-de-marseille-conver` | Tarot de Marseille (Conver 1760) | 83 | printed standard / C-order |
| `tarot/oswald-wirth-tarot` | Oswald Wirth | 23 | Continental esoteric (1889/1926) |
| `tarot/golden-dawn-book-t-tarot` | Golden Dawn (Book T) | 84 | full GD correspondences, RWS imagery |
| `tarot/etteilla-i-livre-de-thot` | Etteilla I — Livre de Thot | 78 | first divination deck (1788) |
| `tarot/etteilla-ii-egyptian` | Etteilla II | 78 | 1838 edition |
| `tarot/etteilla-iii-oracle-des-dames` | Etteilla III — Oracle des Dames | 78 | 1865 edition |
| `tarot/tree-of-tarot` | **The Tree of Tarot** (meta-grammar) | 32 | the genealogy itself |

Also migrated into `tarot/` this round: Tarocchino di Bologna, Mantegna "Tarocchi" (to
explain it is *not* a tarot), Court de Gébelin's plates, Besançon/Swiss 1JJ, and
Tarocco Siciliano. Also live on the platform (not yet migrated here): a public-domain
Marseille, Rider-Waite-Smith, Sola Busca, and the Bolognese-styled modern "Tarocchino
Arlecchino."

The full historical roadmap (fixes owed, future features, the Supabase build log) lives
in the source repo — see *Relationship to recursive.eco-schemas* below.

---

## The genealogy (how to read the tree)

`tarot/tree-of-tarot/grammar.json` is a meta-grammar whose **items are the decks**,
built on **Michael Dummett's A/B/C trump-order** classification:

```
Italian trionfi (c.1440s)
├─ A-order (Bologna/Florence) ── Tarocchino di Bologna · Minchiate · Tarocco Siciliano
├─ B-order (Ferrara) ─────────── "Charles VI" · d'Este
└─ C-order (Milan/West) ──── Visconti/Cary-Yale ──► Tarot de Marseille ──► occult decks
   (Sola Busca = a sui-generis offshoot)
```

It corrects a common belief: **the Marseille is *not* descended from the Bolognese
Tarocchino** — they are cousins (C- vs A-order), both children of the common root. The
meta-grammar uses the platform's *reference-item* structure (see `GRAMMAR_FORMAT.md` →
"Reference items & meta-grammars") so each leaf can open the full deck, and
`default_preview: "tree"` renders it in the tree-viewer.

---

## How it's built (for contributors)

- **Format:** `GRAMMAR_FORMAT.md` is the contract. Each deck is one
  `tarot/<slug>/grammar.json`; the collection index is `tarot/_collection.json`.
- **Layout:** decks live under `tarot/`, grouped into genealogical branches
  (roots · A/B/C-order · occult · sui-generis · `_meta`) by `_collection.json`.
- **Images:** public-domain, hot-linked from Wikimedia Commons via stable
  `Special:FilePath` URLs (filenames pulled from the Commons API, not guessed).
- **Assembly:** `python scripts/build_tarot_collection.py` (re)builds this repo from the
  source grammars and writes the collection index; `python scripts/stamp_canonical_repo.py`
  stamps each deck's `_github_url` home pointer.
- **Provenance:** the original per-deck generators (`generate_<deck>.py`), build logs,
  and the master history/roadmap docs live in the source repo,
  **recursive.eco-schemas** — see below.

> Transparency: these grammars are **AI-assisted** (drafted with Claude, reviewed by the
> maintainer). That is exactly why outside scholarly review is wanted.

---

## Contributing & corrections

Corrections from historians are the most valuable thing this repo can receive.

- **Spotted an error** (a date, an attribution, a mis-mapped archetype, a bad image)?
  Open a GitHub **issue** or a **pull request** against the relevant
  `tarot/<slug>/grammar.json`. This repo is the canonical source, so a merged PR here
  is what the platform re-indexes.
- **Copyright:** PD sources only; paraphrase + attribute, never copy copyrighted text
  (see `CLAUDE.md` → *Copyright Boundaries*). Forum posts and modern deck art are
  copyrighted — cite, don't reproduce.
- **Attribution:** contributors are credited in each grammar's `_grammar_commons.attribution`.

### Sharing this work (plan)
- **Post to the Tarot History Forum** as a human, with this repo link, an upfront note
  that it's AI-assisted, and an explicit invitation to correct — *not* by scraping the
  forum (it blocks bots and its posts belong to their authors).

---

## Relationship to recursive.eco-schemas

This repo (`recursive-tarot`) is one **topic collection** in a multi-repo model — the
**canonical, curated home for tarot**. The broader [`recursive.eco-schemas`](https://github.com/PlayfulProcess/recursive.eco-schemas)
repo is the **catch-all** for every other grammar family (I Ching, sequences, philosophy,
…) and the place where these decks were originally *built* (the `generate_<deck>.py`
generators, build logs, and the master history/roadmap docs live there).

| | `recursive-tarot` (here) | `recursive.eco-schemas` |
|---|---|---|
| Role | Canonical home for tarot | Default catch-all + build provenance |
| Layout | `tarot/<slug>/grammar.json` | `grammars/<slug>/grammar.json` |
| For tarot decks | **Authoritative** (edit/PR here) | Frozen archive (being retired) |
| Holds | Decks + collection index + viewers | Generators, build logs, roadmap, all non-tarot |

How they fit the platform: recursive.eco reads grammars from **Supabase** (a fast,
queryable read-index); a grammar's `_github_url` records which repo is its authoritative
source. For tarot that URL points here. This is the **GitHub-as-database** model — see
`recursive-eco/docs/GITHUB_AS_DATABASE.md` for the full architecture (the index sync,
the publish-destination choice, and the "add your own public repo" advanced option).

**This file is the entry point for the tarot collection.**
