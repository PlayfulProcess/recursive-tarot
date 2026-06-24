# Use case — Build a tarot by talking to recursive.eco

*How a deck got its whole Minor-Arcana layer built in one sitting, with no database, no
image-upload scripts, and no GitHub — just an AI assistant and the recursive.eco MCP.*

## The user story

> "I have a personal deck, **The Ontoject** — 24 existential 'stations' from the Void to
> the Trickster, built on Tillich and Parker Palmer. It has the archetypes I care about,
> but no elemental body — no suits, no pips. I want to give each card a fire / water /
> air / earth refraction, and I don't want to touch a database to do it."

That's the whole brief. What follows is exactly what the assistant did, end to end, through
the **recursive.eco MCP** — the same tools any user (or their AI) can call.

## The toolbox (5 MCP tools)

| Tool | What it does |
|---|---|
| `list_grammars` | find your decks by name |
| `get_grammar` | read a deck's full structure (items, sections, keywords) |
| `add_item` | create a new card |
| `update_item` | set any field — name, keywords, **sections**, `image_url` |
| `cast` | draw a live reading the moment a card exists |

No SQL, no schema, no keys. Your data is yours; the AI just speaks the five verbs.

## The build, step by step

1. **Find & read.** `list_grammars("onto")` → `get_grammar(…)`. The deck came back as 24
   majors, each with the sections `Reflection`, `Poetic_Entry`, `Existential_Entry`,
   `Visual_Contemplation`.

2. **Prove the write.** One `add_item` ("Ace of Sparks") + `update_item` to set its
   sections, then a `cast` to confirm it rendered. The round-trip worked → green light.

3. **Pick the model.** Two options surfaced:
   - *Separate pip cards* — 40 new cards, standard tarot shape, but disconnected from the
     deck's 24 stations.
   - *Refract each major* — one new `Elemental_Play` section per existing card. Keeps the
     deck at 24 archetypes and gives each an elemental body. **Chosen** — it's recursive
     and unified, every station refracted rather than diluted.

4. **Define the four "plays"** (in the deck's own voice):
   - 🔥 **Fire** — the play of *will*: ignition, the *yes* before the plan, courage-to-begin.
   - 💧 **Water** — the play of *feeling*: flow, I-and-Thou, merging, care.
   - 🌬️ **Air** — the play of *mind*: breath, thought, perspective, the spiral.
   - 🌍 **Earth** — the play of *form*: ground, body, structure, the made thing.

5. **Build it out.** 24 `update_item` calls (run in parallel batches of ~6 — the backend
   serialised them cleanly, zero lost writes), each adding the card's four-flavour refraction.

6. **Clean up & verify.** Deleted the throwaway test card; `get_grammar` confirmed all 24
   cards now carry `Elemental_Play` in a consistent slot.

### One card, refracted (The Spiral)

> 🔥 **Fire** — the will to begin again: the spark that chooses to climb rather than merely
> circle, desire turning the loop into an ascent.
> 💧 **Water** — the emotional return: meeting the same grief or the same love at a deeper
> turn of the coil, feeling the tide come back changed.
> 🌬️ **Air** — the thought that deepens on each pass: the question you return to with more
> breath and more altitude, seeing the whole climb from above.
> 🌍 **Earth** — the path worn into the ground by walking it: habit, practice, the body
> that learns by repetition, the structure built ring by patient ring.

## What it costs to follow

| Thing | Cost |
|---|---|
| recursive.eco account | **Free** |
| Card creation & editing via the MCP | **Free** — it's just your own data |
| The AI that drives the MCP | a **Claude plan** (or API credits) you already have |
| Image generation (each card's `Visual_Contemplation` *is* a prompt) | _variable — `<fill in your image-gen tool + price>`_ |

The point of the platform: the two hard parts of deck-building — **storage** (no R2 keys, no
upload scripts) and **image generation** (the prompt already lives on the card) — are handled
by the flow. You build a tarot by *describing* it.

## Why this matters as a pattern

The same five verbs build a deck, a book, an I Ching, a custom oracle — any *grammar*. The
MCP turns recursive.eco into something an AI can author into directly: the human sets the
vision, the assistant makes the calls, and the result is live, castable, and shareable the
moment it's written. *The Ontoject got its elemental body this way in a single conversation.*

---
*Built live against `The Ontoject: A Tarot of Playful Process` via the recursive.eco MCP.
The deck is at [recursive.eco](https://recursive.eco); more from the author at
[playfulprocess.com](https://www.playfulprocess.com/).*
