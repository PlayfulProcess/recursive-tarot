#!/usr/bin/env python3
"""Build Book T's iconography: the deck's third picture set, glyphs composed onto each card.

  python scripts/build_book_t_iconography.py            # write tarot/book-t/iconography/*.svg + the grammar's entries
  python scripts/build_book_t_iconography.py --check    # write nothing; exit 1 if anything is out of date
  python scripts/build_book_t_iconography.py --only wands-05,swords-10   # write just these cards (samples)

Her words (Oct 19 2026): "the lord of strife has iconography like this: Above the middle wand is the
sign Saturn, and below is that of Leo ... That are not rendered in the cards ... render an iconography
as elements that goes into each card, like astro signs and Hebrew letters in SVG and ... a composition
in SVG as composed node."

* The parts are the glyph set in `tarot/book-t/glyphs/` (7 planets, 12 signs, 4 elements + Spirit, the
  22 Hebrew letters): drawn for this site as plain SVG strokes, CC BY-SA 4.0 like the deck (see the
  folder's README). Edit a glyph there, then re-run this script.
* What goes on a card comes from the card's own metadata in `tarot/book-t/grammar.json` (`planet`,
  `sign`, `element`, `element_in_element`, `rules`; the Keys' `hebrew_letter`, `attribution`,
  `tree_path`) and where it goes from Book T's own sentence for that card: the decan's planet and sign
  above and below the central symbol, in the order Book T names them (the Six of Pentacles names
  Taurus first, so Taurus is above), and on "small daggers" or "small wands" when Book T says so.
  The corner letter is the Tetragrammaton letter Book T gives the card ("Geburah of י").
* The central symbol is a schematic of the suit (wands, cups, swords, pentacles), counted as Book T
  counts them; the hands and clouds Book T describes are left to the painted pictures.
* Output: `tarot/book-t/iconography/<card id>.svg`, served by the site at
  https://tarot.recursive.eco/tarot/book-t/iconography/<card id>.svg, and one entry per card in
  `metadata.illustrations` with `edition: "Book T deck, iconography"`. That edition name is the
  picture set: recursive.eco's Play offers it in its Pictures choice, and pages/book-t.html's
  Pictures switch shows it (build_book_t_page.py reads it).
"""
import argparse, json, math, os, re, sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.path.join(ROOT, 'tarot', 'book-t', 'grammar.json')
GLYPHS = os.path.join(ROOT, 'tarot', 'book-t', 'glyphs')
OUT = os.path.join(ROOT, 'tarot', 'book-t', 'iconography')
URL = 'https://tarot.recursive.eco/tarot/book-t/iconography/%s.svg'
EDITION = 'Book T deck, iconography'
ARTIST = ("PlayfulProcess: glyphs drawn for this deck, composed by script (scripts/build_book_t_iconography.py) "
          "from the card's own metadata, placed as Book T (1912) places them")

W, H = 560, 960
CX = W / 2
INK = '#2b2118'
PAPER = '#fbf6ea'
MUTED = '#6b5d4a'

ELEMENT_COLOR = {'Fire': '#b0361f', 'Water': '#1d5c9c', 'Air': '#8f7110', 'Earth': '#3f6b2a', 'Spirit': '#5b3f8c'}
PLANET_COLOR = {'Saturn': '#2d2a5a', 'Jupiter': '#6a2f8a', 'Mars': '#b3261e', 'Sun': '#c0650a',
                'Venus': '#2f7d3a', 'Mercury': '#8f7110', 'Moon': '#2b5fa6'}
SIGN_COLOR = {'Aries': '#c0281c', 'Taurus': '#c4521a', 'Gemini': '#b8700f', 'Cancer': '#98780c', 'Leo': '#7c7c10',
              'Virgo': '#5e8a1e', 'Libra': '#1f7a46', 'Scorpio': '#1b6f6a', 'Sagittarius': '#1f4fa0',
              'Capricorn': '#2d2f7a', 'Aquarius': '#5b2f8a', 'Pisces': '#8a1f5a'}
