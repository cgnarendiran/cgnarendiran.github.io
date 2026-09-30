---
layout: post
title:  "MCTS and AlphaZero - Four Steps in the Dark"
date:   2026-09-27
image:  images/blog39/cover.jpg
description: "How Monte Carlo tree search decides which moves deserve a look, and how AlphaZero learned Go and chess from its own search, with no human games."
tags: [reinforcement-learning, game-theory, test-time-compute, graph-algorithms, deep-learning]
---

*On the cover: a cave survey part way through. Solid outlines are surveyed passage; the dashed red arrows are passages nobody has walked yet. Source: Author.*

Three weeks ago I wrote about [what it would take to solve chess](/blog/solving-chess-paths-nodes/). The game tree has about $10^{123}$ paths through it. The only shortcut anyone has proved safe, alpha-beta pruning, cuts that to about $10^{62}$, which is still hopeless. So chess is not solved today. I think it will be solved one day. I think an AI will do it, by proving new theorems about pruning, convergence and bounds that let it skip most of the tree. Those theorems do not exist yet. So for now, Stockfish (the strongest chess program you can download) guesses, and it guesses very well and very fast.

Now sit the same kind of program down in front of a Go board.

In January 2016, John Tromp finished counting the legal positions on a 19 by 19 Go board: [about $2.08 \times 10^{170}$](https://tromp.github.io/go/legal.html), a 171-digit number. The observable universe has around $10^{80}$ atoms. Give every one of those atoms its own universe of $10^{80}$ atoms, and put one Go position on each. You would still have covered only one position in every twenty billion.

Welcome to the era of **Monte Carlo tree search (MCTS)**. This is the story of how a search that only ever looks at a tiny corner of the tree beat one of the best Go players in the world, years before anyone expected.

## Deep Blue's formula

On the 11th of May 1997, in New York, Deep Blue beat Garry Kasparov 3½ to 2½. A year earlier in Philadelphia, Kasparov had beaten it 4–2. [Campbell, Hoane and Hsu (2002)](https://dl.acm.org/doi/10.1016/s0004-3702(01)00129-1) describe the machine: a 30-node IBM RS/6000 SP supercomputer carrying 480 custom chess chips, averaging 126 million positions a second across the match. On top of all that hardware sat an **evaluation function**, a hand-written formula that gives a position a score. It had thousands of features, tuned with grandmasters in the room. Somebody decided how many points a doubled pawn costs (and somebody else disagreed).

So the recipe has two parts. First, search as many moves ahead as the hardware allows. Then at the end of every line, score the position with the formula that people wrote.

You might think Go is the same job with a bigger board. It is a much bigger board. [The AlphaGo paper](https://www.nature.com/articles/nature16961) puts chess at about 35 legal moves per turn over a game of about 80 moves, and Go at about 250 legal moves over about 150. That works out to roughly $10^{123}$ paths through the chess tree and $10^{360}$ through the Go tree.

But size is only half the problem. The other half is that formula at the end of every line. In chess you can write one: count the material, add a bit for king safety, take a bit off for a doubled pawn. In Go nobody could.

The rules of Go are simple. Two players take turns placing stones, a group of stones that gets completely surrounded is captured, and whoever surrounds more of the board wins. But a single stone is worth nothing by itself, and a wall of stones facing the wrong way can be worth less than nothing. Whether a group of stones survives or gets captured can depend on a single point, forty moves later. So a Go program had no reliable way to score the positions at the end of its search, and Deep Blue's kind of search is useless without that score. Before 2006, the best Go programs played at about 14 kyu. That is the level of somebody who has been going to a Go club for a few months.

## The caving club

I want you to think about a wild cave, the kind with no handrails. A local caving club has been mapping it for twenty years, on weekends, with a tape measure. Every trip takes four people six hours (and one of them always forgets the spare batteries). Every chamber they reach has three or four more holes leading out of it. So they will never survey the whole thing. What they have instead is a survey book, and a rule for deciding where to go next Saturday. A computer search is in the same spot. Its trips are far cheaper, hundreds per move instead of one a week, but a game tree is far bigger than any cave.

Here is how that maps onto a game. A junction in the cave is a position in the game (the state $s$). A passage out of a junction is a legal move (the action $a$). For each passage, the survey book keeps two numbers. One is how many trips have gone down it ($N(s,a)$, the visit count). The other is how well those trips went on average ($Q(s,a)$, the value). A trip that ends in a won game scores $+1$ and one that ends in a loss scores $-1$, so $Q$ sits somewhere in between.

Go has two players, so there is one more rule. At each junction, the book scores the passages for whoever is choosing there. On your moves, the search picks what is best for you. On your opponent's moves, it assumes they pick what is best for them.

One simulation (one run of the search) is one trip, and it has four steps:

1. **Select.** Start at the entrance and walk down through junctions that are already in the book. At each one, take the passage with the best score. The next section is about what "best score" means.
2. **Expand.** Sooner or later you reach a junction the book has never seen. Add it to the book.
3. **Evaluate.** Guess how promising this new junction is. Classic MCTS plays random moves from here to the end of the game and sees who wins, which is called a **rollout**. Later programs skip the rollout and ask a neural network for a score $v$ instead.
4. **Back up.** Walk back out to the entrance. For every passage you came through, add one to its visit count $N$ and fold the result into its average $Q$.

![Four panels of the same search tree during select, expand, evaluate and back up, with visit counts in each circle](/images/blog39/mcts-four-steps.png) *Figure 1: the four steps of one simulation. The search runs this loop hundreds of times before it plays a single move. Source: Author*

Run that loop a few hundred times and the book fills up very unevenly. The promising passages get most of the trips. The bad ones get a few trips, and then they are left alone. That is how the search spends its time on the small part of the tree that matters.

So when it is time to actually play a move, which passage does the club commit to? You might expect the one with the best average. MCTS picks the one with the most visits. Why the count? A passage with a wonderful average from two trips might just have been lucky twice. A passage with 412 trips has survived 412 chances to disappoint everybody.

## The Friday night argument

Every club has the same argument on a Friday night. Half the room wants the main streamway, because it is big and it went well last time. The other half wants to dig at the draughty crack in the third chamber, because nobody has been down it and the club's most experienced caver has a good feeling about it.

Both halves have a point. A club that always goes back to the streamway maps one corridor beautifully and never learns what is behind the crack. But a club that chases every new crack never gets far down any of them. In machine learning this is called **exploration versus exploitation**: try something new, or go back to what already works.

In 2006, [Kocsis and Szepesvári](https://link.springer.com/chapter/10.1007/11871842_29) borrowed an answer from the **multi-armed bandit** problem. That is the maths of deciding which slot machine to feed next when you don't know their payouts. Their method for trees is called UCT. The same year, Rémi Coulom built a Go program on the same kind of search, and [his paper](https://inria.hal.science/inria-00116992) is usually credited with naming it. "Monte Carlo" is the usual name for any method built on random sampling, after the casino in Monaco, and here the random part is the rollouts.

AlphaGo and AlphaZero use a later version of the rule, called PUCT. It scores every passage as two things added together:

$$\text{score of a passage} = \text{how well it has gone so far} + \text{how much it deserves a look}$$

specifically,

$$a_t = \arg\max_a \left[\, Q(s,a) + c_{\text{puct}}\, P(s,a)\, \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)} \,\right]$$

where $a_t$ is the passage the trip takes, $\arg\max_a$ means "the passage that makes the bracket biggest", $Q(s,a)$ is the average result of every trip down passage $a$, $N(s,a)$ is how many trips those were, $\sum_b N(s,b)$ is the total over all passages out of this junction, $P(s,a)$ is the **prior**, a neural network's guess at how good the move is before anyone has walked it (the experienced caver's nose for which hole is worth trying), and $c_{\text{puct}}$ is a constant that sets how much weight exploring gets (how much the club likes trying new holes).

The 2006 rule had the same two-part shape with no prior in it. AlphaGo added $P(s,a)$, so that a trained network could point the search at good moves from the first trip.

Let's look at the second term, the bonus $U$. It has $N(s,a)$ on the bottom, so the bonus shrinks every time somebody walks that passage. It has the square root of all the visits at this junction on top, so an ignored passage's bonus slowly grows while the others are being walked. And it is multiplied by $P(s,a)$, so a hole the nose likes gets a head start.

Let's do one junction by hand. Say forty trips have come through it so far, and $c_{\text{puct}} = 1.5$. The square root of 40 is 6.32. The numbers are made up to show the arithmetic. A real Go position has about 250 legal moves, so these are three passages out of 250. The other 247 have tiny priors, no visits and an average of zero, so their scores are tiny too.

| passage | prior $P$ | visits $N$ | average $Q$ | bonus $U$ | $Q + U$ |
|---|---|---|---|---|---|
| main streamway | 0.55 | 24 | 0.52 | 0.209 | 0.729 |
| draughty crack | 0.25 | 11 | 0.58 | 0.198 | **0.778** |
| wet crawl | 0.05 | 5 | 0.40 | 0.079 | 0.479 |

The crack's bonus is $1.5 \times 0.25 \times 6.32 / 12 = 0.198$. The nose likes the streamway more than twice as much (0.55 against 0.25). But the streamway has also had more than twice as many trips, so the two bonuses come out almost level. Then the crack's better average (0.58 against 0.52) decides it.

![The exploration bonus falling as visits rise, and a stacked bar chart of three passages showing which gets picked](/images/blog39/puct.png) *Figure 2: left, the bonus $U$ shrinking as visits pile up. Right, the worked example. The crack wins by 0.049, which decides where four people spend Saturday. Source: Author*

Now check what happens next. The crack gets its trip, and its bonus drops to 0.185. If its average stays at 0.58, the crack wins the next three trips as well, and then the streamway is back on top. The search settles this argument at every junction, hundreds of times, before it plays a single move.

**NOTE:** AlphaZero adds one more thing at the entrance (the root of the tree). It mixes random noise into the priors there, so even a passage the nose hates gets walked now and then. The noise has one setting per game: 0.3 for chess, 0.15 for shogi and 0.03 for Go. A smaller setting piles the noise onto fewer moves. Go has about 250 legal moves to chess's 35, so the paper shrank the setting in proportion. That way the noise boosts a handful of random moves in every game.

## The draught

Finishing every trip with random moves sounds like a joke. But it works. A position where your side wins 70% of random games is usually better than one where it wins 30%, even though random moves are bad moves. Each trip adds one random game to the averages, and after thousands of trips those averages tell you something real about each position. And nobody had to write down what a good Go position looks like, which was the thing three decades of Go programming had failed to do. With MCTS, Go programs went from about 14 kyu to around 5 dan (a strong amateur) in a few years.

But rollouts are slow, because each one plays all the way to the end of the game. And they are noisy, because random moves are nothing like good moves. What a caver actually wants is the draught. You stand at the crack, feel cold air on your face, and know there is a lot of cave behind it without walking a single step. That is a **value network** ($v$), the piece AlphaGo added. You give it a position, and it gives you back one number for who is winning. It never plays on. AlphaGo trained it on 30 million positions, each taken from a different game the program played against itself, and each labelled with who won that game.

AlphaGo was built at DeepMind by a team led by David Silver and Aja Huang, and it used four networks. Two of them show the trade-off nicely. The **policy network** ($p$) looks at a position and gives a probability for every move, which is a guess at what a strong player would do. AlphaGo's was 13 layers deep, trained on 28.4 million positions from 160,000 games between strong amateurs on the [KGS Go Server](https://www.gokgs.com/), an online place to play Go. It guessed the expert's move 57% of the time, and each guess took 3 milliseconds.

AlphaGo's rollouts were not fully random. They used a fast rollout policy, a single layer that looked at only part of the board. It guessed the expert's move about 24% of the time, and each guess took 2 microseconds. So it was fifteen hundred times faster for a bit under half the accuracy. For something you run to the end of the game, thousands of times per move, that is clearly the right trade. The other two networks were a sharper policy network trained by playing against itself, and the value network.

The team also tried the search with rollouts only, then with the value network only, then with both mixed half and half. The paper rates each version in **Elo**, the system chess and Go use to rate players. A 400-point gap means the stronger player is expected to score about 10 to 1. Rollouts alone rated 2,416 and the value network alone rated 2,177. Mixed, they rated 2,890, just below Fan Hui's 2,908 on the same scale.

## October 2015, and then March 2016

In October 2015, AlphaGo played Fan Hui, the European champion, in five formal games and won all five. [The paper](https://www.nature.com/articles/nature16961) came out in Nature that January. It also reported a 99.8% win rate against every other Go program the team could find. In [a Wired article](https://www.wired.com/2014/05/the-world-of-computer-go/) from May 2014, Coulom had guessed that a machine beating a professional without a head start (a handicap) was "maybe ten years" away. It took less than two.

In March 2016, in Seoul, AlphaGo played Lee Sedol, one of the strongest players alive, and won 4–1.

Two moves from that match are famous, one from each side. In game two, AlphaGo played move 37, a shoulder hit on the fifth line. That is a stone placed much further from the edge than professionals thought sensible, and some commentators called it a mistake. Lee got up, left the room, and took nearly fifteen minutes to reply. AlphaGo's own policy network put the chance of a human playing it at 1 in 10,000. But a tiny prior means few trips, not none. The search walked move 37 enough times to find that it was good, and AlphaGo went on to win the game.

In game four, Lee played move 78, a wedge right into the middle of AlphaGo's position. AlphaGo's policy network had given that move 1 in 10,000 too. This time the few trips it got were not enough to show the danger. Demis Hassabis said afterwards that AlphaGo's mistake was its reply, move 79, and that it only realised this around move 87. Go players call Lee's move the divine move, and Lee won the game. It is the only game a human has won against AlphaGo in an official match. Lee retired in November 2019. "Even if I become the number one," he told Yonhap, "there is an entity that cannot be defeated."

## Zero human games

AlphaGo learned first from 28.4 million positions of human games. So how much of its strength actually needed them? The answer came in [Nature in October 2017](https://www.nature.com/articles/nature24270), with AlphaGo Zero: none of it.

AlphaGo Zero drops the human games, the rollouts and the separate networks. It keeps one network with two outputs (heads), written $f_\theta(s) = (p, v)$, where $\theta$ is the network's weights. The policy head $p$ gives a probability for every move. The value head $v$ gives one number for who is winning. The search calls this network once for every new junction, and that is the whole evaluate step.

The search plays better than the network does on its own, because it is the network plus 1,600 trips down real passages. So AlphaGo Zero takes what the search decided, and trains the network to have guessed that in the first place. The visit counts become the training label:

$$\pi(a \vert s) = \frac{N(s,a)^{1/\tau}}{\sum_b N(s,b)^{1/\tau}}$$

where $\pi(a \vert s)$ is the label for move $a$ in position $s$, $N(s,a)$ is the visit count from the search that just finished, and $\tau$ is a temperature that sets how sharp the label is. With $\tau = 1$, this is just each move's share of the visits: 800 visits out of 1,600 gives a label of 0.5. For the first 30 moves of a game $\tau = 1$, so the label keeps its spread and the games stay varied. After that, $\tau$ goes towards zero and the label becomes "the most-visited move, and nothing else".

Every position from a self-play game becomes one training example. It has the position $s$, the label $\pi$ and the final result of that game $z$. The result is $+1$ for a win and $-1$ for a loss. Training makes this loss as small as it can:

$$\ell = (z - v)^2 - \pi^\top \log p + c\lVert\theta\rVert^2$$

The first term pulls the value head towards the result that actually happened. The second is the cross entropy from the [cross entropy post](/blog/cross-entropy-loss/): for every move, multiply the label by the log of the network's probability, add them up, and flip the sign. It pulls the policy head towards the visit counts. The third is weight decay, a small penalty with a constant $c$ that keeps the weights from growing large.

On day one the network is random, so the first searches are poor. But each search still adds two things the network does not have: 1,600 trips of looking ahead, and the real result of the game at the end. So the label is always a little better than the network, and the network catches up a little at a time. Then the better network guides a better search, and the loop goes round again.

![The self-play loop as three boxes, with a zoom panel showing visit counts becoming the policy label](/images/blog39/selfplay-loop.png) *Figure 3: the self-play loop. The network guides the search, the search's visit counts train the network, and the only thing coming in from outside is the rules of Go. Source: Author*

It passed the version that beat Lee Sedol after 36 hours of training. After three days and 4.9 million games against itself, it beat that version 100 games to 0.

The number I find most interesting is in the same paper. The final AlphaGo Zero network, after 40 days of training, rates 3,055 Elo when it just plays its highest-probability move with no search. The same weights with the search wrapped around them rate 5,185.

![Bar chart of four Elo ratings with the gap between raw network and searched network marked](/images/blog39/search-ablation.png) *Figure 4: AlphaGo Zero's network on its own against the same network with search, at 5 seconds a move, with AlphaGo Fan and AlphaGo Lee in grey for scale. Source: Author*

That is 2,130 Elo between the same weights with and without search. On paper, the network on its own would win about one game in two hundred thousand against the same network with search. So all of that extra strength comes from the trips taken before each move. On its own, the network plays a little below the AlphaGo that beat Fan Hui (3,144). That is excellent instincts and no patience whatsoever.

## One algorithm, three games

AlphaGo Zero still knew it was playing Go. A Go board means the same thing when you rotate it or mirror it, so AlphaGo Zero got eight training positions out of every one. A chess board does not, because pawns only move one way. AlphaZero ([the December 2017 preprint](https://arxiv.org/abs/1712.01815), and then [Science in December 2018](https://www.science.org/doi/10.1126/science.aar6404)) took those Go-specific parts out. It used the same code and the same settings for Go, chess and shogi (Japanese chess), except for the noise from the note above.

Training ran for 700,000 steps, each on a batch of 4,096 positions. 5,000 first-generation TPUs (Google's own AI chips) played the self-play games, and 64 second-generation TPUs trained the network on them. It trained for nine hours on chess, twelve hours on shogi and thirteen days on Go.

| | Deep Blue, 1997 | AlphaZero, 2018 | What changed |
|---|---|---|---|
| positions a second | 126 million | 60,000 | About 2,100 times fewer, because the priors point the search at the few moves worth checking |
| judgement comes from | hand-written features, tuned with grandmasters | one network, trained on its own games | No chess knowledge went in by hand |
| knew on day one | openings, endgames, king safety | the rules | It learned the rest in nine hours of self-play |

**NOTE:** the widely quoted rates are 80,000 positions a second against Stockfish's 70 million, from the 2017 preprint. Science says 60,000 against 60 million. I use the second, as in the [chess post](/blog/solving-chess-paths-nodes/).

In the preprint's 100-game match against Stockfish 8, AlphaZero won 28 games, drew 72 and lost none. In the Science paper the match ran to 1,000 games. AlphaZero won 155 and lost 6, and the other 839 were draws.

## MuZero does not get the rulebook

AlphaZero still needs the rules. The search has to know which position a move leads to before it can walk there. [MuZero](https://arxiv.org/abs/1911.08265) (DeepMind, Nature 2020) takes the rules away too. Instead, it learns its own internal picture of the game (a hidden state), and a way to step that picture forward one move. The hidden state only has to predict three things: the reward, the policy and the value. The reward is the points scored along the way, and in a board game that is just the win or loss at the end. Those are the only three things the search ever asks for. So nothing forces the hidden state to look like a board, and it does not.

The [JEPA post](/blog/jepa-nobody-cares-about-the-wallpaper/) makes the same argument about images: predict only what the job needs, and skip the pixels. MuZero matched AlphaZero on Go, chess and shogi without ever being told how the pieces move. It also learned 57 Atari games, where nobody hands you the rules anyway.

## Where it went after board games

- **[AlphaDev](https://www.nature.com/articles/s41586-023-06004-9)** turned writing assembly code into a game, and found shorter sorting routines. They are now in the C++ standard library that ships with LLVM. **[AlphaTensor](https://www.nature.com/articles/s41586-022-05172-4)** did the same for matrix multiplication, and beat Strassen's 1969 method for 4 by 4 matrices, in arithmetic where every number is 0 or 1 (47 multiplications against 49).
- **[MuZero](https://deepmind.google/blog/muzero-alphazero-and-alphadev-optimizing-computer-systems/)** picks the VP9 video compression settings for some YouTube videos, and saves about 4% of the bitrate.
- **[AlphaProof](https://www.nature.com/articles/s41586-025-09833-y)** runs the same loop over proofs written in [Lean](https://lean-lang.org/), a language in which a computer checks every step of a proof. It solved three of the six problems at the 2024 International Mathematical Olympiad, including the hardest one, and a sister system (AlphaGeometry 2) solved a fourth.
- **[Leela Chess Zero](https://lczero.org/)** and **[KataGo](https://github.com/lightvector/KataGo)** are open-source versions for chess and Go that anyone can run.

The 3,055 against 5,185 result matters outside games too. It says you can make fixed weights stronger by spending more compute at the moment of answering. Reasoning models like DeepSeek-R1 make the same bet: they think for longer before they answer. The [GRPO and RLVR post](/blog/grpo-rlvr/) covers how those are trained. GRPO uses a trick like AlphaGo Zero's training label, without the tree: sample a batch of answers, check which ones are right, and train the model towards those.

But a search needs something to score its trips. Chess has its rules, and Lean has its proof checker. An essay or an email has neither. So a search over a model's reasoning steps is only as good as whatever scores those steps. And if that scorer is itself a learned model, training will find and exploit its mistakes faster than anyone can patch them.

## The honest cons

**DeepMind set up the 2017 match.** In the preprint, Stockfish 8 ran on 64 threads with a 1 GB hash table (its memory of positions it has already looked at). It had no opening book (a database of known good opening moves), and it got a fixed one minute per move. Engines are not normally tested like that, and chess players said so. The Science paper answered most of it, with 1,000 games, a newer Stockfish, opening books, and matches where AlphaZero got only a tenth of Stockfish's thinking time. AlphaZero still won. But DeepMind still chose the Stockfish and the settings.

**Learning from scratch cost 5,000 TPUs.** No human games went in, but a lot of hardware did. Nine hours on 5,000 TPUs is about 45,000 TPU-hours, or around five years on a single chip. Leela Chess Zero reproduced AlphaZero on volunteers' computers, and it took years.

**It needs a perfect, cheap simulator.** AlphaZero's 800 simulations per move only make sense when trying a move costs almost nothing and the result is never in doubt. MuZero learns the rules instead of being told them, but it still needs millions of games of practice and a clear win or loss at the end. Two things you did this week have neither: replying to your landlord, and deciding what to cook on Thursday. There is no rulebook for either. And you cannot run Thursday evening eight hundred times to see which dinner went best.

**Superhuman, until somebody plays it strangely.** [Adversarial Policies Beat Superhuman Go AIs](https://arxiv.org/abs/2211.00241) (Wang et al., ICML 2023) trained an opponent specifically to beat KataGo running at superhuman settings. It won more than 97% of its games. And that opponent plays terrible Go. It sets up one unusual shape, a ring-shaped group, that KataGo misjudges, and it loses to most human amateurs. Self-play never produced that shape often enough for KataGo's network to learn it. A human Go player learned the trick from the attacker and beat superhuman programs with it by hand. And after KataGo was retrained to defend against it, a fine-tuned attacker still won almost half its games.

## Conclusion

Deep Blue and AlphaZero both search, and both need a way to judge a position at the end of a line. Deep Blue's judgement was written by people, feature by feature, and it got as far as people could take it. AlphaZero learns its judgement from its own visit counts. And a visit count is just a tally of where the club spent its Saturdays.

That brings me back to chess. AlphaZero plays chess far better than any human. But it still guesses, so on its own it will never solve the game. This kind of search can also look for proofs, and AlphaProof already does that in Lean. That is how I think chess finally gets solved. An AI will search over proofs the way AlphaZero searches over moves, until it finds the pruning theorems that shrink the tree to something small enough to walk. On that day chess gets a finished map, and nobody will have had to walk every passage to draw it.

And now you know. Fin.
