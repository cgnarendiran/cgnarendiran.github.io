# Narendiran Chembu — Blog Writing Style Guide

Reference for drafting posts on **cgnarendiran.github.io**. Built from a close reading of the
complete archive: all 26 posts, August 2017 through December 2025.

Site is Jekyll (theme adapted from Artem Sheludko). Images live in `images/blogNN/`, numbered
by post. Latest is `blog28`. **Next post folder: `images/blog29/`.**

---

## 1. The archive

| # | Post | Date | Kind |
|---|---|---|---|
| 28 | JEPA - Nobody Cares About the Wallpaper | Jun 2026 | Series explainer, part 1 of 2 |
| 27 | VLAs - Pixels to Tokens | Dec 2025 | Series explainer |
| 26 | VLMs - Pixels to Tokens | Dec 2025 | Series explainer |
| 25 | ViT - Pixels to Tokens | Nov 2025 | Series explainer |
| 24 | Cross Entropy Loss | Oct 2025 | Concept, extended conceit |
| 23 | MoE - Is Attention All You Really Need? | Sep 2025 | Series explainer |
| 22 | RoPE - Is Attention All You Really Need? | Sep 2025 | Series explainer |
| 21 | KV Caching & MLA - Is Attention…? | Aug 2025 | Series explainer |
| 20 | Markov Chain - Nuclear Bombs, Google Search, Perplexity | Aug 2025 | Three-domain sweep |
| 19 | HNSW - Finding Needles in Vector Haystacks | Jul 2025 | Concept, extended conceit |
| 18 | Padlocks to Prime Numbers - RSA and SSH | May 2025 | Concept + practical |
| 17 | How can you cook your pasta fasta? :p | Apr 2025 | Concept, extended conceit |
| 16 | LoRA - The Diet Pill for Obese Language Models | Jan 2025 | Paper explainer |
| 15 | Flux Models - Part 2 | Dec 2024 | Paper explainer |
| 14 | Flux Models - Part 1 | Nov 2024 | Paper explainer, math-heavy |
| 13 | RLHF: Teaching robots right and wrong | Feb 2023 | Concept lineage |
| 12 | ChatGPT - The Conversational Wizard | Feb 2023 | Explainer |
| 11 | Guided Diffusion Models - Part 2 | Dec 2022 | Chronological survey |
| 10 | Guided Diffusion Models - Part 1 | Nov 2022 | Physical intuition |
| 9 | Personal Space for drones - Part 2 | Aug 2021 | Robotics, movie framing |
| 8 | Personal Space for drones - Part 1 | Jul 2021 | Robotics, movie framing |
| 7 | Quaternions - a necessary evil | Jun 2021 | Math explainer |
| 6 | Kill John Connor using Kalman filter | Apr 2021 | Math, full roleplay conceit |
| 5 | Popular models for object detection | Apr 2021 | Reference summary |
| 4 | Sleepless nights in the US | Dec 2017 | Personal narrative |
| 2 | AI: Doomsday or Breakthrough - Part 2 | Aug 2017 | Essay |
| 1 | AI: Doomsday or Breakthrough - Part 1 | Aug 2017 | Essay |

**Three series exist:** *Pixels to Tokens* (25–27), *Is Attention All You Really Need?* (21–23),
and several two-parters. Multi-part is a normal, well-established move on this blog.

---

## 2. The single most important pattern: one extended conceit

This is the signature, and it is stronger than any other feature. **A post picks one metaphor at
the top and rides it to the last sentence.** Not scattered analogies — one governing conceit with
callbacks in every section.

Evidence across the archive:

- **Kalman filter** → you *are* the T-X Terminator hunting John Connor. Position and velocity of
  the motorcycle are the state. Vision sensor is damaged from the T-850 fight. GPS is tracking
  Katherine's cellphone ("stupid humans"). Ends: *"Now fire that missile at John Connor. Boo-yeah!
  Skynet now has a resistance free future! Hasta la what? Yeah, that's right."*
