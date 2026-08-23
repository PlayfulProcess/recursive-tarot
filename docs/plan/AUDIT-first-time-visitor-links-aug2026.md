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

## Highest priority — the core reading experience is broken signed-out

**"Interpret with AI" fails on both `caster.html` and `caster-studio.html`, found independently by
two agents:**
- The chat panel's width sticks at 72px instead of its designed 384px (confirmed via
  `getComputedStyle`, reproduced twice) — it's technically "open" but renders as an invisible
  sliver.
- Separately (or relatedly — same root feature): 10+ console 401s fire, and the UI shows only a
  vague "it will be sent automatically once the app updates" message instead of a clear sign-in
  prompt.
- **Why this matters more than anything else here:** this is the single moment the site is trying
  to deliver its core value (an AI reading) to a first-time visitor, and it silently fails with no
  actionable message. Contrast with the Journal's own signed-out flow, which is genuinely good
  (an honest "sign in to interpret" button + a "Continue as Guest" option) — the Caster doesn't
  match that bar.
- **Suggested next step:** reproduce the 72px width bug directly (likely a CSS class-timing issue
  in the `rec-assistant-shell`/`rec-open` toggle) and decide whether Caster's signed-out messaging
  should just match the Journal's pattern.

## High priority — several decks can't actually be cast

Two independent passes confirm Cast silently fails (infinite "Loading…" in Flow, no error shown)
for a specific subset of decks:

| Deck | Symptom |
|---|---|
| Cary Sheet | `GET /api/tarot-channel/decks/{id}` → 404, deck selector spins forever |
| The Rosenwald Sheet | same 404 pattern |
| Ganjifa | same 404 pattern |
| Jean Noblet Tarot de Marseille | same 404 pattern, retested twice |
| **The Ontoject — Illustrated** | same 404 pattern — **but this one has 24 real items, not a stub** |

The first four all show as 1-item "stub" grammars in `list_grammars` — plausibly just not fully
built out yet, and the tarot-channel endpoint 404s on near-empty decks. **The Ontoject is the odd
one out**: it's a real, populated grammar, and it's also `is_public: false` (confirmed via direct
lookup) — a private grammar can't be fetched by the anonymous-facing tarot-channel endpoint, which
is a much more plausible explanation than "stub." If Ontoject is meant to be a public example
(it's linked from `pages/contribute.html` until today's fix), it needs `set_grammar_visibility`
run on it, or the link needs to stop pointing at it.

**Suggested next step:** decide whether the stub decks (Cary Sheet, Rosenwald Sheet, Ganjifa,
Jean Noblet) are meant to be castable yet — if not, the deck table should show the GitHub-only
door for them too, the same way the other "not yet published" rare sheets already correctly do.
This sweep only checked 9 of ~35+ decks; a fuller pass would likely find more.

## Medium priority

- **"Tree" nav link is broken/misrouting.** `viewers/tree-viewer.html` (linked from the homepage's
  "Every view" grid) auto-redirects through `caster.html` into `caster-studio.html` — a completely
  unrelated spread-building tool, with 401 errors during the chain. Meanwhile two OTHER pages
  already do the "tree" job well and were called the best feature on the whole site by the
  Historian-path agent: **`genealogy-tree.html`** ("Tree of Tarot" — pannable radial genealogy,
  rich detail cards) and **`genealogy.html`** ("Genealogy Graph," honest about simplified edges).
  This reads like a stale nav link pointing at a deprecated/broken implementation instead of the
  two good ones that already exist. Likely a one-line nav fix once you confirm which of the two
  it should point to.
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
