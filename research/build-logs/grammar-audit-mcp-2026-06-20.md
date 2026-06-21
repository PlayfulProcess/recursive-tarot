# Grammar Audit + Improve — "Sources" grammars, via the recursive.eco MCP

**Date:** 2026-06-20 · **Auditor:** Claude (Opus 4.8), Claude Desktop + recursive.eco MCP
**Branch:** `claude/grammar-sources-audit-mcp`
**Scope:** `tarot/books-of-tarot`, `tarot/people-of-tarot` (GENERATED), deck spot-check.
**Convention:** matches `research/AUDIT-historical-claims.md`. Severity:
**FIX NOW** · **IMPROVE** (gap we can close) · **WATCH** · **OK/RESOLVED**.

This file is both the build log (Step 4A) and the findings list (Step 1). Findings
were written *before* any edit. Honest about dead-ends and in-copyright skips.

---

## Step 0 — Orient (done)

- Read `CLAUDE.md` (root), `BACKLOG.md`, `research/AUDIT-historical-claims.md`.
- Confirmed the one cross-link mechanism: the **pill** —
  `metadata.source_deck` + `source_item_id` + `deck`. **Exactly one per item**
  (viewer renders a single "Open in [deck] →"; `viewers/cards.html:4361`). No other
  link field. Pill self-suppresses when already inside `/<slug>/`.
- Confirmed generated files: `all-decks-many-lenses`, `people-of-tarot`,
  `tree-of-tarot`. Never hand-edited.
- **Gate before any change:** `python scripts/check_all.py` →
  `decks=13 cards=768 … items=904 dangling=0` → **"OK: all checks passed (30 grammars)"**. ✅

---

## Step 1 — Findings (written before fixing)

### A. `books-of-tarot` (25 books + 5 lenses)

**Overall:** unusually careful already. Copyright labels are accurate and the
PD/in-copyright split is honest. The real gap is **cross-links**: books carry a
Wikipedia `metadata.url` but **zero pills** to the people/decks they belong to.

| # | Dimension | Finding | Severity |
|---|---|---|---|
| A1 | CROSS-LINK | **No book links to its author's person node.** 10 books have a matching `research/people` dossier and could carry a pill to `people-of-tarot`. (Court de Gébelin, Etteilla, Lévi, Mathers/Book T, Waite, Dummett ×4 incl. co-authored, Kaplan.) | IMPROVE |
| A2 | COVERAGE | **15 book-authors have no person dossier**, so no pill target exists: Agrippa, Papus, Crowley, Farley, Place, Katz & Goodwin, Hundley, Regardie, Fauconnier & Turner, Forer, Rowland, Hyman, Nichols, Jung, White & Epston. Natural future *occultist/scholar* nodes: **Crowley, Papus, Agrippa, Jung**. Not built this pass (≈15 new dossiers = its own task). Logged to backlog. | WATCH |
| A3 | IMAGES | Author portraits present for the 7 occult-revival authors (PD, already on Commons URLs). In-copyright/modern authors correctly imageless. No image gaps to close in books. | OK |
| A4 | COPYRIGHT | Spot-checked every `Copyright` line. All accurate. The **Crowley** entry's jurisdiction-split note (text PD in life+70 since 2018; US ~2039; Harris paintings ~2033) is exemplary — keep as the model. | OK |
| A5 | FACTS | Forer (1949), Hyman (1977), Fauconnier & Turner (2002), White & Epston (1990) dates/venues spot-checked — correct. | OK |

### B. `people-of-tarot` (31 people/institutions — GENERATED)

**Overall:** rich dossiers, but the generated grammar is **thin on surface
affordances** and carries a real cross-platform bug.

