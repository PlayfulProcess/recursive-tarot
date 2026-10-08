# -*- coding: utf-8 -*-
"""Etteilla's own words on the three Etteilla decks (Oct 8 2026, one-shot, idempotent).

  python scripts/archive/etteilla_own_words_2026_10_08.py [--check]

Source: research/sources/etteilla-dictionnaire-synonimique-1791.md, a transcription of the head-words
of the "Table des synonimes du Livre de Thot, suivant l'ordre des feuillets" in the *Dictionnaire
synonimique du Livre de Thot* (Paris, 1791), pp. 19-57, checked against the page images of the
BIU Sante copy on archive.org (BIUSante_55509). Its preface (p. 4) says these words were printed on
each leaf by Etteilla. The script reads the table in that file.

For each of the 78 cards of etteilla-i-livre-de-thot, etteilla-ii-egyptian and
etteilla-iii-oracle-des-dames:
  * `Upright` and `Reversed` become Etteilla's word as printed, this site's English translation,
    and the source with page and scan link. Etteilla II and III say the words are those of his own
    1789 deck and that their own printed captions are not transcribed here.
  * The paraphrases they replace (22 trump Upright + Reversed, 16 court
    `Upright (the person well-disposed)`) move to tarot/_archive/etteilla-paraphrases-2026-10-08.json.
  * The 40 number cards lose the "no transcription ... given here yet" sentence.
  * The three Knights whose word is an event (Depart, Arrivee, Utilite) say so, since the court
    note says every court is a person.
  * On Etteilla II and III, card 78 stops calling La Folie the female querent (leaf 8 is
    "Eteilla ou la Questionnante" in the 1791 table; Etteilla I was already corrected).
  * The PlayfulProcess attribution note says where the words now come from.
"""
import argparse, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SOURCE = os.path.join(ROOT, 'research', 'sources', 'etteilla-dictionnaire-synonimique-1791.md')
SOURCE_URL = ('https://github.com/PlayfulProcess/recursive-tarot/blob/main/research/sources/'
              'etteilla-dictionnaire-synonimique-1791.md')
ARCHIVE = os.path.join(ROOT, 'tarot', '_archive', 'etteilla-paraphrases-2026-10-08.json')
DECKS = ['etteilla-i-livre-de-thot', 'etteilla-ii-egyptian', 'etteilla-iii-oracle-des-dames']
SCAN = 'https://archive.org/details/BIUSante_55509/page/n{n}/mode/1up'

SYS = "Card in Etteilla's System"
COURT_OLD = 'Upright (the person well-disposed)'
PIP_NOTE_OLD = (" Etteilla printed his upright and reversed words on the card itself; no transcription "
                "or source for them is given here yet.")
PIP_NOTE_NEW = " Etteilla's own words for this card, upright and reversed, are below."
KNIGHT_NOTE = (" This Knight's word, though, names an event rather than a person (see Upright and "
               "Reversed below).")
KNIGHTS_EVENT = {24, 38, 66}
FOLIE_OLD = "La Folie — the female querent (significator)"
FOLIE_NEW = ("La Folie — the Fool (0), the unnumbered card left outside the running count. (Not the female "
             "querent: that significator is Card 8, \"Eteilla ou la Questionnante\" in the 1791 table.)")
PARA_MARK = 'paraphrased from modern'

COMMONS_OLD = ("Reversed meanings are kept on the 22 trumps only, paraphrased from reconstructions of his "
               "tables; the pip and court reversals, which were not his, were removed in October 2026, and so "
               "were the number cards' upright lines (one template across the suits). The trump and court "
               "upright lines are paraphrases, labelled as such")
COMMONS_NEW = ("Since October 2026 every card's Upright and Reversed is Etteilla's own word for that leaf, as "
               "the Dictionnaire synonimique du Livre de Thot (Paris, 1791) records it, with this site's "
               "English translation (research/sources/etteilla-dictionnaire-synonimique-1791.md); the earlier "
               "paraphrases are archived")

SRC_SENTENCE = ("in Etteilla's words: the* Dictionnaire synonimique du Livre de Thot *(Paris, 1791), p. {p} "
                "([scan]({url})), whose preface says he printed these words on each leaf. French as printed; "
                "English, this site's translation. [Source notes]({src}).*")
LATER = ("\n\n*Words of his own deck (1789). This later edition's printed captions may differ and are not "
         "transcribed here.*")
NO_R = (" *The 1791 printing sets this second word without its usual \"R.\" (reversed) mark; it stands "
        "where every other leaf's reversed word stands.*")


def read_table():
    rows = {}
    for line in open(SOURCE, encoding='utf-8'):
        m = re.match(r'^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| ([\d-]+) \|\s*$', line)
        if not m:
            continue
        leaf = int(m.group(1))
        pages = [int(x) for x in m.group(6).split('-')]
        rows[leaf] = {'up': m.group(2), 'up_en': m.group(3), 'rv': m.group(4), 'rv_en': m.group(5),
                      'p_up': pages[0], 'p_rv': pages[-1]}
    assert len(rows) == 78 and set(rows) == set(range(78)), sorted(rows)
    return rows


