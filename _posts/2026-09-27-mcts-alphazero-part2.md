---
layout: post
title:  "MCTS and AlphaZero - Four Steps in the Dark, Part 2"
date:   2026-09-27 12:00:00
image:  images/blog40/cover.jpg
description: "AlphaGo gave tree search a policy and a value network. AlphaGo Zero made the search the network's teacher, in an update that sits close to PPO's."
tags: [reinforcement-learning, game-theory, test-time-compute, deep-learning]
---

*On the cover: a caver with the survey book strapped to her helmet, pushing through a new passage. NPS photo, [Public domain](https://commons.wikimedia.org/wiki/File:When_surveying_new_cave_passages,_cavers_must_often_crawl_on_their_hands_and_knees_and_even_on_their_stomachs_to_get_to_bigger_(0112c9d6-155d-4519-3eab-4e9a4ccf6c40).JPG), via Wikimedia Commons.*

In [part 1](/blog/mcts-alphazero/), we built Monte Carlo tree search from scratch. It plays positions out with random moves, keeps a tree of where those games went, and sends the next games down the passages that did well. With nothing but random games, it found the vital point on a 7 by 7 Go board and dodged a back-rank trap in chess. And it took Go programs from club level to strong amateur.

Then it stopped. Strong amateur is a long way from Lee Sedol.

Part 1 ended on the reasons. The select step knows nothing about Go, so at a junction with 250 moves it has to try every one before it can prefer any. And random rollouts are slow and noisy, because each one plays to the end of the game with moves that are nothing like good moves. This post is about how AlphaGo fixed both with neural networks, and how AlphaGo Zero then turned the search into the network's teacher. At the end, it connects that loop to PPO, the reinforcement learning algorithm ChatGPT was trained with.

A quick reminder of the cave from part 1. A caving club is mapping a cave it will never finish. A junction is a position in the game (the state $s$), a passage out of it is a legal move (the action $a$), and one trip is one simulation. The survey book keeps two numbers for each passage: how many trips went down it (the visit count $N(s,a)$) and how well they went on average (the value $Q(s,a)$). At every junction, the rule for picking a passage (UCT) adds that average to a bonus for passages with few trips. When it is time to play, the search picks the most-visited move.

## AlphaGo: four networks and a search

AlphaGo was built at DeepMind by a team led by David Silver and Aja Huang. It trained three networks in stages, used a fourth small one for rollouts, and ran MCTS on top.

![AlphaGo's pipeline: human games train a policy network and a rollout policy, the policy network is copied into an RL policy network that plays itself, its games train a value network, and all of them feed the search](/images/blog40/alphago-pipeline.png) *Figure 1: AlphaGo end to end. The top row is trained before the match; the purple box runs at every move. Source: Author*

1. **Policy network.** This is the reflex from part 1. It looks at a position and gives a probability for every move, which is a guess at what a strong player would do. It had 13 layers and was trained on 28.4 million positions from 160,000 games between strong amateurs on the [KGS Go Server](https://www.gokgs.com/). It guessed the expert's move 57% of the time, and each guess took 3 milliseconds.
2. **RL policy network.** This starts as a copy of network 1 and then plays against randomly picked earlier versions of itself. After each game, every move the winner played is made a little more likely, and every move the loser played a little less likely. That is a **policy gradient**, and AlphaGo used the simplest one, called REINFORCE.
3. **Value network.** This looks at a position and gives one number for who is winning. It was trained on 30 million positions, each taken from a different self-play game, and each labelled with who won that game. It takes only one position per game, because positions from the same game are nearly identical and the network would just memorise them.
4. **Rollout policy.** A tiny network, one layer that looks at only part of the board. It guessed the expert's move 24% of the time, but each guess took 2 microseconds. So it was fifteen hundred times faster for a bit under half the accuracy. For something you run to the end of the game, thousands of times per move, that is the right trade.

The policy gradient in step 2 is one line:

$$\Delta\rho \propto z \,\nabla_\rho \log p_\rho(a \vert s)$$

where $\rho$ is the RL network's weights, $p_\rho(a \vert s)$ is the probability it gave to move $a$ in position $s$, $\nabla_\rho \log p_\rho(a \vert s)$ is the direction to push the weights to make that move more likely, $z$ is $+1$ if the player who made the move went on to win and $-1$ if they lost, and $\propto$ means "in proportion to". So a win pushes up every move that side played, and a loss pushes them all down. The RL network beat network 1 in more than 80% of games. With no search at all, it also won 85% of its games against Pachi, the strongest open-source Go program at the time, which ran 100,000 simulations per move.

At play time, AlphaGo runs MCTS with two changes. First, every new junction gets a **prior** $P(s,a)$ for each move, from network 1. That is the experienced caver's nose for which hole is worth trying. Network 1 worked better here than the stronger network 2. The paper's guess is that "humans select a diverse beam of promising moves, whereas RL optimizes for the single best move". Second, a new junction is scored half by the value network and half by one fast rollout. The value network is the draught. You stand at the crack, feel cold air on your face, and know there is a lot of cave behind it without walking a single step.

The team also tried the search with rollouts only, then with the value network only, then with both. The paper rates each version in **Elo**, the system chess and Go use to rate players. A 400-point gap means the stronger player is expected to score about 10 to 1. Rollouts alone rated 2,416 and the value network alone rated 2,177. Mixed half and half, they rated 2,890, just below Fan Hui's 2,908 on the same scale.

The prior also changes the select rule. AlphaGo's version is called **PUCT**:

$$a_t = \arg\max_a \left[\, Q(s,a) + c_{\text{puct}}\, P(s,a)\, \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)} \,\right]$$

It has the same two parts as UCT from part 1: the average, plus a bonus for few trips. The bonus still shrinks as a passage gets walked, and still grows while the others do. But now it is multiplied by $P(s,a)$. So a hole the nose likes gets a head start, and one the nose hates barely gets looked at. The constant $c_{\text{puct}}$ sets how big the bonus is.

Let's do one junction by hand. Say forty trips have come through it so far, and $c_{\text{puct}} = 1.5$. The square root of 40 is 6.32. The numbers are made up to show the arithmetic. A real Go position has about 250 legal moves, so these are three passages out of 250. The other 247 have tiny priors, no visits and an average of zero, so their scores are tiny too.

| passage | prior $P$ | visits $N$ | average $Q$ | bonus $U$ | $Q + U$ |
|---|---|---|---|---|---|
| main streamway | 0.55 | 24 | 0.52 | 0.209 | 0.729 |
| draughty crack | 0.25 | 11 | 0.58 | 0.198 | **0.778** |
| wet crawl | 0.05 | 5 | 0.40 | 0.079 | 0.479 |

The crack's bonus is $1.5 \times 0.25 \times 6.32 / 12 = 0.198$. The nose likes the streamway more than twice as much (0.55 against 0.25). But the streamway has also had more than twice as many trips, so the two bonuses come out almost level. Then the crack's better average (0.58 against 0.52) decides it.

![The bonus falling as visits rise, and a stacked bar chart of three passages showing which gets picked](/images/blog40/puct.png) *Figure 2: left, the bonus $U$ shrinking as visits pile up. Right, the worked example. The crack wins by 0.049, which decides where four people spend Saturday. Source: Author*

Now check what happens next. The crack gets its trip, and its bonus drops to 0.185. If its average stays at 0.58, the crack wins the next three trips as well, and then the streamway is back on top. The search settles this argument at every junction, hundreds of times, before it plays a single move.

## October 2015, and then March 2016

In October 2015, AlphaGo played Fan Hui, the European champion, in five formal games and won all five. [The paper](https://www.nature.com/articles/nature16961) came out in Nature that January. In [a Wired article](https://www.wired.com/2014/05/the-world-of-computer-go/) from May 2014, Coulom had guessed that a machine beating a professional without a head start (a handicap) was "maybe ten years" away. It took less than two.

In March 2016, in Seoul, AlphaGo played Lee Sedol and won 4–1. Two moves from that match are famous, one from each side, and both come down to the prior.

In game two, AlphaGo played move 37, a shoulder hit on the fifth line. That is a stone placed much further from the edge than professionals thought sensible, and some commentators called it a mistake. Lee got up, left the room, and took nearly fifteen minutes to reply. AlphaGo's own policy network put the chance of a human playing it at 1 in 10,000. But a tiny prior means few trips, not none. The search walked move 37 enough times to find that it was good, and AlphaGo went on to win the game.

In game four, Lee played move 78, a wedge right into the middle of AlphaGo's position. AlphaGo's policy network had given that move 1 in 10,000 too. This time the few trips it got were not enough to show the danger. Demis Hassabis said afterwards that AlphaGo's mistake was its reply, move 79, and that it only realised this around move 87. Go players call Lee's move the divine move, and Lee won the game. Lee retired in November 2019. "Even if I become the number one," he told Yonhap, "there is an entity that cannot be defeated."

## AlphaGo Zero: the search becomes the teacher

AlphaGo learned first from 28.4 million positions of human games. So how much of its strength actually needed them? The answer came in [Nature in October 2017](https://www.nature.com/articles/nature24270), with AlphaGo Zero: none of it.

AlphaGo Zero drops the human games, the rollouts, the RL stage and the separate networks. It keeps one network with two outputs (heads), written $f_\theta(s) = (p, v)$, where $\theta$ is the network's weights. The policy head $p$ gives a probability for every move, and the search uses it as the prior. The value head $v$ gives one number for who is winning, and the search uses it to score each new junction.

The search plays better than the network does on its own, because it is the network plus 1,600 trips down real passages. In the paper's words, MCTS "may therefore be viewed as a powerful policy improvement operator". So AlphaGo Zero takes what the search decided, and trains the network to have guessed that in the first place. The visit counts become the training label:

$$\pi(a \vert s) = \frac{N(s,a)^{1/\tau}}{\sum_b N(s,b)^{1/\tau}}$$

where $\pi(a \vert s)$ is the label for move $a$ in position $s$, $N(s,a)$ is the visit count from the search that just finished, and $\tau$ is a temperature that sets how sharp the label is. With $\tau = 1$, this is just each move's share of the visits. In Figure 3, D4 got 412 of 800 visits, so its label is 0.52. For the first 30 moves of a game $\tau = 1$, so the label keeps its spread and the games stay varied. After that, $\tau$ goes towards zero and the label becomes "the most-visited move, and nothing else".

Every position from a self-play game becomes one training example. It has the position $s$, the label $\pi$ and the final result of that game $z$. The result is $+1$ for a win and $-1$ for a loss. Training makes this loss as small as it can:

$$\ell = (z - v)^2 - \pi^\top \log p + c\lVert\theta\rVert^2$$

The first term pulls the value head towards the result that actually happened. The second is the cross entropy from the [cross entropy post](/blog/cross-entropy-loss/): for every move, multiply the label by the log of the network's probability, add them up, and flip the sign. It pulls the policy head towards the visit counts. The third is weight decay, a small penalty with a constant $c$ that keeps the weights from growing large.

On day one the network is random, so the first searches are poor. But each search still adds two things the network does not have: 1,600 trips of looking ahead, and the real result of the game at the end. So the label is always a little better than the network, and the network catches up a little at a time. Then the better network guides a better search, and the loop goes round again.

![The self-play loop as three boxes, with a zoom panel showing visit counts becoming the policy label](/images/blog40/selfplay-loop.png) *Figure 3: the self-play loop, drawn with AlphaZero's 800 simulations a move (AlphaGo Zero used 1,600). The only thing coming in from outside is the rules of the game. Source: Author*

It passed the version that beat Lee Sedol after 36 hours of training. After three days and 4.9 million games against itself, it beat that version 100 games to 0.

The number I find most interesting is in the same paper. The final AlphaGo Zero network, after 40 days of training, rates 3,055 Elo when it just plays its highest-probability move with no search. The same weights with the search wrapped around them rate 5,185.

![Bar chart of four Elo ratings with the gap between raw network and searched network marked](/images/blog40/search-ablation.png) *Figure 4: AlphaGo Zero's network on its own against the same network with search, at 5 seconds a move, with AlphaGo Fan and AlphaGo Lee in grey for scale. Source: Author*

That is 2,130 Elo between the same weights with and without search. On paper, the network on its own would win about one game in two hundred thousand against the same network with search. So all of that extra strength comes from the trips taken before each move. On its own, the network plays a little below the AlphaGo that beat Fan Hui (3,144). That is excellent instincts and no patience whatsoever.

## Where PPO comes in

PPO is the reinforcement learning algorithm OpenAI used to fine-tune InstructGPT, the model behind ChatGPT, and the [GRPO post](/blog/grpo-rlvr/) goes through it in detail. Here is the short version. The policy plays. For each action, a second network (the critic) guesses how well things should go from there, and the **advantage** is how much better or worse they actually went. The update makes actions with a positive advantage more likely and the rest less likely. And a clip, usually set to 0.2, stops any one update from moving the policy too far from the one that played the games.

AlphaGo's step 2 was the simplest member of this family. REINFORCE uses the game result $z$ where PPO uses the advantage, and it has no clip.

So why did AlphaGo Zero throw that step out? PPO and AlphaGo Zero answer the same question: how do you find a policy slightly better than the one you have, and then move the network towards it? They just find the better policy in different places.

- PPO finds the better policy by trial and error. It plays whole games, sees which moves beat expectations, and nudges. The signal for any one move is weak, because a win or a loss at move 150 says little about move 12.
- AlphaGo Zero finds it by lookahead. At every position, the search works out a better policy right there, 1,600 trips' worth, and the network copies it. The signal is strong at every move. But it needs a simulator.

The two are closer than they look. [Grill et al. (2020)](https://arxiv.org/abs/2007.12509) showed that AlphaZero's visit counts approximately solve a tidy problem. Choose the policy that scores best on the search's $Q$ values, minus a penalty for moving away from the network's prior:

$$\bar{\pi} = \arg\max_y \left[\, Q^\top y - \lambda_N \,\mathrm{KL}(P \,\Vert\, y) \,\right]$$

where $y$ is any candidate policy over the moves, $Q^\top y$ is its average $Q$, $\mathrm{KL}(P \Vert y)$ measures how far it has moved from the prior $P$, and $\lambda_N$ is a weight that shrinks as the number of simulations $N$ grows, roughly as $1/\sqrt{N}$. So early in the search the prior dominates, and after many trips the $Q$ values do.

That is the shape of PPO's update too: improve, but stay close to the policy you had. PPO enforces it with the clip, and the RLHF version adds a KL penalty against a frozen copy, as in the GRPO post. Grill et al. tie AlphaZero most directly to MPO, another method in that family. So one way to read AlphaZero is as a policy update like PPO's, where the improved policy is worked out by lookahead at every position instead of estimated from games already played. The same loop turned up independently in 2017 as **Expert Iteration**, where [Anthony, Tian and Barber](https://arxiv.org/abs/1705.08439) trained a network (the apprentice) to imitate a tree search (the expert) at the game Hex.

| | PPO | AlphaGo Zero and AlphaZero |
|---|---|---|
| where the better policy comes from | moves that beat the critic's guess, in games already played | the search's visit counts, at every position |
| policy training signal | advantage-weighted log-probability, clipped | cross entropy towards $\pi$ |
| value training signal | critic, trained on the rewards that followed | value head, trained on the result $z$ |
| what keeps each step small | the clip, plus a KL penalty in RLHF | the prior's pull in PUCT, which Grill et al. write as a KL penalty |
| needs a simulator | no | yes, or a learned one (MuZero, below) |

The 3,055 against 5,185 result matters for language models too. It says you can make fixed weights stronger by spending more compute at the moment of answering. Reasoning models like DeepSeek-R1 make the same bet: they think for longer before they answer. GRPO trains them with a trick like AlphaGo Zero's label, without the tree. It samples a batch of answers, checks which ones are right, and trains the model towards those.

But a search needs something to score its trips. Chess has its rules, and Lean has its proof checker. An essay or an email has neither. So a search over a model's reasoning steps is only as good as whatever scores those steps. And if that scorer is itself a learned model, training will find and exploit its mistakes faster than anyone can patch them.

## One algorithm, three games

AlphaGo Zero still knew it was playing Go. A Go board means the same thing when you rotate it or mirror it, so AlphaGo Zero got eight training positions out of every one. A chess board does not, because pawns only move one way. AlphaZero ([the December 2017 preprint](https://arxiv.org/abs/1712.01815), and then [Science in December 2018](https://www.science.org/doi/10.1126/science.aar6404)) took those Go-specific parts out. It used the same code and the same settings for Go, chess and shogi (Japanese chess), with one exception.

**NOTE:** the exception is noise. AlphaZero mixes random noise into the priors at the root of the tree, so even a move the network hates gets walked now and then. The setting is 0.3 for chess, 0.15 for shogi and 0.03 for Go, shrunk in proportion to how many legal moves each game usually has.

5,000 first-generation TPUs (Google's own AI chips) played the self-play games, and 64 second-generation TPUs trained the network on them. Training took nine hours for chess, twelve for shogi and thirteen days for Go.

In the Science match, AlphaZero looked at about 60,000 positions a second, against Stockfish's 60 million. That is a thousand times fewer, because the priors point the search at the few moves worth checking.

In the preprint's 100-game match against Stockfish 8, AlphaZero won 28 games, drew 72 and lost none. In the Science paper the match ran to 1,000 games. AlphaZero won 155 and lost 6, and the other 839 were draws.

## MuZero does not get the rulebook

AlphaZero still needs the rules. The search has to know which position a move leads to before it can walk there. [MuZero](https://arxiv.org/abs/1911.08265) (DeepMind, Nature 2020) takes the rules away too. Instead, it learns its own internal picture of the game (a hidden state), and a way to step that picture forward one move. The hidden state only has to predict three things: the reward, the policy and the value. The reward is the points scored along the way, and in a board game that is just the win or loss at the end. Those are the only three things the search ever asks for. So nothing forces the hidden state to look like a board, and it does not.

The [JEPA post](/blog/jepa-nobody-cares-about-the-wallpaper/) makes the same argument about images: predict only what the job needs, and skip the pixels. MuZero matched AlphaZero on Go, chess and shogi without ever being told how the pieces move. It also learned 57 Atari games, where nobody hands you the rules anyway.

## Where it went after board games

- **[AlphaDev](https://www.nature.com/articles/s41586-023-06004-9)** turned writing assembly code into a game, and found shorter sorting routines. They are now in the C++ standard library that ships with LLVM. **[AlphaTensor](https://www.nature.com/articles/s41586-022-05172-4)** did the same for matrix multiplication, and beat Strassen's 1969 method for 4 by 4 matrices, in arithmetic where every number is 0 or 1 (47 multiplications against 49).
- **[MuZero](https://deepmind.google/blog/muzero-alphazero-and-alphadev-optimizing-computer-systems/)** picks the VP9 video compression settings for some YouTube videos, and saves about 4% of the bitrate.
- **[AlphaProof](https://www.nature.com/articles/s41586-025-09833-y)** runs the same loop over proofs written in [Lean](https://lean-lang.org/), a language in which a computer checks every step of a proof. It solved three of the six problems at the 2024 International Mathematical Olympiad, including the hardest one, and a sister system (AlphaGeometry 2) solved a fourth.
- **[Leela Chess Zero](https://lczero.org/)** and **[KataGo](https://github.com/lightvector/KataGo)** are open-source versions for chess and Go that anyone can run.

## The honest cons

**DeepMind set up the 2017 match.** In the preprint, Stockfish 8 got a fixed minute per move. It also had a 1 GB hash table (its memory of positions it has already looked at) and no opening book (a database of known good opening moves). Engines are not normally tested like that, and chess players said so. The Science paper answered most of it, with 1,000 games, a newer Stockfish, opening books, and matches where AlphaZero got only a tenth of Stockfish's thinking time. AlphaZero still won. But DeepMind still chose the Stockfish and the settings.

**Learning from scratch cost 5,000 TPUs.** No human games went in, but a lot of hardware did. Nine hours on 5,000 TPUs is about 45,000 TPU-hours, or around five years on a single chip. Leela Chess Zero reproduced AlphaZero on volunteers' computers, and it took years.

**Superhuman, until somebody plays it strangely.** [Adversarial Policies Beat Superhuman Go AIs](https://arxiv.org/abs/2211.00241) (Wang et al., ICML 2023) trained an opponent specifically to beat KataGo running at superhuman settings. It won more than 97% of its games. And that opponent plays terrible Go. It sets up one unusual shape, a ring-shaped group, that KataGo misjudges, and it loses to most human amateurs. Self-play never produced that shape often enough for KataGo's network to learn it. A human Go player learned the trick from the attacker and beat superhuman programs with it by hand. And after KataGo was retrained to defend against it, a fine-tuned attacker still won almost half its games.

## Conclusion

AlphaGo gave the club a nose and a draught, the policy and value networks. That was enough to beat Lee Sedol. AlphaGo Zero then turned the loop round, so that the search trains the network that guides the search. Seen from reinforcement learning, that is a policy update like PPO's, where the better policy comes from lookahead instead of trial and error.

AlphaZero plays chess far better than any human. But it still guesses, so on its own it will never solve the game. This kind of search can also look for proofs, and AlphaProof already does that in Lean. That is how I think chess finally gets solved. An AI will search over proofs the way AlphaZero searches over moves, until it finds the pruning theorems that shrink the tree to something small enough to walk. On that day chess gets a finished map, and nobody will have had to walk every passage to draw it.

And now you know. Fin.
