# -*- coding: utf-8 -*-
"""Put Book T's own words on every card of the Golden Dawn deck.

  python scripts/import_book_t_1912.py [--check] [--verify-scan OCR.txt]

PlayfulProcess, Oct 4-5 2026: where a tradition wrote its cards down, the card carries that
tradition's own text, not an AI paraphrase. Book T reached print in 1912, in *The Equinox*
I(8) (public domain; see the header of the source file). Until now this deck carried
paraphrases ("Book T's own prose is not safely public domain", a judgement made when only
Regardie's 1937-40 edition was considered).

Source: `research/sources/book-t-equinox-1912.txt` (the 1912 text, transcriber notes removed).

What it writes, on the 78 cards of `tarot/golden-dawn-book-t-tarot/grammar.json`:
  * a `Book T (1912)` section, verbatim: the full description and meaning for the 4 aces,
    16 courts and 36 numbered cards; Book T's brief meaning for each of the 22 keys;
  * it moves the editorial `Divinatory Meaning`, `Reversed / Ill-Dignified` (paraphrases) and
    the AI-written `Symbol` out of those cards, into
    `tarot/_archive/golden-dawn-editorial-2026-10-05.json` (kept, by item id).
Titles, ranks, correspondences and the research note stay as they are.

Text handling: line wraps are joined; "---" becomes a dash; lines that only draw the cups
("U U U") are dropped; Hebrew in the transcription's Latin code (HB:YSVD) is written in Hebrew
letters. Nothing else is changed. Idempotent; `--check` writes nothing and fails if the grammar
differs from what the source gives. `--verify-scan` compares every card's text with the OCR of
the 1912 scan (archive.org IAPSOP-equinox_v1_n8_1912_Sep, file *_djvu.txt) and prints how much of
it the scan confirms.
"""
import argparse, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'research', 'sources', 'book-t-equinox-1912.txt')
DECK = os.path.join(ROOT, 'tarot', 'golden-dawn-book-t-tarot', 'grammar.json')
ARCHIVE = os.path.join(ROOT, 'tarot', '_archive', 'golden-dawn-editorial-2026-10-05.json')
SECTION = 'Book T (1912)'
HEADER = ('*Book T in its own words · as printed in* The Equinox *I(8), 1912 · public domain '
          '(notes in square brackets are Crowley\'s)*')
MOVED = ('Divinatory Meaning', 'Reversed / Ill-Dignified', 'Symbol')
AFTER = ('Golden Dawn Rank', 'Golden Dawn Title')

SUITS = {'wands': 'wands', 'torches': 'wands', 'cups': 'cups', 'chalices': 'cups',
         'swords': 'swords', 'pikes': 'swords', 'spears': 'swords',
         'pentacles': 'pentacles', 'disks': 'pentacles'}
RANKS = {'ace': 'ace', 'two': '02', 'three': '03', 'four': '04', 'five': '05', 'six': '06',
         'seven': '07', 'eight': '08', 'nine': '09', 'ten': '10',
         'knight': 'knight', 'queen': 'queen', 'king': 'king', 'knave': 'page'}
BOUNDARIES = ('THE SIXTEEN COURT, OR ROYAL CARDS', 'THE SPHERES OF INFLUENCE',
              'HEREIN ARE RESUMED', 'OF THE THIRTY-SIX DECANS', 'BRIEF MEANING OF TWENTY-TWO KEYS',
              'OF THE DIGNITIES')
MAJORS = ['the-fool', 'the-magician', 'the-high-priestess', 'the-empress', 'the-emperor',
          'the-hierophant', 'the-lovers', 'the-chariot', 'strength', 'the-hermit',
          'wheel-of-fortune', 'justice', 'the-hanged-man', 'death', 'temperance', 'the-devil',
          'the-tower', 'the-star', 'the-moon', 'the-sun', 'judgement', 'the-world']