def text(r, side, later, leaf):
    word, en, page = (r['up'], r['up_en'], r['p_up']) if side == 'up' else (r['rv'], r['rv_en'], r['p_rv'])
    if side == 'up' and leaf == 8:
        head = ("**%s** (so spelled), on the leaf headed **Repos** — *Etteilla, or the Questioner "
                "(the woman who asks); Rest.*" % word)
    else:
        head = '**%s** — *%s.*' % (word, en[0].upper() + en[1:])
    label = 'Upright' if side == 'up' else 'Reversed'
    out = (head + "\n\n*" + label + ", "
           + SRC_SENTENCE.format(p=page, url=SCAN.format(n=page + 3), src=SOURCE_URL))
    if side == 'rv' and leaf in (9, 71):
        out += NO_R
    if later:
        out += LATER
    return out


def load(slug):
    p = os.path.join(ROOT, 'tarot', slug, 'grammar.json')
    raw = open(p, encoding='utf-8', newline='').read()
    crlf = '\r\n' in raw
    return p, json.loads(raw.replace('\r\n', '\n')), raw, crlf


def dump(g, raw, crlf):
    out = json.dumps(g, ensure_ascii=False, indent=2) + ('\n' if raw.replace('\r\n', '\n').endswith('\n') else '')
    return out.replace('\n', '\r\n') if crlf else out


def rebuild(sections, new_up, new_rv, after):
    """Return sections with Upright/Reversed placed right after `after`, the court label dropped."""
    out = {}
    for k, v in sections.items():
        if k in ('Upright', 'Reversed', COURT_OLD):
            continue
        out[k] = v
        if k == after:
            out['Upright'] = new_up
            out['Reversed'] = new_rv
    if 'Upright' not in out:
        out['Upright'] = new_up
        out['Reversed'] = new_rv
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    rows = read_table()

    archive = {'_about': ("Paraphrases of Etteilla's meanings, moved off the three Etteilla decks on 2026-10-08 "
                          "when each card got Etteilla's own words from the Dictionnaire synonimique du Livre de "
                          "Thot (1791). They were labelled on the cards as paraphrase of modern reconstructions, "
                          "not his words. Kept by deck, item id and section. Written by "
                          "scripts/archive/etteilla_own_words_2026_10_08.py."),
               'decks': {}}
    if os.path.exists(ARCHIVE):
        archive = json.load(open(ARCHIVE, encoding='utf-8'))
    pending, counts = {}, {}

    def bump(k, n=1):
        if n:
            counts[k] = counts.get(k, 0) + n

    for di, slug in enumerate(DECKS):
        later = di > 0
        p, g, raw, crlf = load(slug)
        for it in g['items'][:]:
            m = re.match(r'^(?:etteilla|oracle-dames)-(\d\d)$', it.get('id', ''))
            if not m:
                continue
            num = int(m.group(1))
            leaf = 0 if num == 78 else num
            r = rows[leaf]
            s = it.get('sections') or {}
            new_up, new_rv = text(r, 'up', later, leaf), text(r, 'rv', later, leaf)
            if s.get('Upright') == new_up and s.get('Reversed') == new_rv and COURT_OLD not in s:
                continue
            old = {k: s[k] for k in ('Upright', 'Reversed', COURT_OLD)
                   if isinstance(s.get(k), str) and PARA_MARK in s[k]}
            if old:
                archive['decks'].setdefault(slug, {}).setdefault(it['id'], {}).update(old)
                bump(slug + ' paraphrases archived', len(old))
            sysv = s.get(SYS)
            if isinstance(sysv, str):
                if PIP_NOTE_OLD in sysv:
                    sysv = sysv.replace(PIP_NOTE_OLD, PIP_NOTE_NEW)
                    bump(slug + ' pip notes replaced')
                if num in KNIGHTS_EVENT and KNIGHT_NOTE not in sysv:
                    sysv = sysv.rstrip() + KNIGHT_NOTE
                    bump(slug + ' knight notes')
                if sysv.strip() == FOLIE_OLD:
                    sysv = FOLIE_NEW
                    bump(slug + ' folie fixed')
                s[SYS] = sysv
            it['sections'] = rebuild(s, new_up, new_rv, SYS)
            bump(slug + ' cards written')
        for att in g.get('_grammar_commons', {}).get('attribution', []):
            n = att.get('note') or ''
            if COMMONS_OLD in n:
                att['note'] = n.replace(COMMONS_OLD, COMMONS_NEW)
                bump(slug + ' commons')
        out = dump(g, raw, crlf)
        if out != raw:
            pending[p] = out

    print('[etteilla_own_words_2026_10_08]', json.dumps(counts))
    if a.check:
        print('--check: %s' % ('up to date' if not pending else '%d files would change' % len(pending)))
        sys.exit(1 if pending else 0)
    for p, out in pending.items():
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(out)
    if any(k.endswith('paraphrases archived') for k in counts):
        with open(ARCHIVE, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(archive, fh, ensure_ascii=False, indent=2)
            fh.write('\n')
    print('wrote %d grammar files' % len(pending))


if __name__ == '__main__':
    main()
