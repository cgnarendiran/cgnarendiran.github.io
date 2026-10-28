---
layout: post
title:  "Where a Fact Lives - Two Bits a Parameter"
date:   2026-10-28
image:  images/blog49/cover.png
description: "A model holds about two bits of fact per parameter, and anything it read only once gets memorised in a shape no question can reach."
tags: [llms, information-theory, synthetic-data, transformers, nlp]
---

*On the cover: a placeholder, drawn rather than found. Wikimedia Commons was unreachable from the machine that built this post, so the photograph this wants, a family round a cassette player arguing about who sang what, is missing. Source: Author.*

There is one at every wedding. The uncle who knows every film song ever recorded: the year, the singer, and whether the version you are humming is the film one or the cassette one.

So somebody tests him. Not with a hit, with a B-side from 1991 that he heard maybe twice in his life off a cousin's borrowed tape. He sings the whole thing, every word, in order, no stumbles. Then you ask him who sang it.

Nothing. Not a wrong answer, not even a guess. He has never held that as a fact at all. He has it as a sound that follows another sound.

Welcome to the era of **the physics of language models**. This is the story of where a fact actually sits inside a model, why one it read only once is nearly useless to it, and how many of them fit.

The physics bit is about method, not grandeur. Zeyuan Allen-Zhu and Yuanzhi Li have been publishing a series of papers under that title, and their complaint is that you learn very little by prodding a frontier model about Napoleon. You never know what it saw. You also do not study turbulence by filming the Bay of Bengal, you build a wind tunnel where you control the air and know the shape of the wing. So they built the wind tunnel.

## A hundred thousand people who were never born

The air in this tunnel is a dataset called **bioS**: a hundred thousand biographies of people who do not exist. Each person gets six attributes: birth date, birth city, university, major, employer, and the city they work in. Each attribute becomes one sentence, drawn from about fifty interchangeable templates, so a biography reads like a passport with literary ambitions. The templates vary across the dataset rather than within a person, so each person's own biography is written one way and one way only. There is a second version called **bioR**, where [Llama-30B](https://arxiv.org/abs/2302.13971) rewrites the same people into prose a human might actually have filed. It is there to check that none of this is an artefact of templated text.

Why bother faking it? Because with real text you can never prove the model has not already seen your test question, and a memorised answer and a recovered fact look identical from outside. Here, somebody wrote the universe, so every fact that went in is on a list.

