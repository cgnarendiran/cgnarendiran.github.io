# Narendiran Chembu — Blog Writing Style Guide

Reference for drafting posts on **cgnarendiran.github.io**. Built from a close reading of the
complete archive: all 26 posts, August 2017 through December 2025.

Site is Jekyll (theme adapted from Artem Sheludko). Images live in `images/blogNN/`, numbered
by post. Latest is `blog28`. **Next post folder: `images/blog29/`.**

---

## 1. The archive

| # | Post | Date | Kind |
|---|---|---|---|
| 29 | LeJEPA - Good in Every Direction | Jul 2026 | Series explainer, part 2 of 2 |
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

**This device is occasional, not the default paragraph shape.** Roughly one paragraph in six
should end on a short line; the LeJEPA draft shipped at one in three and read as portentous. See
§18, which is the single most important section in this guide for sounding human, and §20
for the audience rule: one idea per sentence, written for a reader with almost no ML.

**And notice what those landing lines actually are.** Every one is a joke or a concrete fact.
None is a maxim. "Pick your poison" is a joke; "The superstition moved house, it did not leave
town" is a fortune cookie. The maxim is the tell.

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

4. **Never a bare `|` inside inline math.** Kramdown's table parser runs before MathJax and
   treats a paragraph containing a pipe as a table row, so `$1/|o_i|$` splits its paragraph into
   three `<td>` cells and every formula in it dies (the GRPO post shipped like this). Write
   `$1/\vert o_i\vert$` or `\lvert … \rvert`. Pipes are fine inside a standalone `$$` block,
   which kramdown parses as math before the table rule sees it. And close inline math with
   exactly one `$`: a trailing `$$` opens a display block that swallows the rest of the
   paragraph. `prose_lint.py` fails on both.

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

**Covers.** The cover is a real picture of the conceit, not a diagram of it. Naren's rule,
September 2026, after two posts shipped with drawn covers: "you don't need to draw the cover
every time, it needs to be representative of the conceit." The covers that work are found, not
made: Itchō's blind monks for ViT, Bruegel's Babel for VLM, a claw crane for VLA, the Library
of Congress book lift for speculative decoding, the University of Tokyo results boards for GRPO,
the Universal Studios New York Street backlot for world models. A painting, a historical
photograph, or a plain documentary photo of the actual thing.

- **Source: Wikimedia Commons**, through `.claude/scripts/commons_cover.py`. `search` prints
  candidates with their licence; `fetch` re-checks the licence, downloads, crops and prints the
  credit line. It refuses anything that is not public domain, CC0, CC BY or CC BY-SA. No
  stock sites, no AI images, no screenshots of other people's figures.
- **Search like a librarian.** Commons search is literal. Try the object's plain name ("goods
  lift", "book conveyor"), the name in the language of the place ("合格発表" found the results
  boards that "exam results" did not), category names ("Category:Backlot"), and the big
  institutional uploads (Library of Congress, National Archives, the Met). Wide scenes and
  portrait crops rarely read at card size; a tight crop on the object does.
- **Caption carries the credit.** `*On the cover: <what it shows, and the one line that ties it
  to the conceit>. Photo by [Author](commons file page), CC BY 2.0.*` or `[Public
  domain](file page), via <institution>.` The joke or the tie-in goes before the credit.
- **Shape:** landscape, 1.905:1, 1400 px wide, JPEG under 200 KB (the script does this). Mild
  auto-contrast is fine on an old print. No text overlays.
- **Fall back to drawing only when a real search found nothing**, and say so in the PR. A drawn
  cover is a figure; it belongs in the body with a `Source: Author` caption, not on the card.

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
- **Benchmarks, datasets, tools and models get a link and a plain-words gloss on first mention,
  not only papers.** "grade school math [GSM8K](https://huggingface.co/datasets/openai/gsm8k)",
  "a proof in [Lean](https://lean-lang.org/)", "[AIME 2024](https://artofproblemsolving.com/…)".
  Datasets link to HuggingFace, tools to the project site, models to arXiv. See §19.8.
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

**In a series, this section is where repetition hides.** The archive varies its heading on
purpose (`The honest cons`, `The Hangover`, `The Reality Check`, `Common Doubt`, `The honest
weakness`) and you must too: reusing the previous entry's heading verbatim is a defect. Reusing
its *argument* is a worse one. Part 2 of JEPA originally opened its cons with "the superstition
moved house" — which is part 1's con ("collapse is still managed by superstition") wearing a
hat. Before drafting this section, read the previous post's and write down what it already
conceded. Your cons must be the ones that are new *because* of what this post just explained.

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
- [ ] The cover is a real image of the conceit from Wikimedia Commons, licence verified by
      `commons_cover.py`, credited in the `*On the cover:*` line (§8 Covers)
