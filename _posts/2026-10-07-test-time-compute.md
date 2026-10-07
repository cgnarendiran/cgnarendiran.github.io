---
layout: post
title:  "Test-Time Compute - Order One More Test"
date:   2026-10-07
image:  images/blog43/cover.png
description: "A model can be made better after it is trained, just by letting it answer for longer. Almost all of that gain comes from the thing that checks the answer."
tags: [test-time-compute, llms, reinforcement-learning, efficient-inference]
---

*On the cover: four chest films on a backlit viewer, each carrying more pencil rings than the one before it, and a fifth viewer switched on with nothing clipped to it yet. That empty one is the next test somebody could order. Source: Author.*

A doctor in a crowded government outpatient department gets about seven minutes per patient. You look at them, ask three questions, write something on the chit and call the next name. For a sprained ankle that is plenty of time.

Then somebody comes in with a fever that has run three weeks and nothing else. Her chest is clear and the blood count came back ordinary. Seven minutes is not going to do it, and you know that inside thirty seconds.

So you do the other thing. You order a test, read what comes back, and depending on what it says you order another one.

A language model does not get to do that. You ask it something and it answers in one pass, at the same speed, with the same confidence, whether you asked for the boiling point of water or for a proof. The sprained ankle and the three-week fever both get seven minutes.

Welcome to the era of **test-time compute**. This is the story of what you can still buy after a model has finished training, and of why almost all of it belongs to whatever is checking the answer.

One bit of vocabulary first. **Test time** is the ML term for when a model is answering, as opposed to **training time**, when its weights are still moving. A test in the OPD is a blood count. I will say **workup** for that one.

## Buying more of two different things

"Spend more compute at test time" means one of two things, and they behave differently.

![Side by side: one long chain of reasoning steps with a revision loop on the left, and four short parallel chains feeding into a selector box on the right](/images/blog43/sequential-and-parallel.png) *Figure 1: the two axes. Left, one answer written for longer. Right, several answers and something that picks between them. The green box is doing more work than it looks like. Source: Author*

