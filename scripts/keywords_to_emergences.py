#!/usr/bin/env python3
"""Promote shared/structural keywords into emergence pill-nodes.

Generic, grammar-agnostic (the "flexible types" direction): it reads any
grammar's L1 base items, finds keywords shared by enough of them, and adds a
"By Keyword" faceting axis built from the SAME two-level pattern the meta uses:

    axis-keyword            (render_as: "pill-group")   level 3
      └─ kw-<slug>          (render_as: "pill")         level 2
           └─ composite_of: [base item ids with that keyword]

Selective by design (per the Jun 2026 decision): promote keywords that are
shared (count >= MIN) but NOT near-universal (count <= MAX_SHARE * N, so deck-name
tags like "golden dawn" are skipped). One-off descriptive keywords stay as plain
tags. Namespaced machine keys ("suit:coins", "arcana:the-fool") are skipped —
those drive the cross-deck meta axis, not per-deck human pills.

Idempotent: re-running removes prior kw-*/axis-keyword nodes first.

Usage:  python scripts/keywords_to_emergences.py <grammar.json> [MIN=3] [MAX_SHARE=0.7]
"""
import json, sys, re
from collections import defaultdict

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def promote(path, MIN=3, MAX_SHARE=0.7):
    d = json.load(open(path, encoding='utf-8'))
    items = d.get('items', [])
    # idempotent: drop prior artifacts
    items = [i for i in items if not (str(i.get('id', '')).startswith('kw-') or i.get('id') == 'axis-keyword')]
    base = [i for i in items if not i.get('composite_of')]   # L1 leaves only
    N = len(base)
    kwmap = defaultdict(list)
    for i in base:
        for k in (i.get('keywords') or []):
            if ':' in k:           # skip namespaced machine join-keys
                continue
            kwmap[k.strip()].append(i['id'])
    cap = max(MIN, int(MAX_SHARE * N))
    qualifying = {k: ids for k, ids in kwmap.items() if MIN <= len(ids) <= cap}
    imgof = {i['id']: (i.get('image_url') or (i.get('metadata') or {}).get('image_url')) for i in base}
    pills = []
    for k, ids in sorted(qualifying.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        rep = next((imgof[m] for m in ids if imgof.get(m)), None)   # representative thumbnail from a member
        pill = {
            'id': 'kw-' + slug(k),
            'name': k[:1].upper() + k[1:],
            'level': 2,
            'category': 'keyword-emergence',
            'render_as': 'pill',
            'composite_of': ids,
            'metadata': {'emergence_kind': 'keyword', 'keyword': k, 'member_count': len(ids)},
            'sections': {'Description': f'Cards in this deck sharing the keyword “{k}” ({len(ids)}).'},
        }
        if rep:
            pill['image_url'] = rep
        pills.append(pill)
    items.extend(pills)
    if pills:
        items.append({
            'id': 'axis-keyword',
            'name': 'By Keyword',
            'level': 3,
            'category': 'axis',
            'render_as': 'pill-group',
            'composite_of': [p['id'] for p in pills],
            'sections': {'Description': 'Cross-cutting facets derived from shared keywords — the same card appears under every keyword it carries.'},
        })
    d['items'] = items
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return N, cap, pills

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    path = sys.argv[1]
    MIN = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    MAX_SHARE = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7
    N, cap, pills = promote(path, MIN, MAX_SHARE)
    print(f'{path}: N base={N}, threshold {MIN}..{cap}, promoted {len(pills)} keyword-emergences')
    for p in pills:
        print(f"  {p['id']:24} {p['metadata']['member_count']:3}  {p['name']}")
