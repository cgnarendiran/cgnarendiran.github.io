---
layout: post
title:  "MCTS and AlphaZero - Four Steps in the Dark, Part 2"
date:   2026-09-27 12:00:00
image:  images/blog40/cover.jpg
description: "AlphaGo gave tree search a policy and a value network. AlphaGo Zero made the search the network's teacher, in an update that sits close to PPO's."
tags: [reinforcement-learning, game-theory, test-time-compute, deep-learning]
---

*On the cover: a caver with the survey book strapped to her helmet, pushing through a new passage. NPS photo, [Public domain](https://commons.wikimedia.org/wiki/File:When_surveying_new_cave_passages,_cavers_must_often_crawl_on_their_hands_and_knees_and_even_on_their_stomachs_to_get_to_bigger_(0112c9d6-155d-4519-3eab-4e9a4ccf6c40).JPG), via Wikimedia Commons.*

In [part 1](/blog/mcts-alphazero/), we built Monte Carlo tree search from scratch: play positions out at random, keep a tree of where those games went, and send the next games down the passages that did well. In part 1's cave, a position is a junction, a move is a passage, and one simulation is one trip. The survey book keeps a visit count $N(s,a)$ and an average result $Q(s,a)$ for every passage, and the search plays the most-visited move. With nothing but random games, it took Go programs from club level to strong amateur.

Then it stopped. Strong amateur is a long way from Lee Sedol.

Two things held it back. The select step knows nothing about Go, so it has to try all 250 moves at a junction before it can prefer any. And random rollouts are slow and noisy. This post is about how AlphaGo fixed both with neural networks, and how AlphaGo Zero then turned the search into the network's teacher. At the end, that loop turns out to be a close relative of PPO, the algorithm ChatGPT was trained with.

## AlphaGo: four networks and a search

AlphaGo was built at DeepMind by a team led by David Silver and Aja Huang. It trained three networks in stages and a fourth tiny one for rollouts, then ran MCTS on top.

![AlphaGo's pipeline: human games train a policy network and a rollout policy, the policy network is copied into an RL policy network that plays itself, its games train a value network, and all of them feed the search](/images/blog40/alphago-pipeline.png) *Figure 1: AlphaGo end to end. The top row is trained before the match; the purple box runs at every move. Source: Author*

1. **Policy network.** The reflex from part 1. It gives a probability for every move, a guess at what a strong player would do. It had 13 layers, was trained on 28.4 million positions from strong amateurs' games on the [KGS Go Server](https://www.gokgs.com/), and picked the expert's move 57% of the time.
2. **RL policy network.** A copy of network 1 that plays earlier versions of itself. After each game, every move the winner played is made a little more likely, and every move the loser played a little less likely. That is a **policy gradient**, the simplest kind, called REINFORCE.
3. **Value network.** It gives one number for who is winning a position. It learned from 30 million positions, one from each self-play game, because positions from the same game are nearly identical and it would just memorise them.
4. **Rollout policy.** One layer and only 24% accurate, but fifteen hundred times faster than network 1. That is the right trade for something you run thousands of times per move.

The policy gradient in step 2 is one line:

$$\Delta\rho \propto z \,\nabla_\rho \log p_\rho(a \vert s)$$

where $\rho$ is the RL network's weights, $p_\rho(a \vert s)$ is the probability it gave to move $a$ in position $s$, $\nabla_\rho \log p_\rho(a \vert s)$ is the direction that makes that move more likely, $z$ is $+1$ if the player who made the move went on to win and $-1$ if they lost, and $\propto$ means "in proportion to". So a win pushes up every move that side played, and a loss pushes them all down. The RL network beat network 1 in more than 80% of games.

At play time, every new junction gets a **prior** $P(s,a)$ for each move from network 1. That is the experienced caver's nose for which hole is worth trying. Network 1 worked better here than the stronger network 2, and the paper's guess is that humans pick "a diverse beam of promising moves" while RL "optimizes for the single best move". A new junction is then scored half by the value network and half by one fast rollout. The value network is the draught: you feel cold air at a crack and know there is a lot of cave behind it without walking a step.

The paper rates each version of the search in **Elo**, where a 400-point gap means the stronger player scores about 10 to 1. Rollouts alone rated 2,416 and the value network alone rated 2,177. Both together rated 2,890, just below Fan Hui's 2,908 on the same scale.

The prior also enters the select rule. AlphaGo's version, **PUCT**, multiplies UCT's bonus by it:

$$a_t = \arg\max_a \left[\, Q(s,a) + c_{\text{puct}}\, P(s,a)\, \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)} \,\right]$$

