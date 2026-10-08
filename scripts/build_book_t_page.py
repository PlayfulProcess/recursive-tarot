# -*- coding: utf-8 -*-
"""Build pages/book-t.html: the whole of Book T as printed in The Equinox I(8), 1912.

  python scripts/build_book_t_page.py           # write pages/book-t.html
  python scripts/build_book_t_page.py --check   # write nothing; exit 1 if the page is out of date

PlayfulProcess, Oct 8 2026: "highlight and hyperlink things that recursive eco might want to
highlight and hyperlink ... very engaging and maybe easy to scan through to actually read it."

Source: research/sources/book-t-equinox-1912.txt (the 1912 text; its header gives the provenance
and the public-domain reasoning). The transcription's leftovers are removed here, and the places
where it differs from the printed page are corrected from the scan (FIXES, each with its page).
Nothing else in the 1912 words is changed.

What the page adds, all of it styled apart from the 1912 text:
  * a short intro per chapter, labelled as this site's (INTROS);
  * the printed page numbers in the margin (PAGE_STARTS: where each printed page begins, read
    off the scan, archive.org IAPSOP-equinox_v1_n8_1912_Sep);
  * card names link to the card in the Golden Dawn deck (first mention per passage), with the
    card's image beside each card's description; each card header carries its decan, element
    or letter, taken from Book T's own tables;
  * glossary terms link to pages/glossary.html#term and "Path NN" to the Tree of Life map, first
    mention per passage (scripts/link_glossary.py's matcher, reused); single Hebrew letters and
    the sephiroth written in Hebrew link to their glossary entries;
  * Crowley's square-bracket notes, and the one footnote, are set as notes.
Generated: do not hand-edit pages/book-t.html; edit this script or the source and re-run.
check_all.py runs `--check`.
"""
import argparse, html, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from import_book_t_1912 import tidy, BOOK_T_TO_DECK, MAJORS, SUITS, RANKS  # noqa: E402
import link_glossary as LG  # noqa: E402

SRC = os.path.join(ROOT, 'research', 'sources', 'book-t-equinox-1912.txt')
DECK = os.path.join(ROOT, 'tarot', 'golden-dawn-book-t-tarot', 'grammar.json')
GLOSSARY = os.path.join(ROOT, 'tarot', 'glossary-of-tarot', 'grammar.json')
OUT = os.path.join(ROOT, 'pages', 'book-t.html')
SCAN = 'https://archive.org/details/IAPSOP-equinox_v1_n8_1912_Sep'
CARD_HREF = '../viewers/cards.html?src=../tarot/golden-dawn-book-t-tarot/grammar.json&item='
COURSE = 'course-viewer.html?course=walking-the-golden-dawn-path'

PG_A, PG_B = '\ue030', '\ue031'          # page marker: PG_A + "154" + PG_B
NOTE_A, NOTE_B = '\ue010', '\ue011'      # Crowley's [ ... ]
CIPHER = '\ue020'
DOTS10, DOTS6, DOTS9 = '\ue021', '\ue022', '\ue023'   # the little pentacle figures on pp. 180, 181, 197
SIC = '\ue024%d\ue025'                   # a "sic" note of this site's, by number (SICS)

# ── Corrections to the transcription, checked against the scan (page in the comment) ──────────
FIXES = [
    ('WITH THEIR ATTRIBUTIONS; INCLUDING A',
     'A DESCRIPTION OF THE CARDS OF THE TAROT\n\nWITH THEIR ATTRIBUTIONS; INCLUDING A'),  # p.143 (title line)
    ('GR:Alpha chi-alpha-iota Omega', 'Α καὶ Ω'),                                     # p.145
    ('the Seals thereof?\'', 'the Seals thereof?"'),                                  # p.145
    ('S.Y.M.B.O.L.A. Ankh', 'S.Y.M.B.O.L.A. ☥'),                                      # p.145
    ('Angel P Scorpio h> H\nU A;', 'Angel ' + CIPHER + ' H U A;'),                   # p.146
    ('Seventy-eight Symbols of this Book\n;', 'Seventy-eight Symbols of this Book;'),  # p.153
    ('the Flame and\nLighting:', 'the Flame and\nLightning:'),                        # p.147
    ('The Spirit of GR:Alpha-iota-theta-eta-rho', 'The Spirit of Αἰθήρ'),            # p.150
    ('Sun of the Morning, chief', 'Son of the Morning, chief'),                       # p.150
    ('symbolizes GR:Alpha and GR:Omega;', 'symbolizes Α and Ω;'),                     # p.167
    ('ROSE OFTHE PALACE', 'ROSE OF THE PALACE'),                                      # p.171
    ('These four stack represent', 'These four stacks represent'),                    # p.208
    (' 43. | ', ' 43 | '),                                                            # p.149
    ('Peace restored |', 'Peace Restored |'),                                         # p.148
    ('Unstable Effor |', 'Unstable Effort |'),                                        # p.149
    ('Oppresion |', 'Oppression |'),                                                  # p.149
    ('Success unfulfilled |', 'Success Unfulfilled |'),                               # p.149
    ('heavy head or end | \n Red-gold | \n Blue or brown |',
     'heavy head or end | \n Red-gold | \n Blue or borwn |'),                          # p.172, as printed
    ('Flowery land, bull, sceptre with orb and cross, orb held downwards |',
     'Flowerly land, bull, sceptre with orb and cross, orb held downward |'),          # p.172, as printed
    (' Rich brown |', ' Rich-brown |'),                                               # p.172
    ('Capricorn Pisces two swords: 1 each of others.',
     'Capricorn Pisces two swords: 1 each of the other suits.'),                      # p.174
    ('Capricorn Pisces 2 W. 2 C.: 1 each of others.',
     'Capricorn Pisces 2 W. 2 C.: 1 each of the others.'),                            # p.174
    ('Or in Aries Gemini Virgo Scorpio Capricorn 2 pentacles:',
     'Or in Aries Gemini Virgo Scorpio Capricorn two pentacles:'),                    # p.175
    ('Or in Aries Cancer Virgo Scorpio Aquarius 2 Cups:',
     'Or in Virgo Scorpio Aquarius Aries Cancer two Cups:'),                          # p.175
    ('Or in Taurus Cancer Virgo Sagittarius Aquarius two Pentacles: 1 of each of the others.',
     'Or in Virgo Sagittarius Capricorn' + SIC % 1 + ' Taurus Cancer two Pentacles: 1 each of the others.'),  # p.175
    ('Or in Taurus Cancer Libra Sagittarius Aquarius two Swords: 1 of each of the others.',
     'Or in Libra Sagittarius Aquarius Taurus Cancer two wands' + SIC % 2 + ': 1 each of the other suits.'),  # p.175
    ('beginning of the Decanates is', 'beginning of the Decantes is'),                 # p.176, as printed
    ('symbol  thus, and Libra','symbol Moon thus, and Libra'),                       # p.181 (a crescent)
    ('Chokmah of Vau.', 'Chokmah of HB:V.'),                                          # p.182
]
# "sic" notes: the printed page differs from Book T's own table; shown as this site's note.
SICS = {1: 'sic: the table above gives Aquarius', 2: 'sic: the table above gives two Swords'}
# The two pentacle diagrams, which the transcription draws with asterisks over several lines.
DIAGRAMS = [
    (r'thus arranged \n\n \* \*\n\n \*\n\n \* \*\n\n \* \*\n\n \*\n\n \* \*\n',
     'thus arranged ' + DOTS10 + '.\n'),                                              # p.181
    (r'three each \* \* \n\n\* \*\n\n\* \*\n\n\* \*\n\n\. Above',
     'three each ' + DOTS6 + '. Above'),                                               # p.197
    (r'arranged thus (\* ){9}:', 'arranged thus ' + DOTS9 + ':'),                        # p.180
]
# Marks the transcription left behind: a stray ">" after a word, a page reference "172}".
STRAY = [(re.compile(r'(?<=\S)>(?=[\s.,;:]|$)', re.M), ''), (re.compile(r'^\d{3}\}\s*$', re.M), '')]

