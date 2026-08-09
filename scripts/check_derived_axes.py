# -*- coding: utf-8 -*-
"""Semantic regression check for the derived pivot axes on the built meta grammar.

`check_all.py` is structural only (dangling composite_of, valid JSON, mojibake) — it
would happily pass a meta grammar whose `role` / `trump_number` / `rank` / `deck`
fields have quietly rotted, exactly the way the old overloaded `number` field did
before the Aug 7 2026 revamp (_research/TAROT-REVAMP-PLAN-2026-08-07.md Phase 1).
This pins the semantics `scripts/build_meta_grammar.py` is supposed to guarantee:

  1. every card with role == "trump" that has a resolvable `number` also has a
     non-null `trump_number` (the split-axis invariant the revamp introduced);
  2. every card's `role` is one of trump / pip / court / other (no stray values);
  3. `rank` is set for pip/court cards and absent for trump cards (the axis split
     is supposed to be exhaustive and mutually exclusive);
  4. no card's `metadata.deck` disagrees with the deck it was aggregated from —
     the cross-link misattribution bug (audit 2026-08-07 §5): a card's own
     cross-link `metadata.deck` field (pointing at some OTHER grammar, e.g. a
     People or Books cross-link) must never leak into the per-deck pivot label.
     47 items across 5 decks were wrong before the Aug 7 fix. Checked here
     against the meta grammar's own "deck-<slug>" node name, so no separate
     source-of-truth table needs to be kept in sync with build_meta_grammar.py.

Run standalone:  python scripts/check_derived_axes.py
Called by check_all.py after it rebuilds the meta grammar. Exits non-zero on
any failure, printing the offending item ids (not just a count).
"""
import json, os, sys

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
META_PATH = os.path.join(ROOT, "tarot", "all-decks-many-lenses", "grammar.json")

VALID_ROLES = {"trump", "pip", "court", "other"}


def build_id_index(items):
    return {it.get("id"): it for it in items}


def main():
    if not os.path.exists(META_PATH):
        print(f"FAIL: meta grammar not found at {META_PATH} — run build_meta_grammar.py first")
        return 1

    g = json.load(open(META_PATH, encoding="utf-8"))
    items = g.get("items", [])
    by_id = build_id_index(items)
    cards = [it for it in items if it.get("category") == "card"]

    errors = []

    # 1. trump + resolvable number => non-null trump_number
    bad_trump_number = []
    for it in cards:
        m = it.get("metadata", {}) or {}
        if m.get("role") == "trump" and m.get("number") is not None and m.get("trump_number") is None:
            bad_trump_number.append(it["id"])
    if bad_trump_number:
        errors.append(
            f"{len(bad_trump_number)} trump card(s) have a resolvable `number` but no `trump_number`: "
            + ", ".join(bad_trump_number[:20]) + (" ..." if len(bad_trump_number) > 20 else "")
        )

    # 2. role in the closed vocabulary
    bad_role = []
    for it in cards:
        role = (it.get("metadata", {}) or {}).get("role")
        if role not in VALID_ROLES:
            bad_role.append(f"{it['id']} (role={role!r})")
    if bad_role:
        errors.append(f"{len(bad_role)} card(s) have an invalid `role`: " + ", ".join(bad_role[:20])
                       + (" ..." if len(bad_role) > 20 else ""))

    # 3. rank set for pip/court, absent for trump
    bad_rank = []
    for it in cards:
        m = it.get("metadata", {}) or {}
        role = m.get("role")
        rank = m.get("rank")
        if role in ("pip", "court") and rank is None:
            bad_rank.append(f"{it['id']} (role={role}, rank missing)")
        elif role == "trump" and rank is not None:
            bad_rank.append(f"{it['id']} (role=trump, rank={rank!r} should be absent)")
    if bad_rank:
        errors.append(f"{len(bad_rank)} card(s) violate the rank/role split: " + ", ".join(bad_rank[:20])
                       + (" ..." if len(bad_rank) > 20 else ""))

    # 4. deck cross-link misattribution — metadata.deck must match the deck node
    #    the card was actually aggregated under (its own source_deck), not any
    #    cross-link `deck` label the source item itself might carry.
    bad_deck = []
    for it in cards:
        m = it.get("metadata", {}) or {}
        source_deck = m.get("source_deck")
        deck_label = m.get("deck")
        if not source_deck:
            bad_deck.append(f"{it['id']} (no source_deck)")
            continue
        deck_node = by_id.get("deck-" + source_deck.replace("-", ""))
        if deck_node is None:
            continue  # source_deck without a corresponding deck node (e.g. ancestor) — not this check's concern
        expected = deck_node.get("name")
        if deck_label != expected:
            bad_deck.append(f"{it['id']} (source_deck={source_deck}, metadata.deck={deck_label!r}, expected {expected!r})")
    if bad_deck:
        errors.append(f"{len(bad_deck)} card(s) misattributed to the wrong deck: " + ", ".join(bad_deck[:20])
                       + (" ..." if len(bad_deck) > 20 else ""))

    if errors:
        print(f"FAIL: {len(errors)} derived-axes check(s) failed ({len(cards)} cards checked):")
        for e in errors:
            print("  -", e)
        return 1

    print(f"OK: derived axes check passed ({len(cards)} cards checked, dangling deck-mismatch=0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
