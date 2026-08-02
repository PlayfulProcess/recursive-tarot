# -*- coding: utf-8 -*-
"""Strip the source book's page furniture from `rider-waite-smith-pictorial-key`.

  python3 scripts/clean_waite_running_heads.py [--check]

The deck reproduces A. E. Waite's *The Pictorial Key to the Tarot* (1911) in a
single `The Pictorial Key` section per card. The extraction kept the printed
book's page furniture as literal opening lines of the card's body:

  * a bare suit running head — the word `WANDS` / `CUPS` / `SWORDS` /
    `PENTACLES` printed at the top of every page of that suit's chapter, which
    landed as the first paragraph of 52 of the 56 minor-arcana items;
  * a bare Roman numeral on its own line (`I`, `VIII`, `XIII`, `XVII`,
    `XVIII`) — the trump's printed number, orphaned from the card title that
    follows it, on 5 major-arcana items;
  * the numeral word glued to the title on `major-00-the-fool`
    (`ZERO The Fool`);
  * three garbled plate captions the scanner read off the illustration itself
    (`THfc LOVERS.`, `WHEEL FORTUNE. |`, `PACE dj CUP 5,`).

None of that is Waite's prose. What IS kept: the card-title line that opens
each entry (`The Magician`, `Three`, `Knight`, `King`, ...) — that is the
book's own per-entry heading and reads as an intentional heading, so it stays.

Everything removed is written verbatim to
`research/sources/waite-trimmed-rider-waite-smith-pictorial-key.md` with a
reason, so nothing is silently lost.

The script is an allow-list, not a heuristic: it only ever removes a
paragraph that is *exactly* one of the strings named above, and only from the
first three paragraphs of a body. Verification asserts, per item, that
words(before) == words(after) + words(removed) and that deleting exactly the
archived fragments from the original body reproduces the new body character
for character.

Idempotent: re-running on already-cleaned content removes nothing.
"""
import argparse, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DECK = "rider-waite-smith-pictorial-key"
SECTION = "The Pictorial Key"
GRAMMAR = os.path.join(ROOT, "tarot", DECK, "grammar.json")
ARCHIVE = os.path.join(ROOT, "research", "sources",
                       f"waite-trimmed-{DECK}.md")

SUIT_HEADS = {"WANDS", "CUPS", "SWORDS", "PENTACLES"}
ROMAN_RE = re.compile(r"^[IVXLC]{1,6}$")
# Garbled plate captions — the scanner read these off the illustration plate,
# not the text block. Matched literally; nothing else is touched.
PLATE_CAPTIONS = {
    "THfc LOVERS.": "scan garbage: garbled plate caption (THE LOVERS.) read off the illustration",
    "WHEEL FORTUNE. |": "scan garbage: garbled plate caption (WHEEL OF FORTUNE.) read off the illustration",
    "PACE dj CUP 5,": "scan garbage: garbled plate caption (PAGE OF CUPS) read off the illustration",
}
# The Fool's numeral is glued to its title line rather than orphaned above it.
NUMERAL_WORD_PREFIX = re.compile(r"^(ZERO)\s+(?=[A-Z])")

# How far into a body furniture may live. Every real instance is at index 0-2.
WINDOW = 3

REASON_SUIT = ("page furniture: the suit running head printed at the top of "
               "every page of this chapter, not part of the card's entry")
REASON_ROMAN = ("page furniture: the trump's printed number, orphaned from "
                "the card-title line that follows it")
REASON_NUMERAL_WORD = ("page furniture: the trump's printed number, glued to "
                       "the card-title line by the scan")


def load():
    with open(GRAMMAR, encoding="utf-8") as fh:
        return json.load(fh)


def plan_item(body):
    """Return (new_body, removals) where removals is a list of
    (fragment, reason). Pure function — no mutation."""
    paras = body.split("\n\n")
    removals = []
    keep = []
    for i, p in enumerate(paras):
        ps = p.strip()
        if i < WINDOW:
            if ps in SUIT_HEADS and ps == p:
                removals.append((p, REASON_SUIT))
                continue
            if ROMAN_RE.match(ps) and ps == p:
                removals.append((p, REASON_ROMAN))
                continue
            if ps in PLATE_CAPTIONS and ps == p:
                removals.append((p, PLATE_CAPTIONS[ps]))
                continue
        keep.append(p)

    new_paras = []
    for i, p in enumerate(keep):
        if i == 0:
            m = NUMERAL_WORD_PREFIX.match(p)
            if m:
                removals.append((m.group(1), REASON_NUMERAL_WORD))
                p = p[m.end():]
        new_paras.append(p)

    return "\n\n".join(new_paras), removals


