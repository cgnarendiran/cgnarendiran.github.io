---
layout: post
title:  "Jev - The Classifier Strikes Back"
date:   2026-09-25
image:  images/blog38/cover.jpg
description: "Jev returns typed, calibrated decisions instead of text. Underneath, it looks like a very good zero-shot classifier, and calibration is the claim to test."
tags: [llms, rlhf, reinforcement-learning, probability, essay]
---
*On the cover: William Stanley Jevons, engraved for Popular Science Monthly in 1877. Jev is named after him, because in 1865 he argued that more efficient steam engines would make Britain burn more coal, not less. [Public domain](https://commons.wikimedia.org/wiki/File:PSM_V11_D660_William_Stanley_Jevons.jpg), via Wikimedia Commons.*

On the 15th of September, a startup called TypeSafe AI came out of two years of working in secret, with 40 million dollars of funding. It launched a model called Jev, which it calls a "System One model". [The launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev) opens with a question from its founder, Diogo Almeida: "Models have been superhuman at chat for years, so where is all the automation?"

Diogo is one of the authors of [InstructGPT](https://arxiv.org/abs/2203.02155), the 2022 paper that taught GPT-3 to follow instructions and led to [ChatGPT](/blog/chatgpt-future-of-conversational-ai/). Jev took over my timeline within a day, and [The Register](https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711) led with the fact that it plays Doom.

My take, after a week of reading everything I could find, is simple. Jev is a zero-shot classifier: you hand it some text and a list of labels it was never trained on, and it tells you which label fits. Classifiers were most of the AI inside products before ChatGPT. This one is much better than BERT, the 2018 model most of them are still built on. And half my timeline is discovering classifiers this week, lol.

That doesn't make Jev boring, though. The claim I care about is that when Jev gives an answer a probability of 0.9, it's supposed to be right 9 times out of 10.

Welcome to the return of the **classifier**. This is the story of what Jev returns, what outsiders have measured, and why the number next to each answer is the part worth arguing about.

## The problem: an if-statement that writes an essay

Most software is a pile of if-statements. Is this email spam? Which team should get this ticket? For years, we answered these with keyword rules or a small classifier trained for that one question. Then large language models (LLMs) could answer all of them with no training at all. So people started putting an LLM call inside the if-statement.

Let's say this support message comes in: *"I've been trying to connect my Stripe account for 3 days and the integration keeps failing. I'm losing sales. Please help ASAP."* Your code asks a chat model to reply in JSON, a text format code can read, with the team, how frustrated the customer is, and whether it's urgent. The model can only answer by writing, one token at a time (a token is a word or a piece of one). Each token waits for the one before it (the bottleneck from the [speculative decoding post](/blog/speculative-decoding/)). Then your code reads the text back and hopes it's valid JSON.

That takes seconds, and you pay for every output token. You can ask the model how sure it is, but the answer is more text. Nothing in its training checked that number against what really happened. TypeSafe's launch post puts it well: "If a model can do a task 95% of the time but doesn't say when it's in the 5%, it can't automate that task."

## What Jev actually returns

Jev takes the same message, which TypeSafe calls the **state**, plus a list of typed questions, each with the shape of its answer fixed in advance. There are [three kinds](https://docs.typesafe.ai/primitives):

1. A **Choice** picks one option from a list you write. Which team: billing, technical or sales?
2. A **Score** places the state on a scale you describe. Is the customer calm, frustrated but civil, or very angry?
3. A **Noul** is a yes-or-no question, answered with the probability of yes. Is this urgent?

Jev answers all of them in one pass, in parallel, and never writes a sentence. Here is its real reply to that message, from TypeSafe's [quickstart](https://docs.typesafe.ai/introduction/quickstart), trimmed a little:

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "department":  {"choice": "technical", "confidence": 0.78,
                    "probabilities": {"technical": 0.85, "billing": 0.15, "sales": 0.0}},
    "frustration": {"score": 1.0, "confidence": 1.0},
    "is_urgent":   {"noul": 1.0}
  },
  "usage": {"input_tokens": 392}
}
```

Jev thinks this is a technical problem with probability 0.85 and a billing one with 0.15. That's fair, since Stripe is a payments company. The scale's levels are numbered from 0, so a frustration score of 1.0 is the middle one, "frustrated but civil". And urgency is 1.0, because the customer wrote ASAP and meant it.

![Two flows for one support message: a chat model writing JSON token by token, and Jev answering three typed questions at once](/images/blog38/two-ways.png) *Figure 1: The chat model writes its decision out as text, one token at a time. Jev fills in a probability for every option, for all three questions at once. Source: Author*

The confidence of 0.78 is not a chance of being right. It's one number that says how peaked the probabilities are. TypeSafe hasn't published its formula. But the open [adapter](https://github.com/typesafe-ai/system-one-adapter-python) it uses to run ordinary LLMs through its tests in Jev's format gives the same 0.78. It rescales the top probability so that a blind guess scores 0 and certainty scores 1:

$$\text{confidence} = \frac{\text{top probability} - \text{blind-guess share}}{1 - \text{blind-guess share}}$$

specifically,

$$c = \frac{p_{\max} - 1/n}{1 - 1/n}$$

where $p_{\max}$ is the largest probability and $n$ is the number of options, so a blind guess gives each option $1/n$. For our message, $n = 3$ and $p_{\max} = 0.85$, so $c = (0.85 - 0.333) / (1 - 0.333) = 0.775$. That rounds to the 0.78 Jev returned.

The cost is the funniest number in the launch. TypeSafe says a call takes 70 to 500 milliseconds, 40 to 200 times faster than the big LLMs. This one read 392 input tokens, and at 4.2 cents per million that comes to about 0.0016 cents. So a dollar buys you roughly 60,000 of them, and output is free because it's "too cheap to meter".

"System One" comes from Daniel Kahneman's [*Thinking, Fast and Slow*](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow), where System 1 is the fast, gut-feeling part of your head. Jev is named after the man on the cover, whose [paradox](https://en.wikipedia.org/wiki/Jevons_paradox) TypeSafe applies to AI: "Every order of magnitude drop in the cost of intelligence unlocks orders of magnitude more use cases."

## Calibration, from the beginning

Calibration is a simple idea with a boring name. Take a thousand tickets where the model gave "technical" a probability of 0.8. If about 800 of them really were technical, the 0.8 was honest. A **calibrated** model is honest like that at every level from 0 to 1. So it never says exactly 0 about something that happens, because 0 means impossible.

Software cares because the number can then decide what happens next. TypeSafe's [docs](https://docs.typesafe.ai/confidence) sketch a banking bot that hands you to a person when confidence is below 0.5, and only moves money above 0.9. That only works if the probabilities underneath are honest.

So how do you train for honesty? The trick is older than neural networks. In 1950, a meteorologist named Glenn Brier proposed scoring a forecast by the squared gap between the probability you said and what happened. His [paper](https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml) is three pages long, which is shorter than most API terms of service. Formally, for $N$ predictions,

$$\text{BS} = \frac{1}{N} \sum_{i=1}^{N} (f_i - o_i)^2$$

where $f_i$ is the probability the model gave and $o_i$ is 1 if the thing happened and 0 if it didn't. Lower is better.

Let's do one by hand. Say 7 out of 10 tickets like ours really are technical. If the model says 0.7 each time, it's off by 0.3 on the seven technical ones and by 0.7 on the other three, so it scores $(7 \times 0.3^2 + 3 \times 0.7^2) / 10 = 0.21$. If it bluffs 1.0 each time, it's off by 0 seven times and by 1 three times, so it scores $3/10 = 0.3$. Hedging at 0.5 scores 0.25. The best score goes to the probability that matches how often it's right. A score with that property is called a **proper scoring rule**, and the [cross-entropy loss](/blog/cross-entropy-loss/) every classifier trains on is one too.

So why isn't every classifier calibrated? Big networks learn their training data too well and come out overconfident on new data, as [Guo et al. (2017)](https://arxiv.org/abs/1706.04599) measured. That's why scikit-learn, the standard Python library for classic machine learning, has a [page on fixing it](https://scikit-learn.org/stable/modules/calibration.html). (Welcome to the club, everyone.)

TypeSafe trains Jev with **RLCD**, reinforcement learning for calibrated decisions. Reinforcement learning means the model tries answers, gets a score (a reward) and learns to raise it. TypeSafe hasn't said what the reward is, or why it doesn't just train on the score directly. My guess is a proper scoring rule, which is what [RLCR](https://arxiv.org/abs/2507.16806) (Damani et al., 2025) used for reasoning models.

## What Diogo thinks went wrong

Diogo's case, from [a talk](https://www.youtube.com/watch?v=cJ0EOzey--o) at the AI Engineer World's Fair and the [Latent Space podcast](https://www.latent.space/p/jev), is that chat models are badly calibrated because of how we trained them. It starts with [RLHF](/blog/reinforcement-learning-from-human-feedback/), reinforcement learning from human feedback, the step that turned GPT-3 into a chatbot. People pick which of two answers they prefer, and the model learns to give more of that kind.

Why do LLMs still need a human watching? His answer in the talk is "we literally put them in the loop. The goal of the loop is to optimize for human preference". His favourite example is a tweet where someone sent ChatGPT a recording of fart noises and asked what it thought of their music. The reply opened with "Here's a straight, honest reaction. It's a very eerie vibe atmosphere piece." (Very honest, that one.)

That's flattery. The damage to calibration is more serious, and the evidence comes from OpenAI itself. The [GPT-4 technical report](https://arxiv.org/abs/2303.08774), which Diogo co-authored, read the probabilities the model gave the answers A to D on [MMLU](https://arxiv.org/abs/2009.03300), a 57-subject multiple-choice exam. It found that "the pre-trained model is highly calibrated". Then it added: "The post-training hurts calibration significantly."

So why not read an LLM's own probabilities for "technical" and "billing" and skip Jev? You can, where the API shows them. But post-training bends them, as that chart shows, and you still wait for a big model to read everything.

On the podcast he explains why chat is stuck. A chat model picks each token by drawing from its probabilities, hundreds of times in a row, and one bad draw can ruin the answer. So it has to play extremely safe, and he calls calibration "total poison" for text.

In the talk, he says RLHF isn't wrong. "But it was like a weird detour and one that we didn't expect". [RLVR](/blog/grpo-rlvr/), reinforcement learning with verifiable rewards, trained the new reasoning models, and he calls it "a tiny little, like, edit to the direction". RLCD is his new "North Star", with "programs in the loop", meaning the answers go to code instead of a person. When the host, swyx, asked whether there was a paper, the answer was "No, not yet."

I agree with more of this than I expected to. But notice that the argument is about what the model is trained to do. It says nothing about architecture, so you could fix the training target without inventing a new kind of model.

## So is it just a classifier?

My case is about what Jev does, since nobody outside TypeSafe knows what it's made of. Jev takes text plus labels you define at request time, and it returns a probability for each label. That's the textbook definition of zero-shot classification. [Yin et al. (2019)](https://arxiv.org/abs/1909.00161) benchmarked it, and Hugging Face, the main site for sharing open models, has shipped a [zero-shot pipeline](https://huggingface.co/tasks/zero-shot-classification) on [BART-large-MNLI](https://huggingface.co/facebook/bart-large-mnli) for years. In 2023, [GLiNER](https://arxiv.org/abs/2311.08526) made the same pitch for picking names and places out of text: "parallel entity extraction, an advantage over the slow sequential token generation of LLMs".

Jev's failure modes look like a classifier's, too. Its [jaggedness page](https://docs.typesafe.ai/model-jaggedness/jev-1.13), TypeSafe's list of known weak spots, says it can't count reliably, can't tell which of two dates comes first, and "answers the question you wrote, not the one you meant". It can't write text at all. Even LangChain, a popular library for building LLM apps, exposes it through a class called `TypeSafeClassifier`, and its [post](https://www.langchain.com/blog/building-a-harness-with-jev) is happy that "a cheap and performant classifier model exists".

TypeSafe's FAQ says "Jev is neither small nor an LLM". When someone at the talk asked if it was like a classifier head trained alongside pre-training, Diogo said that was complicated. What would change my mind is Jev handling questions that take several steps of reasoning, and TypeSafe's own docs say that's where it struggles.

It's a much better classifier than the ones we had, though. A developer who goes by AbdelStark ran a [pre-registered comparison](https://github.com/AbdelStark/jev-benchmarks) (test plan fixed before any results) against [GLiNER2.5](https://huggingface.co/fastino/gliner2.5-multi-v1) on [BTZSC](https://huggingface.co/datasets/btzsc/btzsc), a zero-shot classification benchmark. On [AG News](https://huggingface.co/datasets/fancyzhx/ag_news), headlines in four topics, Jev got 91% right against GLiNER's 70%. On a 72-intent version of [Banking77](https://huggingface.co/datasets/PolyAI/banking77), customer messages sorted by what they want, it was 87% against 61%. That's only 100 examples each, so treat it as a pilot.

Put together, that's a very good product, and it's still a classifier.

## Laya, the open one from Kasaragod

Three days after Jev, Nandakishor M released [Laya](https://huggingface.co/convaiinnovations/laya) with open weights. He runs Convai Innovations out of [Kasaragod in Kerala](https://analyticsindiamag.com/ai-features/this-kerala-engineer-built-open-source-jev-alternative-a-year-before-the-hype), and his [write-up](https://dev.to/nandakishor_m_6cc0adfde9f/i-built-non-autoregressive-decision-models-a-year-ago-then-a-frontier-lab-called-it-a-18me) has the best title of the week: "I Built Non-Autoregressive Decision Models a Year Ago. Then a Frontier Lab Called It a 'Breakthrough'." Non-autoregressive means it doesn't write one token at a time, and his [March 2025 paper](https://arxiv.org/abs/2503.23303) backs the claim up.

Laya takes the same state and the same three question types, and it tells you what's inside. The English model is [ModernBERT](https://arxiv.org/abs/2412.13663)-large, a 2024 update of BERT, with 421 million parameters. On top sits a small decision head, trained with reinforcement learning against proper scoring rules. It answers a question in 33 to 40 milliseconds on a [T4](https://www.nvidia.com/en-us/data-center/tesla-t4/), a data-centre GPU from 2018. So the one System One model whose insides we can see is literally a classifier. It's a BERT with good manners. That doesn't prove what's inside Jev, but it shows the idea works on one.

Laya's own benchmark uses 2,000 decisions from the same four business workflows TypeSafe tests on. Out of the box, the English Laya's accuracy is 0.362, below the 0.461 you'd get by always picking the most common answer. After fine-tuning on that benchmark's training split, it's 0.766. Jev's published score is 0.727 with no fine-tuning, and TypeSafe says those workflows aren't in its training data. So Laya matched Jev by studying for the test. (Its labels come from a teacher model's probabilities, so that fine-tune is really [distillation](/blog/knowledge-distillation/), a small model copying a bigger one.)

It's also a warning that calibration doesn't travel. Handed text in Khmer, a script it never learned, the English Laya scored 0.000 accuracy at 0.952 confidence.

## What the outside tests found

The biggest independent test so far is [nibzard's decision-model benchmark](https://github.com/nibzard/decision-model-benchmark). He ran Jev and eight LLMs, all forced into the same JSON answer, through five test suites, paid the 28 dollars and 34 cents himself, and published every log.

![Scatter plot of accuracy against median latency for Jev and eight LLMs on banking intents](/images/blog38/independent-benchmark.png) *Figure 2: 900 banking questions per model, each with 77 possible intents. Data: [nibzard's decision-model benchmark](https://github.com/nibzard/decision-model-benchmark), v2 report. Source: Author*

On all 77 banking intents, Jev answered in 274 ms at the median. It cost 7 cents per 1,000 decisions (each question carries all 77 intents), against 19 cents for the cheapest LLM. But its accuracy, 76.3%, sat mid-pack, below AbdelStark's 87% on a different, 72-intent set. The most accurate was [gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b), OpenAI's open-weight model, at 81.3% in 331 ms on [Cerebras](https://www.cerebras.ai/), whose chips are built to run models fast. So Jev is 1.2x faster than the fastest LLM here, not 40 to 200x. The big multiples need slower setups, like [Claude Haiku 4.5](https://www.anthropic.com/claude/haiku) at 4.4 seconds.

He also confirmed the limit on options. With 255 options, Jev worked. With 256, it returned an error, `400 Too many choices`. That's one short of what fits in a byte, and I choose to believe the spare slot is for "none of the above".

Calibration was mixed. He measured **expected calibration error (ECE)**, the average gap between how sure a model was and how often it was right, on Jev's confidence field rather than its probabilities. On banking, Jev's ECE was 0.083, level with Haiku's 0.078. On [SMS spam](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) it was the second most accurate model, but its ECE of 0.249 was the worst in the test. To be fair to the LLMs, most of their stated confidences held up fine.

The worst result came from questions built to have no good answer. Seven of the eight LLMs gave a confidence of 0.5 or less on 97 to 100% of those. Jev did it on 49.7%.

![Dots and rings comparing accuracy with confidence for Jev and GLiNER2.5, and bars for the work each could automate](/images/blog38/calibration-pilot.png) *Figure 3: Left, how often each model was right (dot) against how sure it was (ring). Right, how much work each could take on alone at a 5% error rate. Data: [AbdelStark/jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks), 100 examples per dataset. Source: Author*

AbdelStark scored the probabilities themselves. Say you only act on answers above a cutoff, set so that the answers you act on are 95% right. On news and banking, that cutoff lets Jev handle 83 to 86% of the examples, against about a quarter for GLiNER. That's the number that matters for automation. On [DAIR Emotion](https://huggingface.co/datasets/dair-ai/emotion), tweets labelled with six emotions, Jev said 0.82 on average and was right 48% of the time, so the cutoff lets nothing through. It also gave the true label a probability of exactly zero 16% of the time, which a calibrated model should never do.

| TypeSafe's claim | What outsiders found | What it means for you |
|---|---|---|
| 40-200x faster | 274 ms median; 1.2x faster than gpt-oss-120b on Cerebras | Fast, but the multiple depends on what you compare it with |
| Zero type errors | Not one malformed answer | True by design, though a wrong answer is still a valid one |
| Calibrated | Level with LLMs on banking, worst on spam | Test it on your own data before you trust a cutoff |
| Can't hallucinate | Probability zero on the true label, 16% of the time on emotions | It can't make things up, but it can rule out the truth |

## Where it's used, and where it isn't

A week in, people are using it for:

1. Routing tickets and alerts, and screening what goes in and out of chatbots.
2. Re-ranking search results. TypeSafe's legal [cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe) puts the right court passage first for 18% of 40 queries, up from 5%.
3. Doom. The demo feeds in the game's state as text and picks a move about 10 times a second, for about 7 dollars an hour.

It can't write, and counting, dates and arithmetic belong in your own code. Text written to trick the model can also move the answer, which the jaggedness page admits.

## What nobody outside TypeSafe can check yet

There's no paper, and the weights and architecture are private. So every claim about why Jev works is TypeSafe's word. Their own tests, the [workflow evals](https://evals.typesafe.ai/), grade every model against the average answer of [GPT-6 Astra](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra) and [Claude Fable 5.1](https://www.anthropic.com/claude). TypeSafe lists the biases in that setup themselves, which I respect. But their own team wrote the workflows, so it's still their own exam.

Separate questions don't have to agree, either. The jaggedness page shows a ticket that reads, "I was charged twice for the same order. Can someone look into this?" Asked whether the customer wants a refund, Jev said 0.72. Asked whether they want something other than a refund, it said 0.47. Honest probabilities of opposites add up to 1, and these make 1.19. TypeSafe tells you not to do arithmetic across questions, which is fair advice and also a limit on what "calibrated" means.

And the `jev-latest` name always points at the newest version, so its answers can change under you. If you've tuned your cutoffs on 1.13, pin `jev-1.13.0`, or your 0.9 will quietly mean something else one morning.

## Conclusion

So here's where I've landed. Jev is a zero-shot classifier, and a very good one. It gets close to a big LLM's accuracy for a few cents per thousand calls and about a quarter of a second each.

What's new is the promise that the probability next to every answer means what it says. On news and banking, the outside tests say it roughly does. On emotions, or questions with no right answer, it doesn't yet. I think Diogo is right that chat training works against calibration, since OpenAI's own report shows it. But the LLMs in nibzard's test stated their confidence better than the launch implies.

Jevons would have enjoyed this week. Make steam engines more efficient, and Britain burns more coal. My bet is that within a year every big lab ships a decision API next to its chat API, and that most of them are classifiers underneath. Half the timeline will call each one a breakthrough, and scikit-learn will still be there.

And now you know. Fin.
