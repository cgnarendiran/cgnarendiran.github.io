---
slug: knowledge-distillation
title: Knowledge Distillation - The Perfumer's Apprentice
blog_date: 2026-09-20
image: images/blog35/cover.jpg
alt: a perfumer's organ, which is the real name for the tiered bench a perfume house keeps its bottles on, with the apprentice's much smaller one off to the right. I drew this one, because the machine this post was written on cannot reach Wikimedia Commons. Source: Author
publish_after: 2026-09-23T10:49:53-07:00
source: blog-companion
---

A bottle of perfume goes out with one word on the label, and the word is rose. The master who made it could tell you it is mostly rose, some jasmine, a little oud, and no vanilla.

That gap is knowledge distillation. The teacher hands the student its whole opinion, warmed with a temperature knob so a gradient can see the quiet notes.

So what does one word teach? Almost nothing, while the teacher's numbers say jasmine sits under rose because the two go together.

Hinton's paper pulled every 3 out of the training set, so the student never met one, and with one bias correction it still got 98.6% of the test threes right. It knew a 3 because the teacher kept saying "a bit like a 3" about other digits.

The catch is that the student never actually agrees with the teacher. Stanton and co. measured that gap and it stayed wide under every fix they tried, so distillation is doing the work of a very good regulariser.

What I would build on, imo, is the on-policy version, where the student writes first and the teacher grades the tokens it produced.

I broke it all down, from soft targets to what DeepSeek's distilled models actually are (the word now covers two techniques that share nothing):
https://cgnarendiran.github.io/blog/knowledge-distillation/

#KnowledgeDistillation #LLMs #DeepSeek #Gemma2 #AI
@[Fast Code AI](urn:li:organization:70969206)
