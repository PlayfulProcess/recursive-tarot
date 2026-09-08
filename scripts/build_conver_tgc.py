#!/usr/bin/env python3
"""Build + upload the PRIVATE proof of the Tarot de Marseille (Conver 1760 pattern)
to The Game Crafter — 78 faces + 1 colophon card + an original back + a tarot tuck box.

Faces come straight from `metadata.print.tgc_url` (the border_fit 900x1500 R2 masters,
same pipeline as the proofed sampler — see docs/TGC-STORE-AUDIT.md "Composition spec"),
already downloaded to print/decks/tarot-de-marseille-conver-tgc/ (gitignored) with a
manifest.json. This script GENERATES the three original pieces and uploads everything:

  print/conver-proof/back-conver-lattice-900x1500.png   original 180-deg-symmetric back
  print/conver-proof/colophon-900x1500.png              79th card: sources, licence, QR
  print/conver-proof/tuckbox90-outside-3000x2475.png    TarotTuckBox90 outside wrap

Rights: see print-products.json -> decks.tarot-de-marseille-conver.rights. The deck is
pd-encumbered (54 Gallica faces) so this is a private proof only — nothing published.
NO credits/watermarks on any card face: everything lives on the colophon card + box.

Usage:
    python scripts/build_conver_tgc.py            # build assets only
    python scripts/build_conver_tgc.py --upload   # build + upload to the TGC game below
Credentials: repo-root env-local.txt (gitignored) — TGC_API_KEY_ID / TGC_USERNAME / TGC_PASSWORD.
"""
import argparse, json, math, os, sys, time
from PIL import Image, ImageDraw, ImageFont, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACES_DIR = os.path.join(ROOT, "print", "decks", "tarot-de-marseille-conver-tgc")
OUT_DIR = os.path.join(ROOT, "print", "conver-proof")

# TGC objects created 2026-09-08 (private draft, public=0). Recorded in print-products.json.
GAME_ID = "942AE570-ABC9-11F1-97E7-C337379D9816"
DECK_ID = "95DD96EC-ABC9-11F1-97E7-4638379D9816"
TUCKBOX_ID = "968BCDF2-ABC9-11F1-95E6-FD104066D96C"

CLAIM_URL = "https://tarot.recursive.eco/claim/"
VIEWER_URL = "tarot.recursive.eco/viewers/cards.html?src=../tarot/tarot-de-marseille-conver/grammar.json"

# ---- palette: theme.css tokens (same as make_symmetric_back.py) ----
INK = (34, 31, 26)
GOLD = (154, 115, 34)
GOLD_SOFT = (120, 90, 40)
PAPER = (244, 241, 234)
MUTED = (107, 100, 87)

# ---- TGC specs ----
TW, TH = 900, 1500            # card incl. 1/8" bleed; trim 825x1425; safe 750x1350
HALF = TH // 2
BOX_W, BOX_H = 3000, 2475     # TarotTuckBox90 outside (from /api/tgc/products)
# Fold lines measured from TGC's own overlay (/overlays/tarottuckbox90.png):
#   vertical x = 74 | 479 | 1312 | 1717 | 2551 | 2926 ; horizontal y = 41 | 191 | 595 | 715 | 2029 | 2434
# Safe zones (blue dashed on the overlay), as (x0, y0, x1, y1):
SAFE = {
    "side_a": (120, 654, 437, 1978),      # x 74-479   left side panel
    "p1":     (527, 654, 1268, 1978),     # x 479-1312 big panel under the lid flap
    "side_b": (1351, 654, 1676, 1978),    # x 1312-1717 side panel
    "p2":     (1765, 654, 2505, 1978),    # x 1717-2551 big panel with the thumb notch (notch top-centre, y 595-~680)
    "lid":    (527, 234, 1268, 549),      # x 479-1312, y 191-595
    "bottom": (527, 2071, 1268, 2394),    # x 479-1312, y 2029-2434
}
# glue flap x 2551-2926 and the dust flaps carry no art (plain paper colour).


