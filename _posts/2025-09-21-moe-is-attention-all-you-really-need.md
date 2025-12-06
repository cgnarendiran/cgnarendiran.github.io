---
layout: post
title:  "MoE - Is Attention All You Really Need?"
date:   2025-09-21
image:  images/blog23/cover.jpg
tags:  DeepSeek MoE Mixture of Experts LLMs
---
*On the cover: A bunch of different robots who are expert at different tasks*

It's been 8 years since the landmark paper "Attention is all you need" was published. The paper introduced the attention mechanism, which has revolutionized the field of natural language processing. The self-attention mechanism and consequently the transformer models are the main reason we have large launguage models (LLMs) today.

But these have gone through significant improvements over the years. These include the introduction of multi-head attentions (MHA), rotary positional encodings (RoPE), mixture of experts (MoE), and KV caching. In my [previous post](https://cgnarendiran.github.io/2025-09-09-rope-is-attention-all-you-really-need/) I spoke about RoPE. In this post I'll talk about Mixture of Experts (MoE).

## Intuition

Imagine one musician being asked to play *every* instrument in an orchestra: violin, drums, flute, trumpet, piano, even the tuba. They’d spend more time switching instruments than making music and the result would sound… questionable.

Real orchestras don’t work like that. They rely on specialized players for everything, say violinists for texture, percussionists for rhythm, brass section for power, woodwinds for color, etc. Each group is exceptional at its own style of sound. And at the center stands the conductor, who decides which section should play when, how loudly, and in what combination. They don’t need every musician for every moment, only the ones best suited for that specific passage.

This is exactly how **Mixture of Experts (MoE)** works. Instead of forcing a single giant neural network to handle everything math reasoning, casual conversation, coding, emotional tone, long-context reasoning, MoE creates multiple specialized sub-networks called *experts*. For every incoming token, a *gating function* acts like the conductor: it evaluates the “melody” of the input and decides which experts should play their part.

When transformers first appeared, scaling was simple: More layers. More width. More parameters. But this quickly hit practical limits:

1. **Memory limits** - A 1T-parameter dense model is… unpleasant.
2. **Compute limits** - Every forward pass activates every parameter.
3. **Inefficient specialisation** - A single monolithic network must learn *everything*, even skills it rarely uses.

MoE solves this by decoupling *capacity* from *compute*. It lets you build a model with hundreds of billions or trillions of parameters, while only activating a tiny fraction (say 1–10%) for each token. This makes training faster, inference cheaper, and the architecture more modular.

Just like an orchestra creating a richer, more dynamic performance, MoE models deliver stronger results by letting the right specialists play at the right time. Mathematically, it’s concise and a little mischievous:

$$
y = \sum_{i=1}^{N} g_i(x) \cdot E_i(x)
$$

Where:

* $(E_i(x))$ is the $(i)$-th expert.
* $(g_i(x))$ is the gating function: which expert “gets the package.”
* $(y)$ is the final output-the delivered prediction.

And the clever trick is most experts stay idle most of the time, saving compute while keeping the model huge in capacity.


<!-- 
* **Dense vs. Sparse MoE** - and why “sparse” changed everything.
* **Top-K routing** - how tokens are assigned to experts.
* **Challenges like load balancing & router collapse** - and how modern models avoid them.
* **Practical variants** like Switch Transformers, DeepSeek’s modifications, and shared experts.
* **What MoE means for the future of LLMs** - and why almost every frontier model is now exploring it. -->


## Sparse MoE:

The earliest MoE proposals were **dense**: all experts produce an output, and the gating function blends them. This was the idea from a very old paper (1991) from Hinton's reseach group in Toronto called [Adaptive Mixture of Experts](https://www.cs.toronto.edu/~fritz/absps/jjnh91.pdf). The gating function is essentially a softmax that yields probabilities for each expert. Mathematically,

$$
g_i(x) = \frac{\exp(f_i(x))}{\sum_{j=1}^{N} \exp(f_j(x))}
$$

Where:

* $(f_i(x))$ is the $(i)$-th expert.
* $(g_i(x))$ is the gating function: which expert “gets the package.”
* $(y)$ is the final output-the delivered prediction.

This works, but it computes every expert anyway, even if the gate assigns it near-zero weight. So it has zero computational savings. Dense MoE improves representation power, but not efficiency. So modern LLMs rarely use it. In the context of LLMs, Hinton and his group (a different one with Google Brain this time), released a paper called [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://openreview.net/pdf?id=B1ckMDqlg).

The insight was simple, only activate the best K experts for each token. Instead of running all N experts: the gating function scores each token, selects the top-1 or top-2 experts (top-K routing), and only those experts run. Essentially using an argmax over the softmax.

Suddenly, you get the following benefits:

* **Speed** - far fewer floating-point operations
* **Scale** - larger total capacity without larger per-token cost   
* **Specialisation** - experts discover structure in data
* **Parallelism** - experts can live on different GPUs

Sparse MoE is the core of Switch Transformers, DeepSeek V2/V3, GLaM, Mixtral 8×22B, and almost every modern giant model.

## Router Collapse and Load Balancing

A big danger with sparse MoE is what’s called **router collapse**:

* The router may learn to favor just a few experts and send *most tokens* to them.
* That leaves other experts **underused**, defeating the purpose of having many experts in the first place.
* Over time, the heavily used experts get better (more data), and the underused ones stagnate, creating a vicious feedback loop.

This leads to inefficient specialization, where you don’t get the full expressive power of all experts. Another problem is load imbalance in a distributed setup (GPUs or devices). Essentially, some experts may become bottlenecks, hurting parallelism and compute efficiency.

To solve router collapse and ensure all experts contribute, MoE models use **load-balancing strategies**. Broadly, there are two kinds:

1. **With Auxiliary Losses**
2. **Without Auxiliary Losses (Bias-based)**

### 1. Load Balancing with Auxiliary Losses

This is the traditional method: add a regularization term (or multiple) to the training loss to encourage uniform or balanced usage of the experts.

* For example, in earlier MoE work (e.g., Switch Transformer), the model adds a **balance loss** that penalizes the router for sending too many tokens to one expert.
* The idea: if expert *i* is used too often compared to others, its “frequency” term in the loss will increase, nudging the router to distribute future tokens more evenly.
* But this isn’t perfect: if the auxiliary loss is too strong, it can **hurt model quality**, because the model may prioritize balancing over actually routing tokens to the *most appropriate* expert.

### 2. Load Balancing without Auxiliary Losses

Modern MoE architectures (notably **DeepSeek V3**) use a much more elegant trick: **bias adjustment**, instead of adding extra losses.

* Each expert (i) gets a **bias term** (b_i). Before doing the top-K selection, you add this bias to the affinity scores: (s_{i,t} + b_i). 
* The gating decision (which experts to pick) uses these *biased* scores, but the final weights (used to combine expert outputs) are based on the **original, unbiased affinity scores**. 
* During training, after each batch (or step), you **adjust** these biases dynamically:

  * If expert (i) is overused → **decrease** (b_i)
  * If expert (i) is underused → **increase** (b_i)
  * The adjustment step is controlled via a hyperparameter (\gamma), often called the *bias update speed*.
* This way, the router “learns” to use all experts, but without messing with the main task loss.

DeepSeek’s own technical report shows that this **auxiliary-loss-free strategy** achieves good balance while avoiding the performance hit of traditional balancing losses.

### Switch Transformers: The Simpler, Faster MoE

Before modern architectures like DeepSeek V3 refined MoE systems, one of the most influential designs was **Switch Transformers** (Google, 2021).
They introduced a key simplification:

### **Top-1 Routing Instead of Top-K**

Most MoE systems historically used **top-2** or **top-4** routing to combine multiple experts per token.
Switch Transformers made a bold choice:

> **Each token is routed to exactly one expert.**

This made the model *operationally simple* and extremely fast:

* No need to mix outputs from multiple experts
* No cross-expert load for a single token
* Memory + compute cost per token is dramatically lower
* Routing is easier to parallelize

Even with top-1 routing, Switch achieved large performance gains compared to dense models - showing that *specialization works even when each token only gets one expert*.


## Expert Capacity: What Happens When an Expert Gets Too Many Tokens?

Even with load balancing, token traffic is inherently unpredictable.
Some experts may receive far more tokens than others in a given batch.
But an expert runs on a specific device/TPU core/GPU block, so it has **compute and memory limits**.

This is where **expert capacity** comes in.

### **Definition:**

The *expert capacity* determines the **maximum number of tokens** an expert is allowed to process in a batch.

It is typically:

[
\text{capacity} = \text{capacity factor} \times \frac{\text{batch size} \times \text{tokens per sample}}{\text{num experts}}
]

Where:

* Capacity factor ≈ 1.0–2.0 (tunable)
* Larger factor → more slack → fewer dropped tokens
* Smaller factor → tighter packing → fewer memory spikes


## Token Dropping: A Consequence of Capacity

### ⭐ Switch Transformers’ Key Insight

Because each token only goes to **one expert**, if that expert is **at capacity**, the token must be *dropped* (or re-routed depending on configuration).

Two modes exist:

1. **Dropping (Switch-default)**

   * If expert (E_i) is full, the token is completely dropped (no expert FFN applied).
   * The model uses the skip connection output instead.
   * This surprisingly still works well.

2. **Rerouting (less common)**

   * If expert (E_i) is full, send the token to the next-best expert.
   * Reduces drops but increases compute.

Dropping tokens sounds alarming, but because residual connections bypass the MoE layer, the network remains stable - this is similar to Dropout in spirit.


# 2. **Fine-Grained Top-K Routing (e.g., Top-8)**

Earlier models used **top-1** (Switch) or **top-2** (GLaM, Mixtral) routing.
DeepSeek moved to **top-8** routing - a larger expert subset.

### Why this matters:

More experts per token means:

✔ fewer dropped tokens
✔ smoother traffic across experts
✔ better expert specialization
✔ higher throughput (counterintuitive, but true due to parallelism)
✔ more stable gradients

Top-8 routing reduces the shard-level traffic spikes that plagued top-1 MoE models.
Experts no longer starve or overload; each gets enough gradient flow to “find a role.”


# 3. **Shared Experts + Private Experts (Hierarchical MoE)**

This may be DeepSeek’s most clever idea.

Each MoE layer consists of two kinds of experts:

### **1. Shared Experts**

* A small number of experts used by *all* tokens
* Capture globally useful patterns (syntax, generic logic, common structures)

### **2. Private Experts**

* A large set of experts only used by specific groups of tokens
* Capture *specialized* skills (math, multilingual structures, code behavior, reasoning chains)

### Why this helps:

Shared experts:

* ensure every token has a reliable fallback
* prevent rare experts from starving
* stabilize early-stage training

Private experts:

* allow intense specialization
* reduce interference across modes
* unlock domain-specific capabilities

This hybrid structure is much more robust than pure private-expert MoE systems.

