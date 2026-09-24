---
layout: post
title:  "Mamba - Is Attention All You Really Need? Part 1"
date:   2026-09-23
image:  images/blog36/cover.jpg
description: "State space models come from control theory, run like an RNN and train like a CNN. Mamba's one change lets each word decide what the model remembers."
tags: [state-space-models, attention, cnn, lstm, transformers]
---

*On the cover: the interpreters' section at the Nuremberg trials, 1945-46, where simultaneous interpretation was first used at scale. Headphones on, a microphone each, and nothing in front of them but a few sheets of notes. Photo by Raymond D'Addario, [public domain](https://commons.wikimedia.org/wiki/File:Interpreters_section.jpg), via Wikimedia Commons.*

In the [KV caching post](/blog/kv-caching-mla-is-attention-all-you-really-need/) we spent two thousand words shrinking the thing attention drags behind it. A Transformer keeps every token it has seen as a key and a value (the KV cache). Every new token reads all of them. MLA squeezed that cache down into a smaller latent. And [speculative decoding](/blog/speculative-decoding/) got more tokens out of each read of it. But neither of them changes the shape of the cost. The cache still grows with every word. And the work to produce word $n$ still grows with $n$.

Now try that on sound.

Raw audio at 16,000 samples a second is telephone quality, and not a nice telephone either. Treat each sample as a token and one minute of it is 960,000 tokens. A three-hour session is about 173 million. Attention compares every token with every other token, so that session comes to around $1.5 \times 10^{16}$ pairs.

To be fair, nobody actually feeds a Transformer raw samples. Speech models like [Whisper](https://arxiv.org/abs/2212.04356) first turn the audio into a spectrogram, a picture of which frequencies are loud in each 10-millisecond slice. Then they squash that down to about 50 tokens a second. It works, but it is a hand-built shortcut that throws detail away before the model hears anything. The real question is whether a model could just listen to the raw waveform.

Welcome to the era of **state space models (SSMs)**. This is the story of how an idea control engineers have used since 1960, a small running summary that never grows, got rebuilt into a sequence model that runs like an RNN and trains like a CNN.

## Two ways to follow a conference

I want you to think about a conference hall. The speaker is going at 140 words a minute in Portuguese, and the audience wants English. There are two ways to get it to them.

The first is a typist in the hall. They type up the whole session, every word. Six hours later anyone can go back and find the exact sentence. That is attention, and the typed pile is the KV cache.

The second is the interpreter's booth at the back of the room. Glass on three sides, two people inside, headphones on. The interpreter is about two seconds behind the speaker. They have not written down a single sentence of what was said, because there is no time to. What they have is a small pad, mostly blank, and whatever is in their head right now. That pad is the **state**, and the booth is a state space model.

## The problem: a pile that never stops growing

The typist's pile grows by one line for every line spoken. Before the model can say its next word, it has to read the whole pile. So word 1,000 costs a thousand reads, and word 1,000,000 costs a million.

The booth holds the same small pad at minute one and at hour three. So the cost of the next word stays flat, however long the speaker goes on.

Let's put a number on that pile. A 7B-shaped model keeps about half a megabyte of cache per token. Ten seconds of that telephone audio is 160,000 tokens. So ten seconds fills an 80 GB H100 with nothing but the memory of somebody saying hello. One minute of it wants 480 GB. The booth is still holding the one pad.

| Who is listening | What they keep | Cost of word $n$ | Verdict |
|---|---|---|---|
| The typist (attention) | every word, forever | grows with $n$ | exact recall, and a cost that grows with the meeting |
| The booth (an SSM) | one pad of fixed size | the same as word 1 | constant memory, and it loses whatever it decided not to keep |

![Two line charts: attention's cost per token and memory rising with sequence length while the state space model's stay flat](/images/blog36/cost_curves.png) *Figure 1: The same 60 seconds of 16 kHz audio, priced two ways. The right-hand chart is what your GPU actually runs out of first. Source: Author*

So why doesn't everybody use the pad? Because a pad of fixed size has to forget things. The whole question is what it forgets, and who gets to decide.

## A pad, in plain maths

You already know the simplest pad. It is a running average. Say you want to track the temperature over a long day, but you only have room to write down one number. Every hour you fade the old number a bit and mix in the new reading.

$$
\text{new pad} = (\text{old pad, faded}) + (\text{new reading, scaled})
$$

specifically,

$$
h_t = \bar{A} h_{t-1} + \bar{B} x_t, \qquad y_t = C h_t
$$

where $h_t$ is the state (the pad), $x_t$ is the input at step $t$ (the new word), $\bar{A}$ says how much of the old pad survives, $\bar{B}$ says how much of the new word gets written on, and $C$ says what gets read back out as the output $y_t$.

In a real model $h_t$ is a vector of numbers, not one number. But its size never depends on how long the input is. That is the whole point of it.

So how far back can the pad reach? There is no window and no cut-off. Every word the model has ever heard is still on the pad, just faded. What sets the reach in practice is how fast it fades. If each step keeps 99% of the pad, a word from 100 steps ago is down to about a third. A word from 1,000 steps ago is basically gone. Learn a slower fade and the reach gets longer, at no extra cost.

A Transformer is the opposite. Its recall is exact, but it has a hard edge: the context length it was trained at. [RoPE](/blog/rope-is-attention-all-you-really-need/) does not remove that edge. It only tells the model how far apart two tokens are. Push a model well past its training length and it usually falls apart, which is why stretching tricks like [YaRN](https://arxiv.org/abs/2309.00071) exist. And inside the window, every extra token still costs its line in the cache.

If you read the [Kalman filter post](/blog/kill-john-connor-using-kalman-filter/), this should look familiar. There the state was a motorcycle's position and velocity, and a physics model rolled it forward one step at a time. It is the same shape of equation. The Terminator just wanted a different output.

## Where the name comes from

"State space" is control theory's phrase, not machine learning's. Control engineers describe a system (a car's cruise control, a thermostat, a rocket) by a small set of numbers that capture everything about it right now. That set of numbers is the state. The state space is the set of all the states the system could be in.

The system then follows a rule in continuous time:

$$
h'(t) = A h(t) + B x(t), \qquad y(t) = C h(t)
$$

In words, how fast the state changes depends on the state itself ($A$) and on whatever is pushing on it from outside ($B$). Rudolf Kálmán made this way of writing systems the standard around 1960. Most of control engineering has run on it since.

A thermostat makes it concrete. The state is the room's temperature. $A$ is negative, because a warm room drifts back toward the temperature outside. $B$ is how hard the heater pushes. Switch the heater off and the room slowly forgets it was ever warm.

But a language model does not get a continuous signal. It gets words, one at a time. So you sample the continuous system at steps of size $\Delta$, which is called discretisation. The standard method is the zero-order hold (it simply assumes the input stays constant between two samples).

Where does the maths come from? Switch the input off for a moment, so the rule is just $h' = Ah$. The state changes at a rate proportional to itself. The only function that does that is an exponential, the same one behind radioactive decay and compound interest. So after a time $\Delta$ the pad has been multiplied by $e^{\Delta A}$. Now switch the input back on, hold it constant over the step, and add up how much of it lands on the pad. For a one-number pad that gives

$$
\bar{A} = e^{\Delta A}, \qquad \bar{B} = \frac{e^{\Delta A} - 1}{A}\,B
$$

The bar just means "per step". $A$ is a rate, how fast the pad changes at any instant. $\bar{A}$ is what that rate adds up to over one step of length $\Delta$. Mamba keeps $A$ negative. So $\bar{A}$ always lands between 0 and 1, and every step is a fade. You can think of $\Delta$ as how much time passes between two words. A big $\Delta$ means a lot of time went by. So the old pad fades to almost nothing and the new word takes over. A small $\Delta$ means almost no time passed. So the pad survives and the new word barely registers. That makes $\Delta$ the dial for how fast the pad forgets, and Mamba is going to grab it.

## An RNN and a CNN at the same time

Here is the part that surprised me the first time I saw it. That one little equation can be computed in two completely different ways. And both give exactly the same answer.

**The RNN way.** Walk through the input one word at a time. Keep one pad. At every step, fade it and write the new word on. This is what a recurrent neural network (RNN) does, and it is how LSTMs did machine translation before Transformers. It is perfect for generating text. Each new word costs the same, and the memory stays fixed.

But it is terrible for training. Step 1,000 cannot start until step 999 has finished. A GPU has thousands of cores, and a loop like that leaves almost all of them waiting. Old RNNs had a second problem as well. Their training signal faded over long sequences (the vanishing gradient problem), so they struggled to remember anything from a few hundred steps back.

**The CNN way.** Now notice something about the equation. $\bar{A}$, $\bar{B}$ and $C$ are the same at every step. So you can unroll the recurrence and write each output straight from the inputs:

$$
y_t = C\bar{B}\,x_t + C\bar{A}\bar{B}\,x_{t-1} + C\bar{A}^2\bar{B}\,x_{t-2} + \dots
$$

Each past word is weighted by a fixed number. That number depends only on how long ago the word arrived. Put those numbers in a list and you have a kernel:

$$
K = \left(C\bar{B},\; C\bar{A}\bar{B},\; C\bar{A}^2\bar{B},\; \dots\right)
$$

Sliding one fixed kernel along a sequence is exactly what a convolutional neural network (CNN) does. And a convolution computes every output position at once. With an FFT it costs $O(n \log n)$ for a sequence of length $n$. Every core on the GPU has something to do.

Let's do one by hand, with a single number on the pad. Take $A = -1$, $B = 1$, $C = 1$ and $\Delta = 0.5$. That gives $\bar{A} = e^{-0.5} = 0.607$ and $\bar{B} = 1 - e^{-0.5} = 0.393$. Now feed in four words with the values $x = (1, 0, 2, 0)$.

The RNN way, one step at a time:

1. Word 1: pad $= 0.393 \times 1 = 0.393$
2. Word 2: pad $= 0.607 \times 0.393 = 0.239$
3. Word 3: pad $= 0.607 \times 0.239 + 0.393 \times 2 = 0.932$
4. Word 4: pad $= 0.607 \times 0.932 = 0.565$

The CNN way, all at once. The kernel is $K = (0.393, 0.239, 0.145, 0.088)$, which is just $0.393$ faded by $0.607$ once more at every step. The output at word 3 is $0.393 \times 2 + 0.239 \times 0 + 0.145 \times 1 = 0.932$. That is the same number, and nobody ever built a pad to get it.

![Top: four pad boxes chained left to right, each fading by 0.607 and taking in a word, giving outputs 0.393, 0.239, 0.932 and 0.565. Bottom: the decaying kernel 0.393, 0.239, 0.145, 0.088 as bars, and the weighted sum that gives 0.932 at word 3](/images/blog36/two_views.png) *Figure 2: The worked example computed both ways. The RNN carries a pad from word to word. The CNN slides a kernel and never builds the pad at all. Source: Author*

So you train it as a CNN, with the whole sequence in parallel. And you run it as an RNN, one cheap step per word. The 2021 paper that set this out put all three views in its title: [Combining Recurrent, Convolutional, and Continuous-time Models with Linear State-Space Layers](https://arxiv.org/abs/2110.13985) (Gu et al., 2021). That is where "an RNN and a CNN at the same time" comes from, and it is a fair description.

| View | The equation | What you use it for | Verdict |
|---|---|---|---|
| Continuous (control theory) | $h' = Ah + Bx$ | choosing $A$ and $\Delta$ with real maths | where the theory lives |
| Recurrent (RNN) | $h_t = \bar{A}h_{t-1} + \bar{B}x_t$ | generating, one word at a time | constant memory, slow to train |
| Convolutional (CNN) | $y = K * x$ | training, the whole sequence at once | fast on a GPU, but only while $\bar{A}$, $\bar{B}$ and $C$ never change |

## S4: a pad that actually remembers

The two views fix the speed problem. They do not fix the memory problem. With a random $A$ the kernel dies off within a few steps. So the pad forgets everything except the last few words, which is the same problem the old RNNs had.

[S4](https://arxiv.org/abs/2111.00396) (Gu, Goel and Ré, 2021) fixes it by choosing $A$ carefully. It uses [HiPPO](https://arxiv.org/abs/2008.07669) theory, which picks the matrix so that the pad holds the best polynomial summary of everything heard so far. Think of drawing the smoothest curve you can through the whole history, and then keeping only that curve's few coefficients. Those coefficients are what goes on the pad.

It works. [Long Range Arena](https://github.com/google-research/long-range-arena) is a set of six synthetic tasks built to punish models that cannot hold anything for long, and S4 averages about 86% on it. The hardest task is Path-X. You get two dots that are either joined by a dashed line or not, flattened into a sequence of 16,384 pixels. Every model before S4 scored chance on it. S4 scored 96.4%.

It also classifies raw speech at 16,000 samples a clip to 98.3%. Your phone does the same task from a spectrogram. S4 does it straight from the waveform.

## The interpreter who fades everything at the same rate

S4 still has one fixed $\Delta$. It is learned during training and then frozen. So the pad fades at the same rate for a phone number as for "and, er, as I was saying". The model has decided in advance how fast to forget, which is a pretty strange way to listen to a human being.

There is a toy task that catches it. **Selective copying** hands the model a few real tokens with random junk stuffed between them, and asks for the real tokens back in order. The junk arrives at unpredictable positions. A fixed fade rate treats junk and signal exactly the same, so it cannot keep one and drop the other. Gated models like [H3](https://arxiv.org/abs/2212.14052) only get part of the way there.

## Mamba: let the word choose

[Mamba](https://arxiv.org/abs/2312.00752) (Gu and Dao, December 2023) changes exactly one thing. $\Delta$, $B$ and $C$ stop being fixed numbers. They become functions of the word sitting in front of them:

$$
\Delta_t = \text{softplus}(W_\Delta x_t), \qquad B_t = W_B x_t, \qquad C_t = W_C x_t
$$

where each $W$ is a small learned projection. So the model reads the incoming word and decides, on the spot, how much of the pad to clear and how much of the word to write. That is the whole idea, and it is called **selection**. A filler word can get a tiny $\Delta$, so the pad barely changes. A number worth keeping can get a big one.

![Diagram of the recurrence unrolled over four words, with the pad passed along and delta set big or small for each word](/images/blog36/recurrence.png) *Figure 3: The same recurrence, except that now each word sets its own $\Delta$. Source: Author*

Let's do one by hand again, with the same one-number pad from before. A number arrives ($x = 1$), then three filler words that carry nothing ($x = 0$), and then somebody asks for the number back.

| Word | S4, $\Delta = 0.5$ for everything | Mamba, $\Delta$ chosen per word |
|---|---|---|
| the number | $\bar{B} = 0.393$, pad $= 0.393$ | $\Delta = 2.5$, $\bar{B} = 0.918$, pad $= 0.918$ |
| "and, er" | $\times\, 0.607 \to 0.239$ | $\Delta = 0.02$, $\times\, 0.980 \to 0.900$ |
| "as I was" | $\to 0.145$ | $\to 0.882$ |
| "saying" | $\to 0.088$ | $\to 0.864$ |

The S4 column is the kernel from the last section, read top to bottom. Three words of filler cost the fixed pad 78% of the number. They cost the selective pad about 6%. It is the same recurrence, with the same $A$ and the same filler going in. The only difference is whether $\Delta$ was allowed to look at the word before it chose.

![Two decay curves over the same four words, the fixed-delta pad dropping to 0.088 and the selective pad holding at 0.864](/images/blog36/delta_worked.png) *Figure 4: The worked example above, drawn. The selective pad kept the number because $\Delta$ was close to zero during "and, er". So almost nothing faded. Source: Author*

So what does selection actually buy? On selective copying, the best non-selective model in the Mamba paper's table gets 57%. Making $\Delta$, $B$ and $C$ depend on the input takes it to 99.8%. On induction heads, the model sees a pattern once and has to complete it later. Mamba trains at sequence length 256 and still scores near 100% at length 1,000,000. That is 4,000 times longer than anything it saw in training. The other architectures start falling over a few hundred tokens past their training length.

## The catch

So are we done? Look back at the CNN view. It only worked because $\bar{A}$, $\bar{B}$ and $C$ were the same at every step. That is what let one fixed kernel slide along the whole sequence.

Selection changes them at every step. The fade after a phone number is different from the fade after "and, er". So there is no single kernel to slide, and no FFT to run. You are back to the RNN way: a loop over 960,000 samples, one step at a time, with most of the GPU sitting idle. Mamba built a much better interpreter, and in doing so it lost the fast way to train one.

## Conclusion

State space models come from control theory, where a small state rolled forward by $h' = Ah + Bx$ has been running cruise controls and rockets since the 1960s. Written for words instead of time, the same equation is an RNN when you step through it and a CNN when you unroll it. S4 chose $A$ so the pad would actually remember, and trained it as a CNN. Mamba let every word choose its own $\Delta$. That fixed the forgetting, and it broke the CNN.

Part 2 is how Mamba got its speed back. The trick is one that interpreters already use on a long day, and by the end of it there is a typist back in the room.

Stay tuned for Part 2. Till then ciao.
