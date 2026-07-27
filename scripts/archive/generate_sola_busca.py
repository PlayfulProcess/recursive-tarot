#!/usr/bin/env python3
"""Generate the Sola Busca tarot grammar for recursive-tarot.

Data (card identities + image set) reused from the live recursive.eco Supabase
deck (id 6e4394c2-…) whose images are ALREADY on R2 — so we reference the existing
R2 URLs and upload nothing new. The Sola Busca is sui-generis: its 22 trumps are
named Roman/biblical/historical figures (not the standard tarot trumps), and it is
the earliest deck whose 56 minor cards are ALL scenically illustrated — the model
Pamela Colman Smith drew on for the Rider-Waite-Smith minors.
"""
import json

R2 = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/tarot-wikimedia/'
def img(n): return f'{R2}Sola%20Busca%20tarot%20card%20{n:02d}.jpg'
def commons(n): return f'https://commons.wikimedia.org/wiki/Special:FilePath/Sola%20Busca%20tarot%20card%20{n:02d}.jpg'

# Trump 0-21: (name, brief identification where reasonably attested)
TRUMPS = [
    ('Mato', 'The Fool figure — a ragged man; the deck’s unnumbered/zero card.'),
    ('Panfilio', 'A named protagonist figure opening the trump sequence.'),
    ('Postumio', 'After the Roman gens Postumia / a Postumius.'),
    ('Lenpio', 'A named figure (reading uncertain in the engraving).'),
    ('Mario', 'Gaius Marius, the Roman general and consul.'),
    ('Catulo', 'A Catulus (Lutatius Catulus) / Catullus.'),
    ('Sesto', 'Sextus — a Roman praenomen figure.'),
    ('Deo Tauro', 'A bull/Taurus figure — “the god-bull.”'),
    ('Nerone', 'The emperor Nero.'),
    ('Falco', 'A “falcon” figure / named soldier.'),
    ('Venturio', 'A named figure (Venturius).'),
    ('Tulio', 'A Tullius (echoing Cicero / Servius Tullius).'),
    ('Carbone', 'Gnaeus Papirius Carbo / a Carbo.'),
    ('Catone', 'Cato (the Elder or Younger).'),
    ('Bocho', 'Bocchus, the Mauretanian king.'),
    ('Olivo', 'A named figure associated with the olive.'),
    ('Metelo', 'A Caecilius Metellus.'),
    ('Ipeo', 'A named figure (reading uncertain).'),
    ('Lentulo', 'A Cornelius Lentulus.'),
    ('Sabino', 'A Sabinus / the Sabine.'),
    ('Nenbroto', 'Nimrod, the biblical hunter-king and tower-builder.'),
    ('Nabuchodenasor', 'Nebuchadnezzar, king of Babylon — the highest trump.'),
]

SUITS = [  # (display, id, element, start_index)
    ('Cups', 'cups', 'water', 22),
    ('Coins', 'coins', 'earth', 36),
    ('Batons', 'batons', 'fire', 50),
    ('Swords', 'swords', 'air', 64),
]
RANKS = ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Page','Knight','Queen','King']
RANK_ID = ['ace','02','03','04','05','06','07','08','09','10','page','knight','queen','king']
RANK_KEY = ['ace','two','three','four','five','six','seven','eight','nine','ten','page','knight','queen','king']

def illus(n, scene):
    return [{'url': commons(n), 'artist': 'Anonymous N. Italian engraver ("Master of the Sola Busca")',
             'artist_dates': 'active c. 1491', 'edition': 'Sola Busca tarocchi, copperplate engraving, c. 1491 (hand-coloured exemplar, Pinacoteca di Brera, Milan)',
             'scene': scene, 'license': 'Public Domain', 'is_primary': True}]

items = []
for n, (name, gloss) in enumerate(TRUMPS):
    items.append({
        'id': f'major-{n:02d}-{name.lower().replace(" ","-")}',
        'name': f'{n} — {name}',
        'sort_order': n,
        'category': 'major-arcana',
        'level': 1,
        'keywords': ['sola busca','trionfi','renaissance','engraving','named figure','major', name.lower()],
        'image_url': img(n),
        'metadata': {'arcana': 'major', 'number': n, 'figure': name,
                     'illustrations': illus(n, f'{name} (trump {n})'),
                     'mapping_confidence': 'none'},   # sui-generis trumps do NOT map to standard arcana
        'sections': {
            'Figure': f'**{name}.** {gloss}',
            'Tradition Note': 'The Sola Busca trumps are a unique humanist programme of named Roman, biblical and legendary figures — *not* the standard tarot triumphs. There is no Popess, Hanged Man, Death or Tower here in the Marseille sense; the sequence is the deck’s own invention.',
        },
    })

