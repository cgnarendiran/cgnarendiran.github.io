---
layout: post
title:  "Flux Models: The New Kid on the Generative Block - Part 1"
date:   2024-11-15
image:  images/blog14/cover.png
tags:  flux generative-ai diffusion flow-matching transformers image-generation
---
*On the cover: An AI-generated image of flowing light streams representing the concept of Flux models*

Remember when we were all amazed by diffusion models like DALL-E, Midjourney, and Stable Diffusion? Well, there's a new kid on the block that's making waves in the generative AI community - Flux models. Developed by [Black Forest Labs](https://blackforestlabs.ai/) (founded by the original creators of Stable Diffusion), these models represent a significant leap forward in image generation capabilities. In this two-part post, I'll dive into what makes Flux models special, how they work under the hood, and why they might just be the future of generative AI.

## What are Flux Models?

Flux models are a new class of generative AI models that combine transformer architectures with flow matching techniques to create high-quality images from text prompts. The flagship model, Flux.1, comes in three variants:

- **Flux.1 Pro**: The highest-quality model intended for professional use (12 billion parameters)
- **Flux.1 Dev**: A faster model with guidance distillation, available as an open model
- **Flux.1 Schnell**: An ultra-fast model that generates images in just 1-4 sampling steps

What sets Flux apart from its predecessors is its hybrid architecture that combines multimodal and parallel diffusion transformer blocks, scaled up to a massive 12 billion parameters. For comparison, Stable Diffusion XL has about 3.5 billion parameters, and the original SD 1.5 has less than 1 billion. In the world of generative AI, size does matter!

To understand Flux models, we need to take a step back and look at the evolution from diffusion models to flow matching. Don't worry, I'll try to make the math as painless as possible (though a little pain is necessary for growth, isn't it?).

## The Diffusion Process Revisited

Diffusion models are rooted in non-equilibrium thermodynamics and can be understood through the lens of probability theory. At their core, they define a Markov chain that gradually transforms a complex data distribution into a simple, tractable one (typically Gaussian noise).

Let's start with the basics. Given a data distribution $p_{\text{data}}(x_0)$, diffusion models define a forward process that gradually adds noise to the data over $T$ timesteps:

$$
q(x_t|x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t}x_{t-1}, \beta_t\mathbf{I})
$$

where $\beta_t \in (0,1)$ is a variance schedule that controls the noise level at each step. Due to the Markov property and Gaussian nature of the transitions, we can directly write:

$$
q(x_t|x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t}x_0, (1-\bar{\alpha}_t)\mathbf{I})
$$

This process can be reparameterized to sample $x_t$ directly from $x_0$ using:

$$
x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon
$$

where $\alpha_t = 1-\beta_t$, $\bar{\alpha_t} = \prod_{s=0}^t \alpha_s$ and $\epsilon \sim \mathcal{N}(0, \mathbf{I})$.

In the continuous limit as $T \rightarrow \infty$, this discrete process converges to a stochastic differential equation (SDE):

$$
\frac{dx}{dt} = f(t)x_t + g(t) \frac{dw}{dt}
$$

where $f(t)$ and $g(t)$ are scalar functions of time, and $dw$ is a Wiener process (fancy term for Brownian motion). For the standard diffusion process, $f(t) = -\frac{1}{2}\beta(t)$ and $g(t) = \sqrt{\beta(t)}$.

The beauty of this formulation is that it gives us a continuous view of the diffusion process. Instead of thinking about discrete steps of noise addition, we can view it as a smooth, continuous transformation where our data simultaneously fades and becomes more noisy until it eventually turns into pure Gaussian noise.

The reverse process, which is what we use for generation, is given by:

$$
\frac{dx}{dt} = f(t)x_t - \frac{g^2(t)}{2}\nabla_{x_t}\log p_t(x_t) + g(t)\frac{d\bar{w}}{dt}
$$

Here, $\nabla_{x_t}\log p_t(x_t)$ is the score function and $d\bar{w}$ is a reverse-time Wiener process.

This equation might look intimidating, but it comes from a fundamental result in stochastic calculus called "time reversal of SDEs". The score function $\nabla_{x_t}\log p_t(x_t)$ points towards regions of high probability. Think of it like this: if the forward process is like slowly stirring cream into coffee, the reverse process needs to know both how to "unstir" (the drift term) and where the cream originally was (the score term).

#### The Score Function: The Heart of Diffusion Models

The score function $\nabla_{x}\log p(x)$ is the gradient of the log probability density with respect to the input. Intuitively, it points in the direction of increasing probability density - telling us which way to move to reach more likely data points. It's a fundamental concept in score-based generative models.

For diffusion models, we need to estimate $\nabla_{x_t}\log p_t(x_t)$ for all timesteps $t$. Since we don't have direct access to $p_t(x_t)$, we train a neural network $s_\theta(x_t, t)$ to approximate this score function.

The score function has this relation with the noise:

