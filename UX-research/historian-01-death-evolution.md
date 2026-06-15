# A visitor's report: tracing the **Death** card through tarot history

*Written by a curious site visitor interested in the history of tarot — not a
developer. I came to tarot.recursive.eco wanting to understand how the cards
evolved: where they came from, and how one card in particular — **Death** — was
imagined at the beginning and at the end. Below: what I learned, where the site
helped, the bugs I hit, and what I still couldn't figure out.*

---

## Part 1 — What I came to find out, and what the site told me

### Did tarot really only emerge in the Renaissance? — **Yes, and the site says so clearly.**

I half-expected the usual "ancient Egyptian wisdom" story. The site dismantles it.
From the **Tree of Tarot** overview: *"Tarot begins in the courts of northern
Italy in the 1440s as a luxury card game for aristocrats."* The **Roots** branch is
explicit: the founding decks are *"hand-painted luxury objects commissioned by the
ruling dynasties of Milan and Ferrara in the 1440s … objects of court prestige."*

And crucially — every early card carries a **Tradition Note** that says the quiet
part out loud:

> "These cards were made to play a game — the Italian *trionfi* / *tarocchi* card
> game — not for divination, which arrived centuries later."

So the site let me *find out*, on my own, the thing I most wanted to confirm: tarot
is a **Renaissance card game**, and the fortune-telling/esoteric meaning is a
**later overlay**. That's a strong, honest editorial spine.

### How was Death represented at the beginning vs. the end?

This is where the site genuinely taught me something. Tracing Death from the oldest
deck to the newest, the **image itself oscillates**:

| Year | Deck | How Death is drawn | What it "means" (per the card) |
|---|---|---|---|
| **1442** | Cary-Yale Visconti | **Skeleton on horseback with a great bow**, riding over fallen bodies on gold ground — "the dignity of full gold-ground treatment … a noble rider, not a grotesque" | A *Petrarchan Triumph of Death*; an allegory, no divinatory meaning |
| 1451–1475 | Visconti-Sforza / Charles VI | Gaunt skeleton, "the great equaliser of the danse macabre" | The great levelling — historical/iconographic only |
| **1760** | Marseille (Conver) | **Skeleton on foot with a scythe**, mowing a field of severed heads, hands, feet — including a **crowned** head. **The card has number XIII but no name** | Still a game card; "upright/reversed meanings are a later overlay" |
| 1781 | Court de Gébelin | *same Marseille image* | First esoteric reading: Death is "unnumbered because it belongs to no rank — the great equalizer the *Egyptians* placed among the trumps" (an invented pedigree) |
| 1889 | Oswald Wirth | scythe + sprouting field | "transformation, not extinction" — new plants grow among the cut forms |
| **1909** | Golden Dawn / RWS | **Skeleton in black armor back on a white horse**, banner with a white rose, a bishop pleading, sunrise between two towers | Scorpio / Hebrew **Nun** / Path 24 on the Tree of Life — "not annihilation but transformation" |

**My finding, which the site's data supports but doesn't state in one place:** Death's
posture goes **mounted → on-foot → mounted** (bow → scythe → banner) over five
centuries, while its *meaning* travels from **plain mortal allegory → great
leveller → esoteric transformation**. The "name" disappears in the Marseille
tradition (XIII, blank) and that very blankness later gets *reinterpreted* by
Gébelin as cosmically significant. The card stayed visually recognisable for 500
years while its meaning was completely rewritten — which is exactly the "evolving
tradition that remains recognisably itself" the Tree of Tarot promises.

The site holds **16 distinct Death cards** (1442→1909), each with sourced notes and
GitHub-linked research dossiers. As evidence, it's excellent.

---

## Part 2 — How the site served me (views I used)

- **Lenses → Synopsis** (one card across decks, side by side): the single most
  useful view for my question. I picked "Death" and read six traditions in
  parallel.
- **Lenses → Provenance ribbon**: genuinely revelatory. It plots Death's depictions
  (1451, 1475, 1760, 1781, 1888) against its commentaries (Gébelin 1781, Papus
  1889, Waite 1911, Wirth 1927). Seeing **every "meaning" layer cluster after 1781**
  made the "divination is a late overlay" point *visually*, better than any
  paragraph.
