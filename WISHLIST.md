# WISHLIST

Ideas that are wanted but not built yet, with enough detail to pick up cold.
Distinct from `BACKLOG.md` (planned work) — this is the "someday, if it stays easy" pile.

---

## Spread Studio — presentation-app editing (`viewers/caster-studio.html`)

The Studio's board is a plain absolutely-positioned canvas: each position is a `.slot`
div placed by `left/top` as a 0–1 fraction of `#board`, with pointer handlers attached
in `attachSlot()`. That made the first slice of "edit it like PowerPoint" cheap.

### Shipped (Jul 2026)

- **Shift-click multi-select** — toggles a position into `selected` (a `Set` of position
  ids); selected slots get a `.sel` outline.
- **Group drag** — dragging any selected position moves the whole selection by the same
  delta (`attachSlot` captures a `start` snapshot of every group member's x/y).
- **Ctrl / ⌘ / Alt-drag to duplicate** — the originals snap back to where they were on
  drop and copies are materialised at the dragged geometry, keeping labels and meanings.
  (Implemented at *drop* time rather than at pointerdown so the drag never has to
  survive a re-render and lose pointer capture.)
- **Esc** clears the selection, **Delete / Backspace** removes the selected positions.

### Still wanted

- **Rubber-band marquee select.** Drag on empty board background to sweep a rectangle
  and select everything inside it. Needs a pointerdown handler on `#board` itself (the
  slots stop propagation today), a `position:absolute` marquee div, and a
  rect-intersection test against each slot's `getBoundingClientRect()`.
- **Align & distribute.** With ≥2 selected: align left/centre/right/top/middle/bottom,
  and distribute horizontally/vertically at equal spacing. Pure math over the selected
  positions' x/y; would want a small floating toolbar that appears when `selected.size > 1`.
- **Snap to grid / smart guides.** Snap x/y to a 1/12 grid while dragging (hold Alt to
  bypass), plus dashed alignment guides when a dragged position lines up with another.
  This is what would make hand-built grid spreads land exactly on their `axes` headers
  instead of relying on `axisTicks()`'s 0.07 clustering tolerance.
- **Copy / paste with the keyboard.** Ctrl+C / Ctrl+V on the selection, pasting at a
  small offset. Needs a clipboard buffer in page state (not the system clipboard).
- **Undo / redo.** The single biggest quality-of-life gap. Would need a snapshot stack
  of `{positions, axes, spreadName}` pushed on every mutating action (drag end, add,
  delete, duplicate, label edit, axes edit) with Ctrl+Z / Ctrl+Shift+Z.
- **Nudge with arrow keys.** Move the selection by 0.01 (0.05 with Shift).
- **Resize / rotate positions.** Per-position card scale and rotation (the classic
  "crossing card" in the Celtic Cross is drawn rotated 90°). Would need `w`/`rot` fields
  on the position contract, which is a wire-format change — coordinate with the flow
  side (`lib/oracle/spread-codec.ts`) before adding.

---

## Spread Studio — assistant round-trip

- **Let the assistant edit a spread by name.** Today the flow assistant can only
  `create_spread` (append-only), so "edit my Nature's Negotiation spread" appends a
  duplicate instead of updating. Needs `list_spreads` / `update_spread` tools on the
  flow side, or the user's saved spread names injected into the system prompt. Detail
  and file references in `docs/plan/ORACLE-RECEIVE-CAST-SPEC.md` (appendix).
- **Teach `create_spread` the `axes` field** so the assistant can build grid spreads
  with row/column headers instead of repeating the axis names in every position name.
  Same appendix.

---

## The Book of Fate (1822) — finish the transcription (`pages/book-of-fate-1822.html`)

The page ships a real, working digital edition of Napoleon's *Book of Fate* — but
only **9 of the book's 32 questions** are verified word-for-word against the
original. The frontispiece (the question list) and the main answer bank are both
badly damaged in the OCR the page was built from — decorative italic type on the
frontispiece, and the engraved Hieroglyphic images (Pyramid, Ladder, Cross Bones,
etc.) simply didn't survive OCR at all in the body text, so each Question's own
page can't currently be matched to its Signs and answers with confidence.

We'd love for someone to take this further. What's needed: the original scan
(linked at the top of the page, and in `research/` if pulled locally) read
page-by-page rather than through OCR, to recover the remaining ~23 questions'
answer sets and the star-Sign-to-Hieroglyphic lookup table this page currently
can't render. The data model is already there — `QUESTIONS` in the page's own
`<script>` block, one object per question with an `answers` array of
`{ h, a, kind }` (Hieroglyphic name, the quoted answer, and its "kind" —
positive / mandatory / presumptive / admonitory / conditional, per the book's own
taxonomy). Extending it is additive: more entries, no restructuring. A PR with
even a handful of newly-verified questions is welcome on its own — it doesn't
need to be the whole book at once.