# Where each printed page begins (pp. 145-210), as a pattern found in order in the source.
# p.143 is the title page; p.144 is the coloured plate of the frontispiece (not reproduced).
PAGE_STARTS = [
    (143, r'A DESCRIPTION OF THE CARDS OF THE TAROT'), (145, r'A DESCRIPTION OF'), (146, r'A third is yellow'),
    (147, r'THE TITLES OF THE SYMBOLS'), (148, r'13\. The Knight of Swords'), (149, r'\n 31 \|'),
    (150, r'\n 57 \|'), (151, r'\n 66 \|'), (152, r'\n 73 \|'),
    (153, r'The Descriptions of the Seventy-eight'), (154, r'surround it, answering'),
    (155, r'III\n\nTHE ROOT OF THE POWERS OF THE AIR'), (156, r'red Greek Cross'),
    (157, r'The Four Queens'), (158, r'Chariots\. They represent'),
    (159, r'V\n\nTHE LORD OF THE FLAME'), (160, r'VI\n\nTHE QUEEN OF THE THRONES OF FLAME'),
    (161, r'is shewn\. He wears corslet'), (162, r"tiger's head, and the same"),
    (163, r'but upon his helmet, cuirass'), (164, r'feeling\. Very much affected'),
    (165, r'XII\n\nTHE PRINCESS OF THE WATERS'), (166, r'as that of the Knight of Wands, but he wears'),
    (167, r'If ill dignified, cruel, sly'), (168, r'If ill dignified: harsh'),
    (169, r'XVII\n\nTHE LORD OF THE WIDE'), (170, r'represented in profile'),
    (171, r'Rules from 20 Degree Aries'), (172, r' HEREIN ARE RESUMED'),
    (173, r'OF THE THIRTY-SIX DECANS'), (174, r'The planets govern respectively'),
    (175, r'\n 3\. \|\s*\n Capricorn \|\s*\n Earthly Power'), (176, r'the others\. This is the Planet Mars'),
    (177, r'HB:HVD Solitary'), (178, r'Geburah of HB:Y \(Quarrelling'),
    (179, r'XXIII\n\nTHE LORD OF VALOUR'), (180, r'disks\. All the Pentacles'),
    (181, r'XXVI\n\nTHE LORD OF WEALTH'), (182, r'Contradictory characters'),
    (183, r'Disruption, interruption'), (184, r'XXX\n\nTHE LORD OF LOSS IN PLEASURE'),
    (185, r'each cup\. From these flowers'), (186, r'selfish\ndissipation'),
    (187, r'XXXIV\n\nTHE LORD OF GREAT STRENGTH'), (188, r'to material and selfish'),
    (189, r'XXXVII\n\nTHE LORD OF MATERIAL WORKS'), (190, r'Assured material gain'),
    (191, r'XL\n\nTHE LORD OF EARNED SUCCESS'), (192, r'if the last reserves'),
    (193, r'XLIII\n\nTHE LORD OF MATERIAL HAPPINESS'), (194, r'Permanent and lasting success'),
    (195, r'XLVI\n\nTHE LORD OF ESTABLISHED STRENGTH'), (196, r'and labour\. Rest after'),
    (197, r'XLIX\n\nTHE LORD OF MATERIAL SUCCESS'), (198, r'Pentacles\. Above and below are the'),
    (199, r'in detail of study'), (200, r'LIII\n\nTHE LORD OF RUIN'),
    (201, r'above water, which occupies'), (202, r'success, good luck and'),
    (203, r'BRIEF MEANING OF TWENTY-TWO KEYS'), (204, r'13\. Time, age'),
    (205, r' A Majority of Wands'), (206, r' 4 Sevens'),
    (207, r'A METHOD OF DIVINATION BY THE TAROT'), (208, r'2\. Cut each pack'),
    (209, r'Second Operation'), (210, r'3\. Count and pair as before\. \n\n\[Note that the nature'),
]

CHAPTERS = [  # id, label in the contents, the source paragraph that opens it, icon
    ('front', 'The book and its frontispiece', None, 'book'),
    ('titles', 'The titles of the symbols', 'THE TITLES OF THE SYMBOLS', 'list'),
    ('aces', 'The four Aces', 'The Descriptions of the Seventy-eight Symbols', 'ace'),
    ('courts', 'The sixteen court cards', 'THE SIXTEEN COURT, OR ROYAL CARDS', 'crown'),
    ('decans', 'The thirty-six decans', 'OF THE THIRTY-SIX DECANS', 'wheel'),
    ('keys', 'The twenty-two Keys', 'BRIEF MEANING OF TWENTY-TWO KEYS', 'key'),
    ('dignities', 'Of the dignities', 'OF THE DIGNITIES', 'scale'),
    ('method', 'A method of divination', 'A METHOD OF DIVINATION BY THE TAROT', 'spread'),
]

