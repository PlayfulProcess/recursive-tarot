#!/usr/bin/env python3
"""Remove specific draft decks from the game, then re-list. User-approved removal
of v2/v3/v4 (unproofed drafts); keeps v5 + v6. Card face images remain in the TGC
file folder independently — only the deck assemblies are removed.
"""
import os, requests
API = "https://www.thegamecrafter.com/api"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REMOVE = {
    "6658A246-65E6-11F1-998E-662143BF08F6": "Full Sampler v2 (26)",
    "91168D4E-65E7-11F1-A286-1C698797CA38": "Full Sampler v3 (26)",
    "CAA2ECD8-65EC-11F1-A69B-627566E3122E": "Full Sampler v4 (26)",
}


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
    return body.get("result")


env = load_env()
GAME = "1C2D3BF2-64E5-11F1-9D82-035066E3122E"
sid = call("POST", "/session", api_key_id=env["TGC_API_KEY_ID"],
           username=env["TGC_USERNAME"], password=env["TGC_PASSWORD"])["id"]

for did, label in REMOVE.items():
    r = call("DELETE", f"/tarotdeck/{did}", session_id=sid)
    if isinstance(r, dict) and "__error" in r:
        print(f"  ERR removing {label}: {r['__error'].get('message')}")
    else:
        print(f"  removed {label}")

print("\n--- decks now on game ---")
res = call("GET", f"/game/{GAME}/tarotdecks", session_id=sid)
for d in res.get("items", []):
    proofed = "PROOFED" if str(d.get("has_proofed")) == "1" else "NOT proofed"
    print(f"  [{proofed}] {d.get('name')}  (cards={d.get('card_count')})")

g = call("GET", f"/game/{GAME}", session_id=sid)
print(f"\ngame is_proofed: {g.get('is_proofed')}  | box_required: {g.get('box_required')}  | cost: {g.get('cost')}")
print("game _game_warnings:", g.get("_game_warnings"))
