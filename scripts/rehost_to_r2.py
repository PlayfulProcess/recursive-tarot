#!/usr/bin/env python3
"""Rehost a grammar's Commons-hosted images to Cloudflare R2 — so the viewer loads
fast and reliably instead of waiting on Commons' on-demand (and rate-limited)
thumbnailing. Idempotent: images already on R2 are skipped.

Usage:  python scripts/rehost_to_r2.py tarot/<slug>/grammar.json [--width 1000]

Creds: read from ../recursive-eco/.env.local (gitignored): CLOUDFLARE_ACCOUNT_ID,
R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, R2_PUBLIC_URL.
"""
import json, os, sys, time, re, urllib.request, urllib.parse, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_env():
    env = {}
    p = os.path.join(ROOT, "..", "recursive-eco", ".env.local")
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def fetch(url, tries=4):
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "recursive-tarot-rehost/1.0 (PlayfulProcess)"})
            return urllib.request.urlopen(req, timeout=90).read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and a < tries - 1:
                wait = 20 * (a + 1); print(f"   429 — backoff {wait}s"); time.sleep(wait); continue
            raise
    raise RuntimeError("unreachable")

def main():
    gpath = sys.argv[1]
    width = 1000
    if "--width" in sys.argv:
        width = int(sys.argv[sys.argv.index("--width") + 1])
    env = load_env()
    import boto3
    s3 = boto3.client("s3",
        endpoint_url=f"https://{env['CLOUDFLARE_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=env["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=env["R2_SECRET_ACCESS_KEY"], region_name="auto")
    bucket = env["R2_BUCKET_NAME"]
    pub = env["R2_PUBLIC_URL"].rstrip("/")

    full = os.path.join(ROOT, gpath)
    g = json.load(open(full, encoding="utf-8"))
    slug = g.get("slug") or os.path.basename(os.path.dirname(full))
    changed = 0
    for it in g["items"]:
        url = it.get("image_url")
        if not url or pub in url:
            continue  # no image, or already on R2
        # normalise Commons width to the rehost width
        src = re.sub(r"width=\d+", f"width={width}", url)
        key = f"grammar-illustrations/{slug}-{it['id']}.jpg"
        try:
            data = fetch(src)
            s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType="image/jpeg",
                          CacheControl="public, max-age=31536000")
            it["image_url"] = f"{pub}/{key}"
            changed += 1
            print(f"   ✓ {it['id']} ({len(data)//1024} KB) -> {key}")
            time.sleep(3)  # Commons politeness
        except Exception as e:
            print(f"   ✗ {it['id']}: {str(e)[:60]}")
    json.dump(g, open(full, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"rehosted {changed} images -> R2; grammar updated: {gpath}")

if __name__ == "__main__":
    main()
