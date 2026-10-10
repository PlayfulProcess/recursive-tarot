# -*- coding: utf-8 -*-
"""Ask Wikimedia Commons what each card image is, and write the answer down.

  python scripts/audit_image_rights.py            # query Commons, write docs/rights/
  python scripts/audit_image_rights.py --offline  # rebuild the summary from the saved ledger

For every `record` deck (and the `living` decks, for completeness) this maps each card's
image to its upstream file and records, per card, what the upstream says about it:

  * `metadata.image_source` or `metadata.illustrations[].url` when it points at Commons;
  * otherwise the image's own file name, tried as a Commons file title (most decks on R2
    were mirrored from Commons under the same name);
  * otherwise the card is `unrecorded`: nothing in the repo says where the image came from.

For a Commons file it keeps the licence (`LicenseShortName`), the `Credit` line and the
`Artist`, and flags a scan whose credit points at the BnF / Gallica, because Gallica's
conditions of use allow free reuse only when it is not commercial.

It writes:
  * `docs/rights/image-ledger.json` — one row per card image (the evidence);
  * `docs/rights/IMAGE-LEDGER.md` — one row per deck (the summary).

It changes no grammar. It reads Commons' answer as data: a "Public domain" tag on Commons is
the uploader's claim about the work, not a grant from the institution that made the scan.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'docs', 'rights')
LEDGER = os.path.join(OUT_DIR, 'image-ledger.json')
SUMMARY = os.path.join(OUT_DIR, 'IMAGE-LEDGER.md')
API = 'https://commons.wikimedia.org/w/api.php'
UA = 'recursive-tarot-rights-audit/1.0 (https://github.com/PlayfulProcess/recursive-tarot)'


def commons_title(url):
    """Return a Commons file title for a Commons URL, or None."""
    if not url or 'wikimedia.org' not in url:
        return None
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    m = re.search(r'(?:Special:FilePath/|/wiki/File:)(.+)$', path)
    if m:
        return m.group(1).replace('_', ' ')
    if '/commons/' in path and 'upload.wikimedia.org' in url:
        name = path.rsplit('/', 1)[-1]
        if '/thumb/' in path:  # .../thumb/a/ab/Name.jpg/700px-Name.jpg
            name = path.split('/thumb/', 1)[1].split('/')[2]
        return name.replace('_', ' ')
    return None


def candidates(item):
    md = item.get('metadata') or {}
    out = []
    src = md.get('image_source')
    if isinstance(src, str) and commons_title(src):
        out.append(('image_source', commons_title(src)))
    for il in md.get('illustrations') or []:
        if il.get('is_primary') is False:
            continue
        t = commons_title(il.get('url'))
        if t:
            out.append(('illustrations', t))
            break
    u = item.get('image_url') or ''
    if u:
        base = urllib.parse.unquote(u.split('?', 1)[0].rsplit('/', 1)[-1])
        if not re.match(r'^\d{10,}-', base) and not re.match(r'^[ct]\d\d\.jpg$', base):
            out.append(('file_name', base.replace('_', ' ')))
    return out


def query(titles):
    found = {}
    titles = sorted(set(titles))
    for k in range(0, len(titles), 50):
        chunk = titles[k:k + 50]
        q = {'action': 'query', 'format': 'json', 'prop': 'imageinfo', 'iiprop': 'extmetadata',
             'iiextmetadatafilter': 'LicenseShortName|Credit|Artist|UsageTerms',
             'titles': '|'.join('File:' + t for t in chunk), 'redirects': '1'}
        req = urllib.request.Request(API + '?' + urllib.parse.urlencode(q), headers={'User-Agent': UA})
        for attempt in range(3):
            try:
                data = json.load(urllib.request.urlopen(req, timeout=60))
                break
            except Exception as e:  # noqa: BLE001 — retry, then give up loudly
                if attempt == 2:
                    raise
                time.sleep(3)
        qd = data.get('query', {})
        alias = {}
        for n in qd.get('normalized', []) + qd.get('redirects', []):
            alias[n['to']] = alias.get(n['from'], n['from'])
        for p in qd.get('pages', {}).values():
            asked = alias.get(p['title'], p['title'])
            asked = asked[5:] if asked.startswith('File:') else asked
            if 'missing' in p or not p.get('imageinfo'):
                found[asked] = None
                continue
            m = p['imageinfo'][0].get('extmetadata', {})
            clean = lambda key: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', (m.get(key) or {}).get('value', ''))).strip()
            found[asked] = {'commons_title': p['title'], 'license': clean('LicenseShortName'),
                            'credit': clean('Credit')[:300], 'artist': clean('Artist')[:160]}
        time.sleep(1)
    return found


def classify(row):
    if row['status'] != 'commons':
        return row['status']
    lic = (row['license'] or '').lower()
    credit = (row['credit'] or '').lower()
    if 'gallica' in credit or 'bnf.fr' in credit or 'bibliothèque nationale' in credit:
        return 'commons-pd-tag/bnf-scan'
    if 'public domain' in lic or lic in ('pd', 'cc0', 'pdm-owner') or lic.startswith('pd'):
        return 'commons-pd-tag'
    return 'commons-' + lic.replace(' ', '-')


def build():
    decks = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'tarot', '*', 'grammar.json'))):
        g = json.load(open(f, encoding='utf-8'))
        if g.get('provenance') not in ('record', 'living'):
            continue
        decks.append((os.path.basename(os.path.dirname(f)), g))
    wanted = []
    for _, g in decks:
        for it in g.get('nodes', []):
            if it.get('image_url'):
                wanted += [t for _, t in candidates(it)]
    answers = query(wanted)
    rows = []
    for slug, g in decks:
        for it in g.get('nodes', []):
            if not it.get('image_url'):
                continue
            row = {'deck': slug, 'provenance': g.get('provenance'), 'item': it.get('id'),
                   'name': it.get('name'), 'image_url': it['image_url'], 'via': None,
                   'status': 'unrecorded', 'commons_title': None, 'license': None, 'credit': None, 'artist': None}
            cands = candidates(it)
            for via, t in cands:
                a = answers.get(t)
                if a:
                    row.update(a)
                    row['via'] = via
                    row['status'] = 'commons'
                    break
            else:
                if cands:
                    row['status'] = 'not-on-commons'
                    row['via'] = cands[0][0]
            md = it.get('metadata') or {}
            if row['status'] != 'commons' and isinstance(md.get('image_source'), str) and md['image_source'].startswith('http'):
                row['status'] = 'recorded-elsewhere'
                row['credit'] = md['image_source']
            row['class'] = classify(row)
            rows.append(row)
    return rows


def summarize(rows, checked):
    by = defaultdict(list)
    for r in rows:
        by[r['deck']].append(r)
    lines = [
        '# Image ledger: what each deck\'s images are',
        '',
        f'Generated by `scripts/audit_image_rights.py` on {checked}. One row per deck; the per-card',
        'evidence is in [`image-ledger.json`](image-ledger.json). It changes no grammar.',
        '',
        'Columns: **images** with an image · **Commons PD tag** (the Commons page says public',
        'domain; that is the uploader\'s claim about the work, not a grant from whoever made the',
        'scan) · **BnF scan** (the Commons credit points at Gallica/BnF: free only for',
        'non-commercial reuse) · **CC BY-SA** (a photographer\'s licence: credit and share-alike) ·',
        '**elsewhere** (`image_source` names a non-Commons upstream, e.g. Yale IIIF or Gallica) ·',
        '**not on Commons** (a file name that Commons does not know) · **unrecorded** (nothing in the',
        'repo says where the image came from).',
        '',
        '| Deck | provenance | images | Commons PD tag | BnF scan | CC BY-SA | other licence | elsewhere | not on Commons | unrecorded | top credit lines |',
        '|---|---|---|---|---|---|---|---|---|---|---|',
    ]
    for slug in sorted(by):
        rs = by[slug]
        c = Counter(r['class'] for r in rs)
        other = sum(v for k, v in c.items() if k.startswith('commons-') and k not in (
            'commons-pd-tag', 'commons-pd-tag/bnf-scan') and 'by-sa' not in k)
        bysa = sum(v for k, v in c.items() if 'by-sa' in k)
        credits = Counter(re.sub(r'https?://([^/\s]+).*', r'\1', r['credit'] or '')[:60] for r in rs if r['credit'])
        top = '; '.join(f'{k} ×{v}' for k, v in credits.most_common(3)) or '—'
        lines.append(f"| `{slug}` | {rs[0]['provenance']} | {len(rs)} | {c['commons-pd-tag']} | "
                     f"{c['commons-pd-tag/bnf-scan']} | {bysa} | {other} | {c['recorded-elsewhere']} | "
                     f"{c['not-on-commons']} | {c['unrecorded']} | {top.replace('|', '/')} |")
    lines.append('')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--offline', action='store_true', help='rebuild the summary from the saved ledger')
    a = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)
    if a.offline:
        saved = json.load(open(LEDGER, encoding='utf-8'))
        rows, checked = saved['rows'], saved['checked']
    else:
        rows = build()
        checked = datetime.date.today().isoformat()
        with open(LEDGER, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump({'checked': checked, 'source': API, 'rows': rows}, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    with open(SUMMARY, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(summarize(rows, checked))
    c = Counter(r['class'] for r in rows)
    print(f'[audit_image_rights] images={len(rows)} ' + ' '.join(f'{k}={v}' for k, v in sorted(c.items())))


if __name__ == '__main__':
    sys.exit(main())
