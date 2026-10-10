# -*- coding: utf-8 -*-
"""Draw the four diagrams of the chapter "Dignities, not reversals" as inline SVG.

    python scripts/build_gd_dignity_figures.py          # rewrite the figures in the chapter
    python scripts/build_gd_dignity_figures.py --check  # exit 1 if the chapter is out of date

Writes between the marker pairs <!-- figure:NAME --> ... <!-- /figure:NAME --> in
course/golden-dawn-dignities-not-reversals.mdx. Nothing is drawn by hand: every label that
quotes a source is checked against the source file it comes from (Book T as printed in
The Equinox I(8), 1912; Waite's Pictorial Key) before anything is written, and card images
are read from the Rider-Waite-Smith grammar (Wikimedia Commons scans, public domain in the US).

Colours are theme.css tokens (light only). Each figure is one HTML block with no blank lines,
so marked passes it through untouched.
"""
import json, os, re, sys
from html import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MDX = os.path.join(ROOT, "course", "golden-dawn-dignities-not-reversals.mdx")
BOOK_T = os.path.join(ROOT, "research", "sources", "book-t-equinox-1912.txt")
WAITE_III = os.path.join(ROOT, "research", "sources", "waite-pictorial-key-part-iii.md")
RWS = os.path.join(ROOT, "tarot", "rider-waite-smith-pictorial-key", "grammar.json")
CARDS = "../viewers/cards.html?src=../tarot/rider-waite-smith-pictorial-key/grammar.json&item="


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def load_text(path):
    with open(path, encoding="utf-8") as f:
        return norm(f.read())


BOOK_T_TEXT = load_text(BOOK_T)
WAITE_TEXT = load_text(WAITE_III)
with open(RWS, encoding="utf-8") as f:
    RWS_ITEMS = {it["id"]: it for it in json.load(f)["nodes"]}
RWS_TEXT = norm(json.dumps({k: v.get("sections", {}) for k, v in RWS_ITEMS.items()}, ensure_ascii=False))


def bt(q):
    """A phrase quoted from Book T: refuse to draw it unless the 1912 text has it."""
    if norm(q) not in BOOK_T_TEXT:
        sys.exit(f"not in Book T 1912: {q!r}")
    return q


def waite(q):
    if norm(q) not in RWS_TEXT and norm(q) not in WAITE_TEXT:
        sys.exit(f"not in the Pictorial Key: {q!r}")
    return q


def img(card_id):
    it = RWS_ITEMS[card_id]
    return it.get("image_url") or it["metadata"]["image_url"]


# ---------------------------------------------------------------- drawing helpers
STYLE = (
    "<style>"
    ".gdd text{font-family:var(--sans);fill:var(--ink);font-size:11px}"
    ".gdd .ser{font-family:var(--serif-display)}"
    ".gdd .mut{fill:var(--mut)}.gdd .gold{fill:var(--gold)}.gdd .b{font-weight:600}"
    ".gdd .it{font-style:italic}"
    ".gdd .ln-friend{stroke:var(--good);stroke-width:3;fill:none}"
    ".gdd .ln-enemy{stroke:var(--bad);stroke-width:3;stroke-dasharray:9 5;fill:none}"
    ".gdd .ln-strong{stroke:var(--good);stroke-width:6;fill:none}"
    ".gdd .ln-silent{stroke:var(--faint);stroke-width:2;stroke-dasharray:2 5;fill:none}"
    ".gdd .t-friend{fill:var(--good)}.gdd .t-enemy{fill:var(--bad)}.gdd .t-strong{fill:var(--good)}"
    ".gdd .t-silent{fill:var(--mut)}"
    ".gdd .node{fill:var(--surface);stroke:var(--gold);stroke-width:2}"
    ".gdd .glyph{fill:none;stroke:var(--ink);stroke-width:2;stroke-linejoin:round}"
    ".gdd .ico{fill:none;stroke:var(--ink-soft);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}"
    ".gdd .rule{stroke:var(--line);stroke-width:1}"
    ".gdd .spine{stroke:var(--gold);stroke-width:2}"
    ".gdd .card{fill:var(--thumb-bg);stroke:var(--line);stroke-width:1}"
    ".gdd .pairbg{fill:var(--panel2);stroke:var(--line);stroke-width:1}"
    ".gdd .pill{fill:var(--chip);stroke:var(--gold);stroke-width:1}"
    ".gdd .tile-key{fill:var(--gold)}.gdd .tile-court{fill:var(--ink-soft)}.gdd .tile-ace{fill:var(--surface);stroke:var(--gold);stroke-width:2}"
    "</style>"
)


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, cls="", anchor="start", size=None, n=None, lh=13):
    lines = wrap(s, n) if n else [s]
    st = f' style="font-size:{size}px"' if size else ""
    out = f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{st}>'
    for i, ln in enumerate(lines):
        out += f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{escape(ln)}</tspan>'
    return out + "</text>"


