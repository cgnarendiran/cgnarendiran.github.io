# LinkedIn post ledger

Two jobs share this file.

The **companion job** picks the oldest post in `_posts/` whose front-matter date is on or after
`eligible_from` and whose slug appears in neither table below nor in `.claude/linkedin-outbox/`,
writes a LinkedIn post for it following `.claude/linkedin-style-guide.md`, and commits it to
`.claude/linkedin-outbox/<slug>.md` with a `publish_after` time. One post per run.

The **publisher job** runs `.claude/scripts/linkedin_publish.py`, which posts every due outbox
file through LinkedIn's Posts API, appends a row to the "Posted by the job" table, and deletes
the outbox file. Setup and the review window are described in `.claude/linkedin-api-setup.md`.

Settings, one per line, parsed as `key: value`:

eligible_from: 2026-06-15
publish_delay_minutes: 30
publish_tz: America/Los_Angeles

`eligible_from` is what keeps the job from working through the whole archive. Set it to
`2017-01-01` to backfill everything not listed below, one post per run, oldest first.

`publish_delay_minutes`: the companion sets `publish_after` to its run time plus this many
minutes. Naren chose no review window (2026-09-06): the companion fires at 17:15 UTC on blog
days, about half an hour after the post is live, with a retry at 18:15, and the publisher fires
daily at 16:00, 18:00 and 19:00 UTC and posts anything whose time has passed. So a Sunday or
Wednesday post is on LinkedIn by 18:00 UTC the same day. To hold a post back, edit its
`publish_after` on master before the next publisher fire.

The slug is the part of the filename after the date: `_posts/YYYY-MM-DD-<slug>.md`. Exact match,
not substring. To skip a post for good, add a row for it below with the note `skipped`.

---

## Posted by hand, before the job existed

Naren wrote these himself. Listed so a backfill never re-posts them.

| Slug | Blog date | LinkedIn date |
|---|---|---|
| kv-caching-mla-is-attention-all-you-really-need | 2025-08-22 | 2025-09-19 |
| rope-is-attention-all-you-really-need | 2025-09-09 | 2025-10-20 |
| moe-is-attention-all-you-really-need | 2025-09-21 | 2025-12-09 |
| cross-entropy-loss | 2025-10-13 | 2025-12-19 |
| vit-pixels-to-tokens | 2025-11-08 | 2026-02-09 |
| vlm-pixels-to-tokens | 2025-12-09 | 2026-03-31 |
| vla-pixels-to-tokens | 2026-01-15 | 2026-05-14 |

---

## Posted by the job

The publisher appends rows here; keep this table last in the file.

| Slug | Blog date | Post id | Published (UTC) | Run date (UTC) | Notes |
|---|---|---|---|---|---|
| jepa-nobody-cares-about-the-wallpaper | 2026-06-15 | urn:li:share:7502284468947320832 | 2026-09-06T08:39Z | 2026-09-06 | blog-companion via LinkedIn API |
| lejepa | 2026-07-15 | urn:li:share:7502452735359909888 | 2026-09-06T19:48Z | 2026-09-06 | blog-companion via LinkedIn API |
| solving-chess-paths-nodes | 2026-09-07 | urn:li:share:7502931553073827840 | 2026-09-08T03:31Z | 2026-09-08 | manual via LinkedIn API |
| world-models-learned-simulators | 2026-09-09 | urn:li:share:7503513730584821761 | 2026-09-09T18:04Z | 2026-09-09 | blog-companion via LinkedIn API |
