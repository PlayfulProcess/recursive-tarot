# One-off of Oct 5 2026 (history, not tooling; see scripts/archive/README.md). Reads the WordPress API
# dumps of stolen-thyme.com and Yve Lepkowski's Downloads ZIPs from the folder this file sits in.
"""Parse Yve Lepkowski's guidebook pages (WordPress API dumps) into blocks: the text outside the
accordions, and each accordion section (<details><summary>Title</summary>...)."""
import json, glob, re, html, os

S = os.path.dirname(os.path.abspath(__file__))


def clean(s):
    s = html.unescape(re.sub(r'<br\s*/?>', '\n', s))
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'[ \t]+', ' ', s).strip()


def paras(fragment):
    out = []
    for m in re.finditer(r'<(p|li)[^>]*>(.*?)</\1>', fragment, re.S):
        t = clean(m.group(2))
        if t:
            out.append(('li' if m.group(1) == 'li' else 'p', t))
    return out


def parse(raw):
    sections = {}
    for m in re.finditer(r'<details>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>', raw, re.S):
        sections[clean(m.group(1))] = paras(m.group(2))
    outside = re.sub(r'<details>.*?</details>', '', raw, flags=re.S)
    return {'outside': paras(outside), 'sections': sections}


def load_pages():
    pages = {}
    for f in sorted(glob.glob(os.path.join(S, 'yve-pages-*.json'))):
        for it in json.load(open(f, encoding='utf-8')):
            pages[it['link']] = {'title': clean(it['title']['rendered']), 'raw': it['content']['rendered']}
    return pages


if __name__ == '__main__':
    P = load_pages()
    for k in ('https://stolen-thyme.com/anecdotes-tarot/guidebook/the-suit-of-coins/nine-of-coins/',
              'https://stolen-thyme.com/clown-town-tarot/guidebook/two-of-batons/',
              'https://stolen-thyme.com/tarocchino-arlecchino/guidebook/11-le-vieillard/'):
        p = parse(P[k]['raw'])
        print('=====', P[k]['title'])
        print('  outside:', [(t, len(x), x[:50]) for t, x in p['outside']][2:] if 'anecdotes' in k else [(t, len(x), x[:50]) for t, x in p['outside']])
        for s, ps in p['sections'].items():
            print('  [' + s + ']', [(t, len(x), x[:50]) for t, x in ps])
