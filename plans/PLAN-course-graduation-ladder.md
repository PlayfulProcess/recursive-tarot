# PLAN — Courses that graduate readers into vibe coders (Jul 3 2026)

The builder's ask: improve this repo's courses so people can contribute at every level — and
see **all the ways they can graduate**: from reading a card, to fixing a deck, to building
grammars by talking, to owning a repo + a website "like this one" in THEIR domain expertise.
Surveyed read-only: this repo (courses, viewers, integration docs) + recursive-eco (contribution
machinery, plans). **No recursive-eco changes here or in this plan's build steps** — where a
step depends on app work, it's marked DEPENDS and waits.

## 1. What already exists (verified — don't rebuild)

- **The 5-rung ladder is live** in `course/how-to-contribute.mdx` and it's genuinely good:
  R1 fix-in-app → R2 GitHub web editor → R3 claude.ai drafts → R4 Claude Desktop on the repo →
  R5 the recursive.eco MCP, with a real narrated build-log as proof (Rung 5 in practice).
- **Three contribution objects** (deck / spread / course), each with an easy route and a GitHub
  route; per-deck two-door table (app logo · GitHub pencil) for 26 decks.
- **The integration reference** `docs/RECURSIVE-ECO-INTEGRATION.md` — §9 play/cast URLs, §10
  Journal feature names — is exactly the "API paths for a domain repo" doc; siblings need it.
- **22 course MDX files** exist, but only **5 are registered** in `site-header.js`
  `COURSE_GROUPS` (Start here: history · light-of-tarot · how-to-contribute; More: reading ·
  tarot-today). The rest are reachable only via sources.html or direct URL.
- **The 0→1 graduation course already exists — in the nara repo**: "From Zero to Your First
  Altar" (7 chapters: what-you're-building → fork-the-template → claude account → the two
  manual steps (MCP + GitHub connectors) → first grammar → repo discipline → offer & share),
  with a static viewer at playfulprocess.github.io/nara/course/. It is not linked from ANY
  tarot course — the two halves of the ladder don't know about each other.
- **App-side machinery** (exists, read-only here): community grammars + editor self-add,
  pending-edit → PR merge flow, `course_completions` table, channel offers; trip Sessions 1–2
  are making repos channel-canonical with live GitHub→app sync.

## 2. The gap, in one sentence

The ladder tops out at Rung 5 **inside this commons** — a contributor can master the tarot
repo, but no course tells them the last move: *leave home and found your own*. Everything for
that move exists (nara course, template-shaped repos, channels, Pages) — it's unlinked and
un-narrated.

## 3. The full graduation ladder (target shape)

| Rung | Identity | What they do | Where it's taught |
|------|----------|--------------|-------------------|
| 0 | Reader / Player | read decks, cast spreads, journal | four doors (Player/Historian/Practitioner) |
| 1 | Fixer | one-click in-app edit proposal | how-to-contribute R1 |
| 2 | Editor | GitHub web-editor PRs | R2 |
| 3 | Drafter | claude.ai-assisted edits | R3 |
| 4 | Repo worker | Claude Desktop across files | R4 |
| 5 | Toolsmith | MCP: create/illustrate/publish grammars | R5 |
| **6** | **Founder** | **own repo + own grammars in their domain** | **nara 0→1 course (link it!)** |
| **7** | **Site owner** | **own GitHub Pages site "like this one"** | **NEW: fork-the-site course (W3)** |
| **8** | **Community keeper** | **own channel; later: membership/pass** | **DEPENDS: trip Session 1–2 + memberships plan** |

## 4. Workstreams

