#!/usr/bin/env python3
"""Read-only: list a TGC game's decks with their card count, back and proofing state, and the game's
cost. Changes nothing on TGC.

    python scripts/tgc_list_decks.py --game C07782A2-645A-11F1-87B8-CDFD42BF08F6
    python scripts/tgc_list_decks.py --all        # every game on the account, with its decks
Credentials as in tgc_upload_deck.py (print/.env.tgc, then root env-local.txt, then the environment).
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tgc_upload_deck import load_env, call  # noqa: E402

SITE = "https://www.thegamecrafter.com"


def pages(path, sid, **params):
    page, out = 1, []
    while True:
        res = call("GET", path, params=dict(params, session_id=sid, _page_number=page, _items_per_page=100))
        items = res.get("items", [])
        out += items
        if len(items) < 100:
            return out
        page += 1


def show_game(sid, gid):
    g = call("GET", f"/game/{gid}", params={"session_id": sid})
    print(f"GAME {g['name']}  id={gid}")
    print(f"  public={g.get('public')} box_required={g.get('box_required')} is_proofed={g.get('is_proofed')} "
          f"cost=${g.get('cost')} msrp=${g.get('msrp')}")
    print(f"  edit: {SITE}{g.get('edit_uri')}")
    for w in (g.get("_game_warnings") or []) + (g.get("calculation_warnings") or []):
        print(f"  warning: {w}")
    decks = pages(f"/game/{gid}/decks", sid)
    print(f"  {len(decks)} deck(s)")
    for d in decks:
        cards = pages(f"/deck/{d['id']}/cards", sid)
        faces = sum(1 for c in cards if c.get("face_id"))
        unproofed = sum(1 for c in cards if not int(c.get("has_proofed_face") or 0))
        print(f"  - {d.get('object_name')} '{d['name']}' id={d['id']}")
        print(f"      cards={d.get('card_count')} (faces uploaded {faces}/{len(cards)}) back={'yes' if d.get('back_id') else 'NO'}")
        print(f"      has_proofed={d.get('has_proofed')} has_proofed_back={d.get('has_proofed_back')} "
              f"faces awaiting proof={unproofed} not_proofed_reason={d.get('not_proofed_reason') or '-'}")
    return g, decks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    env = load_env()
    s = call("POST", "/session", params={"api_key_id": env["TGC_API_KEY_ID"],
                                          "username": env["TGC_USERNAME"], "password": env["TGC_PASSWORD"]})
    sid = s["id"]
    if a.all:
        for g in pages(f"/user/{s['user_id']}/games", sid):
            show_game(sid, g["id"])
    elif a.game:
        show_game(sid, a.game)
    else:
        ap.error("--game ID or --all")


if __name__ == "__main__":
    main()
