# TAROT REVAMP PLAN — 2026-08-07

*The astro-style process applied to tarot.recursive.eco. Companion to
`_research/audits/2026-08-07-tarot-ui-truth.md` (the truth audit) and
`_research/2026-08-07-tattvas-research.md` (tattvas grounding).
Method: phases sized in sessions, each with a gate; Fernando tests thoroughly at the end;
ONE merge to main. Local browser verification before any push (standing rule).*

**North star for the Explorer (Fernando, Aug 7):** *"something scholars or artists could use to
compare and inspire themselves with tarot cards"* — and no view that is complex without
generating insight.

---

## Phase 0 — Land what this session already built  *(done, needs her test + push)*

- **Header dropdown fix** (`site-header.js` v46, all 24 pages bumped): dropdown no longer
  disappears when the mouse crosses the gap below the trigger. Root cause + fix documented in
  the audit. Verified locally at DOM level; **her mouse test is the gate.**
- `_private/` folder created + gitignored: Tantra Illuminated Kindle export (moved from repo
  root — it was untracked, never committed), extracted highlights markdown, Bus Passengers
  Supabase export. **IP stays out of the public repo.**
- Audit + research + this plan in `_research/`.

Gate: Fernando hovers Home/Views/Courses/Play on the live-local site; then push (Pages build is
free). Estimate: done + 0.1 session.

---

## Phase 1 — Explorer: from pivot toy to comparison instrument  *(~1 session, high confidence)*

The audit verdict: the pivot engine works; the FIELDS are muddled. Measured on the meta-grammar
(904 items): `number` mixes trump numbers 0–21 with pip/court ranks 1–14 (row "3" = Empress +
every 3-of-suit — the "grouping most number cards together" Fernando saw); `arcana` splits into
`major` (243) vs `trump` (32) vs missing (136); 180 items have no number ("—" landfill row).

Build (data first, then view):
1. **`build_meta_grammar.py` derives clean axes** onto each meta item:
   `role` = trump | pip | court | other (normalizing major/trump at DERIVED level while keeping
   the deck's own vocabulary in the display field — Bologna's "trump" is deliberate editorial
   voice, don't flatten the source data);
   `trump_number` (0–21, trumps only) and `rank` (1–10 + page/knight/queen/king, minors only) —
   splitting the overloaded `number`.
2. **Explorer presets rebuilt on the new axes.** Default landing view =
   **Trump number × Deck** — the "same card across 13 decks" comparison wall, the thing no other
   tarot site does well. Second preset: Suit × Rank (per-deck or cross-deck). Demote raw
   `number` out of the presets (keep it in the tray for the Golden-Dawn-style numerology lens —
   that correspondence is a real esoteric reading, just not a default).
3. **No silent buckets:** pivots state what they exclude ("38 undated items hidden") instead of
   an anonymous "—" row. (Corpus-wide: 670 of 1,918 leaf cards — 34.9% — have no
   `metadata.number`; the "—" row is a third of the library.)
4. **Fix the deck-misattribution bug** (audit §5): `dimension-engine.js` lets an item's
   cross-link `metadata.deck` label beat the inherited real deck — 47 cards across 5 decks
   render under the WRONG deck in Deck pivots on `?decks=` loads (e.g. Paris Anonymous trumps
   shown as "Tarot de Marseille"). Inherit must win for identity fields. Also: pass deck-level
   `year` through on `?src=` loads or retire `?src=` from the docs.
5. Cards/deck/tree viewers untouched in this phase (their cleanups live in Phase 2).
   Note: `trump_number` already exists in golden-dawn-book-t's grammar — precedent for the axis
   split, not an invention.

Gate: Fernando pivots for 5 minutes and reports whether it *feels* like a comparison instrument.
Confidence: high (script + one HTML file; check_all.py + build_meta_grammar are the safety net).
What only she can judge: whether the default view generates the "inspire myself" feeling.

## Phase 2 — Truth-audit fixes + dead-code sweep  *(~1 session, high confidence)*

The ranked bug list from the audit, in order:
1. caster-studio "Contribute a spread on GitHub" → actually carry the exported JSON (GitHub
   new-file URL supports `value=` prefill; fallback: instruct + auto-download).
2. caster-studio "Update spread" → honest labeling: either wire real persistence via the flow
   API (needs POST — check if endpoint exists) or relabel to "this tab only" (no fake ✓).
3. tree-viewer "Get a Reading" → caster-studio reads `?src=` and pre-selects the deck.
4. tree-viewer "Copy to My Grammars" → resolve id from `_eco_ids.json` when only `?src=` is
   present; hide the button if unresolvable.
5. tree-viewer no-tree fallback 404 → point at cards.html.
6. course-viewer: delete dead presentation-mode machinery; fix `relocateCoursePills()` (drop the
   `#present-toggle` dependency); fix or delete the `?grammar_id=` listing path
   (`#course-duration`).
7. Dead-code sweep in one pass: `<view-switcher>` tags + script includes everywhere,
   `NodeContextMenu` hooks (tree-viewer, cards), unused `dimension-engine.js` include
   (genealogy-tree), derive the duplicated SLUG_MAPs from `metadata.source_deck`.
   **cards.html family** (audit §5): sync-from-GitHub functions (+ the latent
   `renderItems()` ReferenceError in the dead branch), hidden type toggle, `switchDeck()`,
   orphaned `showLensMenu()`, empty "View as" dropdown scaffold, dead `eco-links.js` load.
8. cards.html sign-in gate: `window.SigninModal` is never defined anywhere — replace with a
   direct flow.recursive.eco sign-in deep link (or implement the modal for real).
9. Unify cards.html's two "Group by" states (`deckGroupField` persists in the hash,
   `pillAxisId` is silently lost).