The first is **sequential**: one answer, written for longer. The model writes its working out loud before it commits, which is a **chain of thought** ([Wei et al., 2022](https://arxiv.org/abs/2201.11903)). And a longer chain gives it more chances to catch its own mistake. Eight worked examples in the prompt took PaLM-540B from 17.9% to 56.9% on [GSM8K](https://huggingface.co/datasets/openai/gsm8k), a set of 8,500 grade-school word problems. The weights never moved. What changed is that the prompt now showed it worked solutions, so it wrote its own working out instead of guessing a number. That working is what costs the extra **tokens**, the chunks of text a model reads and writes, roughly three-quarters of a word each.

The second is **parallel**: ask the same question $N$ times at a **temperature** above zero, collect $N$ different answers, and keep one. Temperature is the randomness knob on picking each next token. At zero you get the same answer every time.

In the OPD it is the same split. Sequential is one patient and one long afternoon: read the first result, decide what to order next, read that. Parallel is sending the same slide to five pathologists (a panel) and seeing what comes back. One of them costs you time. The other one costs you five pathologists.

## The arithmetic of trying again

Why would asking the same question eight times help at all, when it is the same model every time? Let's do the sums.

Take one problem. Say a single attempt has a chance $p$ of getting it right, and pretend for a moment that the attempts do not influence each other. Then the chance that at least one of $N$ attempts lands, is one minus the chance that every one of them misses:

$$\text{chance at least one of } N \text{ is right} = 1 - (\text{chance one attempt is wrong})^{N}$$

specifically,

$$\text{pass@}N = 1 - (1-p)^{N}$$

where $p$ is the probability a single attempt gets *that* problem right, $N$ is how many attempts you buy, and pass@$N$ is the chance of having a correct answer somewhere in the pile. Averaged over a whole benchmark it gets called **coverage**. At $N = 1$ the formula collapses to $p$, which is why you see **pass@1** quoted as a plain accuracy score.

Two warnings before anybody takes that formula too seriously. The attempts are not really independent, because it is the same weights on the same question and it tends to go wrong the same way twice. And $p$ belongs to one problem, not to a benchmark. A benchmark average hides a huge spread: a handful the model gets most of the time, and a long tail it will never get.

That spread is why coverage behaves the way it does. [Large Language Monkeys](https://arxiv.org/abs/2407.21787) (Brown et al., 2024) ran Pythia-160M, a 160-million-parameter model from 2023 that nobody built for maths, against [MATH](https://huggingface.co/datasets/qwedsacf/competition_math), a set of competition problems. It solves 0.27% on one attempt. Ten thousand attempts later it has a correct solution somewhere in the pile for 57% of them, and not the 100% you would get by putting $p = 0.0027$ into that formula and leaving it there. That gap is the long tail. The authors named their dataset Monkey Business, which is about the right response to having run that experiment.

Coverage keeps climbing over four orders of magnitude of samples. DeepSeek-Coder-V2-Instruct solves 15.9% of [SWE-bench Lite](https://www.swebench.com/) issues, real bugs from real GitHub repositories, on one attempt. At 250 attempts, 56% of those issues have a working patch somewhere in the pile.

![A log-scale plot of coverage rising from 15.9 percent at one try to 56 percent at 250 tries, beside a bar chart of three selection methods scoring 69.6, 72.4 and 78.2 percent](/images/blog43/coverage-and-selection.png) *Figure 2: (a) how high the ceiling goes on SWE-bench Lite as you buy attempts. (b) how much of it you reach on MATH, which depends entirely on how you choose. Different models and benchmarks, so read them as two facts, not one curve. Source: Author*

## Somebody has to read the reports

A pile of 250 patches is not a patch. You have to submit one, and the rule you use to pick is where the gain lives or dies. Three rules do most of the work in practice.

1. **Majority vote**, or **self-consistency** ([Wang et al., 2022](https://arxiv.org/abs/2203.11171)): take whichever final answer shows up most often and bin the working. Nothing trained, no answer key. On PaLM-540B it added about 18 points on GSM8K, 56.5% to 74.4% (its baseline is measured a little differently from the 56.9% above, which is what happens between two papers).
2. **Best-of-N**: train a **reward model**, a network that reads a finished answer and returns a number, then submit whichever answer it liked most. I will say **verifier** for anything that separates right from wrong, be it a unit test, an answer key or a trained reward model.
3. **Weighted vote**: add up the reward model's opinion across every sample that reached the same answer. Formally,

$$\hat{a} = \arg\max_{a} \sum_{i=1}^{N} \mathbb{1}[a_i = a] \cdot r(x, y_i)$$

where $x$ is the question, $y_i$ is the $i$-th full answer, $a_i$ is the final answer it arrived at, $r(x, y_i)$ is the reward model's score for that answer, and $\mathbb{1}[a_i = a]$ is 1 when sample $i$ landed on candidate $a$ and 0 otherwise. So it is majority vote where each vote carries a weight.

Let's do one by hand. Say you sampled eight answers to one problem and they landed on three different numbers:

| final answer | how many of the 8 | best score | score-weighted total | which rule picks it |
|---|---|---|---|---|
| 180 | 4 | 0.31 | 1.06 | majority vote |
| 204 | 3 | 0.95 | 2.58 | best-of-N, and weighted vote |
| 97 | 1 | 0.12 | 0.12 | nothing picks this |

The right answer is 204. Majority vote loses this one because the model made the same plausible slip four times out of eight, and a show of hands cannot tell a popular mistake from a right answer. Those numbers are mine, invented to make the three rules disagree. In a real run they mostly agree, which is why majority voting is still around.

## The discharge summary and the whole chart

So train a better reward model, and the question becomes what you show it while it learns.

An **outcome reward model** sees the question and the final answer and learns to say right or wrong. It is the consultant who reads the discharge summary. A **process reward model** scores every line of the working as the working is written. It is the audit that goes through the whole chart and puts a mark against the line where the reasoning went off.

![Top row: a chain of five steps with one label at the end. Middle row: the same chain with a score under every step and step three flagged. Bottom row: a beam search keeping the best two of four candidates at each round](/images/blog43/outcome-vs-process-model.png) *Figure 3: an outcome model marks the last line. A process model marks every line, which is what lets a search prune a chain before it finishes. Source: Author*

[Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) (Lightman et al., 2023) is the paper that settled this. The team paid humans to label 800,000 individual reasoning steps in model-written solutions to MATH problems (somebody's job, for months), released it as PRM800K, and trained both kinds. Choosing from 1,860 samples per problem, majority voting solved 69.6%, the outcome model 72.4%, and the process model 78.2%. The gap widened as $N$ went up, so the process model is the only one of the three that keeps paying as you buy more samples.

Marking every line also buys you the ability to stop early. If the process model marks step 3 at 0.12, there is no reason to finish the chain. You prune it and spend the budget on a branch that is still alive. Do that at every step, keeping only the few best partial chains and extending those, and you have a **beam search over reasoning steps**. It is the bet AlphaGo made in the [AlphaZero post](/blog/mcts-alphazero-part2/), where a value network scored a position nobody had finished playing out.

## What the extra time is worth against a bigger model

I want you to put a price on that long chain. Generating one token costs roughly two floating-point operations per parameter, so:

$$\text{inference cost} \approx 2 \times (\text{parameters}) \times (\text{tokens generated})$$

Now check what that means. A 7B model writing 10,000 thinking tokens spends $2 \times 7\times10^{9} \times 10^{4} = 1.4 \times 10^{14}$ operations on your one question. A 350B model answering in 200 tokens spends $2 \times 3.5\times10^{11} \times 200$, the same $1.4 \times 10^{14}$. The arithmetic bill is identical, and the small one gets fifty times the thinking.

So which one do you want? That 50:1 is my arithmetic, picked to make the trade visible. [Snell et al. (2024)](https://arxiv.org/abs/2408.03314) measured it with the floating-point operations (FLOPs) matched on both sides, and found a small model given its compute at test time beating one fourteen times larger. Fourteen and not fifty, so the real exchange rate is worse than my envelope. A model fourteen times smaller still wins. Spending per question instead of evenly got the same score for about a quarter of the compute of plain best-of-N, because an easy question does not need the panel. [Wu et al. (2024)](https://arxiv.org/abs/2408.00724) found the same shape with a tree search: Llemma-7B beat Llemma-34B on MATH at every budget they tried.

And then the result that cuts the other way. The 14× only holds on problems where the smaller model already had a fair chance of getting there on its own. Where it had essentially none, the extra budget bought nothing and the bigger model won. Coverage is a multiplier on $p$, and fourteen times nothing is still nothing. This does not contradict the monkeys, by the way, though it looks like it should. Pythia's 57% is coverage, which only says a right answer was in the pile. Snell is counting answers you could submit, at a budget somebody would really pay. Order the full workup on a disease the lab has no assay for, and you lose the afternoon and learn nothing.

## When the thinking is trained in

Everything so far bolts the search on from outside. The 2025 reasoning models moved it inside the weights.

[DeepSeek-R1](https://arxiv.org/abs/2501.12948) is the clearest public account. R1-Zero took DeepSeek-V3-Base and ran GRPO against rewards a script could check, with no human preference data at all. GRPO samples a group of answers and pushes up whichever ones check out, and the [GRPO post](/blog/grpo-rlvr/) walked through it. Its score on [AIME 2024](https://artofproblemsolving.com/wiki/index.php/American_Invitational_Mathematics_Examination), a 15-question American olympiad qualifier, went from 15.6% to 71.0% pass@1 over training. With majority voting over 64 samples it reached 86.7%. Nobody told it to write longer answers, but its average response length climbed throughout training anyway, because sampling a group and keeping whatever checks out, rewards any habit that raises the hit rate. And going back over your own working raises the hit rate.

The cheap version is almost silly. [s1](https://arxiv.org/abs/2501.19393) (Muennighoff et al., 2025) trained Qwen2.5-32B-Instruct further on 1,000 curated questions. The working was copied from Gemini Thinking, the same borrow-the-teacher trick as the [distillation post](/blog/knowledge-distillation/). 26 minutes on 16 H100s. Then they added **budget forcing**: when the model tries to stop, block the token it stops on and append the word "Wait" instead. The model, which has no spine, goes back and checks. That one hack took AIME24 from 50% to 57%.

Seven points for a word. There is a whole literature of elaborate search procedures and the thing that works is typing "Wait" at a model until it changes its mind.

## Ordering too many tests

Every doctor knows the patient who has had every scan twice. Past some point the extra films stop answering the question and start turning up things that were never wrong, and somebody has to chase those too.

Models do this too, and it has a number on it now. [When More Thinking Hurts](https://arxiv.org/abs/2604.10739) (2026) ran DeepSeek-R1-32B and s1-32B under controlled token budgets. The marginal return per extra 500 thinking tokens starts around +2.1%, falls to roughly nothing by 7,000 tokens, and goes negative past 10,000. On AIME, R1-32B peaks at 55.8% around 12K tokens and is back down to 54.9% by 16K.

![A curve of accuracy gained per extra 500 thinking tokens, starting at plus 2.1 percent, crossing zero near 7000 tokens and staying slightly negative out to 17000](/images/blog43/marginal-return-per-500-tokens.png) *Figure 4: what the next 500 tokens are worth. Seven thousand. Not five, not ten, and I have more faith in an awkward number somebody measured than in a round one. Source: Author*

What is going on is specific and a bit sad. The model reaches a correct answer, keeps going because nothing told it to stop, and talks itself out of it. The paper's early-stopping rule holds 97% of peak accuracy on 60% of the compute, which tells you how much of that tail was doing nothing.

[Does Thinking More Always Help?](https://arxiv.org/abs/2506.04210) (2025), the mirage paper, argues the gains are partly a measurement artefact. Thinking longer scatters the model's answers, and a score like pass@1 can read that scatter as improvement while the model is getting less reliable. Their fix is to sample several short chains and take a majority vote, worth up to 20 points over extended thinking. Parallel wins again, which is a strange place to arrive after two years of making chains longer.

## At the counter

Who actually pays for this, and how much?

Everyone, now. The o-series from OpenAI, DeepSeek-R1, Gemini's thinking budget and Claude's extended thinking all ship a dial. And the agent scaffolds in the [benchmarks post](/blog/llm-benchmarks-terminal-bench/), the code wrapped around a model that calls the tools, sample several attempts and run the tests to pick. That post argued an agentic score belongs to a model and its scaffold together. A thinking budget is the same problem one layer down.

The bill is real. o3 scored 87.5% on [ARC-AGI](https://arcprize.org/), grid puzzles where you work out a transformation from a few examples and apply it. The grids go in as text, not as pictures. That run was its efficient configuration, at roughly $17 to $20 of compute per puzzle. There is also a low-efficiency one that uses 172 times more compute, burning between 33 and 111 million tokens and about 1.3 minutes per puzzle. So a benchmark score that costs twenty dollars and a minute and a half a question, is not a feature you can put in a chat box. Which is why the [speculative decoding](/blog/speculative-decoding/) and [KV caching](/blog/kv-caching-mla-is-attention-all-you-really-need/) work matters more every year.

## Where things are going

- **Routing**, not a slider. Snell's four-fold saving came from spending per question. [Tail-guided allocation](https://arxiv.org/abs/2602.01485) (2026) tries to predict the curve before you pay for it.
- **Cheap verifiers.** [Weaver](https://arxiv.org/abs/2506.18203) combines several weak ones rather than training one strong one, and closes 14.5% of the gap between what is in the pile and what gets submitted, on [GPQA Diamond](https://huggingface.co/datasets/Idavidrein/gpqa), graduate-level science questions. [Generative verifiers](https://arxiv.org/abs/2408.15240) instead make the verifier a language model that reasons out loud about the answer.
- **Answer keys for things that have none.** This decides how far any of it travels, and the early news is mixed. [LLMs Gaming Verifiers](https://arxiv.org/abs/2604.15149) (2026) catches models learning the exact patterns a model-based checker mistakes for correctness.

## Contraindications

1. Nearly every number here comes from maths or code, because those are the places with a lab. A unit test passes or it does not. There is no assay for whether a design review is any good, and without a cheap check majority voting plateaus after a few hundred samples. Summarising a document and replying to an email are both in that category, and so is most of what people use these models for. Buying the key is not cheap either. PRM800K is 800,000 steps of paid human labelling, for one subject.
2. The peak-then-decline result may be about the metric rather than the model. If the mirage paper is right that longer thinking mostly scatters the answers, a chunk of this literature has been measuring that scatter. I doubt it is the whole story, because the verifier results are hard to explain that way. But I would not bet against half.
3. The visible chain may not be the computation. Models produce reasoning that does not always match what drove the answer ([Turpin et al., 2023](https://arxiv.org/abs/2305.04388)). So when a process reward model marks step 3 as the bad line, it is marking a story the model told about itself. My guess at why it works anyway is that the story still conditions what gets written next, so a bad-looking step is a decent bet the chain is going nowhere. Useful, and not the same as finding the error.
4. And I could not read most of these papers properly. arXiv and Wikimedia are both blocked from the machine this was written on, so the 2026 numbers especially, the +2.1% and the 7K crossover and the 97%-on-60%, come from abstracts and secondary write-ups rather than the figures. Those are the ones I would most like checked. Everything older I have read before and would stand behind.

## Conclusion

For a decade the only lever anybody had was the size of the model, and pulling it meant a training run you could not take back. Test-time compute moves after training, per question, at a price you can read off an invoice. A 7B model given ten thousand tokens to think costs what a 350B model costs to answer in two hundred, and on the questions it had a chance at, it wins.

But none of it works without something that can check the answer. Every big number here, the 78.2%, the 71.0% out of R1-Zero's RL loop, the 56% of SWE-bench Lite issues patched, has a verifier standing behind it doing the real work. So my bet is that the next good year comes from people building lab tests for the things that have no lab test yet. Making the chains longer looks finished, and the 7K crossover is where it stopped.

Which brings us back to the fifth viewer on the cover, the one switched on with nothing clipped to it. You can always order one more test. Most of the skill is knowing who needs it, because the three-week fever gets the full workup and the sprained ankle gets its seven minutes. And the film you are about to order will probably come back with one more pencil ring on it that meant nothing at all.

And now you know. Fin.
