---
layout: post
title:  "Tokenizers - Out of Sorts"
date:   2026-10-04
image:  images/blog42/cover.png
description: "A model's vocabulary is fitted by counting pairs and frozen before training starts, and it decides what the model can spell, add up and charge you."
tags: [tokenization, nlp, llms, transformers]
---

*On the cover: a compositor's type case, the tray a letterpress shop keeps its metal type in. The top row reads e, t, a, o, i, n, s, h, frequency order rather than alphabetical, and the wider compartments hold ligatures: single pieces carrying `th`, `er` and `the`. One is empty, because somebody has to decide what gets cast. Source: Author.*

Let's say you run a print shop in 1890. Against one wall is a shallow tray of about a hundred compartments, each holding a pile of identical metal letters. The tray is called a **case**. One piece of metal is a **sort**. The man who picks them out one at a time and lines them up in a handheld rail is the **compositor**. (Upper case and lower case were two trays on a frame, capitals above, small letters below. That is the entire etymology.)

Now, you print the same local paper every afternoon. And after a month you notice your compositor reaching for `t`, then `h`, then `e`, thousands of times a day. So you have the foundry cast one piece of metal with `the` on its face, and give it a compartment of its own. Three picks become one pick.

Congratulations, you have invented byte pair encoding about a century early.

There is a catch, and it is the rest of this post. A case has a fixed number of compartments, and every new piece you cast uses one up. So you cast the pieces you counted most, and whatever you did not count gets spelled out letter by letter. Anything you have no metal for at all stops the press. Printers call that being **out of sorts**. (Etymologists say the printing origin is not proven. Printers say it obviously is.)

Welcome to the era of **byte pair encoding (BPE)**. This is the story of the one part of a language model that is never trained by gradient descent, and of how a counting script somebody ran before the real training started, decides what the model can spell, how well it adds up, and what you pay per sentence.

## The shop, in ML terms

Four things to carry, with the real name pinned to each:

1. The **case** is the **vocabulary**: the fixed list of pieces the model may use. GPT-2's has 50,257 compartments.
2. A **sort** is a **token**: one entry in that list. The model never sees it as text. It sees the compartment number and looks up one row of a big table called the **embedding**: a few hundred to a few thousand numbers, all of them learnt during training.
3. A **ligature** is a **merged token**: one piece carrying two or more letters, cast because that pair kept turning up.
4. The **compositor** is the **tokenizer at run time**: it takes your sentence and hands back a list of compartment numbers.

Everything the model knows about your text arrives as that list of numbers, and the letters stay behind in the metal.

## One sort per word, or one per letter?

So why not give every English word its own compartment?

Because the case would have to be enormous and still never be big enough. English has no fixed word count, people make typos, and one URL breaks the scheme. Word-level models handled that with an `<UNK>` sort, a blank slug meaning "something was here". Every unfamiliar name collapses to the same blank, which is a pretty terrible thing to do to a model you are about to ask about people's names.

So cast one sort per letter instead. Now you are never out of sorts, because there are only about a hundred of them. But a sentence that was 20 words is now 110 letters. And attention costs grow with the square of the sequence length, which is what the [KV caching post](/blog/kv-caching-mla-is-attention-all-you-really-need/) was about. You just made every sentence five times longer to save one drawer of metal.

The fix is the one the print shop already found. Keep the letters so you can always spell anything out, and cast ligatures for the combinations that come up constantly. This is **subword tokenization**, and every frontier model uses some version of it.

## Casting the ligatures

The recipe, in the abstract:

1. Start with one sort per character, and split every word in the corpus into characters.
2. Count every adjacent pair of sorts in the corpus.
3. Cast the commonest pair as one new sort, write it down in a book, and apply it everywhere.
4. Go back to step 2 until the case is full.

Notice there is no gradient anywhere in that loop. Choosing a merge is a discrete pick, and you cannot take a derivative of a pick. So none of this trains alongside the network. It is a counting script that runs first, and what it decides is frozen for the life of the model.

Step 3's book matters more than it looks. It is an ordered list, and at run time the compositor replays it from the top. That is the only reason the same sentence always gets set the same way.

![Two flowcharts side by side: a corpus feeding a counting loop into a numbered merge book, and the word imprint being set as three pieces of type](/images/blog42/two-jobs.png) *Figure 1: the tokenizer's two jobs. Fitting the case happens once, by counting; setting a line happens on every input. Source: Author*

The rule for what to cast next, in words:

$$\text{next ligature} \;=\; \underset{(a,b)}{\arg\max}\;\;\text{how often } a \text{ sits directly before } b$$

specifically,

$$(a,b)^\star \;=\; \underset{(a,b)}{\arg\max}\;\sum_{w \in C} f(w)\, n_{ab}(w)$$

