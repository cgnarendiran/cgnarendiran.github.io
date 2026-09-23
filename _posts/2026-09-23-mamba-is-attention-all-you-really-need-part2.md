---
layout: post
title:  "Mamba - Is Attention All You Really Need? Part 2"
date:   2026-09-23
image:  images/blog37/cover.jpg
description: "Selection broke the convolution that made state space models fast to train. Here is how Mamba got the speed back, and why attention stayed in the room."
tags: [state-space-models, attention, transformers, llms, efficient-inference]
---

*On the cover: Margot Bortlin, in the middle, interpreting at the Nuremberg tribunal with two colleagues in the glass booth. The interpreters there worked in teams and took turns at the microphone, which is the trick this post is about. [Public domain](https://commons.wikimedia.org/wiki/File:Margot_Bortlin_nuremberg_interpreter.jpg), via Wikimedia Commons.*

In [Part 1](/blog/mamba-is-attention-all-you-really-need/) we built the interpreter's booth. A state space model keeps one small pad (the state) instead of a transcript of everything said (the KV cache). The idea comes from control theory. And the same equation can be computed as an RNN, one word at a time, or as a CNN, the whole sequence at once. S4 trained it as a CNN and ran it as an RNN. Then Mamba let every word choose how fast the pad forgets, and selective copying went from 57% to 99.8%.

Lovely. Now train it on a few hundred billion tokens.

The CNN view needed the same fade at every step, and selection took that away. So the only way left to compute Mamba is the RNN way, one word after another. That is the one thing a GPU is worst at.

Welcome to the era of **hybrid models**. This is the story of how Mamba got its training speed back, beat Transformers twice its size, and then ended up sharing almost every model that shipped with a few layers of attention.

## The problem: a queue on a card built for crowds

A GPU is fast because it has thousands of cores working at the same time. It is only fast when all of them have something to do.

The RNN way gives them nothing to do. Step 1,000 needs the pad from step 999. Step 999 needs the pad from step 998. So the steps form a queue, and only the one at the front can move. On a sequence of 960,000 audio samples, that is 960,000 steps in a row while almost the whole card waits.

So the question for Mamba was simple. Can you compute a recurrence without walking through it in order?

## The relay

It turns out you can, because of one small property of the fade-and-add.

Every step of the recurrence does the same two things. It multiplies the pad by some number $a$ (the fade). Then it adds some number $b$ (the new word, already scaled). Now ask what happens when you do two steps in a row.

Let's do it by hand. Say step 1 fades by $0.6$ and adds $0.4$. Step 2 fades by $0.5$ and adds $1.0$. Start with whatever pad $h$ you like.

1. After step 1, the pad is $0.6h + 0.4$.
2. After step 2, the pad is $0.5 \times (0.6h + 0.4) + 1.0 = 0.3h + 1.2$.

So two steps are really one step. They fade by $0.3$ and add $1.2$. And you could work that out without ever knowing what $h$ was. In general,

$$
(a_1, b_1) \text{ then } (a_2, b_2) \;=\; (a_1 a_2,\; a_2 b_1 + b_2)
$$

This property is called associativity. It means you can group the steps any way you like and get the same answer.

That is what unlocks the GPU. Chop the sequence into chunks. Give each chunk to its own group of cores. Each group squashes its whole chunk into a single fade-and-add, without waiting for anybody. Then combine the chunks' fade-and-adds, pair by pair, and pass the real pads back through. This is a **parallel scan**. It takes a few dozen rounds of work for a million tokens, instead of a million steps in a queue.

And if you think about it, this is what the booth does on a long day anyway. Interpreters work in pairs and swap every twenty minutes or so (the profession worked out its own context limit a long time before we did). The one coming on does not get the last twenty minutes again. They get about ten seconds of whispered summary (the state).

![Diagram of a sequence split into four chunks, each chunk reduced to one fade-and-add pair, then combined pairwise into the final state](/images/blog37/parallel_scan.png) *Figure 1: A parallel scan over four chunks. Each booth handles its own stretch and hands over a state. Source: Author*

## Keeping the pad on the desk

So is the scan enough on its own? The Mamba paper says no. Moving the pad in and out of memory costs time too, and the second half of the paper is about exactly that.

A GPU has two kinds of memory. HBM is the big one, 80 GB on an H100, and it is slow to reach. SRAM is tiny, but it sits right next to the cores and it is very fast. Think of HBM as the shelf at the back of the hall, and SRAM as the desk inside the booth.

Mamba's pad is sixteen numbers wide per channel by default (that is the number in the released code, not a result anybody proved). Sixteen numbers is small enough to live on the desk. So the kernel fetches the parameters from the shelf once. It does the discretisation and the whole scan on the desk. And it writes only the output back.

It does not even keep the intermediate pads for training. It recomputes them during the backward pass, because doing the maths again is cheaper than the trip to the shelf. That fused kernel runs 20 to 40 times faster than the same thing written naively in PyTorch. And past a sequence length of about 2,000, it beats [FlashAttention-2](https://arxiv.org/abs/2307.08691), which was the fastest attention kernel anybody had.

## What the booth buys you

Mamba-3B was trained on [the Pile](https://arxiv.org/abs/2101.00027), 800 GB of mixed web text, books and code. It beats Transformers of its own size and matches ones twice as big. On common sense reasoning it comes in 4 points ahead of [Pythia](https://arxiv.org/abs/2304.01373)-3B, and ahead of Pythia-7B as well. Pythia is the open model family everybody was using as a like-for-like baseline back then.

Inference throughput is about 5 times a Transformer's at the same size, and that is mostly down to batching. There is no cache to read, so a lot more sequences fit on the card at once.

The audio numbers convince me more than the language ones, because audio is where the transcript was always going to lose. SC09 is a benchmark of one-second clips of people saying the digits zero to nine. It is the most boring possible way to prove that an architecture can hear.

| Model | Parameters | FID (lower is better) | Verdict |
|---|---|---|---|
| [WaveNet](https://arxiv.org/abs/1609.03499) | 4.2M | 5.08 | the 2016 baseline, dilated convolutions |
| [SaShiMi](https://arxiv.org/abs/2202.09729) (S4) | 5.8M | 1.99 | state spaces, no selection |
| Mamba | 6.1M | 0.94 | half the error of the previous best, at the same size |

![Bar chart of SC09 audio quality for WaveNet, SaShiMi and Mamba, next to a bar chart of inference throughput for a Transformer and for Mamba](/images/blog37/results.png) *Figure 2: Six million parameters generating one-second waveforms, and the throughput you get when there is nothing to re-read. Source: Author*

## The evolution

- **Mamba-2 (2024)**: [Transformers are SSMs](https://arxiv.org/abs/2405.21060) restricts $A$ to a single number times the identity matrix. That loses some expressiveness. But it turns the scan into a sequence of matrix multiplications, which is the one thing a GPU is genuinely built for. You get 8 times larger states, 50% faster training, and a core layer 2 to 8 times quicker than Mamba-1's scan. The theory that comes with it is called **state space duality**. It shows that attention with a particular structured mask and a state space model are the same computation, written two ways. Two subfields had been writing out the same algorithm for years. It took a paper with a picture in it before either of them would admit it.
- **Mamba-3 (2026)**: [Mamba-3](https://arxiv.org/abs/2603.15569) (ICLR 2026) swaps Euler discretisation for a trapezoidal rule. It brings back complex-valued states, so the pad can track things that oscillate. And it adds a multi-input multi-output form that gets more arithmetic out of each byte moved during decoding. The complex-valued part connects straight back to the [RoPE post](/blog/rope-is-attention-all-you-really-need/): a complex SSM is doing a data-dependent rotary embedding.
- **The hybrids (2024 onwards)**: [Jamba](https://arxiv.org/abs/2403.19887) (AI21, 2024) put attention layers back in among the Mamba ones. [Nemotron-H](https://arxiv.org/abs/2504.03624) (NVIDIA, 2025) runs about 8% of its layers as self-attention, evenly spread. [Granite 4.0](https://www.ibm.com/granite/docs/models/granite4-0) (IBM, October 2025) uses a 9:1 ratio of Mamba-2 blocks to Transformer blocks. It drops positional encodings entirely (a recurrence already knows what order things turned up in), and reports over 70% less memory for long-context and multi-session serving. [Falcon-H1](https://arxiv.org/abs/2507.22448) (TII, 2025) does it differently again. It runs an attention branch and a Mamba-2 branch in parallel inside every layer.

![Diagram of a 24-layer hybrid stack with attention layers spaced evenly among Mamba layers, next to the memory each design keeps per token](/images/blog37/hybrid_stack.png) *Figure 3: A hybrid at the 9:1 ratio Granite 4.0 uses. One typist per nine interpreters, which is roughly the staffing any real conference would have guessed at. Source: Author*

The cleanest evidence for hybrids is NVIDIA's [empirical study](https://arxiv.org/abs/2406.07887). It trained 8B-parameter Mamba, Mamba-2, Transformer and hybrid models on the same 3.5T tokens. The 8B Mamba-2-Hybrid beats the 8B Transformer on all 12 standard tasks, by 2.65 points on average. And it is projected to generate tokens up to 8 times faster. Pure SSMs match or beat the Transformer on plenty of those tasks too. They lose on the ones that need copying something out of the context.

## Where things are going

Hybrids are now the default rather than the experiment. So the open question has moved from *whether* to mix to *what ratio and where*. Everything shipped so far sits between 8% and 11% attention. Every one of those numbers came out of a sweep rather than a theory. Somebody trained 6%, 8% and 12% and wrote down the winner.

The state is also getting bigger and better organised. Mamba-2 grew it 8-fold by simplifying $A$. Mamba-3's multi-input form is chasing arithmetic intensity rather than raw size, because at inference the bottleneck is bytes moved and not maths done. We priced exactly that out in the [speculative decoding post](/blog/speculative-decoding/).

And the kinds of data that were always a bad fit for attention are filling up with these models: audio, genomics and long sensor streams. The sequences there are enormous, and nobody wants a transcript of them.

## So why is there still a typist in the room?

Because a pad of $N$ numbers can only hold $N$ numbers. That is a counting argument, not a tuning problem. [Repeat After Me](https://arxiv.org/abs/2402.01032) (Jelassi et al., 2024) proves that a two-layer Transformer can copy strings exponentially longer than its own size, and that a model with a fixed state cannot. Past some length the copy just fails, and more training will not fix it.

Anything the interpreter decided an hour ago was not worth the pad is gone now. So a pure SSM will follow your argument for an hour, and then lose a six-digit number you gave it in the second sentence. That is the most human failure mode in this whole series.

It shows up in the perplexity too. [Zoology](https://arxiv.org/abs/2312.04927) (Arora et al., 2023) pretrained 17 attention and gated-convolution models. It found the efficient ones trailing attention by up to 2.1 perplexity points on the Pile. 82% of that gap comes down to one thing, which is recalling something mentioned earlier in the context. NVIDIA hit the same wall at 8B scale. The pure SSMs lag on 5-shot [MMLU](https://arxiv.org/abs/2009.03300), a 57-subject multiple choice exam. They also lag on phonebook lookup, which is exactly what it sounds like.

And "attention-free" is not what anybody shipped. Every hybrid above keeps 8 to 11% of its layers as attention, and those are the layers doing the recall. So the honest version of the claim in 2026 is this. You need far less attention than a Transformer hands you, and everything else can run on a pad.

There is a floor under all of it as well. Mamba's scan beats FlashAttention-2 only past about 2,000 tokens. Below that, you have bought an unusual architecture and a much smaller ecosystem of tools, and not a lot else. If your context is a 500-token prompt, the quadratic cost was never your problem.

## Conclusion

Part 1 built the booth: a pad from control theory that runs like an RNN and trains like a CNN, and a $\Delta$ that every word gets to choose. Choosing broke the CNN. Mamba bought the speed back with a relay. Two fade-and-adds squash into one, so the sequence can be chopped up and finished in parallel. A kernel that keeps the pad on the desk did the rest. Mamba-2 noticed that all of this was linear attention in a different form. And then the field stopped arguing and built hybrids.

So is attention all you really need? No, and about 90% of it was never doing much. But go and ask the interpreter for the fourth figure in that table of numbers from an hour ago, the one with all the decimal places, and watch what they do. They will turn to the person sitting next to them, who wrote it down.

And now you know. Fin.
