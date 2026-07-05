# A website like this one — starter kit

This is a **seed**. It's the bones of [The Recursive Tarot](https://tarot.recursive.eco) with the
tarot lifted out — a static, backend-free site that turns a folder of JSON into a browsable library.
The tarot was only the worked example. The method is general: point it at **your** subject — a craft
lineage, a language you're documenting, a valley's folk songs, your family's recipes, the trees on
your street — and you have a small living library that's yours, on the open web, for free.

> This is **Rung 7** of the contribution ladder — *"a website like this one."* Rung 6 (the
> [nara course](https://playfulprocess.github.io/nara/course/)) teaches you to make your own
> *grammars*; this teaches you to make your own *site* to show them.

## What's in the box

```
template/
├── index.html              a self-contained home that reads one grammar and renders it
├── theme.css               the single source of colour — every page links it, nothing redeclares it
├── grammars/
│   └── street-trees/
│       └── grammar.json    the sample library ("The Trees of Elm Row") — replace with yours
├── check.py                the pre-commit gate: validates every grammar, zero dependencies
├── CLAUDE.md               skeleton instructions for the AI that helps you build (make it yours)
└── GRAMMAR_FORMAT.md       the canonical shape of a grammar (pointer to the full spec)
```

Everything is plain HTML, one CSS file, and JSON. No build step, no framework, no server to run in
production. GitHub Pages serves it as-is.

## The first hour

**1. See it work (2 min).** Browsers block `file://` fetches, so open it over a tiny local server:

```bash
cd template
python -m http.server 8000
# now visit http://localhost:8000/
```

You'll see the sample library — three trees and one *grouping* — rendered as cards you can open.

**2. Make it yours (20 min).** Open `grammars/street-trees/grammar.json`. A grammar is just:

- a **name** and **description** at the top, and
- a list of **items**. Each item has an `id`, a `name`, and `sections` — a set of labelled prose
  blocks (`"What it is"`, `"Where"`, whatever fits your subject).

Rename the folder to your slug, change the name and description, and rewrite the items about your
thing. Reload the page. That's your library.

**3. Let a pattern emerge (10 min).** Look at the last item, `group-the-oaks`. It holds no tree of
its own — it has `composite_of: ["tree-white-oak", "tree-red-oak"]`. That's a **grouping**: an item
made of other items. This is the one real trick — structure grows without a database. A grouping
can gather leaves; a grouping of groupings gives you a whole tree. Make one for your subject.

**4. Check it (1 min).**

```bash
python check.py
# → OK: all checks passed (1 grammar)
```

`check.py` catches the handful of mistakes that stop a grammar from loading. Keep it green.

**5. Put it on the web (15 min).** Create a GitHub repo, push this folder, then **Settings → Pages →
Deploy from a branch → (your default branch) / root**. In a minute your library is live at
`https://<you>.github.io/<repo>/`. Share the link.

## Building with an assistant

You don't have to write JSON by hand. Point Claude (or Claude Code) at this folder, tell it to read
`GRAMMAR_FORMAT.md` and `CLAUDE.md`, and just describe what you want — *"add an item for the maple by
the school, with sections for what it is, where, and how it looks each season."* It edits the JSON;
you run `check.py` and reload. Fill in `CLAUDE.md` with the rules of your commons first, so the help
stays on the rails you set.

## The two rules worth keeping

1. **All colour lives in `theme.css`.** One `:root` of tokens, linked everywhere. Never redeclare a
   colour in a page, never add a dark-mode block — that's what keeps a growing site from drifting
   into a dozen mismatched palettes. To recolour the whole site, edit that one file.
2. **The data outlives the platform.** The viewers are deliberately thin. If this starter vanished
   tomorrow, your `grammars/*.json` would still be a clean, portable, public record of your subject.
   That's the point.

## Where this connects

- **The full spec:** [`GRAMMAR_FORMAT.md`](GRAMMAR_FORMAT.md).
- **Go further — the live app:** your grammars can also open in [recursive.eco](https://recursive.eco)
  for a live oracle, AI readings, and community editing. The parent project's
  `docs/RECURSIVE-ECO-INTEGRATION.md` shows how a repo wires to a channel.
- **The ladder you're on:** [Ways to Contribute](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute)
  — Rungs 1–5 teach you to tend an existing commons; Rung 6 to make your own grammars; this is Rung 7.

Take the method home. Found your own.
