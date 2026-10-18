# LinkedIn post ledger

Two jobs share this file.

The **companion job** picks the newest post in `_posts/` whose front-matter date is on or after
`eligible_from` and whose slug appears in neither table below nor in `.claude/linkedin-outbox/`,
writes a LinkedIn post for it following `.claude/linkedin-style-guide.md`, and commits it to
`.claude/linkedin-outbox/<slug>.md` with a `publish_after` time. One post per run. If the post
still fails the cold-reader test after four rounds, it appends a `held` row for the slug here
instead, so the next run moves on to the next post rather than retrying this one forever.

The **publisher job** runs `.claude/scripts/linkedin_publish.py`, which posts every due outbox
file through LinkedIn's Posts API, appends a row to the "Posted by the job" table, and deletes
the outbox file. Setup and the review window are described in `.claude/linkedin-api-setup.md`.

Settings, one per line, parsed as `key: value`:

eligible_from: 2026-06-15
publish_delay_minutes: 30
publish_tz: America/Los_Angeles

`eligible_from` is what keeps the job from working through the whole archive. Set it to
`2017-01-01` to backfill everything not listed below, one post per run, newest first.

`publish_delay_minutes`: the companion sets `publish_after` to its run time plus this many
minutes. Naren chose no review window (2026-09-06): the companion fires at 17:15 UTC on blog
days, about half an hour after the post is live, with a retry at 18:15. Since 2026-09-13 the
publisher fires Monday to Friday at 03:30 and 04:30 UTC and posts anything whose time has
passed, so a Sunday or Wednesday post is on LinkedIn that evening, Pacific time. To hold a post
back, edit its `publish_after` on master before the next publisher fire.

The slug is the part of the filename after the date: `_posts/YYYY-MM-DD-<slug>.md`. Exact match,
not substring. To skip a post for good, add a row for it below with the note `skipped`.

A row whose note starts `held:` is the companion job giving up after four failed cold-reader
rounds (LinkedIn guide §13). The PR that added the row holds the last draft and the readers'
answers. To let the job try again, delete the row; to post it yourself, change the note.

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
| speculative-decoding | 2026-09-09 | urn:li:share:7503528834714103809 | 2026-09-09T19:04Z | 2026-09-09 | blog-companion via LinkedIn API |
| grpo-rlvr | 2026-09-13 | urn:li:share:7504963213017571329 | 2026-09-13T18:04Z | 2026-09-13 | blog-companion via LinkedIn API |
| quantization-edge-inference | 2026-09-16 | urn:li:share:7507643485982920704 | 2026-09-21T03:34Z | 2026-09-21 | blog-companion via LinkedIn API |
| knowledge-distillation | 2026-09-20 | - | - | 2026-09-23 | skipped: Naren vetoed it, Mamba part 1 goes out instead |
| mamba-is-attention-all-you-really-need | 2026-09-23 | urn:li:share:7508733025787224065 | 2026-09-24T03:44Z | 2026-09-24 | manual via LinkedIn API |
| mamba-is-attention-all-you-really-need-part2 | 2026-09-23 | - | - | 2026-09-26 | skipped: Naren doesn't want a second LinkedIn post on Mamba |
| jev-system-one-models-rlcd | 2026-09-25 | - | - | 2026-09-26 | posted by hand by Naren in the LinkedIn app, text written in session; post id not recorded |
| mcts-alphazero-part2 | 2026-09-27 | - | - | 2026-09-29 | skipped: Naren doesn't want a second LinkedIn post on MCTS |
| mcts-alphazero | 2026-09-27 | - | - | 2026-10-14 | skipped: failed the cold-reader test in all ten companion runs from 09-27 to 10-14 and blocked every newer post; Naren chose to skip it |
| voice-models-holding-a-conversation | 2026-10-11 | - | - | 2026-10-14 | skipped: Naren doesn't want a second LinkedIn post on voice models |
| llm-benchmarks-terminal-bench | 2026-09-30 | - | - | 2026-10-18 | held: failed the cold-reader test four rounds; the last draft is in the PR that added this row |
