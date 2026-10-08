"""Court de Gébelin's own 1781 text on trumps II-XXI, in this site's English translation.

Source: Antoine Court de Gébelin, "Du Jeu des Tarots", Article I, in *Monde primitif, analysé et
comparé avec le monde moderne*, vol. VIII (Paris, 1781), pp. 367-378. Public domain. Translated
for this site from the archive.org scans `mondeprimitifana08cour` and `b30411956_0008` (OCR
checked against both; the long s read as s). Page numbers are the book's printed pages.

Used once by scripts/archive/anachronism_audit_2026_10_08.py (Oct 8 2026), which replaced the
"Court de Gébelin's Egyptian Reading" sections that had mixed his words with later, invented
text (Ma'at, Ra, the weighing of the heart, the Tower of Babel). The replaced text is in
tarot/_archive/anachronisms-2026-10-08.json.
"""

SCAN = 'https://archive.org/details/mondeprimitifana08cour'


def header(pages):
    return ("[Translated from Court de Gébelin's *Du Jeu des Tarots*, *Monde primitif* vol. VIII "
            "(Paris, 1781), %s. This site's translation; [scan](%s)]" % (pages, SCAN))


KINGS = ("Numbers II and III represent two women; numbers IV and V, their husbands. They are the "
         "temporal and spiritual heads of Society.\n\n"
         "**King and Queen.** Number IV represents the King, and III the Queen. Both have as their "
         "attributes the Eagle on a shield, and the sceptre topped by a globe crowned with a cross, "
         "called Tau, the sign above all others.\n\n"
         "The King is seen in profile, the Queen full face. Both sit on a throne. The Queen wears a "
         "trailing robe, and the back of her throne is high; the King sits as if in a gondola or a "
         "shell-shaped chair, his legs crossed. His crown is a half-circle topped by a pearl with a "
         "cross; the Queen's ends in a point. The King wears the badge of an order of knighthood.")

PRIESTS = ("**High Priest and High Priestess.** Number V represents the Chief of the Hierophants, "
           "or the High Priest; number II, the High Priestess, or his wife: it is known that among "
           "the Egyptians the heads of the priesthood were married. If these cards were the "
           "invention of the Moderns, we would see no High Priestess in them, still less under the "
           "name of Papess, as the German card-makers have absurdly named this one.")

CARDMAKERS = ("The Italian or German card-makers, who brought this game down to what they knew, "
              "made of these two figures, whom the Ancients called Father and Mother (as one would "
              "say Abbot and Abbess, Oriental words meaning the same thing), a Pope and a Papess.")