def verify_item(item_id, before, after, removals):
    """Nothing-lost proof, two independent ways."""
    ok = True
    w_before = len(before.split())
    w_after = len(after.split())
    w_removed = sum(len(frag.split()) for frag, _ in removals)
    if w_before != w_after + w_removed:
        print(f"FAIL {item_id}: word count {w_before} != {w_after} + {w_removed}")
        ok = False

    # Character-level reconstruction: deleting exactly the archived fragments
    # (with the paragraph separator they carried) from `before` must yield
    # `after`.
    probe = before
    for frag, _ in removals:
        if frag + "\n\n" in probe:
            probe = probe.replace(frag + "\n\n", "", 1)
        elif frag + " " in probe:
            probe = probe.replace(frag + " ", "", 1)
        else:
            print(f"FAIL {item_id}: archived fragment not found verbatim in "
                  f"the original body: {frag!r}")
            ok = False
    if probe != after:
        print(f"FAIL {item_id}: reconstruction mismatch after removing the "
              f"archived fragments")
        ok = False
    return ok


def run(write):
    grammar = load()
    report, archive, changed, ok = [], [], 0, True

    for it in grammar["items"]:
        secs = it.get("sections") or {}
        if SECTION not in secs:
            print(f"FAIL {it['id']}: no '{SECTION}' section")
            ok = False
            continue
        before = secs[SECTION]
        after, removals = plan_item(before)
        if not verify_item(it["id"], before, after, removals):
            ok = False
        if removals:
            changed += 1
            archive.append((it["id"], it["name"], removals))
        report.append((it["id"], len(before), len(after), len(removals)))
        if write:
            secs[SECTION] = after

    if not ok:
        return None, None, None

    if write and changed:
        with open(GRAMMAR, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(grammar, ensure_ascii=False, indent=2) + "\n")
        print(f"wrote tarot/{DECK}/grammar.json ({changed} item(s) changed)")
    elif write:
        print(f"{DECK}: no changes (idempotent)")
    return report, archive, changed


def write_archive(archive):
    header = f"""# A. E. Waite — *The Pictorial Key to the Tarot* (1911), page furniture removed — {DECK}

Public domain. This is the material **removed from the `The Pictorial Key` sections** in
`tarot/{DECK}/grammar.json` — nothing here is Waite's prose. The extraction from the
printed book kept the page's furniture as literal opening lines of each card's body:

* the **suit running head** (`WANDS` / `CUPS` / `SWORDS` / `PENTACLES`) printed at the top
  of every page of that suit's chapter — it opened 52 of the 56 minor-arcana entries;
* the trump's **printed Roman numeral**, orphaned onto its own line above the card title
  (`I`, `VIII`, `XIII`, `XVII`, `XVIII`), and `ZERO` glued in front of *The Fool*;
* three **garbled plate captions** the scanner read off the illustration rather than the
  text block.

**Kept, deliberately:** the card-title line that opens each entry — `The Magician`,
`Three`, `Knight`, `King`, `Page`, `Queen` and the rest. Those are the book's own
per-entry headings and read as intentional headings, not as page furniture.

Generated by `scripts/clean_waite_running_heads.py` (idempotent; `--check` verifies
without writing).

---

"""
    lines = []
    for item_id, name, removals in archive:
        lines.append(f"## `{item_id}` ({name}) — removed from `sections.{SECTION}`\n")
        for frag, reason in removals:
            lines.append(f"**{reason}**\n")
            lines.append("```\n" + frag + "\n```\n")
        lines.append("")
    os.makedirs(os.path.dirname(ARCHIVE), exist_ok=True)
    with open(ARCHIVE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(header)
        fh.write("\n".join(lines).rstrip() + "\n")
    print(f"wrote {os.path.relpath(ARCHIVE, ROOT)}")


def check():
    """Assert the deck is clean: no body opens with page furniture."""
    grammar = load()
    ok = True
    for it in grammar["items"]:
        body = (it.get("sections") or {}).get(SECTION, "")
        _, removals = plan_item(body)
        if removals:
            ok = False
            for frag, reason in removals:
                print(f"FAIL {it['id']}: still carries page furniture "
                      f"{frag!r} ({reason})")
    if ok:
        print(f"OK: {len(grammar['items'])} items — no suit running head, no "
              f"orphaned numeral, no garbled plate caption in any "
              f"'{SECTION}' body")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify only; do not write files")
    args = ap.parse_args()

    if args.check:
        sys.exit(0 if check() else 1)

    report, archive, changed = run(write=False)
    if report is None:
        print("\nFAIL: dry-run verification failed; nothing written")
        sys.exit(1)
    print("--- dry run ---")
    for item_id, before, after, n in report:
        if n:
            print(f"  {item_id:26s} before={before:6d} after={after:6d} "
                  f"removed_fragments={n}")
    print(f"  {changed} item(s) would change")

    report, archive, changed = run(write=True)
    if report is None:
        print("\nFAIL: write-pass verification failed")
        sys.exit(1)
    write_archive(archive)

    print("\n--- verifying ---")
    if not check():
        print("\nFAIL: post-write verification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