for disp, sid, elem, start in SUITS:
    for r in range(14):
        n = start + r
        rank, rid, rkey = RANKS[r], RANK_ID[r], RANK_KEY[r]
        court = r >= 10
        items.append({
            'id': f'{sid}-{rid}',
            'name': f'{rank} of {disp}',
            'sort_order': n,
            'category': f'suit-{sid}',
            'level': 1,
            'keywords': ['sola busca','minor','scenic', 'court' if court else 'pip',
                         disp.lower(), elem, rkey,
                         f'suit:{sid}', f'rank:{rkey}', f'element:{elem}'],
            'image_url': img(n),
            'metadata': {'arcana': 'minor', 'suit': disp, 'rank': rank, 'number': r+1,
                         'element': elem,
                         'illustrations': illus(n, f'{rank} of {disp} (scenic minor)'),
                         'archetype': f'card:{rkey}-of-{sid}', 'mapping_confidence': 'exact'},
            'sections': {
                'Scene': f'A fully engraved figural scene — the Sola Busca minors are pictorial, not pip arrangements. This is the {rank.lower()} of the {disp.lower()} suit.',
                'Why it matters': 'These 56 illustrated minors (c. 1491) are the earliest of their kind and a documented source for Pamela Colman Smith’s scenic minors in the 1909 Rider-Waite-Smith deck.',
            },
        })

deck = {
    '_github_url': 'https://github.com/PlayfulProcess/recursive-tarot/tree/main/tarot/sola-busca-tarot',
    '_github_source_url': 'https://raw.githubusercontent.com/PlayfulProcess/recursive-tarot/main/tarot/sola-busca-tarot/grammar.json',
    '_grammar_commons': {
        'schema_version': '1.0', 'license': 'CC-BY-SA-4.0',
        'attribution': [
            {'name': 'Anonymous N. Italian engraver ("Master of the Sola Busca")', 'date': 'c. 1491',
             'note': 'Original copperplate engravings; the named hand is unidentified (Ferrara/Venice circle).'},
            {'name': 'Pinacoteca di Brera, Milan', 'date': '1907→',
             'note': 'Holds the unique hand-coloured exemplar; images public domain.'},
        ],
    },
    'name': 'Sola Busca Tarot — The First Fully-Engraved Deck (N. Italy, c. 1491)',
    'description': (
        '# Sola Busca Tarot\n\n'
        '> A deck that breaks every later rule. Its 22 trumps are named **Roman, biblical and '
        'legendary figures** — Nero, Cato, Nimrod, Nebuchadnezzar — not the Fool/Popess/Death '
        'sequence the Marseille made standard. And it is the **earliest tarot whose 56 minor '
        'cards are all scenically illustrated.**\n\n'
        '## At a glance\n\n'
        'Engraved on copper around **1491** in northern Italy (Ferrara/Venice circle), the Sola '
        'Busca is the oldest complete deck to survive as a full set of prints, and the only '
        'Renaissance tarot whose pip cards carry *figural scenes* rather than rows of suit-signs. '
        'Four centuries later those scenic minors became a documented model for **Pamela Colman '
        'Smith**, whose 1909 Rider-Waite-Smith minors are the reason most modern decks illustrate '
        'every card.\n\n'
        '## Read it in its own tradition\n\n'
        'This is a **sui-generis** deck: do not force Marseille or RWS meanings onto its trumps. '
        'The figures form a humanist honour-roll of antiquity, not a moral allegory of Fool-to-World. '
        'The minors are read here by suit, rank and element; the trumps by who they depict.\n\n'
        '*Images: Pinacoteca di Brera exemplar, public domain. Curated by PlayfulProcess, CC-BY-SA-4.0.*'
    ),
    'grammar_type': 'tarot',
    'creator_name': 'PlayfulProcess',
    'creator_link': 'https://recursive.eco',
    'cover_image_url': img(21),
    'tags': ['tarot','sola-busca','renaissance','engraving','ferrara','venice','sui-generis','scenic-minors','public-domain'],
    'roots': ['renaissance','italian-engraving'],
    'shelves': ['wonder','mirror'],
    'lineages': ['Andreotti'],
    'worldview': 'historical',
    'is_published': True,
    'items': items,
}

import os
os.makedirs('tarot/sola-busca-tarot', exist_ok=True)
json.dump(deck, open('tarot/sola-busca-tarot/grammar.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote tarot/sola-busca-tarot/grammar.json with', len(items), 'items')