TEXT = {
    'atout-02': (header('pp. 369-370'), "\n\n".join([
        "Numbers II and III represent two women; numbers IV and V, their husbands. They are the "
        "temporal and spiritual heads of Society.",
        PRIESTS,
        "The High Priestess sits in an armchair. She wears a long robe, with a kind of veil behind "
        "her head that comes to cross over her breast. She has a double crown with two horns, as "
        "Isis had. She holds an open book on her knees. Two scarves set with crosses cross on her "
        "breast and form an X.",
        CARDMAKERS])),
    'atout-03': (header('pp. 369-370'), KINGS),
    'atout-04': (header('pp. 369-370'), KINGS),
    'atout-05': (header('p. 370'), "\n\n".join([
        PRIESTS,
        "The High Priest wears a long robe with a great mantle held by a clasp. He wears the triple "
        "tiara. With one hand he leans on a sceptre with a triple cross; with the other, two fingers "
        "extended, he gives the blessing to two figures seen at his knees.",
        CARDMAKERS,
        "As for the sceptre with the triple cross, it is an entirely Egyptian monument: it is seen "
        "on the Table of Isis, under the letter TT, a precious monument which we have already had "
        "engraved in full, to give to the Public one day. It relates to the triple Phallus that was "
        "carried in procession in the famous Feast of the Pamylia, where people rejoiced at having "
        "found Osiris again, and where it was the symbol of the regeneration of plants and of the "
        "whole of Nature."])),
    'atout-06': (header('p. 371'), "\n\n".join([
        "**No. VI. Marriage.** A young man and a young woman pledge their faith to each other; a "
        "Priest blesses them; Love pierces them with his arrows. The card-makers call this picture "
        "the Lover. They look very much as if they added this Love, with his bow and arrows, "
        "themselves, to make the picture speak more plainly to their eyes.",
        "In the *Antiquities* of Boissard one sees a monument of the same kind, picturing conjugal "
        "union; but it has only three figures: the lover and the beloved, who pledge their faith, "
        "and Love between them, who serves as witness and priest.",
        "This picture is titled *Fidei Simulacrum*, picture of conjugal faith; its figures are "
        "named by these fine names: Truth, Honour and Love. [The essay goes on to read the names "
        "and the monument's dedication.]"])),
    'atout-07': (header('pp. 370-371'),
        "**No. VII. Osiris Triumphant.** Osiris comes next. He appears in the form of a triumphant "
        "King, sceptre in hand, crown on his head. He is in his warrior's chariot, drawn by two "
        "white horses. No one is unaware that Osiris was the great Divinity of the Egyptians, the "
        "same as that of all the Sabaean peoples: the Sun, physical symbol of the invisible supreme "
        "Divinity, who shows himself in this masterpiece of Nature. He had been lost during the "
        "winter; he reappears in the spring with new brilliance, having triumphed over everything "
        "that made war on him."),
    'atout-08': (header('pp. 371-372'), "\n\n".join([
        "**The four Cardinal Virtues.** The figures we have gathered on this plate relate to the "
        "four Cardinal Virtues.",
        "**No. VIII. Justice.** She is a Queen; she is Astraea seated on her throne, holding in one "
        "hand a dagger, in the other a balance.",
        "*Court de Gébelin names Astraea, the star-maiden of Greek myth. He names no Egyptian "
        "goddess for this card; Ma'at's name could not be read until after Champollion's "
        "decipherment of the hieroglyphs in 1822.*"])),
    'atout-09': (header('pp. 372-373'), "\n\n".join([
        "**No. VIIII or IX. The Sage, or the Seeker of Truth and Justice.** Number IX represents a "
        "venerable Philosopher in a long mantle, a hood on his shoulders. He walks bent over his "
        "staff, holding a lantern in his left hand. He is the Sage who seeks Justice and Virtue.",
        "From this Egyptian painting, then, someone imagined the story of Diogenes, who, lantern in "
        "hand, looks for a man at midday. Witticisms, epigrams above all, belong to every age; and "
        "Diogenes was the man to put this picture into action.",
        "The card-makers have made this Sage a Hermit. That is seen well enough: philosophers "
        "willingly live in retreat, or are hardly suited to the frivolity of their age. Heraclide "
        "passed for mad in the eyes of his dear fellow citizens. In the East, besides, to give "
        "oneself to the speculative sciences and to become a hermit are almost one and the same "
        "thing. The Egyptian hermits had nothing to reproach, in this respect, to those of the "
        "Indies and to the Talapoins of Siam: they were, or are, all so many Druids."])),
    'atout-10': (header('p. 377'),
        "**No. X. The Wheel of Fortune.** The last number on this plate is the Wheel of Fortune. "
        "Here human figures, in the form of monkeys, dogs, rabbits and so on, rise in turn on this "
        "wheel to which they are tied: one would say it is a satire against Fortune, and against "
        "those whom she raises quickly and lets fall again just as quickly."),
    'atout-11': (header('pp. 371-372'), "\n\n".join([
        "**The four Cardinal Virtues.** The figures we have gathered on this plate relate to the "
        "four Cardinal Virtues.",
        "**No. XI.** This one represents Strength. She is a woman who has made herself mistress of "
        "a lion, and who opens its jaws as easily as she would open those of her little spaniel. "
        "She wears a shepherdess's hat on her head."])),
    'atout-12': (header('p. 372'), "\n\n".join([
        "**No. XII. Prudence** is one of the four Cardinal Virtues: could the Egyptians have "
        "forgotten her in this painting of Human Life? Yet she is not found in this game. In her "
        "place, under No. XII, between Strength and Temperance, one sees a man hanging by the feet. "
        "But what is this hanged man doing there? It is the work of an unlucky, presumptuous "
        "card-maker who, not understanding the beauty of the allegory hidden under this picture, "
        "took it upon himself to correct it, and thereby disfigured it entirely.",
        "Prudence could only be shown in a way the eye could grasp by a man standing, who, having "
        "one foot set down, advances the other and holds it suspended, examining the place where "
        "he can set it safely. The title of this card was therefore *the man with the suspended "
        "foot*, *pede suspenso*; the card-maker, not knowing what that meant, made of it a man "
        "hanged by the feet.",
        "Then people asked: why a hanged man in this game? And they did not fail to say: it is the "
        "just punishment of the inventor of the game, for having pictured a Papess in it.",
        "But placed between Strength, Temperance and Justice, who does not see that it is Prudence "
        "that was meant, and that was shown in the beginning?"])),
    'atout-13': (header('p. 375'), "\n\n".join([
        "**No. XIII. Death.** Number XIII represents Death: she mows down humans, kings and queens, "
        "the great and the small; nothing resists her murderous scythe.",
        "It is not surprising that she is placed under this number; the number thirteen was always "
        "regarded as unlucky. Some great misfortune must have happened very anciently on such a "
        "day, and its memory must have weighed on all the ancient Nations. Could it be in "
        "consequence of this memory that the thirteen Tribes of the Hebrews were only ever counted "
        "as twelve?",
        "Let us add that it is not surprising either that the Egyptians put Death into a game that "
        "should awaken only pleasant ideas: this game was a game of war, so Death had to enter it. "
        "So the game of chess ends with checkmate, or better, *Shah mat*, the death of the King.",
        "Besides, we have had occasion to recall, in the Calendar, that at their feasts this wise "
        "and thoughtful People brought out a skeleton under the name of Maneros, no doubt to urge "
        "the guests not to kill themselves with gluttony. Everyone has his own way of seeing; there "
        "is no disputing tastes."])),
    'atout-14': (header('p. 372'), "\n\n".join([
        "**The four Cardinal Virtues.** The figures we have gathered on this plate relate to the "
        "four Cardinal Virtues.",
        "**No. XIIII. Temperance.** She is a winged woman who pours water from one vase into "
        "another, to temper the liquor it holds. [The book prints this number as XIII.]"])),
    'atout-15': (header('p. 376'),
        "**No. XV. Typhon.** Number XV represents a famous Egyptian figure, Typhon, brother of "
        "Osiris and of Isis, the evil Principle, the great Demon of Hell. He has bat's wings, and "
        "the feet and hands of a harpy; on his head, ugly stag's horns: he has been made as ugly "
        "and as devilish as could be. At his feet are two little devils with long ears and great "
        "tails, their hands tied behind their backs. They are themselves bound by a cord that "
        "passes round their necks and is fixed to Typhon's pedestal: for he does not let go of "
        "those who are his; he loves those who are his own."),
    'atout-16': (header('pp. 376-377'), "\n\n".join([
        "**No. XVI. House of God, or Castle of Plutus.** This time we have here a lesson against "
        "avarice. This picture represents a Tower called the House of God, that is, the House above "
        "all others. It is a Tower full of gold; it is the Castle of Plutus. It is falling into "
        "ruins, and its worshippers fall crushed beneath its rubble.",
        "From all this together, can one fail to recognise the story of the Egyptian Prince of whom "
        "Herodotus speaks, and whom he calls Rhampsinitus? Having had a great stone Tower built to "
        "shut away his treasures, of which he alone had the key, he nevertheless saw them shrink "
        "before his eyes, though no one passed in any way through the single door the building "
        "had. To discover such skilful thieves, this Prince set traps around the vessels that held "
        "his riches. The thieves were the two sons of the Architect Rhampsinitus had employed: he "
        "had arranged a stone so that it could be taken out and put back at will without anyone "
        "noticing. He taught his secret to his children, who made wonderful use of it, as one sees. "
        "They robbed the Prince, and then they threw themselves down from the Tower: that is how "
        "they are shown here. [The essay goes on to retell the rest of Herodotus's tale.]"])),
    'atout-17': (header('pp. 374-375'), "\n\n".join([
        "**No. XVII. The Dog Star.** Here we have before our eyes a picture no less allegorical, "
        "and wholly Egyptian; it is titled the Star. One sees in it, in fact, a brilliant Star, "
        "around which are seven smaller ones. The bottom of the picture is taken up by a woman "
        "leaning on one knee, who holds two upturned vases from which two rivers flow. Beside this "
        "woman is a butterfly on a flower.",
        "It is pure Egyptianism.",
        "This Star above all others is the Dog Star, or Sirius: the star that rises when the Sun "
        "leaves the sign of Cancer, with which the preceding picture ends, and which this Star "
        "follows here immediately.",
        "The seven stars around it, which seem to pay it court, are the Planets: it is in some way "
        "their Queen, since it fixes at that moment the beginning of the year; they seem to come "
        "to receive its orders, to rule their courses by it.",
        "The Lady below, very intent at this moment on pouring out the water of her vases, is the "
        "Sovereign of the Heavens, ISIS, to whose bounty the floods of the Nile were attributed, "
        "which begin at the rising of the Dog Star; so this rising was the announcement of the "
        "flood. It is for this reason that the Dog Star was consecrated to Isis, that it was her "
        "symbol above all others.",
        "And as the year likewise opened with the rising of this Star, it was called Soth-is, "
        "opening of the year; and it is under this name that it was consecrated to Isis.",
        "Finally, the Flower and the Butterfly it bears were the emblem of regeneration and "
        "resurrection: they showed at the same time that, by the favour of Isis, at the rising of "
        "the Dog Star, the fields of Egypt, which were entirely bare, would be covered with new "
        "harvests."])),
    'atout-18': (header('pp. 373-374'), "\n\n".join([
        "**No. XVIII. The Moon.** So the Moon, which walks in the Sun's train, is also accompanied "
        "by tears of gold and pearls, to mark likewise that she contributes her part to the goods "
        "of the earth.",
        "Pausanias tells us, in his Description of Phocis, that according to the Egyptians it was "
        "the Tears of Isis that swelled the waters of the Nile each year and so made the fields of "
        "Egypt fertile. Accounts of that country also speak of a drop, or tear, that falls from "
        "the Moon at the moment the waters of the Nile are about to rise.",
        "At the bottom of this picture one sees a Crayfish, or Cancer, either to mark the Moon's "
        "retrograde course, or to show that it is at the moment when the Sun and the Moon leave "
        "the sign of Cancer that the flood arrives, caused by their tears at the rising of the Dog "
        "Star, which is seen in the following picture.",
        "One could even join the two motives: is it not very ordinary to be decided by a crowd of "
        "reasons forming a mass one would often be hard put to untangle?",
        "The middle of the picture is taken up by two Towers, one at each end, to mark the two "
        "famous Pillars of Hercules, beyond and short of which these two great lights never passed.",
        "Between the two pillars are two Dogs that seem to bark at the Moon and to guard her: "
        "perfectly Egyptian ideas. This People, unique for allegories, compared the Tropics to two "
        "Palaces each guarded by a dog, which, like faithful doorkeepers, held these Stars in the "
        "middle of the Heavens without letting them slip toward one Pole or the other.",
        "These are not the visions of commentators. Clement, himself an Egyptian since he was of "
        "Alexandria, and who should therefore have known something of it, assures us in his "
        "*Stromata* (Book V) that the Egyptians represented the Tropics in the figure of two Dogs, "
        "which, like doorkeepers or faithful guardians, kept the Sun and the Moon from going "
        "further and reaching the Poles."])),
    'atout-19': (header('p. 373'), "\n\n".join([
        "**No. XIX. The Sun.** We have gathered on this plate all the pictures that relate to "
        "light: so after the Hermit's dark lantern, we shall review the Sun, the Moon, and "
        "brilliant Sirius, the sparkling Dog Star, all of which appear in this game with various "
        "emblems.",
        "The Sun is shown here as the physical Father of Humans and of the whole of Nature: he "
        "gives light to men living in Society, he presides over their Cities; from his rays drip "
        "tears of gold and of pearls: so the happy influences of this star were signified.",
        "This game of Tarots is here perfectly in keeping with the doctrine of the Egyptians, as "
        "we shall see in more detail in the following article."])),
    'atout-20': (header('pp. 377-378'), "\n\n".join([
        "**No. XX. Picture wrongly named the Last Judgement.** This picture shows an Angel "
        "sounding the trumpet: at once one sees, as if coming out of the earth, an old man, a "
        "woman, a child, naked.",
        "The card-makers, who had lost the value of these pictures, and still more their order, saw "
        "here the Last Judgement; and to make it plainer they put in something like tombs. Take "
        "away these tombs, and the picture serves just as well to show the Creation, which came "
        "about in Time, at the beginning of Time, which No. XXI shows."])),
    'atout-21': (header('pp. 367, 378'), "\n\n".join([
        "**No. XXI. Time, wrongly named the World.** This picture, which the card-makers called "
        "the World because they regarded it as the origin of everything, represents Time. One "
        "cannot fail to recognise it from the whole.",
        "In the centre is the Goddess of Time, with her floating veil, which serves her as a belt, "
        "or Peplum, as the Ancients called it. She is in the attitude of running, like Time, and in "
        "a circle which represents the revolutions of Time, as well as the egg from which "
        "everything came out in Time.",
        "In the four corners of the picture are the emblems of the four Seasons, which make the "
        "revolutions of the year, the same that composed the four heads of the Cherubim. These "
        "emblems are the Eagle, the Lion, the Ox and the Young Man. The Eagle represents Spring, "
        "when the birds return; the Lion, Summer, or the heats of the Sun; the Ox, Autumn, when "
        "one ploughs and sows; the Young Man, Winter, when people gather in society.",
        "**How the reading began (p. 367).** Invited some years ago to visit a Lady among our "
        "friends, Madame la C. d'H., who had arrived from Germany or Switzerland, we found her busy playing this game "
        "with some other persons. *We are playing a game you surely do not know... That may be; "
        "what is it?... The game of Tarots... I had occasion to see it when very young, but I have "
        "no idea of it... It is a rhapsody of the most bizarre, the most extravagant figures: here "
        "is one, for example.* Care was taken to choose the one most loaded with figures, and "
        "having no relation to its name: it is the World. I cast my eyes on it, and at once I "
        "recognise its Allegory."])),
}

