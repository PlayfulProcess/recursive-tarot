# Tarot UI Truth Audit — 2026-08-07

*The astro-style truth audit, run on tarot.recursive.eco. Method: code-level audit by three
parallel agents + live verification on a local static server (`python -m http.server 8765`).
Every finding below carries a verdict: WORKS / LIKELY-BROKEN / DEAD / UNCLEAR. Live checks were
signed-out; signed-in-only paths are flagged for Fernando's browser test.*

**Live smoke result (all pages, local):** every audited page loads with zero console errors
except two benign `401`s per page — the `auth-widget.js` session probe against flow.recursive.eco
while signed out. Expected behavior, but it makes real errors harder to spot in DevTools; worth a
quiet `catch` someday.

**Fixed during this audit (already in working tree, v46):** the header dropdown
disappear-on-the-way-down bug. Root cause: the invisible `::before` "bridge" over the 8px gap was
being **clipped by `overflow-y:auto`** on the same `.dd-menu` (scroll containers can't hit-test
pseudo-content outside their box), so pure CSS `:hover` closed the menu the instant the cursor
entered the gap. Fix: desktop hover is now JS-managed with a 260ms close grace period
(`site-header.js`, `?v=46` bumped on all 24 pages). Verified live: menu survives the gap crossing,
re-enter cancels close, Escape/keyboard/touch paths unchanged.

---

## 1. Explorer (viewers/explorer.html) — the informativeness question

Fernando's brief: *"I don't want a view that is complex and does not generate insights… my idea
was that scholars or artists could use it to compare and inspire themselves."*

**Live check:** all seven preset chips work (Major/Minor▸Suit▸Rank, Arcana×Suit, Suit×Rank,
Deck×Arcana, Number line, Lineage▸Deck, Clear), each correctly pre-filters to level=card
(768 of 904 items). The controls are not broken. The problem is the **semantics of the fields**
feeding them.

### The metadata muddle (measured, meta-grammar = 904 items)

| Problem | Numbers | Effect in the UI |
|---|---|---|
| `number` is ONE shared field for trump numbers **and** pip/court ranks | RWS-structure decks (RWS, Marseille, Etteillas, Book T, Sola Busca, Visconti-Sforza, Paris, Vieville…) all have majors 0–21 AND minors 1–14 in the same key | Row "3" = The Empress **+ every 3-of-suit** across 9 decks. This is the "grouping most number cards together" Fernando saw. Numerological trump↔pip correspondence is a real esoteric lens (Golden Dawn), but as the *default* semantics of a shared column it reads as noise. |
| `arcana` has two labels for one concept | 243 `major` + 32 `trump` + 493 `minor` + 136 missing | Arcana pivots split into three bogus groups. Note: "trump" is *deliberate* vocabulary for pre-occult decks (Bologna, Minchiate, Cary-Yale) — the fix is a normalized *view-time* grouping (or an added normalized field), not flattening the editorial distinction. |
| 180 items have no `number` at all | incl. 136 with no `arcana` | The "—" row (44 items even after level filtering): sheets, courts of odd decks, Minchiate's extra trumps, etc. |
| Non-deck grammars share the meta-grammar | courses, people, books, tattvas, Lenormand, Mamluk… | The `level` filter (6 values) already guards the presets — good — but a cleared board exposes all 904 mixed. |

### Verdict on informativeness

The Explorer's *machinery* is sound and the deck-columns × card-rows shape is genuinely the
scholar/artist view — "the same card across 13 decks side by side" is the killer feature and no
other tarot site does it well. What breaks the insight today:

1. **The number axis conflates three orderings** (trump sequence, pip rank, Etteilla's own
   1–78 sequence — the last was overwritten in June, noted in memory). Scholars need
   `trump III across decks`, artists need `all 3-of-Cups`, nobody needs both in one row.
2. **major/trump split** makes every arcana grouping wrong by default.
3. **The "—" bucket** is a landfill row that opens every pivot.

