#!/usr/bin/env python3
"""
Fetch figures from an arXiv paper, but ONLY when the paper's licence permits
redistribution.

The weekly blog job runs unattended and publishes to a public site, so the
default must be to refuse. Papers on arXiv's own "nonexclusive-distrib"
licence grant arXiv the right to distribute; they grant us nothing. Only the
Creative Commons licences below allow us to re-publish a figure with
attribution.

Usage:
    fetch_arxiv_figures.py 2506.09985 --out images/blog29 [--max 6] [--prefix vjepa2]

Prints a JSON manifest to stdout:
    {"arxiv_id","licence","licence_url","redistributable",
     "figures":[{"file","caption","source_path"}], "note"}

Exit codes: 0 usable (or cleanly refused, with redistributable=false), 2 error.
"""
import argparse, json, os, re, ssl, subprocess, sys, tarfile, tempfile, urllib.request

UA = {"User-Agent": "cgnarendiran.github.io figure fetcher (contact: cgnarendiran@gmail.com)"}

def _ctx():
    """Verified TLS. macOS system Python often ships without a CA bundle, so fall
    back to certifi. Verification is never disabled - a silent MITM on a script
    that publishes to a live site is not a trade worth making."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()

_SSL = _ctx()

# Licences that permit redistribution with attribution. Anything not listed is refused.
ALLOWED = {
    "creativecommons.org/licenses/by/4.0":      "CC BY 4.0",
    "creativecommons.org/licenses/by/3.0":      "CC BY 3.0",
    "creativecommons.org/licenses/by-sa/4.0":   "CC BY-SA 4.0",
    "creativecommons.org/licenses/by-sa/3.0":   "CC BY-SA 3.0",
    "creativecommons.org/publicdomain/zero/1.0":"CC0 1.0",
}

def get(url, binary=False):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90, context=_SSL) as r:
        return r.read() if binary else r.read().decode("utf-8", "replace")

def detect_licence(arxiv_id):
    html = get(f"https://arxiv.org/abs/{arxiv_id}")
    for key, name in ALLOWED.items():
        if key in html:
            return name, "https://" + key, True
    m = re.search(r'(arxiv\.org/licenses/[a-z-]+/[0-9.]+)', html, re.I)
    if m:
        return "arXiv non-exclusive licence to distribute", "https://" + m.group(1), False
    return "unknown", "", False

def map_captions(root):
    """Map an included graphic's basename -> its \\caption text."""
    tex = ""
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.endswith(".tex"):
                try:
                    tex += open(os.path.join(dirpath, f), errors="ignore").read() + "\n"
                except OSError:
                    pass
    out = {}
    for env in re.findall(r'\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}', tex, re.S):
        incs = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', env)
        cap = re.search(r'\\caption\{(.*?)(?:\\label|\}\s*\n)', env, re.S)
        if not incs or not cap:
            continue
        text = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?', ' ', cap.group(1))
        text = " ".join(re.sub(r'[{}$\\~^_]', ' ', text).split())
        for inc in incs:
            out[os.path.splitext(os.path.basename(inc))[0]] = text[:400]
    return out

MAX_W = 1600  # web width; keeps the repo from bloating at two posts a week

def _shrink(path):
    try:
        from PIL import Image
        im = Image.open(path)
        if im.width > MAX_W:
            im = im.convert("RGB") if im.mode in ("P", "RGBA") else im
            im.thumbnail((MAX_W, MAX_W * 4), Image.LANCZOS)
            im.save(path, optimize=True)
    except Exception:
        pass  # a large image is still a usable image

def to_png(src, dst):
    if src.lower().endswith((".png", ".jpg", ".jpeg")):
        import shutil; shutil.copy(src, dst); _shrink(dst); return True
    try:
        import pymupdf
    except ImportError:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--user", "pymupdf"],
                           check=True, capture_output=True)
            import pymupdf
        except Exception:
            return False
    try:
        doc = pymupdf.open(src)
        doc[0].get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5)).save(dst)
        _shrink(dst)
        return True
    except Exception:
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arxiv_id")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max", type=int, default=6)
    ap.add_argument("--prefix", default="")
    a = ap.parse_args()
    aid = a.arxiv_id.replace("arXiv:", "").strip()

    try:
        name, url, ok = detect_licence(aid)
    except Exception as e:
        json.dump({"arxiv_id": aid, "error": f"licence check failed: {e}",
                   "redistributable": False, "figures": []}, sys.stdout, indent=2)
        return 2

    result = {"arxiv_id": aid, "licence": name, "licence_url": url,
              "redistributable": ok, "figures": [], "note": ""}

    if not ok:
        result["note"] = ("Licence does not permit redistribution. Do NOT commit or hotlink "
                          "figures from this paper. Draw the diagram yourself with matplotlib "
                          "and caption it 'Source: Author', or cite the paper in prose instead.")
        json.dump(result, sys.stdout, indent=2); print(); return 0

    with tempfile.TemporaryDirectory() as td:
        try:
            blob = get(f"https://arxiv.org/e-print/{aid}", binary=True)
            tgz = os.path.join(td, "s.tar.gz"); open(tgz, "wb").write(blob)
            ex = os.path.join(td, "x"); os.makedirs(ex, exist_ok=True)
            with tarfile.open(tgz) as t:
                # filter= is 3.12+; pass it when available, guard manually otherwise
                try:
                    t.extractall(ex, filter="data")
                except TypeError:
                    for m in t.getmembers():
                        if m.issym() or m.islnk():
                            continue
                        dest = os.path.realpath(os.path.join(ex, m.name))
                        if dest.startswith(os.path.realpath(ex) + os.sep):
                            t.extract(m, ex)
        except Exception as e:
            result["note"] = f"source fetch/extract failed: {e}"
            json.dump(result, sys.stdout, indent=2); print(); return 0

        caps = map_captions(ex)
        os.makedirs(a.out, exist_ok=True)
        cands = []
        for dp, _, fs in os.walk(ex):
            for f in fs:
                if f.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
                    stem = os.path.splitext(f)[0]
                    if stem in caps:
                        cands.append((os.path.join(dp, f), stem, caps[stem]))
        # Prefer a whole figure over one of its panels: files ending _0/_1/-2 are
        # usually sub-panels sharing one caption. Rank non-panels first, then by
        # size, then keep only the first file per distinct caption.
        def rank(c):
            src, stem, cap = c
            is_panel = bool(re.search(r'[_-]\d+$', stem))
            return (is_panel, -os.path.getsize(src))
        cands.sort(key=rank)
        seen, deduped = set(), []
        for c in cands:
            key = c[2][:120]
            if key in seen:
                continue
            seen.add(key); deduped.append(c)
        cands = deduped
        for src, stem, cap in cands[:a.max]:
            safe = re.sub(r'[^a-z0-9-]+', '-', stem.lower()).strip('-')
            dst = os.path.join(a.out, f"{a.prefix + '-' if a.prefix else ''}{safe}.png")
            if to_png(src, dst):
                result["figures"].append({"file": dst, "caption": cap,
                                          "source_path": os.path.relpath(src, ex)})
        result["note"] = (f"{len(result['figures'])} figure(s) written. Licence {name} requires "
                          f"attribution in the caption: 'Source: [<paper>](https://arxiv.org/abs/{aid})'."
                          + (" CC BY-SA additionally requires derivative figures share alike."
                             if "SA" in name else ""))
    json.dump(result, sys.stdout, indent=2); print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
