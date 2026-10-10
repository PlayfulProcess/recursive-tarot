"""Text-first comparison of the five Yve Lepkowski grammars with stolen-thyme.com.

Corpus: every page and post (text, plus each <img alt> as its own document named by the image file),
and every media item (title, description, caption, alt text), from the WordPress API dumps.
For each of our sections that should be her words: find the document holding most of its sentences,
then ask (1) are all its sentences hers, verbatim? (2) does that document belong to the same card?
Never prints lyrics: "Song reference" is skipped, and quoted spans are ignored.

  python scripts/audit_yve_decks.py <dump-dir>

<dump-dir> holds the WordPress API pages, fetched with curl (not committed):
  yve-pages-N.json  https://stolen-thyme.com/wp-json/wp/v2/pages?per_page=100&page=N&_fields=link,content,title
  yve-posts-N.json  https://stolen-thyme.com/wp-json/wp/v2/posts?per_page=100&page=N&_fields=link,content,title
  yvemedia-N.json   https://stolen-thyme.com/wp-json/wp/v2/media?per_page=100&page=N&_fields=id,link,title,caption,description,alt_text,source_url,post
It writes <dump-dir>/yve-audit2.json. Report of the Oct 5 2026 run: docs/rights/YVE-DECKS-AUDIT-2026-10-05.md.
"""
import json, glob, re, html, os, sys, unicodedata
from collections import defaultdict

S = sys.argv[1] if len(sys.argv) > 1 else '.'
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECKS = ['tarocchino-arlecchino', 'clown-town-tarot', 'anecdotes-tarot', 'petit-lenormand', 'arlecchinos-augmented-arcana']
NOT_HERS = {'Traditional meaning', 'Song reference', 'Also called'}
NUM = {'ace': 1, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
       'as': 1, 'deux': 2, 'trois': 3, 'quatre': 4, 'cinq': 5, 'sept': 7, 'huit': 8, 'neuf': 9, 'dix': 10,
       'asso': 1, 'due': 2, 'tre': 3, 'quattro': 4, 'cinque': 5, 'sei': 6, 'sette': 7, 'otto': 8, 'nove': 9, 'dieci': 10}
SUIT = {'batons': 'batons', 'baton': 'batons', 'wands': 'batons', 'bastoni': 'batons', 'baston': 'batons',
        'cups': 'cups', 'cup': 'cups', 'chalices': 'cups', 'coppe': 'cups', 'coupe': 'cups',
        'swords': 'swords', 'sword': 'swords', 'spade': 'swords', 'epee': 'swords', 'depee': 'swords',
        'coins': 'coins', 'coin': 'coins', 'pentacles': 'coins', 'denari': 'coins', 'denier': 'coins', 'deniers': 'coins'}
RANK = {'knave': 'page', 'page': 'page', 'maid': 'page', 'valet': 'page', 'fante': 'page', 'knight': 'knight',
        'cavalier': 'knight', 'cavallo': 'knight', 'chevalier': 'knight', 'cavaliere': 'knight', 'fanti': 'page', 'regine': 'queen', 'queen': 'queen', 'reine': 'queen', 'regina': 'queen',
        'king': 'king', 'roi': 'king', 're': 'king'}


def norm(s):
    s = unicodedata.normalize('NFKD', html.unescape(s or ''))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-')
    s = re.sub(r'[*_#>`]', '', s)
    s = re.sub(r'"[^"]{0,200}"', ' ', s)
    s = re.sub(r"(?<![a-z])'[^']{0,120}'(?![a-z])", ' ', s)
    return re.sub(r'\s+', ' ', s).strip().lower()


def strip(rendered):
    t = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', ' ', rendered)
    return norm(re.sub(r'<[^>]+>', ' ', t))


docs = []
for f in sorted(glob.glob(os.path.join(S, 'yve-pages-*.json')) + glob.glob(os.path.join(S, 'yve-posts-*.json'))):
    for it in json.load(open(f, encoding='utf-8')):
        raw = it['content']['rendered']
        docs.append({'link': it['link'], 'ident': norm(it['title']['rendered']) + ' ' + it['link'].rstrip('/').split('/')[-1], 'text': strip(raw)})
        for m in re.finditer(r'<img[^>]+>', raw):
            tag = m.group(0)
            alt = re.search(r'alt="([^"]*)"', tag)
            src = re.search(r'src="([^"]*)"', tag)
            if alt and len(alt.group(1)) > 40:
                fname = os.path.basename((src.group(1) if src else '').split('?')[0])
                docs.append({'link': it['link'] + '#img:' + fname, 'ident': norm(fname), 'text': norm(alt.group(1))})
