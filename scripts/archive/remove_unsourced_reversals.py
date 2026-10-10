# -*- coding: utf-8 -*-
"""Reversed meanings only where a source gives them (one-shot, Oct 7 2026).

  python scripts/archive/remove_unsourced_reversals.py [--check]

PlayfulProcess, after a reading where the Golden Dawn deck's "Reversed /
Ill-Dignified" lines turned out to be editorial (Book T has no reversals): "I would delete any
reverse meaning that was not there." The tradition's own text stays; reversed lines that no
source for that deck gave are moved out, into
`tarot/_archive/unsourced-reversals-2026-10-07.json` (kept, by deck and item id).

Per deck:
  * tarot-de-marseille-conver (78 Reversed): removed. The deck's own dossier says no native
    upright/reversed meaning exists for these cards (research/decks/tarot-de-marseille-conver.md;
    research/cards/tarot-de-marseille-conver.md, after Decker 1996, Dummett 1980). The Tradition
    Note on every card now says no reversed meanings are given.
  * oswald-wirth-tarot (22 Reversed): removed. The deck's `Wirth` sections (his 1927 text) give no
    reversed meanings, and research/cards/oswald-wirth-tarot.md cites no source for them.
  * etteilla-i / -ii / -iii: Etteilla did print reversed meanings, so the 22 trumps keep theirs
    (paraphrases cited to Benebell Wen's reconstruction and the etteillastrumps translation in
    research/cards/etteilla-*.md), now labelled as paraphrase. Two lines that the cited research
    does not support are replaced by its wording (card 8 in all three decks; card 13 in Etteilla I,
    where II/III's research supports the current line). The 40 pip reversals (one template
    repeated across the four suits) and the 16 court reversals ("the person ill-disposed") were not
    Etteilla's and had no source: removed, with the court sentence that promised them.
  * golden-dawn-book-t-tarot: nothing here; its `Reversed / Ill-Dignified` left the repo with
    PR #43 (tarot/_archive/golden-dawn-editorial-2026-10-05.json). Book T's own "if ill dignified"
    sentences sit inside `Book T (1912)` and stay.
  * rider-waite-smith-pictorial-key (Waite's own text) and Yve Lepkowski's two Arlecchino decks
    (her guidebook's Etteilla-system meanings, PR #45) are not touched.

Idempotent; `--check` writes nothing and exits 1 if anything would change.
"""
import argparse, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ARCHIVE = os.path.join(ROOT, 'tarot', '_archive', 'unsourced-reversals-2026-10-07.json')

ETTEILLA = ['etteilla-i-livre-de-thot', 'etteilla-ii-egyptian', 'etteilla-iii-oracle-des-dames']
TAG = "*Etteilla's reversed sense, paraphrased from modern reconstructions of his tables (not his words).*"
# Card 8 (all three decks) and card 13 (Etteilla I): the research file's own wording, cited there.
REPLACE = {
    (None, 8): ('Imitation; the Garden of Eden; effervescence, fermentation.',
                'research/cards/etteilla-i-livre-de-thot.md, card 8 [@web_etteillastrumps]'),
    ('etteilla-i-livre-de-thot', 13): ('A union broken; an unequal or false bond.',
                                       'research/cards/etteilla-i-livre-de-thot.md, card 13 [@web_etteillastrumps]'),
}
COURT_SENTENCE = ' Upright the person is well-disposed; reversed, ill-disposed.'
COMMONS_OLD = "Grammar architecture; readings rewritten within Etteilla's tradition"
COMMONS_NEW = ("Grammar architecture; readings rewritten within Etteilla's tradition. Reversed meanings "
               "are kept on the 22 trumps only, paraphrased from reconstructions of his tables; the pip "
               "and court reversals, which were not his, were removed in October 2026")

CONVER_OLD = ("The upright and reversed meanings here are a later overlay, added by Etteilla and the "
              "occultists from the 1780s onward; they are not part of the deck's original tradition.")
CONVER_NEW = ("The upright meanings here are a later overlay, added by Etteilla and the occultists from "
              "the 1780s onward; they are not part of the deck's original tradition. No reversed "
              "meanings are given: none belong to this deck.")