# This site's notes, one per chapter. Plain words; never Book T's.
INTROS = {
    'front': ("Book T is the Golden Dawn's own book of the 78 cards. Crowley printed it in "
              "*The Equinox* I(8), September 1912, pp. 143–210. This page gives all of it. "
              "Gold numbers in the margin are the printed pages. Notes in square brackets are "
              "Crowley's. Underlined words open the [glossary](glossary.html) or the card. The pictures "
              "beside the cards are the Rider-Waite-Smith deck's; Book T's own deck, in its own order "
              "and titles, is [Book T](../viewers/cards.html?src=../tarot/book-t/grammar.json), its "
              "pictures still to come."),
    'titles': ("Every card has a title. The Aces are Roots. The court cards are a Lord, a Queen, "
               "a Prince and a Princess. Each small card is the Lord of something, set in one decan "
               "of the zodiac under one planet. The trumps are Keys, each with a Hebrew letter."),
    'aces': ("Four Aces, one for each element. Book T places them at the North Pole of the heavens: "
             "the root of each suit."),
    'courts': ("Book T renames the court. Its King rides a horse: the pack calls him Knight. Its "
               "Prince drives a chariot: the pack calls him King. The Knave is a Princess. Each "
               "card is an element of an element, shown here as triangles, as on the printed page."),
    'decans': ("The Twos to the Tens. Each rules ten degrees of the zodiac, a decan, under one "
               "planet. Each entry gives the picture, the meaning, its place on the "
               "[Tree of Life](tree-of-life.html), and two angels of the Schemhamphorash."),
    'keys': ("One short line for each trump, then what groups of cards say. Book T numbers "
             "Fortitude 11 and Justice 8, as printed; the pictures here follow the Rider-Waite-Smith "
             "order. Crowley calls the list \"very unsatisfactory\"."),
    'dignities': ("Book T reads no reversed cards. A card is made strong or weak by the cards on "
                  "either side of it."),
    'method': ("The Order's reading in five operations, with Crowley's notes. It is given here as "
               "history. On this site a reading is a gate, not a fate: relate to the card; never "
               "obey it. The course [The Golden Dawn — the Map and the Walk](" + COURSE + ") "
               "walks the Tree without telling fortunes."),
}

ELEMENTS = ('Fire', 'Water', 'Air', 'Earth')
PLANETS = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')
SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio',
         'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
VS = '︎'   # text presentation, never emoji
GLYPH = {'Saturn': '♄', 'Jupiter': '♃', 'Mars': '♂', 'Sun': '☉', 'Venus': '♀', 'Mercury': '☿',
         'Moon': '☽', 'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊', 'Cancer': '♋', 'Leo': '♌',
         'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏', 'Sagittarius': '♐', 'Capricorn': '♑',
         'Aquarius': '♒', 'Pisces': '♓'}
LETTERS = 'אבגדהוזחטיכלמנסעפצקרשת'   # the 22 Keys in Book T's order (Fortitude ט, Justice ל)
NUM = {'Ace': 'ace', 'Two': '02', 'Three': '03', 'Four': '04', 'Five': '05', 'Six': '06',
       'Seven': '07', 'Eight': '08', 'Nine': '09', 'Ten': '10'}
CARD_RE = re.compile(r"\b(Ace|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Knight|Queen|King|Knave|"
                     r"[2-9]|10) of (Wands|Cups|Chalices|Swords|Pentacles|Disks|Torches)\b")
NUMERAL_RE = re.compile(r'^[IVXL]+$')


def card_id(rank, suit):
    rank = {'2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight',
            '9': 'nine', '10': 'ten'}.get(rank, rank).lower()
    return '%s-%s' % (SUITS[suit.lower()], RANKS[rank])


def key_id(n):
    n = BOOK_T_TO_DECK.get(n, n)
    return 'major-%02d-%s' % (n, MAJORS[n])


# ── source → marked text ────────────────────────────────────────────────────────────────────
def load_source():
    raw = open(SRC, encoding='utf-8').read()
    text = '\n'.join(l for l in raw.split('\n') if not l.startswith('#'))
    for a, b in FIXES:
        if a not in text:
            raise SystemExit('FIXES: %r not found in the source' % a)
        text = text.replace(a, b)
    for pat, rep in DIAGRAMS:
        text, n = re.subn(pat, rep, text)
        if n != 1:
            raise SystemExit('DIAGRAMS: %r matched %d times' % (pat, n))
    for pat, rep in STRAY:
        text = pat.sub(rep, text)
    text = re.sub(r'\nWEH NOTE:.*?\n\n', '\n\n', text, flags=re.S)   # the transcriber's note
    pos, out = 0, []
    for page, pat in PAGE_STARTS:
        m = re.compile(pat).search(text, pos)
        if not m:
            raise SystemExit('PAGE_STARTS: p.%d %r not found after offset %d' % (page, pat, pos))
        at = m.start() + (1 if m.group(0).startswith('\n') else 0)
        out.append(text[pos:at])
        out.append('%s%d%s' % (PG_A, page, PG_B))
        pos = at
    out.append(text[pos:])
    return ''.join(out)


PG_RE = re.compile(PG_A + r'(\d+)' + PG_B)


def split_pages(s):
    """(text without markers, [page numbers found])"""
    return PG_RE.sub('', s), [int(x) for x in PG_RE.findall(s)]


def paragraphs(text):
    out, cur = [], []
    for line in text.split('\n') + ['']:
        if line.strip():
            cur.append(line)
        elif cur:
            out.append(cur)
            cur = []
    return out


def blocks(text):
    """Flat list of blocks: ('p', text) prose with page markers kept inline, ('row', cells, pages),
    ('cap', text, pages) a table caption, ('pg', pages) markers from dropped header text."""
    out = []
    for lines in paragraphs(text):
        joined = '\n'.join(lines)
        bare, pages = split_pages(joined)
        if all('|' in l for l in bare.split('\n') if l.strip()):
            cells = [c.strip().rstrip('|').strip() for c in bare.split('\n')]
            cells = [c for c in cells if c]
            if cells and cells != ['.']:
                out.append(('row', cells, pages))
            elif pages:
                out.append(('pg', pages))
            continue
        if all(l.startswith(' ') for l in bare.split('\n')) and bare.strip():
            t = ' '.join(bare.split())
            if t in PLANETS:
                out.append(('cap', t, pages))
            elif t.startswith('HEREIN ARE RESUMED'):
                out.append(('p', PG_A + str(pages[0]) + PG_B + t if pages else t))
            else:
                if not re.fullmatch(r"[A-Z .,'-]+", t):     # only table header words are dropped
                    raise SystemExit('unexpected indented text: %r' % t)
                if pages:
                    out.append(('pg', pages))
            continue
        if NUMERAL_RE.match(bare.strip()):          # tidy() would drop a lone numeral
            out.append(('p', joined.strip()))
            continue
        out.append(('p', tidy(joined)))
    # A Key row the transcription broke across a blank line (letter + attribution): join it back.
    merged = []
    for b in out:
        if b[0] == 'row' and merged and merged[-1][0] == 'row' and not re.fullmatch(r'\d+\.?', b[1][0]) \
                and re.fullmatch(r'\d+', merged[-1][1][0]) and 57 <= int(merged[-1][1][0]) <= 78:
            merged[-1] = ('row', merged[-1][1] + b[1], merged[-1][2] + b[2])
        else:
            merged.append(b)
    return merged


