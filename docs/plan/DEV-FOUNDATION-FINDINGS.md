# dev.flow.recursive.eco foundation test — findings (Jun 23 2026)

Read-only reconnaissance via Claude-in-Chrome on `dev.flow.recursive.eco/account`. **No recursive-eco
code changed; no write actions performed.** Logged at the builder's request.

## ✅ Foundation looks healthy (confirmed from /account, read-only)

- **Signed in** as `@PlayfulProcess` on dev.flow (no redirect to sign-in → auth cookie carries on the
  `.recursive.eco` subdomain, as expected).
- **Account state:** 443 grammars · $51.38 credits · 34 starred / 110 submitted.
- **My Channels:** **Personal Channel** + **The Recursive Tarot** (`Channel · /recursive-tarot`) with a
  **Settings** button present → *Door 2's home (the A.2 channel-settings dashboard) exists.*
- **GitHub:** *Connected as @PlayfulProcess.* Connected repos include **playfulprocess/recursive-tarot**
  and **playfulprocess/recursive.eco-schemas** → the App write-path prerequisite (repo connected + App
  installed) is in place.
- **Import a repo as a channel →** present (Door 1's entry exists).
- MCP token set; weekly digest; theme migration note ("about a third of surfaces themed; dark default");
  Data & Privacy controls all render.

## ⚠️ Could not reach the sync/Drift list (two blockers)

1. The browser tab reports a **0×0 viewport** (Chrome window minimized / tab backgrounded), so the
   accessibility tree is empty and **clicks aren't possible**. DOM *text* extraction works; *interaction*
   does not.
2. The channel **Settings** opens via an **in-page button**, not a route — `/recursive-tarot?settings=1`
   returns **404**. So I can't open it by URL either.

→ I did not see the Drift badges or the sync rows; checklist item #4's UX surfaces weren't inspected.

## 🛑 Safety flag — why I did NOT run the write tests

- **#1 "Supabase official" on a Drift row is destructive to repo work.** It resolves drift by making
  **Supabase the source of truth and committing it to the recursive-tarot repo.** If Supabase's copy of
  that deck is older than the grammar edits we made *this session* (community disclaimers, meta rebuilds,
  `_image_usage`, etc.), **it would overwrite our work in the repo.** That contradicts "without destroying
  the work we did," so I stopped.
- **#2 (toggle Published + Save)** and **#3 (Import)** are also writes (public visibility / account state /
  content) — not run.

## ▶️ To proceed safely (need a decision)

1. **Un-minimize / foreground the dev.flow Chrome tab** so I can do the read-only Settings recon and
   actually report the Drift list (which decks drifted, and which direction).
2. For the write proof, pick one:
   - **(a)** I report the Drift list; **you** tap "Supabase official" on a row you know is safe.
   - **(b)** Designate a deck **we did NOT edit this session** and I'll tap it on that row only.
   - **(c)** Confirm whether a Supabase→repo overwrite on a chosen deck is acceptable (everything we did is
     already committed + pushed to `dev`, so a clobber is *recoverable* via git, but still a clobber).
   - Also worth checking in the panel: is there a **"Repo/GitHub official"** option (the *opposite*
     direction, repo→Supabase)? That direction is safe for the repo and may prove the App-commit path
     just as well.

## UPDATE — opened the Channel settings (read-only) and found the drift

With the window foregrounded I opened **The Recursive Tarot → Settings** (viewing only, nothing saved).
- **Channel: Published ✅**, description present → Door 2's home renders fine.
- **Sync status: 27 grammars · 26 in sync · 1 drifted.** The 26 historical decks are all green **In sync**
  (so the sync machinery generally works — good sign).
- **The 1 drift = "The 36 Tattvas: A Grammar of Consciousness"** (`thirty-six-tattvas`) — **one of the two
  community grammars I added the disclaimer to THIS session.** Row offers **"GitHub official"** (repo→Supabase)
  and **"Supabase official"** (Supabase→repo).

### Do NOT tap either button on the 36 Tattvas row
- **"Supabase official"** → Supabase (last edited Jun 17, pre-disclaimer) overwrites the repo → **wipes my
  Jun 23 disclaimer edit.** This is the exact risk I flagged, now concrete.
- **"GitHub official"** → repo → Supabase. Safe for the repo, BUT the repo's `thirty-six-tattvas/grammar.json`
  likely lacks the platform-side **`ai_personality_prompt` / Wallis RAG config** (per recursive-eco CLAUDE.md
  that grammar carries sensitive RAG), so pushing repo→Supabase could **wipe the RAG on the platform.**
- → **The 36 Tattvas is the worst possible deck to test on.** Use a disposable TEST grammar (builder's instinct).
