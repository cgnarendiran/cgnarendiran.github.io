---
layout: post
title:  "Cross Entropy Loss"
date:   2025-10-13
image:  images/blog24/cover.jpg
tags:  Cross Entropy Loss Information Theory KL Divergence
---
*On the cover: Cross Entropy Loss*

Cross Entropy Loss is a loss function that is used to measure the difference between the predicted probability distribution and the true probability distribution. It is a measure of the uncertainty of the model's predictions.

That just sounds like a bunch of jargon doesn't it. Well, let's break it down. All of this is rooted in Information Theory. Claude Shannon-who essentially invented the entire field of information theory-asked a deceptively simple question:

> **“How do we measure information in a way that makes sense?”**

He proposed three axioms for an information measure (H(p)):

### **Shannon’s Axioms**

1. **Continuity**
   (H(p)) should change smoothly as probabilities change.

2. **Maximization**
   For a fixed number of outcomes, entropy is maximized when all outcomes are equally likely.
   (A perfectly fair die is the most chaotic die.)

3. **Additivity (a.k.a. the “Chain Rule”)**
   If a decision can be broken into independent parts, total entropy is the weighted sum of entropies.
   [
   H(X, Y) = H(X) + H(Y|X)
   ]

Shannon proved that the **only** function satisfying these axioms (up to a constant factor) is:

[
H(p_1,\dots,p_n) = -K \sum_i p_i \log p_i
]

Set (K = 1) and we get the familiar form.

---

# 🔥 2. Self-Information: Surprise in a Single Number

Shannon also defined the information content of a single event:

[
I(x) = -\log p(x)
]

Properties:

* When (p(x)) is small → big surprise
* When (p(x)) is large → small surprise
* When (p(x) = 1) → (I(x) = 0) (no surprise)

Example:
Your friend says “gravity still works today.”
Probability = 1.
Surprise = 0 bits.

Your friend says “the stock market went up because Mercury is in retrograde.”
Surprise = ∞ bits.

---

# 🔥 3. Entropy: Expected Surprise

Entropy measures the *average* amount of self-information:

[
H(p) = \mathbb{E}_{x \sim p}[ -\log p(x) ]
]
[
H(p) = -\sum_x p(x) \log p(x)
]

Alternative continuous form:

[
H(p) = -\int p(x) \log p(x), dx
]

Entropy reflects how uncertain the world is.

* High entropy → chaotic, unpredictable
* Low entropy → predictable, boring (like a model that always predicts “cat”)

---

# 🥊 4. Cross Entropy: When Your Beliefs Are Wrong

Cross entropy is:

[
H(p, q) = -\sum_x p(x) \log q(x)
]

Compare with entropy:

[
H(p) = -\sum_x p(x) \log p(x)
]

Interpretation:

> **“How many bits do I need to encode messages drawn from (p) if I assume the world is (q)?”**

This is exactly what we do in machine learning:

* (p) = true labels
* (q) = model’s predicted distribution

For one-hot labels, if true class is (y):

[
H(p,q) = - \log q(y)
]

This is the famous per-sample classification loss.

---

# 💣 5. Negative Log-Likelihood (NLL): The ML Version

Likelihood for a sample (x):

[
\mathcal{L} = q(x)
]

Negative log-likelihood loss:

[
\text{NLL} = -\log q(x)
]

Averaged over the dataset:

[
\frac{1}{N} \sum_{i=1}^N -\log q(x_i)
]

This is **exactly** the empirical cross entropy:

[
H_{\text{empirical}}(p, q)
]

Why log?

* Turns products into sums
* Penalizes confident wrong predictions heavily
* Leads to convex/log-concave objectives (nice gradients)
* Sine/cosine would oscillate and destroy the loss landscape (and your model)

---

# 🧩 6. KL Divergence: Distance Between Belief Systems

Defined as:

[
D_{\text{KL}}(p,||,q) = \sum_x p(x) \log \frac{p(x)}{q(x)}
]

Equivalent form:

[
D_{\text{KL}}(p,||,q) = H(p, q) - H(p)
]

Interpretation:

> **Extra surprise caused by using the wrong model (q)**

Properties:

* (D_{\text{KL}} \ge 0)
* (D_{\text{KL}}(p||q) = 0) only when (p = q)
* Not symmetric:
  [
  D_{\text{KL}}(p||q) \neq D_{\text{KL}}(q||p)
  ]

KL divergence is everywhere:

* Variational inference
* Regularization in VAEs
* Policy updates in RL (Trust Region methods)
* Comparing distributions
* Aligning model predictions with truth

---

# 🎯 7. Importance Sampling: When Rare Events Refuse to Show Up

Suppose you want to estimate:

[
\mu = \mathbb{E}_{x \sim p}[f(x)]
]

But sampling from (p) rarely hits the events that matter (e.g., finance tail losses).

Rewrite expectation using another distribution (q):

[
\mu = \int f(x) p(x) , dx
]

Multiply & divide by (q(x)):

[
\mu = \int f(x) \frac{p(x)}{q(x)} q(x), dx
]

Now sample from (q):

[
\hat{\mu} = \frac{1}{N} \sum_{i=1}^N f(x_i), w(x_i)
]

where
[
w(x) = \frac{p(x)}{q(x)}
]
is the **importance weight**.

Interpretation:

> You sample from a convenient distribution (q)
> and then “fix” the bias using the ratio (p/q).

### Example: Rare Events in Finance

Want the probability of a 5-sigma loss:

* Sampling from the real distribution won’t give you enough 5-sigma events
* You choose a biased distribution that produces more extreme returns
* Apply importance weights to correct the bias
* Estimator now converges with far fewer samples

Importance sampling is basically:

> **“Cheat smartly, and then correct the cheat mathematically.”**

---

# 🔗 8. Deep Connections

All these concepts are unified:

* **Self-information**: surprise of one event
* **Entropy**: expected surprise under true distribution
* **Cross entropy**: expected surprise under model distribution
* **NLL**: empirical cross entropy
* **KL divergence**: the price you pay for being wrong
* **Importance sampling**: fixing the price by reweighting surprise

The common thread?
They all revolve around:

[
-\log(\text{probability})
]

This quantity is the currency of information.