# ── linking ─────────────────────────────────────────────────────────────────────────────────
class Linker:
    def __init__(self, deck, glossary):
        self.terms = LG.load_terms()[0]
        self.heb = {}
        for it in glossary['items']:
            g = (it.get('metadata') or {}).get('glyph')
            if g:
                self.heb[g] = it['id']
        for code, sid in (('ChKMH', 'chokmah'), ('BYNH', 'binah'), ('ChSD', 'chesed'),
                          ('GBVRH', 'geburah'), ('ThPARTh', 'tiphareth'), ('NTzCh', 'netzach'),
                          ('HVD', 'hod'), ('YSVD', 'yesod'), ('MLKVTh', 'malkuth'), ('KThR', 'kether')):
            self.heb[tidy('HB:' + code)] = sid
        self.gloss_names = {it['id']: it['name'] for it in glossary['items']}
        self.cards = {it['id']: it for it in deck['items']}

    def passage(self):
        return Passage(self)


class Passage:
    """First-mention bookkeeping for one passage (a card, or a stretch of a chapter)."""
    def __init__(self, L):
        self.L, self.sec, self.cards = L, LG.Section(L.terms), set()

    def link(self, text, own=None):
        # Crowley's brackets become private marks so the link syntax can't collide with them.
        text = text.replace('[', NOTE_A).replace(']', NOTE_B)

        def card(m):
            cid = card_id(m.group(1), m.group(2))
            if cid == own or cid in self.cards or cid not in self.L.cards:
                return m.group(0)
            self.cards.add(cid)
            return '[%s](card:%s)' % (m.group(0), cid)
        text = CARD_RE.sub(card, text)

        def heb(m):
            sid = self.L.heb.get(m.group(0))
            if not sid:
                return m.group(0)
            return '[%s](gl:%s)' % (m.group(0), sid)
        text = re.sub(r'[א-ת]+', heb, text)
        return self.sec.link_line(text)


LINK_RE = re.compile(r'\[([^\[\]]+)\]\(([^()\s]+)\)')


def inline(text, L):
    """Linked text (markdown-ish links + private marks) → HTML."""
    out, i = [], 0
    for m in LINK_RE.finditer(text):
        out.append(esc_text(text[i:m.start()]))
        label, href = m.group(1), m.group(2)
        if href.startswith('card:'):
            cid = href[5:]
            out.append('<a class="cl" href="%s%s">%s</a>' % (CARD_HREF, cid, esc_text(label)))
        elif href.startswith('gl:'):
            sid = href[3:]
            out.append('<a class="gl he" href="glossary.html#%s" title="%s" lang="he">%s</a>'
                       % (sid, html.escape(L.gloss_names.get(sid, sid)), esc_text(label)))
        elif href.startswith(LG.GLOSS):
            out.append('<a class="gl" href="glossary.html#%s">%s</a>' % (href[len(LG.GLOSS):], esc_text(label)))
        elif href.startswith(LG.TREE):
            out.append('<a class="gl" href="tree-of-life.html?path=%s">%s</a>' % (href[len(LG.TREE):], esc_text(label)))
        else:
            out.append(esc_text(m.group(0)))
        i = m.end()
    out.append(esc_text(text[i:]))
    s = ''.join(out)
    s = s.replace(NOTE_A, '<span class="cn">[').replace(NOTE_B, ']</span>')
    return s


def esc_text(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'&quot;|"(i\.e\.|e\.g\.)"', lambda m: '<em>%s</em>' % m.group(1) if m.group(1) else m.group(0), s)
    s = re.sub(r'[א-ת][א-תְ-ׇ ]*[א-ת]|[א-ת]',
               lambda m: '<bdi lang="he" class="he">%s</bdi>' % m.group(0), s)
    s = re.sub('[Ͱ-Ͽἀ-῿][Ͱ-Ͽἀ-῿̀-ͯ]*',
               lambda m: '<span lang="grc" class="gr">%s</span>' % m.group(0), s)
    s = re.sub('(\\d+)',lambda m: ' <span class="ed">&#8249;%s&#8250;</span>' % SICS[int(m.group(1))], s)
    s = s.replace(DOTS10,dots([2, 1, 2, 2, 1, 2], 'ten pentacles in six rows: 2, 1, 2, 2, 1, 2'))
    s = s.replace(DOTS6, dots([2, 2, 2], 'six pentacles in two columns of three'))
    s = s.replace(DOTS9, '<span class="ed" title="A small figure of nine dots on the printed page, not redrawn here">'
                         '&#8249;figure of nine&#8250;</span>')
    s = s.replace(CIPHER,'<span class="ed" title="Three letters in a cipher script, not reproduced here">'
                          '&#8249;3 cipher letters&#8250;</span>')
    s = PG_RE.sub(lambda m: '<span class="pg" id="p%s" data-p="%s" aria-label="page %s"></span>'
                  % (m.group(1), m.group(1), m.group(1)), s)
    return s


def dots(rows, label):
    """A small inline figure of pentacles, one row per list entry, centred like the printed page."""
    h = 6 * len(rows)
    out = []
    for r, n in enumerate(rows):
        xs = [7] if n == 1 else [3, 11]
        out += ['<circle cx="%d" cy="%d" r="2.1"/>' % (x, 3 + 6 * r) for x in xs]
    return ('<span class="dots" role="img" aria-label="%s" title="%s"><svg viewBox="0 0 14 %d" width="11" height="%d" '
            'fill="currentColor" aria-hidden="true">%s</svg></span>' % (label, label, h, round(h * 11 / 14), ''.join(out)))


