# Blog topic queue

The weekly job reads this file, walks the Queue table top to bottom, and writes the first topic
whose `Post file` does not already exist in `_posts/` on `master`. Reorder rows to change priority.
Delete a row to drop it. Add rows at the bottom (or wherever you want them) to extend the queue.

Post numbering: latest published is **blog28** (JEPA, Sep 2026). The next post takes
`images/blog29/`, then 30, and so on. The job derives the number from `ls images | grep blog`,
not from this table, so a manual post in between will not break it.

---

## Published

Kept here so the job can see the slug already exists and skip it. Move a row up into Queue to
force a rewrite.

| # | Topic | Post file (slug) | Series |
|---|-------|------------------|--------|
| 28 | JEPA — nobody cares about the wallpaper | `jepa-nobody-cares-about-the-wallpaper` | JEPA, part 1 of 2 |

---

## Queue

| # | Topic | Post file (slug) | Series | Conceit to test first |
|---|-------|------------------|--------|----------------------|
| 1 | LeJEPA — provable SSL, no heuristics ([2511.08544](https://arxiv.org/abs/2511.08544)) | `lejepa` | **JEPA part 2 — owed by part 1's cliffhanger** | Tear out the interrogation room; one term (SIGReg) replaces the EMA teacher, the stop-grad and the hobbled predictor |
| 2 | Diffusion policy vs. flow matching for robot actions | `diffusion-policy-vs-flow-matching` | Standalone, follows VLA | A sculptor chipping marble (denoising) vs. a river finding the sea (flow) |
| 3 | World models as learned simulators — Genie 3, Cosmos | `world-models-learned-simulators` | Follows JEPA | A dream you can steer; the driving instructor who never runs out of roads |
| 4 | Speculative decoding | `speculative-decoding` | Is Attention All You Really Need? | The intern who drafts the email and the boss who only proofreads |
| 5 | Quantization — INT8, FP8, NVFP4 and what actually breaks | `quantization-edge-inference` | Standalone, practical | Packing for a carry-on: what you fold, what you leave, what you regret |
| 6 | Knowledge distillation | `knowledge-distillation` | Standalone | The professor's lecture notes vs. the student's crib sheet |
| 7 | Mamba and state space models | `mamba-is-attention-all-you-really-need` | Is Attention All You Really Need? | The goldfish with a good filing system |
| 8 | Test-time compute and reasoning models | `test-time-compute` | Standalone | Paying for thinking by the minute |
| 9 | GRPO and RLVR — what replaced RLHF | `grpo-rlvr` | Follows the 2023 RLHF post | The exam that grades itself |
| 10 | Tokenizers — BPE, and why your model can't spell | `tokenizers-bpe` | Foundational | A dictionary assembled by a committee with a word limit |
| 11 | Gaussian splatting | `gaussian-splatting` | Standalone, visual | Pointillism, but the dots are jelly beans |
| 12 | Retrieval — BM25 to dense to hybrid | `retrieval-bm25-to-hybrid` | Pairs with the HNSW post | The librarian who knows the words vs. the one who knows what you meant |

---

## Rules the job follows

- One post per run. If every row already has a post file, the job writes nothing, opens no PR, and
  says so — it does not invent a topic.
- Every draft follows `.claude/writing-style-guide.md`. The pre-publish checklist in §17 of that
  guide is the acceptance bar; the PR body carries it as a ticked checklist.
- Figures the job cannot legitimately fetch are left as suggestions in the PR body, not silently
  dropped. At least one self-made matplotlib figure (`Source: Author`) is required in every post.
- The job opens a PR against `master`. It never pushes to `master` directly — `master` is the live
  site.
- Slug matching is a substring test against `_posts/`. Keep slugs distinctive enough not to collide
  (`lejepa` will not match the JEPA part 1 file, which contains `jepa-nobody-cares`).

## Note on part 2

Part 1 ends: *"Stay tuned for part 2, where we meet LeJEPA, tear out the entire interrogation room,
and replace it with a single term."* That is a promise to the reader, which is why LeJEPA sits at
row 1 rather than in topic order. Part 1 also seeded it in the honest-cons section — the
Barlow Twins / VICReg family "deserve more credit than they got. Hold that thought, it becomes the
entire story in part 2."
