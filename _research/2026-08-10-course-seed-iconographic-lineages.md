# Course seed — testing the lineage hypothesis iconographically

*2026-08-10. Outline only, for approval — not a shipped course, no files added to `course/`.
Companion to `2026-08-10-researcher-journeys.md`, which this course borrows three exercises from
directly. Format modeled on `course/history-of-tarot.mdx` (front-matter shape, `## ` section
rhythm, `data-embed` usage) and `course/how-to-contribute.mdx` (the rungs pattern for the closing
exercise). If approved, this becomes `course/<id>.mdx`, registered in `site-header.js`'s
`COURSE_GROUPS` and `course/_courses.json`'s gallery — neither edited here.*

## Working title, and three alternatives

**Working title (given): "Testing Lineages with Your Eyes."** Reads a little like an eye exam.
Alternatives, ranked by fit with the site's own titling voice (short, direct, second person or
plain declarative — see "Reading the Cards," "What a Reading Can Do," "Ways to Contribute"):

1. **"Same Card, Every Deck"** — names the actual mechanic (the Trump × Deck wall) in four words;
   plain enough to sit next to "How the Cards Can Work" in a menu.
2. **"How to Compare a Deck"** — matches "Ways to Contribute" 's how-to register exactly; signals
   a practice, not a reading experience.
3. **"The Comparison Method"** — more academic, fits the "Read more deeply" gallery group.
4. *(given)* "Testing Lineages with Your Eyes" — kept as an option; strongest if the course leans
   into the "hypothesis-testing" framing explicitly (which the outline below does).

Recommendation: **"Same Card, Every Deck"** as the title, with "testing tarot's family tree by
eye" as the subtitle/description — it's the one a researcher would click on faith that it does
what it says.

## Where it sits in the site's structure

- **Gallery placement:** `course/_courses.json`, group **"Read more deeply"** (method course, not
  an entry point, not a devotional voice) — alongside "Reading the Cards" and "The Golden Dawn."
  `deck` cover: `tarot-de-marseille-conver` (the standardization case study is the course's own
  spine) or `sola-busca-tarot` if that deck gets added to the meta-grammar first (see gap #1 in
  the companion research file) — worth deciding after that fix lands, since the cover deck should
  be one the course can actually put in front of the reader inside the Explorer.
- **Menu placement:** `site-header.js` `COURSE_GROUPS`, under `'More'`, after "Reading the Cards."
- **The two wings (CLAUDE.md):** this is squarely a **Record/evidence**-layer course, not a
  practice/voice course — it teaches how to read the *tool*, not a reading stance. No voice
  disclaimer needed (`voices.json`'s `shared_intention` doesn't apply directly, though the closing
  "gate, not fate" note still belongs, because the course does touch the divination-turn material).
- **Depends on:** the Emergence Explorer (`viewers/explorer.html`) exactly as it exists today,
  including its current gaps — the course is written to use those gaps as teaching material, not
  to pretend they're fixed. If gap #1 from the companion file (Sola Busca joining the meta-grammar)
  lands before this ships, Exercise 3 gets easier and should be rewritten to match.

## Full outline

**Front matter** (`id`, `title`, `description`, `author: PlayfulProcess`, `date`, no `duration`
given the exercise-heavy shape — reader-paced, not reading-time-paced, matching how
`walking-the-golden-dawn-path.mdx` also omits it).

1. **Why compare decks with your eyes** *(fully written below)* — the thesis: five centuries of
   the same 22 pictures, redrawn by hand, is a natural experiment sitting in public domain; the
   Explorer is a magnifying glass for it, not an oracle. States the epistemology up front:
   correlation (same picture, same slot) is not proof of copying, and copying is not proof of a
   single shared exemplar — three different claims, easy to blur, that the rest of the course
   keeps separate.
2. **The tool in one minute** — what a "pivot" is (drag a field to Rows, another to Columns,
   read the grid); what "— (no value)" honestly means (a stated exclusion, not an error); how to
   open a card's full detail and follow its "Open in [deck] →" pill back to the source.
