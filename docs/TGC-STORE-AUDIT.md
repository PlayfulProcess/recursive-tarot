# TGC Store Audit — resolution, back design, staged products

Written 2026-07-29, after the physical proof cards arrived. Answers three
things: which decks are safe to sell as printed tarot decks, what the new
card back is and how its symmetry was verified, and what got staged as TGC
drafts (and what didn't, and why).

Method: `scripts/tgc_card.py`'s own floor (`PRINT_MIN = 800px` short side of
the *source* image, before it gets fit into the 900×1500 canvas) is the
pipeline's existing bar for "print" vs "web" quality — it's what
`prebake_deck_r2.py` has already stamped onto `metadata.print` for several
decks from earlier sessions. This audit reuses those stamps where they cover
every real card in a deck (trustworthy — computed by the same code, on the
same source URLs), and does a **fresh 6-image sample + PIL measurement** for
every deck that wasn't fully stamped, or where the stamp looked surprising
enough to double-check. Raw sample data: scratchpad `audit_results.json`
(not committed — regenerate with the script described below if needed).

Classification (tightened beyond the pipeline's bare pass/fail, because the
ask was "highly confident," not "technically over the line"):
- **PASS** — min short side (across sampled/stamped cards) ≥ **900px** (TGC's
  own face width) — comfortable headroom, no upscaling at all.
- **MARGINAL** — 780–899px, or a deck with a mixed print/web split — clears
  or nearly clears the pipeline's 800px floor but without real headroom.
  Not staged as a draft automatically; listed for your call.
- **FAIL** — under 780px short side, or a genre that isn't tarot.

## Tarot decks — resolution table

| Deck | Cards | Min short side (sample) | Source | Class | Note |
|---|---:|---:|---|---|---|
| **golden-dawn-book-t-tarot** | 78 | 1090 (median 1112) | prior full stamp | **PASS** | Flagship — already has a TGC product (see below), and it's the one you already hold a physical proof of. |
| **minchiate-florence-tarot** | 97 | 1405 (median 1429) | prior full stamp | **PASS** | Largest deck (97 cards incl. extra trumps) — highest resolution of the set. |
| **paris-anonymous-tarot** | 78 | 1100 (uniform) | prior full stamp | **PASS** | IIIF re-pull at bake time — very consistent. |
| **vieville-tarot** | 78 | 1100 (uniform) | prior full stamp | **PASS** | Same IIIF pipeline as Paris. |
| **etteilla-ii-egyptian** | 78 | 2239 (median 2423) | prior full stamp | **PASS** | Highest-res deck in the library by far. |
| **este-tarot** | 16 | 1100 (uniform) | prior full stamp | **PASS** | Historical fragment — only 16 surviving cards, not a full 78. Sell explicitly as a partial/collector deck. |
| **tarocchino-arlecchino** | 62 | 900×1500 exact, all 6 sampled | fresh sample | **PASS** | Modern deck (see attribution note below) — art was supplied already at TGC's exact target size, so nothing to upscale or crop. |
| **arlecchinos-augmented-arcana** | 84 | 900×1500 exact, all 6 sampled | fresh sample | **PASS** | Same source/attribution as above. |
| oswald-wirth-tarot | 22 | 893 (median 912) | prior full stamp | MARGINAL | Just under the 900px comfort line (~11% margin over the 800px floor). Old plan called it print-ready; I'd want a visual spot-check before selling, so it's not auto-staged. |
| tarot-de-marseille-conver | 78 | 805 (median 814) | prior full stamp | MARGINAL | Every one of the 78 cards sits right at ~805–814px — consistent, but with almost no headroom over the pipeline's own 800px floor. This is the deck I'd expect her to want most (Marseille is the iconic pattern), so flagging clearly: it's *usable* but soft, not comfortable. |
| anecdotes-tarot | 78 | 825 (uniform 825×1125) | fresh sample | MARGINAL | Third-party deck (see attribution). Resolution clears the floor but the **aspect ratio is 0.73, not tarot's 0.6** — fitting it to the 900×1500 canvas means real letterboxing (bars), not just a crop. Needs a look before it goes in the store. |
| etteilla-iii-oracle-des-dames | 78 | 780 (split: 22 cards @ ~1450, 56 cards @ 780) | prior stamp + fresh spot-check | **FAIL (majority)** | Split-quality deck — the majors were rescanned high-res, the minors weren't. 72% of the deck is below the 800px floor. Exclude until the minors are re-sourced. |
| etteilla-i-livre-de-thot | 78 | 780 (uniform) | prior full stamp + fresh spot-check | **FAIL** | All 78 cards below the pipeline's own floor. (Contradicts the June 10 plan doc, which had listed it as printable-bordered — that was before this deck got its own prebake run; trust the newer stamp.) |
| clown-town-tarot | 78 | 747 (uniform 747×1122) | fresh sample | **FAIL** | Just under the floor (~7% short); aspect ratio is close to correct (0.665 vs 0.6) so it's not a bad *shape*, just soft. Worth a higher-res regeneration if this deck matters to you — closest FAIL to the line. |
| sola-busca-tarot | 108 | 474 (uniform 474×877) | fresh sample | **FAIL** | Old Commons hotlink, well under floor. |
| cary-yale-visconti-tarot | 105 | 362–733 (min 362) | prior stamp | **FAIL** | Web-res, as flagged since June. |
| visconti-sforza-tarot | 120 | 362–725 (min 362) | fresh sample | **FAIL** | Web-res. |
| charles-vi-tarot | 18 | 299–318 | fresh sample | **FAIL** | Web-res, severe (under 320px). |
| tarocchino-bologna | 97 | 100–320 (min **100**) | fresh sample | **FAIL** | Some individual cards are literally 100×209px — thumbnail-scale. |
| court-de-gebelin-tarot | 23 | 444–480 | fresh sample | **FAIL** | Web-res. |
| tarot-de-besancon | 14 | 332–736 | fresh sample | **FAIL** | Web-res, inconsistent across cards. |
| belgian-tarot | 23 | 354 (uniform) | prior full stamp | **FAIL** | Web-res. |

