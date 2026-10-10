# -*- coding: utf-8 -*-
"""Build tarot/book-t/grammar.json: Book T's own 78 cards, in Book T's own order, with no pictures.

  python scripts/build_book_t_deck.py           # write (keeps any picture already added)
  python scripts/build_book_t_deck.py --check   # write nothing; exit 1 if the deck is out of date

PlayfulProcess, Oct 8 2026: "this makes it seem as the book T is RWS, which is not. so lets build
the book T and leave the illustrations to be filled slowly by me as we work on them, dont repeat
numbers in the rendering."

Source: Book T as printed in *The Equinox* I(8), 1912 (public domain), from
research/sources/book-t-equinox-1912.txt with the reading page's corrections from the scan
(scripts/build_book_t_page.py FIXES), parsed by scripts/import_book_t_1912.py.

  * Order and numbers: Book T's own list, "The Titles of the Symbols" (pp. 147-152): 1-4 the
    Aces, 5-20 the court cards, 21-56 the small cards in decan order from Leo, 57-78 the Keys.
    `metadata.number` is the card's own number (coordinator's call, Oct 8 2026): a Key's number
    as Book T prints it in 1912 (the Fool 0, Justice 8, Fortitude 11), a small card's pip, 1 for
    an Ace; the court cards have none. The place in the list of 78 is `metadata.book_t_no`.
  * Names: Book T's title, never a number (Keys "Daughter of the Lords of Truth: the Ruler of the
    Balance", courts "Lord of the Flame and the Lightning: the King of the Spirits of Fire",
    small cards "Lord of Strife", Aces "Root of the Powers of Fire"). The courts are Knight,
    Queen, Prince, Princess.
  * Text: `Book T (1912)` verbatim; `In Book T's table` (the row of Book T's own table: name,
    title, letter, decan); `Correspondences`, the short attribution facts shared with the
    Golden Dawn deck (tarot/golden-dawn-book-t-tarot), which keeps the Rider-Waite-Smith pictures.
  * Pictures: none. `image_url` is an empty slot that PlayfulProcess fills over time. A re-run
    keeps every `image_url`, `metadata.illustrations`, and any section this script does not
    write, so pictures and notes added later (by hand or by recursive.eco sync) survive.
"""
import argparse, copy, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import import_book_t_1912 as IB  # noqa: E402
import build_book_t_page as BP  # noqa: E402

OUT = os.path.join(ROOT, 'tarot', 'book-t', 'grammar.json')
GD = os.path.join(ROOT, 'tarot', 'golden-dawn-book-t-tarot', 'grammar.json')
SITE = 'https://tarot.recursive.eco'
PAGE = SITE + '/pages/book-t.html'
OWNED = ('Book T (1912)', "In Book T's table", 'Correspondences')

# The transcription's key names, where the 1912 scan reads otherwise (p.151).
KEY_NAME_FIX = {'The Hanged': 'The Hanged Man', 'The Judgement': 'The Judgment'}
WORD = {1: 'Ace', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight',
        9: 'Nine', 10: 'Ten'}
RANK_1912 = {'Knight': 'Knight', 'Queen': 'Queen', 'King': 'Prince', 'Knave': 'Princess'}
GD_RANK_ID = {'Knight': 'knight', 'Queen': 'queen', 'King': 'king', 'Knave': 'page'}
ELEMENT = {'wands': 'Fire', 'cups': 'Water', 'swords': 'Air', 'pentacles': 'Earth'}
SUIT_NAME = {'wands': 'Wands', 'cups': 'Cups', 'swords': 'Swords', 'pentacles': 'Pentacles'}
DOTS_MD = {BP.DOTS10: '*(a figure on the printed page: ten pentacles in rows of 2, 1, 2, 2, 1, 2)*',
           BP.DOTS6: '*(a figure on the printed page: six pentacles in two columns of three)*',
           BP.DOTS9: '*(a figure of nine dots on the printed page)*'}

