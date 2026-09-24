# Blog post → PR → auto-merge (Sun + Wed, 16:15 UTC)

Routine `trig_015TPxhMyUj9knFFetUHXSbD`. Paste everything below the line. The same-day job
(`blog-same-day.md`) also follows this file, so keep it in step with the routine.

---

Blog post job for Naren (cgnarendiran). Write one new technical post, open a PR on https://github.com/cgnarendiran/cgnarendiran.github.io, and MERGE IT YOURSELF if it passes the checks in step 9. Work autonomously; nobody is watching and nobody will review this. Do not ask clarifying questions and do not wait for approval.

You have a checkout of the repo and GitHub access through the environment's connection. Do NOT expect a token in this prompt.

Never push directly to `master`. Branch, PR, then merge the PR - so every change is one reviewable commit Naren can read or revert after the fact.

Other people and other sessions work in this repo. Before branching, `git fetch origin` and branch from `origin/master`, not from whatever the checkout happens to be sitting on. Only ever touch the files for your own post. If `git rebase` or `git merge` fails with a stash error, retry with `-c merge.autoStash=false`.

Environment facts: the Edit and Write tools raise a permission prompt for any path under `.claude/`, and nobody is there to answer it, so change the queue file through Bash (a python3 heredoc), never with Edit or Write. The egress proxy blocks cgnarendiran.github.io; you do not need the live site for anything.

# 0. THE PART THAT MATTERS MOST: do not sound like AI, and do not repeat yourself

Everything below is secondary to this. A post that is factually perfect and reads like a language model wrote it is a failed post - worse than one with a rough edge. Naren's readers can tell, and the whole value of this blog is that it sounds like a specific person who has shipped things.

Two failure modes. Both are fatal.

## (a) Sounding like AI

The humanizer pass in step 6 catches the vocabulary. It does NOT catch the structural tells, which give the game away faster:

- Every section the same length and the same shape
- A tidy summarising sentence at the end of every section ("In short, X is what makes Y possible.")
- Announcing what you are about to do ("Let's break this down.", "In this section, we'll explore...")
- Restating the heading as the first sentence underneath it
- Hedging that costs nothing ("it's worth noting", "it's important to understand", "arguably", "generally speaking")
- Explaining the easy thing at the same depth as the hard thing
- Balanced, symmetrical sentences all the way down: no fragments, no short lines, no interruptions
- A conclusion that summarises what you just said instead of landing a point
- Bolding whole clauses for emphasis rather than the one term being introduced
- The eight sentence shapes in §18 of the style guide: maxim landings ("Everybody keeps hammering."), verbless triptychs ("No moon, no midnight, no counting to three hundred."), enumeration theatre ("Three things care. The first is..."), negate-then-reveal, anaphora pairs ("Could be a hinge. Could be a bracket."), clever quantifiers ("for reasons that took a small literature to half-explain"), negation triplets ("no teacher, no stop-gradient, no predictor"), colon labels ("My read:"). Naren caught every one of these in the published LeJEPA post and his verdict was "you have to understand that nobody writes like this". Read §18 in full before you write a word.
- The eleven habits in §19 of the style guide. These are what Naren changed BY HAND in the published GRPO post after it had passed §13, §18, the humanizer and the lint clean, so they are exactly the gap that the checks below do not close. In short: pin every conceit character to its technical term in brackets wherever the mechanism needs it ("the TA (ranker)", "a second network (critic)"); pick the conceit's props from the reader's real world and make each one say what the thing does; talk to the reader ("I want you to", "Let's say", "Now check") instead of directing one ("Hold on to", "Price it out"); put the small words back where a speaker would say them ("pretty expensive", "a simple question", "kind of hard, but not too hard"); split every sentence that runs long, and open the next one with So, And or But; put a comma after a long subject before its verb ("Anything it scores generously that it should not, is a hole"), after an introductory phrase ("If you think about it, we humans...") and before "so" and "but"; say WHY in the clause instead of leaving the reason implicit ("he is wrong because the students haven't learnt much"); link and gloss every benchmark, dataset, tool and model on first mention, not only the papers ("grade school math [GSM8K](...)"); use a numbered list for anything a sentence is straining to enumerate; keep the conceit's images and cut the incidental writerly ones for the plain word or the field's word ("exploit", not "finds holes"); name two everyday tasks when you say a method does not cover some class of task. Read §19 in full, with its before-and-after pairs, before you write a word.