The bonus still shrinks as a passage gets walked. But a hole the nose likes gets a head start, and one it hates barely gets looked at. Here is one junction by hand, with made-up numbers: forty trips so far and $c_{\text{puct}} = 1.5$, so $\sqrt{40} = 6.32$. These are three of about 250 passages, and the other 247 have tiny priors and no visits.

| passage | prior $P$ | visits $N$ | average $Q$ | bonus $U$ | $Q + U$ |
|---|---|---|---|---|---|
| main streamway | 0.55 | 24 | 0.52 | 0.209 | 0.729 |
| draughty crack | 0.25 | 11 | 0.58 | 0.198 | **0.778** |
| wet crawl | 0.05 | 5 | 0.40 | 0.079 | 0.479 |

The crack's bonus is $1.5 \times 0.25 \times 6.32 / 12 = 0.198$. The nose likes the streamway more than twice as much. But the streamway has also had more than twice the trips, so the two bonuses come out almost level. Then the crack's better average decides it.

![The bonus falling as visits rise, and a stacked bar chart of three passages showing which gets picked](/images/blog40/puct.png) *Figure 2: left, the bonus $U$ shrinking as visits pile up. Right, the worked example. The crack wins by 0.049, which decides where four people spend Saturday. Source: Author*

## Two moves against Lee Sedol

