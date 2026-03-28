---
layout: post
title:  "VLMs - Pixels to Tokens"
date:   2025-12-09
image:  images/blog26/cover.png
tags:  Tokens Pixels Vision Language Models Computer Vision
---
*On the cover: Pixels to tokens*

In our [last post](https://cgnarendiran.github.io/blog/vit-pixels-to-tokens/), we spoke about how the **Vision Transformer (ViT)** took the candy away from CNNs. We learned that if you slice an image into patches and flatten them, you can treat an image just like a sentence. And a sequence of pixel-patches becomes a sequence of tokens.

This enables the ViT to look at an image and output a label `class_id: 284` ("Siamese Cat"). All this is good, but while ViTs taught computers to "read" images, they are still essentially mute. 

Meanwhile, in the building next door, NLP scientists were using Large Language Models (LLMs) like GPT-3 were writing poetry and coding in Python. But they were blind. They had never seen a sunset, only read descriptions of one.

The obvious question asked by researchers around 2021 was: **"We have a model that understands vision (ViT) and a model that understands language (LLM). What happens if we introduce them to each other?"**

Welcome to the era of **Vision-Language Models (VLMs)**. This is the story of how AI learned to see and speak at the same time.

## The Problem: The Tower of Babel

You might think, "Just glue the ViT to the LLM and be done with it."

It’s not that simple. Even though both models use the Transformer architecture, they speak completely different mathematical languages.

* **The ViT** spits out vectors that represent edges, textures, and shapes.
* **The LLM** spits out vectors that represent grammar, logic, and vocabulary.

If you feed ViT output directly into an LLM, it looks like gibberish. It’s like trying to plug a Nintendo cartridge into a toaster. We needed a "Rosetta Stone"—a way to align these two worlds.

## The Matchmaker (CLIP)

Before we could get models to *chat* about images, we had to get them to *agree* on what images were. The breakthrough came from OpenAI in 2021 with [CLIP: Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020).

CLIP (Contrastive Language-Image Pretraining) wasn't built to generate text. It played a massive game of "Match the Caption."

Imagine you have a batch of N images and N text captions.

1. Run images through an Image Encoder (like a ViT).
2. Run texts through a Text Encoder (like a mini-BERT).
3. **The Goal:** The model must figure out which text belongs to which image.

Mathematically, it maximizes the **dot product** (similarity) between the correct image-text pairs and minimizes it for the incorrect ones. This forces the model to learn a **shared embedding space**. Essentially,

$$
\frac{e^{\text{similarity score of a correct pair}}}{\sum_{\text{all pairs}}e^{\text{similarity score of pairs}}}
$$

specifically,

$$
\mathbb{L} =
\sum_{i=1}^{|\mathbb{B}|}
\log
\frac{e^{x_i^\top y_i / \tau}}
{\sum_{j=1}^{|\mathbb{B}|} e^{x_i^\top y_j / \tau}}
+
\sum_{i=1}^{|\mathbb{B}|}
\log
\frac{e^{x_i^\top y_i / \tau}}
{\sum_{j=1}^{|\mathbb{B}|} e^{x_j^\top y_i / \tau}}

$$

where $x_i$ is an image feature vector and $y_j$ is a text feature vector, $\mathbb{B}$ is the mini-batch size of images and texts, and $\tau$ is a temperature parameter.

The loss is computed twice, one for every image and one for every text.

* Image -> Text
* Text -> Image

Softmax forces every image to compete against *all other texts in the batch*.

![alt](/images/blog26/clip.png){: .center-image }
*Figure 1: CLIP architecture. Source: [CLIP paper](https://arxiv.org/abs/2103.00020)*


Thanks to CLIP, the vector for "cat" (text) and the vector for a picture of a cat (image) pointed in the same direction. The barrier between image and language was broken.

## A better Matchmaker (SigLIP)

CLIP had one major issue. Imagine for a given image there are multiple captions that are relevant:

* "A dog running"
* "A corgi in a park"
* "A small brown dog outdoors"

Softmax assumes **only one is correct within the batch**. That normalization term:

$$
\sum_{j=1}^{|\mathbb{B}|} e^{x_i^\top y_j}
$$

forces captions to compete with each other.

If two captions are semantically similar (dog vs corgi), they *hurt each other’s probability*. The batch becomes a zero-sum game.

This leads to three problems:

* You need carefully curated batches
* You need very large batch sizes
* You must compute the loss twice

Sigmoid Loss for Language-Image Pre-Training (SigLIP) from Google Research asks a radically simpler question:

Instead of “Which caption in this batch matches this image?”
Why not ask: “Does this image match this caption — yes or no?”

Softmax -> Sigmoid

Instead of multi-class classification over the batch, SigLIP treats every image-text pair as a **binary classification problem**.

$$
\mathbb{L}_{ij}
=
y_{ij} \log \sigma(x_i^\top y_j)
+
(1 - y_{ij}) \log (1 - \sigma(x_i^\top y_j))
$$

Where:

* $y_{ij} = 1$ if image $i$ matches text $j$
* $y_{ij} = 0$ otherwise
* $\sigma(\cdot)$ is the sigmoid function


But here’s the twist. Even SigLIP is still a two-tower model.

CLIP and SigLIP both learn:

“This whole image matches that whole sentence.”

It does NOT learn: “This part of the image explains this part of the sentence.”

No token-level interaction. No compositional reasoning. No step-by-step grounding. Two towers. No bridge. Which brings us to actual conversational/generative VLMs.

## The Conversationalist (LLaVA & Friends)

CLIP was great at matching, but it couldn't write you a poem about a salad. To do that, we needed **Generative VLMs**. This generation of models used cross-attention to fuse modalities inside Transformers.

The current standard architecture (popularized by models like [LLaVA](https://arxiv.org/abs/2304.08485)—Large Language and Vision Assistant) is quite simple. It’s essentially a "Frankenstein" model stitched together from three parts:

$$
Tokens_{vision} = P(V(I))
Tokens_{text} = E(T)
Output = LLM(Tokens_{vision}; Tokens_{text})
$$

Where:

* $V(I)$ = Vision encoder
* $P$ = Projection layer
* $E(T)$ = Tokenizer + Embeddings
* $LLM$ = Language decoder

So essentially,

* The Eyes (Vision Encoder)
We take a pre-trained Vision Transformer (usually CLIP’s vision encoder or Google’s SigLIP). We pass the image through it to get those "patch tokens" we discussed in the last blog. *Status during training:* Usually **Frozen** (we don't want to break the eyes).

* The Brain (The LLM)
We take a pre-trained LLM (like Vicuna, Llama 3, or Mistral). This provides the reasoning, grammar, and world knowledge. *Status during training:* **Frozen** initially, then **Fine-tuned** later.

* The Translator (The Projector)
This is the magic glue. The output of the Vision Encoder might have a dimension of 1024, but the LLM expects an input dimension of 4096. We insert a simple **Linear Projection Layer** (or a small MLP) that translates "Visualspeak" into "LLMspeak."

* The Flow:
We concatenate these visual tokens with text tokens. The LLM takes this combined sequence and just predicts the next token, exactly like it always does. It doesn't even know it's "seeing" an image; it just thinks it's reading a very strange language that happens to describe a visual scene perfectly.

### Cross-Attention Mechanism

Given:
* Text queries (Q_T)
* Image keys/values (K_I, V_I)

We compute:

$$
\text{Attn}(Q_T, K_I, V_I) = 
\text{softmax}\left(
\frac{Q_T K_I^T}{\sqrt{d}}
\right)V_I
$$

Now text tokens attend directly to visual tokens. Language can “look” at pixels. This is multimodal grounding part. If you look at the LLaVA paper, you’ll see the training is split into two distinct stages. This is crucial for stability.

### Stage 1: Vision Pre-training

The goal of this stage is to teach the Vision Encoder to see the world. Using image-caption pairs (e.g., "A cat on a mat") as training data, only the **Vision Encoder** learns during this phase while the Projector and LLM remain frozen. As a result, the Vision Encoder learns to see the world.

### Stage 2: Vision Language Alignment

The goal of this stage is to teach the "Projector" to translate. Using simple image-caption pairs (e.g., "A cat on a mat") as training data, only the **Projector** learns during this phase while the Vision Encoder and LLM remain frozen. As a result, the LLM stops seeing the image tokens as noise and starts recognizing them as concepts.

### Stage 3: Visual Instruction Tuning

The goal of this stage is to teach the model to follow instructions and act like a chatbot. Using complex conversations as training data (e.g., *User:* "What is unusual about this image?" *Assistant:* "The man is ironing a sandwich, which is highly atypical..."), both the **Projector** and the **LLM** learn during this phase. As a result, the model can reason, count, and explain visual data.

## Why This Matters: The End of "Just Seeing"

We are moving away from specific tools. We used to have one model for "Is this a hotdog?" and another for "Read this receipt."

VLMs are generalist agents.

* You can show them a picture of your fridge and ask for recipes.
* You can show them a screenshot of code error logs and ask for a fix.
* You can show them a dashboard and ask for a summary of trends.

Why do VLMs scale so well? Because language is compressed human knowledge. Every caption encodes: Physics, Culture, Intent, Affordances, Causality. “A chair” is not pixels. It is: “Something you can sit on.” That’s functional semantics. VLMs learn affordances, not just appearances.

## The Evolution:

There were many variants of VLMs proposed in the research community. Each took a different approach to the same core problem: how to make vision and language work together.

**BLIP and BLIP-2** (Salesforce, 2022-2023) introduced the concept of a **Querying Transformer (Q-Former)** that sits between the frozen vision encoder and frozen LLM. Instead of directly projecting image tokens, the Q-Former learns a set of learnable query tokens that extract the most relevant visual features. This lightweight module (188M parameters) acts as an information bottleneck, compressing visual information while keeping both the vision encoder and LLM frozen. The result? You can swap different LLMs without retraining the entire model.

**Flamingo** (DeepMind, 2022) pioneered the idea of **interleaved multi-image inputs**. Rather than just handling one image at a time, Flamingo can process sequences like: "Here's photo 1, photo 2, and photo 3. What changed?" It introduced **Perceiver Resampler** modules and gated cross-attention layers that allow the LLM to attend to visual information only when needed. This architecture enabled few-shot learning—show it a couple of examples, and it adapts on the fly.

**GPT-4V and Gemini** (OpenAI & Google, 2023) marked the shift to **natively multimodal architectures**. Unlike the "stitched together" approach, these models were trained from scratch with vision and language interleaved from the beginning. The exact architectures remain proprietary, but the performance leap was clear: these models could handle complex spatial reasoning, read dense tables, and even solve geometry problems from textbook diagrams.

**LLaVA-NeXT and Variants** (2024) pushed the boundaries of open-source VLMs by introducing **dynamic high-resolution processing**. Instead of downsampling images to fixed sizes (like 336×336), these models use adaptive tiling—splitting high-res images into multiple crops and processing them in parallel. This allowed models to read small text in screenshots and understand fine-grained details that earlier VLMs would miss.

**DeepSeek-VL** (DeepSeek, 2024) introduced a hybrid vision encoder architecture that combines both **low-resolution semantic features** and **high-resolution detail features**. Instead of relying solely on a single ViT, DeepSeek-VL uses a dual-stream approach: a SigLIP encoder for semantic understanding and a SAM (Segment Anything Model) encoder for fine-grained visual details. This hybrid approach allowed the model to excel at both holistic scene understanding and precise visual grounding tasks, achieving competitive performance with significantly fewer training tokens compared to other open-source alternatives.

The common thread? The community moved from "frozen components glued together" toward **end-to-end trainable systems** that truly understand the interplay between pixels and words. We went from models that could match images to captions, to models that can debug your code by looking at an error screenshot.


## Conclusion

If the Vision Transformer was about turning images into words, the Vision-Language Model is about turning images into **dialogue**.

We have effectively given LLMs eyes. By simply projecting visual vectors into the language space, we tricked the text model into hallucinating a vision system. And it works beautifully.

The future isn't just "Computer Vision" anymore. It's **Multimodal AI**.

And now you know. Fin.

