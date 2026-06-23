# Recursive Tarot — changelog

Newest first. One line per shipped item; reference the TODO id when there is one.
Open work lives in [TODO.md](TODO.md).

## 2026-06-23

### Tracking + this session's later pass (in progress)
- Created `plan/TODO.md` + this changelog so nothing is dropped (per request to log everything).
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
