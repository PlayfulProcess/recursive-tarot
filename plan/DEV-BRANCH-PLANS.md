# Dev-branch plans (June 12 2026, Fable)

Both repos now have a `dev` branch; **GitHub Pages serves from `dev`** (changed via
API — tarot.recursive.eco now previews dev directly, merge to `main` when stable).
recursive-eco `dev` carries the CORS commit + the sign-in return-popup; Vercel's
`dev.flow.recursive.eco` should be aliased to it for live testing.

These four plans are scoped for Sonnet execution. Each is independent.

---

## P1 — Visual identity: match recursive.eco

Goal: a visitor moving tree↔fruit should feel one family, not two sites.

1. **Logo**: the gold spiral SVG already appears inline in `index.html` (§"What this
   is"). Promote it to the brand: put the spiral (small, ~20px) before the wordmark in
   `site-header.js`'s `.brand`, and replace `favicon.svg` content with the same spiral
   path (it's already a gold spiral — verify they match recursive.eco's actual logo;
   the canonical one is in recursive-eco `apps/landing` — copy the path data from
   there, don't redraw).
2. **Palette**: keep the parchment/gold accents for card content, but shift chrome
   (header, buttons, active pills, links) to recursive.eco purple. recursive.eco
   tokens (from `apps/flow/src/lib/ui/tokens.ts`): primary purple `#9333ea`
   (purple-600), hover purple-700, light wash `rgba(147,51,234,.12)`. Concretely in
   `style.css` + `site-header.js`: `--gold` stays for card/scholarly accents;
   introduce `--brand: #9333ea` and use it for `.tab.active` background (currently
   gold), link color `#b794f6` (already purple — keep), and the Caster pill (already
   violet — keep). Smallest change with biggest effect: **active tab gold → purple**.
3. **Typography**: recursive.eco uses the system stack — already matched. No change.
4. Bump `site-header.js?v=` everywhere (13 HTML files) after edits.
5. Verify on local static server: every page header, active states, favicon.

## P2 — Courses as their own repo (`recursive-courses`)

Goal: one public repo holding all course MDX; both tree and fruits render from raw
GitHub; the Library Assistant can read it to answer course questions.

1. **Repo shape** (mirror recursive-tarot's pattern):
   - `courses/<slug>/course.mdx` (or split per-part MDX) + `_collection.json`
     listing courses with title/description/audience.
   - A thin `pages/course-viewer.html` copied from recursive-tarot's (it already
     renders MDX client-side) + GitHub Pages on, CC-BY-SA. Images stay on R2.
2. **Migration**: move `course/` MDX from recursive-tarot and the course content in
   recursive-eco (`apps/flow` course preview + any landing MDX) into it. Tarot's
   course-viewer then fetches `https://raw.githubusercontent.com/PlayfulProcess/recursive-courses/main/courses/build-a-deck/...`
   (keep a local fallback for offline dev).
3. **Library Assistant access** (recursive-eco side): it already has
   `read_codebase_file`/`search_codebase`; add a `read_course` tool that fetches raw
   GitHub from the courses repo (public, no token) so answers cite actual course
   content. This fixes the observed failure: the assistant couldn't see
   "Build a Tarot Deck with Claude Code".
4. **Don't** build a sync/webhook yet — raw-GitHub fetch is enough (L3 ladder rung
   covers sync later).

## P3 — Explorer → general emergent-pattern system

Goal: make meta-grammar writing unnecessary; previews flexible enough to render
emergent patterns of different kinds; default = render all selections.

Already there: multi-deck loading (`?decks=a,b,c`), field discovery, data-inferred
hierarchy chains (functional dependencies), URL-hash spec, localStorage persistence.

Next increments (in order):
1. **Filters as a drop zone**: today filters are per-chip popovers. Add a third zone
   ("⊸ filters") next to rows/cols; dropping a chip there pins it as a visible
   filter bar (multi-select values rendered as toggleable value-pills). Spec gains
   `pinned: [field,...]`.
2. **Left-bar layout option**: a "◧ sidebar" toggle that renders the pinned filters
   + hierarchy chains in a left column (the recursive.eco Library look) instead of
   the top tray — same spec, alternative chrome.
3. **Default render-all**: with no rows/cols chosen, render all selected grammars'
   items as a flat card wall (currently shows a hint). Selection IS the view.
4. **Keyword dimension**: treat `keywords[]` (array field) as a first-class chip —
   explode arrays into multi-membership when grouping (an item with 3 keywords
   appears in 3 row-groups). This is what makes thematic emergence visible without
   anyone writing a meta grammar.
5. **Save a view**: with L1 auth present, "save this arrangement" → POST the spec
   to recursive.eco (L3 rung; spec is already a serializable artifact).

## P4 — Deck completeness pass (Mamluk first)

Audit finding (Jun 12): `mamluk-deck` has **2 L1s, 5 L2s, 1 L3** — and the L1s are
essays ("How the suits became European", "China → Islam → Europe"), not cards. The
suit L2s "emerge" from nothing. That's backwards: emergence with no base layer.

Fix pattern (apply to any deck failing the ratio check):
1. **L1 = actual cards.** Topkapı Sarayı Mamluk pack scans exist (the deck has ~43
   surviving cards; even 8–12 representative cards as L1 items with images would
   ground the suits). Wikimedia Commons "Mamluk playing cards" category; upload via
   the established R2 flow.
2. **Essays → research or description.** The two historical-essay L1s become either
   `research/*.mdx` files (linked from the grammar description) or sections of the
   grammar's `description`. Not items.
3. **L2 suits keep** — they now genuinely emerge from card L1s.
4. **Ratio check across collection**: `python -c` script (or extend
   `scripts/validate_grammars.py` if it exists) flagging any grammar where
   L2+L3 count ≥ L1 count — those are decks whose "emergences" are really content.

Order: P4 needs image sourcing (desktop session); P1 is pure CSS/JS (any session);
P2 needs a new repo (builder creates or Claude via `gh repo create`); P3 is
incremental fruit-side JS.

---

# P5 — One dimension UI for every viewer (June 12 2026, builder request)

Builder's framing: *"most flexibility with UI to see all patterns with the simplest
grammar structure. Stop changing recursive.eco until the structure settles in tarot;
test I Ching next; only then port."* This repo is the laboratory.

## 5.0 Finding that simplifies everything: `render_as` doesn't exist here

A grep across all 31 grammars + all viewer JS: **no grammar uses `render_as`, and no
viewer reads it.** The fields viewers actually consume: `id`, `name`, `level`,
`image_url`, `keywords[]`, `sections{}`, `composite_of[]`, `metadata{}` (with
`branch`, `when`, `number`, `arcana`, `derives_from` inside). So the "simplest grammar
structure" already won in this repo — the work is to *keep* it that way when porting
back to recursive.eco, not to strip anything here. Rule going forward: **a viewer may
only branch on data shape (has image? has when? has composite_of?), never on a type
or render directive stored in the grammar.** That's the tarot-repo version of
recursive-eco's "grammar types are dead code" rule, and it's why meta-grammar files
like `all-decks-many-lenses` can eventually be replaced by multiselect + inheritance
at load time.

## 5.1 Two viewer families, by rendering unit

The split the builder proposed is real and should be named in the code and the nav:

| Family | Unit rendered | Viewers | Shared dimension source |
|---|---|---|---|
| **Card-level** | items (L1 cards + emergences) | Cards, Explorer, Tree | fields discovered from items |
| **Grammar-level** | whole decks (one node/dot per grammar) | Timeline, Tree of Life, Genealogy | fields discovered from deck metadata (`when`/century, `branch`, `function`, `tier`, region) |

Consequences:
- **View-switcher splits in two.** The eye dropdown on card-level pages cycles only
  Cards/Explorer/Tree (same `?decks=` spec carries over). Grammar-level pages get
  their own switcher (Timeline/Tree of Life/Genealogy) — or just the header tabs,
  since those three always show "the whole collection". Remove the eye from
  Tree-of-Life pages (builder: "it would not interchange as easily").
- **Tree of Life CAN render emergent patterns** without going down to cards: the
  radial graph's grouping today is hardcoded (tier/function toggle). Generalize: run
  the same `discoverFields()` over the deck-level records (each deck = one record
  with its `_decks` metadata) and let any discovered field drive hub-grouping —
  century, region, function, branch. The two existing toggle buttons become value
  pills of a "group hubs by: ___" selector fed by discovery. Same for timeline's
  lane field. This is the explorer engine pointed at 31 records instead of 3,000.

## 5.2 The shared engine: extract `dimension-engine.js`

Explorer already contains the whole brain: `flatten()` (metadata inheritance),
`discoverFields()`, `inferHierarchy()`, `groupBy()` (with array-field explosion for
keywords), spec `{rows, cols, filters, pinned}` + URL-hash + localStorage. Extract
those pure functions into `viewers/dimension-engine.js` (no DOM). Explorer becomes
its first consumer; nothing visible changes.

Then each viewer consumes the same spec but renders it its own way:
- **Cards**: `rows` (first entry) = the grouping the left sidebar shows; `filters` =
  the sidebar checkboxes; drag a chip onto the sidebar or the "Group:" dropdown =
  same gesture as explorer's row zone. One grouping dimension is enough here.
- **Tree**: grouping field = what the trunk branches on (today: inferred
  composite_of hierarchy; a dropped chip overrides it).
- **Explorer**: unchanged (rows × cols pivot is its specialty).
- Spec serializes into the URL hash with the same keys on all three, so the eye
  switcher carries the arrangement between viewers losslessly.

## 5.3 Grammar multiselect everywhere (kill the meta-grammar)

Explorer's deck-picker popover (checkbox list from `_collection.json`) becomes a
shared component `deck-picker.js`. Cards/Tree get it too; selected decks load in
parallel via `grammar-loader.js`, run through `flatten()` with deck-name inherited as
a `deck` field — which means "deck" is just another draggable dimension, and
`all-decks-many-lenses/grammar.json` stops being hand-maintained (generate it in CI
or drop it once all multi-deck viewers use the picker).

Add a first-run hint near the picker (dismissable, localStorage):
*"Pick several decks — patterns appear when collections overlap."*

## 5.4 Build order (each step ships alone)

1. ✅ **DONE** (Jun 12) Quick wins: explorer **+N expands the cell**; **multiselect
   hint**; **AI balloon logged-out message** (5.6).
2. ✅ **DONE** (Jun 13, Opus) Extracted `viewers/dimension-engine.js` (pure, DOM-free:
   flatten/discoverFields/inferHierarchy/groupBy/passes/vals/smartCmp). Explorer binds
   thin wrappers — every call site unchanged, verified identical (156/238 items, 22
   chips, 0 errors). **This is the shared core every other viewer now imports.**
   ── Sonnet can pick up from step 3. ──
3. `deck-picker.js` shared; Cards gets multiselect + `deck` dimension. Pattern to
   follow: load `dimension-engine.js?v=1`, then in the viewer's script
   `const { flatten, discoverFields, groupBy, passes, vals, smartCmp } = DimensionEngine;`
   and feed it the loaded grammars exactly as explorer's `boot()` does (see
   explorer.html flatten call sites + the inherit object).
