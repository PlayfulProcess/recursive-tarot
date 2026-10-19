#!/usr/bin/env python3
"""Build Book T's linocut: the deck's fifth picture set, the full imagery printed as a relief print.

  python scripts/build_book_t_linocut.py            # write tarot/book-t/linocut/*.svg + the grammar's entries
  python scripts/build_book_t_linocut.py --check    # write nothing; exit 1 if anything is out of date
  python scripts/build_book_t_linocut.py --only wands-05,swords-10 --png DIR   # samples, rendered to PNG

Her words (Oct 20 2026): "I think the images are overall a bit ugly and childlike ... try to make a new version
focusing on making them pretty. Maybe linocut style."

* The same compositions as the full imagery (`tarot/book-t/full-imagery/compositions.json`: the Book T sentence
  each card follows, and its layers), so the two sets always show the same things in the same places.
* A part is printed from its linocut block when one exists (`tarot/book-t/parts-linocut/<name>.svg`, carved for
  this set), else from the full imagery's part (`tarot/book-t/parts/`), pulled into the print's inks: every fill
  becomes paper, the card's ink (cut with fine gouge lines), or black, by its lightness; every line becomes black.
* The inks: black on warm paper, with one ink for the suit's element (Fire vermilion, Water deep blue, Air ochre,
  Earth olive) and gold for the Keys. The paper grain, the gouge chips and the soft edges of a hand-pulled print are
  SVG filters and patterns (no images), so each card stays a small text file.
* Output: `tarot/book-t/linocut/<card id>.svg` and one `metadata.illustrations` entry per card,
  `edition: "Book T deck, linocut"`; the 1912 page's Pictures switch shows it as **Linocut**.
"""
import argparse, colorsys, hashlib, json, os, re, sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_book_t_iconography as ico  # noqa: E402
import build_book_t_full_imagery as fi  # noqa: E402

ROOT = ico.ROOT
DECK = ico.DECK
BLOCKS = os.path.join(ROOT, 'tarot', 'book-t', 'parts-linocut')
OUT = os.path.join(ROOT, 'tarot', 'book-t', 'linocut')
URL = 'https://tarot.recursive.eco/tarot/book-t/linocut/%s.svg'
EDITION = 'Book T deck, linocut'
ARTIST = ("PlayfulProcess: a linocut printing of the full imagery, composed by script "
          "(scripts/build_book_t_linocut.py) from the same spec per card, which follows Book T (1912)")
W, H, CX, f = ico.W, ico.H, ico.CX, ico.f
PIC_TOP, PIC_BOTTOM = 40, 812

PAPER = '#f2e8d2'
BLACK = '#1c1915'
INK = {'Fire': '#b8371f', 'Water': '#1f4a78', 'Air': '#b88a22', 'Earth': '#56632a', 'Keys': '#a87c22'}


# ── colour: every colour of a part becomes paper, ink or black ──────────────────────────────────

def lum(hexc):
    h = hexc.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b, colorsys.rgb_to_hls(r, g, b)[2]


def tone(hexc):
    """'paper' (cut away), 'tint' (ink cut thin, a light tone), 'ink' (solid ink, fine gouge lines), 'black'."""
    L, S = lum(hexc)
    if L > 0.80:
        return 'paper'
    if L > 0.62:
        return 'tint'
    if L < 0.22:
        return 'black'
    return 'ink'


FILL_OF = {'paper': PAPER, 'tint': 'url(#tint)', 'ink': 'url(#gouge)', 'black': BLACK}


