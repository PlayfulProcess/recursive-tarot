# Content publish pass — July 2026 (v2)

Goal: bring the site's reader-facing prose — starting with **"How the Cards Can Work"** — to a
form the builder is proud to publish. v2 corrects the diagnosis (the rendered version is
**main's**, not dev's) and adds two content requirements from the builder: a fully **linked
bibliography** and the missing **psychology literature**, woven in.

## 1. Diagnosis — which version is which

Three versions of `course/how-tarot-works.mdx` exist; the branches have diverged into two
different essays:

| Version | What's right | What's wrong |
|---|---|---|
| **main** (`4edec36`) — **the one the site renders** | The content and arc the builder likes: map/meaning opening, Tolkien, honest skeptic chapter, gates-vs-oracles, palantír, "light in the eyes of the beholder," Further Reading at the end. | **The ChatGPT failure mode: no sense of paragraphs.** Most "paragraphs" are single-sentence fragments used as a drumbeat ("Not because… / Because…", "We stop noticing. / Recovery interrupts that habit."). The psych literature is compressed into one citation-free paragraph. **Further Reading has zero links.** |
| **dev** (`f6dcc7d`, unmerged rewrite) | Carries most of the missing literature *with URLs*: Forer, Hyman's cold reading, Whitson & Galinsky, Pennebaker, Hobson (ritual), Moore, Levitt, Blackmore, Ivtzan & French, the Bem replication failures. | Bullet-list/table format; ends mid-sentence (truncated link); typos ("necessariky," "a isolated"). Not what renders. |
| **Earlier prose drafts** (`505102e` etc.) | Real paragraphs, real first-person voice. | The Claude failure mode: long sentences, repeated reframes, tic phrases, stacked hedges. |

**Target: main's content and arc, in real paragraphs, with dev's evidence base woven in and
a linked bibliography at the end.** The research already exists — `research/why-tarot-works/`
(REPORT.md, adversarially verified 2026-06-22; does-tarot-predict.md; the shared
`research/bibliography.bib`). No new research phase needed; this is a weaving job.

## 2. The two content additions (builder's request, Jul 15)

### 2a. The missing literature — woven in, depth at the end

Two clusters, both already dossiered in `research/why-tarot-works/REPORT.md`:

**Cluster A — why readings feel personal and predictive** (goes in "The One Thing the
Cards Cannot Honestly Do"). Each mechanism gets its own short, linked paragraph instead of
today's single unlinked paragraph:

- Barnum/Forer effect — Forer 1949; Dickson & Kelly 1985 review.
- Cold reading as the deliberate craft built on it — Hyman 1977 (Skeptical Inquirer).
- Subjective validation — we tailor the suit ourselves.
- Confirmation bias — hits stay bright, misses fade.
- Apophenia + loss of control — Whitson & Galinsky 2008 (*Science*): pattern-seeing
  intensifies exactly when we feel out of control — the state in which people reach for cards.
- The direct tests — Blackmore 1983 (with the honest note that one of three experiments
  survived reanalysis); Ivtzan & French 2004. Precognition replication failures — Ritchie,
  Wiseman & French 2012; Galak et al. 2012 — as a closing paragraph, not a "mechanism."

**Cluster B — therapeutic value per modern psychology** (goes in "Why the Cards Can Still
Help," one short linked paragraph per mechanism):

- Projective surface — art-therapy framing ("semiotic mediators of meaning-making,"
  *Divining the Self*), with the dossier's verified honesty note: projective in mechanism,
  **not** a validated clinical instrument like Rorschach/TAT.
- Externalization & re-narration — narrative therapy (White & Epston lineage).
- Expressive writing — Pennebaker & Beall 1986: putting hard experience into words improves
  measured health outcomes.
- Structured randomness — Oblique Strategies; Moore 1957 (Naskapi divination as
  randomizer); Levitt 2021 (coin-flip study: nudged-to-change participants happier at
  follow-up).
- Ritual & expectancy — Hobson et al. 2018: ritual reliably lowers anxiety and restores
  felt agency, supernatural or not.

**Form (builder's decision, Jul 15): two separate deep-dive courses.** Each cluster becomes
its own course — working titles *"Why a Reading Feels So Personal"* (Cluster A) and *"What a
Reading Can Do — the Psychology"* (Cluster B) — built from the dossier with the standard
four-phase course method, registered in `COURSE_GROUPS` under **More**. The flagship keeps
one short, linked paragraph per mechanism in the body (the essay must still carry its own
evidence) and points to each deep dive with a one-line "the full literature lives here" link
at the end of the relevant section. No content duplicated: the flagship states each
mechanism once; the deep dives own the studies, caveats, and confidence levels.

### 2b. The linked bibliography

Rework "Further Reading" so that:

- **Every entry links out** — DOI, publisher page, or archival PDF. dev's version already
  has working URLs for most; `research/bibliography.bib` (319 entries) covers the rest.
- Entries are **grouped by theme**: Imagination & meaning-making (Tolkien, Korzybski, Kelly,
  James) · Why readings feel accurate (Forer → Galak) · What readings can genuinely do
  (Murray, Pennebaker, Hobson, Moore, Levitt, Eno) · Direct tests of tarot (Blackmore,
  Ivtzan & French). Keep the existing one-line annotations; they're good.
- It ends with a **"see the full bibliography"** link to `research/why-tarot-works/REPORT.md`
  (which carries per-claim confidence marks) — the one place a reader-facing GitHub link is
  right, because the target is prose, not raw JSON.

### 2c. New course: "Working with Claude Desktop" (a Contribute deep dive)

A deep dive expanding Rung 4 of *Ways to Contribute*, for readers who want the powerful
path. Positioning stated up front: **claude.ai is the easiest version; Desktop/Claude Code
is more advanced and more powerful** — this course is for when you're ready for that step.
Contents (builder's spec, Jul 15):

- **GitHub from zero** — what GitHub is, opening a free account, and why the project lives
  there (versions protected, nothing ever lost, every change reviewable).
- **Git, gently** — install, what a repository/branch/commit is, **local vs. remote (what
  "push" means)**, what a **pull request** is and best practices for filing one small and
  reviewable.
- **Session habits** — always start a session by saying **which branch the work should be
  saved on**; commit and push before ending; how to recover when you forget.
- **What CLAUDE.md is** — the repo's standing instructions, and why editing it changes how
  Claude behaves in every future session.
- **Key settings** — permission modes (what "auto" accepts on your behalf and when to use
  it), remote control, and the handful of defaults worth knowing before turning anything on.
- **The private-folder pattern** — if you don't want your context public: keep a private
  folder of personal references *next to* the cloned tarot repo and launch the Claude Code
  session at the parent folder, so Claude sees both but only the repo is ever pushed.
- Cross-reference: in the **claude.ai rung** of *Ways to Contribute*, add one light sentence
  that a branch is created automatically there — versions are protected and no work gets
  lost — with a pointer to this course for the full picture.

## 3. The style contract — additions to HOW-TO-WRITE-A-COURSE.md

The existing voice guardrails (Jul 8–9) cover claims and tone; add formatting guardrails:

- **Paragraphs carry arguments.** A paragraph is 3–6 sentences with one idea. The
  single-sentence paragraph is a deliberate beat used once or twice per essay — not the
  default rhythm (main's current failure), and not replaced by bullet lists (dev's).
- **Lists only for genuinely parallel, enumerable items** a reader might scan or return to.
  If items need connective tissue — *but, so, and yet* — it's a paragraph.
- **No tables for arguments**; tables are for reference data.
- **Bold budget ≈ one per section**, for a term of art on first use (*Recovery*, *gate*);
  italics for emphasis, sparingly.
- **Sentence-case headings** in the builder's register; no numbered headings.
- **Say each reframe once.** If the point landed, the next sentence does new work.
- **Every empirical claim carries its inline link** at first mention; the bibliography
  repeats it grouped by theme.

## 4. Worked sample — for sign-off before the full pass

Main's rendered text currently reads (lines 113–123):

> These are not flaws in human nature.
> They are consequences of being extraordinarily good at making meaning.
> Understanding them does not diminish tarot.
> It changes how we hold it.
> The cards are poor crystal balls.
> They are excellent mirrors.

Same content as paragraphs, with the literature woven in (register proposal):

> None of these are flaws in human nature; they are consequences of being extraordinarily
> good at making meaning. And there is a twist worth knowing: when people feel they have
> lost control, the pattern-seeing intensifies — in experiments they see images in static
> and invent correlations they would otherwise dismiss ([Whitson & Galinsky, 2008](https://doi.org/10.1126/science.1159845)).
> Uncertainty, high stakes, a longing for a sign — the conditions that make tarot most
> appealing are exactly the conditions in which we over-read whatever we draw.
>
> Understanding this does not diminish tarot. It tells you what the deck is for: the cards
> are poor crystal balls and excellent mirrors, and the rest of this essay is about what a
> mirror, held honestly, can actually do.

If this register is right, the whole essay gets this treatment; if not, adjust §3 first —
cheaper to argue over two paragraphs than the whole essay.

## 5. The passes, in order

**Phase 0 — settle deployment truth.** The site renders main's text while CLAUDE.md calls
dev the live static site — reconcile which branch deploys before editing (check Pages/deploy
config). Whatever the answer, the rewrite must land where it renders; dev's diverged
`how-tarot-works.mdx` (with its truncated last line) is superseded by this rewrite rather
than fixed separately.

**Phase 1 — flagship rewrite** of `course/how-tarot-works.mdx`, against main's text:

| Section (main) | Action |
|---|---|
| Opening ("Does it actually work?") | Keep the arc; merge fragments into paragraphs (the Korzybski map passage is nearly there already). |
| Why Fiction Changes Real Lives | Merge fragments; keep Murray/Holmes/Griffin with its link; add Brickman citation to the hedonic-adaptation paragraph. |
| The One Thing the Cards Cannot Honestly Do | Expand per **Cluster A**: one linked paragraph per mechanism, Blackmore + Ivtzan & French as the direct tests, replication failures as the close. |
| Why the Cards Can Still Help | Expand per **Cluster B**: one linked paragraph per mechanism; keep the art-analogy opening. |
| Gates and Oracles / palantír | Merge fragments into paragraphs; content stays. |
| The Light Is in the Eyes of the Beholder | Merge fragments; keep as the emotional close. |
| Continue the Conversation | Keep; edit-on-GitHub link stays. |
| Further Reading | Rebuild per **§2b**: links on every entry, thematic groups, dossier pointer. |

Every existing citation and idea survives; nothing the builder liked is cut.

**Phase 2 — audit + verify.** Post-draft audit checklist (absolutism grep, feeling tags,
one-pass-per-critique); every bibliography link resolves; read start-to-finish once; render
check in course-viewer at 390×844; regenerate mirrors (`scripts/course_to_grammar.py` /
`build_reading_course.py` as applicable), then `build_meta_grammar.py` + `check_all.py` →
"all checks passed", dangling=0.

**Phase 1b — the three new courses** (after the flagship, before the sweep): the two
literature deep dives (§2a) and the Claude Desktop course (§2c), each via the four-phase
method in HOW-TO-WRITE-A-COURSE.md, registered in `COURSE_GROUPS`.

**Phase 3 — sweep the rest of the reader-facing spine**, same contract:

1. `intention-setting.mdx` — bold diet; dedupe the palantír passage against the flagship
   (full treatment lives in How the Cards Can Work). Retitle the
   `marsha-linehan-reads-the-tarot.mdx` redirect stub to the school ("DBT") per the house
   rule on living teachers.
2. `reading-the-cards.mdx` — audit-first; rewrite only failing sections.
3. `tarot-and-the-crack.mdx`, `history-of-tarot.mdx`, `divination-traditions.mdx`,
   `tarot-today.mdx` — one pass each.
4. Stubs and short pages — titles/links only.

**Phase 4 — card-level text (later, optional).** Spot-audit Scene/Symbol sections for the
same failure modes; full pass only if the spot-check fails.

**Phase 5 — publish.** Reconcile dev/main per the integration doc (never discard the App's
write-backs on main). That is the "proudly publish" moment.

## 6. Already fixed on the plan branch (Jul 15)

- **One assistant, the real one.** The hand-rolled plum sparkle-toggle + bare `/assistant`
  iframe on `pages/course-viewer.html`, `viewers/cards.html`, `viewers/tree-viewer.html`
  opened as a dead-end shell next to the shared launcher. All three now load the shared
  `assistant.js` (the recursive.eco item that opens the real thing), finishing the
  retirement started in commit `7ed1224`.
- **QR chip is icon-only.** The "Open on phone" label text is gone site-wide (the chip in
  the course hero keeps its accessible label and still pops the scannable lightbox).

## 7. Definition of publishable (per essay)

- [ ] Paragraphs of 3–6 sentences carry the argument; single-sentence beats ≤2 per essay;
      no bullet lists or tables carrying arguments; bold within budget.
- [ ] Every empirical claim linked inline; every bibliography entry linked; full-dossier
      pointer present; all links resolve.
- [ ] No reframe stated twice; no feeling tags; absolutism grep clean.
- [ ] No content duplicated against a sibling course (cross-link instead).
- [ ] Renders clean in course-viewer at mobile width; `check_all.py` passes.
- [ ] Read aloud once, start to finish, without wincing.
