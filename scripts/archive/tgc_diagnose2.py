#!/usr/bin/env python3
import os, sys, json, requests
API="https://www.thegamecrafter.com/api"
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load_env():
    env={}
    for p in (os.path.join(ROOT,"print",".env.tgc"),os.path.join(ROOT,"env-local.txt")):
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
    if "error" in body: return {"__error":body["error"]}
    return body["result"]
env=load_env()
GAME="1C2D3BF2-64E5-11F1-9D82-035066E3122E"
DECK="E25631D6-66AB-11F1-8CE8-03868797CA38"
sid=call("POST","/session",api_key_id=env["TGC_API_KEY_ID"],username=env["TGC_USERNAME"],password=env["TGC_PASSWORD"])["id"]
d=call("GET",f"/tarotdeck/{DECK}",session_id=sid)
print("DECK has_proofed:",repr(d.get("has_proofed")),"| has_proofed_back:",repr(d.get("has_proofed_back")),"| card_count:",d.get("card_count"),"| back_id:",repr(d.get("back_id")))
print("\nPer-card proof state:")
page=1; total=0; bad=[]
while True:
    res=call("GET",f"/tarotdeck/{DECK}/cards",session_id=sid,_page_number=page,_items_per_page=100)
    its=res.get("items",[])
    for c in its:
        total+=1
        face=str(c.get("has_proofed_face"))
        back=str(c.get("has_proofed_back"))
        faceid=c.get("face_id")
        if face!="1" or back!="1" or not faceid:
            bad.append((c.get("name"),"face="+face,"back="+back,"face_id="+("Y" if faceid else "MISSING"),c.get("id")))
    if len(its)<100: break
    page+=1
print(f"  total: {total}  problematic: {len(bad)}")
for row in bad[:40]: print("   ",row)
