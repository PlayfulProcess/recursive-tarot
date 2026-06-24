# Recursive Tarot — changelog

Newest first. One line per shipped item; reference the TODO id when there is one.
Open work lives in [TODO.md](TODO.md).

## 2026-06-24

- **Tarocchino (TG-DECKS):** the deck dropdown is no longer 3 hardcoded slugs — it now discovers every tarot-branch deck in the index (_collection.json) that actually builds a full 62-card pack, and lists all 9 (Cary-Yale, Etteilla I/II/III, Golden Dawn, Minchiate, Sola Busca, Marseille, Visconti). Self-correcting: a new complete deck appears automatically; fragments are excluded.

- **Tarocchino (TG-TRUMPNUM):** the rules now state that Tarocchino trumps carried no printed numbers (we add the A-order rank for convenience), with a **See all 22 trumps** button that opens a popup rendering every trump in full — image + number — sorted low->high, the four Moors sharing rank 2, the Matto shown as the Excuse star. Verified: 22 cards, numbers correct.

- **Tarocchino (TG-PEEK):** a Peek checkbox reveals the opponents' hands as small face-up cards (trump # in the tooltip) so you can verify the AI only plays legal cards. Off by default; toggles cleanly back to card backs. Verified: 45 backs <-> 45 face-up cards.

- **Tarocchino (TG-AI):** opponents got smarter so the human stops winning every hand — on a point-rich trick they win HIGH when not last (so a later seat cannot overtake cheaply), feed a sure-winning partner their highest point card when last, and lead a low trump when trump-heavy to pull trumps. Added a **Harder opponents** toggle (default on; uncheck for the gentler original). The AI only ever returns cards from legalMoves, so it cannot play illegally; a full hand resolves with no console errors.

- **Tarocchino (TG-HANDNUM, TG-LOGNUM, TG-LOGRESIZE):** trumps in hand now show their A-order number (higher wins) as a badge distinct from the honour star; the Play log renders the trump # inline before the name plus a points chip (e.g. "19 The World +5"); and the log is now resize:vertical (taller default) instead of a fixed scroll. Verified in preview.

## 2026-06-23

