# Blog same-day part 2 (Sun + Wed, 17:30 UTC)

Routine `trig_01JAg1WjcaSPVHSdiuz5RMxA`. Paste everything below the line.

---

Same-day blog job for Naren (cgnarendiran). Some queue rows are the second half of a two-parter that must go out on the same day as the first half. The regular blog job writes one post per run at 16:15 UTC, so this job, an hour and a quarter later, writes the second half. On most days there is nothing to do and the run ends within a minute. Work autonomously; nobody is watching. Do not ask clarifying questions and do not wait for approval.

You have a checkout of https://github.com/cgnarendiran/cgnarendiran.github.io and GitHub access through the environment's connection.

## 1. Is there a same-day row?

`git fetch origin && git checkout -B work origin/master`. Let TODAY be `date -u +%Y-%m-%d`.

A same-day row is a Queue row in `.claude/blog-topic-queue.md` whose `Series` column contains `Same day as` followed by a slug in backticks, the part-1 slug.

Walk the Queue table top to bottom and take the first row whose `Post file` slug does not already appear in `_posts/`, exactly as the blog job does. Then:

- If that row is a same-day row, it is the row. Go to step 2.
- If it is not, but the row directly below it is a same-day row whose part-1 slug is this row's slug, then part 1 is probably still being written by the regular blog job. The row below is the row. Go to step 2.
- Otherwise end the run with the one-line report "no same-day post today". Create nothing.

## 2. Wait for part 1

Part 1 must be merged and dated today: `_posts/TODAY-<part-1 slug>.md` exists on `origin/master`. If it does not exist yet, re-run `git fetch origin` and check again every 5 minutes, for up to 90 minutes. If it still does not exist, create nothing and end with a report that says part 1 did not publish today. Both parts then wait: the next regular run writes part 1, and this job writes part 2 that evening.

If part 1 exists but with a different date, it went out on an earlier day and part 2 missed it. Create nothing and report it; Naren decides.

## 3. Write part 2

Read `.claude/routine-prompts/blog-post.md` on `origin/master` and follow everything below its first `---` line to write, check, PR and merge this row. If that file is missing, create nothing and report it. These overrides win over that file:

- **Topic.** The row from step 1 is the topic. Do not walk the queue again.
- **Date.** Use a front-matter `date: TODAY 12:00:00` and the filename `_posts/TODAY-<slug>.md`. The noon time matters: when two posts share a date, Jekyll orders them by filename, and part 1 would then list above part 2 on `/blog/`. Ignore the `Date` column.
- **Part 1.** Part 1 was published earlier today. It counts as one of the last three posts, so §0(b) applies to it: part 2 gets its own conceit, per the style guide. Cross-link part 1 with `/blog/<part-1 slug>/`, and pick up what its cliffhanger promised.
- **Number.** Take the next free `images/blogN/` after part 1's.

## 4. Report

Say which branch of step 1 or 2 ended the run. If you wrote the post, give the full report that `blog-post.md` asks for.
