# Book T deck: one prompt per card

Written Oct 10 2026 for PlayfulProcess's public deck [Book T: The Golden Dawn's 78 Cards](https://recursive.eco/g/2000ad96-70c6-4aa4-a6fb-c22cce5e9cc7). Each card below quotes Book T's own passage (*The Equinox* I(8), 1912, public domain), then the prompt written from it, then what came back.

## How the pictures were made

1. **Prompt from the text.** One prompt per card, written from Book T's passage for that card. Every prompt starts with the same style line, so the 78 read as one deck.
2. **Paint.** recursive.eco MCP `generate_node_image`, provider `gemini` (it ran `gemini-2.5-flash-image`), 1024x1536 asked (832x1248 returned), no reference image, `verify: true` (a vision check of the picture against the prompt; report only). $0.15 a painting.
3. **Curate.** Contact sheets by suit. Sixteen cards were re-run once (a wrong figure, a missing symbol, a wrong count, painted marks); the first prompt is kept below each of them. Two painted marks were cut off instead (a strip of pseudo-glyphs on the Queen of Wands, the words LORD OF SORROW on the Three of Swords).
4. **Trace.** The painting is cut inside the cream border the model kept drawing (detected per card), resized to 560 px wide and traced to line art + flat fills (`from-gemini/src/lib.py`, the "line art + fills" direction). The title and Book T's name for the card are real SVG text in a caption band under the picture. Every SVG is under 1 MB.
5. **Attach.** The SVG is the card's `image_url`; the painting is the second entry of `metadata.illustrations` (the SVG is the first, `is_primary`), each with its credit and licence.

**The shared style line** (first words of every prompt):

> Hand-painted esoteric card picture in the manner of a Golden Dawn adept's own hand-coloured tarot of the 1890s: gouache on paper, flat areas of strong saturated colour, bold dark ink outlines, no photographic shading, a simple symbolic ground. A full-bleed portrait painting that runs to all four edges: a pure picture, free of any border, frame, banner, letters or numbers.

**Left out on purpose, everywhere:** painted titles and numbers (the caption is real text); for the small cards, the planet and sign Book T sets above and below (image models garble astrological glyphs, so the decan is in the caption: *Five of Wands · Saturn in Leo*); Hebrew letters.

**The Keys:** Book T describes no picture for the twenty-two Keys, only a title, an attribution and a meaning. Their prompts are built from the title's own words ("the dweller between the Waters") and the 1912 card name; the rest is the traditional figure that name implies. These are the least Book-T-bound pictures in the deck.

**The four pilot cards** (Queen of Cups, Knight of Swords, Prince of Pentacles, Princess of Wands) come from the private pilot grammar `3d4838f3` (Oct 8): its chosen paintings, re-traced here with this deck's captions. Their prompts and image trials stay in the pilot grammar's metadata.

**Licence.** The deck is CC BY-SA 4.0. The paintings are AI-generated from public-domain text; PlayfulProcess's images here are offered under the deck's CC BY-SA 4.0 (the pilot had marked its four "all rights reserved for now"; in this public deck they carry the deck's licence).

## Redo first

- **Lord of Harmonious Change** (`pentacles-02`): 1st (tied): Book T's single serpent in a figure eight is this card's whole symbol.
- **Root of the Powers of Earth** (`pentacles-ace`): 1st: this Ace is the pattern for every pentacle in the suit.
- **Lord of the Forces of Life** (`key-10-wheel-of-fate`): 2nd: the sphinx is the card's key figure.
- **Spirit of the Mighty Waters** (`key-12-hanged-man`): 3rd: the posture is the card.
- **Queen of the Thrones of Earth** (`pentacles-queen`): 4th: the crest and the split face are Book T's own marks for this card.
- **Lord of Shortened Force** (`swords-08`): 5th, swords 4 to 10 as a set: every one gives each hand one sword. A reference image of the right layout (or a drawn layout) would help more than another prompt.
- **Lord of Material Happiness** (`cups-09`): 6th, with cups-07, cups-08, cups-10: the counts.

The other notes under each card are smaller misses (a count off by one or two, a crest in the wrong place).

## The twenty-two Keys

### Spirit of Αἰθήρ (The Foolish Man)

**Book T (1912):**

> IF the question refers to spiritual matters, the Fool means idea, thought, spirituality, that which endeavours to transcend Earth. But if question is material, it means folly, stupidity, eccentricity, or even mania.

**Prompt of the kept painting** (after the style line):

> The Foolish Man, the Spirit of the Aether: a young bearded man with short brown hair, in a short tunic of many pale colours and a feathered cap, strides joyfully off the edge of a high grey cliff into open luminous air, arms spread wide, face lifted to the sky. A golden radiance of aether surrounds him; the earth falls away far below. Pale yellow and sky-blue air fills most of the picture. Spirit and thought reaching beyond the earth.

**First prompt** (its painting was re-run once):

> The Spirit of the Aether: a youthful man in a light tunic of many pale colours strides joyfully off a high grey cliff into open luminous air, arms spread, face lifted to the sky, his hair and garments blown upward. A golden radiance of aether surrounds him; the earth falls away far below. Pale yellow and sky-blue air fills most of the picture. A mood of thought and spirit reaching beyond the earth.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650836504-7c4fhshb1qa.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654114949-jjsvjgyhtvs.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650042031-0mo940p5wfa.png)

**Check:** Re-run once: the first painting read as a young woman. Pale palette, lighter than the rest of the deck.

### Magus of Power (The Magician)

**Book T (1912):**

> Skill, wisdom, adaptation, craft, cunning, or occult wisdom or power.

**Prompt of the kept painting** (after the style line):

> The Magus of Power: a young magician in a yellow robe stands behind a stone altar-table. His right hand raises a short white wand toward the sky; his left hand points down to the earth. On the table lie the four elemental weapons side by side: a wooden wand, a golden cup, a short steel sword and a golden disc. Small wings on his sandals, the sign of Mercury. Clear morning light, skill and craft.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650076345-9t0qma9h6x.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654118134-dkqa091n6ob.svg)

### Priestess of the Silver Star (The High Priestess)

**Book T (1912):**

> Change, alternation, increase and decrease, fluctuation; whether for good or evil depends on the dignity.

**Prompt of the kept painting** (after the style line):

> The Priestess of the Silver Star: a calm veiled priestess in pale blue and silver robes sits enthroned between two pillars, one black and one white. A silver crescent moon rests on her brow, and above her head shines a large silver eight-pointed star. Behind her, a silver sea whose tide rises and falls. She holds a closed scroll on her lap. Cool silver-blue light of the Moon.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650099417-l2n1owcee8l.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654120271-vk8b9qedtyr.svg)

### Daughter of the Mighty Ones (The Empress)

**Book T (1912):**

> Beauty, happiness, pleasure, success. But with very bad dignity it means luxury, dissipation.

**Prompt of the kept painting** (after the style line):

> The Daughter of the Mighty Ones: a beautiful crowned young woman sits enthroned in a blossoming green garden, in a flowing green and rose-coloured gown, a crown of stars on her head. In one hand a golden sceptre topped by an orb; on her other hand a white dove rests. Red and white roses bloom around her, a stream flows behind. Warm, happy, Venusian light.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650123348-hfje0wg43xu.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654123375-3uttg8872w4.svg)

**Check:** A jewelled crown with stars as a halo above it, not a crown of stars.

### Son of the Morning, chief among the Mighty (The Emperor)

**Book T (1912):**

> War, conquest, victory, strife, ambition.

**Prompt of the kept painting** (after the style line):

> Son of the Morning, chief among the Mighty: a crowned emperor in red armour and a red mantle sits on a square stone throne carved with rams' heads, against a red dawn sky with the rising sun behind him. In his right hand a sceptre topped by a ram's head; in his left a golden orb. Stern, ambitious face, a grey beard. Barren red mountains behind. War, conquest and rule.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650149444-4yysczfva6i.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654125856-7ycapfjbtkx.svg)

### Magus of the Eternal (The Hierophant)

**Book T (1912):**

> Divine wisdom, manifestation, explanation, teaching, occult force voluntarily invoked.

**Prompt of the kept painting** (after the style line):

> The Magus of the Eternal: a venerable bearded high priest in red and white robes and a triple crown sits on a throne between two grey pillars; his right hand is raised in blessing, his left holds a tall triple-barred cross staff. A white bull lies at the foot of the throne. Two small tonsured listeners kneel before him. Deep green and gold; teaching and divine wisdom.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650170176-zrwxpmvb77.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654128628-c9hbezysvq6.svg)

**Check:** One tiered crown rather than a triple crown.

### Children of the Voice; the Oracles of the Mighty Gods (The Lovers)

**Book T (1912):**

> Inspiration (passive, mediumistic), motive power, action.

**Prompt of the kept painting** (after the style line):

> The Children of the Voice; the Oracles of the Mighty Gods: on the left a young bearded man with short dark hair in a red tunic, on the right a young woman with long golden hair in a blue gown. They stand side by side in a green spring meadow, holding hands, faces lifted, listening. Above them, from a radiant golden cloud, a great beam of light pours down on their heads like a voice from heaven. Inspiration received, passive and listening.

**First prompt** (its painting was re-run once):

> The Children of the Voice; the Oracles of the Mighty Gods: a young man and a young woman stand side by side in a green spring meadow, holding hands, their faces lifted, listening. Above them, from a radiant golden cloud, a great beam of light pours down on their heads like a voice from heaven. They are twins in bearing, alike and paired. Inspiration received, passive and listening.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650864645-yo47lsmqup.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654131503-wycaevw1w5.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650195539-qjzthc02oe.png)

**Check:** Re-run once: the first painting showed two women.

### Child of the Powers of the Waters; the Lord of the Triumph of Light (The Chariot)

**Book T (1912):**

> Triumph, victory, health (sometimes unstable).

**Prompt of the kept painting** (after the style line):

> The Child of the Powers of the Waters; the Lord of the Triumph of Light: a crowned charioteer in silver-blue armour stands in a square chariot rising out of the sea waves, drawn by two white horses splashing through shallow water. A crab emblem is on his breastplate. He holds a sceptre topped by a crescent. A great golden light breaks through the clouds behind him. Triumph and victory.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650249106-79x7qxiv6gt.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654172878-is9bjuk6ji.svg)

### Daughter of the Flaming Sword (Fortitude)

**Book T (1912):**

> Courage, strength, fortitude, power passing on to action. Obstinacy.

**Prompt of the kept painting** (after the style line):

> The Daughter of the Flaming Sword: a calm, strong young woman in a white gown with a garland of flowers gently holds open the jaws of a great golden lion beside her, without effort. Above her head a flaming sword hangs point upward, wreathed in fire. Golden-yellow sky, green ground. Courage and strength passing into action.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650273106-4cuhdpuzdv3.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654175526-rqiwwmu2iw.svg)

**Check:** Her hands rest on the lion's mane; the jaws are closed.

### Magus of the Voice of Power, the Prophet of the Eternal (The Hermit)

**Book T (1912):**

> Wisdom from on high. Active divine inspiration. Sometimes "unexpected current."

**Prompt of the kept painting** (after the style line):

> The Magus of the Voice of Power, the Prophet of the Eternal: an old bearded prophet in a long grey hooded cloak stands on a dark mountain path at night, leaning on a tall staff. In his raised right hand he holds a lantern in which a six-pointed star of light shines. A single ray of light falls from the dark heavens onto the lantern. Wisdom from on high.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650296356-yeluvl98crr.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654177404-zp7odpfd2gl.svg)

### Lord of the Forces of Life (The Wheel of Fate)

**Book T (1912):**

> Good fortune, happiness (within bounds). Intoxication of success.

**Prompt of the kept painting** (after the style line):

> The Lord of the Forces of Life: a great golden eight-spoked wheel turns in a deep blue sky among clouds. A blue sphinx with a sword sits calmly on the top of the wheel. On the right a jackal-headed figure rises with the wheel; on the left a serpent descends with it. Rich royal blue and purple and gold of Jupiter. Good fortune and turning fate.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650317027-p3o5e2cfc8.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654180131-9pectoja3l9.svg)

**Check:** The figure on top of the wheel reads as a dark winged bird more than a sphinx; the rising jackal-headed figure is cut by the right edge.

**Redo:** 2nd: the sphinx is the card's key figure.

### Daughter of the Lords of Truth: the Ruler of the Balance (Justice)

**Book T (1912):**

