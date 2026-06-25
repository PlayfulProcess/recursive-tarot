# Yve Lepkowski decks — import resume plan

## ✅ STATUS (Jun 23 2026): 5 of 6 imported, on dev, verified
- Tarocchino Arlecchino (64), Clown Town Tarot (78), Anecdotes Tarot (78),
  Petit Lenormand (36, gap fixed), Arlecchino's Augmented Arcana (84) — all live in the
  homepage "Contemporary decks" band, all with her own guidebook text + CC-BY-SA attribution,
  archetype-mapped, historical genealogy cut unchanged (25). Verified in the preview:
  homepage band shows all 7 contemporary decks; Clown Town viewer reports "Interpretation 100%
  / The card 100%", images load, console clean.
- REMAINING: only **Clown Town Playing Cards (54)** — a French-suited playing-card art deck,
  NOT on the platform, no card meanings, images only in her downloadable files. Doesn't fit the
  grammar/meaning pattern; would need a manual image-sourcing approach. Deferred.
- Follow-ups: CDN-mirror images (Drive → recursive.eco CDN) for all 5; the 2 Tarocchino
  Significators' art + the 2 Lenormand cards (Cosmia/Bouquet) images; Augmented added-card meanings (her PDF).

---


Status of importing Yve Lepkowski's 6 CC-BY-SA decks (stolen-thyme.com) into recursive-tarot
as contemporary grammars with her **own guidebook text** (not the platform's paraphrase).
Licensing: all CC-BY-SA-4.0 (= repo license); attribution carried in `_grammar_commons`.

Pattern per deck: transplant platform structure (get_grammar) → scrape HER guidebook for
verbatim meanings → write `tarot/<slug>/grammar.json` (provenance:'living', archetype
mappings, lineage to a historical parent) → add to `_collection.json` (auto-sorts into the
homepage "Contemporary decks" band via provenance=='living') → check_all → verify.
Images: hot-linked from the platform's Google Drive URLs for now; CDN-mirror is a follow-up
(user chose: mirror via recursive.eco CDN using MCP set_item_image, then point repo at CDN URLs).

## Deck status

1. **Tarocchino Arlecchino** (64) — ✅ DONE. `tarot/tarocchino-arlecchino/`. Her full Etteilla
   guidebook scraped (62 cards) + 2 Significators added; verbatim meanings in
   `research/yve-lepkowski/tarocchino-arlecchino-cards.json`. Parent: tarocchino-bologna.

2. **Clown Town Tarot** (78) — ⏳ platform structure retrieved (get_grammar bc1953b2…; images on
   Drive). Guidebook HAS per-card pages (her literary prose + image description, NO upright/
   reversed, NO keywords). URL: `stolen-thyme.com/clown-town-tarot/guidebook/<slug>/`
   - Majors (22): the-fool, i-the-magician, ii-the-papess, iii-the-empress, iiii-the-emperor,
     v-the-pope, vi-the-lover, vii-the-chariot, viii-justice, viiii-the-hermit,
     x-the-wheel-of-fortune, xi-strength, xii-the-hanged-one, xiii, xiiii-temperance,
     xv-the-devil, xvi-the-house-of-god, xvii-the-star, xviii-the-moon, xviiii-the-sun,
     xx-judgment, xxi-the-world
   - Minors (56): <ace|two|three|four|five|six|seven|eight|nine|ten|page|knight|queen|king>-of-<coins|batons|swords|cups>
   - SCRAPE BLOCKED by session limit; agents write to research/yve-lepkowski/clown-town-raw/b{1..6}.json.
   - Parent: tarot-de-marseille-conver (RWS/Marseille 78-line). Suits Coins/Batons/Swords/Cups.

3. **Anecdotes Tarot** (78) — ⏳ guidebook HAS per-card pages (Joanna Newsom song epigraph +
   image description + interpretation + "Selected Meanings" keyword list; no reversed).
   URL: `stolen-thyme.com/anecdotes-tarot/guidebook/<section>/<slug>/`, sections: the-trumps,
   the-suit-of-{batons,coins,swords,cups}. Trumps renamed after Newsom songs
   (0 bridges-and-balloons … x-sapokanikan=Wheel … xiii-cosmia=Death … xxi-time-as-a-symptom).
   Minors <rank>-of-<suit>. Parent: tarot-de-marseille-conver. Keep the song epigraph per card.

4. **Arlecchino's Augmented Arcana** (84) — ⚠️ NO meaning guidebook on the web; per-card pages are
   ART DESCRIPTIONS only (e.g. /zz_Prudenza/?longdesc=4455, /batons_02/?longdesc=4396); divinatory
   meanings are PDF-only. Plan: reuse Tarocchino Arlecchino's Etteilla meanings for the overlapping
   cards (by archetype) + her art descriptions for all; the 6 added majors (Arlecchino, Colombina,
   Fede/Faith, Speranza/Hope, Carità/Charity, Prudenza/Prudence) and pips 2–5 use art-desc + note.
   Italian names. Parent: tarocchino-arlecchino. get_grammar 67314102… (saved earlier).

5. **Petit Lenormand** (36; platform has 34 — fix +2) — ⚠️ NO per-card guidebook; one overview page
   with art description + Newsom song ref per card. Her 36-card list (custom names):
   1 Rider, 2 Clover, 3 Ship, 4 Home, 5 Tree, 6 Clouds, 7 Serpent, **8 Cosmia** (vs Coffin),
   9 Bouquet, 10 Scythe, 11 Whip, 12 Birds, 13 Child, 14 Fox, 15 Bear, 16 Stars, **17 Goose** (vs
   Stork), 18 Dog, 19 Tower, 20 Garden, 21 Mountain, **22 Roads** (Crossroads), **23 Rabbits** (Mice),
   24 Heart, 25 Ring, 26 Book, 27 Letter, 28 Man, 29 Lady, **30 Dove** (vs Lily), 31 Sun, 32 Moon,
   33 Key, 34 Fish, 35 Anchor, 36 Cross. The missing 2 in the 34-card import are her renamed cards —
   diagnose by comparing platform names to this list. get_grammar b13cd9ca…. Parent: petit-lenormand
   tradition (cartomancy offshoot). Content scrapeable from the single overview page (no agents needed).

6. **Clown Town Playing Cards** (54) — ❌ NOT on platform; source fully from stolen-thyme
   (clown-town-tarot companion). French-suited 52+2 jokers. Parent: playing-card root
   (madiao-money-cards → mamluk-deck → French-suited). Lowest priority.

## Resume after limit reset (10:40pm America/Sao_Paulo)
Re-run the file-writing scrape agents for Clown Town (6 batches) and Anecdotes (6 batches),
then build each with the import script (generalize scripts/import_yve_deck.py for RWS decks).
Lenormand + its count-fix can be done WITHOUT agents (single-page fetch). Verify each via
check_all + the homepage contemporary band (provenance-driven) + the cards viewer.
