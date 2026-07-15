# Content publish pass — July 2026

Goal: bring the site's reader-facing prose — starting with **"How the Cards Can Work"** — to a
form the builder is proud to publish. This plan names the two failure modes we keep oscillating
between, defines the target voice between them, and lays out the passes in order.

## 1. Diagnosis — three versions of the flagship, two failure modes

Three versions of `course/how-tarot-works.mdx` are in play:

| Version | What's right | What's wrong |
|---|---|---|
| **dev** (`f6dcc7d`, the live site) | Best content and argument order: the map/meaning opening, the honest skeptic section, Levitt's coin-flip, the Palantír close. Compact, well-sourced. | **AI-listicle format.** The argument is carried by bullet lists with bold lead-ins, a two-row table at the essay's hinge, a numbered "this course makes that case in three moves" announcement, Title-Case headers, bold on nearly every paragraph. Prose broken into bullets = "no sense of paragraphs." |
| **main** (`4edec36`) | Punchy, readable. | One-sentence paragraphs used as a rhetorical drumbeat ("Not because… / Because…") — fragments standing in for paragraphs; a different flavor of the same AI cadence. |
| **Earlier prose drafts** (`505102e` etc.) | Real paragraphs, real first-person voice. | Sentences run long; the same reframe is stated two or three times; tic phrases ("at its best," "the whole of," "exactly"); hedges stacked on hedges. Exaggerated, repetitive, dull. |

**Target: dev's content and structure, carried by the earlier drafts' paragraph form, at
dev's length.** Neither more material nor a new argument — a re-setting of type.

Also found on dev, independent of style (fix regardless):

- The file **ends mid-sentence** — last line is a truncated link: `**[Here's how to contribute](course-`. Live bug.
- Typos: "necessariky" (line 13), "connect **a** isolated, private problem" (line 108).
- The "Try the practice" box links readers to a **raw grammar.json blob on GitHub**; it should
  link to the Tolkien's Three deck in the site's own viewer.
- "The Collapse of Precognition" is listed as one of the mechanisms that explain the uncanny
  *how-did-it-know* feeling — but it isn't a mechanism of meaning-making; it's a separate
  evidence claim. Move it out of the bullet list into the section's closing paragraph.
- The Palantír material (including the surveillance-company aside) now appears in **both**
  `how-tarot-works.mdx` and `intention-setting.mdx` on dev. Keep the full treatment in
  How the Cards Can Work; reduce Intention Setting to one sentence plus a link.

## 2. The style contract — additions to HOW-TO-WRITE-A-COURSE.md

The existing voice guardrails (Jul 8–9) cover claims and tone. None cover **formatting** —
which is exactly where the dev version fails. Add a "Formatting guardrails" block:

- **Paragraphs carry arguments.** A bullet list is only for genuinely parallel, enumerable
  items a reader might scan or return to (the five skeptic mechanisms qualify; Tolkien's four
  gifts do not — they argue with each other, so they're paragraphs). Test: if the items need
  connective tissue — *but, so, and yet* — it's a paragraph wearing a list's clothes.
- **No tables for arguments.** A table is for reference data. If the two cells contain
  competing claims, write the two sentences and let them compete in prose.
- **Bold budget: about one per section**, reserved for a term of art on first use
  (*Recovery*, *gate*, *sub-creator*) — never for emphasis. Italics for emphasis, sparingly.
- **Sentence-case headings** in the builder's register ("The thing the cards cannot do"),
  not Title-Case Noun Phrases ("The Catch That Decides the Stance"). No numbered headings.
- **A paragraph is 3–6 sentences with one idea.** A single-sentence paragraph is a deliberate
  beat you get once or twice per essay, not a default rhythm.
- **Say each reframe once.** If the point has landed, the next sentence must do new work.
  (This is the anti-Claude rule, complementing the anti-list rules above.)

## 3. Worked sample — for sign-off before the full pass

Dev's hinge section is currently an announcement ("Here is the hinge of the whole argument"),
a bolded claim, and a two-row table. As prose, same content:

> ## The catch that decides the stance
>
> Projection and subjective validation are the same mechanism wearing two names. The gift
> that lets a card land so personally — your talent for pouring meaning into an open image —
> is exactly what makes a reading feel prophetic when it is not.
>
> That is why the question you bring decides what the deck becomes. Ask "what will happen to
> me?" and you hand a powerful meaning-making engine a job it cannot do; it will oblige
> anyway, and build you a fate out of your own fears and wishes. Ask "what am I not seeing
> here?" and you give the same engine the job it does well. Same cards, same shuffle, same
> chill down the spine. The chill is real — it is your body flagging that an image has
> touched something live. Take it as a cue to look closer, not as proof that an oracle has
> spoken.

If this is the right register, the whole essay gets this treatment. If it isn't, adjust the
contract in §2 first — cheaper to argue over two paragraphs than over the whole essay.

## 4. The passes, in order

**Phase 0 — settle the base.** dev is the canonical text (it's the live site and has the
consolidations: voice courses folded into Intention Setting, Light of Tarot merged). All
content edits happen against dev's versions. main lags and is reconciled later by the normal
dev→main publish merge (per CLAUDE.md / RECURSIVE-ECO-INTEGRATION.md — never discard the
App's write-backs on main).

**Phase 1 — flagship rewrite** (`how-tarot-works.mdx`), section by section on dev's text:

| Section (dev) | Action |
|---|---|
| Opening (map/meaning) | Keep. Fix "necessariky." Delete the numbered "three moves" list — throat-clearing. |
| The Magic of Fiction | Convert the four-gift bullet list to four short paragraphs; fold the Murray blockquote into the Recovery paragraph. Re-point "Try the practice" at the site's Tolkien's Three viewer. |
| Mythopoeia | Already prose; light trim only. |
| The thing the cards cannot do | Keep the mechanism list *as a list* (it's genuinely enumerable) but calm each entry to ≤3 sentences; move "Collapse of Precognition" out to a closing paragraph. |
| Ways a reading can help | Drop numbers from the subheads; sentence-case; fix "a isolated"; cut feeling tags ("extraordinary evidence trail"). |
| The catch (table section) | Replace with the §3 prose. |
| Palantír | Keep — it's the essay's best prose already. Dedupe against Intention Setting (full version lives here). |
| Where this leaves us / Keep digging | Keep; repair the truncated final link. |

Every citation and URL survives the rewrite — this pass moves type, not claims.

**Phase 2 — audit + verify.** Run the existing post-draft audit checklist (absolutism grep,
feeling tags, one-pass-per-critique). Read the whole essay start to finish once. Verify
render with the course-viewer at 390×844 (TOC, no errors), regenerate mirrors
(`scripts/course_to_grammar.py`, `scripts/build_reading_course.py` as applicable), then
`python scripts/build_meta_grammar.py` and `python scripts/check_all.py` → "all checks
passed", dangling=0.

**Phase 3 — sweep the rest of the reader-facing spine**, same contract, in priority order:

1. `intention-setting.mdx` — prose is already close; needs the bold diet and the Palantír
   dedupe. Also: the redirect stub `marsha-linehan-reads-the-tarot.mdx` still titles a
   living person ("Marsha Linehan Reads the Tarot") — retitle the stub to the school
   ("DBT Reads the Tarot") per the house rule; the lens section inside Intention Setting
   already correctly says "DBT."
2. `reading-the-cards.mdx` — the biggest file (~1,000 lines on main, heavily reworked on
   dev); audit-only pass first, rewrite only sections that fail the contract.
3. `tarot-and-the-crack.mdx`, `history-of-tarot.mdx`, `divination-traditions.mdx`,
   `tarot-today.mdx` — one pass each.
4. Redirect stubs and short pages — check titles/links only.

**Phase 4 — card-level text (later, optional).** Spot-audit Scene/Symbol sections in the
deck grammars for the same failure modes (bold sprawl, feeling tags). Only worth a full pass
if the spot-check fails; grammar edits then follow the normal rebuild pipeline.

**Phase 5 — publish.** Merge dev→main per the integration doc. That is the "proudly
publish" moment: the app reads from main.

## 5. Definition of publishable (per essay)

- [ ] No bullet list carrying an argument; no argument tables; bold within budget.
- [ ] Every paragraph 3–6 sentences, one idea; single-sentence paragraphs ≤2 per essay.
- [ ] No reframe stated twice; no feeling tags; absolutism grep clean.
- [ ] All citations intact and resolving; no reader-facing links to raw JSON/GitHub blobs.
- [ ] No content duplicated against a sibling course (cross-link instead).
- [ ] Renders clean in course-viewer at mobile width; `check_all.py` passes.
- [ ] Read aloud once, start to finish, without wincing.
