#!/usr/bin/env python3
"""One-time, local OAuth helper for the LinkedIn publisher.

Gets a 60-day access token with the w_member_social scope and the member URN the
publisher posts as. Run it on your laptop, never in the cloud.

Prerequisites (see .claude/linkedin-api-setup.md):
  - a LinkedIn developer app with the products "Share on LinkedIn" and
    "Sign In with LinkedIn using OpenID Connect" added
  - http://localhost:8765/callback registered as an authorized redirect URL

Usage:
  LINKEDIN_CLIENT_ID=... LINKEDIN_CLIENT_SECRET=... \
    python3 .claude/scripts/linkedin_auth.py [--port 8765] [--write-env .claude/linkedin.env]

Prints three lines to stdout:
  LINKEDIN_ACCESS_TOKEN=...
  LINKEDIN_PERSON_URN=urn:li:person:...
  LINKEDIN_TOKEN_EXPIRES=YYYY-MM-DD
Copy them into the publisher's cloud environment. Re-run before the expiry date.
"""
import argparse
import datetime as dt
import http.server
import json
import os
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser


# python.org builds of Python on macOS ship without system CA certificates, so HTTPS fails
# with CERTIFICATE_VERIFY_FAILED. If certifi is importable, use its bundle. Harmless elsewhere.
if not os.environ.get("SSL_CERT_FILE"):
    try:
        import certifi
        os.environ["SSL_CERT_FILE"] = certifi.where()
    except ImportError:
        pass

AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
SCOPES = "openid profile w_member_social"


def post_form(url, fields):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{url} returned {e.code}: {e.read().decode('utf-8', 'replace')}")


def get_json(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{url} returned {e.code}: {e.read().decode('utf-8', 'replace')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--write-env", help="also write the three variables to this file (mode 0600)")
    ap.add_argument("--no-browser", action="store_true", help="print the URL instead of opening a browser")
    args = ap.parse_args()

    client_id = os.environ.get("LINKEDIN_CLIENT_ID")
    client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit("Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in the environment. Never commit them.")

    redirect_uri = f"http://localhost:{args.port}/callback"
    state = secrets.token_urlsafe(16)
    auth_url = AUTH_URL + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": SCOPES,
    })

    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/callback":
                self.send_error(404)
                return
            result.update(dict(urllib.parse.parse_qsl(parsed.query)))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h2>LinkedIn authorisation received. You can close this tab.</h2>")

        def log_message(self, *a):
            pass

    server = http.server.HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Redirect URL registered in the app must be exactly: {redirect_uri}", file=sys.stderr)
    print("If the browser does not open, paste this URL into it:\n" + auth_url + "\n", file=sys.stderr)
    if not args.no_browser:
        webbrowser.open(auth_url)
    while "code" not in result and "error" not in result:
        server.handle_request()
    server.server_close()

    if result.get("state") != state:
        sys.exit("OAuth state mismatch; run again.")
    if "error" in result:
        sys.exit(f"LinkedIn returned {result['error']}: {result.get('error_description', '')}")

    token = post_form(TOKEN_URL, {
        "grant_type": "authorization_code",
        "code": result["code"],
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    })
    access_token = token["access_token"]
    expires_in = int(token.get("expires_in", 60 * 24 * 3600))
    expires_on = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=expires_in)).date()

    info = get_json(USERINFO_URL, access_token)
    person_urn = f"urn:li:person:{info['sub']}"

    lines = [
        f"LINKEDIN_ACCESS_TOKEN={access_token}",
        f"LINKEDIN_PERSON_URN={person_urn}",
        f"LINKEDIN_TOKEN_EXPIRES={expires_on.isoformat()}",
    ]
    if args.write_env:
        with open(args.write_env, "w") as f:
            f.write("\n".join(lines) + "\n")
        os.chmod(args.write_env, 0o600)
        print(f"Wrote {args.write_env} (mode 600). It is gitignored; keep it that way.", file=sys.stderr)
    print(f"# authorised as {info.get('name', '?')}; scopes: {token.get('scope', '?')}; token expires {expires_on}", file=sys.stderr)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
