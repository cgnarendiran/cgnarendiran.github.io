---
layout: post
title:  "Hierarchical Navigable Small World (HNSW): How We Actually Find Needles in Vector Haystacks"
date:   2025-07-13
image:  images/blog19/cover.jpg
tags:  vector search hnsw
---
*On the cover: HNSW graph depiction*


Imagine you’ve just launched a custom LLM with RAG pipeline. A user comes in with a query, which you convert to an embedding $q$, and you need to find which of your **10 million vectors** is closest.

Sure, you *could* compare $q$ against every single vector. That’s called **brute force**. But unless your startup is secretly running on an infinite GPU budget… well, good luck with latency.


## Step 1: Nearest Neighbor (NN) Search

The textbook definition of **nearest neighbor** is simple:

$$
x^* = \arg\min_{x \in X} d(q, x)
$$

where $d(\cdot, \cdot)$ is your distance metric (say Euclidean).

The catch? Computing this exactly requires $O(n)$ distance evaluations.
For $n = 10^7$, that’s **10 million dot products per query**. Even a fast GPU will start sweating.


## Step 2: Approximate Nearest Neighbor (ANN)

Here comes the trick: instead of demanding the *absolute closest*, we settle for “close enough.”

Formally, ANN finds $\tilde{x}$ such that

$$
d(q, \tilde{x}) \leq (1+\epsilon) d(q, x^*)
$$

with high probability.

This trade-off is magical: we go from scanning **millions** to scanning maybe **thousands**, with almost no loss in recall.

If brute force is like **calling every pizza place in the city** to find the closest delivery, ANN is like **calling your 5 closest friends and asking which one delivers pizza fastest**. You still get fed — much quicker.


## Step 3: ANN with Graphs

One powerful way to do ANN is with **graphs**.

* Each vector = a node.
* Connect nodes to their nearest neighbors.
* To find neighbors of a query, you “walk the graph” instead of scanning everything.

But if we only connect close nodes, you risk getting trapped in a neighborhood. That’s where **small-world graphs** come in: sprinkle a few long-range edges, and suddenly you can jump across the dataset in just a few hops.

Think of it like a social network: your college friends are local edges, but that one LinkedIn connection in another continent is a long-range edge. That’s what makes the graph navigable.


## Step 4: Enter HNSW (Hierarchical Navigable Small World)

Now for the star of the show: **HNSW**.

It adds **two key ideas**:

1. **Hierarchy**: multiple layers of graphs. Top layers are sparse (long highways), bottom layers are dense (local streets).
2. **Greedy navigation**: at each layer, you keep walking to whichever neighbor is closest to your query. When you can’t get closer, you drop one layer down.

At the bottom, you don’t trust greed entirely — you keep a list of candidates (controlled by `efSearch`) to avoid getting stuck.

Result? Instead of millions of comparisons, you explore only a few thousand nodes.
Instead of $O(n)$, search cost behaves like $O(\log n)$.


## Step 5: Tuning the Knobs

* **M**: how many connections per node (graph density).
* **efConstruction**: how widely you search when inserting nodes (better graph quality).
* **efSearch**: how widely you search during queries (higher recall).

Bigger knobs → more accuracy, but more compute. It’s a trade-off buffet.


## Conclusion

Brute force NN is honest but slow. ANN is fast but approximate. HNSW? It’s the clever friend who **builds a multi-layer city map, sprinkles in shortcuts, and then guides you straight to the right coffee shop** — almost every time.

So the next time your vector database finds your nearest neighbor in milliseconds, remember: there’s a tiny greedy traveler sprinting down a small-world graph to make it happen.

