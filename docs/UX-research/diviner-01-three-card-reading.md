# A reader's report: doing a three-card reading

*Persona: a practising tarot reader. I don't care much about which Renaissance duke
paid for which deck — I want to **pull cards and read them**. I want clear
upright/reversed meanings, and ideally a deck that's actually built for divination.
Date of visit: Jun 2026.*

---

## What I came to do

Draw a three-card spread, get meanings I can work with, and figure out which deck
to use for readings.

## What I found out

**The Caster works and is pleasant.** From the landing page, "🔮 Draw a Spread" took
me straight to the Caster. It draws three cards with named positions —
**Structures · Process · Possibilities** — and has a deck dropdown (one deck, or
"All Decks — cross-deck draw, 768 cards"). I cast and got: *13 — Death (Marseille)*,
*Nine of Coins (Visconti-Sforza)*, *Queen of Cups (Visconti-Sforza)*. Re-cast,
Copy JSON, and Download buttons are all there.

**Divination is genuinely supported — on the right decks.** Nine decks carry
divinatory sections. The ones actually built for reading are obvious once you find
them:
- **Etteilla I/II/III (1789+)** — ~202 divinatory entries each; the first decks
  *designed* for fortune-telling. Every card has "Card in Etteilla's System",
  Upright, Reversed.
- **Golden Dawn / RWS (1909)** — 156 entries; "Divinatory Meaning" +
  "Reversed / Ill-Dignified", plus astrology/Hebrew/Tree-of-Life correspondences.
- **Marseille (Conver, 1760)** — 156 entries; Upright/Reversed (added by the
  occultists, and the site says so).

So as a reader I'm well served — *if* I know to pick Etteilla or Golden Dawn.

## UX bugs & friction

1. **The default cross-deck draw mixes traditions in one spread.** My three cards
   came from two different decks (Marseille + Visconti). Fun, but as a reader I'd
   usually want one coherent deck; the cross-deck mix is the default and a purist
   might not notice the dropdown that fixes it.
2. **The Caster is deliberately minimal — the actual *reading* lives elsewhere.** The
   page says plainly: *"This is the simple version: it draws; recursive.eco
   interprets with AI, renders Oracle cards, keeps a Journal."* So to get an
   *interpretation* (not just three card names), I have to leave for recursive.eco
   and sign in. The static site draws but doesn't read. That's an honest boundary
   but a reader arriving for a reading hits a wall at the most interesting moment.
3. **No guidance on which deck to read with.** Nothing tells a reader "for divination,
   start with Etteilla or Rider-Waite." I had to infer it from which decks had the
   most upright/reversed sections.

## Things I couldn't understand (candidate grammar/UX gaps)

1. **Why does a 1442 game deck offer me a "Reading"?** Cary-Yale (1442) and
   Visconti (1451) have "Reading" sections — yet every one of their cards also says
   *"made to play a game… not for divination, which arrived centuries later."* As a
   reader I'm confused: am I meant to read with these or not? The site offers the
   reading and disowns it in the same breath. (A historian loves this honesty; a
   diviner finds it contradictory.)
2. **Upright vs Reversed provenance.** The Marseille Reversed meanings are "a later
   overlay added by Etteilla and the occultists." Good to know — but then *whose*
   reversed meaning am I reading on the Marseille card? Etteilla's? RWS's? The card
   doesn't say which system its reading comes from.
3. **No bridge from a drawn card to its meaning.** After casting, I get card *names*.
   I couldn't tell from the Caster how to jump to each drawn card's
   upright/reversed text without separately going to the Cards view and finding it.

## Verdict / for the team to assess

- **The bones of a reading practice are here** (draw → positions → per-card
  upright/reversed), and the honest sourcing is unusual and trustworthy.
- **Two friction points are worth a decision:** (a) the Caster draws but can't
  interpret without leaving for recursive.eco — is there a lightweight inline
  meaning view we could add? and (b) a reader needs **guidance on deck choice** and a
  **draw → meaning** link.
- **One content question:** decide how to handle "Reading" sections on game-era
  decks — keep them (with a clearer "this is a modern overlay" label) or move
  divination to the decks that were built for it.
