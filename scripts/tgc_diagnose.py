#!/usr/bin/env python3
"""Diagnose why a TGC game won't add to cart. Read-only."""
import os, sys, json, requests
API = "https://www.thegamecrafter.com/api"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load_env():
    env = {}
    for p in (os.path.join(ROOT,"print",".env.tgc"), os.path.join(ROOT,"env-local.txt")):
        if os.path.exists(p):
            for line in open(p,encoding="utf-8"):
                line=line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k,v=line.split("=",1); env.setdefault(k.strip(),v.strip())
    return env
def call(method,path,**params):
    r=requests.request(method,API+path,data=params,timeout=120)
    try: body=r.json()
    except: sys.exit(f"non-JSON {r.status_code}: {r.text[:300]}")
    if "error" in body:
        return {"__error": body["error"]}
    return body["result"]
env=load_env()
GAME=sys.argv[1] if len(sys.argv)>1 else "1C2D3BF2-64E5-11F1-9D82-035066E3122E"
DECK=sys.argv[2] if len(sys.argv)>2 else "E25631D6-66AB-11F1-8CE8-03868797CA38"
sess=call("POST","/session",api_key_id=env["TGC_API_KEY_ID"],username=env["TGC_USERNAME"],password=env["TGC_PASSWORD"])
sid=sess["id"]
print("session ok")
print("\n=== GAME ===")
g=call("GET",f"/game/{GAME}",session_id=sid)
for k in ("name","is_public","sales","edition","has_proofed","price","sku","user_id"):
    if k in g: print(f"  {k}: {g[k]}")
print("\n=== GAME PARTS ===")
parts=call("GET",f"/game/{GAME}/parts",session_id=sid)
items=parts.get("items",parts) if isinstance(parts,dict) else parts
print(json.dumps(items,indent=2)[:2000] if items else "  (none / unexpected shape)")
print("\n=== DECK ===")
d=call("GET",f"/tarotdeck/{DECK}",session_id=sid)
for k in ("name","has_proofed_back","back_id","card_count","quantity"):
    if k in d: print(f"  {k}: {d[k]}")
print("  ALL DECK FIELDS:", list(d.keys()) if isinstance(d,dict) and "__error" not in d else d)
print("\n=== CARDS (unproofed only) ===")
page=1; total=0; unproofed=[]
while True:
    res=call("GET",f"/tarotdeck/{DECK}/cards",session_id=sid,_page_number=page,_items_per_page=100)
    if isinstance(res,dict) and "__error" in res: print("  cards error:",res); break
    its=res.get("items",[])
    for c in its:
        total+=1
        if str(c.get("has_proofed_front","1")) in ("0","","None","null"):
            unproofed.append((c.get("name"),c.get("id")))
    if len(its)<100: break
    page+=1
print(f"  total cards: {total}")
print(f"  unproofed fronts: {len(unproofed)}")
for n,i in unproofed[:20]: print(f"    - {n}  ({i})")
if total and its:
    print("  SAMPLE CARD FIELDS:", list(its[0].keys()))
