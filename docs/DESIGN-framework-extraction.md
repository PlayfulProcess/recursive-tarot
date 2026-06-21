# Design — Framework extraction: turn recursive-tarot into a reusable grammar-site engine

**Status:** proposal (planning, June 2026). No code yet.
**Author:** PlayfulProcess
**Why now:** recursive-tarot is the most mature "framework" we have — icons, the Eye/views,
the one cross-link pill, courses hyperlinked to grammars, `eco-links`/MCP wiring, and the
Two Wings provenance model. The test of whether it's a *framework* (not a one-off) is: **can a
new user with just GitHub + Claude + the recursive.eco MCP fork it for a new domain (the I Ching)
quickly — and can that replication be documented as a course?** Today the answer is "almost,"
because the **engine and the content are interleaved**. This doc defines the seam.

---

## The goal

Make a fork = **copy the engine + drop in your grammars + edit one config**. Concretely:
1. A clean **engine / content seam** so the I Ching site is a copy, not a rewrite.
2. A single **`site.config.json`** that holds everything domain-specific (title, brand, domain,
   nav, course list, the Two Wings labels), so de-tarot-ing is editing config, not hunting strings.
3. The replication itself becomes the **Rung-5 course** ("a new user builds a grammar site").

---

## The seam — what's engine vs content (from the current top level)

| Layer | Files / dirs | Fork action |
|---|---|---|
| **ENGINE** (generic, reusable) | `viewers/` (cards, study, sequence-v2, timeline, explorer, genealogy-tree, `eco-links.js`, prototypes); `scripts/check_all.py`, `refresh_collection.py`; `site-header.js`, `view-switcher.js`, `loader.js`, `auth-widget.js`, `style.css`, `favicon.svg`, `recursive-logo.svg`; the `course/` → `pages/courses/` MDX pipeline + course-viewer; `recording/` sequence player | **Keep as-is** |
| **ENGINE-but-content-shaped** | `scripts/build_meta_grammar.py`, `build_people_grammar.py`, `enrich_cards_from_research.py` | **Keep the mechanism, re-point at the new corpus** (people→? , meta is generic) |
| **CONTENT** (tarot-specific) | `tarot/` (grammars + `_eco_ids.json` + `_collection.json`); `research/` (dossiers); the *content* pages (`pages/play.html`, `pages/sources.html`); `course/*.mdx` text; `print/`, `booklets/`, `data/`, `deck.html`, `print-products.json`, `print_codes.json` | **Drop / replace per domain** |
| **CONFIG (today: hardcoded)** | brand + nav + course list inside `site-header.js`; homepage copy in `index.html`; `CNAME`; the Two Wings labels | **Extract into `site.config.json`** |
| **DOCS / META** | `CLAUDE.md`, `README`, `CHANGELOG`, `FUTURE_PLAN`, `GRAMMAR_FORMAT`, `docs/`, `UX-research/` | **Rewrite per domain** |
| **JUNK to sweep** | `__cowork_probe.md`, `__cowork_writetest.txt`, `env-local.txt` (gitignored — OK, just confirm it never gets committed) | **Delete the probes** |

The big realization: most of the repo is already engine. The friction is the **CONFIG row** —
the handful of places where tarot strings are baked into engine files.

---

## Recommended approach: config-driven convention (not a submodule)

Two ways to share an engine across repos:

- **A. Template/submodule repo** (`recursive-grammar-site`) consumed by tarot + iching. Cleanest
  in theory, but adds sync/submodule overhead and slows the vibe-coding loop. **Reject for now.**
- **B. Convention + config (recommended).** Keep the engine files at known paths; pull every
  domain-specific string into `site.config.json`. A fork = copy the repo, delete `tarot/` +
  `research/` + the content pages, drop in your grammars, edit `site.config.json`. Lowest friction,
  no submodule, fits how we actually work. If we later fork a *third* domain and the copy-drift
  hurts, promote the engine to a template repo then — not before.

### `site.config.json` (the de-tarot target)

```jsonc
{
  "site_title": "The Recursive Tarot",
  "domain": "tarot.recursive.eco",          // drives CNAME
  "brand": { "logo": "recursive-logo.svg", "home_href": "index.html",
             "logo_href": "https://recursive.eco" },
  "nav": [ /* the dropdowns site-header.js renders */ ],
  "courses": [ { "slug": "history-of-tarot", "title": "A History of Tarot", "icon": "📖" } ],
  "two_wings": {
     "record_label": "The Record", "record_sub": "dated, attributed artifacts",
     "living_label": "The Living Tradition", "living_sub": "what each generation made",
     "manifesto": "Below the line, the cards stop being evidence and become interpretation…"
  },
  "item_noun": "card",                        // "card" | "hexagram" | "verse"
  "eco_ids_file": "tarot/_eco_ids.json"
}
```

`site-header.js`, `index.html`, the course list, and the Two Wings divider all read from this
instead of hardcoding. That's ~the entire de-tarot surface.

---

## Concrete extraction tasks (small, ordered)

1. **Create `site.config.json`** with tarot's current values; change nothing visible.
2. **Refactor `site-header.js`** to read brand + nav + course list from the config.
3. **Parametrize `index.html`** hero copy + the homepage tiles from config (or a `pages/` partial).
4. **Generalize the build scripts:** `build_meta_grammar.py` is already generic; `build_people_grammar.py`
   is "build an entity grammar from `research/<entities>/*.md`" — rename/parametrize the entity dir.
5. **Document the contract** in a short `ENGINE.md`: "these files are the engine; this config drives
   them; to fork, copy + drop content + edit config."
6. **Sweep junk** (`__cowork_*`), confirm `env-local.txt` stays gitignored.

Each step keeps `check_all` green and the live site byte-identical — pure refactor.

---

## The fork workflow (what the I Ching build will exercise — and document)

1. Copy the engine (repo minus `tarot/` + `research/` + content pages).
2. `git rm` the tarot content; drop in the harvested I Ching grammars (Zhouyi/Legge already exists
   in recursive.eco-schemas as `zhouyi-legge`) under the same `tarot/`-shaped folder convention.
3. Edit `site.config.json` (title "The Recursive I Ching", item_noun "hexagram", Two Wings labels
   for classical-vs-interpretation, courses, domain).
4. Run `check_all`; publish + cast via the MCP (`set_grammar_visibility`, images via
   `commons_image_search`/`generate_item_image`).
5. **Record every step** → that transcript *is* the Rung-5 course: "a new user with GitHub + Claude
   + MCP stands up a grammar site." This is the payoff: the cleanup makes the replication smooth
   enough that the replication is teachable.

---

## Open questions

1. `item_noun` and view defaults: enough as config, or do some viewers still assume "card"? (Audit
   `cards.html`/`study` for hardcoded "card".)
2. Do we extract now (before the I Ching fork) or fork-first and let the pain reveal the seam? (Lean:
   a *light* extraction of just `site.config.json` first; deeper refactors as the fork demands them.)
3. Where does `_eco_ids.json` + the publish state live per domain? (Per-repo, as now — fine.)
4. Does the schemas repo's Grammar Playground (`previews/index.html`) belong in the engine as a
   generic viewer? (Likely yes — it's already domain-agnostic.)
