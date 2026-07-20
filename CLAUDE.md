# CLAUDE.md — recursive-tarot

## The spine: voices & the one intention

1. **The creed is the spine.** The project turns on `viewers/voices.json` → `shared_intention`: *"Read to know yourself, not to surrender yourself… relate to the card; never obey it."* The history, the why-it-works lenses, the two wings, the courses, and the Caster all exist to serve that one creed.
2. **Gate, not fate — and let each voice speak as itself.** The `shared_intention` creed is the container shown above all voices; under it, present each tradition *faithfully, in its own terms* — a voice's `how` should sound like the Golden Dawn (or Kant, or Jung), not like us editorializing about it. Render any *disagreement* with a tradition in the long form (its **course**), never in the short **intention**. The one hard floor everywhere: stay autonomy-preserving — never state a card as prediction or as something to obey. Honor the tradition's authentic practice (the Golden Dawn's pathworking genuinely *is* gate-not-fate); keep the critique in the course. **Name a school, not a living person:** voices drawn from a living teacher are titled by their tradition (DBT, Non-Dual Tantra, Post-Activism, Hospicing Modernity) and say "inspired by" — only dead, eponymous figures (Kant, Jung) carry their own name. `voices.json` → `shared_intention.interpretation_note` holds the standing disclaimer that every voice is a faithful-but-still-interpretation, never the person's words or endorsement.
3. **Consolidate, don't multiply.** Prefer turning a new idea into something we already have — a **voice** (`voices.json`), a **deck**, a **source** (`books-of-tarot` / `people-of-tarot`), or a **journey** (the four doors: Player · Historian · Practitioner · Contributor) — over a parallel structure. The Golden Dawn is the worked example: it became a *voice* + a short pathworking course, not a separate sub-site.
4. **Voice vs Source (the two wings).** A tradition's *reading stance* is the **Living/practice** layer (voices, courses, the Golden Dawn Path); its *people, books, and decks* are the **Record/evidence** layer (`docs/DESIGN-two-wings-provenance.md`). Keep them in their own places and cross-link with the one pill pattern below — never let a practice claim masquerade as a historical one.

## Theme & colour — ONE source (`theme.css`)

- **All colour lives in `theme.css`** (a single `:root` of tokens), linked by every page and viewer.
  **Never redeclare colour tokens locally** and never add a `@media(prefers-color-scheme:dark)` block —
  that's what caused the recurring light-on-light bugs (each page had its own divergent palette).
- **Light only.** Backgrounds are always light, text always dark enough to read on them. No dark stages
  (video players / game tables are light too). Token names are unified but legacy aliases resolve:
  `--panel`=`--surface`, `--muted`=`--mut`, `--accent`=`--gold`, `--ink-strong`/`--fg`/`--text`=`--ink`.
- To change a colour, edit `theme.css` once. To re-apply the consolidation if a new file drifts:
  `python scripts/apply_theme.py` (links theme.css, strips local colour tokens + dark blocks).
- Bump `style.css?v=N` when style.css changes; `theme.css?v=N` likewise.

## Core architecture

- Grammar files live in `tarot/<slug>/grammar.json`. Never hand-edit `tarot/all-decks-many-lenses/grammar.json` or `tarot/people-of-tarot/grammar.json` — both are generated.
- Always run `python scripts/check_all.py` before committing. Must end "all checks passed" with `dangling=0`.
- After any grammar edit: `python scripts/build_meta_grammar.py` (rebuilds meta + people). Then check_all again.
- **`main` is the live branch** (confirmed Jul 15 2026 from `.github/workflows/build-meta.yml`: Pages deploys on push to `main`; dev was merged back and retired — the leftover `origin/dev` ref is stale, don't work from it). CI lands `chore: rebuild meta-grammar [skip ci]` commits on the deployed branch; always `git pull --rebase` your branch before pushing.

## recursive.eco integration (the GitHub boundary)

This repo is the open half; **recursive.eco** is the private app. They share the grammar JSON format
and pass grammars across GitHub. Full reference: **[docs/RECURSIVE-ECO-INTEGRATION.md](docs/RECURSIVE-ECO-INTEGRATION.md)**. The essentials:
- The app **reads from `main`** (`raw.githubusercontent.com/PlayfulProcess/recursive-tarot/main/tarot/<slug>/grammar.json`) and **writes back to `main`** via `app/recursive-eco` sync PRs ("Resolve all drifts"). `main` is also the live static site (see above); work on a feature branch and merge to `main` to publish, reconciling (never discarding) the App's write-backs that land there.
- **Slug ↔ app UUID:** `tarot/_eco_ids.json`.
- Sync **must not drop repo-only fields** (`_grammar_commons` licence — on *all* grammars — `_image_usage`, `lineages`, cross-link pills, Research notes) and **must skip `_generated: true` grammars** (meta, people, contribute, the course). The doc has the full ownership model + the merge-onto-repo write-back fix.

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

## Image usage across the site (render the most of the library)

Card images appear in site chrome (Home / Play / Historian / Contribute / games). Show the deck's
**range** — keep images **unique within a page**, and avoid reusing the same image across sibling
pages (especially **Home ↔ About ↔ Play**). After editing any page's imagery, run
`python scripts/audit_image_usage.py`: it writes a top-level `_image_usage` onto each deck's
grammar.json (the deck's images + the pages they feed) and regenerates `docs/plan/IMAGE-USAGE.md`, which
flags every cross-page repeat. Keep it up to date — it's how we spread unique cards and render the
most of the library. (Prefer the Star / courts / Empress over yet another Visconti World.)

## Course images — one home, one convention

Course figures/screenshots live in **`pages/courses/images/`** — the single canonical location.
In an MDX course, author them as `images/<name>.ext` (e.g. `![caption](images/01-library.png)`);
the course-viewer rewrites `images/` → `courses/images/` at render time. Don't scatter course
images elsewhere (the old `course/img/` folder was consolidated here Jun 23 2026). Card art still
comes from R2 (see the Image pattern above); this folder is only for course-authored figures.

## Scripts cheat-sheet

| Script | What it does |
|--------|-------------|
| `scripts/build_meta_grammar.py` | Rebuild all-decks-many-lenses + people grammars |
| `scripts/build_people_grammar.py` | Rebuild people-of-tarot from research/people/*.md |
| `scripts/enrich_cards_from_research.py` | Add Research notes from research/cards/*.md (idempotent) |
| `scripts/refresh_collection.py` | Sync _collection.json from grammars |
| `scripts/check_all.py` | Pre-commit gate |
