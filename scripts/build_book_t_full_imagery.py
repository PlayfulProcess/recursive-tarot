#!/usr/bin/env python3
"""Build Book T's full imagery: the deck's fourth picture set, everything Book T's text describes.

  python scripts/build_book_t_full_imagery.py            # write tarot/book-t/full-imagery/*.svg + the grammar's entries
  python scripts/build_book_t_full_imagery.py --check    # write nothing; exit 1 if anything is out of date
  python scripts/build_book_t_full_imagery.py --only wands-05,swords-10   # write just these cards (samples)
  python scripts/build_book_t_full_imagery.py --png DIR  # also render PNGs (needs resvg_py) and two contact sheets

Her words (Oct 20 2026), on seeing the iconography: "go through the whole deck and render a full imagery
in this style as an alternative to current rendering."

* A card is a composition of parts, read from data. What each card shows is written in
  `tarot/book-t/full-imagery/compositions.json`: one small spec per card, each with the Book T sentence
  it follows (`follows`) and its `layers`, drawn in order. Nothing card-specific lives in this script.
* The parts are `tarot/book-t/parts/*.svg` (the white radiating angelic hand issuing from clouds, the
  clasped hands, the suit symbols, roses, lotuses, flames, waters, the court figures and their beasts):
  drawn for this site as hand-written SVG, CC BY-SA 4.0 like the deck (see the folder's README), plus
  the iconography's glyphs in `tarot/book-t/glyphs/` (planets, signs, elements, Hebrew letters).
* The frame, caption, corner letter and element are the iconography's (scripts/build_book_t_iconography.py),
  so the two sets read as one family.

A layer is one of:
  {"part": name, "at": [x, y] | [[x, y], ...], "rot": deg | [deg, ...], "s": scale, "flip": true,
   "color": css colour (fills the part's currentColor), "opacity": 0-1}
      places a part (its origin at `at`); a list of points or of angles repeats it.
  {"glyph": name | "above" | "below" | "letter" | "element" | "attr1" | "attr2", "at": [x, y],
   "size": px, "color": css}
      places a glyph; "above"/"below" are the decan's planet and sign in the order Book T names them,
      "letter" the card's letter (the Keys' own, else the Tetragrammaton letter Book T gives the card).
  {"curve": "stem" | "branch" | "stream" | "stream-gold" | "smoke" | "chain" | "bolt", "paths": [[x0, y0, cx, cy, x1, y1], ...]}
      quadratic curves (eight numbers make a cubic), for stems, branches, poured water, smoke.
The card is 560 x 960; the picture lives between y=40 and y=830, the caption below.
"""
import argparse, json, os, re, sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_book_t_iconography as ico  # noqa: E402  (the frame, the glyphs, Book T's decan order)

ROOT = ico.ROOT
DECK = ico.DECK
PARTS = os.path.join(ROOT, 'tarot', 'book-t', 'parts')
HOME = os.path.join(ROOT, 'tarot', 'book-t', 'full-imagery')
SPECS = os.path.join(HOME, 'compositions.json')
OUT = HOME
URL = 'https://tarot.recursive.eco/tarot/book-t/full-imagery/%s.svg'
EDITION = 'Book T deck, full imagery'
ARTIST = ("PlayfulProcess: parts drawn for this deck (tarot/book-t/parts, tarot/book-t/glyphs), composed by "
          "script (scripts/build_book_t_full_imagery.py) from a spec per card that follows Book T (1912)")
W, H, CX, f = ico.W, ico.H, ico.CX, ico.f
PIC_BOTTOM = 830  # the picture is clipped here; the caption sits below

CURVE_STYLE = {
    # (under-stroke colour, width, over-stroke colour, width, extra)
    'stem': ('#2f5a22', 7, '#5e8a3a', 4, ''),
    'branch': ('#4a3520', 8, '#7a5a34', 5, ''),
    'stream': ('#3f7fbf', 9, '#ffffff', 5, ''),
    'stream-gold': ('#a8822a', 9, '#f2d16b', 5, ''),
    'smoke': ('#9aa0aa', 12, '#d9dce2', 8, ' opacity=".8"'),
    'chain': ('#4a4a52', 5, '#9a9aa4', 2.5, ' stroke-dasharray="7 4"'),
    'bolt': ('#b0361f', 9, '#ffd84a', 5, ''),
}


# ── parts ───────────────────────────────────────────────────────────────────────────────────────

_parts = {}


