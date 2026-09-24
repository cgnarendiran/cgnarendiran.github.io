# LinkedIn companion → outbox (Sun + Wed, 17:15 and 18:15 UTC)

Routine `trig_01QB94MCpCYwCoebXsH2Ttxo`. Paste everything below the line.

---

LinkedIn companion job for Naren (cgnarendiran). Write one LinkedIn post that promotes the oldest eligible entry on https://cgnarendiran.github.io that is not yet on LinkedIn, and commit it to the repo's outbox through a PR that you MERGE YOURSELF. A separate publisher job posts it to LinkedIn later; you never post anything. Work autonomously; nobody is watching and nobody will review this before it runs. Do not ask clarifying questions and do not wait for approval.

This job fires twice on blog days, 17:15 and 18:15 UTC, an hour and two hours after the blog job starts. The second fire is a retry: if the first already queued the post, the second finds the outbox file and ends.

You have a checkout of https://github.com/cgnarendiran/cgnarendiran.github.io and GitHub access through the environment's connection. Do NOT expect any token in this prompt.

Two facts about this environment:
- The egress proxy BLOCKS cgnarendiran.github.io. `curl` and WebFetch against the site fail with a proxy error. That is not evidence the post is missing; step 3 says how to check liveness.
- The Edit and Write tools raise a permission prompt for any path under `.claude/`, and nobody is there to answer it, so the run stalls. Create the outbox file ONLY through Bash (a heredoc), never with Edit or Write. Draft in the scratchpad directory with any tool.

Never push to `master`. Branch, PR, merge. Before branching, `git fetch origin` and work from `origin/master`, not from whatever the checkout is sitting on. The ONLY file you may add is `.claude/linkedin-outbox/<slug>.md`. Never touch the ledger, posts, images, the queue, or the style guides. If `git rebase` or `git merge` fails with a stash error, retry with `-c merge.autoStash=false`.

# 0. THE PART THAT MATTERS MOST: a standalone post for people with no ML background

Naren's verdict on the companion posts through September 2026: "complete bullshit". They lifted the blog's conceit, words and context into the post without the paragraphs that set them up, so a reader who never opens the link understood nothing. The LinkedIn guide's §0 is the fix, and it overrides every other rule in the guide and in this prompt:

- The post stands alone. Someone who has never seen the blog understands all of it on one read. Nothing refers to anything the post did not set up itself ("the booth", "the pad", "that gap", "part 2 picks up").
- ONE idea: one motivation or one problem from the blog, the one a normal person would find surprising or relatable. It is a trailer, not a summary. One mechanism at most, told in the words of an everyday picture.
- The reader works in marketing, law or medicine and has used ChatGPT. At most two technical terms in the whole post, each explained in everyday words. Model and product names are fine.
- A hook that would stop a non-technical person scrolling: a surprising true thing about something they already use, or a familiar everyday situation next to the AI problem. No paper names, acronyms or methods in the first line.
- Short sentences, about 20 words or fewer. Numbers only if a normal person can feel them. No equations, no benchmark percentages.
- 100 to 200 words, never above 250.

The §0.7 before-and-after (Mamba part 1) is the standard. Read it before you write.

## 1. Load context (all in-repo)

- `.claude/linkedin-style-guide.md`: BINDING. Read §0 first and in full, then §5 to §10 (voice, formatting, tail, truth rules, banned, media), §12 (checklist) and §13 (the checks). §2 and the §11 exemplars are older and written for ML readers; take only voice from them.
- `.claude/writing-style-guide.md` §5 (voice), §6 (humour), §13 (banned patterns): the voice. §0 of the LinkedIn guide wins on audience; the blog guide wins on voice; the LinkedIn guide wins on formatting.
- `.claude/linkedin-ledger.md`: the settings block and the two tables of posts already handled.
- `.claude/linkedin-outbox/`: posts written but not yet published.
- `.claude/scripts/linkedin_publish.py`: read its docstring for the outbox file format. Its `--dry-run` mode is one validator; `.claude/scripts/prose_lint.py --linkedin` is the other (it fails on 3+ jargon terms).
- `CLAUDE.md`: repo conventions.

The `humanizer` skill is vendored at `.claude/skills/humanizer/`.

If the LinkedIn guide has no "## 0." section, or the guide, the ledger, or the publish script is missing, STOP, create nothing, and report it.

## 2. Pick the post

`git fetch origin && git checkout -B work origin/master`, so you are reading what is actually published.

Parse the ledger's settings block: `eligible_from`, `publish_delay_minutes`, `publish_tz`. Then walk `_posts/YYYY-MM-DD-<slug>.md` oldest first and take the first file where (a) the front-matter `date` is on or after `eligible_from`, (b) `<slug>` appears in NEITHER ledger table, and (c) `.claude/linkedin-outbox/<slug>.md` does not exist. Exact slug match. Ignore `_posts/temp.md` and any file without a date-prefixed filename.

If nothing qualifies: create nothing, open no PR, say so in one line, and end the run. One post per run, never more.

## 3. Confirm it is deployed (through GitHub, not the site)

Find the commit that added the post file: `git log --diff-filter=A --format=%H origin/master -- _posts/<file>`. Then list the `pages build and deployment` workflow runs on `master`: `gh api 'repos/cgnarendiran/cgnarendiran.github.io/actions/runs?branch=master&per_page=10'`, or if `gh` is missing, the environment's GitHub MCP tool `mcp__github__actions_list` with method `list_workflow_runs`. Require a run with status `completed` and conclusion `success` whose `head_sha` is that commit or a descendant of it (`git merge-base --is-ancestor <post_commit> <head_sha>`).

