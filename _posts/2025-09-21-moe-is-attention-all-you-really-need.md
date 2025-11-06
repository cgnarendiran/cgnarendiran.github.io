---
layout: post
title:  "MoE - Is Attention All You Really Need?"
date:   2025-09-21
image:  images/blog23/cover.jpg
tags:  DeepSeek MoE Mixture of Experts LLMs
---
*On the cover: A MoE, essentially*

It's been 8 years since the landmark paper "Attention is all you need" was published. The paper introduced the attention mechanism, which has revolutionized the field of natural language processing. The self-attention mechanism and consequently the transformer models are the main reason we have large launguage models (LLMs) today.

But these have gone through significant improvements over the years. These include the introduction of multi-head attentions (MHA), rotary positional encodings (RoPE), mixture of experts (MoE), and KV caching. In my [previous post](https://cgnarendiran.github.io/2025-09-09-rope-is-attention-all-you-really-need/) I spoke about RoPE. In this post I'll talk about Mixture of Experts (MoE).

## Gates and Experts

Imagine you’re running a delivery company. Every day, you have packages of all shapes and sizes: pizzas, fragile electronics, and giant inflatable unicorns. You could have one delivery guy try to handle everything—but chances are, your electronics get smashed, the pizzas arrive cold, and the unicorn… well, it never fits in the car.

Instead, you hire **specialized delivery experts**: one for food, one for fragile stuff, and one for oversized packages. When a new order comes in, a smart dispatcher looks at the item and says: “Alice handles the pizzas, Bob handles the electronics, and Clara tackles the unicorns.” Suddenly, efficiency skyrockets, mistakes plummet, and the customers are happy.

This is exactly how **Mixture of Experts (MoE)** works in large language models. Instead of forcing a single monolithic network to handle every token and context, MoE has **multiple specialized sub-networks** (the experts), and a **gating function** that decides which ones get to contribute to the prediction for each token.

Mathematically, it’s concise and a little mischievous:

$$
y = \sum_{i=1}^{N} g_i(x) \cdot E_i(x)
$$

Where:

* $(E_i(x))$ is the $(i)$-th expert.
* $(g_i(x))$ is the gating function: which expert “gets the package.”
* $(y)$ is the final output—the delivered prediction.

And the clever trick: **most experts stay idle most of the time**, saving compute while keeping the model huge in capacity. It’s like having a fleet of 100 delivery experts but only deploying the 2 or 3 you actually need for today’s orders. 💡

In this post, we’ll cover:

1. How the gating function decides which experts are active.
2. Why MoEs make gigantic LLMs cheaper and faster.
3. Sneaky challenges—like load balancing and “rogue experts” that hog all the attention.


### **How the Gating Function Picks the Right Expert (Without Asking HR)**

Continuing with our delivery analogy: the dispatcher is basically the **gating function** of MoE. When a new “package” (token) arrives, the dispatcher decides which expert(s) should handle it. In MoE, this is usually done with a **softmax over scores**. Let’s write it down:

$$
g_i(x) = \frac{\exp(s_i(x))}{\sum_{j=1}^{N} \exp(s_j(x))}
$$

Here:

* $(s_i(x))$ is the “score” that expert (i) gets for input (x). Think of it like the dispatcher checking each expert’s resume for the package at hand.
* $(g_i(x))$ is the probability that expert (i) will do the work.

**Key idea:** only a few experts actually get to process each token. Most are ignored, which saves compute. A common trick is **top-k gating**, where we pick the k highest $(g_i(x))$ values and zero out the rest. It’s like saying: “Only the top 2 experts for this delivery actually get in the van.”

#### Visualizing it:

Imagine 5 experts and an input token:

| Expert | Score (s_i(x)) | g_i(x) after softmax |
| ------ | -------------- | -------------------- |
| 1      | 2.5            | 0.05                 |
| 2      | 7.1            | 0.60                 |
| 3      | 6.8            | 0.35                 |
| 4      | 1.0            | 0.005                |
| 5      | 0.2            | 0.0005               |

If we use **top-2 gating**, only experts 2 and 3 actually handle this token. Everyone else… goes home early. 🏠

So in practice, the output for a token is:

$$
y = g_2(x) E_2(x) + g_3(x) E_3(x)
$$

Which means: “Expert 2 does most of the heavy lifting, expert 3 helps, and the rest… enjoy their coffee.”

#### Why it matters:

1. **Compute efficiency**: We don’t touch all experts, just a subset.
2. **Specialization**: Each expert can focus on a niche—like emojis, Shakespeare, or obscure math.
3. **Scale without meltdown**: You can have billions of parameters, but only a fraction are active per token.