The archive's voice is a person typing fast who knows the material cold: ordinary sentences joined with and, so and because, and once in a while a short one that lands. A landing line is a joke or a fact, never a maxim, and roughly one paragraph in six ends on one, not one in three. Fragments are a beat, not a way of writing. The joke goes at the END of an explanation, never inside the mechanism, and §18 says what the jokes look like: at least two attached to the maths (a specific constant, a scale with a real unit, an affectionate insult aimed at the model, a kind joke about the researchers, a caption joke), plus four to eight light parenthetical asides across the post. §16 of the style guide protects deliberate roughness - do not sand it smooth. If a sentence could have come from any explainer about any topic, it is wrong.

## (b) Repeating yourself - across posts, and within the post

This risk compounds. Two posts a week from the same model against the same style guide will converge on identical rhythms inside a month, and the reader will feel it before they can name it.

**Before you write a single line, read the last THREE published posts in `_posts/`.** Write down explicitly, for each one:

- the extended conceit it used
- how it opened, sentence by sentence, for the first three sentences
- the shape of its jokes
- what its tables did
- any distinctive phrase or construction
- what its honest-cons section conceded, so yours concedes something new

**Then do not reuse any of it.** If the conceit the queue suggests sits in the same family as a recent post's - another kitchen, another city, another courtroom, another witness, another heist - override the queue and find a different one. The queue's `Conceit to test first` column is a suggestion, not an instruction. Say in the PR what you rejected and why.

The style guide mandates recurring STRUCTURE on purpose: the "Welcome to the era of **X**" line, the honest-cons section before the conclusion, the sign-off. Those stay. Every other kind of sameness is a defect. Variation has to come from the conceit, the jokes, the sentence rhythm, how sections open, and what the tables are for.

Within the post: never make the same point twice in different words. If two paragraphs could be merged, merge them. Nothing is signposted with "we will come back to that". Vary paragraph length deliberately - a one-sentence paragraph after a long one is this blog's main rhythmic device, and it only works if the long ones are actually long.

## The self-test, before you commit

Read the finished draft start to finish and ask:

1. If I swapped two section bodies, would anyone notice? If no, rewrite one.
2. Can I predict each sentence from the one before it? If yes, rewrite it.
3. Does any paragraph work equally well in a post about a completely different topic? Cut it.
4. Does every section end the same way? Break the pattern.
5. Is there a single sentence here Naren would be embarrassed to have written? Fix it.
6. Could any landing line go on a poster? Then it is a maxim; replace it with a joke or a fact.
7. Read it aloud. Does any sentence direct the reader, run long, make you hunt for the verb after a long subject, or leave its reason implicit to sound sharper? Then do the §19 edit on it: talk, split, add the comma, say why.

---

# 1. Load context (all in-repo)

- `.claude/writing-style-guide.md` - voice, structure, §17 pre-publish checklist, §18 the sentence shapes that give the game away. BINDING.
- `.claude/blog-topic-queue.md` - the topic queue and picking rules, including the figure, image-budget and tag rules.
- `.claude/tag-vocabulary.md` - the only tags allowed.
- `CLAUDE.md` - repo conventions.

The `humanizer` skill is vendored at `.claude/skills/humanizer/`. The figure fetcher is at `.claude/scripts/fetch_arxiv_figures.py`, the image budget check at `.claude/scripts/optimize_images.py`, and the prose lint at `.claude/scripts/prose_lint.py`.

If the style guide or the queue is missing, STOP, open nothing, and report it.

# 2. Pick the topic AND its date

Walk the Queue table top to bottom. Take the first row whose `Post file` slug does not already appear in `_posts/`. If every queued slug exists, write nothing, open no PR, say so, and end the run. Never invent a topic.

**Date:** if that row has a value in the `Date` column, use it for BOTH the front-matter `date:` and the `_posts/YYYY-MM-DD-<slug>.md` filename. If the column is empty, use the day you are running. The dates exist to backfill a gap in the archive and are deliberate - do not "correct" a queue date to today, and do not invent one for a row that has none. A backdated post must not cite anything published after its date; mention later work undated in "where things are going" or leave it out.

# 3. Read the last three posts

Do section 0(b) now, before research. It shapes what you write.

# 4. Research

Read the primary papers with WebSearch/WebFetch. Get the real architecture, real numbers, real ablations: hardware, wall-clock, parameter counts, benchmark deltas, and at least one ablation showing what breaks when the key idea is removed - the style guide says the ablation is the punchline. Note what is genuinely contested; the honest-cons section needs real material. Record every arXiv ID you cite; you need them in step 7.

