# Tag vocabulary

The controlled list of tags for `_posts/` and `_projects/`. Posts and projects share one
vocabulary — a reader clicking `computer-vision` wants both.

## Rules

- **Pick only from this list.** To add a term, add it here in the same PR that uses it, and
  only if it will plausibly recur. A tag used once is noise.
- **Format:** `tags: [computer-vision, transformers, attention]` — a YAML flow list on one
  line. Never a bare space-separated string: Jekyll splits that on whitespace, so
  `Mixture of Experts` becomes three tags, one of which is `of`.
- **Lowercase, hyphenated, ASCII.** Tag anchors are slugified, so `AI` and `ai` collapse to
  the same target while rendering as two different labels. No `&` (it emits an unescaped
  entity in an href).
- **3–6 tags per document.** Fewer than 3 and it won't surface; more than 6 and none of them
  mean anything.
- Tags render as links to `/tags/#<tag>` on the tag index. There is no per-tag page and no
  tagging plugin — see CLAUDE.md.

## Fields

`computer-vision` · `nlp` · `robotics` · `generative-ai` · `reinforcement-learning` ·
`multimodal` · `deep-learning` · `embodied-ai`

## Architectures

`transformers` · `vision-transformers` · `vision-language-models` · `vision-language-action` ·
`llms` · `cnn` · `lstm` · `diffusion-models` · `flow-matching` · `mixture-of-experts` ·
`jepa` · `world-models` · `clip`

## Techniques and training

`attention` · `positional-encoding` · `kv-caching` · `lora` · `fine-tuning` ·
`efficient-inference` · `efficient-training` · `self-supervised-learning` ·
`representation-learning` · `transfer-learning` · `domain-adaptation` · `rlhf` ·
`imitation-learning` · `alignment` · `image-generation` · `synthetic-data` · `segmentation` ·
`object-detection`

## Retrieval and data

`rag` · `retrieval` · `vector-search` · `hnsw` · `graph-algorithms` ·
`named-entity-recognition` · `document-understanding` · `summarization`

## Maths and foundations

`probability` · `information-theory` · `loss-functions` · `bayesian-inference` ·
`markov-chains` · `pagerank` · `optimization` · `cryptography` · `number-theory` ·
`quaternions` · `rotations` · `kalman-filter` · `state-estimation`

## Systems and science

`python` · `concurrency` · `simulation` · `ros` · `molecular-dynamics` · `fluid-dynamics` ·
`nanoparticles`

## Robotics and autonomy

`collision-avoidance` · `multi-agent-systems` · `drones` · `autonomous-vehicles`

## Domains

`healthcare` · `agriculture` · `automotive` · `manufacturing` · `semiconductor` · `oil-gas` ·
`legal`

## Organisations

`openai` · `deepseek`

## Kind

`ai-safety` · `essay` · `personal` · `competition` · `research`

## Reserved for queued topics

Pre-registered so a drafting run doesn't invent a Title-Case variant:

`quantization` · `knowledge-distillation` · `speculative-decoding` · `tokenization` ·
`gaussian-splatting` · `state-space-models` · `test-time-compute` · `grpo`

## Deliberately not tags

- **Employer and lab names** used once — Aramco, Mercedes-Benz, CTcue, CFI, Abhiyaan, NCL,
  ILASS, DBC. They belong in prose, not in a browsable taxonomy.
- **One-off acronyms** — QRA, PFD, rPPG, NIR, croprow, dota2, exmachina.
- **Umbrella terms** — `ai`, `learning`, `models`, `vision` on their own. Use the specific
  field tag instead; an umbrella tag that matches half the archive sorts nothing.