SUIT_ELEMENT = {'Wands': 'Fire', 'Cups': 'Water', 'Swords': 'Air', 'Pentacles': 'Earth'}
# The Tetragrammaton letter of each suit (Book T: "Geburah of י") and of each court rank (Book T: "the
# horsed figures refer to the Yod of Tetragrammaton, the charioted figures to the Vau").
SUIT_LETTER = {'Wands': 'yod', 'Cups': 'heh', 'Swords': 'vau', 'Pentacles': 'heh'}
RANK_LETTER = {'Knight': 'yod', 'Queen': 'heh', 'Prince': 'vau', 'Princess': 'heh'}
HEBREW = {'א': 'aleph', 'ב': 'beth', 'ג': 'gimel', 'ד': 'daleth', 'ה': 'heh', 'ו': 'vau', 'ז': 'zain',
          'ח': 'cheth', 'ט': 'teth', 'י': 'yod', 'כ': 'kaph', 'ל': 'lamed', 'מ': 'mem', 'נ': 'nun',
          'ס': 'samekh', 'ע': 'ayin', 'פ': 'peh', 'צ': 'tzaddi', 'ק': 'qoph', 'ר': 'resh', 'ש': 'shin', 'ת': 'tau'}
ROMAN = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV',
         'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI']


# ── glyphs ──────────────────────────────────────────────────────────────────────────────────────

_cache = {}


def glyph_file(name):
    """'Saturn' → planet-saturn, 'Leo' → sign-leo, 'Fire' → element-fire, 'yod' → hebrew-yod."""
    n = name.lower()
    if n in (k.lower() for k in PLANET_COLOR):
        return 'planet-' + n
    if n in (k.lower() for k in SIGN_COLOR):
        return 'sign-' + n
    if n in (k.lower() for k in ELEMENT_COLOR):
        return 'element-' + n
    return 'hebrew-' + n


def glyph(name, cx, cy, size, color):
    key = glyph_file(name)
    if key not in _cache:
        s = open(os.path.join(GLYPHS, key + '.svg'), encoding='utf-8').read()
        m = re.search(r'<g id="glyph"([^>]*)>(.*?)</g>', s, re.S)
        if not m:
            raise SystemExit('glyph %s has no <g id="glyph">' % key)
        sw = re.search(r'stroke-width="([\d.]+)"', m.group(1)).group(1)
        _cache[key] = (sw, ''.join(line.strip() for line in m.group(2).splitlines()))
    sw, body = _cache[key]
    k = size / 100.0
    return ('<g transform="translate(%s %s) scale(%s)" style="color:%s" fill="none" stroke="currentColor" '
            'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" data-glyph="%s">%s</g>'
            % (f(cx - size / 2), f(cy - size / 2), f(k), color, sw, key, body))


def f(x):
    return ('%.1f' % x).rstrip('0').rstrip('.')


def color_of(name):
    return PLANET_COLOR.get(name) or SIGN_COLOR.get(name) or ELEMENT_COLOR.get(name) or INK


# ── the suit symbols (schematic) ────────────────────────────────────────────────────────────────

def wand(L):
    """A club, upright, centred on 0,0: a staff with a knob at each end and flames at the top."""
    h = L / 2
    return ('<g><rect x="-7" y="%s" width="14" height="%s" rx="7" fill="#c9a36a" stroke="#5a3a1c" stroke-width="3"/>'
            '<circle cx="0" cy="%s" r="10" fill="#c9a36a" stroke="#5a3a1c" stroke-width="3"/>'
            '<circle cx="0" cy="%s" r="10" fill="#c9a36a" stroke="#5a3a1c" stroke-width="3"/>'
            '<path d="M-9 %s C-16 %s -6 %s 0 %s C6 %s 16 %s 9 %s" fill="#e8742a" stroke="#b0361f" stroke-width="2.5" stroke-linejoin="round"/></g>'
            % (f(-h), f(L), f(-h), f(h), f(-h - 8), f(-h - 22), f(-h - 30), f(-h - 42), f(-h - 30), f(-h - 22), f(-h - 8)))


def sword(L):
    """A sword, point up, centred on 0,0."""
    h = L / 2
    guard = h - L * 0.2
    return ('<g stroke="#3d3d48" stroke-width="3" stroke-linejoin="round">'
            '<path d="M0 %s L8 %s L8 %s L-8 %s L-8 %s Z" fill="#ecebe6"/>'
            '<line x1="0" y1="%s" x2="0" y2="%s" stroke-width="1.5"/>'
            '<rect x="-26" y="%s" width="52" height="9" rx="4" fill="#c9a24a"/>'
            '<rect x="-5" y="%s" width="10" height="%s" fill="#6b4a2a"/>'
            '<circle cx="0" cy="%s" r="8" fill="#c9a24a"/></g>'
            % (f(-h), f(-h + 22), f(guard), f(guard), f(-h + 22), f(-h + 26), f(guard - 6),
               f(guard), f(guard + 9), f(h - guard - 17), f(h - 8)))


