# -*- coding: utf-8 -*-
"""Reconstruct the Papus (`Le Tarot des Bohemiens`, 1889) sections across the
three occult decks that carry one: golden-dawn-book-t-tarot,
court-de-gebelin-tarot, oswald-wirth-tarot.

  python3 scripts/clean_papus_sections.py [--check]

Why a reconstruction, not a per-item trim: the original transcription pasted
book chapters by wherever they physically landed rather than by which card
they described. Several cards' Papus sections ran past their own entry into
scan garbage, running heads, and -- worst -- another card's entire chapter
(The Sun's held all of Judgement's; the Devil's held all of the Tower's),
while the card that chapter actually belonged to was left with no Papus
section, or one missing its own opening.

The book's own "Nth Hebrew letter (Letter)." headings occur exactly once per
card and OCR far more reliably than the Hebrew letter names beside them (a
digit survives a bad scan; "Resh" becomes "Eesh"). This script concatenates
every stored Papus body per deck in the TRUE BOOK ORDER of Le Tarot des
Bohemiens (which is not Golden Dawn's own item order -- Papus/Marseille
numbers Justice VIII and Strength XI in the opposite order from the Golden
Dawn), finds those 22 marker positions, and slices the corpus between
consecutive markers. That recovers a card's real text even when it is
currently trapped entirely inside a neighboring item, and it structurally
prevents any card's cleaned section from running into the next one, because
the slice never contains the next marker to begin with.

Each slice is then cleaned of:
  - the duplicated ALL-CAPS plate-caption preamble before its own marker
    (already excluded by construction -- slices start at the marker),
  - the AFFINITIES/SIGNIFICATIONS recap-table OCR word salad,
  - running heads and page numbers ("THE SYMBOLICAL TAROT. 109", "THE
    TAKOT."),
  - the book's own chapter-divider front matter ("Key to the 2nd Septenary
    -- The Zain and the Chariot -- ...", "CHAPTER XIII."), which introduces
    a *group* of upcoming cards, not any single one,
  - duplicated recap-title fragments ("The Devil,", "20. -i The Judgment."),
  while leaving Papus's own recurring "N. <sentence> --\\n\\nLabel." schema
  intact (real content, not table debris) and never touching coherent prose.

Everything removed is written to `research/sources/papus-trimmed-<deck>.md`
per deck, grouped per card, so nothing is silently lost.

Mapping note: Golden Dawn assigns Hebrew letters to the trumps on a
different scheme than Papus/Levi (starting Aleph at the Fool, not the
Magician) for every card except the World, where both traditions land on
Tau. Where a card's Papus letter conflicts with that card's own Book T
Correspondences, the Papus editorial header gets a one-line clarifier.
Court de Gebelin (1781) predates the Hebrew-letter attribution entirely and
Oswald Wirth's own Correspondences already follow Levi's scheme (the same
one Papus uses), so neither of those decks needs the clarifier.

Idempotent: re-running on already-cleaned files makes no further changes
(the markers are already correctly and uniquely placed, one per item).
"""
import argparse, io, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DECKS = ["golden-dawn-book-t-tarot", "court-de-gebelin-tarot", "oswald-wirth-tarot"]
SOURCES_DIR = os.path.join(ROOT, "research", "sources")

