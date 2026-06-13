---
id: "paris-anonymous-tarot"
type: "deck"
title: "Anonymous Tarot de Paris — BnF (Italian-suited, c. 1600–1650)"
status: "drafting"
confidence: "medium"
last_updated: "2026-06-13"
maintainer_note: "AI-assisted; web-checked against the Dummett spine (Dummett 1980), Depaulis 1984 and Depaulis's BnF cataloguing, Andrea Pollett, Tarot Heritage, WOPC, and the BnF/Gallica object record. WebFetch was blocked (403); web claims rest on WebSearch snippet cross-corroboration, with load-bearing dating anchored to Depaulis. IMPORTANT: the existing tarot/paris-anonymous-tarot/grammar.json MISIDENTIFIES this object as a mainstream named C-order 'Tarot de Marseille'; on the evidence below it is the idiosyncratic *Tarot de Paris*, a pattern of its own. For maintainer + Tarot History Forum review."
era: "c. 1600–1650 (Paris; Depaulis: first half of the 17th century)"
function: "game"
order: "C"
ancestry: "ancestral"
people: []
derives_from: []
---

# Anonymous Tarot de Paris — BnF (c. 1600–1650)

## At a glance

A single surviving, complete **78-card woodcut tarot**, hand-coloured through stencil,
held at the **Bibliothèque nationale de France** and digitised on **Gallica**
(`ark:/12148/btv1b105109624`), catalogued as *"[Jeu de tarot parisien anonyme à enseignes
italiennes]"* [@web_gallica_paris]. It is the deck collectors and scholars call the
**Tarot de Paris** (or *Tarocchi Francesi*): an **early-17th-century Parisian** pack with
**Italian (Latin) suits** — Coins, Cups, Batons, Swords — whose trumps are named and
numbered along the familiar tarot line, *but whose imagery is strikingly idiosyncratic and
unlike either the later Marseille standard or the Belgian/Vieville line*
[@web_wopc_paris; @web_pollett_paris; @web_th_paris]. It is a **game pack**, made for the
trick-taking game of tarot in Paris at the same moment as **Jean Noblet** and **Jacques
Viéville** (both c. 1650), and it survives in **one example only** [@web_wopc_paris;
@dummett1980]. (Confidence: medium overall — the object and its eccentric iconography are
secure; precise dating and "pattern" status rest on Depaulis and secondary description, not
a primary archival document seen here.)

> **Catalogue correction owed.** The repo's `grammar.json` for this slug calls the deck a
> "fully named, mainstream C-order *Tarot de Marseille*" and even gives Marseille-style card
> titles (LA JUSTICE, ATREMPANCE…). That description is **wrong for this object**: the BnF
> pack is the *quirky Tarot de Paris*, not a Marseille. The grammar's own "Honesty notes"
> half-flag this ("note it is **not** the famous idiosyncratic *Tarot de Paris*") — but the
> ark it cites *is* that famous deck. See the grammar-error notes at the end.

## Origin & dating

