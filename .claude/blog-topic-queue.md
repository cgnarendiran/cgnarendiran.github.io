# Blog topic queue

The blog job reads this file, walks the Queue table top to bottom, and writes the first topic
whose `Post file` does not already exist in `_posts/` on `master`. Reorder rows to change
priority. Delete a row to drop it. Add rows at the bottom (or wherever you want them) to extend
the queue.

Post numbering: latest published is **blog37** (Mamba part 2). The next post takes
`images/blog38/`, then 39, and so on. The job derives the number from `ls images | grep blog`,
not from this table, so a manual post in between will not break it.

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
| 31 | World models as learned simulators — Genie 3, Cosmos, GAIA-3 | `world-models-learned-simulators` | 2026-09-09 | Follows JEPA |
| 32 | Speculative decoding — draft, verify, and the rejection rule that keeps it exact | `speculative-decoding` | 2026-09-09 | Is Attention All You Really Need? |
| 33 | GRPO and RLVR — what replaced RLHF | `grpo-rlvr` | 2026-09-13 | Follows the 2023 RLHF post |
| 34 | Quantization — INT8, FP8, NVFP4 and what actually breaks | `quantization-edge-inference` | 2026-09-16 | Standalone, practical |
| 35 | Knowledge distillation — soft targets, temperature and what "distilled" means now | `knowledge-distillation` | 2026-09-20 | Standalone |
| 36 | Mamba part 1 — control theory, the RNN and CNN views, S4 and selection | `mamba-is-attention-all-you-really-need` | 2026-09-23 | Is Attention All You Really Need? Part 1 of 2 |
| 37 | Mamba part 2 — the parallel scan, the kernel, Mamba-2/3 and the hybrids that shipped | `mamba-is-attention-all-you-really-need-part2` | 2026-09-23 | Is Attention All You Really Need? Part 2 of 2 |

---

## Queue

