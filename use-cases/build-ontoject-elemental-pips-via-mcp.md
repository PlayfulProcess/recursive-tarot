# Use case — Refract a deck into elemental pips through the recursive.eco MCP

*How the 24 existential Majors of the Ontoject got a Fire / Water / Air / Earth body —
starting with the four pips of **Structures** — using the new batch MCP tools
(`add_items`, `update_items`, `generate_item_image`). Plus the per-card costs, the
podcast-transcription side-quest that feeds the deck's resonance layer, and one honest
limitation for the course.*

> Companion to [`build-ontoject-illustrated-via-mcp.md`](./build-ontoject-illustrated-via-mcp.md)
> (whole-deck clone) and [`build-ontoject-via-mcp.md`](./build-ontoject-via-mcp.md)
> (the Elemental_Play layer). This one builds the **Minors / pips**: each Major refracted
> into four elemental cards, each carrying **Feeling · Need (NVC) · Structure · Tend**.

## The brief

> "Build into **The Ontoject — Elemental Deck (Majors + Pips)**
> (`ffa74a26-95d6-4108-8211-51a8dd387bb1`). Copy the 24 Majors verbatim from
> **The Ontoject — Illustrated** (`e8c4ca59…`). Then build the four pips of **Structures**
> in an approved shamanic/animist/embodied voice — *less story, more feeling* — and generate
> art for those four only. Then scale the same Feeling/Need/Structure/Tend pattern across the
> other 23 Majors × 4 elements."

## The element system (one line each)

| Element | Feeling | Need (NVC) | Meets structure as |
|---|---|---|---|
| 🔥 Fire | sacred urgency / anger, heat at a wall | autonomy · vitality · liberation | fuel-vs-stone (eats dead wood, tempers true stone) |
| 💧 Water | the ache where sorrow & gladness are one water | flow · belonging · to-be-held | the riverbed, never the dam |
| 🌬️ Air | stale press of certainty → relief of doubt | clarity · meaning · room-to-question | the inherited rule; breath through the lattice |
| 🌍 Earth | deep steadiness / bone-weariness | safety · rest · sustenance | stone & bone (ground to stand on, or that buries) |

**Voice rule (non-negotiable):** shamanic / animist / embodied. The fierce
destroyer-regenerator undertone lives in **Fire only**, *felt but never named* — it appears
in no visible card text.

## The toolbox (new batch tools)

`get_grammar` · **`add_items`** (≤100 items, one DB write) · **`update_items`** ·
**`generate_item_image`** (~$0.15/img, Gemini Imagen) · `cast`. The grammar is one JSONB
document, so batching = one rewrite instead of one-per-card.

## The build, step by step

1. **Copy the 24 Majors.** `get_grammar(e8c4ca59…)` → full `sections`. One `add_items` call
   wrote all 24 verbatim (name + keywords + full sections + `category:"major"`), and carried
   over each Major's existing R2 `image_url` — so 22/24 arrived already illustrated, free
   (image reuse, not regeneration). Items auto-numbered 1–24 in insertion order.
2. **Build the four Structures pips.** One `add_items` call → items #25–28, `category` =
   `fire`/`water`/`air`/`earth`, element emoji in `symbol`, sections =
   **Feeling · Need · Structure · Tend** (approved exemplar text verbatim).
3. **Generate art for the four pips only.** 4 × `generate_item_image` with custom shamanic
   prompts (the pips have no `Visual_Contemplation` to default to). Fire prompt kept the
   goddess undepicted — just fire eating dead timber while the true stone glows and tempers.
4. **Cast & verify.** `cast(count=3)` rendered a live reading; `get_grammar` confirmed
   28 items = 24 majors (22 imaged) + 4 pips (4 imaged), each pip carrying the 4 sections.

## Per-card cost (for the course)

| Work | Tool | Count | Unit | Cost |
|---|---|---|---|---|
| Copy 24 Majors (text + reused art) | `add_items` | 1 write | — | **$0.00** |
| Build 4 Structures pips (text) | `add_items` | 1 write | — | **$0.00** |
| Structures art | `generate_item_image` | 4 | ~$0.15 | **$0.60** |
| **Deck total so far** | | | | **$0.60** |

Image credits after the run: **41.89** remaining (Gemini Imagen, 3× markup, debited from the
recursive.eco account that owns the MCP token). Text writes cost nothing — only AI image
generation draws credits.

Projected to finish the deck: 23 Majors × 4 = **92 more pips** (text = $0). If every pip is
later illustrated: 96 pips × ~$0.15 ≈ **~$14.40** in art, generated only when asked
(*images held beyond Structures by instruction*).

## The resonance layer (podcast transcripts)

Each element links a resonance from **The Emerald** (Josh Schrei). Two episodes were fetched
from the buzzsprout RSS feed and transcribed with the **OpenAI Whisper API** (`whisper-1`,
`verbose_json`), chunked to 16 kHz mono / 600 s segments to stay under the 25 MB limit, then
written to json/srt/tsv/txt/vtt matching the existing transcript folders:

- 🔥 Fire → *"This Episode is FIRE"* — already transcribed locally (full episode).
- 💧 Water → *"Enter the Dragon, Part 2: On Order and Chaos"* — **newly transcribed**
  (132 min, 1504 segments, **$0.79** OpenAI). Part 1 was already local.

(Transcripts are research-local only and never committed — see book-repo copyright rules.)

## One honest limitation for the course

**The MCP item model has no `metadata` field.** `add_items` / `update_items` /
`add_item` / `update_item` expose only `name · symbol · keywords · category · image_url ·
sections · composite_of`. So a per-item "private resonance link" (Emerald episode + song)
**cannot** be stored as hidden metadata through the MCP — anything in `sections` renders as
visible card text. The resonance therefore lives **at the deck level** (in the grammar
`description`, which is metadata, not card text) and in this log. This is different from the
GitHub-backed recursive-tarot viewer, where items *do* carry a `metadata` block
(`source_deck`/`source_item_id`/`deck`) for cross-links. **Lesson:** if you want per-item
private metadata in an MCP-built deck, the platform needs a `metadata` passthrough on the
item write tools; today it has none.

## The IDs (for continuation)

- Target deck: `ffa74a26-95d6-4108-8211-51a8dd387bb1`
- Majors source: `e8c4ca59-7841-4b5d-ad56-584ff52c859d`
- Structures Major (in target): `25001d8f-35de-40af-9aa6-8e2ad4a3081c`
- Structures pips: Fire `620fdf36…` · Water `fb7ab950…` · Air `6f624f1c…` · Earth `3a3c6742…`
