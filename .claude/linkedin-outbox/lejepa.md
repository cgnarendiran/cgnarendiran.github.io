---
slug: lejepa
title: LeJEPA - Good in Every Direction
blog_date: 2026-07-15
image: images/blog29/cover.jpg
alt: a poured melt, cored along two dozen random directions at once. Decorative, and also roughly what SIGReg does a thousand times a step.
publish_after: 2026-09-07T08:30:00-07:00
source: blog-companion
---

A master smith quenches at a temperature his grandfather picked and hammers the billet three hundred times. Ask him which step matters and he cannot tell you.

That was self-supervised learning for five years: an EMA teacher, a stop-gradient, a deliberately weak predictor, and a schedule somebody tuned once and never touched again. Skip one and the run flatlines two days in.

So why not drop the charms and see what breaks? Because you cannot read the loss. It falls whether the model is learning or quietly collapsing onto one answer for everything, so the only way to find out is to finish the run and probe it.

LeJEPA swaps the lot for one term. Cast a part before anyone tells you what it bolts to and you pour it equally strong in every direction, because the load will come from an angle you did not pick. Embeddings work the same way, and the shape that is equally strong in every direction is an isotropic Gaussian. You cannot X-ray an ingot, so LeJEPA core-samples it: a thousand random directions a step, each shadow tested against a bell curve (the test dates from 1936, written by two statisticians with no GPUs between them).

The training loss now tracks probe accuracy at 94%+ Spearman, so you can pick a model without labels. That is the bit I would actually build on.

The catch is that the heuristics are not really gone. It still trains on crops and colour jitter lifted wholesale from DINO, and the theorem says nothing about what should count as two views of the same thing.

I broke it all down. Part 2 of the JEPA two-parter:
https://cgnarendiran.github.io/blog/lejepa/

#LeJEPA #JEPA #SelfSupervisedLearning #RepresentationLearning #AI
@[Fast Code AI](urn:li:organization:70969206)
