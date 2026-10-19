# Book T parts

118 SVG parts for the Book T deck's fourth picture set, the **full imagery** (`tarot/book-t/full-imagery/`). Each file holds one `<g id="part">` drawn around its own origin (the comment in the file says where the origin is: a fist's centre, a wand's middle, a sword's grip, a figure's feet, a beast's body). `currentColor` is the part's one changeable colour (a cloud, a robe, a horse's coat); `data-color` is its default.

- **Hands and clouds**: `hand` (the white radiating angelic hand issuing from clouds, grasping), `hand-palm` (supporting on its palm), `grip` (two hands from clouds right and left, clasped in the grip of the First Order), `cloud`, `cloud-bank`
- **The suits**: `wand`, `wand-small`, `wand-heavy`, `club` (the Ace of Wands), `club-heavy`, `sword`, `dagger`, `cup`, `cup-full`, `cup-overflow`, `pentacle` (Book T's: five circles, a white centre with a red Greek cross, twelve white rays), `maltese-wings`, `serpent-8`, `crown-radiant`, `olive-branch`, `palm-branch`
- **Flowers, fire, water, land**: `rose`, `rose-rayed`, `rosebud`, `petal`, `leaf`, `lotus`, `lily-pad`, `flame`, `flame-burst`, `flames-ground`, `fountain`, `water-calm`, `waves`, `ground`, `corn`, `flowers`, `grove`, `smoke`, `drop`, `path-road`
- **Figures** (symbols, never faces): `figure`, `figure-seated`, `rider`, `hair-long`, `hood`, `head-profile`, `mantle`, `mantle-tiger`, `wings`, `butterfly-wings`, `crown`, `helmet-winged`, `helmet-corinthian`, `throne`, `chariot`
- **Beasts and crests**: `horse`, `lion`, `leopard`, `eagle`, `bull`, `goat`, `ibis`, `dog`, `dolphin`, `crab`, `crayfish`, `serpent`, `turtle`, `swan`, `peacock`, `crest-wings`, `head-horse`, `head-lion`, `head-leopard`, `head-tiger`, `head-stag`, `head-goat`, `head-bull`, `head-ram`, `head-child`, `head-angel`, `head-medusa`, `head-severed`, `star6`
- **Things held**: `rod`, `hexagram`, `pentagram`, `cube`, `orb`, `orb-cross`, `disk`, `sickle`, `altar`, `scales`, `lantern`, `staff`, `scythe`, `vessel`, `trumpet`, `bag`, `cross-triple`, `horns`, `wheat`
- **For the Keys**: `tower`, `lightning`, `pillar`, `table`, `wheel`, `tau`, `tomb`, `wall`, `wreath`, `cube-altar`, `star8`, `star`, `moon-crescent`, `sun-rayed`

**Where they come from.** Drawn for this site (October 2026) as hand-written SVG path data. No font, icon set or image was copied or traced, so no outside licence applies.

**Licence.** CC BY-SA 4.0, like the rest of the Book T deck (`tarot/book-t`). Credit: PlayfulProcess, recursive-tarot.

**How they are used.** `scripts/build_book_t_full_imagery.py` places them, with the glyphs in `../glyphs/`, by each card's spec in `../full-imagery/compositions.json` (the Book T sentence it follows, and its layers). To change a part, edit its file here; to change a card, edit its spec; then run that script and `scripts/build_book_t_page.py`. Its `--check` runs in `scripts/check_all.py`.
