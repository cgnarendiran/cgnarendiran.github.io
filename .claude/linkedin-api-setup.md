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
2. Network access: **Custom**, allowing `api.linkedin.com`, `www.linkedin.com`, `github.com`
   and `api.github.com`. The Trusted default blocks LinkedIn.
3. Environment variables: `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_URN`,
   `LINKEDIN_TOKEN_EXPIRES`, with the values from step 4 above. Use the credential store if the
   plan offers one.
4. Point the LinkedIn publisher routine at this environment and enable it.

## Every 60 days

Re-run step 4 and update the three variables in the environment. The publisher warns in its
report when fewer than 10 days remain and stops with exit code 4 once the token is rejected.
Outbox files wait until the token is refreshed; nothing is lost.

## The review window

- The companion job commits `.claude/linkedin-outbox/<slug>.md` with a `publish_after` time,
  the next weekday at the ledger's `publish_time_local`.
- The publisher runs on weekdays a few minutes after that time and posts every file whose time
  has passed.
- To change a post, edit the file on master before then. To veto it, delete the file and add a
  ledger row for the slug with the note `skipped`, so the companion does not write it again.

## Limits worth knowing

- LinkedIn allows 150 API requests per member per day. A post with an image is three.
- The body must be under 3,000 characters; the script refuses longer.
- An organization mention must match the Page's exact name. `@[Fast Code AI](urn:li:organization:70969206)` is known to work.
- The script pins the API version header to 202608. LinkedIn sunsets each version after about a
  year, so set `LINKEDIN_API_VERSION` or bump the default before September 2027.