DESCRIPTION = """# Book T — the Golden Dawn's 78 cards

Book T is the Golden Dawn's own book of the tarot, set down mainly by S. L. MacGregor Mathers
around 1888 and kept for initiates. Crowley printed it in *The Equinox* I(8), London, 1912. It is
public domain.

This deck is Book T and only Book T: its order, its titles, its words. It is not the
Rider-Waite-Smith deck. Waite and Smith drew their pictures in 1909, from inside the same Order,
and those pictures sit in a deck of their own,
[Golden Dawn Tarot — Book T with Rider-Waite-Smith Imagery](https://tarot.recursive.eco/viewers/cards.html?src=../tarot/golden-dawn-book-t-tarot/grammar.json).

**The pictures will be added by PlayfulProcess over time.** Each card has an empty picture slot
until then.

## How the cards are set out

- **Order.** Book T's own list of the 78 titles: the four Aces, the sixteen court cards, the
  thirty-six small cards in the order of the decans (starting from Leo), then the twenty-two Keys.
- **Number.** Each card shows its own number: a small card its pip, an Ace 1, a Key the number
  Book T prints. The court cards have none. The Key numbers follow the 1912 printing, which
  numbers Justice 8 and Fortitude 11, the reverse of the Rider-Waite-Smith deck; what each source
  prints is set out in
  [Strength and Justice: the numbering](https://github.com/PlayfulProcess/recursive-tarot/blob/main/research/synthesis/strength-justice-numbering.md).
- **Name.** Each card is named by its Book T title: *Lord of Strife*, *Root of the Powers of
  Fire*, *Daughter of the Lords of Truth: the Ruler of the Balance*.
- **Court.** Knight, Queen, Prince, Princess. Book T's Knight rides a horse; its Prince drives a
  chariot; its Princess stands.

Every card carries the 1912 text, word for word, with Crowley's notes in square brackets. The
whole book reads as one page at [Book T (1912)](https://tarot.recursive.eco/pages/book-t.html).

*Source: Book T, as printed in* The Equinox *I(8), 1912, pp. 143-210, from the transcription at
the-equinox.org, checked against [the scan](https://archive.org/details/IAPSOP-equinox_v1_n8_1912_Sep).
Built by `scripts/build_book_t_deck.py`.*
"""

GROUPS = [  # id, name, category, chapter anchor on the reading page, one line of this site's
    ('bt-aces', 'The four Aces', 'aces', 'aces',
     "Book T's first four symbols: the roots of the four elements."),
    ('bt-courts', 'The sixteen court cards', 'courts', 'courts',
     'Knight, Queen, Prince and Princess of each suit: an element within an element.'),
    ('bt-decans', 'The thirty-six small cards', 'decans', 'decans',
     'The Twos to the Tens, one for each decan of the zodiac, starting from Leo.'),
    ('bt-keys', 'The twenty-two Keys', 'keys', 'keys',
     'The trumps, each a Hebrew letter and a path on the Tree of Life.'),
]


def corrected_text():
    """The 1912 text with the reading page's corrections, without its page markers."""
    return BP.PG_RE.sub('', BP.load_source())


