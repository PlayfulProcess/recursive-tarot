# The family replan — one architecture, three skies (July 2026)

Written at the builder's request after the publish pass, the iching build, and the astro
sync — a full re-plan with approval gates. Nothing below Phase A is started without a go.
Supersedes the astro half of ASTRO-ICHING-CONTENT-2026-07.md; the iching half stands.

## 1. The insight the last week surfaced

All three domains turned out to run **one architecture**: a small structured space of
constant objects, read through variable lenses.

| Domain | The constant (space) | The variable (lens/time) | Format |
|---|---|---|---|
| Tarot | the card | the deck / the voice | static museum — mature, stays as-is |
| I Ching | the hexagram | the book across centuries | Next.js app — because its meaning structures are *combinatorial* (trigram matrix, moving-line paths) and an app renders intrinsic structure best |
| Astrology | **the sky-object** | **the tradition** | the replan below |

The alignment convention is identical everywhere and already proven twice: shared item
ids across grammars, so "the same thing through many eyes" costs a viewer nothing.
Tarot's meta-grammar did it first; iching's book rail generalized it; astro inherits it.

## 2. The astro re-vision: from "astrology repo" to the observatory

The builder's brief, kept in its own words: show *how humanity has looked into the sky
and created meaning — physically, metaphysically, relationally — with NASA actual data of
different skies in different times, and how we cannot flatten that into "there is an
astrology that is true."* The structure itself must make flattening impossible. Three
registers, held apart and cross-linked, never merged:

**(a) The referents — the sky as it physically is.** New baseline grammars of the
*objects themselves*: `planets-as-objects`, `bright-stars`, `constellations-as-regions`
(the IAU's 88, as sky-regions with their history). Sections: Scene = what the object
physically is (sourced astronomy); Research note = discovery/observation history. Images
from NASA (public domain; the `nasa_image_search` MCP tool license-checks for us). This
register makes the honesty argument *visible*: precession as the flagship exhibit — the
signs and the constellations have drifted apart by ~24° since the Hellenistic frame was
fixed; "different skies in different times" is not a gotcha, it is the actual history.

**(b) The lenses — the traditions (already 80% built).** The 15 existing grammars are
this register: Mesopotamian omen-craft → Ptolemy → Jyotiṣa → Lilly → Alan Leo → modern
canonical → Tarnas → Proctor's skeptics — each faithful in its own terms, per the house
rule. What changes: tradition grammars adopt the shared-id convention against the
referent grammars (the item for Mars in every tradition carries the same id root), so a
viewer can hold Mars still and page through three thousand years of readings — the iching
book-rail move, pointed at the sky. The one gap that stays on the roadmap: a dedicated
Hellenistic practice set (research-first, its own session).

**(c) The practice — casting, playfully.** The builder's sketch, deferred but designed
for: *a spread might be a trine* — casting positions drawn from the sky's own geometry
(trine, square, the twelve houses as a wheel-spread) instead of a shuffle; charts of a
moment, a place, a relationship, a country, a community as **emergences**. The three
`casting-*` sequence grammars are the seeds. Real charts need ephemeris computation —
genuinely tractable in this stack (open ephemerides + Python; the repos already run
Python gates), but it is a wing, not a foundation.

## 3. The new deck: cosmological beings

The builder's ask, verbatim in spirit: a grammar of **black holes and actual stars we can
think through as we wake up as cosmological beings.** Working title `the-actual-sky` (or
`cosmological-beings`). ~20–30 items: Sagittarius A*, M87*, Betelgeuse, the Crab pulsar,
the Pleiades, Proxima and its planet, Cygnus X-1, the CMB itself… Per item: Scene = the
verified astrophysics, plainly told; Symbol = deliberately open — an *invitation to
relate*, not a meaning system (we are the first generations who can sit with these
objects at all; the deck's honesty is that no tradition owns them yet); Research note =
sourced discovery history; NASA imagery. The autonomy floor unchanged: relate, never obey.
This is the one place the project *creates* a lens rather than curating one — flagged as
exactly that, the project's own voice, like tarot's Ecosystem.

## 4. What we are best at, and the humble first step

The builder's own assessment, adopted as the plan's spine: this team's strengths are the
**historiographic and scientific registers with the code already built** — verified
dossiers, public-domain data processing, reproducible build scripts, honest gates. So the
order of work follows tractability, not ambition:

**Phase A — reconcile & publish (ready now, cheap).**
1. Pull the builder's app-side iching grammar cleanup back into the repo (the app copies
   were corrected; export → repo, regenerate mirrors, re-verify — the astro two-way-sync
   move). The repo stays canon.
2. Publishing decisions: which of the 15 astro grammars and 2 iching books go public
   (`set_grammar_visibility`, one call each; then fill `_public_now` so the channels
   pages light up).
3. Astro historiography polish: sweep the 7 newly exported grammars through the tarot
   formatting contract (cheap-model agents, same guardrails).

**Phase B — the referent register (astro's next real build).**
Research-first dossiers, then `planets-as-objects` + `bright-stars` +
`constellations-as-regions`, NASA imagery, shared-id adoption in the tradition grammars,
and the **precession exhibit** as a page (the "different skies in different times" proof,
rendered).

**Phase C — the cosmological deck.** Dossier per object (adversarially verified, the
why-tarot-works method), then the deck, then narration/imagery. The project's first
created lens; take it slowly and say what it is.

**Phase D — playful casting.** Trine/wheel spreads as sequence grammars on the existing
Caster machinery; no ephemeris yet — sky-shaped shuffles, honestly labeled.

**Phase E — charts as emergences.** Ephemeris-computed charts of a time/place/bond;
app-shaped (recursive.eco proper, or an astro app repo cloned from the starter as iching
was). Not before D proves the appetite.

## 5. Format decisions (settled unless revisited)

- **Tarot**: static museum, untouched. Its publish pass continues independently
  (Phase 4 spot-audit of Scene/Symbol whenever convenient).
- **I Ching**: Next.js app is the right home and stays; static reference viewers remain
  as spec; recursive.eco serves generic viewing (no Pages surface).
- **Astro**: stays thin/static through B–D. The moment E begins, its practice wing goes
  app-shaped rather than bending the static site — decision deferred until then.
- **recursive.eco**: remains the generic renderer + channel host for everything; domain
  sites build only what is domain-specific.

## 6. Approval gates

A is safe and reversible throughout (publishing is the only outward step and is itemized
per grammar). B, C, D, E each start only on an explicit go, and each begins with its
research dossier, not its code.
