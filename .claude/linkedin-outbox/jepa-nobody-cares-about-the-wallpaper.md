---
slug: jepa-nobody-cares-about-the-wallpaper
title: JEPA - Nobody Cares About the Wallpaper
blog_date: 2026-06-15
image: images/blog28/cover.jpg
alt: A police sketch in progress, drawn from a description rather than a photograph
publish_after: 2026-09-07T08:30:00-07:00
source: blog-companion
---
A witness never paints you the room. She says: tall, grey coat, walked with a limp. The wallpaper, the carpet, the coffee cup, all thrown away, none of it missed.

Computer vision made the other choice for a decade.

Masked autoencoders hide 75% of an image and ask for the missing pixels back. It also asks the model to paint the wallpaper. The grain of the tarmac, the speckle in the shadows: unpredictable in principle, and the loss punishes the model for missing them anyway.

Welcome to Joint-Embedding Predictive Architectures. JEPA throws out the decoder. Two encoders turn what you can see and what you can't into descriptions, a deliberately weak predictor guesses one from the other, and the loss never touches a pixel.

Two witnesses graded on whether they agree can just agree to say "a person, probably" about everything. Zero loss, global minimum, nothing learned.

Worth it. V-JEPA 2 gets 77.3% on Something-Something v2 with a frozen backbone, against InternVideo2's 69.7. Freeze that encoder, post-train an action-conditioned predictor on under 62 hours of robot video, and a Franka arm in a lab it never trained on picks things up zero-shot. It plans in 16 seconds per action. Cosmos needs four minutes, because it has to draw pixels to think.

My read: the base model is not a world model. It answers "what's over there", not "what happens if I try this". Those 62 hours of action conditioning buy the name.

And the dragons. Collapse is still managed by superstition. An EMA teacher, a stop-gradient, a predictor kept weak on purpose, not one of them a proof. Pull out any one piece and training falls over, and nobody can say why the rest are enough.

Then in late 2025 somebody wrote down what a good description looks like, and brought a proof. That's part 2.

Part 1 on the blog:
https://cgnarendiran.github.io/blog/jepa-nobody-cares-about-the-wallpaper/

#JEPA #SelfSupervisedLearning #WorldModels #VideoUnderstanding #AI
@[Fast Code AI](urn:li:organization:70969206)
