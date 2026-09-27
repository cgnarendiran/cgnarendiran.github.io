---
layout: post
title:  "MCTS and AlphaZero - Four Steps in the Dark"
date:   2026-09-27
image:  images/blog39/cover.jpg
description: "Monte Carlo tree search never enumerates and never finishes. AlphaZero turned its visit counts into a training target and stopped asking humans."
tags: [reinforcement-learning, game-theory, test-time-compute, graph-algorithms, deep-learning]
---

*On the cover: a cave survey part way through. Solid outlines are surveyed passage; the dashed red arrows are leads nobody has pushed. Source: Author.*

Three weeks ago I wrote about [what it would take to solve chess](/blog/solving-chess-paths-nodes/), and the answer was that nobody is going to. The tree is around $10^{44}$ positions, and the one skipping rule anybody has proved sound only gets you to its square root. So Stockfish guesses, very well and very fast.

Now sit the same machine down in front of a Go board.

In January 2016, John Tromp finished counting the legal positions on a 19 by 19 board: [about $2.08 \times 10^{170}$](https://tromp.github.io/go/legal.html), a 171-digit number. The observable universe holds around $10^{80}$ atoms. So you could hand every atom its own universe of atoms, give each one a position to mind, and still come up ten billion short.

Welcome to the era of **Monte Carlo tree search (MCTS)**. This is the story of how a search that never finishes, and looks at a two-thousandth of what Deep Blue did, took the game that was supposed to be a decade away.

AlphaGo and AlphaZero are the one thing that pulled me into the AI era, so this is not a neutral post. The credit belongs to David Silver, Aja Huang, Julian Schrittwieser, Demis Hassabis and the rest of the DeepMind team, who get talked about a lot less than the algorithm does.

## Deep Blue brought a tape measure

On the 11th of May 1997, in New York, Deep Blue beat Garry Kasparov by 3½ to 2½. It had lost to him 4–2 in Philadelphia the year before, the half that usually gets dropped. [Campbell, Hoane and Hsu (2002)](https://dl.acm.org/doi/10.1016/s0004-3702(01)00129-1) describe thirty nodes of an IBM RS/6000 SP carrying 480 custom chess chips, averaging 126 million positions a second across the match. On top of all that silicon sat a hand-written evaluation function of thousands of features, tuned with grandmasters in the room. Somebody decided how many points a doubled pawn costs (and somebody else disagreed).

So the recipe is two lines. Search as wide as the hardware allows, and at the bottom of every line, ask a human what a good position looks like.

You might think Go is the same job with a bigger board. [The AlphaGo paper](https://www.nature.com/articles/nature16961) puts chess at roughly 35 legal moves per turn over 80 moves and Go at roughly 250 over 150. That is not a gap you buy your way out of, but size is the less interesting half. So why did thirty years of faster chips not fix it? Because alpha-beta needs a number at the bottom of every line, and in Go nobody could write that number down. In chess you can: count the material, add a bit for king safety, subtract a bit for a doubled pawn. A Go stone is worth nothing by itself, and a wall of them facing the wrong way is worth less than nothing. Whether a group is alive or dead can turn on a single point forty moves later. Before 2006 the best Go programs played at about 14 kyu, which is somebody who has been going to a club for a few months.

## I want you to think about a cave

I do not mean a show cave with handrails, but an actual one: a few kilometres of passage a local club has been mapping for twenty years, on weekends, with a tape measure. Every trip is six hours for four people (one of whom forgot the spare batteries), and every chamber has three or four more holes out of it. So they will never survey the whole thing. What they have is a survey book and a rule about where to spend the next Saturday.

That is Monte Carlo tree search, one for one. A junction is a position in the game (the state $s$), a passage out of it is a legal move (the action $a$), and a **lead** is a passage nobody has walked. The survey book holds two numbers per passage: how many trips have gone down it ($N(s,a)$) and how well those went on average ($Q(s,a)$). One simulation is one trip:

1. **Select.** From the entrance, walk down through the junctions already in the book, taking the passage with the best score at each one. The next section is all about what "best score" means.
2. **Expand.** Sooner or later you reach somewhere the book has never heard of. Add it.
3. **Evaluate.** Work out how promising it looks. Classic MCTS plays on from there at random to the end of the game and sees who won. AlphaGo Zero asks a network for a number $v$ and turns round.
4. **Back up.** Walk back out, adding one to $N$ and folding the result into $Q$ for every passage you came through.

![Four panels of the same search tree during select, expand, evaluate and back up, with visit counts in each circle](/images/blog39/mcts-four-steps.png) *Figure 1: one simulation, run a few hundred times per move. Nobody ever looks at the whole tree. Source: Author*

Run that loop a few hundred times and the book fills up very unevenly, which is the point. And then comes the part that catches people out. When the club has to say which way the cave goes, they do not read off the best average. They read off the visit count.

Why the count? Because a passage with a wonderful average and two trips down it might have been lucky twice, while one with 412 trips has survived 412 chances to disappoint everybody.

## The Friday night argument

Every club has the same argument on a Friday night. Half the room wants the main streamway, because it is big and it went well last time. The other half wants to dig at the draughty crack in the third chamber, because nobody has been down it and cold air is coming out.

Both halves are right, which is why the argument never ends. Go back to the good passage every week and you map one corridor beautifully; chase a new crack every week and you map nothing. This is explore against exploit, and in 2006 [Kocsis and Szepesvári](https://link.springer.com/chapter/10.1007/11871842_29) took the answer from the multi-armed bandit literature, the maths of which slot machine to feed next. Rémi Coulom reached the tree version [that year](https://inria.hal.science/inria-00116992) and named it Monte Carlo tree search.

Their rule scores every lead as two things added together:

$$\text{score of a lead} = \text{how well it has gone so far} + \text{how much it deserves a look}$$

specifically,

$$a_t = \arg\max_a \left[\, Q(s,a) + c_{\text{puct}}\, P(s,a)\, \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)} \,\right]$$

where $Q(s,a)$ is the average result of every trip down passage $a$, $N(s,a)$ is how many trips those were, $\sum_b N(s,b)$ is the total over all passages out of this junction, $P(s,a)$ is a prior from the network (the caver's nose for which hole is worth trying), and $c_{\text{puct}}$ sets how argumentative the club is.

The second term is worth reading slowly. It has $N(s,a)$ on the bottom, so a passage goes quieter each time somebody walks it. It has the square root of everybody else's visits on top, so an untouched lead starts shouting again as the others climb. And it is all multiplied by $P(s,a)$, so a hole the nose likes jumps the queue.

Let's do one junction by hand, forty simulations in, with $c_{\text{puct}} = 1.5$ and $\sqrt{40} = 6.32$. A real Go position has about 250 passages out of it, so this is a slice of one:

| lead | prior $P$ | visits $N$ | average $Q$ | bonus $U$ | $Q + U$ |
|---|---|---|---|---|---|
| main streamway | 0.55 | 24 | 0.52 | 0.209 | 0.729 |
| draughty crack | 0.25 | 11 | 0.58 | 0.198 | **0.778** |
| wet crawl | 0.05 | 5 | 0.40 | 0.079 | 0.479 |

The crack's bonus is $1.5 \times 0.25 \times 6.32 / 12 = 0.198$, and that is enough to take it. The nose likes the streamway twice as much and it still loses, because eleven good trips beat twenty-four slightly worse ones once the bonus pays the difference.

![The exploration bonus falling as visits rise, and a stacked bar chart of three leads showing which gets picked](/images/blog39/puct.png) *Figure 2: left, the bonus $U$ collapsing as visits pile up. Right, the worked example. The crack wins by 0.049, which decides where four people spend Saturday. Source: Author*

Now check what happens next. The crack gets its trip, its bonus drops to 0.185, and the streamway is back on top within a few more. That argument gets settled a few hundred times before a move is played.

**NOTE:** one more thing is bolted onto the entrance, and it is my favourite footnote in the paper. AlphaZero mixes random noise into the root priors, so even a passage the nose hates gets walked now and then. The noise is Dirichlet, scaled by how many legal moves a position has: 0.3 for chess, 0.15 for shogi, 0.03 for Go. Somebody divided by the branching factor of three separate games, and I have more faith in those numbers than in most round ones.

## The draught

Finishing every trip at random sounds like a joke, and it worked: a few thousand random finishes tell you something real about a position. And nobody had to write down what a good position looks like, the exact thing three decades of Go programming had failed to do. That is how programs went from 14 kyu to around 5 dan in a few years.

But random finishes are slow, and they are noisy. What you actually want is the draught: you stand at the crack, feel cold air on your face, and know there is a lot of cave behind it without walking a step. That is a **value network** ($v$), the piece AlphaGo added. Give it a position, get back one number for how the game is going, and it never plays on.

AlphaGo carried four networks, and the smallest is the interesting one. Its supervised policy network was 13 layers, trained on 28.4 million positions from the [KGS Go Server](https://www.gokgs.com/), and guessed the expert's move right 57.0% of the time at 3 milliseconds a shot. Its fast rollout policy was one layer, saw part of the board, guessed right about 24% of the time, and took 2 microseconds. Fifteen hundred times faster for a bit under half the accuracy, on something you run a few hundred moves deep, thousands of times a position. Obviously the right trade, and the sort of decision that never makes the press release. They also ran the search with rollouts only, then with the value network only, then with both mixed half and half, and the mix beat both.

## October 2015, and then March 2016

In October 2015 AlphaGo played Fan Hui, the European champion, over five formal games and won all five. [The paper](https://www.nature.com/articles/nature16961) landed in Nature that January with a 99.8% win rate against every other Go program the team could find. Coulom had guessed in [Wired](https://www.wired.com/2014/05/the-world-of-computer-go/) in May 2014 that this was ten years off. It took eighteen months.

Then Seoul, March 2016, against Lee Sedol, one of the strongest players alive, and AlphaGo won 4–1.

Two moves are worth knowing, and they only work as a pair. In game two AlphaGo played move 37, a shoulder hit on the fifth line, while Lee was out of the room. The commentators called it a mistake (a brave thing to say quickly, on live television). AlphaGo's own policy put the chance of a human playing it at 1 in 10,000. It decided the game.

In game four Lee played move 78, a wedge into the middle of AlphaGo's position, and AlphaGo's policy gave that one 1 in 10,000 too. Go players call it the divine move. AlphaGo's read of the game came apart afterwards, and Lee won the only game anybody has won against it. He retired in November 2019. "Even if I become the number one," he told Yonhap, "there is an entity that cannot be defeated."

## Burn the notes

So AlphaGo started with 28.4 million positions of other people's Go. How much of its strength came out of that pile? [Nature, October 2017](https://www.nature.com/articles/nature24270): none of it.

AlphaGo Zero throws out the human games, the separate policy and value networks, and the random rollouts. What is left is one network $f_\theta(s) = (p, v)$ with two heads: a policy head $p$ giving a probability for every move, and a value head $v$ giving one number for how the position is going. The search calls it once per new junction, and that is the evaluation step.

Then comes the trick. The search is better than the network, because it is the network plus eight hundred trips down real passages. So take what the search decided, and train the network to have thought it in the first place. The visit counts become the label:

$$\pi(a \vert s) = \frac{N(s,a)^{1/\tau}}{\sum_b N(s,b)^{1/\tau}}$$

where $N(s,a)$ is the visit count from the search that just finished and $\tau$ is a temperature setting how sharp the label is. Early in a game $\tau = 1$, so the label keeps its spread and the games stay varied. Later it goes towards zero and the label becomes "the most-visited move, and nothing else". The network trains on the position $s$, the label $\pi$ and the result $z$: $+1$ for a win, $-1$ for a loss.

$$\ell = (z - v)^2 - \pi^\top \log p + c\lVert\theta\rVert^2$$

The first term pulls the value head towards the result that actually happened. The second is the cross entropy from the [cross entropy post](/blog/cross-entropy-loss/), pulling the policy head towards the visit counts. The third is weight decay.

![The self-play loop as three boxes, with a zoom panel showing visit counts becoming the policy label](/images/blog39/selfplay-loop.png) *Figure 3: the loop. The network improves the search, the search improves the network, and the only thing entering from outside is the rulebook. Source: Author*

It reached the strength of the version that beat Lee Sedol after 4.9 million self-play games and three days. Then it beat that version 100–0.

Here is the number I find most interesting. The trained network, asked to just pick its highest-probability move with no search, rates 3,055 Elo. The same weights with the search wrapped around them rate 5,185.

![Bar chart of four Elo ratings with the gap between raw network and searched network marked](/images/blog39/search-ablation.png) *Figure 4: the raw network against the same network with 1,600 simulations per move, with AlphaGo Fan and AlphaGo Lee in grey for scale. Source: Author*

Same weights, two thousand one hundred and thirty Elo apart. That much of the strength was never in the network. It is in the trips you take before committing, and on its own the network is a strong club player with excellent instincts and no patience whatsoever.

## One algorithm, three games

AlphaGo Zero still knew it was playing Go. A Go position means the same thing rotated and reflected, so training got eight positions out of every one. Chess does not, because pawns only walk one way. AlphaZero, [the December 2017 preprint](https://arxiv.org/abs/1712.01815) and then [Science in December 2018](https://www.science.org/doi/10.1126/science.aar6404), took those Go-shaped parts out. Same code and hyperparameters for all three games, except the Dirichlet noise. Training ran 700,000 steps of mini-batches of 4,096, on 5,000 first-generation TPUs generating games and 64 second-generation TPUs learning from them (a number worth saying out loud). Nine hours for chess. Twelve for shogi. Thirteen days for Go.

| | Deep Blue, 1997 | AlphaZero, 2018 | What the gap says |
|---|---|---|---|
| positions a second | 126 million | 60,000 | Two thousand times fewer, picked two thousand times better |
| judgement comes from | hand-written features, grandmasters | one network, its own games | Nobody had to know any chess |
| knew on day one | openings, endgames, king safety | the rules | The knowledge was the expensive part, and it was replaceable |

**NOTE:** the widely quoted rates are 80,000 against Stockfish's 70 million, from the 2017 preprint. Science says 60,000 against 60 million, and I use the second, as in the [chess post](/blog/solving-chess-paths-nodes/).

In the preprint's 100-game match against Stockfish 8: 28 wins, 72 draws, no losses. In Science the matches ran to 1,000 games, finishing 155–6.

## MuZero does not get the rulebook

AlphaZero still needs the rules, because the search has to know what the next junction looks like before walking there. [MuZero](https://arxiv.org/abs/1911.08265) (DeepMind, Nature 2020) takes those away too and learns its own hidden state instead, one that only has to predict the reward, the policy and the value. Those are the only three things the search ever consults. So nothing forces that state to look like a board, and it does not. The [JEPA post](/blog/jepa-nobody-cares-about-the-wallpaper/) makes the same argument about pixels: model what the job needs, not what the world looks like. MuZero matched AlphaZero on Go, chess and shogi without being told how the pieces move.

## Where the survey went after the games

- **[AlphaDev](https://www.nature.com/articles/s41586-023-06004-9)** turned writing assembly into a game and found shorter sorting routines, now in LLVM's C++ library. **[AlphaTensor](https://www.nature.com/articles/s41586-022-05172-4)** beat Strassen's 1969 matrix multiplication at some sizes.
- **[MuZero](https://deepmind.google/blog/muzero-alphazero-and-alphadev-optimizing-computer-systems/)** picks VP9 encoder settings on YouTube for roughly 4% less bitrate, and **AlphaChip** laid out three generations of Google's TPU.
- **[AlphaProof](https://www.nature.com/articles/s41586-025-09833-y)** runs the loop over proofs in [Lean](https://lean-lang.org/), which a computer checks line by line, and solved four of six 2024 Mathematical Olympiad problems. [Leela Chess Zero](https://lczero.org/) and [KataGo](https://github.com/lightvector/KataGo) are the open source ones.

And the 3,055 against 5,185 result keeps coming back, because it says you can buy strength from fixed weights at the moment of answering. That is the bet behind reasoning models, and the [GRPO and RLVR post](/blog/grpo-rlvr/) is the same idea with the tree flattened into a batch. Which leaves the real question: what replaces the rulebook? Chess has one and Lean has one. Prose does not, and searching over a model's reasoning steps works only as well as the thing scoring those steps. Gradient descent can exploit a learned scorer faster than anyone can patch it.

## What the survey does not show

**The 2017 match was DeepMind's match.** Stockfish 8 ran on 64 threads with a 1 GB hash table, no opening book, and a flat one minute per move. That is not how engines are normally tested. The criticism was fair. Science answered much of it: a thousand games, a newer Stockfish build, opening books, and time odds for Stockfish. AlphaZero won those too. It was still DeepMind's match against a Stockfish DeepMind picked.

**"From scratch" cost 5,000 TPUs.** Learning with no human data is free of humans and expensive in silicon, and nine hours of chess on five thousand accelerators is not nine hours. Leela Chess Zero reproduced it on volunteer machines, over years. The human data was never the bottleneck, and the compute quietly became one.

**It needs a simulator that is exact, cheap and fast.** Eight hundred simulations per move only makes sense when rolling a position forward costs nothing and the rules are never wrong. MuZero relaxes only the second half. Two things you did this week fit neither: replying to your landlord, and deciding what to cook on Thursday. No rulebook for either, and you cannot run Thursday evening eight hundred times to see which dinner went best.

**Superhuman on its own distribution, and only there.** [Adversarial Policies Beat Superhuman Go AIs](https://arxiv.org/abs/2211.00241) (Wang et al., ICML 2023) trained an opponent against KataGo at superhuman settings and won more than 97%. That opponent plays terrible Go. It sets up one shape KataGo misreads. And it loses to most human amateurs, which is the detail that should bother you. The attack transfers to other superhuman Go programs untouched, and survived retraining meant to defend against it. Somebody found a way in through a crack the survey had marked solid rock.

## Conclusion

Deep Blue and AlphaZero disagree about who writes down what a good position looks like. Deep Blue had it written by people, feature by feature, and it went as far as people could take it. AlphaZero grows the same judgement out of its own visit counts, and a visit count is only a record of where the club spent its Saturdays.

So the survey on the clubhouse wall is twenty years of arguments about which crack was worth a look, drawn as lines. And there was more cave in it than any of them thought.

And now you know. Fin.