Recommended shape (for the plan): keep the pivot engine; derive clean fields at meta-build time
(`role`: trump/pip/court/other · `trump_number` · `rank` · keep deck vocabulary in a separate
display field); make the default landing view "Trump number × Deck" (the comparison wall);
demote raw `number` from the presets. Also: pivots should say what they exclude ("38 undated
items hidden") instead of silently bucketing to "—".

*(Full control-by-control table for explorer/cards/deck: agent report pending — appended below
as §5 when it lands.)*

---

## 2. tree-viewer / caster-studio / genealogy-tree / timeline

### Cross-cutting
- **`<view-switcher>` (the "eye") is retired and renders nothing** (`view-switcher.js:98-104`,
  self-documented) but its script tag + element still ship on genealogy.html, grammar-course.html,
  tree-viewer, genealogy-tree, timeline. DEAD — remove in one pass.
- `dimension-engine.js` loaded by genealogy-tree.html but never called there (dead include);
  timeline.html uses only `smartCmp` from it.

### tree-viewer.html
Tree machinery (drill-down, breadcrumbs, pill filters, hover connector tracing, framed RefResolve
embeds, detail modal) — **WORKS** throughout, and is proportionate. The header button row is where
the debt lives:
- **LIKELY-BROKEN** "Get a Reading": passes `?src=` to caster, but caster-studio only reads
  `?spread=` — deck context silently dropped (tree-viewer.html:1022, caster-studio.html:478).
- **LIKELY-BROKEN** "Copy to My Grammars": reads `?id=`, empty on the site's standard `?src=`
  navigation → forkId-less app URL (tree-viewer.html:1693).
- **DEAD** right-click `NodeContextMenu`: referenced (tree-viewer.html:1058, also cards.html) but
  never defined anywhere in the repo — guarded no-op.
- **BROKEN destination**: "View as Cards" no-tree fallback → `/pages/grammar-viewer.html`, which
  doesn't exist in this repo (404) (tree-viewer.html:1039).

### caster-studio.html
The board itself — drag/multi-select/ctrl-copy geometry editing, grid auto-detect, import/export
split (spread vs full reading), cast with reversal slider, voices carousel, card detail with
framed embeds, hover preview — **WORKS** and earns its ambition. All network traffic is read-only
(no POST anywhere). The **save/persist story is the debt** — three affordances that look like
"save my work":
- **LIKELY-BROKEN (misleading)** "Update spread": patches only the in-memory copy of a saved
  My-spread and flashes "Updated ✓" — nothing is persisted (caster-studio.html:1104-1115).
- **LIKELY-BROKEN (overpromises)** "Contribute a spread on GitHub": static link to a blank GitHub
  new-file page; never carries the actual exported JSON (caster-studio.html:360).
- **UNCLEAR→likely always-fallback** "Interpret with AI": code's own comment says the flow-side
  `recursive:interpret-reading` listener is unshipped, so every click probably hits the 1s
  timeout → clipboard fallback (caster-studio.html:960-966, 1027-1051). **Needs signed-in test.**
- Signed-in-only paths needing Fernando's test: My-spreads dropdown (`/api/spreads`), model-quality
  hint banner.

### genealogy-tree.html (Tree of Life / wheel)
Everything **WORKS** (descent arcs toggle, legend filters, bidirectional descent tracing on hover,
chronological prev/next paging, keyboard). Only debt: hand-maintained `SLUG_MAP` (a new deck node
silently loses its "Open cards →" link), duplicated again in timeline.html — derive from
`metadata.source_deck` instead.

### timeline.html
Same control vocabulary as genealogy-tree on the time axis — **WORKS**. The feared silent
undated-deck drop is **dormant, not active**: live check confirms all ~30 decks render with years
(parseYear handles the "c. 1550"-style values). Worth an "undated" lane eventually, not urgent.

---

## 3. courses gallery / course-viewer / genealogy.html / lenses / sequence players

### pages/courses.html — WORKS, thin and honest. Nothing to cut.

### pages/course-viewer.html
TOC (desktop + mobile), scroll-spy, QR chip + lightbox, course popup pills, image-path rewriting —
**WORKS**. Findings:
- **LIKELY-BROKEN** `relocateCoursePills()` (line 1046): early-returns because `#present-toggle`
  doesn't exist in the DOM → pills never relocate to the hero row as intended. Cosmetic.
- **DEAD** `setPresentationMode()` (lines 1857-1882) + its CSS: unreachable leftovers of the
  presentation-mode toggle retired Jun 23.
- **LIKELY-BROKEN** `showCourseListing()` (line 942): references non-existent `#course-duration` →
  TypeError → generic error screen. Only hit via `?grammar_id=` multi-item path (app-side links),
  not from any static-site link.

### genealogy.html — WORKS (Lineage/Function recolor, node detail, prev/next, cytoscape-fail
fallback list is genuinely good). Debt: dead `<view-switcher>` tag; prev/next matches deck by
rendered `<h2>` text — fragile if two labels ever collide (theoretical today).