> Eternal justice. Strength and force, but arrested as in act of judgment. May mean law, trial, etc.

**Prompt of the kept painting** (after the style line):

> The Daughter of the Lords of Truth: the Ruler of the Balance: a crowned woman in green robes sits upright on a stone throne between two pillars, perfectly still. In her right hand she holds an upright sword; in her left a golden pair of scales, its two pans exactly level. Her gaze is direct and calm, force arrested in the act of judgment. Emerald green and blue.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650339666-6m1amjg4bgj.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654182521-hpkx4haqzva.svg)

### Spirit of the Mighty Waters (The Hanged Man)

**Book T (1912):**

> Enforced sacrifice, punishment, loss, fatal and not voluntary, suffering.

**Prompt of the kept painting** (after the style line):

> The Spirit of the Mighty Waters: a young man hangs upside down by one foot from a crossbeam of living green wood between two trees, over deep blue water. His free leg is bent behind the other to form a cross; his arms are bound behind his back. His face is calm, a faint glow around his head. The deep waters fill the bottom of the picture. Sacrifice and suspension.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650360010-sr5tzmrja6.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654185112-gn0k24yj4s9.svg)

**Check:** Hangs by both feet with the arms bound in front; the crossed-leg posture is missing.

**Redo:** 3rd: the posture is the card.

### Child of the Great Transformers: the Lord of the Gates of Death (Death)

**Book T (1912):**

> Time, age, transformation, change involuntary (as opposed to 18, Pisces). Or death, destruction (only latter with special cards). [Specially, a sudden and quite unexpected change.]

**Prompt of the kept painting** (after the style line):

> The Child of the Great Transformers: the Lord of the Gates of Death: a skeleton swings a great scythe across dark ground before a tall stone gate. Where the scythe passes, new green shoots spring from the cut earth. A scorpion crawls at its feet and an eagle flies above. Dusky violet and dark green. Transformation and change that will not be refused.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650381558-ej2rhza22wq.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654187448-qh3fid54y1e.svg)

### Daughter of the Reconcilers: the Bringer-Forth of life (Temperance)

**Book T (1912):**

> Combination of forces, realization, action (material effect, good or evil).

**Prompt of the kept painting** (after the style line):

> The Daughter of the Reconcilers: the Bringer-Forth of Life: a winged angelic woman in a white robe stands with one foot on land and one foot in a stream. She pours a shining stream from a golden vessel into a silver vessel. Above her head a rainbow arches, and an arrow points upward through it. Soft blue sky. Combination and reconciliation of forces.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650432640-f6ujp6qkwwl.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654189783-2j6dg0kdlvj.svg)

**Check:** Pours from both vessels downward, not from one into the other; both feet on land.

### Lord of the Gates of Matter: the Child of the Forces of Time (The Devil)

**Book T (1912):**

> Materiality, material force, material temptation, obsession.

**Prompt of the kept painting** (after the style line):

> The Lord of the Gates of Matter: the Child of the Forces of Time: a horned, goat-headed figure with dark bat wings sits on a square black stone pedestal, one hand raised, the other holding a torch pointing downward. Two small horned human figures stand chained to the pedestal by loose rings at their necks. Dark indigo and black ground, a dull red glow. Material force and temptation.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650460506-a39t2cu4k6d.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654191951-505in95w0u9.svg)

**Check:** The torch points up, not down.

### Lord of the Hosts of the Mighty (The Blasted Tower)

**Book T (1912):**

> Ambition, fighting, war, courage, or destruction, danger, fall, ruin.

**Prompt of the kept painting** (after the style line):

> The Lord of the Hosts of the Mighty: a tall grey stone tower on a rocky peak is struck by a jagged bolt of lightning from a dark red sky; its crowned top is blasted off and flames burst from its windows. Two figures, one crowned, fall headlong from it. Sparks of fire fall like drops. Red and black: war, ruin and the fall of ambition.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650486056-2p72bhf224f.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654195076-b6p4xmgg22h.svg)

### Daughter of the Firmament, the dweller between the Waters (The Star)

**Book T (1912):**

> Hope, faith, unexpected help. Or dreaminess, deceived hope, etc.

**Prompt of the kept painting** (after the style line):

> The Daughter of the Firmament, the dweller between the Waters: a young woman with long flowing hair, in a simple sleeveless pale-blue shift, kneels on one knee at the edge of a still blue pool, half on the land and half at the water. From a golden vessel in her right hand she pours a stream into the pool; from a silver vessel in her left hand she pours a stream onto the green earth. Above her, in a deep blue night sky, shines one great radiant eight-pointed star, with seven smaller eight-pointed stars around it. A small bird sits on a tree at the side. Calm, hopeful mood.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791649700154-qwkvwo63k69.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653649257-vje2q4uvcn.svg)

### Ruler of Flux and Reflux: the Child of the Sons of the Mighty (The Moon)

**Book T (1912):**

> Dissatisfaction, voluntary change. Error, lying, falsity, deception. This card is very sensitive to dignity.

**Prompt of the kept painting** (after the style line):

> The Ruler of Flux and Reflux: the Child of the Sons of the Mighty: a large pale moon with a quiet face hangs in a dark blue night sky, shedding drops of dew. Below, a winding path runs between two grey towers into the distance. Two dogs howl up at the moon on either side of the path, and a red crayfish climbs out of a dark pool in the foreground. Ebb and flow, illusion.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650509913-1cft2sskybb.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654224621-fmnl1ur03tp.svg)

**Check:** The crayfish sits in the pool rather than climbing out.

### Lord of the Fire of the World (The Sun)

**Book T (1912):**

> Glory, gain, riches. With "very" evil cards it means arrogance, display, vanity.

**Prompt of the kept painting** (after the style line):

> The Lord of the Fire of the World: a great golden sun with a calm face blazes in the top of the sky, its rays alternating straight and wavy, with golden drops falling from it. Below, two young children hold hands in a green garden enclosed by a low stone wall. Brilliant gold, orange and green. Glory, gain and warmth.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650529996-xizbvbruo3s.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654226748-mzx33fg0tdm.svg)

### Spirit of the Primal Fire (The Judgment)

**Book T (1912):**

> Final decision, judgment, sentence, determination of a matter without appeal, "on its plane."

**Prompt of the kept painting** (after the style line):

> The Spirit of the Primal Fire: in a sky full of red and gold flames, a great winged angel blows a long golden trumpet downward. Below, three figures rise upward from open stone tombs with their arms raised: a man, a woman and a child. The whole scene is lit by fire. Final judgment and awakening.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650551683-43qcc86phwr.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654229110-qu5kcf55of9.svg)

### Great One of the Night of Time (The Universe)

**Book T (1912):**

> The matter itself. Synthesis, world, kingdom. Usually denotes actual subject of question, and therefore depends entirely on accompanying cards.

**Prompt of the kept painting** (after the style line):

> The Great One of the Night of Time: a dancing woman, lightly veiled by a long scarf, floats within a large oval wreath of green leaves against a deep indigo night sky full of small stars; she holds a short wand in each hand. In the four corners of the picture are the four living creatures in clouds: a man's head, an eagle, a lion and a bull. Dark blue and black of Saturn, green of the earth.

**Left out / changed:** Book T describes no picture for the Keys: only a title, an attribution and a meaning. The prompt is built from the title's own words and the 1912 card name; the rest is the traditional figure the name implies.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650573659-8q4bx2ymq62.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654231861-p5ifjshgc0i.svg)

## The four Aces

### Root of the Powers of Fire (Ace of Wands)

**Book T (1912):**

> A WHITE Radiating Angelic Hand, issuing from clouds, and grasping a heavy club, which has three branches in the colours, and with the sigils, of the scales. The Right-and Left-hand branches end respectively in three Flames, and the Centre one in four Flames: thus yielding Ten: the Number of the Sephiroth. Two-and-twenty leaping Flames, or Yodh, surround it, answering to the Paths; of these, three fall below the Right branch for Aleph, Men, and Shin, seven above the Central branch for the double letters; and between it and that of the Right twelve: six above and six below about the Left-hand branch. The whole is a great and flaming Torch. It symbolizes Force — strength, rush, vigour, energy, and it governs, according to its nature, various works and questions.
>
> It implies Natural, as opposed to Invoked, Force.

**Prompt of the kept painting** (after the style line):

> The Root of the Powers of Fire: a white, radiant angelic hand comes out of clouds and grasps a heavy wooden club with three branches. The right and left branches end in three flames each, the centre branch in four flames. Twenty-two small leaping flame-drops, like little Yods, surround it. The whole is a great and flaming torch. Fiery red and gold against a pale sky.

**Left out / changed:** Book T's placement of the 22 flames (three below the right branch, seven above the centre, twelve about the left) is simplified to 'surround it'.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650958958-kzhu7487aam.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653717359-qljeflz95ah.svg)

**Check:** The club reads as a forked branch; about 20 flame-drops, not 22.

### Root of the Powers of Water (Ace of Cups)

**Book T (1912):**

> A WHITE Radiant Angelic Hand, issuing from clouds, and supporting on the palm thereof a cup, resembling that of the Stolistes.
>
> From it rises a fountain of clear and glistening water: and sprays falling on all sides into clear calm water below, in which grow Lotuses and Water-lilies. The great Letter of the Supernal Mother is traced in the spray of the Fountain.
>
> It symbolizes Fertility — productiveness, beauty, pleasure, happiness, etc.

**Prompt of the kept painting** (after the style line):

> The Root of the Powers of Water: a white, radiant angelic hand comes out of clouds and holds on its open palm a golden cup. From the cup rises a fountain of clear glistening water; its sprays fall on all sides into calm clear water below, in which lotuses and water-lilies grow. Blue and silver water, pale sky.

**Left out / changed:** Book T's 'great Letter of the Supernal Mother' traced in the spray is left out: image models garble Hebrew letters.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791650983447-t7ya7bi4mwq.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653720303-bggx4mn0hws.svg)

### Root of the Powers of Air (Ace of Swords)

**Book T (1912):**

> A WHITE Radiating Angelic Hand, issuing from clouds, and grasping the hilt of a sword, which supports a White Radiant Celestial Crown; from which depend, on the right, the olive branch of Peace; and on the left, the palm branch of suffering.
>
> Six Vaus fall from its point. It symbolizes "Invoked," as contrasted with Natural Force: for it is the Invocation of the Sword. Raised upward, it invokes the Divine crown of Spiritual Brightness, but reversed it is the Invocation of Demonic Force; and becomes a fearfully evil symbol. It represents, therefore, very great power for good or evil, but invoked; and it also represents whirling Force, and strength through trouble. It is the affirmation of Justice upholding Divine Authority; and it may become the Sword of Wrath, Punishment, and Affliction.

**Prompt of the kept painting** (after the style line):

> The Root of the Powers of Air: a white, radiant angelic hand comes out of clouds and grasps the hilt of an upright sword. The sword's point supports a white radiant celestial crown; from the crown hang, on the right, an olive branch, and on the left, a palm branch. Six small golden drops fall from around the point. Pale blue and silver sky.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651003941-64rakrwdnm.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653722934-xwtkqded6s.svg)

### Root of the Powers of Earth (Ace of Pentacles)

**Book T (1912):**

> A WHITE Radiant Angelic Hand, holding a branch of a Rose Tree, whereon is a large Pentacle, formed of Five concentric circles. The Innermost Circle is white, charged with a red Greek Cross. From this White Centre, Twelve Rays, also white, issue: these terminate at the circumference, making the whole something like an Astrological figure of the Heavens.
>
> It is surmounted by a small circle, above which is a large white Maltese Cross, and with two white wings.
>
> Four Crosses and two buds are shewn. The Hand issueth from the Clouds as in the other three cases.
>
> It represents materiality in all senses, good and evil: and is, therefore, in a sense, illusionary: it shows material gain, labour, power, wealth, etc.

**Prompt of the kept painting** (after the style line):

> The Root of the Powers of Earth: a white, radiant angelic hand comes out of clouds holding a branch of a rose tree. On the branch rests a large pentacle made of five concentric circles: the innermost circle is white with a red Greek cross, and twelve white rays run from the centre to the edge, like an astrological chart of the heavens. Above it a small circle, and over that a large white Maltese cross with two white wings. Green and gold.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651031031-jlkquijd8nc.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653725573-jjy9tjdj7pb.svg)

**Check:** The pentacle hangs under the hand rather than on the branch; 8 rays instead of 12; the cross over it is Greek, not Maltese.