- **Cross entropy** → three cities. City A always sunny (zero entropy), City B three equally likely
  outcomes, City C anything can happen. The conceit then carries entropy, self-information,
  cross-entropy ("using the wrong weather app"), NLL ("daily forecast pain"), KL ("cost of a bad
  weather model"), and importance sampling ("studying rare storms").
- **HNSW** → a city with 10 million coffee shops. Nodes are cafés, edges are friendships,
  `efConstruction` is "how aggressively a new café networks", `efSearch` is "how picky the customer
  is". Ends: *"there's a tiny greedy traveler sprinting down a small-world graph."*
- **Pasta** → a restaurant kitchen. Asyncio is one chef, multithreading is many chefs in one
  kitchen, multiprocessing is many kitchens. The Italian grandma is a running gag that escalates:
  no olive oil in the water → someone breaks the spaghetti → someone puts ketchup in carbonara →
  *"Italy loses another star in the Michelin sky."* Ends: **"Never break the spaghetti. Ever."**
- **MoE** → an orchestra. Experts are sections, the gate is the conductor. Load balancing becomes:
  *"Hey, brass section, stop overpowering everyone; give the flutes a chance."*
- **RSA** → Simon Singh's padlock. `n` is the padlock shape, `e` is the turning method.
- **Drones** → Spiderman's London bridge swarm (part 1), Black Mirror's bee swarm (part 2).
  Ends: *"you're on your way to become the next Mysterio."*
- **VLA** → the articulate paperweight that can describe an apple but not pick it up.

**Rule: choose the conceit before writing, and make sure it can survive the whole post.** If it
runs out after two sections, it's the wrong conceit. The final line should close the loop.

For a JEPA post, the conceit needs to carry: predicting in an abstract space instead of pixels,
representation collapse, and a target geometry. Candidates worth testing against the whole outline
before committing — a weather forecaster who predicts "it'll be miserable" for every day and is
never technically wrong (collapse); a police sketch artist vs. a photocopier (latent vs. pixel
prediction); a lazy witness whose description fits everyone.

---

## 3. Skeleton of a post

Series entries follow this closely. Standalone posts drop steps 2–3 and open on the conceit.

| # | Section | Notes |
|---|---|---|
| 1 | `*On the cover: …*` | Italic. A description, a credit, or a joke. "Decorative" is acceptable |
| 2 | Recap of previous post | Linked, one paragraph, ends on the limitation motivating this post |
| 3 | The deflating turn | 1–2 short lines puncturing that win |
| 4 | "Welcome to the era of **X**." | Bold the term, then one thesis line: "This is the story of how…" |
| 5 | `## The problem` | Why the obvious fix fails. Often opens "You might think…" |
| 6 | The generic recipe | Abstract template before any named model |
| 7 | Named models, 2–4 | Each with a nicknamed heading |
| 8 | `## The Evolution` | Bulleted survey of variants, each with a figure |
| 9 | `## Why this matters` | Zoom out |
| 10 | `## Where things are going` | 3–4 named trends |
| 11 | `## The honest cons` | Real limitations, blunt |
| 12 | `## Conclusion` | One paragraph, callback to the conceit and the series thesis |
| 13 | `And now you know. Fin.` | **Always** |

**There is no body `# Title`.** `_layouts/post.html` already renders the front-matter title as the page's `<h1>`; adding one in the body gives the page two `<h1>`s and leaks the heading into the card excerpt on `/blog/`. The first in-body heading is always `##`.

### The opening formula

The VLA post is the cleanest instance:

> In our [last post], we taught a Transformer to see *and* speak. […] The result was a model that
> can look at a picture of your fridge and write you a thousand words on apples.
>
> Lovely. Now ask it to actually pick up the apple.
>
> The model will keep describing the apple with poetic precision, but it will not move a
> millimeter. We have built the world's most articulate paperweight […]
>
> Welcome to the era of **Vision-Language-Action models (VLAs)**. This is the story of how AI
> stopped being a tour guide and started being a worker.

Beats: *recap → deflating imperative → absurd image → name the era → thesis line.*

Standalone posts instead open cold on the conceit — "Imagine a city with 10 million coffee shops",
"Let's say you are the super hot T-X Terminator", "Imagine you live, work and vacation in three
different cities."

---

## 4. The sign-off

Traceable evolution, so get the current form right:

- 2021: `Fin.` alone (Quaternions)
- Feb 2023: `The secret sauce of ChatGPT is RLHF and now you know :)`
- Aug 2025: `And now you know!` newline `Fin.` (KV Caching)
- Sep 2025: `And now you know.` blank line `Fin.` (RoPE)
- **Oct 2025 onward: `And now you know. Fin.`** — locked in across Cross Entropy, MoE, ViT, VLM, VLA

**Use `And now you know. Fin.`** For a part 1 of a two-parter, substitute a cliffhanger instead:
"Stay tuned for part 2… Till then ciao." / "Stay tuned! :)" / "See you soon :)"

---

## 5. Voice

**Person.** "We" for the technical walkthrough ("we take our sequence of 197 tokens and shove it
into the encoder"). "You" for the reader's hypothetical and for the conceit ("You've got one chef
in the kitchen"). "I" for opinion, confession, and taste ("If only I had a dollar for everytime I
forgot what YOLO does", "my favorite scene", "I really liked the examples he used").

**Tense.** Present, for both mechanism and history.

**Rhythm.** A long explanatory sentence, then a short one that lands. Fragments allowed.
> "A continuous control problem is now a translation task."
> "Lovely. Now ask it to actually pick up the apple."
> "Pick your poison." / "No soda straws required." / "Bad weather app -> more wet clothes."
> "Don't trust this friend :p"

**Verbs are physical and slightly violent.** Slice, shove, smash, beat, bolt on, slap, take a
cleaver to, squash, glue, stitch, smuggle. Never "leverage", "utilize", "facilitate".

**Rhetorical question as transition.** Ubiquitous. Ask, then answer immediately.
> "What the hell is a 'velocity obstacle' you ask? Well, brace yourselves :)"
> "So the question becomes: how do you give the model hands without making it forget everything else?"
> "Okay now why do we do all this you ask?" / "Why is that true?" / "Now what can we do about this?"

**"Brace yourselves"** before a math section is a recurring tell (Quaternions, Drones 1, LoRA).

**`**NOTE:**` callouts** for asides and caveats — used in MoE, Drones, Quaternions, RSA, KV
Caching, Kalman. Good for "the thing I'm about to say is a simplification".

**Footnotes** (`[1](#fn:1)` with definitions at the bottom) appear in the 2017 posts. Largely
retired; modern posts inline the definition or link out instead.

---

## 6. Humour

Structural, not decorative — it does the explaining. Five recurring moves:

**(a) The conceit itself** (see §2). This is most of the humour.

**(b) The anticlimax.** Build up, then deflate in one line.
> "The result was a model that can […] write you a thousand words on apples. Lovely. Now ask it to
> actually pick up the apple."

**(c) The parenthetical aside.** Dry, throwaway, often self-aware.
> "(critical research)" / "(finally, someone who gets restaurant math)"
> "GPT-4 is rumored to have 1.76 trillion parameters, which is approximately the same as the number
> of times I've contemplated whether my coffee needs another shot of espresso. The answer, by the
> way, is always yes."
> "12 billion parameters, which is what happens when engineers are left unsupervised with compute budgets"
> "talk about narcissistic robots" / "talk about being jobless, yeesh; just kidding of course"

**(d) Affectionate insults toward models, never people.**
> "data-hungry monsters" / "brilliant idiots with expensive taste" / "like giving a toddler a PhD"
> "these pesky little bastards called quaternions" / "chonky models" / "computationally ravenous"
> "Modern VLAs reason like they did a humanities PhD and grasp like a toddler."

**(e) The escalating running gag** tied to the conceit — the Italian grandma in the pasta post is
the model. One escalation per section, paying off in the final line.

**Calibration.** Roughly one joke per section, landing at the *end* of an explanation, never inside
the mechanism. Section headings carry a nickname; the body stays clean.

**Emoticons.** Heavy in 2021 (`:p`, `:3`, `:)`, `:/`, `:D`, `huehue`, `UwU`), tapering through
2023–2024, near-zero in the *Pixels to Tokens* series. Cross Entropy (Oct 2025) still uses `:p` and
`:)` twice. **Verdict: one or two, at most, and only in a lighter standalone post. Keep them out of
series entries.**

**Pop culture** in cover captions and openings: Spiderman, Black Mirror, Terminator, Ex Machina,
Avengers, Rick and Morty, Joker, Gordon Ramsay, Marie Kondo, Kahneman. One or two per post.

---

## 7. Mathematical equations

### Delimiters — three distinct cases

1. **Inline:** `$...$` → "for action $a_i$ along dimension $i$"
2. **Display, standalone:** `$$ ... $$` — this site uses `$$`, not `\[ \]`.
   The reason is kramdown: it treats `\[` as an escaped literal `[` and strips the backslash
   before MathJax ever sees the page, so `\[ \]` renders as plain bracketed text. All 26
   archive posts with display math use `$$`; none use `\[ \]`. (Earlier revisions of this
   guide said the opposite. Following that advice breaks every equation in the post.)
3. **Display inside a list item or tight prose:** `\( ... \)` — used when the equation sits within
   a numbered/bulleted step, e.g. MoE's `\(P_i = \frac{1}{T}\sum_{t=1}^T p_{t,i}\)` and Flux 2's
   `\(\mathcal{L}_{FM}(\theta) = \mathbb{E}_{t,x_0,x_1}[\|v_\theta(x_t,t)-(x_1-x_0)\|^2]\)`

Multi-line goes inside a single `$$ $$` using `\\` breaks, or wraps `\begin{aligned}…\end{aligned}`
or `\begin{equation}…\end{equation}`.

### Placement rule: English first, always

Intuition in plain words, then a lead-in, then the equation. Never the reverse.
Lead-ins actually used: **"Formally,"** / **"Essentially,"** / **"Mathematically,"** /
**"specifically,"** / **"Concretely,"** / **"That means,"**

> The idea is dead simple. Pick a target action chunk $A$, sample noise $\epsilon \sim N(0, I)$,
> and pick a flow-time $\tau \in [0, 1]$. Linearly interpolate:
>
> \[A^\tau = \tau A + (1 - \tau)\epsilon\]

### Symbols defined immediately after

Either a "where" clause or a bullet list:
> where $x_i$ is an image feature vector and $y_j$ is a text feature vector, $\mathbb{B}$ is the
> mini-batch size, and $\tau$ is a temperature parameter.

### The conceptual equation

A signature move: write the formula in *words* first, then the real one.
> \[\frac{e^{\text{similarity score of a correct pair}}}{\sum_{\text{all pairs}}e^{\text{similarity score of pairs}}}\]
> specifically,
> \[\mathbb{L} = \sum_{i=1}^{|\mathbb{B}|} \log \frac{e^{x_i^\top y_i / \tau}}{\sum_j e^{x_i^\top y_j / \tau}} + \dots\]

### Colour-coded derivations

The Kalman post traces quantities through a long derivation with `\color{deeppink}{}` (prediction),
`\color{royalblue}{}` (previous/updated state), `\color{mediumaquamarine}{}` (measurement),
`\color{green}{}` (Kalman gain), `\color{tan}{}` (noise). Worth reusing for any derivation where the
same symbol changes role across steps.

### Density

3–6 display equations for a series explainer; 10–20 for a deep math post (Flux 1, Kalman, RoPE).
If a formula doesn't change the reader's mental model, cut it and write the sentence instead.

### Step naming

Numbered steps with joke names: `### Step 1: The Butcher Shop (Patchification)`,
`### Step 2: The Mathematical Smoothie (Linear Projection)`, `### Step 3: The Location Sticker`,
`### Step 2: the dictionary smuggle`, `### Flow matching, in one paragraph`.

---

## 8. Figures

**Format, exactly:**
```markdown
![RT-2 co-fine-tunes a vision-language model on robot trajectories and web data](/images/blog27/rt2.png) *Figure 2: RT-2 architecture. Source: [RT-2](https://arxiv.org/abs/2307.15818)*
```

- **Paths are root-relative** (`/images/blogNN/foo.png`), never the absolute production URL.
  An absolute URL fetches from the live site during local preview, so a new figure cannot be
  checked before it ships.
- **Alt text describes the image.** Never the literal string `alt`, never `Image`. A screen
  reader reads the alt and then the caption, so do not simply repeat the caption: drop the
  `Figure N:` prefix and the `Source: …` clause, drop `$math$`, and keep it under ~125
  characters. For a figure that carries an argument, say what the image *looks like* — the
  caption already says what it means.
- Caption is italic, same line, after the image.
- Pattern: `Figure N: <what it shows>. Source: [<name>](<link>)`
- **`Source: Author`** when the plot is self-made. He does make his own matplotlib figures —
  `binary_pe.png`, `sinusoidal_pe.png`, `vector_rotation.png`, `rope.png`. Worth doing again: a
  hand-made plot is the strongest asset in the RoPE post.
- Original diagrams get an explanatory caption instead of a source, and it can run long:
  > *Figure 3: Rotary Position Embedding in action. The query vector (blue) at position $m$ is
  > rotated by an angle $m\theta$ say $2\theta$… so attention is a function of token distance
  > rather than their absolute positions. Source: Author*
- Captions can carry jokes: *"If it looks complicated, that's because it is. The researchers didn't
  make it complex just to confuse you, but I'm not ruling it out either."*
- **Never hotlink.** Download the image into `images/blogNN/` or do not use it. Medium and
  ResearchGate URLs rot and block hotlinking.
- **Every named architecture gets a figure.** ViT has 6, VLM 5, VLA 5, Guided Diffusion 2 has 8.

**Image budget** — the site serves these on every page load, so weight is not free:

| | limit |
|---|---|
| body figure | ≤1600 px wide, ≤150 KB |
| cover | ≤1600 px wide, ≤200 KB |
| format | WebP for screenshots and diagrams; JPEG for photographs |

Run `.claude/scripts/optimize_images.py --check images/blogNN` before opening the PR.

**Animations.** No GIF over 1 MB — a 40 MB GIF is not a figure, it is an outage. Anything
longer than a second or two becomes an MP4, written as raw HTML at column 0 with the caption
on the line below:

```html
<video class="center-image" autoplay loop muted playsinline preload="metadata"
       poster="/images/blogNN/thing-poster.jpg"
       aria-label="What the clip shows, in one sentence."><source src="/images/blogNN/thing.mp4" type="video/mp4"></video>
*Figure 4: Caption, same as any other figure.*
```

`aria-label` is the video's alt text and follows the same rule.

**Known defect to avoid:** figure numbers repeat in several posts (the VLM post has three "Figure 3",
Guided Diffusion 1 has three). Number them correctly.

---

## 9. Tables

More common than a quick read suggests, and they land well. Recurring types:

- **Config table** — ViT: Image / Patch / Tokens
- **Summary table** — KV Caching: Method / Total cache size, with LaTeX in cells
- **TL;DR table** — Pasta: Model / Kitchen Metaphor / Best For / Avoid When
- **Comparison with a verdict column** — Flux 2: Aspect / Diffusion / Flux / **Winner**
- **Benchmark table** — VLA: Method / ImageNet-1K / SSv2 / K400
- **Transition table** — Markov: From → To / Probability
- **Insight table** — Markov: Model Type / Typical Perplexity / Insight

3–4 columns typical. Superscripts as unicode (`224²`) inside tables, not LaTeX. A "Winner" or
"Insight" column is a good move — it turns a table into an argument.

---

## 10. Citations and links

- First mention: full title, linked, authors/year when it matters.
  > [An image is worth 16X16 words, Dosovitskiy et al., 2020](https://arxiv.org/abs/2010.11929)
- Later mentions: short name, unlinked.
- Survey entries open **bold name (lab, year)**, then the link:
  > **EMMA (Waymo, 2024)**: [EMMA](https://arxiv.org/abs/2410.23262) uses Gemini as the backbone…
- Heading-level linking also used: `## R-CNN (2013): [paper](…)`
- A `## References` numbered list at the end appears in the Flux posts. Optional; inline linking is
  the more common pattern.
- **Cross-link your own posts constantly.** LoRA ← VLA, RoPE ← ViT, ChatGPT ← RLHF, part 1 ← part 2.
  This is a strong habit; keep it.
- Non-arXiv links used freely: HuggingFace, GitHub, YouTube (Veritasium, 3blue1brown, Welch Labs),
  company blogs, Wikipedia, StackOverflow, Medium explainers, lecture PDFs.
- **Watch out:** several internal links in older posts are broken (RLHF's Behavior Cloning link, MoE
  and RoPE's "previous post" links use the old `/2025-09-09-…` date-slug form instead of `/blog/…`).
  Use the `/blog/<slug>/` form.

---

## 11. Numbers and evidence

Concrete figures carry the argument. Never "significantly better" — give the number, the delta, and
the ablation.

> "with co-fine-tuning, generalization to unseen tasks jumps from 52% to 63%. Train from scratch on
> the smaller 5B model without web pretraining and it collapses to 9%."
> "Training takes 64 A100s for 14 days." / "Latency is 99 ms on an H100."
> "A rank-32 LoRA adapter (97.6M params, 1.4% of the model)"
> "Success rates on hard tasks go from 1% (k=1) to 44% (k=100)."
> "a weight matrix of size $4096 \times 4096$ has approximately 16.8 million parameters […]
> LoRA with rank $r = 8$: 65,536 trainable parameters. That's a 256x reduction!"

**The ablation is the punchline.** State the claim, give the number that proves it, then the number
showing what breaks without it.

Hardware, wall-clock, parameter counts and Hz are quoted constantly. They ground the writing in
someone who has actually shipped things.

**Worked micro-examples** are a repeated device and they work: the 3-page PageRank graph carried
through adjacency → stochastic → Google matrix → power iteration; RSA with $p=5, q=11$; the
${4 \choose 2} = 6$ RLHF comparisons. Use one whenever a formula is doing something non-obvious.

---

## 12. Honesty sections

Every post has one. Headings used: `## The honest cons`, `## The Hangover: The Early Cons of ViTs`,
`### The Reality Check: Limitations of VLMs`, `## Common Doubt`, `## The honest weakness`.

Rules observed:
- Name the failure without softening. *"OpenVLA's honest weakness is that it doesn't co-train with
  web data the way RT-2 did. It manipulates better and generalizes semantically worse. Pick your poison."*
- Admit the field is a mess. *"Evaluation is also a mess. […] There is no ImageNet for robots yet."*
- Admit when a result undercuts the thesis you just argued. *"One uncomfortable takeaway from this
  paper was that a big chunk of ViT's success came from better training, not just attention."*
- Give credit to the unfashionable. *"These genuinely forbid collapse […] and they deserve more
  credit than they get."*
- A `## Common Doubt` section that answers the obvious reader objection head-on (Markov post) is a
  good pattern for anything counterintuitive.

**Never end on the honesty section.** It goes before the conclusion so the post lands on synthesis.

---

## 13. Banned patterns

The blog already avoids these. Keep it that way. (See also the `humanizer` skill.)

- Significance inflation: "marks a pivotal moment", "stands as a testament", "evolving landscape",
  "reflects broader trends", "underscores the importance of"
- Promotional adjectives: "groundbreaking", "revolutionary", "vibrant", "seamless", "robust",
  "cutting-edge", "game-changing"
- Superficial `-ing` tails: "…, highlighting the intricate interplay between X and Y"
- Negative parallelism: "It's not just X, it's Y" — used sparingly and deliberately in conclusions;
  don't let it become a tic
- Vague attribution: "researchers argue", "experts believe" — name the paper or cut the claim
- Rule-of-three padding: "faster, cheaper, and more efficient"
- Em-dash overuse. This blog runs on commas, colons and full stops. Keep em dashes rare
- Generic upbeat endings. The real ending is a concrete bet: *"The bet for the next decade is
  whether we can manufacture […] the billion robot trajectories we'd need."*
- "Delve", "realm", "tapestry", "landscape", "harness", "unlock"
- Emoji bullet headers (the 🔑 in the pasta post is the one exception in the whole archive)

---

## 14. Length and formatting

- **2,000–3,000 words** for a series explainer. Standalone concept posts run shorter (HNSW ≈ 1,200);
  deep math posts run longer (Kalman, Flux 1, Object Detection).
- Headings: `##` major, `###` for steps within. Recent series posts drift toward sentence case;
  older posts use Title Case. Pick one per post and hold it.
- Paragraphs: 2–5 sentences. Single-sentence paragraphs for emphasis, frequently.
- **Numbered lists are the dominant explanatory device** across the whole archive — especially for
  mechanism ("1. Compress once, 2. Cache only latent, 3. Reinflate on demand, 4. Preserve positions").
- Bold on first introduction of a term, and on model names in survey lists.
- Backticks for config values, code, literal strings: `class_id: 284`, `slow_down`, `efSearch`,
  `ssh-keygen -t rsa -b 4096`
- Fenced code blocks with real, runnable Python where the topic warrants (pasta post has three full
  scripts; RSA has shell commands).
- Blockquotes for example model I/O and for quotes from papers or people, not for pull quotes.

---

## 15. Series thesis

*Pixels to Tokens* has one running argument, restated at the end of every entry:

> **Everything is a token.** Image patches are tokens. Words are tokens. Robot actions are tokens.
> The same Transformer that summarizes your email can fold your shirt, given the right fine-tuning data.

Each conclusion restates it with the new capability appended:
- ViT: "images into words"
- VLM: "images into dialogue"
- VLA: "images and dialogue into motion"

**A JEPA post breaks this deliberately, and that tension is the story.** The series spent three
posts turning everything into tokens; JEPA's argument is that reconstructing the tokens was never
the point, and you should predict in latent space instead. The VLA post already laid the track —
it ends on world models as the data substrate, the five-order-of-magnitude trajectory deficit, and
V-JEPA 2 / Genie 3 / Cosmos by name. That paragraph is the opening of the next post.

---

## 16. Quirks worth knowing

Recurring typos in the archive: "launguage", "wolrd", "obviosuly", "cascased", "maket cap",
"seprate", "doen", "aummary", "beacuse", "sincec", "equiped", "reseach", "veelocities", "Norht".
Some LaTeX is broken in places (`${\5choose2}$`, `q_{map}^{world}$ *`).

Don't replicate errors — but don't over-polish either. The voice tolerates a little roughness and
reads as a person typing fast, not a copy-edited magazine piece. "That's pretty smort" is
deliberate and should survive any proofread.

---

## 17. Pre-publish checklist

- [ ] One conceit chosen, carried through every section, closed in the final line
- [ ] Opens with a linked recap and a deflating turn (series) or cold on the conceit (standalone)
- [ ] "Welcome to the era of **X**" + one thesis line
- [ ] Generic recipe explained before any named model
- [ ] Every named architecture has a figure with a sourced caption; numbers are sequential
- [ ] At least one self-made figure (`Source: Author`)
- [ ] Display math uses `$$ $$`; list-embedded math uses `\( \)` (kramdown breaks `\[ \]`)
- [ ] English intuition precedes every equation; every symbol defined
- [ ] One worked micro-example
- [ ] Real numbers, with at least one ablation as a punchline
- [ ] At least one table, ideally with a verdict or insight column
- [ ] Honest-cons section, placed before the conclusion
- [ ] Cross-links to earlier posts, using `/blog/<slug>/` form
- [ ] Conclusion restates the series thesis with the new capability
- [ ] Ends with **"And now you know. Fin."**
- [ ] No banned patterns from §13

**Mechanics** (cheap to check, expensive to fix after publish):

- [ ] Tags come from `.claude/tag-vocabulary.md`, 3–6 of them, bracket list —
      `tags: [a, b, c]`, never a bare space-separated string
- [ ] `description:` present, 110–155 characters, a claim about the post — not the
      `*On the cover: …*` line and not the opening joke
- [ ] Every image has descriptive alt text; none of them says `alt` or `Image`
- [ ] No body `# Title` — the layout renders the front-matter title as the `<h1>`
- [ ] Image paths root-relative (`/images/…`); cross-links use `/blog/<slug>/`
- [ ] `.claude/scripts/optimize_images.py --check images/blogNN` passes