def part(name):
    """The inner SVG of tarot/book-t/parts/<name>.svg's <g id="part">, and its default colour."""
    if name not in _parts:
        p = os.path.join(PARTS, name + '.svg')
        if not os.path.exists(p):
            raise SystemExit('no part %s (tarot/book-t/parts/%s.svg)' % (name, name))
        s = open(p, encoding='utf-8').read()
        m = re.search(r'<g id="part"([^>]*)>(.*)</g>\s*</svg>', s, re.S)
        if not m:
            raise SystemExit('part %s has no <g id="part">' % name)
        dc = re.search(r'data-color="([^"]+)"', m.group(1))
        body = ' '.join(line.strip() for line in m.group(2).splitlines() if line.strip()
                        and not line.strip().startswith('<!--'))
        _parts[name] = (body, dc.group(1) if dc else '#888888')
    return _parts[name]


def points(at):
    return at if at and isinstance(at[0], (list, tuple)) else [at]


def layer_part(L, used):
    name = L['part']
    body, default = part(name)
    used.add(name)
    pts = points(L['at'])
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
        style = 'color:%s' % L.get('color', default)
        op = (' opacity="%s"' % L['opacity']) if 'opacity' in L else ''
        out.append('<use href="#p-%s" transform="%s" style="%s"%s/>' % (name, t, style, op))
    return ''.join(out)


def resolve_glyph(name, node):
    m = node['metadata']
    if name in ('above', 'below'):
        above, below, _, _ = ico.decan_order(node)
        return above if name == 'above' else below
    if name == 'letter':
        if node['category'] == 'keys':
            return ico.HEBREW[m['hebrew_letter']]
        if node['category'] == 'courts':
            return ico.RANK_LETTER[m['rank']]
        return ico.tetragrammaton(node)
    if name == 'element':
        return m.get('element') or 'Spirit'
    if name in ('rule1', 'rule2'):
        rm = re.match(r'\s*\d+\D+?([A-Z][a-z]+)\s*\W+\s*\d+\D+?([A-Z][a-z]+)', m.get('rules', ''))
        if not rm:
            raise SystemExit('%s: no two signs in rules %r' % (node['id'], m.get('rules')))
        return rm.group(1) if name == 'rule1' else rm.group(2)
    if name in ('sub', 'of'):
        a, b = [x.strip() for x in m['element_in_element'].split(' of ')]
        return a if name == 'sub' else b
    if name in ('attr1', 'attr2'):
        attrs = [a.strip() for a in re.split(r'\band\b', m['attribution'])]
        i = 0 if name == 'attr1' else 1
        return attrs[i] if i < len(attrs) else attrs[0]
    return name


def layer_glyph(L, node):
    name = resolve_glyph(L['glyph'], node)
    col = L.get('color') or (ico.INK if ico.glyph_file(name).startswith('hebrew') else ico.color_of(name))
    out = []
    for (x, y) in points(L['at']):
        out.append(ico.glyph(name, x, y, L.get('size', 100), col))
    return ''.join(out)


def layer_curve(L):
    under, uw, over, ow, extra = CURVE_STYLE[L['curve']]
    ds = []
    for p in L['paths']:
        if len(p) == 6:
            ds.append('M%s %s Q%s %s %s %s' % tuple(f(v) for v in p))
        elif len(p) == 8:
            ds.append('M%s %s C%s %s %s %s %s %s' % tuple(f(v) for v in p))
        else:
            raise SystemExit('a curve takes 6 or 8 numbers, got %r' % (p,))
    d = ' '.join(ds)
    return ('<g fill="none" stroke-linecap="round" stroke-linejoin="round"%s>'
            '<path d="%s" stroke="%s" stroke-width="%s"/><path d="%s" stroke="%s" stroke-width="%s"/></g>'
            % (extra, d, under, uw, d, over, ow))


# ── a card ──────────────────────────────────────────────────────────────────────────────────────

def chrome(node):
    """The iconography's frame, corner letter, element and caption (the same family of cards)."""
    m = node['metadata']
    cat = node['category']
    if cat == 'keys':
        attrs = [a.strip() for a in re.split(r'\band\b', m['attribution'])]
        color = ico.color_of(attrs[-1]) if len(attrs) == 1 else ico.ELEMENT_COLOR.get(attrs[0], ico.INK)
        sub = '%s · %s · %s' % (m['card_name_1912'], m['hebrew_translit'], m['attribution'])
        top = ico.corner_text(64, 78, ico.ROMAN[m['key_number']], 30)
        return color, top, sub
    color = ico.ELEMENT_COLOR[m['element']]
    if cat == 'decans':
        sub = '%s · %s · %s' % (m['card_name_1912'], m['decan'], m['sephirah'])
    elif cat == 'aces':
        sub = '%s · the Root · %s' % (m['card_name_1912'], m['sephirah'])
    else:
        sub = '%s · %s' % (m['card_name_1912'], m['element_in_element'])
    letter = ico.RANK_LETTER[m['rank']] if cat == 'courts' else ico.tetragrammaton(node)
    top = ico.glyph(letter, 62, 66, 52, ico.INK) + ico.glyph(m['element'], W - 60, 62, 40, color)
    return color, top, sub