ARCHETYPE_POSITION = {
    "arcana:the-fool": 0, "arcana:the-magician": 1, "arcana:the-high-priestess": 2,
    "arcana:the-empress": 3, "arcana:the-emperor": 4, "arcana:the-hierophant": 5,
    "arcana:the-lovers": 6, "arcana:the-chariot": 7, "arcana:justice": 8,
    "arcana:the-hermit": 9, "arcana:wheel-of-fortune": 10, "arcana:strength": 11,
    "arcana:the-hanged-man": 12, "arcana:death": 13, "arcana:temperance": 14,
    "arcana:the-devil": 15, "arcana:the-tower": 16, "arcana:the-star": 17,
    "arcana:the-moon": 18, "arcana:the-sun": 19, "arcana:judgement": 20,
    "arcana:the-world": 21,
}
POSITION_NAME = {
    0: "Fool", 1: "Magician", 2: "High Priestess", 3: "Empress", 4: "Emperor",
    5: "Hierophant", 6: "Lovers", 7: "Chariot", 8: "Justice", 9: "Hermit",
    10: "Wheel of Fortune", 11: "Strength", 12: "Hanged Man", 13: "Death",
    14: "Temperance", 15: "Devil", 16: "Tower", 17: "Star", 18: "Moon",
    19: "Sun", 20: "Judgement", 21: "World",
}
ORDINAL_TO_POSITION = {i: i for i in range(1, 21)}
ORDINAL_TO_POSITION[21] = 0   # Fool carries the 21st Hebrew letter, Shin
ORDINAL_TO_POSITION[22] = 21  # World carries the 22nd Hebrew letter, Tau
POSITION_TO_ORDINAL = {v: k for k, v in ORDINAL_TO_POSITION.items()}

# Golden Dawn assigns Hebrew letters to the trumps on a different scheme
# than Papus/Levi (starting Aleph at the Fool, not the Magician); every
# position except 21 (World, Tau/Tau) conflicts with the Papus letter the
# reconstructed text uses. Only golden-dawn-book-t-tarot's own
# Correspondences section carries the competing Book T attribution: Court
# de Gebelin (1781) predates Hebrew-letter tarot correspondence entirely,
# and Oswald Wirth's own Correspondences already follow Levi's scheme --
# the same one Papus uses -- so neither of those decks gets the clarifier.
DECKS_WITH_MAPPING_CONFLICT = {"golden-dawn-book-t-tarot"}
POSITIONS_WITH_MAPPING_CONFLICT = set(range(22)) - {21}

BASE_HEADER = ("Papus (Gérard Encausse) — Le Tarot des Bohémiens, 1889 "
               "· French occult revival · later interpretation, not written "
               "for this deck")
MAPPING_SUFFIX = " · uses a different letter mapping than Book T"

HEADER_RE = re.compile(r"^\*Papus.*?\*|^\[Papus.*?\]", re.S)
MARKER_RE = re.compile(r"(\d{1,2})(?:st|nd|rd|th)\s+Hebrew letter\s*\(", re.I)

SEPTENARY_WORD = re.compile(r"SEPTEN\w{1,3}Y", re.I)
# BUG, kept for the record: {2,3} requires two-to-three letters between TA
# and OT, so this never matched TAROT (one letter, R) — nor the scan's TAKOT
# / TAEOT. Every "THE SYMBOLICAL TAROT. <page>" running head passed straight
# through this script and survived into papus-tarot-des-bohemiens, where
# scripts/clean_papus_running_heads.py finally removes them with {1,3}. This
# script no longer has any input (one_source_per_deck.py moved every Papus
# section out of the three host decks), so the pattern is left as it ran
# rather than silently changed; use {1,3} in anything new.
TAROT_WORD = r"TA[A-Z]{2,3}OT"
RUNNING_HEAD = re.compile(
    r"^(\d+\s+)?(THE " + TAROT_WORD + r"\.?|THE SYMBOLICAL " + TAROT_WORD + r"\.?|"
    r"(FIRST|SECOND|THIRD|FOURTH) " + SEPTENARY_WORD.pattern + r"\.?|"
    r"GENERAL TRANSITION\.?)( \d+)?$",
    re.I,
)
AFFIN_START = re.compile(r"^(AFFINITIES|SIGNIFICATIONS)$", re.I)
CHAPTER_DIVIDER_STRONG = re.compile(
    r"(CHAPTER\s+[IVXL]+\.?|ARCANA\s+\d+\s*(TO|—|-)\s*\d+|"
    r"Key\s+(to|of)\s+the\s+\S+\s+Septen\w+|"
    r"ARRANGEMENT OF THE FIGURES|CHARACTER OF THE FIGURES|"
    r"Summary of the \d|GENERAL SUMMARY OF THE)",
    re.I,
)
CHAPTER_MARKER = re.compile(
    r"(CHAPTER\s+[IVXL]+\.?|ARCANA\s+\d+\s+TO\s+\d+|GENERAL TRANSITION\.\s*ARCANA)",
    re.I,
)
TAIL_TABLE_MARKER = re.compile(r"^THE \S+ OF TRANSITION\.?$", re.I)
# A running head glued onto a single (uncollapsed) newline mid-sentence in
# the scan never becomes its own paragraph, so RUNNING_HEAD never sees it;
# catch it inline instead. Require the trailing page number so this never
# touches a genuine sentence like "...the first Septenary, taken as a
# whole..." (which has no digit after it).
INLINE_RUNNING_HEAD = re.compile(
    r"(?:([A-Za-z])-\s+)?"
    r"((FIRST|SECOND|THIRD|FOURTH) " + SEPTENARY_WORD.pattern + r"\.|"
    r"GENERAL TRANSITION\.|THE SYMBOLICAL " + TAROT_WORD + r"\.)\s+\d+\s+",
    re.I,
)


