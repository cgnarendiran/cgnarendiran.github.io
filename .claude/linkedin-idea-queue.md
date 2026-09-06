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

Judged on Naren's ten published LinkedIn posts and on the LinkedIn form, not on reach: there is
no engagement data in hand yet, so nothing here is ranked by numbers.

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
- The job writes the post to `.claude/linkedin-outbox/<slug>.md` exactly as the companion job
  does. The publisher job posts it on the next weekday morning and records it in
  `.claude/linkedin-ledger.md`; the row here then moves to Posted with the LinkedIn post URN.
- Every post follows `.claude/linkedin-style-guide.md`, including the length, hook, question and
  first-person rules that came out of the first JEPA promo (guide §11).

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
| T1 | Olympiad gold, arithmetic failure | Not the same capability. The benchmark that impresses you measures the wrong one. ARC Prize's own 2025 report says ARC-AGI-2 scores hinge on orchestration and compute budget more than on pretraining, and ARC-AGI-3 (2026) went interactive for that reason ([2601.10904](https://arxiv.org/abs/2601.10904)). | tokenizers post, once written | Ready |
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
| A6 | One conductor, a thousand players | In 2025 I called MoE the unsung hero. In September 2026 every open-weight leader is MoE: DeepSeek V4, Qwen3.8, Kimi K3, GLM-5.3, Llama 4 (*verify* each on its model card). Then the DeepMind "million experts" paper as where it goes next. | /blog/moe-is-attention-all-you-really-need/ | Ready after verification; use by 2026-10-06 |
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

## Fresh, September 2026

Researched on 2026-09-06 from the last few months of news in Naren's areas. Each row is a take
with a durable claim hooked on something current; "Use by" is when the hook goes stale. Claims
marked *verify* came from roundup blogs rather than primary sources; check them before posting.
The takes job does not exist yet, so these are for writing by hand, or ask for a draft.

