# Shop plan — decks + companion books, no self-run checkout

_Drafted 2026-06-20. Companion to `BACKLOG.md` §E (Shop) and `print-products.json`._

## What you asked for

1. Get the decks in the Shop **running now**, "just via API and I test."
2. **Don't collect any money yourself for now.**
3. Be able to print **description books** alongside the decks, **ordered separately**.
4. **Know how many of those sell.**
5. **Would you need to collect taxes if you do this?**

## The key reassurance: you are not building a checkout

The whole Shop is already designed around **print-on-demand (POD)**, default vendor **The Game Crafter (TGC)**.
In that model **the platform is the merchant** — it prints, ships worldwide, takes the customer's
payment, and pays you a margin. You never run Stripe, never touch card data, never "collect money"
in the sense you're worried about. `shop.html` is just a **static catalogue that links out** to each
product's TGC page (`product_url`). recursive-tarot stays static and dependency-free — nothing changes there.

So "I don't want to collect money for now" is **already true by construction**. Two ways to stay
extra-safe while testing:
- **Set your margin to $0** (sell at TGC's base cost) so you earn nothing yet, **or**
- Keep products **unlisted / private** on TGC and only **order your own proofs** — the public Shop
  buttons stay "Coming soon (proofing)" until you flip `product_url` + `status`.

## Current state (so we don't rebuild what exists)

- `pages/shop.html` reads `print-products.json` + `tarot/_collection.json` and renders a card per deck.
  A deck shows **"Buy printed ↗"** only when its `product_url` is set; otherwise **"Coming soon (proofing)."**
- `print-products.json`: **10 decks print-ready** (`status: ready_full_bleed` / `ready_bordered`),
  **all with empty `product_url`** → nothing is live yet.
- Each deck already offers a **free companion booklet** (`📓 Booklet`) — MDX via `course.html`, or the
  `print-viewer.html?layout=booklet` per-card layout. These are the seed of the printed description books.
- There is a **7×10″ print-book pipeline** already (`print/book/book.html`, `@page 7in 10in`) — the basis
  for a physical description book PDF.

## Getting decks running (recommended sequence)

**Pilot first — one deck, end to end (this is your "test"):**
1. Pick the strongest full-bleed deck (e.g. `golden-dawn-book-t-tarot`, all 78 bleed-ready).
2. Create the product on TGC from the print-ready images, **order one proof to yourself** (quality gate, BACKLOG §E).
3. When the proof looks right: set your margin, paste the public URL into `print-products.json`
   → `golden-dawn-book-t-tarot.product_url`, leave/echo `status`. The Shop button goes live automatically.

**Then the "via API" question — two paths:**
- **Manual (fastest to first sale):** create each of the 10 decks in the TGC web UI. ~boring but zero code.
- **API automation:** TGC has a Developer API. A **local Node script** (run with your TGC API key, _not_
  shipped to the static site) could upload the print-ready card images and assemble each deck product,
  then write the returned URLs back into `print-products.json`. Worth it across 10 decks **only after**
  the manual pilot proves the card spec + proof quality — otherwise you automate a mistake 10×.
  _I can build this script once you've done the pilot and have an API key._

## Description books, ordered separately

- Turn the companion booklets into **standalone printed books**, one per deck (or one per tradition —
  e.g. one "Etteilla" book covering I/II/III, one "Games of the Tarot" book) using the existing
  7×10″ pipeline to generate a **print-ready interior PDF**.
- **Vendor choice for books** (decks stay on TGC regardless):
  - **TGC** — keeps one dashboard, but it's card/game-first (booklet/perfect-bound add-ons exist; less ideal for a real book).
  - **Lulu** — great color/global, you stay seller; good for a proper book.
  - **Amazon KDP** — biggest reach, but KDP is its own marketplace (Amazon is merchant of record; same no-checkout benefit).
- Add a **`books` section to `print-products.json`** and a second grid in `shop.html` ("Companion books")
  rendered exactly like the deck grid — small, static change. _I can wire this once you pick a vendor._

## Knowing how many sell

- You **can't read POD sales from the static site** (no backend), but every vendor shows per-product
  **sales counts in its dashboard** (TGC, Lulu, KDP all do).
- If you want the numbers **visible on your own site**, a **local fetch script** can pull sales counts via
  the vendor API on a schedule and write a tiny `sales.json` the static Shop reads to show "X sold."
  Same shape as the API path above — build it after the first products exist.

## Taxes — would you need to collect them?

> Not tax advice — general info. Confirm with an accountant, especially given you're tax-resident in
> **Portugal** with **Brazil** ties; cross-border royalties have specifics a professional should check.

**Short answer: selling through POD platforms, you generally do _not_ collect sales tax / VAT yourself.**

- **Buyer-side tax (sales tax / VAT / GST):** POD platforms act as the **merchant / marketplace
  facilitator** and **collect + remit** the buyer's local tax themselves. TGC handles US sales tax;
  Lulu/KDP handle VAT/GST where required. You don't register for or remit it. (Customers abroad may
  also pay **import duty** at their border — that's on them, and `shop.html` already says so.)
- **Your-side tax (income):** What you earn is **margin/royalty income**, which you **declare on your
  personal income tax in Portugal** (your country of residence). Keep records of payouts.
- **US withholding:** US platforms (TGC, KDP, Lulu) may withhold **30%** on US-source royalties unless
  you file a **W-8BEN** claiming the **US–Portugal tax treaty** rate (often reduced or 0% for royalties).
  **File the W-8BEN on each US platform** — this is the single most important paperwork step.
- **The line that flips everything:** if you ever sell **direct** (your own Stripe/website checkout),
  **then you become responsible for collecting/remitting VAT/sales tax yourself** (EU VAT-OSS, etc.).
  Staying on POD platforms is precisely what keeps that off your plate. This is a strong reason **not**
  to add self-checkout for now — which matches "I don't want to collect money."

## Who does what

- **You:** TGC account + (optional) API key; order proofs; check print quality; set margins; file W-8BEN;
  pick the book vendor; track payout income for your PT return.
- **Me:** the API/automation scripts (deck creation, sales-count pull), the `books` section in
  `print-products.json` + `shop.html`, and the book interior PDFs from the existing pipeline — on your go.

## Suggested first move

Do the **one-deck pilot + proof order**. It de-risks card spec and print quality, gives you a real "test,"
and tells us whether the API automation is worth building. Everything else (books grid, sales counts,
API scripts) is fast once one product exists and the vendor flow is confirmed.
