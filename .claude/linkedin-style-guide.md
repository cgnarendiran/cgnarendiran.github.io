# Narendiran Chembu — LinkedIn Post Style Guide

Reference for the LinkedIn job that writes a companion post for each new entry on
**cgnarendiran.github.io**. Built from a close reading of Naren's ten LinkedIn posts published
between September 2025 and August 2026, seven of which promote a blog post.

This guide sits on top of `.claude/writing-style-guide.md`. That guide owns the **voice**; this one
owns the **LinkedIn form**. Where they disagree on voice, the blog guide wins. Where they disagree
on formatting, this one wins, because LinkedIn renders plain text and truncates the first lines.

---

## 1. The evidence

| LinkedIn date | Promotes | Hook type | Words | Emoji | Link | Hashtags |
|---|---|---|---|---|---|---|
| 2025-09-08 | (opinion: DeepMind embeddings paper) | Blunt claim | ~200 | many | none | 4 |
| 2025-09-19 | KV Caching & MLA | Famous line, then twist | ~150 | several | body, 👇 | 5 |
| 2025-10-20 | RoPE | Famous line, then twist | ~170 | a few | body, 👇 | 5 |
| 2025-12-09 | MoE | Famous line, then twist | ~230 | several | body, 👇 | 5 |
| 2025-12-19 | Cross Entropy | The question you never asked | ~200 | a few | body, 👇 | 7 |
| 2026-02-09 | ViT | Famous line, then twist | ~200 | a few | body, 👇 | 4 |
| 2026-03-31 | VLM | Absurd pairing | ~210 | a few | body, 👇 | 5 |
| 2026-05-14 | VLA | Quoted meme, then "well, actually" | ~340 | none | body, "Link below:" | 5 |
| 2026-06-07 | (opinion: world models) | Blunt claim | ~400 | none | body, plain | 5 |
| 2026-08-09 | (personal: IGVC, Michigan) | Date, place, sensory detail | ~380 | none | none | 0 |

Two trends matter.

**Emoji are gone.** Eight of them in September 2025, three by spring 2026, zero in every post
since May 2026. Write like the 2026 posts.

**Posts got longer and more opinionated.** The early ones summarise the blog. The recent ones argue
a point and use the blog as the evidence. The world-models post is the clearest example: a claim in
the first line, a fair reading of the other side, a one-line test, then the verdict.

Every blog promo puts the link in the body near the end, tags Fast Code AI, and closes with
hashtags. None of them end with "Fin."

---

## 2. The shape of a blog-promo post

| # | Beat | Notes |
|---|---|---|
| 1 | **Hook** | One or two lines, under 200 characters before the first blank line. LinkedIn cuts the preview at roughly 210 characters, so the hook has to work on its own. It names the concrete object of the conceit (police sketch, coffee shops, a paperweight) and makes sense to someone who never opens the link. Never lift the blog's opening line: the blog had three paragraphs to set the image up, the post has one sentence. "A witness never paints you the room" failed this; "Ask a witness to describe a suspect and you get a police sketch" passes |
| 2 | **The setup** | Two to four short lines. What everybody believed, or what the last post achieved |
| 3 | **The idea in plain words** | One paragraph. The blog's conceit compressed to one image, then the mechanism in one or two sentences. No equations |
| 4 | **One concrete thing** | A number, an ablation, a failure. "Eats 16GB of VRAM for a 2GB checkpoint." "256-bin discretization has no chance at threading a USB cable" |
| 5 | **The dragons** | One line of honest cons, lifted from the post's honest-cons section. Naren's own word for this is "dragons" |
| 6 | **The bet or the turn** | Where it's going, in his opinion. "My bet for the next breakthrough: ..." / "That's the moonshot." |
| 7 | **The pointer** | One line saying what the blog post is, then the URL on its own line |
| 8 | **Series line** | Only if the post is part of a series. "Next up: ... Stay tuned." for a part 1. "Part 2 of my X series" for a part 2 |
| 9 | **Hashtags and mention** | 4 to 6 hashtags on one line, then the Fast Code AI mention |

Beats 5, 6 and 8 can be merged or dropped in a short post. Beats 1, 3, 4, 7 and 9 are not
optional.

---

## 3. Hooks, with the real ones

