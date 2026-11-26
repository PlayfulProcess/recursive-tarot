#!/usr/bin/env python3
"""Build the print files of "Book T: The Golden Dawn's Own Cards" for The Game Crafter (TGC tarot,
70 x 121 mm: 900 x 1500 px with the 1/8 in bleed, trim 825 x 1425, safe 750 x 1350), 80 faces + a back.

Faces 1-78 are the official Book T pictures (`tarot/book-t/painted-symbols/`), in Book T's own order
(the grammar's node order, `metadata.number` 1-78), composed by the same code as the site
(`build_book_t_painted_symbols.card_svg`), with three print changes:
  * the painting is embedded at 900 px (the site embeds 600 px) from the same URL;
  * a card whose illustrations hold a "Book T deck, painting — print version" entry (Key 15 today)
    uses that painting instead of the site's;
  * the outer band has square corners (TGC cuts its own rounded corners).
The 560 x 1030 card is rendered to 734 x 1350, centred in the safe area, and the band's own edge
pixels are extended outwards to the bleed, so the cut lands on plain band colour.
Card 79 is a colophon (all credits live there: never on a face) and card 80 a QR card to the deck in
recursive.eco Play, both drawn in the same frame. The back is 180-degree symmetric by construction
(Book T reads no reversals; the back must not tell which way up a card lies).

Output (gitignored, print/decks/ is kept out of git):
  print/decks/book-t-tgc/faces/NN-<id>.png   80 faces, upload order = file order
  print/decks/book-t-tgc/back.png
Kept in git, like print/conver-proof/: print/book-t-proof/{colophon,qr,back}-900x1500.png

  python scripts/build_book_t_tgc.py                 # build everything + check the safe area
  python scripts/build_book_t_tgc.py --sheet DIR     # also write a contact sheet into DIR
Upload with scripts/tgc_upload_deck.py; nothing here talks to TGC. Uploaded Oct 28 2026 (private, public=0):
  game "Book T: The Golden Dawn's Own Cards"  C07782A2-645A-11F1-87B8-CDFD42BF08F6 (was "Golden Dawn Tarot")
  deck                                        B755CF42-D2E3-11F1-BBED-F8EC8DFE9D6C (80 faces + back)
  python scripts/tgc_upload_deck.py --game C07782A2-645A-11F1-87B8-CDFD42BF08F6       --deck B755CF42-D2E3-11F1-BBED-F8EC8DFE9D6C --cards print/decks/book-t-tgc/faces --back print/decks/book-t-tgc/back.png
  python scripts/tgc_list_decks.py --game C07782A2-645A-11F1-87B8-CDFD42BF08F6
Proofing, ordering and publishing are the owner's steps in TGC's own pages; no script here does them.
"""
import argparse, io, json, os, re, shutil, sys
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_book_t_painted_symbols as ps  # noqa: E402
import resvg_py  # noqa: E402

ROOT = ps.ROOT
OUT = os.path.join(ROOT, 'print', 'decks', 'book-t-tgc')
FACES = os.path.join(OUT, 'faces')
CACHE = os.path.join(OUT, '_paintings')
KEEP = os.path.join(ROOT, 'print', 'book-t-proof')

TW, TH = 900, 1500
TRIM = (37, 37, 863, 1463)        # 1/8 in bleed = 37.5 px
SAFE = (75, 75, 825, 1425)        # 1/4 in from the edge
CW, CH = 734, 1350                # the 560 x 1030 card, scaled into the safe area
CX0, CY0 = (TW - CW) // 2, (TH - CH) // 2
PRINT_EDITION = 'Book T deck, painting — print version'
PRINT_EMBED_W = 900

DECK_TITLE = "Book T: The Golden Dawn's Own Cards"
PLAY_URL = 'https://recursive.eco/play?id=2000ad96-70c6-4aa4-a6fb-c22cce5e9cc7'
# a deep band for the two cards of our own, in the range the paintings' bands take
OWN_TOP, OWN_BOT = '#251c38', '#191427'
W, H = ps.W, ps.H
GOLD, GOLD_LIGHT, CREAM, SERIF = ps.GOLD, ps.GOLD_LIGHT, ps.CREAM, ps.SERIF


# ── faces 1-78 ──────────────────────────────────────────────────────────────────────────────────