def pull(body, current):
    """Pull a part's SVG into the print's inks. `current` is the colour that currentColor resolves to."""
    def fill(m):
        attr, val = m.group(1), m.group(2)
        if val in ('none',) or val.startswith('url('):
            return m.group(0)
        c = current if val == 'currentColor' else val
        if not c.startswith('#'):
            return m.group(0)
        if attr == 'stroke':
            t = tone(c)
            return 'stroke="%s"' % (PAPER if t == 'paper' and STROKE_PAPER.get('on') else BLACK)
        return 'fill="%s"' % FILL_OF[tone(c)]
    out = re.sub(r'\b(fill|stroke)="([^"]+)"', fill, body)
    # lines a little bolder, as a carved line is
    out = re.sub(r'stroke-width="([\d.]+)"', lambda m: 'stroke-width="%s"' % f(float(m.group(1)) * 1.35 + 0.4), out)
    return out


STROKE_PAPER = {}


_blocks = {}


def block(name):
    """A part's linocut block (parts-linocut/<name>.svg) if it has one: (body, default colour, carved?)."""
    if name not in _blocks:
        p = os.path.join(BLOCKS, name + '.svg')
        if os.path.exists(p):
            s = open(p, encoding='utf-8').read()
            m = re.search(r'<g id="part"([^>]*)>(.*)</g>\s*</svg>', s, re.S)
            dc = re.search(r'data-color="([^"]+)"', m.group(1))
            body = ' '.join(line.strip() for line in m.group(2).splitlines()
                            if line.strip() and not line.strip().startswith('<!--'))
            _blocks[name] = (body, dc.group(1) if dc else BLACK, True)
        else:
            body, dc = fi.part(name)
            _blocks[name] = (body, dc, False)
    return _blocks[name]


# ── layers ──────────────────────────────────────────────────────────────────────────────────────

def layer_part(L, defs, ink):
    name = L['part']
    body, default, carved = block(name)
    col = L.get('color', default)
    key = 'p-%s-%s' % (name, hashlib.md5(col.encode()).hexdigest()[:5])
    if key not in defs:
        if carved:
            # a carved block: 'currentColor' is the card's ink unless the spec asks for black or paper
            t = tone(col) if col.startswith('#') else 'ink'
            c = {'black': BLACK, 'paper': PAPER}.get(t, ink)
            defs[key] = '<g id="%s" style="color:%s">%s</g>' % (key, c, body)
        else:
            defs[key] = '<g id="%s">%s</g>' % (key, pull(body, col))
    pts = fi.points(L['at'])
    rots = L.get('rot', 0)
    rots = rots if isinstance(rots, list) else [rots]
    if len(pts) == 1:
        pts = pts * len(rots)
    if len(rots) == 1:
        rots = rots * len(pts)
    s = L.get('s', 1)
    sx = -s if L.get('flip') else s
    out = []
    for (x, y), r in zip(pts, rots):
        t = 'translate(%s %s)' % (f(x), f(y))
        if r:
            t += ' rotate(%s)' % f(r)
        if sx != 1 or s != 1:
            t += ' scale(%s %s)' % (f(sx), f(s)) if sx != s else ' scale(%s)' % f(s)
        op = (' opacity="%s"' % L['opacity']) if 'opacity' in L else ''
        out.append('<use href="#%s" transform="%s"%s/>' % (key, t, op))
    return ''.join(out)


def layer_glyph(L, node, ink):
    name = fi.resolve_glyph(L['glyph'], node)
    # planets and signs in the card's ink, letters and elements in black
    col = BLACK if ico.glyph_file(name).startswith(('hebrew', 'element')) else ink
    out = []
    for (x, y) in fi.points(L['at']):
        g = ico.glyph(name, x, y, L.get('size', 100), col)
        g = re.sub(r'stroke-width="([\d.]+)"', lambda m: 'stroke-width="%s"' % f(float(m.group(1)) * 1.25), g, count=1)
        out.append(g)
    return ''.join(out)


CURVE = {
    'stem': (BLACK, 6, None, 0), 'branch': (BLACK, 7, None, 0),
    'stream': (BLACK, 8, PAPER, 4), 'stream-gold': (BLACK, 8, 'INK', 4),
    'smoke': (BLACK, 11, PAPER, 7), 'chain': (BLACK, 4, None, 0), 'bolt': (BLACK, 9, 'INK', 5),
}