def _inline_running_head_sub(m):
    # a captured trailing hyphen means the page break split a single word
    # ("battle-[running head]ments" -> "battlements"); rejoin it with no
    # space, otherwise just drop the running head.
    return m.group(1) if m.group(1) else ""


def strip_inline_running_heads(text):
    text = INLINE_RUNNING_HEAD.sub(_inline_running_head_sub, text)
    return re.sub(r"[ \t]{2,}", " ", text)


RUNNING_HEAD_PREFIX = re.compile(
    r"^(?:(?:FIRST|SECOND|THIRD|FOURTH) " + SEPTENARY_WORD.pattern + r"\.|"
    r"GENERAL TRANSITION\.|THE SYMBOLICAL " + TAROT_WORD + r"\.)\s+\d+\s+(\S.*)$",
    re.I,
)


def merge_hyphen_across_running_head(paras):
    """A running head can land on its own real paragraph right at a
    word-break hyphen ("battle-" | "THIRD SEPTENARY. 169 ments struck...").
    Splice the two back into one word once the running head is dropped."""
    out = []
    i = 0
    while i < len(paras):
        cur = paras[i]
        if (i + 1 < len(paras) and re.search(r"[A-Za-z]-$", cur.rstrip())):
            m = RUNNING_HEAD_PREFIX.match(paras[i + 1].strip())
            if m and m.group(1)[:1].islower():
                cur = cur.rstrip()[:-1] + m.group(1)
                i += 1
        out.append(cur)
        i += 1
    return out


def dehyphenate(text):
    return re.sub(r"([A-Za-z])-\n([a-z])", r"\1\2", text)


