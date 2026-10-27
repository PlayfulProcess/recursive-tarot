#!/usr/bin/env python3
"""Build Book T's painted-with-its-symbols set: the painting, framed by the card's symbolic system.

  python scripts/build_book_t_painted_symbols.py            # write tarot/book-t/painted-symbols/*.svg + the grammar's entries
  python scripts/build_book_t_painted_symbols.py --check    # write nothing; exit 1 if anything is out of date
  python scripts/build_book_t_painted_symbols.py --only wands-05,key-17-star --png DIR   # samples, rendered to PNG

Her words (Oct 20 2026): "Couldn't we mix up the images that Gemini did with the symbolic system and
render the best of our worlds in SVG?"

* The picture is the card's painting (the first `metadata.illustrations` entry whose edition names a
  painting or the composite: the AI paintings from Book T's words, as corrected where she corrected
  them). It sits whole in a window, never covered: the symbols live in the frame around it.
* The symbols are the iconography's (scripts/build_book_t_iconography.py: the same glyphs from
  `tarot/book-t/glyphs/`, Book T's decan order, its Tetragrammaton letter, its court degrees via
  `text_degree`), set in gold on a band whose colour is sampled from the painting's own top and bottom
  edges, with a soft shadow so they read on any painting:
    top band     the planet (decans; or the sign when Book T names the sign first), the element of the
                 element (courts), the element (aces), the attribution (Keys); the card's letter at
                 the left (Keys: the numeral), the suit's element at the right (Keys: the Path)
    bottom band  the sign (decans), the signs a court rules from and to with Book T's degrees, the
                 letter of the Name (aces), the Hebrew letter (Keys); then the title and the line
                 "card · decan · sephirah"
* Why the painting's pixels are inside the SVG (a JPEG data URI, 600 px wide) and not an <image>
  pointing at R2: browsers draw an SVG shown with <img> in "secure static mode", which never loads an
  external file, so a linked painting comes out as a broken image on every page and in Play (tested
  Oct 20 2026 in Edge: <img> broken, <object> fine). Each SVG records the painting's URL in
  `data-painting` and its <desc>; a re-run reuses the embedded JPEG while that URL is unchanged, so
  `--check` needs no network.
* Output: `tarot/book-t/painted-symbols/<card id>.svg`, served at
  https://tarot.recursive.eco/tarot/book-t/painted-symbols/<card id>.svg, and one entry per card in
  `metadata.illustrations` with `edition: "Book T deck, painted with its symbols"` (the 1912 page's
  Pictures switch: **Painted + symbols**). Since Oct 21 2026 this is Book T's OFFICIAL picture: the entry
  is first, `is_primary`, and the node's `image_url` (see with_illustration).
"""
import argparse, base64, colorsys, io, json, os, re, subprocess, sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_book_t_iconography as ico  # noqa: E402  (the glyphs, Book T's decan order, text_degree)

ROOT = ico.ROOT
DECK = ico.DECK
OUT = os.path.join(ROOT, 'tarot', 'book-t', 'painted-symbols')
URL = 'https://tarot.recursive.eco/tarot/book-t/painted-symbols/%s.svg'
EDITION = 'Book T deck, painted with its symbols'
ARTIST = ("AI painting (gemini-2.5-flash-image) from Book T's words, prompt by PlayfulProcess, framed by "
          "the deck's glyphs (drawn for this site) in Book T's order, composed by script "
          "(scripts/build_book_t_painted_symbols.py)")
f = ico.f

W, H = 560, 1030
CX = W / 2
# the painting's window (2:3, as the paintings are)
PX, PY, PW, PH = 34, 112, 492, 738
GOLD = '#d8b25c'
GOLD_LIGHT = '#f3d78a'
CREAM = '#f5ead0'
SERIF = "Georgia, 'Times New Roman', serif"
EMBED_W = 600  # the embedded painting's width in pixels


# ── the painting ────────────────────────────────────────────────────────────────────────────────

def painting_url(node):
    for i in (node['metadata'].get('illustrations') or []):
        e = i.get('edition') or ''
        if e != EDITION and ('painting' in e or 'composite' in e):
            return i['url']
    raise SystemExit('%s: no painting among its illustrations' % node['id'])


