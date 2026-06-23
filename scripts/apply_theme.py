#!/usr/bin/env python3
"""One-time refactor: make theme.css the single source of colour tokens.
For every page/viewer: link theme.css, strip local definitions of the colour tokens
theme.css now owns, and remove @media(prefers-color-scheme:dark) blocks. Fonts/shadows
are left local (theme.css also defines them, harmlessly). Idempotent."""
import re, glob, os

COLOR = ['bg','surface','panel','panel2','card','paper','chip','thumb-bg','stage','felt',
 'grammar-bg-light','grammar-bg-dark','tree-bg','tree-bg-light','ink','ink-soft','ink-strong',
 'mut','muted','faint','fg','text','grammar-text','grammar-text-muted','tree-text','tree-text-muted',
 'line','line-soft','chipline','tree-line','gold','accent','accent2','violet','grammar-accent',
 'grammar-accent-dark','tree-accent','roots','occult','native','myriads','strings','tens','sui',
 'cash','a','b','c','good','win','us','bad','lose','later']
toks = sorted(COLOR, key=len, reverse=True)
DEF = re.compile(r'--(?:' + '|'.join(map(re.escape, toks)) + r')(?![a-z0-9-])\s*:\s*[^;}]+;?')

def strip_dark(css):
    out = []; i = 0
    while True:
        m = re.search(r'@media[^{]*prefers-color-scheme\s*:\s*dark[^{]*\{', css[i:])
        if not m:
            out.append(css[i:]); break
        out.append(css[i:i + m.start()])
        j = i + m.end(); d = 1
        while j < len(css) and d > 0:
            d += 1 if css[j] == '{' else -1 if css[j] == '}' else 0
            j += 1
        i = j
    return ''.join(out)

def proc_css(css):
    return DEF.sub('', strip_dark(css))

def norm(p): return p.replace(os.sep, '/')

files = glob.glob('*.html') + ['style.css'] + glob.glob('viewers/**/*.html', recursive=True) + \
        glob.glob('pages/**/*.html', recursive=True) + glob.glob('recording/**/*.html', recursive=True)
files = sorted(set(norm(f) for f in files))

report = []
for f in files:
    if not os.path.exists(f): continue
    s = open(f, encoding='utf-8').read(); orig = s
    if f.endswith('.css'):
        s = proc_css(s)
    else:
        if 'theme.css' not in s:
            rel = '../' * f.count('/')
            link = '<link rel="stylesheet" href="' + rel + 'theme.css?v=1">'
            s = re.sub(r'(<head[^>]*>)', r'\1\n' + link, s, count=1)
        s = re.sub(r'(<style[^>]*>)(.*?)(</style>)',
                   lambda m: m.group(1) + proc_css(m.group(2)) + m.group(3), s, flags=re.S)
    if s != orig:
        open(f, 'w', encoding='utf-8', newline='').write(s)
        removed = len(DEF.findall(orig)) - len(DEF.findall(s))
        linked = ('theme.css' in s and 'theme.css' not in orig)
        report.append((f, removed, 'linked' if linked else ''))

for f, d, l in report:
    print(f'{f:44} -{d:3} defs  {l}')
print('\nfiles changed:', len(report))

if __name__ == '__main__':
    pass