where $C$ is the list of distinct words in the corpus, $f(w)$ is how many times word $w$ occurs, and $n_{ab}(w)$ counts how many times sort $a$ sits directly before sort $b$ inside $w$ as it is split right now. That last clause is what makes this iterative, because every merge changes the split of every word it touches.

Let's do one by hand. Our shop's corpus is five words, with counts I am making up as a day's work: `press` eight times, `pressed` three, `printer` four, `printed` five, `printing` six. The base sorts are the nine letters that appear, plus a mark for the end of a word, so ten compartments to start. (The end mark lets the shop tell a `print` that finishes a word from one that does not.)

Round one counts every pair across all 26 word occurrences, not the five distinct words. `p` is followed by `r` in every one of the 26, which beats `i`+`n` at 21. (`printing` carries two `in`s, which is where the extra six come from.) So `pr` is cast first, then `i`+`n`, then `pr`+`in`, then `prin`+`t`. Four rounds in, the shop owns one piece of metal that says `print`.

![Seven rows showing the word printing split into pieces, with the pieces merging into larger ones as each of six merges is applied](/images/blog42/six-merges.png) *Figure 2: six merges on the five-word corpus, following `printing` down the page. Green is a ligature. Rounds five and six cast `pre` and `pres`, which leave this word alone. Source: Author*

Six merges in, the case holds sixteen sorts. Now hand the compositor a word the shop has never printed, say `imprint`. Working down the book entry by entry, he glues every occurrence of that entry's pair before moving on. Book order, never longest-piece-first. So `pr` fires, then `in`, then `prin`, then `print`, and he stops with three pieces in the stick: `i`, `m`, `print`.

Which is lovely, except the shop has no `m`. It never appeared in any of those five words, so no compartment was ever filled with it. The compositor is out of sorts on the second letter, in an alphabet of 26.

## Never out of sorts

The fix is to stop thinking in letters and start thinking in bytes.

