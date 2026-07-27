#!/usr/bin/env python3
"""
Brick 0 of GitHub-as-Database (see recursive-eco/docs/GITHUB_AS_DATABASE.md).

Stamp the canonical home-repo declaration onto every tarot grammar so each
grammar carries its own `_github_url` / `_github_source_url` (recursive-tarot
is the canonical home for tarot). Also records repo/branch/github_url at the
collection level.

Idempotent and byte-conservative: inserts the keys right after the opening
brace via targeted text insertion (no JSON round-trip), preserving CRLF,
indentation, key order, and the no-trailing-newline convention. Re-running
is a no-op once the keys are present.

Run from repo root:  python scripts/stamp_canonical_repo.py
"""
import glob
import os

OWNER = "PlayfulProcess"
REPO = "recursive-tarot"
BRANCH = "main"
FOLDER = "tarot"


def detect_eol(b: bytes) -> bytes:
    return b"\r\n" if b"\r\n" in b else b"\n"


def insert_after_open_brace(text: str, eol: str, keys_block: str) -> str:
    """Insert keys_block right after the first `{<eol>`."""
    anchor = "{" + eol
    idx = text.find(anchor)
    if idx != 0:
        # be strict: the file must start with `{<eol>`
        raise ValueError("file does not start with an opening brace + EOL")
    insert_at = idx + len(anchor)
    return text[:insert_at] + keys_block + text[insert_at:]


def stamp_grammar(path: str) -> str:
    slug = os.path.basename(os.path.dirname(path))
    raw = open(path, "rb").read()
    eol = detect_eol(raw).decode()
    text = raw.decode("utf-8")
    if '"_github_url"' in text:
        return f"skip (already stamped): {slug}"
    blob = f"https://github.com/{OWNER}/{REPO}/blob/{BRANCH}/{FOLDER}/{slug}/grammar.json"
    rawu = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{FOLDER}/{slug}/grammar.json"
    keys = (
        f'  "_github_url": "{blob}",{eol}'
        f'  "_github_source_url": "{rawu}",{eol}'
    )
    out = insert_after_open_brace(text, eol, keys)
    open(path, "wb").write(out.encode("utf-8"))
    return f"stamped: {slug}"


def stamp_collection(path: str) -> str:
    raw = open(path, "rb").read()
    eol = detect_eol(raw).decode()
    text = raw.decode("utf-8")
    if '"repo"' in text and '"github_url"' in text:
        return "skip (already stamped): _collection.json"
    gh = f"https://github.com/{OWNER}/{REPO}"
    keys = (
        f'  "repo": "{OWNER}/{REPO}",{eol}'
        f'  "branch": "{BRANCH}",{eol}'
        f'  "github_url": "{gh}",{eol}'
    )
    out = insert_after_open_brace(text, eol, keys)
    open(path, "wb").write(out.encode("utf-8"))
    return "stamped: _collection.json"


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(here)
    results = []
    for path in sorted(glob.glob(f"{FOLDER}/*/grammar.json")):
        results.append(stamp_grammar(path))
    coll = f"{FOLDER}/_collection.json"
    if os.path.exists(coll):
        results.append(stamp_collection(coll))
    for r in results:
        print(r)
    print(f"\n{len([r for r in results if r.startswith('stamped')])} file(s) stamped, "
          f"{len([r for r in results if r.startswith('skip')])} skipped.")


if __name__ == "__main__":
    main()
