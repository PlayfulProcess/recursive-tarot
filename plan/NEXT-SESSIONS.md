# Next Sessions Plan — split by model

Written June 10 2026 after hitting the session token limit. Run each section in a
FRESH session with the named model; tell the session to "read plan/NEXT-SESSIONS.md
and do your section". Context docs: `print/SHOP-PLAN.md` (status checklist),
`print/HOW-TO-PRINT.md` (verified TGC process), recursive-eco
`docs/future_plan/print-on-demand-pipeline.md` (architecture).

## State as of this writing (do not redo)
- TGC API flow PROVEN. Two products built via API on the builder's account:
  - Golden Dawn Tarot (API): game `C07782A2-645A-11F1-87B8-CDFD42BF08F6`,
    deck `27B3B844-64E4-11F1-9D82-EA4366E3122E`, 78/78 + back
  - Print Sampler: game `1C2D3BF2-64E5-11F1-9D82-035066E3122E`,
    deck `370F9906-64E5-11F1-9D0E-30818797CA38`, 19/19 + back
- Credentials in gitignored `env-local.txt` (key id + username + password).
  BUILDER TODO: delete password line after testing; consider rotating password.
- All 8 print-ready decks have 900×1500 cream-border files in `print/decks/*-tgc/`.
- Shop live (`pages/shop.html`, header Shop tab). Booklets: `booklets/*.mdx`.
- Builder still to do: TGC "Proof All" + Approve on both products, then ORDER 1
  copy of each. Nothing publishes before the physical proof passes.

---

## OPUS 4.8 SECTION (judgment-heavy — run first)

