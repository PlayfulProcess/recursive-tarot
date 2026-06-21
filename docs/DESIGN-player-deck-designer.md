# Design — Player: "Design Your Own Deck" (save via recursive.eco login)

**Status:** proposal (planning, 2026-06-21). The flagship interactive destination of the
**Player** door in [`DESIGN-information-architecture.md`](DESIGN-information-architecture.md).
**Author:** PlayfulProcess

## The frame: this is *play*, not the contributor ladder

A Player designs a deck as a creative toy — *remix and personalize*, not "build 78 cards from
scratch" (that's the Contributor's Rung-5 MCP path). The deliverable is delight + ownership, with
a real save behind it. It produces a **Living-tradition** grammar (new making), **`draft`**, and
**private** until the maker chooses to publish.

## Auth + persistence reality (already most of the way there)

Grounded in the actual repo, not assumptions:

- The site is **`tarot.recursive.eco`** (see `CNAME`). The recursive.eco Supabase auth cookie is
  scoped to **`.recursive.eco`**, so it **carries here automatically**.
- **`auth-widget.js` already reads that shared session** and exposes
  `window.recursiveAuth = { client, getUser() }` — a live, RLS-gated Supabase browser client with
  the signed-in user. Signed-out → it already renders "Sign in ↗" deep-linking to recursive.eco
  (sign-in/out lives on the tree, never re-implemented here).
- So **identity is solved**: the static site already knows who's logged in and can call Supabase
  *as that user*, gated by RLS.

The one thing **not** to do: **don't hand-roll a write into `user_documents` from the static
site.** recursive.eco's save path has hard-won invariants (`buildDocumentData` spread-not-handpick,
RAG/personality canary fields, the `document_data` shape). A raw static insert would bypass all of
that and risk malformed/feature-breaking grammars. **Persistence must go through recursive.eco's
canonical save path.** (recursive-eco `CLAUDE.md`: "fix the grammar, not the app"; one canonical
save; canary-log critical fields.)

## The two viable models

### v1 — Handoff (recommended, least new code)
The static "Design your own deck" toy assembles a **deck seed** in the browser (name, theme, a
handful of chosen public-domain card images from the library, a card back), then **hands off to
recursive.eco's create/fork flow** to persist:
- *Remix path:* fork an existing PD deck — `flow.recursive.eco/create/dashboard/unified/new?forkId=<id>`
  (the fork flow already exists; `_eco_ids.json` has the source UUIDs).
- *From-seed path:* a small create entry that accepts the seed (URL params or a posted draft) and
  writes via the canonical path.
Because the user is already signed in (shared cookie), the hop is seamless. The new deck lands in
their recursive.eco **library**, private, `provenance:living`, `draft`.

### v2 — On-site toy + one create API (optional, later)
Keep the playful designer entirely on the static site (drag/arrange/name), and add **one**
recursive.eco API route that accepts a validated seed and runs the canonical save server-side
(so the static site still never constructs `document_data` itself). More polish, one small
recursive.eco build.

**Recommendation:** ship **v1 (remix/fork handoff)** first — it reuses everything and respects the
save doctrine. Add v2's on-site designer only if the handoff feels too heavy for "play."

## The flow

1. Player opens **Play → Design your own deck** (`play.html`).
2. `window.recursiveAuth.getUser()`:
   - **signed out →** the existing "Sign in ↗" prompt (opens recursive.eco auth in a new tab,
     returns here). Play still works; saving needs the login.
   - **signed in →** greet by name; proceed.
3. Player **remixes**: pick a PD starter deck, rename, choose/swap a few card images (from the
   library's PD set), pick a back/theme.
4. **Save to my account →** handoff to the recursive.eco create/fork flow → canonical save →
   private **Living** draft in their library.
5. **Play it:** Cast/Draw the new deck (recursive.eco oracle) — the payoff.
6. *(optional, later)* **Publish** → enters Band B (Living) as a peer; gated, owner-controlled.

## Two-wings + security ties

- A player-made deck is **`provenance:living`, `draft:true`, private** by default — exactly the
  band model, and it means experiments never pollute the Record or the public Library.
- **RLS does the gating:** a signed-in user can only write their *own* rows; publish is a separate,
  owner-only action (the `set_grammar_visibility` scope we already confirmed). No new trust surface.
- `draft` here means "my deck isn't finished" — never a cultural judgment (the 36-Tattvas lesson).

## Acceptance criteria

- [ ] Signed-out Player can design locally but is clearly prompted to sign in to save.
- [ ] Signed-in Player saves a deck and it appears in their recursive.eco library, **private**,
      tagged `provenance:living` + `draft`.
- [ ] Persistence runs through the canonical save path (no static-site `user_documents` write).
- [ ] The new deck is immediately Castable/drawable.
- [ ] Nothing the Player does can publish or community-open a deck without an explicit owner action.

## Open questions

1. Does a recursive.eco **create route accept a seed payload** today, or only `forkId`? If only
   fork, v1 = "fork a PD deck + edit," which is arguably the better *play* anyway.
2. Remix granularity for "play": rename + swap images + back only (light), or full per-card edit
   (heavier, drifts toward the Contributor editor)? (Lean: light; full editing is the editor's job.)
3. Should the static toy save the in-progress seed to `localStorage` so a signed-out Player doesn't
   lose work across the sign-in hop? (Lean: yes — small, high-value.)
4. Does `provenance:living` + `draft` get set at create time by the flow, or stamped after? (Ties
   to the repo→DB propagation work in USER-JOURNEYS.)
