---
layout: post
title:  "JEPA - Nobody Cares About the Wallpaper"
date:   2026-06-15
image:  images/blog28/cover.jpg
tags: [jepa, self-supervised-learning, world-models, representation-learning]
---
*On the cover: A police sketch in progress, drawn from a description rather than a photograph*

Let's say you are a detective, and a witness sits down across the table from you. She was in the room when it happened, and you want to know who else was there.

So you ask her to describe the person. Tall, grey coat, walked with a limp. A sketch artist turns that into a drawing you can send to every police station in the city.

Her description leaves out almost everything she saw: the wallpaper, the carpet, the light through the blinds, the pattern on the coffee cup. You don't miss any of it, because none of it helps you find anybody. And if she spent twenty minutes on the wallpaper, you would get her a glass of water and go find another witness.

A computer vision model has to make the same choice when it learns from images. For most of the last decade, we asked it to describe the wallpaper.

Here's the setup. The internet has billions of images and videos, but almost none of them come with labels, the little tags that say "this is a dog". Paying people to write labels is slow and expensive. Self-supervised learning gets around this by making up its own questions from the data, so that no human has to answer them. The question the field settled on was fill-in-the-blank. You hide part of the input and ask the model to predict the missing part. To get good at that, the model has to build some understanding of what it is looking at. That understanding is the thing you actually wanted.

It's a great trick. It gave us [BERT](https://arxiv.org/abs/1810.04805), which learned language by filling in hidden words. The trouble starts when you ask what, exactly, the model should fill the blank in with.

Welcome to **Joint-Embedding Predictive Architectures**, or JEPA. This is the story of how vision models stopped trying to paint the room and started trying to describe it.

## We have been asking for a painting