def font(name, size):
    cands = {
        "serif": ["georgia.ttf", "DejaVuSerif.ttf"],
        "serif_b": ["georgiab.ttf", "DejaVuSerif-Bold.ttf"],
        "serif_i": ["georgiai.ttf", "DejaVuSerif-Italic.ttf"],
    }[name]
    for c in cands:
        for d in (r"C:\Windows\Fonts", "/usr/share/fonts/truetype/dejavu", "/Library/Fonts"):
            p = os.path.join(d, c)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, maxw):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=fnt) <= maxw:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, maxw, fill=INK, align="left", lh=1.32, cx=None):
    """Draw wrapped text; returns the y after the block."""
    step = round(fnt.size * lh)
    for ln in wrap(draw, text, fnt, maxw):
        if align == "center":
            w = draw.textlength(ln, font=fnt)
            draw.text(((cx if cx is not None else x + maxw / 2) - w / 2, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def draw_spiral(draw, cx, cy, R, width=6, fill=GOLD, turns=2.6):
    """The site's golden-ratio logarithmic spiral mark (r = a*e^(b*theta)), fitted in radius R."""
    r0 = R * 0.035
    t1 = turns * 2 * math.pi
    b = math.log(R / r0) / t1
    pts = []
    for i in range(0, 601):
        t = t1 * i / 600
        r = r0 * math.exp(b * t)
        pts.append((cx + r * math.cos(t - math.pi / 2), cy + r * math.sin(t - math.pi / 2)))
    for i in range(len(pts) - 1):
        w = max(2, round(width * (0.35 + 0.65 * i / len(pts))))
        draw.line([pts[i], pts[i + 1]], fill=fill, width=w)
    draw.ellipse([cx - width, cy - width, cx + width, cy + width], fill=fill)


# ------------------------------------------------------------------ back
def build_back():
    """Original back: gold lozenge lattice on ink with a central roundel. Drawn only in the
    top half, bottom half = top half rotated 180 -> exactly point-symmetric by construction."""
    top = Image.new("RGB", (TW, HALF), INK)
    d = ImageDraw.Draw(top)
    mx = 84                        # frame margin (safe zone starts at 75)
    cx, cy = TW / 2, HALF          # cy = mirror axis
    # outer double frame, three sides (mirror completes it)
    for m, w, col in ((mx, 7, GOLD), (mx + 16, 3, GOLD_SOFT)):
        d.line([(m, m), (TW - m, m)], fill=col, width=w)
        d.line([(m, m), (m, cy)], fill=col, width=w)
        d.line([(TW - m, m), (TW - m, cy)], fill=col, width=w)
    # lozenge lattice inside the inner frame, clipped by drawing on a mask
    ix0, iy0, ix1 = mx + 34, mx + 34, TW - mx - 34
    lat = Image.new("RGB", (TW, HALF), INK)
    ld = ImageDraw.Draw(lat)
    step = 58
    for k in range(-40, 60):
        off = k * step
        ld.line([(off, 0), (off + HALF * 2, HALF * 2)], fill=GOLD_SOFT, width=3)
        ld.line([(off, HALF * 2), (off + HALF * 2, 0)], fill=GOLD_SOFT, width=3)
    # dots at lattice nodes
    for gy in range(0, HALF + step, step):
        for gx in range(0, TW + step, step):
            ld.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=GOLD)
    clip = Image.new("L", (TW, HALF), 0)
    ImageDraw.Draw(clip).rectangle([ix0, iy0, ix1, HALF], fill=255)
    # keep the roundel area clear
    R = 150
    ImageDraw.Draw(clip).ellipse([cx - R - 26, cy - R - 26, cx + R + 26, cy + R + 26], fill=0)
    top = Image.composite(lat, top, clip)
    d = ImageDraw.Draw(top)
    # central roundel: ring + diamond + four dots (all symmetric about the centre)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=GOLD, width=6)
    d.ellipse([cx - R + 18, cy - R + 18, cx + R - 18, cy + R - 18], outline=GOLD_SOFT, width=3)
    dm = 74
    d.polygon([(cx, cy - dm), (cx + dm, cy), (cx, cy + dm), (cx - dm, cy)], outline=GOLD, width=5)
    d.polygon([(cx, cy - dm * 0.45), (cx + dm * 0.45, cy), (cx, cy + dm * 0.45), (cx - dm * 0.45, cy)], fill=GOLD)
    for px, py in ((cx, cy - R + 46), (cx - R + 46, cy), (cx + R - 46, cy)):
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=PAPER)
    full = Image.new("RGB", (TW, TH), INK)
    full.paste(top, (0, 0))
    full.paste(top.rotate(180), (0, HALF))
    diff = ImageChops.difference(full, full.rotate(180))
    assert diff.getbbox() is None, "back is not exactly 180-symmetric"
    return full


