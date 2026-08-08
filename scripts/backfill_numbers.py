# -*- coding: utf-8 -*-
"""Backfill missing metadata.number on leaf cards, lifted from the item's own
id or name — never invented, never overwritten.

Why: the Explorer groups any card without metadata.number into a single "—"
bucket. Measured 2026-08-07: 670 of 1,918 leaf cards across the deck grammars
had no metadata.number. Many of those numbers are NOT missing data — they are
sitting in the item's id (`major-00-il-matto`, `tattva-01`, `card-07-…`) or
name ("Ace of Cups", "3 of Coins", "1 · The Rider", "12 — The Birds") and were
simply never copied into metadata. This script lifts them, and only them.

Derivation, in order of confidence (never guesses beyond these three):
  1. A rank word or leading numeral in the name, for suited (minor) cards —
     Ace..Ten / Page·Jack·Knave·Knight·Queen·King -> 1..14. Mirrors
     rank_from_name() in scripts/build_meta_grammar.py exactly (same word
     list, same court -> 11-14 convention) so a card's number always agrees
     with what the meta-grammar already derives from the same name.
  2. A leading number in the name ("1 — The Beggar", "6 — Temperance",
     "12 · The Birds").
  3. A zero-padded (or bare) number embedded in the item id
     (`major-00-…`, `trump-14-…`, `tattva-01`, `card-07-…`, `clown-00`),
     for majors/trumps (capped at the deck's own known trump range, default
     0-21) and for decks with their own non-suited numbered sequence
     (Lenormand, Mantegna plates, tattvas) — capped generously (<=99) and
     de-duplicated per deck so a museum catalogue/sheet id (see
     SKIP_ID_NUMBER_DECKS below) can't masquerade as a card number.

What it will NOT do: assign a canonical/RWS archetype number by matching a
major's NAME alone (e.g. "Strength" -> 8). That mapping is exactly right for
the generated meta-grammar's cross-deck archetype lens (build_meta_grammar.py
major_from_name()) but WRONG here — several decks in this repo (Bologna,
Arlecchino, the Bolognese "A-order" family) follow a documented historical
trump order that does not match the RWS/Marseille sequence, and there is
no textual number in their id/name to confirm it either way. Filling those
from a name-only archetype match would silently overwrite a real ordering
question with an invented one. Left unnumbered on purpose — see the report's
"deliberately unnumbered" section.

Idempotent and additive-only: never overwrites an existing metadata.number,
never touches any other field. Safe to re-run.

Usage:
  python scripts/backfill_numbers.py            # dry run (default) — report only
  python scripts/backfill_numbers.py --write     # write changes to disk
"""
import argparse
import glob
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console default is cp1252

HERE = os.path.dirname(__file__)
TAROT = os.path.abspath(os.path.join(HERE, "..", "tarot"))

# Generated grammars — never hand-edit (per CLAUDE.md), never touch here either.
GENERATED = {"all-decks-many-lenses", "people-of-tarot"}
# Another agent is actively editing these two this session — skip entirely.
SKIP_DECKS = GENERATED

# este-tarot's `card-NN` ids are the surviving fragment's museum/uncut-sheet
# catalogue position, not a trump sequence. Proof, from the deck's OWN
# already-numbered court cards: card-01 -> King (num=14), card-07 -> King
# again (num=14), card-13 -> King again (num=14) — the same id template
# lands on the same rank three different times at three different id
# numbers, and neighbouring ids (03/05/09/11/15) land on three other
# different ranks. That is a sheet-position id, not a card number. Confirmed
# by spot-check 2026-08-08 — never derive a number from this deck's ids.
SKIP_ID_NUMBER_DECKS = {"este-tarot"}

# Leaf definition mirrors build_meta_grammar.py's own filter (see its build()):
# skip composite/emergence/axis/overview nodes, keep only real L1 cards.
NON_LEAF_CATEGORIES = {"axis", "keyword-emergence", "overview"}

# --- Name-based rank derivation — copied verbatim from build_meta_grammar.py
# rank_from_name() so a card's number always agrees with what the
# meta-grammar independently derives from the same name. Do not diverge. ---
_PIP_WORDS = [("ace", 1), ("two", 2), ("three", 3), ("four", 4), ("five", 5),
              ("six", 6), ("seven", 7), ("eight", 8), ("nine", 9), ("ten", 10)]


def rank_from_name(name):
    n = (name or "").lower()
    for w, r in _PIP_WORDS:
        if re.search(r"\b" + w + r"\b", n):
            return r
    if re.search(r"page|knave|valet|fante|maid|servante", n):
        return 11
    if re.search(r"knight|chevalier|cavall", n):
        return 12
    if re.search(r"queen|reine|regina|dama", n):
        return 13
    if re.search(r"king|\broi\b|\bre\b", n):
        return 14
    m = re.match(r"^\s*(\d+)\s+of\s", n)
    if m:
        return int(m.group(1))
    return None