REASONS = {
    'tarot-de-marseille-conver': ('No source gives reversed meanings for the Marseille pattern: a game pack, '
                                  'meanings a post-1780s overlay (research/decks/tarot-de-marseille-conver.md, '
                                  'after Decker 1996 and Dummett 1980).'),
    'oswald-wirth-tarot': ("Wirth's own text (the `Wirth` sections) gives no reversed meanings; "
                           'research/cards/oswald-wirth-tarot.md cites no source for them.'),
    'etteilla': ("Not Etteilla's: the pip lines were one template repeated across the four suits and the "
                 'court lines ("the person ill-disposed") were invented; no source in the repo gives them.'),
}


def card_no(item_id):
    m = re.search(r'-(\d+)$', item_id)
    return int(m.group(1)) if m else None


def load(slug):
    p = os.path.join(ROOT, 'tarot', slug, 'grammar.json')
    raw = open(p, encoding='utf-8', newline='').read()
    crlf = '\r\n' in raw
    return p, json.loads(raw.replace('\r\n', '\n')), raw, crlf


def dump(g, raw, crlf):
    out = json.dumps(g, ensure_ascii=False, indent=2) + ('\n' if raw.replace('\r\n', '\n').endswith('\n') else '')
    return out.replace('\n', '\r\n') if crlf else out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    archive = {'_about': ('Reversed meanings moved off the decks on 2026-10-07 because no source for that deck '
                          'gave them (PlayfulProcess: "I would delete any reverse meaning that was not '
                          'there"). Kept by deck and item id. Written by scripts/archive/remove_unsourced_reversals.py.'),
               'reasons': REASONS, 'decks': {}}
    if os.path.exists(ARCHIVE):
        archive = json.load(open(ARCHIVE, encoding='utf-8'))
    pending = {}
    counts = {}

    def move(slug, item, label, reason_key):
        moved = archive['decks'].setdefault(slug, {}).setdefault(item['id'], {})
        moved[label] = item['sections'].pop(label)
        moved['_reason'] = reason_key
        counts[slug] = counts.get(slug, 0) + 1

    for slug in ['tarot-de-marseille-conver', 'oswald-wirth-tarot'] + ETTEILLA:
        p, g, raw, crlf = load(slug)
        for it in g['nodes']:
            s = it.get('sections') or {}
            if slug == 'tarot-de-marseille-conver':
                if 'Reversed' in s:
                    move(slug, it, 'Reversed', slug)
                if isinstance(s.get('Tradition Note'), str) and CONVER_OLD in s['Tradition Note']:
                    s['Tradition Note'] = s['Tradition Note'].replace(CONVER_OLD, CONVER_NEW)
            elif slug == 'oswald-wirth-tarot':
                if 'Reversed' in s:
                    move(slug, it, 'Reversed', slug)
            else:
                major = it.get('category') == 'major'
                if not major:
                    for label in ('Reversed', 'Reversed (the person ill-disposed)'):
                        if label in s:
                            move(slug, it, label, 'etteilla')
                    sysnote = s.get("Card in Etteilla's System")
                    if isinstance(sysnote, str) and COURT_SENTENCE in sysnote:
                        s["Card in Etteilla's System"] = sysnote.replace(COURT_SENTENCE, '')
                elif isinstance(s.get('Reversed'), str):
                    n = card_no(it['id'])
                    rep = REPLACE.get((slug, n)) or REPLACE.get((None, n))
                    body = s['Reversed'].split('\n\n' + TAG)[0]
                    if rep and body != rep[0]:
                        kept = archive['decks'].setdefault(slug, {}).setdefault(it['id'], {})
                        kept['Reversed (replaced)'] = body
                        kept['_reason'] = 'replaced by the cited research wording: ' + rep[1]
                        body = rep[0]
                        counts[slug + ' (replaced)'] = counts.get(slug + ' (replaced)', 0) + 1
                    s['Reversed'] = body + '\n\n' + TAG
        if slug in ETTEILLA:
            for att in g.get('_grammar_commons', {}).get('attribution', []):
                if att.get('note') == COMMONS_OLD:
                    att['note'] = COMMONS_NEW
        out = dump(g, raw, crlf)
        if out != raw:
            pending[p] = out

    print('[remove_unsourced_reversals] moved/replaced:', json.dumps(counts))
    if a.check:
        print('--check: %s' % ('up to date' if not pending else '%d files would change' % len(pending)))
        sys.exit(1 if pending else 0)
    for p, out in pending.items():
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(out)
    if counts:
        with open(ARCHIVE, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(archive, fh, ensure_ascii=False, indent=2)
            fh.write('\n')
    print('wrote %d grammar files' % len(pending))


if __name__ == '__main__':
    main()
