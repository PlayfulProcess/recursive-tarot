# -*- coding: utf-8 -*-
"""Due edits on the decks, Oct 8 2026 (one-shot, idempotent).

  python scripts/archive/due_edits_2026_10_08.py [--check]

PlayfulProcess's rule: the tradition's own text over AI text; AI meaning only where no tradition
wrote one, and labelled; never delete imported source text.

  * etteilla-i / -ii / -iii: the 40 number-card "Upright" lines were one template copied across
    the four suits ("the matter at its fullest ... within enterprise / love / conflict / money"),
    the same problem as the pip reversals removed on Oct 7. Etteilla printed his own upright and
    reversed words on each card, but the repo has no transcription of them and no public-domain
    printing of his tables (Papus 1889/1892 summarises his method, not his card meanings). So the
    lines move to `tarot/_archive/unsourced-pip-uprights-2026-10-08.json`, and the card says no
    source is given here. The trump and court "Upright" lines stay, labelled as paraphrase.
  * oswald-wirth-tarot (22) and tarot-de-marseille-conver (78): the "Upright" lines are summaries
    written for this site. Kept, labelled as editorial (no tradition wrote them for these decks).
  * golden-dawn-book-t-tarot: each of the 16 courts gets a short editorial note where Book T's
    figure differs from the Rider-Waite-Smith picture shown (Book T's Princes ride chariots,
    its Princesses are Amazons, its mounted Knights are the senior court), quoting Book T (1912)
    and Waite's *Pictorial Key* (1911). The 22 Keys item gets Book T's own table for a majority
    of one kind of card in a reading (The Equinox I(8), 1912, p. 205).
"""
import argparse, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ARCHIVE = os.path.join(ROOT, 'tarot', '_archive', 'unsourced-pip-uprights-2026-10-08.json')
ETTEILLA = ['etteilla-i-livre-de-thot', 'etteilla-ii-egyptian', 'etteilla-iii-oracle-des-dames']

SYS = "Card in Etteilla's System"
PIP_NOTE = (" Etteilla printed his upright and reversed words on the card itself; no transcription "
            "or source for them is given here yet.")
TRUMP_TAG = "*Etteilla's upright sense, paraphrased from modern reconstructions of his tables (not his words).*"
COURT_TAG = "*Etteilla's sense for this court, paraphrased from modern summaries of his system (not his words).*"
ETT_COMMONS_OLD = ("pip and court reversals, which were not his, were removed in October 2026")
ETT_COMMONS_NEW = ("pip and court reversals, which were not his, were removed in October 2026, and so were the "
                   "number cards' upright lines (one template across the suits). The trump and court upright "
                   "lines are paraphrases, labelled as such")

WIRTH_TAG = "*Editorial summary written for this site, not Wirth's words: his own text is in the* Wirth *section.*"
WIRTH_COMMONS_OLD = 'Grammar architecture and esoteric summaries'
WIRTH_COMMONS_NEW = "Grammar architecture and esoteric summaries (the Upright lines: editorial, not Wirth's)"

CONVER_TAG = ("*Editorial summary written for this site, after the later fortune-telling tradition; "
              "no source gives meanings for this deck.*")
CONVER_TN_OLD = ("The upright meanings here are a later overlay, added by Etteilla and the occultists from "
                 "the 1780s onward; they are not part of the deck's original tradition.")
CONVER_TN_NEW = ("The upright meanings here are editorial summaries written for this site, after the overlay "
                 "Etteilla and the occultists added from the 1780s onward; they are not part of the deck's "
                 "original tradition.")
CONVER_COMMONS_OLD = 'Grammar architecture; traditional cartomantic summaries'
CONVER_COMMONS_NEW = ('Grammar architecture; the Upright lines are editorial summaries after the later '
                      'cartomantic tradition, written for this site')

GD_HEAD = ("*Editorial note · where Book T's figure and the picture differ. The picture is Pamela Colman "
           "Smith's (1909); Waite's words are from* The Pictorial Key *(1911).*")
SENIOR = ("In Book T the mounted figure is the senior court of the suit, the old King (the 1912 printing: "
          "\"the horsed figures refer to the Yod\"); in the picture's deck the Knight ranks below the King.")