def cup(s):
    """A cup, centred on 0,0, about s tall."""
    k = s / 100.0
    return ('<g transform="scale(%s)" stroke="#6b4e12" stroke-width="%s" stroke-linejoin="round">'
            '<path d="M-38 -46 L38 -46 C38 -10 22 6 0 6 C-22 6 -38 -10 -38 -46 Z" fill="#e2bd4f"/>'
            '<path d="M-5 6 L-5 30 L5 30 L5 6" fill="#e2bd4f"/>'
            '<path d="M-26 46 C-26 34 -12 30 0 30 C12 30 26 34 26 46 Z" fill="#e2bd4f"/>'
            '<ellipse cx="0" cy="-46" rx="38" ry="7" fill="#9fc3e6"/></g>' % (f(k), f(3 / k)))


def pentacle(s):
    """A pentacle (a disk bearing a five-pointed star), centred on 0,0, s across."""
    r = s / 2
    pts = []
    for i in range(5):
        a = -math.pi / 2 + i * 4 * math.pi / 5
        pts.append('%s %s' % (f(r * 0.78 * math.cos(a)), f(r * 0.78 * math.sin(a))))
    return ('<g><circle r="%s" fill="#ead9a2" stroke="#5a4a14" stroke-width="3"/>'
            '<circle r="%s" fill="none" stroke="#5a4a14" stroke-width="1.5"/>'
            '<path d="M%s Z" fill="none" stroke="#3f6b2a" stroke-width="%s" stroke-linejoin="round"/></g>'
            % (f(r), f(r * 0.86), ' L'.join(pts), f(max(2, r / 14))))


def place(sym, x, y, rot=0):
    return '<g transform="translate(%s %s)%s">%s</g>' % (f(x), f(y), (' rotate(%s)' % f(rot)) if rot else '', sym)


# The centre region of a card: y from 270 to 650.
MID_Y = 460
MID_H = 380

# Pip positions for cups and pentacles, as (x, y) in -1..1 (the Seven of Cups as Book T sets it: "two
# descending triangles above a point").
GRID = {
    1: [(0, 0)],
    2: [(0, -.6), (0, .6)],
    3: [(0, -.7), (0, 0), (0, .7)],
    4: [(-.5, -.5), (.5, -.5), (-.5, .5), (.5, .5)],
    5: [(-.5, -.6), (.5, -.6), (0, 0), (-.5, .6), (.5, .6)],
    6: [(-.5, -.65), (.5, -.65), (-.5, 0), (.5, 0), (-.5, .65), (.5, .65)],
    7: [(-.5, -.8), (.5, -.8), (0, -.45), (-.5, -.1), (.5, -.1), (0, .25), (0, .8)],
    8: [(-.5, -.78), (.5, -.78), (-.5, -.26), (.5, -.26), (-.5, .26), (.5, .26), (-.5, .78), (.5, .78)],
    9: [(-.5, -.78), (.5, -.78), (-.5, -.26), (.5, -.26), (0, 0), (-.5, .26), (.5, .26), (-.5, .78), (.5, .78)],
    10: [(-.5, -.82), (.5, -.82), (0, -.55), (-.5, -.27), (.5, -.27), (-.5, .27), (.5, .27), (0, .55), (-.5, .82), (.5, .82)],
}


