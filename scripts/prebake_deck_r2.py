#!/usr/bin/env python3
"""Pre-bake a whole deck's cards to 900x1500 print-ready files on Cloudflare R2,
using the SHARED tgc_card processing — so deck products (and the future
print-on-demand "build your own deck" flow) match the proofed sampler exactly, with
zero per-order image work (the Worker just references these URLs).

Also stamps each card's metadata.print = {quality, source_px, tgc_url} so the UI
knows which cards are print-ready vs low-res (and can show a warning before a user
prints a low-res one).

Usage: python scripts/prebake_deck_r2.py <slug>
R2 creds (gitignored, never echoed): CLOUDFLARE_ACCOUNT_ID from
../recursive-eco/apps/flow/.env.local; R2 keys + bucket from ../recursive-eco/.env.local.
"""
import io, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tgc_card

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = "https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev"
KEY_PREFIX = "grammar-illustrations/print/"

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

def main():
    import boto3
    slug = sys.argv[1]
    e = creds()
    s3 = boto3.client("s3",
        endpoint_url=f"https://{e['CLOUDFLARE_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=e["R2_ACCESS_KEY_ID"], aws_secret_access_key=e["R2_SECRET_ACCESS_KEY"],
        region_name="auto")
    bucket = e["R2_BUCKET_NAME"]
    gp = os.path.join(ROOT, "tarot", slug, "grammar.json")
    g = json.load(open(gp, encoding="utf-8"))
    stats = {"print": 0, "web": 0}
    for it in g["items"]:
        if it.get("composite_of") or it.get("category") in ("axis", "keyword-emergence"):
            continue
        url = it.get("image_url") or (it.get("metadata") or {}).get("image_url")
        if not url:
            continue
        try:
            src = tgc_card.fetch(url)
            q = tgc_card.print_quality(src)
            card = tgc_card.border_fit(src)
            buf = io.BytesIO(); card.save(buf, "JPEG", quality=92)
            key = f"{KEY_PREFIX}{slug}/{it['id']}.jpg"
            s3.put_object(Bucket=bucket, Key=key, Body=buf.getvalue(),
                          ContentType="image/jpeg", CacheControl="public, max-age=31536000")
            it.setdefault("metadata", {})["print"] = {
                "quality": q, "source_px": list(src.size), "tgc_url": f"{PUBLIC}/{key}"}
            stats[q] += 1
            print(f"  [{q:5}] {it['id']} ({src.size[0]}x{src.size[1]})")
            time.sleep(0.25)
        except Exception as ex:
            print(f"  FAIL {it['id']}: {str(ex)[:55]}")
    json.dump(g, open(gp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n{slug}: {stats['print']} print-ready, {stats['web']} low-res "
          f"-> R2 {KEY_PREFIX}{slug}/  (metadata.print stamped on every card)")

if __name__ == "__main__":
    main()
