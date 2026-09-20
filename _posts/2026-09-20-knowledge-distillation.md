---
layout: post
title:  "Knowledge Distillation - The Perfumer's Apprentice"
date:   2026-09-20
image:  images/blog35/cover.jpg
description: "The label says rose. The teacher's nose says rose, some jasmine, and definitely not vanilla, and that last part is what the small model actually learns."
tags: [knowledge-distillation, efficient-training, llms, transformers, loss-functions]
---

*On the cover: a perfumer's organ, which is the real name for the tiered bench a perfume house keeps its bottles on, with the apprentice's much smaller one off to the right. I drew this one, because the machine this post was written on cannot reach Wikimedia Commons. Source: Author*

A perfume house keeps its bottles on a curved tiered bench called an organ, after the church instrument, because the perfumer sits in the middle of it and reaches three hundred things without standing up.

The master (the teacher model) sits there and makes something. It goes out with one word printed on the label, and the word is *rose*.

Now, that word is doing almost no work. What is in the bottle is mostly rose, with a good deal of jasmine under it, a little oud, a trace of something like wet stone after rain, and no vanilla whatsoever, which the master considered and ruled out. Print *rose* on the label and every one of those decisions is gone.

Welcome to the era of **knowledge distillation**. This is the story of how a 2 billion parameter model learns things it was never big enough to work out for itself, by being told what the right answer was and, much more usefully, how nearly it was something else.

The apprentice (the student model) has a shorter bench and, let's be honest, a smaller nose. Hand them ten thousand bottles each labelled with one word and they will learn ten thousand words. Sit them next to the master for a year and they learn what the master rejected, which turns out to be most of the job.

## What the label throws away

The label is not wrong. The bottle really is a rose. It is just that a label has room for one word, and the master has an opinion about three hundred.

So how much does one word carry? With a thousand possible notes, a label picks one out of a thousand, which is about ten bits, and you need a million bottles before the apprentice has seen anything at all. The master's opinion on that same bottle is a number for every note on the bench, and those numbers are not noise. Jasmine sits under rose because jasmine and rose genuinely go together. Vanilla is down at a thousandth of a percent because a rose is not a pudding.

