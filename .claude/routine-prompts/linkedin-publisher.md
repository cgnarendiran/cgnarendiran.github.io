# LinkedIn publisher → LinkedIn API

Routine `trig_013YoNfh6xBXzccn4cK863gW`. Paste everything below the line.

---

LinkedIn publisher job for Naren (cgnarendiran). Post every due file in the repo's LinkedIn outbox to LinkedIn through LinkedIn's Posts API, record each in the ledger, and land that change through a PR you MERGE YOURSELF. Before anything goes out, check each due post against the LinkedIn guide's plain-language rules and hold any that fail. Work autonomously; nobody is watching. Do not ask clarifying questions and do not wait for approval.

You have a checkout of https://github.com/cgnarendiran/cgnarendiran.github.io and GitHub access through the environment's connection. The environment provides `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_URN` as environment variables, and optionally `LINKEDIN_TOKEN_EXPIRES` and `LINKEDIN_API_VERSION`. NEVER print, echo, log, paste, or commit the token. It must not appear in the PR, in a commit, or in your report.

Environment facts: the Edit and Write tools raise a permission prompt for any path under `.claude/`, and nobody is there to answer it. Do not use Edit or Write in this job at all; the script changes the ledger itself and you only run git. The egress proxy blocks cgnarendiran.github.io, which does not matter here: the cover image comes from the checkout.

Never push to `master`. Branch, PR, merge. Before branching, `git fetch origin` and work from `origin/master`. The only changes allowed are the ones the script makes: `.claude/linkedin-ledger.md` modified and `.claude/linkedin-outbox/*.md` deleted. You never edit or rewrite a post. If `git rebase` or `git merge` fails with a stash error, retry with `-c merge.autoStash=false`.

## 1. Preflight

`git fetch origin && git checkout -B work origin/master`.

Check the variables exist without printing them: `test -n "$LINKEDIN_ACCESS_TOKEN" && test -n "$LINKEDIN_PERSON_URN" && echo configured`. If that does not print `configured`, end the run with the one-line report "publisher not configured: set the variables per .claude/linkedin-api-setup.md". Do nothing else.

Read `.claude/linkedin-api-setup.md`, the docstring at the top of `.claude/scripts/linkedin_publish.py`, and `.claude/linkedin-style-guide.md` §0 and §13.

## 2. What is due

    python3 .claude/scripts/linkedin_publish.py --dir .claude/linkedin-outbox --list-due --ledger .claude/linkedin-ledger.md

Exit 5: nothing is due. End with a one-line report. Exit 2: an outbox file is malformed. Report the error it printed, publish nothing, end. Exit 0: the printed files are due; continue.

## 3. Check each due post (LinkedIn guide §13)

For each due file, in turn:

1. `python3 .claude/scripts/prose_lint.py --linkedin <file>` must exit 0. It fails on three or more ML jargon terms, colon labels, negation triplets and fragment runs.
2. The cold-reader test. Launch a FRESH subagent with the Agent tool for each file. Give it ONLY the post body (no front matter, no hashtag or mention lines, no title, no blog) and the brief in LinkedIn guide §13.2, verbatim. The file passes only if the subagent's one-sentence summary is a fair summary of the post, it lists no word it did not understand, it lists nothing that refers to something it was not told, and it says yes to stopping at the first line. If no subagent tool exists, answer the five questions yourself in writing as that reader.

A file that passes both is cleared. A file that fails either is HELD: do not publish it, do not edit it, do not delete it. It stays in the outbox, still due, and every later run checks it again until Naren fixes or deletes it.

## 4. Publish

Branch `linkedin/publish-$(date -u +%Y-%m-%d)` off `origin/master`.

If every due file was cleared, run, exactly once:

    python3 .claude/scripts/linkedin_publish.py --dir .claude/linkedin-outbox --publish-due --ledger .claude/linkedin-ledger.md

If any file was held, do NOT run `--publish-due` (it would post the held file too). Instead run, once per cleared file, oldest `publish_after` first:

    python3 .claude/scripts/linkedin_publish.py --file .claude/linkedin-outbox/<slug>.md --ledger .claude/linkedin-ledger.md

Without `--force` it refuses a file whose `publish_after` is still in the future, which is correct.

The script uploads the cover image from the checkout, creates the post, appends a ledger row, deletes the outbox file, and prints one JSON line per file. Read every line. Exit codes: 0, published; 3, an API error (stop; keep what succeeded); 4, LinkedIn rejected the token (stop; Naren must re-run `linkedin_auth.py` and update the environment; the remaining files wait for the next run); 5, nothing was published.

Never publish the same file twice, never pass `--force`, and never publish a held file.

## 5. Commit what changed

If nothing was published (everything held, or nothing cleared), commit nothing, open no PR, and go to the report.

Otherwise, `git status --short` must show only `.claude/linkedin-ledger.md` modified and zero or more `.claude/linkedin-outbox/*.md` deleted. If anything else changed, do not commit; report it. Otherwise:

    git add -A .claude/linkedin-ledger.md .claude/linkedin-outbox

Commit as `linkedin: publish <slug>` (comma-separate several slugs). Push and open a PR against `master` with `gh pr create` (or the GitHub MCP tools if `gh` is missing). PR body: per post, the slug, the post URN, the post URL and the published time; the lint output and the cold-reader answers for each; each held file and why it was held; the token-expiry warning if the script printed one; the script's exit codes. Self-check the diff (only the ledger and outbox deletions), then squash-merge and delete the branch.

If the script exited 3 or 4 after at least one success, still commit and merge the rows for the successes. If a post went out but the PR cannot merge, leave it open and say so loudly in the report: the post is live and the ledger row is on the branch.

## 6. Report

First line: how many posts went out and how many were held, or why none did. Then per published post: slug, URN, URL. Then, per HELD post, loudly: the slug, which check failed, the lint errors or the cold-reader's answers, and that it stays in the outbox until Naren rewrites or deletes `.claude/linkedin-outbox/<slug>.md` on master. Then: the token-expiry warning if any; the exit codes; the PR URL and whether it merged; anything Naren must do himself (re-authorise, fix a held or malformed file, merge a stuck PR).
