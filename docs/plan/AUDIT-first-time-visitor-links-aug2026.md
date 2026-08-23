# First-time-visitor link audit — Aug 22 2026

*Prompted by a real bug she hit: the contribute course's card-browser link defaulted to the
meta grammar, and Edit there dead-ended at a Library redirect. That specific bug is fixed (see
"Already shipped" below). She then asked for a broader sweep — 5 agents walked the site as
naive first-time visitors from different entry points (Player, Historian, Practitioner/Intention,
Contributor, and a systematic multi-deck sweep) and reported every dead end, broken redirect, or
confusing moment they hit. This doc is the synthesis. Nothing below is fixed except what's marked
shipped — this is a decision/priority document, not a change log.*

## Already shipped (this session)

1. **Per-card "Edit in recursive.eco" button hidden on `_generated` aggregators** (meta grammar,
   people-of-tarot) — `viewers/cards.html` commit `17e5a70`. Their pointer-stub items have no
   real UUID to resolve, so Edit fell through to a bare Create page that redirects to Library.
2. **Page-header "Edit" button, same fix, one level up** — commit `9fa3535`/`cebd675`. Found by
   the Player-path audit agent: the header pen/Edit button had the identical bug, just not on
   the per-card modal.
3. **Contribute course + `pages/contribute.html` links repointed** at Visconti-Sforza's own page
   (public, known-working) instead of the bare meta view / a private "Ontoject" grammar link that
   was broken for anyone but her.

## Cleared — she tested it herself

**"Interpret with AI" on the Caster.** Two agents reported this as broken signed-out (a chat panel
stuck at 72px width; separately, 401s with a vague message instead of a sign-in prompt). She tried
it live (Aug 22) and the sign-in + interpretation flow worked for her — **clearing this from the
list.** Not chasing the 72px width report further without a live repro; if it resurfaces, it's a
CSS class-timing issue in the `rec-assistant-shell`/`rec-open` toggle worth a fresh look then.

## Not reproducible — investigated, no fix made

**"Tree" nav link.** The audit reported `viewers/tree-viewer.html` auto-redirecting into
`caster.html` → `caster-studio.html` on load. Re-tested live (fresh tab, no cache, waited 3s after
load): it loads correctly and stays on the meta-grammar tree view, no redirect. Also confirmed by
reading the source — `loadGrammar()` defaults to the meta grammar exactly like `cards.html` does;
the only `caster.html` reference in the file is the (correct, intentional) "Cast a Reading" button.
**The homepage's bare `viewers/tree-viewer.html` link is fine as-is** — it's one of four sibling
"Card level" view cards (Cards/Explorer/Lenses/Tree) that all deliberately link bare and default to
the meta grammar; my first draft of this doc wrongly suggested repointing it at `genealogy-tree.html`
or `genealogy.html`, which are a different, deliberately separate "whole collection" feature — that
suggestion was wrong and is retracted. Likely the audit agent clicked something mid-exploration
without realizing it. No further action here unless it reproduces again with a clear repro.

## High priority — 5 decks can't actually be cast, and now we know exactly why

Confirmed by direct database lookup (not inference): **all five are `is_public: false`.**

| Deck | Items | Type | Cast symptom |
|---|---|---|---|
| Cary Sheet | 1 (stub) | unified_grammar | 404 from `tarot-channel/decks/{id}`, spinner never resolves |
| The Rosenwald Sheet | 1 (stub) | unified_grammar | same |
| Ganjifa | 1 (stub) | unified_grammar | same |
| Jean Noblet Tarot de Marseille | 1 (stub) | unified_grammar | same, retested twice |
| **The Ontoject — Illustrated** | **24 (real content)** | tarot_deck | same |

The first four are genuine placeholder stubs (1 item, generic `unified_grammar` type) — they were
never finished, and being private is presumably intentional until they are. **The Ontoject is a
fully-built 24-card deck that simply isn't published** — it's not a stub, it's finished and private.
It was linked from `pages/contribute.html`'s "Edit a card now" button until today's fix moved that
link to Visconti-Sforza instead, so a first-time visitor no longer hits it through that specific
door — but it's still listed in the "All Decks" meta view's deck switcher, so anyone browsing there
and picking it will still hit the same 404.

