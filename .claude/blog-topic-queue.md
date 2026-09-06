# Blog topic queue

The blog job reads this file, walks the Queue table top to bottom, and writes the first topic
whose `Post file` does not already exist in `_posts/` on `master`. Reorder rows to change
priority. Delete a row to drop it. Add rows at the bottom (or wherever you want them) to extend
the queue.

Post numbering: latest published is **blog29** (LeJEPA). The next post takes `images/blog30/`,
then 31, and so on. The job derives the number from `ls images | grep blog`, not from this
table, so a manual post in between will not break it.

**Publish date.** If a Queue row has a date in the `Date` column, the job uses it for both the
front matter and the `_posts/` filename. If the column is empty, the job uses the day it runs.
Dates were here to backfill a gap in the archive: VLA published 2026-01-15 and the next post did
not land until September, so JEPA and LeJEPA went out in June and July rather than stacked in the
same week. That backfill is finished; no Queue row carries a date now.

---

## Published

Kept here so the job sees the slug already exists and skips it. Move a row back into Queue to
force a rewrite.

| # | Topic | Post file (slug) | Date | Series |
|---|-------|------------------|------|--------|
| 28 | JEPA — nobody cares about the wallpaper | `jepa-nobody-cares-about-the-wallpaper` | 2026-06-15 | JEPA, part 1 of 2 |
| 29 | LeJEPA — provable SSL, no heuristics ([2511.08544](https://arxiv.org/abs/2511.08544)) | `lejepa` | 2026-07-15 | JEPA, part 2 of 2 |

---

## Queue

| # | Topic | Post file (slug) | Date | Series | Conceit to test first |
|---|-------|------------------|------|--------|----------------------|
| 1 | Diffusion policy vs. flow matching for robot actions | `diffusion-policy-vs-flow-matching` | | Standalone, follows VLA | A sculptor chipping marble (denoising) vs. a river finding the sea (flow) |
| 2 | World models as learned simulators — Genie 3, Cosmos | `world-models-learned-simulators` | | Follows JEPA | A dream you can steer; the driving instructor who never runs out of roads. Now with three production examples: Wayve GAIA-3 (15B, evaluation not just data), the Waymo World Model on Genie 3, XPeng X-World; and WorldLens ([2512.10958](https://arxiv.org/abs/2512.10958)) for how to grade the simulator itself |
| 3 | Speculative decoding | `speculative-decoding` | | Is Attention All You Really Need? | The intern who drafts the email and the boss who only proofreads. Punchline: DFlash (Google, May 2026) has the intern draft a whole paragraph in one go, 3.13x tokens per second on TPU |
| 4 | Quantization — INT8, FP8, NVFP4 and what actually breaks | `quantization-edge-inference` | | Standalone, practical | Packing for a carry-on: what you fold, what you leave, what you regret |
| 5 | Knowledge distillation | `knowledge-distillation` | | Standalone | The professor's lecture notes vs. the student's crib sheet |
| 6 | Mamba and state space models | `mamba-is-attention-all-you-really-need` | | Is Attention All You Really Need? | The goldfish with a good filing system. Open on speech: audio at sample rate is where quadratic attention breaks first |
| 7 | Test-time compute and reasoning models | `test-time-compute` | | Standalone | Paying for thinking by the minute |
| 8 | GRPO and RLVR — what replaced RLHF | `grpo-rlvr` | | Follows the 2023 RLHF post | The exam that grades itself |
| 9 | Tokenizers — BPE, and why your model can't spell | `tokenizers-bpe` | | Foundational | A dictionary assembled by a committee with a word limit |
| 10 | Gaussian splatting | `gaussian-splatting` | | Standalone, visual | Pointillism, but the dots are jelly beans |
| 11 | Retrieval — BM25 to dense to hybrid | `retrieval-bm25-to-hybrid` | | Pairs with the HNSW post | The librarian who knows the words vs. the one who knows what you meant |
| 12 | DeepSeek OCR and optical context compression ([2510.18234](https://arxiv.org/abs/2510.18234)) | `deepseek-ocr-optical-compression` | | Standalone, paper explainer | A photograph of a page is smaller than the page |
| 13 | Physics of language models: where a fact lives and why it is lossy | `physics-of-llms-where-facts-live` | | Standalone, follows the LoRA post | A library with no catalogue, only a floor plan |
| 14 | Is your driving model lying? Counterfactual tests for VLA reasoning ([2605.17268](https://arxiv.org/abs/2605.17268), [2607.16938](https://arxiv.org/abs/2607.16938), [2512.24426](https://arxiv.org/abs/2512.24426)) | `counterfactual-vla-reasoning` | | Follows VLA | The witness who describes the crime perfectly and points at the wrong suspect |
| 15 | Diffusion language models: writing a sentence like a sculptor (find the Sept 2026 survey of the 169 Jun-Aug papers) | `diffusion-language-models` | | Is Autoregression All You Really Need? Follows the Flux posts | Rough block first, details last: the whole paragraph appears at once and sharpens |
| 16 | End-to-end driving: photon in, control out, and why the leaderboards disagree ([2605.00066](https://arxiv.org/abs/2605.00066), Alpamayo-R1 [2511.00088](https://arxiv.org/abs/2511.00088)) | `end-to-end-driving-leaderboards` | | Follows VLA and row 15 | A driving test where the examiner never touches the wheel (open loop) versus one where he does (closed loop) |

No queue row carries a date any more, so every remaining topic publishes on the day it runs. The
backfill that spread JEPA and LeJEPA across June and July is done.

---

## Rules the job follows

- One post per run. If every row already has a post file, the job writes nothing, opens no PR,
  and says so — it does not invent a topic.
- Every draft follows `.claude/writing-style-guide.md`. The pre-publish checklist in §17 of that
  guide is the acceptance bar; the PR body carries it as a ticked checklist.
- Figures come from `.claude/scripts/fetch_arxiv_figures.py`, which only downloads them when the
  paper's licence permits republishing. Anything it refuses gets drawn with matplotlib and
  captioned `Source: Author`.
- Figures are written to `images/blogNN/` with **root-relative** paths in the markdown
  (`/images/blogNN/foo.png`) and **descriptive alt text** — never the literal string `alt`.
- Before opening the PR, run `.claude/scripts/optimize_images.py --check images/blogNN`. If it
  exits non-zero, run it again with `--apply --to-webp`, update the affected image paths in the
  post, and re-check. A figure over 150 KB or 1600 px does not ship.
- Tags come from `.claude/tag-vocabulary.md`: a bracket list of 3-6 lowercase hyphenated terms.
  Adding a new term means adding it to that file in the same PR.
- The job opens a PR against `master`, self-checks it, and merges it if every check passes. It
  never pushes to `master` directly.
- Slug matching is a substring test against `_posts/`. Keep slugs distinctive enough not to
  collide (`lejepa` will not match the JEPA part 1 file, which contains `jepa-nobody-cares`).

## Note on part 2

Settled. Part 1's cliffhanger promised LeJEPA, and `lejepa` (2026-07-15) delivers it: SIGReg in
place of the EMA teacher, the stop-gradient and the hobbled predictor, and the Barlow Twins /
VICReg thread part 1 seeded in its honest-cons section is picked up there. The JEPA two-parter is
closed, so nothing in the Queue is owed to a reader any more.
