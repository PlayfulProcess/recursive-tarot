# Recursive Tarot — Future Plan

This repo is the **free, public, GitHub-Pages home** of the tarot grammars
(`tarot.recursive.eco`). The static viewers in `viewers/` are backend-free and
"committed to drift": good things get promoted to recursive.eco later, but the
data and the self-contained viewers live **here** first.

---

## Parked: live integration with recursive.eco (the hyperlinked grammars)

**Goal.** Each card on the static site can *also* open live in the recursive.eco
app — the full experience (oracle, AI reading, fork). The static deep-link
mechanism is already proven (see below); the only missing ingredient is that the
grammars must exist in Supabase with stable UUIDs.

**Status (Jun 2026).** Static deep-links are DONE and live. Live integration is
**parked** until we choose the import path.

### What already works (no backend)
- `viewers/cards.html` honors `?item=<id>` — opening a card writes it to the URL
  (shareable), and loading with it auto-opens that card.
- On the fat meta (`all-decks-many-lenses`), every card carries
  `metadata.source_deck` (repo slug) + `metadata.source_item_id` (card id in that
  deck). The modal shows **"Open in <deck> deck →"** which loads
  `cards.html?src=../tarot/<slug>/grammar.json&item=<card-id>`. All 811 source
  cards resolve. This is the same `grammar-viewer.html` mechanism recursive.eco
  uses in production (CardDetailModal → `getTarotViewerUrl` → `?item=`), so the
  static site is a faithful rehearsal of the live path.

### The live path (two options)

**Prerequisites for either:** each imported deck must be `is_public = true`, and
the import must preserve `document_data.items[].id` exactly (the `?item=` join
needs `source_item_id` to still match). Log in / own as **pp@playfulprocess.com**.

1. **UI import (manual, ~13 decks).** Import each deck via the recursive.eco
   Create flow, publish public, then **capture each deck's UUID** and build a
   `slug → UUID` map. Pros: no scripting. Cons: **not idempotent** — re-importing
   a deck mints a NEW UUID and breaks any hardcoded links; you must re-capture.
2. **Script import (idempotent).** Stamp a **deterministic UUIDv5** (namespace +
   deck slug) into each repo grammar locally, then `upsert` into Supabase keyed on
   that id. Pros: reproducible, repo stays the source of truth, links never rot,
   no read-back. Cons: one script to write. **Recommended.**

Then: add an "Open live in recursive.eco" link to each static card pointing at
`recursive.eco/pages/grammar-viewer.html?type=tarot&id=<uuid>&item=<card-id>`,
using the `slug → UUID` map.

### ⚠️ UI round-trip fragility (learned the hard way, Jun 2026)
The recursive.eco "Merge edit" write-back **drops custom top-level grammar fields**
it doesn't know about. A UI round-trip on Visconti-Sforza silently stripped:
`lineages`, `roots`, `shelves`, `worldview`, `_grammar_commons`, `_github_source_url`
(restored from git `cf4f242`). Items, images, sections, and L1 metadata survived.
**If you import/edit a deck via the UI, re-check these top-level fields against the
repo afterward and restore any that were dropped.** The script path avoids this
entirely.

---

## Parked: GitHub App write architecture (fixes the silent-overwrite class)

**Why this exists.** What bit us on Visconti-Sforza (the UI write-back silently
stripping `lineages`/`roots`/`shelves`/`worldview`) is a *symptom of the write
architecture*, not a one-off bug: recursive.eco writes to the public repo by
**direct commit to `main`, full-file replace, no review, no validation**, committed
as the builder's personal GitHub identity (that's why merge commits read
*"Merge edit by … [Anonymous]"*). A PR-based GitHub App fixes nearly all of it.

### Core principle
**Repo = source of truth. Supabase = a queryable projection of it. recursive.eco =
the editor.** Today those roles are blurred (Supabase treated as truth, repo as a
backup, writes flowing both ways with no gate). Pick the repo as canonical and make
**every write pass through a gate.**