Now take a model shaped like [GPT-2](https://huggingface.co/openai-community/gpt2), the 2019 text generator these experiments mostly use because it is small enough to train a hundred times over. Train it on the biographies until it has them cold. You can check that it does: hand it the first half of any biography and it finishes the rest word for word, commas and all. Then ask it a simple question in a form it has not seen before. Where was Anya Briar Forger born?

It cannot tell you. Accuracy on questions in that form sits near zero.

## The B-side problem

That is the finding in [Physics of Language Models: Part 3.1, Knowledge Storage and Extraction](https://arxiv.org/abs/2309.14316), and the uncomfortable part is what fails to fix it. Fine-tune the trained model on question-answer pairs afterwards, which is what anybody would try first. It then answers questions about the people whose pairs it was shown. Ask about the other half of the hundred thousand and you are back to nothing.

So the problem is not the question format, because the format is clearly learnt. The facts are in there too, since it can recite them on demand. They are sitting in a shape that a question cannot reach. And fine-tuning cannot move them, because by then the filing is done: it can only teach the model to use what is already reachable, which for the unseen half is nothing.

I want you to sit with how strange that is. The model will produce the string "Anya Briar Forger was born on October 2nd, 1996" if you give it the run-up, and it cannot answer "when was Anya Briar Forger born". Nothing about the information changed between those two requests. Only the order in which it was asked for.

## Where the fact actually sits

To find out where it went, the authors use a **linear probe**. A model chops text into **tokens**, which are words or pieces of words. It carries a list of numbers alongside each one as it reads. You take that list at one chosen token, fit a plain linear classifier on it alone, and see whether an attribute can be read straight off. If the classifier can get the birth city out, the birth city is sitting right there in a usable form. If it cannot, the information is either absent or smeared into a shape only the rest of the network can undo.

The answer is clean, and it is the most useful thing in the whole series. In the model that can answer questions, a person's attributes are linearly readable from the vector sitting on **the tokens of their name**, with nothing but the name in front of it. In the model that cannot, the same information is spread thinly across every token of the biography: a little on "works", a little on "in", a little on the full stop at the end.

And at question time the name is all the model has to go on, so if nothing was filed under the name, nothing comes back.

![Two rows of word boxes for one biography, with orange bars showing attribute information pooled over the name words in the top row and spread evenly over every word in the bottom row, and a zoom panel on the name vector](/images/blog49/where-the-fact-sits.png) *Figure 1: the same facts, two filing systems. Top, the model trained on many wordings: the attributes are readable off the name tokens, which is all a question gives it to work with. Bottom, the model trained on one wording: the same information is spread over every word of the biography, where a question cannot get at it. The zoom is the vector a linear probe reads. Drawn to show the finding, not plotted from the paper's probe scores. Source: Author*

Writing the same fact down many different ways before the model ever sees it is what everybody calls **data augmentation**. The uncle's hit songs are the augmented ones. He heard each of them on the radio, in a lift, as somebody's ringtone, sung flat at three weddings, and on an antakshari show in 1998. Every rendering carries the same facts in a different arrangement. So the facts are the only thing those renderings have in common, and that is what sticks to the title. The B-side he heard twice, and both times it was the same recording.

So the fix is to do deliberately what the radio did by accident. Four things work:

1. Write each person's biography several times over, in different wordings.
2. Shuffle the order of the six sentences.
3. Use the person's full name in every sentence instead of "he" or "she".
4. Mix question-answer pairs for *some* of the people into pretraining, rather than saving all of them for a fine-tuning stage later.

And here is the **ablation**, which means the experiment where you remove one ingredient and see what breaks. Everything is held fixed: the same facts, the same architecture, and the same amount of training. One run sees each person's biography in a single fixed wording, read over and over. The other sees the same facts spread across several wordings. The first memorises every word and answers nothing, the second answers. The facts in the first run were read hundreds of times each. Repetition was never what was missing, and the only difference was how many wordings they arrived in.

These things are magpies. Give a model one wording of a fact and it will learn that sentence, the comma and the typo, and almost nothing about the world the sentence was describing.

## Antakshari

Say you have fixed extraction, so the uncle can answer questions about a song. [Part 3.2, Knowledge Manipulation](https://arxiv.org/abs/2309.14402) asks what else he can do with a fact, and sorts it into four jobs.

1. **Retrieval.** "Who sang this one?" This works, and it is the thing we just fixed.
2. **Classification.** "Was it released in an even year?" Shaky.
3. **Comparison.** "Which came first, this one or that one?" Also shaky.
4. **Inverse search.** You are given the value and have to produce the thing it belongs to. "Which song has the line about the broken bangles?" Or the game itself: somebody ends on *ma*, and you have to name a song whose first syllable is *ma*. This is the flat one.

The shakiness in jobs two and three has a cause worth knowing. They work when the model writes out the intermediate fact before committing to an answer, which is a chain of thought. But asking for the reasoning in the prompt is not enough: it has to have been in the training data as well, in the same shape. The uncle gets the comparison right only if he is the kind of person who mutters it out loud first. *That one was during my college years, so about '94. The other came after my sister's wedding, so '98.*

Inverse search is the one that does not bend. Accuracy stays near zero whatever you do to the prompt, and the revised version of the paper reproduced it on Llama and Mistral shapes too. If the training data only ever says "Anya Briar Forger works in Princeton", then "who works in Princeton" is a question about a direction the model has never once been pushed in.

You have met this as the **reversal curse**, named at almost the same time by [Berglund et al., 2023](https://arxiv.org/abs/2309.12288). A model told that A is B's parent cannot reliably tell you that B is A's child. And it is most of the reason [retrieval](/blog/retrieval-bm25-to-hybrid/) exists as an industry. Put the document in the context window and the backwards question stops being a memory problem. It becomes a lookup, which is the thing computers were always good at.

![Bar chart of four task families with retrieval high, classification and comparison middling with an orange extension for chain of thought, and inverse search at the floor](/images/blog49/four-jobs.png) *Figure 2: four things to do with a fact a model already holds extractably, which is why retrieval is high. The orange is what chain of thought adds, and it only arrives when the reasoning was in the training data too. The bars are the shape of the result rather than exact figures from one table. Inverse search is at the floor and stays there however politely you ask. Source: Author*

## Two bits a parameter

The third paper, [Part 3.3, Knowledge Capacity Scaling Laws](https://arxiv.org/abs/2404.05405), asks the question an engineer actually wants answered. How many facts fit?

To get a number out of this you have to count knowledge in bits, which is the right move and where all the argument lives. In words, the capacity ratio is

$$R = \frac{\text{bits of fact you can get back out of the model}}{\text{number of parameters it has}}$$

specifically,

$$R = \frac{B}{P}$$

where $B$ is the number of bits of the knowledge set the model can be made to answer questions about, and $P$ is its parameter count, meaning how many adjustable numbers the thing has in it. The whole paper is a measurement of that one ratio, run again and again at different model sizes.

Let's do the counting by hand, because the arithmetic is the entire intuition. The option counts below are mine, picked to be roughly the right size rather than lifted from the paper.

- birth date, say 365 days across 200 years, so 73,000 possibilities, which is $\log_2 73{,}000 = 16.16$ bits
- birth city, one of 200: 7.64 bits
- university, one of 300: 8.23 bits
- major, one of 100: 6.64 bits
- employer, one of 250: 7.97 bits
- working city, one of 200: 7.64 bits

Add those up and you get the knowledge in one person, which is

$$B_{\text{person}} = \sum_{a=1}^{6} \log_2 N_a = 54.28 \text{ bits}$$

where $N_a$ is how many different values attribute $a$ could have taken, and the sum runs over the six attributes. So each person costs about 54 bits. Times a hundred thousand people, the entire dataset is 5.4 million bits of actual knowledge. Call it 680 kilobytes, which is one dull photograph. And at two bits a parameter, the smallest model that could hold all of it is about 2.7 million parameters.

Two bits a parameter is the finding. Not 1.7, not 2.4. The authors train small models, millions to hundreds of millions of parameters, on knowledge sets of many sizes. And the ceiling comes back at 2 across widths and depths, and across GPT-2, Llama and Mistral shapes. Architecture barely moves it, which is a quietly brutal result for a decade of architecture papers.

![A log-log plot of bits of fact against parameter count with three straight lines at two, one and 0.7 bits per parameter, a green dot marking this post's worked example and a blue diamond marking a 7B model](/images/blog49/capacity-line.png) *Figure 3: bits of recoverable fact against parameter count, on log axes, so a fixed number of bits per parameter is a straight line. Drawn from the paper's three constants rather than traced off its plots. The top line is the 2-bit ceiling under heavy training, the middle one is a hundred exposures per fact, and the bottom one is int4 weights. Source: Author*

The ceiling comes with conditions, and the conditions are the interesting part. All of them assume extraction is already fixed, so "seen" below means seen in the varied form from the last section.

| What you change | Capacity | What it buys you |
|---|---|---|
| Each fact seen ~1000 times | 2 bits per parameter | the ceiling, and it takes a lot of repetition to reach |
| Each fact seen ~100 times | about 1 bit per parameter | half the storage, for a fact a tenth as familiar |
| Weights to int8 | about 2 bits per parameter | free, which is why 8-bit serving is everywhere |
| Weights to int4 | about 0.7 bits per parameter | roughly two thirds of the facts gone |
| Source name prepended to the text | higher | the model works out which domains to trust |

The int4 row is the one to take to work on Monday. We talked about [quantization](/blog/quantization-edge-inference/) as a story about outliers and activation ranges. At four bits the weights can still do the language, and part of what they can no longer do is remember. So a shrunk model goes vague about dates and names before it goes wrong about grammar.

The last row is the junk-data story, and the uncle explains it best. His head also holds every detergent jingle from 1994, which is a fact I am sorry to report. Those cost him the same storage the songs do. What saves him is that he knows which is which, because a jingle arrives labelled by thirty seconds of television either side of it. The paper's version is to prepend the source, something like `wikipedia.org`, to each piece of training text. Capacity goes up, and the model sorts out for itself which domains are worth the room.

I should flag one gap. The paper also measures what low-quality data costs you. But I have seen that summarised three ways with three different multipliers, so I am quoting the fix rather than the number.

Run the 2 bits out to a model you have actually used. A 7B model is 14 billion bits, or 1.75 gigabytes of fact. The authors reckon that beats English Wikipedia and the textbooks put together, which I think is generous. The photo folder on your phone is bigger than everything a 7B model knows about the world.

## Where this shows up

- **Rewriting the pretraining corpus is a stage now, not a trick.** If one wording of a fact is worth close to nothing extractable, paraphrasing what you already have beats scraping more of it. It also explains why [distillation](/blog/knowledge-distillation/) does better than it should. A teacher rewriting the corpus is an augmentation machine with good taste.
- **"We will fine-tune it on our company documents" usually disappoints.** A few hundred internal PDFs, seen once each, is the B-side case exactly. The model picks up your house style and still cannot answer questions about the contents. That is a retrieval job.
- **Adapters have a ceiling you can estimate.** The worked example in the [LoRA](/blog/lora-efficient-fine-tuning-llms/) post was rank 8 on one $4096 \times 4096$ matrix, which is 65,536 trainable parameters. At two bits each that is 131 kilobits, or 16 kilobytes of new fact in that layer. The papers never measured adapters, so treat it as a back-of-envelope ceiling rather than a result, and note that the bullet above is the usual reason you do not get near it.

## Where things are going

- **Capacity per domain rather than per model.** The useful version of this number is how many bits of medicine, or Tamil, or tax law a given size can hold, and nobody has run that experiment.
- **Quantization-aware training, if you care about facts.** The authors suggest it directly: for a good int4 model the four bits have to be there during training.
- **Editing a fact instead of retraining for one.** If an attribute sits on the name tokens you can go in and change it there, which is what model editing has been trying since 2022, and whether an edit sticks or only paints over one phrasing is the thing to watch.

## The wind tunnel is not the weather

Everything above was measured on invented people, by models between millions and hundreds of millions of parameters. Extending it to a 70B model trained on the open internet is an extrapolation, and the paper is honest that it is one.

The 2 bits also assumes conditions no real corpus has ever met: facts that are clean, deduplicated, roughly uniform, and seen a thousand times each. The web is a long tail where most things appear once, badly, in a forum post from 2011. So 2 bits a parameter is a ceiling reached in a laboratory, and not a budget you can book against.

Then there is the definition. Bits of knowledge are counted against a distribution the authors designed themselves, so the constant is partly a property of their own encoding choices. What survives is the shape of the finding: capacity tracks parameter count linearly and architecture hardly matters. The number 2 stands on shakier ground than the straight line does.

And the triple is a narrow idea of knowing. Most of what a model does for you is not a (person, attribute, value) lookup. Summarising a long email thread and writing a polite refusal both need almost no facts and a great deal of something else, and they run on the same parameters this law is counting. The result says nothing about how much of that fits.

## Conclusion

The uncle who can answer questions got there by hearing the same songs in more voices, which is how the facts came loose from the recording and stuck to the title instead. A model is the same, except that we get to pick how many voices it hears, and until fairly recently nobody thought that was the knob that mattered.

So the engineering bet for the next few years is that the next real gain in pretraining comes from rewriting what we already have rather than finding more. The second bet is that the 2-bit line turns into a planning number somebody drops in a spreadsheet before picking a model size. Both of those are cheap bets. The expensive question is the one I raised just above, which is whether facts are the thing we should be counting in the first place.

Either way, do not feel too bad for the uncle and his broken antakshari. Near zero on inverse search puts him in the same bracket as every model you have ever paid for.

And now you know. Fin.
