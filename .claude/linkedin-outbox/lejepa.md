---
slug: lejepa
title: LeJEPA - Good in Every Direction
blog_date: 2026-07-15
image: images/blog29/cover.jpg
alt: a poured melt, cored along two dozen random directions at once. Decorative, and also roughly what SIGReg does a thousand times a step.
publish_after: 2026-09-07T08:30:00-07:00
source: blog-companion
---

A master smith quenches at a temperature his grandfather picked and hammers the billet three hundred times. Ask which step matters and he cannot tell you.

That was self-supervised learning for five years: an EMA teacher, a stop-gradient, a deliberately weak predictor, a schedule somebody tuned. Remove any one of them and the run flatlines on day two, and nobody could tell you why.

So why not drop the charms and see what breaks? Because you cannot read the loss: it falls whether the model is learning or quietly collapsing toward "a person, probably".

LeJEPA swaps the lot for one term. Cast a part before anyone tells you what it bolts to and you pour it equally strong in every direction, because the load will arrive from an angle you did not choose. Embeddings have the same problem: the downstream task points somewhere nobody has told you about yet. You cannot X-ray an ingot, so LeJEPA core-samples instead, a thousand random directions every step, each shadow tested for normality.

The training loss now tracks probe accuracy at 94%+ Spearman, so you can finally pick a model without labels. That is the bit I would actually build on.

The heuristics are not really gone though. The theorem fixes the shape of the embedding cloud and says nothing about what should count as two views of the same image, and that is still 2 global crops, 6 local crops and a stack of colour jitter thresholds inherited from DINO and never re-derived. Given a choice of which half to put a proof under, I would have picked that one.

I wrote up the isotropy argument and the slicing test. Part 2 of the JEPA two-parter:
https://cgnarendiran.github.io/blog/lejepa/

#LeJEPA #JEPA #SelfSupervisedLearning #RepresentationLearning #AI
@[Fast Code AI](urn:li:organization:70969206)