### What's wrong with the current write path
- **Full-file replace** → any field the serializer doesn't know about is dropped (the Visconti bug). *Fix: deep-merge onto the existing file, never replace.*
- **Direct-to-main** → a bad write is live instantly and destructively; no diff catches it.
- **Personal PAT / identity** → email-privacy push rejections, "Anonymous" attribution, one person's token gates everyone, broad scope, expiry.
- **No CI** → nothing validates the JSON against `GRAMMAR_FORMAT.md` before it lands.

### Target architecture
```
recursive.eco (editor)
   │  edit intent
   ▼
GitHub App ──deep-merge onto current file──▶ branch + Pull Request
   │                                            │
   │                                 GitHub Action (the gate):
   │                                 • JSON parses
   │                                 • conforms to GRAMMAR_FORMAT schema
   │                                 • NO required top-level field dropped ◀ kills the Visconti bug
   │                                 • images resolve, manifest regenerates
   │                                            │
   │                       owner + checks green → auto-merge
   │                       outside contributor  → waits for review
   ▼                                            ▼
push to main ──webhook──▶ Supabase reindex (upsert by UUIDv5) + Pages redeploy
```

### Why a GitHub App (not a PAT or OAuth App)
The right primitive for a multi-tenant platform writing to *many users'* repos:

| | PAT | OAuth App | **GitHub App** |
|---|---|---|---|
| Identity on commits | builder's gmail | acts as user | **`recursive-eco[bot]`** (fixes email-privacy + attribution) |
| Scope | broad, all repos | broad, user's repos | **fine-grained: contents + pull_requests only, per installed repo** |
| Token | long-lived, leak-prone | user refresh | **short-lived (1 hr) installation tokens** |
| Multi-user | juggle everyone's PAT | per-user tokens | **each user installs it on their own repo** |
| Rate limit | per user | per user | **per installation, scales** |
| Revocable by user | no | clumsy | **uninstall per repo (matches "users own their data")** |

The App also nails the stated ethos — *users own their data via git*: they install
the app on their repo, grant only contents + PR, and can revoke anytime. A real
ownership story, not a we-hold-your-token story.

### Isn't PR-per-edit too heavy? No — auto-merge-on-green
The owner's edit still feels one-click: branch → PR → CI validates → **auto-merges in
seconds**. You get the diff, the validation gate, and provenance for free, and a bad
write becomes a *closeable PR* instead of a destructive overwrite. Non-owner edits
(the Editor/contributor model) naturally become PRs that **wait for review** — exactly
the moderation flow we want anyway, and where the maintainer↔contributor messaging
(built Jun 9 2026) becomes PR review comments instead of notification rows.

### Phased plan (estimates in **sessions**, per the build-with-Claude rule)

- **Phase 0 — deep-merge write + schema-validation GitHub Action.** ~1 session, **high confidence, no external handoff.** Kills the data-loss bug immediately. **Do this first regardless of everything else** — it removes ~80% of the pain (no silent field loss, no invalid grammars on `main`) for a fraction of the effort, and needs zero auth changes.
- **Phase 1 — GitHub App for auth** (bot identity, scoped install tokens). ~1–2 sessions of code, **medium confidence** — the gate is the *external handoffs only the builder can do*: register the App in GitHub settings, generate + store the private key, set the webhook secret. Security-sensitive; **checkpoint with the builder on the token-minting code before it runs unsupervised.**
- **Phase 2 — PR + auto-merge-on-green.** ~1 session once the App exists.
- **Phase 3 — webhook → Supabase reindex** (repo becomes canonical). ~1–2 sessions; this is where the idempotent **UUIDv5** from the import-flow plan above pays off (stable repo-file ↔ Supabase-row mapping, no read-back).

