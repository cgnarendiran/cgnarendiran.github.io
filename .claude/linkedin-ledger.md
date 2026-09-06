# LinkedIn post ledger

The LinkedIn job reads this file. It picks the **oldest** post in `_posts/` whose front-matter
date is on or after `eligible_from` and whose slug appears in neither table below, writes a
LinkedIn post for it following `.claude/linkedin-style-guide.md`, schedules it through Postbeam,
and appends a row to the "Posted by the job" table in the same run. One post per run.

Settings, one per line, parsed as `key: value`:

eligible_from: 2026-06-15
publish_time_local: 08:30
publish_tz: America/Los_Angeles
publish_days: Mon Tue Wed Thu Fri

`eligible_from` is what keeps the job from working through the whole archive. Set it to
`2017-01-01` to backfill everything not listed below, one post per run, oldest first.

`publish_time_local` and `publish_days`: the job schedules the post for the next listed day
strictly after the run, at that local time. The Sunday run lands on Monday morning and the
Wednesday run on Thursday morning, which leaves a window to edit or delete the post in Postbeam
before it goes out. Naren's hand-posted promos went out between 03:00 and 14:00 UTC, so an
earlier local time is also reasonable; this is the one line to change.

The slug is the part of the filename after the date: `_posts/YYYY-MM-DD-<slug>.md`. Exact match,
not substring.

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

| Slug | Blog date | Postbeam post id | Scheduled for | Run date (UTC) | Notes |
|---|---|---|---|---|---|
