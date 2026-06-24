# UX Research — persona walkthroughs

This folder holds **use-case walkthroughs**: an agent roleplays a specific kind of
visitor, actually *uses* tarot.recursive.eco to accomplish a real goal, and writes
up what they **found out**, what **UX friction** they hit, and what they **couldn't
understand**. We use these to inform development from **both** a content (grammar)
and a UX (viewer) perspective.

Each report follows the same shape:
1. *What I came to do* (the goal, in the persona's words)
2. *What I found out* (grounded in actual site content)
3. *UX bugs & friction*
4. *Things I couldn't understand* (candidate grammar gaps)
5. *Verdict / for the team to assess*

> Reports describe what the site contained **at the time of writing** (date in each
> file). Re-verify before acting — the grammars and viewers drift.

---

## The personas

**🏛 Historians / researchers** — care about origins, evolution, attribution,
sourcing. Want the *thread* between cards, not just isolated facts.

**🔮 Tarot readers / diviners** — care about meanings (upright/reversed),
correspondences, doing a reading, choosing a deck to read with.

**🙂 Newcomers / curious people** — know little or nothing. Arrive from a show, a
gift deck, or idle curiosity. Want a quick, friendly answer and an easy path in.

---

## Use-case backlog (✅ = walkthrough written)

### 🏛 Historians
- ✅ **H1 — How did one card evolve?** (Death, 1442→1909) → `historian-01-death-evolution.md`
- ⬜ **H2 — The Justice ↔ Strength swap.** When/why did VIII and XI trade places (Marseille vs Golden Dawn)? Now answerable exactly via `trump_key`.
- ⬜ **H3 — Where did the four suits come from?** Trace Mamluk → Latin suits (cups/coins/swords/batons); test the `mamluk-deck` honesty note.
- ⬜ **H4 — Did divination really come later?** Pin the 1781 Gébelin turn across the collection.
- ⬜ **H5 — The "ancient Egyptian origin" myth.** Who invented it (Gébelin/Mellet), and how does the site flag it as fabricated?
- ⬜ **H6 — Regional families.** How do Minchiate (97 cards) and Bologna (Tarocchino) diverge from Marseille?
- ⬜ **H7 — Makers & patrons.** Who actually made these decks? (People & Institutions grammar)

### 🔮 Tarot readers / diviners
- ✅ **D1 — Do a 3-card reading.** → `diviner-01-three-card-reading.md`
- ⬜ **D2 — Reversed / ill-dignified meanings** for a given card.
- ⬜ **D3 — Which deck should I read with?** Compare Etteilla vs RWS vs Marseille divinatory systems.
- ⬜ **D4 — Save / journal a reading** (hand-off to recursive.eco).
- ⬜ **D5 — Esoteric correspondences** (Hebrew letters, astrology, Tree of Life paths).

### 🙂 Newcomers / curious people
- ✅ **N1 — "Is the Death card bad?"** → `newcomer-01-is-death-bad.md`
- ⬜ **N2 — "Is tarot real fortune-telling?"** Test whether the honest "it was a game" framing lands or disappoints.
- ⬜ **N3 — "Find a specific card by name."** (Tests search — currently missing.)
- ⬜ **N4 — "Is this free? Can I use the images?"** Public-domain / licensing clarity.

---

## Recurring themes so far (across reports)

- **The history is honest and well-sourced** — the "Renaissance game, divination
  added in 1781" spine is consistent and reachable. This is the site's biggest
  strength across all personas.
- **No search box** — hurts newcomers most (N3), but every persona eventually wants
  "take me to card X."
- **Cross-deck comparison tools (Lenses) are powerful but limited** — locked to 6
  decks, no deck picker, per-column scrolling.
- **The same content serves different personas differently** — e.g. a 1442 deck
  offering "Reading" sections delights a historian (here's the evidence) but can
  mislead a diviner (am I supposed to read with this?).