AlphaGo beat Fan Hui, the European champion, 5–0 in October 2015. In [a 2014 Wired article](https://www.wired.com/2014/05/the-world-of-computer-go/), Coulom had guessed that a machine was "maybe ten years" from beating a professional. It took less than two. In March 2016 AlphaGo beat Lee Sedol 4–1, and the two famous moves from that match both come down to the prior.

In game two, AlphaGo played move 37, a stone so far from the edge that commentators called it a mistake. Its policy network put the chance of a human playing it at 1 in 10,000. But a tiny prior means few trips, not none, and the search found that the move was good. In game four, Lee played move 78, which AlphaGo's policy network also gave 1 in 10,000. This time the few trips were not enough to show the danger, and Lee won the game. Demis Hassabis said afterwards that AlphaGo's mistake was its reply, move 79, and that it only noticed around move 87.

## AlphaGo Zero: the search becomes the teacher

How much of AlphaGo's strength actually needed the 28.4 million human positions? [AlphaGo Zero](https://www.nature.com/articles/nature24270) (Nature, October 2017) answered that: none of it. It threw out the human games, the rollouts and the separate networks. It keeps one network with two outputs (heads), $f_\theta(s) = (p, v)$, where $\theta$ is its weights. The policy head $p$ supplies the priors, and the value head $v$ scores each new junction.

The search plays better than the network alone, because it is the network plus 1,600 trips of lookahead. In the paper's words, MCTS "may therefore be viewed as a powerful policy improvement operator". So AlphaGo Zero trains the network to predict what the search decided. The visit counts become the label:

$$\pi(a \vert s) = \frac{N(s,a)^{1/\tau}}{\sum_b N(s,b)^{1/\tau}}$$

where $\pi(a \vert s)$ is the label for move $a$ in position $s$, $N(s,a)$ is its visit count, and $\tau$ is a temperature. With $\tau = 1$ the label is each move's share of the visits: in Figure 3, D4 got 412 of 800, so its label is 0.52. After the first 30 moves of a game, $\tau$ goes towards zero and the label becomes just the most-visited move.

Each position of a self-play game becomes a training example, with the label $\pi$ and the game's result $z$ ($+1$ for a win, $-1$ for a loss). Training makes this loss as small as it can:

$$\ell = (z - v)^2 - \pi^\top \log p + c\lVert\theta\rVert^2$$

The first term pulls the value head towards the real result. The second is the [cross entropy](/blog/cross-entropy-loss/) between the label and the policy head, which pulls the policy towards the visit counts. The third is weight decay, a small penalty that keeps the weights from growing large.

On day one the network is random, and the searches are poor. But each search still adds 1,600 trips of lookahead and the real result of the game, so the label is always a little better than the network. The network catches up, guides a better search, and the loop goes round again.

![The self-play loop as three boxes, with a zoom panel showing visit counts becoming the policy label](/images/blog40/selfplay-loop.png) *Figure 3: the self-play loop, drawn with AlphaZero's 800 simulations a move (AlphaGo Zero used 1,600). The only thing coming in from outside is the rules of the game. Source: Author*

It passed the version that beat Lee Sedol after 36 hours, and beat it 100–0 after three days. The number I find most interesting is from the same paper. The final network, after 40 days, rates 3,055 Elo when it plays its top move with no search. The same weights with the search rate 5,185.

![Bar chart of four Elo ratings with the gap between raw network and searched network marked](/images/blog40/search-ablation.png) *Figure 4: AlphaGo Zero's network on its own against the same network with search, at 5 seconds a move, with AlphaGo Fan and AlphaGo Lee in grey for scale. Source: Author*

That is 2,130 Elo from the same weights, which on paper means the network alone would win about one game in two hundred thousand against itself with search. On its own, it plays a little below the AlphaGo that beat Fan Hui. That is excellent instincts and no patience whatsoever.

## Where PPO comes in

PPO is the algorithm OpenAI used to fine-tune InstructGPT, the model behind ChatGPT, and the [GRPO post](/blog/grpo-rlvr/) covers it in detail. In short: the policy plays, a second network (the critic) guesses how well each action should go, and the **advantage** is how much better or worse it actually went. The update makes actions with a positive advantage more likely. A clip, usually 0.2, stops any one update from moving the policy too far. AlphaGo's REINFORCE step was the simplest member of this family: it uses the game result $z$ instead of an advantage, and it has no clip.

So why did AlphaGo Zero drop that step? Both answer the same question: how do you find a policy slightly better than the one you have, and move the network towards it? PPO finds it by trial and error. It plays whole games and nudges the moves that beat expectations. The signal for any one move is weak, because a win at move 150 says little about move 12. AlphaGo Zero finds it by lookahead. At every position the search works out a better policy right there, and the network copies it. The signal is strong, but it needs a simulator.

The two are closer than they look. [Grill et al. (2020)](https://arxiv.org/abs/2007.12509) showed that AlphaZero's visit counts approximately solve

$$\bar{\pi} = \arg\max_y \left[\, Q^\top y - \lambda_N \,\mathrm{KL}(P \,\Vert\, y) \,\right]$$

where $y$ is any policy over the moves, $Q^\top y$ is its average $Q$, $\mathrm{KL}(P \Vert y)$ measures how far it has strayed from the prior $P$, and $\lambda_N$ is a weight that shrinks as the simulations add up. In words: pick the policy that scores best, minus a penalty for straying from what the network already believed. That is the shape of PPO's update too. PPO enforces "stay close" with the clip, and the RLHF version adds a KL penalty. Grill et al. tie AlphaZero most directly to MPO, another method in that family. So you can read AlphaZero as a PPO-like policy update, where the better policy is worked out by lookahead instead of estimated from games already played.

| | PPO | AlphaGo Zero and AlphaZero |
|---|---|---|
| where the better policy comes from | moves that beat the critic's guess, in games already played | the search's visit counts, at every position |
| policy training signal | advantage-weighted log-probability, clipped | cross entropy towards $\pi$ |
| value training signal | critic, trained on the rewards that followed | value head, trained on the result $z$ |
| what keeps each step small | the clip, plus a KL penalty in RLHF | the prior's pull in PUCT, which Grill et al. write as a KL penalty |
| needs a simulator | no | yes, or a learned one (MuZero, below) |

The 3,055 against 5,185 gap is also the bet behind reasoning models like DeepSeek-R1: spend more compute at answer time, and fixed weights get stronger. But a search needs something to score its trips. Chess has its rules, and Lean has its proof checker. An essay has neither. And if the scorer is itself a learned model, training will exploit its mistakes faster than anyone can patch them.

## One algorithm, three games

AlphaGo Zero still used Go-specific tricks, such as training on the eight rotations and mirror images of every position. AlphaZero ([preprint 2017](https://arxiv.org/abs/1712.01815), [Science 2018](https://www.science.org/doi/10.1126/science.aar6404)) dropped them. It used the same code and settings for Go, chess and shogi (Japanese chess). Its self-play games ran on 5,000 TPUs (Google's AI chips), and training took nine hours for chess, twelve for shogi and thirteen days for Go. Against Stockfish 8, it won 28 of 100 games and lost none in the preprint, and won 155 of 1,000 with 6 losses in Science.

## MuZero does not get the rulebook

AlphaZero still needs the rules, so that the search knows where a move leads. [MuZero](https://arxiv.org/abs/1911.08265) (Nature 2020) learns its own internal picture of the game instead. That picture is trained only to predict the reward, the policy and the value, because those are all the search ever asks for. MuZero matched AlphaZero on Go, chess and shogi without being told how the pieces move, and it learned 57 Atari games too. The [JEPA post](/blog/jepa-nobody-cares-about-the-wallpaper/) makes the same argument about images: predict what the job needs, and skip the pixels.

## Where it went after board games

- **[AlphaDev](https://www.nature.com/articles/s41586-023-06004-9)** found shorter sorting routines that are now in LLVM's C++ standard library. **[AlphaTensor](https://www.nature.com/articles/s41586-022-05172-4)** beat Strassen's 1969 method for multiplying 4 by 4 matrices, in arithmetic where every number is 0 or 1.
- **[MuZero](https://deepmind.google/blog/muzero-alphazero-and-alphadev-optimizing-computer-systems/)** tunes VP9 video compression on some YouTube videos, saving about 4% of the bitrate.
- **[AlphaProof](https://www.nature.com/articles/s41586-025-09833-y)** runs the same loop over proofs in [Lean](https://lean-lang.org/), where a computer checks every step. It solved three of the six 2024 International Mathematical Olympiad problems, including the hardest one.
- **[Leela Chess Zero](https://lczero.org/)** and **[KataGo](https://github.com/lightvector/KataGo)** are open-source versions that anyone can run.

## The honest cons

**DeepMind set up the 2017 match.** Stockfish got a fixed minute per move, a small hash table (its memory of positions already seen) and no opening book. That is not how engines are normally tested. The Science rematch fixed most of it, even giving AlphaZero a tenth of Stockfish's thinking time, and AlphaZero still won.

**"From scratch" still cost 5,000 TPUs.** Nine hours on 5,000 TPUs is about 45,000 TPU-hours, or around five years on a single chip.

**Superhuman, until somebody plays it strangely.** [Wang et al. (ICML 2023)](https://arxiv.org/abs/2211.00241) trained an opponent that beat superhuman KataGo in more than 97% of games, by setting up one ring-shaped group that KataGo misjudges. The same opponent loses to most human amateurs. Self-play had never produced that shape often enough for KataGo to learn it.

## Conclusion

AlphaGo gave the club a nose and a draught, the policy and value networks. AlphaGo Zero turned the loop round, so that the search trains the network that guides the search. Seen from reinforcement learning, that is a PPO-like update, where the better policy comes from lookahead.

AlphaZero plays chess far better than any human. But it still guesses, so on its own it will never solve the game. This kind of search can also look for proofs, as AlphaProof does in Lean. That is how I think chess finally gets solved. An AI will search over proofs the way AlphaZero searches over moves, until it finds the pruning theorems that shrink the tree to something small enough to walk. Then chess gets a finished map, and nobody will have had to walk every passage to draw it.

And now you know. Fin.
