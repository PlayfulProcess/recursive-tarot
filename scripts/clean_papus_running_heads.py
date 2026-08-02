# -*- coding: utf-8 -*-
"""Strip the surviving page furniture from `papus-tarot-des-bohemiens`.

  python3 scripts/clean_papus_running_heads.py [--check]

`scripts/clean_papus_sections.py` reconstructed the per-card boundaries of
Papus's *Le Tarot des Bohémiens* (1889) back when its text sat as a third
voice inside three other decks, and `scripts/one_source_per_deck.py` then
moved that text into this deck of its own. One class of debris survived both
passes because of a regex bug: the earlier script's running-head pattern was
`TA[A-Z]{2,3}OT`, which requires **two to three** letters between `TA` and
`OT` — so it never matched `TAROT` (one letter: `R`), nor the scan's `TAKOT`
/ `TAEOT`. Every `THE SYMBOLICAL TAROT. <page>` and `<page> THE TAROT.`
running head therefore passed straight through. This script removes them.

What it removes, and why:

  * **Page running heads** — `THE SYMBOLICAL TAROT. 107`, `108 THE TAKOT.`,
    `144 THE TAEOT.`: the header line printed at the top of every page of the
    1896 Morton translation. Six sit as their own paragraph; three are glued
    to the front of the sentence they interrupted (`THE SYMBOLICAL TAROT. 109
    at least easy to us to follow it...`). Where a running head split a
    sentence, the two halves are rejoined.
  * **Plate captions** — `arcanum-07-le-chariot` carries the caption of the
    Chariot plate twice with the scanner's reading of the lettering *inside*
    the picture between them (`TXTH ARI 0 T JT`). The card's real heading
    pair (`SEVENTH CARD OF THE TAROT.` / `The Chariot.`) follows and stays.
  * **Diagram debris** — `arcanum-21-le-monde` ends its recapitulation with
    two lines the scanner read off the summary figure (`7 ' oci`,
    `(j HUrf-xNl 1`).
  * **Stray box glyphs** (`■`) left at a paragraph edge by the scan.
  * The duplicated recap-title fragment `20. -i ` in front of
    `arcanum-20-le-jugement`'s opening `20th Hebrew letter (Eesh).` — every
    sibling opens with the bare marker.

What it deliberately KEEPS — the judgment call this pass exists to record:

  * `ORIGIN OF THE SYMBOLISM OF THE <ORDINAL> CARD OF THE TAROT.` (22 items)
    and `<THE> <ORDINAL> CARD OF THE TAROT.` + the card-name line (22 items)
    are **not** page furniture. They are the two section headings Papus gives
    every arcanum's own entry, and in every one of the 22 items they already
    stand as their own paragraph — a proper section break, not a heading
    buried in flowing prose. Nothing to convert; they stay.
  * `EXTENSION OF THE THREE GREAT PRINCIPLES THROUGH` and
    `GENERAL RECAPITULATION.` in `arcanum-01-le-bateleur` are likewise the
    book's own subsection headings *inside the First Card's chapter* — Papus
    lays out the whole system there — and the prose under each is his real
    text for that chapter. Removing the headings would orphan that prose, so
    they stay. (Both are OCR-truncated; see the report note.)
  * Ten `ORIGIN ...` headings lose their final `THE TAROT.` to a scan line
    break (`...THIRTEENTH CARD OF`). They are **not** completed here:
    reconstructing words into a quoted source text is fabrication, however
    mechanically the sibling pattern predicts them.

Everything removed is written verbatim, with a reason and grouped per card,
to `research/sources/papus-trimmed-papus-tarot-des-bohemiens.md`.

Nothing-lost proof, per item: deleting exactly the archived fragments from
the original body and discarding all non-alphanumeric characters must
reproduce the new body's alphanumerics exactly — as an ordered sequence for
every item, and as a character multiset for the one item whose footnote and
body sentence swap places (`arcanum-01-le-bateleur`, see below).

Idempotent: re-running on already-cleaned content removes nothing.
"""
import argparse, collections, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DECK = "papus-tarot-des-bohemiens"
SECTION = "Le Tarot des Bohémiens"
GRAMMAR = os.path.join(ROOT, "tarot", DECK, "grammar.json")
ARCHIVE = os.path.join(ROOT, "research", "sources", f"papus-trimmed-{DECK}.md")

# TAROT is TA + one letter + OT. The earlier pass wrote {2,3} here and so
# matched nothing; {1,3} covers TAROT / TAKOT / TAEOT / TABOT.
TAROT_WORD = r"TA[A-Z]{1,3}OT"
RUNNING_HEAD_STANDALONE = re.compile(
    r"^(?:\d+\s+)?THE (?:SYMBOLICAL )?" + TAROT_WORD + r"\.?(?:\s+\d+)?$")
