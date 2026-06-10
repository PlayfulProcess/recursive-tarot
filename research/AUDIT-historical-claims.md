# Historical-Claims Audit — recursive-tarot decks

Date: June 10 2026 (Opus 4.8). Scope: every `tarot/*/grammar.json` name +
description + `index.html`, against the project's evidence-first brand. Severity:
**FIX NOW** (wrong or self-contradictory) · **HEDGE** (overstated) ·
**WATCH** (defensible but worth a clause) · **VERIFY** (likely error, confirm).

## Summary
The library is, overall, unusually careful — game decks are called games, the
"Charles VI", Mantegna, Court de Gébelin and Ganjifa entries actively debunk the
myths attached to them, and most claims are hedged. The problems are concentrated
in a handful of **superlative titles** ("The Oldest", "The First") that collide
with each other across decks. One is a true self-contradiction.

## Findings

| Deck | Claim (quoted) | Problem | Severity | Rewording |
|---|---|---|---|---|
| visconti-sforza | NAME: *"The Oldest Tarot (Bonifacio Bembo, c. 1451)"* | Contradicts our own **cary-yale** (c. 1442, "possibly the oldest tarot fragment of all") and **brera-brambilla** (c. 1442–47). Its OWN description more accurately says "oldest **near-complete** tarot". | **FIX NOW** | "The Oldest Near-Complete Tarot (attr. Bonifacio Bembo, c. 1451)" |
| visconti-sforza | NAME: *"Bonifacio Bembo"* (as fact) | Attribution is debated (also Zavattari workshop). | HEDGE | "attr. Bonifacio Bembo" |
| noblet | NAME/DESC: *"The Oldest Surviving Tarot de Marseille"* | Tension with **cary-sheet** ("earliest surviving evidence of the Tarot de Marseille pattern itself", c. 1500). Resolvable: Cary Sheet = earliest *pattern evidence* (uncut sheet); Noblet = oldest surviving *complete deck*. | HEDGE | "The Oldest Surviving **Complete** Tarot de Marseille **Deck**" |
| oswald-wirth | DESC: *"The first overtly occult tarot deck"* | Superlative; risks colliding with etteilla-i's "first tarot built expressly for divination". Different senses (divination 1788 vs occult-initiatic design 1889) — make that explicit. | HEDGE | "the first tarot conceived as an explicitly occult, initiatic instrument — distinct from Etteilla's earlier divination deck" |
| mamluk | DESC: *"43 of an original 52 cards survive"* | Standard scholarship (Mayer 1939; Dummett) usually cites **~48** surviving cards in the Topkapı set (with some from a second, later deck). "43" looks off. | **VERIFY** | confirm against Mayer/Dummett; likely "48 of ~52". (Not auto-changed — needs a source check.) |
| golden-dawn | NAME: *"…with Rider-Waite-Smith Imagery"* | Honest as-is, but a reader may conflate RWS (1909) with the GD's own deck. | WATCH | already names the imagery; add one DESC clause: the GD's own deck was never published; RWS is Waite & Pamela Colman Smith's later public adaptation of the same school. |
| cary-sheet | NAME: *"Earliest Marseille Pattern"* | Defensible (uncut sheet c. 1500). Pairs fine with the Noblet hedge above. | WATCH | optionally "Earliest **Known** Marseille Pattern". |
| sola-busca | *"The First Fully-Engraved Deck" / "earliest … scenically illustrated"* | Well-established in scholarship and load-bearing for the RWS-borrowing point. | WATCH (keep) | optionally "earliest **known**". |
| etteilla-i | *"the first tarot deck built expressly for divination"* | Accurate and important; keep (now distinguished from Wirth above). | OK | — |
| charles-vi / mantegna / court-de-gebelin / ganjifa / besancon | myth-debunking framings | Exemplary — these are the model. | OK | — |

## Applied this session
FIX-NOW + the clear HEDGE items (visconti-sforza title + attribution; noblet
title; oswald-wirth description) edited in the grammars; meta regenerated.

## Left for a follow-up (needs a source check, not auto-applied)
- **mamluk survivor count** — VERIFY "43" vs "48" against Mayer/Dummett before editing.
- **golden-dawn** — add the one-clause RWS-is-Waite's-adaptation note (judgment edit).
- Per-card **occult-projection** spot-check on game decks (Visconti, Marseille,
  Minchiate, Sola Busca): confirm card `sections` don't present divinatory meanings
  as native to a game deck. (Sampled descriptions are clean; full per-card pass pending.)
