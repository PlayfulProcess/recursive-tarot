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
- 🟡 Court-hierarchy gloss: sections assert flat RWS=GD court equivalence. True by *name*
  (Book T's top court is the "Knight"), but in *rank* the GD Knight ↔ RWS King and GD King
  ↔ RWS Knight. Add one clarifying line so users don't misread the hierarchy. (content edit)

## People-pass flags (for dossiers / future grammar notes — not auto-applied)
- Conver: block date **1760** vs BnF authority **Nicolas Conver 1784–1833** — genuine,
  unresolved (inherited/re-signed blocks). Keep both, flagged; don't assert 1760 as his cut.
- Bembo: Visconti-Sforza & Cary-Yale are "workshop of Bembo" — Zavattari is a live rival
  attribution (Algeri). Preserve the hedge in both deck grammars.
- Viéville/Vandenborre sit in the Rouen-Brussels/Belgian line, distinct from the Marseille
  line (Dummett) — make sure the deck dossiers/grammars don't call Viéville a "Marseille".
