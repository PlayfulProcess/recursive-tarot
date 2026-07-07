# Replicate the Pattern — how to make a new Recursive site from this one

This repo (recursive-tarot) is the **mother pattern**. Astrology was the second site; I Ching
will be the third. This doc exists because the second one went wrong in a specific, instructive
way, and the goal — the builder teaching *anyone* to make a site like this — depends on the
process being honest about that.

## The failure to learn from (astro, Jul 2026)

Astro was supposed to be "tarot with new content." Instead, across many sessions, the site was
**rebuilt piece by piece from scratch** — a hand-rolled homepage, a hand-rolled header, a
hand-rolled course viewer, custom lenses — each individually fine, collectively a thinner cousin
that permanently lagged the mother. Every tarot improvement (dropdown fixes, lens prototypes,
explorer, paging) had to be re-done or was silently missing. The builder asked repeatedly for
"the tarot pattern here"; what she got was re-imaginings of it.

**The root cause was a default:** an AI (or a person) asked to "make astro's X like tarot's X"
will naturally *write a new X inspired by tarot* unless explicitly forced to *copy tarot's X and
change three things*. The first feels creative; the second is correct.

## The Prime Rule

> **COPY the working file. Change only: (1) data paths, (2) branding strings, (3) the accent
> color, (4) content. NEVER change structure. When in doubt, diff against the original — if the
> diff shows anything beyond those four categories, you've started rebuilding. Stop.**

## The recipe (I Ching, and every site after)

**0. Start from a literal copy — of the YOUNGEST sibling.** The most recent port is always
the most generalized: tarot→astro stripped the tarot-isms (deck→grammar, trump-keys→generic
matching, collection-driven menus); astro→iching stripped astro-isms in turn. So copy the tree
of the newest site in the family (as of Jul 2026: the I Ching site in recursive-starter),
falling back to tarot only for mechanisms it alone has (course→grammar build scripts, research
conventions, print pipeline, caster). Delete the *content*, keep every *mechanism*. Do not
start from an empty folder, a template framework, or "the same idea done fresh." Corollary:
you never need to "upstream" improvements by hand — build in whichever site you're actively
working on, and the next port harvests whatever got better. One domain-specific decision no
copy can make for you: the cross-grammar MATCHING KEY in lenses (tarot: trump key; astro:
entity name; iching: hexagram number — names differ across translations). Pick it consciously;
picking wrong fails silently.

**1. The data layer** — one folder per grammar: `grammars/<slug>/grammar.json` (canonical shape:
`docs/GRAMMAR_FORMAT.md` / recursive-eco's `GRAMMAR_COMMONS_SCHEMA`). Then the collection
manifest the viewers read (`_collection.json`), rebuilt by script — port the script, run it,
never hand-maintain the manifest.

**2. The chrome** — `site-header.js` (shadow-DOM header; carries hard-won fixes like the
dropdown hover-gap bridge — copying it inherits the fixes for free), `theme.css` (swap ONE
accent family; tarot=gold, astro=sky blue, pick the new site's own; purple is reserved
ecosystem-wide for recursive.eco-redirect affordances and the shared assistant star),
`assistant.js` (the shared eco assistant — mount, don't re-implement).

**3. The views** — copy `index.html` (thumbnail gallery → REAL pages, never popups) and
`viewers/` (cards, explorer, lenses, tree, timeline). Site-specific instruments (astro's chart
wheel; iching's coin-cast, if built) are ADDITIONS beside the ported set, never replacements
for it.

**4. The eco binding** — `recursive-eco.json` (channel manifest: identity, grammars glob,
`id_map`), `ids.json` (slug→UUID; the webhook resolves through it, so pushes auto-reindex the
app), and the publish loop: import each grammar once in recursive.eco (or insert via the
app), set it public, add it to the channel, record the UUID in `ids.json`. A grammar without a
public row renders an empty page for logged-out visitors — publishing is part of shipping.

**5. The knowledge layer** — `research/` dossiers with ✔/○/◆ confidence markers (verify before
citing; contested claims shown two-sided or excluded), `course/` (see
`docs/HOW-TO-WRITE-A-COURSE.md`: research → thesis → write in the builder's voice → verify),
CHANGELOG.md.

**6. Verify like a visitor** — Playwright against a local static server, 390px and 1280px:
every header link resolves, gallery renders with thumbnails, each viewer loads the collection,
dropdowns survive the mouse crossing the gap, courses reachable from header AND homepage.

## The checklist form (print this for a new site)

- [ ] Copied tarot's tree; deleted content, kept mechanisms
- [ ] `grammars/<slug>/grammar.json` × N, schema-valid; `_collection.json` rebuilt by script
- [ ] `theme.css`: ONE new accent family; purple only for eco-redirects + assistant star
- [ ] `site-header.js` copied (menus re-pointed); dropdown gap-hover verified
- [ ] `index.html` gallery: all grammars, thumbnails, real-page links
- [ ] `viewers/`: cards, explorer, lenses, tree, timeline all load the collection
- [ ] Site-specific instruments added beside (not instead of) the ported set
- [ ] `recursive-eco.json` + `ids.json`; every grammar published (public row + channel listing)
- [ ] `research/` dossiers with confidence markers; course(s) via HOW-TO-WRITE-A-COURSE
- [ ] Playwright pass at 390/1280; CHANGELOG updated
- [ ] GitHub Pages workflow points at the branch actually being pushed

## Why this is teachable

Nothing above requires being a developer. It requires: a copy, a rename, one color decision,
your own content in a well-defined JSON shape, and the discipline to not "improve" the
mechanisms while you're still filling them. The mechanisms already encode years of fixes.
Change them *after* the site is alive, upstream the change to the mother pattern, and every
sibling site inherits it on the next port. That's the recursive public, applied to itself.