def normalize_breaks(text):
    text = dehyphenate(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def is_sentence(p):
    p = p.strip()
    if len(p) < 60 or len(p.split()) < 10:
        return False
    if not re.search(r"[a-z]", p):
        return False
    if not p.rstrip().endswith((".", "?", "!", '."', ".'")):
        return False
    return True


def is_short_fragment(p):
    p = p.strip()
    if not p or len(p) > 45:
        return False
    return not is_sentence(p)


def is_paired_label(lst):
    """True if lst[-1] is the short *label* half of Papus's own recurring
    'N. <sentence> --\\n\\n<Label>.' schema -- real content, distinguished
    from a bare duplicated recap title by a numbered/em-dash-terminated
    sentence immediately before it."""
    if len(lst) < 2:
        return False
    prev = lst[-2].strip()
    return bool(re.match(r"^\d+\.\s", prev)) or prev.endswith(("—", "-"))


def merge_false_paragraph_breaks(paras):
    """Rejoin the handful of spots where the scan has a spurious blank line
    mid-sentence (a column/line-break artifact): the piece before doesn't
    end in sentence-final punctuation and the next piece opens lowercase."""
    out = []
    i = 0
    while i < len(paras):
        cur = paras[i]
        while (i + 1 < len(paras)
               and not cur.rstrip().endswith((".", "?", "!", '"', "'", ":", ";", ")"))
               and paras[i + 1][:1].islower()):
            i += 1
            cur = cur.rstrip() + " " + paras[i].lstrip()
        out.append(cur)
        i += 1
    return out


def tag_reason(p):
    ps = p.strip()
    if RUNNING_HEAD.match(ps):
        return "scan garbage: page running head / page number"
    if AFFIN_START.match(ps) or any(
        k in ps for k in ("Hieroglyphic", "Kabbalah", "Astronomy", "Primitive",
                           "OBSERVATIONS", "SIGNIFICATIONS", "AFFINITIES")
    ):
        return "scan garbage: OCR word-salad from the AFFINITIES/SIGNIFICATIONS table"
    if (CHAPTER_DIVIDER_STRONG.search(ps) or CHAPTER_MARKER.search(ps)
            or TAIL_TABLE_MARKER.match(ps)):
        return ("overflow: the book's own chapter-divider front matter (introduces "
                "the next group of cards, not this card's own entry)")
    return "scan garbage: duplicated plate-caption / recap-title fragment"


def clean_span(paras):
    """paras[0] is this card's own 'Nth Hebrew letter (...)' marker; the
    span already stops at the next card's marker by construction (see
    build_deck), so no leading- or next-card-bleed cut is needed here --
    only the debris inside the card's own span."""
    paras = merge_false_paragraph_breaks(paras)
    paras = merge_hyphen_across_running_head(paras)
    cut = []

    trunc_idx = None
    for i in range(1, len(paras)):
        ps = paras[i].strip()
        if CHAPTER_MARKER.search(ps) or TAIL_TABLE_MARKER.match(ps):
            trunc_idx = i
            break
    if trunc_idx is not None:
        cut.extend(paras[trunc_idx:])
        paras = paras[:trunc_idx]

    affin_idx = None
    for i, p in enumerate(paras):
        if AFFIN_START.match(p.strip()):
            affin_idx = i
            break
        if i > 0 and CHAPTER_DIVIDER_STRONG.search(p) and SEPTENARY_WORD.search(p):
            affin_idx = i
            break

    if affin_idx is not None:
        kept = list(paras[:affin_idx])
        while kept and is_short_fragment(kept[-1]) and not is_paired_label(kept):
            cut.append(kept.pop())
        past_marker = False
        for p in paras[affin_idx:]:
            ps = p.strip()
            if past_marker:
                cut.append(p)
                continue
            if CHAPTER_MARKER.search(ps):
                past_marker = True
                cut.append(p)
                continue
            if RUNNING_HEAD.match(ps):
                cut.append(p)
            elif is_sentence(ps) and not CHAPTER_DIVIDER_STRONG.search(ps):
                kept.append(p)
            else:
                cut.append(p)
    else:
        kept = list(paras)

    final = []
    for p in kept:
        if RUNNING_HEAD.match(p.strip()):
            cut.append(p)
        else:
            final.append(strip_inline_running_heads(p))
    while final and is_short_fragment(final[-1]) and not is_paired_label(final):
        cut.append(final.pop())

    return final, cut


def position_of(item):
    arch = (item.get("metadata", {}) or {}).get("archetype")
    return ARCHETYPE_POSITION.get(arch)


def load_deck(deck):
    path = os.path.join(ROOT, "tarot", deck, "grammar.json")
    with open(path, encoding="utf-8") as fh:
        grammar = json.load(fh)
    return path, grammar


def build_spans(grammar):
    """Returns (by_pos, spans) -- by_pos maps card position -> list of
    (item_id, item) present for that card in this deck; spans maps position
    -> the cleaned corpus slice (list of raw paragraphs, pre-normalize-break
    applied per source item but not yet merged/cleaned -- clean_span does
    that)."""
    by_pos = {}
    for it in grammar["items"]:
        pos = position_of(it)
        if pos is None:
            continue
        by_pos.setdefault(pos, []).append(it)

    order_positions = sorted(by_pos.keys())
    blob_paras = []
    for pos in order_positions:
        for it in by_pos[pos]:
            secs = it.get("sections", {})
            if not isinstance(secs, dict) or "Papus" not in secs:
                continue
            raw = secs["Papus"]
            m = HEADER_RE.match(raw)
            header = m.group(0) if m else ""
            body = raw[len(header):].lstrip("\n") if header else raw
            body = normalize_breaks(body)
            blob_paras.extend([p for p in body.split("\n\n") if p.strip()])

    marker_idx = {}
    for i, p in enumerate(blob_paras):
        m = MARKER_RE.search(p)
        if m:
            marker_idx.setdefault(int(m.group(1)), []).append(i)

    found = []
    dupes = {}
    for ordinal, idxs in marker_idx.items():
        if ordinal not in ORDINAL_TO_POSITION:
            continue
        if len(idxs) > 1:
            dupes[ordinal] = idxs
        found.append((idxs[0], ordinal))
    found.sort()

    spans = {}
    for k, (idx, ordinal) in enumerate(found):
        end = found[k + 1][0] if k + 1 < len(found) else len(blob_paras)
        spans[ORDINAL_TO_POSITION[ordinal]] = blob_paras[idx:end]

    missing = [pos for pos in range(22) if pos not in spans]
    return by_pos, spans, missing, dupes


def header_for(deck, pos):
    if deck in DECKS_WITH_MAPPING_CONFLICT and pos in POSITIONS_WITH_MAPPING_CONFLICT:
        return "*" + BASE_HEADER + MAPPING_SUFFIX + "*"
    return "*" + BASE_HEADER + "*"


def insert_papus_key(sections, new_text):
    """Insert a brand-new 'Papus' key in the same relative slot siblings
    use: right before 'Research note' if present, else right before
    'Wirth' if present (oswald-wirth-tarot), else appended at the end."""
    keys = list(sections.keys())
    if "Research note" in keys:
        idx = keys.index("Research note")
    elif "Wirth" in keys:
        idx = keys.index("Wirth")
    else:
        idx = len(keys)
    new_items = list(sections.items())
    new_items.insert(idx, ("Papus", new_text))
    return dict(new_items)


def process_deck(deck, write, archive_lines):
    path, grammar = load_deck(deck)
    by_pos, spans, missing, dupes = build_spans(grammar)
    if missing:
        print(f"FAIL {deck}: no Papus marker found anywhere for "
              f"{[POSITION_NAME[p] for p in missing]}")
        return None
    if dupes:
        print(f"WARN {deck}: duplicate markers for ordinals {sorted(dupes)} "
              f"(used the first occurrence)")

    report = []
    changed = 0
    for pos in range(22):
        items = by_pos.get(pos, [])
        if not items:
            continue
        item = items[0]
        kept, cut = clean_span(spans[pos])
        body = "\n\n".join(kept).strip()
        new_text = header_for(deck, pos) + "\n\n" + body

        old_text = (item.get("sections", {}) or {}).get("Papus")
        before_len = len(old_text) if old_text else 0
        after_len = len(new_text)
        report.append((deck, pos, POSITION_NAME[pos], item["id"], before_len,
                        after_len, len(cut)))

        if old_text != new_text:
            changed += 1
        if write:
            sections = item.setdefault("sections", {})
            if "Papus" in sections:
                sections["Papus"] = new_text
            else:
                item["sections"] = insert_papus_key(sections, new_text)

        if cut:
            archive_lines.append(
                f"## `{item['id']}` ({POSITION_NAME[pos]}) — removed from `sections.Papus`\n"
            )
            for c in cut:
                archive_lines.append(f"**{tag_reason(c)}**\n")
                archive_lines.append(c.strip() + "\n")
            archive_lines.append("")

    if write and changed:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(grammar, ensure_ascii=False, indent=2))
        print(f"wrote {os.path.relpath(path, ROOT)} ({changed} card(s) changed)")
    elif write:
        print(f"{deck}: no changes (idempotent)")

    return report


