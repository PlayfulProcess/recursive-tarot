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
