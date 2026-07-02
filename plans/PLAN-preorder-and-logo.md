# PLAN — deck pre-orders + the forest-of-hearts logo (logged Jul 2 2026)

Builder's ask, verbatim spirit: in the shop, people should be able to **pre-order a deck
that isn't purchasable yet** — signed in = 1 click; not signed in = leave an email to be
notified when available. Plus: the new forest-of-hearts logo should actually APPEAR on the
site, and the hero's breathing spiral and the animated logo should feel like one family.

## A. Pre-order / notify-me (replaces the dead "Coming soon (proofing)" button)

Current state: `pages/shop.html` renders products from `print-products.json`; decks without
`product_url` get a disabled "Coming soon (proofing)" button. `auth-widget.js` already gives
the page the recursive.eco session (`.recursive.eco` cookie).

Flow:
1. **Signed in** → button says "Pre-order · 1 click". POST to a new recursive-eco endpoint
   `/api/preorder` `{ product_slug, deck_name }` with credentials (same CORS pattern as the
   course assistant: exact-origin `https://tarot.recursive.eco`, `Vary: Origin`). Row lands in
   a new `preorders` table (user_id, product_slug, email inferred from profile, created_at,
   notified_at null). Button flips to "You're on the list ✓".
2. **Not signed in** → inline email field + "Notify me" (no account creation). Same endpoint,
   `{ product_slug, email }`, honeypot + the existing per-IP rate-limit pattern from
   `grammar-report`. Store with user_id null.
3. **When a deck goes live** (product_url added to print-products.json): a desktop session
   sends the notification batch (Resend, like report emails) and stamps `notified_at`.
   NO auto-email pipeline v1 — a human presses the button.

Build notes: table + RLS (insert: anon-with-rate-limit via service role route; select: admin
only), one API route, ~30 lines in shop.html. **1 desktop session, high confidence.**
Do NOT collect payment at pre-order — it's an interest list, not a deposit (no Stripe scope).

## B. Logo placement + motion family

- New mark lives at `public/forest-of-hearts-logo.svg` (live:
  https://tarot.recursive.eco/public/forest-of-hearts-logo.svg) — one trunk breaking into
  three spiral branches, hearts in the eyes, reaching for a gold light, verified non-touching.
- **Placement v1**: add alongside the spiral-mark in the ecotree footer block
  (`index.html:298`) and/or as the shop page's header mark — builder picks.
- **Motion**: the hero uses `public/spiral/hero-spiral.js` (the animated logo); the static
  breathing spiral elsewhere doesn't match it. Task: give the forest-of-hearts mark the same
  treatment — grow the trunk, unfurl the three spirals toward the light (SVG stroke-dashoffset
  draw-on, ~3s, prefers-reduced-motion honored), so the brand breathes the same way everywhere.
  The generator script pattern lives in the git history of this file's commit.
- Related asset now live: `public/heart-forest-animated-hearts.html` (the builder's
  "A heart that fell" animated forest page).
