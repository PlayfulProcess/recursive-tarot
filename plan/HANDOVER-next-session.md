# HANDOVER — next session (start here)

*Written 2026-06-13 ~17:00 UTC by the Opus accuracy/research session. This is the single
entry point for the next session. Read this, then `plan/MASTER-accuracy-and-people.md`
(the live ledger) and `plan/CORRECTIONS-to-apply.md` (the ✅ STATUS block at its top).*

---

## 0. First moves (paste-prompt is in §6)

1. **Branch to pull:** `dev` is the active branch **and** the GitHub-Pages deploy source
   (`.github/workflows/build-meta.yml` deploys `dev` → tarot.recursive.eco). The accuracy work
   was developed on `claude/tarot-deck-accuracy-n4dv2r` and **fast-forwarded into `dev`** — as of
   this writing **`dev` == `claude/tarot-deck-accuracy-n4dv2r`** (same HEAD). `main` is behind `dev`.
2. **Verify nothing is stranded** (the maintainer's explicit ask):
   ```bash
   git fetch --all --prune
   git status                       # working tree clean?
   git branch -avv                  # local vs remote tracking
   for b in main dev claude/tarot-deck-accuracy-n4dv2r recursive-eco/merge-9a87b7b1-8ee072b; do
     echo "== $b =="; git log -1 --format='%h %ci %s' origin/$b 2>/dev/null; done
   git log --oneline origin/main..origin/dev | head      # what dev has that main doesn't
   git log --oneline origin/dev..origin/claude/tarot-deck-accuracy-n4dv2r   # should be empty (in sync)
   ```
   - The CI `chore: rebuild meta-grammar [skip ci]` commits land on `dev` only; if `dev` moved,
     merge it back into the working branch before continuing. The only file that ever conflicts is
     the generated `tarot/all-decks-many-lenses/grammar.json` — resolve by re-running
     `python3 scripts/build_meta_grammar.py` and committing.
   - There is a `recursive-eco/merge-*` branch (platform merges) — check it isn't holding edits we want.
3. **Run the gate before any commit:** `python3 scripts/check_all.py` (must end "all checks passed").

## 1. What this repo now has (done — see CHANGELOG Jun 13)

- **Research catalogue** — `research/SCHEMA.md`, `research/bibliography.bib` (~290 cited sources),
  `research/decks/<slug>.md` + `research/cards/<slug>.md` for **all ~25 decks**, and
  `research/people/<slug>.md` × **23**. Dossiers are the **source of truth**; every `[@key]` resolves.
- **People & Institutions grammar** — `tarot/people-of-tarot/grammar.json`, **generated** by
  `scripts/build_people_grammar.py` from `research/people/*.md`. (To change a person, edit the
  dossier and re-run.) Registered in `tarot/_collection.json` (is_meta).
- **471 cards enriched** with sourced "Research note" sections via
  `scripts/enrich_cards_from_research.py` (ADD-only, idempotent; re-run after editing any dossier).
- **Grammar accuracy** — corrections + the 5 delegated editorial calls applied (see
  `plan/CORRECTIONS-to-apply.md` top); anachronistic RWS pip-symbol metadata erased from the
  3 Etteilla decks; sourced RESEARCH NOTEs / EDITORIAL CALL notes in each affected deck description.
- **deck-picker** orders decks by year with the year in parentheses (`viewers/deck-picker.js`,
  `scripts/refresh_collection.py` curates `year`/`year_label` in `_collection.json`).

### Where the **people** work lives (the maintainer asked)
- Sourced biographies: **`research/people/*.md`** (23 files).
- Rendered grammar: **`tarot/people-of-tarot/grammar.json`** (generated; do NOT hand-edit).
- View it: `deck.html?file=tarot/people-of-tarot/grammar.json` locally, or on
  **tarot.recursive.eco** (it's in `_collection.json`, `default_preview: tree`).
- Regenerate: `python3 scripts/build_people_grammar.py`.

## 2. NEXT ACTIONS — needs WebFetch / image access (blocked in prior envs)

**Status 2026-06-13 (this session):** Wikimedia Commons API works; BM, Gallica, wopc, pollett,
mamluk.spiorad.net all return 403 or SSL errors. Progress made below — but full resolution
still requires a session with non-sandboxed access to those blocked hosts.

- **Mamluk original cards** — ✅ PARTIAL: 3 of 7 existing images correctly assigned to their cards
  (card 1 = 6 of Coins, card 2 = 3 of Cups, card 7 = King of Cups — confirmed via Commons API categories).
  cups-king corrected from card 2 → card 7; cups-pip corrected from card 1 → card 2; image notes added.
  **Remaining:** cards 3–6 still unverified stand-ins; the full ~48-card set (mamluk.spiorad.net,
  l-pollett.tripod.com) still blocked. The "IMAGE PROVENANCE / TODO" note in the grammar remains valid.
- **Sola Busca minors** — ✅ PARTIAL: 4 sourced scene descriptions added (2 of Cups, Page of Swords,
  Knight of Swords, Page of Coins) from secondary web sources. 52 of 56 still carry honest placeholders.
  To fill the remaining 52: need actual image viewing (BM/Brera scans) or Di Vincenzo 1998 book.
- **Paris-Anonymous (Tarot de Paris)** — ✅ ALREADY DONE: grammar has French captions from the card
  labels ("printed on the card") and comparative Research notes for all 22 trumps. Gallica blocked.
  Specific staging details ("Hell-mouth Foudre at XVI", "figural animal Aces") still need Gallica.
- **Verify medium-confidence dossier claims** against primaries — blocked (same sources 403).
  Medium-confidence claims spread across: belgian-tarot, cary-yale-visconti, este-tarot,
  etteilla decks, ganjifa, court-de-gebelin. Requires museum catalogs or paywalled scholarship.

## 3. NEXT ACTIONS — frontend (no fetch needed)

- **Drag-and-drop dimensions — code exists but is GATED & runtime-unverified.** Honest status
  (corrected 2026-06-13 after the maintainer reported "I don't see any drag-and-drop"):
  - `viewers/explorer.html` — full Rows/Columns/Filters pivot with draggable field chips. SEPARATE
    page; only there.
  - `viewers/cards.html` — a draggable dim-chip tray + a sidebar drop zone, but ONLY in **multi-deck
    mode** (`buildDimChipTray` / `buildDeckSidebar`, ~lines 2456–2525). It renders only after the user
    picks **2+ decks** via the "✦ Decks ▾" button (`?decks=a,b`). It does **NOT** appear in the default
    single-grammar / "All Decks (the meta)" view — which is why it looks missing.
  - **NOT in Tree view** at all; `viewers/tree-viewer.html` / genealogy don't consume
    `viewers/dimension-engine.js`.
  - **Runtime UNVERIFIED** — the prior session had no browser; only confirmed the code is present, not
    that it works. **First action: actually load the app and test it** (use the `run`/`verify` skills
    or a browser) — it may be broken, not just hidden.
  - TODO options: (a) surface the chip tray in single-grammar/meta view too, not only multi-deck;
    (b) wire drag-drop into Tree view via `dimension-engine.js`. Plan: `plan/EXPLORER-DESIGN.md`.

## 4. Tooling cheat-sheet (all idempotent)
- `scripts/build_people_grammar.py` — people dossiers → people grammar.
- `scripts/enrich_cards_from_research.py [--apply]` — cards dossiers → per-card "Research note".
- `scripts/refresh_collection.py` — re-sync `_collection.json` (names/counts/year) from grammars.
- `scripts/build_meta_grammar.py` — rebuild the generated meta (`all-decks-many-lenses`).
- `scripts/check_all.py` — the pre-commit gate.

## 5. Guardrails (unchanged)
- Never invent a citation; doubts get **erased or attributed** (who claims it), never asserted.
- Game decks have no native divinatory meanings; preserve peculiarities; keep the Dummett-spine baseline.
- Commit + push frequently; keep `check_all` green and the meta `dangling=0`.

## 6. PASTE-PROMPT for the next desktop session
> Continue the recursive-tarot accuracy/research work. **Pull and work from the `dev` branch**
> (it's also the GitHub-Pages deploy source). FIRST: `git fetch --all`, run the "verify nothing
> stranded" block in `plan/HANDOVER-next-session.md` §0 (check working tree, `git branch -avv`,
> and that `origin/dev`, `origin/claude/tarot-deck-accuracy-n4dv2r`, `origin/main`, and the
> `recursive-eco/merge-*` branch have no uncommitted/unmerged work we want — merge `dev`'s CI
> meta-rebuild commits back if needed), then `python3 scripts/check_all.py`. THEN read
> `plan/HANDOVER-next-session.md` (this file), `plan/MASTER-accuracy-and-people.md`, and the
> ✅ STATUS block atop `plan/CORRECTIONS-to-apply.md`. Confirm outbound fetch works
> (`curl -sI https://upload.wikimedia.org/ | head -1`). Then tackle the §2 image-blocked TODOs
> (start with the **Mamluk** original cards from Wikimedia Commons "Category: Mamluk playing cards",
> then Sola Busca scenes and the Tarot de Paris captions), and optionally the §3 tree-view
> drag-drop dimensions. The people work is in `research/people/*.md` → `tarot/people-of-tarot/grammar.json`.
