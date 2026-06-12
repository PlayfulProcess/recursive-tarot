# Next-session delegation plan (written June 11 2026, by Fable)

*Hand this file to the model named per section. SONNET tasks are mechanical with
acceptance checks — no historical judgment, no new design. OPUS/FABLE tasks need
judgment. Standing rules at the bottom apply to everything.*

Context docs: `EMERGENCES.md` · `plan/EXPLORER-DESIGN.md` ·
`plan/HANDOFF-rearchitect-genealogy.md` · `print/SHOP-PLAN.md` · `plan/NEXT-SESSIONS.md`.

---

## SONNET — mechanical queue (do in order)

### S1. Verify / finish the high-res print re-bakes
A background run re-baked **vieville-tarot, paris-anonymous-tarot, este-tarot**
(print masters pulled straight from Gallica/Yale via `high_res_url()` in
`scripts/prebake_deck_r2.py`) and retried **mantegna-tarocchi** (Commons 429s).
- Check: `python -c "import json;d=json.load(open('tarot/vieville-tarot/grammar.json',encoding='utf-8'));print(sum(1 for i in d['items'] if (i.get('metadata') or {}).get('print',{}).get('quality')=='print'))"`
  → expect **78** (and 78 paris / 16 este / ~50 mantegna).
- If any deck still shows `web` for cards that should be print: rerun
  `python scripts/prebake_deck_r2.py <slug>` (idempotent) — Gallica needs no auth.
- Then: commit stamped grammars, regen meta (`python scripts/build_meta_grammar.py`),
  push (see conflict rule below).

### S2. R2 migration — display images for the Commons-hotlinked decks
Decks whose `image_url`s still hotlink `commons.wikimedia.org/Special:FilePath`
(rate-limited, slow) must move to R2 like the rest. Likely: mantegna-tarocchi,
sola-busca-tarot, noblet-tarot, cary-sheet, rosenwald-sheet, ganjifa, mamluk-deck,
tarot-de-besancon, court-de-gebelin-tarot, some etteilla. **Audit first**:
`grep -l "Special:FilePath" tarot/*/grammar.json`.
- Tool: `python scripts/rehost_to_r2.py tarot/<slug>/grammar.json --width 1000`
  (already handles 429 backoff; rewrites image_urls to R2).
- **Creds** (gitignored, never echo values): `CLOUDFLARE_ACCOUNT_ID` from
  `../recursive-eco/apps/flow/.env.local`; `R2_ACCESS_KEY_ID`,
  `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME` from `../recursive-eco/.env.local`.
  NOTE: `rehost_to_r2.py:load_env` reads only `recursive-eco/.env.local` — patch it
  to merge the flow env for the account id (copy the `creds()` helper from
  `scripts/prebake_deck_r2.py`).
- If Commons 429s persist, fetch via weserv like `scripts/rehost_backs_r2.py` does.
- Acceptance: `grep -c "Special:FilePath" tarot/<slug>/grammar.json` → 0 per
  migrated deck; spot-check 3 R2 URLs return HTTP 200; regen meta; push.
- Do NOT migrate `cover_image_url`s in `_collection.json` blindly — update them to
  the deck's new R2 first-card URL while you're there (faster shop/collection loads).

