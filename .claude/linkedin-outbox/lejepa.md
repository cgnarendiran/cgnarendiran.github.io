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

That was self-supervised learning for five years: an EMA teacher, a stop-gradient, a deliberately weak predictor, a schedule somebody tuned. Skip one and the run flatlines two days in.

So why not drop the charms and see what breaks? Because you cannot read the loss: it falls whether the model is learning or quietly collapsing toward "a person, probably".

LeJEPA swaps the lot for one term. Cast a part before anyone tells you what it bolts to and you pour it equally strong in every direction. The load comes from an angle you did not pick. Embeddings, same. You cannot X-ray an ingot, so it core-samples: random directions, test each shadow.

The training loss now tracks probe accuracy at 94%+ Spearman, so you can finally pick a model without labels. That is the bit I would actually build on.

The heuristics are not really gone though, since it still trains on crops and colour jitter lifted wholesale from DINO. The superstition moved house, it did not leave town.

I wrote up the isotropy argument and the slicing test. Part 2 of the JEPA two-parter:
https://cgnarendiran.github.io/blog/lejepa/

#LeJEPA #JEPA #SelfSupervisedLearning #RepresentationLearning #AI
@[Fast Code AI](urn:li:organization:70969206)