The deck is anonymous — **no cardmaker's name** appears on the cards (notably the Two of
Coins cartouche, where a maker would normally sign), which is why it is the "anonymous"
Parisian tarot [@web_wopc_paris; @web_pollett_paris]. **Thierry Depaulis**, cataloguing the
BnF holdings, dates it to the **first half of the 17th century** (*"première moitié du
XVIIᵉ s."*) and records it as a complete 78-card set, **woodcut, hand-coloured with stencil,
12.8 × 7 cm**, with a back pattern of **hexagons and Maltese crosses**
[@depaulis1984; @web_tarotsanciens_paris; @web_th_paris]. Popular sources round this to
**"c. 1650"** or **"early 1600s"**; a minority claim of **1559** circulates but is not
supported by the document-minded reading and should be treated as unverified
[@web_wopc_paris; @web_tarotsanciens_paris] (confidence: low on any year more precise than
"first half of the 17th c."). The relevant context is that the **earliest known written
rules of the game of tarot in France** are the abbé **Michel de Marolles**' booklet,
printed at Nevers in **1637** — placing a living French tarot-playing culture exactly around
this deck [@web_marolles_depaulis; @dummett1980].

## Provenance & evidence

The **sole surviving example** is the BnF object on Gallica
(`ark:/12148/btv1b105109624`); there is no second complete witness known
[@web_gallica_paris; @web_wopc_paris]. Modern facsimile/restoration editions exist
(Grimaud/André Dimanche, 1984–85; the *Museo dei Tarocchi* restoration), which is how the
imagery became widely reproducible, but they descend from the one BnF pack
[@web_arnell_paris; @web_th_paris]. The card images used by this collection's grammar are
from the public-domain BnF scan.

## Structure

A standard-count **78-card pack** in outline, but eccentric in nearly every picture:

- **22 trumps (atouts):** 21 numbered + the unnumbered **Fool (Mat)**. The **titles are
  French and the numbering follows the standard tarot trump line** — which is why the deck
  is conventionally read as part of the same family as the later Marseille [@web_wopc_paris;
  @web_pollett_paris]. Card captions are in **rough, often broken period spelling** (e.g.
  *LAN PEREUT* for the Emperor, *LER MITE* for the Hermit, *A TREMPANCE* for Temperance,
  *LES TOILLES* for the Star, *LA FOUDRE* — "the lightning" — for trump XVI), a hallmark of
  the deck [@web_pollett_paris; @web_th_paris].
  - **Order.** Numbered along the C-line that became the Marseille norm (the broad
    southern/French order), *but this deck is not a Marseille*: it carries its own
    pictures. We tag `order: "C"` for the trump *sequence* while flagging that the **pattern
    is the Tarot de Paris's own**, neither Marseille nor Belgian
    [@web_pollett_paris; @dummett1980]. (Confidence: medium — the broad order is reported as
    "as in the standard Marseille sequence," but a card-by-card numeral check against the
    BnF scan is owed; see Open questions.)
- **56 suit cards,** four **Italian (Latin) suits** — **Deniers (Coins), Coupes (Cups),
  Bâtons (Batons), Épées (Swords)** — each Ace–Ten plus four courts
  (**Valet, Cavalier, Reine, Roi**) [@web_gallica_paris; @web_wopc_paris].
  - **The four Aces are unique:** each shows an **animal carrying a flag** that bears its
    suit sign — a **lion** (Coins), a **deer/stag** (Cups), a **griffon** (Batons) and a
    **unicorn** (Swords) [@web_wopc_paris; @web_th_paris]. (Sources agree on the animal/flag
    device but vary on which animal goes with which suit — flag as confidence: medium.)
  - **The Coins pips carry emblems of French cities**; the **Cups** are each a different
    individual vessel; the **Swords and Batons** are drawn so the pieces **intersect /
    cross one another**, in neither the straight Italian nor the Spanish manner
    [@web_th_paris; @web_pollett_paris].
  - Card framing uses a **trompe-l'œil "folded-edge" border** evoking the look of an Italian
    tarot seen with its back turned over — a distinctive Parisian conceit
    [@web_pollett_paris].

## Game or divination?

**Game, unambiguously.** This is a Parisian playing pack of the early 17th century, made for
the trick-taking game of tarot — the same game whose first French rules Marolles wrote down
in 1637 [@web_marolles_depaulis; @dummett2004; @dummett1980]. No divinatory or cartomantic
use of these images is attested; the "meanings" attached to tarot trumps are a documented
**later (18th-century) overlay** that has nothing to do with this object
[@decker1996; @dummett1980]. The grammar should label the deck **"game"** and carry **no
upright/reversed meanings** for its cards.

## What changed from its parent

This is a **root / ancestral** deck in the collection: **no `derives_from` parent** within
the catalogue. Iconographically it is **not** a descendant of the Marseille (which it
predates as a printed standard) and **not** the Belgian/Viéville line; it is a **Parisian
pattern of its own**, drawing on a synthesis of imported card traditions (Italian *trionfi*
ancestry in the trump *subjects*, but with locally invented *pictures*)
[@web_wopc_paris; @web_pollett_paris; @web_th_paris]. The honest framing is comparative
rather than genealogical: alongside **Noblet (Type I Marseille, c. 1650)** and **Viéville
(c. 1650)** it shows that **mid-17th-century Paris hosted several competing tarot patterns at
once**, of which only the Marseille line went on to standardise [@dummett1980;
@web_th_paris]. Where the per-card dossier notes "Changed from…," it is measuring the deck's
pictures **against the later Marseille standard** (as a point of comparison), not against a
true parent.

## The fear question

**No concealment.** A regulated commercial playing pack of the Paris card trade, subject to
the period's playing-card duties; there is nothing hidden or heterodox about it as an object
[@depaulis1984; @dummett1980]. Its eccentric pictures (the ass-eared conjurer, the
goose-drawn chariot, the hell-mouth "Foudre") are **playful and satirical**, in the register
of the carnival/print culture of the day, not a coded esoteric programme — that reading is a
much later import [@web_pollett_paris; @decker1996].

## Counter-voices

Because the imagery is so unusual, esoteric and "lost-knowledge" readers have at times
treated the Tarot de Paris as a repository of special symbolism, and a fringe **1559** dating
has been floated to make it earlier and more "original" [@web_tarotsanciens_paris;
@web_wopc_paris]. The document-first reading is sober: it is a **first-half-17th-century
Parisian game pack**, idiosyncratic because its anonymous maker **localised and embroidered**
the standard trump subjects, not because it transmits hidden doctrine
[@depaulis1984; @dummett1980].

## People

- **Maker: anonymous** — no name on the cards; hence `people: []`. The deck cannot be tied to
  a documented Parisian *cartier* [@web_wopc_paris; @web_pollett_paris].
- **Context figures** (not makers, no dossier required here): **Michel de Marolles**, abbé,
  whose 1637 Nevers booklet gives the earliest French tarot rules and fixes the playing
  culture around this deck [@web_marolles_depaulis]; **Thierry Depaulis**, who catalogued and
  dated the BnF object [@depaulis1984].

## Open questions / corrections owed

- **Fix the grammar's identity claim.** `grammar.json` describes a mainstream named Marseille
  and must be corrected to the **Tarot de Paris** (own pattern). (Do not edit the grammar in
  this pass — flagged for the maintainer.)
- **Verify the trump numbering card-by-card** against the BnF scan; confirm Justice/Force
  positions and the exact captioned numerals before asserting a clean "C-order"
  (confidence: medium).
- **Resolve the Ace animal↔suit pairings** (lion/deer/griffon/unicorn vs which suit) from the
  scan; secondary sources disagree.
- **Devil (XV) vs. Foudre (XVI).** Snippet sources describe both "a Devil beating drums
  before a hell-mouth" and trump XVI *La Foudre* as a hell-mouth; the two cards may have been
  conflated in description. Disambiguate from the scan (confidence: low on the Devil's exact
  scene).
- **Confirm the 12.8 × 7 cm, hexagon-and-Maltese-cross back** and the precise Depaulis
  wording from the printed BnF catalogue (cited here via secondary report).

## Sources

[@dummett1980], [@dummett2004], [@decker1996], [@depaulis1984], [@web_gallica_paris],
[@web_wopc_paris], [@web_pollett_paris], [@web_th_paris], [@web_arnell_paris],
[@web_spiritone_paris], [@web_tarotsanciens_paris], [@web_marolles_depaulis].

---
*Research notes — AI-assisted draft, pending review by the maintainer and the Tarot History
Forum. Skeptical, document-first (Dummett spine; Depaulis on the BnF object). WebFetch
blocked (403); web claims rest on WebSearch cross-corroboration. Corrections welcome.*