### Recommendation
**Do Phase 0 now; decide on the App after.** Even if the GitHub App never gets built,
switching the write to deep-merge + adding a validation Action removes most of the
pain. The App is the right *destination* — bot identity, scoped tokens, PR review, the
ownership story — but it's a security-sensitive build with handoffs only the builder
can do, so it deserves its own focused session rather than being rushed in alongside
everything else.

### Contribution models — how a community edits (e.g. historians on a public deck)

Two paths, with different maturity today:

**A. Edit *in the app* (works now — no GitHub account needed).** Mark the deck *Community*
(`open_to_community`). Contributors sign in to recursive.eco, self-add as Editors, edit
cards, and submit. Proposals **stage in the private vault**, not the public repo. The
maintainer reviews each in the Pending Edits panel (preview diff, leave a note/message),
then Accept → **deep-merges** into the public repo + Supabase (curatorial fields survive),
now committed as `recursive-eco[bot]`. This is the Design V flow, verified end-to-end.

**B. Edit *via GitHub directly* (repo works; app-sync pending).** A contributor with GitHub
access edits `grammar.json` / opens a PR; the maintainer merges on GitHub. The PR is gated
by the `validate-grammar` Action (parse + required fields + no dropped top-level field).
**Gap:** a direct-GitHub merge does not yet flow back into Supabase, so the app won't show
it until **Phase 3 (webhook → reindex)** lands. Until then, Path A is the reliable route
even for GitHub-comfortable contributors.

**C. Bring-your-own-repo (not yet).** The vision: a community owns *their* repo, installs the
`recursive-eco[bot]` App on it, and edits via app or GitHub — they own the data and can
uninstall anytime. Needs the App scope flipped to "Any account" + an install-registration
UI + a per-user installation→repo mapping. The hardcoded writable-repo allow-list
(`recursive-tarot`, `recursive.eco-schemas`) becomes per-installation.

### Phase status (Jun 9 2026)
Phase 0 (deep-merge) ✅ live · Phase 1 (App auth + bot writes) ✅ done · Phase 2 (validation
Action) ⏳ templates ready, needs repo install + branch protection · Phase 3 (webhook
reindex) 🟡 dry-run scaffold · Bring-your-own-repo ⛔ not started.

### Interim mitigation already in place
- Design V (Jun 9 2026): proposals always stage + read from the private vault, so a public-repo-backed deck's pending edits are visible to the maintainer. Merge is still full-replace, so the deep-merge fix (Phase 0) is the next guard.
- The ⚠️ note above ("re-check top-level fields after a UI round-trip") remains the manual workaround until Phase 0 lands.

---

## Viewers

- `viewers/cards.html` — card grid + hierarchy sidebar + per-card deep-links.
- `viewers/tree-viewer.html` — faceted level-rows tree (L1/L2/L3 by deck/age/rank/…).
- `viewers/genealogy-tree.html` — **NEW radial "Tree of Life."** Renders
  `tarot/tree-of-tarot` as root → 6 scholarly branches → decks, with the actual
  `derives_from` descent overlaid as curved arcs (hover a deck to trace its
  lineage upstream). Click → detail panel + "Open <deck> cards." Self-contained
  D3, no backend.
- `viewers/caster.html` — draw 3 cards (one deck or cross-deck) → export JSON for
  recursive.eco Journal.
- `genealogy.html` — Cytoscape force-graph of the genealogy.

### Tree-format ideas not yet built
- **Chronological phylogeny**: place decks on a horizontal time axis (parse
  `metadata.when` → year) with `derives_from` edges — shows descent *and*
  chronology at once. `deck-italian-trionfi` is referenced as an ancestor by 6
  decks but isn't yet a node; add it (or a synthetic "trionfi root") so those
  descent arcs render.
- **Archetype axis** (cross-deck): one card (e.g. Death) across all decks, joined
  on the stamped `metadata.archetype` controlled vocabulary. Engine is general;
  tarot is the first dictionary.