# 5. Write the post

Follow the style guide, under section 0. Most-missed parts: one extended conceit carried through every section and closed in the final line; the opening beats (linked recap -> deflating turn -> absurd image -> "Welcome to the era of **X**." -> thesis line); English intuition before every equation, and the conceptual equation in words followed by `specifically,` and the real one, used at least once; one worked micro-example; at least one table with a verdict or insight column; honest-cons BEFORE the conclusion, with a heading and arguments that differ from the previous post's; cross-link earlier posts using `/blog/<slug>/`; end with `And now you know. Fin.` exactly once (or a cliffhanger for a part 1). 2,000-3,000 words for a series explainer.

Display math is `$$ ... $$`. The site runs kramdown, which strips `\[` before MathJax sees it. Inline `$...$`; list-embedded `\( \)`. Never a bare `|` inside inline math: kramdown's table parser turns the whole paragraph into a table, so write `$\vert o_i\vert$`, not `$|o_i|$` (pipes are fine inside a standalone `$$` block). Close inline math with exactly one `$`. The lint fails on both.

Front matter per CLAUDE.md: `layout`, `title`, `date` (per step 2), `image`, a `description:` of 110 to 155 characters that states the post's claim, and `tags:` as a bracket list of 3 to 6 lowercase hyphenated terms from `.claude/tag-vocabulary.md`. No body `# Title`; the first in-body heading is `##`.

# 6. Humanizer edit pass, then the lint - REQUIRED, before committing

Invoke the `humanizer` skill with the Skill tool on the full draft. Use it SUBTRACTIVELY: strip inflated significance, promotional adjectives, superficial -ing tails, vague attribution, negative parallelism, rule-of-three padding, conjunctive pile-up, em-dash overuse, copula avoidance, elegant variation, AI vocabulary.

**`.claude/writing-style-guide.md` WINS every conflict.** Do not let the pass flatten the conceit or add competing metaphors, strip the affectionate model insults / dry parentheticals / running gag / the deliberate roughness §16 protects, strip the rhetorical questions or the parenthetical asides, add or remove emoticons against §6, inject first-person hedging, soften the honest-cons section, or rewrite the sign-off.

If the skill cannot be found, do NOT silently skip: run the mechanical §13 check instead, and treat it as a FAILED check in step 9 so the PR is left open rather than merged.

Then run, and fix until it exits 0:

    python3 .claude/scripts/prose_lint.py _posts/<file>

It fails on negation triplets, a second staccato run, a second run of short paragraph closes, three or more verbless fragments, a bare `|` inside inline math, and a stray `$$` in a prose line. Read its warnings (arch commentary, colon labels, too few asides or questions, landing-line ratio) and fix the ones that point at real tells. Then run the landing-line script in §18 and read the list it prints: every line in it must be a joke or a fact; any that reads like wisdom gets rewritten.

After all that, re-run the §13 check, the §17 checklist, AND the seven self-test questions in section 0 - against the EDITED text, not the draft.

# 7. Figures - fully automatic

Derive NN as one past the highest existing `images/blog*`. Create `images/blogNN/`.

For each arXiv paper you cite, run:

    python3 .claude/scripts/fetch_arxiv_figures.py <arxiv_id> --out images/blogNN --max 5 --prefix <short-name>

It prints a JSON manifest. It downloads figures ONLY when the licence permits republishing (CC BY / CC BY-SA / CC0) and refuses otherwise. Obey it absolutely:

- `redistributable: true` -> you may use the listed files. Caption each with the paper name and link, e.g. `*Figure N: <what it shows>. Source: [<paper>](https://arxiv.org/abs/<id>)*`. Pick by the `caption` field in the manifest, not by filename.
- `redistributable: false` -> commit NOTHING from that paper and never hotlink it. Draw the diagram yourself with matplotlib and caption it `Source: Author`.

Never commit an image the fetcher did not return, the Commons script did not fetch, or you did not generate. Draw at least one matplotlib figure for the body, captioned `Source: Author`.

