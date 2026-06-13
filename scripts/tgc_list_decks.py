#!/usr/bin/env python3
"""List every deck attached to the game with proof status. Read-only."""
import os, requests
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


env = load_env()
GAME = "1C2D3BF2-64E5-11F1-9D82-035066E3122E"
sid = call("POST", "/session", api_key_id=env["TGC_API_KEY_ID"],
           username=env["TGC_USERNAME"], password=env["TGC_PASSWORD"])["id"]

res = call("GET", f"/game/{GAME}/tarotdecks", session_id=sid)
decks = res.get("items", [])
print(f"{len(decks)} decks attached to game:\n")
for d in decks:
    proofed = "PROOFED" if str(d.get("has_proofed")) == "1" else "NOT proofed"
    print(f"  [{proofed}] {d.get('name')}")
    print(f"      id={d.get('id')}  cards={d.get('card_count')}")
    if str(d.get("has_proofed")) != "1":
        print(f"      reason: {d.get('not_proofed_reason')}")
    print()