def print_painting(node):
    for i in node['metadata'].get('illustrations') or []:
        if (i.get('edition') or '') == PRINT_EDITION:
            return i['url']
    return ps.painting_url(node)


def embed_print(url):
    """(data URI, top, bottom) at PRINT_EMBED_W, cached by URL so a re-run is offline."""
    os.makedirs(CACHE, exist_ok=True)
    key = re.sub(r'[^A-Za-z0-9._-]', '_', url.split('//', 1)[-1])[-120:]
    jp, meta = os.path.join(CACHE, key + '.jpg'), os.path.join(CACHE, key + '.json')
    if not (os.path.exists(jp) and os.path.exists(meta)):
        im = Image.open(io.BytesIO(ps.fetch(url))).convert('RGB')
        w, h = im.size
        top = ps.band_colour(im.crop((w // 12, h // 16, w - w // 12, h // 5)))
        bot = ps.band_colour(im.crop((w // 12, h - h // 5, w - w // 12, h - h // 16)))
        im.resize((PRINT_EMBED_W, round(h * PRINT_EMBED_W / w)), Image.LANCZOS).save(jp, 'JPEG', quality=92)
        json.dump({'url': url, 'top': top, 'bottom': bot}, open(meta, 'w'))
    m = json.load(open(meta))
    import base64
    data = 'data:image/jpeg;base64,' + base64.b64encode(open(jp, 'rb').read()).decode('ascii')
    return data, m['top'], m['bottom']


def face_svg(node):
    url = print_painting(node)
    data, top, bot = embed_print(url)
    site = ps.reuse(os.path.join(ps.OUT, node['id'] + '.svg'), url)
    if site:  # same painting as the site: keep the site's band colours exactly
        top, bot = site[1], site[2]
    return square(ps.card_svg(node, url, data, top, bot))


def square(svg):
    s = svg.replace('<rect width="%d" height="%d" rx="20" fill="url(#band)"/>' % (W, H),
                    '<rect width="%d" height="%d" fill="url(#band)"/>' % (W, H))
    if s == svg:
        raise SystemExit('band rect not found: card_svg changed, update square()')
    return s


def to_print(svg):
    """560 x 1030 SVG -> 900 x 1500 RGB: card in the safe area, edges extended to the bleed."""
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg, width=CW * 2))
    card = Image.open(io.BytesIO(png)).convert('RGB').resize((CW, CH), Image.LANCZOS)
    a = np.asarray(card)
    a = np.pad(a, ((CY0, TH - CH - CY0), (CX0, TW - CW - CX0), (0, 0)), mode='edge')
    return Image.fromarray(a)


# ── cards 79 and 80 ─────────────────────────────────────────────────────────────────────────────

def frame(body, top=OWN_TOP, bot=OWN_BOT, title=''):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
            '<title>%s</title><defs><linearGradient id="band" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
            '<rect width="%d" height="%d" fill="url(#band)"/>'
            '<rect x="9" y="9" width="%d" height="%d" rx="14" fill="none" stroke="%s" stroke-width="2.5"/>'
            '<rect x="16" y="16" width="%d" height="%d" rx="10" fill="none" stroke="%s" stroke-width="1" opacity=".55"/>'
            '%s</svg>' % (W, H, W, H, escape(title), top, bot, W, H, W - 18, H - 18, GOLD, W - 32, H - 32, GOLD, body))


def t(y, s, size, color=CREAM, italic=False, weight='normal', spacing=0):
    return ('<text x="%s" y="%s" text-anchor="middle" font-family="%s" font-size="%s" fill="%s"%s%s%s>%s</text>'
            % (W / 2, y, SERIF, size, color, ' font-style="italic"' if italic else '',
               ' font-weight="bold"' if weight == 'bold' else '',
               ' letter-spacing="%s"' % spacing if spacing else '', escape(s)))


def rule(y, half=70):
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.5"/>'
            '<circle cx="%s" cy="%s" r="3" fill="%s"/>' % (W / 2 - half, y, W / 2 + half, y, GOLD, W / 2, y, GOLD))


def spiral_logo(cx, cy, size, color=GOLD_LIGHT):
    """The site's spiral mark (public/recursive-logo.svg), recoloured to the deck's gold."""
    src = open(os.path.join(ROOT, 'public', 'recursive-logo.svg'), encoding='utf-8').read()
    d = re.search(r' d="([^"]+)"', src).group(1)
    s = size / 100.0
    return ('<g transform="translate(%s %s) scale(%s)"><path d="%s" stroke="%s" stroke-width="3.2" fill="none" '
            'stroke-linecap="round"/></g>' % (cx - size / 2, cy - size / 2, s, d, color))


def painters(cards):
    seen = []
    for n in cards:
        p = ps.painter(n)
        if p not in seen:
            seen.append(p)
    return seen


def colophon_svg(cards):
    models = ', '.join(painters(cards))
    lines = [
        (150, 'COLOPHON', 15, GOLD_LIGHT, False, 'normal', 3),
        (205, 'Book T', 46, CREAM, False, 'normal', 0),
        (243, "The Golden Dawn's Own Cards", 24, CREAM, True, 'normal', 0),
    ]
    body = ''.join(t(*l) for l in lines) + rule(275)
    paras = [
        ('The text', ["Book T, the Golden Dawn's tarot", 'manuscript, as printed in The Equinox', 'I(8), 1912. Public domain.']),
        ('The paintings', ["AI-assisted, painted from Book T's own", 'words; prompts by PlayfulProcess.', 'Models: ' + models.split(', ')[0] + ',',
                           ', '.join(models.split(', ')[1:]) + '.']),
        ('The frames', ['Glyphs of planets, signs, elements and', 'Hebrew letters drawn for this deck,', 'set where Book T places them.']),
        ('The order', ["Book T's own: four Aces, sixteen courts,", 'thirty-six small cards from Leo,', 'twenty-two Keys. No reversals.']),
    ]
    y = 325
    for head, ls in paras:
        body += t(y, head, 17, GOLD_LIGHT, True)
        y += 26
        for ln in ls:
            body += t(y, ln, 17)
            y += 23
        y += 16
    body += rule(y + 2)
    y += 40
    body += t(y, 'Prompts, glyphs and design: PlayfulProcess.', 16)
    body += t(y + 22, 'Licensed CC BY-SA 4.0: share and adapt', 16)
    body += t(y + 44, 'with credit, under the same licence.', 16)
    body += t(930, 'tarot.recursive.eco', 24, GOLD_LIGHT, spacing=.5)
    body += spiral_logo(W / 2, 985, 42)
    return frame(body, title='Colophon')


def qr_svg():
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    qr.add_data(PLAY_URL)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)
    side = 330.0
    cell = side / n
    x0, y0 = (W - side) / 2, 420
    pad = cell * 4  # the quiet zone: four modules of cream
    d = ''.join('M%.3f %.3fh%.3fv%.3fh-%.3fz' % (x0 + c * cell, y0 + r * cell, cell, cell, cell)
                for r in range(n) for c in range(n) if m[r][c])
    body = (t(200, 'Book T', 46) + t(238, "The Golden Dawn's Own Cards", 22, CREAM, True) + rule(272)
            + spiral_logo(W / 2, 325, 50)
            + '<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s"/>' % (
                x0 - pad, y0 - pad, side + 2 * pad, side + 2 * pad, CREAM)
            + '<path d="%s" fill="#1a1426" shape-rendering="crispEdges"/>' % d
            + t(y0 + side + pad + 70, 'Read with this deck, free', 30, GOLD_LIGHT, True))
    return frame(body, title='Read with this deck')


# ── the back ────────────────────────────────────────────────────────────────────────────────────

def back_svg():
    """Drawn at print size (900 x 1500). Every element is symmetric under a half turn about the centre,
    and the raster is then forced to exact point symmetry (bottom half = top half turned)."""
    cx, cy = TW / 2, TH / 2
    g = []
    g.append('<defs><radialGradient id="bg" cx="50%%" cy="50%%" r="65%%"><stop offset="0" stop-color="#2e2347"/>'
             '<stop offset="1" stop-color="#171223"/></radialGradient>'
             '<pattern id="lat" width="60" height="60" patternUnits="userSpaceOnUse" x="%s" y="%s">'
             '<path d="M30 0L60 30L30 60L0 30Z" fill="none" stroke="%s" stroke-width="1" opacity=".22"/>'
             '<circle cx="30" cy="30" r="1.6" fill="%s" opacity=".45"/></pattern></defs>' % (cx - 30, cy - 30, GOLD, GOLD))
    g.append('<rect width="%d" height="%d" fill="url(#bg)"/>' % (TW, TH))
    m = 96  # the frame sits inside the safe area (75)
    g.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#lat)"/>' % (m + 22, m + 22, TW - 2 * m - 44, TH - 2 * m - 44))
    g.append('<rect x="%d" y="%d" width="%d" height="%d" rx="18" fill="none" stroke="%s" stroke-width="4"/>' % (m, m, TW - 2 * m, TH - 2 * m, GOLD))
    g.append('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="none" stroke="%s" stroke-width="1.5" opacity=".7"/>'
             % (m + 12, m + 12, TW - 2 * m - 24, TH - 2 * m - 24, GOLD))
    # corner rosettes (four corners: the set is symmetric under a half turn and both mirrors)
    for x in (m + 12, TW - m - 12):
        for y in (m + 12, TH - m - 12):
            g.append('<circle cx="%s" cy="%s" r="16" fill="#1c1629" stroke="%s" stroke-width="2"/>'
                     '<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (x, y, GOLD, x, y, GOLD_LIGHT))
    # the centre: a dark medallion, twelve dots (the signs), a hexagram, a rose of eight petals
    R = 250
    g.append('<circle cx="%s" cy="%s" r="%s" fill="#1a1426" stroke="%s" stroke-width="4"/>' % (cx, cy, R, GOLD))
    g.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="1.5" opacity=".7"/>' % (cx, cy, R - 14, GOLD))
    import math
    for k in range(12):
        a = math.pi / 12 + k * math.pi / 6
        g.append('<circle cx="%.2f" cy="%.2f" r="5" fill="%s"/>' % (cx + (R - 34) * math.cos(a), cy + (R - 34) * math.sin(a), GOLD_LIGHT))
    r = R - 62
    for up in (True, False):
        s = -1 if up else 1
        pts = [(cx + r * math.cos(math.radians(a)), cy + s * r * math.sin(math.radians(a))) for a in (-90, 30, 150)]
        g.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round"/>'
                 % (' '.join('%.2f,%.2f' % p for p in pts), GOLD))
    g.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="2"/>' % (cx, cy, r / 2, GOLD))
    for k in range(8):
        a = k * 45
        g.append('<ellipse cx="%s" cy="%s" rx="13" ry="38" fill="%s" opacity=".85" transform="rotate(%d %s %s) translate(0 -40)"/>'
                 % (cx, cy, '#b5473f' if k % 2 == 0 else '#8e2f3a', a, cx, cy))
    g.append('<circle cx="%s" cy="%s" r="16" fill="%s"/>' % (cx, cy, GOLD_LIGHT))
    # above and below the medallion: a column of lozenges, the same both ways
    for s in (-1, 1):
        for i, (dy, rr) in enumerate(((R + 60, 22), (R + 130, 15), (R + 185, 10), (R + 225, 6))):
            y = cy + s * dy
            g.append('<path d="M%s %sL%s %sL%s %sL%s %sZ" fill="%s" stroke="%s" stroke-width="2"/>'
                     % (cx, y - rr * 1.6, cx + rr, y, cx, y + rr * 1.6, cx - rr, y, '#1a1426', GOLD))
        g.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.5" opacity=".7"/>'
                 % (cx - 120, cy + s * (R + 95), cx + 120, cy + s * (R + 95), GOLD))
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>' % (TW, TH, TW, TH, ''.join(g))


