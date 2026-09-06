# Plan — a modern Commedia: spiralling through every path (for the tarot app)

*6 September 2026. Her question: "Can we build something akin to a modern version of Dante's Inferno,
spiralling through all possible paths like we are doing for the I Ching? Could this live in the
recursive tarot app?" Short answer: yes, and the tarot app is the right home — the Commedia is a spiral,
a spiral is a path, and the app already has a spread engine.*

## Why Dante fits the machinery

- **The geometry is already a path.** Inferno is a cone descending in nine circles; Purgatory a mountain
  ascending in seven terraces; Paradiso nine spheres outward. Dante walks it once, in one order. The
  combinatorial move is the same one the I Ching book makes: fix the beginning (the dark wood, canto I)
  and the end (the final vision, Paradiso XXXIII), and let the reader cast the middle.
- **A unit exists: the canto.** 100 cantos, 3 realms. Each canto is a stop with a place, a guide, an
  encounter, a sin or virtue, and an exit — exactly the shape of a hexagram-chapter (scenery / text /
  what it asks / story / exit).
- **The text is public domain.** Longfellow's translation (1867): Gutenberg #1004 complete, #1001–1003 by
  realm; Cary's (#1005–1006); the Italian (#997–999). Quote freely; the app's "Text" section can carry the
  actual tercets.
- **The tarot already maps onto it.** Fool = the pilgrim; Hermit = Virgil (the lamp in the dark wood);
  High Priestess = Beatrice; Tower = the gates and Dis; Devil = Cocytus; Judgement = the Purgatorial
  ascent; Star, Moon, Sun = the spheres; World = the final vision. Twenty-two trumps as the pilgrim's
  guides and thresholds is not a stretch — it is what the 15th-century trumps were already doing with
  the Christian cosmos (Death, Judgement, the Devil, the World).

## What it is, concretely

1. **A grammar: `tarot/commedia-longfellow/`** — 100 items (cantos), level 1, category by realm, sections:
   *Where* (the circle/terrace/sphere), *Who* (guide + the encountered soul), *Text* (the tercets that
   carry the encounter — Longfellow, PD), *The sin / the virtue*, *The exit* (how Dante leaves the canto).
   Metadata: realm, ring number, canto number, guide, trump-link (which tarot trump this canto most
   answers to). Built by a script from the Gutenberg text (cantos are cleanly delimited).
2. **A spread: "The Spiral."** Positions: *the dark wood* (where you are — cast), *the descent* (n stops),
   *the turn* (the bottom, Lucifer / the centre of the earth — fixed), *the climb* (n stops), *the vision*
   (fixed end). Saved as a normal SpreadContract; castable in `viewers/caster-studio.html` today.
3. **The spiral caster** — the Path Caster's own idea in the tarot app: the reader casts a trump for each
   position; the trump chooses the canto (via trump-link), and the canto's *exit* is the changing line
   that carries them to the next ring. Down nine, across, up seven, out nine. Every cast is a different
   Commedia; the beginning and the end are Dante's.
4. **The modern layer** — the author's own cantos. The Inferno was Florence in 1300 with real names;
   the modern version is the feed, the diagnosis, the founding story, the machines everyone calls
   inevitable — the "living myths in the room" from *Tarot as Myth* ch. 1. One modern canto per ring,
   written by her, sits beside Longfellow's. Nobody living named; the circles are structures, not people.

## Where it lives

- Grammar + spread + caster page in **recursive-tarot** (`tarot/commedia-longfellow/`, a spread JSON,
  `viewers/spiral.html` reusing caster-studio's engine). The I Ching repo's `caster-engine.js` is the
  path math; the tarot repo's `caster-studio` is the spread UI. Both are static.
- Published to recursive.eco as a grammar like the others (ids.json), so the Commedia is also castable
  in the app's oracle.

## The poetic film (Suno + image generation + Vidu) — advice

The record says (25 Aug): the whole-film route was retired after Lilac v3 — TTS and still-image
continuity broke it. So not a film. **Short pieces per stop** are the form this machinery supports:
60–90 seconds each, one canto or one path — a Suno song as the frame (the Belchior box, made instead
of licensed), six to eight generated images in one graphic identity, light motion, the tercet or the
line text spoken or shown. Each is a grammar item's *performance*; the spiral caster plays them in the
order the reader cast. Rights to settle first: Suno's commercial terms on the plan you use; image
models' terms; no living faces. Start with three stops (the dark wood, the bottom, the vision) and see
whether the form holds before making a hundred.

## Order of work (after her word)
1. Build the canto grammar from Gutenberg #1004 (script, ~1 hour).
2. Write the trump-link table (22 trumps ↔ 100 cantos; many-to-one).
3. Save "The Spiral" spread; cast it in caster-studio; read the cantos it returns.
4. `viewers/spiral.html`: the descent/climb rendered as a spiral, the reader's casts marked.
5. Her modern cantos, one per ring.