# Only strips when a lowercase word follows the page number — proof that the
# head landed inside a sentence rather than at a real paragraph start.
RUNNING_HEAD_INLINE = re.compile(
    r"^THE (?:SYMBOLICAL )?" + TAROT_WORD + r"\.\s+\d+\s+(?=[a-z])")
FOOTNOTE = re.compile(r"^\d+\s+\S")
BOX_GLYPH_LEAD = re.compile(r"^■\s*")
BOX_GLYPH_TAIL = re.compile(r"\s*■$")
RECAP_PREFIX = re.compile(r"^20\.\s+-i\s+(?=20th Hebrew letter)")

REASON_RH = ("page furniture: the running head printed at the top of every "
             "page of the translation, plus its page number")
REASON_RH_INLINE = ("page furniture: the same running head, glued to the "
                    "front of the sentence the page break interrupted "
                    "(the two halves are rejoined)")
REASON_BOX = "scan garbage: a stray box glyph left at the paragraph edge"
REASON_RECAP = ("scan garbage: a duplicated recap-title fragment in front of "
                "the card's own opening marker (every sibling opens with the "
                "bare marker)")

# Exact paragraphs, per item, that are picture furniture rather than text.
# An allow-list, never a heuristic.
PICTURE_FURNITURE = {
    "arcanum-07-le-chariot": [
        ("THE CHARIOT.",
         "picture furniture: the plate's printed caption, repeated above and "
         "below the illustration (the card's own heading pair, 'SEVENTH CARD "
         "OF THE TAROT.' / 'The Chariot.', follows and is kept)"),
        ("TXTH ARI 0 T JT",
         "scan garbage: the scanner's reading of the lettering inside the "
         "Chariot plate"),
        ("THE CHARIOT.",
         "picture furniture: the plate's printed caption, repeated above and "
         "below the illustration (the card's own heading pair, 'SEVENTH CARD "
         "OF THE TAROT.' / 'The Chariot.', follows and is kept)"),
    ],
    "arcanum-21-le-monde": [
        ("7 ' oci",
         "scan garbage: read off the summary figure that closes the "
         "recapitulation, not prose"),
        ("(j HUrf-xNl 1",
         "scan garbage: read off the summary figure that closes the "
         "recapitulation, not prose"),
    ],
}


def alnum(s):
    return re.sub(r"[^0-9A-Za-z]", "", s)


def can_merge(prev, nxt):
    """The page break split a sentence: the half before it does not end on
    sentence-final punctuation and the half after it opens lowercase."""
    return bool(nxt[:1].islower()) and not prev.rstrip().endswith((".", "?", "!"))


def plan_item(item_id, body):
    """Return (new_body, removals, hopped) — pure, no mutation. `hopped` is
    True when a rejoin had to reach back over an intervening footnote
    paragraph, which reorders that footnote after the mended sentence."""
    paras = body.split("\n\n")
    furniture = collections.deque(PICTURE_FURNITURE.get(item_id, []))
    out, removals = [], []
    pending_merge = False
    hopped = False

    for p in paras:
        ps = p.strip()

        if furniture and ps == furniture[0][0]:
            frag, reason = furniture.popleft()
            removals.append((p, reason))
            continue

        if RUNNING_HEAD_STANDALONE.match(ps):
            removals.append((p, REASON_RH))
            pending_merge = True
            continue

        m = RUNNING_HEAD_INLINE.match(p)
        if m:
            removals.append((m.group(0).rstrip(), REASON_RH_INLINE))
            p = p[m.end():]
            pending_merge = True

        m = BOX_GLYPH_LEAD.match(p)
        if m:
            removals.append(("■", REASON_BOX))
            p = p[m.end():]
        m = BOX_GLYPH_TAIL.search(p)
        if m:
            removals.append(("■", REASON_BOX))
            p = p[:m.start()]

        m = RECAP_PREFIX.match(p)
        if m:
            removals.append((m.group(0).rstrip(), REASON_RECAP))
            p = p[m.end():]

        if pending_merge and out:
            # The page's footnote block can land between the two halves of the
            # broken sentence. Test that first — a footnote often ends without
            # sentence-final punctuation (it closes on a verse or a citation),
            # so it would otherwise swallow the body text that follows it.
            if (len(out) >= 2 and FOOTNOTE.match(out[-1].strip())
                    and can_merge(out[-2], p)):
                out[-2] = out[-2].rstrip() + " " + p.lstrip()
                hopped = True
                pending_merge = False
                continue
            if can_merge(out[-1], p):
                out[-1] = out[-1].rstrip() + " " + p.lstrip()
                pending_merge = False
                continue
        pending_merge = False
        out.append(p)

    return "\n\n".join(out), removals, hopped


