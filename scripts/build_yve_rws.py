#!/usr/bin/env python3
"""Build a repo grammar.json for one of Yve Lepkowski's RWS-structured decks
(Clown Town Tarot, Anecdotes Tarot) from:
  - a platform-structure dump (images/order/names): research/yve-lepkowski/<deck>-platform.json
  - her scraped guidebook batches: research/yve-lepkowski/<deck>-raw/*.json
Matches the two by archetype key (major number / (suit,rank)) so images + her own text line up,
maps cross-deck archetypes, and writes tarot/<slug>/grammar.json (provenance:'living', CC-BY-SA
attribution to Yve, lineage to a historical parent). Config dict per deck at the bottom.
Run: python scripts/build_yve_rws.py <deck-key>
"""
import json, glob, re, sys, os

ARCANA_BY_NUM = {0:"the-fool",1:"the-magician",2:"the-high-priestess",3:"the-empress",4:"the-emperor",
 5:"the-hierophant",6:"the-lovers",7:"the-chariot",8:"justice",9:"the-hermit",10:"wheel-of-fortune",
 11:"strength",12:"the-hanged-man",13:"death",14:"temperance",15:"the-devil",16:"the-tower",
 17:"the-star",18:"the-moon",19:"the-sun",20:"judgement",21:"the-world"}
MAJOR_SLUG = {"the-fool":0,"i-the-magician":1,"ii-the-papess":2,"iii-the-empress":3,"iiii-the-emperor":4,
 "v-the-pope":5,"vi-the-lover":6,"vii-the-chariot":7,"viii-justice":8,"viiii-the-hermit":9,
 "x-the-wheel-of-fortune":10,"xi-strength":11,"xii-the-hanged-one":12,"xiii":13,"xiiii-temperance":14,
 "xv-the-devil":15,"xvi-the-house-of-god":16,"xvii-the-star":17,"xviii-the-moon":18,"xviiii-the-sun":19,
 "xx-judgment":20,"xxi-the-world":21}
RANK = {"ace":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,
 "page":11,"knight":12,"queen":13,"king":14}
SUIT = {"batons":("wands","Fire"),"cups":("cups","Water"),"swords":("swords","Air"),"coins":("coins","Earth")}
RANK_LABEL = {1:"Ace",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten",
 11:"Page",12:"Knight",13:"Queen",14:"King"}

def gb_key(slug):
    """archetype key for a guidebook card slug."""
    s = slug.strip().lower()
    if s in MAJOR_SLUG: return ("M", MAJOR_SLUG[s])
    m = re.match(r"(ace|two|three|four|five|six|seven|eight|nine|ten|page|knight|queen|king)-of-(batons|cups|swords|coins)", s)
    if m: return (m.group(2), RANK[m.group(1)])
    return None

def plat_key(it):
    if it.get("category") == "major" or it.get("suit") in (None,"",):
        n = it.get("arc_number")
        return ("M", n) if n is not None else None
    return (it.get("suit"), it.get("arc_number"))

