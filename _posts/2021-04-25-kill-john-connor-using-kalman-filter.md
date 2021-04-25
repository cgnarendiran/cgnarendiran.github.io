---
layout: post
title:  "Kill John Connor using Kalman filter"
date:   2021-04-25
image:  images/blog6/cover.jpg
tags:  kalman filter gaussian ai state estimate bayesian
---
*On the cover: T-X Terminator from Terminator3: Rise of the Machines (2003)*

Let's say you are the super hot T-X Terminator sent from the future by Skynet. You mission is to destroy a young John Connor who later on becomes the leader of the Resistance (booooo). You started your mission, took some damage, but fought off a relentless and annoying T-850 (Arnold Schwaznegger) and disabled it. However you see John Connor and his girlfriend Katherine trying to escape in a motorcycle. You are at the top of a bridge and see them getting away from you. Your long range weapons are damaged, hence you grab a shoulder-fired missile from the scene that has one missile left. You are now weapons hot and ready to engage but only with one shot. Ready to make it count? Let's do it!

The problem here is to track the motorcycle. Once tracked, it is fairly easy for you to aim and shoot. For tracking, let's say that you have to estimate the motorcycle's position $p_t$ and velocity $v_t$ at any point of time. You can also estimate other variables like acceleration (throttle that John uses) but let's keep it simple. Let's call this the **state** $\mathbf{x}_t$ of the system. You also need to track the **uncertainity** of your state $\mathbf{P}_t$ which is nothing but the covariance matrix.

$$
\begin{equation}
\begin{aligned} 
\mathbf{x}_t &= \begin{bmatrix} 
p_t\\ 
v_t
\end{bmatrix}
\\
\mathbf{P}_t &= \begin{bmatrix} 
\Sigma_{pp} & \Sigma_{pv} \\ 
\Sigma_{vp} & \Sigma_{vv}
\end{bmatrix} 
\end{aligned} 
\end{equation}
$$

Since $p_t$ and $v_t$ are uncorrelated at a time step $t$, the non-diagonal terms in the covaraince matrix are zero. 

You have at your disposal:
1. An inbuilt **physics-kinematics model** that predicts the current state of the motorcycle based on it's previous state
2. A **vision sensor** that measures the current state of the motorcycle, but gives noisy readings due to damage during the fight with T-850
3. A **GPS tracker** that tracks Katherine's cellphone and also measures the current state of the target (stupid humans)


The prediction from the physics model may not be accurate because the bike can encounter unforseen obstacles that might decrease it's speed or slip on the road. The vision sensor estimates are only accurate to a certain extent since it is faulty from the fight. And the GPS is not that accuracte since you're forced to use only 20th century technology at this time. However you do know the uncertainity of these estimates in terms of their covariances. 

So how do you finalize on the state of the vehicle before taking your final shot? You could just choose one of these estimates or take an average of these three estimates. But this will not yield the best estimate and you could miss your shot. Fortunately Skynet has equiped you with Kalman filters :D Now we gonna get that kill oooo yeh. Kalman filter is a technique that lets you combine multiple uncertain measurements. It yields the future state estimate based on the previous state estimate. It essentially has two steps:

1. Predict: Next state is estimated from previous state according to the kinematic model
2. Update: Combine sensor informations recursively to the prediction

