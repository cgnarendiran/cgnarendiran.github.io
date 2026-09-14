#!/usr/bin/env python3
"""Find and fetch an openly licensed cover image from Wikimedia Commons.

Usage:
  commons_cover.py search "<term>" ["<term>" ...]
      Print candidates: title | licence | author | WxH | description. Only files whose
      licence is public domain, CC0, CC BY or CC BY-SA, and at least 1000 px wide.
      Commons search is literal: try the object's plain name, its name in the language of
      the place (合格発表 found what "exam results" did not), and category names.

  commons_cover.py fetch "File:<title>" --out images/blogNN/cover.jpg [--crop x0,y0,x1,y1]
      Verify the licence again, download the original, crop (fractions of width/height,
      default the whole image), trim to the site's 1.905:1 cover shape, resize to 1400 px
      wide, and save a progressive JPEG under 200 KB. Prints the caption credit to paste
      into the `*On the cover: …*` line.

Refuses any file whose licence is not on the allow list. Needs Pillow. If the machine's
Python has no CA bundle (python.org builds), install certifi; the script uses it if present.
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "cgnarendiran-blog-cover/1.0 (https://cgnarendiran.github.io)"}


def licence_ok(lic):
    """Public domain, CC0, CC BY or CC BY-SA, any version. Anything with NC or ND is refused,
    as is GFDL-only, fair use, or an unknown string."""
    l = lic.lower()
    if re.search(r"\b(nc|nd)\b|non-?commercial|no ?derivatives", l):
        return False
    return ("public domain" in l or l.startswith("cc0") or l.startswith("pd")
            or re.match(r"^cc[ -]by(-sa)?(\b|$)", l) is not None)

RATIO = 1.905
WIDTH = 1400
MAX_BYTES = 195 * 1024

try:
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except ImportError:
    pass


def api(params):
    params = dict(params, format="json")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=60))


def strip(s):
    return re.sub(r"<[^>]+>", "", html.unescape(s or "")).strip()


def info(page):
    ii = page["imageinfo"][0]
    em = ii.get("extmetadata", {})
    lic = em.get("LicenseShortName", {}).get("value", "?")
    return {
        "title": page["title"],
        "licence": lic,
        "ok": licence_ok(lic),
        "author": strip(em.get("Artist", {}).get("value", ""))[:80],
        "desc": strip(em.get("ImageDescription", {}).get("value", ""))[:160].replace("\n", " "),
        "w": ii["width"], "h": ii["height"], "mime": ii["mime"],
        "url": ii["url"], "page": ii["descriptionurl"],
    }


def search(terms):
    for term in terms:
        print(f"=== {term}")
        r = api({"action": "query", "generator": "search", "gsrsearch": term, "gsrnamespace": 6,
                 "gsrlimit": 15, "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata"})
        for page in r.get("query", {}).get("pages", {}).values():
            i = info(page)
            if i["mime"] not in ("image/jpeg", "image/png") or i["w"] < 1000 or not i["ok"]:
                continue
            print(f"  {i['title']} | {i['licence']} | {i['author']} | {i['w']}x{i['h']} | {i['desc']}")


def fetch(title, out, crop):
    from PIL import Image, ImageOps
    r = api({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata"})
    page = next(iter(r["query"]["pages"].values()))
    if "imageinfo" not in page:
        sys.exit(f"not found on Commons: {title}")
    i = info(page)
    if not i["ok"]:
        sys.exit(f"REFUSED: licence is '{i['licence']}', not public domain / CC0 / CC BY / CC BY-SA")
    data = urllib.request.urlopen(urllib.request.Request(i["url"], headers=UA), timeout=300).read()
    tmp = out + ".orig"
    with open(tmp, "wb") as f:
        f.write(data)
    im = ImageOps.exif_transpose(Image.open(tmp)).convert("RGB")
    os.remove(tmp)
    x0, y0, x1, y1 = crop
    im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    w, h = im.size
    if w / h > RATIO:
        nw = int(h * RATIO); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / RATIO); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((WIDTH, int(WIDTH / RATIO)), Image.LANCZOS)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    for q in (88, 82, 76, 70, 64, 58, 52, 46):
        im.save(out, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(out) <= MAX_BYTES:
            break
    lic = i["licence"]
    if "public domain" in lic.lower():
        credit = f"[Public domain]({i['page']}), via Wikimedia Commons."
    else:
        credit = f"Photo by [{i['author'] or 'the uploader'}]({i['page']}), {lic}."
    print(f"saved {out} {im.size} {os.path.getsize(out) // 1024} KB (quality {q})")
    print(f"licence: {lic}")
    print(f"credit for the caption: {credit}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("terms", nargs="+")
    f = sub.add_parser("fetch"); f.add_argument("title"); f.add_argument("--out", required=True)
    f.add_argument("--crop", default="0,0,1,1", help="x0,y0,x1,y1 as fractions, default whole image")
    a = ap.parse_args()
    if a.cmd == "search":
        search(a.terms)
    else:
        crop = tuple(float(v) for v in a.crop.split(","))
        if len(crop) != 4:
            sys.exit("--crop needs four numbers")
        fetch(a.title, a.out, crop)


if __name__ == "__main__":
    main()