def glyph(el, cx, cy, s=13):
    """Alchemical element triangles: Fire up, Water down, Air up + bar, Earth down + bar."""
    up = el in ("fire", "air")
    if up:
        pts = f"{cx},{cy - s} {cx - .9 * s:.1f},{cy + .6 * s:.1f} {cx + .9 * s:.1f},{cy + .6 * s:.1f}"
    else:
        pts = f"{cx},{cy + s} {cx - .9 * s:.1f},{cy - .6 * s:.1f} {cx + .9 * s:.1f},{cy - .6 * s:.1f}"
    out = f'<polygon class="glyph" points="{pts}"/>'
    if el in ("air", "earth"):
        out += f'<line class="glyph" x1="{cx - .75 * s:.1f}" y1="{cy}" x2="{cx + .75 * s:.1f}" y2="{cy}"/>'
    return out


def figure(svgs, caption, extra_cls=""):
    """svgs: list of (layout_cls, svg). Several layouts become sibling figures toggled by CSS."""
    out = []
    for cls, svg in svgs:
        klass = " ".join(k for k in ("gdd-fig", cls, extra_cls) if k)
        out.append(f'<figure class="{klass}">' + svg + f"<figcaption>{caption}</figcaption></figure>")
    return "\n".join(out)


def svg_open(w, h, label):
    return (f'<svg class="gdd" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">{STYLE}<title>{escape(label)}</title>')


# ---------------------------------------------------------------- 1. the dignity wheel
ELEMENTS = {  # Book T, "The Titles of the Symbols", 1-4
    "fire": ("Fire", "Wands", bt("The Ace of Wands is called the Root of the Powers of Fire")),
    "water": ("Water", "Cups", bt("The Ace of Cups is called the Root of the Powers of Water")),
    "air": ("Air", "Swords", bt("The Ace of Swords is called the Root of the Powers of Air")),
    "earth": ("Earth", "Pentacles", bt("The Ace of Pentacles is called the Root of the Powers of Earth")),
}
# Book T, "Of the Dignities". Cups-Pentacles is the one pair the 1912 text does not name.
bt("Swords are inimical to Pentacles.")
bt("Wands are inimical to Cups.")
bt("Swords are friendly with Cups and Wands.")
bt("Wands are friendly with Swords and Pentacles.")
RELATION = {
    frozenset(("air", "earth")): "enemy",
    frozenset(("fire", "water")): "enemy",
    frozenset(("air", "water")): "friend",
    frozenset(("air", "fire")): "friend",
    frozenset(("fire", "earth")): "friend",
    frozenset(("water", "earth")): "silent",
}
REL_WORD = {"enemy": "inimical", "friend": "friendly", "silent": "not named", "strong": "same suit"}


