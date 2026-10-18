---
slug: tokenizers-bpe
title: Tokenizers - Out of Sorts
blog_date: 2026-10-04
image: images/blog42/cover.jpg
alt: A line of type set in a composing stick, resting on a case of sorts.
publish_after: 2026-10-18T14:55:17-07:00
source: manual
---

Type "hello" into GPT-2, an early OpenAI model, and it reads one piece. Type வணக்கம், the Tamil word for hello, and it reads twenty-one.

It's the same word, and it costs twenty-one times as much. An AI never reads letters, only pieces cast for it in advance.

Picture a print shop in 1890. A tray holds a hundred compartments, one metal letter in each. The typesetter reaches for t, then h, then e, all day long. So the shop casts one piece that reads "the", and three picks become one.

Every AI model has a tray like this, bigger but still a fixed size. It's filled before the model learns anything, by counting the commonest letter groups in a pile of text. That pile was mostly English. So "hello" got a compartment of its own and Tamil never got one.

I counted both words myself, in the piece list OpenAI published for GPT-2. Bigger trays help, but a 2023 study still found one sentence needing up to 15 times more pieces in some languages. And you pay for AI by the piece (guess whose bill comes out bigger?).

I wrote something on how the tray gets filled (the pieces are called tokens), and why a bigger one is no free fix. Link below:
https://cgnarendiran.github.io/blog/tokenizers-bpe/

#AI #MachineLearning #LLMs #Tokenization #NLP
@[Fast Code AI](urn:li:organization:70969206)
