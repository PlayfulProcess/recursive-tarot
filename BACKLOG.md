# Backlog — ideas & unfinished threads (recursive-tarot)

A running capture of everything discussed but not yet finished, so nothing is lost between
sessions. Companion to `LAUNCH-CHECKLIST.md` (launch gates) and `FUTURE_PLAN.md` (older roadmap).
Newest context first. Status: ☐ todo · ◐ partial · ✅ done.

> **▶ Jun 2026 site-redesign + practitioner-course arc has its own master status doc:**
> [`plan/SITE-REDESIGN-AND-COURSE-2026-06.md`](plan/SITE-REDESIGN-AND-COURSE-2026-06.md) — start
> there for the editorial homepage redesign, the collapsed "Reading the Cards" course, the
> dark-mode sweep, the Fraunces font, the "Tarot & the Crack" philosophy enrichment, the video
> program (7 lenses), and the open queue (icons/de-emoji, broader dark audit, cards.html, screenshots).

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
- ✅ Folded the Marziano/Cola/Marcello beats into `course/history-of-tarot.mdx` ("The First Deck").
- ☐ **Illustrate the contributor course** — use the **Chrome MCP** to screenshot each step of
  `build-a-tarot-deck-with-claude.mdx` (sign-in → Library → fork/edit → Grammar Assistant → GitHub
  web-editor → open PR), save under `pages/courses/images/`, embed in the MDX as `images/<name>.png`
  (course-viewer rewrites the path) for visual, follow-along navigation.

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
3) ILLUSTRATE THE COURSE with real screenshots (use the Chrome MCP). Walk each step in
   course/build-a-tarot-deck-with-claude.mdx in a real browser — sign in to recursive.eco, open
   Library, fork/edit a deck, use the Grammar Assistant, then GitHub's web editor and opening a
   pull request — and SCREENSHOT each step. Save the PNGs under recursive-tarot/pages/courses/images/
   and embed them in the MDX as images/<name>.png (the course-viewer already rewrites that path to
   the live origin), so users can follow the steps visually instead of from text alone.
4) Then build, in recursive-tarot, the items in BACKLOG.md the user has greenlit — likely:
   the illustrated Ma Diao money deck (40 SVG faces), extend the Cast/View/Edit bar to the
   tree/timeline viewers + deck headers, and the multiplayer spec.

Constraints: recursive-tarot stays static/dependency-free. Don't push recursive-eco apps/flow just
to verify (paid Vercel builds — build locally). Confirm each deck's UUID via the MCP before publishing.
```

---

## MCP: make public-domain image retrieval first-class (answers "can I tailor the MCP so PD images are easier?")

**Yes — the reason I "choke" on PD images is that I reach for the broken screenshot tool. The fix is an
API-backed MCP tool, because Wikimedia is fully queryable over HTTP (no browser needed).** Proven this
session: Wikipedia REST `GET /api/rest_v1/page/summary/<Title>` → `.thumbnail.source` returns a Commons
`upload.wikimedia.org` URL; all 8 historical-author portraits + 2 book links resolved 200 via plain curl.

Propose adding to `recursive-eco/apps/flow/src/lib/ai-pkg/mcp-tools.ts`:

- **`commons_image_search`** — input `{ query, limit?, license_filter? }`. Hits the MediaWiki Commons API
  (`https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata|mime`).
  Returns `[{ title, url, thumb_url, width, height, mime, license, license_url, artist, credit }]` parsed
  from `imageinfo.extmetadata` (LicenseShortName / UsageTerms / Artist). Lets me pick a verified PD/CC image
  + its attribution in one call, instead of guessing or screenshotting.
- **`wikipedia_summary`** — input `{ title }` → `{ extract, thumbnail, content_url }` from the REST summary
  endpoint. Gives both the lead portrait *and* the canonical Wikipedia URL (exactly what "redirect people to
  their Wikipedia page" needs).
- Optional **`set_item_image_from_url`** convenience (the existing `set_item_image` likely already takes a URL;
  if so this is just docs) — so the flow is search → set in two MCP calls.

Filter to `license` ∈ {public domain, CC0, CC-BY, CC-BY-SA} and always return the attribution string so the
caller can store `metadata.image_credit`. This makes "populate thumbnails with PD images" a 2-call loop for
any future deck/people/book grammar.

## Still pending from this arc
- **People grammar → portraits + Wikipedia redirects + cross-links to books.** people-of-tarot is GENERATED
  from `research/people/*.md` via `scripts/build_people_grammar.py`. To do this right: add `image:` and
  `wikipedia:` front-matter fields to each dossier, teach the generator to emit `image_url` +
  (for the redirect) a `metadata.url`, then rebuild. Same Wikimedia REST method as the books. ~31 people.
- **Cross-link decks/people → their books** via the one pill pattern
  (`metadata.source_deck:"books-of-tarot"`, `source_item_id:"book-…"`, `deck:"Books Behind the Tarot"`).
- **Ambiguous titles to confirm with the user before adding to books-of-tarot:** "Michael Thomas" (which
  book?), "12 tarot games" (likely Dummett & McLeod's games book — now added), "The Neuroscience of Tarot"
  (looked low-credibility — left out), and the practice manuals named in the source video (Greer *Paths of
  Wisdom*, Gareth Knight, Ashcroft-Nowicki *The Shining Paths*) — these are modern *practice* books, a
  separate "further practice" category from "sources behind the tarot."
