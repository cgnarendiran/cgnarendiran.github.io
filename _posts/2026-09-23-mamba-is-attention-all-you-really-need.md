---
layout: post
title:  "Mamba - Is Attention All You Really Need?"
date:   2026-09-23
image:  images/blog36/cover.jpg
description: "Attention keeps every word it has ever heard. Mamba keeps one small pad and decides, word by word, what is worth writing on it."
tags: [state-space-models, transformers, attention, llms, efficient-inference]
---

*On the cover: the interpreters' section at the Nuremberg trials, 1945-46, where simultaneous interpretation was first used at scale. Headphones on, a microphone each, and nothing in front of them but a few sheets of notes. Photo by Raymond D'Addario, [public domain](https://commons.wikimedia.org/wiki/File:Interpreters_section.jpg), via Wikimedia Commons.*

In the [KV caching post](/blog/kv-caching-mla-is-attention-all-you-really-need/) we spent two thousand words shrinking the thing attention drags behind it. Every token a model has ever seen is kept as a key and a value, and every new token reads all of them. MLA squeezed that cache down into a latent, and [speculative decoding](/blog/speculative-decoding/) got more tokens out of each read of it. But neither of them changes the shape of the cost. The cache still grows with every word, and the work to produce word $n$ still grows with $n$.

Now try that on sound.

Raw audio at 16,000 samples a second, which is telephone quality and not a nice one, is 960,000 tokens for one minute. A three-hour session comes to about 173 million (one speaker, one language). Attention compares every token with every other token, so that session is around $1.5 \times 10^{16}$ pairs. And nobody has multiplied anything by a weight yet.

Welcome to the era of **selective state space models (SSMs)**. This is the story of how the oldest idea in sequence modelling, a fixed-size running summary, came back from the dead, beat Transformers twice its size, and then quietly agreed to share a building with them.

I want you to think about the interpreter's booth at the back of that conference hall. Glass on three sides, two people inside, headphones on. The speaker is going at 140 words a minute in Portuguese and the interpreter is about two seconds behind in English, and they have not written down a single sentence of what was said. There is no time to. What they have is a small pad, mostly blank, and whatever is in their head right now.

Down in the hall the whole session is being typed up in full, every word, so that anyone can go back six hours later and find the exact sentence. That transcript is attention (the KV cache). The booth is a state space model.

## A pad that never gets any bigger

The typist's pile grows by one line for every line spoken. And a model doing attention has to read the whole pile before it can say the next word. The booth holds the same small pad at minute one and at hour three. So the cost of the next word is flat, no matter how long the speaker has been going.

Let's put a number on that pile. A 7B-shaped model keeps about half a megabyte of cache per token, so ten seconds of that telephone audio fills an 80 GB H100 with nothing but the memory of somebody saying hello. One minute of it wants 480 GB. The booth is still holding the one pad.

| Who is listening | What they keep | Cost of word $n$ | Verdict |
|---|---|---|---|
| The typist (attention) | every word, forever | grows with $n$ | exact recall, and a bill that grows with the meeting |
| The booth (an SSM) | one pad of fixed size | the same as word 1 | constant memory, and it loses whatever it decided not to keep |
| A typist inside the booth (hybrid) | the pad, plus the last stretch on paper | grows slowly | what everybody actually shipped in 2025 |

![Two line charts: attention's cost per token and memory rising with sequence length while the state space model's stay flat](/images/blog36/cost_curves.png) *Figure 1: The same 60 seconds of 16 kHz audio, priced two ways. The right-hand chart is what your GPU actually runs out of first. Source: Author*

The rule for the pad is one line, and you already know it if you have ever kept a running average. Whatever is on the pad fades a bit, whatever just arrived gets written on, and what you say out loud is a read of the pad.

$$
\text{new pad} = (\text{old pad, faded}) + (\text{what just arrived, scaled})
$$

specifically,

$$
h_t = \bar{A} h_{t-1} + \bar{B} x_t, \qquad y_t = C h_t
$$

where $h_t$ is the state (the pad), a vector whose size does not depend on how long the meeting runs, $x_t$ is the input at step $t$, $\bar{A}$ says how much of the pad survives, $\bar{B}$ how much of the new word gets written on it, and $C$ is what gets read back out.

So where do those bars come from? This thing started life in control theory as a continuous system, $h'(t) = Ah(t) + Bx(t)$, which you then sample at some step size $\Delta$. Discretise it with a zero-order hold and $\bar{A} = \exp(\Delta A)$. So $\Delta$ is the dial that sets how fast the pad forgets. A big $\Delta$ means a lot of time went by between words, so the pad fades to nothing and the new word is written over it. A small $\Delta$ means almost no time passed, so the pad survives and the word barely registers at all.

![Diagram of the recurrence unrolled over four steps, with the pad passed along and the delta dial setting how much fades](/images/blog36/recurrence.png) *Figure 2: One pad, four words, no transcript. Everything the model will ever know about word 1 has to fit through the arrow on the left. Source: Author*

[S4](https://arxiv.org/abs/2111.00396) (Gu, Goel and Ré, 2021) is the version of this that made people sit up. It picks $A$ using [HiPPO](https://arxiv.org/abs/2008.07669) theory, which chooses the matrix so that the pad holds the best polynomial summary of everything heard so far, rather than whatever a random initialisation would have settled into. On [Long Range Arena](https://github.com/google-research/long-range-arena), six synthetic tasks built to punish models that cannot hold anything for long, S4 averages about 86%. On the hardest of them, Path-X, you get two dots that are either joined by a dashed line or not, flattened into a sequence of 16,384 pixels. Every model before S4 scored chance on it. S4 scored 96.4%. It also classifies raw speech at 16,000 samples a clip to 98.3%, which is the same task your phone does with a spectrogram, done on the waveform itself.

And here is the part that made it trainable. If $\bar{A}$, $\bar{B}$ and $C$ are the same at every step, the recurrence is a convolution with one very long kernel, and an FFT does that in $O(n \log n)$. So you train it as a convolution and you run it as a recurrence. That trick holds only as long as nothing inside the recurrence is allowed to look at the input, which is going to be a problem.

## The interpreter who fades everything at the same rate

The catch is that an S4 pad fades at a rate fixed at training time. The same $\Delta$ for a phone number as for "and, er, as I was saying". A model doing that has decided in advance how fast to forget, which is a pretty strange way to listen to a human being.

There is a toy task that catches it. **Selective copying** hands the model a sequence of tokens with random junk stuffed between them and asks for the real tokens back in order. Since the junk arrives at unpredictable positions, a constant fade rate cannot separate signal from filler, and gated architectures like [H3](https://arxiv.org/abs/2212.14052) only get part of the way there.

[Mamba](https://arxiv.org/abs/2312.00752) (Gu and Dao, December 2023) changes exactly one thing. $\Delta$, $B$ and $C$ stop being fixed parameters and become functions of the token sitting in front of them:

$$
\Delta_t = \text{softplus}(W_\Delta x_t), \qquad B_t = W_B x_t, \qquad C_t = W_C x_t
$$

where each $W$ is a small learned projection, so the model reads the incoming word and decides on the spot how much of the pad to clear and how much of the word to write. That is the whole contribution, and it is called **selection**.

Let's do one by hand. Take a one-dimensional pad with $A = -1$ and $B = 1$, which discretises to $\bar{A} = e^{-\Delta}$ and $\bar{B} = 1 - e^{-\Delta}$. Say a number arrives ($x = 1$), then three filler words that carry nothing ($x = 0$), and then somebody asks for the number back.

| Word | S4, $\Delta = 0.5$ for everything | Mamba, $\Delta$ chosen per word |
|---|---|---|
| the number | $\bar{B} = 0.393$, pad $= 0.393$ | $\Delta = 2.5$, $\bar{B} = 0.918$, pad $= 0.918$ |
| "and, er" | $\times\, 0.607 \to 0.239$ | $\Delta = 0.02$, $\times\, 0.980 \to 0.900$ |
| "as I was" | $\to 0.145$ | $\to 0.882$ |
| "saying" | $\to 0.088$ | $\to 0.864$ |

Three words of nothing cost the fixed pad 78% of the number. They cost the selective pad about 6%. It is the same recurrence with the same $A$ and the same filler going in. The only difference is whether $\Delta$ was allowed to look at the word before it chose.

![Two decay curves over the same four words, the fixed-delta pad dropping to 0.088 and the selective pad holding at 0.864](/images/blog36/delta_worked.png) *Figure 3: The worked example above, drawn. The selective pad kept the number because $\Delta$ was close to zero during "and, er". So almost nothing faded. Source: Author*

So what does selection actually buy? On selective copying the best non-selective baseline in the Mamba paper's table gets 57%, and making $\Delta$, $B$ and $C$ input-dependent takes it to 99.8%. On induction heads, where the model sees a pattern once and has to complete it later, Mamba trains at sequence length 256 and still scores near 100% at length 1,000,000. That is 4,000 times longer than anything it saw. The other architectures start falling over a few hundred tokens past their training length.

## The relay

Selection breaks the trick that made S4 trainable. If $\bar{A}$ changes at every step, then there is no single convolution kernel and so no FFT. You are back to a for-loop over 960,000 samples. On a GPU a loop like that wastes almost the whole card, because every core sits idle waiting for the step in front of it to finish.

What saves it is that the recurrence is associative. "Fade by $a_1$ then add $b_1$", followed by "fade by $a_2$ then add $b_2$", is itself just a fade-and-add: fade by $a_1a_2$, add $a_2b_1 + b_2$. So you can chop the sequence into chunks, work out each chunk's fade-and-add independently on its own core, and combine them afterwards. This is a **parallel scan**. And if you think about it, it is what the booth does on a long day anyway. Interpreters work in pairs and swap every twenty minutes or so (the profession worked out its own context limit a long time before we did). The one coming on gets about ten seconds of whispered summary (the state), not the last twenty minutes again.

![Diagram of a sequence split into four chunks, each chunk reduced to one fade-and-add pair, then combined pairwise into the final state](/images/blog36/parallel_scan.png) *Figure 4: A parallel scan over four chunks. Each booth handles its own stretch and hands over a state, which is the only reason any of this trains in a reasonable time. Source: Author*

Then there is the engineering, which is half the paper. Mamba's pad is sixteen numbers wide per channel by default (that is the number in the released code, not a result anybody proved), and sixteen numbers is small enough to live in a GPU's SRAM. So the kernel loads the parameters up from HBM once, does the discretisation and the whole scan up there, and writes back only the output. Intermediate states are not saved at all, they are recomputed during the backward pass, which is cheaper than the round trip to memory would be. That fused kernel runs 20 to 40 times faster than the same thing written naively in PyTorch. And past a sequence length of about 2,000 it beats [FlashAttention-2](https://arxiv.org/abs/2307.08691), which was the fastest attention kernel anybody had.

## What the booth buys you

Mamba-3B, trained on [the Pile](https://arxiv.org/abs/2101.00027), 800 GB of mixed web text, books and code, beats Transformers of its own size and matches ones twice as big. It comes in 4 points ahead of [Pythia](https://arxiv.org/abs/2304.01373)-3B on common sense reasoning, and ahead of Pythia-7B as well. Pythia is the open model family everybody was using as a like-for-like baseline back then. Inference throughput is about 5 times a Transformer's at the same size, and that is mostly down to batching. There is no cache to read, so a lot more sequences fit on the card at once.

The audio numbers convince me more than the language ones, because audio is where the transcript was always going to lose. On SC09, a benchmark of one-second clips of people saying the digits zero to nine, which is the most boring possible way to prove that an architecture can hear:

| Model | Parameters | FID (lower is better) | Verdict |
|---|---|---|---|
| [WaveNet](https://arxiv.org/abs/1609.03499) | 4.2M | 5.08 | the 2016 baseline, dilated convolutions |
| [SaShiMi](https://arxiv.org/abs/2202.09729) (S4) | 5.8M | 1.99 | state spaces, no selection |
| Mamba | 6.1M | 0.94 | half the error of the previous best, at the same size |

![Bar chart of SC09 audio quality for WaveNet, SaShiMi and Mamba, next to a bar chart of inference throughput for a Transformer and for Mamba](/images/blog36/results.png) *Figure 5: Six million parameters generating one-second waveforms, and the throughput you get when there is nothing to re-read. Source: Author*

## The evolution

- **Mamba-2 (2024)**: [Transformers are SSMs](https://arxiv.org/abs/2405.21060) restricts $A$ to a scalar times the identity. That is a real loss of expressiveness, and it turns the scan into a sequence of matrix multiplications, which is the one thing a GPU is genuinely built for. You get 8 times larger states, 50% faster training, and a core layer 2 to 8 times quicker than Mamba-1's scan. The theory that comes with it, **state space duality**, shows that attention with a particular structured mask and a state space model are the same computation written two ways. Two subfields had been writing out the same algorithm for years, and it took a paper with a picture in it before either of them would admit it.
- **Mamba-3 (2026)**: [Mamba-3](https://arxiv.org/abs/2603.15569) (ICLR 2026) swaps Euler discretisation for a trapezoidal rule, brings back complex-valued states so the pad can track things that oscillate, and adds a multi-input multi-output form that gets more arithmetic out of each byte moved during decoding. The complex-valued part connects straight back to the [RoPE post](/blog/rope-is-attention-all-you-really-need/): a complex SSM is doing a data-dependent rotary embedding.
- **The hybrids (2024 onwards)**: [Jamba](https://arxiv.org/abs/2403.19887) (AI21, 2024) put attention layers back in among the Mamba ones. [Nemotron-H](https://arxiv.org/abs/2504.03624) (NVIDIA, 2025) runs about 8% of its layers as self-attention, evenly spread. [Granite 4.0](https://www.ibm.com/granite/docs/models/granite4-0) (IBM, October 2025) uses a 9:1 ratio of Mamba-2 blocks to Transformer blocks, drops positional encodings entirely (a recurrence already knows what order things turned up in), and reports over 70% less memory for long-context and multi-session serving. [Falcon-H1](https://arxiv.org/abs/2507.22448) (TII, 2025) does it differently again, running an attention branch and a Mamba-2 branch in parallel inside every layer.

![Diagram of a 24-layer hybrid stack with attention layers spaced evenly among Mamba layers, next to the memory each design keeps per token](/images/blog36/hybrid_stack.png) *Figure 6: A hybrid at the 9:1 ratio Granite 4.0 uses. One typist per nine interpreters, which is roughly the staffing any real conference would have guessed at. Source: Author*

The cleanest evidence for hybrids is NVIDIA's [empirical study](https://arxiv.org/abs/2406.07887), which trained 8B-parameter Mamba, Mamba-2, Transformer and hybrid models on the same 3.5T tokens. The 8B Mamba-2-Hybrid beats the 8B Transformer on all 12 standard tasks, by 2.65 points on average. And it is projected to generate tokens up to 8 times faster. Pure SSMs match or beat the Transformer on plenty of those tasks too. They lose on the ones that need copying out of the context.

## Where things are going

Hybrids are now the default rather than the experiment, and the interesting question has moved from *whether* to mix to *what ratio and where*. Everything shipped so far sits between 8% and 11% attention, and every one of those numbers came out of a sweep rather than a theory. Somebody trained 6%, 8% and 12% and wrote down the winner.

The state is also getting bigger and better organised. Mamba-2 grew it 8-fold by simplifying $A$, and Mamba-3's multi-input form is chasing arithmetic intensity rather than raw size, because at inference the bottleneck is bytes moved and not maths done. We priced exactly that out in the [speculative decoding post](/blog/speculative-decoding/).

And the modalities that were always a bad fit for attention are filling up with these models: audio, genomics and long sensor streams, where the sequences are enormous and nobody wants a transcript of them.

## So why is there still a typist in the room?

Because a pad of $N$ numbers can only hold $N$ numbers, and that is a counting argument rather than a tuning problem. [Repeat After Me](https://arxiv.org/abs/2402.01032) (Jelassi et al., 2024) proves that a two-layer transformer can copy strings exponentially longer than its own size, and that a model with a fixed state cannot. Past some length the copy just fails, and more training will not fix it. Anything the interpreter decided an hour ago was not worth the pad, is gone now. So a pure SSM will follow your argument for an hour and then lose a six-digit number you gave it in the second sentence, which is the most human failure mode in this whole series.

It shows up in the perplexity too. [Zoology](https://arxiv.org/abs/2312.04927) (Arora et al., 2023) pretrained 17 attention and gated-convolution models and found the efficient ones trailing attention by up to 2.1 perplexity points on the Pile. 82% of that gap comes down to one thing, which is recalling something that was mentioned earlier in the context. NVIDIA hit the same wall at 8B scale. The pure SSMs lag on 5-shot [MMLU](https://arxiv.org/abs/2009.03300), a 57-subject multiple choice exam. They also lag on phonebook lookup, which is exactly what it sounds like.

And "attention-free" is not what anybody shipped. Every hybrid above keeps 8 to 11% of its layers as attention, and those are the layers doing the recall. So the honest version of the claim in 2026 is that you need far less attention than a Transformer hands you, and that everything else can run on a pad.

There is a floor under all of it as well. Mamba's scan beats FlashAttention-2 past about 2,000 tokens, so below that you have bought an unusual architecture and a much smaller ecosystem of tools and not a lot else. If your context is a 500-token prompt, the quadratic term was never your problem.

## Conclusion

From S4 to Mamba-3, what changed is only what the interpreter is allowed to do with the pad.

S4 gave them a pad and a fixed rule for how fast to forget. That was enough to solve tasks 16,000 steps long, but not enough to follow a sentence with a phone number in it. Mamba let the rule look at the word first, which cost the FFT and bought the parallel scan back with an associativity trick and a kernel that never leaves SRAM. Mamba-2 noticed that this was linear attention wearing a different hat. And then the field stopped arguing and built hybrids.

So is attention all you really need? No, and about 90% of it was never doing much. But go and ask the interpreter for the fourth figure in that table of numbers from an hour ago, the one with all the decimal places, and watch what they do. They will turn to the person sitting next to them, who wrote it down.

And now you know. Fin.
