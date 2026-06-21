# recording/examples

Worked **sequence / performance** grammars used as data by the
backend-free player at [`viewers/sequence.html`](../../viewers/sequence.html)
and as reference for authoring new programs.

These are **not** tarot decks and must never be imported as grammars.
They live here (not under `tarot/<slug>/`) and are not named
`grammar.json`, so neither this repo's tooling nor the recursive.eco
GitHub importer will pick them up. See
[`../docs/sequence-format.md`](../docs/sequence-format.md).

| File | What it is |
|------|------------|
| `passarinho-sequence.json` | "Passarinho Complete" — a 104-item card-and-clip program (52 title cards interleaved with 52 cropped YouTube clips). Authored on recursive.eco; saved here as the canonical example of the sequence format. |
| `history-of-tarot-sequence.json` | "The Recursive Tarot — A History in Cards & Clips" — a 36-item program tracing tarot's history (Mamluk → trionfi → Marseille → Golden Dawn → RWS → modern), cross-referenced to [`course/history-of-tarot.mdx`](../../course/history-of-tarot.mdx). **All items are cards on purpose: no YouTube IDs are invented.** Each clip beat is a footage-slot card (`▶ …`, `metadata.footage_slot:true`) whose `card_subtitle` names exactly what to source; convert it to a `segment` (add `metadata.youtube_video_id` + `performance.start_sec/end_sec`) once you have a verified clip. Includes a reserved "The Games, Played" stub for future screen-captures of `pages/games/`. |
| `history-of-tarot-watchlist-sequence.json` | "The Recursive Tarot — Further Watching" — a 24-item companion **playlist** of 18 external YouTube documentaries in four sections: Cards & Games, Tarot History, the Renaissance, and Press & Paper. **Every video ID was verified embeddable via YouTube oEmbed (2026-06-16); non-embeddable candidates were dropped.** Videos play full (`start_sec:0`, no `end_sec`) and advance on natural end or ⏭; add an `end_sec` to crop any into a tight beat. Third-party videos belong to their channels. |

Play them:

```
viewers/sequence.html?src=../recording/examples/passarinho-sequence.json
viewers/sequence.html?src=../recording/examples/history-of-tarot-sequence.json
viewers/sequence.html?src=../recording/examples/history-of-tarot-watchlist-sequence.json
```