Text on a computer is already a sequence of bytes under [UTF-8](https://en.wikipedia.org/wiki/UTF-8), and a byte has 256 possible values. An English letter takes one byte, because the English alphabet got the first 128 values back in the 1960s. A Tamil letter takes three, an emoji four. So you fill 256 compartments before you count anything, and cast your ligatures on top. Now there is no unknown character: emoji, Sanskrit and a corrupted PDF all decompose into bytes you already own. This is **byte-level BPE**, and [GPT-2](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) shipped it in 2019.

GPT-2's case is 256 bytes, plus 50,000 merges, plus one special sort marking the end of a document. That is 50,257, and the name is now literal: [Philip Gage's 1994 algorithm](https://en.wikipedia.org/wiki/Byte-pair_encoding) compressed files by replacing the commonest pair of bytes with an unused one, over and over. This is that on a bigger budget.

I pulled GPT-2's merge book down to see what it cast first. The first six, in order, are a space plus `t`, a space plus `a`, then `he`, `in`, `re`, `on`. The seventh joins space-plus-`t` to `he`, giving one piece of metal that reads ` the`. Merge eight is `er`. (`th` does not get cast until merge 145, because `he` and space-`t` keep eating it first. The book is greedy and it does not plan ahead.)

The space gets attached to the front of the word, and that detail has consequences nobody expects. A rule, usually a regular expression, splits text at spaces and punctuation before any merging, so a ligature can never span two words, exactly as a compositor drops a spacer between them. In GPT-2's case, ` strawberry` with its leading space is a single sort, number 41236. The same word at the start of a line, with no space in front, is three: `st`, `raw`, `berry`.

## Two other recipes

BPE won, but it is not the only way to decide what to cast. **[WordPiece](https://huggingface.co/docs/transformers/tokenizer_summary)**, the one BERT made famous, runs the same loop. But it takes the pair that most raises the corpus likelihood, not the commonest one, scoring each as

$$\text{score}(a,b) = \frac{\mathrm{count}(ab)}{\mathrm{count}(a)\cdot\mathrm{count}(b)}$$

So two rare pieces that always turn up together beat two common ones that merely bump into each other a lot. It is the difference between casting `ing` because you saw it everywhere, and casting `ough` because the `o` is basically a hostage. **Unigram**, from [Kudo in 2018](https://arxiv.org/abs/1804.10959) inside [SentencePiece](https://github.com/google/sentencepiece), runs backwards instead: start with an oversized case and melt down whichever sorts cost the corpus least.

| recipe | how it picks | what you get | where it shows up | verdict |
|---|---|---|---|---|
| BPE | the commonest adjacent pair | one setting per word, fast and deterministic | GPT-2 through GPT-4o, Llama, Mistral | the default; nothing has dislodged it |
| WordPiece | the pair that most raises corpus likelihood | favours pairs that only occur together | BERT and its descendants | better reasoning, almost identical output |
| Unigram | prune a big case down by likelihood | a probability over several settings | T5, ALBERT, most SentencePiece models | the only one that can sample; slowest to fit |

## Why your model can't spell

When you ask a model how many `r`s are in "strawberry", it is not looking at a word. It received the number 41236, looked up row 41236 of the embedding, and got back 768 floats learnt from the contexts that sort appeared in. The letters are inside the metal, face down, and nobody on the press floor reads them. Asking that model to count them is like asking the compositor what is cast on a slug he has already locked into the forme.

It is not completely hopeless though. [Itzhak and Levy (2022)](https://arxiv.org/abs/2108.11193) built a probe called Spelling-Bee that tries to spell a token out of its embedding alone. GPT-2 and RoBERTa carry enough there to spell up to a third of their vocabulary exactly, because spelling leaks in sideways from all the text that talks about spelling. It just leaks unevenly, and you cannot tell which third you got.

Arithmetic is the same wound, and more expensive. Digits get merged into ligatures too, and the merging runs left to right. GPT-2 sets ` 1234567` as three sorts: ` 123`, `45`, `67`. Does anything in that tell the model the `45` is tens of thousands? It does not. So it is adding two numbers whose pieces do not line up by place value, and the answer's pieces line up with neither.

[Singh and Strouse (2024)](https://arxiv.org/abs/2402.14903) ran the ablation. Take the same addition problems and insert commas. A comma is a boundary the merges are not allowed to cross, so `1,234,567` has to come apart as `1`, `234`, `567`. Which is groups of three counted from the right, which is exactly what place value needs. Nothing about the model changes. GPT-3.5 went from 75.6% to 97.8%, and GPT-4 from 84.4% to 98.9%. A model everybody was measuring on reasoning was dropping a fifth of its arithmetic because of where a counting script had put the boundaries.

This is why Llama splits every digit into its own sort, while GPT-3.5 and GPT-4 kept sorts for every one-, two- and three-digit number. Somebody read that paper.

## The tokenization tax

The merge book is cast from a corpus, and that corpus is overwhelmingly English. Everybody who writes in something else pays for that choice, in money and in context window.

I ran one ordinary word through GPT-2's case in a few languages. `hello` is one sort. The Tamil word வணக்கம் also means hello. It is seven characters, 21 bytes of UTF-8, and **21 sorts**. Not one merge was ever cast for Tamil, so every byte comes out of the byte drawer on its own. My own name in Tamil costs 30.

![Horizontal bars comparing byte counts with GPT-2 token counts for one word in eight languages; the Tamil bars are equal length](/images/blog42/fertility.png) *Figure 3: what one ordinary word costs in GPT-2's case. Where the bars match, the merge book learnt nothing about that script and is spelling it a byte at a time. Source: Author*

This is called **fertility**, the average number of tokens per word, and [Petrov et al. (2023)](https://arxiv.org/abs/2305.15425) measured it across a batch of tokenizers and the same text in many languages. They found gaps of up to 15 times between languages for one sentence, and the gaps survive in tokenizers built to be multilingual. My 21-against-1 above is the worst-hit script through an old tokenizer, so treat it as a ceiling rather than an average. And the consequences are not academic. You are billed per token, the context window (how much text a model holds at once) is measured in tokens, and latency grows with the count. So the same message costs a Tamil speaker several times what it costs me, in all three currencies.

The fix is boring and it works: count on a corpus that is not only English, and buy more compartments. [Llama 3](https://arxiv.org/abs/2407.21783) shipped 128,256 sorts against Llama 2's 32,000, by taking about 100,000 from [tiktoken](https://github.com/openai/tiktoken) and adding 28,000 chosen for non-English text. Meta's own measurement has characters per token going from 3.17 to 3.94 on English, with most of the win on code.

## How big should the case be?

So why not cast a million sorts?

Because the case is not free. Every compartment is a row in the embedding table on the way in, and a column in the output layer on the way out. At a width of 4,096 with untied weights, that is $2 \times 4096 = 8{,}192$ parameters per compartment, including the ones nothing ever goes through. A 256,000-sort case spends about 2.1 billion parameters before the model has done any thinking.

![Bar chart of six shipped tokenizers' vocabulary sizes, from 32,000 to 256,000, each labelled with its parameter cost](/images/blog42/vocab-sizes.png) *Figure 4: what the shops actually keep, from Llama 2's 32,000 to Gemma's 256,000. At a width of 4,096 that last drawer alone would outweigh the whole of GPT-2. Source: Author*

[Tao et al. (2024)](https://arxiv.org/abs/2407.13623) put vocabulary size into the scaling law and fitted it, training models from 33M to 3B parameters. Their conclusion is that bigger models deserve bigger cases, and that most shipped ones are too small. At a fixed budget of 2.3e21 FLOPs, going from 32,000 sorts to 43,000 took [ARC-Challenge](https://huggingface.co/datasets/allenai/ai2_arc), a set of grade-school science questions written to be hard for retrieval, from 29.1% correct to 32.0%. Same compute, same architecture, three points, from a counting script. They put Llama 2 70B's optimum at 216,000 sorts or more, about seven times what it shipped with.

You can also go stranger. [SuperBPE (2025)](https://arxiv.org/abs/2503.13423) asks why a ligature may never cross a space, when "of course" and "New York" behave like single units. Let the merges span whitespace after a while, and at a fixed 200,000-sort case the same text costs up to 33% fewer tokens. Their 8B model, trained at matched compute, came out 4.0 points better on average across 30 tasks and 8.2 better on [MMLU](https://arxiv.org/abs/2009.03300), the 57-subject test the [benchmarks post](/blog/llm-benchmarks-terminal-bench/) watched saturate. And it cost 27% less to run.

## The sorts nobody ever inked

In February 2023, Jessica Rumbelow and Matthew Watkins went through GPT-2's embedding table and found sorts (tokens) that made models behave strangely. Ask about ` SolidGoldMagikarp` and you got evasion, insults, or a different word. I checked GPT-2's case myself: ` SolidGoldMagikarp` is compartment 43453, ` petertodd` is 37444, ` davidjl` is 23282, all three single sorts cast from somebody's Reddit username.

The cause is that the two steps read different corpora. The case was fitted on a scrape containing a subreddit where a few users posted constantly, so their names counted as frequent pairs and won compartments. Then the training text was filtered and those strings were gone, so the row never moved off its random initialisation. Feed one in and the model gets a vector pointing somewhere arbitrary, which is why the failures look unhinged rather than blank. [Land and Bartolo (2024)](https://arxiv.org/abs/2405.05417) automated the search and found them across most open models.

## Where things are going

The obvious move is to stop keeping a case at all.

**[Byte Latent Transformer](https://arxiv.org/abs/2412.09871) (Meta, 2024)** works on raw bytes and cuts a new patch wherever a small model says the next byte is hard to predict. Predictable stretches get long patches and cheap compute, surprising ones get short patches and more of it. At matched training compute it keeps up with Llama 3 to 8B parameters, on up to 50% fewer operations at inference.

**[MambaByte](https://arxiv.org/abs/2401.13660)** takes the other road. If byte sequences only hurt because they are long, use an architecture whose cost is linear in length, which the [Mamba posts](/blog/mamba-is-attention-all-you-really-need/) were about.

**[H-Net](https://arxiv.org/abs/2507.07955) (Hwang, Wang and Gu, 2025)** learns the chunking itself, with a routing module that predicts boundaries and a smoothing trick that makes a discrete cut differentiable. One stage of it already beats a BPE Transformer on standard benchmarks. The gap is widest on Chinese, code and DNA, the three places a handcrafted case has always looked silly.

## Broken type

I would not bet the house on any of that yet. Five things I would push back on.

**The byte-level models move the cost rather than deleting it.** BLT's patcher is a second network you have to train, and its entropy threshold is one more number somebody picks by hand. The shop has not stopped deciding what to cast. It has hired somebody to decide live, and it is paying him.

**Nobody can fix a tokenizer after the fact.** The case is frozen before a run that may cost eight figures, and changing it later means retraining or surgery on the embedding table. That is a terrible place for a decision made by counting pairs on whatever corpus was handy that week.

**Bigger cases are a tax too.** "Larger models deserve larger vocabularies" is fitted from models up to 3B and extrapolated to 70B. I want to see somebody train the 216,000-sort Llama before I treat it as settled.

**There is no agreed way to score a tokenizer.** Fertility is the usual proxy because it is easy to compute, and it measures compression, not whether the model learns better. So people pick one by fertility, freeze it, train, and find out eight figures later.

**And my own numbers come in two piles.** I ran the GPT-2 ones on its published merge file: the merge order, the 50,257, the 21 sorts for வணக்கம், the glitch compartments, the ` 123`/`45`/`67` split. Everything else here comes from papers and launch posts I read about rather than reran.

## Conclusion

The tokenizer is the least glamorous part of a language model and the only part that is not learnt. It is a case of metal type, cast once by counting pairs in somebody's corpus, frozen, and blamed for the rest of the model's life. It decides that my name costs 30 compartments and yours costs one, and that your addition problem arrives with its digits grouped the wrong way round.

My bet is that the fixed case goes on cost rather than on principle. The moment a byte-level model is plainly cheaper to serve at the same quality, nobody will defend a drawer fitted on a corpus they cannot name. Until then we are running the largest computers anybody has built on top of a frequency count, and every so often the press stops because the compositor reached for a letter that was never cast.

And now you know. Fin.
