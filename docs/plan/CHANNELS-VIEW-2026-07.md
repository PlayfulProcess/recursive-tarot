# Channels view — every grammar as a channel card (tarot · astro · iching)

Goal: one page per public repo that shows **all of that repo's grammars as channels** — a
lightweight, static echo of recursive.eco's channels UI in plain HTML + JS (no build step,
no framework) — where every card links out to **the actual channel in recursive.eco**.

## 1. What already exists (tarot repo — nothing new to invent)

The two data files the page needs are already maintained:

- **`tarot/_collection.json`** — 36 grammars with exactly the card fields: `slug`, `name`,
  `common_name`, `items` (count), `cover_image_url`, `blurb`, `year_label`, `provenance`
  (record/practice), `category`, `branch` (roots/marseille/occult/…). Kept fresh by
  `scripts/refresh_collection.py` (idempotent; grammars are the source of truth).
- **`tarot/_eco_ids.json`** — slug → recursive.eco UUID, plus `_public_now` (which decks
  actually resolve for visitors). Link patterns are documented in the file itself:
  open/read `https://flow.recursive.eco/?deckId=<uuid>`, and the app's channel page
  `https://flow.recursive.eco/g/<uuid>` (the pattern already used by Ways to Contribute).

Site conventions the page must reuse rather than duplicate: `theme.css` tokens only (no
local colours), `<site-header>`/`site-footer.js`, the **purple spiral "Open in
recursive.eco ↗"** affordance (one affordance, learned once — per Ways to Contribute), and
**thumbnails resized never cropped** (`object-fit:contain`).

## 2. The page — `pages/channels.html` (tarot first)

One static file, ~250 lines, modelled on how the other viewers are built:

- **Fetch at runtime:** `../tarot/_collection.json` + `../tarot/_eco_ids.json`. No build
  step; when a grammar is added and `refresh_collection.py` runs, the page is current.
- **Card** (CSS grid, responsive, letterboxed cover): cover image · name (`common_name`
  big, full `name` as the subtitle) · year label · item count · provenance pill
  (Record/Practice — the two wings) · one-line blurb.
- **Card actions, two only:**
  - **Read here** → the site's own viewer (`viewers/cards.html?deck=<slug>` — same
    resolution path the card browser already uses via `_eco_ids.json`).
  - **Open channel in recursive.eco ↗** (purple spiral) → `flow.recursive.eco/g/<uuid>`,
    rendered **only when the slug is in `_public_now`** — a link that 404s for visitors is
    worse than no link. Non-public grammars show a quiet "not yet published" note instead.
- **Grouping:** by the collection's existing `branch` curation (Roots · Marseille ·
  Occult · Games · Sources · Meta), which is the repo's own taxonomy — not a new one.
- **Nav:** one entry in `site-header.js` (Views → Channels). No other structure — this is
  a *view over existing grammars*, per the consolidate-don't-multiply rule.

## 3. Porting to recursive-astrology and recursive-iching

The page is written once with a tiny config header, so the port is copy + 5 lines:

```js
const CHANNELS_CONFIG = {
  dataRoot: 'tarot',            // astro/iching: 'grammars'
  collection: '../tarot/_collection.json',
  ecoIds: '../tarot/_eco_ids.json',
  readerUrl: (slug) => `../viewers/cards.html?deck=${slug}`,
};
```

Two unknowns to verify in each sibling repo before porting (they aren't in this session's
scope — add them via the session's repo picker when we do the work):

1. **Do they have a `_collection.json` and `_eco_ids.json`?** If not, port
   `refresh_collection.py` alongside (it's ~80 lines and derives everything from the
   grammar files) and seed an `_eco_ids.json` from the recursive.eco MCP
   (`list_grammars`, matching by name — exactly how tarot's was built on 2026-06-20/24).
2. **Their reader URL** (astro's course-viewer is grammar-driven, so the "Read here"
   target differs per repo — the config line above absorbs that).

Precedent for cross-repo pattern sharing: `assistant.js` (tarot is the pattern source,
astro mirrors it by hand, each file's header says so). `channels.html` follows the same
convention — no shared package, a header comment naming the canonical copy.

## 4. Honest constraints

- **Public-only links.** `_public_now` is a hand-maintained snapshot; a grammar published
  after the snapshot won't get its channel link until the list is updated. Acceptable —
  and the MCP (`list_grammars`) can refresh it in one call whenever we notice drift.
- **No live data from the app.** The page is static by design; item counts and covers are
  as fresh as the last `refresh_collection.py` run. That script should be mentioned in
  CLAUDE.md's scripts cheat-sheet as part of the add-a-deck routine (it already is).
- **Imagery audit.** Cover images are per-deck and unique by construction, but run
  `python scripts/audit_image_usage.py` after the page lands, since it adds a new page
  that renders deck imagery.

## 5. Order of work

1. **Tarot** (this repo): build `pages/channels.html`, register in the header Views menu,
   verify at 390×844, `check_all.py`, ship. ~1 session.
2. **Astro**: add repo to session, verify the two unknowns, port page + (if needed)
   `refresh_collection.py`, seed `_eco_ids.json` via MCP. ~1 session.
3. **I Ching**: same as astro. ~1 session.
4. **Optional follow-up**: a "channels" strip on each Home page reusing the same cards —
   only if the standalone page proves itself first.