def wheel():
    W, H, R = 380, 530, 52
    cx, cy = 190, 196
    pos = {"fire": (cx, 66), "earth": (cx + 128, cy), "water": (cx, 326), "air": (cx - 128, cy)}
    s = svg_open(W, H, "Book T's elemental dignities: Fire (Wands) and Water (Cups) are inimical, "
                       "Air (Swords) and Earth (Pentacles) are inimical; Air is friendly with Fire and Water, "
                       "Fire with Earth; the 1912 text does not name Water with Earth.")
    order = [("fire", "earth"), ("earth", "water"), ("water", "air"), ("air", "fire"), ("fire", "water"), ("air", "earth")]
    for a, b in order:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        p1 = (x1 + ux * (R + 4), y1 + uy * (R + 4))
        p2 = (x2 - ux * (R + 4), y2 - uy * (R + 4))
        rel = RELATION[frozenset((a, b))]
        s += f'<line class="ln-{rel}" x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}"/>'
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if (a, b) == ("fire", "water"):
            s += text(cx + 7, cy - 42, REL_WORD[rel], f"t-{rel} b", size=13)
        elif (a, b) == ("air", "earth"):
            s += text(cx + 40, cy - 9, REL_WORD[rel], f"t-{rel} b", "middle", 13)
        else:  # square sides: push the label outward from the centre
            ox, oy = mx - cx, my - cy
            k = 26 / ((ox * ox + oy * oy) ** .5)
            s += text(mx + ox * k, my + oy * k + 5, REL_WORD[rel], f"t-{rel} b", "middle", 13)
    for el, (x, y) in pos.items():
        name, suit, _ = ELEMENTS[el]
        s += f'<circle class="node" cx="{x}" cy="{y}" r="{R}"/>'
        s += glyph(el, x, y - 15, 15)
        s += text(x, y + 17, name.upper(), "b", "middle", 13)
        s += text(x, y + 33, suit, "mut", "middle", 12.5)
    # legend: Book T's own words
    y = 410
    s += f'<line class="rule" x1="6" y1="{y - 24}" x2="{W - 6}" y2="{y - 24}"/>'
    legend = [
        ("strong", "same suit on either side", "\u201c" + bt("strengthen it greatly") + "\u201d"),
        ("friend", "neighbours on the rim", "\u201c" + bt("friendly with") + "\u201d"),
        ("enemy", "opposite natures", "\u201c" + bt("weaken it greatly") + "\u201d"),
        ("silent", "Cups with Pentacles", "not named in 1912"),
    ]
    for i, (rel, lead, words) in enumerate(legend):
        yy = y + i * 30
        s += f'<line class="ln-{rel}" x1="8" y1="{yy - 4}" x2="50" y2="{yy - 4}"/>'
        s += (f'<text x="60" y="{yy}" style="font-size:12.5px"><tspan class="mut">{escape(lead)} </tspan>'
              f'<tspan class="b">{escape(words)}</tspan></text>')
    return s + "</svg>"