**Famous line, then a twist.** The most used opener, five of the seven promos.
> "Attention is All You Need"... but that says nothing about how we handle fast inference for
> insanely large trillion-parameter models.

> CNNs are great. But Attention is still all you need!

> "Attention is All You Need"... but did we really pay attention to this part?

**The question you were embarrassed to ask.**
> "Why does cross-entropy loss use a log function? Why not sin or tan or x^2 or 1/x or e^x?"

> Why sine for even and cosine for odd indices? What's that random 10,000 doing there? And why is
> the index i sitting inside the exponent like it owns the place?

**The absurd pairing.**
> LLMs could write like Shakespeare but had never seen a sunset. ViTs could recognize an image of
> a cat, but couldn't tell you why it's cute.

> The most articulate LLMs on Earth couldn't pick up an apple in early 2022.

**The blunt contrarian claim.** The two best-argued posts open this way.
> Most of the AI systems being sold as "world models" are not world models.

**Quoted meme, then "well, actually".**
> "I want AI to do my laundry and dishes so I can do art and writing, not the other way around".
> Well, it is already doing it!

Pick the hook from the blog post's own opening. The blog opens on a conceit or an absurd image;
the LinkedIn hook is that image in one line.

---

## 4. Moves in the middle

- **From / to.** "We moved from: Inductive Bias: 'Here's how you should see.' to Data Scale:
  'Figure it out yourself.'" Two lines. No arrows, no 👉.
- **The staccato triplet.** "Pixels became tokens. Images became sequences. Vision became another
  language." / "Not Linear Algebra. Not Calculus. But Information Theory." Once per post at most.
- **The recipe in one line.** "Eyes (frozen ViT) + Brain (frozen LLM) + Translator (a tiny MLP)."
  / "Take a VLM that already knows what an 'egg' is and what 'carefully' means. Convince it that
  motor commands are just another token to predict."
- **The dry aside**, in parentheses, once. "(it's better to call it 'surprise' or 'chaos' imo
  actually)" / "(hope they release it soon to the public)".
- **The affectionate insult**, aimed at models. "The LLM doesn't even know it's seeing an image;
  it just thinks it's reading a very strange language." / "the world's most articulate paperweight".
- **The failure anecdote from the post.** "we gave a picture of an ice-cream bowl instead of a
  road scene to a driving VLA, and it confidently said go forward :p"
- **Rhetorical question, answered at once.** "So what do we do? We take a shortcut. More
  precisely, we route."
- **The one-line test.** "Does it predict consequences?" Then the verdict.
- **Ask something.** At least one rhetorical question in the first half, answered at once: "So why
  hasn't everyone switched?" / "Sounds amazing, right?" / "So what do we do?" A post with no
  question in it reads like a summary.
- **One number.** "Eats 16GB of VRAM for a 2GB checkpoint." Two at most. The first JEPA promo
  dumped five numbers into four sentences and read like a benchmark table.
- **Vary the rhythm.** No more than two consecutive paragraphs ending on a fragment aphorism
  ("Worth it." "And the dragons." "My read:"). When every paragraph lands a zinger, the sameness
  is the tell, and the humanizer cannot see it because it works one sentence at a time.

---

## 5. Voice, what carries over from the blog

- Physical verbs: shove, slice, bolt on, squash, glue, tear out. Never leverage, utilize, unlock,
  harness.
- "imo", "pretty much", "insanely", "Oppa", "yeesh". A person typing fast.
- First person for opinion and bets: "My bet", "what I'm noticing", "I broke it all down". "We"
  for the field and for the walkthrough. At least two "I" sentences per post: what Naren did
  (wrote it, went back to basics, noticed something) and what he thinks. What §8 bans is
  invented events, not the first person.
- One emoticon at most, `:p` or `:)`, and only on a lighter topic. No emoji bullets, no 🚀, no 👀.
  One 👇 before the link is the only surviving emoji and even that is optional now.
- Affectionate insults toward models, never toward people or papers. Fei-Fei Li gets "the
  Godmother of AI" and a fair reading of her argument, then a disagreement.

---

## 6. What changes for LinkedIn

- **Plain text.** No markdown. No headings, no bold, no italics, no backticks, no tables.
  Asterisks and pound signs print literally.