- [ ] Display math uses `$$ $$`; list-embedded math uses `\( \)` (kramdown breaks `\[ \]`)
- [ ] English intuition precedes every equation; every symbol defined
- [ ] One worked micro-example
- [ ] Real numbers, with at least one ablation as a punchline
- [ ] At least one table, ideally with a verdict or insight column
- [ ] Honest-cons section, placed before the conclusion
- [ ] Cross-links to earlier posts, using `/blog/<slug>/` form
- [ ] Conclusion restates the series thesis with the new capability
- [ ] Ends with **"And now you know. Fin."** — as a sentence with a verb, not a verbless coda
- [ ] No banned patterns from §13
- [ ] No banned patterns from §18, and the landing-line count is roughly one paragraph in six
- [ ] Honest-cons heading and arguments differ from the previous post's (§12)
- [ ] At least two jokes attached to the maths (§18), and the conceptual-equation move used once
- [ ] No point is made twice; nothing is signposted with "we'll come back to that"
- [ ] `python3 .claude/scripts/prose_lint.py _posts/<file>` exits 0, and its warnings were read
- [ ] Every conceit character is pinned to its technical term in brackets wherever the mechanism
      needs it: "the TA (ranker)", "a second network (critic)" (§19.1)
- [ ] Benchmarks, datasets, tools and models are linked and glossed on first mention (§19.8)
- [ ] The post talks to the reader ("I want you to", "Let's say") rather than directing one
      ("Hold on to", "Price it out"); the small words are in ("pretty", "kind of", "simple") (§19)
- [ ] Every long sentence is split, with So, And or But opening the next one; every long subject
      has a comma before its verb and every introductory phrase has one after it (§19.5, §19.6)
- [ ] Every clever line has its reason spelled out in the clause; no image outside the conceit
      is doing a plain word's job (§19.7, §19.10)
- [ ] A reader who knows what a neural network is and little more can follow every section;
      each term is explained before it is used (§20.2)
- [ ] The problem has its own paragraph, with a number or an everyday example, before the fix is
      named (§20.3)
- [ ] One idea per sentence: the lint's "chained sentences" and "long sentences" warnings are
      resolved or are lists (§20.1); none of the §20.4 patterns is left
- [ ] Every formula says where it comes from, and every symbol (barred and hatted ones included)
      is defined in words (§21.1)
- [ ] The worked example says what it is a slice of, and one paragraph connects it to the
      model's real output (§21.2); hypotheticals are flagged as such (§21.3)
- [ ] The architecture figure shows how the units connect, with a zoom on the part the maths
      computes, a legend and no overlapping text (§21.7, §21.8)
- [ ] A short "where it is used" section, and the name explained if it is not obvious (§21.9,
      §21.10)
- [ ] The ten-questions test was run and every question it raised is answered (§21)

**Mechanics** (cheap to check, expensive to fix after publish):

- [ ] Tags come from `.claude/tag-vocabulary.md`, 3–6 of them, bracket list —
      `tags: [a, b, c]`, never a bare space-separated string
- [ ] `description:` present, 110–155 characters, a claim about the post — not the
      `*On the cover: …*` line and not the opening joke
- [ ] Every image has descriptive alt text; none of them says `alt` or `Image`
- [ ] No body `# Title` — the layout renders the front-matter title as the `<h1>`
- [ ] Image paths root-relative (`/images/…`); cross-links use `/blog/<slug>/`
- [ ] `.claude/scripts/optimize_images.py --check images/blogNN` passes
- [ ] No bare `|` inside `$...$` (use `\vert`), and no inline formula closed with `$$` (§7)

---

## 18. The six sentence shapes that give the game away

Every one of these was caught by Naren in the published LeJEPA post (blog29), after that draft
had already passed §13, the humanizer skill and the whole of §17. §13 catches *vocabulary*.
These are **structures**, they survive a vocabulary check untouched, and they are what actually
makes a reader say "this was written by a model". His verdict on the worst of them was
"you have to understand that nobody writes like this."