3. **Exercise 1 — Find the turn** *(the easy win; builds confidence before the trap)*. Guided
   version of Q5 from the research file: reset the wall, put `century` in Rows and `function` in
   Columns, watch three centuries of "game" give way to a hard right-angle turn into "origin-myth,"
   "divination," "esoteric" starting in 1781. Teaches: a *documented, hand-classified* axis
   (function) can make a historical argument visually, in one pivot, faster than a paragraph can.
4. **Exercise 2 — The swap hiding in plain sight** *(fully written below)* — guided version of Q2.
   Row 8, row 11, the Strength/Justice reversal — and the moment the exercise turns the tool on
   itself: what the wall *doesn't* tell you, and how to go find it anyway.
5. **What the pictures can prove — and what they can't** — the epistemology section, worked in
   full rather than asserted: three case studies of "resemblance," ranked by what kind of claim
   each one actually supports —
   - *Same slot, same picture, five centuries* (the trumps generally) — strong evidence of a
     **shared game convention**, weak evidence of anything about meaning, because the meaning
     changed completely while the picture didn't (this is the site's own history-course thesis,
     cited, not re-argued).
   - *Same suit-sign iconography across independently-produced decks* (cups/coins/swords/batons
     tracing to the Mamluk pack) — evidence of a **single transmission event** (cards moving west),
     not evidence that any two specific decks copied each other directly.
   - *Sola Busca's scenic minors and the Rider-Waite-Smith minors* — the hard case, worked with the
     hedge the site's own Golden Dawn course already uses: a **documented opportunity** (Pamela
     Colman Smith could plausibly have seen British-Museum photographs of Sola Busca around
     1907–08, before drawing RWS in 1909) is not the same claim as **documented influence**, which
     is not the same claim as **direct copying** — three different epistemic weights for what looks,
     to the eye, like "the same kind of resemblance." A reader is asked to hold open which one the
     Explorer can actually help them test (comparing specific scenes side by side) and which one
     it can't (settling what was in Smith's head).
6. **Exercise 3 — When the tool says no** *(the hard lesson)*. Guided version of Q6: try to put
   Sola Busca in the wall. It isn't there. Walk the "✦ Decks ▾" multi-select instead, load Sola
   Busca alongside Golden Dawn (Book T), and hit the Batons/Wands mismatch firsthand — two suits
   that are the same suit, rendered as if they were different, because the raw data was never
   told they're the same. Teaches the course's real payload: **a negative result from a tool is
   itself data** — about the tool, and sometimes about the state of the underlying scholarship —
   never proof the underlying question is unanswerable.
