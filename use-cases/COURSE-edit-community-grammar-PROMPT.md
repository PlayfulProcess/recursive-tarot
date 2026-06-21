# New-chat prompt — build the "Edit a Community Grammar" course

Paste the block below into a fresh chat (with the recursive.eco MCP connected, in
the GitHub parent folder so both `recursive-tarot/` and `recursive-eco/` are
reachable). It's self-contained — it carries the facts already verified so the
new session doesn't re-derive them.

---

```
You are a contributor to the open `recursive-tarot` project (static GitHub-Pages
site) working alongside `recursive-eco` (the private app + the recursive.eco MCP).
Both are checked out under the GitHub parent folder. Read recursive-tarot/CLAUDE.md,
recursive-tarot/course/build-a-tarot-deck-with-claude.mdx (the "Contribute to the
Commons" ladder), and use-cases/USER-JOURNEYS.md first.

GOAL: extend the contributor course with a focused lesson — "Edit a Community
Grammar" — that teaches the SAME task (improve a deck that someone else owns and
has opened to the community) through THREE doors, so a reader picks the rung that
fits them. Write it as a reproducible walkthrough with real prompts/clicks/screens,
author byline "PlayfulProcess".

The three doors:
  1. In the recursive.eco APP — sign in → open the community deck → it's
     open_to_community, so self-add as an Editor → make an edit → it becomes a
     PENDING proposal the owner reviews + merges. (No code, no Git.)
  2. claude.ai + code + the recursive.eco MCP — drive the same flow by tool calls:
     get_grammar to read it; for a deck you DON'T own, today the MCP only edits
     grammars your token owns, so the working path is "fork the grammar (not the
     repo) into your own library and improve it" (get_grammar → create_grammar +
     add_items → update_items / set_item_images). Show this honestly as the
     today-path, and note that true in-place community editing via MCP is the
     "Model B" build (below) that's coming.
  3. Claude Desktop + the GitHub tarot repo — clone recursive-tarot, edit the
     deck's tarot/<slug>/grammar.json locally, run `python scripts/check_all.py`
     (must end "all checks passed", dangling=0), commit on a branch, open a PR to
     `dev`. On merge, dev→main carries it to the canonical branch.

VERIFIED FACTS to build on (do not re-litigate):
- PERMISSION MODEL: set_grammar_visibility and every visibility/content write in
  the gpt MCP routes is owner-scoped (.eq('user_id', userId)); a non-owner token
  cannot publish or edit another user's grammar in place — even for community
  grammars. open_to_community grants only the Editor role = PROPOSE edits the owner
  reviews/merges. The propose→merge lane already exists: editor saves land as
  pending files ({owner}/{doc}/pending/{editor}.json in the backup vault); owner /
  granted-reviewer runs merge-pending. Self-assigned roles never merge.
- "MODEL B" (in-place community edit via MCP) is a small, scoped build in
  recursive-eco, not yet shipped: (1) a join_grammar_as_editor MCP tool mirroring
  the in-app self-add; (2) make the gpt content routes, when the caller is a
  non-owner editor of a community-open grammar, write to the existing PENDING lane
  instead of the live row (never the live row, never visibility). Design rule:
  contributors ALWAYS go to pending review; only owner / owner-granted reviewers
  write directly. It's the flow app → build locally (cd apps/flow && rm -rf .next
  && npx next build, check the real exit code), don't push to verify; new MCP tools
  aren't callable until deployed AND a fresh chat (tool list is cached per session).
- TWO WINGS: decks carry provenance = record | living | reference; boolean draft =
  early/incomplete only. Community editing applies to any band.
- BRANCH MODEL: canonical = `main` (the recursive.eco GitHub-App webhook syncs the
  default branch = main). Work on `dev`; dev→main merge is the publish event. The
  webhook is installed and fires, BUT only 2/32 grammars carry the _recursive_eco_url
  backlink it needs, and content propagation (e.g. the provenance field) isn't yet
  confirmed end-to-end — so for now push repo state live via the MCP, not by trusting
  auto-sync.

DELIVERABLES:
  A. The course lesson (append to course/build-a-tarot-deck-with-claude.mdx, or a
     new sibling MDX if cleaner), covering the three doors with real screens.
  B. Screenshots under pages/courses/images/ referenced as images/<name>.png
     (course-viewer rewrites the path). Use the Chrome MCP for app/claude.ai
     screens; for MCP/CLI steps, faithful session figures are acceptable IF
     labeled honestly (not GUI captures).
  C. Keep the site static + dependency-free; check_all green, dangling=0; work on a
     branch off dev; PR to dev (no force-push, no merge to main without asking).

OPTIONAL (only if the human confirms — spends nothing but touches prod): publish a
small demo community grammar via the MCP to use as the live example the lesson
links to.

Start by proposing the lesson outline (the three doors + which real grammar to use
as the running example) and confirm before writing.
```

---

*Why three doors, one task:* it mirrors the existing ladder's ethos — same
reviewable outcome, climb only as high as you like — and it's the natural sequel
to the "build a deck" Rung-5 lesson. Door 2's honest "fork the grammar, not the
repo" today-path becomes "edit in place" once Model B ships, so the lesson has a
clean upgrade seam.