[Masked Autoencoders](https://arxiv.org/abs/2111.06377) (MAE) are the simplest version of fill-in-the-blank for images. You chop the image into small square patches, hide 75% of them, and ask the model to redraw the missing pixels. The loss is:

$$
\mathcal{L}_{\text{MAE}} = \frac{1}{|\mathcal{M}|}\sum_{i \in \mathcal{M}} \|\hat{x}_i - x_i\|^2
$$

where $\mathcal{M}$ is the set of masked patches, $x_i$ the true pixels, and $\hat{x}_i$ the reconstruction. In words, it is the average squared difference between the pixels the model drew and the pixels that were really there. This works pretty well. But it also asks the model to paint the wallpaper.

Think about what this loss rewards. Some of what's behind the mask is predictable. If you can see three quarters of a dog, the last quarter is going to be a dog. But most of the detail is noise, like the exact grain of the tarmac, the speckle in the shadows, or which way each leaf was pointing when the photo was taken. No model can predict those pixels, however well it understands the scene. And the loss punishes it for missing them anyway.

So the model ends up spending a lot of its effort on the least useful part of the image. Nobody designed it that way. The squared error is biggest exactly where the pixels are hardest to guess, and the model chases whatever error is biggest.

Video makes this worse. That's unfortunate, because video is the biggest pile of unlabeled data we have. A clip has a future, and now the model is asked to predict that too. Even if you understand the scene perfectly, you can't know where every leaf will be in the next frame.

So what if we asked for the description instead? Let's see what breaks.

## The anatomy of a JEPA

Yann LeCun sketched the blueprint in a 2022 position paper, [A Path Towards Autonomous Machine Intelligence](https://openreview.net/forum?id=BZ5a1r-kVsf). It has three parts:

1. A **context encoder** $f_\theta$, which is a network that turns an image into a list of numbers. This is the witness who saw part of the scene, and the list of numbers is her description (an embedding).
2. A **target encoder** $\bar{f}_\theta$, a second witness who saw a different part.
3. A **predictor** $g_\phi$, the sketch artist. It takes the first witness's description, plus a note saying which part of the room you're asking about, and guesses what the second witness would say.

The loss compares two descriptions and never touches an image:

$$
\mathcal{L}_{\text{JEPA}} = \big\| g_\phi(f_\theta(x),\, z) - \bar{f}_\theta(y) \big\|^2
$$

where $x$ is the visible context, $y$ the hidden target, and $z$ the positional information telling the predictor what it's being asked about.

![The JEPA blueprint: two encoders, a predictor conditioned on a latent, and an energy comparing two descriptions](/images/blog28/lv_jepa.png) *Figure 1: The JEPA blueprint. Two encoders turn $x$ and $y$ into descriptions $s_x$ and $s_y$, the predictor guesses $\tilde{s}_y$ from $s_x$ plus a latent $z$, and the energy $D(s_y, \tilde{s}_y)$ scores one description against the other. Nothing decodes back to pixels. Source: [A Path Towards Autonomous Machine Intelligence](https://openreview.net/forum?id=BZ5a1r-kVsf)*

That's also where the name comes from. Both inputs get turned into embeddings (joint embedding), and one embedding is predicted from the other (predictive architecture).

There is no decoder here, so no part of the model ever turns a description back into pixels. That means the wallpaper never shows up in the loss. But this comes with a cost, and that cost is what the rest of this post is about.

## The witnesses can collude

Say you are grading two witnesses on whether their descriptions agree. What is the laziest way for them to get full marks?

Easy. They agree beforehand to say "a person, probably" about everything.

In maths terms, the encoder can learn to output the same vector $c$ for every input $x$, and the predictor can pass it along unchanged. Then

$$
\mathcal{L}_{\text{JEPA}} = \|c - c\|^2 = 0
$$

The loss is zero, the best possible score. And the model has learned nothing. This is called **representation collapse**, and for years it made people think joint-embedding methods were cursed. Reconstruction never had this problem, because you can't fake a photograph. You can absolutely fake a description though (ask anyone who has written a self-appraisal).

People came up with two kinds of fix, and the difference between them matters a lot for part 2.

The first kind keeps the witnesses apart and hopes for the best. [BYOL](https://arxiv.org/abs/2006.07733) gives one branch an extra predictor. The other branch, the target, is a slowly updated copy of the first, called an exponential moving average (EMA). And the target branch is never trained directly, which is called a stop-gradient. The copy's weights $\bar{\theta}$ follow the real ones $\theta$ like this:

$$
\bar{\theta} \leftarrow \tau \bar{\theta} + (1-\tau)\theta
$$

where the decay $\tau$ is usually somewhere between 0.996 and 0.999 (the gap between those two numbers has cost somebody a month, and I am glad it was not me). Since the copy moves slowly, the two witnesses can never quite settle on a shared story.

[SimSiam](https://arxiv.org/abs/2011.10566) throws out the EMA and keeps the stop-gradient. [DINO](https://arxiv.org/abs/2104.14294) calls the two branches a teacher and a student, and adds two more tricks. Centering pushes the outputs to spread out evenly, and sharpening pushes them to commit to a few strong values. The two pull against each other, and a schedule that somebody tuned by hand keeps them balanced.

Here is the part I find uncomfortable. **None of this rules out collapse.** The constant answer still gets a perfect score on BYOL's loss. It just doesn't happen in practice. The papers explaining why came out years after the methods, written by people who had been using them the whole time. And a lot of foundation models got built on top of that anyway.

The second kind of fix puts rules on the descriptions themselves. [Barlow Twins](https://arxiv.org/abs/2103.03230) makes the two views agree on each number in the description, while making different numbers carry different information. [VICReg](https://arxiv.org/abs/2105.04906) spells it out as three terms:

1. an invariance term $s$, which pulls the descriptions of two views of the same image together,
2. a variance term $v$, which forces every number in the description to actually vary from image to image, and
3. a covariance term $c$, which stops two numbers from carrying the same information.

$$
\mathcal{L}_{\text{VICReg}} = \lambda\, s(Z, Z') + \mu\, [v(Z) + v(Z')] + \nu\, [c(Z) + c(Z')]
$$

A constant answer doesn't vary at all, so it fails the variance term. These methods rule out collapse without any teacher, and I think they deserved more credit than they got. Hold that thought, because it comes back in part 2.

**NOTE:** JEPA went with the first kind of fix. I-JEPA, V-JEPA and V-JEPA 2 all ship an EMA target encoder and a stop-gradient. They also keep the predictor deliberately small, so it can't do the job by itself.

## I-JEPA: the first witness

[I-JEPA](https://arxiv.org/abs/2301.08243) (Assran et al., CVPR 2023) is the first working version of this recipe, for images.

### Step 1: the interrogation

You pick one big **context block** and four **target blocks** from the image. They don't overlap, so the context can't peek at the answer. The context encoder sees only the patches in the context block. The target encoder sees the whole image, and we cut its output at the four target locations to get the four answers.

How you pick these blocks turns out to matter more than anything else in the paper. The ablations show that the target blocks have to be large, big enough to hold part of an object. The context block has to be spread out over the image. If the targets are small, the model can get away with answering "beige", because colour and texture are enough to guess a small patch. If a target holds half a dog's head, the model has to have understood the picture to describe it. (Any schoolteacher could have told them that.)

![I-JEPA: one context block predicting several target blocks through positional tokens](/images/blog28/ijepa.png) *Figure 2: I-JEPA. One context block predicts the representations of several target blocks, with the predictor conditioned on positional tokens shown in colour. Source: [I-JEPA](https://arxiv.org/abs/2301.08243)*

### Step 2: the sketch artist

The predictor is a small [vision transformer](/blog/vit-pixels-to-tokens/) (ViT). We feed it the context descriptions plus a set of **mask tokens**, which carry the position of the block we want. It produces a guess at that block's description. Change the position in the mask tokens, and the same predictor gives you a guess for a different block.

### Step 3: the verdict

The loss is the squared distance between each guess and the real description, averaged over all four blocks:

$$
\mathcal{L} = \frac{1}{M}\sum_{n=1}^{M} \sum_{i \in B_n} \|\hat{y}_i - y_i\|_2^2
$$

where $M = 4$ is the number of target blocks, $B_n$ the patch indices in block $n$, $\hat{y}_i$ the predictor's output and $y_i$ the target encoder's. Only the context encoder and the predictor are trained by this loss. The target encoder just follows along as an EMA copy.

So how do you check whether the descriptions are any good? The standard test is a **linear probe**. You freeze the encoder and train a single linear layer on top of it to classify ImageNet images. If one simple layer can read the class off the description, then the description must contain it. With a ViT-L/16, I-JEPA gets **77.5%** against MAE's **76.0%**. The margin is small and I wouldn't lean on it. What I find more interesting is how it got there. It used no hand-made image augmentations (random crops, colour jitter and so on), which BYOL, DINO and the rest all depended on. And a ViT-Huge/14 trained on **16 A100s in under 72 hours**, which for a Meta vision paper is a suspiciously modest number.

## V-JEPA: moving pictures

[V-JEPA](https://arxiv.org/abs/2404.08471) (Bardes et al., TMLR 2024) takes the recipe to video. The masks become tubes, meaning the same patch is hidden in every frame of the clip. Otherwise the model could cheat by copying the patch from the frame just before. The training data was **VideoMix2M**, two million videos stitched together from Kinetics-710, Something-Something v2 and HowTo100M.

![V-JEPA: a tube-masked clip through the context encoder, an EMA target encoder, and a stop-gradient on the target branch](/images/blog28/vjepa.png) *Figure 3: V-JEPA. The context encoder sees a tube-masked clip, the target encoder is an EMA copy fed the unmasked clip, and the stop-grad on the target branch is the thing standing between this and the constant solution. Source: [V-JEPA](https://arxiv.org/abs/2404.08471)*

The number that matters here is the frozen evaluation. The encoder isn't fine-tuned at all, and only a small probe on top of it gets trained:

| Model | Kinetics-400 | Something-Something v2 | ImageNet-1K |
| ----- | ----- | ----- | ----- |
| V-JEPA ViT-H/16 | 81.9 | 72.2 | 77.9 |
| V-JEPA ViT-L/16 | 82.1 | 71.2 | — |

Something-Something v2 is the column I'd look at. Its classes are things like "uncovering something" and "pushing something so it falls off the table". Knowing what the objects are doesn't help much, so the model has to understand the motion. With frozen features on SSv2, V-JEPA beats VideoMAEv2, which reconstructs pixels, by **11 points** (72.2 against 61.2).

The label-efficiency results tell you even more. The fewer labels you give the probe, the bigger V-JEPA's lead over pixel reconstruction gets. That's what you'd expect if one model has a description and the other has a photocopy.

## V-JEPA 2: what happens with a million hours

[V-JEPA 2](https://arxiv.org/abs/2506.09985) (Assran et al., 2025) is not modest about compute at all. The encoder is a ViT-g with over a billion parameters. It was trained on **VideoMix22M**, which is more than a million hours of internet video plus a million images. That's about 114 years of footage, so some of it is definitely cats. The recipe is mostly the same as V-JEPA, just bigger: more data, a bigger model, longer training and higher resolution. It also switches to 3D [rotary position embeddings](/blog/rope-is-attention-all-you-really-need/), which tell the model where each patch sits in space and time.

- Something-Something v2: **77.3%** top-1, against InternVideo2-1B at 69.7 and PEcoreG at 55.4
- ImageNet-1K: 84.6%, so specializing on motion cost nothing on appearance
- Epic-Kitchens-100 action anticipation: **39.7 recall@5**, up 44% relative on PlausiVL's 27.6
- Aligned with an LLM at 8B: 84.0 on PerceptionTest, 76.9 on TempCompass

![Bar chart of Something-Something v2 accuracy with frozen backbones, V-JEPA 2 ahead of InternVideo2 and PEcoreG](/images/blog28/ssv2-frozen-eval.png) *Figure 4: Something-Something v2 with a frozen backbone. The classes are things like "pushing something so it falls off the table", so recognizing objects gets you nowhere; you have to have understood the motion. Source: Author*

Look at the anticipation number for a second. The task is to watch video from a head-mounted camera and name the action one second before it happens, like "cut onion" or "open fridge". The encoder was never trained to do this. It was trained to describe hidden patches, and predicting a second into the future came along for free.

## Is it actually a world model?

I want to be a little pedantic here, because the marketing has gotten ahead of the architecture.

A world model needs a transition function, $s_{t+1} = f(s_t, a_t)$. It takes where you are ($s_t$) and what you *do* ($a_t$), and tells you where you end up. Now go back and look at what the JEPA predictor gets as input. It gets the position of the hidden block, and nothing else. So it can answer "what's over there?" but not "what happens if I do this?".

Our witness can describe the room in great detail. But ask her what happens when someone opens the door, and she can't tell you. She only ever watched the room. She never touched anything in it.

| Tier | Predictor conditioned on | Examples | World model? |
|---|---|---|---|
| 1 | Nothing, no predictor at all | Pure joint-embedding methods | No, it's a state space |
| 2 | Position, "what's in this hole?" | I-JEPA, V-JEPA, V-JEPA 2 base | No, it's latent inpainting |
| 3 | State and action, "what if I do X?" | V-JEPA 2-AC, DINO-WM, Dreamer | Yes |

![The same JEPA architecture with mask tokens in the latent slot on the left and robot actions on the right](/images/blog28/action_conditioning.png) *Figure 5: The whole argument in one picture. Same architecture, same $z$ slot. On the left $z$ carries mask tokens and you get latent inpainting; on the right $z$ carries robot actions and poses, the encoders are frozen, and you get a transition function. Source: [V-JEPA 2](https://arxiv.org/abs/2506.09985)*

Which brings us to the part of the paper that earns the label. **V-JEPA 2-AC** (AC for action-conditioned) freezes the encoder and trains a new, small predictor on top of it. This predictor gets the robot's actions as input, not just positions, and it can only look at past frames. It was trained on **under 62 hours** of unlabeled robot video from the [Droid](https://droid-dataset.github.io/) dataset (a long weekend, if the robot skips sleep). Now there's a real transition function, so you can plan with it.

Planning works like this. You show the robot a picture of the goal, say the cup sitting on the plate. For any sequence of actions the robot could take, the predictor imagines the description of where it would end up. You score each sequence by how far that imagined description is from the goal picture's description (an L1 distance), and pick the closest:

$$
a^*_{t:t+T} = \arg\min_{a_{t:t+T}} \; \big\| \hat{s}_{t+T}(a_{t:t+T}) - s_{\text{goal}} \big\|_1
$$

The search uses the cross-entropy method, which samples a lot of candidate sequences and keeps refining around the best ones. The robot runs only the first action of the winner, looks again, and replans. This is called model-predictive control. All of it happens in description space, so no frame is ever drawn.

They put it on Franka robot arms in two labs that contributed no training data. With no extra training, it picked and placed a cup 80% of the time and a box 65% of the time. It reached for a target while holding an object 75% of the time. Grasping was harder: 65% for a cup and 25% for a box. Octo, a popular open robot policy, grasped the cup 15% of the time. Planning takes **16 seconds per action**, against about 4 minutes for Cosmos. Cosmos has to generate pixels to imagine the future (imagine having to paint a watercolour of the kitchen before you can decide to open the fridge).

The paper also checks that the actions are doing the work. It sweeps the arm's movement over a grid and plots the planning score for each one. The score bottoms out close to the movement that actually reaches the goal, so the predictor has learned what its actions do. A tier 2 predictor has no action input to sweep, so there is nothing to plan with.

## Why this matters

What I take from all this is that the objective was holding things back, more than the architecture was. JEPA uses the same transformers as MAE, on the same kind of data. Changing what you ask the model to predict made the representations better and cheaper to train.

You can see the payoff in the frozen encoder. V-JEPA 2's encoder doesn't change at all during robot training. That's why 62 hours of robot video is enough to plan with. The encoder already knows what a cup is, what "behind" means and what falling looks like, because it watched a million hours of people doing things. Language models learned what they know by reading the internet, and we are running low on internet. We are nowhere near running out of video.

## The honest cons

Collapse is still held off by superstition. Everything above relies on an EMA teacher, a stop-gradient and a predictor kept weak on purpose. None of those comes with a proof. The constant answer is still sitting there with a perfect score. We've just piled enough tricks around it that training doesn't wander in. Take away any one of them and training falls over. And nobody can tell you exactly why the rest are enough.

The evaluation is doing some of the work too. Frozen probes are the right idea. But the "attentive probe" in these papers has four transformer blocks in it, which is a small network of its own. So it's fair to ask how much of the 77.3 comes from the encoder and how much from the probe. I haven't seen that settled.

"World model" has also become branding. Meta's launch post calls V-JEPA 2 the first world model trained on video. That quietly gives the base model credit for what the AC variant does, and the base model has no action input anywhere in it. The base model learns representations. It's the 62 hours of post-training that earn the name.

And when a JEPA is wrong, you can't see it. A diffusion model that predicts the future gives you a picture, and you can look at it and say "no, the cup doesn't go there". A JEPA gives you 1,024 numbers that are wrong in some direction, and good luck arguing with those. V-JEPA ships a separate diffusion decoder just so humans can look at what the model believes.

## Conclusion

So the idea is to stop painting the room. You describe it, predict the description and throw the wallpaper away. The benchmarks, the frozen encoders and a Franka arm in a lab it had never seen all say this works.

But look again at what's holding it up. There's an EMA copy, a stop-gradient and a predictor kept weak on purpose. Each one is a workaround for the same question: what stops the witnesses from agreeing on nothing?

For five years, people could say what a bad description looks like, but not what a good one looks like. In late 2025 somebody wrote it down, with a proof.

Stay tuned for part 2, where we meet LeJEPA, tear out the entire interrogation room, and replace it with a single term. Till then, ciao.