# ---------------------------------------------------------------- 2. the court cards
def icon(kind, ox, oy):
    c = 'class="ico"'
    if kind == "steed":
        return (f'<ellipse {c} cx="{ox + 25}" cy="{oy + 38}" rx="17" ry="7"/>'
                + "".join(f'<line {c} x1="{ox + x}" y1="{oy + 43}" x2="{ox + x - 1}" y2="{oy + 57}"/>' for x in (13, 19, 31, 37))
                + f'<polyline {c} points="{ox + 40},{oy + 34} {ox + 47},{oy + 21} {ox + 53},{oy + 26}"/>'
                + f'<line {c} x1="{ox + 24}" y1="{oy + 31}" x2="{ox + 24}" y2="{oy + 17}"/>'
                + f'<circle {c} cx="{ox + 24}" cy="{oy + 11}" r="5"/>')
    if kind == "throne":
        return (f'<polyline {c} points="{ox + 10},{oy + 4} {ox + 10},{oy + 57}"/>'
                + f'<polyline {c} points="{ox + 10},{oy + 38} {ox + 38},{oy + 38} {ox + 38},{oy + 57}"/>'
                + f'<circle {c} cx="{ox + 22}" cy="{oy + 13}" r="5"/>'
                + f'<polyline {c} points="{ox + 22},{oy + 18} {ox + 22},{oy + 33} {ox + 34},{oy + 33} {ox + 34},{oy + 50}"/>')
    if kind == "chariot":
        spokes = "".join(f'<line {c} x1="{ox + 20}" y1="{oy + 48}" x2="{ox + 20 + 9 * dx}" y2="{oy + 48 + 9 * dy}"/>'
                         for dx, dy in ((1, 0), (0, 1), (.7, .7), (-.7, .7)))
        return (f'<rect {c} x="{ox + 6}" y="{oy + 26}" width="34" height="16" rx="2"/>'
                + f'<circle {c} cx="{ox + 20}" cy="{oy + 48}" r="9"/>' + spokes
                + f'<line {c} x1="{ox + 40}" y1="{oy + 36}" x2="{ox + 54}" y2="{oy + 31}"/>'
                + f'<circle {c} cx="{ox + 24}" cy="{oy + 10}" r="5"/>'
                + f'<line {c} x1="{ox + 24}" y1="{oy + 15}" x2="{ox + 24}" y2="{oy + 26}"/>')
    # standing
    return (f'<circle {c} cx="{ox + 26}" cy="{oy + 9}" r="5"/>'
            + f'<line {c} x1="{ox + 26}" y1="{oy + 14}" x2="{ox + 26}" y2="{oy + 38}"/>'
            + f'<polyline {c} points="{ox + 19},{oy + 57} {ox + 26},{oy + 38} {ox + 33},{oy + 57}"/>'
            + f'<line {c} x1="{ox + 15}" y1="{oy + 24}" x2="{ox + 37}" y2="{oy + 24}"/>')


COURTS = [  # Book T, "The Sixteen Court, or Royal Cards"; the 1912 names from "The Titles of the Symbols"
    dict(gd="King", posture="steed", quote=bt("Figures mounted on steeds"), letter="Yod",
         printed="Knight", rws="swords-knight", rws_name="Knight of Swords",
         waite=waite("He is riding in full course"), same=True),
    dict(gd="Queen", posture="throne", quote=bt("seated upon Thrones"), letter="He",
         printed="Queen", rws="swords-queen", rws_name="Queen of Swords",
         waite=waite("the hilt rests on an arm of her royal chair"), same=True),
    dict(gd="Prince", posture="chariot", quote=bt("Figures seated in Chariots, and thus borne forward"), letter="Vau",
         printed="King", rws="swords-king", rws_name="King of Swords",
         waite=waite("He sits in judgment"), same=False),
    dict(gd="Princess", posture="standing", quote=bt("figures of Amazons, standing firmly of themselves"), letter="He final",
         printed="Knave", rws="swords-page", rws_name="Page of Swords",
         waite=waite("in the act of swift walking"), same=True),
]
bt("Note that the Kings are now called Knights, and the Princes are now called Kings.")