HEB = [("a'a", 'ע'), ('Ch', 'ח'), ('Sh', 'ש'), ('Th', 'ת'), ('Tz', 'צ'),
       ('A', 'א'), ('B', 'ב'), ('G', 'ג'), ('D', 'ד'), ('H', 'ה'), ('V', 'ו'), ('Z', 'ז'),
       ('T', 'ט'), ('Y', 'י'), ('K', 'כ'), ('L', 'ל'), ('M', 'מ'), ('N', 'נ'), ('S', 'ס'),
       ('O', 'ע'), ('P', 'פ'), ('Q', 'ק'), ('R', 'ר')]
# Book T numbers the keys VIII = Justice (Libra) and XI = Fortitude (Leo); this deck's cards follow
# the Rider-Waite-Smith order (8 Strength, 11 Justice). MAJORS above is in the deck's order, so a
# Book T key number must be translated before it is used as an index, or the two cards get each
# other's 1912 text (fixed Oct 6 2026). Book T's own table (source file: "11 | Fortitude",
# "8 | Justice") is asserted in `parse` so the translation can't drift from the source.
BOOK_T_TO_DECK = {8: 11, 11: 8}

FINAL = {'כ': 'ך', 'מ': 'ם', 'נ': 'ן', 'פ': 'ף', 'צ': 'ץ'}


def hebrew(code):
    out, i = [], 0
    while i < len(code):
        for lat, heb in HEB:
            if code.startswith(lat, i):
                out.append(heb)
                i += len(lat)
                break
        else:
            raise ValueError('unknown Hebrew code %r in HB:%s' % (code[i:], code))
    if len(out) > 1 and out[-1] in FINAL:
        out[-1] = FINAL[out[-1]]
    return ''.join(out)


def tidy(block):
    lines = [l.rstrip() for l in block.split('\n')]
    lines = [l for l in lines if not re.fullmatch(r'\s*(U\s*)+', l)]        # cup drawings
    while lines and re.fullmatch(r'\s*[IVXLC]*\s*', lines[-1]):             # trailing numeral
        lines.pop()
    paras, cur = [], []
    for l in lines + ['']:
        if l.strip():
            cur.append(l.strip())
        elif cur:
            paras.append(' '.join(cur))
            cur = []
    text = '\n\n'.join(paras)
    text = re.sub(r'\s*---\s*', ' — ', text)
    text = re.sub(r"HB:([A-Za-z']+)", lambda m: hebrew(m.group(1)), text)
    return re.sub(r'[ \t]{2,}', ' ', text).strip()


def parse(src_text):
    text = '\n'.join(l for l in src_text.split('\n') if not l.startswith('# '))
    head = re.compile(r"\n(?:THE )?(?:LORD|QUEEN|PRINCE|PRINCESS|ROOT)[A-Z ,;:'-]+?[ \n]+"
                      r"(Ace|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Knight|Queen|King|Knave)"
                      r" of (Wands|Cups|Chalices|Swords|Pentacles|Disks|Torches)(?: or [A-Z][a-z]+)? *\n")
    marks = [(m.start(), m.end(), m.group(1).lower(), m.group(2).lower()) for m in head.finditer(text)]
    stops = sorted([s for s, *_ in marks] + [text.find(b) for b in BOUNDARIES if text.find(b) > 0])
    cards = {}
    for start, end, rank, suit in marks:
        nxt = min(s for s in stops if s > start) if any(s > start for s in stops) else len(text)
        cid = '%s-%s' % (SUITS[suit], RANKS[rank])
        assert cid not in cards, cid
        cards[cid] = tidy(text[end:nxt])
    keys = text[text.find('BRIEF MEANING OF TWENTY-TWO KEYS'):text.find('OF THE DIGNITIES')]
    for n, name in ((8, 'Justice'), (11, 'Fortitude')):          # Book T's own key numbers
        assert re.search(r'\n\s*%d \|\s*\n\s*%s \|' % (n, name), text), 'Book T table: %d %s' % (n, name)
    for m in re.finditer(r'\n(\d{1,2})\. (.+?)(?=\n\d{1,2}\. |\Z)', keys, re.S):
        n = BOOK_T_TO_DECK.get(int(m.group(1)), int(m.group(1)))   # Book T's number -> deck's number
        # one paragraph per key; after 21 the text goes on to the table of groupings
        cards['major-%02d-%s' % (n, MAJORS[n])] = tidy(m.group(2)).split('\n\n')[0]
    return cards