### Excluded on genre grounds — not tarot (per your instruction), resolution noted for completeness only

| Deck | What it actually is | Resolution | Verdict |
|---|---|---|---|
| mamluk-deck | Islamic Mamluk playing cards — predates and differs from tarot | 128px min | Excluded — not tarot, and low-res anyway. |
| ganjifa | Indo-Persian round playing cards | one composite plate image (2100×1635), not individual card files | Excluded — not tarot, and structurally not a per-card deck (would need real digitization first). |
| madiao-money-cards | Chinese money-suited cards, tarot's distant ancestor | 1000px min (actually PASSES resolution) | Excluded — genuinely not tarot, regardless of the good resolution. |
| mantegna-tarocchi | 15th-c. educational engraving series, historically miscalled "tarocchi" but not a tarot deck (no suits/trumps structure) | 960px min (PASSES resolution) | Excluded — the project's own docs already call this "not a game, not a tarot." |
| petit-lenormand | 36-card Lenormand cartomancy oracle — a different, later card system | not sampled (excluded on genre before resolution) | Excluded — the deck's own description says "distinct from the tarot proper." |
| cary-sheet, rosenwald-sheet, noblet-tarot | Single uncut historical printer's sheets, one image each | n/a | Excluded — not individually-printable card sets as they stand (each is ONE image of a whole sheet, not 78 separable card files). Genuinely important historically; not a store product without real per-card digitization work. |
| ontoject-illustrated | Original PlayfulProcess "existential tarot" concept sequence | 1024×1536 min (PASSES resolution) | Excluded — not suit/trump structured like a playable tarot deck; it's a 24-item conceptual sequence, not a 78-card deck. Resolution is fine if you ever want to print it as something else (art book plates, a small oracle). |
| tree-of-tarot | Meta/reference grammar (genealogy diagram, not cards) | n/a | Excluded — not a deck at all. |

## Third-party decks — attribution matters if these go on sale

`tarocchino-arlecchino`, `arlecchinos-augmented-arcana`, `anecdotes-tarot`,
and `petit-lenormand` are **not PlayfulProcess originals** — all four are by
**Yve Lepkowski (stolen-thyme.com)**, released CC-BY-SA-4.0. CC-BY-SA permits
commercial resale, but the share-alike license requires real attribution to
the actual creator. The two staged products below (Tarocchino Arlecchino,
Arlecchino's Augmented Arcana) carry a description crediting Yve Lepkowski by
name — **never presented as a PlayfulProcess original**. `ontoject-illustrated`
is a genuine PlayfulProcess original but wasn't staged (see table above).

## The new card back — mathematically 180°-symmetric

**File:** `print/backs/back-symmetric-spiral-900x1500.png` (lossless master)
and the `.jpg` sibling used for the actual TGC upload. Also registered in
`print/card-backs.json` as `back-symmetric-spiral`, and rehosted to R2 at
`grammar-illustrations/card-backs/back-symmetric-spiral.jpg` (same pattern as
every other back in that file) so the print viewer can offer it as a choice.

**Design:** the repo's own golden-ratio logarithmic spiral (`public/spiral/`
uses the same formula, `r = a·e^(bθ)` with `b` tied to `φ`), in `--gold`
(`#9a7322`) on `--ink` (`#221f1a`), inside a double gold rule frame, with a
small dot lattice for texture and beaded nodes along the spiral arm — same
visual language as the site (`theme.css` tokens), no new palette invented.

