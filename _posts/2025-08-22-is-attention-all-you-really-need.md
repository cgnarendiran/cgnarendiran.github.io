---
layout: post
title:  "Is Attention All You Really Need?"
date:   2025-08-22
image:  images/blog21/cover.webp
tags:  DeepSeek Attention MLA KV Caching MoE 
---
*On the cover: MLA Architecture*

## Why do we even cache keys and values?

Large language models generate text one token at a time by taking all the tokens that came before them as input. They are the classic autoregressive models after all. At step *t*, the attention for head *i* is:

$$
\text{Attention}_t^{(i)} = \text{softmax}\!\left(\frac{Q_t^{(i)} K_{1:t}^{(i)\,T}}{\sqrt{d_h}}\right)V_{1:t}^{(i)}.
$$

Without caching, every new token requires recomputing all past $K$ and $V$, giving a per-sequence cost:

$$
O(T^2 d_h).
$$

With KV caching, we reuse stored $K,V$, so cost drops to:

$$
O(T d_h).
$$

Miss caching and your GPU ends up grinding away on the same math over and over, like a hamster on an espresso drip.


## The cache bites back

Each token requires storing one key and one value vector per head:

$$
\text{Cache per token per layer} = 2 d_h H.
$$

Across $L$ layers and sequence length $T$:

$$
\text{Total cache size} = 2 d_h H L T.
$$

This linear growth in $T$ and multiplicative scaling with $H$ and $L$ makes cache the dominant memory consumer. Engineers tried sharing keys and values to cut this down—**MQA** shares one K/V across all heads, and **GQA** shares K/V across groups. Let's see what those are.


## MQA and GQA: Taming the Cache Explosion

Once you realize that the memory footprint grows linearly with the number of attention heads, the natural question is: *do we really need to store a full key-value cache for every single head?*

### Multi-Query Attention (MQA)

MQA proposes a simple but powerful trick: instead of giving **each head its own set of keys and values**, we let **all heads share the same K and V projections**.

* Queries (`Q`) remain head-specific (so each head can still look at the sequence differently).
* Keys (`K`) and Values (`V`) are shared (so we store just one copy in the cache).

**Cache implication:**
Instead of storing `h * d_h * L` for keys and values, you only store `d_h * L`. The reduction factor is roughly the number of heads `h`.

This means a model with 32 heads and hidden dimension 4096 cuts cache memory by **32×**, without changing the sequence length or batch size. That’s a massive saving.

### Grouped-Query Attention (GQA)

MQA is an extreme case. GQA generalizes it by letting **groups of heads share K and V** instead of *all* heads.

* For example, with 32 heads, you could split them into 4 groups of 8.
* Within each group, heads share K and V, but across groups they don’t.

**Cache implication:**
Now the cache size scales as `(h / g) * d_h * L` where `g` is the group size.

* With `g = h`, you recover standard attention (each head has its own KV).
* With `g = 1`, you get MQA (all heads share the same KV).
* Anywhere in between gives you a tradeoff between **memory efficiency** and **expressive power**.


This idea is so effective that many modern LLMs (like PaLM, LLaMA 2, Falcon, Mistral) have switched to MQA or GQA. For long-context inference, where KV caching dominates memory cost, this is one of the most impactful architectural tweaks. Both MQA and GQA help, but once you stretch context lengths, accuracy starts to sag.

## Enter DeepSeek’s Multi-Head Latent Attention (MLA)

Instead of lugging around full-rank keys and values, MLA asks: why not store a compressed latent “carry-on” and reconstruct the rest only when needed?

1. **Compress once:**

   $$
   L_t = H_t W^{DKV}, \quad W^{DKV} \in \mathbb{R}^{d_{\text{model}} \times r}, \quad r \ll d_h.
   $$

2. **Cache only latent:**

   $$
   \text{Cache per token per layer} = r.
   $$

3. **Reinflate on demand:**

   $$
   K_t^{(i)} = L_t W^{UK}_i, \quad V_t^{(i)} = L_t W^{UV}_i, \quad W^{UK}_i, W^{UV}_i \in \mathbb{R}^{r \times d_h}.
   $$

4. **Preserve positions:** RoPE is applied in a decoupled way so compression doesn’t break positional encoding.

The effective compression ratio is:

$$
\frac{\text{MLA cache}}{\text{Naive cache}} = \frac{r}{2 d_h H}.
$$

It’s Marie Kondo for tensors—only what sparks inference joy makes the cut.

## But won’t extra projections slow things down?

The reconstruction step adds multiplications of size $O(r d_h)$. Compared to the dominant attention cost $O(d_h T)$, this is negligible. So memory shrinks drastically while latency barely moves.

## DeepSeek’s final flourish: pre-multiplying weights

Some products are constant with respect to the input and can be fused.

* Score side:

  $$
  (H_t W^{UQ}_i)(L_{1:t} W^{UK}_i)^T \quad \Rightarrow \quad (W^{UQ}_i)^T W^{UK}_i \; \text{is constant}.
  $$

* Value side:

  $$
  (L_t W^{UV}_i) W^O_i \quad \Rightarrow \quad W^O_i W^{UV}_i \; \text{is constant}.
  $$

By folding these products at model load, two matmuls disappear from every inference step. It’s like realizing two roommates can split rent by moving into the same apartment.

## Curtain call

By compressing K/V into a latent and fusing static weight multiplications, DeepSeek cut cache size from

$$
2 d_h H L T \quad \to \quad r L T,
$$

over an order of magnitude smaller, while keeping accuracy nearly intact. Cache bloat turned into cache chic—enabling 128K contexts on a single GPU without blowing up memory.

## Summary table

| Method                   | Cache per token per layer | Total cache size ($T$ tokens, $L$ layers) |
| ------------------------ | ------------------------- | ----------------------------------------- |
| **Naive KV**             | $2 d_h H$                 | $2 d_h H L T$                             |
| **MQA**                  | $2 d_h$                   | $2 d_h L T$                               |
| **GQA** (group size $g$) | $\tfrac{2 d_h H}{g}$      | $\tfrac{2 d_h H}{g} L T$                  |
| **MLA**                  | $r$                       | $r L T$                                   |

