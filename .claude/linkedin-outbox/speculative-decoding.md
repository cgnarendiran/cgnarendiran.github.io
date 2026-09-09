---
slug: speculative-decoding
title: Speculative Decoding - Is Attention All You Really Need?
blog_date: 2026-09-09
image: images/blog32/cover.png
alt: a goods lift with one sheet of paper on the left and a slip of eight guesses on the right. Same journey, same forty-two milliseconds.
publish_after: 2026-09-09T11:49:10-07:00
source: blog-companion
---

A goods lift takes forty-two milliseconds to reach the basement archive whether you send down one question or eight, because the walk is what costs.

That lift is your GPU, dragging its weights out of memory to write one more word, and since 2017 we have been sending it down with a single sheet of paper on it.

So what else goes on the lift? Guesses. A small model writes the next eight tokens, the big one scores them all in the pass it was making anyway, and a rejection sampling step at the bottom means the words that come out are provably the ones the big model would have written on its own (first-year statistics, wearing a lanyard).

Mismatch the pair and it runs backwards, because a drafter that guesses wrong often enough gets you 0.95x. The catch is that the free capacity is only free while nobody else wants it, so speculation goes negative as the batch size climbs.

My favorite part is that diffusion models, which keep failing to replace autoregression, have found honest work guessing what autoregression is about to say.

I wrote up the sampling trick and the cases where it loses:
https://cgnarendiran.github.io/blog/speculative-decoding/

Part 4 of my Is Attention All You Really Need? series.

#SpeculativeDecoding #LLMInference #Transformers #EAGLE #AI
@[Fast Code AI](urn:li:organization:70969206)
