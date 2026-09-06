# LinkedIn API setup for the publisher

This replaces Postbeam. The companion job writes each post to `.claude/linkedin-outbox/`, and
the publisher job posts every due file through LinkedIn's own Posts API. No third-party tool,
no subscription. The cost is one browser login every 60 days.

## One-time, on your laptop

1. **Create the app** at https://www.linkedin.com/developers/apps. It must be tied to a LinkedIn
   Page you administer: the Fast Code AI page if you are an admin there, otherwise create a Page
   for yourself. Any logo will do. Then under the app's Settings, press Verify next to the Page
   and complete the link as the Page admin.
2. **Add two products** under Products: "Share on LinkedIn" (grants `w_member_social`, the right
   to post as you) and "Sign In with LinkedIn using OpenID Connect" (grants `openid profile`,
   needed once to read your member id). Both are self-serve.
3. **Auth tab.** Add `http://localhost:8765/callback` under Authorized redirect URLs. Note the
   Client ID and the Primary Client Secret.
4. **Get a token.** From the repo root:

       LINKEDIN_CLIENT_ID=... LINKEDIN_CLIENT_SECRET=... \
         python3 .claude/scripts/linkedin_auth.py --write-env .claude/linkedin.env

   A browser tab opens, you approve, and the script prints three variables and writes them to
   `.claude/linkedin.env`, which is gitignored. The token lasts 60 days.
5. **Test with the JEPA post.** Validate, then publish for real if you want it out now:

       python3 .claude/scripts/linkedin_publish.py --env-file .claude/linkedin.env \
         --file .claude/linkedin-outbox/jepa-nobody-cares-about-the-wallpaper.md --dry-run

       python3 .claude/scripts/linkedin_publish.py --env-file .claude/linkedin.env \
         --file .claude/linkedin-outbox/jepa-nobody-cares-about-the-wallpaper.md \
         --force --ledger .claude/linkedin-ledger.md

   The second command posts to LinkedIn with the cover image, appends the ledger row, and
   deletes the outbox file. Commit and push what changed.

## Cloud environment for the publisher routine

1. At https://claude.ai/code, under environments, create one named `linkedin-publisher`.
   Keep the default environment for the blog job untouched; its Trusted network setting is what
   lets the blog job reach arXiv.
2. Network access: **Custom**, with two lines in Allowed domains: `api.linkedin.com` and
   `www.linkedin.com`. GitHub traffic takes its own proxy and needs no entry. Leave the
   package-manager checkbox off; the script is stdlib only. The Trusted default blocks LinkedIn.
3. Environment variables, `.env` format, one per line: `LINKEDIN_ACCESS_TOKEN`,
   `LINKEDIN_PERSON_URN`, `LINKEDIN_TOKEN_EXPIRES`, with the values from step 4 above. Any
   session in this environment can read them, which is why the publisher gets its own
   environment. Pro and Max also offer API credentials that the agent proxy attaches without the
   session seeing the key; the script would need to stop sending its own Authorization header for
   that, so treat it as a later hardening step, after the first cloud run works.
4. Open the LinkedIn publisher routine at https://claude.ai/code/routines, pick this environment
   in its environment selector, and enable it.

## Every 60 days

Re-run step 4 and update the three variables in the environment. The publisher warns in its
report when fewer than 10 days remain and stops with exit code 4 once the token is rejected.
Outbox files wait until the token is refreshed; nothing is lost.

## Timing

- The companion job fires at 17:15 UTC on blog days (retry 18:15), about half an hour after the
  post is live, and commits `.claude/linkedin-outbox/<slug>.md` with `publish_after` set to its
  run time plus `publish_delay_minutes` (30).
- The publisher fires daily at 16:00, 18:00 and 19:00 UTC and posts every file whose time has
  passed, so the LinkedIn post lands the same day. There is no day-long review window, by
  Naren's choice; the window is the gap to the next publisher fire.
- To change a post, edit the file on master before then. To veto it, delete the file and add a
  ledger row for the slug with the note `skipped`, so the companion does not write it again.
- To change a post after it went out, put the new text in an outbox-format file and run
  `linkedin_publish.py --file <file> --update <post urn>`. Only the text changes; the image stays.

## Limits worth knowing

- LinkedIn allows 150 API requests per member per day. A post with an image is three.
- The body must be under 3,000 characters; the script refuses longer.
- An organization mention must match the Page's exact name. `@[Fast Code AI](urn:li:organization:70969206)` is known to work.
- The script pins the API version header to 202608. LinkedIn sunsets each version after about a
  year, so set `LINKEDIN_API_VERSION` or bump the default before September 2027.