### Tracking + this session's later pass (in progress)
- Created `plan/TODO.md` + this changelog so nothing is dropped (per request to log everything).
- **Tarot Today figures + image consistency:** used the real Google Trends screenshot — cropped it to a clean **full time-series** and a **recent zoom**, rendered both *below* the built bar charts. Added an honest 'the gap closes' section (in this 5-topic pull tarot is the lowest line and astrology sits above it, but recently the two **converge**; a clean 2-topic pull is the real test). Consolidated the stray `course/img/` into the canonical `pages/courses/images/` (CLAUDE.md documents the one-home/one-convention rule).
- **Tarot Today course — deep enrichment from research/17-contemporary-tarot.txt:** rebuilt into 8 sourced sections (Pew fall-2024 practice numbers, the Trends rescaling caveat, app infrastructure, community adoption, Pamela Colman Smith + Lady Frieda Harris, the two theses — license-to-create AND tarot-as-subjunctive-play with Seligman/Butler + the "oblique" etymology, the honest affordance-vs-timing refinement, and a thin-evidence section). Both real-data figures preserved; research prompt updated.
- **SRC-THUMBS:** sources page prettified — all 9 text-icon tiles now carry public-domain card thumbnails, and a **Tarot Today** tile was added so the list reflects the current library. Image URLs verified 200; usage audit re-run.
- **recursive.eco brand review + logo v2 candidate:** logged `plan/RECURSIVE-ECO-BRAND-REVIEW.md` (the research's bricolage/resignification/found-by-making thesis -> positioning + 'where meaning gets made, by hand, together' + the credit-the-maker principle). Built a v2 logo candidate (`spiral/spiral-v2.svg`: the spiral as a crowd of distinct strokes — many hands, one form) at the bottom of the About page; v1 hero stays live.
- **Tarot Today — Butler/Campbell layer + a bricoleur's bench:** added the Butler *correction* (performativity = compelled citation, not theatrical choice; resignification; the Austin->Derrida->Butler lineage; 'Waite-Smith' as resignification), a 'Found by making' keystone (Campbell's *discovered* vs Butler's *made*, reconciled as found-by-making; 'the discovered erases the maker' ties Smith's erasure to Campbell's universalism), and an essential-readings **bricoleur's bench** (Lévi-Strauss homage) with a frontmatter `maintenance` rule to keep it updated on every revision. Pre-launch checklist gained a Butler-reading homework gate.
- **COURSE-ENDINGS:** added a tailored "Keep digging — and contribute" close (course-specific open questions + a paste-ready Claude research prompt + a contribute link) to history-of-tarot, how-tarot-works, intention-setting, and games-of-the-tarot — matching the pattern set in Tarot Today.
- **QR simplification:** retired Presentation Mode (the per-link QR toggle) and the per-link QRs; kept exactly one **course QR at the top, shown always** (scan to open the course; click to enlarge). Verified: toggle gone, 0 inline QRs, course QR renders.
- **Spiral, corrected (U, round 2):** dropped my hand-rolled init and reproduced the landing EXACTLY — the About hero now uses recursive.eco's placeholder pattern + a verbatim copy of its hero CSS (spiral/hero-spiral.css). The SVG breathes (spiral-size-breath 30s) AND each line animates on its own rhythm: WHY:Sense 36s, HOW:Recursive 22.5s, WHAT:Make Belief 13.5s. The text animations that were missing now render.
- **Purple wayfinding (round 2):** header mark flipped back to purple; recursive.eco/flow.recursive.eco **buttons** render purple (filled + outline, `!important`); the "One branch of a larger tree" spiral links out to recursive.eco.
- **Caster (SB-BTNS, SB-IMPORT):** Re-cast merged into Cast (the Cast button re-casts on repeat clicks); "Import" → "Import Spread".
- **Tarocchino (TG-76):** rules now explain why the target is 76 (all card-points in the pack) and that you win with >38.
- **Tarocchino clarity (TG-TRUMPHL):** the legal-move logic was already correct (on your lead, every card is legal; trumps only highlight when you're void and *must* trump). Rewrote the misleading "play a trump or discard" status into accurate guidance ("void in X, so you must play a trump (highlighted)" vs "void and no trump: play any card") and made the lead message explicit ("no card is forced").
- **Launch checklist (X-CHECKLIST):** added the item to better integrate the local Caster with the recursive.eco Oracle (turn the one-way hand-off into a real bridge).
- **New course (COURSE-TAROT-TODAY):** *Tarot Today — a living question* — the phenomenon, a Google-Trends figure (recreated as inline SVG), the "license to create" hypothesis (meaning attributed later; honouring shadowed artists like Pamela Colman Smith), open threads, and a paste-ready Claude research prompt + contribute link. Establishes the **COURSE-ENDINGS** pattern (open questions → Claude prompt → contribute). Registered in the header Courses menu.
- **Spiral (U):** copied recursive.eco's `spiral/spiral.js` + `hero-spiral.js` **verbatim** (md5-matched). The About-page hero now runs the real recursive.eco spiral — purple `#9333ea`, the building/rebuilding **draw** + breathe + rotate, with **WHY/HOW/WHAT: Sense/Recursive/Make Belief** — at ~4× size (320px). The home ecotree box renders a **static** purple spiral. `spiral-mark.svg` → static purple.
- **Header icon (T):** brand mark → the static **gold** recursive spiral (`spiral-gold.svg`).
- **Purple redirects (X-PURPLE):** every link to recursive.eco / flow.recursive.eco renders in platform purple `#9333ea` (theme.css rule, app-wide) including the **Oracle ↗** item in the header Play dropdown.
- **Play parity (V):** added the poetic opener — *"Tarot has always been play — first a game, then a divination practice or trick, and now a play of sense-making belief"* — and surfaced the course's named mechanisms (conceptual blending, Barnum, cold reading, depth psychology, narrative therapy) on the Play page.
- Answered inline: meta-grammar **can** be the deck index (Q-INDEX); the **>38 of 76** point math (Q-76); the correct **follow→trump→discard** rule (Q-TRUMP-RULE).

### Earlier 2026-06-23 (verified in preview, pushed to `dev`)
- Newsletter footer confirmed working end-to-end: `you@email.com` stored with `subscribed_from='recursive-tarot'`, `subscribed=true`.
- `spiral-mark.svg` rebuilt from recursive.eco's own golden-ratio algorithm (superseded later this session — see TODO note about copying the file verbatim).
- Cards viewer readability: transparent + borderless cards, transparent thumbnail mat, black lighter-weight numbers & names (fixes the Shaiva Tantra deck). Description now shows a full paragraph.
- Footer propagated app-wide (18 pages) + hides itself in embed mode.
- Community grammars (Ontoject, 36 Tattvas): disclaimer — objects of study by PlayfulProcess, may contain errors, contributions welcome.
- About "How to Contribute" → Contribute page; contribute "Create your own" → flow.recursive.eco/create; removed sources' "See the whole collection"; eye icon retired site-wide.
- Play page: course banner moved under the title; added Tolkien/sub-creation lens; "Watch the history" reordered (documentaries first) + a "Contribute a video" course section; "Help keep it alive" rebuilt on Kelty's *recursive public* + Contribute link.
- Header: Contribute tab; Home▾ dropdown → About. Homepage: dropped the redundant Practitioner door; arch rebuilt as a dated, clickable timeline.
- Timeline: year now inline after the title in readable dark gold.
- Consolidated the contributor guide into one course (how-to-contribute); favicon → gold spiral.
