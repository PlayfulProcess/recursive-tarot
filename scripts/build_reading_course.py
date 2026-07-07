#!/usr/bin/env python3
"""Build the single collapsed course `course/reading-the-cards.mdx` from the 12
Book-II chapters (the individual essays stay the source of truth).

Each chapter's `# Title` is demoted to `## Title` (a collapsible H2 section in the
course-viewer outline) and its internal `## sections` become `### children`. Run
after editing any Intention/voice essay:  python scripts/build_reading_course.py
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "course" / "books" / "how-to-read-the-cards" / "book.json"
COURSE = ROOT / "course"
OUT = COURSE / "reading-the-cards.mdx"

def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text

def demote_headings(text):
    # add one '#' to every ATX heading line so # -> ##, ## -> ###, etc.
    return re.sub(r"^(#{1,5}) ", r"#\1 ", text, flags=re.MULTILINE)

def main():
    book = json.loads(BOOK.read_text(encoding="utf-8"))
    chapters = []
    for part in book.get("parts", []):
        for ch in part.get("chapters", []):
            if ch.get("status") == "to-write":
                continue
            chapters.append(ch)

    header = (
        "---\n"
        "id: reading-the-cards\n"
        'title: "Reading the Cards"\n'
        'description: "The whole practitioner course in one place — why a reading can '
        "genuinely help, how to set an intention, the lenses to read through, a ritual to "
        "walk, and the long human history of casting lots. Use the collapsible outline to "
        'jump between chapters."\n'
        "author: PlayfulProcess\n"
        "date: 2026-06-22\n"
        "---\n\n"
        "# Reading the Cards\n\n"
        "> *Read to know yourself, not to be told your fate. A card starts a conversation "
        "with what is already alive in you. Relate to the card; never obey it.*\n\n"
        "This is the full course in one place — twelve chapters, from *why a reading can "
        "help* through the lenses, a ritual, and the long human history of divination. "
        "Open the outline on the left and jump to any chapter; each expands to its own "
        "sections. Read it straight through, or wander.\n"
    )

    parts_out = [header]
    n = 0
    for ch in chapters:
        src = COURSE / ch["src"]
        if not src.exists():
            print(f"  ! missing {src}", file=sys.stderr); continue
        body = demote_headings(strip_frontmatter(src.read_text(encoding="utf-8"))).rstrip()
        parts_out.append("\n\n---\n\n" + body + "\n")
        n += 1

    OUT.write_text("\n".join(parts_out) + "\n", encoding="utf-8")
    print(f"[build_reading_course] {n} chapters -> {OUT.relative_to(ROOT)} ({OUT.stat().st_size//1024} KB)")

if __name__ == "__main__":
    main()
