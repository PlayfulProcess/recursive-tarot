# Yve Lepkowski's five decks against what she publishes (October 5 2026)

PlayfulProcess asked for a check of "her cards and information vs what she publishes", for errors.

## How

Every page, post and media description of stolen-thyme.com (311 pages and posts, 922 media items,
read through its WordPress API on Oct 5, including the `alt` text of every card image), compared
with the sections of our five grammars that are meant to be her words. For each section: which of
its sentences appear word for word on her site, and whether the page holding them is the same
card. Song titles and anything in quotation marks are ignored, so lyric lines and punctuation in
quotes cannot cause a miss. "Song reference", "Traditional meaning" and "Also called" are skipped
(not hers, or not prose). Script: `scripts/audit_yve_decks.py` (it reads the API dumps; the dumps
are not committed).

**Not checked:** the images. Whether each picture sits on the right card needs her original files
(the ZIPs on her Downloads page, or the copy in PlayfulProcess's Drive).

## What it found

- **No text sits on the wrong card.** Every passage that is hers comes from her page for that card.
- **Petit Lenormand: 100%** of the card descriptions are hers, word for word (her image `alt` text).
- **Clown Town Tarot: 99%.** Three interpretations (Judgement, 8 of Batons, 4 of Swords) and a
  sentence here and there are not on her site; they may come from her PDF guidebook.
- **Anecdotes Tarot: 95%.** Two cards are rewritten rather than hers: the **Nine of Coins** and the
  **Page of Coins** (both "The card" and "Interpretation" are shorter paraphrases of her pages). The
  **Three of Cups** "Interpretation" is not hers at all. About 25 more cards each have one or two
  sentences that are not on her site.
- **Arlecchino's Augmented Arcana: 97%.** Most meanings come from her Tarocchino guidebook, as the
  deck's note says, but a few are not hers: Il Vecchio's upright and reversed (a chronos/kairos
  split that is not in Etteilla), and single meanings on the King of Batons, Nine of Coins, Knight of
  Cups and Ace of Cups. The Queen of Batons ends with a summary sentence ("The description continues
  with details about…") that a machine wrote. Her Augmented meanings are published only in her PDF,
  so these need the file.
- **Tarocchino Arlecchino: the 64 "The card" sections are paraphrases**, not her words. The deck's
  own note says so ("'The card' notes paraphrase her iconography text"), but the deck is presented
  as hers. Her own descriptions are on her guidebook pages.

## Proposed fix (waits for PlayfulProcess's word)

1. Replace every passage that is not hers with her own text, from her pages (and her PDFs for the
   Augmented meanings and the three Clown Town interpretations), leaving out the lyric epigraph at
   the top of each Anecdotes page.
2. Where she wrote nothing for a field, leave the field empty rather than fill it.
3. Update each deck's `modifications` note to say exactly what was changed, as her licence asks.
4. Check the pictures against her ZIP files.

## Per deck

### tarocchino-arlecchino: 120 of 229 sentences found word for word on her site (52%)

- **Not hers at all** (no sentence found): The card on 64 card(s); Upright meaning (Etteilla system) on 3 card(s); Reversed meaning (Etteilla system) on 2 card(s); Significator (Etteilla tradition) on 2 card(s)
   Le Bateleur (The Magician) (The card), La Papesse (The High Priestess) (The card), L'Imperatrice (The Empress) (The card), L'Empereur (The Emperor) (The card), Le Pape (The Hierophant) (The card), L'Amour (The Lovers) (The card), Le Chariot (The Chariot) (The card), La Temperance (Temperance) (The card), La Justice (Justice) (The card), La Force (Strength) (The card), La Roue de Fortune (Wheel of Fortune) (The card), Le Vieillard (The Hermit) (The card), Le Vieillard (The Hermit) (Upright meaning (Etteilla system)), Le Vieillard (The Hermit) (Reversed meaning (Etteilla system)), Le Pendu (The Hanged Man) (The card), La Mort (Death) (The card), Le Diable (The Devil) (The card), Le Foudre (The Tower) (The card), L'Étoile (The Star) (The card), La Lune (The Moon) (The card), Le Soleil (The Sun) (The card), Le Monde (The World) (The card), L'Ange (Judgement) (The card), Le Roi de Baton (King of Batons) (The card), La Reine de Baton (Queen of Batons) (The card), Le Chevalier de Baton (Knight of Batons) (The card), Le Valet de Baton (Page of Batons) (The card), L'As de Baton (Ace of Batons) (The card), Le Dix de Baton (Ten of Batons) (The card), Le Neuf de Baton (Nine of Batons) (The card), Le Huit de Baton (Eight of Batons) (The card), Le Sept de Baton (Seven of Batons) (The card), Le Six de Baton (Six of Batons) (The card), Le Roi de Coupe (King of Cups) (The card), La Reine de Coupe (Queen of Cups) (The card), Le Chevalier de Coupe (Knight of Cups) (The card), Le Chevalier de Coupe (Knight of Cups) (Upright meaning (Etteilla system)), La Servante de Coupe (Maid of Cups) (The card), L'As de Coupe (Ace of Cups) (The card), L'As de Coupe (Ace of Cups) (Upright meaning (Etteilla system)), Le Dix de Coupe (Ten of Cups) (The card), Le Neuf de Coupe (Nine of Cups) (The card), Le Huit de Coupe (Eight of Cups) (The card), Le Sept de Coupe (Seven of Cups) (The card), Le Six de Coupe (Six of Cups) (The card), Le Roi d'Épée (King of Swords) (The card), La Reine d'Épée (Queen of Swords) (The card), Le Chevalier d'Épée (Knight of Swords) (The card), Le Valet d'Épée (Page of Swords) (The card), L'As d'Épée (Ace of Swords) (The card), Le Dix d'Épée (Ten of Swords) (The card), Le Neuf d'Épée (Nine of Swords) (The card), Le Huit d'Épée (Eight of Swords) (The card), Le Sept d'Épée (Seven of Swords) (The card), Le Six d'Épée (Six of Swords) (The card), Le Roi de Denier (King of Coins) (The card), La Reine de Denier (Queen of Coins) (The card), Le Chevalier de Denier (Knight of Coins) (The card), La Servante de Denier (Maid of Coins) (The card), L'As de Denier (Ace of Coins) (The card), Le Dix de Denier (Ten of Coins) (The card), Le Neuf de Denier (Nine of Coins) (The card), Le Neuf de Denier (Nine of Coins) (Reversed meaning (Etteilla system)), Le Huit de Denier (Eight of Coins) (The card), Le Sept de Denier (Seven of Coins) (The card), Le Six de Denier (Six of Coins) (The card), La Folie (The Fool) (The card), Significator — Arlecchino (the Harlequin) (The card), Significator — Arlecchino (the Harlequin) (Significator (Etteilla tradition)), Significator — Arlecchina (the Lady Harlequin) (The card) …

### clown-town-tarot: 922 of 936 sentences found word for word on her site (99%)

- **Not hers at all** (no sentence found): Interpretation on 3 card(s)
   Judgement (Interpretation), 8 of Batons (Interpretation), 4 of Swords (Interpretation)
- **Partly different** (some sentences not on her site): The Papess (High Priestess) (Interpretation, 1 of 11), The Empress (Interpretation, 1 of 5), The Pope (Hierophant) (Interpretation, 1 of 5), The Devil (Interpretation, 1 of 6), 2 of Batons (Interpretation, 1 of 3), 4 of Batons (Interpretation, 1 of 4), 6 of Cups (Interpretation, 1 of 2), 7 of Cups (Interpretation, 1 of 2), 10 of Cups (Interpretation, 1 of 2), 10 of Swords (Interpretation, 1 of 4), 3 of Coins (Interpretation, 1 of 3)

### anecdotes-tarot: 959 of 1013 sentences found word for word on her site (95%)

- **Not hers at all** (no sentence found): The card on 2 card(s); Interpretation on 3 card(s)
   Nine of Coins (The card), Nine of Coins (Interpretation), Page of Coins (The card), Page of Coins (Interpretation), Three of Cups (Interpretation)
- **Partly different** (some sentences not on her site): Anecdotes (Interpretation, 2 of 11), Divers (Interpretation, 1 of 17), 81 (Interpretation, 1 of 12), Book of Right-On (Interpretation, 2 of 10), Soft as Chalk (Interpretation, 1 of 11), Sapokanikan (Interpretation, 1 of 10), Ace of Batons (Interpretation, 1 of 4), Eight of Batons (Interpretation, 1 of 5), Four of Coins (Interpretation, 1 of 5), Ten of Coins (Interpretation, 1 of 7), Two of Swords (Interpretation, 1 of 8), Three of Swords (Interpretation, 4 of 8), Four of Swords (Interpretation, 2 of 6), Five of Swords (The card, 1 of 3), Five of Swords (Interpretation, 2 of 4), Six of Swords (Interpretation, 1 of 5), Seven of Swords (Interpretation, 2 of 5), Eight of Swords (Interpretation, 1 of 8), Nine of Swords (Interpretation, 3 of 9), Ten of Swords (Interpretation, 1 of 7), King of Swords (The card, 1 of 8), Ace of Cups (Interpretation, 1 of 7), Five of Cups (Interpretation, 2 of 3), Ten of Cups (Interpretation, 1 of 4)

### petit-lenormand: 67 of 67 sentences found word for word on her site (100%)


### arlecchinos-augmented-arcana: 551 of 570 sentences found word for word on her site (97%)

- **Not hers at all** (no sentence found): Upright meaning (Etteilla system) on 3 card(s); Reversed meaning (Etteilla system) on 2 card(s); Note on 6 card(s)
   Il Vecchio (The Old Man/Hermit) (Upright meaning (Etteilla system)), Il Vecchio (The Old Man/Hermit) (Reversed meaning (Etteilla system)), Arlecchino (The Harlequin) (Note), Colombina (The Dove) (Note), La Fede (Faith) (Note), La Speranza (Hope) (Note), La Carità (Charity) (Note), La Prudenza (Prudence) (Note), Nove di Denari (Nine of Coins) (Reversed meaning (Etteilla system)), Cavaliere di Coppe (Knight of Cups) (Upright meaning (Etteilla system)), Asso di Coppe (Ace of Cups) (Upright meaning (Etteilla system))
- **Partly different** (some sentences not on her site): Regina di Bastoni (Queen of Batons) (The card, 1 of 3), Sei di Bastoni (Six of Batons) (The card, 1 of 2)