7. **Document what you find** *(outline only — the closing exercise)*. Modeled on
   `how-to-contribute.mdx`'s rungs. Ask the reader to run one comparison of their own choosing —
   any two decks, any shared field — and write down, in three sentences: what they compared, what
   they found, and which of the three epistemic weights from section 5 it actually supports. Two
   routes out, mirroring the contribute course exactly: **Rung 1**, post it as a note on the
   relevant card via "Fork / Edit" in recursive.eco (no git); **Rung 2**, open a PR adding a short
   `Research note` to the deck's `grammar.json` with a `[@citation]`-style source if they have one,
   or flagged as their own observation if they don't. Explicitly *not* asking for a finished
   argument — a well-stated observation ("the Empress's crown gets a bird only in decks after
   1750 — worth checking") is the whole ask.
8. **Sources & honesty** — the standard closing embed (`<div data-embed="apparatus"></div>`),
   plus an explicit line that every "gap" named in sections 3–6 is a snapshot of the tool as of
   this writing, dated, so a later reader can tell whether it's since been fixed.

---

## Sample section 1 (fully written) — "Why compare decks with your eyes"

> *Front matter for context, if this became the real file:*
> ```yaml
> id: same-card-every-deck
> title: "Same Card, Every Deck"
> description: "Five centuries of the same twenty-two pictures, redrawn by hand, sitting in one public-domain library — a natural experiment in how meaning travels. A practical course in reading the comparison tool honestly: what a matching picture proves, what it doesn't, and where the tool itself still gets in the way."
> author: PlayfulProcess
> date: 2026-08-10
> ```

# Same Card, Every Deck

Open the [Emergence Explorer](../viewers/explorer.html) and the first thing you see is a grid: the
twenty-two trumps down the side, thirteen historical decks across the top, five and a half
centuries collapsed into one table you can scroll. That grid is not a museum wall. It's an
instrument — the same instrument an art historian would build by hand, spreading facsimiles across
a table, except this one already has 768 cards loaded and lets you re-sort them by year, by suit,
by which regional order they follow, in the time it takes to drag a chip from one box to another.

Here is the natural experiment sitting inside it, worth stating plainly before you touch anything.
Tarot's twenty-two trumps were fixed as a *set* — Fool through World, in some order — by the 1440s,
in northern Italy, and the picture on each one has been recognizably the same picture ever since:
a skeleton for Death, a falling tower for the Tower, a dancing figure in a wreath for the World.
What has *not* stayed the same, not even slightly, is what anyone believed those pictures were for.
For three centuries they illustrated a card game. Then, starting in 1781, a small group of French
and English writers — none of them citing each other's evidence, most of them inventing their own —
began reading the same twenty-two pictures as a lost Egyptian book, a fortune-telling system, a map
of the soul. The picture is a fossil. The meaning is poured in fresh, over and over, by people who
each believed they were the first to see what was really there.

That is the whole argument of this site's [History of Tarot](course-viewer.html?course=history-of-tarot)
course, told as a story. This course asks a narrower, more mechanical question: **now that all of it
is sitting in one comparable dataset, what can you actually verify by eye, and how do you tell the
difference between verifying something and just noticing a resemblance?**

Those are not the same skill, and it is worth naming the three claims a resemblance can support,
because the rest of this course keeps coming back to them:

- **Correlation** — two cards, in two different decks, occupy "the same slot" (both are the eighth
  trump, say) or share a visual motif. This is the cheapest claim and the Explorer is very good at
  surfacing it — that's what a pivot table *is*.
- **Copying** — one deck's maker had the other deck (or a description of it) in front of them, and
  reproduced something from it on purpose. This is a much stronger claim, and a shared slot alone
  never proves it — you need provenance: who could have seen what, and when.
- **Shared exemplar** — two decks that look alike didn't copy each other at all; they both descend,
  independently, from some earlier common source neither maker ever saw side by side (the way the
  European suit-signs — cups, coins, swords, batons — all trace back through the Mamluk pack to
  cards that were already old by the time they reached Italy, without any European cardmaker ever
  touching a Mamluk deck directly).

An untrained eye collapses all three into "huh, these look similar." A researcher's job — and this
course's actual subject — is keeping them apart even when the tool in front of you makes them look
identical. Three guided exercises follow, each one a real question a historian or working artist
would bring to this library, each one navigated honestly: two of them work cleanly, one of them
hits a wall the tool doesn't tell you about until you go looking. The wall is not a flaw in the
course. It's the best lesson in it.

---

## Sample section 2 (fully written) — "Exercise 2: The swap hiding in plain sight"

## Exercise 2 — The swap hiding in plain sight

You'll need: the [Emergence Explorer](../viewers/explorer.html), loaded fresh (its default view is
already what this exercise starts from — the Trump × Deck wall, thirteen decks, twenty-two rows).