**NOTE:**
The following equations with their color schemes are adopted from this very nice explanation [here](https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/). Also for a slightly non-flattering explanation refer [this document](http://www.cl.cam.ac.uk/~rmf25/papers/Understanding%20the%20Basis%20of%20the%20Kalman%20Filter.pdf).

## Predict:

In this step the physics-kinematics model, essentially modeling the system is used to predict the current state based on the previous state. You have to write the transition equations for both the state and it's uncertainity. Simple kinematics tells us the following:

$$
\begin{equation} 
\begin{split} 
\color{deeppink}{p_t} &= \color{royalblue}{p_{t-1}} + {\Delta t} &\color{royalblue}{v_{t-1}} \\ 
\color{deeppink}{v_t} &= &\color{royalblue}{v_{t-1}} 
\end{split} \\

\begin{split} 
\color{deeppink}{\mathbf{\hat{x}}_t} &= 
\begin{bmatrix} 
1 & \Delta t \\ 
0 & 1 
\end{bmatrix} 
\color{royalblue}{\mathbf{\hat{x}}_{t-1}} \\

\color{deeppink}{\mathbf{\hat{x}}_t} &= \mathbf{F}_t \color{royalblue}{\mathbf{\hat{x}}_{t-1}}
\end{split} 
\end{equation}
$$

where $\mathbf{F}_t$ is the state transition matrix. Notice that the state transition equation is time independent ($\Delta t$ is just incremental) and linear. Kalman filter assumes this to be the case when applied. If the equations are non-linear and time dependent, then we can use an Extended Kalman filter that makes Taylor-series approximations to obtain locally linear values. If there are **known** forces or external influences, one can also add this into the equation: 
$$
\begin{aligned} 
\color{deeppink}{\mathbf{\hat{x}}_t} &= \mathbf{F}_t \color{royalblue}{\mathbf{\hat{x}}_{t-1}} + \mathbf{B}_t \color{darkorange}{\mathbf{u}_t}
\end{aligned} 
$$ 
where $\mathbf{B}_t$ is called the control matrix and $\color{darkorange}{\mathbf{u}_t}$ the control vector. This comes in handy when the system is in your control. This is not the case here, as John Connor is the one driving the vehicle. If you're controlling the vehicle, you can add acceleration/throttle as the control vector.

Also most times, unknown forces (such as road slip and obstacles in this case) are always involved. Let's assume a Gaussian noise vector $\color{tan}{\mathbf{w_t}}$. The true state then becomes (notice the absence of hat):
$$
\begin{aligned} 
\color{deeppink}{\mathbf{x}_t} &= \mathbf{F}_t \color{royalblue}{\mathbf{x}_{t-1}} + \mathbf{B}_t \color{darkorange}{\mathbf{u}_t} + \color{tan}{\mathbf{w_t}}
\end{aligned}
$$

Now the prediction equation for the uncertainity is as follows:

$$
\begin{aligned} 
\color{deeppink}{\mathbf{P}_t} &= \mathbf{F_t} \color{royalblue}{\mathbf{P}_{t-1}} \mathbf{F}_t^T + \color{tan}{\mathbf{Q}_t} 
\end{aligned}
$$

Here the $\color{tan}{\mathbf{Q}_t}$ is nothing but the variance of the Gaussian noise $\color{tan}{\mathbf{w_t}}$. The first term can be derived according to the following rule of covariance:

$$
\begin{aligned} 
Cov(x) &= \Sigma\\ 
Cov(\color{firebrick}{\mathbf{A}}x) &= \color{firebrick}{\mathbf{A}} \Sigma \color{firebrick}{\mathbf{A}}^T 
\end{aligned}
$$

## Update:
In this step, the measurements of the sensors are combined with the predictions of the kinematics model. Skynet has given you an advanced tracking algorithm (let's say DEEPSORT) that gives you both the position and velocity of the target in the video feed. Let's say the vision sensor's observed measurement and uncertainity is:

$$
\begin{aligned}
(\color{mediumaquamarine}{\mu_1}, \color{mediumaquamarine}{\Sigma_1}) = (\color{mediumaquamarine}{\mathbf{z}_t}, \color{mediumaquamarine}{\mathbf{R}_t})
\end{aligned}
$$

From the first step of Kalman filter, you have a predicted state estimate and it's uncertainity. Let's convert that into sensor readings using an observation matrix $\mathbf{H_t}$. The observation matric essentially relates the units of sensor measurement to that of the state vector. For example the observation matrix converts your GPS readings in latitudes and longitudes to meters. The **predicted measurements** are then as follows:

$$
\begin{aligned}
(\color{deeppink}{\mu_0}, \color{deeppink}{\Sigma_0}) = (\color{deeppink}{\mathbf{H}_t \mathbf{\hat{x}}_t}, \ \  \color{deeppink}{\mathbf{H}_t \mathbf{P}_t \mathbf{H}_t^T})
\end{aligned}
$$

Now you have two Gaussians probability densities in your hand and can combine them. A nice property of Gaussians is that the combination of Gaussians yield a Gaussain as well. A multivariate Gaussian distribution is defined as follows:

$$
\begin{equation}
\mathcal{N}(\mathbf{x}, \mu, \Sigma) = \frac{1}{2 \pi^{k/2} \ \|\Sigma\|^{-1/2}} \exp\Big[-\frac{1}{2}(\mathbf{x}-\mu) \Sigma^{-1} (\mathbf{x}-\mu)^T \Big]
\end{equation}
$$

Combining two Gaussians (product of their pdfs) yields a scaled Gaussian. A nice derivation is provided [here](http://www.lucamartino.altervista.org/2003-003.pdf) for the univariate case. Without getting too mathy, combining two multivariate Gaussians after normalization yields another Gaussian with mean $ \color{mediumblue}{\mu’}$ and covariance $\color{mediumblue}{\Sigma’}$ as follows:

$$
\begin{aligned} 
\mathcal{N}(\mathbf{x}, \color{deeppink}{\mu_0}, \color{deeppink}{\Sigma_0}) \cdot \mathcal{N}(x, \color{mediumaquamarine}{\mu_1}, \color{mediumaquamarine}{\Sigma_1}) \stackrel{?}{=} \mathcal{N}(x, \color{mediumblue}{\mu’}, \color{mediumblue}{\Sigma’})
\end{aligned}
$$

Defining Kalman Gain as $\color{purple}{\mathbf{K}}$,

$$
\begin{equation} 
\begin{aligned} 
\color{purple}{\mathbf{K}} &= \Sigma_0 (\Sigma_0 + \Sigma_1)^{-1} \\
\color{mediumblue}{\mu’} &= \color{deeppink}{\mu_0} + \color{purple}{\mathbf{K}} (\color{mediumaquamarine}{\mu_1} – \color{deeppink}{\mu_0})\\ 
\color{mediumblue}{\Sigma’} &= \color{deeppink}{\Sigma_0} – \color{purple}{\mathbf{K}} \color{deeppink}{\Sigma_0} 
\end{aligned}
\end{equation}
$$

Here we can observe that Kalman gain defines the importance of sensor measurements as against the kinematic predictions. If the $\color{purple}{\mathbf{K}} \rightarrow 0$ then the sensor measurements are highly unreliable. If $\color{purple}{\mathbf{K}} \rightarrow 1$ then the sensor measurements are quite reliable and can be solely used for state estimate. Now, substituiting the means and covariances from kinematic estimate and sensor estimate into the above equation gives us:

$$
\begin{equation} 
\begin{aligned} 
\mathbf{H}_t \color{royalblue}{\mathbf{\hat{x}}_t’} &= \color{deeppink}{\mathbf{H}_t \mathbf{\hat{x}}_t} & + & \color{purple}{\mathbf{K}} ( \color{mediumaquamarine}{\mathbf{z}_t} – \color{deeppink}{\mathbf{H}_t \mathbf{\hat{x}}_t} ) \\ 
\mathbf{H}_t \color{royalblue}{\mathbf{P}_t’} \mathbf{H}_t^T &= \color{deeppink}{\mathbf{H}_t \mathbf{P}_t \mathbf{H}_t^T} & – & \color{purple}{\mathbf{K}} \color{deeppink}{\mathbf{H}_t \mathbf{P}_t \mathbf{H}_t^T} 
\end{aligned}
\end{equation}
$$

And the Kalman gain,

$$
\begin{equation}
\color{purple}{\mathbf{K}} = \color{deeppink}{\mathbf{H}_t \mathbf{P}_t \mathbf{H}_t^T} ( \color{deeppink}{\mathbf{H}_t \mathbf{P}_t \mathbf{H}_t^T} + \color{mediumaquamarine}{\mathbf{R}_t})^{-1} 
\end{equation}
$$

We can remove $\color{deeppink}{\mathbf{H}_t}$ from front of these equations (there's a $\color{deeppink}{\mathbf{H}_t}$ inside $\color{purple}{\mathbf{K}}$) and a $\color{deeppink}{\mathbf{H}_t^T}$ in rear of the covariance equation and simplify. We get,

$$
\begin{equation} 
\begin{split} 
\color{royalblue}{\mathbf{\hat{x}}_t’} &= \color{deeppink}{\mathbf{\hat{x}}_t} & + & \color{purple}{\mathbf{K}’} ( \color{mediumaquamarine}{\mathbf{z}_t} – \color{deeppink}{\mathbf{H}_t \mathbf{\hat{x}}_t} ) \\ 
\color{royalblue}{\mathbf{P}_t’} &= \color{deeppink}{\mathbf{P}_t} & – & \color{purple}{\mathbf{K}’} \color{deeppink}{\mathbf{H}_t \mathbf{P}_t} 
\end{split} \\

\color{purple}{\mathbf{K}’} = \color{deeppink}{\mathbf{P}_t \mathbf{H}_t^T} ( \color{deeppink}{\mathbf{H}_t \mathbf{P}_t \mathbf{H}_t^T} + \color{mediumaquamarine}{\mathbf{R}_t})^{-1} 
\label{kalgainfull} 
\end{equation}
$$

Now you have combined the information from kinematics model and the vision sensor. Wait, what about the GPS sensor? Well, you just use a subsequent update step just like above to combine the information from GPS sensor as well. It doesn't matter in what order you update these measurements. Viola! You got what you wanted. A combined state estimate from Kalman filter. These values $\color{royalblue}{\mathbf{\hat{x}}_t’}$ and $\color{royalblue}{\mathbf{P}_t’}$ can be subsequently plugged in and used to predict the next state using kinematics and update using sensor measurements in a loop. 

A few seconds of tracking using Kalman filter and you got yourself a target lock. Now fire that missile at John Connor. Boo-yeah! Skynet now has a resistance free future! Mission accomplished. Hasta la what? Yeah, that's right.


![alt](/images/blog6/close.jpg)
*Skynet is pretty kinky for an AI :3*