**Redo:** 1st: this Ace is the pattern for every pentacle in the suit.

## The sixteen court cards

### Lord of the Flame and Lightning: the King of the Spirits of Fire (Knight of Wands)

**Book T (1912):**

> Note that the Kings are now called Knights, and the Princes are now called Kings. This is unfortunate, and leads to confusion; the Princes may be called Emperors without harm. Remember only that the horsed figures refer to the Yod of Tetragrammaton, the charioted figures to the Vau.
>
> A WINGED Warrior riding upon a black horse with flaming mane and tail: the horse itself is not winged. The rider wears a winged helmet (like the old Scandinavian and Gaulish helmet) with a Rayed Crown, a corslet of scale-mail and buskins of the same, and a flowing scarlet mantle. Above his helmet, upon his curass, and on the shoulder-pieces and buskins, he wears as a crest a winged black horse's head. He grasps a club with flaming ends, somewhat similar to that in the symbol of the Ace of Wands, but not so heavy, and also the sigil of his scale is shown; beneath the rushing feet of his steed are waving flames and fire. He is active — generous — fierce — sudden — impetuous.
>
> If ill dignified, he is evil-minded — cruel — bigoted — brutal. He rules the celestial heavens from above the Twentieth Degree of Scorpio to the First Two Decans of Sagittarius: and this includes a part of the Constellation Hercules. (Hercules is always represented with a Club.)
>
> Fire of Fire
>
> King of the Salamanders.

**Prompt of the kept painting** (after the style line):

> The Lord of the Flame and Lightning: a winged warrior rides a black horse with a flaming mane and tail; the horse has no wings. Large wings grow from the rider's shoulders. He wears a winged helmet in the old Gaulish manner with a golden rayed crown, a corslet of scale-mail, scale-mail buskins and a flowing scarlet mantle. His crest, above the helmet and again on his cuirass and buskins, is a winged black horse's head. His right hand grasps a club with flaming ends. Beneath the rushing hooves are waving flames and fire. Fierce, sudden, impetuous.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651051938-pjfp6kk4wq.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653728954-c993fcz9apg.svg)

**Check:** The winged black horse's head crest is missing from the helmet (a rayed crown sits there).

### Queen of the Thrones of Flame (Queen of Wands)

**Book T (1912):**

> A CROWNED queen with long red-golden hair, seated upon a Throne, with steady flames beneath. She wears a corslet and buskins of scale-mail, which latter her robe discloses. Her arms are almost bare. On cuirass and buskins are leopard's heads winged, and the same symbol surmounteth her crown. At her side is a couchant leopard on which her hands rest. She bears a long wand with a very heavy conical head. The face is beautiful and resolute.
>
> Adaptability, steady force applied to an object, steady rule, great attractive power, power of command, yet liked notwithstanding. Kind and generous when not opposed.
>
> If ill dignified, obstinate, revengeful, domineering, tyrannical, and apt to turn against another without a cause.
>
> She rules the heavens from above the last Decan of Pisces to above the 20 Degree of Aries: including thus a part of Andromeda.
>
> Water of Fire
>
> Queen of the Salamanders.

**Prompt of the kept painting** (after the style line):

> The Queen of the Thrones of Flame: a crowned queen with long red-golden hair sits frontally on a throne, with steady flames beneath it. She wears a corslet and buskins of golden scale-mail which her red robe discloses; her arms are almost bare. A winged leopard's head is on her cuirass and on each buskin, and the same winged leopard's head tops her crown. At her side a leopard lies couchant and her hand rests on it. Her other hand holds a long wand with a very heavy conical head. Her face is beautiful and resolute.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651073337-7ubkvuiawtp.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653731130-i6y7tz96mhh.svg)

**Check:** A band of pseudo-glyphs along the bottom of the painting was trimmed off before tracing.

### Prince of the Chariot of Fire (King of Wands)

**Book T (1912):**

> A KINGLY Figure with a golden, winged crown, seated on a chariot. He has large white wings. One wheel of his chariot is shewn. He wears corslet and buskins of scale armour decorated with a winged lion's head, which symbol also surmounts his crown. His chariot is drawn by a lion. His arms are bare, save for the shoulder-pieces of the corslet, and he bears a torch or fire-wand, somewhat similar to that of the Zelator Adeptus Minor. Beneath the chariot are flames, some waved, some salient.
>
> Swift, strong, hasty; rather violent, yet just and generous; noble and scorning meanness.
>
> If ill dignified — cruel, intolerant, prejudiced and ill natured.
>
> He rules the heavens from above the last Decan of Cancer to the second Decan of Leo; hence he includes most of Leo Minor.
>
> Air of Fire
>
> Prince and Emperor of Salamanders.

**Prompt of the kept painting** (after the style line):

> The Prince of the Chariot of Fire: a kingly figure with large white wings and a golden winged crown sits in a chariot drawn by a lion; one wheel of the chariot is shown. He wears a corslet and buskins of scale armour decorated with a winged lion's head, and the same winged lion's head surmounts his crown. His arms are bare save for the shoulder-pieces. He holds up a flaming torch. Beneath the chariot are flames, some waving and some leaping upward. Swift, strong, noble.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651108265-eao2oqhzcru.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653734174-20hnxi0imbi.svg)

**Check:** The lion's heads on the armour are not winged.

### Princess of the Shining Flame: the Rose of the Palace of Fire (Knave of Wands)

**Book T (1912):**

> A VERY strong and beautiful woman with flowing red-gold hair, attired like an Amazon. Her shoulders, arms, bosom and knees are bare. She wears a short kilt reaching to the knee. Round her waist is a broad belt of scale-mail; narrow at the sides; broader in front and back; and having a winged tiger's head in front. She wears a Corinthian-shaped helmet and crown with a long plume. It also is surmounted by a tiger's head, and the same symbol forms the buckle of her scale-mail buskins. A mantle lined with tiger's skin falls back from her shoulders. Her right hand rests on a small golden or brazen altar ornamented with ram's heads and with Flames of Fire leaping from it. Her left hand leans on a long and heavy club, swelling at the lower end, where the sigil is placed; and it has flames of fire leaping from it the whole way down; but the flames are ascending. This club or torch is much longer than that carried by the King or Queen. Beneath her firmly placed feet are leaping Flames of Fire.
>
> Brilliance, courage, beauty, force, sudden in anger or love, desire of power, enthusiasm, revenge.
>
> If ill dignified, she is superficial, theatrical, cruel, unstable, domineering.
>
> She rules the heavens over one quadrant of the portion around the North Pole.
>
> Earth of Fire
>
> Princess and Empress of the Salamanders.
>
> Throne of the Ace of Wands.

**Prompt:** from the pilot grammar (see its `image_trials`).

**Result:** [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653737433-9hh0p7g1mg.svg)

### Lord of the Waves and the Waters: the King of the Hosts of the Sea (Knight of Cups)

**Book T (1912):**

> A BEAUTIFUL, winged, youthful Warrior with flying hair, riding upon a white horse, which latter is not winged. His general equipment is similar to that of the Knight of Wands, but upon his helmet, cuirass and buskins is a peacock with opened wings. He holds a cup in his hand, bearing the sigil of the scale. Beneath his horse's feet is the sea. From the cup issues a crab.
>
> Graceful, poetic, Venusian, indolent, but enthusiastic if roused.
>
> Ill dignified, he is sensual, idle and untruthful.
>
> He rules the heavens from above 20 Degree of Aquarius to 20 Degree of Pisces, thus including the greater part of Pegasus.
>
> Fire of Water
>
> King of Undines and Nymphs.

**Prompt of the kept painting** (after the style line):

> The Lord of the Waves and the Waters: a beautiful young winged warrior with flying hair rides a white horse; the horse has no wings. He wears a winged helmet with a rayed crown, a corslet and buskins of scale-mail and a flowing mantle. A peacock with opened wings is his crest, and the same peacock is on his cuirass and buskins. In his hand he holds a golden cup, and a small crab climbs out of the cup. Beneath the horse's hooves is the sea. Graceful and poetic.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651136521-xc2sihvfazq.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653787086-dt8z2vy5ofj.svg)

**Check:** The peacock is only on the helmet, not on the cuirass and buskins.

### Queen of the Thrones of the Waters (Queen of Cups)

**Book T (1912):**

> A VERY beautiful fair woman like a crowned Queen, seated upon a throne, beneath which is flowing water wherein Lotuses are seen. Her general dress is similar to that of the Queen of Wands, but upon her crown, cuirass and buskins is seen an Ibis with opened wings, and beside her is the same bird, whereon her hand rests. She holds a cup, wherefrom a crayfish issues. Her face is dreamy. She holds a lotus in the hand upon the Ibis.
>
> She is imaginative, poetic, kind, yet not willing to take much trouble for another. Coquettish, good-natured and underneath a dreamy appearance. Imagination stronger than feeling. Very much affected by other influences, and therefore more dependent upon dignity than most symbols.
>
> She rules from 20 Degree Gemini to 20 Degree Cancer.
>
> Water of Water
>
> Queen of Nymphs or Undines.

**Prompt:** from the pilot grammar (see its `image_trials`).

**Result:** [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653789371-pkl7kfcy41e.svg)

**Check:** Pilot painting (Oct 8). Her hand holds the lotus above the ibis rather than resting on it.

### Prince of the Chariot of the Waters (King of Cups)

**Book T (1912):**

> A WINGED Kingly Figure with winged crown seated in a chariot drawn by an eagle. On the wheel is the symbol of a scorpion. The eagle is borne as a crest on his crown, cuirass and buskins. General attire like King of Wands. Beneath his chariot is the calm and stagnant water of a lake. His armour resembles feathers more than scales. He holds in one hand a lotus, and in the other a cup, charged with the sigil of his scale. A serpent issues from the cup, and has its head tending down to the waters of the lake. He is subtle, violent, crafty and artistic; a fierce nature with calm exterior. Powerful for good or evil but more attracted by the evil if allied with apparent Power or Wisdom.
>
> If ill dignified, he is intensely evil and merciless.
>
> He rules from 20 Degree Libra to 20 Degree Scorpio.
>
> Air of Water
>
> Prince and Emperor of Nymphs or Undines.

**Prompt of the kept painting** (after the style line):

> The Prince of the Chariot of the Waters: a winged kingly figure with a winged crown is seated in a low chariot pulled forward by a great eagle flying in front of it on a harness. On the chariot wheel is the figure of a scorpion. An eagle is his crest; his armour looks like feathers more than scales. In one hand he holds a lotus; in the other a cup, and a green serpent issues from the cup, its head bending down to the water. The chariot glides over the calm, still water of a lake. A fierce nature with a calm exterior.

**First prompt** (its painting was re-run once):

> The Prince of the Chariot of the Waters: a winged kingly figure with a winged crown sits in a chariot drawn by an eagle. On the chariot wheel is the figure of a scorpion. An eagle is his crest, on his crown, cuirass and buskins; his armour looks like feathers more than scales. In one hand he holds a lotus; in the other a cup, and a serpent issues from the cup, its head bending down toward the water. Beneath the chariot lies the calm, still water of a lake. A fierce nature with a calm exterior.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651459247-ngttzhhl6yh.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653792080-mo0b2q30qgd.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651197937-jlfhob5o94.png)

**Check:** Re-run once: the first painting had a painted number 43 and the figure standing. In the kept one the eagle stands at the chariot's front instead of pulling it.

### Princess of the Waters: the Lotus of the Palace of the Floods (Knave of Cups)

**Book T (1912):**

> A BEAUTIFUL Amazon-like figure, softer in nature than the Princess of Wands. Her attire is similar. She stands on a sea with foaming spray. Away to her right a Dolphin. She wears as a crest a swan with opening wings. She bears in one hand a lotus, and in the other an open cup from which a turtle issues. Her mantle is lined with swansdown, and is of thin floating material.
>
> Sweetness, poetry, gentleness and kindness. Imaginative, dreamy, at times indolent, yet courageous if roused.
>
> When ill dignified she is selfish and luxurious.
>
> She rules a quadrant of the heavens around Kether.
>
> Earth of Water
>
> Princess and Empress of the Nymphs or Undines
>
> Throne of the Ace of Cups.

**Prompt of the kept painting** (after the style line):

