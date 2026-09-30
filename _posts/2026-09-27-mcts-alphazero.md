---
layout: post
title:  "MCTS and AlphaZero - Four Steps in the Dark, Part 1"
date:   2026-09-27
image:  images/blog39/cover.jpg
description: "Why game programs search a tree, why they fill it with random games, and what plain Monte Carlo tree search does on real Go and chess positions."
tags: [game-theory, graph-algorithms, reinforcement-learning, probability]
---

*On the cover: a cave survey part way through. Solid outlines are surveyed passage; the dashed red arrows are passages nobody has walked yet. Source: Author.*

In January 2016, John Tromp finished counting the legal positions on a 19 by 19 Go board: [about $2.08 \times 10^{170}$](https://tromp.github.io/go/legal.html), a 171-digit number. The observable universe has around $10^{80}$ atoms. Give every one of those atoms its own universe of $10^{80}$ atoms, and put one Go position on each. You would still have covered only one position in every twenty billion.

Two months later, AlphaGo beat Lee Sedol, one of the best Go players alive, 4 games to 1. It never came anywhere near looking at all those positions. Its search looked at a tiny corner of the tree, picked by playing out games, and it is called **Monte Carlo tree search (MCTS)**. This post builds it up from the start. First, why a program searches a tree at all, and why it would fill that tree with random games. Then what the search does on a real Go position and a real chess position, with no neural network anywhere. [Part 2](/blog/mcts-alphazero-part2/) is how AlphaGo and AlphaZero wrapped neural networks around it, and how all of that connects to PPO, the reinforcement learning algorithm ChatGPT was trained with.

## Why search a tree at all

A game is a tree. Every position is a node, and every legal move is a branch to the position it leads to. The start of the game is the root, and the finished games are the leaves. So picking a move means asking which branch out of the current position leads to a win.

The fast way to pick is by reflex. You look at the board and play whatever looks right. A neural network trained on expert games can do this pretty well: AlphaGo's first network guessed the expert's move 57% of the time. But a reflex never checks itself. It does not ask what the opponent will do next.

Looking ahead does check. "If I take his knight, can he mate me?" You follow a move down the tree, assume the opponent answers with their best reply, and see where you end up. This rule is called **minimax**. You pick the move that is best for you, on the assumption that your opponent always picks the move that is worst for you. If you could follow every line to the end of the game, minimax would play perfectly.

You can't. [The AlphaGo paper](https://www.nature.com/articles/nature16961) puts chess at about 35 legal moves per turn over a game of about 80 moves, and Go at about 250 legal moves over about 150. That works out to roughly $10^{123}$ paths through the chess tree and $10^{360}$ through the Go tree.

So chess programs cut the search off after a set number of moves. They score the position they reach with a hand-written formula (an **evaluation function**), which counts the material, adds a bit for king safety and takes a bit off for a doubled pawn. And they skip branches that provably cannot change the answer (**alpha-beta pruning**). That recipe beat Kasparov in 1997. Stockfish, the strongest chess engine today, still runs alpha-beta search, although its formula has been a small neural network since 2020.

## Why Monte Carlo

Go breaks that recipe, because nobody could write the formula.

The rules of Go are simple. Two players take turns placing stones, a group of stones that gets completely surrounded is captured, and whoever surrounds more of the board wins. But a single stone is worth nothing by itself, and a wall of stones facing the wrong way can be worth less than nothing. Whether a group survives or gets captured can depend on a single point, forty moves later. So a Go program had no reliable way to score a position at the end of its search. Before 2006, the best Go programs played at about 14 kyu, the level of somebody who has been going to a Go club for a few months.

The Monte Carlo idea is to stop trying to write the formula. If you can't score a position, play it out. From the position, play random moves for both sides until the game ends, and note who won. Do that a few thousand times, and the fraction of games your side wins is the score. "Monte Carlo" is the usual name for any method built on random sampling, after the casino in Monaco.

Why would random games tell you anything, when random moves are terrible moves? Because a position where your side wins 70% of random games is usually better than one where it wins 30%. And Go suits this well. Every game ends, because the board fills up. The final count is simple. And a big lead in territory tends to survive a lot of bad play from both sides.

Bernd Brügmann tried this on 9 by 9 Go [in 1993](http://www.ideanest.com/vegos/MonteCarloGo.pdf). His program played thousands of near-random games after each candidate move and picked the move that did best on average. It reached about 25 kyu, which is roughly a beginner. This version is called **flat Monte Carlo**, and it has two problems. It spends as many games on obviously bad moves as on good ones. And it assumes the opponent plays at random, so a move that loses to one precise reply still looks fine, because a random opponent rarely finds that reply.

The fix came in 2006: put the random games in a tree. Every random game adds its result to the moves it passed through. Moves that do well get more games, so the tree grows deeper along the good lines. And at the opponent's turns, the tree assumes the opponent picks their best reply, which is minimax again. [Kocsis and Szepesvári](http://ggp.stanford.edu/readings/uct.pdf) proved that as the number of games grows, the chance of this search picking the wrong move goes to zero. Rémi Coulom built a Go program on the same idea that year, and [his paper](https://inria.hal.science/inria-00116992) is usually credited with the name. With MCTS, Go programs went from about 14 kyu to around 5 dan (a strong amateur) in a few years.

Here are the four ways of choosing a move so far, side by side:

| approach | how it scores a position | expects the opponent's best reply | where it breaks |
|---|---|---|---|
| minimax to the end | plays every line out | yes | the tree is far too big |
| alpha-beta with a formula | a hand-written evaluation function | yes | Go has no formula |
| flat Monte Carlo | random games after each move | no | falls for one precise reply |
| MCTS | random games, steered by a tree | yes | sharp traps, and it starts out blind |

So when is MCTS the right tool? When four things are true:

1. You can simulate. Given a position and a move, you can work out the next position, because you know the rules or have a model of them.
2. There is a clear result at the end: a win, a loss or a score.
3. The tree is too big to search fully, and you can't write a good formula to score positions part way.
4. You have time to think before each decision, enough for hundreds or thousands of simulated games.

Most of daily life fails the first two. Replying to your landlord and deciding what to cook on Thursday have no rulebook. And you cannot run Thursday evening eight hundred times to see which dinner went best.

## The caving club

I want you to think about a wild cave, the kind with no handrails. A local caving club has been mapping it for twenty years, on weekends, with a tape measure. Every trip takes four people six hours (and one of them always forgets the spare batteries). Every chamber they reach has three or four more holes leading out of it. So they will never survey the whole thing. What they have instead is a survey book, and a rule for deciding where to go next Saturday. A computer search is in the same spot. Its trips are far cheaper, hundreds per move instead of one a week, but a game tree is far bigger than any cave.

Here is how that maps onto a game. A junction in the cave is a position in the game (the state $s$). A passage out of a junction is a legal move (the action $a$). For each passage, the survey book keeps two numbers. One is how many trips have gone down it ($N(s,a)$, the visit count). The other is how well those trips went on average ($Q(s,a)$, the value). A trip that ends in a won game scores 1 and one that ends in a loss scores 0, so $Q$ sits somewhere in between.

Go has two players, so the book scores the passages at each junction for whoever is choosing there. On your moves, the search picks what is best for you. On your opponent's moves, it assumes they pick what is best for them, which is the minimax rule from earlier.

One simulation (one run of the search) is one trip, and it has four steps:

1. **Select.** Start at the entrance and walk down through junctions that are already in the book. At each one, take the passage with the best score. The next section is about what "best score" means.
2. **Expand.** Sooner or later you reach a junction the book has never seen. Add it to the book.
3. **Evaluate.** Guess how promising this new junction is. Plain MCTS plays random moves from here to the end of the game and sees who wins, which is called a **rollout**. Later programs skip the rollout and ask a neural network for a score $v$ instead.
4. **Back up.** Walk back out to the entrance. For every passage you came through, add one to its visit count $N$ and fold the result into its average $Q$.

![Four panels of the same search tree during select, expand, evaluate and back up, with visit counts in each circle](/images/blog39/mcts-four-steps.png) *Figure 1: the four steps of one simulation. The search runs this loop hundreds of times before it plays a single move. Source: Author*

Run that loop a few hundred times and the book fills up very unevenly. The promising passages get most of the trips. The bad ones get a few trips, and then they are left alone. That is how the search spends its time on the small part of the tree that matters.

So when it is time to actually play a move, which passage does the club commit to? You might expect the one with the best average. MCTS picks the one with the most visits. Why the count? A passage with a wonderful average from two trips might just have been lucky twice. A passage with 412 trips has survived 412 chances to disappoint everybody.

## Which passage next

The select step needs a rule for picking a passage at each junction. Kocsis and Szepesvári took theirs from the maths of slot machines (the multi-armed bandit problem), and it is called **UCT**. It scores every passage as two things added together:

$$\text{score of a passage} = \text{how well it has gone so far} + \text{a bonus for having had few trips}$$

specifically, in its usual textbook form,

$$a_t = \arg\max_a \left[\, Q(s,a) + c \sqrt{\frac{\ln \sum_b N(s,b)}{N(s,a)}} \,\right]$$

where $a_t$ is the passage the trip takes, $\arg\max_a$ means "the passage that makes the bracket biggest", $Q(s,a)$ is the average result of the trips down passage $a$, $N(s,a)$ is how many trips those were, $\sum_b N(s,b)$ is the total over all passages out of this junction, $\ln$ is the natural log, and $c$ is a constant that sets how big the bonus is (how much the club likes trying new holes).

The bonus has $N(s,a)$ on the bottom, so it shrinks every time somebody walks that passage. The junction's total sits on top, inside the log, so the bonus of a passage that has been left alone slowly grows while the others get walked. And a passage with no trips at all has an infinite bonus, so it gets tried before anything else. That's it. There is no knowledge of Go in there, only counts and averages.

## Plain MCTS on a Go position

Here is plain MCTS on a real position, with random rollouts and no neural network anywhere. I wrote it in about 190 lines of Python, on a 7 by 7 board so that it runs in seconds.

Black's group in the bottom-left corner has three empty points inside it: A1, B1 and C1. A group needs two separate empty points inside it (two **eyes**) to be safe from capture for good. If Black plays B1, the group has two eyes, A1 and C1, and it lives. If White plays B1 first, the group can only ever make one eye, and it dies. The rest of the board is settled so that this corner decides the game. So B1 is the only good move for either side, and Go players have a proverb for exactly this: your opponent's vital point is your vital point.

![A 7 by 7 Go board with visit counts on every empty point, B1 with 4,331 visits, beside a line chart of B1's share of visits rising with the number of simulations](/images/blog39/go-vital-point.png) *Figure 2: plain MCTS, 5,000 simulations, Black to play. Left, the visits each Black move got. Right, B1's share of all visits as the search went on. Source: Author*

After 5,000 simulations, which took about six seconds, B1 had 4,331 of the visits and won 90% of its games. The next most-visited move, F1, had 51 visits and won 53%. B1 was already the most-visited move after 100 simulations. Why 90% against about 50%? After B1, Black's group lives in every random game. After any other move, it lives only if Black happens to reach B1 before White does, which is about half the time.

## Plain MCTS on a chess position

Chess is where random games go wrong, and a trap shows how. In this position, White's queen can take the knight on d7 for free. But the queen is the only piece guarding e1, and White's own pawns box the king in. So after Qxd7, Black plays Re1, and it is checkmate.

I ran two searches from here, with the same rollout: six random moves, then count the material. The first is flat Monte Carlo, with 400 random games after each of White's 26 moves and no tree. It scores Qxd7 at 0.686, the best of all 26, ahead of Kf1 at 0.626. Black has 20 legal replies after Qxd7, so a random reply finds Re1 only one time in twenty. Most of those games just see White a knight up.

The second is MCTS with 5,000 simulations. It likes Qxd7 too at first, and Qxd7 is its most-visited move between about 200 and 500 simulations. But each visit to Qxd7 adds one more of Black's replies to the tree. Once Re1 is in the tree, it wins every trip for Black, so the search keeps choosing it at that junction. Re1 ended with 27 visits and a perfect record, and Qxd7's average sank with every one of them.

![A chess board with arrows for Qxd7, the Re1 mate that follows, and f4, beside two charts comparing flat Monte Carlo scores and MCTS visit counts for seven White moves](/images/blog39/chess-trap.png) *Figure 3: the same rollouts, with and without a tree. Flat Monte Carlo ranks the free knight first. MCTS gives it 73 visits out of 5,000. Source: Author*

After 5,000 simulations Qxd7 had 73 visits. The most-visited moves were f4, f3, Kf1, h3, g4 and h4. None of them moves the queen off the first rank, and most of them give the king an escape square.

## Where plain MCTS runs out

Plain MCTS took Go programs from club level to strong amateur, and then it stopped getting better. More simulations help, but they do not fix these:

1. **Sharp tactics.** [Ramanujan, Sabharwal and Selman (2010)](https://cdn.aaai.org/ojs/13437/13437-40-16955-1-2-20201228.pdf) call them **shallow traps**: moves that lose to a short, forced sequence. They showed that plain MCTS caught traps three moves deep but missed them at five moves and deeper, and that it spent most of its time exploring far deeper lines than it needed to. The trap above was only one move deep, so the tree found it within a few hundred simulations. A trap five moves deep needs the tree to find the one right reply at every level. Chess is full of traps like that, which is part of why the strongest chess engines stayed with alpha-beta.
2. **A blind select step.** UCT knows nothing about the game. At a junction with 250 moves, it has to try every one of them before it can prefer any.
3. **Noisy rollouts.** Each rollout plays to the end of the game with moves that are nothing like good moves. So it takes thousands of them to say anything useful, and they can still be wrong about a position a strong player would read in a second.

## Conclusion

MCTS is a small idea. When you can't score a position, play it out at random, and keep a tree of where those games went so that the next ones go somewhere useful. It needs nothing but the rules, and on a 7 by 7 board it found a vital point that Go players learn from a proverb. But it walks into every passage blind. And a visit count is just a tally of where the club spent its Saturdays.

[Part 2](/blog/mcts-alphazero-part2/) gives the club a nose and a draught. That is AlphaGo's policy and value networks, then AlphaGo Zero, where the search becomes the network's teacher, and then how that loop connects to PPO.

Stay tuned for Part 2. Till then ciao.