GD_COURTS = {
    'wands-knight': "Both ride. Book T's Knight is a winged warrior on a black horse with flaming mane, holding "
                    "\"a club with flaming ends\"; Waite's is \"shewn as if upon a journey, armed with a short "
                    "wand\". " + SENIOR,
    'wands-queen': "Both are a crowned queen on a throne. Book T's rests her hands on \"a couchant leopard\" and "
                   "bears a wand \"with a very heavy conical head\"; Waite's wands are \"always in leaf\", and "
                   "his description has no leopard.",
    'wands-king': "Book T's figure is a Prince: winged, \"seated on a chariot\" drawn by a lion, holding \"a torch "
                  "or fire-wand\". The picture is a King on a throne, the lion \"emblazoned on the back of his "
                  "throne\" (Waite), holding a flowering wand.",
    'wands-page': "Book T's figure is a Princess, \"a very strong and beautiful woman ... attired like an "
                  "Amazon\". The picture is a page, a young man who \"stands in the act of proclamation\" (Waite).",
    'cups-knight': "Both ride, and both wear a winged helmet. Book T's Knight rides a white horse over the sea, "
                   "and a crab issues from his cup. " + SENIOR,
    'cups-queen': "Both are a crowned queen on a throne, and both texts call her dreamy. Book T's emblems, an "
                  "ibis at her side and a crayfish issuing from her cup, are not in Waite's description.",
    'cups-king': "Book T's figure is a Prince: winged, \"seated in a chariot drawn by an eagle\" over the still "
                 "water of a lake, holding a lotus and a cup with a serpent. The picture is a King whose \"throne "
                 "is set upon the sea\", with a ship and a leaping dolphin (Waite).",
    'cups-page': "Book T's figure is a Princess, \"a beautiful Amazon-like figure\" standing on the sea, a turtle "
                 "issuing from her cup. The picture is a page who \"contemplates a fish rising from a cup\" "
                 "(Waite).",
    'swords-knight': "Both ride. Book T's Knight is winged, on a brown steed, with the star of the Twins as his "
                     "crest; Waite's is \"riding in full course, as if scattering his enemies\". " + SENIOR,
    'swords-queen': "Both are a crowned queen on a throne, holding a sword. Book T's holds in her other hand \"a "
                    "large, bearded, newly severed head of a man\"; in Waite's, \"the left hand is extended, the "
                    "arm raised\".",
    'swords-king': "Book T's figure is a Prince: winged, \"seated in a chariot drawn by Arch Fays\", with a sword "
                   "in one hand and a sickle in the other. The picture is a King who \"sits in judgment, holding "
                   "the unsheathed sign of his suit\" (Waite).",
    'swords-page': "Book T's figure is a Princess, \"an Amazon figure\", \"a mixture of Minerva and Diana\", one "
                   "hand on a small silver altar. The picture is a page who \"holds a sword upright in both "
                   "hands, while in the act of swift walking\" (Waite).",
    'pentacles-knight': "Both ride. Book T's Knight is \"a dark winged warrior\" on a light brown horse; Waite's "
                        "\"rides a slow, enduring, heavy horse\". " + SENIOR,
    'pentacles-queen': "Both texts make her dark (Book T: \"dark hair\"; Waite: \"a dark woman\"). Book T gives her a "
                       "goat by her side, \"a sceptre surmounted by a cube\" and \"an orb of gold\"; in Waite she "
                       "\"contemplates her symbol\".",
    'pentacles-king': "Book T's figure is a Prince: winged, \"seated in a chariot drawn by a bull\" over land with "
                      "many flowers. The picture is a King on a throne, where \"the bull's head should be noted "
                      "as a recurrent symbol\" (Waite).",
    'pentacles-page': "Book T's figure is a Princess, \"a strong and beautiful Amazon figure\" in a mantle of "
                      "sheepskin, near a grove of trees. The picture is a page, \"a youthful figure, looking "
                      "intently at the pentacle which hovers over his raised hands\" (Waite).",
}

MAJORITY_LABEL = 'Book T (1912)'
MAJORITY = (
    "*Book T in its own words · as printed in* The Equinox *I(8), 1912, p. 205 · public domain. Its table "
    "for a reading in which one kind of card is the majority (\"Keys\" are the trumps; Book T's "
    "\"Kings (Knights)\" are the mounted figures):*\n\n"
    "A Majority of Wands: Energy, opposition, quarrel.\n\n"
    "A Majority of Cups: Pleasure, merriment.\n\n"
    "A Majority of Swords: Trouble, sadness, sickness, death.\n\n"
    "A Majority of Pentacles: Business, money, possessions.\n\n"
    "A Majority of Keys: Strong forces beyond the Querent's control.\n\n"
    "A Majority of Court Cards: Society, meetings of many persons.\n\n"
    "A Majority of Aces: Strength generally. Aces are always strong cards.\n\n"
    "*The same page goes on to three and four of a kind (4 Aces: \"Great power and force\"), and the page "
    "before it says: \"Princes and Queens shew almost always actual men and women connected with the "
    "matter. But the Kings (Knights) sometime represent coming or going of a matter, according as they "
    "face. The Princesses shew opinions, thoughts, ideas, either in harmony with or opposed to, the "
    "subject.\" Full text: research/sources/book-t-equinox-1912.txt.*"
)