def layer_curve(L, ink):
    under, uw, over, ow = CURVE[L['curve']]
    ds = []
    for p in L['paths']:
        if len(p) == 6:
            ds.append('M%s %s Q%s %s %s %s' % tuple(f(v) for v in p))
        else:
            ds.append('M%s %s C%s %s %s %s %s %s' % tuple(f(v) for v in p))
    d = ' '.join(ds)
    out = '<path d="%s" stroke="%s" stroke-width="%s"/>' % (d, under, uw)
    if over:
        out += '<path d="%s" stroke="%s" stroke-width="%s"/>' % (d, ink if over == 'INK' else over, ow)
    dash = ' stroke-dasharray="7 4"' if L['curve'] == 'chain' else ''
    return '<g fill="none" stroke-linecap="round" stroke-linejoin="round"%s>%s</g>' % (dash, out)


# ── the print ───────────────────────────────────────────────────────────────────────────────────

def defs_common(ink):
    """Patterns for the gouge and the tint, the paper grain, and the print's soft edges."""
    return (
        # solid ink, cut with fine parallel gouge lines (the cutter's stroke, 45 degrees)
        '<pattern id="gouge" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)">'
        '<rect width="9" height="9" fill="%s"/><path d="M0 4.5 H9" stroke="%s" stroke-width="1.1" opacity=".55"/></pattern>'
        # a light tone: paper, with short ink cuts
        '<pattern id="tint" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)">'
        '<rect width="10" height="10" fill="%s"/><path d="M0 5 H10" stroke="%s" stroke-width="2.2"/></pattern>'
        # shading on a white thing: paper with fine black cuts
        '<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)">'
        '<rect width="6" height="6" fill="%s"/><path d="M0 3 H6" stroke="%s" stroke-width="1.3"/></pattern>'
        # the soft, slightly uneven edge of a pulled print
        '<filter id="press" x="-2%%" y="-2%%" width="104%%" height="104%%">'
        '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G"/></filter>'
        # the paper's grain: sparse pale flecks where the ink did not take
        '<filter id="grain" x="0" y="0" width="100%%" height="100%%">'
        '<feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="3"/>'
        '<feColorMatrix values="0 0 0 0 .95  0 0 0 0 .91  0 0 0 0 .82  0 0 0 -6 3.1"/></filter>'
        % (ink, PAPER, PAPER, ink, PAPER, BLACK))


def chatter(seed, ink):
    """The short cuts left standing in the cleared ground of a block (a real print's 'chatter'), placed from a
    seed so each card's ground is its own and every build is the same."""
    h = hashlib.md5(seed.encode()).digest()
    out = []
    # three little groups of parallel cuts, low in the picture, where a carver's gouge skipped
    for i in range(3):
        x = 60 + (h[2 * i] / 255) * 380
        y = 640 + (h[2 * i + 1] / 255) * 130
        for k in range(2 + h[8 + i] % 2):
            L = 12 + (h[11 + i + k] % 16)
            out.append('M%s %s h%s' % (f(x + k * 3), f(y + k * 5), f(L)))
    return '<path d="%s" stroke="%s" stroke-width="1.8" stroke-linecap="round" opacity=".35"/>' % (' '.join(out), ink)


def arch(ink):
    """The picture stands in a carved arch: the two spandrels above it are cut in fine horizontal lines of the
    card's ink, and a double rule follows the arch."""
    a = 'M30 250 C30 110 140 64 280 64 C420 64 530 110 530 250'
    lines = ''.join('M30 %d H530 ' % y for y in range(34, 250, 6))
    return ('<clipPath id="spandrel"><path d="M30 30 H530 V250 C530 110 420 64 280 64 C140 64 30 110 30 250 Z"/></clipPath>'
            '<g clip-path="url(#spandrel)"><path d="%s" stroke="%s" stroke-width="1.6" opacity=".55"/></g>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="3.2"/>'
            '<path d="M36 252 C36 116 144 72 280 72 C416 72 524 116 524 252" fill="none" stroke="%s" stroke-width="1.2"/>'
            % (lines, ink, a, BLACK, BLACK))