10. Quiet the signed-out 401 pair from auth-widget (catch → silent).

Deliberately NOT in scope: "Interpret with AI" (blocked on the flow-side listener — an
apps/flow task, different repo/costs; log it there).

Gate: her click-through of the fixed handoffs (tree → caster with deck carried, contribute link
carrying content). Confidence: high; all static-site, free Pages builds.

## Phase 3 — Bus Passengers oracle into the repo  *(~1 session + HER DECISION FIRST)*

Found in Supabase: two identical "Bus Passengers" grammars (35 items — Jun 17 copy is a pure
duplicate of the Jul 7 one, `68c76f60…` is canonical) + an older "Bus Grammar — System Prompts"
(41 items, May 12, superseded). Export saved at
`_private/bus-passengers-68c76f60-supabase-export.json`. Structure: 29 passenger cards in four
tiers + 6 category/position cards; six layered sections (Thoughts → Thinking → Perception →
Sensing → Context → Mystery) plus About/Lineage/Where-this-isn't-enough.

**⚠ Propose-first — the licensing/ethics question the deck itself raises.** Its own description
says: *"STUDY DECK — IN ACTIVE EDITORIAL REVISION… under attribution review."* Tier 4b (the four
Mountains) is **Indigenous Cree teaching from elder John Crier**, transmitted via Andreotti/
Ahenakew. This repo is public **CC-BY-SA-4.0** — publishing would place Cree teaching under a
license nobody asked the knowledge-holders about. Options for Fernando to pick:
- **A (recommended): import Tiers 1–3 + Tier 4a** (Pixar emotions, parts-work, Voice Dialogue,
  Andreotti-inspired passengers — all name-a-school compatible), and hold Tier 4b out of the
  public repo until the attribution review she already flagged is resolved; the deck's
  "Positions, not passengers" card and description note the held tier honestly.
- B: import everything with the STUDY-DECK banner intact (still publishes 4b under CC-BY-SA).
- C: keep the whole deck app-only; feature it on the site as a link to flow.recursive.eco.

Build (once she picks): `tarot/bus-passengers/grammar.json` with `_grammar_commons` provenance
block, name-a-school compliance pass (description already does this well), format conformance to
GRAMMAR_FORMAT.md, `check_all.py` green, `_eco_ids.json` mapping to `68c76f60…`, image strategy
(items have Supabase image URLs — either mirror to R2 per repo convention or keep remote; R2
mirror needs desktop creds, noted), feature on Play menu + a home/play tile. Also: propose
deleting the Jun 17 duplicate in-app (destructive — her click, not mine).

## Phase 4 — 36 Tattvas deepening  *(~1–2 sessions, high confidence on content, gated on her pastes)*