def titles(text):
    """Book T's list of the 78 titles: {no: dict}."""
    seg = text[text.find('THE TITLES OF THE SYMBOLS'):text.find('Such are the Titles')]
    rows = {}
    prose = re.sub(r'\s+', ' ', seg[:seg.find(' NO.')])
    for m in re.finditer(r'(\d+)\. The (Ace|Knight|Queen|King|Knave) of (\w+) is (?:called )?"?(.+?)"?\.? ?(?=\d+\. The |$)', prose):
        no, rank, suit, title = int(m.group(1)), m.group(2), m.group(3).lower(), m.group(4).strip().rstrip('."')
        rows[no] = dict(kind='ace' if rank == 'Ace' else 'court', rank=rank, suit=suit, title=title)
    cells = [c.strip().split('\n')[-1].strip() for c in seg[seg.find(' NO.'):].split('|')]
    cells = [c for c in cells if c]
    i = 0
    while i < len(cells):
        if not re.fullmatch(r'\d+\.?', cells[i]):
            i += 1
            continue
        no = int(cells[i].rstrip('.'))
        if 21 <= no <= 56:
            card, lord, planet, sign = cells[i + 1:i + 5]
            pip, suit = re.fullmatch(r'(\d+) of (\w+)', card).groups()
            rows[no] = dict(kind='small', pip=int(pip), suit=suit.lower(), title='Lord of ' + lord,
                            planet=planet, sign=sign)
            i += 5
        elif 57 <= no <= 78:
            key, name, title, _letter, attr = cells[i + 1:i + 6]
            title = re.sub(r',(?=\S)', ', ', title)      # "Power,the Prophet": the scan has the space
            rows[no] = dict(kind='key', key=int(key), card=KEY_NAME_FIX.get(name, name), title=title, attribution=attr)
            i += 6
        else:
            i += 1
    assert sorted(rows) == list(range(1, 79)), 'titles: got %d rows' % len(rows)
    return rows


def gd_id(r):
    """The matching card's id in the Golden Dawn deck (and on the reading page)."""
    if r['kind'] == 'key':
        return IB.MAJORS and 'major-%02d-%s' % (IB.BOOK_T_TO_DECK.get(r['key'], r['key']),
                                                IB.MAJORS[IB.BOOK_T_TO_DECK.get(r['key'], r['key'])])
    if r['kind'] == 'ace':
        return '%s-ace' % r['suit']
    if r['kind'] == 'court':
        return '%s-%s' % (r['suit'], GD_RANK_ID[r['rank']])
    return '%s-%02d' % (r['suit'], r['pip'])


def new_id(r):
    if r['kind'] == 'key':
        return 'key-%02d-%s' % (r['key'], re.sub(r'[^a-z]+', '-', r['card'].lower().replace('the ', '')).strip('-'))
    if r['kind'] == 'ace':
        return '%s-ace' % r['suit']
    if r['kind'] == 'court':
        return '%s-%s' % (r['suit'], RANK_1912[r['rank']].lower())
    return '%s-%02d' % (r['suit'], r['pip'])


def no_the(s):
    s = re.sub(r'^the ', '', s, flags=re.I)
    return s[:1].upper() + s[1:]