- **No math.** If the point needs an equation, describe it: "the loss compares two descriptions and
  never touches a pixel".
- **Short paragraphs.** One to three sentences, blank line between them. A single-sentence
  paragraph is a normal move.
- **Numbered lists** are fine (the world-models post uses one). Dash bullets are fine. Emoji
  bullets are retired.
- **Names, not links.** Mention papers and models by name. The only URL in the post is the blog
  link. No arXiv links, no shorteners.
- **Length: 120 to 220 words, target 170, hard stop at 250 (about 1,600 characters).** RoPE is
  170 words, KV Caching 150, VLA 340, and that one is the ceiling, not the norm. The first JEPA
  promo was written to an older 320-word ceiling and read like a summary.

---

## 7. The pointer and the tail

The last third of every promo looks like this, with small variations:

> Full deep-dive (the trilogy: ViT, VLM, VLA) on the blog. Link below:
> https://cgnarendiran.github.io/blog/vla-pixels-to-tokens/
>
> #AI #Robotics #VLA #AutonomousDriving #Causality @Fast Code AI

Other pointer lines he has used: "I broke it all down in my new blog:", "Part 2 of my Pixels to
Tokens series breaks down the full VLM stack:", "In this blog, I broke down where the log comes
from...", "If you've ever wondered how modern frontier LLMs actually scale ... you might want to
read this blog:".

Rules:

- The URL is the canonical `https://cgnarendiran.github.io/blog/<slug>/`, on its own line, in the
  body. Not in a first comment. Every one of his promos has it in the body.
- 4 to 6 hashtags, CamelCase for multi-word tags, specific to the post (`#JEPA`,
  `#SelfSupervisedLearning`, `#WorldModels`), plus at most one broad one (`#AI`). Series posts add
  the series tag in the lowercase form he uses (`#pixelstotokens`).
- Mention Fast Code AI at the very end, after the hashtags, as
  `@[Fast Code AI](urn:li:organization:70969206)`. That is the mention syntax Postbeam stores for
  his published posts. If it comes back from `get_post` mangled or as literal text, replace it
  with plain `Fast Code AI`.
- No sign-off. No "Fin.", no "Thanks for reading", no question to the audience.

---

## 8. Truth rules

The job writes about the blog post and nothing else. It has not had a conversation with Arjun
Jain, it did not go to Michigan, and it does not know what Fast Code AI is working on this week.

- Every claim, number and anecdote comes from the blog post or the papers it cites. Nothing else.
- No invented first-person experience. No "we ran into this at Fast Code AI", no "a colleague
  asked me", no "at 2am I was debugging". Naren adds those himself in the review window if he
  wants them.
- No claim about Naren's role, employer or projects beyond what the post itself says.
- Do not overstate the post. "I broke down" is fine. "I solved", "I discovered" are not.
- Read the honest-cons section before writing the bet. The bet has to survive the cons.

---

## 9. Banned

Everything in §13 of the blog guide, plus the LinkedIn strain of the same disease:

- "I'm thrilled/excited/humbled to announce", "Big news", "🚀"
- "Let that sink in", "Read that again", "Agree?", "Thoughts?", "What do you think?"
- "Here's the thing", "Hot take:", "Unpopular opinion:", "Most people don't know..."
- "game-changer", "mind-blowing", "insane" as praise (Naren uses "insanely large" as a size word;
  that is fine)
- Broetry: one-word lines all the way down. The staccato triplet is one move, not the whole post.
- "In this post, I explore..." abstract voice. It's a post, not a paper abstract.
- Engagement bait: "comment X and I'll send you", "repost if", "follow for more"
- Ending on a question to the audience ("Thoughts?"). His posts end on the link and the tags.
  Rhetorical questions inside the post are required (§4); this rule is about the last line.

---

## 10. Media

Attach the blog's cover image via its live URL: `https://cgnarendiran.github.io/` plus the
front-matter `image:` path. Alt text is the post's "On the cover" caption without the italics.
One image. No carousels, no video.

---

## 11. Two exemplars, verbatim

Mention and hashtag syntax normalised to plain text; the links are as posted.

### The VLA promo (May 2026), the strongest of the series