| # | Post | The stance | Hook and sources | Kind | Use by | Status |
|---|---|---|---|---|---|---|
| F1 | Waymo is end-to-end too | The fight is not end-to-end versus modular. Waymo's own December blog says its driver is trained end-to-end: a Gemini-based VLM, a sensor-fusion encoder for lidar and camera, and a world decoder, with gradients flowing through all three. The real difference is a millisecond-latency fusion path that can override the language model. Ties to /blog/vla-pixels-to-tokens/ | Waymo spent late August saying pure pixels-to-steering "runs the risk of black box failures" ([Axios, 26 Aug](https://www.axios.com/2026/08/26/waymo-ai-shortcut-self-driving); [TechCrunch, 1 Sep](https://techcrunch.com/2026/09/01/waymo-goes-on-offense-ahead-of-teslas-cybercab-launch/)), a week before the Cybercab launched on 3 Sep with about 200 unsupervised cars and a claimed 1M unsupervised miles. Architecture: [understandingai.org, 17 Dec 2025](https://www.understandingai.org/p/waymo-and-teslas-self-driving-systems) | Take | 2026-09-20 | Ready |
| F2 | Somebody measured whether driving VLAs mean what they say | A reasoning trace in a driving model is decoration until it is tested counterfactually. Cite only the public papers; nothing from Naren's own benchmark until it is out. Ties to the VLA promo's "can it reason about why" | "Is VLA Reasoning Faithful?" ([2605.17268](https://arxiv.org/abs/2605.17268)): 42.5% fidelity, 8.9% hallucination, 53.3% reasoning-action inconsistency, 94 missed pedestrians over 300 inferences. Counter-nuScenes ([2607.16938](https://arxiv.org/abs/2607.16938)) inpaints objects out of scenes to measure their causal pull on the trajectory. Counterfactual VLA, CVPR 2026 ([2512.24426](https://arxiv.org/abs/2512.24426)): 17.6% lower trajectory error, 20.5% fewer collisions when the model reasons about alternatives | Take, then blog row 15 | none | Ready |
| F3 | One hyperparameter, twenty times less compute | The tricks were the cost, not the architecture. LeVJEPA matches or beats V-JEPA 2 at 5.6 to 20.8x less pretraining compute with one encoder, no teacher, no stop-gradient, one hyperparameter (lambda = 0.02). Ties to the JEPA post and blog row 1 | LeVJEPA ([2608.27395](https://arxiv.org/abs/2608.27395), Aug 2026). LeWorldModel (Mar 2026): about 15M parameters, one GPU for a few hours, planning up to 48x faster than foundation-model world models (*verify* in the paper). "When Does LeJEPA Learn a World Model?" ([2605.26379](https://arxiv.org/abs/2605.26379)) | Take, after the LeJEPA post is out | none | Hold for blog row 1 |
| F4 | The world model you can download beats the one you can rent | For builders, open weights plus post-training win. Genie 3 sits behind a $200-a-month, US-only, 18+ subscription (*verify* on Google's own page); NVIDIA Cosmos and Tencent HY-World ship as open-licence weights you can run today. Sequel to the June world-models post | Roundups: [introl.com](https://introl.com/blog/world-models-race-agi-2026), [tech-insider.org](https://tech-insider.org/genie-3-vs-marble-vs-nvidia-cosmos-world-models-2026/) | Take | 2026-10-06 | Ready after verification |
| F5 | Runway called a UI generator a world model | Same one-line test as June: does it predict the consequence of your click, or paint the next frame? A short sequel to "renderers in a costume" | Runway Solaris, "Interface World Model", 1 Sep 2026 (*verify* on Runway's own announcement) | Take | 2026-09-15 | Ready after verification |
| F6 | The intern now drafts a whole paragraph | The draft model's shape matters more than its size. Block-diffusion drafting proposes a whole block in one pass instead of one token at a time: 3.13x tokens per second on TPU v5p, nearly 6x on math, 2.29x end to end against EAGLE-3's 1.30x on Llama-3.1-8B. Feeds blog row 4's conceit | DFlash, [Google Developers Blog, 4 May 2026](https://developers.googleblog.com/supercharging-llm-inference-on-google-tpus-achieving-3x-speedups-with-diffusion-style-speculative-decoding/) | Angle, after blog row 4 | none | Hold for blog row 4 |
| F7 | pi0.7 ran an air fryer it had seen twice | Compositional generalisation is the VLA milestone that matters, not new bodies. The internet teaches the model the world, the robot data teaches it its hands, and now the two combine on objects it barely saw | Physical Intelligence pi0.7, 16 Apr 2026 ([humanoidsdaily.com](https://www.humanoidsdaily.com/news/physical-intelligence-unveils-0-7-the-rise-of-compositional-generalization-in-robotics), *verify* on pi.website). Gemini Robotics 2 and ER 2, 30 Jul 2026 ([marktechpost](https://www.marktechpost.com/2026/07/30/google-deepmind-gemini-robotics-2-whole-body-control-dexterity-multi-robot-collaboration/)) | Take | none | Ready after verification |
| F8 | The first humanoid number that is a price | Humanoids become real when they are billed per hour like labour, and the software that survives an eight-hour shift is what earns it. Figure 03 at BMW at roughly $25 per robot-hour; Chinese firms shipped about 97% of H1 2026 humanoids; Unitree listed on 19 Aug | [technology.org, 18 Jul 2026](https://www.technology.org/2026/07/18/humanoid-robots-in-2026-what-is-actually-deployed/), [evsint.com](https://www.evsint.com/top-8-humanoid-robot-companies-2026/); *verify* both numbers | Take | 2026-10-06 | Lowest priority: closest to the generic robotics-news genre |

### Driving: end-to-end stacks and world models

Researched on 2026-09-06. This is the area where Naren's own work sits, so the truth rule is
strict: cite only what is public, never the unpublished benchmark.

| # | Post | The stance | Hook and sources | Kind | Use by | Status |
|---|---|---|---|---|---|---|
| D1 | Waymo spent its first chip on the sensors, not the brain | Everyone's driver is end-to-end now (Tesla since v12, Waymo per its own December post, Wayve, XPeng). The argument left is what feeds the model. Waymo's first custom silicon is a 5nm ASIC of over 1,000 TOPS whose job is to fuse 13 cameras, lidar and radar before the model sees anything, with temporal denoising for low light; onboard compute is up 20x in eight years. That is where Waymo thinks the safety margin lives. Pairs with F1 | Waymo blog, 20 Aug 2026, via [Bloomberg](https://www.bloomberg.com/news/articles/2026-08-20/google-s-waymo-has-built-a-custom-chip-for-its-robotaxis), [TechCrunch, 23 Aug](https://techcrunch.com/2026/08/23/techcrunch-mobility-the-custom-chip-driving-waymos-robotaxi-ambitions/), [Semafor](https://www.semafor.com/article/08/21/2026/waymo-builds-custom-chip-for-robotaxi-fleet) | Take | 2026-09-30 | Ready |
| D2 | The driving simulator is now a video model, and it grades the driver | In nine months three companies replaced hand-built simulators with generative world models used for evaluation, not just data: Wayve GAIA-3 (Dec 2025, 15B parameters, double GAIA-2, synthetic test rejection down fivefold, simulated results said to mirror the road), the Waymo World Model on Genie 3 (Feb 2026, tornadoes and planes on freeways the fleet never saw), XPeng X-World (Apr 2026, multi-view video diffusion in real time). The June test still applies: a simulator that cannot count pedestrians is grading your car. Feeds blog row 3 | [Wayve GAIA-3 press](https://wayve.ai/press/wayve-launches-gaia3/) and [technical post](https://wayve.ai/thinking/gaia-3/); [Waymo World Model](https://www.marktechpost.com/2026/02/06/waymo-introduces-the-waymo-world-model-a-new-frontier-simulator-model-for-autonomous-driving-and-built-on-top-of-genie-3/) (*verify* on waymo.com); [XPeng X-World report](https://www.xpeng.com/news/019dd72da86c9dd703de8a0282290002); WorldLens evaluation of driving world models ([2512.10958](https://arxiv.org/abs/2512.10958)) | Take, then blog row 3 | none | Ready |
| D3 | Alpamayo explains itself, and the audits are already out | NVIDIA's Alpamayo-R1 is the first open-weight driving VLA you can inspect: Cosmos-Reason1 as the VLM plus a diffusion transformer for trajectories, trained on 80,000 hours of video with reasoning labels; up to 12% better planning on hard cases and 35% fewer close encounters in closed loop. Because it is open, the audits followed within months: ReasonBreak probes reasoning-enabled driving VLAs through their own explanations, and the faithfulness paper in F2 puts fidelity at 42.5%. Naren's VLA promo already named Alpamayo | [2511.00088](https://arxiv.org/abs/2511.00088); [HF nvidia/Alpamayo-R1-10B](https://huggingface.co/nvidia/Alpamayo-R1-10B); [TechCrunch, 5 Jan 2026](https://techcrunch.com/2026/01/05/nvidia-launches-alpamayo-open-ai-models-that-allow-autonomous-vehicles-to-think-like-a-human/); ReasonBreak ([2605.29114](https://arxiv.org/abs/2605.29114)) | Take | none | Ready |
| D4 | The leaderboard number is not the road number | Open-loop displacement error grades imitation, not driving. A 2026 cross-benchmark study of 15 methods finds ADE and FDE have no reliable correlation with closed-loop Driving Score on Bench2Drive, and even NAVSIM's PDM score correlates non-monotonically, with ranking inversions. This is the ice-cream test's cousin: the metric that impresses you measures the wrong thing. Ties to T1 and S1 | [2605.00066](https://arxiv.org/abs/2605.00066), "Do Open-Loop Metrics Predict Closed-Loop Driving?"; NAVSIM v2 EPDMS; Bench2Drive (CARLA, closed loop) | Take | none | Ready |
| D5 | Li Auto put a JEPA inside the car | MindVLA-o1 (GTC 2026) adds a latent world model that predicts future tokens as visual reasoning for planning, inside a native multimodal transformer. The "describe, don't paint" argument from the JEPA post is now a production roadmap. The honest con from that post follows it in: a latent future you cannot see is a future you cannot argue with | [Medium summary of China's VLA and world-model stacks](https://schen583.medium.com/vla-and-world-models-powered-autonomous-driving-in-china-96364c6ac2c2) (*verify* on Li Auto's GTC 2026 materials); XPeng VLA 2.0 with Volkswagen as launch partner, delivery 2027 ([XPeng press](https://www.xpeng.com/pressroom/news/019cae5e67b99c0960ee8a028129016a)) | Take | none | Ready after verification |
| D6 | Ten times the parameters on the same chip | FSD v15 is reported to go from about 1B to about 10B parameters while staying on HW4, "photon in, control out" since v12. If true, the story is quantisation and distillation at a fixed latency budget, not architecture. Ties to blog row 5 (quantisation) and the KV caching post | Fan-site reporting only ([notateslaapp](https://www.notateslaapp.com/news/4035/tesla-confirms-fsd-v15-will-run-on-hw4-shares-release-date), [teslarati](https://www.teslarati.com/tesla-vp-explains-why-end-to-end-ai-future-self-driving/)); the release date (end of 2026) contradicts claims that the Cybercab already runs v15. *Verify* against Tesla's own statements before touching it | Take | 2026-12-31 | Hold until verified |

Two more evaluation papers for the blog rows rather than LinkedIn: "Post-Training in End-to-End
Autonomous Driving" ([2607.08072](https://arxiv.org/abs/2607.08072)) and GraphWorld, long-horizon
planning with world models ([2606.16274](https://arxiv.org/abs/2606.16274)).

### Culture: movies, music, art

Two kinds. The first seven are conceits: a film, a song or a painting carrying one technical
idea, the blog's signature move (Terminator for Kalman, Spider-Man for drones, a police sketch
for JEPA). They never expire. The last four are takes on AI-in-culture news, and they do.

| # | Post | The stance or the conceit | Hook and sources | Kind | Use by | Status |
|---|---|---|---|---|---|---|
| C1 | Memento is a KV cache | Leonard's Polaroids and tattoos are what the model keeps so it never recomputes the past. MLA is learning to write smaller tattoos. Why your model eats 16GB of VRAM for a 2GB checkpoint, told through a man who cannot form new memories | /blog/kv-caching-mla-is-attention-all-you-really-need/ | Angle | none | Ready |
| C2 | Her is the articulate paperweight | Samantha can talk about anything and touch nothing. The VLA post's whole argument in one film: the gap between describing the apple and picking it up | /blog/vla-pixels-to-tokens/ | Angle | none | Ready |
| C3 | The Prestige is knowledge distillation | The pledge, the turn, the prestige: the student copies the teacher's outputs without ever learning the trick underneath, and it works anyway, until the one input where the trick mattered | Conceit for blog row 6; standalone angle once that post exists | Angle | none | Hold for blog row 6 |
| C4 | Autotune is quantisation | Snapping every weight to a grid is snapping every note to a pitch. What you lose is the vibrato, and at INT8 nobody notices; at NVFP4 the singer sounds like a robot | Conceit for blog row 5 | Angle | none | Hold for blog row 5 |
| C5 | Inception's totem is the causal test | A dream you can steer is a world model. The totem is the one-line test from the June post: does it predict consequences, or just render? Waymo's simulator on Genie 3 is the architect building the dream; the totem is what the car does when you spin it | Pairs with D2 and /blog/ world-models post | Angle | none | Ready |
| C6 | Groundhog Day is reinforcement learning with verifiable rewards | Phil replays the same day until the day grades him. RLVR is the exam that grades itself, and the honest con is that Punxsutawney is a very small world | Conceit for blog row 9 | Angle | none | Hold for blog row 9 |
| C7 | Vermeer's camera obscura and the tracing question | Art history spent a century arguing whether Vermeer looked or traced. Courts just split the same hair for AI: reading legally acquired books to learn is fair use (Bartz v. Anthropic), a picture with no human author gets no copyright (Thaler v. Perlmutter, Supreme Court denied 2 Mar 2026), and Andersen v. Stability is where "traced" gets decided | [Constitution Center on Thaler](https://constitutioncenter.org/blog/supreme-court-denies-artificial-intelligence-authorship-claim-for-artwork-copyright); [analyticsinsight roundup](https://www.analyticsinsight.net/news/the-copyright-battle-over-ai-generated-images-where-things-stand-in-2026) (*verify* case status) | Take | 2026-12-31 | Ready after verification |
| C8 | Sony is the last label standing | Warner and Universal settled with Suno and Udio for licensed models and artist opt-in; Sony is still pushing to trial. Meanwhile Deezer says 44% of new uploads are AI and Spotify badges the humans. The economic question was never the artist's; it is the platform's, and the "Verified" badge is the parental-advisory sticker inverted | [Music Business Worldwide on Warner-Suno](https://www.musicbusinessworldwide.com/warner-music-group-settles-with-suno-strikes-first-of-its-kind-deal-with-ai-song-generator/); [lawsuit tracker](https://www.chartlex.com/blog/business/music-industry-ai-lawsuits-tracker-2026) (*verify* the 44% and the badge) | Take | 2026-10-31 | Ready after verification |
| C9 | The Oscars wrote a Turing test in reverse | Since May 2026 only performances "demonstrably performed by humans with their consent" and human-authored screenplays are eligible, with AI disclosure for VFX, sound and script. The Academy is fine with AI in the pipeline; what it protects is the credit. A model can write the screenplay; it cannot be nominated. Tilly Norwood's feature film and Gal Gadot's AI-lit set are the two edges of the line | [TechCrunch, 2 May 2026](https://techcrunch.com/2026/05/02/ai-generated-actors-and-scripts-are-now-ineligible-for-oscars/); [Variety on Gadot](https://variety.com/2026/film/news/gal-gadot-defends-bitcoin-movie-ai-sets-lighting-1236847413/); [NBC on Tilly Norwood](https://www.nbcnews.com/video/studio-announces-a-feature-film-will-star-controversial-ai-actor-tilly-norwood-266256965823) | Take | none | Ready |
| C10 | Gameslop, and the world model that plays the game | 52% of game developers now call generative AI net negative, up from 18% in 2024; a third of 2025 Steam releases disclosed AI use; Ubisoft, Pearl Abyss and 11 Bit apologised for not disclosing. The backlash is not anti-AI, it is anti-undisclosed, the same line the Academy drew. At the other end, Microsoft's Muse and Google's Genie generate the game itself; the question for those is the June one: rendering or simulating? | [GamesRadar](https://www.gamesradar.com/games/why-so-many-game-developers-dont-want-to-use-generative-ai/); [techbuzz on the backlash](https://www.techbuzz.ai/articles/ai-in-game-development-why-the-2026-backlash-is-real) (*verify* survey numbers) | Take | 2026-10-31 | Ready after verification |
| C11 | Sora dies on 24 September | The video model that shocked 2024 is being switched off: app gone 26 Apr 2026, API off 24 Sep 2026, per OpenAI's own help page, after Disney walked. Runway and Veo took the professional slot by shipping a workflow, not a demo. Sequel to "renderers in a costume": the best renderer lost to the ones that fit a pipeline | [OpenAI help center](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation); [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations); [eMarketer on Disney](https://www.emarketer.com/content/openai-discontinue-sora-app-disney-exits-partnership) | Take | 2026-09-26 | Ready |

### Money: rounds and acquisitions

Template for all of these is the June world-models post: a claim, a fair reading of the other
side, a one-line test, a verdict. Never cheer a round. The question a funding post answers is
what the price says about the problem.

| # | Post | The stance | Hook and sources | Kind | Use by | Status |
|---|---|---|---|---|---|---|
| M1 | $60 billion for an agent that ships | SpaceX closed the largest startup acquisition on record on 14 Aug 2026: Cursor, all stock, about 391M shares, into a new SpaceXAI unit. Cursor owns no frontier model and books about $2.6B annualised revenue. The price says the moat was the workflow inside the editor, not the model behind it. SpaceX held an April option: $10B for a partnership or $60B to own it, and chose to own it | [CNBC, 16 Jun](https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html); [completion, Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/spacex-completes-record-60-billion-131311785.html) | Take | 2026-10-15 | Ready |
| M2 | Stripe bought the switchboard | OpenRouter routes 400+ models from 80+ providers. Stripe paid over $7B (Bloomberg) or over $8B (Axios), 5.4x the $1.3B valuation from May. Whoever meters the tokens owns the customer, which is the same claim as T6: the inference bill is the product decision | [Stripe newsroom](https://stripe.com/newsroom/news/stripe-agrees-to-acquire-openrouter); [TechCrunch, 16 Aug](https://techcrunch.com/2026/08/16/stripe-will-reportedly-acquire-ai-gateway-startup-openrouter-for-7b/); [Axios, 17 Aug](https://www.axios.com/2026/08/17/stripe-openrouter-paypal) | Take | 2026-10-15 | Ready |
| M3 | Valuation is not validation | Four robot-brain companies have raised about $5B against about $62B of valuation: Skild at $14B, Physical Intelligence in talks at over $11B, Figure, Spirit AI. Robot foundation models took $3.9B across nine deals. Set that against F8's number: the only humanoid figure that is a price is $25 an hour. Rounds measure conviction; they do not measure what breaks when the robot leaves the lab | [PYMNTS on Physical Intelligence](https://www.pymnts.com/news/artificial-intelligence/2026/physical-intelligence-seeks-1-billion-as-robotics-interest-grows/); [newmarketpitch roundups](https://newmarketpitch.com/blogs/news/physical-ai-top-startups-valuation) (*verify* every figure) | Take | 2026-10-31 | Ready after verification |
| M4 | Carmakers are buying brains, not building them | XPeng licenses VLA 2.0 to Volkswagen for 2027; Wayve's stack goes into Stellantis platforms for Uber across 12 cities; NVIDIA gives Alpamayo away as open weights. The driving stack is turning into a supplied component, like an engine from Bosch. The test for an OEM is no longer "can we build it" but "can we audit what we bought", which is D3 and F2 | [XPeng press](https://www.xpeng.com/pressroom/news/019cae5e67b99c0960ee8a028129016a); [autoconnectedcar on Wayve-Stellantis-Uber](https://www.autoconnectedcar.com/2026/06/autonomous-self-driving-vehicle-news-waymo-teradar-plusai-mobileye-tesla-uber-nuro-lucid-stellantis-wayve-weride-applied-intuition-roadzen/) | Take | none | Ready |
| M5 | The wrapper die-off has a pattern | Forty percent of AI companies funded in 2021 to 2023 are already closed; 60 to 70 percent of wrappers book zero revenue; Yupp.ai shut a year after a $33M raise. The three killers in the failure databases: the foundation model shipped your feature, GPU burn over $1M a month before revenue, no data you could not download. The last one is the VLA promo's point: the internet is free, robot data is not, and that asymmetry is the only moat left | [machinebrief](https://www.machinebrief.com/news/death-of-ai-wrapper-startups-wont-survive-2026); [ideaproof failure database](https://ideaproof.io/failures/ai-startups); [Yupp shutdown](https://www.techbuzz.ai/articles/yupp-ai-shuts-down-after-33m-a16z-crypto-raise) (*verify* the percentages) | Take | 2026-10-31 | Ready after verification |
| M6 | Instinct is priced on permissions | A personal agent by a 23-year-old ex-Sierra founder went from $50M to $2.5B in months, with $350M raised. The product is access: it needs every permission on your phone to book, cancel and buy for you, and early users are already alarmed by the scope. The valuation prices the access, not the model | [TechCrunch, 26 Aug](https://techcrunch.com/2026/08/26/viral-ai-startup-instinct-has-raised-350-million-at-a-2-5-billion-valuation/) | Take | 2026-09-30 | Ready |

**Skipped on purpose:** GPT-6 Astra (3 Sep) and the Qwen3.8 and DeepSeek V4 release posts. The
model-release genre is the most crowded feed on LinkedIn and expires in a day. Naren's edge is
the robotics, driving and world-model side, where F1 and F2 sit.

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

| # | Post | Kind | Post id | Published (UTC) | Run date (UTC) | Notes |
|---|---|---|---|---|---|---|
