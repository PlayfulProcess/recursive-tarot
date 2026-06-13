# Grammar corrections queue (from research → apply to grammar.json in a batch)

Research dossiers flagged these factual errors in the live grammars. Each is applied
in a focused, verified pass (research-first, then grammar edits — the maintainer's order).
Confidence noted; only ✅-corroborated items get applied without a further check.

## tarot/etteilla-i-livre-de-thot/grammar.json
- ✅ **Card 13 "Le Grand Prêtre"**: `archetype` maps to `the-hierophant` → should be
  **the-lovers** (TdM VI). Card 13 = *Le Mariage* (Marriage/Union), the reworked Lovers.
  "High Priest" is a *posthumous* Etteilla II/III re-titling. Corroborated: agent + my
  independent WebSearch (Papus correspondence 13↔Lovers) [@web_etteillastrumps; @web_pdr_etteilla].
- ✅ **Card 21 "Le Despote Africain"**: `archetype` maps to `the-emperor` → should be
  **the-chariot** (TdM VII). Corroborated: agent + independent search (21↔Chariot)
  [@web_etteillastrumps; @web_benebell_etteilla]. (Edition note: Grimaud/Etteilla-III names
  this card "Dissension"; both still map to the Chariot.)
- ✅ **Card 78 "La Folie"**: named "The Questioner – Female" / `etteilla:significator-female`
  → La Folie is **the Fool (0 / unnumbered)**. The **female querent significator is Card 8
  (Le Repos)**; Card 1 (Le Chaos) = male significator (already correct). Fix the name +
  significator label on card 78, and tag card 8 as female significator.
- ⚠️ **Description** says the deck "adds querent cards and four element cards" → it is a
  78-card pack: querent significators ARE trumps 1 & 8; elements are embedded in the
  cosmogony trumps, not extra cards. Reword (medium — reword, don't delete the nuance).
- note: Card 15 "Maladie" correctly = the Bateleur/Magician (TdM I) — a *demotion*; fine as is.

## tarot/court-de-gebelin-tarot/grammar.json
- ✅ **atout-06 (Lovers)**: the "Vice/Virtue – Hercules at the crossroads" reading is the
  **Comte de Mellet's**, not Gébelin's (Gébelin only added the caption "Marriage"). Re-attribute
  [@web_robertplace_firstoccult; @web_benebell_lovers].
- 🟡 **atout-09 (Hermit)**: "Egyptian seeker ('Capuchin')" → Gébelin reads the lantern-bearer
  as **Diogenes** (seeking an honest man by daylight). Replace "Capuchin"/Egyptian-seeker
  (medium) [@web_villarevak_gebelin].
- 🟡 **atout-10 (Wheel)**: keep — but do NOT let Sphinx/Typhon/Hermanubis migrate in; those are
  Lévi/Waite additions, not in Gébelin's 1781 plate.
- 🟡 **book-of-thoth / description**: split the etymologies — "Royal Road" (Tar+Ro) is
  **Gébelin's**; "Ta-Rosh = road/science of Thoth" is **Mellet's**.
- note: Gébelin birth year is contested (1719/1724/1725/1728); "1725" defensible, footnote the spread.

## tarot/mamluk-deck/grammar.json
- ✅ already fixed on dev: survivor count "~48 survive / ~43 original + later replacements / 52 complete".

## tarot/madiao-money-cards/grammar.json
- ✅ description cites **"Dummett & Mann, The Game of Tarot"** → correct to **Dummett (1980)**
  solo, or **Dummett & McLeod (2004)** for the games history. "Mann" is an error.
- 🟡 metadata.year 1600 / "17th–18th-c. European collection" (Skokloster) loosely sourced;
  money-suited form firmly attested from Lu Rong (1436–94); Ma Diao codified late Ming. Hedge.

## tarot/golden-dawn-book-t-tarot/grammar.json
- ✅ FIXED: 8 court cards had duplicate "knight"/"queen" keywords (deduped); "a ardent"
  → "an ardent" in the 4 Wands courts.
- ✅ DONE: added a deck-level court-rank naming caution (RWS King=GD Knight, RWS Knight=GD Prince, RWS Page=GD Princess).

## People-pass flags (for dossiers / future grammar notes — not auto-applied)
- Conver: block date **1760** vs BnF authority **Nicolas Conver 1784–1833** — genuine,
  unresolved (inherited/re-signed blocks). Keep both, flagged; don't assert 1760 as his cut.
- Bembo: Visconti-Sforza & Cary-Yale are "workshop of Bembo" — Zavattari is a live rival
  attribution (Algeri). Preserve the hedge in both deck grammars.
- Viéville/Vandenborre sit in the Rouen-Brussels/Belgian line, distinct from the Marseille
  line (Dummett) — make sure the deck dossiers/grammars don't call Viéville a "Marseille".

## tarot/etteilla-ii-egyptian/grammar.json (from research; same family as Etteilla I)
- ✅ Card 78 "La Folie" mislabelled female querent → it's the Fool (0); female significator = Card 8 (Le Repos). (inherited)
- ✅ Card 13 archetype Hierophant → the Lovers (mapping_confidence exact→reworked).
- ✅ Card 21 archetype Emperor → the Chariot.
- ✅ DONE (etteilla-i): card 6 french_name → "Les Astres"; card 8 name → "Le Repos".
- 🟡 Card 8: name "Repos" → "Le Repos" (missing article).
- ⚠️ Minors 22–77 carry **RWS `card:*` archetypes + RWS scenic-pip descriptions** (sunflower, bandage…)
  — anachronistic for an Etteilla near-pip pack. Flag/rewrite (do not import RWS scenes).

## tarot/oswald-wirth-tarot/grammar.json (from research)
- ✅ Le Fou: keep Shin, but it belongs **unnumbered between XX and XXI**, NOT as card 0 at the head
  (card-0-at-head implies the Golden Dawn arrangement Wirth rejected). Fix ordering/note.
- ✅ Le Pendu (12): "element of Water" is the **Golden Dawn** (Mem) reading; Wirth follows Lévi's
  **Lamed** — remove the Water note.
- ✅ Le Monde: "21th letter" typo → "22nd letter" (Tav, 22nd Hebrew letter; World = 21st trump).
- 🟡 Several cards mix Lévi planetary + Golden-Dawn zodiacal attributions under one label — verify vs Wirth.

## tarot/visconti-sforza-tarot/grammar.json (from research; confidence high)
- ✅ `major-20-il-giudizio` tagged `painter_hand: "second"` → should be **bembo**. The six later
  replacements are Fortitude, Temperance, Star, Moon, Sun, World — NOT Judgement (which is original).
- 🟡 Cicognara replacement-hand attribution (e.g. Strength #11 "attributed to Antonio Cicognara")
  is **discredited** (rests on a 19th-c. forgery) — add the hedge.
- 🟡 Refresh provenance line to the verified split: Morgan 35 / Accademia Carrara 26 / Casa Colleoni 13.

## tarot/etteilla-iii-oracle-des-dames/grammar.json (same family)
- ✅ Card 78 La Folie female-querent → Fool; female significator = Card 8 (Le Repos).
- ✅ Card 13 archetype Hierophant → Lovers; Card 21 archetype Emperor → Chariot.

## tarot/tarot-de-marseille-conver/grammar.json (from research; confidence high)
- ✅ `major-03` (L'Impératrice) Iconography claims "Conver's block mislabels her 'II'; she is trump III."
  Uncorroborated and the item's own number=3 — likely a factual error in the prose. Remove/correct.
- 🟡 Elemental suit labels (Coins=Earth, Cups=Water, Swords=Air, Batons=Fire) are a later Golden Dawn
  overlay, not native to a 1760 game pack — mark as overlay, not native.

## tarot/golden-dawn-book-t-tarot/grammar.json (court naming, from RWS/Book-T pass)
- 🟡 Courts use RWS names (King/Queen/Knight/Page) — correct for the imagery, but add the Book T
  equivalents: RWS Knight→GD King, RWS King→GD Prince, RWS Page→GD Princess (rank, not name).
- note: the "mother-letter" trumps' "modern decks add an outer planet" line is correctly hedged
  ("modern decks add"), not a Book T attribution — leave, it's flagged.

## tarot/cary-yale-visconti-tarot/grammar.json (from research; six-rank courts)
- ⚠️ Archetype collisions: Damsel + Knave both → card:page-of-X; Horsewoman + Knight both →
  card:knight-of-X. Six-rank courts can't key onto a 4-archetype scheme — needs distinct ids
  or a disambiguator (design decision — flag for maintainer).
- 🟡 Bembo artist_dates "active c.1444–1482" vs deck "c.1442" — align to floruit c.1442.
- 🟡 description vague on counts; state firm 67 surviving / ~86 original.

## tarot/charles-vi-tarot/grammar.json — SCHOLARLY DEBATE (maintainer decision)
- ⚠️ Origin attribution: repo says **Ferrarese / B-order** (older Dummett classification). Newer
  **BnF Catalogue général** attributes it to the **Florentine** workshop of Apollonio di Giovanni
  & Marco del Buono, c. 1460 (A-leaning: all virtues below Death). Genuinely debated — do NOT
  silently flip; maintainer should choose framing. Sources in research/decks/charles-vi-tarot.md.
- 🟡 "17 trumps" overcount where it appears — it's 16 trumps + 1 Page of Swords = 17 cards
  (the emergence node "16 Surviving Trumps" is already correct).
- 🟡 Missing trumps: Magician, Popess, Empress, Wheel, Devil, Star.

## tarot/minchiate-florence-tarot/grammar.json — Papi identities (verify before applying)
- ⚠️ The five Papi: grammar names them Popess/Empress/Emperor/Pope/Love. Scholarly identities:
  I=Bagatto (Juggler), II=Grand Duke, III=Western Emperor, IV=Eastern Emperor, V=Love. NO Pope
  card; Popess dropped (not folded in). 5-card identity rewrite — confidence medium; verify.
- ✅ DONE: Il Gobbo (XI)→Hermit mapping_confidence "exact" → "loose".
- 🟡 suit→element pairings are a modern overlay, mark non-historical.

## Fragment grammars — safe metadata gaps (from fragments pass)
- ✅ este-tarot: add metadata function: game, ancestry: ancestral (has order:B, branch:roots).
- ✅ cary-sheet: add metadata order: C, function: game (has ancestry).
- ✅ rosenwald-sheet: add metadata order: A, function: game (has ancestry).
- 🟡 este description "c. 1450" — add the c.1470s (Pollett) hedge.

## tarot/sola-busca-tarot/grammar.json (from research; quality flags)
- 🟡 Per-card "Scene" texts are generic placeholders, not real engraving descriptions — rewrite
  from primary scans when WebFetch is restored (do not fabricate).
- 🟡 Grammar omits the named court figures (Amone/Olinpia/Natanabo, Alexander cycle); court order
  listed Page→King (standard is King–Queen–Knight–Page).
- ✅ corroborated downstream: SB Three of Swords → RWS Three of Swords; SB Ten of Swords echoes RWS.

## tarot/tarocchino-bologna/grammar.json (from research; mostly accurate)
- 🟡 sort_order 0–21 is positional; the printed Bolognese numbering runs only 5–16 (low/high
  trumps unnumbered). Note this so users don't read it as full sequential numbering.
- 🟡 1725 gloss: equal-rank Papi predate 1725; only the turbaned-Moor imagery is the 1725 change
  (Montieri affair / Cardinal Ruffo edict). The two identical Moors (mor2.gif reuse) is genuine.
- note: Fibbia origin legend (c.1419) is apocryphal (Berti) — keep flagged.

## tarot/vieville-tarot/grammar.json (from research; confidence medium)
- ✅ DONE: re-tagged metadata.tradition/branch to Rouen-Brussels/Belgian line.
- 🟡 Trump-16: it's **La Foudre** (a tree under fire/hail + shepherd), NOT the Marseille struck Tower.
- 🟡 Trump-12 Hanged Man is **upright**; trumps 17/18/19 = astronomer-with-compasses / woman-with-spindle / youth-on-horseback (celestial divergences).
- 🟡 "Eastern trump order" label → Bologna-via-Piedmont/Savoy (Belgian line), not "Eastern".

## tarot/mamluk-deck/grammar.json (from research; confidence high)
- ✅ DONE: mamluk-overview reconciled to "~48 survive / ~43 original + replacements / 52".

## tarot/tarot-de-besancon/grammar.json (from research; confidence high)
- 🟡 Tradition Note calls it a "regional cousin" of Marseille → it's a direct **descendant**
  (Marseille Type-II with Juno/Jupiter swap); derives_from set in dossier. Tighten wording.
- 🟡 Juno→high-priestess / Jupiter→hierophant archetypes are the occult overlay, not the game
  deck's own — keep as reading aid with a note. (14 items = 13 cards + 1 emergence.)

## tarot/paris-anonymous-tarot/grammar.json — MISIDENTIFICATION (maintainer review)
- ⚠️ The grammar frames this as a mainstream "C-order Tarot de Marseille (Parisian)", but the
  cited BnF object (ark:/12148/btv1b105109624) IS the famous idiosyncratic **Tarot de Paris** —
  a pattern of its OWN (broken period captions: LAN PEREUT, LER MITE, A TREMPANCE, LES TOILLES,
  LA FOUDRE; figural animal Aces; Hell-mouth XVI = La Foudre, not La Maison-Dieu).
- ⚠️ Self-contradiction: the grammar's "Honesty notes" say it is "NOT the famous Tarot de Paris,"
  yet the cited ark is exactly that deck. Resolve.
- Substantial reframe (name, description, trump titles, branch/tradition). Confidence medium
  (Gallica scan not read card-by-card — WebFetch 403). See research/decks/paris-anonymous-tarot.md.

## tarot/belgian-tarot/grammar.json (from research; confidence medium, Belgian-line corroborated)
- ✅ DONE: trump-13 corrected (Belgian Death IS named La Mort).
- ✅ DONE: belgian metadata re-tagged to Rouen-Brussels/Belgian line.
- 🟡 trump-02 "Le Capitaine Fracasse" → inscription is "L'Espagnol Capitano Eracasse" (Fracasse =
  later Commedia name). trump-12 Hanged Man hangs right-side-up. trump-16 = tree struck by
  lightning + shepherd, NOT a tower / "Maison-Dieu".

## tarot/noblet-tarot/grammar.json (from research; confidence medium)
- 🟡 name/description say "oldest surviving COMPLETE TdM" → it's **near-complete** (Six–Ten of
  Swords missing per BnF/WOPC). Title wording — maintainer call (was deliberately "complete" to
  contrast the Cary *sheet*). Hedge to "near-complete" or keep with a clause.
- 🟡 date "c. 1650" — BnF dates the object **1659** (Noblet active c.1659–1681). Hedge c.1650/1659.
- note: grammar is a 1-item overview stub; cards dossier now supplies trump-by-trump for a fill.
