# scripts/archive — historical, already run

**The grammar JSONs are the data. These scripts are not.**

Everything in this folder is a **one-shot** script that has already run. Each one built or
patched a deck, stamped a field, or probed an API at a point in time. Its output is now
canonical in `tarot/<slug>/grammar.json` (or in `research/`, `print/`), and in many cases the
data has been hand-edited many times since — so **re-running one of these would overwrite
current, better content with the state it produced months ago.**

## The rule

- **To change a deck, edit `tarot/<slug>/grammar.json` directly.** That file is the source of
  truth. There is no generator to re-run for these decks.
- Nothing here is deleted — it's kept for provenance: it records *how* a deck first came into
  the repo, and what the seed data was.
- If you need one of these as a starting point for a genuinely new deck, **copy it out** and
  adapt the copy. Don't run it in place.

## The exceptions (still live, still in `scripts/`)

These stayed put because something calls them or they're safe to re-run:

| Script | Why it stays |
|---|---|
| `build_meta_grammar.py` | **CI runs it** — `.github/workflows/build-meta.yml` |
| `validate-grammar.mjs` | **CI runs it** — `.github/workflows/validate-grammar.yml` |
| `check_all.py` | The pre-commit gate. Shells out to `build_people_grammar.py` + `build_meta_grammar.py` by their `scripts/` path |
| `build_people_grammar.py` | Regenerates `people-of-tarot` from `research/people/*.md` (the dossiers are the source of truth) |
| `course_to_grammar.py`, `build_contribute_grammar.py`, `build_reading_course.py` | Regenerate `_generated` grammars from `course/*.mdx` |
| `enrich_cards_from_research.py`, `refresh_collection.py`, `audit_image_usage.py`, `apply_theme.py` | Idempotent, add-only or re-derive-only |
| `normalize_book_t_sections.py` | Idempotent; `--check` mode asserts the Book T sections are still token-for-token intact |
| `tgc_card.py`, `build_sampler.py`, `build_sampler_v6.py`, `prebake_deck_r2.py`, `detect_flood_bg.py`, `resize_for_tgc.py`, `download_deck_images.py`, `tgc_upload_deck.py`, `generate_book.py`, `rehost_to_r2.py`, `migrate_covers_to_r2.py`, `stamp_print_metadata.py` | The print / proofing pipeline documented in `print/PROOFING-PROTOCOL.md` and `print/HOW-TO-PRINT.md`. **`tgc_card.py` is a shared library** imported by four of them — they only resolve because they sit in the same directory, so they move together or not at all |

## What's in here

| Script | What it did once |
|---|---|
| `build_ancestor_decks.py` | Generated the Cary Sheet / Rosenwald / Noblet / Ganjifa grammars from hardcoded data |
| `build_augmented.py` | Built Arlecchino's Augmented Arcana |
| `build_belgian.py` | Built the Belgian / Vandenborre grammar |
| `build_este.py` | Built the d'Este Tarocchi grammar (hardcoded Yale labels) |
| `build_madiao.py` | Built the Ma Diao money-cards grammar |
| `build_paris.py` | Built the Anonymous Parisian Tarot grammar |
| `build_vieville.py` | Built the Viéville grammar |
| `build_yve_rws.py` | Built the Yve Lepkowski RWS grammar from scraped dumps |
| `generate_sola_busca.py` | Generated the Sola Busca grammar |
| `import_yve_deck.py` | Transformed a platform deck export into a repo grammar |
| `build_tarot_collection.py` | Migrated grammars in from the sibling `recursive.eco-schemas` repo (migration complete) |
| `add_history_sources.py` | Appended a "provenance & sources" block to deck descriptions — superseded by `enrich_from_research.py`, itself superseded by the current text |
| `enrich_from_research.py` | Folded `research/<deck>.mdx` into grammar descriptions |
| `add_minor_keys.py` | Wrote `minor_key` onto every minor item (now canonical in the grammars) |
| `keywords_to_emergences.py` | Promoted shared keywords into emergence nodes |
| `seed_deck_index.py` | Seeded `common_name` / `category` / `year` into deck metadata |
| `stamp_canonical_repo.py` | Stamped `_github_url` / `_github_source_url` onto every grammar |
| `fix_links_and_parents.py` | Two source-level fixes — its own docstring says "run once" |
| `analyze_numbers.py` | Cross-deck number analysis; its output lives in `research/synthesis/` |
| `rehost_backs_r2.py` | Rehosted card-back images to R2 and rewrote `print/card-backs.json` |
| `tgc_diagnose.py`, `tgc_diagnose2.py`, `tgc_game_state.py`, `tgc_inspect_card.py`, `tgc_list_decks.py` | Read-only Game Crafter API probes from a debugging session |
| `tgc_proof_backs.py` | Flipped `has_proofed_back` on every card once |
| `tgc_remove_decks.py` | Removed specific draft decks — **hardcoded UUID list, do not run** |

Moved here 2026-07-27. Nothing was deleted, and no live path imports anything in this folder.