def md_intro(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return re.sub(r'\*([^*]+)\*', r'<em>\1</em>', s)


# ── icons (inline SVG, currentColor) ────────────────────────────────────────────────────────
def svg(inner, size=18, sw=1.6, vb=24):
    return ('<svg viewBox="0 0 %d %d" width="%d" height="%d" fill="none" stroke="currentColor" '
            'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            'focusable="false">%s</svg>' % (vb, vb, size, size, sw, inner))


ICON = {
    'book': '<path d="M4 5c3-1.5 6-1.5 8 .5 2-2 5-2 8-.5v14c-3-1.5-6-1.5-8 .5-2-2-5-2-8-.5z"/><path d="M12 5.5v14"/>',
    'list': '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>',
    'ace': '<rect x="6" y="3" width="12" height="18" rx="1.5"/><path d="M12 8v8M9.5 10.5L12 8l2.5 2.5"/>',
    'crown': '<path d="M4 17l1.5-9 4.5 4 2-6 2 6 4.5-4L20 17z"/><path d="M4 20h16"/>',
    'wheel': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="2"/><path d="M12 3.5v6.5M12 14v6.5M3.5 12H10M14 12h6.5M6 6l4.6 4.6M13.4 13.4L18 18M18 6l-4.6 4.6M10.6 13.4L6 18"/>',
    'key': '<circle cx="7.5" cy="12" r="3.5"/><path d="M11 12h10M17.5 12v3M20.5 12v2.5"/>',
    'scale': '<path d="M12 4v16M7 20h10M5 7h14"/><path d="M5 7l-2.5 6a2.5 2.5 0 0 0 5 0zM19 7l-2.5 6a2.5 2.5 0 0 0 5 0z"/>',
    'spread': '<rect x="2.5" y="8" width="5.5" height="8.5" rx="1"/><rect x="9.25" y="4" width="5.5" height="8.5" rx="1"/><rect x="16" y="8" width="5.5" height="8.5" rx="1"/><rect x="9.25" y="13.5" width="5.5" height="8" rx="1"/>',
    'note': '<path d="M5 4h14v12l-4 4H5z"/><path d="M15 20v-4h4M8.5 9h7M8.5 12.5h5"/>',
    'scan': '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'grid': '<rect x="4" y="4" width="6" height="8" rx="1"/><rect x="14" y="4" width="6" height="8" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><rect x="14" y="14" width="6" height="6" rx="1"/>',
    'up': '<path d="M6 14l6-6 6 6"/>',
}
TRI = {  # the four elemental triangles, as printed
    'Fire': '<path d="M12 4l8 15H4z"/>',
    'Water': '<path d="M12 20L4 5h16z"/>',
    'Air': '<path d="M12 4l8 15H4z"/><path d="M6.6 13h10.8"/>',
    'Earth': '<path d="M12 20L4 5h16z"/><path d="M6.6 11h10.8"/>',
}


def tri(el, size=15):
    return '<span class="tri" title="%s">%s</span>' % (el, svg(TRI[el], size, 1.7))


def astro(name, link=True):
    g = '<span class="ag" aria-hidden="true">%s%s</span>' % (GLYPH[name], VS)
    if link:
        return '<a class="chip" href="glossary.html#%s" title="%s">%s<span>%s</span></a>' % (
            name.lower(), name, g, name)
    return '<span class="sym" title="%s">%s<span class="sr">%s</span></span>' % (name, g, name)


# ── building ────────────────────────────────────────────────────────────────────────────────
def build():
    deck = json.load(open(DECK, encoding='utf-8'))
    glossary = json.load(open(GLOSSARY, encoding='utf-8'))
    L = Linker(deck, glossary)
    cards = L.cards
    bl = blocks(load_source())

    # Book T's own tables, read once for the card headers.
    decan_of, key_row = {}, {}
    for b in bl:
        if b[0] == 'row' and len(b[1]) == 5 and re.fullmatch(r'\d+', b[1][0]) and 21 <= int(b[1][0]) <= 56:
            r, s = b[1][1].split(' of ')
            decan_of[card_id(r, s)] = (b[1][2], b[1][3], b[1][4])          # title, planet, sign
        if b[0] == 'row' and len(b[1]) >= 5 and re.fullmatch(r'\d+', b[1][0]) and 57 <= int(b[1][0]) <= 78:
            key_row[int(b[1][1])] = (b[1][2], b[1][3], b[1][-1], int(b[1][0]) - 57)

    # Split into chapters.
    chap_of, cur = [], 'front'
    opens = {c[2]: c[0] for c in CHAPTERS if c[2]}
    for b in bl:
        if b[0] == 'p':
            bare = split_pages(b[1])[0]
            for start, cid in opens.items():
                if bare.startswith(start):
                    cur = cid
        chap_of.append(cur)

    body, toc, finder = [], [], {'keys': [], 'aces': [], 'courts': [], 'decans': []}
    for cid, label, _, icon in CHAPTERS:
        cb = [b for b, c in zip(bl, chap_of) if c == cid]
        pages = sorted({p for b in cb for p in (split_pages(b[1])[1] if b[0] == 'p' else b[-1] if b[0] != 'pg' else b[1])})
        html_c, ncards = render_chapter(cid, cb, L, cards, decan_of, key_row, finder)
        first = pages[0] if pages else ''
        rng = ('pp. %d–%d' % (pages[0], pages[-1]) if len(pages) > 1 else 'p. %d' % pages[0]) if pages else ''
        toc.append((cid, label, icon, rng, ncards))
        body.append('<section class="chap" id="%s" aria-labelledby="h-%s">\n'
                    '<header class="chead"><span class="cico">%s</span><div><h2 id="h-%s">%s</h2>'
                    '<p class="crng">%s%s</p></div></header>\n'
                    '<aside class="intro" aria-label="This site\'s note"><span class="ilab">%s This site\'s note</span>'
                    '<p>%s</p></aside>\n%s\n</section>'
                    % (cid, cid, svg(ICON[icon], 22), cid, html.escape(label), rng,
                       (' · <a class="scanl" href="%s/page/%s/mode/1up" target="_blank" rel="noopener">%s the scan</a>'
                        % (SCAN, first, svg(ICON['scan'], 14))) if first else '',
                       svg(ICON['note'], 14), md_intro(INTROS[cid]), html_c))
    return page_html(body, toc, finder, cards)


def thumb(it, cls='th', size=None):
    return ('<img class="%s" src="%s" alt="%s" loading="lazy" decoding="async" width="300" height="520">'
            % (cls, html.escape(it['image_url']), html.escape(it['name'])))


def render_chapter(cid, cb, L, cards, decan_of, key_row, finder):
    out, i, n = [], 0, 0
    P = L.passage()
    pending_pages = []

    def para(text, cls=None, passage=None):
        t = (passage or P).link(text)
        h = inline(t, L)
        bare = split_pages(text)[0].strip()
        if bare.startswith('[') and bare.endswith(']') and bare.count('[') == 1:
            return ('<aside class="cnote"><span class="nlab">%s Crowley\'s note</span><p>%s</p></aside>'
                    % (svg(ICON['note'], 13), h.replace('<span class="cn">', '<span class="cn cn-all">', 1)))
        return '<p%s>%s</p>' % (' class="%s"' % cls if cls else '', h)

    def take_pages():
        s = ''.join('%s%d%s' % (PG_A, p, PG_B) for p in pending_pages)
        pending_pages.clear()
        return s

    while i < len(cb):
        b = cb[i]
        if b[0] == 'pg':
            pending_pages.extend(b[1])
            i += 1
            continue
        if b[0] in ('row', 'cap'):
            j = i
            while j < len(cb) and cb[j][0] in ('row', 'cap', 'pg'):
                j += 1
            out.append(render_tables(cb[i:j], L, cards, pending_pages))
            i = j
            continue
        text = b[1]
        bare = split_pages(text)[0].strip()
        # a card: numeral, title (maybe with the card name), card name
        if NUMERAL_RE.match(bare) or (cid == 'courts' and bare.startswith('PRINCESS OF THE ECHOING')):
            k = i if not NUMERAL_RE.match(bare) else i + 1
            numeral = bare if NUMERAL_RE.match(bare) else 'XX'
            pre = take_pages() + (split_pages(text)[1] and ''.join('%s%d%s' % (PG_A, p, PG_B) for p in split_pages(text)[1]) or '')
            title_raw = cb[k][1]
            tbare, tpages = split_pages(title_raw)
            m = CARD_RE.search(tbare)
            if m and m.start() > 0:
                title, cname, k2 = tbare[:m.start()].strip(), tbare[m.start():].strip(), k + 1
            else:
                cn_raw = cb[k + 1][1]
                cnb, cnp = split_pages(cn_raw)
                tpages += cnp
                title, cname, k2 = tbare.strip(), cnb.strip(), k + 2
            pre += ''.join('%s%d%s' % (PG_A, p, PG_B) for p in tpages)
            m = CARD_RE.search(cname)
            ident = card_id(m.group(1), m.group(2))
            j = k2
            while j < len(cb) and cb[j][0] == 'p':
                nb = split_pages(cb[j][1])[0].strip()
                if NUMERAL_RE.match(nb) or nb.startswith(('HEREIN ARE RESUMED', 'PRINCESS OF THE ECHOING')) \
                        or nb.startswith(tuple(c[2] for c in CHAPTERS if c[2])):
                    break
                j += 1
            out.append(render_card(cid, numeral, title, cname, ident, pre, cb[k2:j], L, cards, decan_of))
            finder[cid].append(ident)
            n += 1
            i = j
            continue
        # the Keys: "N. text"
        km = re.match(r'(%s\d+%s)?(\d{1,2})\. ' % (PG_A, PG_B), text) if cid == 'keys' else None
        if km and 'Majority' not in text:
            out.append(render_key(int(km.group(2)), take_pages() + text, L, cards, key_row))
            finder['keys'].append(key_id(int(km.group(2))))
            n += 1
            i += 1
            continue
        # headings printed in the book
        if re.fullmatch(r"[A-Z][A-Z ,;:'.-]+", bare) and len(bare) > 6 and not bare.startswith(('L.I.F.E', 'T. A. P')) \
                and bare not in ('H R U', 'FATHER.') and not any(bare.startswith(c[2]) for c in CHAPTERS if c[2] and c[0] == cid and c[0] != 'front'):
            out.append('<h3 class="bt">%s</h3>' % inline(take_pages() + text, L))
            P = L.passage()
            i += 1
            continue
        if any(bare.startswith(c[2]) for c in CHAPTERS if c[2] and c[0] == cid):
            out.append('<h3 class="bt opener">%s</h3>' % inline(take_pages() + text, L))
            i += 1
            continue
        if re.fullmatch(r'(The Four (Kings|Queens|Princes|Princesses)|(First|Second|Third|Fourth|Fifth) Operation)', bare):
            out.append('<h3 class="bt">%s</h3>' % inline(take_pages() + text, L))
            P = L.passage()
            i += 1
            continue
        if cid == 'method' and re.fullmatch(r'(Development of the Question|Further Development of the Question|'
                                            r'Penultimate Aspects of the Question|Final Result)', bare):
            out.append('<p class="bt-sub">%s</p>' % inline(take_pages() + text, L))
            i += 1
            continue
        cls = None
        if cid == 'front' and bare in ('H R U', 'THE GREAT ANGEL', 'is set over the operations of the Secret Wisdom',
                                       'Α καὶ Ω', 'The First and the Last', 'S.Y.M.B.O.L.A. ☥',
                                       'L.I.F.E. B.I.O.S. V.I.T.A.,', 'and the letters —', 'T. A. P. O., Tarot.'):
            cls = 'ctr'
        if cid == 'titles' and re.match(r'(Such are the Titles|Abodes or Atouts|of the$|Mansions of|my$|FATHER\.)', bare):
            cls = 'ctr sm'
        if cid == 'decans' and re.match('[א-ת]+ ', bare):
            cls = 'seph'
        if cid == 'titles' and re.match(r'\d+\. The ', bare):
            m = CARD_RE.search(bare)
            ident = card_id(m.group(1), m.group(2)) if m else None
            out.append('<p class="trow">%s%s</p>' % (
                ('<a class="tt" href="#%s" aria-label="%s">%s</a>' % (ident, html.escape(cards[ident]['name']),
                                                                       thumb(cards[ident], 'tth'))) if ident else '',
                '<span>%s</span>' % inline(P.link(take_pages() + text), L)))
            i += 1
            continue
        out.append(para(take_pages() + text, cls))
        i += 1
    return '\n'.join(out), n


def render_card(cid, numeral, title, cname, ident, pre, body_blocks, L, cards, decan_of):
    it = cards[ident]
    P = L.passage()
    chips = []
    if ident in decan_of:
        lord, planet, sign = decan_of[ident]
        chips.append('%s<span class="in">in</span>%s' % (astro(planet), astro(sign)))
    paras, foot = [], []
    for b in body_blocks:
        text = b[1]
        bare = split_pages(text)[0].strip()
        em = re.fullmatch(r'(Fire|Water|Air|Earth) of (Fire|Water|Air|Earth)', bare)
        if em:
            pg = ''.join('%s%d%s' % (PG_A, p, PG_B) for p in split_pages(text)[1])
            paras.append('<p class="ctr el">%s%s<span class="of">of</span>%s<span class="sr">%s</span></p>'
                         % (inline(pg, L), tri(em.group(1), 20), tri(em.group(2), 20), bare))
            chips.append('<span class="chip plain">%s<span>%s</span></span>' % (tri(em.group(1)) + tri(em.group(2)), bare))
            continue
        if bare.startswith('Note that the Kings are now called Knights'):
            foot.append('<aside class="cnote foot"><span class="nlab">%s Footnote, 1912</span><p>%s</p></aside>'
                        % (svg(ICON['note'], 13), inline(P.link(text), L)))
            continue
        cls = None
        if re.match(r'(Princess and Empress|Prince and Emperor|Queen of the|King of the|King of Gnomes|Throne of the Ace)', bare) \
                and len(bare) < 60:
            cls = 'ctr'
        elif re.match(r'(Kether|Chokmah|Binah|Chesed|Geburah|Tiphareth|Netzach|Hod|Yesod|Malkuth) of ', bare):
            cls = 'seph'
        elif re.search(r'\b(Angels?|angels)\b.*\b(rule|reign|ruling|dominion)\b|^(Herein|Therein|Ruled by|This Decan hath)', bare):
            cls = 'angels'
        t = P.link(text, own=ident)
        h = inline(t, L)
        if bare.startswith('[') and bare.endswith(']') and bare.count('[') == 1:
            paras.append('<aside class="cnote"><span class="nlab">%s Crowley\'s note</span><p>%s</p></aside>'
                         % (svg(ICON['note'], 13), h))
        else:
            paras.append('<p%s>%s</p>' % (' class="%s"' % cls if cls else '', h))
    head_pg = inline(pre, L) if pre else ''
    return ('<article class="ce" id="%s">\n<header class="ch">%s<span class="num">%s</span>'
            '<h3>%s</h3><p class="cname"><a href="%s%s">%s</a></p>%s</header>\n'
            '<a class="side" href="%s%s" aria-label="Open %s in the Golden Dawn deck">%s'
            '<span class="sl">Open in the deck</span></a>\n<div class="cbody">\n%s\n%s\n</div>\n</article>'
            % (ident, head_pg, numeral, html.escape(title), CARD_HREF, ident, html.escape(cname),
               ('<p class="chips">%s</p>' % ''.join(chips)) if chips else '',
               CARD_HREF, ident, html.escape(it['name']), thumb(it), '\n'.join(paras), '\n'.join(foot)))


def render_key(n, text, L, cards, key_row):
    ident = key_id(n)
    it = cards[ident]
    P = L.passage()
    name, title, attr, idx = key_row[n]
    path = (it.get('metadata') or {}).get('tree_path')
    letter = LETTERS[idx]
    lid = L.heb.get(letter)
    chips = ['<a class="chip" href="glossary.html#%s" title="%s"><bdi lang="he" class="he big">%s</bdi><span>%s</span></a>'
             % (lid, html.escape(L.gloss_names.get(lid, '')), letter, html.escape(L.gloss_names.get(lid, '')))]
    for a in re.split(r' and ', attr):
        a = a.strip()
        if a in GLYPH:
            chips.append(astro(a))
        elif a in ELEMENTS:
            chips.append('<a class="chip" href="glossary.html#%s">%s<span>%s</span></a>' % (a.lower(), tri(a), a))
        elif a == 'Spirit':
            chips.append('<span class="chip plain"><span>Spirit</span></span>')
    if path:
        chips.append('<a class="chip path" href="tree-of-life.html?path=%d">%s<span>Path %d</span></a>'
                     % (path, svg('<circle cx="12" cy="4" r="2"/><circle cx="12" cy="20" r="2"/><path d="M12 6v12"/>', 14), path))
    body = re.sub(r'^(%s\d+%s)?\d{1,2}\. ' % (PG_A, PG_B), lambda m: m.group(1) or '', text)
    h = inline(P.link(body), L)
    return ('<article class="ce key" id="%s">\n<header class="ch"><span class="num">%d</span>'
            '<h3><a href="%s%s">%s</a></h3><p class="cname">%s</p><p class="chips">%s</p></header>\n'
            '<a class="side" href="%s%s" aria-label="Open %s in the Golden Dawn deck">%s'
            '<span class="sl">Open in the deck</span></a>\n<div class="cbody">\n<p>%s</p>\n</div>\n</article>'
            % (ident, n, CARD_HREF, ident, html.escape(name), html.escape(title), ''.join(chips),
               CARD_HREF, ident, html.escape(it['name']), thumb(it), h))


TABLE_HEAD = {
    5: None,  # set per table kind below
}


def render_tables(seq, L, cards, pending_pages):
    """A run of rows/captions → one or more <table>s. Header labels follow the printed page."""
    groups, cur = [], None
    for b in seq:
        if b[0] == 'cap':
            cur = {'cap': b[1], 'rows': [], 'pages': list(b[2])}
            groups.append(cur)
            continue
        if b[0] == 'pg':
            if cur is None:
                cur = {'cap': None, 'rows': [], 'pages': []}
                groups.append(cur)
            cur.setdefault('pending', []).extend(b[1])
            continue
        rk = classify(b[1], None)
        if cur is not None and cur['rows'] and classify(cur['rows'][0][0], None) == 'keys' \
                and not re.fullmatch(r'\d+', b[1][0]):
            # a key row the transcription broke across a blank line: letter + attribution
            prev, ppages = cur['rows'][-1]
            cur['rows'][-1] = (prev + b[1], ppages + list(b[2]))
            continue
        if cur is not None and not cur['cap'] and cur['rows'] and rk in ('decans', 'keys') \
                and classify(cur['rows'][0][0], None) != rk:
            carry = cur.pop('pending', [])
            cur = {'cap': None, 'rows': [], 'pages': [], 'pending': carry}
            groups.append(cur)
        if cur is None:
            cur = {'cap': None, 'rows': [], 'pages': []}
            groups.append(cur)
        pages = cur.pop('pending', []) + list(b[2])
        cur['rows'].append((b[1], pages))
    out = []
    for g in groups:
        rows = g['rows']
        if not rows:
            continue
        first = rows[0][0]
        kind = classify(first, g['cap'])
        out.append(table_html(kind, g, L, cards, pending_pages))
    return '\n'.join(out)


def classify(cells, cap):
    if cap:
        return 'planet'
    if re.fullmatch(r'\d+', cells[0]) and len(cells) == 5 and 21 <= int(cells[0]) <= 56:
        return 'decans'
    if re.fullmatch(r'\d+', cells[0]) and 57 <= int(cells[0]) <= 78:
        return 'keys'
    if cells[0] in ('Wands', 'Cups', 'Swords', 'Pentacles'):
        return 'court'
    if CARD_RE.match(cells[0]) and len(cells) == 4:
        return 'central'
    return 'pairs'


def pg_html(pages):
    return ''.join('<span class="pg" id="p%d" data-p="%d" aria-label="page %d"></span>' % (p, p, p) for p in pages)


def cardcell(text, cards):
    m = CARD_RE.search(text)
    if not m:
        return html.escape(text)
    cid = card_id(m.group(1), m.group(2))
    if cid not in cards:
        return html.escape(text)
    return '<a class="cl" href="#%s">%s</a>' % (cid, html.escape(text))


def table_html(kind, g, L, cards, pending_pages):
    rows = g['rows']
    lead = pg_html(pending_pages)
    pending_pages.clear()
    lead += pg_html(g.get('pages', []))
    if kind == 'decans':
        head = ['No.', 'Card', 'Lord of', 'Decan', 'In']
        body = []
        for cells, pages in rows:
            no, card, lord, planet, sign = cells
            body.append('<tr><td class="no">%s%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                        % (pg_html(pages), no, cardcell(card, cards), html.escape(lord), astro(planet, False), astro(sign, False)))
    elif kind == 'keys':
        head = ['No.', 'The twenty-two Keys of the Book', '', 'Letter', 'Attribution']
        body = []
        for cells, pages in rows:
            no, n, name, title, attr = cells[0], cells[1], cells[2], cells[3], cells[-1]
            ident = key_id(int(n))
            letter = LETTERS[int(no) - 57]
            att = ' '.join(astro(a.strip(), False) if a.strip() in GLYPH else
                           (tri(a.strip()) if a.strip() in ELEMENTS else html.escape(a.strip()))
                           for a in re.split(r' and ', attr))
            body.append('<tr><td class="no">%s%s</td><td><a class="cl" href="#%s">%s. %s</a></td><td>%s</td>'
                        '<td><bdi lang="he" class="he big">%s</bdi></td><td class="att">%s</td></tr>'
                        % (pg_html(pages), no, ident, n, html.escape(name), html.escape(title), letter, att))
    elif kind == 'court':
        head = ['Suit', 'Card', 'Crest', 'Symbols', 'Hair', 'Eyes']
        body, suit = [], None
        for cells, pages in rows:
            if len(cells) == 6:
                suit, cells = cells[0], cells[1:]
            card, crest, sym, hair, eyes = cells
            rank = {'King': 'knight', 'Queen': 'queen', 'Prince': 'king', 'Princess': 'page'}[card]
            cid = '%s-%s' % (SUITS[suit.lower()], rank)
            body.append('<tr><td>%s%s</td><td><a class="cl" href="#%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                        % (pg_html(pages), html.escape(suit), cid, html.escape(card), html.escape(crest),
                           html.escape(sym), html.escape(hair), html.escape(eyes)))
    elif kind == 'central':
        head = ['Card', 'Central decan of', 'Meaning', 'Day']
        body = ['<tr><td>%s%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                % (pg_html(pages), cardcell(c[0], cards), astro(c[1], False), html.escape(c[2]), astro(c[3], False))
                for c, pages in rows]
    elif kind == 'planet':
        head = None
        body = ['<tr><td class="no">%s%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                % (pg_html(pages), html.escape(c[0]), astro(c[1], False), html.escape(c[2]), cardcell(c[3], cards))
                for c, pages in rows]
    else:  # pairs: groups of cards
        head = None
        body = ['<tr><th scope="row">%s%s</th><td>%s</td></tr>' % (pg_html(pages), html.escape(c[0]), html.escape(c[1]))
                for c, pages in rows if len(c) == 2]
    cap = ''
    if g['cap']:
        cap = '<caption>%s</caption>' % astro(g['cap'], True)
    thead = ('<thead><tr>%s</tr></thead>' % ''.join('<th scope="col">%s</th>' % h for h in head)) if head else ''
    return ('%s<div class="tw"><table class="bt-t t-%s">%s%s<tbody>%s</tbody></table></div>'
            % (lead, kind, cap, thead, ''.join(body)))


# ── the page ────────────────────────────────────────────────────────────────────────────────
FINDER = [('keys', 'Keys'), ('aces', 'Aces'), ('courts', 'Court cards'), ('decans', 'Decans')]


def page_html(body, toc, finder, cards):
    toc_html = ''.join(
        '<li><a href="#%s" data-ch="%s"><span class="tico">%s</span><span class="tl">%s</span>'
        '<span class="tm">%s%s</span></a></li>'
        % (cid, cid, svg(ICON[icon], 18), html.escape(label), rng, (' · %d' % n) if n else '')
        for cid, label, icon, rng, n in toc)
    fin = ''
    for key, label in FINDER:
        ids = finder[key]
        if key == 'keys':
            ids = sorted(ids, key=lambda x: int(x.split('-')[1]))
        fin += ('<div class="fg"><span class="fl">%s</span><div class="fr">%s</div></div>'
                % (label, ''.join('<a href="#%s" title="%s">%s</a>' % (i, html.escape(cards[i]['name']), thumb(cards[i], 'fth'))
                                  for i in ids)))
    return TEMPLATE.replace('{{TOC}}', toc_html).replace('{{FINDER}}', fin) \
        .replace('{{BODY}}', '\n'.join(body)).replace('{{SCAN}}', SCAN) \
        .replace('{{ICON_MENU}}', svg(ICON['menu'], 20)).replace('{{ICON_GRID}}', svg(ICON['grid'], 18)) \
        .replace('{{ICON_UP}}', svg(ICON['up'], 20)).replace('{{ICON_SCAN}}', svg(ICON['scan'], 16)) \
        .replace('{{ICON_BOOK}}', svg(ICON['book'], 26))


TEMPLATE = open(os.path.join(ROOT, 'scripts', 'book_t_page_template.html'), encoding='utf-8').read() \
    if os.path.exists(os.path.join(ROOT, 'scripts', 'book_t_page_template.html')) else ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    out = build()
    cur = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
    if a.check:
        print('[build_book_t_page] --check: %s' % ('up to date' if cur == out else 'out of date; run: python scripts/build_book_t_page.py'))
        sys.exit(0 if cur == out else 1)
    if cur != out:
        with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(out)
    print('[build_book_t_page] %s (%d KB)' % ('written' if cur != out else 'unchanged', len(out.encode('utf-8')) // 1024))


if __name__ == '__main__':
    main()
