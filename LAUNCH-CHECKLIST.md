# Launch Checklist — The Recursive Tarot

Working notes for what to address before a real public launch. Live site: **tarot.recursive.eco** (GitHub Pages serves the `dev` branch).

---

## ✅ Done (recent sessions)
- **Header** — logo now links to `recursive.eco`; "The Recursive Tarot" links to the project home; removed the ugly typed-out "part of recursive.eco" line (and the invalid nested `<a>` inside `<a>`). Cache bumped to `site-header.js?v=17` across all pages.
- **Play page** — four-door lede (added "Watch the history"); every tile thumbnail is now a distinct public-domain card (no repeats, no gradient-glyph placeholders).
- **Viewers** — `sequence-v2.html` (fuller recursive-eco port) added alongside `sequence.html` (v1).
- **Programs** — `history-of-tarot-sequence.json` (cards + footage slots) and `history-of-tarot-watchlist-sequence.json` (18 verified YouTube docs).
- **Course** — added "Part 9: the recursive.eco MCP" to *Build a Tarot Deck with Claude*.

---

## 1. AI assistants — test ALL of them (not just the course)
The **Library Assistant** (floating 💬 button, bottom-right — iframes the flow app, needs a free recursive.eco login) is on **three** pages:
- [ ] `viewers/cards.html`
- [ ] `viewers/tree-viewer.html`
- [ ] `pages/course-viewer.html`

For each: button appears → logged-out shows the sign-in prompt → logged-in loads the iframe and the assistant actually answers. Then the cross-app tools:
- [ ] **Oracle** (`flow.recursive.eco/cast`) opens and reads when signed in.
- [ ] **Create your own deck** (`flow.recursive.eco/create/...`) opens the editor.
- [ ] **recursive.eco MCP** — run the MCP test prompt (create grammar / generate image / import) to confirm Course Part 9 only advertises capabilities that actually work.

## 2. Shop — rewire with the print API (after print-quality check)
`pages/shop.html` reads `print-products.json` and only links a product to its `product_url` when that product's `live` flag is `true` (otherwise the buy link is `#`).
- [ ] **Order proofs and check print QUALITY first.**
- [ ] Then set `live: true` + real `product_url` per product (or wire the print/commerce checkout API).
- [ ] Verify `print-viewer.html` booklet layouts match what the printer actually produces.

## 3. Sequence viewer — pick the canonical one
- [ ] Decide v1 (`sequence.html`) vs v2 (`sequence-v2.html`). Play page currently points the "history of tarot" tile at **v2 (beta)**. Options: keep v2 / revert to v1 / rename v2 → `sequence.html` and retire v1.
- [ ] Fill the **footage slots** in `history-of-tarot-sequence.json` with verified clips over time.
- [ ] Decide whether to surface the **watchlist** program on the site (currently reachable by URL only, not linked from any page).

## 4. Site hygiene sweep
- [ ] Click every nav item + every Play/Shop tile — no 404s (root, `/viewers/`, `/pages/`, `/pages/games/`).
- [ ] Mobile: header wraps cleanly, tiles stack, dropdowns work on tap.
- [ ] Light + dark mode both readable on every page.
- [ ] OG/meta tags + favicon present on key pages; `CNAME` = `tarot.recursive.eco`.
- [ ] Auth widget (`recursive-auth`) renders in the header and sign-in works.
- [ ] **Reminder:** any time `site-header.js` changes, bump `?v=` across all pages (currently `v=17`).

## 5. Content honesty
- [ ] Generated vs. historical images clearly labeled (especially if MCP-made decks get published — historical decks here are scanned public-domain art, not generated).
- [ ] Game-vs-divination framing intact across pages.