> The Princess of the Waters, the Lotus of the Palace of the Floods: a beautiful warrior maiden, gentle in bearing, dressed like an Amazon in a sleeveless sea-green tunic with a short skirt and a belt of silver scale-mail, stands upon the sea amid foaming spray. As her crest she wears a white swan with opening wings. In one hand she holds a pink lotus; in the other an open golden cup from which a small turtle climbs. Her thin floating mantle is lined with white swansdown. Away to her right a dolphin leaps from the waves. Sweet, dreamy, gentle.

**First prompt** (its painting was re-run once):

> The Princess of the Waters, the Lotus of the Palace of the Floods: a beautiful young woman dressed like an Amazon, gentle in bearing, stands upon the sea amid foaming spray. Her shoulders and arms are bare; she wears a short kilt and a belt of scale-mail. As her crest she wears a swan with opening wings. In one hand she holds a lotus; in the other an open cup from which a small turtle climbs. Her thin floating mantle is lined with white swansdown. Away to her right a dolphin leaps from the waves. Sweet, dreamy, gentle.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651387668-ya0ugdny9i.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653794731-d0uoshtw1ou.svg)

**Check:** First request was refused by the image service (no reason given); re-worded as 'warrior maiden in a sleeveless tunic'.

### Lord of the Wind and the Breezes: the King of the Spirits of Air (Knight of Swords)

**Book T (1912):**

> A WINGED Warrior with crowned Winged Helmet, mounted upon a brown steed. His general equipment is as that of the Knight of Wands, but he wears as a crest a winged six-pointed star, similar to those represented on the heads of Castor and Pollux the Dioscuri, the twins Gemini (a part of which constellation is included in his rule). He holds a drawn sword with the sigil of his scale upon its pommel. Beneath his horse's feet are dark-driving stratus clouds.
>
> He is active, clever, subtle, fierce, delicate, courageous, skilful, but inclined to domineer. Also to overvalue small things, unless well dignified.
>
> If ill dignified, deceitful, tyrannical and crafty.
>
> Rules from 20 Degree Taurus to 20 Degree Gemini.
>
> Fire of Air
>
> King of the Sylphs and Sylphides.

**Prompt:** from the pilot grammar (see its `image_trials`).

**Result:** [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653797049-buatv9ixl5r.svg)

**Check:** Pilot painting (Oct 8): its painted title read KING OF SWORDS (the 1912 rank) and is cut away here.

### Queen of the Thrones of Air (Queen of Swords)

**Book T (1912):**

> A GRACEFUL woman with wavy, curling hair, like a Queen seated upon a Throne and crowned. Beneath the Throne are grey cumulus clouds. Her general attire is as that of the Queen of Wands, but she wears as a crest a winged child's head. A drawn sword in one hand, and in the other a large, bearded, newly severed head of a man.
>
> Intensely perceptive, keen observation, subtle, quick and confident: often persevering, accurate in superficial things, graceful, fond of dancing and balancing.
>
> If ill dignified, cruel, sly, deceitful, unreliable, though with a good exterior.
>
> Rules from 20 Degree Virgo to 20 Degree Libra.
>
> Water of Air
>
> Queen of the Sylphs and Sylphides.

**Prompt of the kept painting** (after the style line):

> The Queen of the Thrones of Air: a graceful woman with wavy, curling hair sits crowned on a throne; beneath the throne are grey cumulus clouds. She wears a corslet and buskins of scale-mail which her robe discloses; her arms are almost bare. As her crest she wears a winged child's head. In her right hand she holds a drawn sword upright; in her left hand she holds up by its hair the large bearded head of a man, newly severed. A keen, perceptive face.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651236733-rtnn2suhsw.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653799333-scra7z6psop.svg)

### Prince of the Chariot of the Winds (King of Swords)

**Book T (1912):**

> A WINGED King with Winged Crown, seated in a chariot drawn by Arch Fays, represented as winged youths very slightly dressed, with butterfly wings: heads encircled by a fillet with a pentagram thereon: and holding wands surmounted by pentagrams, the same butterfly wings on their feet and fillets. General equipment as the King of Wands: but he bears as a crest a winged angelic head with a pentagram on the brows. Beneath the chariot are grey nimbus clouds. His hair long and waving in serpentine whirls, and whorl figures compose the scales of his armour. A drawn sword in one hand; a sickle in the other. With the sword he rules, with the sickle he slays.
>
> Full of ideas and thoughts and designs, distrustful, suspicious, firm in friendship and enmity; careful, observant, slow, over-cautious, symbolizes Α and Ω; he slays as fast as he creates.
>
> If ill dignified: harsh, malicious, plotting; obstinate, yet hesitating; unreliable.
>
> Rules from 20 Degree Capricorn to 20 Degree Aquarius.
>
> Air of Air
>
> Prince and Emperor of the Sylphs and Sylphides.

**Prompt of the kept painting** (after the style line):

> The Prince of the Chariot of the Winds: a bearded winged king with a winged crown and long hair waving in serpentine whirls sits in a chariot; whorls form the scales of his armour. In his right hand a drawn sword, in his left a sickle. His crest is a small winged angelic head with a star on its brow. The chariot is drawn by two small winged youths with butterfly wings, each holding a wand topped by a star. Beneath the chariot are dark grey rain clouds.

**First prompt** (its painting was re-run once):

> The Prince of the Chariot of the Winds: a winged king with a winged crown sits in a chariot drawn by two Arch Fays: winged youths, lightly dressed, with butterfly wings on their backs and on their feet, a fillet with a pentagram around their heads, each holding a wand topped by a pentagram. His crest is a winged angelic head with a pentagram on its brow. His long hair waves in serpentine whirls, and whorls form the scales of his armour. In one hand a drawn sword, in the other a sickle. Beneath the chariot are grey nimbus clouds.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651431826-cb7twlvb1ef.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653801407-019pz9s204ty.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651261319-7dcgk5q35ny.png)

**Check:** Re-run once: the first painting showed a woman. The re-run prompt says star where Book T says pentagram (the Arch Fays' fillets and wands, the crest's brow); put pentagram back on the next pass.

### Princess of the Rushing Winds: the Lotus of the Palace of Air (Knave of Swords)

**Book T (1912):**

> AN AMAZON figure with waving hair, slighter than the Rose of the Palace of Fire. Her attire is similar. The Feet seem springy, giving the idea of swiftness. Weight changing from one foot to another and body swinging around. She is a mixture of Minerva and Diana: her mantle resembles the AEgis of Minerva. She wears as a crest the head of the Medusa with serpent hair. She holds a sword in one hand; and the other rests upon a small silver altar with grey smoke (no fire) ascending from it. Beneath her feet are white clouds.
>
> Wisdom, strength, acuteness; subtlety in material things: grace and dexterity.
>
> If ill dignified, she is frivolous and cunning.
>
> She rules a quadrant of the heavens around Kether.
>
> Earth of Air
>
> Princess and Empress of the Sylphs and Sylphides.
>
> Throne of the Ace of Wands.

**Prompt of the kept painting** (after the style line):

> The Princess of the Rushing Winds: an Amazon with waving hair, slight and swift, her weight shifting from one foot to the other and her body swinging round. She is like Minerva and Diana: her mantle is like Minerva's aegis, and as her crest she wears the head of Medusa with serpent hair. She holds a sword in one hand; her other hand rests on a small silver altar from which grey smoke rises, without any flame. Beneath her feet are white clouds.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651285392-kl1qhm0knjf.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653803459-v8h8wgoq59l.svg)

### Lord of the Wide and Fertile Land: the King of the Spirits of Earth (Knight of Pentacles)

**Book T (1912):**

> A DARK Winged Warrior with winged and crowned helmet: mounted on a light brown horse. Equipment as the Knight of Wands.
>
> The winged head of a stag or antelope as a crest. Beneath the horse's feet is fertile land with ripened corn. In one hand he bears a sceptre surmounted by a hexagram: in the other a Pentacle like that of the Zelator Adeptus Minor.
>
> Unless very well dignified he is heavy, dull, and material. Laborious, clever, and patient in material matters.
>
> If ill dignified, he is avaricious, grasping, dull, jealous; not very courageous, unless assisted by other symbols.
>
> Rules from above 20 Degree of Leo to 20 Degree of Virgo.
>
> Fire of Earth
>
> King of Gnomes.

**Prompt of the kept painting** (after the style line):

> The Lord of the Wide and Fertile Land: a dark-haired winged warrior with a winged and crowned helmet rides a light-brown horse; the horse has no wings. He wears a corslet and buskins of scale-mail and a flowing mantle. His crest is the winged head of a stag. In one hand he holds a sceptre topped by a six-pointed star; in the other a golden disc, a pentacle. Beneath the horse's hooves is fertile land with ripe golden corn. Patient and laborious.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651304852-dvf15zs1fj.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653843664-lskpbqkbzy9.svg)

**Check:** Plain boots, not scale-mail buskins.

### Queen of the Thrones of Earth (Queen of Pentacles)

**Book T (1912):**

> A WOMAN of beautiful face with dark hair; seated upon a throne, beneath which is dark sandy earth. One side of her face is light, the other dark; and her symbolism is best represented in profile. Her attire is similar to that of the Queen of Wands: but she bears a winged goat's head as a crest. A goat is by her side. In one hand she bears a sceptre surmounted by a cube, and in the other an orb of gold.
>
> She is impetuous, kind; timid, rather charming; great-hearted; intelligent, melancholy; truthful, yet of many moods.
>
> If ill dignified she is undecided, capricious, changeable, foolish.
>
> She rules from 20 Degree Sagittarius to 20 Degree Capricorn.
>
> Water of Earth
>
> The Queen of Gnomes.

**Prompt of the kept painting** (after the style line):

> The Queen of the Thrones of Earth: a woman with a beautiful face and dark hair sits on a throne, shown in profile; one side of her face is in light and the other in shadow. Beneath the throne is dark sandy earth. She wears a corslet and buskins of scale-mail which her robe discloses, and as her crest a winged goat's head. A goat stands by her side. In one hand she holds a sceptre topped by a cube, in the other an orb of gold. Melancholy, kind, many-mooded.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651328765-4r7123db1xo.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653846939-m83v6hdz0lr.svg)

**Check:** The crest is a winged bird on the throne, not a winged goat's head on her; light and dark halves of the face are not shown.

**Redo:** 4th: the crest and the split face are Book T's own marks for this card.

### Prince of the Chariot of Earth (King of Pentacles)

**Book T (1912):**

> A WINGED Kingly Figure seated in a chariot drawn by a bull. He bears as a crest the symbol of the head of the winged bull. Beneath the chariot is land, with many flowers. In the one hand he bears an orb of gold held downwards, and in the other a sceptre surmounted by an orb and cross.
>
> Increase of matter. Increases good or evil, solidifies; practically applies things. Steady; reliable.
>
> If ill dignified he is selfish, animal and material: stupid. In either case slow to anger, but furious if roused.
>
> Rules from 20 Degree Aries to 20 Degree Taurus.
>
> Air of Earth
>
> Prince and Emperor of the Gnomes.

**Prompt:** from the pilot grammar (see its `image_trials`).

**Result:** [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653850314-jdvl7u1dplg.svg)

### Princess of the Echoing Hills: the Rose of the Palace of Earth (Knave of Pentacles)

**Book T (1912):**

> A STRONG and beautiful Amazon figure with rich brown hair, standing on grass or flowers. A grove of trees near her. Her form suggests Hebe, Ceres, and Proserpine. She bears a winged ram's head as a crest: and wears a mantle of sheepskin. In one hand she carries a sceptre with a circular disk: in the other a Pentacle similar to that of the Ace of Pentacles.
>
> She is generous, kind, diligent, benevolent, careful, courageous, persevering, pitiful.
>
> If ill dignified she is wasteful and prodigal. She rules over one quadrant of the heavens around the North Pole of the Ecliptic.
>
> Earth of Earth
>
> Princess and Empress of the Gnomes.
>
> Throne of the Ace of Pentacles.

**Prompt of the kept painting** (after the style line):

> The Princess of the Echoing Hills: a strong and beautiful warrior maiden with rich brown hair, in a green and russet tunic, stands on grass and flowers with a grove of trees near her, like Ceres the harvest goddess. As her crest she wears a winged ram's head, and a mantle of sheepskin falls from her shoulders. In one hand she carries a sceptre topped by a round disc; in the other a large golden pentacle disc of concentric circles with a red cross at its white centre and twelve white rays. Generous, careful, steady.

**First prompt** (its painting was re-run once):

