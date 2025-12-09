---
layout: post
title:  "KV Caching & MLA - Is Attention All You Really Need?"
date:   2025-08-22
image:  images/blog21/cover.jpeg
tags:  DeepSeek Attention MLA KV Caching MoE 
---
*On the cover: MLA Architecture. Credits: Welch Labs*

It's been 8 years since the landmark paper "Attention is all you need" was published. The paper introduced the attention mechanism, which has revolutionized the field of natural language processing. The self-attention mechanism and consequently the transformer models are the main reason we have large launguage models (LLMs) today.

But these have gone through significant improvements over the years. These include the introduction of KV caching, multi-head attentions (MHA), rotary positional encodings (RoPE), and mixture of experts (MoE). In this post I'll talk about KV caching, their variants and DeepSeek's Multi-Head Latent Attention (MLAs). I will cover the remaining topics in subsequent posts.

## Inference in LLMs

Large language models generate text one token at a time by taking all the tokens that came before them as input. They are the classic autoregressive models after all. At step *t*, the attention for head *i* is:

$$
\text{Attention}_t = \text{softmax}\!\left(\frac{Q_t K_{1:t}^{T}}{\sqrt{d_h}}\right)V_{1:t}.
$$

where $t$ is the token position, $d_h$ is the hidden dimension. And the $Q_t$, $K_{1:t}$, $V_{1:t}$ are the query, key, and value vectors for the token $t$ and $1:t$.

$$
Q_t = W^{Q}_i X_t\\
K_{1:t} = W^{K}_i X_{1:t}\\
V_{1:t} = W^{V}_i X_{1:t}\\
$$


Problem with this is that most of the computations are repeated again and again for the same previous tokens. There must be a better way to do this right? Welcome to *KV Caching*.


## Why do we even cache keys and values?

Essentially we cache the $K$ and $V$ encodings of the tokens. Why do we do this? Because without caching, every new token requires recomputing all past $K$ and $V$, giving a per-sequence cost of:

$$
O(T^2 d_h).
$$

where $T$ is the sequence length and $d_h$ is the hidden dimension.

With KV caching, we reuse stored $K,V$, so cost drops to:

$$
O(T d_h).
$$

If we didn't do caching, our GPU ends up grinding away on the same math over and over, like a hamster on an espresso drip.


## The cache bites back

This is fine, but there's a new problem now. We traded the compute problem with a memory problem. Each token requires storing one key and one value vector per head:

$$
\text{Cache per token per layer} = 2 d_h H.
$$

There's a $2$ because we store $K$ and $V$ both.

We also need to worry about the number of layers $L$ and sequence length $T$. Across $L$ layers and sequence length $T$, this becomes,

$$
\text{Total cache size} = 2 d_h H L T.
$$

This linear growth in $T$ and multiplicative scaling with $H$ and $L$ makes cache the dominant memory consumer. Now what can we do about this? Engineers tried sharing keys and values to cut this down, resulting in **MQA** that shares one K/V across all heads, and **GQA** that shares K/V across groups. Let's see what those are.


## Taming the Cache Explosion

Once you realize that the memory footprint grows linearly with the number of attention heads, the natural question is: *do we really need to store a full key-value cache for every single head?*

### Multi-Query Attention (MQA)

MQA proposes a simple but powerful trick: instead of giving **each head its own set of keys and values**, we let **all heads share the same K and V projections**.

* Queries (`Q`) remain head-specific (so each head can still look at the sequence differently).
* Keys (`K`) and Values (`V`) are shared (so we store just one copy in the cache).

**Cache implication:**
Instead of storing $H * d_h * L$ for keys and values, you only store $d_h * L$. The reduction factor is roughly the number of heads $H$.

This means a model with 32 heads and hidden dimension 4096 cuts cache memory by **32×**, without changing the sequence length or batch size. That’s a massive saving.

### Grouped-Query Attention (GQA)

MQA is an extreme case. GQA generalizes it by letting **groups of heads share K and V** instead of *all* heads.

* For example, with 32 heads, you could split them into 4 groups of 8.
* Within each group, heads share K and V, but across groups they don’t.

**Cache implication:**
Now the cache size scales as $g * d_h * L$ where $g$ is the group size.

