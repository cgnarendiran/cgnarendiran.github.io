---
slug: mamba-is-attention-all-you-really-need
title: Mamba - Is Attention All You Really Need? Part 1
blog_date: 2026-09-23
image: images/blog36/cover.jpg
alt: the interpreters' section at the Nuremberg trials, 1945-46, a row of interpreters behind glass with headphones and microphones and a few sheets of notes
publish_after: 2026-09-24T03:00:00Z
source: manual
---

An interpreter in a conference booth never keeps a transcript. They keep one small pad and decide, word by word, what is worth writing on it.

A Transformer is the typist in the hall instead. It keeps every word it has heard (the KV cache), and every new word reads all of them. On raw audio that is 960,000 tokens a minute.

So where does the pad come from? Control theory. A state space model describes a system by a small state that rolls forward one step at a time (think of a thermostat tracking a room). And the same equation runs like an RNN when you step through it, and trains like a CNN when you unroll it into one fixed kernel.

Mamba changes one thing. It lets each word decide how fast the pad forgets. On selective copying, that takes the best non-selective model from 57% to 99.8%.

The catch is that letting the words choose breaks the CNN trick, so training is back to one step at a time. I think that tension is the whole story of Mamba, and it is where part 2 picks up.

I started this one from the control theory basics and built up to Mamba. Part 1 of the post is here:
https://cgnarendiran.github.io/blog/mamba-is-attention-all-you-really-need/

#Mamba #StateSpaceModels #LLMs #Transformers #DeepLearning
@[Fast Code AI](urn:li:organization:70969206)