$$
\nabla_{x_t}\log p_t(x_t) = \mathbb{E}_{x_0|x_t}[\nabla{x_t}\log q(x_t|x_0)] = -\frac{\epsilon}{\sqrt{1-\bar{\alpha}t}}
$$


The training objective is derived from score matching and can be simplified to:

$$
\mathcal{L}_{DM}(\theta) = \mathbb{E}_{t \sim \mathcal{U}(0,1), x_0 \sim p_{\text{data}}, \epsilon \sim \mathcal{N}(0,\mathbf{I})}\left[\left\|s_\theta(x_t, t) - \left(-\frac{\epsilon}{\sqrt{1-\alpha_t}}\right)\right\|^2\right]
$$

This is equivalent to predicting the noise $\epsilon$ that was added to create $x_t$ from $x_0$. In practice, most diffusion models are trained to predict this noise directly, which is mathematically equivalent to score matching.

During sampling, we start with pure noise $x_T \sim \mathcal{N}(0, \mathbf{I})$ and iteratively apply:

$$
x_{t-1} = \frac{1}{\sqrt{1-\beta_t}}\left(x_t - \frac{\beta_t}{\sqrt{1-\alpha_t}}s_\theta(x_t, t)\right) + \sigma_t z
$$

where $z \sim \mathcal{N}(0, \mathbf{I})$ and $\sigma_t$ controls the stochasticity of the reverse process. This gradually transforms noise into a sample from the data distribution.

## Enter Flow Matching

Flow matching takes a different approach. Instead of thinking about adding and removing noise, it views the process as a continuous transformation from a simple distribution (like Gaussian noise) to the complex data distribution. The key insight is that we can define a deterministic path between noise and data.

Flow matching builds on the theory of continuous normalizing flows (CNFs), which model the transformation between probability distributions using deterministic flows governed by ordinary differential equations (ODEs). 

Let's denote our data distribution as $p_{\text{data}}(x_0)$ and our noise distribution as $p_{\text{noise}}(x_1)$, where $x_1 \sim \mathcal{N}(0, \mathbf{I})$ (it was $\epsilon$ in diffusion theory above, it's the same thing). The goal is to find a continuous path $\{p_t(x_t)\}_{t \in [0,1]}$ that smoothly interpolates between these distributions.

In flow matching, we define a deterministic path between a data point $x_0$ and a noise sample $x_1$ as:

$$
x_t = (1-t)x_0 + tx_1
$$

where $t \in [0,1]$ is the time parameter. This is a simple linear interpolation, but it defines a valid transport plan between the distributions. Note that in diffusion models (DDPM) this was:

$$
x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}x_1
$$

The velocity or "flow" along this path is given by the time derivative:

$$
\frac{dx_t}{dt} = v_t(x_t) = x_1 - x_0
$$

This velocity field $v_t(x_t)$ is what we aim to learn with our neural network. Note that unlike in diffusion models where we learn the score function $\nabla_{x_t}\log p_t(x_t)$, here we directly learn the velocity field.

#### The Conditional Flow Matching Objective

To train our model, we need pairs of $(x_0, x_1)$ where $x_0 \sim p_{\text{data}}$ and $x_1 \sim \mathcal{N}(0, \mathbf{I})$. For each pair, we can compute $x_t$ for any $t \in [0,1]$ and the corresponding target velocity $v_t(x_t) = x_1 - x_0$.

The loss function for flow matching is:

$$
\mathcal{L}_{FM}(\theta) = \mathbb{E}_{t \sim \mathcal{U}(0,1), x_0 \sim p_{\text{data}}, x_1 \sim \mathcal{N}(0,\mathbf{I})}\left[\left\|v_{\theta}(x_t, t) - (x_1 - x_0)\right\|^2\right]
$$

This is a simple mean squared error between the predicted velocity and the target velocity. The elegance of this approach lies in its simplicity - we're directly learning the vector field that transforms our distributions.

#### Sampling via ODE Solving

Once trained, we can generate samples by solving the ODE:

$$
\frac{dx_t}{dt} = v_\theta(x_t, t)
$$

To generate an image $x_0$, we:
1. Sample noise $x_1 \sim \mathcal{N}(0, \mathbf{I})$
2. Solve the ODE from $t=1$ to $t=0$ to get:
   $$x_0 = x_1 - \int_0^1 v_\theta(x_t, t)dt$$

In practice, we solve this integral numerically by dividing the time interval $[0,1]$ into $N$ steps (e.g., $N=4$ for Flux.1 Schnell). Using Euler's method:

1. Set step size $\Delta t = 1/N$
2. Initialize $x_1$ as random noise
3. For $i = 1$ to $N$:
   $$x_{t_i-\Delta t} = x_{t_i} - v_\theta(x_{t_i}, t_i) \cdot \Delta t$$
4. The final $x_0$ is our generated image

