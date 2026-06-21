# Design — Information Architecture: journeys × provenance × destinations

**Status:** proposal (planning, 2026-06-21). The map that sits *above*
[`USER-JOURNEYS.md`](../use-cases/USER-JOURNEYS.md),
[`DESIGN-two-wings-provenance.md`](DESIGN-two-wings-provenance.md) (+ REVIEW + v2),
and [`DESIGN-framework-extraction.md`](DESIGN-framework-extraction.md). It supersedes none —
it ties them into one structure.
**Author:** PlayfulProcess

## The core idea: three layers, not two competing maps

The "organize by user journeys" idea and the "two wings / provenance" idea are **not rivals** —
they answer different questions and live on different layers:

| Layer | Answers | Owned by |
|---|---|---|
| **1 · Navigation** | "Where do I go?" — by **intent** | **User journeys** (the four doors) |
| **2 · Destinations** | "What can I do here?" — the hubs you land in | both (tabs = journeys' endpoints) |
| **3 · Labeling** | "What am I looking at?" — evidence vs interpretation | **Two-wings provenance** (cross-cutting) |
| **Engine** | "How is this reusable for the I Ching?" | **Framework-extraction** |

**The one rule that keeps them from colliding:** *journeys are the primary navigation;
provenance is labeling **within** a destination, never a top-level menu.* The visitor never has
to pick "Record vs Living" at the front door — the bands appear once they're inside a listing.
This protects the historian's "record held apart" and the practitioner's "equal peer" at once.

## Layer 1 — the four doors (intent-first)

A tidy parallel of **role + activity**. (Personas from USER-JOURNEYS; "Lover" → **Player**, since
the project's thesis is *tarot was a game first* — the honest front door is to play.)

| Persona | Door | Home | Journeys served |
|---|---|---|---|
| **Player** | **Play** | `play.html` — games · draw · browse · **design your own deck** | J1 |
| **Historian** | **The history** | sources hub · genealogy · timeline · courses | J2 |
| **Practitioner** | **Practice** | **The Golden Dawn Path** · living decks · Cast | J3 |
| **Contributor** | **Contribute** | the 5-rung ladder (in-app → MCP) | J4 · J5 · J6 |

"Curious" is a *motive*, not a door — it's why a Player shows up; the curious-but-serious
graduate Player → Historian or Practitioner. Keeping personas as parallel **roles** (not mixing
in a state like "curious") is what makes the nav legible.

## Layer 2 — destinations, mapped to door AND band

| Destination | Door(s) | Provenance band | Status |
|---|---|---|---|
| Card pages + Cast/Draw | Play / Practice | per-deck badge | exists (badge UI todo) |
| **Design your own deck** | Play | lands in **Living** (private draft) | scoped → [`DESIGN-player-deck-designer.md`](DESIGN-player-deck-designer.md) |
| Games (Tarocchino, Trionfi…) | Play | **Record** (how cards were *played*) | exists |
| Sources hub (books + people) | The history | **reference** | exists (`pages/sources.html`) |
| Genealogy · Timeline · Tree | The history | **Record only, by definition** | exists |
| Courses | The history / Contribute | reference | exists |
| **The Golden Dawn Path** | Practice | **Living** (esoteric practice) | design TODO (J3's missing endpoint) |
| **Rituals** (pathworking the Tree via the trumps) | Practice | **Living** | design TODO |
| Contribute ladder | Contribute | owner-controlled | exists |

Two structural beauties worth preserving:
- **Games (Record) ↔ Rituals (Living)** — the same parallel serves a *journey* (Player vs
  Practitioner) *and* a *band* (how cards were played vs how occultists used them). One move,
  both models satisfied.
- **The Golden Dawn Path is the concrete J3 destination** USER-JOURNEYS flagged as missing.

## Layer 3 — provenance labeling (cross-cutting)

Per the two-wings **v2 agreed conclusion**: `provenance: record | living | reference`, boolean
`draft` (early/incomplete — *never* a proxy for "interpretive/non-Western"), **peer** bands of
equal weight with a framing line *above both* (not below-the-line/collapsed), and a reworded
manifesto. Every card/deck/destination wears its badge regardless of which door you came through.

## Engine — framework-extraction

The whole IA (the four doors, the provenance labeling, the destination pattern) is what a fork
inherits. `site.config.json` carries the door labels, brand, courses, and band labels — so
`recursive-iching` gets the same journey-led, provenance-labeled structure by copying the engine
and editing config. The IA *is* the template.

## Build order (merging USER-JOURNEYS' order with this map)

1. **Engine-side (other chat / live data):** stamp `_recursive_eco_url` on all grammars; confirm
   `provenance` propagates repo→DB; live-sync provenance via MCP. *(unblocks J2/J3 filtering)*
2. **Nav (Layer 1):** journey-led homepage + header — the four doors. *(needs `site.config.json`)*
3. **Player destination:** Design-your-own-deck (see its scope doc). *(J1)*
4. **Practitioner destination:** The Golden Dawn Path + Rituals. *(J3)*
5. **Labeling (Layer 3):** Library provenance facet + peer-band presentation + badges. *(J1/J2/J3)*
6. **Publish the 2 Living decks** once peer presentation exists. *(J3)*

Each gated by its journey's acceptance test (the "how served" line) so "done" is observable.

## Division of labor (avoid two agents editing the same files)

- **Design/doc layer (this map, the GD-Path design, persona naming):** held here.
- **Integration/build layer (stamping, DB sync, peer-band UI, publishing, nav build):** the
  session deep in the live MCP/DB work owns it. Rule of thumb: *decide & document here; wire &
  ship there.* New doc files only, to keep collisions at zero.

## Open questions

1. Header: 4 doors as top-level tabs, or homepage hero with 4 cards + a slimmer header? (Lean: both — hero on `index.html`, doors in the header dropdown.)
2. Does "Play" need its own landing distinct from today's `play.html`, or is `play.html` *renamed* to Play and given the four-door context? (Lean: rename + reframe, don't duplicate.)
3. Where do courses sit — under "The history," or their own door? (Lean: under The history; they're how the record is taught.)