SYMBOL = {
    'atout-00': "Court de Gébelin calls the Fool Zero: it counts for nothing alone and gives value to the other cards. He names no god for it; his Typhon is trump XV.",
    'atout-01': "Court de Gébelin's Cup-and-Ball Player, placed at the head of all the estates of life: life as a dream and a sleight of hand.",
    'atout-02': "Court de Gébelin's High Priestess, wife of the High Priest (V). He likens her horned crown to Isis's but does not call her Isis.",
    'atout-03': "Court de Gébelin's Queen, one of the four heads of society (II-V), with the eagle shield and the tau-sceptre. He gives her no Egyptian goddess.",
    'atout-04': "Court de Gébelin's King, the Queen's husband and a temporal head of society. He does not call him Osiris; his Osiris is the Chariot (VII).",
    'atout-05': "Court de Gébelin's Chief of the Hierophants, the High Priest. He reads the triple-cross sceptre as Egyptian, after the Table of Isis.",
    'atout-06': "Court de Gébelin calls this card Marriage: a couple pledging faith, blessed by a priest. He thought the card-makers had added the Cupid.",
    'atout-07': "Court de Gébelin's Osiris Triumphant: the Sun, lost in winter, returning in spring after triumphing over all that made war on him.",
    'atout-08': "Court de Gébelin's Justice is Astraea, a queen on her throne with a dagger and a balance, one of four Cardinal Virtues. He names no Egyptian goddess for her.",
    'atout-09': "Court de Gébelin's Sage, the seeker of truth and justice with his lantern. He took the story of Diogenes to come from this picture.",
    'atout-10': "Court de Gébelin read the Wheel as a satire on Fortune: human figures shaped as monkeys, dogs and rabbits, raised and dropped in turn.",
    'atout-11': "Court de Gébelin's Strength, one of the four Cardinal Virtues: a woman in a shepherdess's hat who opens a lion's jaws as easily as a spaniel's.",
    'atout-12': "Court de Gébelin's Prudence: he held that a card-maker had misdrawn a man stepping forward with one foot raised (pede suspenso) as a man hanged by the feet.",
    'atout-13': "Court de Gébelin's Death, mowing down kings and commoners under the unlucky number thirteen. He compares the skeleton the Egyptians showed at their feasts.",
    'atout-14': "Court de Gébelin's Temperance, one of the four Cardinal Virtues: a winged woman pouring water from one vase into another to temper the liquor.",
    'atout-15': "Court de Gébelin's Typhon, brother of Osiris and Isis, the evil principle, holding two little devils by a cord.",
    'atout-16': "Court de Gébelin's Castle of Plutus: a tower full of gold falling on its worshippers, a lesson against avarice, after Herodotus's tale of King Rhampsinitus.",
    'atout-18': "Court de Gébelin's Moon: tears of Isis swelling the Nile, the crayfish as the sign of Cancer, the towers as the Pillars of Hercules, the dogs as the guardians of the Tropics.",
    'atout-19': "Court de Gébelin's Sun, the physical Father of humans and of all Nature, shedding tears of gold and pearls.",
    'atout-20': "Court de Gébelin read this card as the Creation, wrongly named the Last Judgement; he thought the card-makers had added the tombs.",
    'atout-21': "Court de Gébelin's Time, wrongly named the World: the goddess of Time in a circle, the four corner figures as the four seasons. This was the card that started his Egyptian reading.",
}

RESEARCH_ADD = {
    'atout-01': "Checked against the 1781 text (Oct 8 2026): Court de Gébelin lists dice, cups, knives and balls on the table and makes none of them element-symbols (p. 369).",
    'atout-02': "Checked against the 1781 text (Oct 8 2026): Court de Gébelin calls her the High Priestess, wife of the High Priest; he likens her horned crown to Isis's but does not call her a goddess (p. 370).",
    'atout-03': "Checked against the 1781 text (Oct 8 2026): III is simply the Queen, wife of the King (IV); no Osiris is named here (p. 369).",
    'atout-04': "Checked against the 1781 text (Oct 8 2026): IV is the King. Court de Gébelin's Osiris is VII, the Chariot (pp. 369-370).",
    'atout-07': "Checked against the 1781 text (Oct 8 2026): the essay does title VII \"Osiris triomphant\" (p. 370).",
    'atout-21': "Checked against the 1781 text (Oct 8 2026): Court de Gébelin calls XXI Time; Isis and \"the Universe\" are the Comte de Mellet's reading in the same volume (p. 396).",
}
