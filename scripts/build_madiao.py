#!/usr/bin/env python3
"""Build the Ma Diao (Chinese money-suited cards) grammar — the deep root of the
playing-card form. Sources: 12 PD museum scans at Skokloster Castle, Sweden."""
import json, os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import re as _re
# Images are committed to tarot/madiao-money-cards/images/ and served by GitHub
# Pages (a real CDN). Hotlinking Commons or weserv failed: Commons' on-demand
# thumbnailer and weserv's free tier both rate-limit the grid's ~14 concurrent
# requests for these 22-megapixel museum TIFs, so the cards rendered blank.
# To (re)generate the local JPEGs, run scripts/localize_madiao_images once
# (downloads each Commons render sequentially → images/<inv>.jpg).
def fp(name, w=1000):
    m = _re.search(r"(\d+)\.tif", name)
    inv = m.group(1) if m else "x"
    fn = ("sheet-" + inv if "Mo Diao" in name else inv) + ".jpg"
    return "https://tarot.recursive.eco/tarot/madiao-money-cards/images/" + fn

CARDS = [  # (Skokloster inventory no, filename)
    ("102351", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102351.tif"),
    ("102352", "Kinesiskt spelkort Ma Diao - Skoklosters slott - 102352.tif"),
    ("102353", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102353.tif"),
    ("102354", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102354.tif"),
    ("102355", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102355.tif"),
    ("102356", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102356.tif"),
    ("102357", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102357.tif"),
    ("102358", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102358.tif"),
    ("102359", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102359.tif"),
    ("102360", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102360.tif"),
    ("102361", "Kinesiskt spelkort till Ma Diao - Skoklosters slott - 102361.tif"),
]
SHEET = ("13617", "Kinesiska spelkort för kortspelet Mo Diao - Skoklosters slott - 13617.tif")

SUITS = [
    ("suit-cash", "文錢 · Cash (Coins)", "The lowest money suit: single copper coins (wén). The coin is the ancestor of the European 'Coins/Pentacles' suit — the one suit that survived the long diffusion west more or less recognisably."),
    ("suit-strings", "索子 · Strings of Cash", "Strings or ropes (suǒ) on which coins were threaded — each string a bundle of one hundred cash. A denomination, not an abstract pip: the suits of this pack are literally units of money."),
    ("suit-myriads", "萬貫 · Myriads", "Ten-thousand-cash units (wàn). In many money-card sets this suit was illustrated with the 108 bandit-heroes of the novel *Water Margin* (水滸傳) — so 'Water Margin cards' (水滸牌) are a famous money-suited variety."),
    ("suit-tens", "十萬 · Tens of Myriads", "The top suit (the 'decade' / tens-of-myriads), carrying the honour cards. The four ascending money denominations — cash → strings → myriads → tens-of-myriads — are the whole structure of the game."),
]

items = []

# The four money suits (descriptive system node)
suit_ids = []
for sid, nm, about in SUITS:
    items.append({"id": sid, "name": nm, "level": 1, "category": "suit",
                  "sections": {"What it is": about}})
    suit_ids.append(sid)
items.append({"id": "axis-money-suits", "name": "The Four Money Suits", "level": 3,
              "category": "axis", "render_as": "pill-group", "composite_of": suit_ids,
              "sections": {"What it is": "Ma Diao is a *money-suited* pack: its four suits are ascending denominations of cash, not the cups/swords/coins/batons of the Mamluk and European line. This is the structural signature of the East-Asian card tradition."}})

# The surviving cards
card_ids = []
for inv, fname in CARDS:
    cid = "card-" + inv
    items.append({
        "id": cid, "name": "Ma Diao card — Skokloster " + inv, "level": 1,
        "image_url": fp(fname),
        "metadata": {"collection": "Skokloster Castle, Sweden", "inventory": inv,
                     "source": "Wikimedia Commons (public domain)"},
        "sections": {"About": "One of the surviving Ma Diao cards in the Chinese holdings at Skokloster Castle, Sweden — a 17th–18th-century European collection of an East-Asian money-suited pack. The individual suit and value are not separately catalogued here; the card is shown as a physical survivor of the tradition, not assigned a reading."},
    })
    card_ids.append(cid)
# the multi-card sheet
items.append({
    "id": "card-sheet-" + SHEET[0], "name": "Ma Diao cards (sheet) — Skokloster " + SHEET[0],
    "level": 1, "image_url": fp(SHEET[1]),
    "metadata": {"collection": "Skokloster Castle, Sweden", "inventory": SHEET[0],
                 "source": "Wikimedia Commons (public domain)"},
    "sections": {"About": "Several Ma Diao cards together (catalogued as 'Mo Diao') from the same Skokloster holdings."},
})
card_ids.append("card-sheet-" + SHEET[0])
items.append({"id": "skokloster-set", "name": "The Skokloster Surviving Set", "level": 3,
              "category": "axis", "render_as": "pill-group", "composite_of": card_ids,
              "image_url": fp(CARDS[0][1]),
              "sections": {"What it is": "The twelve Ma Diao items that survive in Sweden at Skokloster Castle — a fragmentary but high-resolution, openly public-domain witness to a money-suited Chinese pack."}})

grammar = {
    "name": "Ma Diao (馬吊) — Chinese Money-Suited Cards (the Deep Root)",
    "slug": "madiao-money-cards",
    "description": "# Ma Diao (馬吊) — Chinese money-suited cards\n\n## At a glance\n\nThe **deepest root of the playing-card form itself** — and, deliberately, *not* a direct ancestor of tarot. Paper playing cards are first documented in **Tang-dynasty China** (618–907 CE); by the time of the Song and Ming they had developed into **money-suited** packs whose suits are denominations of currency. **Ma Diao** (馬吊, 'hanging horse') is the best-documented of these games, codified in the **late Ming** (16th–17th c.) and described in period manuals. This library includes it to show where the *idea* of a suited pack of cards begins, several removes upstream of anything European.\n\n## The money suits\n\nFour ascending money denominations: **cash → strings of cash → myriads → tens-of-myriads** (文 · 索 · 萬 · 十萬). The suits are not abstract pips but units of money — the structural signature of the East-Asian tradition. The **myriad (萬) suit** was, in many sets, illustrated with the 108 bandit-heroes of the novel *Water Margin* (水滸傳), so painted 'Water Margin cards' (水滸牌) are a famous money-suited variety still made in folk workshops today.\n\n## Relationship to tarot — a deep root, not a parent\n\nThe standard scholarly thesis (Wilkinson, Needham, Lo) is that the playing-card *form* diffused **westward out of China**, reaching Europe through the **Islamic world**, where the **Mamluk pack** (Egypt/Syria) is the deck Europe directly copied. So the line to tarot runs **China → (centuries, many intermediaries) → Mamluk → Italian/Spanish suits → trionfi/tarot**. Ma Diao is a **cousin and a deep root**, like Ganjifa — it shows the origin of the form, but no card here descends by a clean line into a tarot trump. The detail of the transmission is genuinely debated; what is not debated is that paper cards are a Chinese invention.\n\n## Game, never divination\n\nMa Diao is a **trick-and-draw gambling game** for four players, played with a 40-card money-suited pack. There is no cartomantic tradition attached to it — it sits in this library purely as the upstream of the *object*, not of any reading practice.\n\n## Provenance & evidence\n\nThe cards shown are the **public-domain holdings at Skokloster Castle, Sweden** (high-resolution museum scans on Wikimedia Commons), a European collection of an East-Asian pack. Twelve items survive there. Individual suit/value identification is left open rather than guessed.\n\n## Sources\n\n- W. H. Wilkinson, 'Chinese Origin of Playing Cards' (1895); Joseph Needham, *Science and Civilisation in China*, vol. 5; Andrew Lo on Ma Diao and Water Margin cards; Dummett & Mann, *The Game of Tarot* (on the China→Islam→Europe diffusion). Card images: Skokloster Castle / Wikimedia Commons, public domain.\n\n---\n*AI-assisted first-pass draft in the house evidence-first style — claims hedged, transmission flagged as debated. Corrections welcome.*",
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "license": "CC-BY-SA-4.0",
    "default_view": "cards",
    "metadata": {"year": 1600, "tradition": "Chinese money-suited cards", "branch": "ancestors"},
    "_source": "Wikimedia Commons (Skokloster Castle), public domain. Hotlinked with attribution.",
    "items": items,
}

out = os.path.join(ROOT, "tarot", "madiao-money-cards")
os.makedirs(out, exist_ok=True)
json.dump(grammar, open(os.path.join(out, "grammar.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("wrote", out, "| items:", len(items))
