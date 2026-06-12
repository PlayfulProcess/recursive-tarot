# Proofing Protocol — from deck grammar to sellable print product

*One pipeline, used twice: the sampler proves it physically, then the identical
pipeline bakes the full product. If the proof looks right, the product IS right.*

## The pipeline (shared, single source of truth)

All card processing lives in `scripts/tgc_card.py` — never duplicate resize logic:

| Step | What | Set |
|---|---|---|
| autotrim / content_crop | strip scan margins (density crop for wide stock) | `TIGHT_TRIM` |
| blend_frame | canvas colour sampled from clean corners (cream-stock decks) | `BLEND_FRAME` |
| **flood** | flood-fill border-connected scan background (white lightbox / black velvet), repaint with the canvas colour — bg and bleed become one colour, seam impossible | `FLOOD_BG` |
| border_fit | fit inside TGC trim (800×1395) on the 900×1500 canvas | — |

**FLOOD_BG is opt-in and visually verified** — on open line art the flood leaks
through the engraving into the artwork. Run `scripts/detect_flood_bg.py --preview
<dir>` on any new deck and LOOK at the before/after before adding it to the set.

## Steps for a new deck

1. **Ingest** — deck grammar with `image_url`s (R2 or stable archive; never
   Commons hotlinks — `scripts/migrate_covers_to_r2.py` if needed).
2. **Flood audit** — `python scripts/detect_flood_bg.py --preview print/flood-preview`,
   inspect flagged before/afters, update `tgc_card.FLOOD_BG`.
3. **Sampler** — `python scripts/build_sampler_v6.py` regenerates the full proof
   deck: cards grouped per deck by (print-quality stamp, source host); one
   representative per group, so split-quality decks (e.g. Etteilla III print
   majors / web minors) contribute one card from EACH group. High-res IIIF decks
   re-pull print masters per card. Output + `manifest.json` in
   `print/decks/sampler-v6-tgc/`.
4. **Upload & physical proof** — `scripts/tgc_upload_deck.py` (TGC creds in
   gitignored `print/env-local.txt`); order ONE copy. **Nothing sells before the
   builder holds the physical proof.**
5. **Product bake** — proof passed → `python scripts/prebake_deck_r2.py <slug>`
   (identical pipeline incl. flood) writes 900×1500 print masters to R2
   `grammar-illustrations/print/<slug>/` and stamps `metadata.print` per card.
6. **Go live** — create the TGC product from the prebaked R2 files, paste
   `product_url` + `status: live` into `print-products.json`. The shop page reads
   it automatically. ≥90% print-quality required for an unbadged listing.

## Re-bake required (June 2026)

The R2 print prebakes for the FLOOD_BG decks predate the flood fix. Before any of
these go live, rerun `prebake_deck_r2.py` for: charles-vi, paris-anonymous, este,
madiao, mantegna, sola-busca, noblet, visconti-sforza, cary-sheet, rosenwald-sheet.

## Future: recursive.eco user decks

The same pipeline is the engine for "print your own grammar": user picks items →
Worker (holds the TGC secret, `NEXT-SESSION-DELEGATION.md` §O3) pulls the prebaked
R2 masters (or bakes via this pipeline) → TGC checkout. The sampler protocol then
doubles as the per-grammar quality gate before offering print.

## Standing rules
- PD-or-CC-BY only for print (never NC).
- Proof-first: physical proof in hand before anything sells.
- No credentials in chat or commits.
