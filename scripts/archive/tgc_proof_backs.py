#!/usr/bin/env python3
"""Flip has_proofed_back=1 on every card in the deck.

All cards share the deck-level back image, which is already proofed
(tarotdeck.has_proofed_back == 1). TGC's add-to-cart additionally requires
each card's own has_proofed_back flag, which the face-proofing wizard skips.
This propagates the already-approved deck back to every card. Read the
diagnosis from scripts/tgc_diagnose2.py before running.
"""
import os, sys, requests

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
    return env


def call(method, path, **params):
    r = requests.request(method, API + path, data=params, timeout=120)
    body = r.json()
    if "error" in body:
        return {"__error": body["error"]}
    return body["result"]


def main():
    env = load_env()
    deck = sys.argv[1] if len(sys.argv) > 1 else "E25631D6-66AB-11F1-8CE8-03868797CA38"
    sid = call("POST", "/session",
               api_key_id=env["TGC_API_KEY_ID"],
               username=env["TGC_USERNAME"],
               password=env["TGC_PASSWORD"])["id"]

    ids, page = [], 1
    while True:
        res = call("GET", f"/tarotdeck/{deck}/cards", session_id=sid,
                   _page_number=page, _items_per_page=100)
        its = res.get("items", [])
        ids += [c["id"] for c in its if str(c.get("has_proofed_back")) != "1"]
        if len(its) < 100:
            break
        page += 1

    print(f"flipping {len(ids)} card backs to proofed…")
    done = 0
    for cid in ids:
        r = call("PUT", f"/card/{cid}", session_id=sid, has_proofed_back=1)
        if isinstance(r, dict) and "__error" in r:
            print("  ERR", cid, r["__error"].get("message"))
            continue
        done += 1
    print(f"done: {done}/{len(ids)}")

    page, bad = 1, 0
    while True:
        res = call("GET", f"/tarotdeck/{deck}/cards", session_id=sid,
                   _page_number=page, _items_per_page=100)
        its = res.get("items", [])
        bad += sum(1 for c in its
                   if str(c.get("has_proofed_back")) != "1"
                   or str(c.get("has_proofed_face")) != "1")
        if len(its) < 100:
            break
        page += 1
    print(f"remaining unproofed (face or back): {bad}")


if __name__ == "__main__":
    main()