**How the symmetry is guaranteed, not just eyeballed:** the design is drawn
*only* in the top half of the 900×1500 canvas (rows 0–749). The bottom half
is then produced as `top_half.rotate(180)`, pasted directly below. That
construction is exact for any content in the top half — for every pixel
`(x, y)`, `full(x, y) == full(W-1-x, H-1-y)` by the way the two halves are
built, not by symmetric-looking brushwork. **Verified**: `full.rotate(180)`
diffed against `full` via `PIL.ImageChops.difference` — `bbox = None`,
`extrema = ((0,0),(0,0),(0,0))` on the lossless PNG (bit-for-bit identical).
The JPEG export (used for the actual upload) reintroduces a small amount of
compression-only noise on re-diff (mean delta ≈0.3/255, invisible, doesn't
touch the design's actual symmetry) — the PNG is the artifact that proves
the claim; the JPEG is a practical export of it. Frame sits at an 84px
margin — inside TGC's 750×1350 safe zone (which starts at 75px) with a
buffer, so cutting variance can't crop it unevenly. No stroke is under 3px
(≈0.01in at 300dpi) — nothing "hairline."

Regenerate/tweak with `python scripts/make_symmetric_back.py` — it re-derives
both files and re-asserts the symmetry check on every run (fails loudly if a
future edit breaks it).

## Composition spec — art-fill, so this never regresses

Builder caught this from her physical proof: her printed **Justice** card
(sampler deck `E25631D6`) fills the card properly; the freshly-staged
**Golden Dawn "The Fool"** showed the art floating small inside a huge
cream margin. Root cause found and fixed 2026-07-30.

**The one correct pipeline** (`scripts/tgc_card.py` → `border_fit()`, used by
both `prebake_deck_r2.py` and `build_sampler_v6.py` — this is *why* the
sampler prints correctly, and the spec every future face upload must match):

1. Canvas is **900×1500** (TGC bleed spec). Trim/cut line is **825×1425**,
   safe zone is **750×1350**, all centered.
2. `autotrim()` (or `content_crop()` for `TIGHT_TRIM` decks) strips the raw
   scan's own margin first.
3. The trimmed card is scaled to fit **fully inside `FIT = (800, 1395)`**
   — i.e. **~89% of canvas width / ~93% of canvas height** — preserving
   aspect, never cropping the card's own printed frame.
4. It's pasted centered on the 900×1500 canvas, filled with a **sampled
   border colour** (corner colour for `BLEND_FRAME` decks, edge-ring median
   otherwise, or the flood-filled card-stock colour for `FLOOD_BG` decks) —
   never plain white — so the added margin reads as a continuation of the
   card's own frame, not a mismatched box.

**What actually went wrong:** the Golden Dawn deck's 78 card faces were
uploaded to TGC on **2026-06-10**, before this pipeline existed in its
current form (`prebake_deck_r2.py`'s R2 masters and `metadata.print.tgc_url`
came later). That original upload fit the art far smaller than the `FIT`
box above — visually closer to 60–65% of the canvas instead of ~89%/93% —
so it sat on TGC untouched through every later session, including this
one's initial staging pass (which only updated the *back*, correctly
assuming the faces were already fine — they weren't; they were just old).
The 7 newly-created products never had this problem: they were built fresh
from the current `metadata.print.tgc_url` R2 masters (or, for
`tarocchino-arlecchino` / `arlecchinos-augmented-arcana`, native art that's
already exactly 900×1500 — no `border_fit` needed at all).

**Fix applied:** re-baked nothing new (the R2 masters were already correct)
— downloaded the current `tgc_url` for all 78 Golden Dawn cards and, for
each *existing* TGC card object, `PUT /card/{id}` with a freshly-uploaded
`face_id` (matched card-by-card via name, not a create-new pass, so no
duplicate cards were introduced). Verified via TGC's own preview image
before and after on "The Fool" (visibly fixed — art now fills to the `FIT`
box, matching the sampler's Justice) — see `stage_results` / chat for the
before/after preview URLs. All 78 faces replaced; `has_proofed_face` reset
to `0` on each (expected — she'll need to re-run Proof All before ordering).

**Verified clean on spot-check** (all match the sampler's fill ratio):
paris-anonymous-tarot, etteilla-ii-egyptian, vieville-tarot,
arlecchinos-augmented-arcana. Every other staged deck (minchiate,
etteilla-ii, este, tarocchino-arlecchino) was built the same way as these
four, so treated as clean without a separate check on every single card.

**Standing rule:** any future TGC card-face upload — new product or update
— must come from `metadata.print.tgc_url` (or a fresh `border_fit()` bake if
that's stale/missing), never from an ad-hoc local folder or an older
one-off script's output. If a deck's `tgc_url` predates a `tgc_card.py`
change, re-run `prebake_deck_r2.py <slug>` before uploading.

## Staged TGC products (drafts — nothing published, nothing purchased)

All confirmed `public: 0` (private draft) via a read-only account listing on
2026-07-29. Edit link pattern: `https://www.thegamecrafter.com/make/games/<game_id>`.

| Deck | Game id | Deck id | Cards | New back? |
|---|---|---|---:|---|
| golden-dawn-book-t-tarot | `C07782A2-645A-11F1-87B8-CDFD42BF08F6` (existing, updated) | `27B3B844-64E4-11F1-9D82-EA4366E3122E` | 78/78 | yes — replaced the old Napoletane back |
| minchiate-florence-tarot | `795691FC-8B78-11F1-84DD-ECC0EC690B95` | `7BC6D000-8B78-11F1-84DD-0AC1EC690B95` | 97/97 | yes |
| paris-anonymous-tarot | `2B767F64-8B79-11F1-964F-71BB2FE3B2B9` | `2D207608-8B79-11F1-84DD-A2C8EC690B95` | 78/78 | yes |
| vieville-tarot | `BBF41A2E-8B79-11F1-964F-FEC22FE3B2B9` | `BDCC6A0E-8B79-11F1-B8B4-AA9440A950E6` | 78/78 | yes |
| etteilla-ii-egyptian | `49F36F0A-8B7A-11F1-964F-C2C92FE3B2B9` | `4BA0B920-8B7A-11F1-964F-CDC92FE3B2B9` | 78/78 | yes |
| este-tarot | `45E377D6-8B78-11F1-B8B4-9E8340A950E6` | `477CF7FC-8B78-11F1-B8B4-A08340A950E6` | 16/16 | yes |
| tarocchino-arlecchino | `D66048DC-8B7A-11F1-9B66-4CF3DFA4E030` | `D8BF8548-8B7A-11F1-B8B4-BAA240A950E6` | 62/64 (2 significators excluded — broken source images, see below) | yes |
| arlecchinos-augmented-arcana | `44C11036-8B7B-11F1-B8B4-3FA840A950E6` | `46A59FE8-8B7B-11F1-9B66-A3F8DFA4E030` | 84/84 | yes |

All 8 use the same uploaded back file (`file_id 78A97A8A-8B78-11F1-84DD-DEC0EC690B95`
for the 7 new ones; Golden Dawn's own upload got its own file id since it was a
separate PUT call). `has_proofed_back` was reset to `0` on every deck touched
(new back means the old digital proof no longer applies) — each needs a fresh
**Proof All** pass in the TGC UI before it can be ordered or published; see the
walkthrough in chat.

**Known gap:** `tarocchino-arlecchino`'s two Significator cards
(`significator-62`, `significator-63`) have corrupted/truncated source images on
R2 (9.6KB, ~220×405px, fails to decode) — excluded from this print run rather
than uploading broken art. Flagged as a separate background task
(`task_d7e2ac52`) to re-source and re-upload; once fixed, re-run the upload for
just those two cards and the deck goes from 62 to the full 64.

MARGINAL decks (oswald-wirth-tarot, tarot-de-marseille-conver,
anecdotes-tarot) were **not** staged — see the table above for why, and
what would need to happen (a spot-check, or a re-source) before they're
store-ready.
