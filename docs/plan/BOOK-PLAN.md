# The Recursive Tarot — Book Plan

*A web-first "course" that doubles as a printable book: an introduction to tarot
across all the decks, then card by card. Built from the grammars we already have,
rendered with the live viewers inline, and made to print cleanly — not a separate
flat-PDF pipeline.*

Status: **planning + proof.** Companion to `MULTI_LENS_PLAN.md` and `FUTURE_PLAN.md`.

---

## 0. The format decision (why a course, not a PDF dump)

Author direction: a direct print-to-PDF won't carry the experience. Instead —
**one web artifact, two modes**:
- **On screen** it's a course: scrollable, with the **Lineage** and **Timeline**
  viewers and the card **image-strips** rendered *inline* (interactive).
- **In print** the same page paginates cleanly via `@media print` + page-break
  rules, with each interactive viewer swapped for a **static figure** (browsers do
  not print live iframes/SVG-pan-zoom reliably — see §5).

This keeps a single source of truth (the grammars) and avoids maintaining a
parallel book manuscript.

---

## 1. Renames & navigation cleanup (quick win, do first)

| Now | Problem | Change |
|---|---|---|
| **"Tree of Life"** (header → `genealogy-tree.html`) | It's a *deck genealogy*, but "Tree of Life" is the Kabbalistic 10-sephiroth / 22-path diagram we cite in every trump synthesis. The label collides with a real concept in our own data. | Rename to **"Lineage"**. |
| **"Genealogy"** (header → `genealogy.html`) **and** "Tree of Life" | Two genealogy views side by side — redundant/confusing. | Keep one as **"Lineage"** (the radial). Demote or merge the other. |
| Reserve "Tree of Life" | We *could* build a real Kabbalistic Tree (data supports it: every trump has a sephirah-path + Hebrew letter). | Future view; don't spend the name on a family tree. |

Files: `site-header.js` (CARD_VIEWS/GRAMMAR_VIEWS labels + `autoActive`),
`view-switcher.js`, the viewer `<title>`/H1s. Also surface each branch's narrative
(the `tree-of-tarot` branch Scenes) in a side panel, and label descent arcs as
**"influence — often conjectural"** (deck descent is contested scholarship).

---

## 2. Content inventory — HAVE vs. NEED

**HAVE (built this arc):**
- ✅ 22 trump **cross-deck syntheses** (`research/synthesis/trumps.json`) → emergent
  nodes + Lenses overview.
- ✅ `tree-of-tarot` **branch + deck Scenes** (the genealogy narrative).
- ✅ Per-deck **overviews** (deck grammar descriptions).
- ✅ Per-card **Scene / Symbol / Tradition Note / Research note** across decks.
- ✅ Public-domain **images** on R2; `trump_key` stamped for exact cross-deck strips.
- ✅ The **"Divination Question"** essay (referenced by the meta).
- ✅ **Timeline** + **Lineage** viewers (iframe-able via `?src=`).

**NEED (to produce):**
1. **Intro narrative** assembled into front-matter (what tarot is; Renaissance game;
   the 1781 divination turn; how to read the book). ~80% exists in branch Scenes +
   the Divination essay; needs stitching.
2. **Per-deck spread** content: a one-page overview + a cover image + 2–3 signature
   cards per deck. Overviews exist; needs *curation* (pick the signature cards,
   confirm a clean cover image per deck).
3. **Image credits / provenance** per image (PD source line) — **required for KDP**.
4. **Consistent image per trump per deck** for the across-decks strips (some decks
   lack an image for some trumps; flag gaps).
5. *(Optional, later)* **Minor-arcana** + **court** syntheses (trumps first).
6. **Captions** for each inline figure (Lineage, Timeline, image-strips).

---

## 3. Book structure (the flow)