**This needs your call, not mine** — it's your content:
- Do any of the 4 stub decks need finishing + publishing, or should their card-browser pages show
  the GitHub-only door (matching how the course's own deck table already correctly curates them)
  instead of a Cast/Edit button that can never work while they're private?
- Is The Ontoject meant to go public? It reads like a real, finished piece — if so, one
  `set_grammar_visibility` call publishes it and Cast starts working immediately. If it should stay
  private for now, its entry could be pulled from the meta view's deck switcher so visitors don't
  find the dead end at all.

This sweep only checked 9 of ~35+ decks; a fuller pass would likely find a few more in the same
state — worth a full `is_public` audit across all `tarot/_eco_ids.json` entries at some point.

## Medium priority

- **Spread Studio and Caster are the same page.** `caster-studio.html` and `caster.html` are
  byte-for-byte identical in content and controls, despite being presented as two different tools
  ("fancier Spread Studio" vs. plain Caster) in nav copy and in the how-to-contribute course. Either
  merge the copy/naming down to one tool, or actually differentiate them.
- **Cross-link pills ("Open in [X] →") don't appear on individual deck cards.** The pattern exists
  and works well — but only in two places: the meta aggregator (card → its own source deck) and
  inside Books/People entries (linking to each other). A card on e.g. Visconti-Sforza's own page
  never links out to the person who made it or a book that discusses it, despite that being the
  documented intent of the pattern. Confirmed absent on 4 sampled cards across 3 well-known decks.
- **Books Behind the Tarot / People & Institutions have no nav path.** Neither the homepage nor
  `pages/historian.html` link to them — they're only reachable by guessing the URL or by already
  being on a cross-linked entry. Worth a "Sources" nav entry or a homepage card.

## Small / already queued

- **GitHub edit links across the contribute course point at the retired `dev` branch**
  (confirmed via the GitHub API: `default_branch` is `main`). The Spread Studio's own "Contribute
  a spread on GitHub" button already correctly targets `main`, so this is a real inconsistency, not
  policy. *(Already spawned as a separate task earlier today — task title "Fix stale 'dev branch'
  PR references in recursive-tarot" — this audit just independently confirms it's real and
  sitewide, not just in the one spot originally found.)*
- Course text says "Spreads live in `viewers/spreads.json`," but the GitHub button actually creates
  a new file at `spreads/my-spread.json` — different path than what's written.
- `contribute.html`'s Path 3 CTA ("draft in claude.ai chat, copy-paste the result") links to the
  Rung 5 MCP-connector instructions instead of Rung 3 (the actual copy-paste workflow it describes).
- "Contribute a video" section only offers a Claude-Code prompt, despite the course's own promise
  that "you don't need to touch JSON by hand" — no simpler UI path exists for this one.
- Sitewide 401 console noise on nearly every page load while signed out (harmless today, but a
  standing error signature that could hide a real regression later).
- Minor redundancy in the meta card modal: "Open in X deck →" and "View this card in X →" sit next
  to each other and appear to do the same thing.

## Confirmed clean

**The ethics/voice framing was explicitly stress-tested and passed.** All 8 voices (Kant, DBT,
The Ecosystem, Jung, Non-Dual Tantra, Post-Activism, Hospicing Modernity, Golden Dawn) consistently
use "inspired by / a lens, not \[their\] words" language in both the Caster carousel and the
Intention Setting course — nothing found claims to speak as or channel a living teacher. The
Golden Dawn course was specifically praised for clearly separating the Order's own historical
claims from the site's "gate not fate" reframing.

**What was genuinely delightful**, for the record — worth protecting, not just fixing bugs:
the Tree of Tarot genealogy view, the Books↔People bidirectional cross-linking, the Trionfi
trick-taking game (loads instantly, no sign-in, real historical deck), the Journal's signed-out
sign-in flow with a Guest option, and the Rider-Waite-Smith card browser's grouping UI.
