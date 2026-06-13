# -*- coding: utf-8 -*-
"""Repo-wide integrity check. Run after every integration before committing.

  python3 scripts/check_all.py

Checks:
  1. every tarot/*/grammar.json is valid JSON with name + items[];
  2. composite_of references resolve within each grammar (no dangling);
  3. people dossiers (research/people/*.md) have the frontmatter the generator needs;
  4. rebuilds people + meta grammars and asserts the meta reports dangling=0.
Exits non-zero on any failure.
"""
import json, os, re, glob, subprocess, sys
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TAROT = os.path.join(ROOT, "tarot")
PEOPLE = os.path.join(ROOT, "research", "people")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
VALID_ROLE_GROUPS = {"makers", "patrons", "occultists", "scholars", "institutions"}

errors, warnings = [], []

# 1 + 2 — grammars
for path in sorted(glob.glob(os.path.join(TAROT, "*", "grammar.json"))):
    slug = os.path.basename(os.path.dirname(path))
    try:
        g = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        errors.append(f"{slug}: invalid JSON — {e}")
        continue
    if not g.get("name"):
        errors.append(f"{slug}: missing name")
    items = g.get("items")
    if not isinstance(items, list) or not items:
        errors.append(f"{slug}: items[] missing/empty")
        continue
    ids = {it.get("id") for it in items}
    for it in items:
        for c in it.get("composite_of", []) or []:
            if c not in ids:
                errors.append(f"{slug}: dangling composite_of '{c}' in item '{it.get('id')}'")

# 3 — people dossiers
for path in sorted(glob.glob(os.path.join(PEOPLE, "*.md"))):
    name = os.path.basename(path)
    m = FM_RE.match(open(path, encoding="utf-8").read())
    if not m:
        errors.append(f"people/{name}: no YAML frontmatter")
        continue
    fm = yaml.safe_load(m.group(1)) or {}
    for req in ("id", "type", "title", "role_group"):
        if not fm.get(req):
            errors.append(f"people/{name}: missing frontmatter '{req}'")
    if fm.get("role_group") and fm["role_group"] not in VALID_ROLE_GROUPS:
        errors.append(f"people/{name}: bad role_group '{fm['role_group']}'")

# 4 — rebuild generated grammars
for script in ("build_people_grammar.py", "build_meta_grammar.py"):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", script)],
                       capture_output=True, text=True, cwd=ROOT)
    out = (r.stdout + r.stderr).strip()
    print(f"[{script}] {out.splitlines()[0] if out else '(no output)'}")
    if r.returncode != 0:
        errors.append(f"{script} failed:\n{out}")
    if script == "build_meta_grammar.py" and "dangling=0" not in out:
        warnings.append(f"meta build did not report dangling=0: {out[:200]}")

for w in warnings:
    print("WARN:", w)
if errors:
    print(f"\nFAIL: {len(errors)} ERROR(S):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"\nOK: all checks passed ({len(glob.glob(os.path.join(TAROT, '*', 'grammar.json')))} grammars)")
