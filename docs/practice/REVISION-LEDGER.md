# Revision ledger

**For any future session:** when PlayfulProcess practises with a chapter or a card, update its
line here. Set the status, put the date (YYYY-MM-DD) in the Date column, and add a few words in
Notes: what she read, what she changed, what she wants changed. A single card from a deck counts
for the deck's line; say which card in Notes. Do not mark anything as read or revised on her
behalf unless she said so. The daily order lives in [READING-PATH.md](READING-PATH.md).

Statuses, one per line:

- **not yet read in practice**: nobody has told us she has worked with it in practice.
- **read in practice**: she read it in practice and said so.
- **revised by PlayfulProcess**: she changed the text herself, or told a session exactly what to change.

## How this was seeded (2026-10-08)

Every line starts as **not yet read in practice**. There is no record of practice in git, so nothing could be
seeded as read.

For "revised", the git history of this repo was read file by file (`git log` and `git blame` on
branch `due/oct8`):

- Commits with a `Co-Authored-By: Claude` trailer, or made by the Claude account, are
  Claude-assisted.
- Many commits under your name have no trailer but were made from your machine by
  Claude sessions (their messages say "Builder direction", "her live test" and so on). They are
  counted as "local without trailer" and were not taken as your own revisions.
- The clearest sign of your own hand is a commit made in the GitHub web editor (committer
  "GitHub") under your name with no Claude trailer. Five exist in the whole history. Two touch the
  files listed here: `how-tarot-works.mdx` on 2026-07-09 (later rewritten, see its note) and
  the Oswald Wirth deck on 2026-06-24 (the creator link only). Neither leaves your revision on the
  page today, so neither line was seeded as revised.
- App write-backs (recursive-eco[bot]) carry edits made in the recursive.eco app. The commits do
  not record who made the edit, so they were not counted either way.

If any of this is wrong, because you did revise something that git cannot show, change the line.

"Last changed" in Notes is the newest commit that still owns a line of that chapter (`git blame`),
so a chapter whose words you revised long ago may still show a recent date from a small fix.

## Courses (229 chapters)

Chapters are the `##` sections of each course in `course/`, in the order of the reading path.

### [How the Cards Can Work](https://tarot.recursive.eco/pages/course-viewer.html?course=how-tarot-works)