def build(prev):
    text = corrected_text()
    words = IB.parse(text)                      # verbatim card texts, keyed by the GD deck's ids
    rows = titles(text)
    gd = {it['id']: it for it in json.load(open(GD, encoding='utf-8'))['nodes']}
    keep = {it['id']: it for it in (prev or {}).get('nodes', [])}
    items = []
    for no in range(1, 79):
        r, gid = rows[no], gd_id(rows[no])
        g = gd[gid]
        gm = g.get('metadata') or {}
        body = words[gid]
        for k, v in DOTS_MD.items():
            body = body.replace(k, v)
        assert not re.search('[-]', body), gid
        suit = r.get('suit')
        md = {'book_t_no': no}
        kw = ['book t', 'golden dawn']
        if r['kind'] == 'key':
            card = r['card']
            md.update(arcana='major', number=r['key'], key_number=r['key'], trump_number=r['key'],
                      trump_key=gm.get('trump_key'), card_name_1912=card,
                      hebrew_letter=gm.get('hebrew_letter'), hebrew_translit=gm.get('hebrew_translit'),
                      tree_path=gm.get('tree_path'), attribution=r['attribution'])
            assert r['attribution'].lower().startswith(re.sub(r'^the ', '', (gm.get('attribution') or '').lower())[:4]) \
                or r['key'] in (20, 21), (no, r['attribution'], gm.get('attribution'))
            row = ('No. %d of Book T\'s 78 titles · **%s**, Key %d · letter %s %s · %s'
                   % (no, card, r['key'], gm.get('hebrew_letter'), gm.get('hebrew_translit'), r['attribution']))
            if r['key'] in (8, 11):
                row += ('\n\nBook T numbers Justice 8 and Fortitude 11, and seats Fortitude on Leo, '
                        'the letter Teth, in the eighth place among the Keys.')
            category = 'keys'
            kw += [card.lower().replace('the ', ''), (gm.get('hebrew_translit') or '').lower(),
                   r['attribution'].lower(), 'key', 'major arcana']
        elif r['kind'] == 'ace':
            card = 'Ace of %s' % SUIT_NAME[suit]
            md.update(arcana='minor', number=1, suit=SUIT_NAME[suit], element=ELEMENT[suit], rank='Ace', pip=1,
                      sephirah=gm.get('sephirah'), world=gm.get('world'), card_name_1912=card)
            row = "No. %d of Book T's 78 titles · **%s** · %s" % (no, card, ELEMENT[suit])
            category = 'aces'
            kw += [suit, ELEMENT[suit].lower(), 'ace', 'root']
        elif r['kind'] == 'court':
            rank = RANK_1912[r['rank']]
            card = '%s of %s' % (rank, SUIT_NAME[suit])
            c1912 = '%s of %s' % (r['rank'], SUIT_NAME[suit])
            md.update(arcana='minor', suit=SUIT_NAME[suit], element=ELEMENT[suit], rank=rank, court=True,
                      card_name_1912=c1912, element_in_element=gm.get('element_in_element'), rules=gm.get('rules'))
            row = "No. %d of Book T's 78 titles · **%s**" % (no, card)
            if c1912 != card:
                row += " (the 1912 list calls it the %s)" % c1912
            row += ' · %s' % gm.get('element_in_element')
            category = 'courts'
            kw += [suit, ELEMENT[suit].lower(), rank.lower(), 'court card']
        else:
            card = '%s of %s' % (WORD[r['pip']], SUIT_NAME[suit])
            decan = '%s in %s' % (r['planet'], r['sign'])
            assert decan.lower() == (gm.get('decan') or '').lower(), (no, decan, gm.get('decan'))
            md.update(arcana='minor', number=r['pip'], suit=SUIT_NAME[suit], element=ELEMENT[suit], pip=r['pip'],
                      decan=decan, planet=r['planet'], sign=r['sign'], sephirah=gm.get('sephirah'),
                      world=gm.get('world'), card_name_1912=card)
            row = "No. %d of Book T's 78 titles · **%s** · decan: %s" % (no, card, decan)
            category = 'decans'
            kw += [suit, ELEMENT[suit].lower(), decan.lower(), 'decan']
        title = no_the(r['title'])
        md['title'] = r['title'][:1].upper() + r['title'][1:]
        md['archetype'] = gm.get('archetype')
        md['illustrations'] = []
        row += '\n\n[Read it on the 1912 page](%s#%s)' % (PAGE, gid)
        nid = new_id(r)
        sections = {
            'Book T (1912)': IB.HEADER + '\n\n' + body,
            "In Book T's table": row,
            'Correspondences': g['sections']['Correspondences'],
        }
        item = {'id': nid, 'name': title, 'sort_order': no - 1, 'category': category,
                'keywords': [k for k in dict.fromkeys(kw) if k], 'image_url': '',
                'metadata': {k: v for k, v in md.items() if v is not None}, 'sections': sections}
        old = keep.get(nid)
        if old:                                   # keep what PlayfulProcess (or the app) added
            item['image_url'] = old.get('image_url', '')
            if (old.get('metadata') or {}).get('illustrations'):
                item['metadata']['illustrations'] = old['metadata']['illustrations']
            for k, v in (old.get('sections') or {}).items():
                if k not in OWNED:
                    item['sections'][k] = v
        items.append(item)
    assert len({i['id'] for i in items}) == 78
    assert not any(re.search(r'\d', i['name']) for i in items), 'a card name carries a number'
    for n, (gid, name, cat, anchor, line) in enumerate(GROUPS):
        items.append({'id': gid, 'name': name, 'sort_order': 78 + n, 'category': 'chapter',
                      'parts': [i['id'] for i in items if i.get('category') == cat],
                      'relationship_type': 'emergence', 'metadata': {},
                      'sections': {'About': '*This site\'s note.* ' + line +
                                   ' [Read the chapter on the 1912 page](%s#%s).' % (PAGE, anchor)}})
    g = {
        '_github_url': 'https://github.com/PlayfulProcess/recursive-tarot/blob/main/tarot/book-t/grammar.json',
        '_github_source_url': 'https://raw.githubusercontent.com/PlayfulProcess/recursive-tarot/main/tarot/book-t/grammar.json',
        '_grammar_commons': {
            'schema_version': '1.0', 'license': 'CC-BY-SA-4.0',
            'attribution': [
                {'name': 'S.L. MacGregor Mathers / Hermetic Order of the Golden Dawn', 'date': 'c. 1888',
                 'note': 'Book T: the cards, their titles, attributions and meanings'},
                {'name': 'Aleister Crowley (ed.), The Equinox I(8)', 'date': '1912',
                 'note': 'First printing of Book T, pp. 143-210; his notes in square brackets'},
                {'name': 'the-equinox.org', 'date': 'transcription',
                 'note': 'Transcription used, checked against the scan of the 1912 issue (archive.org)'},
                {'name': 'PlayfulProcess', 'date': '2026', 'note': 'This deck; the pictures, as they come'},
            ]},
        '_source': {'single_source': 'Book T, as printed in The Equinox I(8), 1912',
                    'section': 'Book T (1912)', 'rule': 'one source per deck — see GRAMMAR_FORMAT.md',
                    'built_by': 'scripts/build_book_t_deck.py'},
        'name': 'Book T — The Golden Dawn\'s 78 Cards',
        'description': DESCRIPTION,
        'grammar_type': 'tarot',
        'provenance': 'record',
        'creator_name': 'PlayfulProcess',
        'creator_link': 'https://recursive.eco',
        'cover_image_url': '',
        'tags': ['tarot', 'golden-dawn', 'book-t', 'equinox-1912', 'kabbalah', 'decans', 'astrology',
                 'esoteric', 'public-domain', 'tree-of-life'],
        'roots': ['western-esoteric', 'mysticism'],
        'shelves': ['wonder', 'mirror'],
        'worldview': 'esoteric',
        'is_published': False,
        '_community_folder': 'tarot',
        '_community_slug': 'book-t',
        'image_credit': 'No pictures yet: PlayfulProcess adds them over time.',
        'metadata': {'common_name': 'Book T', 'category': 'historical', 'year': 1912,
                     'year_label': 'c. 1888 · printed 1912'},
        'nodes': items,
    }
    if prev:                                       # keep deck-level edits made after the first build
        for k in ('cover_image_url', 'is_published', 'image_credit'):
            if k in prev and prev[k] != g[k] and prev[k] not in ('', None):
                g[k] = prev[k]
        for k, v in prev.items():
            if k not in g:
                g[k] = v
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    prev = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else None
    g = build(copy.deepcopy(prev))
    out = json.dumps(g, ensure_ascii=False, indent=2) + '\n'
    cur = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
    if a.check:
        print('[build_book_t_deck] --check: %s' % ('up to date' if cur == out else 'out of date; run: python scripts/build_book_t_deck.py'))
        sys.exit(0 if cur == out else 1)
    if cur != out:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(out)
    print('[build_book_t_deck] %s: %d cards, %d chapters' % ('written' if cur != out else 'unchanged', 78, len(GROUPS)))


if __name__ == '__main__':
    main()
