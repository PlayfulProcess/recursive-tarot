# -*- coding: utf-8 -*-
"""Backfill image provenance on the five decks that ship images without it.

  python3 scripts/backfill_image_provenance.py [--check] [--verify-urls]

58 of 63 tarot decks carry a `_grammar_commons` licence block. These five do
not — `belgian-tarot`, `este-tarot`, `madiao-money-cards`,
`paris-anonymous-tarot`, `vieville-tarot` — and between them they ship ~220
card images plus 5 covers with no per-image source of any kind. They are the
only five exceptions out of 63, which makes it an omission rather than a
different-but-valid pattern.

**Nothing here is invented.** Every per-card source below is recovered from
the deck's own one-shot generator in `scripts/archive/`, which still holds
the exact upstream identifier it downloaded from, and from
`scripts/prebake_deck_r2.py`, whose `high_res_url()` still holds the IIIF
mapping used to bake the print masters:

| Deck | Recovered mapping | From |
|---|---|---|
| `belgian-tarot` | `images/tNN.jpg` → `File:Tarot Belgijski - A<NN> - <name>.jpg` on Wikimedia Commons | `scripts/archive/build_belgian.py` `POL` |
| `este-tarot` | `images/cNN.jpg` → Yale IIIF image `33215685 + NN` | `scripts/prebake_deck_r2.py` `high_res_url()` |
| `madiao-money-cards` | `images/<inv>.jpg` → `File:… Skoklosters slott - <inv>.tif` on Commons | `scripts/archive/build_madiao.py` `CARDS` / `SHEET` |
| `paris-anonymous-tarot` | `images/cNN.jpg` → Gallica `ark:/12148/btv1b105109624` folio `2·NN−1` | `scripts/prebake_deck_r2.py` `high_res_url()` |
| `vieville-tarot` | `images/cNN.jpg` → Gallica `ark:/12148/btv1b10510963k` folio `2·NN−1` | `scripts/prebake_deck_r2.py` `high_res_url()` |

(The odd folios are the card faces; the even folios are the patterned backs.
That is why `cNN` maps to `f(2·NN−1)` and why `este-tarot` only uses odd
`cNN` filenames.)

What gets written:

  * `_grammar_commons` — the repo's own licence/attribution block, in the
    same shape the other 58 decks use (maker · holding institution · the
    archive the scans came from · this repo). This is the documented gap.
  * `cover_image_credit` — the structured block, in the shape the astrology
    repo made canonical (`title`/`creator`/`date`/`source`/`file_page`/
    `license`/`pd_basis`/`verified`), for the cover image that until now had
    no credit at all.
  * `_image_provenance` — one deck-level block naming the holding
    institution, the archive, the licence, the `pd_basis`, the verification
    date, and the *rule* that maps any committed display image to its
    upstream source, so all ~220 images are individually traceable without
    220 copies of the same paragraph.
  * `metadata.image_source` on every item that has an `image_url` — that
    item's own upstream file page or folio page. Exact, per card.

`image_credit` stays a **string**: `viewers/course-embeds.js` and
`pages/course-viewer.html` both read it as one (`(dg && dg.image_credit) ||
…`), and `GRAMMAR_FORMAT.md` says deck-level credit is stated once,
factually. Only `belgian-tarot`'s is rewritten, because "Reproductions in the
public domain (Vandenborre / Belgian type)" names no archive at all.

**Where the record is genuinely thin, it says so** rather than inventing a
provenance: `belgian-tarot` has no recorded holding institution for the
physical pack its scans were made from, and `este-tarot` has no recorded Yale
catalogue-record URL (only the open-access IIIF endpoints). Both carry an
explicit `unknown` field naming what is missing.

`--verify-urls` HEAD-checks every source URL this script writes and fails on
any non-200. Run it when the sources change; it is not run by `--check`,
which stays offline so the pre-commit gate needs no network.

Idempotent: re-running writes the same values and reports no change.
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VERIFIED = "2026-08-02"
UA = "recursive-tarot provenance backfill (PlayfulProcess)"

COMMONS_FILE = "https://commons.wikimedia.org/wiki/File:"

# --- recovered from scripts/archive/build_belgian.py -------------------------
BELGIAN_POL = {
    1: "Mag", 2: "Kapitan Eracasse", 3: "Cesarzowa", 4: "Cesarz", 5: "Bachus",
    6: "Kochankowie", 7: "Rydwan", 8: "Sprawiedliwość", 9: "Pustelnik",
    10: "Koło Fortuny", 11: "Siła", 12: "Wisielec", 13: "Śmierć",
    14: "Umiarkowanie", 15: "Diabeł", 16: "Gniew Boży", 17: "Gwiazda",
    18: "Księżyc", 19: "Słońce", 20: "Sąd Boży", 21: "Świat", 22: "Głupiec",
}
# --- recovered from scripts/archive/build_madiao.py --------------------------
MADIAO_FILES = {"102352": "Kinesiskt spelkort Ma Diao - Skoklosters slott - 102352.tif",
                "13617": "Kinesiska spelkort för kortspelet Mo Diao - Skoklosters slott - 13617.tif"}
for _inv in ["102351"] + [str(i) for i in range(102353, 102362)]:
    MADIAO_FILES[_inv] = f"Kinesiskt spelkort till Ma Diao - Skoklosters slott - {_inv}.tif"


def commons_file_page(filename):
    return COMMONS_FILE + urllib.parse.quote(filename.replace(" ", "_"))


def source_for(slug, image_url):
    """The upstream source page for one committed display image. Returns None
    for an image this mapping does not cover — never a guess."""
    fname = (image_url or "").rsplit("/", 1)[-1]
    if slug == "belgian-tarot":
        m = re.fullmatch(r"t(\d{2})\.jpg", fname)
        if m and int(m.group(1)) in BELGIAN_POL:
            n = int(m.group(1))
            return commons_file_page(f"Tarot Belgijski - A{n} - {BELGIAN_POL[n]}.jpg")
        return None
    if slug == "madiao-money-cards":
        m = re.fullmatch(r"(?:sheet-)?(\d+)\.jpg", fname)
        if m and m.group(1) in MADIAO_FILES:
            return commons_file_page(MADIAO_FILES[m.group(1)])
        return None
    m = re.fullmatch(r"c(\d{2})\.jpg", fname)
    if not m:
        return None
    n = int(m.group(1))
    if slug == "este-tarot":
        return f"https://collections.library.yale.edu/iiif/2/{33215685 + n}/info.json"
    if slug == "paris-anonymous-tarot":
        return f"https://gallica.bnf.fr/ark:/12148/btv1b105109624/f{2 * n - 1}.item"
    if slug == "vieville-tarot":
        return f"https://gallica.bnf.fr/ark:/12148/btv1b10510963k/f{2 * n - 1}.item"
    return None


PD_COMMONS = "Public domain (as stated on the Wikimedia Commons file page)"
PD_GALLICA = "Public domain (as stated by the BnF on Gallica)"
PD_YALE = "Open access (as stated by Yale University Library)"

DECKS = {
    "belgian-tarot": {
        "image_credit": ("Wikimedia Commons, 'Tarot Belgijski' set — the Vandenborre / "
                         "Rouen-Brussels pattern, c. 1780, public domain. No holding "
                         "institution is recorded for the pack these scans were made from."),
        "commons": [
            {"name": "F. I. Vandenborre (workshop), Brussels", "date": "c. 1780",
             "note": "Printer of the Vandenborre / 'Tarot Flamand' pattern; the pattern "
                     "itself is older than the firm and descends from Jacques Viéville "
                     "via Bodet (Liège, 1693) and de Hautot (Rouen)"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "Card images, the 'Tarot Belgijski' set — 22 atouts only; clean "
                     "public-domain scans of the Flemish minors have not been located"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture and summaries"},
        ],
        "provenance": {
            "holding_institution": None,
            "archive": "Wikimedia Commons — the 'Tarot Belgijski' set",
            "license": PD_COMMONS,
            "pd_basis": "The cards are a c. 1780 print, so the artwork is long out of "
                        "copyright; each Commons file page states public domain.",
            "unknown": "Which institution or private collection holds the physical "
                       "Vandenborre pack these scans were made from is not recorded "
                       "anywhere in this repo, and the Commons upload does not say. The "
                       "images are display resolution and the print masters are flagged "
                       "quality: web because there is no higher-resolution upstream. "
                       "Source under reconstruction — do not read the credit as naming a "
                       "holder.",
            "rule": "images/tNN.jpg is Commons 'File:Tarot Belgijski - A<NN> - <name>.jpg', "
                    "the <name> suffix recovered from scripts/archive/build_belgian.py.",
        },
        "cover": {
            "title": "Le Monde (XXI) — Vandenborre / 'Tarot Flamand' pattern",
            "creator": "F. I. Vandenborre (workshop), Brussels",
            "date": "c. 1780",
            "source": "Wikimedia Commons, the 'Tarot Belgijski' set",
            "license": PD_COMMONS,
            "pd_basis": "c. 1780 print, long out of copyright; the Commons file page "
                        "states public domain",
        },
    },
    "este-tarot": {
        "image_credit": None,
        "commons": [
            {"name": "Ferrarese workshop, in the orbit of the House of Este",
             "date": "c. 1450 (a 1470s date is also argued)",
             "note": "Painter of the 16 surviving hand-painted d'Este cards; no maker "
                     "is documented by name"},
            {"name": "Beinecke Rare Book & Manuscript Library, Yale",
             "date": "holding institution",
             "note": "Holds the fragment as Cary Collection of Playing Cards, "
                     "PLAYING CARDS GEN 966; completely digitised, open access"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture and summaries"},
        ],
        "provenance": {
            "holding_institution": "Beinecke Rare Book & Manuscript Library, Yale "
                                   "University — Cary Collection of Playing Cards, "
                                   "PLAYING CARDS GEN 966",
            "archive": "Yale University Library open-access IIIF",
            "license": PD_YALE,
            "pd_basis": "A 15th-century hand-painted object, long out of copyright; "
                        "Yale publishes the digitisation as open access (credit: Yale "
                        "University Library).",
            "unknown": "Yale's own human-readable catalogue-record URL for this object "
                       "is not recorded in this repo — only the IIIF image endpoints the "
                       "images were fetched from. The per-item source below is therefore "
                       "the IIIF image description, not a catalogue page.",
            "rule": "images/cNN.jpg is Yale IIIF image 33215685 + NN, the offset "
                    "recovered from scripts/prebake_deck_r2.py high_res_url().",
        },
        "cover": {
            "title": "A card from the d'Este (Estensi) Tarocchi fragment",
            "creator": "Ferrarese workshop (unnamed), in the orbit of the House of Este",
            "date": "c. 1450 (a 1470s date is also argued — see the deck dossier)",
            "source": "Beinecke Rare Book & Manuscript Library, Yale — Cary Collection "
                      "of Playing Cards, PLAYING CARDS GEN 966",
            "license": PD_YALE,
            "pd_basis": "15th-century object, long out of copyright; Yale publishes the "
                        "digitisation as open access",
        },
    },
    "madiao-money-cards": {
        "image_credit": None,
        "commons": [
            {"name": "Unknown Chinese cardmaker", "date": "money-suited cards, Ming era",
             "note": "Money-suited packs are described by Lu Rong (1436-1494); Ma Diao "
                     "itself is codified in the late Ming. The collection's own dating "
                     "is approximate — see the deck dossier"},
            {"name": "Skokloster Castle, Sweden", "date": "holding institution",
             "note": "Holds the twelve surviving items; high-resolution museum scans "
                     "released to Wikimedia Commons"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "Card images, the Skokloster Ma Diao / Mo Diao scans"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture and summaries"},
        ],
        "provenance": {
            "holding_institution": "Skokloster Castle, Sweden",
            "archive": "Wikimedia Commons (museum scans released by Skokloster)",
            "license": PD_COMMONS,
            "pd_basis": "An early-modern object, long out of copyright; each Commons "
                        "file page states public domain.",
            "unknown": "The individual cards are not catalogued by suit or value at "
                       "source, and the collection's dating is loosely sourced — this "
                       "block records where each image came from, not what each card is.",
            "rule": "images/<inv>.jpg (and sheet-13617.jpg) is the Commons file of the "
                    "same Skokloster inventory number, the exact filenames recovered "
                    "from scripts/archive/build_madiao.py.",
        },
        "cover": {
            "title": "Chinese money-suited playing card, Skokloster inventory 102351",
            "creator": "Unknown Chinese cardmaker",
            "date": "Ming era (the collection's 'c. 1600' label is approximate)",
            "source": "Skokloster Castle, Sweden, via Wikimedia Commons",
            "license": PD_COMMONS,
            "pd_basis": "Early-modern object, long out of copyright; the Commons file "
                        "page states public domain",
        },
    },
    "paris-anonymous-tarot": {
        "image_credit": None,
        "commons": [
            {"name": "Anonymous Parisian cardmaker", "date": "c. 1600-1650",
             "note": "No maker's name appears on the cards, not even in the Two of "
                     "Coins cartouche where a maker would normally sign"},
            {"name": "Bibliothèque nationale de France", "date": "holding institution",
             "note": "Holds the sole surviving complete copy, shelfmark RESERVE KH-34; "
                     "digitised on Gallica as ark:/12148/btv1b105109624"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture and summaries"},
        ],
        "provenance": {
            "holding_institution": "Bibliothèque nationale de France, Paris — shelfmark "
                                   "RESERVE KH-34",
            "archive": "Gallica, ark:/12148/btv1b105109624",
            "license": PD_GALLICA,
            "pd_basis": "A 17th-century woodcut, long out of copyright; the BnF "
                        "publishes the scan on Gallica as public domain.",
            "unknown": "This block records the image source only. The deck's own "
                       "`description` still carries the misidentification the deck "
                       "dossier flags (research/decks/paris-anonymous-tarot.md) — it "
                       "denies being the Tarot de Paris while citing that object's ark. "
                       "That is a separate text correction, not touched here.",
            "rule": "images/cNN.jpg is Gallica folio 2·NN−1 of the same ark — odd folios "
                    "are the card faces, even folios the patterned backs. Mapping "
                    "recovered from scripts/prebake_deck_r2.py high_res_url().",
        },
        "cover": {
            "title": "Le Monde (XXI) — anonymous Parisian tarot",
            "creator": "Anonymous Parisian cardmaker",
            "date": "c. 1600-1650 (Depaulis: first half of the 17th century)",
            "source": "Bibliothèque nationale de France, RESERVE KH-34, on Gallica "
                      "(ark:/12148/btv1b105109624)",
            "license": PD_GALLICA,
            "pd_basis": "17th-century woodcut, long out of copyright; the BnF publishes "
                        "the scan as public domain",
        },
    },
    "vieville-tarot": {
        "image_credit": None,
        "commons": [
            {"name": "Jacques Viéville", "date": "c. 1650",
             "note": "Maître-cartier, Paris; the earliest surviving witness of the "
                     "non-Marseille pattern that descends to the Belgian line"},
            {"name": "Bibliothèque nationale de France", "date": "holding institution",
             "note": "Holds the single known copy; digitised on Gallica as "
                     "ark:/12148/btv1b10510963k"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture and summaries"},
        ],
        "provenance": {
            "holding_institution": "Bibliothèque nationale de France, Paris",
            "archive": "Gallica, ark:/12148/btv1b10510963k",
            "license": PD_GALLICA,
            "pd_basis": "A c. 1650 woodcut, long out of copyright; the BnF publishes "
                        "the scan on Gallica as public domain.",
            "unknown": "Viéville's precise working dates are undocumented; 'c. 1650' "
                       "rests on style and trade context, not a dated colophon.",
            "rule": "images/cNN.jpg is Gallica folio 2·NN−1 of the same ark — odd folios "
                    "are the card faces, even folios the patterned backs. Mapping "
                    "recovered from scripts/prebake_deck_r2.py high_res_url().",
        },
        "cover": {
            "title": "Le Monde (XXI) — Jacques Viéville tarot",
            "creator": "Jacques Viéville",
            "date": "c. 1650",
            "source": "Bibliothèque nationale de France, on Gallica "
                      "(ark:/12148/btv1b10510963k)",
            "license": PD_GALLICA,
            "pd_basis": "c. 1650 woodcut, long out of copyright; the BnF publishes the "
                        "scan as public domain",
        },
    },
}


def grammar_path(slug):
    return os.path.join(ROOT, "tarot", slug, "grammar.json")


def insert_after(d, anchor, key, value):
    """Insert key immediately after `anchor`, preserving key order; if the key
    already exists, overwrite in place."""
    if key in d:
        d[key] = value
        return d
    out = {}
    for k, v in d.items():
        out[k] = v
        if k == anchor:
            out[key] = value
    if key not in out:
        out[key] = value
    return out


def build(slug, grammar):
    """Return (new_grammar, stats). Pure enough — operates on a fresh dict."""
    spec = DECKS[slug]
    g = dict(grammar)

    g = insert_after(g, "license", "_grammar_commons", {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": spec["commons"],
    })

    prov = dict(spec["provenance"])
    prov = {
        "schema_version": "1.0",
        "holding_institution": prov.pop("holding_institution"),
        "archive": prov.pop("archive"),
        "license": prov.pop("license"),
        "pd_basis": prov.pop("pd_basis"),
        "verified": VERIFIED,
        "per_item_field": "metadata.image_source",
        "mapping_rule": prov.pop("rule"),
        "unknown": prov.pop("unknown"),
    }
    g = insert_after(g, "_grammar_commons", "_image_provenance", prov)

    cover = dict(spec["cover"])
    cover_src = source_for(slug, g.get("cover_image_url"))
    g = insert_after(g, "cover_image_url", "cover_image_credit", {
        "title": cover["title"],
        "creator": cover["creator"],
        "date": cover["date"],
        "source": cover["source"],
        "file_page": cover_src,
        "license": cover["license"],
        "pd_basis": cover["pd_basis"],
        "verified": VERIFIED,
    })

    if spec["image_credit"]:
        g["image_credit"] = spec["image_credit"]

    stamped, unmapped = 0, []
    items = []
    for it in g["items"]:
        it = dict(it)
        url = it.get("image_url")
        if url:
            src = source_for(slug, url)
            if src is None:
                unmapped.append((it["id"], url))
            else:
                md = dict(it.get("metadata") or {})
                md["image_source"] = src
                it["metadata"] = md
                stamped += 1
        items.append(it)
    g["items"] = items

    return g, {"stamped": stamped, "unmapped": unmapped,
               "cover_mapped": cover_src is not None}


def all_source_urls():
    urls = set()
    for slug in DECKS:
        g = json.load(open(grammar_path(slug), encoding="utf-8"))
        for u in [g.get("cover_image_url")] + [i.get("image_url") for i in g["items"]]:
            s = source_for(slug, u)
            if s:
                urls.add(s)
    return sorted(urls)


def verify_urls():
    urls = all_source_urls()
    print(f"HEAD-checking {len(urls)} distinct source URLs...")
    bad = []
    for u in urls:
        # Gallica and Commons both throttle a fast sequential sweep; back off
        # and retry rather than recording a rate-limit as a broken source.
        code = None
        for attempt in range(4):
            try:
                code = urllib.request.urlopen(urllib.request.Request(
                    u, method="HEAD", headers={"User-Agent": UA}), timeout=60).status
            except urllib.error.HTTPError as e:
                code = e.code
            except Exception as e:
                code = type(e).__name__
            if code == 200:
                break
            time.sleep(3 * (attempt + 1))
        if code != 200:
            bad.append((code, u))
            print(f"  FAIL {code} {u}")
        time.sleep(0.35)
    if bad:
        print(f"\nFAIL: {len(bad)} of {len(urls)} source URLs did not return 200")
        return False
    print(f"OK: all {len(urls)} source URLs return 200")
    return True


def run(write):
    ok, changed = True, 0
    for slug in DECKS:
        path = grammar_path(slug)
        before = json.load(open(path, encoding="utf-8"))
        after, stats = build(slug, before)

        # Nothing-lost: the backfill only ADDS keys. Every pre-existing value
        # must survive byte-for-byte, apart from belgian-tarot's deliberately
        # rewritten image_credit string.
        allowed = {"image_credit"} if DECKS[slug]["image_credit"] else set()
        for k, v in before.items():
            if k == "items":
                continue
            if k in allowed:
                continue
            if after.get(k) != v:
                print(f"FAIL {slug}: pre-existing top-level '{k}' changed")
                ok = False
        for a, b in zip(before["items"], after["items"]):
            if a["id"] != b["id"]:
                print(f"FAIL {slug}: item order changed")
                ok = False
                break
            for k, v in a.items():
                if k == "metadata":
                    continue
                if b.get(k) != v:
                    print(f"FAIL {slug}/{a['id']}: pre-existing '{k}' changed")
                    ok = False
            for k, v in (a.get("metadata") or {}).items():
                if (b.get("metadata") or {}).get(k) != v:
                    print(f"FAIL {slug}/{a['id']}: pre-existing metadata.{k} changed")
                    ok = False
        if len(before["items"]) != len(after["items"]):
            print(f"FAIL {slug}: item count changed")
            ok = False

        n_img = sum(1 for i in before["items"] if i.get("image_url"))
        if stats["unmapped"]:
            for iid, url in stats["unmapped"]:
                print(f"FAIL {slug}/{iid}: no recovered source for {url}")
            ok = False
        if not stats["cover_mapped"]:
            print(f"FAIL {slug}: no recovered source for the cover image")
            ok = False
        print(f"  {slug:24s} images={n_img:3d} stamped={stats['stamped']:3d} "
              f"cover_credit=yes commons=yes provenance=yes")

        if before != after:
            changed += 1
            if write:
                with open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(json.dumps(after, ensure_ascii=False, indent=2) + "\n")
    if write:
        print(f"wrote {changed} grammar(s)" if changed else "no changes (idempotent)")
    return ok, changed


def check():
    ok = True
    for slug in DECKS:
        g = json.load(open(grammar_path(slug), encoding="utf-8"))
        for key in ("_grammar_commons", "_image_provenance", "cover_image_credit"):
            if key not in g:
                print(f"FAIL {slug}: missing {key}")
                ok = False
        for it in g["items"]:
            if it.get("image_url") and not (it.get("metadata") or {}).get("image_source"):
                print(f"FAIL {slug}/{it['id']}: image_url with no metadata.image_source")
                ok = False
        rebuilt, _ = build(slug, g)
        if rebuilt != g:
            print(f"FAIL {slug}: provenance is out of date — re-run without --check")
            ok = False
    if ok:
        total = sum(sum(1 for i in json.load(open(grammar_path(s), encoding="utf-8"))["items"]
                        if i.get("image_url")) for s in DECKS)
        print(f"OK: {len(DECKS)} decks — _grammar_commons, _image_provenance and "
              f"cover_image_credit present; {total} item images all carry "
              f"metadata.image_source")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify only; no writes, no network")
    ap.add_argument("--verify-urls", action="store_true",
                    help="HEAD-check every source URL this script writes")
    args = ap.parse_args()

    if args.verify_urls:
        sys.exit(0 if verify_urls() else 1)
    if args.check:
        sys.exit(0 if check() else 1)

    print("--- dry run ---")
    ok, _ = run(write=False)
    if not ok:
        print("\nFAIL: dry-run verification failed; nothing written")
        sys.exit(1)
    print("--- writing ---")
    ok, _ = run(write=True)
    if not ok:
        print("\nFAIL: write-pass verification failed")
        sys.exit(1)
    print("\n--- verifying ---")
    if not check():
        sys.exit(1)


if __name__ == "__main__":
    main()