def centre(suit, n, text):
    """The suit's symbols, counted as Book T counts them, in the centre region."""
    out = []
    if suit in ('Cups', 'Pentacles'):
        size = {1: 200, 2: 130, 3: 96, 4: 100, 5: 92, 6: 92, 7: 72}.get(n, 66)
        mk = cup if suit == 'Cups' else pentacle
        for (x, y) in GRID[n]:
            out.append(place(mk(size), CX + x * 130, MID_Y + y * (MID_H / 2 - size / 2)))
        return ''.join(out)
    mk = wand if suit == 'Wands' else sword
    L = 330 if n > 1 else 360
    if n == 1:
        return place(mk(L), CX, MID_Y)
    if n == 10:
        # Book T: four hands hold eight crossed (the points falling away, for the swords), and in the
        # centre two more: crossed (Ten of Swords) or upright through the junction (Ten of Wands).
        fan = (34, 48, 62, 76) if suit == 'Swords' else (24, 40, 56, 72)
        for a in fan:
            out += [place(mk(L), CX, MID_Y, a), place(mk(L), CX, MID_Y, -a)]
        if suit == 'Swords':
            out += [place(mk(L * 0.95), CX, MID_Y, 12), place(mk(L * 0.95), CX, MID_Y, -12)]
        else:
            out += [place(mk(L), CX - 14, MID_Y), place(mk(L), CX + 14, MID_Y)]
        return ''.join(out)
    pairs, upright = n // 2, n % 2
    span = {1: [30], 2: [22, 50], 3: [20, 40, 60], 4: [16, 32, 48, 64]}[pairs]
    for a in span:
        out += [place(mk(L), CX, MID_Y, a), place(mk(L), CX, MID_Y, -a)]
    if upright:
        out.append(place(mk(L + 10), CX, MID_Y))
    return ''.join(out)


def support(kind, cx, y_tip, up):
    """The small dagger or flaming wand a glyph stands on (Book T: "on the points of two small
    daggers"; "on two small wands ... with flames"). `up`: the support points up, its tip at y_tip."""
    d = -1 if up else 1
    L = 54
    if kind == 'dagger':
        g = y_tip - d * 0  # tip
        base = y_tip - d * L
        return ('<g stroke="#3d3d48" stroke-width="2.5" stroke-linejoin="round">'
                '<path d="M%s %s L%s %s L%s %s Z" fill="#ecebe6"/>'
                '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="6" stroke-linecap="round" stroke="#c9a24a"/></g>'
                % (f(cx), f(g), f(cx + 6), f(base), f(cx - 6), f(base), f(cx - 16), f(base), f(cx + 16), f(base)))
    # a small flaming wand
    base = y_tip - d * L
    return ('<g><line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#5a3a1c" stroke-width="10" stroke-linecap="round"/>'
            '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#c9a36a" stroke-width="5" stroke-linecap="round"/>'
            '<path d="M%s %s q-7 %s 0 %s q7 %s 0 %s" fill="#e8742a" stroke="#b0361f" stroke-width="2"/></g>'
            % (f(cx), f(y_tip), f(cx), f(base), f(cx), f(y_tip), f(cx), f(base),
               f(cx - 9), f(y_tip + d * 2), f(d * 10), f(d * 18), f(-d * 8), f(-d * 18)))


# ── Book T's own placement ──────────────────────────────────────────────────────────────────────

def book_t_text(node):
    return (node.get('sections') or {}).get('Book T (1912)', '')


def decan_sentence(node):
    """Book T's sentence naming the decan's planet and sign (e.g. "Above the middle wand is the sign
    Saturn, and below is that of Leo")."""
    m = node['metadata']
    body = book_t_text(node).split('\n\n', 1)[-1]
    for s in re.split(r'(?<=[.:])\s+', body):
        if re.search(r'\b%s\b' % m['planet'], s) and re.search(r'\b%s\b' % m['sign'], s):
            return s.strip()
    return ''


def decan_order(node):
    """(above, below, support, sentence): the one Book T names first goes above."""
    m = node['metadata']
    s = decan_sentence(node)
    above, below = m['planet'], m['sign']
    if s and s.find(m['sign']) < s.find(m['planet']):
        above, below = below, above
    low = s.lower()
    kind = ''
    if 'dagger' in low or ('short' in low and 'sword' in low):
        kind = 'dagger'
    elif re.search(r'(small|short) (flaming )?wands', low) or 'small wands' in low:
        kind = 'wand'
    return above, below, kind, s


def tetragrammaton(node):
    """The letter Book T gives the card ("Geburah of י"), else the suit's."""
    m = re.search(r'\b[A-Z][a-z]+ of ([יהו])', book_t_text(node))
    if m:
        return HEBREW[m.group(1)]
    return SUIT_LETTER.get(node['metadata'].get('suit'), '')


# ── a card ──────────────────────────────────────────────────────────────────────────────────────

def frame(color):
    return ('<rect x="8" y="8" width="%d" height="%d" rx="18" fill="%s" stroke="%s" stroke-width="6"/>'
            '<rect x="24" y="24" width="%d" height="%d" rx="10" fill="none" stroke="%s" stroke-width="1.5" opacity=".55"/>'
            % (W - 16, H - 16, PAPER, color, W - 48, H - 48, color))