def render_back():
    png = bytes(resvg_py.svg_to_bytes(svg_string=back_svg(), width=TW))
    im = Image.open(io.BytesIO(png)).convert('RGB')
    top = im.crop((0, 0, TW, TH // 2))
    im.paste(top.rotate(180), (0, TH // 2))
    from PIL import ImageChops
    assert ImageChops.difference(im, im.rotate(180)).getbbox() is None, 'back is not point-symmetric'
    return im


# ── checks + contact sheet ──────────────────────────────────────────────────────────────────────

def safe_check(im, kind):
    """Nothing but plain colour outside the safe area: the band (faces) or the back's ground. Returns
    a list of problems. On the faces the band is dark and every glyph, line and letter is light, so a
    light pixel outside the safe area is clipped content."""
    a = np.asarray(im).astype(int)
    lum = a.mean(axis=2)
    x0, y0, x1, y1 = SAFE
    out = np.ones(lum.shape, bool)
    out[y0:y1, x0:x1] = False
    probs = []
    if lum[out].max() > 110:
        ys, xs = np.nonzero(out & (lum > 110))
        probs.append('%d light pixels outside the safe area (first at %d,%d)' % (len(xs), xs[0], ys[0]))
    if kind == 'face':
        # the band itself must not change along an extended edge row/column (pure extension)
        if not (a[:CY0, CX0:CX0 + CW] == a[CY0:CY0 + 1, CX0:CX0 + CW]).all():
            probs.append('top bleed is not a pure edge extension')
    return probs


def contact_sheet(files, back, out_path):
    tw, th = 150, 250
    cols = 9
    n = len(files) + 1
    rows = (n + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (tw + 10) + 10, rows * (th + 30) + 10), '#f4f1ea')
    d = ImageDraw.Draw(sheet)
    sx, sy = tw / TW, th / TH
    for k, (label, p) in enumerate(list(files) + [('back', back)]):
        x = 10 + (k % cols) * (tw + 10)
        y = 10 + (k // cols) * (th + 30)
        im = Image.open(p).convert('RGB').resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (x, y))
        # the trim (red) and the safe area (cyan), as TGC's overlay draws them
        d.rectangle([x + TRIM[0] * sx, y + TRIM[1] * sy, x + TRIM[2] * sx, y + TRIM[3] * sy], outline='#d33')
        d.rectangle([x + SAFE[0] * sx, y + SAFE[1] * sy, x + SAFE[2] * sx, y + SAFE[3] * sy], outline='#2ab')
        d.text((x, y + th + 4), label[:26], fill='#222')
    sheet.save(out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sheet', default='', help='write the contact sheet here')
    ap.add_argument('--keep-faces', action='store_true', help='reuse faces 1-78 already built (slow to render)')
    a = ap.parse_args()
    g = json.load(open(ps.DECK, encoding='utf-8'))
    cards = [n for n in g['nodes'] if n.get('category') in ('aces', 'courts', 'decans', 'keys')]
    if len(cards) != 78:
        raise SystemExit('expected 78 cards, found %d' % len(cards))
    if not a.keep_faces:
        shutil.rmtree(FACES, ignore_errors=True)
    os.makedirs(FACES, exist_ok=True)
    os.makedirs(KEEP, exist_ok=True)
    made, problems = [], []
    for i, n in enumerate(cards, 1):
        p = os.path.join(FACES, '%02d-%s.png' % (i, n['id']))
        if a.keep_faces and os.path.exists(p):
            im = Image.open(p).convert('RGB')
        else:
            im = to_print(face_svg(n))
            im.save(p, 'PNG', optimize=True)
        made.append(('%02d %s' % (i, n['id']), p))
        problems += ['%s: %s' % (n['id'], x) for x in safe_check(im, 'face')]
        print('  %02d %s' % (i, n['id']), flush=True)
    for i, (slug, svg) in enumerate((('colophon', colophon_svg(cards)), ('qr', qr_svg())), 79):
        im = to_print(svg)
        keep = os.path.join(KEEP, '%s-900x1500.png' % slug)
        im.save(keep, 'PNG', optimize=True)
        p = os.path.join(FACES, '%02d-%s.png' % (i, slug))
        shutil.copyfile(keep, p)
        made.append(('%02d %s' % (i, slug), p))
        problems += ['%s: %s' % (slug, x) for x in safe_check(im, 'face')]
    back = render_back()
    bk = os.path.join(KEEP, 'back-900x1500.png')
    back.save(bk, 'PNG', optimize=True)
    shutil.copyfile(bk, os.path.join(OUT, 'back.png'))
    problems += ['back: %s' % x for x in safe_check(back, 'back')]
    print('[build_book_t_tgc] %d faces + back in %s' % (len(made), OUT))
    if a.sheet:
        os.makedirs(a.sheet, exist_ok=True)
        contact_sheet(made, bk, os.path.join(a.sheet, 'contact-sheet.png'))
        print('[build_book_t_tgc] contact sheet: %s' % os.path.join(a.sheet, 'contact-sheet.png'))
    if problems:
        print('SAFE-AREA PROBLEMS:\n  ' + '\n  '.join(problems))
        sys.exit(1)
    print('[build_book_t_tgc] safe area: all 81 images clean (nothing light outside 750 x 1350)')


if __name__ == '__main__':
    main()
