# Backlog — ideas & unfinished threads (recursive-tarot)

A running capture of everything discussed but not yet finished, so nothing is lost between
sessions. Companion to `LAUNCH-CHECKLIST.md` (launch gates) and `FUTURE_PLAN.md` (older roadmap).
Newest context first. Status: ☐ todo · ◐ partial · ✅ done.

---

## A. recursive.eco integration (the big one — for the new MCP chat)

- ◐ **Per-deck Cast/View/Edit links.** `tarot/_eco_ids.json` holds the slug→deckId map (all 28
  decks). `viewers/eco-links.js` renders 🔮 Cast (`flow.recursive.eco/?deckId=<id>`) · 👁 View
  (`recursive.eco/pages/grammar-viewer.html?type=&id=`) · ✏️ Edit (fork-to-edit). **Wired into
  `cards.html` card modal only** — still TODO: deck headers, `tree-viewer.html`, `timeline.html`
  detail panels (same `RecursiveEcoLinks.barHTML(slug,…)` call).
- ☐ **Publish + community-open all 28 decks.** Only `visconti-sforza-tarot` + `all-decks-many-lenses`
  are `is_public` today; the rest are private drafts, so their links don't resolve for visitors.
  Backed-up publish SQL was generated (publish + `open_to_community`). **The new MCP chat should do
  this via the MCP, not raw SQL** — see section C (the MCP currently has NO publish tool).
- ☐ **Copy-to-my-grammars / Play / Build buttons in `cards.html`** were the original ask — now
  unblocked by `_eco_ids.json`. Wire them to use the deckId map.
- ☐ **View link `type=` param** — eco-links sends `type=<grammar_type>` (Visconti reads as `custom`,
  not `tarot`). Confirm whether recursive.eco's grammar-viewer needs `type=tarot` and force it.
- ☐ **Course deck table deep links** — `course/build-a-tarot-deck-with-claude.mdx` table uses GitHub
  edit links; add `?deckId=` "open in recursive.eco" once decks are public.

## B. Games

- ☐ **Ma Diao illustrated money deck (≈1 session).** `madiao.html` already builds a complete 40-card
  money deck *from type* (Cash 文 / Strings 索 / Myriads 萬 / Tens-of-Myriads 十萬). Build **40 SVG
  card faces from 4 suit templates** (coins-with-square-hole, strung coins, 萬 / Water-Margin motif,
  十萬) — PD by construction — and wire into the existing `buildDeck()`. Turns it from typeset into a
  real illustrated deck, zero copyright risk.
- ☐ **Real-people multiplayer (spec then build).** Today all 3 games are client-side vs local AI.
  Needs a backend: realtime sync (Supabase Realtime / WebSockets), **server-authoritative** game
  state (deal + validate moves server-side so no cheating), lobby/matchmaking + invite links, auth
  (the existing recursive.eco login). Reuse the existing rules engines. Write the scoped spec.
- ☐ **madiao.html play log → emergent table** (tarocchino got the table; madiao still uses the old
  card-list `#log`).
- ✅ Tarocchino: emergent play-log table, readable trump order, bigger cards, trump names (not numerals).
- Note (rules, confirmed correct): the **leader of a trick may lead ANY card** (suit or trump). The
  "follow, then trump, then discard" obligation applies only to **followers** when they're **void**
  in the led suit. So you're never required to *have* a trump to lead — leading is unrestricted.

## C. recursive.eco MCP — capability gaps (audit 2026-06-20)

MCP server: `recursive-eco/apps/flow/src/lib/ai-pkg/mcp-tools.ts` (22 tools). Existing plan doc:
`recursive-eco/docs/future_plan/MCP-CAPABILITY-AND-MONETIZATION.md`.

Present: list/get/create/delete_grammar · add/update/delete_item(s) · generate/set images · cast ·
import_grammars (→ **private draft**) · storage/list/delete_file · set_item_performance ·
set_grammar_media · upload_audio · narrate_grammar · align_audio.