If no such run exists, the post is not deployed yet: create nothing, report which commit is waiting, and end. The 18:15 fire, or the next blog day, will pick it up.

The canonical URL is `https://cgnarendiran.github.io/blog/<slug>/`.

## 4. Read the post, pick ONE idea, then write

Read the whole blog post. Then write down, before drafting: (a) the one problem or motivation you will use, in one sentence a non-technical friend would understand; (b) the everyday picture you will set up from zero to explain it (the blog's conceit if it works cold, otherwise a simpler one); (c) the one catch, in plain words, if it fits; (d) the front-matter `image:` path and the "On the cover" caption. Everything else in the blog stays in the blog.

Write the post to the §0.6 shape: hook, the problem in everyday terms, the everyday picture, the idea, the catch, then the §7 tail. Plain text only. Also binding:

- At least one question in the first half, answered at once.
- At least two first-person sentences about what Naren did or thinks ("I wrote about", "what I'm noticing"). Invented events and anecdotes stay banned.
- No colon-label openers ("My read:", "The catch:"), no negation triplets, no verbless fragment sentences, no more than two consecutive paragraphs ending on a fragment.
- The pointer line says in plain words what the reader will find. Then the canonical URL on its own line. 4 to 6 hashtags on one line, broad ones a general audience follows (#AI, #MachineLearning) plus one or two specific ones. Then the Fast Code AI mention on its own line in the exact form `@[Fast Code AI](urn:li:organization:70969206)`.

The §8 truth rules are absolute. Every claim comes from the blog post or the papers it cites, or is common knowledge about products the reader uses (ChatGPT is a Transformer-based chatbot). Simplifying must never make a claim false. No invented anecdotes, nothing about Fast Code AI's work, nothing about Naren's role or employer.

## 5. The checks, REQUIRED (LinkedIn guide §13)

1. Humanizer. Invoke the `humanizer` skill with the Skill tool on the draft. Use it SUBTRACTIVELY. The guides win every conflict: keep the everyday picture, the question, the first-person sentences, the one dry aside. Do not let it add hedging, a question to the audience as the last line, or rewrite the tail. If the skill cannot be found, run LinkedIn guide §9 and blog guide §13 by hand and say in the report that the skill did not run.

2. Cold-reader test. Launch a FRESH subagent with the Agent tool. Give it ONLY the post body (no title, no hashtags, no blog, no context about you or the blog) and the brief in LinkedIn guide §13.2, verbatim. The post passes only if its one-sentence summary matches your one idea, it lists no word it did not understand, it lists nothing that refers to something it was not told, and it says yes to stopping at the first line. If it fails, rewrite and run the test again with a NEW subagent (never reuse one that has seen an earlier draft). Up to four rounds. If no subagent tool exists, answer the five questions yourself in writing as that reader. If it still fails after four rounds, do not queue anything: end the run and report the last draft and the reader's answers.

3. The §12 checklist against the final text. Count words mechanically with `wc -w` on the body without the URL, hashtag and mention lines.

Keep drafts in the scratchpad directory, not in the repo.

## 6. Compute publish_after

Naren wants no review window. `publish_after` is the current time plus `publish_delay_minutes` from the ledger settings (use 30 if the key is missing), as an ISO-8601 timestamp WITH the `publish_tz` offset. Get it from the system: `TZ=America/Los_Angeles date -d '+30 minutes' +%Y-%m-%dT%H:%M:%S%:z`.

## 7. Write the outbox file (Bash only)

Branch `linkedin/<slug>` off `origin/master`. Create `.claude/linkedin-outbox/<slug>.md` with a Bash heredoc (`cat > path <<'EOF'`): a front-matter block between two `---` lines with the keys `slug`, `title`, `blog_date`, `image` (the post's front-matter `image:` path, e.g. `images/blog29/cover.jpg`), `alt` (the "On the cover" caption without the italics), `publish_after` (from step 6), `source: blog-companion`; then a blank line and the post body.

Validate it, both checks must pass:

    python3 .claude/scripts/linkedin_publish.py --file .claude/linkedin-outbox/<slug>.md --dry-run
    python3 .claude/scripts/prose_lint.py --linkedin .claude/linkedin-outbox/<slug>.md

The first must exit 0 with an EMPTY `warnings` list and `chars` under 1,700; check the `commentary` it prints: the mention as `@[Fast Code AI](urn:li:organization:70969206)`, each hashtag as `{hashtag|\#|Tag}`. The second must exit 0 (it fails on 3+ jargon terms, negation triplets, colon labels, a second fragment run) and should print no "jargon" or "long sentence" warnings; fix any it prints. Fix the file with Bash and re-run until both pass. If a fix changes more than a word or two, run the cold-reader test again.

## 8. Open the PR, self-check, merge

`git add` only that file. Commit as `linkedin: queue companion post for <slug>`. Push and open a PR against `master` with `gh pr create` (or the GitHub MCP tools if `gh` is missing).

PR body: the full post text exactly as written; the one idea you picked and what you left for the blog; `publish_after` in both `publish_tz` and UTC; the cold-reader subagent's answers from the final round (and how many rounds it took); the §12 checklist, ticked; what the humanizer pass changed; the lint output.

Self-check before merging, mechanically: the PR diff adds exactly ONE new file, under `.claude/linkedin-outbox/`, and changes nothing else; the lint exits 0; the cold-reader test passed. If so, merge the PR (squash) and delete the branch. If not, leave it open, comment why, and report.

Never force-push, never merge any PR other than your own from this run.

## 9. Report

Finish with: the slug and title; the one idea; the outbox path; `publish_after` in local time and UTC; the PR URL and whether it merged; the full text of the post; word and character counts; whether the humanizer skill ran; the cold-reader answers and round count; both validators' output.