# ------------------------------------------------------------------ colophon
COLOPHON_TITLE = "Tarot de Marseille"
COLOPHON_SUB = "Conver 1760 pattern · 78 cards"
COLOPHON_BODY = (
    "Public domain work. This edition reproduces two public-domain sources of the same "
    "Marseille pattern:\n"
    "Trumps, Ace of Swords, Ace of Batons — Nicolas Conver, Marseille, 1760. Photographs "
    "by Tarot World Project (Wikimedia Commons), CC BY-SA 4.0, from a 2020 reprint.\n"
    "Pips and courts — Édition Lequart, Paris, c. 1890 (Collection Paul Marteau). Scan: "
    "Bibliothèque nationale de France, Gallica, ark:/12148/btv1b10539498w.\n"
    "Card composition, back and this edition: PlayfulProcess · recursive.eco, 2026. "
    "Deck data CC BY-SA 4.0."
)


def build_colophon():
    im = Image.new("RGB", (TW, TH), PAPER)
    d = ImageDraw.Draw(im)
    m = 90
    d.rectangle([m, m, TW - m, TH - m], outline=GOLD, width=4)
    d.rectangle([m + 12, m + 12, TW - m - 12, TH - m - 12], outline=GOLD_SOFT, width=2)
    x0, maxw = m + 44, TW - 2 * (m + 44)
    y = m + 52
    y = text_block(d, x0, y, "COLOPHON", font("serif", 26), maxw, fill=GOLD, align="center", cx=TW / 2)
    y += 8
    y = text_block(d, x0, y, COLOPHON_TITLE, font("serif_b", 50), maxw, align="center", cx=TW / 2)
    y = text_block(d, x0, y, COLOPHON_SUB, font("serif_i", 28), maxw, fill=MUTED, align="center", cx=TW / 2)
    y += 10
    d.line([(TW / 2 - 90, y), (TW / 2 + 90, y)], fill=GOLD, width=3)
    y += 26
    y = text_block(d, x0, y, COLOPHON_BODY, font("serif", 24), maxw, lh=1.34)
    y += 14
    y = text_block(d, x0, y, "Read every card, with its history, online:", font("serif_i", 23), maxw, fill=MUTED)
    # no spaces in a URL -> break it by hand so it can never overflow the frame
    y = text_block(d, x0, y, VIEWER_URL.replace("?src=", "?src=\n    "), font("serif", 21), maxw, fill=INK, lh=1.25)
    # QR -> claim page
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
    qr.add_data(CLAIM_URL); qr.make(fit=True)
    qim = qr.make_image(fill_color=INK, back_color=PAPER).convert("RGB")
    qs = 300
    qim = qim.resize((qs, qs), Image.NEAREST)
    qy = TH - m - 44 - qs
    im.paste(qim, (x0, qy))
    d = ImageDraw.Draw(im)
    tx = x0 + qs + 30
    ty = qy + 26
    ty = text_block(d, tx, ty, "Bought this deck?", font("serif_b", 30), TW - m - 44 - tx)
    ty = text_block(d, tx, ty, "Scan to claim $10 in recursive.eco credits — one claim per order.",
                    font("serif", 23), TW - m - 44 - tx, fill=MUTED, lh=1.3)
    ty += 6
    text_block(d, tx, ty, CLAIM_URL.replace("https://", ""), font("serif", 22), TW - m - 44 - tx, fill=INK)
    return im


# ------------------------------------------------------------------ tuck box
BOX_SOURCE = (
    "Public domain work. Trumps and two Aces: Nicolas Conver, Marseille, 1760 — photographs "
    "Tarot World Project, Wikimedia Commons, CC BY-SA 4.0. Pips and courts: Édition Lequart, "
    "Paris, c. 1890 — Bibliothèque nationale de France, Gallica ark:/12148/btv1b10539498w. "
    "Full credits on the colophon card inside."
)