### S3. Surface the 6 hidden ancestor decks in the collection
`mamluk-deck, ganjifa, sola-busca-tarot, noblet-tarot, cary-sheet, rosenwald-sheet`
are built but missing from `tarot/_collection.json` (so they're absent from the
explorer/caster/shop pickers). Add entries copying the existing shape
(slug/name/type/branch/is_meta/items/cover_image_url/blurb/path; branch:
"ancestors" for mamluk/ganjifa, "roots" for the sheets, "sui-generis" for
sola-busca... check each deck's grammar `metadata.branch` first and follow it).
Regen meta, push. Acceptance: collection count 20 → 26; decks appear in the
explorer's deck picker.

### S4. Wire the Explorer into navigation
- `site-header.js`: add tab `['explorer','Explore', PFX+'viewers/explorer.html']`
  (match existing TABS shape) and **bump every `?v=6` include to `?v=7` across all
  html files** (grep `site-header.js?v=`).
- `view-switcher.js`: add the explorer entry; same version bump caveat.
- Homepage `index.html`: add an "⊞ Pivot the collection" card in the explore grid
  pointing at `viewers/explorer.html`.
- Acceptance: live check — explorer loads from the header on 3 pages, no
  `[object ShadowRoot]`-style path bugs (root-relative PFX pattern!).

### S5. Shop refresh from real data
`pages/shop.html` lists 8 hand-maintained products. Regenerate its data source
from `_collection.json` + each grammar's `metadata.print` stats: a deck is
"print-ready" iff ≥90% of its cards have `print.quality == "print"`. Show a
LOW-RES warning badge otherwise (user decision: users may print anything, but
warned). Don't publish/sell anything — buttons stay "Coming soon (proofing)" until
the physical proof passes (proof-first rule).

### S6. Housekeeping
- Delete stale regenerable folders: `print/decks/*-tgc/` EXCEPT keep
  `sampler-tgc` (machine is disk-tight; all regenerable from scripts).
- Seed `CHANGELOG.md` at repo root from the last ~3 days of git log (one bullet
  per shipped thing, newest first); add to README docs map.
- `favicon` (gold spiral SVG) + `og:` tags on index/shop (old S3 task).

## OPUS / FABLE — judgment queue

### O1. Explorer v2 (after using v1 — `viewers/explorer.html`)
Per `plan/EXPLORER-DESIGN.md`: extract `explorer-core.js` (flatten/discover/query),
nested column headers, pointer-events drag (mobile), virtualised cells, "open this
cell in cards.html" deep link, saved-pivot presets ("Suits across the centuries",
"Print-ready by deck", "Trumps across orders"). Decide whether Alternative B/C
add anything after real use.

### O2. Genealogy re-architecture
Already specced in `plan/HANDOFF-rearchitect-genealogy.md` (tags in → emergences
out; `derives_from` edge map; regenerate tree-of-tarot; Supabase/webhook runtime
for recursive.eco). The explorer's `flatten()` is the same extraction layer — keep
them one engine.

### O3. Cloudflare Worker (the last new build for print-on-demand)
Browser → Worker (holds TGC secret) → TGC API (session→deck→cards→back, proven in
`scripts/tgc_upload_deck.py`) → checkout URL. Cards come pre-baked from R2
`grammar-illustrations/print/<slug>/<card-id>.jpg` (no image work at order time).
Needs the builder in the loop for: Cloudflare deploy, TGC secret storage, auth/rate
limiting decisions. Pattern exists in `recursive.eco-schemas/mcp-server/worker/`.

### O4. Etteilla III mixed-resolution hunt
22 print / 56 web — find where the 56 low-res cards came from and whether a better
PD scan exists (provenance judgment, copyright trap rules apply).

## BUILDER (user) — your clicks
- TGC: keep **Full Sampler v5**, trash v1–v4 + the old "Print Sampler"; proof v5;
  **order ONE copy**; then remove `TGC_PASSWORD` from `env-local.txt` (and consider
  rotating it).

## Standing rules (apply to every task)
- Meta conflicts: `git pull` → `git checkout --ours tarot/all-decks-many-lenses/grammar.json`
  → rerun `python scripts/build_meta_grammar.py` → commit → push.
- All card processing goes through `scripts/tgc_card.py` (FIT/autotrim/
  BLEND_FRAME/TIGHT_TRIM) — never duplicate resize logic.
- No credentials in chat or commits. PD-or-CC-BY only for print (never NC).
- recursive-tarot pushes freely; recursive-eco commits LOCAL only.
- Proof-first: nothing sells before the builder holds the physical proof.
- Windows console: `PYTHONIOENCODING=utf-8` and ASCII-only prints in scripts.