> The Princess of the Echoing Hills: a strong and beautiful Amazon with rich brown hair stands on grass and flowers, a grove of trees near her; her form recalls Ceres and Proserpine. As her crest she wears a winged ram's head, and a mantle of sheepskin falls from her shoulders. In one hand she carries a sceptre topped by a round disc; in the other a large pentacle: a golden disc of concentric circles with a red cross at its white centre and twelve white rays. Generous, careful, steady.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651410433-kh8ehkakf9.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653852887-qgiquzs02ia.svg)

**Check:** The pentacle carries an eight-pointed star instead of the Ace's rays and cross.

## The thirty-six small cards

### Lord of Strife (Five of Wands)

**Book T (1912):**

> TWO White Radiant Angelic Hands issuant per nubes dexter and sinister. They are clasped together in the grip of the First Order, "i.e." the four fingers of each right hand crooked into each other, the thumbs meeting above; and they hold, at the same time, by their centres, five wands or torches which are similar unto the wands of a Zelator Adeptus Minor. One wand is upright in the middle; the others cross each other. Flames leap from the point of junction. Above the middle wand is the sign Saturn, and below is that of Leo: thus representing the Decante. Violent strife and boldness, rashness, cruelty, violence, lust, desire, prodigality and generosity; depending on whether the card is well or ill dignified.
>
> Geburah of י (Quarrelling and fighting).
>
> This Decan hath its beginning from the Royal Star of Leo: and unto it are allotted the two great Angels of the Schemhamphorash והויה and יליאל.
>
> [The proper meaning of the small cards is to be found by making thorough meditation and harmony between these four symbols of each card. It will be seen that this is how the meanings have been done; but the advanced student can go beyond this rude working.]

**Prompt of the kept painting** (after the style line):

> Lord of Strife: in the centre, two white radiant angelic hands, one from a cloud on the left and one from a cloud on the right, meet in a clasped handshake grip. Through their clasped grip pass exactly five long wooden wands, held at their middles: one wand stands straight upright, and four wands cross it diagonally in two X shapes. Red and gold flames leap from the point where the wands cross. Dark red ground. Violent strife.

**First prompt** (its painting was re-run once):

> Lord of Strife: two white radiant angelic hands come out of clouds on the left and right, clasped together in a grip, the fingers of each hooked into the other, thumbs meeting above. Together they hold five wooden wands by their centres: one upright in the middle, the other four crossing each other. Flames leap from the point where they cross. Red and gold fire. Violent strife.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653430674-wfokbjyx4l9.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653864480-w4fdpko1e6.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651822912-mezqspqiiv.png)

**Check:** Re-run once (the first was a bundle of ten sticks); the kept one still shows more than five wands.

### Lord of Victory (Six of Wands)

**Book T (1912):**

> TWO hands in grip as the last, holding six wands crossed three and three. Flames issue from the point of junction. Above and below are short wands with flames issuing, surmounted respectively by the symbols of Jupiter and Leo, representing the Decan.
>
> Victory after strife: Love: pleasure gained by labour: carefulness, sociability and avoiding of strife, yet victory therein: also insolence, and pride of riches and success, etc. The whole dependent on the dignity.
>
> Tiphareth of י (Gain).
>
> Hereunto are allotted the great Angels סיטאל and עלמיה of the Schemhamphorash.

**Prompt of the kept painting** (after the style line):

> Lord of Victory: two white radiant angelic hands, one from a cloud on the left and one from a cloud on the right, meet in a clasped grip at the centre. Through their grip pass exactly six long wooden wands: three slanting one way and three slanting the other, forming a broad X of six wands. Flames burst from the crossing. A short flaming wand floats at the top and another at the bottom. Red and gold fire on a clear blue sky. Victory after strife.

**First prompt** (its painting was re-run once):

> Lord of Victory: two white radiant angelic hands come out of clouds left and right, clasped in a grip at the centre, and hold six wooden wands crossed three and three. Flames burst from the crossing. Above and below, short wands with flames issuing. Red and gold fire, a clear sky. Victory after strife.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653518461-66pcehojws8.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653866471-97r54kdo2t.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651847427-kiygtfbvfrh.png)

**Check:** Re-run once; still four wands, not six.

### Lord of Valour (Seven of Wands)

**Book T (1912):**

> TWO hands holding by grip six wands, three crossed. A third hand issuing from a cloud at the lower part of the card, holding an upright wand which passes between the others. Flames leap from the point of junction. Above and below the central wand are the symbols of Mars and Leo, representing the Decan.
>
> Possible victory, depending on the energy and courage exercised; valour; opposition, obstacles and difficulties, yet courage to meet them; quarrelling, ignorance, pretence, and wrangling, and threatening; also victory in small and unimportant things: and influence upon subordinates.
>
> Netzach of י (Opposition, yet courage).
>
> Therein rule the two great Angels מהשיה and ללהאל of the Schemhamphorash.

**Prompt of the kept painting** (after the style line):

> Lord of Valour: two white radiant angelic hands from clouds left and right hold six wooden wands, three crossed over three; a third hand rises from a cloud at the bottom of the card and holds an upright wand that passes between the others. Flames leap from the crossing. Red and gold fire. Courage against opposition.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651869944-x6ymoq5kwa.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653868611-4mmxa51qkrj.svg)

**Check:** Count off: more than six crossed wands.

### Lord of Prudence (Eight of Pentacles)

**Book T (1912):**

> A WHITE Radiating Angelic Hand, issuing from a cloud, and grasping a branch of a rose tree, with four white roses thereon, which touch only the four lowermost Pentacles. No rosebuds even, but only leaves, touch the four uppermost disks. All the Pentacles are similar to that of the Ace, but without the Maltese cross and wings. They are arranged like the geomantic figure Populus. Above and below them are the symbols Sun and Virgo for the Decan.
>
> Over-careful in small things at the expense of great: "Penny wise and pound foolish": gain of ready money in small sums; mean; avaricious; industrious; cultivation of land; hoarding, lacking in enterprise.
>
> Hod of ה (Skill: prudence: cunning).
>
> Therein rule those mighty Angels אכאיה and כהתאל.

**Prompt of the kept painting** (after the style line):

> Lord of Prudence: a white radiant angelic hand comes out of a cloud and grasps a rose branch with four white roses, which touch only the four lowest of eight golden pentacles; only leaves touch the four upper ones. The eight pentacles, discs of concentric rings with a small red cross at the centre, are arranged in four rows of two. Careful, earthy green and gold.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652854890-vsz05sjiix.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653914527-2yz49cx87s6.svg)

### Lord of Material Gain (Nine of Pentacles)

**Book T (1912):**

> A WHITE Radiating Angelic Hand, holding a rose branch with nine white roses, each of which touches a Pentacle. The Pentacles are arranged thus *(a figure of nine dots on the printed page)*: and there are rosebuds on the branches as well as flowers. Venus and Virgo above and below.
>
> Complete realization of material gain, good, riches; inheritance; covetous; treasuring of goods; and sometimes theft and knavery. The whole according to dignity.
>
> Yesod of ה (Inheritance, much increase of goods).
>
> Herein those mighty Angels הזיאל and אלדיה have rule and dominion.

**Prompt of the kept painting** (after the style line):

> Lord of Material Gain: a white radiant angelic hand holds a rose branch with nine white roses, each touching one of nine golden pentacles, discs of concentric rings with a small red cross at the centre; there are rosebuds on the branch as well as flowers. Rich harvest light.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652885899-73pn8qdicjh.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653918010-e3dc3nybed.svg)

**Check:** Ten discs, not nine.

### Lord of Wealth (Ten of Pentacles)

**Book T (1912):**

> AN Angelic Hand, holding by the lower extremity a branch whose roses touch all the Pentacles. No buds, however, are shewn. The symbols of Mercury and Virgo are above and below.
>
> The Pentacles are thus arranged *(a figure on the printed page: ten pentacles in rows of 2, 1, 2, 2, 1, 2)*.
>
> Completion of material gain and fortune; but nothing beyond: as it were, at the very pinnacle of success. Old age, slothfulness; great wealth, yet sometimes loss in part; heaviness; dullness of mind, yet clever and prosperous in money transactions.
>
> Malkuth of ה (Riches and wealth).
>
> Herein are לאויה and ההעיה set over this Decan as Angel Rulers.

**Prompt of the kept painting** (after the style line):

> Lord of Wealth: exactly ten golden discs, each with concentric rings and a small red cross at the centre, set in the shape of the Tree of Life: one at the top, two below it, one, two, one, two and one at the bottom. A white angelic hand at the bottom holds a long rose branch by its lower end; the branch climbs up through the discs and its white roses touch every disc. No buds. Plain green and gold ground, heavy golden wealth.

**First prompt** (its painting was re-run once):

> Lord of Wealth: an angelic hand holds a rose branch by its lower end; its white roses touch all ten golden pentacles, discs of concentric rings with a small red cross at the centre, arranged in rows of two, one, two, two, one and two. No buds are shown. Heavy golden wealth.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653317636-14mqfsbce0ph.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653920681-rh7hw5mzvt.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652914378-shrieq91fp.png)

**Check:** Re-run once: the first was a heap of more than sixteen discs.

### Lord of Peace Restored (Two of Swords)

**Book T (1912):**

> Two crossed swords, like the air dagger of a Z.A.M., each held by a White Radiant Angelic Hand. Upon the point where the two cross is a rose of five petals, emitting white rays. At the top and bottom of the card are two small daggers, supporting respectively the symbol Moon thus, and Libra representing the Decanate.
>
> Contradictory characters in the same nature, strength through suffering; pleasure after pain. Sacrifice and trouble, yet strength arising therefrom, symbolized by the position of the rose, as though the pain itself had brought forth beauty. Arrangement, peace restored; truce; truth and untruth; sorrow and sympathy. Aid to the weak; arrangement; justice, unselfishness; also a tendency to repetition of affronts on being pardoned; injury when meaning well; given to petitions; also a want of tact, and asking question of little moment; talkative.
>
> Chokmah of ו. Quarrel made up, yet still some tension in relations: actions sometimes selfish, sometimes unselfish.
>
> Herein rule the Great Angels יזלאל and מנהאל.

**Prompt of the kept painting** (after the style line):

> Lord of Peace Restored: only two long straight steel swords, crossed in an X. One white radiant angelic hand comes out of a cloud at the lower left and holds the first sword; a second white hand comes out of a cloud at the lower right and holds the second. Where the two blades cross sits a red rose of five petals, sending out thin white rays. A small upright dagger floats at the top centre and another at the bottom centre. Pale blue sky. A truce, peace restored.

**First prompt** (its painting was re-run once):

> Lord of Peace Restored: two crossed straight steel swords, each held by a white radiant angelic hand coming out of clouds left and right. Where the blades cross sits a red rose of five petals, sending out white rays. Above and below, two small upright daggers. Pale blue sky. A truce, peace restored.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653400184-vop82hpec2a.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653922723-eb55cn6sfvf.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652375158-yry08zxk7wk.png)

**Check:** Re-run once: the first painting had four swords.

### Lord of Sorrow (Three of Swords)

**Book T (1912):**

> THREE White Radiating Angelic Hands, issuing from clouds, and holding three swords upright (as though the central sword had struck apart the two others, which were crossed in the preceding symbol): the central sword cuts asunder the rose of five petals, which in the previous symbol grew at the junction of the swords; its petals are falling, and no white rays issue from it.
>
> Above and below the central sword are the symbols of Saturn and Libra.
>
> Disruption, interruption, separation, quarrelling; sowing of discord and strife, mischief-making, sorrow and tears; yet mirth in Platonic pleasures; singing, faithfulness in promises, honesty in money transactions, selfish and dissipated, yet sometimes generous: deceitful in words and repetitions; the whole according to dignity.
>
> Binah of ו (Unhappiness, sorrow, and tears).
>
> Herein rule the Great Angels הריאל and הקמיה as Lords of the Decan.

**Prompt of the kept painting** (after the style line):

> Lord of Sorrow: three white radiant angelic hands come out of grey clouds at the bottom of the card, each holding one upright steel sword: three swords in all. The central sword stands straight and has struck apart the two outer swords, which lean away to left and right. The central blade cuts through a red rose of five petals; its petals fall in the rain. Grey stormy sky with slanting rain; the picture holds only the clouds, the hands, the swords, the rose and the rain.

**First prompt** (its painting was re-run once):