def load(slug):
    p = os.path.join(ROOT, 'tarot', slug, 'grammar.json')
    raw = open(p, encoding='utf-8', newline='').read()
    crlf = '\r\n' in raw
    return p, json.loads(raw.replace('\r\n', '\n')), raw, crlf


def dump(g, raw, crlf):
    out = json.dumps(g, ensure_ascii=False, indent=2) + ('\n' if raw.replace('\r\n', '\n').endswith('\n') else '')
    return out.replace('\n', '\r\n') if crlf else out


def tag(s, label, t):
    v = s.get(label)
    if isinstance(v, str) and t not in v:
        s[label] = v.rstrip() + '\n\n' + t
        return 1
    return 0


def commons(g, old, new):
    for att in g.get('_grammar_commons', {}).get('attribution', []):
        n = att.get('note') or ''
        if old in n and new not in n:
            att['note'] = n.replace(old, new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    archive = {'_about': ("Number-card upright lines moved off the three Etteilla decks on 2026-10-08: one template "
                          "copied across the four suits, not Etteilla's, and no source in the repo gives his own "
                          "words for these cards. Kept by deck and item id. Written by "
                          "scripts/archive/due_edits_2026_10_08.py."),
               'decks': {}}
    if os.path.exists(ARCHIVE):
        archive = json.load(open(ARCHIVE, encoding='utf-8'))
    pending, counts = {}, {}

    def bump(k, n=1):
        if n:
            counts[k] = counts.get(k, 0) + n

    for slug in ETTEILLA:
        p, g, raw, crlf = load(slug)
        for it in g['nodes']:
            s = it.get('sections') or {}
            cat = it.get('category')
            if cat == 'minor' and 'Upright (the person well-disposed)' not in s:
                if 'Upright' in s:
                    archive['decks'].setdefault(slug, {})[it['id']] = {'Upright': s.pop('Upright')}
                    bump(slug + ' pip uprights moved')
                v = s.get(SYS)
                if isinstance(v, str) and PIP_NOTE.strip() not in v:
                    s[SYS] = v.rstrip() + PIP_NOTE
            elif cat == 'minor':
                bump(slug + ' court tagged', tag(s, 'Upright (the person well-disposed)', COURT_TAG))
            elif cat == 'major':
                bump(slug + ' trump tagged', tag(s, 'Upright', TRUMP_TAG))
        commons(g, ETT_COMMONS_OLD, ETT_COMMONS_NEW)
        out = dump(g, raw, crlf)
        if out != raw:
            pending[p] = out

    p, g, raw, crlf = load('oswald-wirth-tarot')
    for it in g['nodes']:
        bump('wirth tagged', tag(it.get('sections') or {}, 'Upright', WIRTH_TAG))
    commons(g, WIRTH_COMMONS_OLD, WIRTH_COMMONS_NEW)
    out = dump(g, raw, crlf)
    if out != raw:
        pending[p] = out

    p, g, raw, crlf = load('tarot-de-marseille-conver')
    for it in g['nodes']:
        s = it.get('sections') or {}
        bump('conver tagged', tag(s, 'Upright', CONVER_TAG))
        if isinstance(s.get('Tradition Note'), str) and CONVER_TN_OLD in s['Tradition Note']:
            s['Tradition Note'] = s['Tradition Note'].replace(CONVER_TN_OLD, CONVER_TN_NEW)
    commons(g, CONVER_COMMONS_OLD, CONVER_COMMONS_NEW)
    out = dump(g, raw, crlf)
    if out != raw:
        pending[p] = out

    p, g, raw, crlf = load('golden-dawn-book-t-tarot')
    for it in g['nodes']:
        s = it.get('sections') or {}
        if it['id'] in GD_COURTS:
            note = GD_HEAD + '\n\n' + GD_COURTS[it['id']]
            bump('gd court notes', tag(s, 'Golden Dawn Rank', note))
        if it['id'] == 'emg-majors' and MAJORITY_LABEL not in s:
            s[MAJORITY_LABEL] = MAJORITY
            bump('gd majority table')
    out = dump(g, raw, crlf)
    if out != raw:
        pending[p] = out

    print('[due_edits_2026_10_08]', json.dumps(counts))
    if a.check:
        print('--check: %s' % ('up to date' if not pending else '%d files would change' % len(pending)))
        sys.exit(1 if pending else 0)
    for p, out in pending.items():
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(out)
    if any(k.endswith('pip uprights moved') for k in counts):
        with open(ARCHIVE, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(archive, fh, ensure_ascii=False, indent=2)
            fh.write('\n')
    print('wrote %d grammar files' % len(pending))


if __name__ == '__main__':
    main()
