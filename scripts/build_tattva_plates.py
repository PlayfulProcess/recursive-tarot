#!/usr/bin/env python3
"""
build_tattva_plates.py — constructed-geometry yantra plates for the 36 Tattvas deck.

Generates one deterministic SVG per grammar item (56 total) under
tarot/thirty-six-tattvas/plates/, plus a CONTACT-SHEET.html that renders all
56 at thumbnail size grouped by family, so the set can be judged as a set.

Design thesis: these are yantras — constructed, not painted. Exact geometry,
bilateral/radial symmetry, a bindu at centre, restraint. One shared system
(palette / stroke weights / 400x400 grid / margins) governs all 56 plates;
only the parameters vary per card. Re-running this script reproduces
byte-identical files — no randomness, no timestamps.

Does NOT touch grammar.json. Does NOT run git.
"""

import math
import os
import sys
from xml.sax.saxutils import escape

# Make console output safe on Windows terminals stuck on a legacy codepage —
# group names contain diacritics (Śaktis, Kañcukas, ...).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PLATES_DIR = os.path.join(REPO_ROOT, "tarot", "thirty-six-tattvas", "plates")
CONTACT_SHEET_PATH = os.path.join(PLATES_DIR, "CONTACT-SHEET.html")

# --------------------------------------------------------------------------
# Shared system: palette, stroke weights, grid — the ONE place to edit it
# --------------------------------------------------------------------------

VIEWBOX = "0 0 400 400"
CENTER = (200.0, 200.0)

GROUND = "#f7f3e8"   # site parchment ground
INK = "#221f1a"       # site ink
GOLD = "#9a7322"      # site gold
MUTED = "#cbbf9f"     # site muted line
FAINT = "#e0d6bd"     # site faint line

STROKE_THIN = 1.0
STROKE = 1.6
STROKE_HEAVY = 2.2

# The five gross-element colours, muted to sit on parchment rather than
# shout (hard constraint). Used wherever a card's metadata.element or
# metadata.shakti->element resolves to one of these five.
ELEMENT_COLOR = {
    "akasha": "#3f5872",   # deep muted blue  — space
    "vayu": "#5f7562",     # grey-green       — air
    "tejas": "#a13f2e",    # muted red        — fire
    "jala": "#7c8896",     # silver-grey      — water
    "prithvi": "#a9761f",  # yellow-ochre     — earth
}
SHAKTI_ELEMENT = {"cit": "akasha", "ananda": "jala", "iccha": "tejas", "jnana": "vayu", "kriya": "prithvi"}

# A handful of one-off blended tones used where the briefs specify a colour
# that isn't one of the five pure element tones (kept in the same muted
# parchment-safe family as everything else).
ROSE_GOLD = "#b9865a"
GOLD_GREEN = "#8f8a4a"
VIOLET = "#6b4a72"
COOL_GREY_BLUE = "#5a6b78"
ROSE_BROWN = "#9a6b55"
DUSTY_ROSE = "#b5768a"

FRAME_INSET = 24.0

# --------------------------------------------------------------------------
# Numeric / SVG primitives
# --------------------------------------------------------------------------


def n(x):
    """Deterministic number formatting."""
    return f"{x:.2f}"


def pt(cx, cy, angle_deg, r):
    """Point at angle (0 = straight up, clockwise) and radius r from (cx,cy)."""
    rad = math.radians(angle_deg)
    return (cx + r * math.sin(rad), cy - r * math.cos(rad))


def bindu(cx, cy, r, color=INK, opacity=1.0, outline=False):
    """A bindu: the point of concentration. `outline=True` renders it
    uncoloured (ground-filled, ink outline) for the deck's 'white bindu'
    cards — the unconditioned core no covering reaches."""
    if outline:
        return (f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" '
                 f'fill="{GROUND}" stroke="{INK}" stroke-width="{STROKE_THIN}"/>')
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{color}" opacity="{opacity}"/>'