> Lord of Sorrow: three white radiant angelic hands come out of clouds and hold three upright steel swords. The central sword has struck apart the other two and cuts through a red rose of five petals; its petals are falling and no rays come from it. Grey stormy sky with rain. Sorrow and tears.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653375363-et0z30fakwg.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653926003-2lii173aw4y.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652402131-18bsk13g1aq.png)

**Check:** Re-run once: the first painting had an eye in a pool. The kept one had 'LORD OF SORROW' painted at the bottom; that strip was cut off before tracing.

### Lord of Rest from Strife (Four of Swords)

**Book T (1912):**

> TWO White Radiating Angelic Hands, each holding two swords; which four cross in the centre. The rose of five petals with white radiations is reinstated on the point of their intersection. Above and below, on the points of two small daggers, are Jupiter and Libra, representing the Decanate.
>
> Rest from sorrow; yet after and through it. Peace from and after war. Relaxation of anxiety. Quietness, rest, ease and plenty, yet after struggle. Goods of this life; abundance; modified by dignity as is usual.
>
> Chesed of ו (Convalescence, recovery from sickness; change for the better).
>
> Herein do לאויה and כליאל bear rule.

**Prompt of the kept painting** (after the style line):

> Lord of Rest from Strife: two white radiant angelic hands come out of clouds, each holding two steel swords; the four blades cross at the centre, and a red rose of five petals with white rays sits again at the crossing. Two small daggers above and below. Calm pale sky. Rest after strife.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652433095-bsgwe66yt1j.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653929514-4yqs53cday8.svg)

**Check:** Four hands with one sword each, not two hands with two.

### Lord of Loss in Pleasure (Five of Cups)

**Book T (1912):**

> A WHITE Radiating Angelic Hand, holding lotuses or water-lilies, of which the flowers are falling right and left. Leaves only, and no buds, surmount them. These lotus stems ascend between the cups in the manner of a fountain, but no water flows therefrom; neither is there water in any of the cups, which are somewhat of the shape of the magical instrument of the Zelator Adeptus Minor.
>
> Above and below are the symbols of Mars and Scorpio for the Decan.
>
> Death, or end of pleasure: disappointment, sorrow and loss in those things from which pleasure is expected. Sadness, treachery, deceit; ill-will, detraction; charity and kindness ill requited; all kinds of anxieties and troubles from unsuspected and unexpected sources.
>
> Geburah of ה (Disappointment in love, marriage broken off, unkindness of a friend; loss of friendship).
>
> Herein rule לוויה and פהליה.

**Prompt of the kept painting** (after the style line):

> Lord of Loss in Pleasure: five large empty golden goblets stand clearly in the picture, two at the top, one in the middle and two at the bottom. A white radiant angelic hand from a cloud at the bottom holds a bunch of lotus stems that rise like a dry fountain between the five goblets. The lotus flowers are falling away to right and left; only green leaves remain at the tops of the stems. No water anywhere: all five goblets are dry. Grey-violet, sad autumnal mood.

**First prompt** (its painting was re-run once):

> Lord of Loss in Pleasure: a white radiant angelic hand from a cloud at the bottom holds a bunch of lotus or water-lily stems that rise like a fountain between five golden cups. The lotus flowers are falling away to right and left; only leaves crown the stems, with no buds. No water flows: all five cups are dry and empty. Sad, autumnal mood.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653261546-86tbw2dlu23.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653932340-1og6t1tdy8e.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652142485-3ebt38d3iys.png)

**Check:** Re-run once: the first painting had no cups at all.

### Lord of Pleasure (Six of Cups)

**Book T (1912):**

> AN Angelic Hand, as before, holds a group of stems of water-lilies or lotuses, from which six flowers bend, one over each cup. From these flowers a white glistening water flows into the cups as from a fountain, but they are not yet full. Above and below are Sun and Scorpio referring to the Decan.
>
> Commencement of steady increase, gain and pleasure; but commencement only. Also affront, detection, knowledge, and in some instances contention and strife arising from unwarranted self-assertion and vanity. Sometimes thankless and presumptuous; sometimes amiable and patient. According to dignity as usual.
>
> Tiphareth of ה (Beginning of wish, happiness, success, or enjoyment).
>
> Therein rule נלכאל and יייאל.

**Prompt of the kept painting** (after the style line):

> Lord of Pleasure: exactly six large golden goblets in two columns of three, well spaced on a soft blue ground. An angelic hand from a cloud at the bottom holds a group of lotus stems rising between the columns; six lotus flowers bend outward, one over each goblet, and from each flower a thin stream of glistening white water flows into its goblet, which is only half full. Soft blue and gold.

**First prompt** (its painting was re-run once):

> Lord of Pleasure: an angelic hand from a cloud holds a group of water-lily or lotus stems from which six flowers bend, one over each of six golden cups. From each flower a white glistening water flows into its cup, as from a fountain, but the cups are not yet full. Soft blue and gold.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653463177-0rig0mumndx.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653935116-0w7wxlkh6ws.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652166096-8i2krgnt8tg.png)

**Check:** Re-run once: the first painting had nine cups.

### Lord of Illusionary Success (Seven of Cups)

**Book T (1912):**

> THE seven cups are arranged as two descending triangles above a point: a hand, as usual, holds lotus stems which arise from the central lower cup. The hand is above this cup and below the middle one. With the exception of the central lower cup, each is overhung by a lotus flower, but no water falls from these into any of the cups, which are all quite empty. Above and below are the symbols of the Decanate Venus and Scorpio.
>
> Possible victory, but neutralized by the supineness of the person: illusionary success, deception in the moment of apparent victory. Lying, error, promises unfulfilled. Drunkenness, wrath, vanity. Lust, fornication, violence against women, selfish dissipation, deception in love and friendship. Often success gained, but not followed up. Modified as usual by dignity.
>
> Netzach of ה (Lying, promises unfulfilled; illusion, deception, error; slight success at outset, not retained).
>
> Herein the Angels מלהאל and חהויה rule.

**Prompt of the kept painting** (after the style line):

> Lord of Illusionary Success: seven golden cups are arranged as two downward-pointing triangles above a single cup at the bottom. A hand, just above that lowest cup, holds lotus stems rising from it. A lotus flower overhangs each of the other six cups, but no water falls from them: every cup is empty. A dreamlike, deceptive violet mood.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652192385-dljcfa6c0s.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653937443-s7cipsxjgyp.svg)

**Check:** Six cups in one triangle, not two.

### Lord of Swiftness (Eight of Wands)

**Book T (1912):**

> FOUR White Radiating Angelic Hands (two proceeding from each side) issuant from clouds; clasped in two pairs in the centre with the grip of the First Order. They hold eight wands, crossed four with four. Flames issue from the point of junction. Surmounting the small wands with flames issuing down them, and placed in the centre at the top and bottom of the card respectively, are the symbols of Mercury and Sagittarius for the Decan.
>
> Too much force applied too suddenly. Very rapid rush, but quickly passed and expended. Violent, but not lasting. Swiftness, rapidity, courage, boldness, confidence, freedom, warfare, violence; love of open air, field-sports, gardens and meadows. Generous, subtle, eloquent, yet somewhat untrustworthy; rapacious, insolent, oppressive. Theft and robbery. According to dignity.
>
> Hod of י (Hasty communications and messages; swiftness).
>
> Therein rule the Angels נתהיה and האאיה.

**Prompt of the kept painting** (after the style line):

> Lord of Swiftness: four white radiant angelic hands, two coming out of clouds on each side, clasp in two pairs at the centre and hold eight wooden wands crossed four and four. Flames burst from the crossing. Short flaming wands at the top and bottom. A swift rush of red and gold fire.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651893247-z3s3lv4gbqk.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653940387-4utfx5c7ri.svg)

**Check:** The four hands hold the wands but do not clasp each other.

### Lord of Great Strength (Nine of Wands)

**Book T (1912):**

> FOUR hands, as in the previous symbol, holding eight wands crossed four and four; but a fifth hand at the foot of the card holds another wand upright, which traverses the point of junction with the others: flames leap herefrom. Above and below are the symbols Moon and Sagittarius.
>
> Tremendous and steady force that cannot be shaken. Herculean strength, yet sometimes scientifically applied. Great success, but with strife and energy. Victory, preceded by apprehension and fear. Health good, and recovery not in doubt. Generous, questioning and curious; fond of external appearances: intractable, obstinate.
>
> Yesod of י (Strength, power, health, recovery from sickness).
>
> Herein rule the Angels ירתאל and שאהיה.

**Prompt of the kept painting** (after the style line):

> Lord of Great Strength: four white radiant angelic hands, two from clouds on each side, clasped in pairs, hold eight wooden wands crossed four and four; a fifth hand rises from a cloud at the bottom and holds a ninth wand upright through the crossing. Flames leap from it. Red and gold fire. Steady, unshakable strength.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651915253-xc1xy3lcvgl.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653976722-53pqpaorsfw.svg)

### Lord of Oppression (Ten of Wands)

**Book T (1912):**

> FOUR hands holding eight wands crossed as before. A fifth hand holding two wands upright, which traverses the junction of the others. Flames issuant. Saturn and Sagittarius.
>
> Cruel and overbearing force and energy, but applied only to material and selfish ends. Sometimes shows failure in a matter, and the opposition too strong to be controlled; arising from the person's too great selfishness at the beginning. Ill-will, levity, lying, malice, slander, envy, obstinacy; swiftness in evil and deceit, if ill dignified. Also generosity, disinterestedness and self-sacrifice, when well dignified.
>
> Malkuth of ו (Cruelty, malice, revenge, injustice).
>
> Therein rule רייאל and אומאל.

**Prompt of the kept painting** (after the style line):

> Lord of Oppression: four white radiant angelic hands, two from clouds on each side, hold eight wooden wands crossed four and four; a fifth hand from a cloud at the bottom holds two more wands upright through the crossing. Flames burst everywhere. Heavy dark red fire, oppressive force.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651941565-4d989wscx2y.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653979956-itvi66mseij.svg)

**Check:** The side hands hold one wand each.

### Lord of Harmonious Change (Two of Pentacles)

**Book T (1912):**

> TWO wheels, disks or pentacles, similar to that of the Ace. They are united by a green-and-gold serpent, bound about them like a figure of 8. It holds its tail in its mouth. A White Radiant Angelic Hand holds the centre of the whole. No roses enter into this card. Above and below are the symbols of Jupiter and Capricorn. It is a revolving symbol.
>
> The harmony of change, alternation of gain and loss; weakness and strength; everchanging occupation; wandering, discontented with any fixed condition of things; now elated, then melancholy; industrious, yet unreliable; fortunate through prudence of management, yet sometimes unaccountably foolish; alternatively talkative and suspicious. Kind, yet wavering and inconsistent. Fortunate in journeying. Argumentative.
>
> Chokmah of ה (Pleasant change, visit to friends).
>
> Herein the Angels לכבאל and ושריה have rule.

**Prompt of the kept painting** (after the style line):

> Lord of Harmonious Change: two golden pentacles, each a disc of concentric rings with a small red cross at its centre, one above the other, bound together by a green-and-gold serpent that loops around them like a figure eight and holds its tail in its mouth. A white radiant angelic hand from a cloud holds the centre of the whole. No roses. A revolving, playful motion.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652669239-9h7fia8ql.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653983713-sfcaxjivh7.svg)

**Check:** Two serpents, each around one disc, instead of one serpent in a figure eight around both.

**Redo:** 1st (tied): Book T's single serpent in a figure eight is this card's whole symbol.

### Lord of Material Works (Three of Pentacles)

**Book T (1912):**

> A WHITE-WINGED Angelic Hand, as before, holding a branch of a rose tree, of which two white rosebuds touch and surmount the topmost Pentacle. The Pentacles are arranged in an equilateral triangle. Above and below the symbols Mars and Capricorn.
>
> Working and constructive force, building up, creation, erection; realization and increase of material things; gain in commercial transactions, rank; increase of substance, influence, cleverness in business, selfishness. Commencement of matters to be established later. Narrow and prejudiced. Keen in matters of gain; sometimes given to seeking after impossibilities.
>
> Binah of ה (Business, paid employment, commercial transaction).
>
> Herein are יחויה and להחיה Angelic Rulers.

**Prompt of the kept painting** (after the style line):

