#!/usr/bin/env python3
"""Keep images/ within budget.

There is no build-time image pipeline: whatever is committed is exactly what every
reader downloads. This checks a directory against the budget in the writing style
guide (§8) and, with --apply, brings it back in line.

    optimize_images.py --check images/blog29      # default; exits 1 if over budget
    optimize_images.py --apply images/blog29      # resize/recompress in place
    optimize_images.py --apply --to-webp images/  # also convert heavy PNGs to WebP
    optimize_images.py --report images            # before/after table, changes nothing

--check is the default so an accidental invocation cannot destroy an image.
--apply never upscales and never writes a file larger than the one it replaces.
--to-webp writes new .webp files and prints {"renames": {...}} to stdout; it does not
edit any markdown, so the filesystem change and the content change stay separate and
separately reviewable (the same contract as fetch_arxiv_figures.py).

Pillow only — no ffmpeg, no cwebp, no Homebrew — because this has to run in the cloud
sandbox. Animated formats are skipped: converting a GIF to video is a one-time local
job, see the style guide.
"""

import argparse, json, io, os, sys

MAX_W = 1600
FIGURE_MAX_BYTES = 150 * 1024
COVER_MAX_BYTES = 200 * 1024
QUALITY = 82
OK_EXT = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG", ".webp": "WEBP"}
PRUNE_DIRS = {".claude", "_site", ".git", ".sass-cache"}


def budget_for(path):
    return COVER_MAX_BYTES if os.path.basename(path).startswith("cover.") else FIGURE_MAX_BYTES


def iter_images(paths):
    for p in paths:
        if os.path.isfile(p):
            candidates = [p]
        else:
            candidates = []
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if d not in PRUNE_DIRS]
                candidates += [os.path.join(root, n) for n in names]
        for f in sorted(candidates):
            if os.path.splitext(f)[1].lower() in OK_EXT:
                yield f


def load(path, max_width):
    """Open, and downscale to max_width if wider. Never upscales."""
    from PIL import Image
    im = Image.open(path)
    im.load()
    if im.width > max_width:
        im = im.copy()
        im.thumbnail((max_width, max_width * 8), Image.LANCZOS)
    return im


def is_flat_art(im):
    """A diagram or screenshot has few colours and quantizes cleanly; a photo does not."""
    try:
        return im.convert("RGB").getcolors(4096) is not None
    except Exception:
        return False


def encode(im, fmt):
    buf = io.BytesIO()
    if fmt == "WEBP":
        im.save(buf, "WEBP", quality=QUALITY, method=6)
    elif fmt == "JPEG":
        im.convert("RGB").save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    else:
        out = im
        if is_flat_art(im) and im.mode in ("RGB", "RGBA"):
            from PIL import Image
            out = im.convert("P", palette=Image.ADAPTIVE, colors=256)
        out.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def best_encoding(path, max_width, to_webp):
    """Return (new_path, data) for the best result, or None to leave the file alone."""
    size = os.path.getsize(path)
    fmt = OK_EXT[os.path.splitext(path)[1].lower()]
    im = load(path, max_width)

    data, new_path = encode(im, fmt), path
    if to_webp and fmt == "PNG" and len(data) > budget_for(path):
        webp = encode(im, "WEBP")
        if len(webp) < len(data):
            data, new_path = webp, os.path.splitext(path)[0] + ".webp"

    if new_path == path and len(data) >= size:   # never grow
        return None
    return new_path, data


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--check", action="store_true", help="report over-budget files, exit 1 (default)")
    ap.add_argument("--apply", action="store_true", help="rewrite files in place")
    ap.add_argument("--to-webp", action="store_true", help="convert heavy PNGs to WebP (preview under --report)")
    ap.add_argument("--report", action="store_true", help="before/after table, changes nothing")
    ap.add_argument("--max-width", type=int, default=MAX_W)
    args = ap.parse_args()

    paths = args.paths or ["images"]
    if not (args.apply or args.report):
        args.check = True

    over, rows, renames, saved = [], [], {}, 0

    for path in iter_images(paths):
        size = os.path.getsize(path)
        try:
            if args.check:
                from PIL import Image
                with Image.open(path) as probe:
                    width = probe.width
                why = []
                if size > budget_for(path):
                    why.append("%.0f KB > %.0f KB" % (size / 1024.0, budget_for(path) / 1024.0))
                if width > args.max_width:
                    why.append("%d px wide > %d px" % (width, args.max_width))
                if why:
                    over.append((path, "; ".join(why)))
                continue

            result = best_encoding(path, args.max_width, args.to_webp)
        except Exception as e:
            print("  ! skipped %s (%s)" % (path, e), file=sys.stderr)
            continue

        if not result:
            continue
        new_path, data = result

        if args.apply:
            with open(new_path, "wb") as fh:
                fh.write(data)
            if new_path != path:
                os.remove(path)
                renames["/" + path] = "/" + new_path
        rows.append((path, new_path, size, len(data)))
        saved += size - len(data)

    if args.check:
        for p, why in over:
            print("OVER BUDGET  %-52s %s" % (p, why))
        if over:
            print("\n%d file(s) over budget. Run with --apply to fix." % len(over))
            return 1
        print("All images within budget (<=%d px; <=%d KB figures, <=%d KB covers)."
              % (args.max_width, FIGURE_MAX_BYTES / 1024, COVER_MAX_BYTES / 1024))
        return 0

    print("| file | before | after |")
    print("|---|---|---|")
    for p, np_, a, b in rows:
        name = p if p == np_ else "%s → %s" % (p, os.path.basename(np_))
        print("| %s | %.0f KB | %.0f KB |" % (name, a / 1024.0, b / 1024.0))
    print("\n**%d file(s), %.1f MB %s.**"
          % (len(rows), saved / 1048576.0, "saved" if args.apply else "savable"))
    if renames:
        print(json.dumps({"renames": renames}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
