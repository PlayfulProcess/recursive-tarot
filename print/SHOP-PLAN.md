# Shop & Print Plan — products, sampler, booklets, ancestors

Logged June 10 2026. The working plan for turning the library into printable
products. Companion docs: `HOW-TO-PRINT.md` (the verified TGC process),
`recursive-eco/docs/future_plan/print-on-demand-pipeline.md` (architecture).

## 0. Test strategy — the SAMPLER deck (first proof order)
One TGC product, ~21 cards, that tests EVERYTHING in a single cheap proof:
- 1 representative card from each of the **8 print-ready decks** (cream-bordered)
- 1 card from each of the **6 web-res decks**, labelled `WEBRES TEST` — so we see
  with our own eyes what low-res prints like (and confirm the exclusion)
- every **historical card back** printed as a face (incl. the low-res Dodal,
  deliberately — same lesson)
Built by `scripts/build_sampler.py` → `print/decks/sampler-tgc/`.
**Order ONE copy of the sampler before anything else.** It answers print texture,
cream-margin blending, stock feel, back choice, and the web-res question at once.

## 1. Per-deck products (the shop shelf)
All 8 print-ready decks have TGC-ready files in `print/decks/<slug>-tgc/`
(900×1500, border mode with sampled-cream margins). Product per deck on TGC,
URL pasted into `print-products.json` → site Buy button goes live.

| Deck | Cards | Margin | Booklet idea |
|---|---|---|---|
| Golden Dawn (RWS art) | 78 | cream | YES — Book T correspondences (grammar already holds them per card) |
| Minchiate | 97 | cream | covered by the shared *Games* booklet |
| Oswald Wirth | 22 | cream | short — Wirth's symbolism notes (grammar sections) |
| Etteilla I / II / III | 78×3 | cream | ONE shared Etteilla-tradition intro (meanings are printed on the cards) |
| Mantegna | 50 | cream | covered by *Games*/education booklet (not a game, not a tarot) |
| Marseille (Conver) | 78 | cream | covered by the shared *Games* booklet |

## 2. Booklets / interpretations — only where meaningful
Principle: don't force a "meanings" booklet onto game decks; that would repeat the
occult-projection mistake the library exists to correct.
- **Golden Dawn booklet** (the real one): per-card Book T correspondences +
  divinatory meanings — already in the grammar sections. Generate from grammar →
  print-viewer Booklet layout → PDF. This deck is *from* a divination tradition,
  so a meanings booklet is honest.
- **"Games of the Tarot" overview** (ONE standalone booklet for all game decks):
  what trionfi/tarocchi/minchiate were as GAMES, basic trick-taking shape, the
  orders (Southern/Eastern/Western), Mantegna as an educational engraving series.
  Write from our research files (facts only, own words — pagat text is copyrighted).
- **Etteilla intro** (one for the 3 decks): the 1788 cartomancy system, how to read
  the printed keywords, upright/reversed.
- Delivery v1: **free PDF + QR/link on the shop page** (zero marginal cost);
  later option: TGC printed booklet component in the same box.

## 3. Ancestors line — "before the tarot" (incl. Chinese)
Goal: PD games that PRECEDED tarot as products/grammars, telling the China →
Islamic world → Europe story (research/00c).
- Already in library: **Mamluk deck** (Islamic suits), **Ganjifa** (Indo-Persian),
  **Cary sheet / Rosenwald sheet** (early European uncut sheets).
- TO BUILD: **Chinese money-suited cards** (yezi / madiao lineage — the earliest
  playing cards). Step 1 is an image hunt: verify Commons/museum PD scans exist at
  usable resolution (the famous Ming-era printed card, Water-Margin money cards);
  build the grammar with the same evidence-first framing; audit for print.
- Sampler v2 can include one ancestor card per deck once built.
- These are primarily EDUCATIONAL grammars; print products only if scans clear
  the 300-DPI audit.

## 4. Shop page (static, this week)
`pages/shop.html` on tarot.recursive.eco: one card per product — cover, year,
blurb, quality badge (full-bleed/bordered), booklet link (print-viewer Booklet
layout), Buy button from `print-products.json` ("coming soon" until URL pasted).
No backend. Lights up product-by-product.

## 5. API / automation (decided so far)
- TGC API verified live; `scripts/tgc_upload_deck.py` ready — waiting on API key
  (TGC: **Account → Apps** — that page IS the API keys; creds go in gitignored
  `print/.env.tgc` or `env-local.txt`, never in chat).
- Test flow locally first (script fills a fresh deck), THEN decide where the
  service sits. Current lean: a **Cloudflare Worker** (lightest deployable unit
  that can hold a secret; no Vercel builds; pattern exists in
  recursive.eco-schemas/mcp-server/worker). recursive.eco integration later =
  the app calls the same worker.
- Deep-research vendor report (worldwide + China + Brazil) pending; re-rank
  vendor choice when it lands. Brazil: domestic POD niche exists (Fábrica de
  Tarot, Fábrica do Baralho, Atual Card, Copag custom) — serves BR buyers
  domestically (import tax avoidance), not a US export base.

## Status checklist
- [x] 8 decks audited print-ready, files built at 900×1500 cream-border
- [x] Sampler deck built (15/21; 6 backs pending a Commons rate-limit retry)
- [x] TGC API probed live + upload script ready
- [ ] TGC API key created (builder: Account → Apps)
- [ ] API test: script fills a fresh Golden Dawn deck
- [ ] SAMPLER proof ordered (builder, 1 copy)
- [ ] Proof inspected → decide: scans as-is vs restoration pass
- [ ] Shop page built
- [ ] Booklets: Golden Dawn, Games overview, Etteilla intro
- [ ] Chinese money-cards grammar (image hunt first)
- [ ] Vendor report → final architecture (worker) → build (2 sessions)