# A leading number in the name: "0 — The Fool", "1 · The Rider", "12. The Birds".
# Requires an explicit delimiter right after the digits so a card whose NAME
# just happens to be a number (anecdotes-tarot's "81") is never mistaken for
# a positional marker — "81" has no trailing "-·.:" so this never matches it.
_LEADING_NUM_RE = re.compile(r"^\s*(\d{1,3})\s*[-‐-―·.:]")

# A number embedded in the id, delimited by hyphens or the string's edges:
# "major-00-il-matto" -> 00, "trump-14-diavolo" -> 14, "tattva-01" -> 01,
# "card-07-x" -> 07, "card-0" -> 0. Deliberately bounded to 1-3 digits so a
# long catalogue/UUID number segment (madiao's "card-102351", ontoject's hex
# UUIDs) can never match.
_ID_NUM_RE = re.compile(r"(?:^|-)(\d{1,3})(?=-|$)")


def leading_number_in_name(name):
    m = _LEADING_NUM_RE.match(name or "")
    return int(m.group(1)) if m else None


def id_embedded_number(item_id):
    m = _ID_NUM_RE.search(item_id or "")
    return int(m.group(1)) if m else None


# Suit vocabulary an "X of <suit>" name can end in — deliberately a specific
# word list, NOT a bare "\bof\b" check. rank_from_name()'s court-word patterns
# (below, copied verbatim from build_meta_grammar.py) are unbounded substring
# matches ("king", "queen", "knight" with no \b), so gating on any name that
# merely contains "of" is unsafe: "Book of Right-On" and "Waltz of the 101st
# Lightborne" (anecdotes-tarot) both contain "of" and would spuriously read
# as suited, and course-lesson titles like "The Four Suits" or "Two voices,
# one ecosystem" spuriously contain a pip word. Requiring an actual suit word
# after "of" is what makes it safe to try rank_from_name at all.
_SUIT_WORD_RE = re.compile(
    r"\bof\s+(the\s+)?(wand|baton|bastoni|cup|coupe|coppe|sword|[ée]p[ée]e|spade"
    r"|coin|pentacl|denier|denari|polo|cash|string|myriad)", re.I)


def has_suit_context(metadata, name):
    """Gate for minor-rank derivation: an explicit metadata.suit, or an
    "X of <suit>" name shape (Ace of Cups, King of Swords, Mamluk's
    "Malik … — King of Cups", "… King of Polo-sticks")."""
    if metadata.get("suit"):
        return True
    return bool(_SUIT_WORD_RE.search(name or ""))


def is_major_ish(metadata, category, has_suit):
    """A trump/major-arcana-shaped item: no suit, and its own category or
    arcana says so. Used only to pick the id-number range/cap — never to
    assign a canonical archetype number (see module docstring)."""
    if has_suit:
        return False
    cat = (category or "").lower()
    arcana = (metadata.get("arcana") or "").lower()
    return arcana in ("major", "trump") or "trump" in cat or "major" in cat


def _leaves(items):
    return [it for it in items
            if not it.get("composite_of")
            and it.get("category") not in NON_LEAF_CATEGORIES]


# Non-card leaves that are still real leaves (no composite_of) but were never
# candidates for a "card number" in the first place — course lessons and book
# citations (id prefix), and extra/role cards that sit outside any deck's own
# ranked sequence (Cary-Yale's virtues, tarocchino-arlecchino's Harlequin
# significators — real cards, just not ones with a rank). Left alone entirely
# — no rule below is even attempted — so they never turn a lesson's position
# in a course, or a significator's physical slot in the deck, into something
# that reads as a trump/pip number.
def _out_of_scope(item_id, category, arcana):
    if (item_id or "").startswith(("lesson-", "book-")):
        return True
    cat = (category or "").lower()
    arc = (arcana or "").lower()
    return cat in ("significator", "virtue") or arc in ("significator", "virtue")