```
Front matter
  · Title / colophon (public-domain, CC-BY-SA, repo link)
  · What is tarot?  (Renaissance game; divination added 1781) — honest hook
  · How to read this book

Part I — THE LINEAGE
  · The whole tree (inline LINEAGE viewer → static figure in print)
  · The timeline (inline TIMELINE viewer → static figure in print)
  · One section per branch (Roots / Southern / Eastern / Western / Occult / Sui
    Generis): the branch narrative + the decks in it

Part II — THE DECKS
  · One spread per deck: overview + cover image + 2–3 signature cards

Part III — THE CARDS  (the heart)
  · One chapter per trump (0–21): the "Across the decks" synthesis
    + an image-strip of that card across decks (Small-Multiples)
    + selected per-deck notes (Scene / the dated later-commentary)

Back matter
  · The Divination Question (essay)
  · Sources & bibliography (from research/)
  · Image credits (PD provenance) · Index
```

---

## 4. Item 1 — the course-format introduction (inline viewers)

Build `pages/book/intro.html` (or `course/history-of-tarot.html`): a single page
that renders the intro narrative and **embeds the Lineage + Timeline viewers
inline**. On screen they're the live interactive viewers (iframe with `?embed=1`);
the page carries `@media print` rules and a **static print fallback** per viewer.

The proof in this commit tests exactly this and the print behaviour (§5).

---

## 5. Item 2 — print strategy & the iframe problem

**Risk:** browsers do **not** reliably print iframe contents (often blank or
first-page-only), and pan/zoom SVG viewers print as a tiny slice. So "iframe the
viewers inline" works on screen but **fails in print as-is.**

**Solution — dual render per figure:**
- On screen: `<iframe class="screen-only">` the live viewer.
- In print: `@media print { .screen-only{display:none} .print-figure{display:block} }`
  shows a **static** figure — a captured **SVG/PNG snapshot** of the Lineage tree
  and Timeline (generated once, stored in `print/book/figures/`), at full page
  width, with a caption.

**Pagination rules (the "page breaks just work" part):**
- `@page { size: <trim>; margin: <m> }` + running header/footer.
- `.chapter { break-before: page }` ; `.figure, .card-strip { break-inside: avoid }`.
- `h2/h3 { break-after: avoid }` (no orphaned headings).
- Hide all site chrome (`header`, nav, buttons) in print.

**Trim size:** target a KDP size early (e.g. **7×10 in** or **8.27×11.69 / A4** for
images) — it changes margins and figure sizing, so decide before laying out.

---

## 6. Item 3 — per-card printable rendering in Lenses

Give each trump a **book-chapter layout** that prints as 1–2 clean pages:
synthesis + image-strip across decks + per-deck notes. Either:
- a print mode inside `lenses.html` (a "Book view" toggle), or
- a dedicated `pages/book/card.html?trump=death` printable view that pulls the
  same data (trump_key + synthesis + images). *(Recommended — cleaner print CSS.)*

This is also the per-chapter source the full book assembles.

---

## 7. Item 4 — KDP / print-on-demand workflow

**KDP needs:** a print-ready **interior PDF** (chosen trim, ≥0.125" bleed for
full-bleed images, embedded fonts, ~300dpi images) + a **cover PDF** (computed
spine width from page count). Image rights: **all interior images must be
public-domain with a credits page** — we're clear (PD sources), but must *list*
provenance.

**Two paths:**
1. **Browser print-to-PDF** from the web book — simplest; good for proofs, but
   margins/bleed/headers are fiddly and browser-dependent.
2. **Headless render** — `scripts/generate-book.mjs` drives Puppeteer/Playwright
   over the web book with print emulation and `@page` rules → a deterministic,
   KDP-grade PDF. Reproducible; the real pipeline. *(Recommended for the final.)*

**Recommendation:** build the **web book** so it prints "good enough" via the
browser first (validates content + flow), *then* add the headless workflow for
KDP-grade output. Don't build the PDF pipeline until the web book's content and
pagination are settled.

---

## 8. Build order (phased, each shippable)

1. **Renames + nav cleanup** (§1) — quick clarity win.
2. **Course-intro proof + print test** (§4–5) — *this commit*; proves inline-viewer
   + print works (with static fallbacks).
3. **Per-card printable card view** (§6) — `pages/book/card.html`, the chapter unit.
4. **Curate per-deck spreads + image credits** (§2) — content pass.
5. **Assemble the full web book** (front → Part I → II → III → back).
6. **KDP headless render workflow** (§7) — final, reproducible PDF.

Open questions for the author: trim size? include minors/courts or trumps-only v1?
hardcover/paperback? working title?
