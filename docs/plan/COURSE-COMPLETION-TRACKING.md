# Course completion tracking — FUTURE PLAN (parked Jun 29 2026)

Per-reader progress through a course when logged in: which sections they've read,
whether the whole course is complete, and a "last visited" timestamp. Parked for
later; this is the design so it can be picked up cold.

## Difficulty: moderate. Most of it is easy; one piece is the real work.

| Layer | Difficulty | How |
|---|---|---|
| Know who's logged in | Easy | `auth-widget.js` already reads the recursive.eco session |
| Detect "read this section" | Easy | `IntersectionObserver` on each section heading → mark seen on view, or after an N-second dwell |
| Show the UI | Easy | ✓ checkmarks in the TOC, a progress bar, "last visited <ts>", a "Course complete" badge |
| **Persist per-user** | The real work | One small Supabase table + RLS, written from the static site as the logged-in user |

## The one hard part: authenticated write from the static site
The static tarot site must write to Supabase **as the logged-in user** (their auth
token from the recursive.eco session). This is the SAME auth bridge needed for the
"edit the course through the assistant" work — build it once, both features unlock.
**As of Jun 29 2026 the builder believes this auth bridge already exists** — verify
before estimating.

## Proposed shape (minimal DB — matches house style)
```
table course_progress
  user_id      uuid     -- recursive.eco user
  course_id    text     -- course grammar slug or UUID (history-of-tarot-course)
  section_id   text     -- the item/section id within the course
  seen_at      timestamptz
  primary key (user_id, course_id, section_id)
  RLS: a user can only read/write their own rows
```
- Write: on section-seen (debounced) → upsert `(user_id, course_id, section_id, now())`.
- "Whole course complete" = count(distinct section_id) for this user/course ==
  number of sections in the course (read from the grammar).
- "Last visited" = max(seen_at) for the course.
- Display: hydrate the TOC on load with one read of the user's rows for this course.

## Effort once the auth bridge exists
~half a day: the observer + the table + RLS + TOC checkmarks/timestamps. The
observer and UI are trivial; the table is one migration; RLS is one policy.

## Dependencies / links
- Shares the auth bridge with the course-assistant work (build the bridge once).
- Course is rendered by `viewers/grammar-course.html` from the course grammar
  (`tarot/<course>/grammar.json`, generated from `course/*.mdx` by
  `scripts/course_to_grammar.py` — MDX is source of truth, code-first).