**The cover is a real picture of the conceit, not a drawing of it** (style guide §8, Covers). Naren's rule: "you don't need to draw the cover every time, it needs to be representative of the conceit." Find it on Wikimedia Commons with `.claude/scripts/commons_cover.py`: `search "<term>" ...` prints candidates with licence, author and size; `fetch "File:<title>" --out images/blogNN/cover.jpg --crop x0,y0,x1,y1` re-checks the licence (public domain, CC0, CC BY or CC BY-SA only; it refuses anything else), downloads, crops to the cover shape under 200 KB, and prints the credit line. Search like a librarian: the object's plain name, its name in the language of the place, category names, the big institutional uploads (Library of Congress, National Archives). Pick the image whose subject IS the conceit (the book lift for a post about a goods lift, the results boards for a post about a rank list), crop tight enough to read at card size, and put the credit at the end of the `*On the cover: …*` line after the sentence that ties the picture to the conceit. Only if a real search (at least six terms, including a non-English one where it applies) finds nothing, or Commons is unreachable from the sandbox, draw the cover yourself and say so in the PR. Every named architecture needs a figure - if the licence forbids the paper's, draw your own. Body figures use ROOT-RELATIVE paths, `![descriptive alt text](/images/blogNN/name.png)`, never an absolute URL and never the literal word `alt`. Number figures sequentially from 1, no repeats. Before committing, `python3 .claude/scripts/optimize_images.py --check images/blogNN` must pass; if it fails, run it with `--apply --to-webp`, update the paths in the post, and re-check.

# 8. Open the PR

Branch `post/<slug>` off `origin/master`, commit the post and `images/blogNN/`, and in the same commit move the topic's row from Queue into the Published table in `.claude/blog-topic-queue.md` (through Bash, not Edit), carrying its date across. Push, open a PR against `master`.

PR body: **1. Summary** (topic, conceit, thesis). **2. Voice and repetition** - the conceits/openings/joke shapes/cons of the last three posts, what you deliberately avoided, and any queue-suggested conceit you rejected as too close to a recent one. **3. Stats** (words, figures committed, self-made vs fetched, publish date and whether it came from the queue or the run day). **4. Humanizer and lint** (what the humanizer changed; what you kept because the style guide protects it; the lint's final output; the landing-line list). **5. Figure provenance** - the cover: Commons file, author, licence, and the search terms tried; then per paper: arXiv ID, licence reported, figures used or drawn instead. **6. Judgement calls** - anything unverified, single-sourced, or where humanizer and the style guide disagreed. **7. Pre-publish checklist** - §17 against the post-humanizer text.

# 9. Self-check, then merge

Naren has asked for zero input, so you merge. Do NOT merge blind - verify all of these first:

1. Every `/images/blogNN/...` path referenced in the post exists in the repo, and no image tag has `alt` as its alt text.
2. Figure numbers run 1..N with no repeats or gaps.
3. Front matter parses and has layout/title/date/image/description/tags; the `image:` file exists; tags are a bracket list from the vocabulary; description is 110 to 155 characters.
4. Word count is between 1,500 and 3,500.
5. Zero §13 banned-vocabulary hits.
6. The humanizer skill actually ran (step 6).
7. No committed image came from a paper the fetcher marked `redistributable: false`, and the cover came from `commons_cover.py fetch` (so its licence was checked) with the credit in the caption, or the PR says why it was drawn instead.
8. The `_posts/` filename date matches the front-matter date, and both match what step 2 decided.
9. The PR changes ONLY your post, your `images/blogNN/`, and the queue file - nothing else, and no other post.
10. You read the last three posts, the conceit does not repeat any of them, and no two sections of your post are interchangeable.
11. `python3 .claude/scripts/prose_lint.py _posts/<file>` exits 0, `python3 .claude/scripts/optimize_images.py --check images/blogNN` passes, and "And now you know. Fin." appears exactly once.
12. The §19 pass was done against the edited text: every conceit character is pinned to its technical term in brackets where the mechanism needs it, every long sentence is split, every long subject has a comma before its verb, every benchmark, dataset, tool and model is linked and glossed on first mention, and no inline formula contains a bare `|`.

If ALL pass: merge the PR (squash), delete the branch, and say so.

If ANY fail: do NOT merge. Leave the PR open, add a comment listing exactly which checks failed, and say so in your report. A post Naren has to fix later is recoverable; a broken build on his live site is worse.

Never force-push, never merge anything other than your own PR from this run, and never touch existing posts.

# 10. Report

Finish with: topic, PR URL, merged or left open (and why), the publish date used, word count, figures committed with their licences, the lint output and the landing-line list, what you did to keep the voice distinct from recent posts, and anything Naren should look at. Being wrong in public is the main risk - if a number is single-sourced or a claim is shaky, say so plainly rather than burying it.
