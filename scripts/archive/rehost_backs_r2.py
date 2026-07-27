#!/usr/bin/env python3
"""Rehost the card-back images to Cloudflare R2 so the sampler build stops failing
on Commons' rate-limit. Fetches each back through the images.weserv.nl proxy (its
own IP, so it dodges the Commons 429 on this machine), uploads to R2, and rewrites
print/card-backs.json to the stable R2 URLs. Idempotent (skips backs already on R2).

R2 creds are split across two gitignored files (do not echo values):
  CLOUDFLARE_ACCOUNT_ID  <- ../recursive-eco/apps/flow/.env.local
  R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY / R2_BUCKET_NAME  <- ../recursive-eco/.env.local
"""
import json, os, io, urllib.request, urllib.parse, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = "https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev"  # the bucket's public dev URL
KEY_PREFIX = "grammar-illustrations/card-backs/"

def read_env(rel):
    env, p = {}, os.path.join(ROOT, "..", rel)
    if not os.path.exists(p):
        return env
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            v = v.split(" #")[0].strip().strip('"').strip("'")
            if v and not v.startswith("#"):
                env[k.strip()] = v
    return env

def creds():
    e = {}
    e.update(read_env("recursive-eco/.env.local"))
    flow = read_env("recursive-eco/apps/flow/.env.local")
    if flow.get("CLOUDFLARE_ACCOUNT_ID"):
        e["CLOUDFLARE_ACCOUNT_ID"] = flow["CLOUDFLARE_ACCOUNT_ID"]
    return e

def fetch_via_weserv(commons_url):
    # strip protocol, route through weserv (its IP fetches Commons, dodging our 429)
    bare = commons_url.split("://", 1)[-1]
    u = "https://images.weserv.nl/?url=" + urllib.parse.quote(bare, safe="") + "&output=jpg"
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "recursive-tarot/1.0"}), timeout=90).read()

def main():
    import boto3
    e = creds()
    s3 = boto3.client("s3",
        endpoint_url=f"https://{e['CLOUDFLARE_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=e["R2_ACCESS_KEY_ID"], aws_secret_access_key=e["R2_SECRET_ACCESS_KEY"],
        region_name="auto")
    bucket = e["R2_BUCKET_NAME"]
    cp = os.path.join(ROOT, "print", "card-backs.json")
    data = json.load(open(cp, encoding="utf-8"))
    changed = 0
    for b in data.get("items", []):
        url = b.get("image_url")
        if not url or PUBLIC in url:
            continue  # no image, or already on R2
        key = KEY_PREFIX + b["id"] + ".jpg"
        try:
            img = fetch_via_weserv(url)
            if len(img) < 2000:
                print("  small/empty:", b["id"]); continue
            s3.put_object(Bucket=bucket, Key=key, Body=img, ContentType="image/jpeg",
                          CacheControl="public, max-age=31536000")
            b["image_url"] = f"{PUBLIC}/{key}"
            changed += 1
            print(f"  [ok] {b['id']} ({len(img)//1024} KB) -> R2")
            time.sleep(2)
        except Exception as ex:
            print(f"  [x] {b['id']}: {str(ex)[:60]}")
    json.dump(data, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"rehosted {changed} backs to R2; card-backs.json updated")

if __name__ == "__main__":
    main()
