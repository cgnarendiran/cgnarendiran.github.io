# LinkedIn idea queue

Source for a second LinkedIn job, the **takes job**, which does not exist yet. The blog
companion job (see `.claude/linkedin-ledger.md`) promotes each new blog post. This queue holds
everything else: stories from Naren's own work, contrarian takes, second angles on posts already
in the archive, and stories from the public project pages.

**This repository is public.** Nothing goes in this file that could not appear in the post
itself: no client names, contract details, unpublished results, or specifics that identify an
account. Uncleared notes stay out of the repo. A private Notion page works for those, and a job
can read it through the Notion connector if that is ever wired up.

---

## What works and what doesn't

Judged on Naren's ten published LinkedIn posts and on the LinkedIn form, not on reach: Postbeam's
analytics have not synced for any post yet, so nothing here is ranked by numbers.

**Works**

- A moment with a concrete failure and a number. The ice cream line in the VLA promo is the model.
- A stance with a one-line test the reader can apply themselves. "Does it predict consequences?"
- A negative result, published as one. Almost nobody posts them, and the people who tried the
  same thing reply.
- A money claim with figures. The most reliable reason a technical post gets reshared.
- A second angle on a post already in the archive, with the link. Zero clearance, zero invention.

**Doesn't**

- A topic with no claim attached. "Os vs pathlib" is a heading; writing it produces a summary.
- Anything a man page answers. Tooling comparisons read like a content calendar.
- Anything that needs an equation, a figure, or 600+ words. That is a blog post, and the
  companion job promotes it once it exists.
- News reactions. They expire before the queue reaches them, and the generic version is exactly
  what Postbeam's own generator produced in the eleven drafts sitting in the account.
- A story the job would have to invent. First-person experience appears only when Naren has
  written the facts into the Notes cell.

---

## Triage of the old list

| Old idea | Verdict | Why |
|---|---|---|
| Vision LLM and DeepSeek OCR | Blog queue, then promo | Paper explainer. The real claim is optical context compression, and it needs figures |
| SSMs and Mamba, for speech | Already blog queue row 7 | Add the speech angle to that row's conceit: audio at sample rate is where quadratic attention breaks |
| Autoregressive models in CSM | Cut | No claim attached |
| Memory in LLMs, physics of LLMs | Blog queue | Allen-Zhu's series is a post with experiments, not a LinkedIn post |
| Counting tokens, the simple math | Take T9 | Back-of-envelope with real numbers. Also feeds blog row 10 |
| Reproducibility, Thinking Machines | Cut | News reaction, expired |
| Olympiad gold but fails basic math | Take T1 | Signature stance. Link the tokenizers post once it exists |
| Single shot vs multi shot | Hold | Only with a measured case where few-shot starts hurting |
| Rsync vs scp | Cut | Man page |
| Vector DB or flat search for small docs | Take T2 | A threshold and a cost. Links the HNSW post as the "when you do" |
| Paragraph-number referencing in summaries | Story S4 | Needs Notes. The legal research project page is public, so a genericised version is fine |
| Same model for document and query embeddings | Story S3 | Universal, zero clearance |
| Reranker: can a regular LLM do it? | Take T5 | Clear stance |
| Prompt caching saves money | Take T6 | Public list prices only |
| Os vs pathlib | Cut | Man page |
| Linters and formatters | Cut | Most commoditised genre on the platform |
| Google index, RAG all along? | Take T3 | Links the Markov / PageRank post |
| NMS as slow as template matching | Story S5 | Needs the numbers |
| Masked template matching doesn't work | Take T8 | Negative result, if Notes say what was tried |
| Lines, boxes, tables in dense diagrams | Story S6 | Three items, one story, only with Notes |
| Chat threads that work for you | Cut | No claim |
| When do we need a GNN (aircraft) | Story S7 | Anonymise the proposer and the domain |
| Why is RL underused | Take T7 | The reward is the product |
| Heart rate from video | Story S2 | The rPPG project page is public. Genericise the client |
| Face tracking and filters | Cut | Off-position |
| Vector vs raster, OCR vs extracting text | Take T4 | Clear stance, saves money |
| GIL removal | Take T10 | Links the pasta post |
| MoE, Mixtral, one million experts | Angle A6 | Second angle on the MoE post with the PEER paper |
| The ice cream result | Story S1 | Facts already public in the VLA post and its promo. Ready without Notes |