def process_grammar(slug, g, write):
    items = g.get("items", [])
    leaves = _leaves(items)

    before_missing = 0
    filled = 0
    fill_log = []          # (id, name, number, source) for filled items
    still_missing = []     # items left without a number

    pending_id_fallback = []
    for it in leaves:
        md = it.get("metadata") or {}
        if md.get("number") is not None:
            continue
        before_missing += 1
        name = it.get("name") or ""
        if _out_of_scope(it.get("id"), it.get("category"), md.get("arcana")):
            still_missing.append(it)
            continue
        suited = has_suit_context(md, name)

        candidate, source = None, None
        if suited:
            r = rank_from_name(name)
            if r is not None:
                candidate, source = r, "name-rank"
        if candidate is None:
            ln = leading_number_in_name(name)
            if ln is not None:
                candidate, source = ln, "name-leading"

        if candidate is not None:
            fill_log.append((it.get("id"), name, candidate, source))
            if write:
                it.setdefault("metadata", {})["number"] = candidate
            filled += 1
        elif not suited:
            pending_id_fallback.append(it)
        else:
            still_missing.append(it)

    # id-embedded number fallback — majors/trumps and other deck-own
    # numbered sequences (Lenormand, Mantegna plates, …) only; never for
    # suited minors (those always resolve, or don't, via rank_from_name above).
    if slug in SKIP_ID_NUMBER_DECKS:
        still_missing.extend(pending_id_fallback)
    else:
        # Effective major/trump cap = 21 (standard tarot), or higher if this
        # deck's OWN rank_from_name/leading-number pass already established a
        # higher trump number (e.g. minchiate-florence-tarot's trump-40).
        major_cap = 21
        used_major_numbers = set()
        for it in leaves:
            md = it.get("metadata") or {}
            n = md.get("number")
            # Some decks (belgian/paris-anonymous/vieville) already store the
            # printed Roman numeral ("I".."XXI") as metadata.number — a real,
            # deliberate value, just not one this cap/dedupe math can use.
            # Skip it here; it's already filled, so it never reaches this
            # script's own fill path either way.
            if not isinstance(n, (int, float)):
                continue
            if is_major_ish(md, it.get("category"), has_suit_context(md, it.get("name") or "")):
                major_cap = max(major_cap, int(n))
                used_major_numbers.add(int(n))

        used_other_numbers = {}  # category -> set(numbers already used)
        for it in leaves:
            md = it.get("metadata") or {}
            n = md.get("number")
            if not isinstance(n, (int, float)):
                continue
            cat = it.get("category")
            if not is_major_ish(md, cat, has_suit_context(md, it.get("name") or "")):
                used_other_numbers.setdefault(cat, set()).add(int(n))

        for it in pending_id_fallback:
            md = it.get("metadata") or {}
            name = it.get("name") or ""
            category = it.get("category")
            n = id_embedded_number(it.get("id") or "")
            if n is None:
                still_missing.append(it)
                continue
            if is_major_ish(md, category, False):
                if n > major_cap or n in used_major_numbers:
                    still_missing.append(it)
                    continue
                used_major_numbers.add(n)
            else:
                bucket = used_other_numbers.setdefault(category, set())
                if n > 99 or n in bucket:
                    still_missing.append(it)
                    continue
                bucket.add(n)
            fill_log.append((it.get("id"), name, n, "id-number"))
            if write:
                it.setdefault("metadata", {})["number"] = n
            filled += 1

    return dict(
        deck=slug, before=before_missing, filled=filled,
        still_missing=len(still_missing),
        examples=[(it.get("id"), it.get("name")) for it in still_missing][:5],
        fill_log=fill_log,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true",
                     help="write changes to disk (default: dry run, report only)")
    ap.add_argument("-v", "--verbose", action="store_true",
                     help="print every fill (id, name, number, source), not just the summary table")
    args = ap.parse_args()

    reports = []
    total_before = total_filled = total_after = 0

    for path in sorted(glob.glob(os.path.join(TAROT, "*", "grammar.json"))):
        slug = os.path.basename(os.path.dirname(path))
        if slug in SKIP_DECKS:
            continue
        with open(path, encoding="utf-8") as f:
            g = json.load(f)
        report = process_grammar(slug, g, args.write)
        if report["before"] == 0:
            continue
        reports.append(report)
        total_before += report["before"]
        total_filled += report["filled"]
        total_after += report["still_missing"]
        if args.write and report["filled"]:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(g, f, indent=2, ensure_ascii=False)

    # --- report ---
    mode = "WRITE" if args.write else "DRY RUN"
    print(f"backfill_numbers.py — {mode}\n")
    hdr = f"{'deck':<32}{'before':>8}{'filled':>8}{'after':>8}   examples still missing"
    print(hdr)
    print("-" * len(hdr))
    for r in reports:
        ex = "; ".join(f"{i} ({n})" for i, n in r["examples"]) if r["still_missing"] else ""
        print(f"{r['deck']:<32}{r['before']:>8}{r['filled']:>8}{r['still_missing']:>8}   {ex}")
    print("-" * len(hdr))
    print(f"{'TOTAL':<32}{total_before:>8}{total_filled:>8}{total_after:>8}")

    if args.verbose:
        print("\nAll fills:")
        for r in reports:
            for iid, name, num, source in r["fill_log"]:
                print(f"  [{r['deck']}] {iid} | {name!r} -> number={num} ({source})")

    if not args.write:
        print("\n(dry run — pass --write to save)")


if __name__ == "__main__":
    main()