**Missing — needed so the new chat can "do anything grammars-related via MCP":**
- ☐ **publish / set-visibility tool** — flip `is_public` and `open_to_community` (the whole reason
  the per-deck links don't resolve). `import_grammars` deliberately leaves drafts private.
- ☐ **grammar-metadata update** — set name / description / cover_image_url / tags at the grammar
  level (only item-level edits exist).
- ☐ **tools-table / channel operations** — offer a grammar to a curated channel, set submission
  state (the `tools` table is untouched by the MCP).
- ☐ **repo awareness** — the MCP edits the **DB library only**, not the repo `grammar.json` files.
  "Grammars in code" = git/GitHub, a separate surface. Decide if MCP should round-trip to GitHub.
- Action for the new chat: read `mcp-tools.ts`, add the publish + metadata + tools-table tools,
  update `api/mcp/docs/route.ts`, and correct code where needed.

## D. History & content

- ✅ **Marziano da Tortona** (lost first deck, text survives) → `research/decks/marziano-da-tortona.md`,
  incl. the **Cola di Rienzo / Petrarch *Trionfi*** procession lineage and the **Marcello 1449
  "royal robbery"** transmission beat. Cross-reference into the history course next.
- ☐ **Marziano reconstruction DECK** — only if usable **public-domain** art is found (the original is
  lost; any deck is interpretive). Research-session candidate.
- ☐ **More pre-tarot decks** — Chinese money cards (Water Margin 水滸牌), Persian As-Nas — PD-image
  check first. (Prompt drafted earlier.)
- ◐ **Watchlist commentary** — agree/differ notes written for 3 clips (Cannucciari, Mamluk→Visconti,
  ARTE Marseille). Annotate the rest where we have a grounded take.
- ☐ Fold the Marziano/Cola/Marcello beats into `course/history-of-tarot.mdx` "first tarot" section.

## E. Polish / launch (see also LAUNCH-CHECKLIST.md)

- ☐ **Shop** — check print QUALITY (order proofs), then wire `product_url`/`live` or a commerce API.
- ☐ **AI assistant QA** — Library Assistant on `cards.html`, `tree-viewer.html`, `course-viewer.html`;
  Oracle; and the MCP capabilities the course advertises.
- ☐ **HTML cache headers** — only `site-header.js?v=N` is cache-busted; the HTML pages are served
  stale (this caused repeated "looks unchanged" confusion). Add a cache strategy before launch.
- ☐ **Sequence viewer v1 vs v2** — decide the canonical one; maybe rename `sequence-v2.html` →
  `sequence.html` and retire v1.
- ☐ **Generated meta covers** — `all-decks-many-lenses`, `people-of-tarot`, `tree-of-tarot` have no
  cover (they're generated; needs a generator tweak).
- ☐ **play.html Contribute** — the "contributor's course" 📓 tile still uses a glyph thumb.
- Env note: backgrounded `python -m http.server` keeps getting reaped on this machine — restart as
  needed; verify via the preview tool, not `localhost` curl alone.

---

## Handoff prompt — start a fresh chat with the recursive.eco MCP connected

> Paste into a new session that has the recursive.eco MCP **and** the Supabase MCP connected.

```
Work across two repos checked out under the GitHub parent folder:
  • recursive-tarot/  — the static GitHub-Pages site (branch dev). Read its BACKLOG.md first.
  • recursive-eco/    — the app; the MCP server lives at apps/flow/src/lib/ai-pkg/mcp-tools.ts.

Use the recursive.eco MCP (not raw SQL) for everything grammars-related. Goals, in order:

1) PUBLISH the 28 repo decks: for each deckId in recursive-tarot/tarot/_eco_ids.json, set
   is_public=true and open_to_community=true so the per-deck links resolve for visitors.
   - If the MCP has no publish/visibility tool yet (it doesn't, as of 2026-06-20), ADD one to
     mcp-tools.ts (e.g. publish_grammar / set_grammar_visibility), update api/mcp/docs/route.ts,
     build locally (cd apps/flow && rm -rf .next && npx next build), and use it. Back up the
     affected rows first (single Supabase project = prod; see recursive-eco/CLAUDE.md migration rules).
2) AUDIT the MCP for full grammar coverage and CORRECT the code where needed: grammar-metadata
   update (name/description/cover/tags), tools-table/channel operations, and decide repo round-trip.
   See BACKLOG.md section C.
3) Then build, in recursive-tarot, the items in BACKLOG.md the user has greenlit — likely:
   the illustrated Ma Diao money deck (40 SVG faces), extend the Cast/View/Edit bar to the
   tree/timeline viewers + deck headers, and the multiplayer spec.

Constraints: recursive-tarot stays static/dependency-free. Don't push recursive-eco apps/flow just
to verify (paid Vercel builds — build locally). Confirm each deck's UUID via the MCP before publishing.
```