def courts():
    W, top, RH = 360, 58, 156
    H = top + RH * 4 + 6
    s = svg_open(W, H, "Book T's four court figures beside the Rider-Waite-Smith Swords courts: mounted King "
                       "printed as Knight; enthroned Queen; Prince in a chariot printed as King, where Waite's King sits "
                       "on a throne; standing Princess printed as Knave, Waite's Page.")
    s += text(8, 20, "BOOK T", "b gold", size=12) + text(8, 36, "the Order’s text, printed 1912", "mut", size=10)
    s += text(200, 20, "RIDER–WAITE–SMITH", "b gold", size=12) + text(200, 36, "the deck, 1909", "mut", size=10)
    for i, c in enumerate(COURTS):
        y0 = top + i * RH
        s += f'<line class="rule" x1="0" y1="{y0}" x2="{W}" y2="{y0}"/>'
        s += icon(c["posture"], 6, y0 + 16)
        s += text(70, y0 + 28, c["gd"], "ser b", size=17)
        s += text(70, y0 + 46, f"“{c['quote']}”", "it", size=10.5, n=19, lh=13)
        nq = len(wrap(f"“{c['quote']}”", 19))
        s += text(70, y0 + 50 + nq * 13, f"letter: {c['letter']}", "mut", size=10)
        s += text(8, y0 + RH - 14, f"printed 1912 as “{c['printed']}”", "gold b", size=10)
        s += f'<polyline class="ico" points="{180},{y0 + 70} {190},{y0 + 78} {180},{y0 + 86}"/>'
        s += (f'<a href="{CARDS}{c["rws"]}"><rect class="card" x="198" y="{y0 + 16}" width="66" height="112"/>'
              f'<image href="{escape(img(c["rws"]))}" x="199" y="{y0 + 17}" width="64" height="110" '
              f'preserveAspectRatio="xMidYMid meet"><title>{escape(c["rws_name"])}, Rider-Waite-Smith 1909</title></image></a>')
        s += text(272, y0 + 30, c["rws_name"], "b", size=11.5, n=12, lh=14)
        s += text(272, y0 + 64, f"“{c['waite']}”", "it", size=10.5, n=15, lh=13)
        tag = "same posture" if c["same"] else "posture changed"
        s += text(272, y0 + RH - 14, tag, "t-friend b" if c["same"] else "t-enemy b", size=10)
    return s + "</svg>"


# ---------------------------------------------------------------- 3. the worked example
# Book T, "The Twenty-Two Keys of the Book": the attribution of each key (checked below).
CARD = {
    "swords-king": dict(name="King of Swords", attr="Swords", el="air", ed=False),
    "major-05-the-hierophant": dict(name="The Hierophant", attr="Taurus", el="earth", ed=True),
    "pentacles-ace": dict(name="Ace of Pentacles", attr="Pentacles", el="earth", ed=False),
    "major-16-the-tower": dict(name="The Tower", attr="Mars", el=None, ed=False),
    "major-01-the-magician": dict(name="The Magician", attr="Mercury", el=None, ed=False),
    "major-07-the-chariot": dict(name="The Chariot", attr="Cancer", el="water", ed=True),
    "major-04-the-emperor": dict(name="The Emperor", attr="Aries", el="fire", ed=True),
    "major-15-the-devil": dict(name="The Devil", attr="Capricorn", el="earth", ed=True),
}
for title, attr in [("The Hierophant", "Taurus"), ("The Blasted Tower", "Mars"), ("The Magician", "Mercury"),
                    ("The Chariot", "Cancer"), ("The Emperor", "Aries"), ("The Devil", "Capricorn")]:
    if not re.search(re.escape(title) + r" \|[^|]*\|[^|]*\| " + re.escape(attr) + r" \|", BOOK_T_TEXT):
        sys.exit(f"Book T's key table does not give {title} = {attr}")
ISSUE, BODY = "swords-king", "major-15-the-devil"
PAIRS = [("major-05-the-hierophant", "pentacles-ace"), ("major-16-the-tower", "major-01-the-magician"),
         ("major-07-the-chariot", "major-04-the-emperor")]
MAJORITY = bt("A Majority of Keys | Strong forces beyond the Querent's control.").split(" | ")
ACES = bt("Aces are always strong cards.")
REL_PAIR = {"strong": "strengthen", "enemy": "weaken", "friend": "support", "silent": "rule silent"}


def pair_rel(a, b):
    ea, eb = CARD[a]["el"], CARD[b]["el"]
    if not ea or not eb:
        return "silent"
    if ea == eb:
        return "strong"
    return RELATION[frozenset((ea, eb))]


