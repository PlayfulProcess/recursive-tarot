# The Tarot Reader

A way to have Claude read a spread with you in the style of this site: you say the spread,
write down or photograph the cards and name the deck, and Claude reads the handwriting (asking
about what it isn't sure of), quotes Book T and Waite briefly, notices patterns, offers
questions rather than instructions, links each card to its page on recursive.eco, and can draw
the spread as a grid of the card images. It can also make a new spread with you.

Anyone can use it. A draft, Oct 6 2026.

## What is in this folder

| File | What it is |
|---|---|
| [`READER.md`](READER.md) | The instructions for Claude: the style, the procedure, the safety lines, making spreads, what to save. |
| [`grid-template.html`](grid-template.html) | A self-contained page that lays a reading on its spread's grid. Claude fills one JSON block and returns it as an artifact. |
| [`spreads/`](spreads/) | The spread format ([`SPREAD-FORMAT.md`](spreads/SPREAD-FORMAT.md)) and four starters: three cards, the five-card cross, the Celtic Cross, and Four and Three. |
| [`examples/sleep-reading.html`](examples/sleep-reading.html) | The template with one reading filled in: seven cards in two rows, from the Golden Dawn deck. |

## Set it up in claude.ai

You need a claude.ai account (Projects are available on the free plan, which allows up to five
projects) and, for the card lookups, a free recursive.eco account.

**1. Make the Project.**
1. Go to [claude.ai/projects](https://claude.ai/projects) and click **+ New Project** (upper
   right).
2. Give it a name (e.g. *Tarot Reader*) and a short description, and create it.

**2. Paste the instructions.**
1. In the Project, click **Set project instructions**.
2. Open [`READER.md`](READER.md), copy everything below its first line (from "You are a tarot
   reading companion…" to the end) and paste it in.
3. Click **Save instructions**.

**3. Add the files Claude reads.** In the Project's knowledge panel (on the right), click
**+** and upload:
- `grid-template.html` (from this folder; on GitHub, open it and use the download button).
  Claude needs it to draw the grid.
- *Your Card Table* (`course/your-card-table.mdx` in this repo): the notation, with the hand-drawn
  suit signs. READER.md already carries a short version, so this one is optional.
- Optionally, the spread files in `spreads/` you use most.

**4. Connect recursive.eco** (once per account, not per Project).
1. In claude.ai, open **Customize**, then **Connectors**.
2. Click **+ Add**, then **Add custom connector**.
3. Name it *recursive.eco* and paste the address `https://flow.recursive.eco/api/mcp`. Click
   **Continue**.
4. Sign in to recursive.eco when it asks, and press **Approve**. There is no token to copy.

**5. Turn it on in a chat.** In a new chat inside the Project, click **+** (lower left of the
message box), then **Connectors**, and make sure *recursive.eco* is on.

**6. Try it.** "Celtic Cross, default deck" and a photo of your notes; or type the cards:
`3♥ KW 4S XI↓ / 6⛤↓ 8W KnP, two rows, a question about sleep`.

### As a skill instead (unverified)

claude.ai also takes custom skills (**Customize > Skills**, **Add**): a zip holding a folder
with a `skill.md` whose frontmatter has a `name` (64 characters at most) and a `description`
(200 at most), and READER.md as the body. That route is not tested here; the Project route
above is the one this draft was written for.

### What was checked, and what wasn't

- The Project labels (**+ New Project**, **Set project instructions**, **Save instructions**,
  the **+** in project knowledge) and the connector labels (**Customize > Connectors**,
  **+ Add**, **Add custom connector**, **Continue**, the **+ → Connectors** toggle in a chat)
  are from Anthropic's help pages as of Oct 6 2026:
  [creating projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects),
  [custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
  They were not clicked through for this draft.
- The connector address and the **Approve** step are from recursive.eco's own guide
  ([build with your AI](https://recursive.eco/pages/build-with-your-ai.html)).
- **Unverified:** whether the card images (hosted on recursive.eco's public image store) load
  inside a claude.ai artifact. If they don't, the grid shows each card's name in its place,
  and every card still links to its page.
- **Unverified:** whether the connector is on by default in Project chats; step 5 covers it
  either way.

## Without a connector

READER.md still works: Claude reads from the notation alone and leaves out the quotations
rather than quoting from memory. The grid needs image addresses, so without the connector it
draws the card names only.

## Links that need no setup

- Each card's page on recursive.eco, with its Connections to the same card in other decks:
  `https://flow.recursive.eco/g/<deck id>?item=<item id>`.
- The site's [Card Table](../viewers/table.html) draws a typed table of cards from a link
  (`?t=`, see READER.md, "Lay the grid"); its **Copy link** button makes the same kind of link.
- The [Spread Caster](../viewers/caster-studio.html) loads a spread file from a link
  (`?spread=` with the file base64url-encoded) or from its upload button, for casting or editing
  the layout. It loads the layout only, not the cards.
