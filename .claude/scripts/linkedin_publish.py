#!/usr/bin/env python3
"""Publish LinkedIn posts from the repo outbox through LinkedIn's Posts API.

Outbox files live in .claude/linkedin-outbox/<slug>.md: a front-matter block between
two '---' lines, then the post body as plain text. Keys:
  slug            required, matches the blog post filename slug
  publish_after   required, ISO-8601 with a UTC offset, e.g. 2026-09-07T08:30:00-07:00
  blog_date       recommended, YYYY-MM-DD
  title, image (repo-relative path), alt, source   optional

The body is plain text. Two constructs are recognised and everything else is escaped for
LinkedIn's "little" text format:
  @[Fast Code AI](urn:li:organization:70969206)   a mention
  #Hashtag                                         a hashtag

Usage:
  linkedin_publish.py --file <outbox.md> --dry-run            validate and show the escaped text
  linkedin_publish.py --file <outbox.md> [--force] [--ledger .claude/linkedin-ledger.md]
  linkedin_publish.py --dir .claude/linkedin-outbox --list-due
  linkedin_publish.py --dir .claude/linkedin-outbox --publish-due --ledger .claude/linkedin-ledger.md

Environment (or --env-file KEY=VALUE lines):
  LINKEDIN_ACCESS_TOKEN    OAuth token with w_member_social; lives 60 days
  LINKEDIN_PERSON_URN      urn:li:person:<sub>, printed by linkedin_auth.py
  LINKEDIN_API_VERSION     optional, default 202608 (YYYYMM, LinkedIn sunsets after a year)
  LINKEDIN_TOKEN_EXPIRES   optional YYYY-MM-DD, only used to warn

With --ledger, a successful publish appends a row to the ledger and deletes the outbox
file, so the caller only has to commit. Prints one JSON object per file on stdout.

Exit codes: 0 ok, 2 input or configuration error, 3 API error, 4 token rejected
(re-run linkedin_auth.py and update the environment), 5 nothing due.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request


# python.org builds of Python on macOS ship without system CA certificates, so HTTPS fails
# with CERTIFICATE_VERIFY_FAILED. If certifi is importable, use its bundle. Harmless elsewhere.
if not os.environ.get("SSL_CERT_FILE"):
    try:
        import certifi
        os.environ["SSL_CERT_FILE"] = certifi.where()
    except ImportError:
        pass

API = "https://api.linkedin.com"
DEFAULT_VERSION = "202608"
MAX_CHARS = 3000
RESERVED = set("\\|{}@[]()<>#*_~")
TOKEN_RE = re.compile(
    r"(?P<mention>@\[(?P<name>[^\]]+)\]\((?P<urn>urn:li:(?:person|organization):[A-Za-z0-9_\-]+)\))"
    r"|(?P<hashtag>(?<![\w/&])#(?P<tag>[A-Za-z0-9_]+))"
)


class TokenRejected(Exception):
    pass


class ApiError(Exception):
    def __init__(self, where, status, body):
        super().__init__(f"{where}: HTTP {status}: {body[:500]}")
        self.where, self.status, self.body = where, status, body


# ----- text -----

def esc(s):
    return "".join("\\" + c if c in RESERVED else c for c in s)


def little_text(body):
    """Escape plain text for LinkedIn's little format, keeping mentions and hashtags live."""
    out, pos = [], 0
    for m in TOKEN_RE.finditer(body):
        out.append(esc(body[pos:m.start()]))
        if m.group("mention"):
            out.append("@[" + esc(m.group("name")) + "](" + m.group("urn") + ")")
        else:
            out.append("{hashtag|\\#|" + m.group("tag") + "}")
        pos = m.end()
    out.append(esc(body[pos:]))
    return "".join(out)


# ----- files -----

