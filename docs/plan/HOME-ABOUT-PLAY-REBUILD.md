# Home / About / Play rebuild — build plan (Jun 23 2026)

Autonomous build per the maintainer's directive. Light theme; `theme.css` is the one colour
source; never crop card art. Git identity: `PlayfulProcess <17236172+PlayfulProcess@users.noreply.github.com>`.

## Phase 1 — Tarot History Forum, About, footer (authorship & honesty)
1. **Strip the AI/Forum warning from grammars.** The note *"Research notes — AI-assisted first-pass
   draft, pending review by the maintainer and the Tarot History Forum. Skeptical, document-first
   (Dummett spine). Corrections welcome via pending edit."* is injected by `scripts/enrich_from_research.py`
   and sits in **25** grammar `description`s. Remove the injector; strip the line from every grammar.
   Reword in-description deferrals like *"A point for the Tarot History Forum to settle"* →
   *"genuinely debated in the literature."* **Keep the Tarot History Forum / blogs ONLY inside explicit
   "Sources" lists** — never as reviewer/guarantor. They are not responsible for my errors.
2. **About page** (`pages/about.html`): a plain statement — *this is the work so far of a solo developer,
   passionate about tarot and meaning systems, who relied heavily on AI; the hope is that real humans
   become collaborators and make the whole thing better.* Render **`tree.jpg`** (root) — the first vision
   of the ecosystem. Add the recursive.eco-style footer (below). PlayfulProcess byline, never the legal name.
3. **Footer** (shared): copy recursive.eco's landing footer feel — *under construction* + the **gold
   recursive spiral** + a **newsletter sign-up** (post to recursive.eco's newsletter endpoint if one
   exists, else link to recursive.eco). Replace the homepage's "Scholarship consulted… Tarot History
   Forum" line — keep a neutral sources note, no Forum-as-reviewer.

## Phase 2 — Homepage
4. **"From the Recursive Community"** band — split the contemporary band:
   - **Recursive Community** = **Ontoject Tarot** + **The 36 Tattvas / Shaiva Tantra** (PlayfulProcess's own).
     Each gets: a **collaborator status pill** ("Looking for collaborators" — both yes), and a description
     framing them as *objects of study by PlayfulProcess, who is not the expert in these systems/traditions.*
     **Ontoject** specifically: a creative / tattvas tone, marked **"still under process."**
   - **Contemporary decks (CC-BY-SA)** = Yve Lepkowski's five (unchanged).
5. **recursive.eco box** (`.ecotree`, "One branch of a larger tree"): replace the hand-drawn "crazy"
   spiral with the **animated gold logarithmic spiral** (recursive.eco's, recoloured) + the `recursive-mark`.
6. **Image variety**: stop repeating the Visconti **World**. Across hero/ways/arch/gallery use **unique**
   cards — more **Star, court cards, Empress**; **less World and Chariot**. Pull from R2 deck images.
7. **Card names readable in Cards view**: `.item-name` is dark but `0.7rem` + `nowrap` + ellipsis → clipped.
   Bump size, allow 2-line wrap, ensure not clipped.

## Phase 3 — Play / Divination + courses
8. **Divination = section two in Play** (`pages/play.html`): a Divination section (the "how a reading
   works" lenses + the divination course) as the second section.
9. **Games of the Tarot → course format**: the booklet is hard to read — render it as a proper course;
   fix the faint course body text; **thumbnail the game courses in the middle** and **summarise how to play** each.
10. **Original images everywhere; no repeats Play↔About.** Use real card art on every page. Add
    **`metadata.image_usage`** to grammars (which page/slot each image feeds) so we can spread unique cards
    and not collide; note the upkeep rule in `CLAUDE.md`.

## Phase 4 — verify (contrast audit + visual) → commit/push to dev.