def build(cfg):
    plat = json.load(open(cfg["platform_file"], encoding="utf-8"))
    gb = {}
    for f in glob.glob(cfg["guidebook_glob"]):
        for c in json.load(open(f, encoding="utf-8")):
            k = gb_key(c["slug"])
            if k: gb[k] = c
    items=[]; matched=0
    for i, p in enumerate(plat):
        k = plat_key(p)
        g = gb.get(k)
        # archetype + suit metadata
        meta = {"tradition":"contemporary", "era":"contemporary"}
        if k and k[0]=="M":
            slug = ARCANA_BY_NUM.get(k[1])
            meta.update({"arcana":"trump","archetype":(f"arcana:{slug}" if slug is not None else None),
                         "mapping_confidence":"exact" if slug is not None else "none"})
            cat = "trump"
        elif k:
            suit, num = k
            a_suit, element = SUIT.get(suit, (suit,""))
            court = num >= 11
            meta.update({"arcana":"minor","suit":suit.capitalize(),"element":element,"rank":RANK_LABEL.get(num),
                         "court":court,"archetype":(None if court else f"card:{RANK_LABEL[num].lower()}-of-{a_suit}"),
                         "mapping_confidence":"none" if court else "exact"})
            cat = f"suit-{a_suit}"
        else:
            meta.update({"arcana":"minor","archetype":None,"mapping_confidence":"none"}); cat="card"
        sec = {}
        if g:
            matched += 1
            if g.get("image_description"): sec["The card"] = g["image_description"]
            if g.get("interpretation"): sec["Interpretation"] = g["interpretation"]
            if g.get("epigraph"): sec["Epigraph"] = g["epigraph"]
            if g.get("selected_meanings"): sec["Selected meanings"] = g["selected_meanings"]
        img = p.get("image_url")
        if img:
            meta["illustrations"]=[{"url":img,"artist":"Yve Lepkowski","license":"CC-BY-SA-4.0",
                "source":cfg["creator_link"],"note":"Hot-linked from the platform mirror (Google Drive); CDN-mirror is a follow-up."}]
        items.append({"id":p.get("id",f"card-{i}"),"name":p["name"],"sort_order":i,"category":cat,
            "keywords":p.get("keywords",[]),"sections":sec,"image_url":img,"metadata":meta})
    out = {
        "_community_slug":cfg["slug"],"name":cfg["name"],"slug":cfg["slug"],"grammar_type":"tarot",
        "provenance":"living","worldview":"contemporary","creator_name":"Yve Lepkowski",
        "creator_link":cfg["creator_link"],"cover_image_url":plat[0].get("image_url"),
        "image_credit":"Art & guidebook text by Yve Lepkowski (stolen-thyme.com), CC-BY-SA-4.0.",
        "description":cfg["description"],"tags":cfg["tags"],"roots":["western-esoteric"],
        "lineages":[cfg["parent"]],"parent_deck":cfg["parent"],"is_published":True,
        "_grammar_commons":{"schema_version":"1.0","license":"CC-BY-SA-4.0",
            "license_url":"https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution":[{"name":"Yve Lepkowski","role":"artist & deck creator","link":"https://stolen-thyme.com",
                "note":cfg["attrib_note"]},
                {"name":"PlayfulProcess","role":"compiled into this library as a recursive.eco grammar","link":"https://recursive.eco"}],
            "modifications":cfg["modifications"]},
        "items":items}
    d=f"tarot/{cfg['slug']}"; os.makedirs(d,exist_ok=True)
    json.dump(out, open(f"{d}/grammar.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {d}/grammar.json — {len(items)} cards, {matched} matched to her guidebook")

CONFIGS = {
 "clown-town-tarot": dict(
    slug="clown-town-tarot", name="Clown Town Tarot",
    platform_file="research/yve-lepkowski/clown-town-platform.json",
    guidebook_glob="research/yve-lepkowski/clown-town-raw/b*.json",
    creator_link="https://stolen-thyme.com/clown-town-tarot/", parent="tarot-de-marseille-conver",
    description=("A whimsical 78-card tarot of clowns and circus life by Yve Lepkowski (stolen-thyme.com), "
        "CC-BY-SA-4.0. A full Marseille-structured deck (Justice VIII, Strength XI; suits of Coins, Batons, "
        "Swords, Cups) reimagined through vaudeville and the big top. **A contemporary deck**, descending "
        "from the historical Tarot de Marseille in this library. Card text is the author's own guidebook prose."),
    tags=["tarot","clown","circus","vaudeville","marseille-order","contemporary","cc-by-sa","yve-lepkowski"],
    attrib_note="Clown Town Tarot — original deck & guidebook, CC-BY-SA-4.0 (stolen-thyme.com/clown-town-tarot).",
    modifications=("Restructured Yve Lepkowski's deck into the recursive.eco grammar schema with cross-deck "
        "archetype mappings + a genealogy link to the Tarot de Marseille. Each card's 'Interpretation' and "
        "'The card' sections are her own guidebook text (verbatim prose + image description). No meanings altered.")),
}

if __name__ == "__main__":
    build(CONFIGS[sys.argv[1]])
