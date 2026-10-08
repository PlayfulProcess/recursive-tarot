# recursive.eco cleanup after PR #43: a checklist for PlayfulProcess

PR #43 changes the repo's copies of the decks. recursive.eco keeps its own copies. When the repo
pushes to the app, the app keeps any section the repo no longer has. When the app writes back
("Resolve all drifts"), the app's items win. So the sections PR #43 archives must also be removed in
the app, or they come back. The platform chat (recursive.eco session) built the tool for it; this
file is the order of steps. **Every step that changes a live grammar waits for your word.**

## The open question first (from the platform chat, Oct 5)

The platform chat compared one AI Scene with its picture: the Golden Dawn Sun. The Scene describes
the 1909 Waite-Smith card accurately, with one slip (the red feather is in the child's hair; the
banner is on a staff). The text that described a *different* picture (the two-children Sun) was the
Golden Dawn `Symbol` section, which PR #43 already moves out. Its evaluation:
`recursive-eco/docs/research/EVAL-vision-golden-dawn-sun-2026-10-05.md`.

So before removing every Scene in the app:

- [ ] **Your call:** sample-check about 20 Scenes across 5 decks against their pictures, then
  decide: (a) remove all Scenes (what PR #43 does in the repo), or (b) keep the ones that hold up
  as plain picture descriptions ("alt text"), labelled as machine descriptions, and remove only the
  text that describes a different picture. If (b), PR #43's Scene commit is reverted for the decks
  that pass, from `tarot/_archive/ai-scenes-2026-10-04/`.

## Steps

1. [ ] **Deploy the tool.** The widened `update_items` (it can select "every item that has section
   X": `where: {has_section: "<label>"}`) is commit `dba27020` on recursive-eco's
   `claude/prayer-for-the-loop`, local, not pushed. It works on the live MCP only after you push
   and it deploys. Until then the live MCP rejects `has_section`.
2. [ ] **Backup.** The platform chat takes a backup table of the grammars below (RLS on), before
   any write. Each MCP save is also versioned (`list_grammar_versions`, `restore_grammar_version`
   is the undo).
3. [ ] **Dry run, every grammar** (`dry_run: true` is the default), and record the count:
   `update_items(grammar_id, where: {has_section: "Scene"}, set: {sections: {Scene: null}})`.
   The counts should match the table.
4. [ ] **The Golden Dawn deck has three more sections to remove** on its 78 cards (Book T's own
   text replaces them): the same call with `has_section: "Divinatory Meaning"`,
   `"Reversed / Ill-Dignified"` and `"Symbol"`, each with `{sections: {<label>: null}}`.
   Expect 78 each. (`Symbol` stays on the deck's 6 group items; the repo keeps those too.)
5. [ ] **Apply, deck by deck, with your word** (`dry_run: false`). One save and one version per
   deck.
6. [ ] **Merge PR #43, with your word.** The push then adds the `Book T (1912)` sections to the
   Golden Dawn cards in the app and rewrites the Anecdotes "Song reference" lines.
7. [ ] **Check:**
   - [ ] `get_grammar` with `include_sections: false` on two or three decks: no `Scene` in the
     section labels.
   - [ ] The Golden Dawn Sun in the app shows `Book T (1912)`, and no Divinatory Meaning / Symbol.
   - [ ] One Anecdotes card in the app shows only "Song: “Title” (Album, Year) — Joanna Newsom".
   - [ ] The channel's drift check shows nothing for these grammars on either side.

## The grammars and the expected Scene counts

| Repo deck | recursive.eco id | Scenes |
|---|---|---|
| belgian-tarot | 9e364631-d879-4c5a-84a6-79b2c5263d97 | 23 |
| cary-yale-visconti-tarot | 4102566c-1d94-4f35-b1f8-c647e8ff7099 | 105 |
| charles-vi-tarot | cc5bda4c-f47b-43e9-aa35-d3164f7c3c0e | 18 |
| court-de-gebelin-tarot | ba98bf95-e08d-409f-a16c-2dcb660e4545 | 23 |
| este-tarot | 7af567b3-3bf7-4047-b199-c8758dd2c9e8 | 18 |
| etteilla-i-livre-de-thot | 50fb5980-5be5-4702-9a4f-858ddd524fe3 | 94 |
| etteilla-ii-egyptian | c310e5d9-f954-458c-9462-aa1eefd95209 | 94 |
| etteilla-iii-oracle-des-dames | 9c62d3ca-4e96-44ff-bffb-b7d3da55423c | 94 |
| golden-dawn-book-t-tarot | edac5d5a-8100-486d-b822-2f31b20a194c | 104 (+78 ×3, step 4) |
| madiao-money-cards | 51858640-0605-4428-b6b0-633b115f642e | 18 |
| mamluk-deck | 2403af8b-1350-4df4-b04c-976ebe5c9326 | 18 |
| mantegna-tarocchi | 44c379aa-5bfa-40d4-91ea-b593e18cbc2d | 64 |
| minchiate-florence-tarot | 2fd5ebb0-a69d-4731-9acd-bbf4e37c17e8 | 147 |
| oswald-wirth-tarot | 2b757b2e-b4d9-4896-bc72-f9ae6b7f5656 | 23 |
| paris-anonymous-tarot | cd170781-33d7-44f3-b5e5-23e50c52ba7e | 83 |
| sola-busca-tarot | 277953bc-b745-419a-a265-484865e75516 | 108 |
| tarocchino-bologna | 37ff6a9d-ba38-42e2-92ea-aa5871716bcc | 97 |
| tarot-de-besancon | 0aab46a2-38b1-4ba3-8dc1-914af67a026c | 14 |
| tarot-de-marseille-conver | ac47f7af-ac80-4942-a422-dd4a15614738 | 118 |
| tree-of-tarot | 1aa29bd2-eb06-4cf4-b53d-ab46da5e2d43 | 34 |
| vieville-tarot | 748bd669-1a0b-4f71-b5fa-b7c15601fda5 | 83 |
| visconti-sforza-tarot | 6dc092b0-9972-43f0-b493-ff6c2a61dcfc | 120 |
| **Total** | | **1,500** |

Counts are the repo's. If the app's count differs for a deck, the two copies have drifted; stop and
look before applying. The ids come from `tarot/_eco_ids.json`.

## Added Oct 7: reversed meanings that no source gave

The branch `reversals/sourced-only` ("Reversed meanings: only where a source gives them") removes
these from the repo, archived in `tarot/_archive/unsourced-reversals-2026-10-07.json`. Same rule
as above: the push does not remove them in the app, so each needs the app-side call, with your word,
**before** any "Resolve all drifts" write-back (or the app's copies come back into the repo).

| Repo deck | recursive.eco id | Remove in the app | Expect |
|---|---|---|---|
| golden-dawn-book-t-tarot | edac5d5a-8100-486d-b822-2f31b20a194c | `Reversed / Ill-Dignified` (step 4 above) | 78 |
| tarot-de-marseille-conver | ac47f7af-ac80-4942-a422-dd4a15614738 | `Reversed` | 78 |
| oswald-wirth-tarot | 2b757b2e-b4d9-4896-bc72-f9ae6b7f5656 | `Reversed` | 22 |
| etteilla-i-livre-de-thot | 50fb5980-5be5-4702-9a4f-858ddd524fe3 | `Reversed (the person ill-disposed)`; `Reversed` on the minors only | 16 + 40 |
| etteilla-ii-egyptian | c310e5d9-f954-458c-9462-aa1eefd95209 | as Etteilla I | 16 + 40 |
| etteilla-iii-oracle-des-dames | 9c62d3ca-4e96-44ff-bffb-b7d3da55423c | as Etteilla I | 16 + 40 |

On the Etteilla decks, `has_section: "Reversed"` alone would also catch the 22 trumps, which keep
theirs: select the 40 minors (`category: "minor"`, or the item ids listed in the archive file).

## Added Oct 8: the Etteilla number cards' upright lines

The branch `due/oct8` moves the 40 number-card `Upright` lines off each Etteilla deck (one template
copied across the suits), archived in `tarot/_archive/unsourced-pip-uprights-2026-10-08.json`. Same
rule: remove them in the app too, with your word, before any "Resolve all drifts" write-back.

| Repo deck | recursive.eco id | Remove in the app | Expect |
|---|---|---|---|
| etteilla-i-livre-de-thot | 50fb5980-5be5-4702-9a4f-858ddd524fe3 | `Upright` on the 40 number cards only | 40 |
| etteilla-ii-egyptian | c310e5d9-f954-458c-9462-aa1eefd95209 | as Etteilla I | 40 |
| etteilla-iii-oracle-des-dames | 9c62d3ca-4e96-44ff-bffb-b7d3da55423c | as Etteilla I | 40 |

`has_section: "Upright"` alone would also catch the 22 trumps, which keep theirs (now labelled as
paraphrase): select the 40 by the item ids in the archive file. The courts carry
`Upright (the person well-disposed)`, a different label, and are not touched.

## Added Oct 8: Etteilla's own words on all 78 cards

The branch `sources/etteilla-own-words` gives every card on the three Etteilla decks an `Upright` and
a `Reversed` holding Etteilla's own word for that leaf (from the *Dictionnaire synonimique du Livre de
Thot*, 1791), and drops the 16 courts' `Upright (the person well-disposed)` label. The paraphrases it
replaces are archived in `tarot/_archive/etteilla-paraphrases-2026-10-08.json`. Before any "Resolve all
drifts" write-back, with your word, the app copy needs the same:

| Repo deck | recursive.eco id | In the app | Expect |
|---|---|---|---|
| etteilla-i-livre-de-thot | 50fb5980-5be5-4702-9a4f-858ddd524fe3 | take `Upright` and `Reversed` from the repo for all 78 cards; remove `Upright (the person well-disposed)` on the 16 courts | 78 cards, 16 removals |
| etteilla-ii-egyptian | c310e5d9-f954-458c-9462-aa1eefd95209 | as Etteilla I | 78, 16 |
| etteilla-iii-oracle-des-dames | 9c62d3ca-4e96-44ff-bffb-b7d3da55423c | as Etteilla I | 78, 16 |

A pull from `main` after merge brings the new sections in; the court label is the one field a pull
would leave behind in the app.