4. Cards sidebar accepts chip drops (one `rows` slot); eye-switcher carries spec
   between Cards/Explorer/Tree.
5. Tree of Life + Timeline: deck-level field discovery drives hub/lane grouping;
   remove eye icon from grammar-level pages, split the switcher.
6. I Ching test: load the python-schema experiments as grammars, point the same
   viewers at them. What breaks defines the porting spec for recursive.eco.
7. Only after 6: port the engine + spec format to recursive.eco viewers.

## 5.5 What porting back to recursive.eco will look like (later, do not start)

The deliverable to port is **one JS module + one spec format**, not seven viewers.
recursive.eco's GrammarReader/eye-views adopt `dimension-engine.js` semantics; the
`render_as`-style fields in eco grammars become candidates for deletion once the
data-shape-driven viewers prove out here (matches eco's existing "fix the grammar,
not the app" + "every preview renders every grammar" principles).

## 5.6 AI balloon for logged-out users

`cards.html` (and tree-viewer) lazy-load `flow/assistant` in an iframe. Logged-out
users currently get whatever the flow page does in an anonymous iframe — confusing.
Fix tarot-side: on first open, `await window.recursiveAuth?.getUser()`; if no user,
render a small message in the balloon instead of the iframe: *"The Library Assistant
needs a free recursive.eco account — Sign in ↗"* (same link the auth widget uses,
`FLOW + '/?signin=1'`, new tab). After sign-in the popup-return flow already
refreshes auth; reopening the balloon then loads the iframe.
