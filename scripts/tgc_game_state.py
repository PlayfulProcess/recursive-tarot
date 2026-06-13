#!/usr/bin/env python3
"""Dump full game object + related parts to find the cart-add blocker. Read-only."""
import os, sys, json, requests
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

print("=== FULL GAME OBJECT ===")
g = call("GET", f"/game/{GAME}", session_id=sid)
print(json.dumps(g, indent=2))

# Try common related-collection endpoints to enumerate parts
print("\n=== probing part collections ===")
for rel in ("tarotdecks", "decks", "parts", "components", "designertickets"):
    r = call("GET", f"/game/{GAME}/{rel}", session_id=sid)
    if isinstance(r, dict) and "__error" in r:
        print(f"  /{rel}: {r['__error'].get('code')} {r['__error'].get('message')}")
    else:
        its = r.get("items", r) if isinstance(r, dict) else r
        print(f"  /{rel}: {len(its) if hasattr(its,'__len__') else '?'} items")
        if its:
            print("    ", json.dumps(its, indent=2)[:1500])