def verify_item(item_id, before, after, removals, hopped):
    probe = before
    ok = True
    for frag, _ in removals:
        if frag not in probe:
            print(f"FAIL {item_id}: archived fragment not found verbatim in "
                  f"the original body: {frag!r}")
            ok = False
            continue
        probe = probe.replace(frag, "", 1)
    if hopped:
        if collections.Counter(alnum(probe)) != collections.Counter(alnum(after)):
            print(f"FAIL {item_id}: character multiset changed")
            ok = False
    else:
        if alnum(probe) != alnum(after):
            print(f"FAIL {item_id}: alphanumeric sequence changed")
            ok = False
    return ok


def load():
    with open(GRAMMAR, encoding="utf-8") as fh:
        return json.load(fh)


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
        after, removals, hopped = plan_item(it["id"], before)
        if not verify_item(it["id"], before, after, removals, hopped):
            ok = False
        if removals:
            changed += 1
            archive.append((it["id"], it["name"], removals, hopped))
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
    header = f"""# Papus (Gérard Encausse) — *Le Tarot des Bohémiens* (1889), page furniture removed — {DECK}

Public domain. This is the material **removed from the `{SECTION}` sections** in
`tarot/{DECK}/grammar.json` — none of it is Papus's text.

An earlier pass (`scripts/clean_papus_sections.py`) was meant to catch the running heads
and missed them all: its pattern was `TA[A-Z]{{2,3}}OT`, which requires two to three
letters between `TA` and `OT` and so never matched `TAROT` — one letter, `R` — nor the
scan's `TAKOT` / `TAEOT`. Every `THE SYMBOLICAL TAROT. <page>` line therefore survived
into this deck. That is what is removed here, together with the Chariot plate's caption
and lettering, the diagram debris closing the World's recapitulation, two stray box
glyphs, and one duplicated recap-title fragment.

**Kept, deliberately.** `ORIGIN OF THE SYMBOLISM OF THE <ORDINAL> CARD OF THE TAROT.` and
`<ORDINAL> CARD OF THE TAROT.` + the card-name line are Papus's own two section headings
for each arcanum's entry, and in all 22 items they already stand as their own paragraph —
a genuine section break, not a heading buried mid-paragraph. `EXTENSION OF THE THREE
GREAT PRINCIPLES THROUGH` and `GENERAL RECAPITULATION.` in `arcanum-01-le-bateleur` are
the book's own subsection headings inside the First Card's chapter, and the prose beneath
each is Papus's real text for that chapter; removing them would orphan it. Ten `ORIGIN`
headings lose their closing `THE TAROT.` to a scan line break and are **not** completed —
writing words into a quoted source is fabrication however strongly the sibling pattern
predicts them.

Generated by `scripts/clean_papus_running_heads.py` (idempotent; `--check` verifies
without writing).

---

"""
    lines = []
    for item_id, name, removals, hopped in archive:
        lines.append(f"## `{item_id}` ({name}) — removed from `sections.{SECTION}`\n")
        if hopped:
            lines.append(
                "> Rejoin note: the page's footnote block sat between the two halves of "
                "the sentence this running head interrupted. The sentence is mended and "
                "the footnote paragraph now follows it.\n")
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
    grammar = load()
    ok = True
    heading_ok = 0
    for it in grammar["items"]:
        body = (it.get("sections") or {}).get(SECTION, "")
        _, removals, _ = plan_item(it["id"], body)
        for frag, reason in removals:
            ok = False
            print(f"FAIL {it['id']}: still carries {frag!r} ({reason})")
        # The kept headings must remain their own paragraph, never glued into
        # flowing prose. A paragraph that mentions one of the two heading
        # forms must BE that heading — i.e. be short and set in capitals.
        for p in body.split("\n\n"):
            ps = p.strip()
            if not re.search(r"ORIGIN[0-9]? O[FP] THE SYMBOLISM|"
                             r"CARD OF THE TAROT", ps):
                continue
            letters = [c for c in ps if c.isalpha()]
            caps = sum(1 for c in letters if c.isupper()) / max(1, len(letters))
            if caps >= 0.9 and len(ps) <= 90:
                heading_ok += 1
            else:
                ok = False
                print(f"FAIL {it['id']}: a section heading is buried "
                      f"mid-paragraph: {ps[:120]!r}")
    if ok:
        print(f"OK: {len(grammar['items'])} items — no running head, plate "
              f"caption, diagram debris or box glyph left; {heading_ok} "
              f"section headings all stand as their own paragraph")
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