| # | Topic | Post file (slug) | Date | Series | Conceit to test first |
|---|-------|------------------|------|--------|----------------------|
| 1 | MCTS and AlphaZero — how DeepMind taught a machine Go, then chess, from nothing. Naren's own framing, to use in his voice without embellishing it into an invented scene: AlphaGo and AlphaZero were the one thing that pulled him into the AI era, and the post gives DeepMind (David Silver, Aja Huang, Julian Schrittwieser, Demis Hassabis and team) real credit for it. For readers with minimal ML: make the problem land first (why you cannot search every move; Go's roughly 2×10^170 legal positions, Tromp 2016), then the fix in plain words. The history is half the story: Deep Blue beats Kasparov (lost 1996 4–2, won the 1997 rematch 3½–2½, brute-force alpha-beta plus hand-written evaluation); why that recipe failed at Go; MCTS (Coulom 2006; UCT, Kocsis and Szepesvári 2006) as explore-versus-exploit; AlphaGo beats Fan Hui 5–0 (Oct 2015) and Lee Sedol 4–1 (Mar 2016: move 37 in game 2, Lee's move 78 in game 4, Lee's 2019 retirement remark); AlphaGo Zero learns with no human games (Nature 2017); AlphaZero does chess, shogi and Go with one algorithm ([1712.01815](https://arxiv.org/abs/1712.01815), Science 2018); MuZero learns the rules too ([1911.08265](https://arxiv.org/abs/1911.08265)). The mechanism: policy and value network, PUCT selection, visit counts as the training target, self-play loop. DO GOOD RESEARCH: read the Nature 2016, Nature 2017 and Science 2018 papers and the Deep Blue paper (Campbell, Hoane, Hsu 2002) at the source, verify every date, score and number there, and prefer the papers over press. Honest cons with real material: the 2017 Stockfish match conditions and what the 2018 paper changed; compute cost; adversarial policies that beat superhuman Go AIs ([2211.00241](https://arxiv.org/abs/2211.00241)) | `mcts-alphazero` | | Standalone. Follows [Solving Chess](/blog/solving-chess-paths-nodes/), which already covers minimax, alpha-beta and the 60,000-vs-60-million nodes line: link it, do not repeat it. Links to the RLHF and GRPO posts for RL, and to the world-models post for MuZero | A food critic in a city with more restaurants than atoms: go back to the promising ones, take the odd gamble on a new one, and over time learn to trust your nose (the network) |
| 2 | Jev and System One models — TypeSafe AI's model that returns typed, calibrated decisions instead of text ([announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev), Sept 2026), and RLCD (Reinforcement Learning for Calibrated Decisions), the training method behind it. Why calibration is the product, how it differs from RLHF-tuned chat models, and where it sits among the latest frontier models. No paper yet: the speed, cost and zero-hallucination figures are vendor claims, so present them as claims and check the independent write-ups | `jev-system-one-models-rlcd` | | Standalone, timely (Jev launched Sept 2026). Links back to GRPO/RLVR and the 2023 RLHF post | The weather forecaster whose "70% chance of rain" means it rains on 7 days out of 10: a System One model answers fast, and its confidence is the part you can bank on |
| 3 | LLM benchmarks — the famous ones (MMLU, GSM8K, HumanEval, GPQA, Humanity's Last Exam, LMArena) and why they saturate or leak, then the agentic ones that score the model *and its harness*: SWE-bench Verified, Terminal-Bench, τ-bench, OSWorld, METR's time horizons. Same model, different scaffold, different score | `llm-benchmarks-terminal-bench` | | Standalone. Follows Jev | The bar exam versus the first week at the firm: one tests what you know, the other hands you the keys and watches what you do with them |
| 4 | Tokenizers — BPE, and why your model can't spell | `tokenizers-bpe` | | Foundational | A dictionary assembled by a committee with a word limit |
| 5 | Test-time compute and reasoning models | `test-time-compute` | | Standalone | Paying for thinking by the minute |
| 6 | Voice models part 1 — turning sound into tokens: spectrograms, wav2vec/HuBERT features, neural codecs (EnCodec, SoundStream, Mimi) and residual vector quantization, semantic vs acoustic tokens, frame rates from 50 Hz to 12.5 Hz | `voice-models-sound-to-tokens` | | Voice models, part 1 of 2. Follows the Mamba series, whose 16 kHz numbers set it up | The walkie-talkie against the phone call; part 1 is what goes down the wire |
| 7 | Voice models part 2 — holding a conversation: cascaded ASR → LLM → TTS vs end-to-end, half-duplex (VAD, endpointing, semantic VAD, barge-in), full-duplex (Moshi's two streams, backchannels, overlap, silence as input), echo cancellation, and voice data caveats (scarce two-channel data like Fisher, overlap labelling, accents and noise, consent and cloning, synthetic dialogue) | `voice-models-holding-a-conversation` | | Voice models, part 2 of 2. Same day as `voice-models-sound-to-tokens`. Links back to Mamba on full-duplex | A walkie-talkie is literally half-duplex: VAD is the model guessing when you would have said "over". A phone call is full-duplex |
| 8 | Gaussian splatting | `gaussian-splatting` | | Standalone, visual | Pointillism, but the dots are jelly beans |
| 9 | Retrieval — BM25 to dense to hybrid | `retrieval-bm25-to-hybrid` | | Pairs with the HNSW post | The librarian who knows the words vs. the one who knows what you meant |
| 10 | DeepSeek OCR and optical context compression ([2510.18234](https://arxiv.org/abs/2510.18234)) | `deepseek-ocr-optical-compression` | | Standalone, paper explainer | A photograph of a page is smaller than the page |
| 11 | Physics of language models: where a fact lives and why it is lossy | `physics-of-llms-where-facts-live` | | Standalone, follows the LoRA post | A library with no catalogue, only a floor plan |
| 12 | Is your driving model lying? Counterfactual tests for VLA reasoning ([2605.17268](https://arxiv.org/abs/2605.17268), [2607.16938](https://arxiv.org/abs/2607.16938), [2512.24426](https://arxiv.org/abs/2512.24426)) | `counterfactual-vla-reasoning` | | Follows VLA | The witness who describes the crime perfectly and points at the wrong suspect |
| 13 | Diffusion language models: writing a sentence like a sculptor (find the Sept 2026 survey of the 169 Jun-Aug papers) | `diffusion-language-models` | | Is Autoregression All You Really Need? Follows the Flux posts | Rough block first, details last: the whole paragraph appears at once and sharpens |
| 14 | End-to-end driving: photon in, control out, and why the leaderboards disagree ([2605.00066](https://arxiv.org/abs/2605.00066), Alpamayo-R1 [2511.00088](https://arxiv.org/abs/2511.00088)) | `end-to-end-driving-leaderboards` | | Follows VLA and row 15 | A driving test where the examiner never touches the wheel (open loop) versus one where he does (closed loop) |

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
- **Same-day parts.** A row whose `Series` says ``Same day as `<slug>` `` is written by the
  same-day job (`.claude/routine-prompts/blog-same-day.md`, Sun + Wed 17:30 UTC) on the day
  `<slug>` publishes, with a noon time in its front-matter `date` so it lists above part 1. If
  part 1 slips to a later blog day, part 2 slips with it.
- Slug matching is a substring test against `_posts/`. Keep slugs distinctive enough not to
  collide (`lejepa` will not match the JEPA part 1 file, which contains `jepa-nobody-cares`).

## Note on part 2

Settled. Part 1's cliffhanger promised LeJEPA, and `lejepa` (2026-07-15) delivers it: SIGReg in
place of the EMA teacher, the stop-gradient and the hobbled predictor, and the Barlow Twins /
VICReg thread part 1 seeded in its honest-cons section is picked up there. The JEPA two-parter is
closed, so nothing in the Queue is owed to a reader any more.