More accurate methods like Heun's or Runge-Kutta can be used, but Flux models are designed to work well even with simple Euler steps. The key advantage over diffusion models is that this process:
- Is deterministic (no added noise during sampling)
- Uses straight paths (fewer steps needed)
- Can use larger step sizes (faster generation)

This is why Flux.1 Schnell can generate high-quality images in as few as 4 steps, while diffusion models typically need 20-50 steps.

#### Relationship to Diffusion Models

Interestingly, there's a deep connection between flow matching and diffusion models. The probability flow ODE of a diffusion model:

$$
\frac{dx_t}{dt} = f(t)x_t - \frac{g^2(t)}{2}\nabla_{x_t}\log p_t(x_t)
$$

is a special case of the general flow matching framework. The difference is that in diffusion models, this ODE is derived from a stochastic process, while in flow matching, we directly parameterize and learn the ODE.

This connection helps explain why flow matching models can be more efficient - they cut out the "middleman" of the stochastic process and directly learn the deterministic path between distributions.

## Rectified Flow: The Secret Sauce

One of the key innovations in Flux models is the use of "rectified flow," which aims to make the paths from noise to data as straight as possible. This is achieved through a process called "path straightening" or "rectification."

While flow matching provides a framework for learning deterministic paths between distributions, rectified flow specifically focuses on finding the *optimal* paths. In the context of generative modeling, we want paths that:

1. Accurately transform between the noise and data distributions
2. Require minimal computational effort to traverse during sampling

From the theory of optimal transport, we know that the most efficient path between two points in Euclidean space is a straight line. Rectified flow extends this intuition to the space of probability distributions.

![alt](/images/blog14/lemme-get-this-straight.gif){: .center-image }
*Figure 1: Lemme get this straight - meme from Joker*

#### Mathematical Formulation

Formally, rectified flow seeks to find a coupling between the data distribution $p_{\text{data}}(x_0)$ and the noise distribution $p_{\text{noise}}(x_1)$ that minimizes the expected path length. The key idea is to find the best way to pair data points ($x_0$) with noise points ($x_1$) so that the path between them is as efficient as possible. $p(x_0, x_1)$ is called a "coupling"

$$
\min_{p(x_0, x_1)} \mathbb{E}_{(x_0, x_1) \sim p(x_0, x_1)}\left[\int_0^1 \left\|\frac{d}{dt}x_t\right\|^2 dt\right]
$$

where $x_t = (1-t)x_0 + tx_1$ is the linear interpolation path between the paired points. The optimal solution is the one that makes the paths as straight as possible in the probability space.

#### Training with Rectified Flow

To train a model with rectified flow, we use an iterative process:

1. Start with an initial coupling between $p_{\text{data}}(x_0)$ and $p_{\text{noise}}(x_1)$
2. Train a velocity field model $v_\theta(x_t, t)$ to match the current coupling
3. Use the trained model to generate new samples and update the coupling
4. Repeat steps 2-3 until convergence

The loss function for training the velocity field is similar to flow matching:

$$
\mathcal{L}_{RF}(\theta) = \mathbb{E}_{t \sim \mathcal{U}(0,1), (x_0, x_1) \sim p(x_0, x_1)}\left[\left\|v_{\theta}(x_t, t) - (x_1 - x_0)\right\|^2\right]
$$

The key difference is that the coupling $p(x_0, x_1)$ is iteratively refined to make the paths straighter.

#### Sampling Efficiency

The primary benefit of rectified flow is sampling efficiency. Because the paths are optimized to be as straight as possible, we can use much larger step sizes when solving the ODE:

$$
\frac{dx_t}{dt} = v_\theta(x_t, t)
$$

In practice, this means we can generate high-quality samples with as few as 1-4 steps using a simple Euler solver:

$$
x_{t-\Delta t} = x_t - v_\theta(x_t, t) \cdot \Delta t
$$

where $\Delta t$ can be much larger than in traditional flow matching or diffusion models.

This dramatic reduction in sampling steps is what enables Flux models, particularly the Schnell variant, to generate images so quickly while maintaining high quality. It's the mathematical equivalent of finding a shortcut through a complex landscape - why follow a winding path when you can go straight from A to B?

Stay tuned for Part 2, where we'll continue our exploration of these fascinating models and their potential to reshape the generative AI landscape!

## References

1. [Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) - The foundational paper behind Flux models
2. [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) - Key paper on flow matching techniques
3. [Rectified Flow: A Marginal Preserving Approach to Optimal Transport](https://arxiv.org/abs/2209.14577) - Paper on rectified flow methods
4. [Stable Diffusion 3.5 vs. Flux](https://modal.com/blog/best-text-to-image-model-article) - Comparison of the two models
5. [FLUX.1 vs Stable Diffusion: AI Text to Image Models Comparison](https://getimg.ai/blog/flux-1-vs-stable-diffusion-ai-text-to-image-models-comparison) - Detailed comparison with examples 