Already written, per the strikethroughs: RoPE, RSA, database vs files, LoRA, Elo, asyncio vs
threads, ANN search, snake vs camel, batch API, text in the DB, DFS vs BFS, KV caching. Several
of those get a second angle below.

---

## How the takes job reads this file

- Walks the four queue tables in order (Stories, Takes, Archive angles, Project stories) and
  takes the first row with Status `Ready`, except that it never posts two rows of the same Kind
  back to back. Check the last row of the Posted table.
- **Story rows** are written only when the Notes cell is filled in by Naren. The post uses
  nothing that is not in Notes or on the linked public page. Empty Notes means skip the row.
- **Take and Angle rows** are written from public sources and the linked blog post. Every number
  gets a source. First person is allowed only for opinion and for "I wrote about this in ...".
- **Project story rows** are written from the linked `_projects/` page only. Read the page first;
  if it has no concrete moment, mark the row `Thin` and move on.
- Publish time and zone come from the settings block in `.claude/linkedin-ledger.md`.
- After pushing to Postbeam, the row moves to Posted with the Postbeam id.

---

## Queue

### Stories

Kind = Story. Needs Notes. Clearance is set by Naren, not the job.

| # | Post | The moment | Clearance | Notes | Status |
|---|---|---|---|---|---|
| S1 | The bowl of ice cream | A driving VLA that never fails a road scene is shown a bowl of ice cream and says go forward. It was never looking at the road. Close on the general test: swap the input for something absurd and watch what the model does. | Public. Already in the VLA post and its May 2026 promo | Source: /blog/vla-pixels-to-tokens/. Add what was tried next if it can be said | Ready |
| S2 | Can a camera feel your pulse? | It can. The signal was never the hard part. A person who will not sit still was, and every month after the demo went into that. | Genericise the client. The rPPG project page is public | | Needs Notes |
| S3 | Two models, one retrieval system | Documents embedded with one model, queries with another. Weeks of "our RAG is bad" was a one-line fix. | Public | | Needs Notes |
| S4 | Paragraph 47 does not say that | Summaries were clean, cited, checkable, which is why nobody checked. Citations pointed at paragraphs that did not contain the claim. | Genericise. The legal research project page is public | | Needs Notes |
| S5 | The cleanup cost more than the work | NMS, the step nobody profiles because it is obviously cheap, cost as much as the matching it cleaned up after. | Public | Bring the real timings | Needs Notes |
| S6 | What worked on real engineering drawings | Lines, boxes and tables in dense diagrams, after the obvious approaches failed. | Genericise | | Needs Notes |
| S7 | The GNN nobody needed | Someone proposed a GNN and on paper it was right. Then you counted the nodes. | Anonymise the proposer and the domain | | Needs Notes |
| S8 | Losing the A100 | Downgraded to CPU mid-project. Half of what the GPU hid was work that was never needed. | Public | | Needs Notes |
| S9 | The test nobody passed | Benchmark results on driving models. | Hold until the paper is public | | Hold |

### Takes

Kind = Take. No personal facts needed.

| # | Post | The stance | Link | Status |
|---|---|---|---|---|
| T1 | Olympiad gold, arithmetic failure | Not the same capability. The benchmark that impresses you measures the wrong one. | tokenizers post, once written | Ready |
| T2 | You do not need a vector database yet | Under roughly ten thousand chunks, a flat array and cosine beats a vector DB on latency, cost and debuggability. Most RAG stacks are built for a scale the product never reaches. | /blog/hnsw-graph-based-vector-search/ | Ready |
| T3 | Google was doing RAG all along | Retrieve, rank, generate over top-k is PageRank with an LLM bolted on. Inverted indices still beat embeddings on precision. Hybrid is the default, not a compromise. | /blog/markov-chain-pagerank-and-perplexity/ | Ready |
| T4 | Stop running OCR on text you already have | Most pipelines rasterise a PDF that has a text layer, then pay a model to read the picture back. You lose structure, reading order and money. | | Ready |
| T5 | A reranker is not an LLM you were too lazy to call | Cross-encoders exist because joint pair scoring is a different computation. A general LLM gives worse calibration, unstable ordering, ten times the bill. | | Ready |
| T6 | Your inference bill is a design decision | Prompt caching and batch APIs change what you can afford to build at all. Public list prices only. | | Ready |
| T7 | RL is underused because the reward is the product | Most teams cannot specify what "good" means precisely enough to optimise against. A spec problem in an algorithms costume. | /blog/rlhf-teaching-robots-right-and-wrong/ | Ready |
| T8 | What failed: masked template matching | A negative result, published as one. | | Needs Notes |
| T9 | The token arithmetic nobody does | Context, cost and throughput on a real workload, back of the envelope. Unglamorous is the appeal. | | Ready |
| T10 | What GIL removal changes for ML people | Which data-loading workarounds stop being necessary, and which were never about the GIL. | /blog/asyncio-vs-multithreading-vs-multiprocessing/ | Ready |
| T11 | An image is a cheaper way to store text | DeepSeek OCR's real claim is optical context compression, not the OCR. | blog post first if it gets written | Ready |