def fetch(url):
    # R2 refuses Python's default user agent; curl is everywhere the scripts run.
    r = subprocess.run(['curl', '-sfL', url], capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit('could not fetch %s' % url)
    return r.stdout


def band_colour(im):
    """A deep colour for the frame, sampled from an edge strip of the painting: its mean hue, kept
    rich but dark enough that gold reads on it."""
    q = im.resize((64, 32)).quantize(4)  # the strip's dominant colour, not its muddy mean
    pal = q.getpalette()
    k = max(q.getcolors(), key=lambda c: c[0])[1]
    small = pal[3 * k:3 * k + 3]
    h, l, s = colorsys.rgb_to_hls(*[c / 255.0 for c in small[:3]])
    l = 0.17
    s = min(max(s, 0.25), 0.55)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))


def embed(url):
    """(data URI, top colour, bottom colour) of the painting, downscaled to EMBED_W."""
    from PIL import Image
    im = Image.open(io.BytesIO(fetch(url))).convert('RGB')
    w, h = im.size
    # a strip just inside each edge, past any border the painting drew round itself
    top = band_colour(im.crop((w // 12, h // 16, w - w // 12, h // 5)))
    bot = band_colour(im.crop((w // 12, h - h // 5, w - w // 12, h - h // 16)))
    im = im.resize((EMBED_W, round(h * EMBED_W / w)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=80, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode('ascii'), top, bot


def reuse(path, url):
    """The embedded painting and colours of an existing SVG, when it was made from the same URL."""
    if not os.path.exists(path):
        return None
    s = open(path, encoding='utf-8').read()
    m = re.search(r'data-painting="([^"]*)" data-top="(#[0-9a-f]{6})" data-bottom="(#[0-9a-f]{6})"', s)
    d = re.search(r'href="(data:image/jpeg;base64,[^"]+)"', s)
    if m and d and m.group(1) == escape(url):
        return d.group(1), m.group(2), m.group(3)
    return None


# ── the frame's pieces ──────────────────────────────────────────────────────────────────────────

def g_glyph(name, cx, cy, size, color=GOLD_LIGHT):
    return '<g filter="url(#sh)">%s</g>' % ico.glyph(name, cx, cy, size, color)


def medallion(cx, cy, r, fill):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="2.5"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="1" opacity=".6"/>'
            % (f(cx), f(cy), f(r), fill, GOLD, f(cx), f(cy), f(r - 5), GOLD))


def cartouche(cx, cy, w, h, fill):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="2.5"/>'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="1" opacity=".6"/>'
            % (f(cx - w / 2), f(cy - h / 2), f(w), f(h), f(h / 2), fill, GOLD,
               f(cx - w / 2 + 5), f(cy - h / 2 + 5), f(w - 10), f(h - 10), f((h - 10) / 2), GOLD))


def rule(y, x0, x1):
    """A gold rule with a small diamond at each end."""
    d = lambda x: ('<path d="M%s %s l5 -5 l5 5 l-5 5 Z" fill="%s"/>' % (f(x - 5), f(y), GOLD))
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.5" opacity=".85"/>%s%s'
            % (f(x0), f(y), f(x1), f(y), GOLD, d(x0), d(x1)))


def text(x, y, s, size, color=CREAM, italic=False, anchor='middle', spacing=0):
    return ('<text x="%s" y="%s" font-size="%s" text-anchor="%s" fill="%s" font-family="%s"%s%s filter="url(#sh)">%s</text>'
            % (f(x), f(y), f(size), anchor, color, SERIF, ' font-style="italic"' if italic else '',
               (' letter-spacing="%s"' % spacing) if spacing else '', escape(s)))


def fit(s, width_px, base):
    """A font size at which `s` fits in width_px (Georgia averages about 0.5 em a character)."""
    return min(base, max(15, width_px / (0.5 * max(1, len(s)))))


def title_lines(name):
    if len(name) <= 30:
        return [name], ''
    for sep in (': ', '; ', ', '):
        if sep in name:
            a, b = name.split(sep, 1)
            return [a], b[0].upper() + b[1:]
    return [name], ''


# ── a card ──────────────────────────────────────────────────────────────────────────────────────

TOP_Y = 62       # the top band's centre line
SIGN_Y = 898     # the bottom medallion's centre
SIDE_L, SIDE_R = 84, W - 84


def symbols(node, top_fill, bot_fill):
    """The top band, the bottom medallion row, the subtitle and a plain description."""
    m = node['metadata']
    cat = node['category']
    out, desc = [], []
    if cat == 'keys':
        letter = ico.HEBREW[m['hebrew_letter']]
        attrs = [a.strip() for a in re.split(r'\band\b', m['attribution'])]
        if len(attrs) == 1:
            out.append(rule(TOP_Y, 130, W - 130))
            out.append(medallion(CX, TOP_Y, 40, top_fill) + g_glyph(attrs[0], CX, TOP_Y, 52))
        else:
            out.append(rule(TOP_Y, 130, W - 130))
            out.append(cartouche(CX, TOP_Y, 150, 80, top_fill))
            out.append(g_glyph(attrs[0], CX - 36, TOP_Y, 44) + g_glyph(attrs[1], CX + 36, TOP_Y, 44))
        out.append(text(SIDE_L, TOP_Y + 11, ico.ROMAN[m['key_number']], 30, GOLD_LIGHT))
        out.append(text(SIDE_R, TOP_Y - 4, 'Path', 14, GOLD_LIGHT, True))
        out.append(text(SIDE_R, TOP_Y + 20, str(m['tree_path']), 24, GOLD_LIGHT))
        out.append(medallion(CX, SIGN_Y, 34, bot_fill) + g_glyph(letter, CX, SIGN_Y, 44))
        out.append(text(CX - 52, SIGN_Y + 7, m['hebrew_translit'], 18, GOLD_LIGHT, True, 'end'))
        out.append(text(CX + 52, SIGN_Y + 7, m['attribution'], 18, GOLD_LIGHT, True, 'start'))
        sub = m['card_name_1912']
        desc.append('Above, %s, the Key\'s attribution; below, the letter %s (%s); Key %s, Path %d.'
                    % (m['attribution'], m['hebrew_translit'], m['hebrew_letter'], ico.ROMAN[m['key_number']], m['tree_path']))
        return out, sub, desc
    el = m['element']
    letter = ico.RANK_LETTER[m['rank']] if cat == 'courts' else ico.tetragrammaton(node)
    out.append(rule(TOP_Y, 130, W - 130))
    out.append(g_glyph(letter, SIDE_L, TOP_Y, 44))
    out.append(g_glyph(el, SIDE_R, TOP_Y, 40))
    if cat == 'decans':
        above, below, _, sentence = ico.decan_order(node)
        out.append(medallion(CX, TOP_Y, 40, top_fill) + g_glyph(above, CX, TOP_Y, 50))
        out.append(medallion(CX, SIGN_Y, 34, bot_fill) + g_glyph(below, CX, SIGN_Y, 42))
        sub = '%s · %s · %s' % (m['card_name_1912'], m['decan'], m['sephirah'])
        desc.append('%s above the painting and %s below, as Book T places them: "%s"' % (above, below, sentence))
    elif cat == 'aces':
        out.append(medallion(CX, TOP_Y, 40, top_fill) + g_glyph(el, CX, TOP_Y, 48))
        out.append(medallion(CX, SIGN_Y, 34, bot_fill) + g_glyph(ico.SUIT_LETTER[m['suit']], CX, SIGN_Y, 40))
        sub = '%s · the Root · %s' % (m['card_name_1912'], m['sephirah'])
        desc.append('The root of %s: its element above, its letter of the Name below.' % el)
    else:  # courts
        sub_el, of_el = [x.strip() for x in m['element_in_element'].split(' of ')]
        out.append(cartouche(CX, TOP_Y, 168, 80, top_fill))
        out.append(g_glyph(sub_el, CX - 46, TOP_Y, 42))
        out.append(text(CX, TOP_Y + 7, 'of', 18, GOLD_LIGHT, True))
        out.append(g_glyph(of_el, CX + 46, TOP_Y, 42))
        rm = re.match(r'\s*(\d+)\D+?([A-Z][a-z]+)\s*\W+\s*(\d+)\D+?([A-Z][a-z]+)', m.get('rules', ''))
        if rm:
            _, s1, _, s2 = rm.groups()
            d1, d2 = ico.text_degree(node, s1), ico.text_degree(node, s2)
            out.append(cartouche(CX, SIGN_Y, 236, 64, bot_fill))
            out.append(text(CX - 98, SIGN_Y + 6, '%s°' % d1, 17, GOLD_LIGHT, False, 'start'))
            out.append(g_glyph(s1, CX - 40, SIGN_Y, 36))
            out.append('<path d="M%s %s L%s %s M%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/>'
                       % (f(CX - 12), f(SIGN_Y), f(CX + 12), f(SIGN_Y), f(CX + 6), f(SIGN_Y - 6), f(CX + 12), f(SIGN_Y),
                          f(CX + 6), f(SIGN_Y + 6), GOLD))
            out.append(g_glyph(s2, CX + 40, SIGN_Y, 36))
            out.append(text(CX + 98, SIGN_Y + 6, '%s°' % d2, 17, GOLD_LIGHT, False, 'end'))
            desc.append('%s; rules from %s° %s to %s° %s, as Book T counts.' % (m['element_in_element'], d1, s1, d2, s2))
        else:
            # The Princesses rule a quadrant of the heavens around the North Pole.
            out.append(medallion(CX, SIGN_Y, 34, bot_fill))
            out.append('<g filter="url(#sh)" fill="none" stroke="%s" stroke-width="2.5"><path d="M%s %s L%s %s A36 36 0 0 1 %s %s Z" fill="%s" fill-opacity=".25"/>'
                       '<circle cx="%s" cy="%s" r="3" fill="%s"/></g>'
                       % (GOLD_LIGHT, f(CX - 16), f(SIGN_Y + 16), f(CX - 16), f(SIGN_Y - 20), f(CX + 20), f(SIGN_Y + 16),
                          GOLD_LIGHT, f(CX - 16), f(SIGN_Y + 16), GOLD_LIGHT))
            out.append(text(CX + 46, SIGN_Y + 6, 'the Pole', 15, GOLD_LIGHT, True, 'start'))
            desc.append('%s; rules %s.' % (m['element_in_element'], m['rules']))
        sub = '%s · %s' % (m['card_name_1912'], m['element_in_element'])
    return out, sub, desc


def card_svg(node, url, data, top, bot):
    parts, sub, desc = symbols(node, top, bot)
    lines, second = title_lines(node['name'])
    tw = W - 90
    if second:
        cap = (text(CX, 960, lines[0], fit(lines[0], tw, 26)) +
               text(CX, 983, second, fit(second, tw, 17), CREAM, True))
    else:
        cap = text(CX, 968, lines[0], fit(lines[0], tw, 29))
    cap += text(CX, 1004 if second else 996, sub, fit(sub, tw, 15), GOLD_LIGHT, True, spacing=.3)
    title = '%s: %s (Book T deck, painted with its symbols)' % (node['name'], sub)
    head = (
        '<defs>'
        '<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
        '<filter id="sh" x="-30%%" y="-30%%" width="160%%" height="160%%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.3" flood-color="#000" flood-opacity=".7"/></filter>'
        '<clipPath id="win"><rect x="%s" y="%s" width="%s" height="%s" rx="6"/></clipPath>'
        '</defs>'
        '<rect width="%d" height="%d" rx="20" fill="url(#band)"/>'
        '<rect x="9" y="9" width="%d" height="%d" rx="14" fill="none" stroke="%s" stroke-width="2.5"/>'
        '<rect x="16" y="16" width="%d" height="%d" rx="10" fill="none" stroke="%s" stroke-width="1" opacity=".55"/>'
        '<image href="%s" x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="xMidYMid slice" clip-path="url(#win)"/>'
        '<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" stroke="%s" stroke-width="3"/>'
        '<rect x="%s" y="%s" width="%s" height="%s" rx="9" fill="none" stroke="%s" stroke-width="1" opacity=".6"/>'
        % (top, bot, f(PX), f(PY), f(PW), f(PH), W, H, W - 18, H - 18, GOLD, W - 32, H - 32, GOLD,
           data, f(PX), f(PY), f(PW), f(PH), f(PX), f(PY), f(PW), f(PH), GOLD,
           f(PX - 5), f(PY - 5), f(PW + 10), f(PH + 10), GOLD))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-labelledby="t d" '
            'data-painting="%s" data-top="%s" data-bottom="%s">\n'
            '<title id="t">%s</title>\n<desc id="d">%s The painting: %s (AI painting from Book T\'s words, prompt by PlayfulProcess, CC BY-SA 4.0). '
            'Glyphs drawn for recursive-tarot (CC BY-SA 4.0); composed by scripts/build_book_t_painted_symbols.py.</desc>\n'
            '%s\n%s\n%s\n</svg>\n'
            % (W, H, W, H, escape(url), top, bot, escape(title), escape(' '.join(desc)), escape(url),
               head, '\n'.join(parts), cap))


# ── the grammar ─────────────────────────────────────────────────────────────────────────────────

def with_illustration(node):
    """The official picture (her words, Oct 21 2026: "let's make these cards the official ones"): this
    set's entry goes first in `metadata.illustrations`, carries `is_primary`, and is the node's
    `image_url`. The other sets stay in the list, in their order, one tap away."""
    m = node['metadata']
    entry = {'url': URL % node['id'], 'artist': ARTIST, 'edition': EDITION, 'license': 'CC-BY-SA-4.0',
             'is_primary': True}
    ills = [dict(i) for i in (m.get('illustrations') or []) if i.get('edition') != EDITION]
    for i in ills:
        i.pop('is_primary', None)
    m['illustrations'] = [entry] + ills
    node['image_url'] = entry['url']


def render_pngs(ids, out_dir):
    import resvg_py
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    files = []
    for i in ids:
        p = os.path.join(out_dir, i + '.png')
        png = resvg_py.svg_to_bytes(svg_path=os.path.join(OUT, i + '.svg'), width=560)
        open(p, 'wb').write(bytes(png))
        files.append(p)
    if len(files) > 1:
        cols = 8 if len(files) > 8 else 3
        tw, th = (175, 312) if len(files) > 8 else (420, 750)
        half = (len(files) + 1) // 2 if len(files) > 8 else len(files)
        for k, chunk in enumerate([c for c in (files[:half], files[half:]) if c]):
            rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new('RGB', (cols * tw, rows * th), 'white')
            for j, p in enumerate(chunk):
                im = Image.open(p).convert('RGB').resize((tw - 6, th - 6), Image.LANCZOS)
                sheet.paste(im, ((j % cols) * tw + 3, (j // cols) * th + 3))
            sheet.save(os.path.join(out_dir, '_sheet-%d.png' % (k + 1)))
    print('[build_book_t_painted_symbols] %d PNGs in %s' % (len(files), out_dir))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--only', default='')
    ap.add_argument('--png', default='')
    a = ap.parse_args()
    only = set(x for x in a.only.split(',') if x)
    cur_json = open(DECK, encoding='utf-8').read()
    g = json.loads(cur_json)
    cards = [n for n in g['nodes'] if n.get('category') in ('aces', 'courts', 'decans', 'keys')]
    if len(cards) != 78:
        raise SystemExit('expected 78 cards, found %d' % len(cards))
    stale, done = [], []
    if not a.check:
        os.makedirs(OUT, exist_ok=True)
    for n in cards:
        if only and n['id'] not in only:
            continue
        url = painting_url(n)
        p = os.path.join(OUT, n['id'] + '.svg')
        got = reuse(p, url)
        if not got:
            if a.check:
                stale.append(n['id'])
                continue
            got = embed(url)
        svg = card_svg(n, url, *got)
        old = open(p, encoding='utf-8').read() if os.path.exists(p) else None
        if old != svg:
            stale.append(n['id'])
            if not a.check:
                with open(p, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(svg)
        done.append(n['id'])
    if not only:
        for n in cards:
            with_illustration(n)
    out_json = json.dumps(g, ensure_ascii=False, indent=2) + '\n'
    grammar_stale = not only and out_json != cur_json
    if a.check:
        ok = not stale and not grammar_stale
        print('[build_book_t_painted_symbols] --check: %s' % ('up to date (78 cards)' if ok else
              'out of date (%d pictures%s); run: python scripts/build_book_t_painted_symbols.py'
              % (len(stale), ', the grammar' if grammar_stale else '')))
        sys.exit(0 if ok else 1)
    if grammar_stale:
        with open(DECK, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(out_json)
    print('[build_book_t_painted_symbols] %d pictures written%s' % (len(stale), ', grammar updated' if grammar_stale else ''))
    if a.png:
        render_pngs(done, a.png)


if __name__ == '__main__':
    main()
