# How to get a deck printed (step by step)

You couldn't do it before because the card art is **hot-linked** (it lives on
Cloudflare/Wikimedia, not in the repo), so there were no files to upload. The
`scripts/download_deck_images.py` helper fixes that: it pulls a deck's print-ready
cards into a folder you can upload. Here's the whole flow.

## Which decks are ready
Only list a deck where **every card is print-ready**. From the audit:

| Sell as-is (full bleed) | Sell as bordered cards |
|---|---|
| Golden Dawn / RWS · Minchiate · Oswald Wirth · Etteilla II · Mantegna | Marseille · Etteilla I · Etteilla III |

(Visconti, Cary-Yale, Charles VI, Tarocchino, Besançon, Court de Gébelin are
web-resolution — don't print them.)

## Phase 1 — get the card files (≈2 min)
In a terminal, from the repo folder:

```bash
python scripts/download_deck_images.py golden-dawn-book-t-tarot
```

This creates `print/decks/golden-dawn-book-t-tarot/` with one image per card,
named in order (`00 - The Fool.jpg`, `01 - The Magician.jpg`, …). Only print-ready
cards are saved. **Delete this folder after you upload** — the files are large and
this machine is tight on disk. (The folder is gitignored, so it never commits.)

## Phase 2 — create the product at The Game Crafter (≈30–45 min, one time)
The Game Crafter is the right vendor: it prints, ships, and **takes the payment**
— customers check out on *their* site, you never touch money or fulfilment, and
you set your own markup (your margin, which beats any affiliate cut).

1. Make a free account at **thegamecrafter.com**.
2. **Make a Game** → name it (e.g. "Golden Dawn Tarot — Recursive Tarot").
3. Add the **Tarot Deck** component (78 cards, 70×120 mm) — or **Poker Deck** for
   non-78-card decks like Oswald Wirth (22) or Minchiate (97 → use a larger deck
   component / two decks).
4. **Upload the card faces**: use their bulk uploader and select every file in the
   folder from Phase 1. They sort by filename, so the `NN -` prefix keeps order.
5. **Set the card back**: pick one of the historical backs from the print page
   (Print → "Deck back"). Download that back image (right-click → Save) and upload
   it as the deck's single back. Or choose **Plain**.
6. For the **bordered** decks (Marseille, Etteilla I/III), use TGC's bordered/
   safe-area layout so nothing important sits in the cut margin.
7. Set a **price** (TGC shows your base cost; add your markup), add a short
   description, and **publish to the Game Crafter shop**.

## Phase 3 — wire the Buy button (≈1 min)
1. Copy your product's **public shop URL**.
2. Open `print-products.json`, find the deck, paste the URL into `product_url`
   (add any affiliate tag here if you ever have one).
3. Commit + push. The print page's button flips from *"Print-ready — vendor coming
   soon"* to **"Buy a printed deck at The Game Crafter ↗"** automatically.

## What I can't do for you
Creating the account, uploading products, setting prices, and connecting payment
are yours — I won't act on payment/accounts. Everything up to that line (the files,
the quality audit, the buy button) is built and waiting for your product URL.

## Cheaper / different routes (optional)
- **Gelato / Prodigi** if you ever want a **3-card** print or a subscription —
  deck printers won't print 3 cards, but these per-card printers will (needs your
  own checkout + Stripe; bigger build).
- **MakePlayingCards (MPC)** is another bulk deck printer with a similar uploader.
