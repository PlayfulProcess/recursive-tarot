# Fruits of the Tree — integrating the public-domain sites with recursive.eco

*The metaphor, made architecture: **recursive.eco is the tree** (identity, AI,
credits, community, user-created grammars in Supabase). **Public-domain
collections are its fruits** — free, static, forkable sites (this tarot site
first; I Ching, astrology, kids-stories could follow the same template). A fruit
must stand alone (no login, no backend, CC-BY-SA, "just files in a repo") AND
plug into the tree when a user wants identity, AI, or commerce.*

Written June 12 2026 (Fable), grounded in the actual recursive-eco code (read-only
recon of `apps/flow/src/lib/supabase-client.ts` and `apps/flow/src/app/api/ai/*`).

---

## The integration ladder (each rung independently shippable)

| Rung | What | Status |
|---|---|---|
| **L0 — Links & canonical pointers** | Header links both ways; `_github_url` stamps; import-a-grammar-as-user path | ✅ built & tested |
| **L1 — Shared identity** | One sign-in across `recursive.eco` and `tarot.recursive.eco` | ✅ shipped Jun 12 (cookie domain confirmed in Vercel prod; `auth-widget.js` in the site header reads the session) |
| **L2 — Shared AI** | Fruit pages call the tree's AI routes (course tutor, caster readings) | 🟡 CORS on `/api/ai/chat` committed LOCALLY in recursive-eco (builder pushes); fruit-side chat panel + caster wiring next |
| **L3 — Shared data** | GitHub main → Supabase webhook sync; user favourites/spreads saved from fruit pages | 📋 specced in `HANDOFF-rearchitect-genealogy.md` |
| **L4 — Commerce** | TGC print-on-demand Worker; credits wallet shared | 📋 specced in `NEXT-SESSION-DELEGATION.md` O3 |

## L1 — Persistent sign-in between the apps: YES, and most of it exists

**Found in the code:** `apps/flow/src/lib/supabase-client.ts` already creates the
browser client with `@supabase/ssr` (cookie-based session, `storageKey:
'recursive-eco-auth'`) and reads **`NEXT_PUBLIC_AUTH_COOKIE_DOMAIN`** with the
comment *"Production: '.recursive.eco'"* — i.e. the app was already designed to
set its auth cookie for **all subdomains**. Since `tarot.recursive.eco` is a
subdomain, the same session cookie is readable there.

What's left:
1. **Builder check (5 min):** confirm `NEXT_PUBLIC_AUTH_COOKIE_DOMAIN=.recursive.eco`
   is actually set in Vercel **production** env (Settings → Environment Variables).
   If it wasn't set until now, existing users re-login once to mint the
   domain-wide cookie.
2. **Tarot site: a tiny shared `auth-widget.js`** (Sonnet task). Loads
   `createBrowserClient` from `@supabase/ssr` via esm.sh CDN with the SAME
   `storageKey: 'recursive-eco-auth'` and `cookieOptions: { domain:
   '.recursive.eco' }`, plus the project URL + **anon key** (public by design —
   never the service key). Renders in the site header: signed-out → "Sign in ↗"
   (links to recursive.eco login with `?next=` back-redirect); signed-in → avatar
   + name. No login form on the static site — the tree owns sign-in; the fruit
   only *reads* the session.
3. **Caveats:** HTTPS on both (✓); cookie not HttpOnly (required — the static
   site needs JS access; that's how `@supabase/ssr` browser cookies work anyway);
   dev/preview domains don't share (by design, the env var is prod-only).

## L2 — AI in the course preview calling recursive.eco: YES — the route exists

**Found in the code:** `apps/flow/src/app/api/ai/chat/route.ts` is already
tarot-aware (TarotReading types, "use the deck author's actual content, don't
invent reversal meanings" instructions), **authenticates via the Supabase cookie
session** (`supabase.auth.getUser()`), and **meters usage with the credits
wallet** (new-user grant included). There are also `ai/grammar-assistant` and
`ai/library-assistant` routes.

So the course-preview tutor is: *shared cookie (L1) + one fetch + CORS*:
```js
fetch('https://recursive.eco/api/ai/chat', {
  method:'POST', credentials:'include',            // sends the .recursive.eco session
  headers:{'Content-Type':'application/json'},
  body: JSON.stringify({ messages, context: {     // course step + grammar excerpt
    course:'build-a-deck', step, grammar_url } })
})
```
What's missing, in order:
1. **CORS on the AI route(s)** — the only real gap (recursive-eco change, commit
   LOCAL only; builder pushes when ready): answer `OPTIONS` preflight and set
   `Access-Control-Allow-Origin: https://tarot.recursive.eco` (exact origin — `*`
   is forbidden with credentials) + `Access-Control-Allow-Credentials: true` on
   `/api/ai/chat` (or a dedicated thin `/api/ai/fruit-tutor` wrapper that injects
   a course-tutor system prompt and reuses the same wallet — cleaner scope).
2. **Course-viewer chat box** (tarot side, Sonnet): a small panel in
   `pages/course-viewer.html` — visible to signed-in users (from L1), with a
   signed-out state that says "Sign in at recursive.eco to ask the tutor".
   Context payload: the current course step + the loaded grammar's relevant items
   (truncated), so answers cite the deck author's actual content.
3. **Guards already exist:** auth requirement + credits wallet = no anonymous
   token burn; per-user metering for free. Add the fruit origin to any CSRF/
   origin allowlist if one exists.
4. Same pattern then gives the **Caster** real readings ("Get a Reading" calls
   `ai/chat` with the drawn spread) — one more fetch, same auth, same wallet.

## L3/L4 — already specced elsewhere (don't duplicate)
- **Data**: GitHub→Supabase webhook + emergences-from-tags runtime:
  `plan/HANDOFF-rearchitect-genealogy.md`. Once user favourites exist, a fruit
  page can save "my spread" / "my pivot" (the Explorer's URL-hash spec is already
  a serialisable artifact — saving it to Supabase is one POST).
- **Commerce**: Cloudflare Worker holding the TGC secret:
  `plan/NEXT-SESSION-DELEGATION.md` §O3. With L1, orders attach to the user.

## Sequencing & delegation
1. **Builder** (5 min): verify `NEXT_PUBLIC_AUTH_COOKIE_DOMAIN` in Vercel prod.
2. **Opus session in recursive-eco** (local commits only): CORS/preflight on
   `/api/ai/chat` (+ optional `fruit-tutor` wrapper). Builder pushes → Vercel.
3. **Sonnet session in recursive-tarot**: `auth-widget.js` in the shared header
   (signed-in state) + course-viewer chat panel + caster "Get a Reading" wiring.
4. Later rungs ride the existing handoffs (webhook sync, Worker).

**Principles** (from `EMERGENCES.md` + house rules): the fruit never holds
secrets (anon key only); the fruit works fully signed-out (AI/identity are
enhancements, not gates); the tree owns auth, credits and AI keys; PD content
flows tree-ward via GitHub (the repo stays the source of truth).