def norm_words(s):
    return re.sub(r'[^a-z ]+', ' ', s.lower()).split()


def verify(cards, ocr_path):
    ocr = ' '.join(norm_words(open(ocr_path, encoding='utf-8', errors='ignore').read()))
    worst = []
    for cid, txt in sorted(cards.items()):
        w = [x for x in norm_words(re.sub(r'[֐-׿]+', ' ', txt)) if len(x) > 1]
        grams = [' '.join(w[i:i + 4]) for i in range(0, max(1, len(w) - 3), 2)]
        hit = sum(1 for g in grams if g in ocr) / max(1, len(grams))
        worst.append((hit, cid, len(w)))
    worst.sort()
    print('[verify-scan] 4-word runs of each card found in the 1912 scan OCR:')
    print('  lowest:', ', '.join('%s %.0f%% (%d words)' % (c, h * 100, n) for h, c, n in worst[:6]))
    print('  median: %.0f%%' % (100 * worst[len(worst) // 2][0]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--verify-scan')
    a = ap.parse_args()
    cards = parse(open(SRC, encoding='utf-8').read())
    if len(cards) != 78:
        sys.exit('expected 78 cards from the source, got %d' % len(cards))
    if a.verify_scan:
        verify(cards, a.verify_scan)
    raw = open(DECK, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    g = json.loads(raw)
    moved = json.load(open(ARCHIVE, encoding='utf-8'))['items'] if os.path.exists(ARCHIVE) else {}
    changed = 0
    for it in g['items']:
        if it['id'] not in cards:
            continue
        sec = it.setdefault('sections', {})
        want = HEADER + '\n\n' + cards[it['id']]
        for k in MOVED:
            if k in sec:
                moved.setdefault(it['id'], {'name': it.get('name')})[k] = sec.pop(k)
                changed += 1
        if sec.get(SECTION) != want:
            changed += 1
            new, placed = {}, False
            anchor = next((k for k in AFTER if k in sec), None)
            for k, v in sec.items():
                if k == SECTION:
                    continue
                new[k] = v
                if k == anchor:
                    new[SECTION] = want
                    placed = True
            if not placed:
                new = {SECTION: want, **new}
            it['sections'] = new
    missing = set(cards) - {i['id'] for i in g['items']}
    if missing:
        sys.exit('cards in the source but not in the deck: %s' % sorted(missing))
    if a.check:
        print('[import_book_t_1912] --check: %s' % ('up to date' if not changed else '%d changes pending' % changed))
        sys.exit(1 if changed else 0)
    if changed:
        with open(DECK, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(json.dumps(g, ensure_ascii=False, indent=2) + ('\n' if raw.endswith('\n') else ''))
        archive = {'_about': ('Editorial sections moved off the Golden Dawn deck on 2026-10-05 when Book T\'s '
                              'own 1912 text replaced them: the paraphrased "Divinatory Meaning" and '
                              '"Reversed / Ill-Dignified", and the AI-written "Symbol". Kept by item id.'),
                   'items': moved}
        with open(ARCHIVE, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(archive, fh, ensure_ascii=False, indent=2)
            fh.write('\n')
    print('[import_book_t_1912] cards=%d changes=%d archived_items=%d' % (len(cards), changed, len(moved)))


if __name__ == '__main__':
    main()
