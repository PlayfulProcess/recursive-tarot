#!/usr/bin/env python3
"""Inspect one card + the deck back relationship. Read-only."""
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
DECK = "E25631D6-66AB-11F1-8CE8-03868797CA38"
sid = call("POST", "/session", api_key_id=env["TGC_API_KEY_ID"],
           username=env["TGC_USERNAME"], password=env["TGC_PASSWORD"])["id"]

res = call("GET", f"/tarotdeck/{DECK}/cards", session_id=sid, _page_number=1, _items_per_page=1)
card = res["items"][0]
print("=== FIRST CARD (full) ===")
print(json.dumps(card, indent=2))

cid = card["id"]
print("\n=== GET /card/{id} (full) ===")
full = call("GET", f"/card/{cid}", session_id=sid)
print(json.dumps(full, indent=2))

print("\n=== DECK back_id check ===")
d = call("GET", f"/tarotdeck/{DECK}", session_id=sid)
print("deck back_id:", d.get("back_id"), "| has_proofed_back:", d.get("has_proofed_back"))