Grounding done (see `_research/2026-08-07-tattvas-research.md`). Structure of the existing
grammar checks out (order, 5/7/24 groups, kañcuka↔śakti mapping all verified). Revisions:
1. **PRIORITY: de-Wallis the text.** Essence fields for tattvas 01–12 and 32–36 quote "Wallis"
   by name; description cites his podcast as source. Rewrite in our own words, grounded in
   Kṣemarāja/Sanderson/Torella + the primary-text translations, attributed as
   **"inspired by Non-Dual Śaiva Tantra"** per the name-a-school rule (matching the existing
   non-dual-tantra-reads-the-tarot voice conventions). Her Kindle highlights (in `_private/`,
   never quoted, never committed) inform emphasis and tone only.
2. Add the missing doctrine: **anupāya** (fourth upāya — real gap), a **ṣaḍadhvan/dīkṣā**
   concept card (the tradition's own name for ascent/descent), and a **Sāṃkhya-25 vs Śaiva-36**
   card ("why 36?").
3. Fix the 12-petals/"twelve vowels" claim (Sanskrit counts 16); keep the already-well-flagged
   interpretive correspondences as interpretive.
4. Re-audit the 36-Tattvas SVGs (long-standing backlog item — fold in here).
5. Wallis RAG note: the app-side grammar carries `ai_personality_prompt` (the Wallis RAG voice).
   Repo-side rewrite must NOT clobber app-side fields on sync (sync skips repo-only fields both
   ways — verify with one-card dry run first).

Gate: she reads three rewritten cards (one per group) before the sweep runs.

## Phase 5 — The rolling oracle disclaimer  *(~0.5 session; PROPOSAL below, build on her nod)*

**Intent:** part of the ritual, not a legal warning. Mirror, not command.

**Proposed placement:** a single thin line directly beneath the casting board (caster-studio),
appearing only after a cast lands — the moment of maximum "the cards have spoken" energy is
exactly when the frame matters. Same component under the card-detail modal's reading sections.
One implementation (`oracle-ribbon.js`), adoptable later by astro/iching sites.

**Proposed motion:** not a marquee — a **slow drift**. The line sits in a fixed position and
its text *changes by slow crossfade* through 4–6 short fragments (one on screen at a time,
~12s each, ~8s hold + 2s fade), like a votive inscription being re-lit. Muted gold italic
serif (Fraunces), small caps feel, on the parchment background — liturgical, not legalese.
`prefers-reduced-motion`: static first fragment, no cycling. Dismissible for the session (tiny
×, localStorage), because ritual furniture you can't move becomes a banner ad.

**Proposed fragments** (refining her draft, creed vocabulary):
1. *"An oracle is a recursive process — make-believe becoming sense-making, sometimes becoming real."*
2. *"Keep your agency. The cards ask; you decide."*
3. *"The map is not the territory."*
4. *"A mirror, not a command."*
5. *"Gate, not fate."*

Gate: she approves fragments + placement mock (I'll build it behind `?ribbon=1` first so she can
see it live before it defaults on).

## Phase 6 (optional) — Retirements  *(~0.5 session, her call per item)*

- Delete `viewers/sequence.html` (v1) — zero inbound links; rename sequence-v2 → sequence.html
  (redirect stub for old URLs).
- Fold `perform.html`'s audio+overlay playback into sequence-v2, or explicitly keep as the
  "performance format" player and link it properly.
- Graduate `viewers/prototypes/lenses.html` out of `prototypes/` (it's a first-class nav item).

---

## Standing items kept on the board (from memory, different scope)

- **Astro leftovers awaiting her words:** "recalculate my charts" (28 Porphyry-cusp saved
  charts, backed-up batch refresh offered) · "delete it" (stray Aug 4 journal entry
  "BLOCKED BY VERIFICATION STUB").
- "Interpret with AI" flow-side listener (apps/flow, paid builds — batch with next flow round).

## Session math

| Phase | Size | Confidence | Blockers only she can clear |
|---|---|---|---|
| 0 | done + 0.1 | — | mouse test, push go |
| 1 Explorer | 1 | high | judge the default view |
| 2 Fixes+sweep | 1 | high | click-through test |
| 3 Bus oracle | 1 | high once decided | **Tier 4b decision (A/B/C)** |
| 4 Tattvas | 1–2 | high | read 3 sample cards; optional pastes |
| 5 Ribbon | 0.5 | high | approve fragments + placement |
| 6 Retirements | 0.5 | high | per-item go |

Recommended order: 0 → 1 → 2 in one arc (all static, free builds, one merge at the end per the
process), 3–5 as the following arc, 6 opportunistic.