def circle_outline(cx, cy, r, color=INK, width=STROKE, opacity=1.0):
    return (f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="none" '
            f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>')


def circle_fill(cx, cy, r, color, opacity=1.0):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{color}" opacity="{opacity}" stroke="none"/>'


def square_outline(cx, cy, half, color=INK, width=STROKE, rotate=0, opacity=1.0, fill="none"):
    x, y, size = cx - half, cy - half, half * 2
    t = f' transform="rotate({rotate} {n(cx)} {n(cy)})"' if rotate else ""
    return (f'<rect x="{n(x)}" y="{n(y)}" width="{n(size)}" height="{n(size)}" '
            f'fill="{fill}" stroke="{color}" stroke-width="{width}" opacity="{opacity}"{t}/>')


def triangle_pts(cx, cy, size, direction="up"):
    if direction == "up":
        apex = (cx, cy - size)
        bl = (cx - size * 0.866, cy + size * 0.5)
        br = (cx + size * 0.866, cy + size * 0.5)
    else:
        apex = (cx, cy + size)
        bl = (cx - size * 0.866, cy - size * 0.5)
        br = (cx + size * 0.866, cy - size * 0.5)
    return [apex, bl, br]


def triangle(cx, cy, size, color=INK, width=STROKE, direction="up", fill="none", opacity=1.0):
    p = triangle_pts(cx, cy, size, direction)
    pts_str = " ".join(f"{n(x)},{n(y)}" for x, y in p)
    return f'<polygon points="{pts_str}" fill="{fill}" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>'


def line_el(x1, y1, x2, y2, color=INK, width=STROKE, opacity=1.0):
    return (f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" '
            f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>')


def rays(cx, cy, r_inner, r_outer, count, color=INK, width=STROKE_THIN, start_angle=0,
         opacity=1.0, bend=0.0, arrow=False, hook=False, fade=False):
    """A ring of `count` evenly spaced rays. `bend` gives a gentle wind-curve
    (perpendicular bezier bulge); `arrow` adds a small targeting arrowhead;
    `hook` curls the tip back toward centre (the taste/rasanā treatment);
    `fade` dims the whole set (the elimination/pāyu treatment)."""
    parts = []
    op = opacity * (0.55 if fade else 1.0)
    for i in range(count):
        angle = start_angle + i * (360.0 / count)
        x1, y1 = pt(cx, cy, angle, r_inner)
        x2, y2 = pt(cx, cy, angle, r_outer)
        if hook:
            xm, ym = pt(cx, cy, angle, r_outer * 0.85)
            xc, yc = pt(cx, cy, angle + 6, r_outer * 0.85)
            xe, ye = pt(cx, cy, angle + 14, r_outer * 0.68)
            parts.append(f'<path d="M {n(x1)} {n(y1)} L {n(xm)} {n(ym)} Q {n(xc)} {n(yc)} {n(xe)} {n(ye)}" '
                         f'fill="none" stroke="{color}" stroke-width="{width}" opacity="{op}"/>')
        elif bend:
            rad = math.radians(angle)
            perp = (math.cos(rad), math.sin(rad))
            mx = (x1 + x2) / 2 + perp[0] * bend
            my = (y1 + y2) / 2 + perp[1] * bend
            parts.append(f'<path d="M {n(x1)} {n(y1)} Q {n(mx)} {n(my)} {n(x2)} {n(y2)}" '
                         f'fill="none" stroke="{color}" stroke-width="{width}" opacity="{op}"/>')
        else:
            parts.append(line_el(x1, y1, x2, y2, color, width, op))
        if arrow:
            a1, a2 = angle - 8, angle + 8
            ax1, ay1 = pt(cx, cy, a1, r_outer - 9)
            ax2, ay2 = pt(cx, cy, a2, r_outer - 9)
            parts.append(f'<polyline points="{n(ax1)},{n(ay1)} {n(x2)},{n(y2)} {n(ax2)},{n(ay2)}" '
                         f'fill="none" stroke="{color}" stroke-width="{width}" opacity="{op}"/>')
    return "\n".join(parts)


def ray_cluster(cx, cy, center_angle, spread, count, r_inner, r_outer, color, width=STROKE_THIN, opacity=1.0):
    """A biased cluster of rays within one arc — the directional 'lean' used
    for locomotion (pāda): more, longer rays on the side of travel."""
    if count == 1:
        angles = [center_angle]
    else:
        step = spread / (count - 1)
        angles = [center_angle - spread / 2 + i * step for i in range(count)]
    parts = []
    for angle in angles:
        x1, y1 = pt(cx, cy, angle, r_inner)
        x2, y2 = pt(cx, cy, angle, r_outer)
        parts.append(line_el(x1, y1, x2, y2, color, width, opacity))
    return "\n".join(parts)


def rings(cx, cy, r_start, count, r_end, color=INK, width=STROKE_THIN, opacity=1.0):
    if count <= 1:
        radii = [r_start]
    else:
        step = (r_end - r_start) / (count - 1)
        radii = [r_start + i * step for i in range(count)]
    return "\n".join(circle_outline(cx, cy, r, color, width, opacity) for r in radii)


def lotus(cx, cy, r, petals, color=INK, width=STROKE_THIN, fraction=1.0, fill="none", accent=None, accent_r=3.0):
    petal_r = r * fraction
    parts = []
    for i in range(petals):
        angle = i * (360.0 / petals)
        tip = pt(cx, cy, angle, petal_r)
        half_w = (360.0 / petals) * 0.28
        c1 = pt(cx, cy, angle - half_w, petal_r * 0.55)
        c2 = pt(cx, cy, angle + half_w, petal_r * 0.55)
        d = (f'M {n(cx)} {n(cy)} Q {n(c1[0])} {n(c1[1])} {n(tip[0])} {n(tip[1])} '
             f'Q {n(c2[0])} {n(c2[1])} {n(cx)} {n(cy)} Z')
        parts.append(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>')
        if accent:
            parts.append(circle_fill(tip[0], tip[1], accent_r, accent, 0.6))
    return "\n".join(parts)


def colored_lotus(cx, cy, r, petals, colors, width=STROKE_THIN, fraction=0.85, opacity=0.55):
    petal_r = r * fraction
    parts = []
    for i in range(petals):
        angle = i * (360.0 / petals)
        tip = pt(cx, cy, angle, petal_r)
        half_w = (360.0 / petals) * 0.28
        c1 = pt(cx, cy, angle - half_w, petal_r * 0.55)
        c2 = pt(cx, cy, angle + half_w, petal_r * 0.55)
        color = colors[i % len(colors)]
        d = (f'M {n(cx)} {n(cy)} Q {n(c1[0])} {n(c1[1])} {n(tip[0])} {n(tip[1])} '
             f'Q {n(c2[0])} {n(c2[1])} {n(cx)} {n(cy)} Z')
        parts.append(f'<path d="{d}" fill="{color}" fill-opacity="{opacity}" stroke="{INK}" stroke-width="{width}"/>')
    return "\n".join(parts)


def crescent(cx, cy, r, color, fill_opacity=0.55, stroke_width=STROKE_THIN, offset_frac=0.55, orientation=0):
    """A silver crescent (ap/water): outer arc minus a smaller inner arc."""
    top = (cx, cy - r)
    bottom = (cx, cy + r)
    inner_rx = r * offset_frac
    d = (f'M {n(top[0])} {n(top[1])} A {n(r)} {n(r)} 0 1 1 {n(bottom[0])} {n(bottom[1])} '
         f'A {n(inner_rx)} {n(r)} 0 1 0 {n(top[0])} {n(top[1])} Z')
    t = f' transform="rotate({orientation} {n(cx)} {n(cy)})"' if orientation else ""
    return f'<path d="{d}" fill="{color}" opacity="{fill_opacity}" stroke="{color}" stroke-width="{stroke_width}"{t}/>'


def six_dot(cx, cy, r, color, dot_r=3.4, opacity=1.0):
    parts = []
    for i in range(6):
        x, y = pt(cx, cy, i * 60, r)
        parts.append(circle_fill(x, y, dot_r, color, opacity))
    return "\n".join(parts)


def hatch_diagonal(cx, cy, half, color, width=STROKE_THIN, count=5, opacity=0.7):
    parts = []
    for i in range(count):
        t = (i + 1) / (count + 1)
        x1, y1 = cx - half + t * 2 * half, cy - half
        x2, y2 = cx - half, cy - half + t * 2 * half
        parts.append(line_el(x1, y1, x2, y2, color, width, opacity))
    return "\n".join(parts)


def veil_bands(cx, cy, half, count, color=None, colors=None, opacity=0.5, width=STROKE_THIN):
    parts = []
    for i in range(count):
        y = cy - half + (i + 0.5) * (2 * half / count)
        c = colors[i] if colors else color
        parts.append(line_el(cx - half, y, cx + half, y, c, width, opacity))
    return "\n".join(parts)


def ticks(cx, cy, angle, r, length, color=FAINT, width=1.0, opacity=1.0):
    x1, y1 = pt(cx, cy, angle, r - length / 2)
    x2, y2 = pt(cx, cy, angle, r + length / 2)
    return line_el(x1, y1, x2, y2, color, width, opacity)


# --------------------------------------------------------------------------
# The shared frame — same border, same construction-grid ticks, every plate
# --------------------------------------------------------------------------

def frame_svg():
    cx, cy = CENTER
    half = 200 - FRAME_INSET
    parts = [square_outline(cx, cy, half, MUTED, 1.2)]
    # four midpoint construction ticks, one per edge — the shared grid mark
    for angle in (0, 90, 180, 270):
        parts.append(ticks(cx, cy, angle, half, 10, FAINT, 1.0, 1.0))
    return "\n".join(parts)


FRAME_SVG = frame_svg()


def svg_doc(item_id, title, body):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VIEWBOX}" width="400" height="400" '
        f'role="img" aria-labelledby="title-{item_id}">\n'
        f'<title id="title-{item_id}">{escape(title)}</title>\n'
        f'<rect x="0" y="0" width="400" height="400" fill="{GROUND}"/>\n'
        f'{FRAME_SVG}\n'
        f'<g fill="none" stroke="{INK}" stroke-width="{STROKE}" stroke-linecap="round" stroke-linejoin="round">\n'
        f'{body}\n'
        '</g>\n'
        '</svg>\n'
    )


# ==========================================================================
# FAMILY 1 — The Five Śaktis
# ==========================================================================

SHAKTI_PARAMS = {
    "shakti-cit": dict(mode="rays", rays=16, r_outer=145, color=ELEMENT_COLOR["akasha"], bindu_r=6),
    "shakti-ananda": dict(mode="lotus", petals=8, r=105, fraction=0.55, color=ELEMENT_COLOR["jala"],
                           bindu_r=6, accent="#c98a4b"),
    "shakti-iccha": dict(mode="triangle", size=120, color=ELEMENT_COLOR["tejas"], bindu_r=7),
    "shakti-jnana": dict(mode="circle_rays", r=112, ray_len=20, rays=12, color=ELEMENT_COLOR["vayu"], bindu_r=5),
    "shakti-kriya": dict(mode="diamond", half=95, color=ELEMENT_COLOR["prithvi"], bindu_r=7),
}


def render_shakti(item_id):
    p = SHAKTI_PARAMS[item_id]
    cx, cy = CENTER
    color = p["color"]
    parts = []
    if p["mode"] == "rays":
        parts.append(rays(cx, cy, 0, p["r_outer"], p["rays"], color, STROKE_THIN))
        parts.append(bindu(cx, cy, p["bindu_r"], color))
    elif p["mode"] == "lotus":
        parts.append(lotus(cx, cy, p["r"], p["petals"], color, STROKE_THIN, p["fraction"], accent=p.get("accent")))
        parts.append(bindu(cx, cy, p["bindu_r"], color))
    elif p["mode"] == "triangle":
        parts.append(triangle(cx, cy, p["size"], color, STROKE))
        ax, ay = cx, cy - p["size"]
        parts.append(bindu(ax, ay, p["bindu_r"], color))
    elif p["mode"] == "circle_rays":
        parts.append(circle_outline(cx, cy, p["r"], color, STROKE))
        parts.append(rays(cx, cy, p["r"], p["r"] + p["ray_len"], p["rays"], color, STROKE_THIN))
        parts.append(bindu(cx, cy, p["bindu_r"], color))
    elif p["mode"] == "diamond":
        parts.append(square_outline(cx, cy, p["half"], color, STROKE_HEAVY, rotate=45))
        parts.append(hatch_diagonal(cx, cy, p["half"] * 0.7, color))
        parts.append(bindu(cx, cy, p["bindu_r"], color))
    return "\n".join(parts)


# ==========================================================================
# FAMILY 2 — The Five Pure Tattvas (1–5): aham/idam progression
# ==========================================================================

PURE_TATTVA_PARAMS = {
    "tattva-01": dict(mode="rays", rays=32, r_outer=155, color=ELEMENT_COLOR["akasha"], bindu_r=6, width=STROKE_THIN),
    "tattva-02": dict(mode="lotus", petals=12, r=118, fraction=0.8, color=ROSE_GOLD, bindu_r=7),
    "tattva-03": dict(mode="triangle", size=100, color=ELEMENT_COLOR["tejas"], bindu_r=5, opacity=0.55),
    "tattva-04": dict(mode="circle_inv_triangle", r=118, tsize=88, color=GOLD_GREEN, bindu_r=6),
    "tattva-05": dict(mode="hexagram", size=108, bindu_r=9),
}


def render_pure_tattva(item_id):
    p = PURE_TATTVA_PARAMS[item_id]
    cx, cy = CENTER
    color = p.get("color", INK)
    parts = []
    if p["mode"] == "rays":
        parts.append(rays(cx, cy, 0, p["r_outer"], p["rays"], color, p.get("width", STROKE_THIN)))
        parts.append(bindu(cx, cy, p["bindu_r"], color))
    elif p["mode"] == "lotus":
        parts.append(lotus(cx, cy, p["r"], p["petals"], color, STROKE_THIN, p["fraction"]))
        parts.append(bindu(cx, cy, p["bindu_r"], color))
    elif p["mode"] == "triangle":
        op = p.get("opacity", 1.0)
        parts.append(triangle(cx, cy, p["size"], color, STROKE_THIN, opacity=op))
        parts.append(bindu(cx, cy - p["size"], p["bindu_r"], color, opacity=max(op, 0.7)))
    elif p["mode"] == "circle_inv_triangle":
        parts.append(circle_outline(cx, cy, p["r"], color, STROKE + 0.2))
        parts.append(triangle(cx, cy, p["tsize"], color, STROKE, direction="down"))
        parts.append(bindu(cx, cy, p["bindu_r"], color))
    elif p["mode"] == "hexagram":
        parts.append(triangle(cx, cy, p["size"], INK, STROKE, direction="up"))
        parts.append(triangle(cx, cy, p["size"], INK, STROKE, direction="down"))
        parts.append(bindu(cx, cy, p["bindu_r"], outline=True))
    return "\n".join(parts)


# ==========================================================================
# FAMILY 3 — The Seven Kañcukas (6–12): one square-in-circle-or-square
#   pattern, growing tattva by tattva, per the grammar's own text.
# ==========================================================================

KANCUKA_PARAMS = {
    "tattva-06": dict(mode="veil", outer_r=132, half=92, bands=5, color=VIOLET),
    "tattva-07": dict(mode="rings", half=70, ring_count=3, color=ELEMENT_COLOR["prithvi"]),
    "tattva-08": dict(mode="rings", half=82, ring_count=3, color=ELEMENT_COLOR["vayu"]),
    "tattva-09": dict(mode="rings", half=94, ring_count=3, color=ELEMENT_COLOR["jala"]),
    "tattva-10": dict(mode="rings", half=106, ring_count=4, color=ELEMENT_COLOR["akasha"], tight=True),
    "tattva-11": dict(mode="rings", half=120, ring_count=3, color=ELEMENT_COLOR["tejas"]),
    "tattva-12": dict(mode="veil", outer_r=132, half=92, bands=5,
                       colors=[ELEMENT_COLOR["prithvi"], ELEMENT_COLOR["vayu"], ELEMENT_COLOR["jala"],
                               ELEMENT_COLOR["akasha"], ELEMENT_COLOR["tejas"]],
                       bindu=True),
}


def render_kancuka(item_id):
    p = KANCUKA_PARAMS[item_id]
    cx, cy = CENTER
    parts = []
    if p["mode"] == "veil":
        parts.append(circle_outline(cx, cy, p["outer_r"], INK, STROKE))
        parts.append(square_outline(cx, cy, p["half"], INK, STROKE))
        if "colors" in p:
            parts.append(veil_bands(cx, cy, p["half"], p["bands"], colors=p["colors"], opacity=0.5, width=1.4))
        else:
            parts.append(veil_bands(cx, cy, p["half"], p["bands"], color=p["color"], opacity=0.55, width=1.6))
        if p.get("bindu"):
            parts.append(bindu(cx, cy, 6, INK, opacity=0.75))
    elif p["mode"] == "rings":
        color = p["color"]
        parts.append(square_outline(cx, cy, p["half"], color, STROKE))
        r_end = p["half"] * (0.68 if p.get("tight") else 0.85)
        parts.append(rings(cx, cy, p["half"] * 0.3, p["ring_count"], r_end, color, STROKE_THIN))
        parts.append(bindu(cx, cy, 5, color))
    return "\n".join(parts)


# ==========================================================================
# FAMILY 4 — Prakṛti (13), the pivot. One card; the poised plate.
# ==========================================================================

def render_prakriti():
    cx, cy = CENTER
    parts = [
        circle_fill(cx, cy, 138, "#dfe6ea", 0.28),   # cool tint — sattva
        circle_fill(cx, cy, 108, "#f2e6d3", 0.28),   # warm tint — rajas
        circle_fill(cx, cy, 78, "#e7e2da", 0.28),    # neutral tint — tamas
    ]
    parts.append(rings(cx, cy, 40, 5, 140, MUTED, STROKE_THIN))
    parts.append(bindu(cx, cy, 7, INK))
    return "\n".join(parts)


# ==========================================================================
# FAMILY 5 — The Inner Instrument (14–16): one circle+triangle+bindu form,
#   differentiated only by how much space the bindu claims.
# ==========================================================================

INNER_INSTRUMENT_PARAMS = {
    "tattva-14": dict(bindu_r=5, color=COOL_GREY_BLUE, hatch=False),
    "tattva-15": dict(bindu_r=9, color=ROSE_BROWN, hatch=False),
    "tattva-16": dict(bindu_r=13, color=DUSTY_ROSE, hatch=True),
}


def render_inner_instrument(item_id):
    p = INNER_INSTRUMENT_PARAMS[item_id]
    cx, cy = CENTER
    color = p["color"]
    parts = [
        circle_outline(cx, cy, 118, INK, STROKE),
        triangle(cx, cy, 88, INK, STROKE, direction="up"),
    ]
    bx, by = cx, cy - 88
    parts.append(bindu(bx, by, p["bindu_r"], color))
    if p["hatch"]:
        for i in range(8):
            angle = i * 45
            x1, y1 = pt(bx, by, angle, p["bindu_r"] + 3)
            x2, y2 = pt(bx, by, angle, p["bindu_r"] + 11)
            parts.append(line_el(x1, y1, x2, y2, color, STROKE_THIN, 0.7))
    return "\n".join(parts)


# ==========================================================================
# FAMILY 6 — The Ten Sense Powers (17–26): two parallel families of five,
#   perception (circle+lotus) and action (square), same element sequence.
# ==========================================================================

SENSE_PERCEPTION_PARAMS = {
    "tattva-17": dict(rays=8, color=ELEMENT_COLOR["akasha"]),
    "tattva-18": dict(rays=11, color=ELEMENT_COLOR["vayu"]),
    "tattva-19": dict(rays=14, color=ELEMENT_COLOR["tejas"], arrow=True),
    "tattva-20": dict(rays=17, color=ELEMENT_COLOR["jala"], hook=True),
    "tattva-21": dict(rays=20, color=ELEMENT_COLOR["prithvi"]),
}


def render_sense_perception(item_id):
    p = SENSE_PERCEPTION_PARAMS[item_id]
    cx, cy = CENTER
    color = p["color"]
    r_circle = 100
    parts = [
        circle_outline(cx, cy, r_circle, color, STROKE),
        lotus(cx, cy, 68, 5, color, STROKE_THIN, 0.65),
        bindu(cx, cy, 6, color),
        rays(cx, cy, r_circle, r_circle + 32, p["rays"], color, STROKE_THIN,
             arrow=p.get("arrow", False), hook=p.get("hook", False)),
    ]
    return "\n".join(parts)


SENSE_ACTION_PARAMS = {
    "tattva-22": dict(rays=8, color=ELEMENT_COLOR["akasha"]),
    "tattva-23": dict(rays=11, color=ELEMENT_COLOR["vayu"]),
    "tattva-24": dict(rays=14, color=ELEMENT_COLOR["tejas"], lean=True),
    "tattva-25": dict(rays=17, color=ELEMENT_COLOR["jala"], fade=True),
    "tattva-26": dict(rays=20, color=ELEMENT_COLOR["prithvi"]),
}


def render_sense_action(item_id):
    p = SENSE_ACTION_PARAMS[item_id]
    cx, cy = CENTER
    color = p["color"]
    half = 78
    parts = [
        square_outline(cx, cy, half, color, STROKE),
        bindu(cx, cy, 6, color),
        rays(cx, cy, half * 1.05, half * 1.05 + 38, p["rays"], color, STROKE_THIN, fade=p.get("fade", False)),
    ]
    if p.get("lean"):
        parts.append(ray_cluster(cx, cy, 135, 50, 5, half * 1.05, half * 1.7, color, STROKE_THIN, 0.9))
    return "\n".join(parts)


# ==========================================================================
# FAMILY 7 — The Five Tanmātras (27–31): rising ring-count, rising density —
#   the accumulation doctrine rehearsed at the subtle-element scale.
# ==========================================================================

TANMATRA_PARAMS = {
    "tattva-27": dict(element="akasha", ring_count=3),
    "tattva-28": dict(element="vayu", ring_count=4),
    "tattva-29": dict(element="tejas", ring_count=5),
    "tattva-30": dict(element="jala", ring_count=6),
    "tattva-31": dict(element="prithvi", ring_count=7),
}


def render_tanmatra(item_id):
    p = TANMATRA_PARAMS[item_id]
    cx, cy = CENTER
    color = ELEMENT_COLOR[p["element"]]
    r_max = 132.0
    k = p["ring_count"]
    step = r_max / (k + 1)
    radii = [step * (i + 1) for i in range(1, k + 1)]  # smallest..largest
    parts = []
    n_r = len(radii)
    for i, r in enumerate(sorted(radii, reverse=True)):  # outer (faint) -> inner (dense)
        t = i / (n_r - 1) if n_r > 1 else 1.0
        op = 0.20 + (0.72 - 0.20) * t
        parts.append(circle_outline(cx, cy, r, color, STROKE_THIN, op))
    if k >= 7:
        parts.append(circle_fill(cx, cy, step * 0.9, color, 0.85))
    parts.append(bindu(cx, cy, 3, color))
    return "\n".join(parts)


# ==========================================================================
# FAMILY 8 — The Five Gross Elements (32–36): THE accumulation set.
#   Classical pañca-bhūta symbols nested cumulatively — space keeps almost
#   nothing; each element after it keeps every prior symbol (faded) and adds
#   its own (prominent); earth alone carries all five.
# ==========================================================================

def render_gross_element(item_id):
    cx, cy = CENTER
    parts = []

    # Inherited shapes (a prior element's symbol, carried forward into a
    # later one) get a floor opacity and a uniformly thinner stroke instead
    # of fading toward invisibility — hierarchy comes from weight + colour
    # dominance, not from being nearly unrenderable at 120px. Each element's
    # OWN shape stays full colour, full weight, so the row still reads as a
    # progression rather than five identical faint stacks.
    INHERIT_OP = 0.55
    INHERIT_W = STROKE_THIN

    def field(op=0.15):
        return circle_outline(cx, cy, 150, FAINT, STROKE_THIN, op)

    def air_hexagram(own=True, r=108):
        # Canonical bhuta-shuddhi symbol for vayu: a hexagram (two interlocking
        # equilateral triangles). triangle_pts() places an up-triangle's three
        # vertices at angles 0/120/240 and a down-triangle's at 60/180/300 (both
        # at radius r), so the six outer points land exactly on six_dot()'s
        # i*60 positions — the point-dots keep working unchanged. Outline only
        # (no fill), and the inherited copy uses the thinnest stroke in the
        # system + a floor opacity, per the accumulation convention, so the
        # busier six-line shape doesn't overwhelm tejas/jala/prithvi's own
        # marks when it's carried forward into their plates.
        op = 1.0 if own else INHERIT_OP
        w = STROKE if own else INHERIT_W
        dot_r = 3.2 if own else 2.2
        up = triangle(cx, cy, r, ELEMENT_COLOR["vayu"], w, direction="up", opacity=op)
        down = triangle(cx, cy, r, ELEMENT_COLOR["vayu"], w, direction="down", opacity=op)
        dots = six_dot(cx, cy, r, ELEMENT_COLOR["vayu"], dot_r, op)
        return up + "\n" + down + "\n" + dots

    def fire_triangle(own=True, size=88):
        op = 1.0 if own else INHERIT_OP
        w = STROKE if own else INHERIT_W
        return triangle(cx, cy, size, ELEMENT_COLOR["tejas"], w, direction="up", opacity=op)

    def water_crescent(own=True, r=68):
        op = 0.8 if own else max(INHERIT_OP - 0.1, 0.45)
        return crescent(cx, cy, r, ELEMENT_COLOR["jala"], fill_opacity=op, stroke_width=STROKE_THIN)

    def earth_square(op=1.0, half=54):
        return square_outline(cx, cy, half, ELEMENT_COLOR["prithvi"], STROKE_HEAVY, opacity=op,
                               fill=ELEMENT_COLOR["prithvi"] if op > 0.8 else "none")

    if item_id == "tattva-32":  # Akasha — the canonical bhuta-shuddhi symbol:
        # a plain black disc, flat and unornamented — doctrinally the
        # HEAVIEST mark in the set, not the emptiest. (An earlier version of
        # this plate read space as a near-empty field to express "least
        # contracted"; the builder's source documents the disc instead, so
        # that is what ships. See the build report for the tension between
        # the two readings.) Unornamented per brief: no rays, no rings
        # inside it — just the disc, centred, on the shared frame.
        # Her call (Aug 10): "Black disc" — INK, not the slate element tone.
        # The canonical symbol is black; the muted blue read as a soft
        # compromise between the two readings, and she chose the canon.
        parts.append(circle_fill(cx, cy, 92, INK, 1.0))

    elif item_id == "tattva-33":  # Vayu — space's field + air's own hexagram
        parts.append(field(0.18))
        parts.append(air_hexagram(True, 108))
        parts.append(bindu(cx, cy, 5, ELEMENT_COLOR["vayu"], opacity=0.85))

    elif item_id == "tattva-34":  # Tejas — + air carried forward (visible, thin), fire's own triangle
        parts.append(field(0.16))
        parts.append(air_hexagram(False, 108))
        parts.append(fire_triangle(True, 92))
        apex = (cx, cy - 92)
        parts.append(bindu(apex[0], apex[1], 7, ELEMENT_COLOR["tejas"], opacity=1.0, outline=True))

    elif item_id == "tattva-35":  # Jala — + air & fire carried forward, water's own crescent
        parts.append(field(0.14))
        parts.append(air_hexagram(False, 108))
        parts.append(fire_triangle(False, 92))
        parts.append(water_crescent(True, 66))
        parts.append(bindu(cx, cy, 6, ELEMENT_COLOR["jala"]))

    elif item_id == "tattva-36":  # Prithvi — holds all five shapes at once
        parts.append(field(0.14))
        parts.append(air_hexagram(False, 108))
        parts.append(fire_triangle(False, 92))
        parts.append(water_crescent(False, 66))
        parts.append(earth_square(1.0, 46))
        parts.append(bindu(cx, cy, 7, GOLD))

    return "\n".join(parts)


# ==========================================================================
# FAMILY 9 — The Five Realms: one shared container (square/circle/lotus/
#   bindu), differentiated by colour/interior treatment.
# ==========================================================================

REALM_PARAMS = {
    "realm-pure": dict(mode="plain", color="#c9ad74", opacity=0.55),
    "realm-coverings": dict(mode="petals_colored"),
    "realm-psyche": dict(mode="plain", color="#6b5d4f", opacity=0.85),
    "realm-senses": dict(mode="alt_marks", color=INK),
    "realm-elements": dict(mode="bands"),
}
KANCUKA_5 = [ELEMENT_COLOR["prithvi"], ELEMENT_COLOR["vayu"], ELEMENT_COLOR["jala"],
             ELEMENT_COLOR["akasha"], ELEMENT_COLOR["tejas"]]
BHUTA_ORDER = [ELEMENT_COLOR["akasha"], ELEMENT_COLOR["vayu"], ELEMENT_COLOR["tejas"],
               ELEMENT_COLOR["jala"], ELEMENT_COLOR["prithvi"]]


def render_realm(item_id):
    p = REALM_PARAMS[item_id]
    cx, cy = CENTER
    parts = [square_outline(cx, cy, 140, INK, STROKE)]

    if p["mode"] == "plain":
        color, op = p["color"], p["opacity"]
        parts.append(circle_outline(cx, cy, 115, color, STROKE, op))
        parts.append(lotus(cx, cy, 85, 6, color, STROKE_THIN, 0.85))
        parts.append(bindu(cx, cy, 7, INK))

    elif p["mode"] == "petals_colored":
        parts.append(circle_outline(cx, cy, 115, INK, STROKE))
        parts.append(colored_lotus(cx, cy, 85, 6, KANCUKA_5, STROKE_THIN, 0.85, 0.5))
        parts.append(bindu(cx, cy, 7, INK))

    elif p["mode"] == "alt_marks":
        parts.append(circle_outline(cx, cy, 115, INK, STROKE))
        parts.append(lotus(cx, cy, 85, 6, INK, STROKE_THIN, 0.85))
        for i in range(10):
            angle = i * 36
            r = 130 if i % 2 == 0 else 100
            parts.append(ticks(cx, cy, angle, r, 14, GOLD, 1.4, 0.85))
        parts.append(bindu(cx, cy, 7, INK))

    elif p["mode"] == "bands":
        n_bands = len(BHUTA_ORDER)
        for i, color in enumerate(BHUTA_ORDER):  # outer (akasha) -> inner (prithvi)
            r = 115 - i * (115 - 30) / (n_bands - 1)
            parts.append(circle_fill(cx, cy, r, color, 0.30))
        parts.append(circle_outline(cx, cy, 115, INK, STROKE))
        parts.append(lotus(cx, cy, 85, 6, INK, STROKE_THIN, 0.85))
        parts.append(bindu(cx, cy, 7, INK))

    return "\n".join(parts)


# ==========================================================================
# FAMILY 10 — Concepts (10 cards): the most bespoke family. Each yantra text
#   is essentially unique, so this family branches per-card, still sharing
#   the one palette / stroke system / frame as every other plate.
# ==========================================================================

def render_concept(item_id):
    cx, cy = CENTER
    parts = []

    if item_id == "concept-trinity":
        parts.append(triangle(cx, cy, 110, INK, STROKE, direction="up"))
        parts.append(triangle(cx, cy, 110, INK, STROKE, direction="down"))
        parts.append(bindu(cx, cy, 8, outline=True))

    elif item_id == "concept-spanda":
        radii = [20 + i * 16 for i in range(8)]
        for i, r in enumerate(radii):
            w = STROKE if i % 2 == 0 else STROKE_THIN
            color = GOLD if i % 2 == 0 else MUTED
            parts.append(circle_outline(cx, cy, r, color, w, 0.85))
        # deliberately no bindu — spanda is the pulse between points, not a point

    elif item_id == "concept-pratyabhijna":
        parts.append(circle_outline(cx - 4, cy, 120, INK, STROKE))
        parts.append(circle_outline(cx + 4, cy, 110, GOLD, STROKE))
        parts.append(bindu(cx, cy, 6, GOLD))
        parts.append(rays(cx, cy, 8, 34, 8, GOLD, STROKE_THIN))

    elif item_id == "concept-svatantrya":
        parts.append(circle_outline(cx, cy, 140, GOLD, STROKE))
        parts.append(rays(cx, cy, 10, 150, 24, GOLD, STROKE_THIN))
        parts.append(bindu(cx, cy, 10, outline=True))

    elif item_id == "concept-three-malas":
        tri = triangle_pts(cx, cy, 110, "up")
        pts_str = " ".join(f"{n(x)},{n(y)}" for x, y in tri)
        parts.append(f'<polygon points="{pts_str}" fill="none" stroke="{MUTED}" stroke-width="{STROKE_THIN}" opacity="0.4"/>')
        colors = ["#8a8580", "#7a5a72", "#8a5a3a"]  # anava, mayiya, karma
        for (x, y), c in zip(tri, colors):
            parts.append(bindu(x, y, 6, c, opacity=0.85))

    elif item_id == "concept-three-upayas":
        # outer: effortful cross-hatch ring
        parts.append(circle_outline(cx, cy, 140, INK, STROKE))
        for i in range(16):
            angle = i * 22.5
            x1, y1 = pt(cx, cy, angle, 133)
            x2, y2 = pt(cx, cy, angle, 147)
            parts.append(line_el(x1, y1, x2, y2, INK, STROKE_THIN, 0.8))
        # middle: one light curved brushstroke (a wobbled circle)
        wpts = []
        for i in range(65):
            angle = i * (360 / 64)
            r = 95 + 4 * math.sin(math.radians(angle * 3))
            x, y = pt(cx, cy, angle, r)
            wpts.append(f"{n(x)},{n(y)}")
        parts.append(f'<polyline points="{" ".join(wpts)}" fill="none" stroke="{GOLD}" stroke-width="{STROKE}" opacity="0.75"/>')
        # inner: barely visible ring
        parts.append(circle_outline(cx, cy, 50, MUTED, 0.6, 0.35))
        parts.append(bindu(cx, cy, 7, outline=True))

    elif item_id == "concept-anupaya":
        # No-means: still a single quiet circle, but held at a considered
        # proportion with the deck's own construction ticks (the frame's
        # vocabulary, echoed inward) so the emptiness reads as placed, not
        # missing. An outline bindu — the deck's mark elsewhere for
        # "presence without technique" (concept-trinity, tattva-05) — keeps
        # the centre from reading as a blank gap.
        parts.append(circle_outline(cx, cy, 100, MUTED, STROKE_THIN, 0.6))
        for angle in (0, 90, 180, 270):
            parts.append(ticks(cx, cy, angle, 100, 14, FAINT, 1.0, 0.7))
        parts.append(bindu(cx, cy, 5, outline=True))

    elif item_id == "concept-shadadhvan":
        top, bottom = (cx, 50.0), (cx, 350.0)
        parts.append(line_el(cx, 60, cx, 340, MUTED, STROKE_THIN, 0.8))
        rung_ys = [80, 130, 180, 230, 280, 330]
        for i, y in enumerate(rung_ys):
            heavy = i < 3
            color = INK if heavy else GOLD
            w = STROKE if heavy else STROKE_THIN
            parts.append(line_el(cx - 32, y, cx + 32, y, color, w, 1.0 if heavy else 0.8))
        parts.append(bindu(top[0], top[1], 6, INK))
        parts.append(bindu(bottom[0], bottom[1], 6, INK))

    elif item_id == "concept-samkhya-comparison":
        # Why thirty-six, not twenty-five: the shared count first (three
        # close ink lines — Sāṅkhya's twenty-five), a marked seam, then the
        # eleven tattvas unique to this system continuing alone in gold.
        # Endpoint bindus close the line the way concept-shadadhvan's do,
        # so a bare divided line reads as a considered count, not a stub.
        top_y, bottom_y = 60.0, 340.0
        band_y = top_y + (bottom_y - top_y) * 2 / 3
        for dx in (-3, 0, 3):
            parts.append(line_el(cx + dx, top_y, cx + dx, band_y, INK, STROKE_THIN, 0.85))
        parts.append(line_el(cx, band_y, cx, bottom_y, GOLD, STROKE_THIN, 0.85))
        parts.append(line_el(cx - 18, band_y, cx + 18, band_y, MUTED, 1.0, 0.7))
        parts.append(line_el(cx - 18, band_y - 6, cx - 18, band_y + 6, MUTED, 1.0, 0.6))
        parts.append(line_el(cx + 18, band_y - 6, cx + 18, band_y + 6, MUTED, 1.0, 0.6))
        parts.append(bindu(cx, top_y, 5, INK, opacity=0.85))
        parts.append(bindu(cx, bottom_y, 5, GOLD, opacity=0.85))

    elif item_id == "concept-tanmatra-accumulation":
        bands = [
            (140, ELEMENT_COLOR["akasha"], 0.10),
            (112, ELEMENT_COLOR["vayu"], 0.26),
            (84, ELEMENT_COLOR["tejas"], 0.44),
            (56, ELEMENT_COLOR["jala"], 0.64),
            (30, ELEMENT_COLOR["prithvi"], 0.95),
        ]
        for r, color, op in bands:
            parts.append(circle_fill(cx, cy, r, color, op))
        parts.append(bindu(cx, cy, 5, GROUND, outline=True))

    return "\n".join(parts)


# ==========================================================================
# Item table: (id, name, family, render_fn)
# ==========================================================================

def _sh(i):  # bound helper: render_shakti(item) partial
    return lambda: render_shakti(i)


def _pt_(i):
    return lambda: render_pure_tattva(i)


def _kc(i):
    return lambda: render_kancuka(i)


def _ii(i):
    return lambda: render_inner_instrument(i)


def _sp(i):
    return lambda: render_sense_perception(i)


def _sa(i):
    return lambda: render_sense_action(i)


def _tm(i):
    return lambda: render_tanmatra(i)


def _ge(i):
    return lambda: render_gross_element(i)


def _rm(i):
    return lambda: render_realm(i)


def _cn(i):
    return lambda: render_concept(i)


GROUPS = [
    ("The Five Śaktis", [
        ("shakti-cit", "Cit Shakti — The Power of Awareness", _sh),
        ("shakti-ananda", "Ānanda Shakti — The Power of Bliss", _sh),
        ("shakti-iccha", "Icchā Shakti — The Power of Will", _sh),
        ("shakti-jnana", "Jñāna Shakti — The Power of Knowing", _sh),
        ("shakti-kriya", "Kriyā Shakti — The Power of Action", _sh),
    ]),
    ("The Five Pure Tattvas", [
        ("tattva-01", "Shiva Tattva — Pure Awareness", _pt_),
        ("tattva-02", "Shakti Tattva — The Bliss of Existence", _pt_),
        ("tattva-03", "Sadāshiva Tattva — The Arising of Will", _pt_),
        ("tattva-04", "Īshvara Tattva — The Clarity of Knowing", _pt_),
        ("tattva-05", "Shuddha Vidyā — Pure Knowledge in Action", _pt_),
    ]),
    ("The Seven Kañcukas (Coverings)", [
        ("tattva-06", "Māyā — The Great Forgetting", _kc),
        ("tattva-07", "Kalā — Limited Agency", _kc),
        ("tattva-08", "Vidyā — Limited Knowledge", _kc),
        ("tattva-09", "Rāga — Attachment", _kc),
        ("tattva-10", "Kāla — Time", _kc),
        ("tattva-11", "Niyati — Causality", _kc),
        ("tattva-12", "Purusha — The Limited Self", _kc),
    ]),
    ("Prakṛti — The Pivot", [
        ("tattva-13", "Prakriti — Primordial Nature", None),
    ]),
    ("The Inner Instrument", [
        ("tattva-14", "Buddhi — Discernment", _ii),
        ("tattva-15", "Ahamkāra — The I-Maker", _ii),
        ("tattva-16", "Manas — Conceptual Mind", _ii),
    ]),
    ("The Five Perception Senses (Jñānendriyas)", [
        ("tattva-17", "Shrotra — Hearing", _sp),
        ("tattva-18", "Tvak — Touch", _sp),
        ("tattva-19", "Chakshu — Sight", _sp),
        ("tattva-20", "Rasanā — Taste", _sp),
        ("tattva-21", "Ghrāna — Smell", _sp),
    ]),
    ("The Five Action Senses (Karmendriyas)", [
        ("tattva-22", "Vāk — Speech", _sa),
        ("tattva-23", "Pāni — Grasping", _sa),
        ("tattva-24", "Pāda — Locomotion", _sa),
        ("tattva-25", "Pāyu — Elimination", _sa),
        ("tattva-26", "Upastha — Procreation", _sa),
    ]),
    ("The Five Tanmātras (Subtle Elements)", [
        ("tattva-27", "Shabda Tanmātra — Subtle Sound", _tm),
        ("tattva-28", "Sparsha Tanmātra — Subtle Touch", _tm),
        ("tattva-29", "Rūpa Tanmātra — Subtle Form", _tm),
        ("tattva-30", "Rasa Tanmātra — Subtle Flavor", _tm),
        ("tattva-31", "Gandha Tanmātra — Subtle Scent", _tm),
    ]),
    ("The Five Gross Elements (Mahābhūtas)", [
        ("tattva-32", "Ākāsha — Space", _ge),
        ("tattva-33", "Vāyu — Air", _ge),
        ("tattva-34", "Tejas — Fire", _ge),
        ("tattva-35", "Jala — Water", _ge),
        ("tattva-36", "Prithvī — Earth", _ge),
    ]),
    ("The Five Realms", [
        ("realm-pure", "Shuddhādhvan — The Pure Universe", _rm),
        ("realm-coverings", "The Kañcukas — Garments of Forgetting", _rm),
        ("realm-psyche", "Antaḥkaraṇa — The Inner Instrument", _rm),
        ("realm-senses", "The Ten Sense Powers", _rm),
        ("realm-elements", "Pañca Mahābhūta — The Great Elements", _rm),
    ]),
    ("Concepts", [
        ("concept-trinity", "Shiva-Shakti-Nara — The Sacred Trinity", _cn),
        ("concept-spanda", "Spanda — The Divine Pulsation", _cn),
        ("concept-pratyabhijna", "Pratyabhijñā — Recognition", _cn),
        ("concept-svatantrya", "Svātantrya — Absolute Freedom", _cn),
        ("concept-three-malas", "The Three Malas — Impurities of Forgetting", _cn),
        ("concept-three-upayas", "The Three Upāyas — Means of Practice", _cn),
        ("concept-anupaya", "Anupāya — No-Means, Beyond Technique", _cn),
        ("concept-shadadhvan", "Ṣaḍadhvan — The Six Paths", _cn),
        ("concept-samkhya-comparison", "Why Thirty-Six, Not Twenty-Five", _cn),
        ("concept-tanmatra-accumulation", "The Qualities That Accumulate — Why Earth Holds All Five", _cn),
    ]),
]


def render_body(item_id, wrapper):
    if wrapper is None:
        return render_prakriti()
    return wrapper(item_id)()


# ==========================================================================
# Main
# ==========================================================================

def main():
    os.makedirs(PLATES_DIR, exist_ok=True)
    written = []
    for group_name, items in GROUPS:
        for item_id, name, wrapper in items:
            body = render_body(item_id, wrapper)
            doc = svg_doc(item_id, name, body)
            out_path = os.path.join(PLATES_DIR, f"{item_id}.svg")
            with open(out_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(doc)
            written.append((item_id, name, group_name))

    build_contact_sheet(written)

    print(f"Wrote {len(written)} plates to {PLATES_DIR}")
    for group_name, items in GROUPS:
        print(f"  {group_name}: {len(items)}")
    print(f"Contact sheet: {CONTACT_SHEET_PATH}")


def build_contact_sheet(written):
    sections = []
    for group_name, items in GROUPS:
        cards = []
        for item_id, name, _wrapper in items:
            cards.append(
                f'<figure class="plate">\n'
                f'  <img src="{item_id}.svg" alt="{escape(name)}" width="120" height="120" loading="lazy">\n'
                f'  <figcaption>{escape(name)}<span class="id">{item_id}</span></figcaption>\n'
                f'</figure>'
            )
        sections.append(
            f'<section>\n<h2>{escape(group_name)} <span class="count">({len(items)})</span></h2>\n'
            f'<div class="grid">\n{"".join(cards)}\n</div>\n</section>'
        )

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>36 Tattvas — Plate Contact Sheet</title>
<style>
  :root {{
    --ground: {GROUND};
    --ink: {INK};
    --gold: {GOLD};
    --muted: {MUTED};
    --faint: {FAINT};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    background: var(--ground);
    color: var(--ink);
    font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
    margin: 0;
    padding: 32px 24px 80px;
  }}
  h1 {{
    font-size: 1.6rem;
    letter-spacing: 0.02em;
    border-bottom: 1px solid var(--muted);
    padding-bottom: 12px;
    margin-bottom: 4px;
  }}
  .sub {{
    color: var(--gold);
    font-size: 0.9rem;
    margin-bottom: 36px;
  }}
  h2 {{
    font-size: 1.05rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--gold);
    border-bottom: 1px solid var(--faint);
    padding-bottom: 8px;
    margin-top: 44px;
  }}
  .count {{
    color: var(--muted);
    font-weight: normal;
    text-transform: none;
    letter-spacing: normal;
  }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 20px;
    margin-top: 16px;
  }}
  figure.plate {{
    margin: 0;
    text-align: center;
  }}
  figure.plate img {{
    width: 100%;
    max-width: 120px;
    height: auto;
    background: var(--ground);
    border: 1px solid var(--muted);
    border-radius: 2px;
  }}
  figcaption {{
    margin-top: 6px;
    font-size: 0.72rem;
    line-height: 1.25;
    color: var(--ink);
  }}
  figcaption .id {{
    display: block;
    color: var(--muted);
    font-family: ui-monospace, Consolas, monospace;
    font-size: 0.62rem;
    margin-top: 2px;
  }}
</style>
</head>
<body>
<h1>The 36 Tattvas — Plate Contact Sheet</h1>
<div class="sub">{len(written)} constructed-geometry plates &middot; one shared system: ground {GROUND}, ink {INK}, gold {GOLD}, stroke {STROKE}px on a 400&times;400 grid</div>
{"".join(sections)}
</body>
</html>
"""
    with open(CONTACT_SHEET_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


if __name__ == "__main__":
    main()