def card(cid, x, y, role=None):
    c = CARD[cid]
    s = ""
    if role:
        s += text(x + 32, y - 8, role.upper(), "gold b", "middle", 10)
    s += (f'<a href="{CARDS}{cid}"><rect class="card" x="{x - 1}" y="{y - 1}" width="66" height="112"/>'
          f'<image href="{escape(img(cid))}" x="{x}" y="{y}" width="64" height="110" preserveAspectRatio="xMidYMid meet">'
          f'<title>{escape(c["name"])}, Rider-Waite-Smith 1909</title></image></a>')
    s += text(x + 32, y + 126, c["name"], "b", "middle", 11)
    label = c["attr"] + ("*" if c["ed"] else "")
    if c["el"]:
        label += " · " + ELEMENTS[c["el"]][0]
        s += glyph(c["el"], x + 32, y + 150, 7)
        s += text(x + 32, y + 141, label, "mut", "middle", 10)
    else:
        s += text(x + 32, y + 141, label + " · a planet", "mut", "middle", 10)
    return s


def link(x1, x2, y, rel):
    s = f'<line class="ln-{rel}" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>'
    return s + text((x1 + x2) / 2, y - 9, REL_PAIR[rel], f"t-{rel} b", "middle", 11.5)


def tally(x, y, w):
    kinds = ["key"] * 6 + ["court", "ace"]
    s = ""
    for i, k in enumerate(kinds):
        s += f'<rect class="tile-{k}" x="{x + i * 26}" y="{y}" width="20" height="30" rx="3"/>'
    s += text(x, y + 50, "6 keys \u00b7 1 court \u00b7 1 ace, of 8 cards", "b", size=12)
    s += text(x, y + 72, f"Book T: \u201c{MAJORITY[0]}: {MAJORITY[1]}\u201d", "it", size=12, n=int(w / 6.4), lh=15)
    nl = len(wrap(f"Book T: \u201c{MAJORITY[0]}: {MAJORITY[1]}\u201d", int(w / 6.4)))
    s += text(x, y + 76 + nl * 15, f"\u201c{ACES}\u201d", "it", size=12)
    return s


FOOT = "* a sign read by its element: our step, not Book T\u2019s, whose rule names suits only."


def example_narrow():
    W, RH = 360, 186
    H = 40 + 5 * RH + 172
    s = svg_open(W, H, "A reading, Oct 2026, with the dignity drawn inside each pair (narrow layout).")
    s += text(8, 22, "a reading, Oct 2026", "ser b", size=15)
    y = 52
    s += card(ISSUE, 148, y, "issue")
    for i, (a, b) in enumerate(PAIRS):
        y = 52 + (i + 1) * RH
        s += f'<rect class="pairbg" x="14" y="{y - 22}" width="{W - 28}" height="{RH - 6}" rx="10"/>'
        s += text(180, y - 8, f"PAIR {i + 1}", "gold b", "middle", 10)
        s += card(a, 36, y) + card(b, 260, y)
        s += link(106, 254, y + 55, pair_rel(a, b))
    y = 52 + 4 * RH
    s += card(BODY, 148, y, "body")
    y = 52 + 5 * RH - 6
    s += f'<line class="rule" x1="0" y1="{y - 14}" x2="{W}" y2="{y - 14}"/>'
    s += tally(8, y, W - 16)
    s += text(8, y + 132, FOOT, "mut", size=10.5, n=58, lh=13)
    return s + "</svg>"


def example_wide():
    W, H = 800, 660
    s = svg_open(W, H, "A reading, Oct 2026, with the dignity drawn inside each pair (wide layout).")
    s += text(6, 24, "a reading, Oct 2026", "ser b", size=17)
    s += card(ISSUE, 368, 52, "issue")
    for i, (a, b) in enumerate(PAIRS):
        c = 134 + i * 266
        s += f'<rect class="pairbg" x="{c - 122}" y="248" width="244" height="214" rx="10"/>'
        s += text(c, 266, f"PAIR {i + 1}", "gold b", "middle", 10.5)
        s += card(a, c - 104, 280) + card(b, c + 40, 280)
        s += link(c - 34, c + 34, 335, pair_rel(a, b))
    s += card(BODY, 368, 500, "body")
    s += tally(16, 512, 320)
    s += text(470, 540, FOOT, "mut", size=11.5, n=44, lh=15)
    return s + "</svg>"


