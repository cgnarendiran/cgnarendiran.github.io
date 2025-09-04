---
layout: post
title:  "Markov Chain - The connection between Nuclear Bombs, Google Search, and Perplexity"
date:   2025-08-02
image:  images/blog21/cover.jpg
tags:  markov chain pagerank perplexity
---
*On the cover: Markov Chain*

Recently I watched this video by Veritasium talking about [Markov Chains](https://www.youtube.com/watch?v=KZeIEiBrT_w&ab_channel=Veritasium). I really liked the examples he used to explain the usage of Markov Chains, ranging from Nuclear Bombs to Google Search and Perplexity scores of LLMs. At first, comparing an Atom Bomb to Google Search might sound like the setup to a terrible joke—but in fact, they *do* share this wonderful mathematical lineage called **Markov Chains**. In the Manhattan Project, Stanislaw Ulam and John von Neumann used them to model neutron behavior in nuclear fission; Google’s PageRank models web navigation similarly—except with links instead of neutrons and a slightly friendlier ending. But what the video lacked is perhaps a detailed mathematical explanation of how PageRank works or the math behind Perplexity scores of LLMs. In this blog, I will try to explain the math behind PageRank and Perplexity scores of LLMs.

## PageRank: Google’s Markovian Math in Action

Let me take you deeper into the maze—starting from “random surfer” intuition, moving to matrices, and reaching the heart of the algorithm with math you can actually sink your teeth into.


### 1. The Random Surfer & Markov Chains

* **Basic idea**: Picture a “random surfer” on the internet. They click random links, but occasionally get bored and teleport to a completely new page.
* **Markovian nature**: The next page they choose depends *only* on what page they’re currently on—not their surfing history.

This is the essence of a **discrete-time Markov chain**—the same mathematical idea behind modeling neutrons in a fission process, but now repurposed for web pages.

### 2. Building the Google Matrix (a.k.a. G)

1. **Adjacency → Stochastic Matrix $S$**

   * Start with an adjacency matrix $A$ where $A_{ij} = 1$ if page *j* links to page *i*.
   * Convert it into a Markov (column-stochastic) matrix $S$ by dividing each column by the total outgoing links $k_j$.
   * For “dangling pages” (with no outgoing links), every entry in that column is replaced with $1/N$, ensuring no dead ends. ([Wikipedia][4])

2. **Teleportation (via damping factor $\alpha$)**

   * Define the Google matrix:

     $$
     G_{ij} = \alpha S_{ij} + (1 - \alpha) \frac{1}{N}
     $$
   * This means: with probability $\alpha$, follow an outgoing link; with probability $1-\alpha$, teleport to a random page. ([Wikipedia][4])

### 3. The Stationary Distribution: $\pi = G\pi$

The goal is to find the **stationary distribution** $\pi$, a probability vector satisfying:

$$
\pi = G \pi, \quad \sum_i \pi_i = 1
$$

* By the **Perron–Frobenius theorem**, because $G$ is positive, there exists a unique, positive $\pi$. ([Mathematics LibreTexts][2])
* Intuition: over time, the random surfer visits different pages according to probabilities in $\pi$. Pages with higher $\pi_i$ are *more important*.

### 4. Power Iteration: Getting $\pi$ in Practice

Rather than solving $(I - G)\pi = 0$ directly, PageRank uses **power iteration**:

1. Start with any initial distribution $\pi^{(0)}$ (e.g., uniform).
2. Iterate:

   $$
   \pi^{(t+1)} = G\,\pi^{(t)}
   $$
3. Repeat until $\pi^{(t+1)} \approx \pi^{(t)}$.

This converges to $\pi$ efficiently—even in massive graphs—thanks to the matrix’s sparsity and structure. ([Wikipedia][5], [math.umd.edu][6])

### 5. Worked-Out Mini Example

Suppose we have 4 pages (P1–P4). Page P1 links to none (dangling), P2 links to P3, P3 links to P2 and P4, and P4 links to P1.

1. Construct adjacency, fix dangling node.
2. Convert to $S$, then to $G$ with, say, $\alpha=0.85$.
3. Iterate power method:

   $$
   \pi^{(t+1)} = G\,\pi^{(t)}
   $$
4. Convergence yields a rank vector like $[0.04, 0.05, 0.47, 0.44]^T$. ([math.umd.edu][6])

We can rank pages by descending $\pi_i$—there’s your “Who gets to sit at the top of search results” math.

### 6. Why It Matters

* **Relevance vs. Importance**: PageRank provides a *query-independent* global measure of page authority, later combined with relevance signals (like keyword match, freshness, personalization) for ranking.
* **Variants galore**: Google uses multiple PageRank versions—topic-specific, personalized, maybe even “pagerank for kittens”—all rooted in the same Markov logic.

### 7. Visualizing PageRank

Here’s a conceptual illustration of the PageRank process as a Markov chain random walk:

[![commons.wikimedia.org/wi...](https://images.openai.com/thumbnails/url/wZ-sgnicu1mUUVJSUGylr5-al1xUWVCSmqJbkpRnoJdeXJJYkpmsl5yfq5-Zm5ieWmxfaAuUsXL0S7F0Tw4uLkzK961MTS4I83cPLMjO8PQvyMjXdS4N90lPziov9vHNzsvPTY30MCyzSHQ2KAjKS3d280o1KXNRKwYAAJkqXg)](https://commons.wikimedia.org/wiki/File%3APageRank_with_Markov_Chain.png?utm_source=chatgpt.com)

Each diagram helps show:

* Random transitions between pages
* Teleport jumps
* Influence flowing through linking structure

### Comments:

> “PageRank: the algorithm that models your browsing as one long, scrappy road trip—occasionally powered by links, sometimes by pure boredom.”

If the Manhattan Project mathematicians thought neutrons’ journeys were chaotic, Google’s random surfers show them how it’s done—with style.



## N-Gram Models: The Word-Level Markov Chains

If PageRank is Markov chains in the wild on the web, then **n-gram models** are Markov chains living in your text—predicting the next word based on the last few. It’s like your phone finishing your sentences… and often gets it wrong. Damn you, autocorrect!


### The N-Gram Formula

In an **n-gram model**, to predict the probability of a word $w_i$, we approximate:

$$
P(w_i \mid w_1, \dots, w_{i-1}) \approx P(w_i \mid w_{i-n+1}, \dots, w_{i-1})
$$

— this is the **Markov assumption** in action, limiting context to the last $n-1$ words. ([Wikipedia][1])

* **Bigram** (2-gram): Looks at just the previous word — e.g., $P(\text{"dog"} \mid \text{"the"})$
* **Trigram** (3-gram): Considers the last two words — e.g., $P(\text{"park"} \mid \text{"the", "big"})$ ([Wikipedia][2])


### Estimating Probabilities

We estimate probabilities using raw counts:

$$
P(w_i \mid \text{history}) = \frac{\text{Count}(\text{history}, w_i)}{\text{Count}(\text{history})}
$$

E.g., in a bigram model:

$$
P(\text{"rain"} \mid \text{"heavy"}) = \frac{\text{Count}(\text{"heavy rain"})}{\text{Count}(\text{"heavy"})}
$$

This is how your spellchecker knows “heavy rain” is more likely than “heavy reign.” ([devopedia.org][3], [Wikipedia][2])

### Handling Data Sparsity: Katz Back-off

Real-world text is messy—many n-grams never occur in your training data. Enter **Katz's back-off model**, a neat way to handle this:

$$
P_{bo}(w_i \mid \text{history})
=
\begin{cases}
\text{(MLE estimate)} & \text{if count > threshold} \\
\alpha \times P_{bo}(w_i \mid \text{shorter history}) & \text{otherwise}
\end{cases}
$$

This way, if “heavy fluffy rain” never appears in your data, you back off to “fluffy rain,” and if that’s missing—back to “rain.”  ([Wikipedia][4])

## Perplexity: How Confused Is the Model?

So your model can generate text—but how good is it? Enter **perplexity**, the metric that literally asks, “Just how perplexed are you, model?”

### What Does Perplexity Measure?

Perplexity quantifies a model’s **uncertainty** in predicting text. Formally:

$$
\mathrm{Perplexity}(W) = \exp\left(-\frac{1}{N}\sum_{i=1}^N \log P(w_i \mid \text{context})\right)
$$

Or equivalently, it’s the **median branching factor**—how many choices the model is considering on average for the next word. ([Wikipedia][5], [GeeksforGeeks][6], [Stanford University][7], [Fiveable][8])

### Why Perplexity Matters

* **Low perplexity**: The model is confident and accurate—like knowing your coffee before you even say it.
* **High perplexity**: The model stares at the screen in uncertainty (“Did they say Java or JavaScript?”).

It’s widely used to evaluate both n-gram and modern language models. For instance, a trigram model on the Brown corpus inherently had perplexity around **247 per word** — meaning it was as confused as facing 247 equally likely words at each step. ([Wikipedia][5])

### Perplexity in Practice

| Model Type        | Typical Perplexity     | Insight                                                        |
| ----------------- | ---------------------- | -------------------------------------------------------------- |
| **Unigram (n=1)** | Very high (e.g., 900+) | No context, very uncertain                                     |
| **Bigram**        | Lower (e.g., 170)      | Slightly better guesses                                        |
| **Trigram**       | Even lower (e.g., 109) | Context helps a lot ([Stanford University][7], [Wikipedia][5]) |

As you increase context (higher n), the model becomes sharper—until data sparsity bites and smoothing becomes critical.

### Perplexity: Not Perfect, But Useful

Perplexity doesn’t tell us if the model truly *understands*—just how confident it is. A model can be confidently wrong. Still, it’s quick, interpretable, and widely used:

* Reflects entropy – how “surprised” the model is on average ([Comet][9], [Medium][10], [Wikipedia][5])
* Easy to compute – perfect for tracking during training
* Partners well with other metrics for full evaluation (fluency, task accuracy) ([Comet][9])

## Final Wrap-up

> **Markov chains** let us predict the next click or word, forgetting the rest (because why hold grudges?)
> **N-gram models** use Markov assumptions to power autocomplete, speech recognition, and translation—with help from back-off magic when data runs dry.
> **Perplexity** is our way of measuring the model’s “WTF” moment—how lost it is when making predictions.

From hidden web walks to sentence puzzles, Markov chains remain the unsung heroes. Perplexity just whispers, “Nice try—but you could be less bewildered next time.”
