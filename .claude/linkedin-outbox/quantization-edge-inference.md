---
slug: quantization-edge-inference
title: "Quantization - Four Bits and a Winter Coat"
blog_date: 2026-09-16
image: images/blog34/cover.jpg
alt: "On the cover: the sizer at the gate, the bag that has to go through it, and the pile that stays on the bed."
publish_after: 2026-09-20T10:49:14-07:00
source: blog-companion
---

Every boarding gate has a metal frame, and your cabin bag has to fit through it. So you roll the jeans instead of folding them, and you wear the coat onto the plane.

A 70B model has the same evening ahead of it. In sixteen bits its weights need two H100s (and the cable between them). In four bits it sits on one card, and answers to within a rounding error.

So why is anyone still serving in sixteen bits? Because one thing in the pile always weighs as much as the rest. A handful of channels in a Transformer shout far louder than their neighbours, and a ruler stretched to reach them rounds everything else to zero. That is the coat, and every trick since 2022 is about getting it into the bag.

The catch is that perplexity never tells you when it went wrong. Push AWQ down to three bits and a reasoning model keeps reaching the right answer and then talking itself out of it. MATH-500 accuracy falls from 85.6% to 47.0%.

I wrote up the ruler, the coat and the three ways round it:
https://cgnarendiran.github.io/blog/quantization-edge-inference/

What I'm noticing is that the folding has moved upstream, because models now ship in four bits on purpose.

#Quantization #LLMs #EfficientInference #FP4 #Transformers
@[Fast Code AI](urn:li:organization:70969206)