* With $g = H$, you recover standard attention (each head has its own KV).
* With $g = 1$, you get MQA (all heads share the same KV).
* Anywhere in between gives you a tradeoff between **memory efficiency** and **expressive power**.


This idea is so effective that many modern LLMs (like PaLM, LLaMA 2, Falcon, Mistral) have switched to MQA or GQA. For long-context inference, where KV caching dominates memory cost, this is one of the most impactful architectural tweaks. Both MQA and GQA help, but once you stretch context lengths, accuracy starts to sag.

## Enter DeepSeek’s Multi-Head Latent Attention (MLA)

This is where the brilliance of DeepSeek’s Multi-Head Latent Attention (MLA) comes in. Instead of lugging around full-rank keys and values, MLA asks: why not store a compressed latent “carry-on” and reconstruct the rest only when needed?

1. **Compress once:**

   $$
   L_t = X_t W^{DKV}, \quad W^{DKV} \in \mathbb{R}^{d_{\text{model}} \times r}, \quad r \ll d_h.
   $$

   where $L_t$ is the latent encoding and $X_t$ is the input token embedding of token $t$. $W^{DKV}$ is the projection matrix for the latent encoding.

2. **Cache only latent:**

   $$
   \text{Cache per token per layer} = r.
   $$

   This $r$ is the rank of the latent encoding. It is much smaller than $d_h$.

3. **Reinflate on demand:**

   $$
   K_t^{(i)} = L_t W^{UK}_i, \quad V_t^{(i)} = L_t W^{UV}_i, \quad W^{UK}_i, W^{UV}_i \in \mathbb{R}^{r \times d_h}.
   $$

   where $W^{UK}_i$ and $W^{UV}_i$ are the projection matrices for the key and value encoding.

4. **Preserve positions:** RoPE (Rotary Positional Encoding) is applied in a decoupled way so compression doesn’t break positional encoding.

The effective compression ratio is:

$$
\frac{\text{MLA cache}}{\text{Naive cache}} = \frac{r}{2 d_h H}.
$$

It’s Marie Kondo for tensors: whatever sparks inference joy only those make the cut.

**NOTE:** But won’t extra projections slow things down?

The reconstruction step adds multiplications of size $O(r H d_h)$. Compared to the dominant attention cost $O(H d_h T)$, this is negligible. So memory shrinks drastically while latency barely moves.

## DeepSeek’s final flourish: pre-multiplying weights

Some products are constant with respect to the input and can be fused.

* Score side:

  $$
  (X_t W^{UQ}_i)(L_{1:t} W^{UK}_i)^T \quad \Rightarrow \quad (W^{UQ}_i)^T W^{UK}_i \; \text{is constant}.
  $$

  If you take a look at the score side, where we multiply the query and key, we can combine the $W^{UQ}_i$ and $W^{UK}_i$ to get a constant matrix, since these are always the same.

* Value side:

  $$
  (L_t W^{UV}_i) W^O_i \quad \Rightarrow \quad W^O_i W^{UV}_i \; \text{is constant}.
  $$

  Same goes in the value side, where we multiply the latent matrix $W^{UV}_i$ and the output projection matrix $W^O_i$.

By folding these products at model load, two matmuls disappear from every inference step. It’s like realizing two roommates can split rent by moving into the same apartment. 

## Curtain call

By compressing K/V into a latent and fusing static weight multiplications, DeepSeek cut cache size from

$$
2 d_h H L T \quad \to \quad r L T,
$$

over an order of magnitude smaller, while keeping accuracy nearly intact. Cache bloat turned into cache chic-enabling 128K contexts on a single GPU without blowing up memory.

## Summary table

| Method                   | Total cache size ($T$ tokens, $H$ heads, $L$ layers) |
| ------------------------ | ---------------------------------------------------- |
| **Naive KV**             | $2 d_h H L T$                                        |
| **MQA** (same K/V)       | $2 d_h L T$                                          |
| **GQA** (group size $g$) | $2 d_h g L T$                                        |
| **MLA**                  | $r L T$                                              |

Mind you, this is a significant speedup, while also reducing the memory footprint. All this put together is what caused DeepSeek to wipe out billions of dollars in maket cap in the US. Because now you can run more accurate models with less memory. And now you know!

Fin.