# ---------------------------------------------------------------- 4. the timeline
EVENTS = [  # (year label, lane, title, line, icon) -- each line cited in the chapter text
    ("1781", "pub", "Court de Gébelin", "Le Monde primitif VIII: the tarot as an Egyptian “Book of Thoth”", None),
    ("1783–85", "pub", "Etteilla’s tarot books", "upright and reversed meanings; his deck of 1788–89 prints both", "rev"),
    ("1888", "pub", "Mathers’ booklet", "“R. means Reversed”", "rev"),
    ("1888", "inn", "Golden Dawn founded", "Book T kept in manuscript; members copy the cards by hand", "dig"),
    ("1909", "pub", "Rider–Waite–Smith deck", "by two members: Waite (joined 1891), Smith (1901)", None),
    ("1910/11", "pub", "Pictorial Key", "a “Reversed” meaning for each card", "rev"),
    ("1912", "inn", "Book T printed", "The Equinox I(8): “" + bt("well dignified or ill dignified") + "”", "dig"),
]


def ev_icon(kind, x, y):
    if kind == "rev":  # a card with an upside-down R
        return (f'<rect class="card" x="{x}" y="{y}" width="20" height="30" rx="2"/>'
                f'<text x="{x + 10}" y="{y + 15}" class="b t-enemy" text-anchor="middle" '
                f'transform="rotate(180 {x + 10} {y + 15})" dy="5" style="font-size:15px">R</text>')
    if kind == "dig":  # three cards in a row, linked
        return "".join(f'<rect class="card" x="{x + i * 13}" y="{y + 2}" width="10" height="16" rx="1.5"/>' for i in range(3)) \
            + f'<line class="ln-friend" x1="{x + 5}" y1="{y + 22}" x2="{x + 31}" y2="{y + 22}" style="stroke-width:2"/>'
    return ""


def _years():
    years = []
    for e in EVENTS:
        if e[0] not in years:
            years.append(e[0])
    return years


def lane_label(x, y, head, word, cls, anchor):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font-size:11.5px"><tspan class="b gold">{escape(head)} \u00b7 </tspan>'
            f'<tspan class="b {cls}">{escape(word)}</tspan></text>')


def timeline_narrow():
    W, RH = 360, 104
    years = _years()
    H = 70 + len(years) * RH
    s = svg_open(W, H, "Timeline, 1781 to 1912: reversals in the printed, public books; dignities inside the Order "
                       "until Book T was printed in 1912 (narrow layout).")
    s += text(170, 18, "PRINTED FOR ANYONE", "b gold", "end", 11)
    s += text(170, 33, "reversals", "t-enemy b", "end", 11)
    s += text(190, 18, "INSIDE THE ORDER", "b gold", "start", 11)
    s += text(190, 33, "dignities", "t-friend b", "start", 11)
    s += f'<line class="spine" x1="180" y1="44" x2="180" y2="{H - 10}"/>'
    for i, yl in enumerate(years):
        y = 70 + i * RH
        s += f'<rect class="pill" x="152" y="{y - 13}" width="56" height="22" rx="11"/>'
        s += text(180, y + 2, yl, "b", "middle", 11)
        for e in EVENTS:
            if e[0] != yl:
                continue
            pub = e[1] == "pub"
            x, anchor = (146, "end") if pub else (214, "start")
            if e[4]:
                s += ev_icon(e[4], 4 if pub else W - 38, y - 12)
            s += text(x, y + 2, e[2], "b", anchor, 12, n=15, lh=14)
            nt = len(wrap(e[2], 15))
            s += text(x, y + 6 + nt * 15, e[3], "mut", anchor, 10.5, n=21, lh=13)
    return s + "</svg>"


