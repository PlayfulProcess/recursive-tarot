# How to get a deck printed (The Game Crafter) — full process

This is the verified, end-to-end process, written after actually walking through
it on The Game Crafter (TGC). It includes the **image-conversion step** that isn't
obvious and will get your upload rejected if you skip it.

> **Policy: proof first, publish later.** Always order **one** physical proof
> deck, hold it in your hands, and confirm the print quality before you publish
> it for sale. Don't list a deck you haven't seen printed.

---

## 0. Which decks are print-ready
Only list/print a deck where **every** card cleared the 300-DPI audit:

| Sell as-is (full bleed) | Sell as bordered cards |
|---|---|
| Golden Dawn / RWS · Minchiate · Oswald Wirth · Etteilla II · Mantegna | Marseille · Etteilla I · Etteilla III |

Web-resolution (do **not** print): Visconti, Cary-Yale, Charles VI, Tarocchino,
Besançon, Court de Gébelin.

---

## 1. Get the card files — and convert them to TGC's exact size
The deck art is hot-linked (Cloudflare/Wikimedia), so first pull it to disk, then
**resize to TGC's required 900×1500 px** (our art is 1114×1919 — TGC rejects
anything that isn't *exactly* 900×1500).

```bash
# a) download the print-ready cards into print/decks/<slug>/
python scripts/download_deck_images.py golden-dawn-book-t-tarot

# b) resize them to TGC's exact tarot-card face size (900x1500), cover-fit
python scripts/resize_for_tgc.py print/decks/golden-dawn-book-t-tarot
#   -> writes print/decks/golden-dawn-book-t-tarot-tgc/  (78 files, all 900x1500)
```

`resize_for_tgc.py` scales each card to **fill** 900×1500 and centre-crops the
tiny overflow (only the bleed/border margin is touched — no art is lost). Both
`print/decks/` folders are gitignored; delete them after uploading.

**The deck back** also must be exactly 900×1500. Pick a historical back from the
Print page ("Deck back"), and resize it the same way (or reuse
`print/decks/golden-dawn-BACK-900x1500.jpg`, the blue Carta Francese back already
prepared). TGC note: if you want front and back oriented the same way, rotate the
back image 180°.

---

## 2. Build the deck on The Game Crafter
1. Sign in → **Make → Make a New Game** → name it (e.g. *"Golden Dawn Tarot —
   Recursive Tarot"*).
2. On the game's **Make** tab → **Add Custom Component** (the green button — **not**
   "Add Stock Component"; stock parts are physically blank cards for prototyping).
3. Left sidebar → **Cards** category → search **tarot** → **Tarot Deck**
   (2.75×4.75″, ~$2.84 base) → **Add to Game**. (The "Foil Tarot Deck" is the
   pricier foil variant — skip unless you want foil.)
4. In the Tarot Deck editor:
   - **Name** the deck.
   - **Cards box** ("…exactly 900×1500 to create cards"): drag in **all 78**
     resized faces from the `…-tgc` folder (or click the box → select all 78).
     Each file becomes one card. *(Naming trick: `Name[face,3].png` would set a
     card's face and quantity to 3; plain filenames just make one card each.)*
   - **Back box**: drag in your 900×1500 back image.
5. The page shows **78 cards / 78 total** when done. Cards print double-sided on
   12pt 320gsm black-core matte stock and arrive **unsorted** (TGC's standard).

---

## 3. Proof it (do this before selling)
1. Add the game to your cart (the **$ price** chip, top right) and **check out for
   ONE copy** — this is *you* buying one proof deck.
2. Wait for it to print + ship. Inspect: colour, crop/centring, the bordered cards,
   the back orientation.
3. If anything's off, fix the source image, re-run `resize_for_tgc.py`, re-upload
   that card, and re-proof.

---

## 4. Publish for sale (only after the proof passes)
1. **Sell** tab → set a **price** (TGC shows your base cost; your markup is your
   margin — better than any affiliate cut) + a short description.
2. **Publish to the Game Crafter shop** → copy the public product URL.
3. Paste that URL into `print-products.json` → the deck's `product_url`, commit +
   push. The site's "Print-ready — vendor coming soon" button automatically becomes
   **"Buy a printed deck at The Game Crafter ↗"**.

---

## What an assistant can and can't do here
Documented so future sessions don't re-learn it the hard way:

- **Can** (done for you): download the art, run the 300-DPI audit, resize to TGC's
  exact 900×1500, prep the back, drive the browser to **create the game, add the
  correct Tarot Deck component, and name it**.
- **Can't** (reserved for a human at the keyboard, by design):
  - **Drag files into the page** — `file_upload` is sandboxed to chat-attached
    files, and browsers don't let an agent push arbitrary disk files into a web
    form. So the 78-file drop and the back drop are yours.
  - **Pay / check out** (the proof order) and **accept Terms / Publish** — money,
    legal, and public-listing steps are not done on your behalf.

So the division of labour: the assistant preps every file and builds the deck
shell; you do the drag, the proof purchase, and the publish.

---

## TGC facts worth keeping
- Component: **Tarot Deck**, finished size **2.75×4.75″ (70×121 mm)**.
- Required image size: **900×1500 px** (face and back).
- Stock: 12pt 320gsm black-core matte; double-sided; cards arrive unsorted.
- Price per card ≈ **$0.28**; 10 cards per sheet; component base ≈ $2.84;
  bulk component price drops (e.g. ~$1.13 each at 1000 games).
- Foil and UV-coating are optional upsells.