> "I want AI to do my laundry and dishes so I can do art and writing, not the other way around".
> Well, it is already doing it!
>
> The most articulate LLMs on Earth couldn't pick up an apple in early 2022. By 2024, the same
> architecture was picking up apples, folding laundry, and driving cars. In 2026, things are looking
> up in this space with Helix from Figure and Alpamayo from NVIDIA.
>
> Welcome to Vision-Language-Action (VLA) models. The recipe is simple. Take a Vision-Language-Model
> (VLM) that already knows what an "egg" is and what "carefully" means. Convince it that motor
> commands are just another token to predict. The same Transformer that summarizes your email can
> now drive your car or fold your shirt, given the right fine-tuning data. We have essentially given
> brains to our robots.
>
> For autonomous driving specifically, the old stack of perception, prediction, and planning is
> collapsing into one end-to-end VLA model. Your next Tesla may run on something like this.
>
> But what I'm noticing is that the bottleneck has shifted. The question is no longer "can the AI
> see the world clearly?" It's "can it reason about why things happen?" or "why does it predict a
> certain action?" That's a much harder problem. What's worse is that we gave a picture of an
> ice-cream bowl instead of a road scene to a driving VLA, and it confidently said go forward :p
>
> At Fast Code AI, (in collaboration with Renesas Electronics), this is what we've been working on:
> an evaluation framework that tests whether driving models actually reason about cause and effect,
> or just pattern-match on common scenarios. For safety-critical systems, that distinction matters
> a lot.
>
> My bet for the next breakthrough: it'll come from world models that understand causality and
> preserve it while predicting actions.
>
> Today's VLAs hallucinate trajectories that are close to the robot data deficit. They also predict
> actions while hallucinating the why. Crack the why, and you get grounded reasoning and genuinely
> safe and useful systems. That's the moonshot.
>
> Full deep-dive (the trilogy: ViT, VLM, VLA) on the blog. Link below:
> https://lnkd.in/dBzXxXyu
>
> #AI #Robotics #VLA #AutonomousDriving #Causality

Note the Fast Code AI / Renesas paragraph. That is Naren's own knowledge of his own work. The job
must not write a paragraph like it (§8). Everything else in this post is the template.

### The world-models opinion piece (June 2026), the argument voice