| # | Dimension | Finding | Severity |
|---|---|---|---|
| B1 | GENERATOR BUG | **Windows-backslash noise baked into the repo.** Committed `people-of-tarot/grammar.json` has `"research": "research\\people\\<id>.md"` on **all 31** items (a Windows build was committed). `build_people_grammar.py` uses `os.path.relpath`, which emits `\` on Windows and `/` on Linux/CI → guaranteed churn. **Fix the generator to emit posix (`/`) always.** | **FIX NOW** |
| B2 | IMAGES | **Zero portraits.** `image_url` is never emitted. Dossiers have no `image:` field and the generator can't emit one. ~13 figures have a verified free portrait (table below). | IMPROVE |
| B3 | CROSS-LINK / REDIRECT | **No Wikipedia redirect, no pills.** No `metadata.url` (the "redirect people to Wikipedia" ask) and no book/deck pill. `made[]` is metadata only — never rendered as a link. | IMPROVE |
| B4 | COVERAGE | Rival/■connected figures named in dossiers but with no node: **Zavattari** (Bembo's rival hand), **Francesco / Bianca Maria Sforza** (folded into `visconti-sforza-patrons`). Acceptable as-is; logged. | WATCH |

### C. Deck spot-check (covers + cross-links + the open VERIFY)

| # | Finding | Severity |
|---|---|---|
| C1 | All 26 real deck grammars have a `cover_image_url`. Only the 4 generated/meta grammars lack covers — already BACKLOG §E. | OK |
| C2 | Deck→people pills are abundant and well-formed (counts span 13–114 per deck). | OK |
| C3 | **RESOLVED:** the June-10 mamluk "43 vs 48" VERIFY is already fixed — `mamluk-deck` now reads *"roughly 48 cards survive — about 43 from the original pack plus a handful of cruder later replacement cards (the original deck had 52)"*. Accurate and hedged. No action. | RESOLVED |

---

## Image availability — MCP evidence (read-only calls, 2026-06-20)

Every call below was real. `commons_image_search` returns license + artist;
`wikipedia_summary` returns the canonical page URL + lead image (license then
verified on Commons). **Only PD / CC0 / CC-BY / CC-BY-SA accepted.**

| Person | Tool call | Result → decision |
|---|---|---|
| Andrea Mantegna | `commons_image_search("Andrea Mantegna self-portrait")` | `Andrea_Mantegna_049_detail_possible_self-portrait.jpg` — **PD** ✅ use |
| Pamela Colman Smith | `commons_image_search("Pamela Colman Smith photograph portrait")` | `Pamela_Colman_Smith,_"In_Private_life"_(1904).jpg` — **PD** ✅ use |
| Petrarch | `commons_image_search("Petrarch portrait Andrea del Castagno")` | `Petrarch_by_Bargilla.jpg` (del Castagno) — **PD** ✅ use |
| Oswald Wirth | `wikipedia_summary("Oswald Wirth")` → `commons_image_search("Oswald Wirth occultist")` | `Oswald_Wirth.jpg` — **CC BY-SA 3.0** (credit la-rose-bleue.org) ✅ use w/ credit |
| Wynn Westcott | `wikipedia_summary` + `commons_image_search("William Wynn Westcott Golden Dawn")` | `William_Wynn_Westcott_PNG.png` — **PD** (photo pre-1897) ✅ use |
| Filippo Maria Visconti | `wikipedia_summary("Filippo Maria Visconti")` | `Pisanello_-_Codex_Vallardi_2484.jpg` — **PD** ✅ use |
| Michael Dummett | `wikipedia_summary` + `commons_image_search("Michael Dummett philosopher")` | `Michael_Dummett_September_2004.jpg` — **CC BY-SA 4.0** (Klaus Reisinger / R. S. Kissel) ✅ use w/ credit |
| Stuart Kaplan | `wikipedia_summary("Stuart Kaplan")` | **No en.wikipedia page** → no free portrait → **stays imageless** (honest skip) |
| A. E. Waite, Court de Gébelin, Éliphas Lévi, Etteilla, MacGregor Mathers | (reuse) | Already on PD Commons URLs in `books-of-tarot` — reuse the same URLs |

**Still to confirm in the fix pass (likely imageless):** Comte de Mellet (obscure
18th-c.), Gertrude Moakley (d. 1998), Franco Pratesi (b. 1939), La Mayer, the two
anonymous "Masters", and the card-maker floruit-only figures (Noblet, Vieville,
Conver, Madenié, Vandenborre, Gringonneur) — no portrait is expected to exist.

**Dead-ends logged:** `commons_image_search("Oswald Wirth portrait")` returned only
unrelated Internet-Archive book PDFs — the bare-name query is noisy; the
`wikipedia_summary` lead-image route is more reliable for people, then verify the
license with a second targeted Commons search. `wikipedia_summary("Mamluk
playing cards")` / `("Mamluk Kanjifa")` both miss (redirect to *Playing card* /
404) — there is no clean dedicated EN article; the deck grammar's own sourcing
already settles the count (C3).

---

## Proposed fix plan (awaiting go-ahead before editing)

1. **Generator upgrade** (`scripts/build_people_grammar.py`):
   - B1: emit `research` path as posix (`.replace(os.sep,"/")`).
   - B2: read optional `image:` + `image_credit:` front-matter → emit `image_url`
     + `metadata.image_credit`.
   - B3: read optional `wikipedia:` → emit `metadata.url` (the redirect). Read
     optional `book:` → emit the **pill** (`source_deck:"books-of-tarot"`,
     `source_item_id:"book-…"`, `deck:"Books Behind the Tarot"`); else if `made[]`,
     emit a pill to `made[0]` deck. One pill max, book preferred over deck.