Commits to this file: 12 Claude-assisted, 2 local without trailer, 1 GitHub web editor. You rewrote this course in the GitHub editor on 2026-07-09 (4c90f4b). A Claude-assisted rewrite on 2026-07-15 (5d82e7e) replaced most of that text, so what is on the page now is not the version you revised.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=how-tarot-works) | not yet read in practice | | last changed 2026-07-30 |
| [Why fiction changes real lives](https://tarot.recursive.eco/pages/course-viewer.html?course=how-tarot-works#why-fiction-changes-real-lives) | not yet read in practice | | last changed 2026-07-15 |
| [The one thing the cards cannot honestly do](https://tarot.recursive.eco/pages/course-viewer.html?course=how-tarot-works#the-one-thing-the-cards-cannot-honestly-do) | not yet read in practice | | last changed 2026-10-08 |
| [Why the cards can still help](https://tarot.recursive.eco/pages/course-viewer.html?course=how-tarot-works#why-the-cards-can-still-help) | not yet read in practice | | last changed 2026-07-30 |
| [The crystal ball and the gate](https://tarot.recursive.eco/pages/course-viewer.html?course=how-tarot-works#the-crystal-ball-and-the-gate) | not yet read in practice | | last changed 2026-07-30 |
| [The light is in the eyes of the beholder](https://tarot.recursive.eco/pages/course-viewer.html?course=how-tarot-works#the-light-is-in-the-eyes-of-the-beholder) | not yet read in practice | | last changed 2026-07-15 |
| [Continue the conversation](https://tarot.recursive.eco/pages/course-viewer.html?course=how-tarot-works#continue-the-conversation) | not yet read in practice | | last changed 2026-07-15 |
| [Further reading](https://tarot.recursive.eco/pages/course-viewer.html?course=how-tarot-works#further-reading) | not yet read in practice | | last changed 2026-10-08 |

### [What a Reading Can Do](https://tarot.recursive.eco/pages/course-viewer.html?course=what-a-reading-can-do)

Commits to this file: 2 Claude-assisted, 1 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=what-a-reading-can-do) | not yet read in practice | | last changed 2026-07-15 |
| [Projection — the surface you fill](https://tarot.recursive.eco/pages/course-viewer.html?course=what-a-reading-can-do#projection-the-surface-you-fill) | not yet read in practice | | last changed 2026-07-20 |
| [Re-narration — the story you can finally look at](https://tarot.recursive.eco/pages/course-viewer.html?course=what-a-reading-can-do#re-narration-the-story-you-can-finally-look-at) | not yet read in practice | | last changed 2026-07-15 |
| [Productive randomness — the grooves the shuffle breaks](https://tarot.recursive.eco/pages/course-viewer.html?course=what-a-reading-can-do#productive-randomness-the-grooves-the-shuffle-breaks) | not yet read in practice | | last changed 2026-07-30 |
| [Ritual — the container that does real work](https://tarot.recursive.eco/pages/course-viewer.html?course=what-a-reading-can-do#ritual-the-container-that-does-real-work) | not yet read in practice | | last changed 2026-07-15 |
| [The stance that unlocks all four](https://tarot.recursive.eco/pages/course-viewer.html?course=what-a-reading-can-do#the-stance-that-unlocks-all-four) | not yet read in practice | | last changed 2026-07-20 |
| [Sources](https://tarot.recursive.eco/pages/course-viewer.html?course=what-a-reading-can-do#sources) | not yet read in practice | | last changed 2026-07-15 |

### [Why a Reading Feels So Personal](https://tarot.recursive.eco/pages/course-viewer.html?course=why-a-reading-feels-personal)

Commits to this file: 5 Claude-assisted, 1 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=why-a-reading-feels-personal) | not yet read in practice | | last changed 2026-07-15 |
| [The debunking that needed its own debunking](https://tarot.recursive.eco/pages/course-viewer.html?course=why-a-reading-feels-personal#the-debunking-that-needed-its-own-debunking) | not yet read in practice | | last changed 2026-10-08 |
| [Cold reading — the same effect, run on purpose](https://tarot.recursive.eco/pages/course-viewer.html?course=why-a-reading-feels-personal#cold-reading-the-same-effect-run-on-purpose) | not yet read in practice | | last changed 2026-07-15 |
| [Tarot, tested directly](https://tarot.recursive.eco/pages/course-viewer.html?course=why-a-reading-feels-personal#tarot-tested-directly) | not yet read in practice | | last changed 2026-08-11 |
| [The bigger claim, tested at scale](https://tarot.recursive.eco/pages/course-viewer.html?course=why-a-reading-feels-personal#the-bigger-claim-tested-at-scale) | not yet read in practice | | last changed 2026-07-15 |
| [The honest limits of the claim](https://tarot.recursive.eco/pages/course-viewer.html?course=why-a-reading-feels-personal#the-honest-limits-of-the-claim) | not yet read in practice | | last changed 2026-07-15 |
| [What to do with all this](https://tarot.recursive.eco/pages/course-viewer.html?course=why-a-reading-feels-personal#what-to-do-with-all-this) | not yet read in practice | | last changed 2026-07-20 |
| [Sources](https://tarot.recursive.eco/pages/course-viewer.html?course=why-a-reading-feels-personal#sources) | not yet read in practice | | last changed 2026-07-15 |

### [Tarot & the Crack](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack)

Commits to this file: 9 Claude-assisted, 1 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack) | not yet read in practice | | last changed 2026-06-21 |
| [The book that promised everything](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#the-book-that-promised-everything) | not yet read in practice | | last changed 2026-10-08 |
| [Why I shuffle](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#why-i-shuffle) | not yet read in practice | | last changed 2026-07-30 |
| [The reading that changed the question](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#the-reading-that-changed-the-question) | not yet read in practice | | last changed 2026-07-15 |
| [There is always a crack](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#there-is-always-a-crack) | not yet read in practice | | last changed 2026-06-14 |
| [The ground is chosen, not given](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#the-ground-is-chosen-not-given) | not yet read in practice | | last changed 2026-06-14 |
| [Structures, process, possibilities](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#structures-process-possibilities) | not yet read in practice | | last changed 2026-07-15 |
| [The sun does not need to be more](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#the-sun-does-not-need-to-be-more) | not yet read in practice | | last changed 2026-06-21 |
| [Two beliefs I had been confusing](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#two-beliefs-i-had-been-confusing) | not yet read in practice | | last changed 2026-06-22 |
| [The altar, and how one speaks to the invisible](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#the-altar-and-how-one-speaks-to-the-invisible) | not yet read in practice | | last changed 2026-06-22 |
| [The numinous borrows our language](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#the-numinous-borrows-our-language) | not yet read in practice | | last changed 2026-06-22 |
| [Faith, curiosity, and the skeptic you keep at the table](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#faith-curiosity-and-the-skeptic-you-keep-at-the-table) | not yet read in practice | | last changed 2026-06-22 |
| [Dialoguing with the crack](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-the-crack#dialoguing-with-the-crack) | not yet read in practice | | last changed 2026-06-22 |

### [Intention Setting](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting)

Commits to this file: 10 Claude-assisted, 2 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting) | not yet read in practice | | last changed 2026-07-20 |
| [DBT](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#dbt) | not yet read in practice | | last changed 2026-07-15 |
| [Kant](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#kant) | not yet read in practice | | last changed 2026-07-07 |
| [The Ecosystem](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#the-ecosystem) | not yet read in practice | | last changed 2026-06-21 |
| [The Golden Dawn](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#the-golden-dawn) | not yet read in practice | | last changed 2026-07-30 |
| [Jung](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#jung) | not yet read in practice | | last changed 2026-06-22 |
| [Non-Dual Tantra](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#non-dual-tantra) | not yet read in practice | | last changed 2026-07-15 |
| [Post-Activism](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#post-activism) | not yet read in practice | | last changed 2026-07-15 |
| [Hospicing Modernity](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#hospicing-modernity) | not yet read in practice | | last changed 2026-07-15 |
| [Game, crystal ball, gate](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#game-crystal-ball-gate) | not yet read in practice | | last changed 2026-07-30 |
| [Why this matters off the table](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#why-this-matters-off-the-table) | not yet read in practice | | last changed 2026-07-30 |
| [Keep digging — and contribute](https://tarot.recursive.eco/pages/course-viewer.html?course=intention-setting#keep-digging-and-contribute) | not yet read in practice | | last changed 2026-07-15 |

### [Your Card Table](https://tarot.recursive.eco/pages/course-viewer.html?course=your-card-table)

Commits to this file: 2 Claude-assisted.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=your-card-table) | not yet read in practice | | last changed 2026-10-02 |
| [The practice](https://tarot.recursive.eco/pages/course-viewer.html?course=your-card-table#the-practice) | not yet read in practice | | last changed 2026-10-02 |
| [The notation, in five minutes](https://tarot.recursive.eco/pages/course-viewer.html?course=your-card-table#the-notation-in-five-minutes) | not yet read in practice | | last changed 2026-10-02 |
| [Try it](https://tarot.recursive.eco/pages/course-viewer.html?course=your-card-table#try-it) | not yet read in practice | | last changed 2026-10-03 |
| [What it is not](https://tarot.recursive.eco/pages/course-viewer.html?course=your-card-table#what-it-is-not) | not yet read in practice | | last changed 2026-10-02 |

### [How Could DBT Read the Tarot?](https://tarot.recursive.eco/pages/course-viewer.html?course=marsha-linehan-reads-the-tarot)

Commits to this file: 6 Claude-assisted.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=marsha-linehan-reads-the-tarot) | not yet read in practice | | last changed 2026-07-15 |
| [Wise mind — the synthesis Kant split](https://tarot.recursive.eco/pages/course-viewer.html?course=marsha-linehan-reads-the-tarot#wise-mind-the-synthesis-kant-split) | not yet read in practice | | last changed 2026-06-21 |
| [The dialectic — a card holds two true things](https://tarot.recursive.eco/pages/course-viewer.html?course=marsha-linehan-reads-the-tarot#the-dialectic-a-card-holds-two-true-things) | not yet read in practice | | last changed 2026-06-21 |
| [Radical acceptance — the Tower is not a verdict](https://tarot.recursive.eco/pages/course-viewer.html?course=marsha-linehan-reads-the-tarot#radical-acceptance-the-tower-is-not-a-verdict) | not yet read in practice | | last changed 2026-06-21 |
| [Neither for nor against — how to relate](https://tarot.recursive.eco/pages/course-viewer.html?course=marsha-linehan-reads-the-tarot#neither-for-nor-against-how-to-relate) | not yet read in practice | | last changed 2026-06-22 |
| [The three filters — is this a wise reading?](https://tarot.recursive.eco/pages/course-viewer.html?course=marsha-linehan-reads-the-tarot#the-three-filters-is-this-a-wise-reading) | not yet read in practice | | last changed 2026-06-30 |
| [How to cast in wise mind](https://tarot.recursive.eco/pages/course-viewer.html?course=marsha-linehan-reads-the-tarot#how-to-cast-in-wise-mind) | not yet read in practice | | last changed 2026-06-21 |
| [Two voices, one ecosystem](https://tarot.recursive.eco/pages/course-viewer.html?course=marsha-linehan-reads-the-tarot#two-voices-one-ecosystem) | not yet read in practice | | last changed 2026-06-21 |

### [How Could Kant Read the Tarot?](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot)

Commits to this file: 5 Claude-assisted, 2 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot) | not yet read in practice | | last changed 2026-10-08 |
| [The same decade — Kant and the cards](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#the-same-decade-kant-and-the-cards) | not yet read in practice | | last changed 2026-06-21 |
| [The one test — autonomy or heteronomy](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#the-one-test-autonomy-or-heteronomy) | not yet read in practice | | last changed 2026-07-07 |
| [Four ways to play](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#four-ways-to-play) | not yet read in practice | | last changed 2026-10-08 |
| [The Devil's Picture Book — avarice, and the over-ban](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#the-devil-s-picture-book-avarice-and-the-over-ban) | not yet read in practice | | last changed 2026-06-21 |
| [The alea machine — Brazilian bets](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#the-alea-machine-brazilian-bets) | not yet read in practice | | last changed 2026-06-21 |
| [The con — Forer, Barnum, cold reading](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#the-con-forer-barnum-cold-reading) | not yet read in practice | | last changed 2026-10-08 |
| [The flip — divination you author, held flexibly](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#the-flip-divination-you-author-held-flexibly) | not yet read in practice | | last changed 2026-06-22 |
| [The good will — why open a deck at all?](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#the-good-will-why-open-a-deck-at-all) | not yet read in practice | | last changed 2026-06-21 |
| [The purified motive — Kant and the tantra](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#the-purified-motive-kant-and-the-tantra) | not yet read in practice | | last changed 2026-06-22 |
| [Six people meet the cards](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#six-people-meet-the-cards) | not yet read in practice | | last changed 2026-07-30 |
| [Why the game outlives the belief](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#why-the-game-outlives-the-belief) | not yet read in practice | | last changed 2026-10-08 |
| [Where I part ways — the emergence of morality](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#where-i-part-ways-the-emergence-of-morality) | not yet read in practice | | last changed 2026-07-07 |
| [The deck is a collective endeavour — so no one owns its meaning](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#the-deck-is-a-collective-endeavour-so-no-one-owns-its-meaning) | not yet read in practice | | last changed 2026-07-07 |
| [Sapere aude, with a deck](https://tarot.recursive.eco/pages/course-viewer.html?course=kant-and-the-tarot#sapere-aude-with-a-deck) | not yet read in practice | | last changed 2026-07-07 |

### [Morality Is an Ecosystem](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem)

Commits to this file: 3 Claude-assisted.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem) | not yet read in practice | | last changed 2026-06-21 |
| [Nobody sets the price](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#nobody-sets-the-price) | not yet read in practice | | last changed 2026-06-21 |
| [What "emergent" means](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#what-emergent-means) | not yet read in practice | | last changed 2026-06-21 |
| [Kant's lonely method](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#kant-s-lonely-method) | not yet read in practice | | last changed 2026-06-21 |
| [Morality was never derived; it evolved](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#morality-was-never-derived-it-evolved) | not yet read in practice | | last changed 2026-06-21 |
| [There is more than one healthy wood](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#there-is-more-than-one-healthy-wood) | not yet read in practice | | last changed 2026-07-15 |
| [Gifts, passions, and wounds](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#gifts-passions-and-wounds) | not yet read in practice | | last changed 2026-06-21 |
| [The is/ought guard](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#the-is-ought-guard) | not yet read in practice | | last changed 2026-07-15 |
| [Where Kant survives — relocated, not refuted](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#where-kant-survives-relocated-not-refuted) | not yet read in practice | | last changed 2026-06-21 |
| [Gardening, not legislation](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#gardening-not-legislation) | not yet read in practice | | last changed 2026-07-15 |
| [A garden we are planted in](https://tarot.recursive.eco/pages/course-viewer.html?course=morality-is-an-ecosystem#a-garden-we-are-planted-in) | not yet read in practice | | last changed 2026-06-21 |

### [Jung Reads the Tarot](https://tarot.recursive.eco/pages/course-viewer.html?course=jung-reads-the-tarot)

Commits to this file: 6 Claude-assisted.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=jung-reads-the-tarot) | not yet read in practice | | last changed 2026-07-07 |
| [The unconscious is the other half of you](https://tarot.recursive.eco/pages/course-viewer.html?course=jung-reads-the-tarot#the-unconscious-is-the-other-half-of-you) | not yet read in practice | | last changed 2026-06-22 |
| [The shadow: the card you did not want](https://tarot.recursive.eco/pages/course-viewer.html?course=jung-reads-the-tarot#the-shadow-the-card-you-did-not-want) | not yet read in practice | | last changed 2026-06-22 |
| [Archetypes: why the images feel older than you](https://tarot.recursive.eco/pages/course-viewer.html?course=jung-reads-the-tarot#archetypes-why-the-images-feel-older-than-you) | not yet read in practice | | last changed 2026-07-20 |
| [Active imagination: let the figure speak](https://tarot.recursive.eco/pages/course-viewer.html?course=jung-reads-the-tarot#active-imagination-let-the-figure-speak) | not yet read in practice | | last changed 2026-06-22 |
| [Synchronicity: permission, honestly framed](https://tarot.recursive.eco/pages/course-viewer.html?course=jung-reads-the-tarot#synchronicity-permission-honestly-framed) | not yet read in practice | | last changed 2026-07-20 |
| [How to cast in the depths](https://tarot.recursive.eco/pages/course-viewer.html?course=jung-reads-the-tarot#how-to-cast-in-the-depths) | not yet read in practice | | last changed 2026-06-22 |
| [One voice among many](https://tarot.recursive.eco/pages/course-viewer.html?course=jung-reads-the-tarot#one-voice-among-many) | not yet read in practice | | last changed 2026-06-22 |

### [The Non-Dual Tantra Lens](https://tarot.recursive.eco/pages/course-viewer.html?course=non-dual-tantra-reads-the-tarot)

Commits to this file: 5 Claude-assisted.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=non-dual-tantra-reads-the-tarot) | not yet read in practice | | last changed 2026-07-15 |
| [Līlā — the cards as one more game](https://tarot.recursive.eco/pages/course-viewer.html?course=non-dual-tantra-reads-the-tarot#l-l-the-cards-as-one-more-game) | not yet read in practice | | last changed 2026-06-22 |
| [Pratyabhijñā — the recognition that the two are one](https://tarot.recursive.eco/pages/course-viewer.html?course=non-dual-tantra-reads-the-tarot#pratyabhij-the-recognition-that-the-two-are-one) | not yet read in practice | | last changed 2026-06-22 |
| [Spanda — the chill is the play stirring](https://tarot.recursive.eco/pages/course-viewer.html?course=non-dual-tantra-reads-the-tarot#spanda-the-chill-is-the-play-stirring) | not yet read in practice | | last changed 2026-06-22 |
| [Camatkāra — hold it with delight, not dread](https://tarot.recursive.eco/pages/course-viewer.html?course=non-dual-tantra-reads-the-tarot#camatk-ra-hold-it-with-delight-not-dread) | not yet read in practice | | last changed 2026-07-15 |
| [How to cast as līlā](https://tarot.recursive.eco/pages/course-viewer.html?course=non-dual-tantra-reads-the-tarot#how-to-cast-as-l-l) | not yet read in practice | | last changed 2026-06-22 |
| [One game among the voices](https://tarot.recursive.eco/pages/course-viewer.html?course=non-dual-tantra-reads-the-tarot#one-game-among-the-voices) | not yet read in practice | | last changed 2026-06-22 |

### [The Post-Activism Lens](https://tarot.recursive.eco/pages/course-viewer.html?course=post-activism-reads-the-tarot)

Commits to this file: 5 Claude-assisted.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=post-activism-reads-the-tarot) | not yet read in practice | | last changed 2026-06-22 |
| [Slowing is not slowness](https://tarot.recursive.eco/pages/course-viewer.html?course=post-activism-reads-the-tarot#slowing-is-not-slowness) | not yet read in practice | | last changed 2026-06-22 |
| [The card as sanctuary](https://tarot.recursive.eco/pages/course-viewer.html?course=post-activism-reads-the-tarot#the-card-as-sanctuary) | not yet read in practice | | last changed 2026-06-22 |
| [The crack is where the new gets in](https://tarot.recursive.eco/pages/course-viewer.html?course=post-activism-reads-the-tarot#the-crack-is-where-the-new-gets-in) | not yet read in practice | | last changed 2026-06-22 |
| [How to cast in the slowing](https://tarot.recursive.eco/pages/course-viewer.html?course=post-activism-reads-the-tarot#how-to-cast-in-the-slowing) | not yet read in practice | | last changed 2026-06-22 |
| [One voice in an ecosystem of conscience](https://tarot.recursive.eco/pages/course-viewer.html?course=post-activism-reads-the-tarot#one-voice-in-an-ecosystem-of-conscience) | not yet read in practice | | last changed 2026-07-15 |

### [The Hospicing-Modernity Lens](https://tarot.recursive.eco/pages/course-viewer.html?course=hospicing-modernity-reads-the-tarot)

Commits to this file: 5 Claude-assisted.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=hospicing-modernity-reads-the-tarot) | not yet read in practice | | last changed 2026-07-15 |
| [Hospicing and midwifing — two labors in one image](https://tarot.recursive.eco/pages/course-viewer.html?course=hospicing-modernity-reads-the-tarot#hospicing-and-midwifing-two-labors-in-one-image) | not yet read in practice | | last changed 2026-06-22 |
| [Complicity — the grammar shows you inside the thing](https://tarot.recursive.eco/pages/course-viewer.html?course=hospicing-modernity-reads-the-tarot#complicity-the-grammar-shows-you-inside-the-thing) | not yet read in practice | | last changed 2026-06-22 |
| [Staying with the trouble — against the rush to hope](https://tarot.recursive.eco/pages/course-viewer.html?course=hospicing-modernity-reads-the-tarot#staying-with-the-trouble-against-the-rush-to-hope) | not yet read in practice | | last changed 2026-06-22 |
| [How to cast in the hospicing stance](https://tarot.recursive.eco/pages/course-viewer.html?course=hospicing-modernity-reads-the-tarot#how-to-cast-in-the-hospicing-stance) | not yet read in practice | | last changed 2026-06-22 |
| [One voice in an ecosystem](https://tarot.recursive.eco/pages/course-viewer.html?course=hospicing-modernity-reads-the-tarot#one-voice-in-an-ecosystem) | not yet read in practice | | last changed 2026-07-15 |

### [The Golden Dawn — the Map and the Walk](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path)

Commits to this file: 5 Claude-assisted, 1 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path) | not yet read in practice | | last changed 2026-07-30 |
| [One honest frame](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path#one-honest-frame) | not yet read in practice | | last changed 2026-07-30 |
| [Who they were](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path#who-they-were) | not yet read in practice | | last changed 2026-10-08 |
| [The Tree, for a first reader](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path#the-tree-for-a-first-reader) | not yet read in practice | | last changed 2026-07-30 |
| [Every card has an address](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path#every-card-has-an-address) | not yet read in practice | | last changed 2026-10-08 |
| [How they actually used it](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path#how-they-actually-used-it) | not yet read in practice | | last changed 2026-10-08 |
| [Walking four gates](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path#walking-four-gates) | not yet read in practice | | last changed 2026-07-30 |
| [The deck it gave the world: Rider-Waite-Smith](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path#the-deck-it-gave-the-world-rider-waite-smith) | not yet read in practice | | last changed 2026-07-30 |
| [Holding it honestly](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path#holding-it-honestly) | not yet read in practice | | last changed 2026-07-30 |
| [Where the rest lives — and where to go deeper](https://tarot.recursive.eco/pages/course-viewer.html?course=walking-the-golden-dawn-path#where-the-rest-lives-and-where-to-go-deeper) | not yet read in practice | | last changed 2026-07-30 |

### [The History of Tarot](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot)

Commits to this file: 32 Claude-assisted, 3 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot) | not yet read in practice | | last changed 2026-07-30 |
| [Before Tarot — the cards come west](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#before-tarot-the-cards-come-west) | not yet read in practice | | last changed 2026-10-08 |
| [The First Deck — and What Came Before](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#the-first-deck-and-what-came-before) | not yet read in practice | | last changed 2026-07-27 |
| [A Game, First of All](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#a-game-first-of-all) | not yet read in practice | | last changed 2026-10-08 |
| [The Lineage](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#the-lineage) | not yet read in practice | | last changed 2026-07-15 |
| [The three Ways — how the family split](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#the-three-ways-how-the-family-split) | not yet read in practice | | last changed 2026-07-30 |
| [Why a tree](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#why-a-tree) | not yet read in practice | | last changed 2026-06-21 |
| [Seeing it from every angle](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#seeing-it-from-every-angle) | not yet read in practice | | last changed 2026-06-21 |
| [The Decks](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#the-decks) | not yet read in practice | | last changed 2026-06-15 |
| [A Few Plates](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#a-few-plates) | not yet read in practice | | last changed 2026-06-15 |
| [The Divination Question](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#the-divination-question) | not yet read in practice | | last changed 2026-09-02 |
| [The Four Suits](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#the-four-suits) | not yet read in practice | | last changed 2026-07-15 |
| [The Numbers](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#the-numbers) | not yet read in practice | | last changed 2026-06-15 |
| [The Trumps](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#the-trumps) | not yet read in practice | | last changed 2026-06-23 |
| [Tarot today — the recursion continues](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#tarot-today-the-recursion-continues) | not yet read in practice | | last changed 2026-07-30 |
| [Keep digging — and contribute](https://tarot.recursive.eco/pages/course-viewer.html?course=history-of-tarot#keep-digging-and-contribute) | not yet read in practice | | last changed 2026-06-23 |

### [Games of the Tarot — A Player's Companion](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot)

Commits to this file: 2 Claude-assisted, 1 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot) | not yet read in practice | | last changed 2026-06-23 |
| [The first thing to know](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot#the-first-thing-to-know) | not yet read in practice | | last changed 2026-07-30 |
| [The shape of every tarot game](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot#the-shape-of-every-tarot-game) | not yet read in practice | | last changed 2026-06-23 |
| [Minchiate — Florence's maximalist variant (97 cards)](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot#minchiate-florence-s-maximalist-variant-97-cards) | not yet read in practice | | last changed 2026-06-23 |
| [Tarocchino di Bologna — the compact cousin (62 cards)](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot#tarocchino-di-bologna-the-compact-cousin-62-cards) | not yet read in practice | | last changed 2026-06-23 |
| [Tarot de Marseille — the printed standard](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot#tarot-de-marseille-the-printed-standard) | not yet read in practice | | last changed 2026-06-23 |
| [Mantegna — the odd one out (50 cards, not a game)](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot#mantegna-the-odd-one-out-50-cards-not-a-game) | not yet read in practice | | last changed 2026-06-23 |
| [Where the cards came from](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot#where-the-cards-came-from) | not yet read in practice | | last changed 2026-06-23 |
| [Sources](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot#sources) | not yet read in practice | | last changed 2026-06-23 |
| [Keep digging — and contribute](https://tarot.recursive.eco/pages/course-viewer.html?course=games-of-the-tarot#keep-digging-and-contribute) | not yet read in practice | | last changed 2026-06-23 |

### [Same Card, Every Deck](https://tarot.recursive.eco/pages/course-viewer.html?course=same-card-every-deck)

Commits to this file: 2 Claude-assisted. A draft: some sections are still stubs.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=same-card-every-deck) | not yet read in practice | | last changed 2026-10-04 |
| [The tool in one minute](https://tarot.recursive.eco/pages/course-viewer.html?course=same-card-every-deck#the-tool-in-one-minute) | not yet read in practice | | last changed 2026-08-11 |
| [Exercise 1 — Find the turn](https://tarot.recursive.eco/pages/course-viewer.html?course=same-card-every-deck#exercise-1-find-the-turn) | not yet read in practice | | last changed 2026-08-11 |
| [Exercise 2 — The swap hiding in plain sight](https://tarot.recursive.eco/pages/course-viewer.html?course=same-card-every-deck#exercise-2-the-swap-hiding-in-plain-sight) | not yet read in practice | | last changed 2026-08-11 |
| [What the pictures can prove — and what they can't](https://tarot.recursive.eco/pages/course-viewer.html?course=same-card-every-deck#what-the-pictures-can-prove-and-what-they-can-t) | not yet read in practice | | last changed 2026-08-11 |
| [Exercise 3 — When the tool says no (and what still slips through)](https://tarot.recursive.eco/pages/course-viewer.html?course=same-card-every-deck#exercise-3-when-the-tool-says-no-and-what-still-slips-through) | not yet read in practice | | last changed 2026-08-11 |
| [Document what you find](https://tarot.recursive.eco/pages/course-viewer.html?course=same-card-every-deck#document-what-you-find) | not yet read in practice | | last changed 2026-08-11 |
| [Sources & honesty](https://tarot.recursive.eco/pages/course-viewer.html?course=same-card-every-deck#sources-honesty) | not yet read in practice | | last changed 2026-08-11 |

### [How Humans Have Cast Lots](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions)

Commits to this file: 7 Claude-assisted, 1 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions) | not yet read in practice | | last changed 2026-07-30 |
| [How old is this, really?](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#how-old-is-this-really) | not yet read in practice | | last changed 2026-07-30 |
| [Ifá — West Africa (Yoruba)](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#if-west-africa-yoruba) | not yet read in practice | | last changed 2026-06-22 |
| [The casting of lots — ancient Israel](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#the-casting-of-lots-ancient-israel) | not yet read in practice | | last changed 2026-07-30 |
| [The I Ching — China](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#the-i-ching-china) | not yet read in practice | | last changed 2026-06-22 |
| [Delphi and the Roman signs — the Greco-Roman world](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#delphi-and-the-roman-signs-the-greco-roman-world) | not yet read in practice | | last changed 2026-06-22 |
| [The runes — pre-Christian Scandinavia and Germania](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#the-runes-pre-christian-scandinavia-and-germania) | not yet read in practice | | last changed 2026-10-08 |
| [Oracle bones — Shang dynasty China](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#oracle-bones-shang-dynasty-china) | not yet read in practice | | last changed 2026-06-22 |
| [Mo — Tibetan Buddhism](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#mo-tibetan-buddhism) | not yet read in practice | | last changed 2026-07-30 |
| [Whose fairness, whose adaptation](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#whose-fairness-whose-adaptation) | not yet read in practice | | last changed 2026-07-30 |
| [What the whole tour shows](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#what-the-whole-tour-shows) | not yet read in practice | | last changed 2026-07-30 |
| [On randomness itself](https://tarot.recursive.eco/pages/course-viewer.html?course=divination-traditions#on-randomness-itself) | not yet read in practice | | last changed 2026-07-20 |

### [Tarot Today — a living question](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today)

Commits to this file: 11 Claude-assisted, 2 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today) | not yet read in practice | | last changed 2026-07-15 |
| [An unlikely rival](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#an-unlikely-rival) | not yet read in practice | | last changed 2026-10-08 |
| [Something you can hold](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#something-you-can-hold) | not yet read in practice | | last changed 2026-07-06 |
| [A cheaper door in](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#a-cheaper-door-in) | not yet read in practice | | last changed 2026-07-20 |
| [Tarot's cousins are surging too](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#tarot-s-cousins-are-surging-too) | not yet read in practice | | last changed 2026-10-08 |
| [Who's re-authoring the deck, and why](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#who-s-re-authoring-the-deck-and-why) | not yet read in practice | | last changed 2026-10-08 |
| [A practice without a church](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#a-practice-without-a-church) | not yet read in practice | | last changed 2026-07-06 |
| [What's still thin](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#what-s-still-thin) | not yet read in practice | | last changed 2026-10-02 |
| [The invitation](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#the-invitation) | not yet read in practice | | last changed 2026-07-06 |
| [A bricoleur's bench — the essential readings](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#a-bricoleur-s-bench-the-essential-readings) | not yet read in practice | | last changed 2026-10-02 |
| [Keep digging — and contribute](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-today#keep-digging-and-contribute) | not yet read in practice | | last changed 2026-07-20 |

### [Tarot as a Source of Fiction](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction)

Commits to this file: 5 Claude-assisted.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction) | not yet read in practice | | last changed 2026-09-02 |
| [1. The man, and why the answer matters](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction#1-the-man-and-why-the-answer-matters) | not yet read in practice | | last changed 2026-09-02 |
| [2. A commission, not a calling](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction#2-a-commission-not-a-calling) | not yet read in practice | | last changed 2026-09-02 |
| [3. The machine](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction#3-the-machine) | not yet read in practice | | last changed 2026-09-02 |
| [4. What it produced — a worked example](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction#4-what-it-produced-a-worked-example) | not yet read in practice | | last changed 2026-09-02 |
| [5. The confession, which is the best part](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction#5-the-confession-which-is-the-best-part) | not yet read in practice | | last changed 2026-09-02 |
| [6. The third part he never wrote](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction#6-the-third-part-he-never-wrote) | not yet read in practice | | last changed 2026-09-02 |
| [7. The company it keeps — and the contrast that matters](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction#7-the-company-it-keeps-and-the-contrast-that-matters) | not yet read in practice | | last changed 2026-10-02 |
| [8. What a fiction machine has to risk](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction#8-what-a-fiction-machine-has-to-risk) | not yet read in practice | | last changed 2026-09-02 |
| [9. Try the method yourself](https://tarot.recursive.eco/pages/course-viewer.html?course=tarot-and-fiction#9-try-the-method-yourself) | not yet read in practice | | last changed 2026-10-02 |

### [Reading the Cards](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards)

Commits to this file: 13 Claude-assisted, 2 local without trailer. The anthology: built from the voice courses, so each part follows the course of the same name. Mark the course, not this page, unless you read it here.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards) | not yet read in practice | | last changed 2026-07-20 |
| [How the Cards Can Work](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#how-the-cards-can-work) | not yet read in practice | | last changed 2026-10-08 |
| [Tarot & the Crack](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#tarot-the-crack) | not yet read in practice | | last changed 2026-10-08 |
| [Intention Setting](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#intention-setting) | not yet read in practice | | last changed 2026-07-30 |
| [How Could Kant Read the Tarot?](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#how-could-kant-read-the-tarot) | not yet read in practice | | last changed 2026-10-08 |
| [How Could DBT Read the Tarot?](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#how-could-dbt-read-the-tarot) | not yet read in practice | | last changed 2026-07-15 |
| [Morality Is an Ecosystem](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#morality-is-an-ecosystem) | not yet read in practice | | last changed 2026-07-15 |
| [Jung Reads the Tarot](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#jung-reads-the-tarot) | not yet read in practice | | last changed 2026-07-30 |
| [The Non-Dual Tantra Lens](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#the-non-dual-tantra-lens) | not yet read in practice | | last changed 2026-07-15 |
| [The Post-Activism Lens](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#the-post-activism-lens) | not yet read in practice | | last changed 2026-07-15 |
| [The Hospicing-Modernity Lens](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#the-hospicing-modernity-lens) | not yet read in practice | | last changed 2026-07-15 |
| [The Golden Dawn — the Map and the Walk](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#the-golden-dawn-the-map-and-the-walk) | not yet read in practice | | last changed 2026-10-08 |
| [How Humans Have Cast Lots](https://tarot.recursive.eco/pages/course-viewer.html?course=reading-the-cards#how-humans-have-cast-lots) | not yet read in practice | | last changed 2026-10-08 |

### [Ways to Contribute](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute)

Commits to this file: 14 Claude-assisted, 4 local without trailer.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute) | not yet read in practice | | last changed 2026-10-08 |
| [Contribute a deck](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#contribute-a-deck) | not yet read in practice | | last changed 2026-08-23 |
| [Contribute a spread](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#contribute-a-spread) | not yet read in practice | | last changed 2026-07-01 |
| [Contribute a course](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#contribute-a-course) | not yet read in practice | | last changed 2026-07-01 |
| [Every deck — and where to correct it](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#every-deck-and-where-to-correct-it) | not yet read in practice | | last changed 2026-10-08 |
| [Rung 1 — Fix it in the app (recursive.eco)](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#rung-1-fix-it-in-the-app-recursive-eco) | not yet read in practice | | last changed 2026-08-23 |
| [Rung 2 — Edit on GitHub (no other tools)](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#rung-2-edit-on-github-no-other-tools) | not yet read in practice | | last changed 2026-06-23 |
| [Rung 3 — Work the repo in Claude.ai](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#rung-3-work-the-repo-in-claude-ai) | not yet read in practice | | last changed 2026-07-15 |
| [Rung 4 — Claude Desktop on the repo](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#rung-4-claude-desktop-on-the-repo) | not yet read in practice | | last changed 2026-07-15 |
| [Rung 5 — The recursive.eco MCP (the full toolkit)](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#rung-5-the-recursive-eco-mcp-the-full-toolkit) | not yet read in practice | | last changed 2026-06-24 |
| [Rung 5 in practice — a real audit-and-improve pass](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#rung-5-in-practice-a-real-audit-and-improve-pass) | not yet read in practice | | last changed 2026-07-27 |
| [The ethos](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#the-ethos) | not yet read in practice | | last changed 2026-06-23 |
| [The one rule (read this)](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#the-one-rule-read-this) | not yet read in practice | | last changed 2026-06-23 |
| [Contribute a video](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute#contribute-a-video) | not yet read in practice | | last changed 2026-06-23 |

### [Working with Claude Desktop](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop)

Commits to this file: 2 Claude-assisted.

| Chapter | Status | Date | Notes |
|---|---|---|---|
| [Opening](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop) | not yet read in practice | | last changed 2026-07-15 |
| [Which Claude is which](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#which-claude-is-which) | not yet read in practice | | last changed 2026-07-15 |
| [GitHub, from zero](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#github-from-zero) | not yet read in practice | | last changed 2026-07-15 |
| [Git, gently](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#git-gently) | not yet read in practice | | last changed 2026-10-08 |
| [Install the tools](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#install-the-tools) | not yet read in practice | | last changed 2026-07-15 |
| [The session habits that save you](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#the-session-habits-that-save-you) | not yet read in practice | | last changed 2026-10-08 |
| [What a pull request is, and how to file a good one](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#what-a-pull-request-is-and-how-to-file-a-good-one) | not yet read in practice | | last changed 2026-07-15 |
| [CLAUDE.md — the repo's standing instructions](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#claude-md-the-repo-s-standing-instructions) | not yet read in practice | | last changed 2026-07-15 |
| [The settings that matter](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#the-settings-that-matter) | not yet read in practice | | last changed 2026-07-15 |
| [The private-folder pattern](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#the-private-folder-pattern) | not yet read in practice | | last changed 2026-07-15 |
| [Where to start](https://tarot.recursive.eco/pages/course-viewer.html?course=working-with-claude-desktop#where-to-start) | not yet read in practice | | last changed 2026-07-15 |

### Pages kept only so old links work

| Page | Status | Date | Notes |
|---|---|---|---|
| [This course has moved](https://tarot.recursive.eco/pages/course-viewer.html?course=build-a-tarot-deck-with-claude) | n/a | | a pointer to another course, nothing to read |
| [How the Golden Dawn Read the Tarot](https://tarot.recursive.eco/pages/course-viewer.html?course=how-the-golden-dawn-read-the-tarot) | n/a | | a pointer to another course, nothing to read |
| [The Light of Tarot](https://tarot.recursive.eco/pages/course-viewer.html?course=the-light-of-tarot) | n/a | | a pointer to another course, nothing to read |

## Decks (36)

Each link opens the deck in the card viewer.

| Deck | Status | Date | Notes |
|---|---|---|---|
| [Visconti-Sforza Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/visconti-sforza-tarot/grammar.json) | not yet read in practice | | 120 items; last changed 2026-10-04; commits: 25 Claude-assisted, 20 local without trailer |
| [Cary-Yale Visconti Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/cary-yale-visconti-tarot/grammar.json) | not yet read in practice | | 105 items; last changed 2026-10-04; commits: 21 Claude-assisted, 9 local without trailer, 1 app write-back |
| [The 'Charles VI' Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/charles-vi-tarot/grammar.json) | not yet read in practice | | 18 items; last changed 2026-10-07; commits: 23 Claude-assisted, 10 local without trailer, 1 app write-back |
| [Minchiate](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/minchiate-florence-tarot/grammar.json) | not yet read in practice | | 147 items; last changed 2026-10-04; commits: 23 Claude-assisted, 8 local without trailer, 1 app write-back |
| [Tarocchino di Bologna](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/tarocchino-bologna/grammar.json) | not yet read in practice | | 97 items; last changed 2026-10-04; commits: 22 Claude-assisted, 9 local without trailer, 1 app write-back |
| [Tarot de Marseille](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/tarot-de-marseille-conver/grammar.json) | not yet read in practice | | 118 items; last changed 2026-10-07; commits: 30 Claude-assisted, 11 local without trailer, 2 app write-backs |
| [Tarot de Besançon / Swiss 1JJ](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/tarot-de-besancon/grammar.json) | not yet read in practice | | 14 items; last changed 2026-10-04; commits: 17 Claude-assisted, 8 local without trailer, 1 app write-back |
| [Oswald Wirth Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/oswald-wirth-tarot/grammar.json) | not yet read in practice | | 23 items; last changed 2026-10-07; commits: 20 Claude-assisted, 12 local without trailer, 1 GitHub web editor, 1 app write-back. Your one web-editor commit here (bb444c1, 2026-06-24) changed only the creator link |
| [Golden Dawn Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/golden-dawn-book-t-tarot/grammar.json) | not yet read in practice | | 104 items; last changed 2026-10-07; commits: 27 Claude-assisted, 18 local without trailer, 1 app write-back |
| [Court de Gébelin's Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/court-de-gebelin-tarot/grammar.json) | not yet read in practice | | 23 items; last changed 2026-10-04; commits: 18 Claude-assisted, 11 local without trailer, 1 app write-back |
| [Etteilla I](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/etteilla-i-livre-de-thot/grammar.json) | not yet read in practice | | 94 items; last changed 2026-10-07; commits: 21 Claude-assisted, 9 local without trailer, 1 app write-back |
| [Etteilla II](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/etteilla-ii-egyptian/grammar.json) | not yet read in practice | | 94 items; last changed 2026-10-07; commits: 20 Claude-assisted, 9 local without trailer, 1 app write-back |
| [Grand Jeu de l'Oracle des Dames](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/etteilla-iii-oracle-des-dames/grammar.json) | not yet read in practice | | 94 items; last changed 2026-10-07; commits: 20 Claude-assisted, 9 local without trailer, 1 app write-back |
| [The 'Mantegna Tarocchi'](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/mantegna-tarocchi/grammar.json) | not yet read in practice | | 64 items; last changed 2026-10-04; commits: 17 Claude-assisted, 10 local without trailer, 1 app write-back |
| [Ma Diao](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/madiao-money-cards/grammar.json) | not yet read in practice | | 18 items; last changed 2026-10-04; commits: 11 Claude-assisted, 10 local without trailer, 1 app write-back |
| [Jacques Viéville Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/vieville-tarot/grammar.json) | not yet read in practice | | 83 items; last changed 2026-10-04; commits: 16 Claude-assisted, 11 local without trailer, 1 app write-back |
| [Belgian Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/belgian-tarot/grammar.json) | not yet read in practice | | 23 items; last changed 2026-10-04; commits: 14 Claude-assisted, 9 local without trailer, 1 app write-back |
| [Tarot de Paris](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/paris-anonymous-tarot/grammar.json) | not yet read in practice | | 83 items; last changed 2026-10-04; commits: 15 Claude-assisted, 10 local without trailer, 1 app write-back |
| [d'Este Tarocchi](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/este-tarot/grammar.json) | not yet read in practice | | 18 items; last changed 2026-10-04; commits: 13 Claude-assisted, 9 local without trailer, 1 app write-back |
| [Mamluk Playing Cards](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/mamluk-deck/grammar.json) | not yet read in practice | | 18 items; last changed 2026-10-04; commits: 13 Claude-assisted, 3 local without trailer, 1 app write-back |
| [Ganjifa](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/ganjifa/grammar.json) | not yet read in practice | | 1 items; last changed 2026-06-24; commits: 7 Claude-assisted, 1 local without trailer |
| [Sola Busca Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/sola-busca-tarot/grammar.json) | not yet read in practice | | 108 items; last changed 2026-10-04; commits: 15 Claude-assisted, 8 local without trailer, 1 app write-back |
| [Jean Noblet Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/noblet-tarot/grammar.json) | not yet read in practice | | 1 items; last changed 2026-10-04; commits: 13 Claude-assisted, 4 local without trailer |
| [The Cary Sheet](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/cary-sheet/grammar.json) | not yet read in practice | | 1 items; last changed 2026-06-24; commits: 8 Claude-assisted, 4 local without trailer |
| [The Rosenwald Sheet](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/rosenwald-sheet/grammar.json) | not yet read in practice | | 1 items; last changed 2026-06-24; commits: 6 Claude-assisted, 2 local without trailer |
| [The Ontoject](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/ontoject-illustrated/grammar.json) | not yet read in practice | | 24 items; last changed 2026-06-24; commits: 5 Claude-assisted |
| [The 36 Tattvas: A Grammar of Consciousness](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/thirty-six-tattvas/grammar.json) | not yet read in practice | | 56 items; last changed 2026-08-10; commits: 7 Claude-assisted, 1 app write-back |
| [Tarocchino Arlecchino](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/tarocchino-arlecchino/grammar.json) | not yet read in practice | | 64 items; last changed 2026-08-08; commits: 8 Claude-assisted, 1 local without trailer |
| [Clown Town Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/clown-town-tarot/grammar.json) | not yet read in practice | | 78 items; last changed 2026-08-08; commits: 6 Claude-assisted |
| [Anecdotes Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/anecdotes-tarot/grammar.json) | not yet read in practice | | 78 items; last changed 2026-10-04; commits: 6 Claude-assisted, 1 app write-back |
| [Petit Lenormand](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/petit-lenormand/grammar.json) | not yet read in practice | | 36 items; last changed 2026-08-10; commits: 5 Claude-assisted, 1 app write-back |
| [Arlecchino's Augmented Arcana](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/arlecchinos-augmented-arcana/grammar.json) | not yet read in practice | | 84 items; last changed 2026-08-08; commits: 6 Claude-assisted |
| [Christmas: The Rebirth](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/christmas-the-rebirth/grammar.json) | not yet read in practice | | 12 items; last changed 2026-07-09; commits: 1 Claude-assisted |
| [Papus](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/papus-tarot-des-bohemiens/grammar.json) | not yet read in practice | | 22 items; last changed 2026-10-04; commits: 1 Claude-assisted, 3 local without trailer, 1 app write-back |
| [Rider-Waite-Smith](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/rider-waite-smith-pictorial-key/grammar.json) | not yet read in practice | | 78 items; last changed 2026-08-10; commits: 2 local without trailer, 1 app write-back |
| [Bus Passengers](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/bus-passengers/grammar.json) | not yet read in practice | | 39 items; last changed 2026-10-03; commits: 8 Claude-assisted, 2 app write-backs |

## Reference grammars and spreads

| Grammar | Status | Date | Notes |
|---|---|---|---|
| [The Tree of Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/tree-of-tarot/grammar.json) | not yet read in practice | | 38 items. |
| [People & Institutions of Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/people-of-tarot/grammar.json) | not yet read in practice | | 37 items. Generated: edit its sources, not this file. |
| [Books Behind the Tarot](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/books-of-tarot/grammar.json) | not yet read in practice | | 30 items. |
| [The Tarot — All Decks, Many Lenses (meta)](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/all-decks-many-lenses/grammar.json) | not yet read in practice | | 1596 items. Generated: edit its sources, not this file. |
| [Tolkien's Three](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/tolkien-three/grammar.json) | not yet read in practice | | 3 items. |
