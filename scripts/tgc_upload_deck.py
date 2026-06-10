#!/usr/bin/env python3
"""Upload a full deck to The Game Crafter via their public API.

Replaces the flaky browser drag-upload entirely: creates a session, uploads every
card face + the back to your TGC file folder, and attaches them to a Tarot Deck —
server-to-server, no browser. This is also session-1 validation for the planned
Cloudflare-Worker integration ("user builds a deck -> API creates the product").

Credentials (NEVER in chat, NEVER committed): put them in print/.env.tgc
    TGC_API_KEY_ID=...        (thegamecrafter.com -> Account -> API Keys -> public key id)
    TGC_USERNAME=...          (your TGC username)
    TGC_PASSWORD=...          (your TGC password — you type it into this file yourself)
The file is gitignored. The API key page also shows a private key; not needed for
session auth.

Usage:
    python scripts/tgc_upload_deck.py --game C07782A2-... --deck 1DF2F35A-... \
        --cards print/decks/golden-dawn-book-t-tarot-tgc \
        --back print/decks/golden-dawn-BACK-900x1500.jpg

If --deck is omitted, a new Tarot Deck is created in the game.
Nothing is published or purchased — this only fills the draft deck.
"""
import argparse, glob, json, os, sys, time
import requests

API = "https://www.thegamecrafter.com/api"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env():
    env = {}
    for p in (os.path.join(ROOT, "print", ".env.tgc"), os.path.join(ROOT, "env-local.txt")):
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env.setdefault(k.strip(), v.strip())
    for k in ("TGC_API_KEY_ID", "TGC_USERNAME", "TGC_PASSWORD"):
        env.setdefault(k, os.environ.get(k, ""))
    missing = [k for k in ("TGC_API_KEY_ID", "TGC_USERNAME", "TGC_PASSWORD") if not env.get(k)]
    if missing:
        sys.exit(f"Missing credentials: {missing}. Create print/.env.tgc (see header).")
    return env


def call(method, path, *, params=None, files=None, expect=200):
    r = requests.request(method, API + path, data=params, files=files, timeout=120)
    try:
        body = r.json()
    except Exception:
        sys.exit(f"{method} {path}: non-JSON response {r.status_code}: {r.text[:300]}")
    if "error" in body:
        sys.exit(f"{method} {path}: API error {body['error'].get('code')}: "
                 f"{body['error'].get('message')} ({body['error'].get('data')})")
    return body["result"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, help="TGC game id")
    ap.add_argument("--deck", default=None, help="existing TarotDeck id (else create)")
    ap.add_argument("--cards", required=True, help="folder of 900x1500 face images")
    ap.add_argument("--back", default=None, help="back image (900x1500)")
    ap.add_argument("--name", default="Tarot Deck", help="deck name if creating")
    a = ap.parse_args()

    env = load_env()
    print("1) session…")
    sess = call("POST", "/session", params={
        "api_key_id": env["TGC_API_KEY_ID"],
        "username": env["TGC_USERNAME"],
        "password": env["TGC_PASSWORD"],
    })
    sid = sess["id"]
    user_id = sess.get("user_id")
    print(f"   session ok (user {user_id})")

    # user root folder (uploads must live in a folder you own)
    user = call("GET", f"/user/{user_id}", params={"session_id": sid})
    folder_id = user.get("root_folder_id")
    if not folder_id:
        folders = call("GET", "/folder", params={"session_id": sid, "user_id": user_id})
        items = folders.get("items", folders if isinstance(folders, list) else [])
        folder_id = items[0]["id"] if items else sys.exit("no folder found on account")
    print(f"   root folder {folder_id}")

    deck_id = a.deck
    if not deck_id:
        print("2) creating Tarot Deck…")
        deck = call("POST", "/tarotdeck", params={
            "session_id": sid, "game_id": a.game, "name": a.name})
        deck_id = deck["id"]
        print(f"   deck {deck_id}")
    else:
        print(f"2) using existing deck {deck_id}")

    def upload(path):
        with open(path, "rb") as fh:
            f = call("POST", "/file", params={
                "session_id": sid, "folder_id": folder_id,
                "name": os.path.basename(path)},
                files={"file": (os.path.basename(path), fh, "image/jpeg")})
        return f["id"]

    if a.back:
        print("3) back image…")
        back_file = upload(a.back)
        call("PUT", f"/tarotdeck/{deck_id}", params={
            "session_id": sid, "back_id": back_file, "has_proofed_back": 0})
        print(f"   back set ({back_file})")

    faces = sorted(glob.glob(os.path.join(a.cards, "*.jpg")) +
                   glob.glob(os.path.join(a.cards, "*.png")))
    # idempotency: skip cards that already exist in the deck (by name)
    existing = set()
    try:
        page = 1
        while True:
            res = call("GET", f"/tarotdeck/{deck_id}/cards",
                       params={"session_id": sid, "_page_number": page, "_items_per_page": 100})
            items = res.get("items", [])
            existing |= {c.get("name") for c in items}
            if len(items) < 100:
                break
            page += 1
    except SystemExit:
        pass
    if existing:
        print(f"   ({len(existing)} cards already in deck — skipping those)")
    print(f"4) uploading {len(faces)} cards…")
    ok = len([f for f in faces if os.path.splitext(os.path.basename(f))[0] in existing])
    for i, f in enumerate(faces, 1):
        name = os.path.splitext(os.path.basename(f))[0]
        if name in existing:
            continue
        try:
            fid = upload(f)
            call("POST", "/card", params={
                "session_id": sid, "deck_id": deck_id, "name": name,
                "face_id": fid, "quantity": 1})
            ok += 1
            print(f"   [{i}/{len(faces)}] {name}")
        except SystemExit as e:
            print(f"   [{i}/{len(faces)}] FAILED {name}: {e}")
        time.sleep(0.3)   # be polite to their API
    print(f"\ndone: {ok}/{len(faces)} cards attached to deck {deck_id}")
    print("Open the deck page on TGC to verify, then proof + order ONE copy yourself.")


if __name__ == "__main__":
    main()