def caption(title, sub):
    t = title
    lines = [t]
    if len(t) > 28:
        for sep in (': ', '; ', ', '):
            if sep in t:
                a, b = t.split(sep, 1)
                lines = [a + sep.strip(), b[0].upper() + b[1:]]
                break
    size = 30 if max(len(x) for x in lines) <= 26 else (25 if max(len(x) for x in lines) <= 34 else 21)
    out = []
    y0 = 880 if len(lines) == 1 else 854
    for i, ln in enumerate(lines):
        out.append('<text x="%s" y="%d" font-size="%d" text-anchor="middle" fill="%s" font-family="Georgia, \'Times New Roman\', serif">%s</text>'
                   % (f(CX), y0 + i * (size + 4), size, INK, escape(ln)))
    out.append('<text x="%s" y="%d" font-size="18" text-anchor="middle" fill="%s" font-family="Georgia, \'Times New Roman\', serif" font-style="italic">%s</text>'
               % (f(CX), 924, MUTED, escape(sub)))
    return ''.join(out)


def corner_text(x, y, s, size=22, anchor='middle'):
    return ('<text x="%s" y="%s" font-size="%d" text-anchor="%s" fill="%s" font-family="Georgia, \'Times New Roman\', serif">%s</text>'
            % (f(x), f(y), size, anchor, MUTED, escape(s)))


def card_svg(node):
    m = node['metadata']
    cat = node['category']
    el = m.get('element') or ''
    parts, desc = [], []
    name = node['name']

    if cat == 'keys':
        letter = HEBREW[m['hebrew_letter']]
        attrs = [a.strip() for a in re.split(r'\band\b', m['attribution'])]
        color = color_of(attrs[-1]) if len(attrs) == 1 else ELEMENT_COLOR.get(attrs[0], INK)
        parts.append(frame(color))
        if len(attrs) == 1:
            parts.append(glyph(attrs[0], CX, 150, 130, color_of(attrs[0])))
        else:
            parts.append(glyph(attrs[0], CX - 70, 150, 110, color_of(attrs[0])))
            parts.append(glyph(attrs[1], CX + 70, 150, 110, color_of(attrs[1])))
        parts.append(glyph(letter, CX, 470, 330, INK))
        parts.append('<text x="%s" y="750" font-size="40" text-anchor="middle" fill="%s" font-family="Georgia, \'Times New Roman\', serif" font-style="italic">%s</text>'
                     % (f(CX), INK, escape(m['hebrew_translit'])))
        parts.append(corner_text(CX, 790, 'Path %d on the Tree of Life' % m['tree_path'], 20))
        parts.append(corner_text(64, 78, ROMAN[m['key_number']], 30))
        sub = '%s · %s · %s' % (m['card_name_1912'], m['hebrew_translit'], m['attribution'])
        desc.append('The letter %s (%s) in the centre; above it %s, the Key\'s attribution; Path %d.'
                    % (m['hebrew_translit'], m['hebrew_letter'], m['attribution'], m['tree_path']))
    else:
        suit = m['suit']
        color = ELEMENT_COLOR[el]
        parts.append(frame(color))
        parts.append(glyph(tetragrammaton(node) if cat != 'courts' else RANK_LETTER[m['rank']], 70, 74, 72, INK))
        parts.append(glyph(el, W - 66, 70, 52, color))
        if cat == 'decans':
            above, below, kind, sentence = decan_order(node)
            parts.append(centre(suit, m['pip'], sentence))
            top_c, bot_c = 150, 770
            if kind:
                parts.append(support(kind, CX, top_c + 64, True))
                parts.append(support(kind, CX, bot_c - 64, False))
            parts.append(glyph(above, CX, top_c, 116, color_of(above)))
            parts.append(glyph(below, CX, bot_c, 116, color_of(below)))
            sub = '%s · %s · %s' % (m['card_name_1912'], m['decan'], m['sephirah'])
            desc.append('%s above the central symbol and %s below, as Book T places them: "%s"'
                        % (above, below, sentence))
        elif cat == 'aces':
            rays = ''.join('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2" opacity=".45"/>'
                           % (f(CX + 60 * math.cos(a)), f(MID_Y + 60 * math.sin(a)),
                              f(CX + 230 * math.cos(a)), f(MID_Y + 230 * math.sin(a)), color)
                           for a in [i * math.pi / 12 for i in range(24)])
            parts.append(rays)
            parts.append(centre(suit, 1, ''))
            parts.append(glyph(el, CX, 140, 100, color))
            parts.append(glyph(SUIT_LETTER[suit], CX, 790, 100, INK))
            sub = '%s · the Root · %s' % (m['card_name_1912'], m['sephirah'])
            desc.append('The root of %s: its element above, its letter of the Name below.' % el)
        else:  # courts
            sub_el, of_el = [x.strip() for x in m['element_in_element'].split(' of ')]
            parts.append(glyph(sub_el, CX - 62, 145, 104, ELEMENT_COLOR[sub_el]))
            parts.append(corner_text(CX, 158, 'of', 24))
            parts.append(glyph(of_el, CX + 62, 145, 104, ELEMENT_COLOR[of_el]))
            parts.append(centre(suit, 1, ''))
            rm = re.match(r'\s*(\d+)\D+?([A-Z][a-z]+)\s*\W+\s*(\d+)\D+?([A-Z][a-z]+)', m.get('rules', ''))
            if rm:
                d1, s1, d2, s2 = rm.groups()
                parts.append(glyph(s1, CX - 80, 770, 96, color_of(s1)))
                parts.append(glyph(s2, CX + 80, 770, 96, color_of(s2)))
                parts.append(corner_text(CX - 80, 838, '%s°' % d1, 20))
                parts.append(corner_text(CX + 80, 838, '%s°' % d2, 20))
                parts.append('<path d="M%s 770 L%s 770 M%s 762 L%s 770 L%s 778" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>'
                             % (f(CX - 18), f(CX + 18), f(CX + 10), f(CX + 18), f(CX + 10), MUTED))
                desc.append('%s; rules %s.' % (m['element_in_element'], m['rules']))
            else:
                # The Princesses rule a quadrant of the heavens around the North Pole.
                parts.append('<g fill="none" stroke="%s" stroke-width="3"><path d="M%s 820 L%s 720 A100 100 0 0 1 %s 820 Z" fill="%s" fill-opacity=".12"/>'
                             '<circle cx="%s" cy="820" r="5" fill="%s"/></g>'
                             % (color, f(CX - 50), f(CX - 50), f(CX + 50), color, f(CX - 50), color))
                parts.append(corner_text(CX + 70, 838, 'Pole', 18, 'start'))
                desc.append('%s; rules %s.' % (m['element_in_element'], m['rules']))
            sub = '%s · %s' % (m['card_name_1912'], m['element_in_element'])
    parts.append(caption(name, sub))
    title = '%s: %s (Book T deck, iconography)' % (name, sub)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-labelledby="t d">\n'
            '<title id="t">%s</title>\n<desc id="d">%s Glyphs drawn for recursive-tarot (CC BY-SA 4.0); composed by scripts/build_book_t_iconography.py.</desc>\n'
            '%s\n</svg>\n' % (W, H, W, H, escape(title), escape(' '.join(desc)), '\n'.join(parts)))