The common root: the model reaching for **the register of profundity**. Short, balanced,
verbless, quotable. Real people writing fast do not compose aphorisms at the end of every
thought, and they especially do not do it seven times in one post.

**1. The maxim landing.** A paragraph that closes on a short quotable fragment.
> ✗ "Everybody keeps hammering." / "This one hands you a gauge." / "The superstition moved house, it did not leave town."
>
> **Test:** could it go on a poster? Then cut it, or replace it with a joke. Landing lines in
> the archive are jokes ("Never break the spaghetti. Ever.") or facts. Never wisdom.

**2. The verbless triptych**, usually in the conclusion.
> ✗ "Same blade at the end of it. No moon, no midnight, no counting to three hundred. Just a gauge, and something to hold it against."
>
> That is free verse. Compare the archive: "Now fire that missile at John Connor. Boo-yeah!",
> "you're on your way to become the next Mysterio." Verbs, full sentences, usually a joke.
> **A conclusion is a person talking, not a poem.**

**3. Enumeration theatre.** Announcing a count, then marching through it in parallel.
> ✗ "Three things care. The first is… The second is… The third is the one that actually hurts."
>
> Merge them, vary the openings, drop the count. The portentous twist on the last item
> ("the one that actually hurts") is the giveaway.

**4. Negate, then reveal.**
> ✗ "So the barrier to entry was never really the compute. It was that you had to be able to afford being wrong a hundred times."
> ✗ "'Without the heuristics' is oversold, and the gap is not small."
>
> Say the thing once, in one sentence, with the concrete image in it.

**5. Anaphora pairs.** Two or three clauses opening identically.
> ✗ "Could be a hinge. Could be a bracket taking a load straight down."
> ✗ "Skip one and the blade cracks in the fire. Skip another and nothing happens at all."
>
> Fine once in a post as a deliberate beat. Twice is a tic; the draft had four.

**6. The clever quantifier.** A wry abstract measurement standing in for a fact.
> ✗ "for reasons that took a small literature to half-explain"
>
> Name the papers, or say the real thing: "the papers explaining *why* came out years
> afterwards, written by people who had been shipping it the whole time."

**7. The negation triplet.** Rule-of-three padding in a black turtleneck.
> ✗ "no teacher, no stop-gradient, no predictor, no schedules" / "No labels, no held-out probe, no waiting three days"
>
> List the items with commas and a verb, or keep the one that matters.

**8. The colon label.** A paragraph that opens with a tag instead of a clause.
> ✗ "My read: that gauge is the result, not the leaderboard." / "The dragons: the augmentation stack is still lifted from DINO."
>
> Naren flagged both in the LeJEPA LinkedIn draft. The bet and the dragons are sentences: "What I would actually build on is the gauge." / "The catch is that the augmentation stack is still DINO's."

### The humour that should be there instead

Cutting shapes 1–6 empties the slots where the jokes belong, so **fill them**. The LeJEPA draft
had wit (dry irony, "a debugging tool that got written up as a feature") and no *jokes*. Wit is
what a model produces by default; it reads as AI. The archive is goofier, more specific, more
self-deprecating:

> "GPT-4 is rumored to have 1.76 trillion parameters, which is approximately the same as the
> number of times I've contemplated whether my coffee needs another shot of espresso. The
> answer, by the way, is always yes."

**Maths is where this blog is funniest, and it is the easiest thing to forget.** Per post, aim
for at least two of:

- A joke about a specific constant. *"Seventeen. Not sixteen, not twenty. Somebody ran the ablation over 5, 17 and 41 and came back with 17, and I have more faith in that number than in any round one."*
- A joke about scale, with a real unit. *"34 floats per direction, whether the global batch is 512 images or 512,000 — less traffic than your laptop spends telling a server it is still awake."*
- An affectionate insult aimed at the model (§6d), landing after the mechanism. *"These models are lazy animals. Leave a free lunch in the loss and gradient descent will have found it before you have finished typing `wandb.init`."*
- A joke about the researchers, never unkind. *"published in 1936 by two statisticians with, I am confident, no GPUs between them."*
- A caption joke (§8). *"If it looks complicated, that's because it is. The researchers didn't make it complex just to confuse you, but I'm not ruling it out either."*

And use the **conceptual equation** (§7): the formula in words, then `specifically,`, then the
real one. It is a signature move, it is funny in its own dry way, and the LeJEPA draft shipped
without it.

### How to check

Mechanical, and worth running on every draft. First the lint, which must exit 0:

```bash
python3 .claude/scripts/prose_lint.py _posts/YYYY-MM-DD-slug.md
```

It fails on negation triplets, a second staccato run, a second run of short paragraph closes,
and three or more verbless fragments; it warns on arch commentary, colon labels, too few asides
or questions, and a landing-line ratio above one in four (`--linkedin` tightens it for posts).
Then the landing-line list, which is the part a script cannot judge:

```bash
# landing-line density: aim for roughly 1 paragraph in 6, not 1 in 3
python3 - <<'EOF'
import re
t = open("_posts/YYYY-MM-DD-slug.md").read().split("---\n",2)[2]
ps = [p.strip() for p in t.split("\n\n")
      if p.strip() and not p.startswith(("#","|","$$","!["))]
land = [re.split(r'(?<=[.!?]) ', p.replace("\n"," "))[-1] for p in ps
        if len(re.split(r'(?<=[.!?]) ', p.replace("\n"," "))) > 1
        and len(re.split(r'(?<=[.!?]) ', p.replace("\n"," "))[-1].split()) <= 12]
print(f"{len(land)}/{len(ps)} paragraphs end short")
for l in land: print("   ", l)
EOF
```

Then read that list. **Every line in it must be a joke or a fact.** Any that reads like advice,
wisdom or a moral is the defect this section exists to catch.

---

## 19. What Naren changes by hand: the GRPO edit pass

Naren edited the published GRPO post (blog33, September 2026) by hand after it had passed §13,
§18, the humanizer and the lint clean. None of the edits was a vocabulary fix and none was a §18
shape. They are the difference between a draft that is *correct* and one that sounds like him
explaining the thing across a table. Eleven habits, each with the actual before and after.

**1. Pin the conceit's character to its technical term, in brackets, every time the mechanism
needs it.** The draft called the reward model "the marker" and expected the reader to hold the
mapping for 2,500 words. Naren renamed it and then kept pinning the real name to it:
> ✗ "we asked people which of two answers they preferred" → ✓ "we asked people which of two answers they preferred (a human ranker)"
> ✗ "The marker is gone. The teacher predicting ranks is still at the front of the room" → ✓ "The TA (ranker) is gone. The teacher predicting ranks (critic) is still at the front of the room"
> ✗ "Reference and reward models sit frozen" → ✓ "Reference (frozen policy) and reward models sit frozen"
> ✗ "two networks that will never emit a token" → ✓ "two networks (critic and reference) that will never emit a token"
> ✗ "train a second network to predict it" → ✓ "train a second network (critic) to predict it"
>
> The conceit carries the intuition and the bracket carries the name. A reader skimming for the
> mechanism must never have to scroll back to find out who the TA is.

**2. The conceit's props come from the reader's real world, and each one says what the thing
does.** "Marker" became "ranker" because ranking is what a reward model does. The human reading
papers became a TA. The "photocopier" the centre kept in the last line became an "OMR machine",
and "a rank list on the noticeboard" became "the scores on the noticeboard". The coaching centre
is an Indian one; its furniture should be too.

**3. Talk to the reader instead of staging the conceit.**
> ✗ "Hold on to a coaching centre for the rest of this, because the whole post runs on one. Two hundred students, one classroom" → ✓ "I want you to now think about a coaching centre: two hundred students, one classroom"
> ✗ "Do one group by hand. Eight answers to the same question" → ✓ "Let's do one group by hand. Let's say group size is 8, so eight answers to the same question"
> ✗ "Price it out for a 7B policy." → ✓ "Now check the price this setup has for a 7B policy."
> Added, unprompted: "That's it." / "If you think about it, we humans do the rough work all the time for complex problems." / "…and somebody else sat through the meeting about it smh"
>
> The draft's imperatives are a writer directing a reader. "I want you to", "Let's say", "Now
> check" are a person talking. "smh" and "That's it." are the 2026 form of the 2021 emoticons:
> one or two per post, in the lighter spots, never in the mechanism.

**4. Put the small words back.** Each of these is a softener the draft had sanded off because it
looked like padding:
> "expensive" → "pretty expensive" · "a question about the boiling point" → "a simple question about the boiling point" · "turned PPO loose" → "set PPO loose" · "the useful problems are the ones sitting near a coin flip" → "the useful problems are the ones can be kind of hard, but not too hard"
>
> A person explaining across a table says "pretty", "kind of" and "simple". A draft with none of
> them reads clipped, which is its own AI tell. Not everywhere: where the spoken version would
> have them.