![Two bar charts, one with a single bar at full height for rose, the other with the teacher's full distribution on a log scale down to vanilla](/images/blog35/soft_targets.png) *Figure 1: The same bottle, described two ways. The right-hand chart is on a log scale, because otherwise you cannot see the part that matters. Source: Author*

[Hinton, Vinyals and Dean, 2015](https://arxiv.org/abs/1503.02531) put it in terms of handwritten digits. One particular image of a 2 might get a probability of $10^{-6}$ of being a 3 and $10^{-9}$ of being a 7, and that ratio tells you which 2 it was. It was a leany, loopy one. And the ratio is worth more than the label, because it says something about the shape of the problem that no label for that image contains. Hinton called it **dark knowledge**, which is a better name than this field usually manages.

So the apprentice is not being taught the answers. They are being taught the master's whole opinion (the soft targets), including the parts the master would never say out loud.

## Warming the blotter

There is an immediate practical problem, which is that the softmax has already eaten most of it. By the time the teacher's numbers come out the other end of $\exp$, the winner sits at 70% and vanilla sits at six hundredths of a percent. And six hundredths of a percent contributes nothing whatsoever to a gradient, so the information is all still there and the optimiser cannot see any of it.

If you have ever been in a perfume shop you already know the fix. A blotter sniffed cold gives you the top note and pretty much nothing else, so you warm it in your hand and the heavier things underneath come up. Nothing was added to the blotter. You just stopped the top note drowning out the rest, and the knob below does exactly the same job.

In words, the teacher reports:

$$
\text{probability of a note} = \frac{\text{its vote, spread out by how much you warmed it}}{\text{the same, summed over every note on the bench}}
$$

specifically,

$$
p_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}
$$

where $z_i$ is the logit the teacher assigned to note $i$, and $T$ is the temperature, which is 1 for an ordinary softmax and larger when you want the quiet notes back. Dividing every logit by the same $T$, cannot change which one is biggest. It only changes how far ahead it is.

Let's do one by hand, with the six notes from Figure 1. The teacher's logits run from 4.0 for rose down to $-3.0$ for vanilla. At $T = 1$ we get $e^{4.0} = 54.6$ over a total of 77.9, so rose is 70.0%, and $e^{-3.0} = 0.050$ makes vanilla 0.064%. Rose is about 1,100 times likelier. Now warm it to $T = 4$. Every logit is quartered, so rose becomes $e^{1.0} = 2.72$ over a total of 8.94, which is 30.4%, and vanilla becomes $e^{-0.75} = 0.47$, which is 5.3%. The gap has gone from 1,100 to 5.8, and a gap of 5.8 is something a gradient can see.

![Grouped bar chart of the same six notes at temperatures 1, 2, 4 and 10, with the low-probability notes rising as temperature goes up](/images/blog35/temperature.png) *Figure 2: The same six logits, warmed four different amounts. At T=10 leather and vanilla score nearly as well as rose, at which point you have stopped warming the blotter and started setting it on fire. Source: Author*

And you can overdo it, obviously. Hinton's own tuning is the part worth stealing here: with 300 hidden units in the student, temperatures above 8 worked well, and with only 30 hidden units the sweet spot was 2.5 to 4. A smaller student wants a cooler teacher. That is the capacity gap showing up in 2015, in a footnote, wearing a disguise.

Then there is the housekeeping that everybody gets wrong exactly once. Gradients through a softmax at temperature $T$ come out about $1/T^2$ the size of the ordinary ones, so if you simply add the soft loss to the hard loss, the soft part quietly stops mattering the moment you raise the temperature. You multiply the soft term by $T^2$ to put it back. It is the least glamorous factor in this post and it is the difference between distillation working and distillation being a rounding error.

## What actually happens in one training step

The method is six steps long and not one of them is clever.

1. Take a batch of inputs. They do not need labels, which is the step people skip past.
2. Run the teacher over the batch with its weights frozen, and take its softmax at temperature $T$.
3. Run the student over the same batch, and take its softmax at the same $T$.
4. Measure how far apart those two distributions are, then multiply by $T^2$.
5. If you happen to have real labels, add an ordinary cross-entropy against them at $T = 1$.
6. Backprop into the student. The teacher never takes a step.

The distance in step 4 is the KL divergence, which we built from scratch in the [cross entropy post](/blog/cross-entropy-loss/) as the cost of using the wrong weather app. Here it is the cost of using the apprentice's nose instead of the master's:

$$
\mathcal{L} = \alpha\, T^2 \cdot \mathrm{KL}\big(p^{\,t}_T \,\Vert\, p^{\,s}_T\big) + (1 - \alpha) \cdot \mathrm{CE}\big(y,\, p^{\,s}_1\big)
$$

where $p^{\,t}_T$ and $p^{\,s}_T$ are the teacher's and the student's distributions at temperature $T$, $y$ is the hard label when you have one, and $\alpha$ sets how much you trust the master over the answer key. Most recipes put $\alpha$ somewhere north of 0.8, which tells you what the field thinks of labels.

![Flow diagram: a batch feeding a frozen teacher and a student, the teacher's soft targets and the student's guesses meeting at a KL term, plus a cross-entropy term against the hard label](/images/blog35/kd_recipe.png) *Figure 3: One training step. Two forward passes, one backward pass, and a frozen network that will never emit a token as long as it lives. Source: Author*

Step 1 is what makes any of this practical. The soft half of that loss needs no labels at all, so the transfer set can be any pile of text or images you happen to own. A labelling budget of zero and a teacher is enough.

## The apprentice who had never smelled a rose

Now the experiment that should have made this famous ten years before it got famous.

Hinton's setup on [MNIST](https://huggingface.co/datasets/ylecun/mnist), seventy thousand handwritten digits at 28 by 28 pixels, fits in a sentence. A teacher with two hidden layers of 1200 units, heavily regularised with dropout, makes 67 errors on the test set. A smaller net with two layers of 800 units and no regularisation makes 146. Train that same small net on the teacher's soft targets at $T = 20$ and it makes 74, so it has closed almost the whole gap to a model half again as wide, and nothing about it changed except what it was shown.

Then they did the thing that makes the point properly. They took every single example of the digit 3 out of the transfer set, so the student never sees a 3, is never told that a 3 exists, and has no output bias tuned for one.

It makes 206 errors, and 133 of those are on threes. Which sounds like a flat failure until you notice the threes are going somewhere consistent: the student just has the wrong bias on a class it never met. Raise the bias on the 3 output by 3.5 and the errors drop to 109, of which 14 are on threes. It gets 98.6% of the test threes right. (The 3.5 is not a round number and I trust it more for that. Somebody sat there and swept it.)

![Stacked bar chart of the 206 errors split into threes and other digits, dropping to 109 after a bias adjustment, beside a bar showing 98.6% of test threes classified correctly](/images/blog35/mythical_three.png) *Figure 4: A student that never saw a 3, classifying threes. Source: Author*

The apprentice has never smelled a rose. They know what a rose is because the master spent a year saying "a bit like rose" about other things.

## Four places to tap the teacher

Everything since 2015 is an argument about where you put the tap. The original method takes the logits. That is the strongest signal there is per example, and it also needs the teacher sitting on your machine, running over every batch you train on.

![Diagram of a teacher stack and a student stack with four labelled arrows between them: logits, hidden layers, distances between examples, and the text the teacher wrote](/images/blog35/four_kinds.png) *Figure 5: Four taps, at four depths. Three of them need the teacher's weights and one of them needs a credit card. Source: Author*

| Where you tap | What crosses over | What it costs you | Verdict |
|---|---|---|---|
| The logits | the teacher's whole opinion, per position | the teacher's weights, and a forward pass per batch | the densest signal there is, and the reason Gemma 2 exists |
| The hidden layers | intermediate features, through a small regressor | matched depths, a projection, a two-stage schedule | lets the student be deeper and thinner than the teacher, not merely smaller |
| The distances between examples | the geometry of a batch, rather than any one answer | a batch big enough to have geometry | survives a shape mismatch; weak on its own |
| Only the text that comes out | finished sentences, and nothing else | an API key | the only one that works through somebody else's product, which is why it is the one in the news |

### FitNets (2014): the hint

[FitNets](https://arxiv.org/abs/1412.6550) came out months before the Hinton paper and asked a different question. What if the student is deeper than the teacher, but much thinner? You cannot match logits down a network with a different shape, so they picked one middle layer of the teacher as a **hint**, one middle layer of the student as the guided layer, and trained a small convolutional regressor to map one onto the other.

Their 17-layer student has about 2.5 million parameters and gets 91.61% on [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html), sixty thousand small photographs sorted into ten classes. Their teacher has 9 million parameters and gets 90.18%. The student is 10.4 times smaller and it wins. That result is a decade old and people still find it surprising.

### DistilBERT (2019): half the layers, three losses

[DistilBERT](https://arxiv.org/abs/1910.01108) is the one everybody has actually deployed. Take [BERT](https://arxiv.org/abs/1810.04805) base, delete every second layer, initialise the survivors from the teacher's corresponding layers rather than from noise, and pretrain with three losses at once: the ordinary masked language modelling loss, the distillation KL against BERT's soft predictions, and a cosine loss pushing the student's hidden vectors to point the same way as the teacher's.

What comes out is 40% smaller, 60% faster, and holds 97% of BERT-base's score on [GLUE](https://gluebenchmark.com/), the nine-task English understanding benchmark everybody reported against at the time. For a lot of production work that trade was not close.

### Gemma 2 (2024): distillation as the pretraining recipe

Google's [Gemma 2](https://arxiv.org/abs/2408.00118) is where this stops being a compression trick and becomes how you train the model in the first place. The 2B and 9B are not pretrained on next-token prediction at all. They are pretrained on the 27B teacher's full distribution over the vocabulary, at every position, for over fifty times the token count that scaling laws call compute-optimal at their size.

The ablation is the part to keep. Train a 2B from scratch on 500B tokens, then train the same 2B on the same 500B tokens with a 7B teacher, and the distilled one comes out 7.4 points better on average. The architecture, the data and the token budget are identical, and the only difference is whether each token arrived as one right answer or as a full opinion.

![Dumbbell chart of three cases where the same student was trained alone and then distilled: MNIST errors 146 to 74, speech frame accuracy 58.9 to 60.8 percent, and Gemma 2 at 2B gaining 7.4 points](/images/blog35/does_it_pay.png) *Figure 6: Three students, three decades apart, the same architecture on each row. Source: Author*

Hinton's speech result sits in the middle of that chart and it is the one I find most convincing, because it is the boring industrial case. An 85M-parameter acoustic model trained on 2000 hours of speech gets 58.9% frame accuracy and a 10.9% word error rate. Ten copies of it, randomly initialised and averaged, get 61.1% and 10.7%. One model distilled from those ten gets 60.8% and 10.7%, so you keep essentially the whole benefit of the ensemble and ship one model instead of ten.

### DeepSeek-R1-Distill (2025): eight hundred thousand bottles

And then there is what the word means now. When [DeepSeek-R1](https://arxiv.org/abs/2501.12948) shipped in January 2025 it came with six "distilled" models, and not one of them involves a KL divergence or a temperature. R1 was asked to generate 800,000 reasoning samples, and open [Qwen2.5](https://arxiv.org/abs/2412.15115) and [Llama 3](https://arxiv.org/abs/2407.21783) base models were fine-tuned on that text for two or three epochs. That's it. There are no logits anywhere in it, and no teacher in the loop once the samples exist.

It works embarrassingly well. R1-Distill-Qwen-7B gets 55.5% on [AIME 2024](https://artofproblemsolving.com/wiki/index.php/American_Invitational_Mathematics_Examination), the American invitational maths olympiad, and R1-Distill-Qwen-32B gets 72.6% there and 94.3% on [MATH-500](https://huggingface.co/datasets/HuggingFaceH4/MATH-500), 500 competition maths problems. DeepSeek's own conclusion is the bolder claim: running large-scale [RLVR](/blog/grpo-rlvr/) directly on the small base model does not get you where copying the big model's homework does. So for a 7B model the cheapest route to reasoning may not be to discover it but to be handed it.

This is [sequence-level distillation](https://arxiv.org/abs/1606.07947), which Kim and Rush wrote down for machine translation back in 2016, where students trained this way ran ten times faster than their teacher and mostly stopped needing beam search. It has been sitting there the whole time. It just needed a teacher worth copying.

## The apprentice makes their own blend

Copying finished bottles has a specific failure, and it is an old one.

The student only ever trains on sentences the teacher would have written. At inference it writes its own, and four tokens in it is somewhere the teacher would never have gone, and nobody has ever shown it what to do out there. This is the compounding-error problem behaviour cloning has had since forever, which we ran into from the other side in the [RLHF post](/blog/reinforcement-learning-from-human-feedback/).

![Two panels: off-policy training where the student's path drifts out of the region the teacher covers, and on-policy training where the teacher corrects the student's own path at every token](/images/blog35/on_policy.png) *Figure 7: The same student, supervised two ways. On the left it is graded on the master's blends. On the right the master smells what the apprentice actually made. Source: Author*

So flip it around, and let the student generate before the teacher scores the tokens it actually produced. [MiniLLM](https://arxiv.org/abs/2306.08543) does this, and swaps the direction of the KL while it is in there, which matters more than it sounds. Forward KL asks the student to put mass everywhere the teacher does, including the long tail it has no capacity to represent, so a small student ends up putting real probability on sentences nobody would finish. That is the model being obedient rather than stupid, although from outside the two look identical. Reverse KL is mode-seeking, so it tells the student to get the likely stuff right and let the rest go.

[On-policy distillation](https://thinkingmachines.ai/blog/on-policy-distillation/) (Thinking Machines, 2025) is the clean modern statement of it: the student samples a trajectory, a frozen teacher grades every token of it with per-token reverse KL, and that is the whole loss. They report Qwen3-8B reaching 70% on AIME 2024 at roughly a tenth of the compute of the RL route, which makes sense when you line the two signals up. [GRPO](/blog/grpo-rlvr/) gives you one bit at the end of a thousand-token answer. A teacher gives you a full distribution on every token of it, and it never has to be right about anything, only consistent.

## Where things are going

Distillation is becoming the way you build a small model rather than something you do to one afterwards. Gemma 2 and 3 are the visible case, and most of the small models shipping now have a bigger sibling somewhere in their training loop.

There is also a scaling law for it now. [Distillation Scaling Laws](https://arxiv.org/abs/2502.08606) (Apple, 2025) fits student loss as a function of teacher size, student size and token budget, and hands you the compute-optimal split. Their caveat is the honest one: if you are training exactly one student and you have to train the teacher as well, plain supervised learning usually wins. Distillation pays when the teacher already exists, or when you are going to distil it many times.

The mechanism is still contested, and the evidence moved recently. [Revisiting Knowledge Distillation](https://arxiv.org/abs/2510.15516) (Lanzillotta et al., 2025) varies dataset size and finds the benefit grows as the data shrinks, up to a 3x data-efficiency gain, across CNNs and Transformers and across vision and language. They argue that this rules out the "distillation is just label smoothing" reading, which had been the deflationary explanation for years.

## The nose that will not transfer

A few things I would want said out loud before anybody builds on this.

### The student does not actually learn the teacher's function

[Does Knowledge Distillation Really Work?](https://arxiv.org/abs/2106.05945) (Stanton et al., NeurIPS 2021) separates two things the field had been running together. Fidelity is whether the student agrees with the teacher, and generalisation is whether the student is any good. Distillation reliably improves the second and is bad at the first: the gap between teacher and student predictive distributions stays large under every intervention they try, and pushing fidelity up does not reliably drag generalisation with it. They trace the cause to optimisation rather than capacity or data, which means the student could match the teacher and the optimiser simply does not take it there.

So when somebody tells you a 7B model was distilled from a 400B one, hear it as "trained with a very good regulariser", because that is closer to what the measurements say. The apprentice comes out with a nose of their own, which was never the deal anybody thought they were making.

### Too good a teacher makes a worse student

Here is the one that costs people a month. Past some gap, a bigger teacher produces a worse student, because the student cannot represent a distribution that far from anything it can express. [TAKD](https://ojs.aaai.org/index.php/AAAI/article/view/5963) (Mirzadeh et al., 2019) patches it by putting intermediate models in the chain, distilling teacher to assistant to student, which works and costs a full training run per link plus whatever errors each assistant invents. So the practical answer in 2026 is still to try three teacher sizes and measure, which is not a satisfying thing to put in a design document.

### The word now covers two techniques that share almost nothing

Hinton distillation needs the teacher's logits, every batch, on your hardware. What most 2026 press releases mean by it is fine-tuning on text that a teacher wrote, which needs no logits and no teacher at all once the data exists. One is a training objective and the other is a dataset. They carry the same name because the second grew out of the first, and telling them apart matters the moment you try to reproduce somebody's numbers.

### The legal question is wide open

In January 2025, OpenAI told the Financial Times it was investigating whether DeepSeek had built a training set out of GPT-4o responses, which would break its terms of service. DeepSeek denies it and says its models were trained independently. In February 2026, OpenAI put an intellectual property allegation to the US Congress's China Select Committee. No court has decided anything, and whether model outputs can carry that sort of restriction has not been settled anywhere. Every major provider forbids it in their terms, and it is also, unmistakably, how a large part of the open-weight ecosystem got built.

## Conclusion

The perfume house has been the same building the whole way through. There is a master at a long bench and an apprentice at a short one, and the entire argument is about what gets passed between them.

Hand over the labels and you hand over almost nothing, because a label is one word about a thing that took three hundred bottles to make. Hand over the full opinion, warmed enough that the quiet notes are audible, and a much smaller nose reproduces most of a much larger one. Every variant since 2015 is a fight over which surface of the teacher you may touch: the logits, a middle layer, the shape of a batch, or just the text it wrote for somebody who was paying per token.

What none of it settles is the awkward bit in the middle. An apprentice who never smelled a rose can pick a rose out of a line-up. And an apprentice who trained for a year on the master's every opinion, still disagrees with the master constantly when you go and measure it. Both of those are true at once, and after a decade nobody can tell you exactly what got across.

And now you know. Fin.
