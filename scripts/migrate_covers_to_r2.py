#!/usr/bin/env python3
"""Migrate ALL Commons-hotlinked images to R2:
  - grammar.json top-level cover_image_url
  - items[].image_url (e.g. mantegna's 64 cards, tree-of-tarot deck thumbnails)
  - _collection.json cover_image_url (synced to the deck's new cover)

Idempotent: skips anything already on R2. Writes grammar.json + _collection.json in place.
Usage: python scripts/migrate_covers_to_r2.py [slug ...]   # or all if no args
"""
import json, os, sys, time, re, urllib.request
import boto3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB  = "https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev"

# ---------------------------------------------------------------------------
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

def make_s3(e):
    return boto3.client("s3",
        endpoint_url=f"https://{e['CLOUDFLARE_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=e["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=e["R2_SECRET_ACCESS_KEY"],
        region_name="auto")

def fetch_url(url, tries=5):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "recursive-tarot-rehost/1.0 (PlayfulProcess)"})
            return urllib.request.urlopen(req, timeout=90).read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < tries - 1:
                wait = 25 * (attempt + 1)
                print(f"   429 — backoff {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("max retries")

def upload(s3, bucket, key, data):
    s3.put_object(Bucket=bucket, Key=key, Body=data,
                  ContentType="image/jpeg",
                  CacheControl="public, max-age=31536000")
    return f"{PUB}/{key}"

def is_r2(url):
    return url and (url.startswith(PUB) or "r2.dev" in url)

def rehost(s3, bucket, url, key):
    """Download from url, upload to R2 key, return new R2 url."""
    if is_r2(url):
        return url  # already done
    # add width hint for Commons thumbnailing
    src = re.sub(r"\?width=\d+", "", url)
    src = re.sub(r"Special:FilePath/", "Special:FilePath/", src)
    if "Special:FilePath" in src and "width=" not in src:
        src += "?width=1200"
    data = fetch_url(src)
    r2url = upload(s3, bucket, key, data)
    print(f"   uploaded {len(data)//1024}KB  -> {key}")
    time.sleep(3)
    return r2url

# ---------------------------------------------------------------------------
def migrate_deck(s3, bucket, slug, collection_map):
    gp = os.path.join(ROOT, "tarot", slug, "grammar.json")
    if not os.path.exists(gp):
        print(f"  skip (no grammar): {slug}")
        return

    g = json.load(open(gp, encoding="utf-8-sig"))
    changed = 0

    # 1. Grammar-level cover_image_url
    cov = g.get("cover_image_url", "")
    if cov and not is_r2(cov):
        key = f"grammar-illustrations/{slug}-cover.jpg"
        try:
            new_url = rehost(s3, bucket, cov, key)
            g["cover_image_url"] = new_url
            changed += 1
            # also update _collection.json
            if slug in collection_map:
                collection_map[slug]["cover_image_url"] = new_url
                print(f"   collection.json cover updated for {slug}")
        except Exception as e:
            print(f"   FAIL cover: {e}")

    # 2. Item-level image_url
    for it in g.get("items", []):
        url = it.get("image_url", "")
        if not url or is_r2(url):
            continue
        iid = it.get("id", "unknown")
        key = f"grammar-illustrations/{slug}-{iid}.jpg"
        try:
            it["image_url"] = rehost(s3, bucket, url, key)
            changed += 1
        except Exception as e:
            print(f"   FAIL item {iid}: {e}")

    if changed:
        json.dump(g, open(gp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  {slug}: {changed} images rehosted")
    else:
        print(f"  {slug}: nothing to rehost")

# ---------------------------------------------------------------------------
def main():
    e = creds()
    s3 = make_s3(e)
    bucket = e["R2_BUCKET_NAME"]

    # load collection for cover sync
    col_path = os.path.join(ROOT, "tarot", "_collection.json")
    col = json.load(open(col_path, encoding="utf-8"))
    col_map = {g["slug"]: g for g in col.get("grammars", [])}

    # which slugs to process
    if len(sys.argv) > 1:
        slugs = sys.argv[1:]
    else:
        # auto-detect: any grammar with a Commons hotlink
        import glob
        slugs = []
        for f in glob.glob(os.path.join(ROOT, "tarot", "*", "grammar.json")):
            slug = os.path.basename(os.path.dirname(f))
            if slug in ("all-decks-many-lenses", "test"):
                continue
            d = json.load(open(f, encoding="utf-8-sig"))
            has_item = any("Special:FilePath" in (i.get("image_url") or "")
                           for i in d.get("items", []))
            has_cover = "Special:FilePath" in (d.get("cover_image_url") or "")
            if has_item or has_cover:
                slugs.append(slug)

    print(f"Migrating {len(slugs)} decks: {slugs}\n")
    for slug in slugs:
        print(f"--- {slug} ---")
        migrate_deck(s3, bucket, slug, col_map)

    # write updated collection
    json.dump(col, open(col_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\nDone. _collection.json updated.")

if __name__ == "__main__":
    main()