### W1 — Stitch the ladder together (1 session incl. writing; HIGH confidence; no gates)
- Add **"Rung 6 — Found your own commons"** to `how-to-contribute.mdx`: a short section that
  says the quiet part ("the point of this repo is to be left — take the method to YOUR
  domain") and hands off to the nara course (live link + what the 7 chapters cover). Add
  Rung 7/8 as two paragraphs with "coming" markers pointing at W3 and the app's channels.
- Add the reverse link: a final chapter/note in nara's course pointing BACK here ("apprentice
  in an existing commons first — the tarot repo takes contributions at 5 rungs").
- Register `how-to-contribute` follow-ups in `COURSE_GROUPS` under a new group **"Contribute &
  graduate"** so the ladder is one menu item, not folklore.

### W2 — Course discovery & curriculum (1 session; HIGH confidence)
- 22 courses / 5 registered: decide each unregistered course's fate — register under a group
  (Start here / Lenses ("X reads the tarot") / Practice / Contribute & graduate), fold into
  another course, or archive. Consolidate-don't-multiply rules the call.
- Give the four doors (Player · Historian · Practitioner · Contributor) an explicit course
  order per door — "read these 3, in this order" — on course.html/sources.html, so a door is
  a curriculum, not a link pile.
- Duration + prerequisites in every course's front-matter (most have duration already).

### W3 — "A website like this one": the fork-the-site path (2 sessions; MEDIUM confidence —
the extraction is judgment work; gate: none, all repo-local)
The nara course teaches fork-the-CONTENT-template; nobody yet teaches fork-the-SITE. This repo
IS the best template (viewers, theme.css single-source, site-header, check scripts, courses)
but it ships with 26 decks of tarot content tangled in.
- **Session A:** extract a **starter kit** — either a `template/` folder here or (better) a
  sibling `recursive-domain-starter` repo marked "Use this template" on GitHub: theme.css,
  site-header.js (menu emptied), course-viewer + one sample course, cards/caster viewers
  pointed at ONE sample grammar, `check_all.py`, `CLAUDE-AI-INSTRUCTIONS.md` skeleton,
  `_eco_ids.json` stub, README that narrates the first hour. Grammar format docs come along
  (`GRAMMAR_FORMAT.md`, the cross-link pill pattern, the sections table).
- **Session B:** the course `course/build-a-site-like-this-one.mdx` (Rung 7): fork the starter
  → rename → GitHub Pages on → swap the sample grammar for yours → wire your repo to your
  recursive.eco channel using `docs/RECURSIVE-ECO-INTEGRATION.md` §9–10 (copy that doc into
  the starter). Phone-viable up to Pages-on; Claude Desktop for the rest — say so honestly.

### W4 — Course experience upgrades (1 session; MEDIUM confidence; DEPENDS partially on app)
- **Completions:** the app has `course_completions` — add a "mark complete" affordance from
  course-viewer via the existing play-URL pattern (DEPENDS: needs an app endpoint check —
  park until the builder is back in recursive-eco).
- **Course-as-grammar** (integration doc §6): courses are `_generated:true` grammars, so they
  get the app's starring/offer flow for free — verify the registration covers all registered
  courses, so "star a course" works. (Mostly repo-side; small.)
- **Screenshot convention** stays `pages/courses/images/` (already canonical) — add the trip's
  incoming nara screenshots the same way when they arrive.

### W5 — Recognition (½ session; HIGH confidence)
- A `CONTRIBUTORS.md` + a short section on the Contribute door: every merged PR name-listed
  (CC-BY-SA attribution made visible, not just legally present). The ethos section already
  promises "your name rides along" — make it a page someone can point at.

## 5. What NOT to do (guardrails from CLAUDE.md)
- No parallel structures: Rung 6–8 EXTEND how-to-contribute; the lens courses stay courses;
  the four doors stay the only journey frame.
- No new cross-link mechanism — the pill pattern is the only cross-grammar nav.
- Nothing in this plan edits recursive-eco. DEPENDS items (completions endpoint, channel/pass
  rungs) wait for the trip sessions + the memberships plan (`PLAN-profiles-communities-
  contribute-miniapps.md` §4½ in the app repo).
- Keep the honesty floor in every new course: PD images only, game-vs-divination line,
  gate-not-fate, name-a-school-not-a-living-person.

## 6. Order & effort (builder's units: sessions, confidence, gates)
1. **W1** — 1 session, HIGH, no gates. Biggest payoff per hour: the ladder becomes whole.
2. **W2** — 1 session, HIGH, no gates (pure curation).
3. **W3** — 2 sessions, MEDIUM (extraction judgment), no external gates. This is the "great
   website within their domain expertise" deliverable.
4. **W5** — ½ session, HIGH.
5. **W4** — 1 session, MEDIUM, gated on app availability (post-trip).

Total ≈ 5½ sessions; W1+W2 are phone-reviewable immediately after a desktop session ships them.