### viewers/prototypes/lenses.html
All five lenses (Ribbon / Synopsis / Multiples / Matrix / Reader), deck picker, per-view card
selects, deep-link `?card=` — **WORKS**, zero dead controls. Naming inconsistency: a first-class
nav item living in `prototypes/`. Densest page on the site; Matrix + Small-multiples overlap
Synopsis/Ribbon in purpose — merge candidates if it ever needs a diet.

### Sequence players — three overlapping formats
- **viewers/sequence.html (v1): ORPHAN** — zero inbound links sitewide (only v2's "open in v1"
  escape hatch). Already flagged in BACKLOG/LAUNCH-CHECKLIST as an undecided fork. v2 is a strict
  superset and the only one linked from play/sources. → retire v1.
- **viewers/sequence-v2.html: WORKS** across all controls (J/L seek, fullscreen, scrubber,
  end-overlay, swipe). → promote to canonical `sequence.html`.
- **viewers/perform.html: WORKS** as code; reachable from exactly ONE tile on play.html; a third
  player format (performance JSON + audio overlays). → candidate to fold into sequence-v2.

---

## 4. Ranked bug list (what a fix phase should take, in order)

| # | Where | What | Class |
|---|---|---|---|
| 1 | site-header.js | dropdown disappears crossing the gap | **FIXED this session (v46)** |
| 2 | caster-studio:360 | Contribute-on-GitHub link carries no content | broken promise to contributors |
| 3 | caster-studio:1104 | "Update spread" fakes persistence ("Updated ✓") | trust |
| 4 | tree-viewer:1022 | Get-a-Reading drops deck context (`?src=` unread by caster) | broken handoff |
| 5 | tree-viewer:1693 | Copy-to-My-Grammars empty forkId on `?src=` pages | broken handoff |
| 6 | tree-viewer:1039 | 404 fallback link to nonexistent grammar-viewer.html | 404 |
| 7 | course-viewer:1046 | course pills never relocate (missing #present-toggle) | cosmetic |
| 8 | course-viewer:942 | `?grammar_id=` listing path throws (#course-duration) | app-side path |
| 9 | everywhere | dead `<view-switcher>` tags + script, dead NodeContextMenu hooks, dead setPresentationMode + CSS, unused dimension-engine include | dead-code sweep |
| 10 | caster-studio:1027 | Interpret-with-AI likely always falls back (flow listener unshipped) | needs signed-in test + flow-side work |
| 11 | genealogy-tree/timeline | hand-maintained duplicate SLUG_MAPs | maintenance debt |

**Orphans to retire/merge:** sequence.html (v1) → delete; perform.html → fold into sequence-v2;
lenses.html → graduate out of `prototypes/`.

---

## 5. Explorer / cards.html / deck.html — full control table

### viewers/explorer.html (+ dimension-engine.js)
All primary controls **WORK**: Decks▾ multiselect popover (`?decks=` navigation), Cards/Counts/
Sections modes, section picker with attributed/"later" inference, zoom slider, sidebar toggle
(persisted), presets, drag-to-pivot chip tray with hierarchy chaining (desktop drag + 420ms
long-press touch path, both reaching the same logic), rows/cols/filters drop zones, filter
popover, "+N more" cell expansion, detail panel, hover preview, lightbox.

How fields are derived (`dimension-engine.js flatten()`, lines 26-67): a **blind pass-through**
of every scalar `metadata` key into a same-named pivot field, no per-field semantics; missing
values bucket to a literal `—` (`vals()`, line 113). Confirmations and new bugs:

- **`number` conflation confirmed at the source**: in golden-dawn-book-t, `major-01` has
  `metadata.number: 1` (trump) and `wands-ace` has `metadata.number: 1` (pip) — same field,
  same row. Courts 11–14 overlap trumps 11–14. Across 1,918 leaf cards in the 61 deck grammars,
  **670 (34.9%) have no `metadata.number` at all** → one undifferentiated `—` row.
  Fix lead: `trump_number` **already exists** on Golden Dawn's own grammar — the engine just
  isn't told to prefer it.
- **LIKELY-BROKEN — inherit loses to same-named item metadata** (dimension-engine.js:53-54:
  inherit applies only `if (!r[k])`, but the metadata loop ran first). Real instance: the
  repo's cross-link convention stamps `metadata.deck` with the *other* grammar's label, so on
  `?decks=` loads (the only path the UI builds) **47 items across 5 decks are misattributed**
  — e.g. paris-anonymous-tarot's trumps 01–04 appear as "Tarot de Marseille" in Deck × Arcana
  and every deck filter (books-of-tarot: 10, paris-anonymous: 21, tarot-de-besancon: 13,
  tarocchino-bologna: 2, noblet: 1). Fix: inherit wins for identity fields, or namespace the
  cross-link label so it can't collide with a dimension.
- **`?src=` single-deck loads never get `century`** (flatten called with `inherit=null`,
  explorer.html:689/691) — deck-level `metadata.year` ignored; e.g. Book T (year 1909, no
  per-item years) loses the field entirely. Mitigating: nothing in the UI links `?src=` — but
  `docs/GRAMMAR-INVENTORY.md:34` still documents it (stale).
- **Arcana presets are all-`—` for 37 of 61 grammar folders** (courses + genuinely non-tarot
  decks) — not a crash, but a preset that silently does nothing for a large slice of the library.
- Minor dead code: redundant `{once:true}` delegated listener in `renderPinnedFilters()`
  (line 536) — harmless, self-flagged in a comment.

### viewers/cards.html (5,967 lines)
Core browsing surface **WORKS**: search, deck multiselect round trip, title dropdown, filter
pills, dimension chip tray, Section Lens (incl. "Hide later interpretations", live modal
re-render), item modal with prev/next/Esc, `?item=` deep links, framed RefResolve embeds
(matches CLAUDE.md spec exactly), sidebar resize, report modal, print/edit/GitHub-source
buttons. Findings:
- **LIKELY-BROKEN**: community-grammar sign-in gate guards on `window.SigninModal` — **no
  signin-modal.js exists anywhere in the repo**; signed-out visitors always get
  `alert('Sign in functionality not available…')` (cards.html:5010-5039, 5176-5200).
- **DEAD** (legacy weight from the Supabase-app era): hidden `#deck-switcher` select +
  `switchDeck()` (2159, 3817) · "Tarot / I Ching" type toggle (2191) · `showLensMenu()` — full
  context menu with zero call sites (3855) · `NodeContextMenu` hook, never defined (3500) ·
  "Sync from GitHub" functions, target elements never injected, **plus a latent
  `ReferenceError` (`renderItems()` doesn't exist) inside the dead branch** (3525, 4946-4982) ·
  modal "View as" eye dropdown hardcoded empty since Jun 29 (4553) · `eco-links.js` loaded but
  only `.ready()` called, render never used (2137).
- **Quiet state-loss gap**: two same-looking "Group by" features — `deckGroupField` (chip tray)
  persists via `location.hash`, `pillAxisId` (built-in emergence axes select) never touches the
  hash and is silently lost across hash-carrying navigation.
- cards.html hand-rolls its records and is **not** susceptible to the explorer's deck-clobber
  bug in its multi-deck path (whitelists keys, sets `r.deck` unconditionally).
- Selection mode (`?mode=select`, ~450 lines) works but is a second product (flow.recursive.eco
  reading picker) bolted onto the browsing page — split-out candidate.

### deck.html (+ loader.js)
Minimal flat renderer; both links work; no bugs in traced paths; consistent escaping. No
control surface to audit — it's the "view source" fallback. Merge-into-cards.html candidate.

### Additions to the ranked fix list (§4)
- **2a (Phase-1-class, data-correctness):** the inherit-vs-metadata deck misattribution (47
  cards mislabeled in the Explorer's only reachable load path).
- **9 (sweep) grows:** cards.html dead family — sync buttons + latent ReferenceError, type
  toggle, switchDeck, showLensMenu, viewModeOptions scaffold, eco-links dead load; SigninModal
  gate → fix or replace with a direct flow sign-in deep link; unify the two Group-by states.