### Archive angles

Kind = Angle. A second LinkedIn angle on a blog post, promoted before or never. Facts come from
the post.

| # | Post | Angle | Link | Status |
|---|---|---|---|---|
| A1 | Your car's GPS is wrong every second, and that's fine | A Kalman filter is how the car decides who to believe. Terminator framing survives. | /blog/kill-john-connor-using-kalman-filter/ | Ready |
| A2 | Four numbers for three rotations | Why quaternions, via gimbal lock. Robotics audience. | /blog/quaternions-a-necessary-evil/ | Ready |
| A3 | Your SSH key is two prime numbers and a padlock | Evergreen. | /blog/primes-and-rsa-encryption/ | Ready |
| A4 | A city with ten million coffee shops | HNSW in one image. Pairs with T2 as the follow-up. | /blog/hnsw-graph-based-vector-search/ | Ready |
| A5 | Spider-Man's drones knew about personal space | Velocity obstacles, from the drones posts. | /blog/personal-space-for-drones-part1/ | Ready |
| A6 | One conductor, a thousand players | MoE routing plus the DeepMind "million experts" paper. | /blog/moe-is-attention-all-you-really-need/ | Ready |
| A7 | The wrong weather app | Cross-entropy as a bad forecast, second angle. | /blog/cross-entropy-loss/ | Optional |

### Project stories

Kind = Angle. Written from the public `_projects/` page only. Read the page first.

| # | Post | Page | Status |
|---|---|---|---|
| P1 | Crop rows | _projects/2020-12-31-crop-row-detection.md | Ready if the page has a moment |
| P2 | Fixed-wing swarming | _projects/2021-10-01-fixedwing-swarming.md | Ready if the page has a moment |
| P3 | A fab and a reward function | _projects/2023-05-15-semiconductor-fab-optimization.md | Ready if the page has a moment |
| P4 | Pixie | _projects/2020-12-30-project-pixie.md | Ready if the page has a moment |
| P5 | Domain adaptation for NER | _projects/2020-08-30-unsupervised-domain-adaptation-for-entity-recognition.md | Optional |

---

## Moved to the blog queue

These are blog posts, not LinkedIn posts. Proposed rows for `.claude/blog-topic-queue.md`; the
companion job promotes them once written.

| Topic | Slug | Conceit to test first |
|---|---|---|
| DeepSeek OCR and optical context compression | `deepseek-ocr-optical-compression` | A photograph of a page is smaller than the page |
| Physics of language models: where a fact lives | `physics-of-llms-where-facts-live` | A library with no catalogue, only a floor plan |

Row 7 (Mamba) gets the speech angle added to its conceit. Row 10 (tokenizers) absorbs the token
counting math.

---

## Cut

- Rsync vs scp, os vs pathlib, linters and formatters: one man page answers each. No version only
  Naren could write.
- Snake case vs camel case: already struck, correctly.
- Autoregressive models in CSM: no thesis attached. File again when there is a specific claim.
- Reproducibility and Thinking Machines: timely posts expire. Needs a fresh hook if ever.
- Chat threads working for you: no claim.
- Face tracking and filters: off-position unless it becomes a detail inside S2.
- Single shot vs multi shot: hold, not cut, until there is a measured case.

---

## Posted

| # | Post | Kind | Postbeam id | Scheduled for | Run date (UTC) | Notes |
|---|---|---|---|---|---|---|
