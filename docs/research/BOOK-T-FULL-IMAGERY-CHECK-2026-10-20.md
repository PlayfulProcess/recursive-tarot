# Book T full imagery: picture against text (Oct 20 2026)

PlayfulProcess (Oct 20): "Have an agent play with it later and see if images are consistent with text."

All 78 cards of `tarot/book-t/full-imagery/` were rendered to PNG (`build_book_t_full_imagery.py --png`)
and each one was looked at against its card's full Book T (1912) text in `tarot/book-t/grammar.json`
(not only the `follows` excerpt): counts and poses of the suit symbols, hands and clouds, roses, lotuses,
flames and waters, the decan planet above and sign below in Book T's order, the corner letter and element,
the courts' crests, beasts, held objects and rule signs.

**Result: 4 mismatches, all fixed in `compositions.json` (data only) and re-checked; 12 readings left
ambiguous for PlayfulProcess (listed at the end). Every planet/sign pair is in the order Book T names it,
every count of wands, cups, swords and pentacles is right, every Key carries its letter and attribution.**

Verdicts: ok · **fixed** (was a mismatch) · ambiguous (Book T is unclear or the picture leaves a
detail out; the agent's `note` choice kept).

## Aces

| Card | Book T says | Picture shows | Verdict |
|---|---|---|---|
| wands-ace | hand from clouds grasps heavy club, 3 branches (3+4+3 flames), 22 Yods: 3 below right branch, 7 above centre, 12 about left | that, branches with coloured sigil collars; 3/7/6+6 flames | ambiguous (Yod placement; note) |
| cups-ace | hand supports cup on palm, fountain, sprays into calm water, lotuses + lilies, Heh in the spray | all present | ok |
| swords-ace | hand grasps hilt; sword supports white radiant crown; olive right, palm left; six Vaus fall from point | crown, olive viewer's right, palm left, six Vaus beside the blade | ambiguous (whose right; Vaus along the blade, not below the point) |
| pentacles-ace | hand holds rose branch; pentacle of 5 circles, red Greek cross, 12 white rays; small circle, white Maltese cross, 2 wings; "four crosses and two buds" | all present; 4 roses + 2 buds | ambiguous ("four crosses" read as four roses; note) |

## Courts

| Card | Book T says | Picture shows | Verdict |
|---|---|---|---|
| wands-knight | winged warrior, black horse flaming mane + tail, winged helmet + rayed crown, scarlet mantle, winged black horse's head crest, club with flaming ends, flames beneath; 20° Scorpio–Sagittarius | all; crest above helmet and on cuirass; Scorpio, Sagittarius | ok (sigil of the scale and buskin crests left out) |
| wands-queen | crowned, red-gold hair, throne, steady flames beneath; winged leopard heads on crown, cuirass, buskins; hands on couchant leopard; long wand, heavy conical head; Pisces–Aries | all present | ambiguous (flames drawn leaping, Book T says "steady") |
| wands-prince | golden winged crown, large white wings, one wheel, winged lion's head on armour + crown, chariot drawn by lion, fire-wand, flames beneath; Cancer–Leo | all present | ok |
| wands-princess | Amazon, red-gold hair, Corinthian helmet + plume + tiger head, tiger-lined mantle, winged tiger's head on belt, right hand on altar with ram's heads + flames, left on long club with ascending flames and sigil, flames beneath; Earth of Fire | all present, altar at her right (viewer's left) | ok |
| cups-knight | winged youth, white horse not winged, peacock crests, cup with crab issuing, sea beneath; Aquarius–Pisces | all present | ok |
| cups-queen | crowned, throne over flowing water with lotuses, ibis crests, **ibis beside her "whereon her hand rests"**, lotus "in the hand upon the Ibis", cup with crayfish; Gemini–Cancer | was: ibis standing apart on the water, not under her hand. Now: ibis beside the throne, her lotus hand resting on it | **fixed** |
| cups-prince | winged, winged crown, chariot drawn by eagle, scorpion on wheel, eagle crests, still lake, lotus + cup, serpent from cup head down to the lake; Libra–Scorpio | all present | ok ("armour like feathers" left plain; note) |
| cups-princess | Amazon on foaming sea, dolphin to her right, swan crest, lotus + cup with turtle, swansdown mantle | all, dolphin on her right (viewer's left) | ok |
| swords-knight | winged, crowned winged helmet, brown steed, winged six-pointed star crest, drawn sword, dark-driving stratus clouds; Taurus–Gemini | all; clouds dark grey but drawn as a cumulus bank | ambiguous (cloud shape: stratus vs cumulus) |
| swords-queen | wavy hair, crowned, throne over grey cumulus, winged child's head crest, sword + bearded severed head; Virgo–Libra | all present | ok |
| swords-prince | winged, winged crown, chariot drawn by Arch Fays (butterfly wings, pentagram fillets, pentagram wands), winged angelic head crest with pentagram, nimbus clouds, long whirling hair, sword + sickle; Capricorn–Aquarius | all present (2 Fays) | ok |
| swords-princess | Amazon, Medusa crest, Aegis mantle, sword, small silver altar with grey smoke, white clouds | all present | ok |
| pentacles-knight | dark winged warrior, crowned winged helmet, light-brown horse, winged stag crest, ripe corn, hexagram sceptre + pentacle; Leo–Virgo | all present, pentacle at his side | ok |
| pentacles-queen | dark hair, face half light half dark (profile), winged goat crest, goat by her, cube sceptre + gold orb, dark sandy earth; Sagittarius–Capricorn | all present | ok |
| pentacles-prince | winged, chariot drawn by bull, winged bull crest, flowered land, gold orb held downwards + orb-and-cross sceptre; Aries–Taurus | all present | ok |
| pentacles-princess | Amazon, rich brown hair, grass/flowers, grove, winged ram crest, sheepskin mantle, disk sceptre + Ace-like pentacle | all present | ok |

## Small cards (decans)

| Card | Book T says | Picture shows | Verdict |
|---|---|---|---|
| wands-02 | 1 hand from clouds, 2 crossed wands, flames at junction; small wands with five flames; Mars above, Aries below | same | ok |
| wands-03 | 1 hand, 3 wands (2 crossed, 1 upright), flames; Sun / Aries | same | ok |
| wands-04 | 2 hands clasped (First Order grip), 4 crossed wands, flames; small flaming wands; Venus / Aries | same | ok |
| wands-05 | 2 clasped hands, 5 wands (1 upright, 4 crossed), flames; Saturn / Leo | same | ok |
| wands-06 | 2 hands, 6 wands crossed 3 and 3; short flaming wands; Jupiter / Leo | same | ok |
| wands-07 | 2 hands, 6 wands; third hand from cloud at foot holds an upright wand through them; Mars / Leo | 7 wands, third hand below | ok |
| wands-08 | 4 hands (2 each side) in 2 clasped pairs, 8 wands 4 with 4; small wands; Mercury / Sagittarius | same | ok |
| wands-09 | as 8 + fifth hand at foot with a ninth wand upright; Moon / Sagittarius | 9 wands, 5 hands | ok |
| wands-10 | as 8 + fifth hand holding two upright wands; Saturn / Sagittarius | 10 wands, 5 hands | ok |
| cups-02 | hand from cloud low holds lotus over water; stem to top lotus fountain; two crossed dolphins argent and or; gold and silver streams into 2 cups that overflow; Venus / Cancer | same | ok |
| cups-03 | 2 flowers either side over the top cup, flowers pour into lower cups, all overflow, erect triangle; Mercury / Cancer | same | ok |
| cups-04 | 2 upper overflow into 2 lower (not overflowing), one flower at top, two leaves crosswise; Moon / Cancer | same | ok |
| cups-05 | lotus flowers falling right and left, leaves only, stems between cups like a fountain, no water; Mars / Scorpio | same, 5 empty cups | ok |
| cups-06 | 6 flowers, one over each cup, white water flowing, cups not yet full; Sun / Scorpio | same | ok |
| cups-07 | two descending triangles above a point; hand above the lowest cup, below the middle; 6 lotuses (none over the lowest), cups empty; Venus / Scorpio | same | ok |
| cups-08 | 2 flowers over the 2 central cups, overflowing into the 3 lowest (not full); 3 uppermost empty; Saturn / Pisces | same | ok |
| cups-09 | 3 rows of 3, a flower over each pouring; Jupiter / Pisces | same | ok |
| cups-10 | all run over; top cup held sideways by a hand pours into the left upper cup; single lotus over the top cup; Mars / Pisces | same; Mars at upper left | ambiguous (layout; note) |
| swords-02 | 2 crossed swords, a hand each, rose of 5 petals with white rays at the crossing; small daggers supporting Moon / Libra | same | ok |
| swords-03 | 3 hands, 3 swords upright, the central cuts the rose, petals falling, no rays; Saturn / Libra | same | ok |
| swords-04 | 2 hands, 2 swords each, crossing in the centre, rayed rose; daggers with Jupiter / Libra | same | ok |
| swords-05 | 2 hands with 2 swords each falling apart; third hand central upright; petals falling; Venus / Aquarius | same | ok |
| swords-06 | 2 hands, 2 swords each crossing, rose; daggers with Mercury / Aquarius | same | ok |
| swords-07 | 2 hands **each holding three swords**; third hand central sword + the rose; points just touch; Moon / Aquarius | was: each hand's three swords stacked within 2° of each other, so only two showed per side (the card read as five swords). Now fanned from the fist to one meeting point: 3 + 1 + 3 | **fixed** |
| swords-08 | 4 hands (two at each bottom angle), **two swords each**, points touching near the top; the centre pose re-established; Jupiter / Gemini | was: each pair within 0.3°, drawn as one blade (the card read as about five). Now each pair fanned to the shared point: 8 blades | **fixed** (rose for "the pose ... re-established" is the note's reading: ambiguous) |
| swords-09 | 4 hands, 8 swords nearly upright falling apart; fifth hand central; no rose; Mars / Gemini | 9 swords, 5 hands | ok |
| swords-10 | 4 hands, 8 swords falling apart; 2 hands with 2 swords crossed in the centre; no rose; Sun / Gemini | 10 swords, 6 hands | ok |
| pentacles-02 | 2 pentacles joined by a green-and-gold serpent in a figure 8, tail in mouth; a hand holds the centre; no roses; Jupiter / Capricorn | same | ok |
| pentacles-03 | white-winged hand, rose branch, 2 white buds touching and surmounting the top pentacle, equilateral triangle; Mars / Capricorn | same | ok |
| pentacles-04 | branch with no flowers or buds but one white rose in the centre; pentacles on a square; Sun / Capricorn | same | ok |
| pentacles-05 | roses falling, no buds; 5 pentacles; Mercury / Taurus | quincunx | ambiguous (arrangement not given; note) |
| pentacles-06 | white roses and buds each touching a pentacle; 2 columns of 3; Taurus above, Moon below (Book T's order) | same | ok |
| pentacles-07 | 7 as Rubeus; 5 buds overhang, not touching, the 5 uppermost; Saturn / Taurus | 2-1-2-2, 5 buds | ok |
| pentacles-08 | 4 white roses touch the 4 lowest; leaves only the 4 upper; Populus; Sun / Virgo | same | ok |
| pentacles-09 | 9 white roses each touching a pentacle, buds too; figure of nine; Venus / Virgo | 3 rows of 3 | ambiguous (the 1912 figure is not in the transcription; note) |
| pentacles-10 | roses touch all, no buds; rows 2,1,2,2,1,2; Mercury / Virgo | same | ok |

## Keys

Book T gives the Keys meanings only, no picture; each was checked against its letter and attribution
(both right on all 22) and against its own `note`.

| Card | Picture against its note | Verdict |
|---|---|---|
| key-00 Aleph · Air, key-01 Beth · Mercury, key-02 Gimel · Moon, key-03 Daleth · Venus, key-04 Heh · Aries, key-05 Vau · Taurus, key-06 Zain · Gemini, key-07 Cheth · Cancer, key-09 Yod · Virgo, key-10 Kaph · Jupiter, key-08 Lamed · Libra, key-12 Mem · Water, key-13 Nun · Scorpio, key-14 Samekh · Sagittarius, key-15 Ayin · Capricorn, key-16 Peh · Mars, key-17 Tzaddi · Aquarius (8-point star + 7 lesser), key-18 Qoph · Pisces, key-19 Resh · Sun, key-20 Shin · Spirit and Fire, key-21 Tau · Earth and Saturn (four Kerubim) | each shows what its note says | ok |
| key-11 Teth · Leo | note said "a woman who closes the lion's jaws with her hands"; the picture has her hand on the lion's head | **fixed** (note now says what the picture shows: her hand upon its head) |

## Ambiguous, left for PlayfulProcess

1. wands-ace: where the 12 Yods "about the Left-hand branch" go (Book T's sentence is garbled).
2. swords-ace: olive "on the right" drawn on the viewer's right; the six Vaus beside the blade rather than below the point.
3. pentacles-ace: "Four Crosses and two buds" read as four roses and two buds.
4. wands-queen: "steady flames" drawn with the same leaping flames as the Knight's and Princess's.
5. swords-knight: "dark-driving stratus clouds" drawn as a dark cumulus bank.
6. Courts' small details left out: the "sigil of his scale" on the Knights' club/cup/pommel and the Princes' cup, crests on shoulder-pieces and buskins, the Prince of Cups' feather-like armour.
7. cups-10: placement of the top cup and its lotus; Mars moved to the upper left.
8. swords-08: "the pose of the other sword symbols is re-established in the centre" read as the rose.
9. pentacles-05: five pentacles as a quincunx (Book T gives no arrangement).
10. pentacles-09: nine as three rows of three (the 1912 figure is not in the transcription).
11. On several pentacle cards the sign below sits on the hand's cloud and reads small.
12. The Keys as a whole: pictures from the titles and tradition, since Book T gives none.

## Also in this round

The deck grammar's court `metadata.rules` now give Book T's own degree (20°) at both bounds, read
from each card's sentence with `build_book_t_iconography.text_degree()` (reused by
`build_book_t_deck.py`), instead of the Golden Dawn deck's "21°"; the deck's `Correspondences` line
("Rules 20° Scorpio – 20° Sagittarius") follows them, and the `book-t/*.html` pages were regenerated.