- **Card detail**: native sections first, then the dated later-commentary at the
  end — so I read the card's own voice before the occult overlay. Good ordering.

---

## Part 3 — UX bugs & friction I hit (as a non-technical visitor)

1. **Synopsis columns each scroll independently and clip the text.** To compare,
   say, everyone's "Scene," I had to scroll six separate little boxes, and the text
   cut off mid-sentence ("…rides over falle…"). I wanted to compare *the same
   section across decks*, but the layout is deck-columns, so the comparison I
   actually wanted (one section, all decks) isn't possible. **A "compare by section"
   toggle (transpose the grid) would fix this.**
2. **The Lenses page is locked to 6 decks.** The site *has* 16 Death cards (Etteilla
   1789/1838/1865, Minchiate 1506, Bologna 1660, Belgian, Viéville, Paris…), but the
   Synopsis/Ribbon/Multiples only ever show the same fixed six. As a researcher I
   felt I was seeing a *third* of the evidence with no way to add the rest. **The
   prototypes need the same "✦ Decks" picker the other views have.**
3. **Ribbon labels collide on the right.** Around 1888–1927 the ticks (native 1888,
   Papus 1889, Waite 1911, Wirth 1927) overlap and the labels overprint each other —
   readable but messy. Two events in the same year (1781 image + 1781 Gébelin) draw
   on top of each other.
4. **Ribbon image in Synopsis scrolls away.** The card image sits at the top of each
   column and scrolls out of view as you read; I lost the picture I was reading
   about. The image should stay pinned.
5. (Already fixed during my visit, noting for completeness) the earlier "Show as →
   section" text in the card grid was an unreadable scroll-in-a-box; it now clamps
   cleanly.

None of these are blockers — I still got my answer — but #1 and #2 are the ones
that limited my actual research.

---

## Part 4 — Things I still couldn't understand (candidate gaps in the *grammars*)

These are content questions the site raised but didn't resolve. They may be data
gaps rather than bugs:

1. **Petrarchan Triumph vs. *danse macabre* — which is it?** The Cary-Yale Scene
   says Death is a Petrarchan *Triumph*, explicitly **"not the macabre grotesquerie
   of the danse macabre."** But the Visconti-Sforza "History" calls the very same
   era's Death **"the great equaliser of the *danse macabre*."** So two of the
   oldest decks are filed under two different visual lineages. Is that a real
   art-historical distinction (refined court allegory vs. popular death-dance), or
   an inconsistency between two notes? I couldn't tell, and I'd want the site to
   reconcile them.
2. **Why does Death lose its name?** The Marseille note says the blank title is "a
   Marseille convention." Gébelin says it's blank "because Death belongs to no
   rank." These are a *descriptive* and an *esoteric* explanation of the same fact,
   presented side by side without saying that the convention came **first** and the
   cosmic rationale was attached **later**. A one-line bridge ("the blank was a
   printing convention; Gébelin retro-fitted meaning onto it") would close the loop.
3. **The mounted → on-foot → mounted oscillation is never narrated.** Each card has
   a "what changed vs. its parent" research note, but no view chains them into the
   single evolution story I had to assemble by hand. The data is all there; the
   *thread* isn't. (This is arguably what the genealogy view should do for a single
   card.)
4. **The bow.** The earliest Death (Cary-Yale 1442) carries a **bow**, not a scythe.
   Nothing explains when or why the scythe replaced it. For someone tracing the
   card's evolution, that's the most striking early detail and it's left hanging.

---

## Part 5 — For the team to assess (my visitor's verdict)

- **The history is here and it's honest.** The Renaissance-origin / late-divination
  thesis is reachable and well-sourced. I trust this site more than most tarot
  sites precisely because it keeps saying "this meaning was added later."
- **The Synopsis and Ribbon are the right tools** for "how did a card evolve" — they
  just need (a) a deck picker and (b) section-transpose to be genuinely powerful.
- **A few grammar reconciliations** (danse-macabre vs. Triumph; the name-loss
  bridge; the bow→scythe transition) would turn good per-card notes into a coherent
  *evolution narrative*, which is what a history-minded visitor actually wants.

*— end of visitor report*
