# Research: The 36 Tattvas of Kashmir Śaiva (Trika) Tantra — 2026-08-07

*Web research grounding the planned deepening of `tarot/thirty-six-tattvas/grammar.json`.
Constraint honored: content claims are sourced from the tradition's primary texts and academic
literature, NOT from Christopher Wallis's copyrighted material (living teacher — "inspired by"
rule applies). Fernando's private Kindle highlights live in `_private/` (gitignored) as
reference-only context for tone; never quoted.*

## Existing grammar reviewed

52 items: 5 "shakti" cards (cit/ānanda/icchā/jñāna/kriyā), 36 numbered tattva cards, 5 composite
"realm" cards, 6 "concept" cards (trinity, spanda, pratyabhijñā, svātantrya, three malas, three
upāyas). The core structure checks out — correct 36-item count, 5/7/24 grouping, correct order,
correct shakti↔pure-tattva mapping, correct aham/idam dynamics for Sadāśiva vs. Īśvara.

## 1. The canonical 36 tattvas

Where classical Sāṃkhya counts 25 tattvas, the non-dual Śaiva systems of Kashmir — the Trika as
synthesized by Abhinavagupta (c. 950–1016 CE) and epitomized by Kṣemarāja's *Pratyabhijñāhṛdayam*
— keep the Sāṃkhya 25 nearly intact as the lower two-thirds and prepend 11 principles above them,
naming what Sāṃkhya's dualism had no vocabulary for: the stages by which a single free
consciousness differentiates into subject and object, and the coverings by which it contracts
into an individual soul.

### Group I — Śuddha (pure), 1–5

Progressive phases of a single self-recognizing consciousness, each keyed to one of five śaktis,
each a shift in how "I" (*aham*) and "this" (*idam*) relate:

| # | Sanskrit (IAST) | Meaning | Note |
|---|---|---|---|
| 1 | Śiva | Absolute subject, pure light of consciousness (*prakāśa*) | "I," no object-pole |
| 2 | Śakti | Self-referential awareness (*vimarśa*), bliss of self-recognition | Consciousness turning back to know itself |
| 3 | Sadāśiva (Sadākhya) | "I am this" — a faint "this" appears inside "I" | Icchā-śakti dominant |
| 4 | Īśvara | "This is my own self" | Jñāna-śakti dominant |
| 5 | Śuddhavidyā (Sadvidyā) | "I am I and this is this" — unity-in-difference | Kriyā-śakti dominant; last tattva where oneness is directly felt |

### Group II — Śuddhāśuddha (pure-impure), 6–12

The hinge: how universal consciousness contracts into a bounded soul. Māyā (6) is — in Trika
terms — NOT Advaita's cosmic illusion but the real power of differentiation, freely exercised
(svātantrya). From it, the five *kañcukas* (cloaks, 7–11), each contracting one universal śakti;
terminating in puruṣa (12), the contracted experiencer Sāṃkhya takes as a given.

| # | Sanskrit | Contracts | Limited to |
|---|---|---|---|
| 6 | Māyā | (differentiation itself) | the formative cause of limitation |
| 7 | Kalā | Kriyā-śakti | "I can do only some things" |
| 8 | Vidyā | Jñāna-śakti | "I can know only some things" |
| 9 | Rāga | Ānanda-śakti | craving born of felt incompleteness |
| 10 | Kāla | Cit-śakti as eternity | sequential time |
| 11 | Niyati | Icchā-śakti as freedom | causal necessity / fate |
| 12 | Puruṣa | all five | the individual embodied experiencer |

### Group III — Aśuddha (impure), 13–36

Runs parallel to Sāṃkhya's prakṛti-tattvas: prakṛti (13, three guṇas in equilibrium) → the inner
instruments buddhi (14), ahaṃkāra (15), manas (16) → five jñānendriyas (17–21: śrotra, tvak,
cakṣus, rasanā, ghrāṇa) → five karmendriyas (22–26: vāk, pāṇi, pāda, pāyu, upastha) → five
tanmātras (27–31: śabda, sparśa, rūpa, rasa, gandha) → five mahābhūtas (32–36: ākāśa, vāyu,
tejas, ap, pṛthvī). Antaḥkaraṇa + tanmātras = the *puryaṣṭaka* ("city of eight"), the subtle
body said to transmigrate.