### O1. Historical-claims audit + fixes (the big one)
Audit every `tarot/*/grammar.json` (names, descriptions, axis/composite sections;
sample ~10 items/deck) + `index.html` against the project's evidence-first brand.
Hunt: (a) absolutist/superlative claims — house rule requires hedging ("among the
earliest", "arguably"); KNOWN ISSUE: Visconti-Sforza is titled "The Oldest Tarot
(c. 1451)" while our own Cary-Yale is dated ~1442-45 — self-contradiction, fix;
(b) debated attributions stated as fact (Bembo for Visconti decks; "Charles VI" is
NOT 1392 French — check framed as misnomer; Mantegna misnomer framing; the
golden-dawn deck uses 1909 RWS imagery — verify name/description don't imply it IS
the Golden Dawn's own deck); (c) false date precision (prefer "c."); (d)
occult-projection leakage: game decks (Visconti, Marseille, Minchiate, Tarocchino,
Sola Busca, Charles VI, Besançon, Mantegna) must not present divinatory meanings as
native — Etteilla/Wirth/Golden Dawn are divination-native and fine. Write findings
to `research/AUDIT-historical-claims.md` (table: deck | quoted claim | problem |
rewording | severity), then APPLY the FIX-NOW and HEDGE items to the grammars,
regenerate meta (`scripts/build_meta_grammar.py`), commit, push.

### O2. Ma Diao (Chinese money cards) grammar — ancestors line
Skokloster Castle (Sweden) has 12 digitized Ma Diao cards on Commons (search
`Skoklosters Ma Diao`, files like "Kinesiskt spelkort till Ma Diao - Skoklosters
slott - 102351.tif"; use `Special:FilePath/<name>?width=1200` to get JPEG renders;
also 水滸牌 Water Margin money-card images exist). Build
`tarot/madiao-money-cards/grammar.json` in the house style (see `mamluk-deck` and
`ganjifa` for the ancestors framing): evidence-first, money-suited system
explained (cash/strings/myriads), Ming-era game context, China → Islamic world →
Europe transmission per `research/00c-islamic-and-chinese-card-origins.mdx`. Add a
node + derives edge in `tarot/tree-of-tarot/grammar.json` next to the Mamluk node.
Run `scripts/stamp_print_metadata.py`-style audit only if images measure ≥750×1050
(unlikely for TIF renders — fine, it's an educational deck). Validate, regen meta,
add to `_collection.json` the way other decks appear, push, verify renders live.

### O3. Homepage clarity pass
`index.html`: a newcomer should understand in 10 seconds what they can DO. Add a
"Start here" strip (Browse the cards / Get a reading / Print a deck → shop), add
the missing 🛒 Shop card to the explore grid, gloss the word "grammar" in one
clause, keep the history + misconceptions sections. Keep dark style. Verify live.

### O4. Vendor research synthesis (when token budget allows)
The deep-research run stalled twice; treat its "refuted" verdicts as ARTIFACTS of
the token limit (verifiers died 0-0), NOT real. Salvageable unverified findings:
QPMN (QP Printing Ltd, Hong Kong) markets an API + MOQ-1 POD tarot at 2.75×4.75 +
Shopify app w/ split fulfillment but VERY low adoption (1 review, multi-week
delivery) and order flow partially manual; MPC (makeplayingcards.com) confirms
MOQ-1 POD + per-card images + 2-3 day production but web-UI only, no public API.
Task: verify QPMN's API docs directly + MPC reseller/API programs, compare against
TGC (proven, US, hosted checkout), decide the worker's vendor; update
`print/SHOP-PLAN.md` §5 and recursive-eco pipeline doc. Brazil angle: Fábrica de
Tarot / Fábrica do Baralho / Atual Card / Copag = BR-domestic candidates (no APIs
found) — serves BR buyers, not US export.

---

## SONNET SECTION (mechanical, well-specified — run second)

### S1. Finish the sampler (21/21) + push via API
`python scripts/build_sampler.py` (idempotent; only 2 backs missing: aluette-1860,
napoletane — Commons 429s, the script now has backoff). Then
`python scripts/tgc_upload_deck.py --game 1C2D3BF2-64E5-11F1-9D82-035066E3122E
--deck 370F9906-64E5-11F1-9D0E-30818797CA38 --cards print/decks/sampler-tgc`
(idempotent — uploads only the new cards).

### S2. Planned-deck image hunts (report, build only if rich)
Commons API searches for: "Soprafino Della Rocca tarot" (1835), "Gumppenberg
tarot Lombardy" (1810), "d'Este tarot Ferrara" (~1450), "Brera-Brambilla". For
each: count usable PD scans + max resolution; log results in
`plan/PLANNED-DECKS-IMAGE-HUNT.md`. Only build a grammar if ≥20 cards exist at
usable res; otherwise leave the planned node as-is.

### S3. Site polish
(a) Favicon: small gold spiral SVG (`favicon.svg`, reuse the spiral path from
index.html's logo) + `<link rel="icon">` in all pages; (b) og:title/og:description
/og:image meta on index + shop; (c) shop covers: swap Commons cover URLs for
R2-hosted first-card images from each deck grammar (Commons is slow/429-prone).

### S4. After the builder's proofs PASS (do not run before)
Create the remaining 6 deck products via API (one `tgc_upload_deck.py` run each,
new game per deck named "<Deck> — Recursive Tarot"); builder publishes + pastes
shop URLs into `print-products.json` (flips Buy buttons live automatically).

### S5. Disk cleanup (after all TGC uploads done)
Delete `print/decks/*-tgc/` raw folders (machine is disk-tight; files regenerate
via download+resize scripts).

---

## Standing rules for both sessions
- Push recursive-tarot freely (GitHub Pages, free). recursive-eco: docs commit
  LOCALLY only (no push — Vercel cost).
- The meta-rebuild GitHub Action auto-pushes "chore: rebuild meta-grammar" —
  `git pull` + `git checkout --ours` on the meta file when it conflicts.
- Never put credentials in chat or commits; `env-local.txt` is gitignored.
- House writing style: no absolutist claims; hedge; each deck framed in its own
  tradition; PD images only, with attribution; builder = PlayfulProcess publicly.
- Proof-first: nothing publishes for sale before the builder holds the physical
  proof and approves.
