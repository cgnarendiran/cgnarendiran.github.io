---
layout: post
title:  "Guided Diffusion Models - Part 1"
date:   2022-10-01
image:  images/blog10/cover.png
tags:  diffusion dalle midjourney imagen generation guidance ai vision
---
*On the cover: Midjourney's creation for the prompt "Astronauts exploring an alien red planet"*

Diffusion models are all the rage these days. Why do we need diffusion models? In fact, image generation is not new, we have GANs, VAEs, Flow models, etc. If you consider text-to-image generation, there are versions such as StackGAN, AttnGAN and VQ-VAE. But recently, diffusion models have taken the center-stage because of their high quality, high diversity and high fidelity (compliance to text prompts). Some of the popular diffusion models that has hit the news are:
- DALL-E2 (OpenAI)
- Imagen (Google Brain)
- Midjourney (independent company)
- Stable diffusion (StabilityAI)

In this 2 part blog post, we will take a look at the physical intiution, training and sampling of diffusion models, followed by the various guidance aspects. 

## Physical intuition
Diffusion is a well-defined physical process. Consider an ink droplet in a glass of water: it starts off with a unique shape (complex density distribution) when first dropped and it mixes down to the shapeless uniformity of water (uniform distribution). So we can think about diffusion as a process, where the structure of a substance get destroyed sequentially in time leading to just noise. 

![alt](/images/blog10/ink_in_water.jpg){: .center-image }
*Figure 1: Diffusion of ink droplet in a glass of water*

It is mathematically easy to represent the final uniform distribution, but much harder to represent the initial complex density distribution. Is it possible to start with the final uniform distribution and arrive at the initial density distribution? Well, the physical process of diffusion is irreversible, just as you could not spontaneously unbreak a glassware.

But it is possible to model this irreversible process through a neural network and we can learn the initial density distribution. How do we do that you ask? Well we can make use of this nice observation from the diffusion process: When you look at the ink droplet in water microscopically and for a small time period, the forward and reverse processes look exactly the same! If I ask you whether the gif below of diffusion of ink is forward in time or backwards, I bet that your guess is as good as a coin flip. We will make use of this nice property in our neural network.

![alt](/images/blog10/brownian_motion.gif){: .center-image }
*Figure 2: Brownian motion of particles in diffusion. Forwards and reverse in time is indistinguishable*

## What's underneath?
- During the forward diffusion process $q$, we take a good image $x_0$, destroy and add noise to it sequentially little by little to get isotropic (looks same in all directions) gaussian noise image $x_T$ ($t=0,1,2,...,T$)
- During the reverse diffusion process $p_\theta$ we use a neural network to transform from noise $x_T$ back to the original image $x_0$. 

We can see that the forward diffusion is a Gaussian noise addition process. Since we know that the forward and reverse process look the same, we can model the reverse process by a Gaussian as well! How neat. The mean and variance of this Gaussian can be obtained by transforming the input image $x_t$ by a neural network with parameters $\theta$. We use a Gaussian here instead of Uniform distribution since it is [more common](https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/VELDHUIZEN/node11.html) in imaging systems. Also, in these equations below, $\{\beta_t \in (0,1) \}^T_{t=1}$ is noise scheduling parameter that determines how much noise is added and how much destruction is happening.

![alt](/images/blog10/inner_working.png){: .center-image }
![alt](/images/blog10/inner_working1.png){: .center-image }
*Figure 3: Forward and reverse diffusion.*

## Tricks
There are couple of tricks to make the training and sampling of these models easier. Some of these are as follows:
- To get to a random timestep, need not sample repeatedly, use reparameterization. Essentially you can rewrite the noise scheduling parameter as follows: $\alpha_t = 1-\beta_t$ and $\bar{\alpha_t} = \prod_{s=0}^t \alpha_s$. This makes the forward diffusion $q(x_t \vert x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha_t}} x_0, (1 - \bar{\alpha_t}) \mathbf{I})$

- One can have various schedules for the diffusion parameter $\alpha_t$. Improved DDPM suggest using cosine-scheduling which provides near-linear drop in the middle of the training process and subtle changes around t=0 and t=T which we can see in the figures below. $\quad\bar{\alpha_t} = \frac{f(t)}{f(0)}\quad\text{where }f(t)=\cos\Big(\frac{t/3T+s}{1+s}\cdot\frac{\pi}{2}\Big)^2$
![alt](/images/blog10/beta_schedule.png){: .center-image }
![alt](/images/blog10/beta_schedule1.png){: .center-image }
*Figure 4: Beta schedule comparison for linear and cosine schedule*

- Predict the noise instead of the mean directly; they are equivalent. From the DDPM paper, “We have shown that the 𝞊-prediction parameterization both resembles Langevin dynamics and simplifies the diffusion model variational bound to an objective that resembles denoising score matching”. The relation between $\mu_\theta(x_t, t)$ and $\epsilon_\theta(x_t, t)$ is given as, $\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}} \Big(x_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha_t}}} \epsilon_\theta(x_t, t) \Big)$. Thus images can be sampled as follows by using the predicted noise: $x_{t-1} = \mathcal{N}(x_{t-1}; \frac{1}{\sqrt{\alpha_t}} \Big(x_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha_t}}} \epsilon_\theta(x_t, t) \Big), \Sigma_\theta(x_t, t))$

- Variance can be either fixed or learned; learned variance reduces number of timesteps during sampling. Improved DDPM propose to have a learned variance as follows by the model predicting a mixing vector $\mathbf{v}$: $\Sigma_\theta(x_t, t) = \exp(\mathbf{v} \log \beta_t + (1-\mathbf{v}) \log \tilde{\beta_t})$ where $\tilde{\beta_t} = \frac{1 - \bar{\alpha_{t-1}}}{1 - \bar{\alpha_t}} \cdot \beta_t$

## Training and Sampling
### Training
- Take an image $x_0$, sample $t ~ [1,T]$, destroy and add noise $\epsilon ~ \mathcal{N}(0,\boldsymbol{I})$ to it through the schedule $\alpha_t$ to get image $x_t$
- Train a model $\epsilon_\theta(x_t, t)$ (with say a U-Net architecture) given inputs of noisy image xt and timestep t, predicts the noise that was added
![alt](/images/blog10/training.png){: .center-image }
*Figure 5: Training process depiction*

### Sampling
- Start with random noise $x_T ~  \mathcal{N}(0,\boldsymbol{I})$ and use the model $\epsilon_\theta(x_t, t)$ to predict the noise 
- Convert the predicted noise $\epsilon_\theta(x_t, t)$ to mean $\mu_\theta(x_t, t)$
- Sample the previous image $x_{t-1}$ from the distribution $p_\theta(x_{t-1} \vert x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$
- Repeat from $t=T$ till $t=0$
![alt](/images/blog10/sampling.png){: .center-image }
*Figure 3: Sampling process depiction*

![alt](/images/blog10/algos.png){: .center-image }
*Figure 3: Training and sampling algorithms for diffusion models from DDPM*

The algorithms diagram above shows this process nicely. Alright, so far we have seen how to train a diffusion model and sample from it. If we sample from this trained model it will give use random samples. How do we get the model to give us say a picture of a Cute Cat Cthulu with tentacles instead of arms? In the next post we will look at guidance for diffusion models to achieve this. Stay tuned! :)

![alt](/images/blog10/cat_cthulu.webp){: .center-image }
*Figure 3: Cute Cat Cthulu generated from Midjourney*