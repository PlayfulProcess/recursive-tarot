# Next Sessions Plan — split by model (rev. 2, June 10 2026)

**Revised strategy (builder's directive):** Do NOT print a whole deck, and do NOT
use the API-built test decks as the proof. Instead:
1. **Build every PLANNED deck** as a real library grammar (honest history + the
   best available public-domain images, even if fragmentary).
2. **Then** assemble ONE "1-card-per-deck" sampler spanning EVERY deck (built +
   planned) and print THAT single deck as the workflow proof — so the resize /
   margin / print settings are tested for every deck's image at once.

Context docs: this file, `print/SHOP-PLAN.md`, `print/HOW-TO-PRINT.md`,
recursive-eco `docs/future_plan/print-on-demand-pipeline.md`.

---

## THE BOTTLENECK (why this is Opus work, not a quick Sonnet job)
The 8 planned decks are gated by **image provenance**, which only careful judgment
can clear. From a June 10 Commons hunt (`plan/PLANNED-DECKS-IMAGE-HUNT.md`):

| Planned deck | Commons PD images? | Print-res? | Note |
|---|---|---|---|
| **Brera-Brambilla** | ✅ yes, 15th-c PD | ~954×1921 (some) | BUILD FIRST — genuine PD, decent res |
| Tarocco Siciliano | partial, low-res PD | ✗ tiny | display-only stub; fragments exist |
| Tarocco Piemontese | tiny PD scans | ✗ 120×211 | **living deck — modern scans are COPYRIGHTED**; only pre-1900 PD usable |
| d'Este (Ferrara) | ✗ catalogs only | ✗ | image-blocked; fragmentary (~16 cards survive) |
| Soprafino (1835) | ✗ none found | — | exists but **Lo Scarabeo "Ancient Italian" reproduction is COPYRIGHTED**; need original Della Rocca scans (Gallica/museum) |
| Ancient Lombardy (1810) | ✗ none found | — | Gumppenberg; original PD but not on Commons under these terms |
| Belgian / Vandenborre | ✗ none found | — | try Gallica/BnF |
| Marseille Type I (Noblet/Dodal) | noblet already BUILT | — | this planned node is largely redundant with `noblet-tarot`; decide: merge or repurpose to "Dodal 1701" |

**Implication:** "build all planned decks fully" isn't a fast mechanical job — half
of them need deep sourcing from museum/library digital collections (BnF Gallica,
Beinecke, World of Playing Cards, un-searched Commons categories) AND copyright
judgment (PD original vs. modern reproduction). That sourcing + the house-style
historical writing is the Opus work. Where no clean PD scan exists, the deck still
becomes a real grammar entry with honest history and a "fragmentary / no surviving
high-res scan" note (a catalogue stub), so it appears in the library and the
genealogy even before it has full card art.

---

## OPUS SECTION (judgment, research, writing — only Opus)

### O0. (DONE this session) Historical-claims audit + fixes
Did the integrity pass FIRST (correctness before count): `research/AUDIT-historical-claims.md`
written; FIX-NOW + clear HEDGE items applied to grammars (visconti-sforza title:
"Oldest" → "Oldest Near-Complete" + "attr. Bembo"; noblet: "oldest TdM" → "oldest
surviving *complete* TdM *deck*", with a Cary-Sheet distinction; oswald-wirth:
"first overtly occult deck" → "first occult/initiatic instrument, distinct from
Etteilla's 1788 divination deck"). Meta regenerated. STILL OPEN (need source check):
mamluk "43 vs 48" survivor count; golden-dawn RWS-is-Waite's-adaptation clause;
full per-card occult-projection pass on game decks.

Also surveyed planned-deck image availability (table above) — image sourcing is
the real bottleneck; no planned deck was *built* this session (building one with
wrong provenance is worse than not building it — see O1).

### O1pipeline. ✅ PROVEN: the Gallica → contact-sheet → build pipeline
Built **Jacques Viéville (Paris c.1650)** end-to-end from BnF/Gallica
(`tarot/vieville-tarot/`, 78 cards, named trumps + 4 suit groups, live). The
reusable method for any Gallica-digitised deck:
1. IIIF manifest `…/ark/manifest.json` → count canvases (often face/back pairs:
   odd = faces, even = patterned backs).
2. Download faces `…/ark/f{N}/full/600,/0/native.jpg` → `tarot/<slug>/images/cNN.jpg`.
3. **Contact-sheet card-ID** (PIL montage of all faces → one image → Read it):
   identify trumps by their printed numerals + suits by symbol, in ONE-few views
   instead of N. (scripts/build_vieville.py + the montage snippets show how.)
4. Commit images → served by Pages (robust CDN; Commons/weserv throttle concurrent
   grids — see Ma Diao). Add to `_collection`. Honesty note in the grammar for any
   best-effort pip-rank assignments.
This same pipeline is the cleanest path for the remaining planned decks that are
on Gallica/BnF (Noblet's other sibling the anonymous Parisian `btv1b105109624`;
Belgian/Vandenborre if locatable; possibly Soprafino/Lombardy at museum sites).

### O1. Source + build the remaining planned decks (the core work)
**Status (June 11):** ✅ **Viéville** (Gallica, 78), ✅ **Belgian/Vandenborre** (Commons
'Tarot Belgijski' PD set, 22 trumps, 22/22 imaged), ✅ **Anonymous Parisian Tarot**
(Gallica btv1b105109624, 78 named cards) — the three early Parisian tarots
(Noblet + Viéville + Anonymous) are now all in the library. Ma Diao ✅ too.
**✅ d'Este UNBLOCKED (June 11)** via **Yale Beinecke / Cary Collection** (the same
archive as our Cary Sheet + Cary-Yale): `collections.library.yale.edu`, IIIF v3
manifests, open access, museum-res. d'Este = 16 surviving cards at 3256×5640,
named from Yale's own catalogue. **Yale is the unblock pathway** — its catalog API
(`/catalog.json?q=`) + manifests (`/manifests/{oid}`, IIIF v2 image API
`/iiif/2/{id}/full/{w},/0/default.jpg`) hold the early Italian hand-painted decks.
KEY LESSON: when Commons/Gallica are dry, **hunt the holding institution directly**
(Yale Beinecke, British Museum, Pinacoteca di Brera) — planning doesn't unblock,
sourcing does.

**Still blocked — and now with the reasons nailed down (June 11 hunt: Met API +
Commons Italian/BM terms both 0):**
- **Soprafino / Lombardy / Siciliano / Piemontese** — NOT on any queryable open-PD
  archive (Commons, Gallica, **Met Museum open API**, Yale Beinecke all dry). The
  originals are PD (pre-1900) but **no institution has released clean PD scans**.
- **Brera-Brambilla** — physically at Pinacoteca di Brera (Milan), not openly digitised.
- ⚠️ **LICENSE TRAP for the print goal:** the **British Museum** *does* hold these
  decks, but released its images under **CC BY-NC-SA 4.0** — **Non-Commercial**.
  That's usable for the free educational library (display) but **NOT for printed
  products you sell**. So BM is a dead end for the shop track; only use it (if at
  all) for display, clearly flagged. World of Playing Cards claims rights on its scans.
- **Conclusion:** d'Este was the only one of the six with an accessible,
  print-compatible PD source. The other five are genuinely blocked — leave as
  catalogue stubs / future digitisation, do NOT fake. Print-compatible images must
  be **PD or CC-BY / CC-BY-SA — never NC**.
For EACH remaining planned deck, in priority order:
1. **Source PD images** with provenance judgment — confirm PD (pre-1900 / museum
   PD release), NOT a modern reproduction. Try, in order: Commons categories
   directly (not just search), BnF Gallica (gallica.bnf.fr), Beinecke (Yale),
   World of Playing Cards (wopc.co.uk), Trionfi.com. Record source + license per
   image.
2. **Write the grammar** in house style (model on `mamluk-deck` / `ganjifa` for
   fragmentary/ancestor decks, full decks on `tarot-de-marseille-conver`):
   evidence-first, hedged claims, framed in its OWN tradition, no occult
   projection onto game decks.
3. Add/repurpose its node + derives-edge in `tarot/tree-of-tarot/grammar.json`;
   add to `_collection.json` like the others.
4. Where images are missing, ship a catalogue stub (history + "no high-res PD scan
   located yet") rather than a fake.
Priority: Brera-Brambilla (done) → d'Este → Soprafino → Lombardy → Siciliano →
Piemontese (PD-only) → Belgian → resolve Marseille-Type-I node.

### O1b. Ancestors line — Ma Diao (Chinese money cards) — ✅ DONE
Built `tarot/madiao-money-cards/grammar.json` (18 items, 12 PD Skokloster scans),
house-style "deep root, not a parent" framing, added to `_collection` (branch:
ancestors), live. `scripts/build_madiao.py`. NOTE: the tree-of-tarot has NO
ancestors layer (mamluk/ganjifa aren't tree nodes either), so Ma Diao was added as
a discoverable DECK but intentionally not a trump-genealogy node. FOLLOW-UP idea
(Opus): add an "ancestors" cluster to the tree (Ma Diao + Mamluk + Ganjifa as deep
roots) AND add the 6 built-but-uncollected ancestors (mamluk, ganjifa, sola-busca,
noblet, cary-sheet, rosenwald) to `_collection` so they're discoverable too.

### O2. Historical-claims audit + fixes (integrity pass)
The audit agent died on the token limit. Redo it directly (no subagent). Audit
every `tarot/*/grammar.json` name/description/sections + `index.html`:
- **KNOWN, FIX NOW:** Visconti-Sforza titled "The Oldest Tarot (c. 1451)" while our
  own Cary-Yale is ~1442–45 and Brera-Brambilla ~1442–47 — self-contradiction.
  Reword to "among the earliest surviving" / cite the genuine dating debate.
- Hedge all absolutist claims (house rule); flag debated attributions stated as
  fact (Bembo; "Charles VI" must read as a misnomer for an Italian c.1475–1500
  deck; Mantegna misnomer; golden-dawn deck = 1909 RWS imagery, NOT the Golden
  Dawn's own deck — verify framed honestly); prefer "c." dates; ensure no game
  deck presents divinatory meanings as native.
Write `research/AUDIT-historical-claims.md` (table: deck | quoted claim | problem |
rewording | severity), then APPLY fix-now + hedge edits, regen meta, commit, push.

### O3. Homepage clarity pass — ✅ DONE
`index.html` now leads with a "Start here" 3-action strip (Browse the decks / Pull
a reading / Print a deck → shop), Shop is linked, "grammar" is glossed in the repo
card, lede is plainer. History + misconceptions kept.

### O4. Vendor synthesis (business judgment)
The deep-research run's "all refuted" output is a TOKEN-LIMIT ARTIFACT (verifiers
died 0-0), NOT real. Unverified-but-useful: QPMN (QP Printing, Hong Kong) markets
an API + MOQ-1 tarot POD + Shopify split-fulfillment but tiny adoption / partly
manual orders; MPC confirms MOQ-1 POD + per-card images + 2–3 day production but
web-UI only, no public API. TGC API is PROVEN (US, hosted checkout). Verify QPMN's
actual API docs + MPC reseller program, then pick the worker's vendor; update
`SHOP-PLAN.md` §5. Brazil = domestic-only candidates (Fábrica de Tarot etc.).

---

## SONNET SECTION (mechanical — run AFTER Opus delivers verified grammars)

### S1. Package each new deck for print
For every deck Opus builds: `download_deck_images.py <slug>` →
`resize_for_tgc.py print/decks/<slug>` (border mode) → `stamp_print_metadata.py`
audit → regen meta (`build_meta_grammar.py`) → confirm it's in `_collection.json`
→ push. (Skip print packaging for catalogue-stub decks with no usable images.)

### S2. Build the comprehensive "1-card-per-deck" SAMPLER (the proof)
Extend `scripts/build_sampler.py` to include ONE representative card from EVERY
deck in the library (built + newly-planned), labelled, plus the historical backs.
This is the single deck the builder prints to test the workflow across all decks.
Output `print/decks/sampler-tgc/`.

### S3. Site polish
favicon (gold spiral SVG + `<link rel=icon>` on all pages); og:title/description
/image on index + shop; swap shop cover URLs from slow Commons to R2-hosted
first-card images.

### S4. (when builder re-adds TGC_PASSWORD) push the sampler via API
`tgc_upload_deck.py` into a fresh game "Recursive Tarot — Print Sampler v2".
Builder then proofs + orders ONE copy. Nothing else publishes.

### S5. Disk cleanup
After uploads: delete `print/decks/*-tgc/` (regenerable; machine disk-tight).

---

## Standing rules
- Push recursive-tarot freely (free Pages). recursive-eco docs: commit LOCAL only.
- Meta-rebuild Action auto-pushes "chore: rebuild meta-grammar" → on conflict:
  `git pull` + `git checkout --ours tarot/all-decks-many-lenses/grammar.json` + regen.
- No credentials in chat/commits; `env-local.txt` gitignored (password currently
  removed by builder — re-add the TGC_PASSWORD line only when running an API upload).
- House style: hedge all claims; each deck in its own tradition; PD images only,
  with attribution + source recorded; "PlayfulProcess" in public content.
- **Proof-first:** nothing sells before the builder holds the physical proof.
- **Copyright trap:** many historical decks have COPYRIGHTED modern reproductions
  (Lo Scarabeo, Modiano, US Games). Only the pre-1900 originals are PD. Verify
  every image's actual age/source — this is the #1 thing Sonnet must NOT guess.