def teeth():
    """Small triangles cut along the inside of the frame (the woodcut's dog-tooth border)."""
    d = []
    for x in range(34, 520, 14):
        d.append('M%d 30 l7 7 l7 -7 Z' % x)
    for y in range(34, PIC_BOTTOM - 12, 14):
        d.append('M30 %d l7 7 l-7 7 Z' % y)
        d.append('M530 %d l-7 7 l7 7 Z' % y)
    return '<path d="%s" fill="%s"/>' % (' '.join(d), BLACK)


def border(ink, sub, name):
    """A carved border and a title cartouche cut into a black block (the letters are the paper left standing)."""
    lines = [name]
    if len(name) > 28:
        for sep in (': ', '; ', ', '):
            if sep in name:
                a, b = name.split(sep, 1)
                lines = [a + sep.strip(), b[0].upper() + b[1:]]
                break
    size = 27 if max(len(x) for x in lines) <= 26 else (23 if max(len(x) for x in lines) <= 34 else 19)
    y0 = 868 if len(lines) == 1 else 852
    title = ''.join('<text x="%s" y="%d" font-size="%d" text-anchor="middle" fill="%s" letter-spacing="1.2" '
                    'font-family="Georgia, \'Times New Roman\', serif">%s</text>'
                    % (f(CX), y0 + i * (size + 5), size, PAPER, escape(ln.upper() if len(ln) < 22 else ln)) for i, ln in enumerate(lines))
    return (
        '<g filter="url(#press)">'
        # the outer frame, carved as a thick black band with an inner cut line
        '<path d="M14 14 H546 V946 H14 Z M30 30 V%d H530 V30 Z" fill="%s" fill-rule="evenodd"/>' % (PIC_BOTTOM, BLACK) +
        '<rect x="21" y="21" width="518" height="918" fill="none" stroke="%s" stroke-width="1.6"/>' % PAPER +
        teeth() +
        # the cartouche
        '<rect x="30" y="%d" width="500" height="%d" fill="%s"/>' % (PIC_BOTTOM, 946 - 14 - PIC_BOTTOM, BLACK) +
        '<path d="M44 %d H516" stroke="%s" stroke-width="1.4"/>' % (PIC_BOTTOM + 10, ink) +
        title +
        '<text x="%s" y="912" font-size="15" text-anchor="middle" fill="%s" font-style="italic" '
        'font-family="Georgia, \'Times New Roman\', serif" opacity=".8">%s</text>' % (f(CX), PAPER, escape(sub)) +
        '</g>')


