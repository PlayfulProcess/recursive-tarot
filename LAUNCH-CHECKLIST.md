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
- [ ] **Integrate the local tester with the Oracle (do this better).** The local Caster (`viewers/caster.html`) draws a spread but stops there — handing it off to the recursive.eco Oracle is currently just a one-way link. Build a real bridge so a local draw can carry its cards/question into the Oracle and become a saved, AI-read Journal entry on the platform (and ideally come back). This is the seam between the static tester and the live product; it should feel seamless before launch.

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

---

## Scholarly integrity — before publishing the contemporary-tarot thesis

The *Tarot Today* course leans on Judith Butler's performativity (resignification, performativity-≠-performance). Butler is one of the most systematically *misread* theorists alive — most summaries reproduce the "you choose your gender like an outfit" voluntarism error, which is close to the opposite of the argument. **If we keep this thesis as a public reading, do this homework first** (paraphrase-with-attribution is fine from summaries; a *quotation* is a promise you read the original):

- [ ] **"Critically Queer"** — final chapter of *Bodies That Matter* (1993). The core text: "queer" as a reclaimed, resignifiable performative. Read this one if you read nothing else.
- [ ] **The 1999 Preface to *Gender Trouble*** (anniversary edition). Short; Butler personally correcting the voluntarism misreading. Highest value-to-length.
- [ ] **A chapter of *Excitable Speech* (1997)** on injurious speech + reclamation — the engine for "taking back a sign used against you."
- [ ] Optional scaffold: **Sara Salih, *The Judith Butler Reader*** (verified primary excerpts) + her *Judith Butler* (Routledge Critical Thinkers) on-ramp.
- [ ] Nail the one distinction in the course prose: **performativity is compelled citation, not sovereign choice** — the self is the *residue* of the citations, not their author. (Source: research/17-contemporary-tarot.txt.)