**5. Split any sentence that runs long, and open the next one with So, And or But.** If a
sentence is carrying two ideas, or has a ", so" or ", and" in the middle of it, it is two
sentences:
> ✗ "…has to write out the good answer every time, so instead we asked people…" → ✓ "…every time. So instead we asked people…"
> ✗ "…$G$ is the group size, and every token $t$ of answer $i$ carries…" → ✓ "…$G$ is the group size. Every token $t$ of answer $i$ carries…"
> ✗ "Sampling a group and keeping whatever checks out rewards any habit that raises the hit rate, and going back over your own working raises the hit rate." → ✓ "Sampling a group and keeping whatever checks out, rewards any habit that raises the hit rate. And turns out, going back over your own working raises the hit rate."
> ✗ "…unremarkable if everyone did, so the gradient needs a baseline to subtract" → ✓ "…unremarkable if everyone scored 1. So the gradient needs a baseline to subtract"
>
> The draft joined clauses with ", so" and ", and" to get the long-sentence rhythm §5 asks for.
> Naren split every one of those he found. The rule is simple: long sentence, full stop, and a
> conjunction opening the next one. The long-then-short rhythm of §5 still holds; "long" just
> means one idea with its qualifiers, not two ideas glued together.

**6. Put a comma where the reader needs to find the verb.** Three of the edits added nothing
but a comma, each after a subject phrase long enough that the reader would otherwise run past
the verb:
> ✗ "Anything it scores generously that it should not is a hole" → ✓ "Anything it scores generously that it should not, is a hole"
> ✗ "Sampling a group and keeping whatever checks out rewards any habit that raises the hit rate" → ✓ "Sampling a group and keeping whatever checks out, rewards any habit that raises the hit rate"
> ✗ "whether a room marked only against an answer key can ever learn" → ✓ "whether a room of students marked only against an answer key, can ever learn"
>
> And a comma after every introductory phrase: "And turns out, going back over your own working
> raises the hit rate", "If you think about it, we humans do the rough work all the time". A copy
> editor would strike the first three; Naren adds them on purpose, because a subject that is a
> whole clause needs a mark where it ends. So: a comma after a long subject before its verb,
> after an introductory phrase, and before "so" and "but" ("group size is 8, so eight answers",
> "kind of hard, but not too hard"). Do not add commas between a short subject and its verb.

**7. Say why, not just that.**
> ✗ "for the first few weeks of any new syllabus he is wrong." → ✓ "…he is wrong because the students haven't learnt much."
> ✗ "unremarkable if everyone did" → ✓ "unremarkable if everyone scored 1"
> ✗ "Push that into the gradient and you are done; there was never a value network in the room." → ✓ "…and you are done; you don't need a value network in the room."
> ✗ "The setup is deliberately stripped: take DeepSeek-V3-Base" → ✓ "The setup is deliberately stripped of any RLHF: take DeepSeek-V3-Base"
>
> A line that leaves the reason implicit reads clever to the writer and opaque to the reader.
> Spell the mechanism out in the clause, even when it costs the rhythm.