def write_archive(deck, archive_lines):
    if not archive_lines:
        return
    out_path = os.path.join(SOURCES_DIR, f"papus-trimmed-{deck}.md")
    header = f"""# Papus (Gérard Encausse) — *Le Tarot des Bohémiens* (1889), OCR-cleanup overflow — {deck}

Public domain. This is the material **removed while cleaning the `Papus` sections** in
`tarot/{deck}/grammar.json`. The original transcription pasted book chapters wherever
they physically landed rather than by which card they described: several cards' Papus
sections ran past their own entry into scan garbage, running heads, and — worst —
another card's entire chapter (The Sun's held all of Judgement's; the Devil's held all
of the Tower's, whose own item then opened directly onto the Star's).

This pass reconstructed the true per-card boundaries from the book's own "Nth Hebrew
letter (Letter)." headings, which occur exactly once per card and survive OCR far more
reliably than the Hebrew letter names beside them (a digit survives a bad scan; "Resh"
becomes "Eesh"). Every card's real, complete text now lives in its own item — including
Judgement's and the Tower's, both fully recovered from where they had been trapped — so
nothing below is lost, only removed: OCR table debris from the AFFINITIES/SIGNIFICATIONS
recap tables, duplicated plate captions and running heads, and the book's own
chapter-divider front matter (which introduces a *group* of upcoming cards, not any one
of them).

Generated by `scripts/clean_papus_sections.py`.

---

"""
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(header)
        fh.write("\n".join(archive_lines).rstrip() + "\n")
    print(f"wrote {os.path.relpath(out_path, ROOT)}")