def card_svg(node, spec):
    m = node['metadata']
    cat = node['category']
    ink = INK['Keys'] if cat == 'keys' else INK[m['element']]
    _, top, sub = fi.chrome(node)
    defs, body = {}, []
    for L in spec['layers']:
        if 'part' in L:
            body.append(layer_part(L, defs, ink))
        elif 'glyph' in L and cat == 'keys' and L['glyph'] == 'letter':
            continue  # the Key's letter is cut in its corner roundel
        elif 'glyph' in L:
            body.append(layer_glyph(L, node, ink))
        elif 'curve' in L:
            body.append(layer_curve(L, ink))
    # the corner marks of the iconography, in black; a Key carries its number and its letter
    if cat == 'keys':
        num = ico.ROMAN[m['key_number']]
        top = ('<text x="64" y="%d" font-size="%d" text-anchor="middle" fill="%s" font-family="Georgia, \'Times New Roman\', serif">%s</text>'
               % (78 if len(num) < 4 else 76, 28 if len(num) < 3 else (22 if len(num) < 4 else 17), BLACK, num)
               + ico.glyph(ico.HEBREW[m['hebrew_letter']], W - 64, 68, 34, BLACK))
    top = re.sub(r'style="color:[^"]+"', 'style="color:%s"' % BLACK, top)
    top = re.sub(r'fill="#6b5d4a"', 'fill="%s"' % BLACK, top)
    # the corner marks sit on small paper roundels cut out of the spandrels
    corners = ''.join('<circle cx="%d" cy="%d" r="27" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x, y, PAPER, BLACK)
                      for x, y in ((64, 68), (W - 64, 68)))
    title = '%s: %s (Book T deck, linocut)' % (node['name'], sub)
    desc = ('A linocut printing of the full imagery. %s Book T (1912): "%s"' % (spec.get('note', ''), spec['follows'])).replace('  ', ' ')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-labelledby="t d">\n'
            '<title id="t">%s</title>\n<desc id="d">%s Parts drawn for recursive-tarot (CC BY-SA 4.0); printed by scripts/build_book_t_linocut.py.</desc>\n'
            '<defs>%s%s<clipPath id="pic"><rect x="30" y="30" width="500" height="%d"/></clipPath></defs>\n'
            '<rect width="%d" height="%d" fill="%s"/>\n'
            '<g clip-path="url(#pic)">%s'
            '<g filter="url(#press)">\n%s\n%s\n</g></g>\n%s\n'
            '<rect width="%d" height="%d" filter="url(#grain)"/>\n</svg>\n'
            % (W, H, W, H, escape(title), escape(desc), defs_common(ink), ''.join(defs.values()), PIC_BOTTOM - 30,
               W, H, PAPER, arch(ink) + chatter(node['id'], ink), '\n'.join(body), corners + top, border(ink, sub, node['name']), W, H))


def with_illustration(node):
    m = node['metadata']
    entry = {'url': URL % node['id'], 'artist': ARTIST, 'edition': EDITION, 'license': 'CC-BY-SA-4.0'}
    ills = list(m.get('illustrations') or [])
    at = [k for k, i in enumerate(ills) if i.get('edition') == EDITION]
    if at:
        ills[at[0]] = entry
        ills = [i for k, i in enumerate(ills) if k not in at[1:]]
    else:
        ills.append(entry)
    m['illustrations'] = ills


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--only', default='')
    ap.add_argument('--png', default='')
    a = ap.parse_args()
    only = set(x for x in a.only.split(',') if x)
    specs = json.load(open(fi.SPECS, encoding='utf-8'))
    cur_json = open(DECK, encoding='utf-8').read()
    g = json.loads(cur_json)
    cards = [n for n in g['nodes'] if n.get('category') in ('aces', 'courts', 'decans', 'keys')]
    if len(cards) != 78:
        raise SystemExit('expected 78 cards, found %d' % len(cards))
    os.makedirs(OUT, exist_ok=True) if not a.check else None
    stale, done = [], []
    for n in cards:
        if only and n['id'] not in only:
            continue
        svg = card_svg(n, specs[n['id']])
        done.append(n['id'])
        p = os.path.join(OUT, n['id'] + '.svg')
        old = open(p, encoding='utf-8').read() if os.path.exists(p) else None
        if old != svg:
            stale.append(n['id'])
            if not a.check:
                with open(p, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(svg)
        if not only:
            with_illustration(n)
    out_json = json.dumps(g, ensure_ascii=False, indent=2) + '\n'
    grammar_stale = not only and out_json != cur_json
    if a.check:
        ok = not stale and not grammar_stale
        print('[build_book_t_linocut] --check: %s' % ('up to date (78 cards)' if ok else
              'out of date (%d pictures%s); run: python scripts/build_book_t_linocut.py'
              % (len(stale), ', the grammar' if grammar_stale else '')))
        sys.exit(0 if ok else 1)
    if grammar_stale:
        with open(DECK, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(out_json)
    print('[build_book_t_linocut] %d pictures written%s' % (len(stale), ', grammar updated' if grammar_stale else ''))
    if a.png:
        fi.OUT = OUT
        fi.render_pngs(done, a.png)


if __name__ == '__main__':
    main()