## 2. Contemplative use & difference from Sāṃkhya

- **Ascent/descent (adhvan):** the *ṣaḍadhvan* (six paths) doctrine — varṇa/mantra/pada
  (subjective) correlated with kalā/tattva/bhuvana (objective). Creation = descent (nimeṣa),
  initiation (dīkṣā) and practice = ascent (unmeṣa) back through the tattvas.
- **Recognition (pratyabhijñā):** liberation as recognition, not acquisition — the map is a
  diagnostic of where in the chain of self-forgetting present experience sits (Kṣemarāja's
  20-sūtra *Pratyabhijñāhṛdayam* is the classic manual).
- **Vs. Sāṃkhya:** Sāṃkhya is dualist (plural inactive puruṣas + one prakṛti); the Śaiva 36
  absorbs its 25 as the lower tier but makes puruṣa and prakṛti *products* of one non-dual
  consciousness contracting itself.

## 3. Gap analysis of the existing grammar (revision priorities)

1. **PRIORITY — single-source over-reliance / living-teacher rule violation.** Nearly every
   `Essence` field for tattvas 01–12 and 32–36 **directly quotes "Wallis" by name**, and the
   grammar's `description` cites the "Tantra Illuminated podcast" as source. Per the repo's own
   name-a-school rule this must become school-titled, "inspired by," own-words content grounded
   in primary texts (Kṣemarāja's aham/idam sūtras, Sanderson/Torella on the kañcukas).
2. **Missing: the Sāṃkhya-25 vs Śaiva-36 comparison** — the single most orienting fact
   ("why 36 and not 25?"). New concept card or addition to `realm-pure`.
3. **Missing: the fourth upāya.** `concept-three-upayas` presents 3 as complete; the Tantrāloka
   recognizes **anupāya** ("no-means"). Real doctrinal gap, not a variant.
4. **Missing: ṣaḍadhvan / dīkṣā framework** — the tradition's own technical name for
   ascent/descent; would connect the deck's oracle framing to an authentic contemplative-ritual
   precedent (the existing unmeṣa/nimeṣa language is the deck's own vocabulary, fine to keep,
   but should not stand alone).
5. **Minor factual:** Śakti tattva yantra claims 12 petals ↔ "twelve vowels of Sanskrit" —
   Sanskrit traditionally counts 16 (or 14) vowels. Reframe as free symbolic choice or fix.
6. **Keep as-is:** the `holographic_mirror` element↔pure-tattva correspondences and chakra
   pairings are already labeled interpretive/inferred — correct; no classical source found for a
   strict 1:1 mirror, so the caveats stay (or strengthen).

**No errors found in:** tattva order/numbering, group boundaries, kañcuka↔śakti mapping,
indriya scheme, three-malas definitions, prakāśa/vimarśa framing.

## 4. Sources

Primary-adjacent / freely citable:
- https://en.wikipedia.org/wiki/Pratyabhijnahridayam
- https://en.wikipedia.org/wiki/Shuddhashuddha_tattvas
- https://en.wikipedia.org/wiki/Tattva_(Shaivism)
- https://en.wikipedia.org/wiki/Aham_(Kashmir_Shaivism)
- https://iep.utm.edu/kashmiri/ (Internet Encyclopedia of Philosophy)
- https://archive.org/details/in.gov.ignca.40271 (Jaideva Singh, *Pratyabhijñāhṛdayam*, full translation)
- https://www.wisdomlib.org/hinduism/essay/gitartha-samgraha-critical-study/d/doc1239318.html
- https://www.hindupedia.com/en/Purya%E1%B9%A3%E1%B9%ADaka · https://www.wisdomlib.org/definition/puryashtaka
- https://library.oapen.org/bitstream/id/00ead885-2d28-40d2-9bee-3b3dab331783/9789004432802.pdf (Sanderson, open access)
- https://www.academia.edu/62632667/Nondualistic_%C5%9Aaivism_of_Kashmir (Torella)

Secondary cross-checks: ashtangayoga.info (Sāṃkhya-vs-Śaiva table), saivism.net (non-standard
grouping — cross-check only), kashmirblogs.wordpress.com + lakshmanjooacademy.org (confirm
anupāya), hindu-blog.com (kañcukas).

Deliberately NOT used for content: Christopher Wallis's *Tantra Illuminated* / podcast / blog.
