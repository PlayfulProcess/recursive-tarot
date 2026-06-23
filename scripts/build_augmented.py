#!/usr/bin/env python3
"""Build Arlecchino's Augmented Arcana (84) grammar.json. Her divinatory meanings are PDF-only
(not on the web), so: reuse her Tarocchino Arlecchino Etteilla meanings for every overlapping card
(matched by canonical archetype/court key), and attach her scraped per-card ART DESCRIPTIONS for all
84. The 6 added majors (Arlecchino, Colombina, the four virtues) and pips 2-5 carry art-desc only
(meanings are in her PDF — noted). Italian-named, full 56-card minors. Parent: tarocchino-arlecchino.
"""
import json, re, os, glob

ARCANA = {"The Fool":"the-fool","The Magician":"the-magician","The Papess":"the-high-priestess",
 "The High Priestess":"the-high-priestess","The Empress":"the-empress","The Emperor":"the-emperor",
 "The Pope":"the-hierophant","The Hierophant":"the-hierophant","Love":"the-lovers","The Lovers":"the-lovers",
 "The Chariot":"the-chariot","Temperance":"temperance","Justice":"justice","Strength":"strength",
 "Wheel of Fortune":"wheel-of-fortune","The Old Man":"the-hermit","The Hermit":"the-hermit",
 "The Traitor":"the-hanged-man","The Hanged Man":"the-hanged-man","Death":"death","The Devil":"the-devil",
 "The Lightning":"the-tower","The Tower":"the-tower","The Star":"the-star","The Moon":"the-moon",
 "The Sun":"the-sun","The World":"the-world","The Angel":"judgement","Judgment":"judgement","Judgement":"judgement"}
SUITN = {"batons":"wands","wands":"wands","coins":"coins","denari":"coins","cups":"cups","coppe":"cups",
 "swords":"swords","spade":"spade" and "swords"}
PIP = {"ace":"ace","two":"two","three":"three","four":"four","five":"five","six":"six","seven":"seven",
 "eight":"eight","nine":"nine","ten":"ten"}
COURT = {"king":"king","queen":"queen","knight":"knight","page":"page","knave":"page","maid":"page",
 "valet":"page","servante":"page","fante":"page"}

def english(name):
    m = re.search(r"\(([^)]+)\)", name); return (m.group(1).strip() if m else name.strip())

def canon_key(name):
    """canonical join key from a card's English name."""
    en = english(name)
    # strip a trailing '/Wands' style alt
    base = en.split("/")[0].strip()
    if base in ARCANA: return "arcana:" + ARCANA[base]
    # try the whole english against ARCANA (e.g. 'The Old Man/Hermit')
    for k in ARCANA:
        if en.startswith(k): return "arcana:" + ARCANA[k]
    m = re.match(r"(King|Queen|Knight|Page|Knave|Maid|Valet|Servante|Fante|Ace|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)\s+of\s+(\w+)", en, re.I)
    if m:
        rank, suit = m.group(1).lower(), m.group(2).lower()
        sn = SUITN.get(suit, suit)
        if rank in PIP: return f"card:{PIP[rank]}-of-{sn}"
        if rank in COURT: return f"court:{COURT[rank]}-{sn}"
    return None