def load_env_file(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def parse_outbox(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{path}: unterminated front matter")
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    body = text[end + 5:].strip("\n")
    for key in ("slug", "publish_after"):
        if not meta.get(key):
            raise ValueError(f"{path}: front matter needs '{key}'")
    if not body:
        raise ValueError(f"{path}: empty body")
    return meta, body


def parse_when(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    d = dt.datetime.fromisoformat(s)
    if d.tzinfo is None:
        raise ValueError(f"publish_after must carry a UTC offset: {s}")
    return d


def ledger_has(ledger, slug):
    if not ledger or not os.path.exists(ledger):
        return False
    pat = re.compile(r"^\|\s*" + re.escape(slug) + r"\s*\|", re.M)
    return bool(pat.search(open(ledger, encoding="utf-8").read()))


def append_ledger(ledger, meta, post_urn, now):
    row = "| {slug} | {blog_date} | {urn} | {published} | {run} | {notes} |\n".format(
        slug=meta["slug"],
        blog_date=meta.get("blog_date", ""),
        urn=post_urn,
        published=now.strftime("%Y-%m-%dT%H:%MZ"),
        run=now.strftime("%Y-%m-%d"),
        notes=(meta.get("source", "") + " via LinkedIn API").strip(),
    )
    s = open(ledger, encoding="utf-8").read().rstrip("\n") + "\n" + row
    open(ledger, "w", encoding="utf-8").write(s)


# ----- API -----

def http(method, url, headers, data=None):
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, e.read().decode("utf-8", "replace")


def api_headers(token, version, content_type="application/json"):
    h = {
        "Authorization": f"Bearer {token}",
        "Linkedin-Version": version,
        "X-Restli-Protocol-Version": "2.0.0",
    }
    if content_type:
        h["Content-Type"] = content_type
    return h


def upload_image(token, version, owner, path):
    st, hd, body = http(
        "POST", f"{API}/rest/images?action=initializeUpload", api_headers(token, version),
        json.dumps({"initializeUploadRequest": {"owner": owner}}).encode(),
    )
    if st == 401:
        raise TokenRejected(body)
    if st != 200:
        raise ApiError("initializeUpload", st, body)
    value = json.loads(body)["value"]
    with open(path, "rb") as f:
        data = f.read()
    st, hd, body = http(
        "PUT", value["uploadUrl"],
        {"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"},
        data,
    )
    if st not in (200, 201):
        raise ApiError("upload", st, body)
    return value["image"]


def create_post(token, version, author, commentary, image_urn=None, alt=None):
    payload = {
        "author": author,
        "commentary": commentary,
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    if image_urn:
        media = {"id": image_urn}
        if alt:
            media["altText"] = alt
        payload["content"] = {"media": media}
    st = body = None
    for attempt in range(4):
        st, hd, body = http("POST", f"{API}/rest/posts", api_headers(token, version), json.dumps(payload).encode())
        if st == 201:
            return hd.get("x-restli-id")
        if st == 401:
            raise TokenRejected(body)
        transient = st in (409, 500, 503) or (st in (400, 422) and "process" in body.lower())
        if transient and attempt < 3:
            time.sleep(10 * (attempt + 1))
            continue
        raise ApiError("createPost", st, body)
    raise ApiError("createPost", st, body or "")


# ----- driver -----

def check_file(path, args, now):
    meta, body = parse_outbox(path)
    when = parse_when(meta["publish_after"])
    warnings = []
    if len(body) > MAX_CHARS:
        raise ValueError(f"{path}: body is {len(body)} characters, LinkedIn's limit is {MAX_CHARS}")
    image_path = None
    if meta.get("image"):
        image_path = os.path.join(args.image_root, meta["image"])
        if not os.path.exists(image_path):
            raise ValueError(f"{path}: image not found at {image_path}")
    if "@[Fast Code AI](urn:li:organization:70969206)" not in body:
        warnings.append("no Fast Code AI mention in the body")
    if not re.search(r"https://cgnarendiran\.github\.io/", body):
        warnings.append("no cgnarendiran.github.io link in the body")
    return meta, body, when, image_path, warnings


def publish_file(path, args, env, now):
    meta, body, when, image_path, warnings = check_file(path, args, now)
    due = when <= now
    commentary = little_text(body)
    result = {
        "file": path, "slug": meta["slug"], "publish_after": when.isoformat(), "due": due,
        "chars": len(body), "commentary_chars": len(commentary), "image": image_path, "warnings": warnings,
    }
    if args.ledger and ledger_has(args.ledger, meta["slug"]):
        result["skipped"] = "slug already in ledger"
        return result
    if args.dry_run:
        result["dry_run"] = True
        result["commentary"] = commentary
        return result
    if not due and not args.force:
        result["skipped"] = "not due yet"
        return result

    token, author, version = env["token"], env["urn"], env["version"]
    image_urn = None
    if image_path:
        image_urn = upload_image(token, version, author, image_path)
        result["image_urn"] = image_urn
        time.sleep(5)
    post_urn = create_post(token, version, author, commentary, image_urn, meta.get("alt") or None)
    result["post_urn"] = post_urn
    result["post_url"] = f"https://www.linkedin.com/feed/update/{post_urn}/" if post_urn else None
    if args.ledger:
        append_ledger(args.ledger, meta, post_urn or "unknown", now)
        os.remove(path)
        result["ledger"] = "row appended, outbox file removed"
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="one outbox file")
    src.add_argument("--dir", help="outbox directory")
    ap.add_argument("--list-due", action="store_true", help="with --dir: list due files and exit")
    ap.add_argument("--publish-due", action="store_true", help="with --dir: publish every due file, oldest first")
    ap.add_argument("--dry-run", action="store_true", help="validate and print the escaped commentary; no network")
    ap.add_argument("--force", action="store_true", help="with --file: publish even if publish_after is in the future")
    ap.add_argument("--ledger", help="ledger to append to (and delete the outbox file) on success")
    ap.add_argument("--env-file", help="KEY=VALUE file with the LINKEDIN_* variables")
    ap.add_argument("--image-root", default=".", help="directory the image path is relative to (repo root)")
    args = ap.parse_args()

    if args.env_file:
        load_env_file(args.env_file)
    now = dt.datetime.now(dt.timezone.utc)

    if args.file:
        files = [args.file]
    else:
        files = sorted(glob.glob(os.path.join(args.dir, "*.md")))
        try:
            files.sort(key=lambda p: parse_when(parse_outbox(p)[0]["publish_after"]))
        except ValueError as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(2)

    if args.list_due:
        due = []
        for p in files:
            try:
                meta, body, when, image_path, warnings = check_file(p, args, now)
            except ValueError as e:
                print(json.dumps({"file": p, "error": str(e)}))
                sys.exit(2)
            if when <= now and not (args.ledger and ledger_has(args.ledger, meta["slug"])):
                due.append((p, when))
        for p, when in due:
            print(f"{p}\t{when.isoformat()}")
        sys.exit(0 if due else 5)

    warn_days = None
    if os.environ.get("LINKEDIN_TOKEN_EXPIRES"):
        try:
            exp = dt.date.fromisoformat(os.environ["LINKEDIN_TOKEN_EXPIRES"])
            warn_days = (exp - now.date()).days
        except ValueError:
            pass

    env = None
    if not args.dry_run:
        token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
        urn = os.environ.get("LINKEDIN_PERSON_URN")
        if not token or not urn:
            print(json.dumps({"error": "LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN must be set"}))
            sys.exit(2)
        env = {"token": token, "urn": urn, "version": os.environ.get("LINKEDIN_API_VERSION", DEFAULT_VERSION)}

    published = 0
    for p in files:
        try:
            result = publish_file(p, args, env, now)
        except ValueError as e:
            print(json.dumps({"file": p, "error": str(e)}))
            sys.exit(2)
        except TokenRejected as e:
            print(json.dumps({"file": p, "error": "token rejected (401); re-run linkedin_auth.py", "detail": str(e)[:300]}))
            sys.exit(4)
        except ApiError as e:
            print(json.dumps({"file": p, "error": str(e), "where": e.where, "status": e.status}))
            sys.exit(3)
        if warn_days is not None and warn_days <= 10:
            result.setdefault("warnings", []).append(f"access token expires in {warn_days} days; re-run linkedin_auth.py")
        print(json.dumps(result, ensure_ascii=False))
        if "post_urn" in result:
            published += 1
        if args.file and not args.publish_due:
            break
    if not args.dry_run and not args.file and published == 0:
        sys.exit(5)


if __name__ == "__main__":
    main()