def build_box():
    im = Image.new("RGB", (BOX_W, BOX_H), PAPER)
    d = ImageDraw.Draw(im)

    def frame(box, inset=0):
        x0, y0, x1, y1 = box
        d.rectangle([x0 + inset, y0 + inset, x1 - inset, y1 - inset], outline=GOLD, width=4)
        d.rectangle([x0 + inset + 12, y0 + inset + 12, x1 - inset - 12, y1 - inset - 12], outline=GOLD_SOFT, width=2)

    # ---- P1 (under the lid flap): title panel
    x0, y0, x1, y1 = SAFE["p1"]; frame(SAFE["p1"]); cx = (x0 + x1) / 2; w = x1 - x0 - 80
    y = y0 + 120
    y = text_block(d, x0 + 40, y, "TAROT", font("serif_b", 118), w, align="center", cx=cx, lh=1.0)
    y = text_block(d, x0 + 40, y + 6, "DE MARSEILLE", font("serif_b", 74), w, align="center", cx=cx, lh=1.0)
    y += 30
    d.line([(cx - 120, y), (cx + 120, y)], fill=GOLD, width=4); y += 40
    y = text_block(d, x0 + 40, y, "Conver, 1760", font("serif_i", 60), w, align="center", cx=cx)
    draw_spiral(d, cx, y + 300, 190, width=9)
    y = y + 300 + 190 + 90
    y = text_block(d, x0 + 40, y, "78 cards · tarot size", font("serif", 40), w, fill=MUTED, align="center", cx=cx)
    text_block(d, x0 + 40, y1 - 120, "recursive.eco", font("serif", 44), w, fill=GOLD, align="center", cx=cx)

    # ---- P2 (thumb-notch panel): sources
    x0, y0, x1, y1 = SAFE["p2"]; frame(SAFE["p2"]); cx = (x0 + x1) / 2; w = x1 - x0 - 90
    y = 800   # clear of the thumb notch (y 595-~680)
    y = text_block(d, x0 + 45, y, "Tarot de Marseille", font("serif_b", 62), w, align="center", cx=cx, lh=1.0)
    y = text_block(d, x0 + 45, y + 8, "Conver 1760 pattern", font("serif_i", 40), w, fill=MUTED, align="center", cx=cx)
    y += 30
    d.line([(cx - 90, y), (cx + 90, y)], fill=GOLD, width=3); y += 50
    y = text_block(d, x0 + 45, y, BOX_SOURCE, font("serif", 31), w, lh=1.36)
    y += 40
    y = text_block(d, x0 + 45, y, "Every card, with its history, free online:", font("serif_i", 30), w, fill=MUTED)
    y = text_block(d, x0 + 45, y, "tarot.recursive.eco", font("serif_b", 40), w)
    y += 30
    text_block(d, x0 + 45, y, "Deck data CC BY-SA 4.0 · PlayfulProcess · recursive.eco, 2026", font("serif", 28), w, fill=MUTED)
    draw_spiral(d, cx, y1 - 170, 110, width=7)

    # ---- sides: vertical title
    for key in ("side_a", "side_b"):
        x0, y0, x1, y1 = SAFE[key]
        strip = Image.new("RGB", (y1 - y0, x1 - x0), PAPER)
        sd = ImageDraw.Draw(strip)
        sw, sh = strip.size
        f = font("serif_b", 54)
        t = "TAROT DE MARSEILLE · CONVER 1760"
        tw = sd.textlength(t, font=f)
        assert tw < sw - 80, "side title too long for the strip"
        sd.text(((sw - tw) / 2, (sh - f.size) / 2 - 10), t, font=f, fill=INK)
        sd.line([(60, sh / 2 + 52), (sw - 60, sh / 2 + 52)], fill=GOLD, width=4)
        rot = strip.rotate(90 if key == "side_a" else -90, expand=True)
        im.paste(rot, (x0, y0))
    d = ImageDraw.Draw(im)

    # ---- lid: mark + wordmark
    x0, y0, x1, y1 = SAFE["lid"]; cx = (x0 + x1) / 2
    draw_spiral(d, cx, (y0 + y1) / 2 - 20, 105, width=7)
    text_block(d, x0, y1 - 62, "recursive.eco", font("serif", 36), x1 - x0, fill=GOLD, align="center", cx=cx)

    # ---- bottom panel
    x0, y0, x1, y1 = SAFE["bottom"]; cx = (x0 + x1) / 2
    text_block(d, x0 + 20, y0 + 90, "Tarot de Marseille · Conver 1760 pattern", font("serif_i", 36), x1 - x0 - 40, align="center", cx=cx)
    text_block(d, x0 + 20, y0 + 160, "Public domain work · credits on the colophon card", font("serif", 30), x1 - x0 - 40, fill=MUTED, align="center", cx=cx)
    return im


