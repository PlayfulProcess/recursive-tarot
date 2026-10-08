"""One-shot fixer for the anachronism audit of Oct 8 2026 (docs/plan/ANACHRONISM-AUDIT-2026-10-08.md).

Pattern fixed: an author, deck or tradition credited with a name, fact or object it could not have
known (Ma'at before 1822, Ra, the weighing of the heart, the suit-elements on 15th-century cards,
Rider-Waite-Smith pip meanings on Etteilla's cards), or editorial/AI text presented as the source's.

Every section this script changes is copied, as it was, into
tarot/_archive/anachronisms-2026-10-08.json (deck -> item -> section -> old text).
Run once from the repo root:  python scripts/archive/anachronism_audit_2026_10_08.py [--check]
Re-running is safe: each rule checks whether it has already been applied.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))
from cdg_1781_text import TEXT as CDG_TEXT, SYMBOL as CDG_SYMBOL, RESEARCH_ADD as CDG_RESEARCH  # noqa: E402

ARCHIVE = os.path.join(ROOT, 'tarot', '_archive', 'anachronisms-2026-10-08.json')
CDG_READING = "Court de Gébelin's Egyptian Reading"

ETTEILLA = ['etteilla-i-livre-de-thot', 'etteilla-ii-egyptian', 'etteilla-iii-oracle-des-dames']
# Decks made before any occult writer tied the four suits to the four elements.
PRE_OCCULT = ['visconti-sforza-tarot', 'cary-yale-visconti-tarot', 'tarot-de-marseille-conver',
              'minchiate-florence-tarot', 'tarocchino-bologna', 'paris-anonymous-tarot',
              'vieville-tarot', 'tarot-de-besancon']
ELEMENT_NOTE = "*Linking the suits to the four elements is a later occult attribution, not the card-makers'.*"
ELEMENT_LINK = re.compile(
    r"suit of (fire|water|air|earth)\b|(fire|water|air|earth) is the element of the|"
    r"carr(y|ies) the (fire|water|air|earth) element|element associated with the \w+ suit|"
    r"elemental registers|linked to the \w+ suit|suit tradition", re.I)


def load(slug):
    p = os.path.join(ROOT, 'tarot', slug, 'grammar.json')
    raw = open(p, encoding='utf-8', newline='').read()
    return p, json.loads(raw.replace('\r\n', '\n')), raw, '\r\n' in raw


def dump(g, raw, crlf):
    out = json.dumps(g, ensure_ascii=False, indent=2) + ('\n' if raw.replace('\r\n', '\n').endswith('\n') else '')
    return out.replace('\n', '\r\n') if crlf else out


class Fixer:
    def __init__(self):
        self.archive = {}
        self.counts = {}

    def keep(self, slug, item, section, old):
        self.archive.setdefault(slug, {}).setdefault(item, {}).setdefault(section, old)

    def count(self, key):
        self.counts[key] = self.counts.get(key, 0) + 1

    def set(self, slug, it, section, new, key):
        old = it['sections'].get(section)
        if old == new:
            return
        self.keep(slug, it['id'], section, old)
        it['sections'][section] = new
        self.count(key)

    def drop(self, slug, it, section, key):
        if section in it['sections']:
            self.keep(slug, it['id'], section, it['sections'].pop(section))
            self.count(key)


def fix_cdg(f, slug, g):
    for it in g['items']:
        iid, s = it['id'], it.get('sections') or {}
        if iid in CDG_TEXT and CDG_READING in s:
            head, body = CDG_TEXT[iid]
            f.set(slug, it, CDG_READING, head + "\n\n" + body, 'cdg: reading replaced by the 1781 text')
        if iid in CDG_SYMBOL and 'Symbol' in s:
            f.set(slug, it, 'Symbol', CDG_SYMBOL[iid], 'cdg: Symbol corrected to the 1781 text')
        if iid in CDG_RESEARCH and 'Research note' in s and 'Checked against the 1781 text' not in s['Research note']:
            note = s['Research note']
            add = "\n\n*" + CDG_RESEARCH[iid] + "*"
            cut = note.find('\n\n*Sources:*')
            new = note[:cut] + add + note[cut:] if cut >= 0 else note + add
            f.set(slug, it, 'Research note', new, 'cdg: research note corrected')


def fix_etteilla(f, slug, g):
    for it in g['items']:
        s = it.get('sections') or {}
        iid = it['id']
        m = re.fullmatch(r'(?:etteilla|oracle-dames)-(\d+)', iid)
        num = int(m.group(1)) if m else None
        hc = s.get('Historical Context')
        if hc and 'Temple of Ptah at Memphis' in hc:
            new = hc.replace(
                "believed tarot originated with the Egyptian priests of the Temple of Ptah at Memphis, encoding",
                "held that the tarot was an ancient Egyptian book, the Book of Thoth, encoding")
            f.set(slug, it, 'Historical Context', new, 'etteilla: Ptah/Memphis claim corrected')
        if hc and "Ma'at" in hc:
            new = re.sub(r"\s*In the Hermetic tradition, Justice connects to Ma'at[^\n]*", '', hc).rstrip()
            f.set(slug, it, 'Historical Context', new, "etteilla: Ma'at sentence removed")
        md = it.get('metadata') or {}
        einsof = " In Hermetic philosophy, this is the Ein Sof or Tao—divine consciousness before manifestation."
        for k, v in list(s.items()):
            if isinstance(v, str) and einsof in v:
                f.set(slug, it, k, v.replace(einsof, ''), 'etteilla: Kabbalah/Tao misattributed to Hermetic philosophy, removed')
        nested = [('meta.%s.' % k, v) for k, v in md.items() if isinstance(v, dict)]
        for prefix, holder in [('meta.', md), ('item.', it)] + nested:
          for k, v in list(holder.items()):
            if isinstance(v, str) and einsof in v:
                f.keep(slug, iid, prefix + k, v)
                holder[k] = v.replace(einsof, '')
                f.count('etteilla: Kabbalah/Tao misattribution removed from metadata')
        if "Ma'at" in md.get('hermetic_correspondence', ''):
            f.keep(slug, iid, 'meta.hermetic_correspondence', md['hermetic_correspondence'])
            md['hermetic_correspondence'] = "Cosmic balance; the weighing of actions (editorial comparison, not Etteilla's)"
            f.count("etteilla: Ma'at removed from metadata")
        hm = s.get('Hermetic Correspondence')
        if hm and 'Editorial comparison' not in hm:
            body = 'Cosmic balance; the weighing of actions' if "Ma'at" in hm else hm
            f.set(slug, it, 'Hermetic Correspondence',
                  body + "\n\n*Editorial comparison, not Etteilla's words.*",
                  'etteilla: Hermetic Correspondence labelled editorial')
        sym = s.get('Symbol')
        if sym and num is not None and 22 <= num <= 77:
            f.drop(slug, it, 'Symbol', 'etteilla: Rider-Waite-Smith pip/court meaning removed')
        elif sym and slug == 'etteilla-ii-egyptian' and num is not None and (num <= 21 or num == 78) and re.search(
                r"Egypt|pharaoh|Nile", sym):
            f.drop(slug, it, 'Symbol', 'etteilla II: invented Egyptian imagery removed')


def fix_elements(f, slug, g):
    for it in g['items']:
        s = it.get('sections') or {}
        for sec in list(s):
            v = s[sec]
            if not isinstance(v, str):
                continue
            new = v
            if sec == 'History':
                new = re.sub(r", the suit of (Earth|Water|Fire|Air)(?=[,.])", '', new)
            if sec == 'The Besançon variant':
                new = re.sub(r" \((Air|Water|Fire|Earth)\)", '', new)
            if sec == 'Symbol':
                new = re.sub(r"^Suit: (Earth|Water|Air|Fire)\. ",
                             r"Suit: \1 (a later occult attribution, not Conver's). ", new)
                new = new.replace(" in the Marseille elemental system", '')
                new = new.replace("In Italian tradition the bastoni suit is associated with the merchant class and with the fire element.",
                                  "Later occult writers linked the batons to Fire.")
                new = new.replace("The fifty-six minor arcana divide the human world into four elemental registers:",
                                  "Later occult readers divided the fifty-six suit cards into four elemental registers:")
            if sec in ('Symbol', 'About this Suit') and ELEMENT_LINK.search(new) and ELEMENT_NOTE not in new \
                    and not new.startswith('Suit: '):
                new = new + "\n\n" + ELEMENT_NOTE
            if new != v:
                f.set(slug, it, sec, new, 'element attribution relabelled (%s)' % sec)


def fix_misc(f, slug, g):
    for it in g['items']:
        s = it.get('sections') or {}
        iid = it['id']
        if slug == 'visconti-sforza-tarot' and iid == 'major-08-la-giustizia' and 'two swords' in s.get('Symbol', ''):
            f.set(slug, it, 'Symbol',
                  "Justice holds an upraised sword and a balance, the usual attributes of the virtue. "
                  "The mounted knight above her, rare in tarot iconography, grounds the allegorical "
                  "figure in the reality of military enforcement: justice backed by force.",
                  'visconti: Justice Symbol matched to the card (sword and balance)')
        if slug == 'oswald-wirth-tarot' and iid == 'emg-the-great-work' and 'Golden Dawn-adjacent' in s.get('Symbol', ''):
            f.set(slug, it, 'Symbol',
                  "Wirth's 22-card system, designed under the direction of Stanislas de Guaïta, sets the "
                  "Hebrew alphabet on the trumps in Eliphas Lévi's order. The deck joins Marseille "
                  "iconography to the French occultism of Lévi and his followers, not to the English "
                  "Golden Dawn, whose letters differ; it shaped 20th-century tarot practice.",
                  'wirth: Golden Dawn link removed')
        if slug == 'oswald-wirth-tarot' and iid == 'arcanum-08-la-justice' and "Ma'at" in s.get('Symbol', ''):
            f.set(slug, it, 'Symbol', s['Symbol'].replace(
                "Justice as cosmic equilibrium: Ma'at in the Egyptian sense, the scales that weigh the heart against a feather.",
                "Justice as cosmic equilibrium: the balance and the sword."),
                "wirth: Ma'at removed from the editorial Justice note")
        if slug == 'golden-dawn-book-t-tarot' and iid == 'emg-majors' and 'visual keys for pathworking' in s.get('Symbol', ''):
            new = s['Symbol'].replace(
                "In GD practice the Trumps were used as visual keys for pathworking — the initiate contemplated the image to project consciousness along the corresponding path.",
                "The Order's papers teach skrying and travelling in the spirit-vision through symbols; "
                "the name pathworking for entering a trump this way came later, from the Order's heirs.")
            f.set(slug, it, 'Symbol', new, 'golden dawn: pathworking named as a later term')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    f = Fixer()
    pending = {}
    plan = [('court-de-gebelin-tarot', fix_cdg)] + [(d, fix_etteilla) for d in ETTEILLA] + \
           [(d, fix_elements) for d in PRE_OCCULT] + \
           [(d, fix_misc) for d in ('visconti-sforza-tarot', 'oswald-wirth-tarot', 'golden-dawn-book-t-tarot')]
    loaded = {}
    for slug, fn in plan:
        if slug not in loaded:
            loaded[slug] = load(slug)
        fn(f, slug, loaded[slug][1])
    for slug, (p, g, raw, crlf) in loaded.items():
        out = dump(g, raw, crlf)
        if out != raw:
            pending[p] = out
    print(json.dumps(f.counts, indent=1, ensure_ascii=False))
    if a.check:
        print('--check: %s' % ('up to date' if not pending else '%d files would change' % len(pending)))
        sys.exit(1 if pending else 0)
    for p, out in pending.items():
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(out)
    if f.archive:
        old = {}
        if os.path.exists(ARCHIVE):
            old = json.load(open(ARCHIVE, encoding='utf-8')).get('decks', {})
        for slug, items in f.archive.items():
            for iid, secs in items.items():
                for sec, txt in secs.items():
                    old.setdefault(slug, {}).setdefault(iid, {}).setdefault(sec, txt)
        doc = {'_about': "Text moved or rewritten by the anachronism audit of 2026-10-08 "
                         "(docs/plan/ANACHRONISM-AUDIT-2026-10-08.md): each section as it stood before, "
                         "by deck, item id and section. Sections absent from the live deck were removed; "
                         "the others were corrected or relabelled. Written by "
                         "scripts/archive/anachronism_audit_2026_10_08.py.",
               'decks': old}
        with open(ARCHIVE, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=2)
            fh.write('\n')
    print('wrote %d grammar files' % len(pending))


if __name__ == '__main__':
    main()