def check_deck(deck):
    """Assert every remaining Papus section: (a) opens with its own card's
    marker and mentions no other card's marker; (b) report char counts."""
    path, grammar = load_deck(deck)
    ok = True
    for it in grammar["items"]:
        pos = position_of(it)
        if pos is None:
            continue
        secs = it.get("sections", {})
        if not isinstance(secs, dict) or "Papus" not in secs:
            print(f"FAIL {deck}/{it['id']}: no Papus section")
            ok = False
            continue
        raw = secs["Papus"]
        m = HEADER_RE.match(raw)
        body = raw[len(m.group(0)):].lstrip("\n") if m else raw
        markers = [int(mm.group(1)) for mm in MARKER_RE.finditer(body)]
        expected = POSITION_TO_ORDINAL[pos]
        if markers.count(expected) != 1:
            print(f"FAIL {deck}/{it['id']}: expected exactly one marker for ordinal "
                  f"{expected} ({POSITION_NAME[pos]}), found {markers.count(expected)}")
            ok = False
        others = [o for o in markers if o != expected]
        if others:
            print(f"FAIL {deck}/{it['id']}: mentions other card marker(s) {others} "
                  f"-- {[POSITION_NAME[ORDINAL_TO_POSITION[o]] for o in others if o in ORDINAL_TO_POSITION]}")
            ok = False
        print(f"  {deck}/{it['id']} ({POSITION_NAME[pos]}): {len(raw)} chars")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                     help="verify only; do not write files")
    args = ap.parse_args()

    if args.check:
        ok = True
        for deck in DECKS:
            print(f"--- {deck} ---")
            if not check_deck(deck):
                ok = False
        if not ok:
            print("\nFAIL: verification failed")
            sys.exit(1)
        print("\nOK: every Papus section is self-scoped (own marker once, no other "
              "card's marker)")
        return

    print("--- before/after (dry run computed, not yet written) ---")
    all_reports = []
    for deck in DECKS:
        report = process_deck(deck, write=False, archive_lines=[])
        if report is None:
            sys.exit(1)
        all_reports.append((deck, report))
    for deck, report in all_reports:
        print(f"\n{deck}")
        removed_total = 0
        for _, pos, name, item_id, before, after, ncut in report:
            delta = before - after
            removed_total += max(delta, 0)
            print(f"  {item_id:32s} {name:16s} before={before:5d} after={after:5d} "
                  f"removed={delta:6d} cut_fragments={ncut}")
        print(f"  TOTAL removed: {removed_total} chars")

    print("\n--- writing ---")
    os.makedirs(SOURCES_DIR, exist_ok=True)
    for deck in DECKS:
        archive_lines = []
        process_deck(deck, write=True, archive_lines=archive_lines)
        write_archive(deck, archive_lines)

    print("\n--- verifying ---")
    ok = True
    for deck in DECKS:
        if not check_deck(deck):
            ok = False
    if not ok:
        print("\nFAIL: post-write verification failed")
        sys.exit(1)
    print("\nOK")


if __name__ == "__main__":
    main()