def timeline_wide():
    W, H = 800, 340
    years = _years()
    s = svg_open(W, H, "Timeline, 1781 to 1912: reversals in the printed, public books above the line; dignities "
                       "inside the Order below it, until Book T was printed in 1912 (wide layout).")
    ax = 176
    s += lane_label(6, 18, "PRINTED FOR ANYONE", "reversals", "t-enemy", "start")
    s += lane_label(6, H - 8, "INSIDE THE ORDER", "dignities", "t-friend", "start")
    s += f'<line class="spine" x1="10" y1="{ax}" x2="{W - 10}" y2="{ax}"/>'
    s += text(W - 10, 18, "not to scale", "mut", "end", 10.5)
    step = (W - 130) / (len(years) - 1)
    for i, yl in enumerate(years):
        x = 65 + i * step
        s += f'<rect class="pill" x="{x - 32}" y="{ax - 12}" width="64" height="24" rx="12"/>'
        s += text(x, ax + 5, yl, "b", "middle", 12)
        for e in EVENTS:
            if e[0] != yl:
                continue
            if e[1] == "pub":
                s += ev_icon(e[4], x - 10, 30) if e[4] else ""
                s += text(x, 82, e[2], "b", "middle", 12.5, n=18, lh=15)
                nt = len(wrap(e[2], 18))
                s += text(x, 86 + nt * 15, e[3], "mut", "middle", 11, n=21, lh=13)
            else:
                s += ev_icon(e[4], x - 18, 200) if e[4] else ""
                s += text(x, 244, e[2], "b", "middle", 12.5, n=18, lh=15)
                nt = len(wrap(e[2], 18))
                s += text(x, 248 + nt * 15, e[3], "mut", "middle", 11, n=21, lh=13)
    return s + "</svg>"


# ---------------------------------------------------------------- assemble
CAPTIONS = {
    "wheel": "<strong>Figure 1.</strong> <strong>ed.</strong> Book T’s rule of dignities as a wheel. Opposite elements "
             "face each other across the circle and weaken a card between them; neighbours round the rim are friendly. "
             "The 1912 text names every pair but Cups with Pentacles, left dotted.",
    "courts": "<strong>Figure 2.</strong> <strong>ed.</strong> The four court figures of Book T beside Waite and Smith’s "
              "Swords. Rows follow the 1912 printing’s own names. The card both call King of Swords is a different "
              "figure in each: a Prince in a chariot, a King on a throne. Card images: Rider–Waite–Smith, 1909.",
    "timeline": "<strong>Figure 3.</strong> <strong>ed.</strong> Two layers, 1781 to 1912. On one side, the books printed "
                "for anyone, with reversed meanings; on the other, the Order’s text, read by dignity, which reached "
                "print in 1912. An upside-down R marks a book that gives reversed meanings; three linked cards mark reading "
                "by neighbours.",
    "example": "<strong>Figure 4.</strong> <strong>ed.</strong> A reading, Oct 2026. The line inside each pair is Book T’s "
               "dignity: green for the same element, red dashes for opposite natures, dotted where the rule is silent. "
               "The tiles count what the spread holds most of.",
}


def build():
    return {
        "wheel": figure([("", wheel())], CAPTIONS["wheel"]),
        "courts": figure([("gdd-tall", courts())], CAPTIONS["courts"]),
        "timeline": figure([("gdd-narrow", timeline_narrow()), ("gdd-wide", timeline_wide())], CAPTIONS["timeline"]),
        "example": figure([("gdd-narrow gdd-tall", example_narrow()), ("gdd-wide", example_wide())], CAPTIONS["example"]),
    }


def main():
    check = "--check" in sys.argv
    with open(MDX, encoding="utf-8") as f:
        src = f.read()
    out = src
    for name, html in build().items():
        pat = re.compile(r"(<!-- figure:%s -->\n)(.*?)(<!-- /figure:%s -->)" % (name, name), re.S)
        if not pat.search(out):
            sys.exit(f"marker for figure {name!r} missing in {MDX}")
        out = pat.sub(lambda m: m.group(1) + html + "\n" + m.group(3), out)
    if check:
        if out != src:
            sys.exit("figures out of date: run python scripts/build_gd_dignity_figures.py")
        print("gd dignity figures: up to date")
        return
    with open(MDX, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("gd dignity figures: written")


if __name__ == "__main__":
    main()
