---
layout: post
title:  "Artificial Intelligence: Doomsday or Breakthrough - Part 2"
date:   2017-08-15
image:  images/blog2/cover.jpg
tags:  Artificial Intelligence AI doomsday breakthrough singularity reinforcement learning openai exmachina turing test convolutionals neural networks
---
This post is a continuation of part one: [READ PART 1 HERE][part1]

Spoilers Ahead: One of the best portrayals of AI is the movie 'Ex Machina' in which the humanoid robot 'Ava' (in the cover picture) turns rogue to escape the 'prison' built by its creator Nathan, a genius coder, billionaire and founder of BlueBook (set to mimic Google). In the movie, Nathan invites Caleb (a loner, best coder and closely monitored 'chosen' fellow from BlueBook office) to perform the famous Turing Test[^1] and determine whether Ava demonstrates true AI capabilities. Caleb soon gets attracted to Ava during those Turing test interactions. He also learns from Ava that Nathan is trying to experiment with humanoid bots and eventually going to kill Ava for a better version. When confronted, Nathan says that Ava has only pretended to like Caleb, exploiting his vulnerabilities to escape the confinement and this ability of deception to achieve freedom, is what makes Ava remarkably better than the previous Androids that he created. Although it is fairly difficult to comprehend the possibility of such a self-aware robot, it is interesting to think about. If you don't get creeped out by a non-organic adaptive robot capable of learning and perhaps even better at manipulation than humans, then this movie is definitely worth watching.

![ex-machina-1](/images/blog2/1.jpg)
*Image Courtesy: Photographer REX. In photo: My favorite scene where Nathan shows Caleb the structured gel. In his words, "to get away from circuitry I needed something that rearranges on a molecular level but retain the form when required" most likely to mimic human brain"*

Our brain is a result of millions of years of evolution seeking perfection in tasks that we specialise. For instance, our vision accounts for two-thirds of the electrical activity of the brain — a full 2 billion of the 3 billion neurons firings per second. Since our ancestors are arboreal (trees as habitat), one wrong calculation of placement of that branch or depth of that tree trunk would have been devastating on that failed jump. So intense natural selection was at play. Because of this, we have developed highly refined stereo vision and it is said that we can identify more than 10 million colours. Now, where do computers stand in this regard? It is true that CNNs (Convolutional Neural Networks - used to predict the content of an image) have reached state of the art, thanks to the advent of graphics cards to crunch those heavy pixel numbers from image feed.

But evidence suggests that Deep CNNs are processing images differently than humans and are prone to miscalculations. In fact, it is pretty easy to fool a CNN to make it believe that a particular image contains, say an ostrich when it is obviously not the case.

![iitm1](/images/blog2/2.png)
*Image Courtesy: Deep Learning Lectures by Prof. Mitesh Khapra CSE department IITM*

Instead of maximizing the log-likelihood of the correct class (in this case 'bus') we maximize it over an incorrect class ('ostrich') and backpropagate the error to the input image. With minimal changes to the input image, CNN predicts that the current image is now an ostrich.

![iitm2](/images/blog2/3.jpg)
*Image Courtesy: Deep Learning Lectures by Prof. Mitesh Khapra CSE department IITM*

In the above set of images, adding the transition image pixels in the middle to the set image on the left, produces the corresponding images on the right. CNN now predicts and is 99 percent sure that there is an ostrich for all images on the right, which any human can confirm that it's false. This shows that there is something else at play in how we human process an image; it is intuitive, immune to errors and powerful2.

All these are compiled as an insiders' perspective of how AI is either grossly underestimated or overestimated. So next time you see a statement from Elon Musk saying World War 3 would be sparked by competition of countries seeking superiority in AI, please rethink. We are indeed closer to Artificial General Intelligence now more than ever in the past. But we still need to travel a long way. What we could possibly worry about now is how regulations are developed for specific AI systems like self-driving cars. Drafting new road rules and ethical issues sit on top of this list. This is very similar to how we fought for net neutrality recently which is a very apt example of how technology has to be regulated.  Our generation is probably one of the most luckiest to behold a revolution which is unique and challenging. We are living in an age where websites ask us to confirm that we are not a robot. What a time to be alive!

[^1]: Turing Test: Developed by the revolutionary Mathematician Alan Turing in 1950 who claimed a method to test machines which articulate intelligence to speak with a human. And given the responses are close to how a human would respond and the tester is not able to distinguish the responses from a computer to a human being, then the machine is said to be intelligent and to have 'passed' the test. Turing test is outdated now but newer versions of these kind of tests have been proposed.
Although vision is a separate domain on its own and needs just DL still it comes across as an important capabilities of an AI system.  

[part1]: /2017/08/12/ai-doomsday-or-breakthrough-part1/