# ------------------------------------------------------------------ upload
def upload_all(paths):
    from tgc_upload_deck import load_env, call
    env = load_env()
    sess = call("POST", "/session", params={"api_key_id": env["TGC_API_KEY_ID"],
                                             "username": env["TGC_USERNAME"], "password": env["TGC_PASSWORD"]})
    sid, uid = sess["id"], sess["user_id"]
    folder = call("GET", f"/user/{uid}", params={"session_id": sid})["root_folder_id"]

    def up(path):
        with open(path, "rb") as fh:
            return call("POST", "/file", params={"session_id": sid, "folder_id": folder,
                                                  "name": os.path.basename(path)},
                        files={"file": (os.path.basename(path), fh, "image/png" if path.endswith(".png") else "image/jpeg")})["id"]

    game = call("GET", f"/game/{GAME_ID}", params={"session_id": sid})
    assert int(game.get("public") or 0) == 0, "game is public — refusing"
    print("game", game["name"], "public=", game.get("public"))

    print("back…")
    bid = up(paths["back"])
    call("PUT", f"/deck/{DECK_ID}", params={"session_id": sid, "back_id": bid, "has_proofed_back": 0})

    existing = {}
    page = 1
    while True:
        res = call("GET", f"/deck/{DECK_ID}/cards", params={"session_id": sid, "_page_number": page, "_items_per_page": 100})
        for c in res.get("items", []):
            existing[c["name"]] = c["id"]
        if len(res.get("items", [])) < 100:
            break
        page += 1
    print(f"{len(existing)} cards already in deck")

    man = json.load(open(os.path.join(FACES_DIR, "manifest.json"), encoding="utf-8"))["cards"]
    faces = [(c["name"], os.path.join(FACES_DIR, c["file"])) for c in man] + [("Colophon", paths["colophon"])]
    ok = 0
    for i, (name, path) in enumerate(faces, 1):
        if name in existing:
            ok += 1; continue
        fid = up(path)
        call("POST", "/card", params={"session_id": sid, "deck_id": DECK_ID, "name": name, "face_id": fid, "quantity": 1})
        ok += 1
        print(f"  [{i}/{len(faces)}] {name}")
        time.sleep(0.25)
    print(f"cards: {ok}/{len(faces)}")

    print("box…")
    oid = up(paths["box"])
    call("PUT", f"/tuckbox/{TUCKBOX_ID}", params={"session_id": sid, "outside_id": oid, "has_proofed_outside": 0})

    deck = call("GET", f"/deck/{DECK_ID}", params={"session_id": sid})
    box = call("GET", f"/tuckbox/{TUCKBOX_ID}", params={"session_id": sid})
    game = call("GET", f"/game/{GAME_ID}", params={"session_id": sid})
    print(json.dumps({"game_public": game.get("public"), "edit_uri": game.get("edit_uri"),
                      "card_count": deck.get("card_count"), "back_id": deck.get("back_id"),
                      "deck_preview": deck.get("preview_uri"), "box_outside_id": box.get("outside_id"),
                      "box_preview": box.get("preview_uri")}, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--upload", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)
    paths = {
        "back": os.path.join(OUT_DIR, "back-conver-lattice-900x1500.png"),
        "colophon": os.path.join(OUT_DIR, "colophon-900x1500.png"),
        "box": os.path.join(OUT_DIR, "tuckbox90-outside-3000x2475.png"),
    }
    build_back().save(paths["back"], "PNG")
    build_colophon().save(paths["colophon"], "PNG")
    build_box().save(paths["box"], "PNG", optimize=True)
    for k, p in paths.items():
        print(k, Image.open(p).size, f"{os.path.getsize(p)//1024} KB")
    if a.upload:
        upload_all(paths)


if __name__ == "__main__":
    main()