2. **Dossiers** (`research/people/*.md`): add `image:` / `image_credit:` /
   `wikipedia:` / `book:` front-matter to the ~13 figures with verified portraits
   and the ~7 with a book. No body edits.
3. **books-of-tarot** (hand-edit; not generated): add the A1 author pills (book →
   `people-of-tarot`).
4. **Rebuild** generated grammars via their scripts; **discard backslash/CRLF
   noise** in `all-decks-many-lenses`; re-run `check_all` (must stay dangling=0).
5. Backlog: A2 new person nodes (Crowley/Papus/Agrippa/Jung); B4 Zavattari.

> Not touched: deck grammars (spot-check only), `tree-of-tarot`, anything
> in-copyright (cited + linked, never hosted).

---

## Step 2 — Fixes applied (repo)

- **Generator** (`scripts/build_people_grammar.py`): posix `research` path; emits
  `image_url` + `metadata.image_credit` (from `image:`/`image_credit:`),
  `metadata.url` (from `wikipedia:`), and one pill via `make_pill()` —
  priority **book > featured-card > made-deck**. `make_pill` reads the
  *existing* `made`/`features_cards`, so deck pills auto-generate.
- **Dossiers**: 14 files gained front-matter (12 portraits + 13 Wikipedia
  redirects + 7 book links). Sourced via the MCP table above.
- **books-of-tarot** (hand-edit; not generated): 10 author pills →
  `people-of-tarot`.
- **Rebuild**: `build_people_grammar.py` →
  `image_url=12, pill=18, url=13, backslashes=0`. All deck-pill targets verified
  to resolve (0 broken). `all-decks-many-lenses` timestamp-only churn **discarded**.
- **Gate**: `check_all.py` → `dangling=0`, "all checks passed (30 grammars)". ✅

## Step 3 — Live sync to recursive.eco (via MCP, owner-confirmed)

| Action | MCP call | Result |
|---|---|---|
| Import Books grammar | `import_grammars(url=<branch raw books-of-tarot>)` | new id `7ff3ad23-6ceb-4b20-8c27-8bb04d0876ef` (private draft) |
| Publish + open Books | `set_grammar_visibility(7ff3ad23…, is_public, open_to_community)` | `is_public:true, open_to_community:true` |
| Mirror Books portraits | `set_item_images(7ff3ad23…, 8 imgs)` | `set:8 failed:0` → R2 |
| Sync People portraits | `set_item_images(a284fa37…, 12 imgs)` | `set:12 failed:0` → R2 |
| Sync People metadata | `update_items(a284fa37…, 22 items)` | `updated:22, not_found:[]` (pills + wiki url + credits) |
| Publish + open People | `set_grammar_visibility(a284fa37…, is_public, open_to_community)` | `is_public:true, open_to_community:true` |

`people-of-tarot` already existed in the DB (`a284fa37…`), so it was updated
**in place** (no duplicate, no prod deletion). `books-of-tarot` did not exist →
imported fresh. `get_grammar(7ff3ad23…)` confirmed the importer preserved every
`image_url`, pill, and copyright label. `tarot/_eco_ids.json` updated: books id
added; both grammars added to `_public_now`.

Live: <https://flow.recursive.eco/g/7ff3ad23-6ceb-4b20-8c27-8bb04d0876ef> ·
<https://flow.recursive.eco/g/a284fa37-694f-48dc-b977-f093658bc2b7>

## Step 4 — Documentation

- This build log.
- Course lesson appended to `course/build-a-tarot-deck-with-claude.mdx`
  ("Rung 5 in practice"), with 5 session figures under
  `pages/courses/images/mcp-audit-*.png`. The figures are faithful renderings of
  the real MCP/CLI exchanges (this pass ran head-less in **Claude Code**, not the
  Desktop GUI); calls/args/results are verbatim and a maintainer can replace them
  with live Desktop captures.

## Definition of done

- ☑ `check_all` passes, `dangling=0`.
- ☑ Findings logged, then fixes applied (PD/CC images + wiki redirects +
  cross-links). No facts needed correcting (mamluk already fixed).
- ☑ Generated grammars rebuilt via scripts, not hand-edited; backslash/timestamp
  noise discarded.
- ☑ Build log + course lesson with figures.
- ☑ Live on recursive.eco (owner-confirmed); both public + community-open.
- ☐ Pull request opened (final step).

## Backlog spun out (not done this pass)

- New person nodes for book-authors with no dossier: **Crowley, Papus, Agrippa,
  Jung** (would unlock those books' author pills). ~15 authors total lack a node.
- **Zavattari** node (Bembo's rival hand); folded Sforza patrons could split out.
- Per-dossier confirmation of the few floruit-only makers' Wikipedia pages.
