---
slug: grpo-rlvr
title: "GRPO and RLVR - The Answer Key and the Rank List"
blog_date: 2026-09-13
image: images/blog33/cover.png
alt: "On the cover: an answer key on the left, a rank list on the right. Between them they replaced two neural networks with a Python function."
publish_after: 2026-09-13T10:56:20-07:00
source: blog-companion
---

A coaching centre can mark two hundred papers two ways. Pay a marker who takes a week, or print the answer key and put a rank list on the noticeboard.

RLHF hired the marker, a network fitted to human preferences, and let PPO chase its score. The model learned what the examiner actually marks, so it gives you a confident opening and gets the boiling point wrong.

So why pay a marker for a maths problem? You don't. The answer is at the back of the book, and you cannot flatter a string comparison.

GRPO sacks the teacher who predicts your rank too, since a sampled group's average mark is a baseline you can measure instead of predict (that one is model-sized and never writes a token). DeepSeek ran it with no supervised fine-tuning, went from 15.6% to 71% on AIME, and the model invented rough work on its own.

The catch is that rerunning it on Qwen with random rewards kept most of the gain, so the answer key may not have been doing the work.

My bet is that the verifier becomes the product, since the algorithm is a few lines of numpy and the checkers are what you compete on. I broke it down in my new blog:
https://cgnarendiran.github.io/blog/grpo-rlvr/

#GRPO #RLVR #DeepSeek #ReinforcementLearning #LLMs
@[Fast Code AI](urn:li:organization:70969206)