> Lord of Material Works: on a plain green and gold ground, three large golden discs, each with concentric rings and a small red cross at the centre, form an upright triangle: one at the top, two below. A white angelic hand with a white wing at the wrist comes out of a cloud and holds a branch of a rose tree that rises between the discs; two white rosebuds touch the topmost disc and rise above it. The picture holds only the hand, the cloud, the branch and the three discs.

**First prompt** (its painting was re-run once):

> Lord of Material Works: a white-winged angelic hand comes out of a cloud and holds a branch of a rose tree. Three golden pentacles, discs of concentric rings with a small red cross at the centre, are arranged in an upright equilateral triangle; two white rosebuds touch and rise above the topmost pentacle. Green and gold. Building and work.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653340749-ubfyk7iukdk.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653986852-qdfst96unt.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652709006-qn65ik8rxh7.png)

**Check:** Re-run once: the first painting added a building.

### Lord of Earthly Power (Four of Pentacles)

**Book T (1912):**

> A HAND holding a branch of a rose tree, but without flowers or buds, save that in the centre is one fully blown white rose. Pentacles are disposed as on the points of a square; a rose in its centre. Symbols Sun and Capricorn above and below to represent the Decan.
>
> Assured material gain: success, rank, dominion, earthy power, completed but leading to nothing beyond. Prejudicial, covetous, suspicious, careful and orderly, but discontented. Little enterprise or originality. According to dignity as usual.
>
> Chesed of ה (Gain of money or influence: a present).
>
> Herein do כוקיה and מנדאל bear rule.

**Prompt of the kept painting** (after the style line):

> Lord of Earthly Power: a hand comes out of a cloud holding a branch of a rose tree with no flowers or buds, except one fully blown white rose at the centre. Four golden pentacles, discs of concentric rings with a small red cross at the centre, sit at the corners of a square around that rose. Solid, guarded, orderly.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652732518-kt6fzcsn88.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653988947-z7i394ulpc.svg)

### Lord of Defeat (Five of Swords)

**Book T (1912):**

> TWO Rayed Angelic Hands each holding two swords nearly upright, but falling apart of each other, right and left of the card. A third hand holds a sword upright in the centre as though it had disunited them. The petals of the rose, which in the four had been reinstated in the centre, are torn asunder and falling. Above and below are Venus and Aquarius for Decan.
>
> Contest finished and decided against the person; failure, defeat, anxiety, trouble, poverty, avarice, grieving after gain, laborious, unresting; loss and vileness of nature; malicious, slanderous, lying, spiteful and tale-bearing. A busybody and separator of friends, hating to see peace and love between others. Cruel, yet cowardly, thankless and unreliable. Clever and quick in thought and speech. Feelings of pity easily roused, but unenduring.
>
> Geburah of ו (Defeat, loss, malice, spite, slander, evil-speaking).
>
> Herein the Angels אניאל and חעמיה bear rule.

**Prompt of the kept painting** (after the style line):

> Lord of Defeat: two radiant angelic hands come out of clouds, each holding two steel swords nearly upright but falling apart from each other to right and left; a third hand from below holds a sword upright in the centre, as if it had split them. The petals of a red rose are torn apart and falling. Bleak grey sky. Defeat.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652458230-dv4ffdpsfjf.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653991632-qc2jtfwnvx.svg)

**Check:** One sword per hand.

### Lord of Earned Success (Six of Swords)

**Book T (1912):**

> TWO hands, as before, each holding two swords which cross in the centre. Rose re-established thereon. Mercury and Aquarius above and below, supported on the points of two short daggers or swords.
>
> Success after anxiety and trouble; self-esteem, beauty, conceit, but sometimes modesty therewith; dominance, patience, labour, etc.
>
> Tiphareth of ו (Labour, work, journey by water).
>
> Ruled by the Great Angels רהעאל and ייוהל.

**Prompt of the kept painting** (after the style line):

> Lord of Earned Success: two white radiant angelic hands come out of clouds, each holding two steel swords; the four blades cross in the centre and a red rose of five petals sits again at the crossing. Two short daggers at the top and bottom. Clear, cool blue sky. Success after trouble.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652483683-wc6ootltd5t.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653994446-wthqcpa7wyh.svg)

**Check:** One sword per hand.

### Lord of Unstable Effort (Seven of Swords)

**Book T (1912):**

> TWO Angelic Radiating Hands as before, each holding three swords. A third hand holds up a single sword in the centre. The points of all the swords "just touch" each other, the central sword not altogether dividing them.
>
> The Rose of the previous symbols of this suit is held up by the same hand which holds the central sword: as if the victory were at its disposal. Symbols of Moon and Aquarius.
>
> Partial success. Yielding when victory is within grasp, as if the last reserves of strength were used up. Inclination to lose when on the point of gaining, through not continuing the effort. Love of abundance, fascinated by display, given to compliments, affronts and insolences, and to spy upon others. Inclined to betray confidences, not always intentionally. Rather vacillatory and unreliable.
>
> Netzach of ו (Journey by land: in character untrustworthy).
>
> Herein rule the Great Angels הההאל and מעכאל.

**Prompt of the kept painting** (after the style line):

> Lord of Unstable Effort: two radiant angelic hands come out of clouds left and right, each holding three steel swords; a third hand from below holds up a single sword in the centre and, with the same hand, a red rose beside its hilt. The points of all seven swords just touch at the top. Unsettled grey-blue sky.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652504984-inqgaonykp.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653996966-ts21r9qr5j.svg)

**Check:** Five swords, not seven.

### Lord of Abandoned Success (Eight of Cups)

**Book T (1912):**

> A WHITE Radiating Angelic Hand, holding a group of stems of lotuses or water-lilies. There are only two flowers shown, which bend over the two central cups, pouring into them a white water which fills them and runs over into the three lowest, which later are not yet filled The three uppermost are quite empty. At the top and bottom of the card are symbols Saturn and Pisces.
>
> Temporary success, but without further results. Thing thrown aside as soon as gained. Not lasting, even in the matter in hand. Indolence in success. Journeying from place to place. Misery and repining without cause. Seeking after riches. Instability.
>
> Hod of ה (Success abandoned; decline of interest).
>
> The Angels ruling are ווליה and ילהיה.

**Prompt of the kept painting** (after the style line):

> Lord of Abandoned Success: a white radiant angelic hand holds a group of lotus stems. Only two lotus flowers bend over the two central cups and pour white water into them; these overflow into the three lowest cups, which are not yet full. The three uppermost cups are quite empty. Eight golden cups in all. Grey, waning light.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652219206-bd2rrof7mcv.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791653999895-0t3y778eq01f.svg)

**Check:** Six cups, not eight; two hands with vessels pour instead of two lotus flowers.

### Lord of Material Happiness (Nine of Cups)

**Book T (1912):**

> A WHITE Radiant Angelic Hand, issuing from a cloud holding lotus or water-lilies, one flower of which overhangs each cup; from it a white water pours. Cups are arranged in three rows of 3. Jupiter and Pisces above and below.
>
> Complete and perfect realization of pleasure and happiness, almost perfect; self-praise, vanity, conceit, much talking of self, yet kind and lovable, and may be self-denying therewith. High-minded, not easily satisfied with small and limited ideas. Apt to be maligned through too much self-assumption. A good and generous, but sometimes foolish nature.
>
> Yesod of ה (Complete success, pleasure and happiness, wishes fulfilled).
>
> Therein rule the Angels סאליה and עריאל.

**Prompt of the kept painting** (after the style line):

> Lord of Material Happiness: exactly nine large golden goblets in a simple grid of three rows with three goblets in each row, well spaced on a deep blue ground. A white radiant angelic hand comes out of a cloud at the top holding lotus stems; nine lotus flowers bend down, one over each goblet, and a thin stream of white water pours from each flower into its goblet. Rich, contented blue and gold.

**First prompt** (its painting was re-run once):

> Lord of Material Happiness: a white radiant angelic hand comes out of a cloud holding lotus or water-lily stems; one flower overhangs each of nine golden cups arranged in three rows of three, and white water pours from each flower into its cup. Rich, contented blue and gold.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653290477-19px0wlex69.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654003459-zvr07x7bzc.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652240615-z7zpm8ldtj.png)

**Check:** Re-run once (the first had about 25 cups); the kept one has ten.

**Redo:** 6th, with cups-07, cups-08, cups-10: the counts.

### Lord of Perfected Success (Ten of Cups)

**Book T (1912):**

> HAND, as usual, holding bunch of water-lilies or lotuses, whose flowers pour a white water into all the cups, which "all run over." The uppermost cup is held sideways by a hand, and pours water into the left-hand upper cup. A single lotus flower surmounts the top cup, and is the source of the water that fills it. Above and below the symbols Mars and Pisces.
>
> Permanent and lasting success and happiness, because inspired from above. Not so sensual as "Lord of Material Happiness," yet almost more truly happy. Pleasure, dissipation, debauchery, quietness, peacemaking. Kindness, pity, generosity, wantonness, waste, etc., according to dignity.
>
> Malkuth of ה (Matter settled: complete good fortune).
>
> Herein the Great Angels עשליה and מיהאל rule.
>
> [This is not such a good card as stated. It represents boredom, and quarrelling arising therefrom; disgust springing from too great luxury. In particular it represents drug-habits, the sottish excess of pleasure and the revenge of nature.]

**Prompt of the kept painting** (after the style line):

> Lord of Perfected Success: a hand holds a bunch of lotus stems whose flowers pour white water into ten golden cups, which all run over. At the very top one cup is held sideways by a hand and pours water into the upper left cup; a single lotus flower above that top cup is the source of its water. Abundant, overflowing blue and gold.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652255891-6x3jfoko3yo.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654040658-idlx6ptv8jg.svg)

**Check:** Eleven cups in a pyramid; the sideways cup pours into the lotus.

### Lord of Dominion (Two of Wands)

**Book T (1912):**

> A WHITE Radiating Angelic hand, issuing from clouds, and grasping two crossed wands. Flames issue from the point of junction. On two small wands above and below, with flames of five issuing therefrom, are the symbols of Mars and Aries for the Decan.
>
> Strength, domination, harmony of rule and of justice. Boldness, courage, fierceness, shamelessness, revenge, resolution, generous, proud, sensitive, ambitious, refined, restless, turbulent, sagacious withal, yet unforgiving and obstinate.
>
> Chokmah of י (Influence over others, authority, power, dominion).
>
> Therein the Angels והואל and דניאל bear rule.

**Prompt of the kept painting** (after the style line):

> Lord of Dominion: a white radiant angelic hand comes out of clouds and grasps two crossed wooden wands at their centre. Flames burst from the point where they cross. Above and below, two short wands with five small flames each. Red and gold fire against a pale sky. Strength and dominion.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651744508-g6q3or9hqj8.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654043634-kbhqmnz95b.svg)

**Check:** The hand lies on the wands rather than grasping them.

### Lord of Established Strength (Three of Wands)

**Book T (1912):**

> A WHITE Radiating Angelic Hand, as before, issuing from clouds and grasping three wands in the centre (two crossed, the third upright). Flames issue from the point of junction. Above and below are the symbols Sun and Aries.
>
> Established force, strength, realization of hope. Completion of labour. Success after struggle. Pride, nobility, wealth, power, conceit. Rude self-assumption and insolence. Generosity, obstinacy, etc.
>
> Binah of י (Pride, arrogance, self-assertion).
>
> Herein rule the Angels ההשיה and עממיה.
>
> [This card is much better than as described.]

**Prompt of the kept painting** (after the style line):

> Lord of Established Strength: a white radiant angelic hand comes out of clouds and grasps three wooden wands at their centre: two crossed and the third upright. Flames burst from the point where they cross. Red and gold fire against a pale sky. Established strength.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651772686-5txag7ilam8.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654046690-ydtj4xlwckq.svg)

**Check:** The hand grasps only the upright wand.

### Lord of Perfected Work (Four of Wands)

**Book T (1912):**

> TWO White Radiating Angelic Hands, as before, issuing from clouds right and left of the card and clasped in the centre with the grip of the First Order, holding four wands or torches crossed. Flames issue from the point of junction. Above and below are two small flaming wands, with the symbols of Venus and Aries representing the Decan.
>
> Perfection or completion of a thing built up with trouble and labour. Rest after labour, subtlety, cleverness, beauty, mirth, success in completion. Reasoning faculty, conclusions drawn from previous knowledge. Unreadiness, unreliable and unsteady through over-anxiety and hurriedness of action. Graceful in manner, at times insincere, etc.
>
> Chesed of י (Settlement, arrangement, completion).
>
> Herein are ננאאל and ניתהל Angelic rulers.

