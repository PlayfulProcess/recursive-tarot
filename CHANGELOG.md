# Changelog

Newest first. One bullet per shipped thing.

## Jun 12 2026

- **S3: 6 hidden ancestor decks surfaced** — mamluk-deck, ganjifa, sola-busca-tarot, noblet-tarot, cary-sheet, rosenwald-sheet added to `_collection.json`; new "ancestors" branch; collection 20 → 26 decks
- **S4: Explorer wired into homepage** — "⊞ Explorer" card added to the "More ways in" grid on index.html (header + view-switcher already had it)
- **S5: Shop expanded** — vieville-tarot and paris-anonymous-tarot (both 78/78 print-ready, 94%) added to print-products.json as coming-soon entries
- **S6: favicon + og tags** — gold spiral SVG favicon + og:title/description/url on index.html
- **Plan: Fruits of the Tree** — integration ladder doc (L0–L4 tree↔fruit identity/AI/data/commerce) pushed by Fable session
- **POD: print masters re-baked** — vieville 78/78, paris 78/78, este 16/16, mantegna 50/50 print-ready (Gallica/Yale high-res)
- **Explorer: branch colour fix** — Belgian pill colour restored (order→branch→violet fallback)
- **Explorer: emergence pills surface first** — pills label the cell; cards shown behind +N count

## Jun 11 2026

- **Explorer v2** — trace ⬆⬇ relationships, branch-coloured level-gradient pills, deck multiselect
- **Explorer v1** — drag-drop pivot over the full card collection (Emergence Explorer); design doc + delegation plan
- **Header: views vs tools** — nav reorganised into ◫ views group (Cards, Explorer, Tree of Life, Timeline, Tree, Genealogy) + tools group (Caster, Course, Shop, GitHub)
- **Genealogy re-architecture plan** — keyword-in / emergence-out engine; derives_from edge map; Supabase/webhook runtime design (HANDOFF-rearchitect-genealogy.md)
- **Sampler v5** — density content-crop (TIGHT_TRIM) for wide-margin cream-stock decks; always re-process from source
- **DRY: BLEND_FRAME** moved into tgc_card.py — deck-product bakes match the sampler automatically
- **Sampler: frame-blend mode** — corner-sampled bleed for 7 cream-stock decks; eliminates white/black contour seam

## Jun 10 2026

- **Shop: Full Sampler v5 pushed to TGC** (deck ED62C786) — ready to proof
- **R2: 7 card backs rehosted** — stable URLs, no more Commons 429 on backs
- **Sampler: 19 decks covered** + high-res re-pull for Gallica/Yale decks
- **Webhook: Supabase←GitHub live** — grammar changes reindex Supabase automatically
- **Docs: EMERGENCES.md** — cataloguing model (keywords in, emergences out)

## Earlier (Jun 2026)

- Anonymous Parisian Tarot de Marseille (BnF, 17th–18th c.) — 78 cards
- d'Este Tarocchi (Ferrara, c.1450) — 16 cards via Yale Beinecke
- Belgian/Vandenborre Tarot Flamand (Brussels, c.1780) — 22 majors
- Jacques Viéville Tarot (Paris, c.1650) — 78 cards from BnF/Gallica
- Ma Diao Chinese money-suited cards — 12 Skokloster survivors
- Shop page + TGC API upload flow proven
- Course-viewer ported from recursive.eco
- Print-viewer (Grid / Booklet / Memory / Storyboard / Story layouts)
- Caster: Import cast (load exported .json, re-render spread)
- Timeline: proportional time axis + branch lanes
