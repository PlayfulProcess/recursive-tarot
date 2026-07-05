# CLAUDE.md — your library

*This is a skeleton. Rename the project, delete the tarot-specific memory, and make it yours.
It's the file Claude reads first when working in this repo — tell it the rules of YOUR commons.*

## What this is

A small, backend-free website for a **library about `<your subject>`** — built on the
recursive.eco grammar format. The data is public JSON; the site is thin HTML; the point is
that the **data**, not the platform, is what lasts.

Fill this in:
- **The subject.** One paragraph: what this library is about and who it's for.
- **The one rule.** Every commons needs a floor. (The tarot one is *"a gate, not a fate — relate
  to the card, never obey it."* Yours will be different — but name it, so contributions hold a line.)
- **Sources & honesty.** Where your facts come from; what you will and won't claim; images must be
  yours or openly licensed, always attributed.

## Architecture (don't change without reason)

- **Grammars** live in `grammars/<slug>/grammar.json`. One file per library. See
  [`GRAMMAR_FORMAT.md`](GRAMMAR_FORMAT.md) for the canonical shape.
- **All colour lives in `theme.css`** — one `:root` of tokens, linked by every page. Never
  redeclare colour tokens in a page, and never add a dark-mode block. To change a colour, edit
  `theme.css` once.
- **`index.html`** reads one grammar and renders it. Add pages the same way — thin, self-contained,
  linking `theme.css`.

## Before you commit

Run `python check.py` — it must end **"all checks passed"**. It validates every grammar against
the format and catches the three mistakes that stop a grammar from loading.

## Growing it

- A **leaf** is an item with `sections`. A **grouping** is an item with `composite_of: [ids]` —
  that's how structure emerges without a database.
- Keep changes small and reviewable — one item, one fix at a time.
- When you're ready to go live: turn on **GitHub Pages** (Settings → Pages → deploy from your
  default branch), and your site is on the web for free.

## Connecting to recursive.eco (optional)

Your grammars can also open in the recursive.eco app — for the live oracle, AI readings, and
community editing. See the integration reference in the parent project
(`docs/RECURSIVE-ECO-INTEGRATION.md`) for how a repo wires to a channel.