> Most of the AI systems being sold as "world models" are not world models.
>
> Fei-Fei Li, the Godmother of AI, just raised $1.23 billion for her company World Labs and
> published the cleanest definition of the term yet. It is also imo, quietly, a sales pitch.
>
> Her argument: the phrase got so overloaded and overused everywhere, that it makes sense to broadly
> classify the world models based on their use case into three types:
>
> 1. Renderers, which output pixels for you to look at. eg. Nano Banana (Google)
>
> 2. Simulators, which output state, the geometry and physics underneath (Marble, World Labs)
>
> 3. Planners, which output actions, what to do next. eg. Alpamayo-R1 (NVIDIA)
>
> So the classification is based on outputs. Useful. But notice the move. The category she crowns
> the linchpin in her post, the simulator, is exactly where her own product, Marble, is placed. But
> what most people don't consider: none of that is the actual definition.
>
> The realest definition of world model is not new. It comes from model-based reinforcement
> learning. A world model is an action-conditioned model of the real world you can roll forward to
> plan. The test is one line.
>
> Does it predict consequences?
>
> How well are you able to approximate this state transition term: p(s' | s, a)
>
> Shove a glass off a table, and it should know the glass falls and shatters. Run the popular
> systems through that test.
>
> Google's Nano Banana paints a flawless street with no idea what is down it. A gorgeous renderer.
> NVIDIA's Alpamayo picks a driving move based on correlations. A capable planner. Neither one of
> them models the world.
>
> A world model is not defined by what comes out of it. Not pixels, not state, not actions. It is
> defined by whether it knows what happens next given some action. Reliably.
>
> Most things out there are wearing the label 'world model' are renderers in a costume. And to be
> fair, nobody has cracked it. Not World Labs, not anyone. Genie3 from Google and JEPA from Yan
> LeCun comes close to it. We have spent billions approximating what a five-year-old does for free,
> which is learn how the world works just by watching.
>
> By the strict definition, a video game engine is closer to a world model than most of what got
> funded this year.
>
> #worldmodels #worldlabs #feifeili #marble #jepa
>
> Fei Fei Li's post: https://lnkd.in/gKnNjG6H

This is not a blog promo, but it is the voice the promos are drifting toward: a claim, a fair
reading of the other side, a one-line test, a verdict. Note "the realest", "imo", "Shove a glass
off a table", and that the typos ("Most things out there are wearing", "comes close") survived.
Don't manufacture typos, but don't polish the voice out either.

### The RoPE promo (October 2025), the length to aim for

170 words. Three questions, two "I" sentences, one running joke, one pointer line. Drop the
emoji, which are 2025-era, and keep everything else.

> "Attention is All You Need"… but did we really pay attention to this part?
>
> We've all read the paper.
> We've all nodded at those weird sine–cosine Positional Embedding equations at the end of the
> Model Architecture section.
>
> But if you're honest, you probably thought:
> - Why sine for even and cosine for odd indices?
> - What's that random 10,000 doing there?
> - And why is the index i sitting inside the exponent like it owns the place?
>
> Most of us just shrugged and said,
> "Eh, I know what Q, K, and V are… that's enough, right?"
>
> But those two little equations hide a ton of intuition about how Transformers actually
> understand order and why Rotary Positional Embeddings (RoPE) were the next big twist. I broke
> it all down in my new blog:
>
> https://lnkd.in/gRzYVxrg
>
> #PositionalEmbeddings #RoPE #Attention #Transformers #AI @Fast Code AI

### The JEPA promo, before and after (September 2026)

The routine's first draft ran 320 words and opened "A witness never paints you the room. She
says: tall, grey coat, walked with a limp." Naren's verdict: reads like AI, too long, and the
first sentence is in limbo without the words "police sketch". It had five numbers in one
paragraph, no question, one "I", and eleven paragraphs each ending on a zinger. The 209-word
replacement that went live in its place:

> Ask a witness to describe a suspect and you get a police sketch: tall, grey coat, walked with a limp. Ask her to paint the whole room and you get a mess.
>
> For a decade, computer vision asked for the painting. Masked autoencoders hide 75% of an image and demand the missing pixels back, wallpaper included. Most of those pixels are noise, so the model burns its capacity predicting noise.
>
> JEPA asks for the sketch instead. Two encoders describe what they see, a small predictor guesses one description from the other, and the loss never touches a pixel.
>
> So why hasn't everyone switched? Because two witnesses graded on agreement can just agree to say "a person, probably" about everything. Zero loss, nothing learned. Every JEPA carries three tricks to stop that, and nobody has proven the tricks are enough.
>
> Still, it works. V-JEPA 2's frozen encoder plus under 62 hours of robot video lets a Franka arm pick things up in a lab it never trained in.
>
> I wrote up the whole idea, the collapse problem, and where the tricks come from. Part 1 of two:
> https://cgnarendiran.github.io/blog/jepa-nobody-cares-about-the-wallpaper/
>
> Part 2 is LeJEPA, where someone finally shows up with a proof. Stay tuned.
>
> #JEPA #SelfSupervisedLearning #WorldModels #ComputerVision #AI
> @Fast Code AI

---

## 12. Pre-schedule checklist

- [ ] First sentence names the concrete object of the conceit and stands alone for a cold reader
- [ ] Hook under 200 characters before the first blank line
- [ ] Opens on the post's conceit or absurd image, not on "I wrote a post"
- [ ] The mechanism in plain words. No equations, no markdown
- [ ] One concrete number or failure from the post
- [ ] One line of dragons from the honest-cons section
- [ ] A bet or a turn, in first person
- [ ] Pointer line, then the canonical URL on its own line
- [ ] Series line if the post is part of a series
- [ ] 4 to 6 hashtags, then the Fast Code AI mention
- [ ] 120 to 220 words, never above 250
- [ ] At least one rhetorical question in the first half, answered at once
- [ ] At least two first-person sentences about what Naren did or thinks
- [ ] One number, two at most
- [ ] No more than two consecutive paragraphs ending on a fragment
- [ ] Zero emoji bullets, at most one 👇, at most one emoticon
- [ ] Nothing claimed that is not in the post. No invented anecdotes, no role claims
- [ ] No §9 or blog-guide §13 banned patterns
- [ ] Cover image attached with alt text