# ── the grammar ─────────────────────────────────────────────────────────────────────────────────

def with_illustration(node):
    m = node['metadata']
    ills = [i for i in (m.get('illustrations') or []) if i.get('edition') != EDITION]
    ills.append({'url': URL % node['id'], 'artist': ARTIST, 'edition': EDITION, 'license': 'CC-BY-SA-4.0'})
    m['illustrations'] = ills


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    only = set(x for x in a.only.split(',') if x)
    cur_json = open(DECK, encoding='utf-8').read()
    g = json.loads(cur_json)
    cards = [n for n in g['nodes'] if n.get('category') in ('aces', 'courts', 'decans', 'keys')]
    if len(cards) != 78:
        raise SystemExit('expected 78 cards, found %d' % len(cards))
    stale = []
    os.makedirs(OUT, exist_ok=True) if not a.check else None
    for n in cards:
        if only and n['id'] not in only:
            continue
        svg = card_svg(n)
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
        print('[build_book_t_iconography] --check: %s' % ('up to date (78 cards)' if ok else
              'out of date (%d pictures%s); run: python scripts/build_book_t_iconography.py'
              % (len(stale), ', the grammar' if grammar_stale else '')))
        sys.exit(0 if ok else 1)
    if grammar_stale:
        with open(DECK, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(out_json)
    print('[build_book_t_iconography] %d pictures written%s' % (len(stale), ', grammar updated' if grammar_stale else ''))


if __name__ == '__main__':
    main()