def card_svg(node, spec):
    color, top, sub = chrome(node)
    used, body = set(), []
    for L in spec['layers']:
        if 'part' in L:
            body.append(layer_part(L, used))
        elif 'glyph' in L:
            body.append(layer_glyph(L, node))
        elif 'curve' in L:
            body.append(layer_curve(L))
        else:
            raise SystemExit('%s: unknown layer %r' % (node['id'], L))
    defs = ''.join('<g id="p-%s">%s</g>' % (n, part(n)[0]) for n in sorted(used))
    title = '%s: %s (Book T deck, full imagery)' % (node['name'], sub)
    if spec.get('note'):
        desc = '%s Book T (1912): "%s"' % (spec['note'], spec['follows'])
    else:
        desc = 'Drawn as Book T (1912) describes it: "%s"' % spec['follows']
    clip = ('<clipPath id="pic"><rect x="24" y="24" width="%d" height="%d" rx="10"/></clipPath>'
            % (W - 48, PIC_BOTTOM - 24))
    rule = ('<line x1="24" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.5" opacity=".55"/>'
            % (PIC_BOTTOM, W - 24, PIC_BOTTOM, color))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-labelledby="t d">\n'
            '<title id="t">%s</title>\n<desc id="d">%s Parts drawn for recursive-tarot (CC BY-SA 4.0); composed by scripts/build_book_t_full_imagery.py.</desc>\n'
            '<defs>%s%s</defs>\n%s\n<g clip-path="url(#pic)">\n%s\n</g>\n%s\n%s\n%s\n</svg>\n'
            % (W, H, W, H, escape(title), escape(desc), defs, clip,
               ico.frame(color), '\n'.join(body), rule, top, ico.caption(node['name'], sub)))


# ── the grammar ─────────────────────────────────────────────────────────────────────────────────

def with_illustration(node):
    m = node['metadata']
    entry = {'url': URL % node['id'], 'artist': ARTIST, 'edition': EDITION, 'license': 'CC-BY-SA-4.0'}
    ills = list(m.get('illustrations') or [])
    at = [k for k, i in enumerate(ills) if i.get('edition') == EDITION]
    if at:  # replace in place, so the other picture sets' generators keep their order too
        ills[at[0]] = entry
        ills = [i for k, i in enumerate(ills) if k not in at[1:]]
    else:
        ills.append(entry)
    m['illustrations'] = ills


def render_pngs(ids, out_dir):
    import resvg_py
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    files = []
    for i in ids:
        p = os.path.join(out_dir, i + '.png')
        png = resvg_py.svg_to_bytes(svg_path=os.path.join(OUT, i + '.svg'), width=420)
        open(p, 'wb').write(bytes(png))
        files.append(p)
    if len(files) > 1:  # contact sheets: two for the whole deck, one for a few samples
        half = (len(files) + 1) // 2 if len(files) > 8 else len(files)
        for k, chunk in enumerate([c for c in (files[:half], files[half:]) if c]):
            cols = 8 if len(files) > 8 else 3
            tw, th = (175, 300) if len(files) > 8 else (420, 720)
            rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new('RGB', (cols * tw, rows * th), 'white')
            for j, p in enumerate(chunk):
                im = Image.open(p).convert('RGB').resize((tw - 6, th - 6))
                sheet.paste(im, ((j % cols) * tw + 3, (j // cols) * th + 3))
            sheet.save(os.path.join(out_dir, '_sheet-%d.png' % (k + 1)))
    print('[build_book_t_full_imagery] %d PNGs in %s' % (len(files), out_dir))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--only', default='')
    ap.add_argument('--png', default='')
    a = ap.parse_args()
    only = set(x for x in a.only.split(',') if x)
    specs = json.load(open(SPECS, encoding='utf-8'))
    cur_json = open(DECK, encoding='utf-8').read()
    g = json.loads(cur_json)
    cards = [n for n in g['nodes'] if n.get('category') in ('aces', 'courts', 'decans', 'keys')]
    if len(cards) != 78:
        raise SystemExit('expected 78 cards, found %d' % len(cards))
    missing = [n['id'] for n in cards if n['id'] not in specs and (not only or n['id'] in only)]
    if missing:
        raise SystemExit('no composition for: %s (tarot/book-t/full-imagery/compositions.json)' % ', '.join(missing))
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
        print('[build_book_t_full_imagery] --check: %s' % ('up to date (78 cards)' if ok else
              'out of date (%d pictures%s); run: python scripts/build_book_t_full_imagery.py'
              % (len(stale), ', the grammar' if grammar_stale else '')))
        sys.exit(0 if ok else 1)
    if grammar_stale:
        with open(DECK, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(out_json)
    print('[build_book_t_full_imagery] %d pictures written%s' % (len(stale), ', grammar updated' if grammar_stale else ''))
    if a.png:
        render_pngs(done, a.png)


if __name__ == '__main__':
    main()