**Prompt of the kept painting** (after the style line):

> Lord of Perfected Work: two white radiant angelic hands come out of clouds on the left and right and clasp each other at the centre in a firm grip, holding four crossed wooden wands. Flames burst from the point where they cross. Above and below, two short flaming wands. Red and gold fire against a pale sky. Completion and rest after labour.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791651798995-96va9fg0dgp.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654049322-gx5ynnlmddc.svg)

### Lord of Material Trouble (Five of Pentacles)

**Book T (1912):**

> A WHITE Radiant Angelic Hand issuing from clouds, and holding a branch of the white rose tree, but from which the roses are falling, and leaving no buds behind. Five Pentacles similar to the Ace. Above and below are Mercury and Taurus.
>
> Loss of money or position. Trouble about material things. Labour, toil, land cultivation; building, knowledge and acuteness of earthly things, poverty, carefulness, kindness; sometimes money regained after severe toil and labour. Unimaginative, harsh, stern, determined, obstinate.
>
> Geburah of ה (Loss of profession, loss of money, monetary anxiety).
>
> Herein the angels מבהיה and פניאל rule.

**Prompt of the kept painting** (after the style line):

> Lord of Material Trouble: a white radiant angelic hand comes out of clouds and holds a branch of a white rose tree from which the roses are falling, leaving no buds behind. Five golden pentacles, discs of concentric rings with a small red cross at the centre. Cold, bare, wintry grey ground.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652760203-iljj0tcqd1g.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654051977-5nctzb5c2yd.svg)

**Check:** Roses still on the branch.

### Lord of Material Success (Six of Pentacles)

**Book T (1912):**

> A WHITE Radiant Angelic Hand holding a rose branch with white roses and buds, each of which touches a Pentacle. Pentacles are arranged in two columns of three each *(a figure on the printed page: six pentacles in two columns of three)*. Above and below are the symbols Taurus and Moon of the Decan.
>
> Success and gain in material undertakings. Power, influence, rank, nobility, rule over the people. Fortunate, successful, liberal and just.
>
> If ill dignified, may be purse-proud, insolent from excess, or prodigal.
>
> Tiphareth of ה (Success in material things, prosperity in business).
>
> Herein rule the Angels נממיה and יילאל.

**Prompt of the kept painting** (after the style line):

> Lord of Material Success: exactly six golden discs, each with concentric rings and a small red cross at its centre, in two columns of three. A white radiant angelic hand at the bottom holds a rose branch climbing between the columns; its white roses and rosebuds each touch one disc. Plain warm ochre ground, prosperous light.

**First prompt** (its painting was re-run once):

> Lord of Material Success: a white radiant angelic hand holds a rose branch with white roses and buds, each touching one of six golden pentacles, discs of concentric rings with a small red cross at the centre, arranged in two columns of three. Warm, prosperous light.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791653492047-gurfmxkxvxi.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654054552-yjxxu3g5zne.svg) · earlier attempts: [1](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652791025-vzaovhonqk.png)

**Check:** Re-run once: the first had eight discs with six-pointed stars.

### Lord of Success Unfulfilled (Seven of Pentacles)

**Book T (1912):**

> A WHITE Radiating Angelic Hand issuing from a cloud, and holding a white rose branch. Seven Pentacles arranged like the geomantic figure Rubeus. There are only five buds, which overhang, but do not touch the five uppermost Pentacles. Above and below are the Decan symbols, Saturn and Taurus respectively.
>
> Promises of success unfulfilled. (Shewn, as it were, by the fact that the rosebuds do not come to anything.) Loss of apparently promising fortune. Hopes deceived and crushed. Disappointment, misery, slavery, necessity and baseness. A cultivator of land, and yet a loser thereby. Sometimes it denotes slight and isolated gains with no fruits resulting therefrom, and of no further account, though seeming to promise well.
>
> Netzach of ה (Unprofitable speculations and employments; little gain for much labour).
>
> Therein הרחאל and מצראל are ruling Angels.

**Prompt of the kept painting** (after the style line):

> Lord of Success Unfulfilled: a white radiant angelic hand comes out of a cloud and holds a white rose branch. Seven golden pentacles, discs of concentric rings with a small red cross at the centre, are arranged in rows of two, one, two and two. There are only five rosebuds, which hang over the five uppermost pentacles but do not touch them. A waiting, disappointed mood.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652822226-m6yv2jvwey.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654056998-ulu86yx35xl.svg)

**Check:** Seven roses, not five buds.

### Lord of Shortened Force (Eight of Swords)

**Book T (1912):**

> FOUR White Radiant Angelic Hands issuing from clouds, each holding two swords, points upwards; all the points touch near the top of the card. Hands issue, two at each bottom angle of the card. The pose of the other sword symbols is re-established in the centre. Above and below are the Decan symbols Jupiter and Gemini.
>
> Too much force applied to small things: too much attention to detail at the expense of the principal and more important points. When ill dignified, these qualities produce malice, pettiness, and domineering characteristics. Patience in detail of study; great care in some things, counterbalanced by equal disorder in others. Impulsive; equally fond of giving or receiving money or presents; generous, clever, acute, selfish and without strong feeling of affection. Admires wisdom, yet applies it to small and unworthy objects.
>
> Hod of ו (Narrow, restricted, petty, a prison).
>
> Therein rule the Angels ומבאל and יההאל.

**Prompt of the kept painting** (after the style line):

> Lord of Shortened Force: four white radiant angelic hands come out of clouds, two at each lower corner of the card, each holding two steel swords points upward; all eight points touch near the top of the card. A red rose of five petals sits at the centre where the blades cross. Narrow, constricted feeling.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652541194-upy0c4sdadh.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654059151-zdi8w0wg3z.svg)

**Check:** One sword per hand; the points do not meet.

**Redo:** 5th, swords 4 to 10 as a set: every one gives each hand one sword. A reference image of the right layout (or a drawn layout) would help more than another prompt.

### Lord of Despair and Cruelty (Nine of Swords)

**Book T (1912):**

> FOUR Hands, as in the preceding figure, hold eight swords nearly upright, but with the points falling away from each other. A fifth hand holds a ninth sword upright in the centre, as if it had struck them asunder. No rose at all is shewn, as if it were not merely cut asunder, but utterly destroyed. Above and below are the Decan symbols Mars and Gemini.
>
> Despair, cruelty, pitilessness, malice, suffering, want, loss, misery. Burden, oppression, labour, subtlety and craft, dishonesty, lying and slander.
>
> Yet also obedience, faithfulness, patience, unselfishness, etc. According to dignity.
>
> Yesod of ו (Illness, suffering, malice, cruelty, pain).
>
> Therein do ענואל and מחיאל bear rule.

**Prompt of the kept painting** (after the style line):

> Lord of Despair and Cruelty: four hands come out of clouds at the lower corners and hold eight steel swords nearly upright, their points falling away from each other; a fifth hand holds a ninth sword upright in the centre, as if it had struck them apart. No rose anywhere. Dark night sky. Despair and cruelty.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652572306-4v5v4yjjp0k.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654061942-wkqrqf01ix.svg)

### Lord of Ruin (Ten of Swords)

**Book T (1912):**

> FOUR hands holding eight swords, as in the preceding symbol; the points falling away from each other. Two hands hold two swords crossed in the centre, as though their junction had disunited the others. No rose, flower or bud, is shewn. Above and below are Sun and Gemini, representing the Decan.
>
> Almost a worse symbol than the Nine of Swords. Undisciplined, warring force, complete disruption and failure. Ruin of all plans and projects. Disdain, insolence and impertinence, yet mirth and jollity therewith. A marplot, loving to overthrow the happiness of others; a repeater of things; given to much unprofitable speech, and of many words. Yet clever, eloquent, etc., according to dignity.
>
> Malkuth of ו (Ruin, death, defeat, disruption).
>
> Herein the Angels דמביה and מנקאל reign.

**Prompt of the kept painting** (after the style line):

> Lord of Ruin: four hands come out of clouds and hold eight steel swords whose points fall away from each other; two more hands hold two swords crossed in the centre, as though their crossing had broken the others apart. No rose, flower or bud. A ruined dark red and black sky.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652603992-nt0ysycgdjj.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654064581-76aczx6bnc8.svg)

**Check:** Four swords, not ten.

### Lord of Love (Two of Cups)

**Book T (1912):**

> A WHITE Radiant Hand, issuant from the lower part of the card from a cloud, holds lotuses. A lotus flower rises above water, which occupies the lower part of the card rising above the hand. From this flower rises a stem, terminating near the top of the card in another lotus, from which flows a sparkling white water, as from a fountain. Crossed on the stem just beneath are two dolphins, Argent and Or, on to which the water falls, and from which it pours in full streams, like jets of gold and silver, into two cups; which in their turn overflow, flooding the lower part of the card. Venus and Cancer above and below.
>
> Harmony of masculine and feminine united. Harmony, pleasure, mirth, subtlety: but if ill dignified — folly, dissipation, waste, silly actions.
>
> Chokmah of ה (Marriage, love, pleasure).
>
> Therein rule the Angels אועאל and חבויה.

**Prompt of the kept painting** (after the style line):

> Lord of Love: a white radiant hand comes out of a cloud at the bottom of the card and holds lotus stems. A lotus flower rises above water that fills the lower part of the card; from it a stem climbs to another lotus near the top, from which sparkling white water flows like a fountain. Crossed on the stem just beneath are two dolphins, one silver and one gold; the water falls on them and pours in streams like jets of gold and silver into two golden cups, which overflow and flood the lower part of the card.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652063373-u5ndr43s99o.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654106298-g26g9re1bkc.svg)

### Lord of Abundance (Three of Cups)

**Book T (1912):**

> A WHITE Radiating Hand, as before, holds a group of lotuses or water-lilies, from which two flowers rise on either side of, and overhanging the top cup; pouring into it the white water. Flowers in the same way pour white water into the lower cups. All the cups overflow; the topmost into the two others, and these upon the lower part of the card. Cups are arranged in an erect equilateral triangle. Mercury and Cancer above and below.
>
> Abundance, plenty, success, pleasure, sensuality, passive success, good luck and fortune; love, gladness, kindness, liberality.
>
> Binah of ה (Plenty, hospitality, eating and drinking, pleasure, dancing, new clothes, merriment).
>
> Therein the Angels ראהאל and יבמיה are lords.

**Prompt of the kept painting** (after the style line):

> Lord of Abundance: a white radiant hand holds a group of lotuses or water-lilies. Two flowers rise on either side of the top cup and pour white water into it; other flowers pour white water into the two lower cups. Three golden cups stand in an upright triangle, all overflowing: the top cup into the two below, and these onto the lower part of the card. Joyful, abundant blue water.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652091054-i5ctoozqv5m.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654109301-noz4784wqx.svg)

**Check:** The hand holds a cup, not the lotus group.

### Lord of Blended Pleasure (Four of Cups)

**Book T (1912):**

> FOUR cups: the two upper overflowing into the two lower, which do not overflow. An Angelic Hand grasps a branch of lotus, from which ascends a stem bearing one flower at the top of the card, from which the white water flows into the two upper cups. From the centre two leaves pass right and left, making, as it were, a cross between the four cups. Above and below are the symbols Moon and Cancer for the Decan.
>
> Success or pleasure approaching their end. A stationary period in happiness, which may, or may not, continue. It does not mean love and marriage so much as the previous symbol. It is too passive a symbol to represent perfectly complete happiness. Swiftness, hunting and pursuing. Acquisition by contention: injustice sometimes; some drawbacks to pleasure implied.
>
> Chesed of ה (Receiving pleasure or kindness from others, but some discomfort therewith).
>
> Therein rule the great Angels הייאל and מומיה.

**Prompt of the kept painting** (after the style line):

> Lord of Blended Pleasure: four golden cups, two above and two below. An angelic hand grasps a lotus branch from which a stem rises to one flower at the top of the card; from that flower white water flows into the two upper cups, which overflow into the two lower cups, which do not overflow. From the centre two leaves pass right and left, making a cross between the four cups.

**Left out / changed:** The decan's planet and sign, which Book T sets above and below, are left out of the painting (image models garble astrological glyphs) and set as real text under the card instead.

**Result:** [painting](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1791652121779-ziw1xaczcos.png) · [SVG](https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammars/1791654112174-zt3k53356gk.svg)