**8. Link and gloss every benchmark, dataset, tool and model on first mention.** The draft linked
the papers and left the benchmarks bare. Naren added six links in one pass: a proof in
[Lean](https://lean-lang.org/), grade school math [GSM8K](https://huggingface.co/datasets/openai/gsm8k),
[MATH](https://huggingface.co/datasets/qwedsacf/competition_math),
[AIME 2024](https://artofproblemsolving.com/wiki/index.php/American_Invitational_Mathematics_Examination),
[MATH-500](https://huggingface.co/datasets/HuggingFaceH4/MATH-500), [Olmo 3](https://arxiv.org/abs/2512.13961).
The gloss is two or three plain words in front of the link, so a reader who has never met GSM8K
knows what kind of test it is without clicking. §10 has the link targets.

**9. A numbered list for anything the sentence is straining to enumerate.**
> ✗ "run GRPO against two rule-based rewards. Accuracy, from the answer key. Format, which asks only that the working sits inside `<think>` tags." → ✓ "run GRPO against two rule-based rewards:" then `1. Accuracy, from the answer key.` / `2. Format, which asks only that the working sits inside <think> tags.`
>
> §14 already says numbered lists are the archive's main explanatory device. The draft wrote the
> list as two fragments to protect the prose rhythm; Naren undid that.

**10. Keep the conceit's images, cut the incidental ones.** The coaching centre stays. The one-off
writerly flourishes went, each for the plain word or the field's own word:
> "the bill" → "the cost" · "arrived as subsection 4.1" → "came as subsection 4.1" · "Their reading is" → "Their conclusion is" · "gradient descent finds holes faster than anyone can patch them" → "gradient descent can exploit holes faster than anyone can patch them" · "sitting near a coin flip" → "kind of hard, but not too hard"
>
> "Exploit" is what the RL literature says and what the reader already knows. A metaphor that is
> not the conceit is competing with it.

**11. Everyday examples for an abstract category.**
> ✗ "A memo, a diagnosis, a design review, or a piece of code that is correct and horrible all fall outside it." → ✓ "A memo, a diagnosis, a design review, or a piece of code that is correct. Tasks like summarization and email writing all fall outside it."
>
> When the post says a method does not cover some class of task, name two tasks the reader does
> every day.

**What he did not touch.** The conceit, the numbers, the tables, the honest cons, the maths
jokes, the landing lines, the sign-off. Every §17 and §18 item held. The edits were local, all in
the direction of plainer, and they added words: the post came out about 80 words longer. And
nothing was cut for length: every edit either added a word, a comma, a link or a full stop.

**Mechanics caught in the same pass.** `$1/|o_i|$` turned its whole paragraph into a kramdown
table, and a stray `$$` after it swallowed the next formula. Both are in §7 now and the lint
fails on them.

---

## 20. Write for a reader with almost no ML: the September 2026 pass

Naren's rule, September 2026, after a review of the quantization, distillation and Mamba posts
(blog34-36): **anyone should be able to understand the post with minimal ML knowledge.** Those
three drafts passed §13, §18, §19 and the lint clean, and still read as written by a model for
people who already knew the subject. This section is what he asked for instead.

**1. One idea per sentence. Simple statements.** Several clauses glued together to make one
point is the tell this section exists to catch. If a sentence has two or more of ", and",
", so", ", which" or ", but" in it, it is two or three sentences. Split it, and open the next
one with So, And or But (§19.5). The lint warns on these ("chained sentences") and on anything
over 35 words.
> ✗ "LLM.int8() splits each matrix multiply in two: the outlier channels go through in 16-bit, everything else, which is more than 99.9% of the values, goes through in 8-bit, and the two halves are added back together." → ✓ "LLM.int8() splits each matrix multiply in two. The outlier channels go through in 16-bit. Everything else, which is more than 99.9% of the values, goes through in 8-bit. Then the two halves are added back together."
> ✗ "At inference it writes its own, and four tokens in it is somewhere the teacher would never have gone, and nobody has ever shown it what to do out there." → ✓ "At inference it writes its own. Four tokens in, it is somewhere the teacher would never have gone, and nobody has ever shown it what to do out there."
> ✗ "If $\bar{A}$ changes at every step then there is no single convolution kernel, so no FFT, and you are back to a for-loop over 960,000 samples." → ✓ "If $\bar{A}$ changes at every step, then there is no single convolution kernel and so no FFT. You are back to a for-loop over 960,000 samples."
>
> Exempt: the "where $x$ is …" line that defines an equation's symbols, the §3 thesis line, and
> a sentence that is really a list (better still, make it a numbered list, §19.9).

**2. Start from the basics and build up.** Assume the reader knows what a neural network is
and not much more. Before a technical term is used, say what it is in plain words, or pin it in
brackets (§19.1). Each section should need only what the sections above it taught. When a post
needs control theory, GPU memory hierarchies, FFTs and a benchmark suite in its first two
sections, it is doing too much for one post (see "Split test" below).

**3. Make the problem land before the fix.** The reader should be able to say, in one sentence
of their own, what goes wrong before the post names the method that fixes it. Give the problem
its own paragraph, with a number or an everyday example, and do not start the solution in the
same sentence.

**4. The patterns caught in blog34-36**, each with the fix that shipped. These are §18 shapes
that survived the lint because they were phrased a little differently.
- **Quotable paragraph closes** (§18.1).
  > ✗ "The size of a weight tells you almost nothing about whether it matters, and the size of what runs through it tells you almost everything." → ✓ "So you pick the important channels by the activations running through them."
  > ✗ "It has been sitting there the whole time. It just needed a teacher worth copying." → cut.
  > ✗ "And then the field did the thing that actually works, which is to stop arguing." → ✓ "And then the field stopped arguing and built hybrids."
  > ✗ "That is the capacity gap showing up in 2015, in a footnote, wearing a disguise." → ✓ "That is the capacity gap, already showing up in 2015."
  > ✗ "A labelling budget of zero and a teacher is enough." / "Everything since is a variation on that split." → cut.
- **Negate, then reveal**, including the "stopped being X and became Y" form (§18.4).
  > ✗ "The label is not wrong. The bottle really is a rose. It is just that a label has room for one word" → ✓ "The label is right, because the bottle really is a rose. But a label only has room for one word"
  > ✗ "The selective pad is not remembering harder. It just declined to start the timer during 'and, er'." → ✓ "The selective pad kept the number because $\Delta$ was close to zero during 'and, er'. So almost nothing faded."
  > ✗ "So the question stopped being how small you can get a model and became which parts of it were ever worth sixteen bits." → ✓ "So the question now is which parts of a model were ever worth sixteen bits."
  > ✗ "The 2B and 9B are not pretrained on next-token prediction at all. They are pretrained on the 27B teacher's full distribution" → ✓ "Instead of plain next-token prediction, the 2B and 9B are pretrained on the 27B teacher's full distribution"
- **The narrator staging the conceit** (§19.3). A sentence whose only job is to point at the
  metaphor.
  > ✗ "The perfume house has been the same building the whole way through." / "The booth has been the same three square metres the whole way through this post" → cut, or say what changed: "From S4 to Mamba-3, what changed is only what the interpreter is allowed to do with the pad."
  > ✗ "Everything else in this post is the same evening it always was." → cut.
- **Verbless openers and triptychs** (§18.2).
  > ✗ "Same architecture, same training run, same answers to within a rounding error. One card." → ✓ "It is the same model, and it gives the same answers to within a rounding error. And it fits on one card."
- **Vague attribution and portentous framing.**
  > ✗ "the calibration set is doing more work than anybody admits" → ✓ "And then there is the calibration set."
  > ✗ "Nobody likes this result" → cut. ✗ "people still find it surprising" → ✓ "I still find it surprising" (§5: "I" for opinion)
  > ✗ "That is the tension everything since has been working on." → ✓ "Every method since has been trying to fix that."
  > ✗ "the shape of the finding is the interesting part. The outliers are not scattered about." → ✓ "It found that they bunch up."
- **Stray images competing with the conceit** (§19.10).
  > ✗ "a lovely thing to find at the bottom of two different ladders" → cut. ✗ "the shape of the bill" → ✓ "the shape of the cost". ✗ "a batching story" → ✓ "down to batching". ✗ "which surface of the teacher you may touch" → ✓ "where you tap the teacher"
- **Emphatic restatement.**
  > ✗ "Selection breaks the trick that made S4 trainable, and it breaks it completely." → ✓ "Selection breaks the trick that made S4 trainable."
  > ✗ "Both of those are true at once, and after a decade nobody…" → ✓ "After a decade, nobody…"
- **The tacked-on kicker.** A last sentence added only to make the number feel bigger. Naren:
  "looks like AI written. I never write like this."
  > ✗ "so that session is around $1.5 \times 10^{16}$ pairs. And nobody has multiplied anything by a weight yet." → ✓ end on "pairs." The number is the point; let it land on its own.
  >
  > Same family: "and we haven't even started", "and that's before X". The lint flags "nobody has … yet".
- **Unglossed shorthand** (§19.8).
  > ✗ "That buys W8A8 on OPT-175B" → ✓ "That buys W8A8 (8-bit weights and 8-bit activations) on OPT-175B"
- **A flourish hiding a factual slip.** "Three students, three decades apart" was over rows
  dated 2015, 2015 and 2024. Check every number in a caption against the table it describes.

**What stays.** Jokes that are jokes ("Four and a half bits per weight, which is a lovely thing
to say out loud to a hardware engineer and watch what happens"), the conceit, the numbers, the
worked examples. The lint's arch-commentary list now carries the phrases above.

**Split test.** Split a post into two when the basics it needs (point 2) and the method it is
about cannot both be explained plainly in about 3,500 words. The natural cut is after the
problem and its fix have landed, with the engineering, the follow-up models and the honest cons
going to part two. Each part keeps the same conceit and gets its own worked example.

---

## 21. Answer the reader's next question: the Mamba Q&A pass

Naren read the published Mamba part 1 (blog36) as a reader and came back with a list of
questions. Every one was a gap the post should have closed itself: where does $e^{\Delta A}$
come from, what are $\bar{A}$ and $\bar{B}$, is speech really one token per sample, how long is
the pad, how does a kernel "grow", is $y_t$ really one number, how do the dimensions talk, where
are these models used, why the name. The post had passed §13, §18, §19, §20 and the lint. None
of those checks ask what a curious reader will ask next. This section does. The fixes that
shipped in PR #62 are the examples.

**1. Every formula says where it came from.** No equation arrives from nowhere. Give one or two
plain sentences of derivation, or the intuition that forces the form ("the only function whose
rate of change is proportional to itself is an exponential"). Every symbol gets defined,
including the barred, hatted and discretised versions. "Along with a matching $\bar{B}$" is not
a definition. Write $\bar{B}$ down, and say what the bar means in words ("per step").

**2. Say what the toy example is a slice of.** A worked example with one number in and one
number out is fine, but say so, and say what the real thing looks like: "this is one channel of
5,120, and a real pad holds 16 numbers, not one". Then close the loop to the model's actual
output. If the post is about a language model, one paragraph says how the thing it explained
turns into the next word. Otherwise the reader looks at $y_t$ and asks how a single number
predicts a word.

**3. Flag a hypothetical as a hypothetical.** "Treat each audio sample as a token" is a fine
thought experiment. But say in the next breath what real systems do (spectrograms, about 50
tokens a second) and why the thought experiment still matters. A reader who knows a little will
otherwise think the post got the basics wrong. A reader who knows nothing will learn something
false.

**4. Metaphor words must not collide with technical words.** "Pad" for the state sat right
next to CNN padding, and Naren asked whether the pad was a fixed size "because CNNs expect it".
When the conceit's word is also a term of art nearby (pad, cache, head, bank, window, kernel),
either choose another word or say once, plainly, which one you mean.

**5. Say what is stored and what is computed, and what sets each size.** "The kernel is as long
as the sequence" raised "how does it keep growing?". The answer, that the model learns $A$, $B$
and $C$ and the kernel is generated from them, was one sentence away. For anything with a size
(a kernel, a state, a context window, a cache), say what fixes that size, whether it was learned
or computed, and what happens when the input gets longer.

**6. Compare against what the reader already knows.** Any claim about memory, length or cost
gets a sentence on how the familiar alternative handles it. The Mamba post said the pad "never
grows" but never said how far back it reaches, or what a Transformer's limit actually is (the
training length, which RoPE does not remove). The reader filled that gap with a wrong guess.

**7. Show how the pieces connect, not only the piece.** If the mechanism works on one unit (a
channel, a head, a patch, an expert), say how the units talk to each other, and draw it. The
figure for a named architecture (§8) shows the whole block. It draws the part the worked example
computes as a zoom and labels it that way, so the reader can place the maths in the picture.

**8. Figures a reader can follow at first look.** Naren sent the first Mamba block diagram back
with "not fully clear". The redraw that shipped (blog36, Figure 2) follows these rules:
- One message per figure, stated in the title or a legend, e.g. "orange boxes mix the channels,
  blue boxes work on one channel alone".
- Numbered steps in reading order when there are more than three stages.
- Repeated units drawn as parallel tracks, so "per unit" and "across units" are visible without
  reading anything.
- A zoom panel for the part the worked example computes.
- No line crosses text, and no label overlaps a box. Render it, look at it, and fix every
  overlap before committing.
- Put the explanation in the caption: what the colours mean, what the zoom is, how to read it.

**9. Say where it is used.** Any post about a method has a short section, a few bullets, on who
ships it today, for what, and where it loses. The reader wants to know whether this is a lab
curiosity or something inside products they use. Keep it to what you can source, and point to
part 2 if part 2 covers it in depth.

**10. Explain the name** when it is not self-explanatory (Mamba, JEPA, LoRA, Flux). One or two
sentences. If the authors never explained it, say so and give the usual story as the usual
story.

### How to check: the ten-questions test

After the §17 checklist, reread the finished post as the §20 reader, one section at a time. At
the end of each section, write down the question that reader would ask next. Then ask yourself
if the post answers it within a paragraph or two. If it does not, add the answer or cut the
claim that raised it. A post that leaves more than two such questions open is not finished.
When a subagent is available, hand it the post alone with this brief: "You know what a neural
network is and nothing more. List the ten questions you would ask the author after reading
this, in order." Then answer every one it raises in the post, or decide in the PR why not.
