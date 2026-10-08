# One-off of Oct 5 2026 (history, not tooling; see scripts/archive/README.md). Reads the WordPress API
# dumps of stolen-thyme.com and Yve Lepkowski's Downloads ZIPs from the folder this file sits in.
"""Is each picture on the right card? Compare our card images (R2) with Yve Lepkowski's own files
(the ZIPs on her Downloads page) by a 256-bit difference hash; report the nearest of her files for
every card, and flag large distances or a different card name."""
import io, json, os, re, sys, zipfile, urllib.request, concurrent.futures as cf
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(S, 'tarot')
DECKS = {
    'tarocchino-arlecchino': 'Tarocchino-Arlecchino-Cards.zip',
    'arlecchinos-augmented-arcana': 'Arlecchinos_Augmented_Arcana.zip',
    'anecdotes-tarot': 'Anecdotes_Tarot_Pocket_Edition.zip',
    'petit-lenormand': 'Petit_Lenormand.zip',
    'clown-town-tarot': 'Clown_Town_Tarot.zip',
}


def dhash(img, n=16):
    g = img.convert('L').resize((n + 1, n), Image.LANCZOS)
    px = list(g.getdata())
    bits = 0
    for r in range(n):
        for c in range(n):
            bits = (bits << 1) | (px[r * (n + 1) + c] > px[r * (n + 1) + c + 1])
    return bits


def ham(a, b):
    return bin(a ^ b).count('1')


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'recursive-tarot-image-check/1.0'})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read()))


out = {}
for deck, zname in DECKS.items():
    zf = zipfile.ZipFile(os.path.join(S, 'yvezips', zname))
    hers = {}
    for n in zf.namelist():
        if n.lower().endswith(('.png', '.jpg', '.jpeg')) and 'back' not in n.lower():
            hers[n.split('/', 1)[-1]] = dhash(Image.open(io.BytesIO(zf.read(n))))
    g = json.load(open(os.path.join(REPO, 'tarot', deck, 'grammar.json'), encoding='utf-8'))
    items = [it for it in g['items'] if it.get('image_url')]

    def one(it):
        try:
            h = dhash(fetch(it['image_url']))
        except Exception as e:  # noqa
            return it, None, str(e)
        ranked = sorted(((ham(h, v), k) for k, v in hers.items()))
        return it, ranked[:2], None

    rows = []
    with cf.ThreadPoolExecutor(8) as ex:
        for it, ranked, err in ex.map(one, items):
            if err:
                rows.append({'id': it['id'], 'name': it['name'], 'error': err})
                continue
            (d1, f1), (d2, f2) = ranked[0], ranked[1]
            rows.append({'id': it['id'], 'name': it['name'], 'nearest': f1, 'dist': d1, 'second': f2, 'dist2': d2})
    used = {}
    for r in rows:
        if 'nearest' in r:
            used.setdefault(r['nearest'], []).append(r['name'])
    out[deck] = {'rows': rows, 'her_files': len(hers), 'shared_nearest': {k: v for k, v in used.items() if len(v) > 1},
                 'her_files_unused': sorted(set(hers) - set(used))}
    d = sorted(r['dist'] for r in rows if 'dist' in r)
    print(f'## {deck}: {len(rows)} of our images vs {len(hers)} of hers | distance median {d[len(d)//2]} max {d[-1]}')
    for r in sorted((r for r in rows if r.get('dist', 999) > 40 or 'error' in r), key=lambda r: -r.get('dist', 999))[:12]:
        print('   far/err:', r['name'][:40], '->', r.get('nearest'), r.get('dist'), r.get('error', ''))
    for k, v in out[deck]['shared_nearest'].items():
        print('   two cards share', k, ':', v)
    print('   her files no card matched:', out[deck]['her_files_unused'][:10])
json.dump(out, open(os.path.join(S, 'yve-images.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
