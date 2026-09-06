# Blog topic queue

The blog job reads this file, walks the Queue table top to bottom, and writes the first topic
whose `Post file` does not already exist in `_posts/` on `master`. Reorder rows to change
priority. Delete a row to drop it. Add rows at the bottom (or wherever you want them) to extend
the queue.

Post numbering: latest published is **blog28** (JEPA). The next post takes `images/blog29/`,
then 30, and so on. The job derives the number from `ls images | grep blog`, not from this
table, so a manual post in between will not break it.

**Publish date.** If a Queue row has a date in the `Date` column, the job uses it for both the
front matter and the `_posts/` filename. If the column is empty, the job uses the day it runs.
Dates are here to backfill a gap in the archive: VLA published 2026-01-15 and the next post did
not land until September, so JEPA and LeJEPA are being spread across June and July rather than
stacked in the same week.

---

## Published

Kept here so the job sees the slug already exists and skips it. Move a row back into Queue to
force a rewrite.

| # | Topic | Post file (slug) | Date | Series |
|---|-------|------------------|------|--------|
| 28 | JEPA — nobody cares about the wallpaper | `jepa-nobody-cares-about-the-wallpaper` | 2026-06-15 | JEPA, part 1 of 2 |

---

## Queue

| # | Topic | Post file (slug) | Date | Series | Conceit to test first |
|---|-------|------------------|------|--------|----------------------|
| 1 | LeJEPA — provable SSL, no heuristics ([2511.08544](https://arxiv.org/abs/2511.08544)) | `lejepa` | **2026-07-15** | **JEPA part 2 — owed by part 1's cliffhanger** | Tear out the interrogation room; one term (SIGReg) replaces the EMA teacher, the stop-grad and the hobbled predictor |
| 2 | Diffusion policy vs. flow matching for robot actions | `diffusion-policy-vs-flow-matching` | | Standalone, follows VLA | A sculptor chipping marble (denoising) vs. a river finding the sea (flow) |
| 3 | World models as learned simulators — Genie 3, Cosmos | `world-models-learned-simulators` | | Follows JEPA | A dream you can steer; the driving instructor who never runs out of roads |
| 4 | Speculative decoding | `speculative-decoding` | | Is Attention All You Really Need? | The intern who drafts the email and the boss who only proofreads |
| 5 | Quantization — INT8, FP8, NVFP4 and what actually breaks | `quantization-edge-inference` | | Standalone, practical | Packing for a carry-on: what you fold, what you leave, what you regret |
| 6 | Knowledge distillation | `knowledge-distillation` | | Standalone | The professor's lecture notes vs. the student's crib sheet |
| 7 | Mamba and state space models | `mamba-is-attention-all-you-really-need` | | Is Attention All You Really Need? | The goldfish with a good filing system. Open on speech: audio at sample rate is where quadratic attention breaks first |
| 8 | Test-time compute and reasoning models | `test-time-compute` | | Standalone | Paying for thinking by the minute |
| 9 | GRPO and RLVR — what replaced RLHF | `grpo-rlvr` | | Follows the 2023 RLHF post | The exam that grades itself |
| 10 | Tokenizers — BPE, and why your model can't spell | `tokenizers-bpe` | | Foundational | A dictionary assembled by a committee with a word limit |
| 11 | Gaussian splatting | `gaussian-splatting` | | Standalone, visual | Pointillism, but the dots are jelly beans |
| 12 | Retrieval — BM25 to dense to hybrid | `retrieval-bm25-to-hybrid` | | Pairs with the HNSW post | The librarian who knows the words vs. the one who knows what you meant |
| 13 | DeepSeek OCR and optical context compression ([2510.18234](https://arxiv.org/abs/2510.18234)) | `deepseek-ocr-optical-compression` | | Standalone, paper explainer | A photograph of a page is smaller than the page |
| 14 | Physics of language models: where a fact lives and why it is lossy | `physics-of-llms-where-facts-live` | | Standalone, follows the LoRA post | A library with no catalogue, only a floor plan |

Rows 2 onward have no date, so they publish on the day they run. Only the backfill rows carry
one; once LeJEPA is published, the queue is back to normal same-day behaviour.

---

## Rules the job follows

- One post per run. If every row already has a post file, the job writes nothing, opens no PR,
  and says so — it does not invent a topic.
- Every draft follows `.claude/writing-style-guide.md`. The pre-publish checklist in §17 of that
  guide is the acceptance bar; the PR body carries it as a ticked checklist.
- Figures come from `.claude/scripts/fetch_arxiv_figures.py`, which only downloads them when the
  paper's licence permits republishing. Anything it refuses gets drawn with matplotlib and
  captioned `Source: Author`.
- The job opens a PR against `master`, self-checks it, and merges it if every check passes. It
  never pushes to `master` directly.
- Slug matching is a substring test against `_posts/`. Keep slugs distinctive enough not to
  collide (`lejepa` will not match the JEPA part 1 file, which contains `jepa-nobody-cares`).

## Note on part 2

Part 1 ends: *"Stay tuned for part 2, where we meet LeJEPA, tear out the entire interrogation
room, and replace it with a single term."* That is a promise to the reader, which is why LeJEPA
sits at row 1 rather than in topic order. Part 1 also seeded it in the honest-cons section — the
Barlow Twins / VICReg family "deserve more credit than they got. Hold that thought, it becomes
the entire story in part 2."