def main():
    plat_file = ("C:/Users/ferna/.claude/projects/C--Users-ferna-OneDrive-Documentos-GitHub/"
                 "f8bb4a3a-268a-42dd-9596-28e77d67add8/tool-results/"
                 "mcp-6b361191-1fb9-4ce8-bfa5-928a3833b8a0-get_grammar-1782175398563.txt")
    g = json.loads(open(plat_file, encoding="utf-8").read())
    plat = g["items"]

    # 1) meaning lookup from the built Tarocchino grammar (her Etteilla text)
    tg = json.load(open("tarot/tarocchino-arlecchino/grammar.json", encoding="utf-8"))
    meanings = {}
    for it in tg["items"]:
        a = it["metadata"].get("archetype")
        key = a if a else canon_key(it["name"])
        if not key: continue
        s = it.get("sections", {})
        up = s.get("Upright meaning (Etteilla system)"); rev = s.get("Reversed meaning (Etteilla system)")
        if up or rev: meanings[key] = {"up": up, "rev": rev}

    # 2) art descriptions by a (suit,rank)/major key
    art = {}
    for f in glob.glob("research/yve-lepkowski/augmented-raw/c*.json"):
        for c in json.load(open(f, encoding="utf-8")):
            art[c["slug"]] = c.get("art_description")
    def art_for(p):
        # platform name -> art slug guess
        en = english(p["name"]); ital = p["name"].split("(")[0].strip().lower()
        # majors: last italian word
        root = re.sub(r"^(il|la|l'|lo|le)\s*", "", ital).strip().replace("'", "")
        root = root.split()[0] if root else ""
        for slug, desc in art.items():
            s = slug.lower()
            if root and (s.endswith("_"+root) or s.endswith(root) or root in s.split("_")):
                return desc
        # minors by suit_rank
        m = re.match(r"(King|Queen|Knight|Knave|Page|Maid|Ace|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)\s+of\s+(\w+)", en, re.I)
        if m:
            rank, suit = m.group(1).lower(), m.group(2).lower()
            sa = {"batons":"batons","coins":"coins","cups":"cups","swords":"swords"}.get(suit, suit)
            num = {"ace":"01","two":"02","three":"03","four":"04","five":"05","six":"06","seven":"07","eight":"08","nine":"09","ten":"10"}.get(rank)
            cand = [f"{sa}_{num}"] if num else [f"{sa}_{rank}"]
            for slug, desc in art.items():
                if slug.lower().split("?")[0].rstrip("/").endswith(tuple(cand)) or any(slug.lower().startswith(c) for c in cand):
                    return desc
        return None

    items = []; reused = 0; arted = 0
    for i, p in enumerate(plat):
        en = english(p["name"]); key = canon_key(p["name"])
        meta = {"tradition":"contemporary-bolognese","era":"contemporary","italian_name":p["name"].split("(")[0].strip()}
        cat = p.get("category")
        if cat == "major" or (p.get("metadata") or {}).get("arcana") == "major":
            slug = ARCANA.get(en.split("/")[0].strip())
            meta.update({"arcana":"trump","archetype":(f"arcana:{slug}" if slug else None),
                         "mapping_confidence":"exact" if slug else "none"}); category = "trump"
        else:
            m = re.match(r"(\w+)\s+of\s+(\w+)", en)
            suit = (m.group(2).lower() if m else None); rank = (m.group(1).lower() if m else None)
            sn = {"batons":"wands","coins":"coins","cups":"cups","swords":"swords"}.get(suit, suit)
            court = rank in COURT
            meta.update({"arcana":"minor","suit":(suit.capitalize() if suit else None),
                "rank":(rank.capitalize() if rank else None),"court":court,
                "archetype":(None if (court or not key or not key.startswith("card:")) else key),
                "mapping_confidence":"exact" if (key and key.startswith("card:")) else "none"})
            category = f"suit-{sn}" if sn else "card"
        sec = {}
        ad = art_for(p)
        if ad: sec["The card"] = ad; arted += 1
        mn = meanings.get(key) if key else None
        if mn:
            reused += 1
            if mn["up"]: sec["Upright meaning (Etteilla system)"] = mn["up"]
            if mn["rev"]: sec["Reversed meaning (Etteilla system)"] = mn["rev"]
        elif category == "trump" and meta["archetype"] is None:
            sec["Note"] = ("An added card beyond the standard tarot (Arlecchino's own expansion). Yve Lepkowski's "
                "divinatory meaning for this card is in her printed guidebook (stolen-thyme.com), not published online.")
        img = p.get("image_url")
        if img:
            meta["illustrations"] = [{"url":img,"artist":"Yve Lepkowski","license":"CC-BY-SA-4.0",
                "source":"https://stolen-thyme.com/tarocchino-arlecchino/arlecchinos-augmented-arcana/"}]
        items.append({"id":p.get("id",f"card-{i}"),"name":p["name"],"sort_order":i,"category":category,
            "keywords":p.get("keywords",[]),"sections":sec,"image_url":img,"metadata":meta})

    out = {"_community_slug":"arlecchinos-augmented-arcana","name":"Arlecchino's Augmented Arcana",
     "slug":"arlecchinos-augmented-arcana","grammar_type":"tarot","provenance":"living","worldview":"contemporary",
     "creator_name":"Yve Lepkowski","creator_link":"https://stolen-thyme.com/tarocchino-arlecchino/arlecchinos-augmented-arcana/",
     "cover_image_url":plat[0].get("image_url"),
     "image_credit":"Art & guidebook by Yve Lepkowski (stolen-thyme.com), CC-BY-SA-4.0.",
     "description":("The 84-card expansion of Yve Lepkowski's Tarocchino Arlecchino (stolen-thyme.com), CC-BY-SA-4.0: "
       "the full Bolognese deck with complete pip cards, two Significators (Arlecchino & Colombina), and the four "
       "virtues — including **La Prudenza (Prudence)**, the cardinal virtue the historical tarot never depicted. "
       "**A contemporary deck**, descending from her own Tarocchino Arlecchino. 'The card' is her art description; "
       "Etteilla upright/reversed meanings are carried over from her Tarocchino guidebook where the cards overlap; "
       "meanings for the added cards live in her printed guidebook."),
     "tags":["tarot","tarocchino","arlecchino","commedia-dellarte","bolognese","virtues","prudence","contemporary","cc-by-sa","yve-lepkowski"],
     "roots":["western-esoteric"],"lineages":["tarocchino-arlecchino"],"parent_deck":"tarocchino-arlecchino","is_published":True,
     "_grammar_commons":{"schema_version":"1.0","license":"CC-BY-SA-4.0",
       "license_url":"https://creativecommons.org/licenses/by-sa/4.0/",
       "attribution":[{"name":"Yve Lepkowski","role":"artist & deck creator","link":"https://stolen-thyme.com",
         "note":"Arlecchino's Augmented Arcana — original deck, CC-BY-SA-4.0."},
         {"name":"PlayfulProcess","role":"compiled into this library as a recursive.eco grammar","link":"https://recursive.eco"}],
       "modifications":("'The card' sections are her own art descriptions (from her per-card pages). Etteilla upright/"
         "reversed meanings are reused verbatim from her Tarocchino Arlecchino guidebook for overlapping cards; the "
         "6 added majors and the 2-5 pips carry her art description only (their meanings are PDF-only). No meanings altered.")},
     "items":items}
    os.makedirs("tarot/arlecchinos-augmented-arcana", exist_ok=True)
    json.dump(out, open("tarot/arlecchinos-augmented-arcana/grammar.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote arlecchinos-augmented-arcana — {len(items)} cards, {reused} reused Etteilla meanings, {arted} with art description")

if __name__ == "__main__":
    main()
