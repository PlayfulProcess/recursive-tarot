# Design — Two Wings: provenance as the organizing principle

**Status:** proposal (planning, June 2026). No code yet.
**Author:** PlayfulProcess
**Problem it solves:** how to weave modern / interpretive / experimental decks (other PD decks
from the recursive.eco tarot channel, the **Ontoject Tarot**, the **36 Tattvas**) into a site
that tarot *historians* (the Dummett–Depaulis–Pratesi school) respect — **without** dismissing
the living tradition that practitioners like **Benebell Wen** care about.

---

## The insight

Historians and practitioners disagree about almost everything except **one shared value:
honest provenance.** Historians want every deck dated and attributed so interpretation never
masquerades as evidence. Wen wants honest sourcing so nothing is culturally flattened or waved
away as "fake." So the design that satisfies both makes **provenance the spine** — and lets the
labels, not a hide-the-other-side toggle, do the diplomatic work.

> We do **not** ship a hard "history-only / modern" global mode. A toggle that hides half the
> library reads as the site being ashamed of one wing — the version *both* camps find slightly
> insulting. We ship labels + a soft, persistent lens with smart per-surface defaults instead.

---

## The model: one library, two wings, by *kind* not *quality*

Split along the only axis both camps respect — **evidence vs. interpretation**:

- **The Record** — datable, attributed artifacts. Visconti-Sforza, Charles VI, Sola Busca,
  Marseille, Minchiate… *and* the modern historical decks (RWS 1909, Thoth 1944). These are
  evidence. Each carries **date + maker + place**.
- **The Living Tradition** — decks that interpret, reframe, or are newly made: recursive.eco
  originals (Ontoject Tarot), reinterpretations, cross-tradition grammars, modern PD-art decks
  from the channel. Each carries **creator + year + "what it interprets."**

Plus one orthogonal flag — **`status: draft`** — *not* a third wing. The 36 Tattvas is
*Living Tradition · draft*; framing it as "a draft interpretation drawn from Śaiva tattva
philosophy, not a historical tarot" is cultural **care**, not demotion.

### Where each deck lands

| Deck | Wing | Status | Frame |
|---|---|---|---|
| Historical artifacts (Visconti, Marseille, RWS, Thoth, …) | The Record | published | dated + attributed |
| Other channel PD decks | Record *if* scans of real historical decks; else Living Tradition | published | tier by what they *are* |
| **Ontoject Tarot** (recursive.eco original) | The Living Tradition | published / draft | "a platform original — new work, not historical evidence" |
| **36 Tattvas** | The Living Tradition | **draft** | "interpretive grammar from Śaiva tattva philosophy — not a historical tarot" |

---

## The data layer (small — mostly labeling, not machinery)

Add two fields per grammar (in `_collection.json` derived fields + grammar metadata):

```
provenance: "record" | "living"
status:     "published" | "draft"     # orthogonal; draft hidden from default lists
# plus the facts that earn the badge:
made:       { who: "<maker/creator>", where: "<place|—>", year: "<c.1450 | 2026> }
interprets: "<one line — only for Living Tradition>"
```

Everything else rides patterns that already exist (the `lens` facet, HashtagFilter, the
`all-decks-many-lenses` meta-grammar, the Eye/view dropdown).

---

## Per-surface behavior

| Surface | Default | Behavior |
|---|---|---|
| **Explorer / Play / Library** | The Record foregrounded | Living Tradition in a **labeled, collapsed band** below the divider (manifesto on it). One **persistent** preference remembers the visitor's choice. |
| **Timeline / Genealogy / Tree of Life / History course** | **The Record only — by definition** | Footnote: *"Interpretive and contemporary decks are honored in The Living Tradition; they're excluded here because this view maps historical descent."* This is the move that protects the historians: the descent tree is never polluted by an interpretive "node." |
| **Deck page** | — | A **provenance badge**: `Historical artifact · Milan, c. 1450` vs `Living tradition · created 2026 · draft`. |
| **Genealogy (optional nicety)** | — | A Living-Tradition deck may appear as a **dotted, greyed "off-record" leaf** branching from its inspiration (Ontoject off RWS): lineage visible, record visually quarantined + labeled. |

---

## The divider manifesto (the sentence where the diplomacy lives)

**Primary (recommended):**

> *Below the line, the cards stop being evidence and become interpretation — a difference of
> kind, not of rank. We date the record and attribute the tradition, and never confuse the two.*

**Alternates:**

- *Above: the record — every deck dated, attributed, held to the evidence. Below: the living
  tradition — what each generation made of the cards. Held to the truth, both; neither outranks
  the other.*
- *What follows is not history but what history became. We keep the two clearly apart so each
  can be honored on its own terms.*

Badge microcopy:
- Record: **Historical artifact** · `‹place›, ‹date›` · maker ‹name›
- Living: **Living tradition** · created ‹year› · ‹creator› — *interprets ‹x›*
- Draft ribbon: **Draft** · "a work in progress, shared early"

---

## Why it pleases both

- **Historians:** the Record is epistemically clean — dated artifacts only; descent views never
  mixed; divination still framed as an 18th-c. accretion. The category error that offends them
  (interpretation dressed as history) becomes structurally impossible, and a pure-history view
  is the *default* on every scholarly surface.
- **Wen / practitioners:** the Living Tradition is a **first-class wing** with equal content
  depth and full Cast/use — not a debunking, not a junk drawer — and its cultural sourcing is
  explicit. Nothing is called fake; the "why it works" psychology lenses live here proudly.
- **Both at once:** provenance is the shared value, so satisfying one camp automatically
  satisfies the other.

---

## Open questions / decisions to make

1. Does RWS/Thoth sit in **The Record** (my call: yes — they're dated, attributed 20th-c.
   artifacts historians track) or feel "modern" enough to bridge? Decide once, document.
2. Is the persistent lens a **segmented control** ("Record · Both · Living") or a pair of
   collapsible bands? (Lean: bands on listings, no global hard mode.)
3. Ship the **dotted off-record genealogy leaf** in v1 or defer? (Defer — nice-to-have.)
4. Where do **drafts** surface at all? (Lean: hidden from default lists; visible via a "show
   drafts" pill and on their own deck page, always wearing the Draft ribbon.)