**The question.** Around 1909, the designers of what's now called the Rider-Waite-Smith deck — the
most reproduced tarot in the world — made one change to the trump sequence that nobody who plays
the original card game would recognize: they swapped Strength and Justice. In the old Marseille
pattern, card VIII is *La Justice* and card XI is *La Force*. In the Golden Dawn's system (which
RWS inherited wholesale — see [The Golden Dawn — the Map and the Walk](course-viewer.html?course=walking-the-golden-dawn-path)),
card VIII is Strength and card XI is Justice. It's a small change with a real reason behind it —
the Order wanted the trump sequence to track the zodiac in order, and Leo (Strength's astrological
attribution) needs to come before Libra (Justice's) — but it's exactly the kind of change that
proves the sequence was never a fixed, ancient thing. Someone, in living memory, just... moved two
cards. Can you *see* that in the data you're looking at right now?

**Step 1 — find the archetype.** You're already looking at it: the default wall's rows are numbered
0–21, and row 8 and row 11 are right there. Scroll to row 8. Every deck's column shows a Strength
card — a figure and a lion, roughly, dress and composition varying, subject constant. Scroll to row
11: every deck shows a Justice card — scales, a sword, a seated figure. This part is clean. The
Explorer built these rows by matching each card's *name* to a canonical list, not by trusting
whatever number each deck printed on it — so row 8 really is "every deck's Strength card," full
stop, regardless of what any individual deck called it internally.

**Step 2 — and that's exactly the trap.** Open the Tarot de Marseille (Conver) card in row 8 (click
it; the detail panel opens on the right). Nothing in that panel — not the title, not the metadata
line, not the "Origin" text — tells you what number is actually printed on that card in the
Marseille deck. It isn't VIII, but the panel doesn't say so, because the number the Explorer
tracks internally has *already been remapped* to the shared archetype slot before it ever reaches
you. The swap you came here to find is sitting one click away — inside the source deck itself,
readable straight off the card image — but invisible from the comparison view built to show it to
you.

**Step 3 — go get the fact the tool won't hand you.** Click the "Open in [deck] →" pill on that
Marseille card (or open the [Tarot de Marseille card browser](../viewers/cards.html?src=../tarot/tarot-de-marseille-conver/grammar.json)
directly and find *La Force*). Read the roman numeral printed on the card: **XI**. Now do the same
for Golden Dawn's Strength card: **VIII**. You've now confirmed the swap by hand, using the
Explorer to *find* the right two cards to compare and the source decks to *read* the fact itself.

**What this teaches, beyond the swap.** A tool that normalizes data for you — matches "Strength" in
five languages to one archetype slot, so you can compare across thirteen decks without doing that
matching yourself — is doing real, valuable work. It is also, by definition, throwing something
away: here, the one fact that made the comparison interesting in the first place. Neither the
normalization nor the loss is a bug exactly — it's a trade-off, made silently, and a careful reader
checks what got traded before trusting a view that looks this clean. That habit — *ask what a tool
normalized before you cite what it shows you* — is worth more than this one swap. Carry it into
every pivot in this library, and into every dataset you ever compare by eye again.

---

## Notes for whoever builds this

- Exercises 1 and 3 above are outlined, not written — Exercise 1 is straightforward to draft from
  the research file's Q5 finding directly; Exercise 3 needs a decision first (does it teach the
  *current* Sola-Busca-is-absent gap, or wait for that gap to close and teach the Batons/Wands
  suit-name lesson instead, which survives either way and is arguably the better lesson).
- Section 5 ("What the pictures can prove") is the intellectual spine of the whole course and
  deserves the most editorial attention before this ships — it's the one section making a claim
  (about Sola Busca → RWS) that the site already hedges carefully elsewhere
  (`walking-the-golden-dawn-path.mdx`: "several historians think she saw them, though how much she
  drew on them is genuinely debated") and this course must match that hedge exactly, not sharpen it.
- No images were created for this seed (read-only task); section 3's and 4's write-ups would each
  want one screenshot of the relevant Explorer state, captured fresh at build time per
  `CLAUDE.md`'s course-images convention (`pages/courses/images/`, referenced as `images/<name>.ext`
  in the `.mdx`).
- Registration, if approved: one line in `site-header.js`'s `COURSE_GROUPS` (`'More'` group), one
  entry in `course/_courses.json` (group **"Read more deeply"**) — neither touched by this file.