for f in sorted(glob.glob(os.path.join(S, 'yvemedia-*.json'))):
    for m in json.load(open(f, encoding='utf-8')):
        text = ' '.join(strip(m[k]['rendered']) for k in ('description', 'caption') if isinstance(m.get(k), dict)) + ' ' + norm(m.get('alt_text', ''))
        if len(text.strip()) > 40:
            docs.append({'link': m['link'], 'ident': norm(m['title']['rendered']) + ' ' + os.path.basename(m.get('source_url', '')), 'text': text})


def identity(s):
    s = norm(s)
    s = re.sub(r'\.(png|jpe?g)\b', ' ', s)
    w = re.findall(r'[a-z]+|\d+', s.replace('_', ' ').replace('-', ' '))
    suit = next((SUIT[x] for x in w if x in SUIT), None)
    rank = next((RANK[x] for x in w if x in RANK), None)
    num = next((NUM[x] for x in w if x in NUM), None)
    if num is None and not suit:
        num = next((int(x) for x in w if x.isdigit() and int(x) < 80), None)
    words = {x for x in w if len(x) > 3 and x not in SUIT and x not in RANK and x not in NUM and x not in ('png', 'jpeg', 'card', 'tarot', 'resize', 'scaled')}
    return suit, rank, num, words


def same_card(ours, theirs):
    s1, r1, n1, w1 = ours
    s2, r2, n2, w2 = theirs
    if s1 and s2:
        if s1 != s2:
            return False
        if r1 or r2:
            return r1 == r2
        if n1 is None or n2 is None:
            return None
        return n1 == n2 if (n1 and n2) else None
    if w1 & w2:
        return True
    if n1 is not None and n2 is not None:
        return n1 == n2
    return None


def sentences(t):
    return [x for x in re.split(r'(?<=[.!?;])\s+|\n+', norm(t)) if len(x) > 25]


out = {}
for deck in DECKS:
    g = json.load(open(os.path.join(REPO, 'tarot', deck, 'grammar.json'), encoding='utf-8'))
    rows = []
    for it in g['nodes']:
        md = it.get('metadata') or {}
        ours = identity(' '.join(str(x) for x in (it.get('name'), md.get('italian_name'), md.get('traditional_name'), md.get('lenormand_number'), md.get('rank'), md.get('suit')) if x))
        for sec, val in (it.get('sections') or {}).items():
            if sec in NOT_HERS or not isinstance(val, str):
                continue
            sents = sentences(val)
            if not sents:
                continue
            score = defaultdict(int)
            for d_i, d in enumerate(docs):
                for x in sents:
                    if x in d['text']:
                        score[d_i] += 1
            if score:
                best = max(score, key=lambda k: (score[k], -len(docs[k]['text'])))
                d = docs[best]
                match = same_card(ours, identity(d['ident']))
                found_any = sum(1 for x in sents if any(x in dd['text'] for dd in docs))
            else:
                d, match, found_any = None, None, 0
            rows.append({'id': it['id'], 'name': it.get('name'), 'section': sec, 'sentences': len(sents),
                         'found_on_best': score[best] if score else 0, 'found_anywhere': found_any,
                         'best_doc': d['link'] if d else None, 'best_ident': d['ident'] if d else None,
                         'same_card': match,
                         'missing': [x[:150] for x in sents if not any(x in dd['text'] for dd in docs)][:4]})
    out[deck] = rows

json.dump(out, open(os.path.join(S, 'yve-audit2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for deck, rows in out.items():
    tot = sum(r['sentences'] for r in rows)
    anyw = sum(r['found_anywhere'] for r in rows)
    wrong = [r for r in rows if r['same_card'] is False]
    unsure = [r for r in rows if r['same_card'] is None and r['best_doc']]
    none = [r for r in rows if not r['best_doc']]
    print(f'## {deck}: sections={len(rows)} sentences={tot} found verbatim on her site={anyw} ({100*anyw/max(1,tot):.0f}%)')
    print(f'   text sitting on a DIFFERENT card of hers: {len(wrong)}')
    for r in wrong[:10]:
        print(f'     - {r["name"]} / {r["section"]} -> {r["best_ident"][:70]}')
    print(f'   identity unclear: {len(unsure)}; no source found: {len(none)} {[r["name"]+"/"+r["section"] for r in none][:6]}')
