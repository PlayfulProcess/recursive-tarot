# One-off of Oct 5 2026 (history, not tooling; see scripts/archive/README.md). Reads the WordPress API
# dumps of stolen-thyme.com and Yve Lepkowski's Downloads ZIPs from the folder this file sits in.
"""Put Yve Lepkowski's own words back on her cards, from her published guidebook pages (WordPress
API dumps of Oct 5 2026). Only sections meant to be hers are touched. Reports every change."""
import json, os, re, sys, difflib, unicodedata
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yve_parse import load_pages, parse, clean

REPO = sys.argv[1]
DRY = '--dry' in sys.argv
P = load_pages()


def key(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'\([^)]*\)', ' ', s)
    s = re.sub(r'^[\divxlc]+\s*[.:-]\s*', '', s.strip())
    s = re.sub(r'\b(the|le|la|l|il)\b', ' ', s)
    for a, b in (('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'), ('seven', '7'),
                 ('eight', '8'), ('nine', '9'), ('ten', '10')):
        s = re.sub(r'\b%s\b' % a, b, s)
    return ' '.join(re.findall(r'[a-z0-9]+', s))


MANUAL = {'Death': 'clown-town-tarot/guidebook/xiii/', 'The House (Tower)': 'clown-town-tarot/guidebook/xvi-the-house-of-god/'}


def pick(prefix, name):
    if name in MANUAL and prefix in MANUAL[name]:
        k = 'https://stolen-thyme.com/' + MANUAL[name]
        return (k, P[k]) if k in P else (None, None)
    cands = [(k, v) for k, v in P.items() if prefix in k]
    best = max(cands, key=lambda kv: difflib.SequenceMatcher(None, key(name), key(kv[1]['title'])).ratio())
    r = difflib.SequenceMatcher(None, key(name), key(best[1]['title'])).ratio()
    return best if r >= 0.8 else (None, None)


def join(ps):
    return '\n\n'.join(t for _, t in ps)


EPIGRAPHS = []


def drop_epigraph(ps, where):
    """Leave out a verse epigraph: the paragraph(s) before an attribution line starting with a dash.
    Song lyrics are never stored, so no epigraph is copied, whatever its age."""
    out = list(ps)
    for i, (_, txt) in enumerate(ps):
        if re.match(r'^\s*[–—-]\s*\S', txt) and i <= 3:
            EPIGRAPHS.append((where, txt[:80]))
            out = ps[i + 1:]
    # a verse paragraph first (short lines), with or without an attribution line after it
    if out and '\n' in out[0][1] and all(len(l) < 80 for l in out[0][1].split('\n')):
        EPIGRAPHS.append((where, 'verse: ' + out[0][1].split('\n')[0][:40]))
        out = out[1:]
        if out and len(out[0][1]) < 120 and not out[0][1].rstrip().endswith('.'):
            EPIGRAPHS.append((where, 'attribution: ' + out[0][1][:60]))
            out = out[1:]
    return out


def by_heading(raw):
    """Tarocchino pages use h-tags: return {heading: [paragraph texts]}."""
    parts = re.split(r'<h[1-6][^>]*>(.*?)</h[1-6]>', raw, flags=re.S)
    out, cur = {}, None
    for i, chunk in enumerate(parts):
        if i % 2 == 1:
            cur = clean(chunk)
            out.setdefault(cur, [])
        elif cur:
            out[cur] += [t for t in (clean(m.group(2)) for m in re.finditer(r'<(p|li)[^>]*>(.*?)</\1>', chunk, re.S)) if t]
    return out


def load(slug):
    p = os.path.join(REPO, 'tarot', slug, 'grammar.json')
    raw = open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    g = json.loads(raw)
    assert json.dumps(g, ensure_ascii=False, indent=2).rstrip('\n') == raw.rstrip('\n'), slug
    return p, g, raw.endswith('\n')


def save(p, g, nl):
    if not DRY:
        open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(g, ensure_ascii=False, indent=2) + ('\n' if nl else ''))


report = {}
unmatched = {}


def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-')
    return re.sub(r'\s+', ' ', s).strip()


def setsec(slug, it, sec, new):
    old = (it.get('sections') or {}).get(sec)
    if new and norm(old) != norm(new):
        it.setdefault('sections', {})[sec] = new
        report.setdefault(slug, Counter())[sec] += 1


# Anecdotes Tarot: accordions "Image Description" and "Interpretation"
p, g, nl = load('anecdotes-tarot')
for it in g['nodes']:
    k, page = pick('anecdotes-tarot/guidebook/', it['name'])
    if not page:
        unmatched.setdefault('anecdotes-tarot', []).append(it['name']); continue
    s = parse(page['raw'])['sections']
    setsec('anecdotes-tarot', it, 'The card', join(s.get('Image Description', [])))
    setsec('anecdotes-tarot', it, 'Interpretation', join(s.get('Interpretation', [])))
    sm = s.get('Selected Meanings') or s.get('Selected meanings')
    if sm:
        setsec('anecdotes-tarot', it, 'Selected meanings', join(sm))
save(p, g, nl)

# Clown Town Tarot: text outside the accordion is the interpretation; "Image Description" is the card
p, g, nl = load('clown-town-tarot')
for it in g['nodes']:
    k, page = pick('clown-town-tarot/guidebook/', it['name'])
    if not page:
        unmatched.setdefault('clown-town-tarot', []).append(it['name']); continue
    pr = parse(page['raw'])
    setsec('clown-town-tarot', it, 'The card', join(pr['sections'].get('Image Description', [])))
    setsec('clown-town-tarot', it, 'Interpretation', join(drop_epigraph(pr['outside'], it['name'])))
save(p, g, nl)

# Tarocchino Arlecchino: headings; "Image Description" is the card; meanings under Upright / Reversed
p, g, nl = load('tarocchino-arlecchino')
for it in g['nodes']:
    k, page = pick('tarocchino-arlecchino/guidebook/', it['name'])
    if not page:
        unmatched.setdefault('tarocchino-arlecchino', []).append(it['name']); continue
    h = by_heading(page['raw'])
    setsec('tarocchino-arlecchino', it, 'The card', '\n\n'.join(h.get('Image Description', [])))
    if h.get('Upright'):
        setsec('tarocchino-arlecchino', it, 'Upright meaning (Etteilla system)', '\n\n'.join(h['Upright']))
    if h.get('Reversed'):
        setsec('tarocchino-arlecchino', it, 'Reversed meaning (Etteilla system)', '\n\n'.join(h['Reversed']))
save(p, g, nl)

for w, a in EPIGRAPHS:
    print('epigraph left out:', w, '|', a)
for slug, c in report.items():
    print(slug, dict(c))
for slug, names in unmatched.items():
    print('UNMATCHED', slug, len(names), names[:8])
