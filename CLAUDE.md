# CLAUDE.md — recursive-tarot

## The spine: voices & the one intention

1. **The creed is the spine.** The project turns on `viewers/voices.json` → `shared_intention`: *"Read to know yourself, not to be told your fate… relate to the card; never obey it."* The history, the why-it-works lenses, the two wings, the courses, and the Caster all exist to serve that one creed.
2. **Gate, not fate.** Any voice, course, or feature that touches divination or esoterica must stay autonomy-preserving — *a prompt, not a prophecy.* Never reintroduce "the card reveals / determines your fate," even when rendering an occult tradition (Golden Dawn, Etteilla, Lévi) faithfully. Render the tradition; correct the fatalism.
3. **Consolidate, don't multiply.** Prefer turning a new idea into something we already have — a **voice** (`voices.json`), a **deck**, a **source** (`books-of-tarot` / `people-of-tarot`), or a **journey** (the four doors: Player · Historian · Practitioner · Contributor) — over a parallel structure. The Golden Dawn is the worked example: it became a *voice* + a short pathworking course, not a separate sub-site.
4. **Voice vs Source (the two wings).** A tradition's *reading stance* is the **Living/practice** layer (voices, courses, the Golden Dawn Path); its *people, books, and decks* are the **Record/evidence** layer (`docs/DESIGN-two-wings-provenance.md`). Keep them in their own places and cross-link with the one pill pattern below — never let a practice claim masquerade as a historical one.

## Core architecture

- Grammar files live in `tarot/<slug>/grammar.json`. Never hand-edit `tarot/all-decks-many-lenses/grammar.json` or `tarot/people-of-tarot/grammar.json` — both are generated.
- Always run `python scripts/check_all.py` before committing. Must end "all checks passed" with `dangling=0`.
- After any grammar edit: `python scripts/build_meta_grammar.py` (rebuilds meta + people). Then check_all again.
- CI lands `chore: rebuild meta-grammar [skip ci]` commits on `dev`; always `git pull --rebase origin dev` before pushing.

## The one cross-link pattern (DO NOT INVENT ANOTHER)

The viewer renders a pill link automatically when an item has:
```json
{
  "metadata": {
    "source_deck": "<slug>",
    "source_item_id": "<item-id>",
    "deck": "<human label>"
  }
}
```
The pill reads: **"Open in [deck] →"**. This is the ONLY cross-grammar navigation mechanism. Use it for everything — meta → deck, deck → people, deck → related grammar. Never add a new link field.

Examples:
- Meta grammar item → source deck: `source_deck: "visconti-sforza-tarot"`, `source_item_id: "major-00-il-matto"`, `deck: "Visconti-Sforza"`
- Individual deck item → people: `source_deck: "people-of-tarot"`, `source_item_id: "person-bonifacio-bembo"`, `deck: "People & Institutions"`

The pill suppresses itself if the current page URL already contains `/<slug>/`, so it never shows a circular link.

## People grammar

- Source of truth: `research/people/*.md` dossiers. Edit those, then run `python scripts/build_people_grammar.py`.
- Do NOT hand-edit `tarot/people-of-tarot/grammar.json`.
- To link a deck item to a person: add `source_deck / source_item_id / deck` to that item's `metadata` (same pattern as above).

## Sections used across grammars

| Section | Meaning |
|---------|---------|
| `Scene` | Narrative description of what is literally depicted |
| `Symbol` | Semiotic note: what the visual elements mean in the tradition they come from |
| `Research note` | Sourced historical claims with `[@citation]` keys |
| `Figure` | Named figure on the card (courts, named trumps) |
| `Tradition Note` | Contextual note placing the card in its historical programme |

## Image pattern

All deck images are on R2 at:
`https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/<deck-folder>/<filename>`

To write Scene/Symbol sections: download images from R2 to a temp dir, use Read tool vision to view each, write descriptions, delete temp dir. Sola Busca minors done 2026-06-13 this way.

**Thumbnails are always resized, never cropped.** Card images must show the whole card — use
`object-fit:contain` (letterboxed on a neutral background), never `object-fit:cover`. A clipped
card hides the very iconography the thumbnail exists to show. Applies to every card thumbnail:
play tiles, course strips/detail, game cards, deck covers, viewers.

## Scripts cheat-sheet

| Script | What it does |
|--------|-------------|
| `scripts/build_meta_grammar.py` | Rebuild all-decks-many-lenses + people grammars |
| `scripts/build_people_grammar.py` | Rebuild people-of-tarot from research/people/*.md |
| `scripts/enrich_cards_from_research.py` | Add Research notes from research/cards/*.md (idempotent) |
| `scripts/refresh_collection.py` | Sync _collection.json from grammars |
| `scripts/check_all.py` | Pre-commit gate |
