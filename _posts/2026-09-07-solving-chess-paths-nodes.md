---
layout: post
title:  "Solving Chess - Paths, Nodes and the Proof Nobody Has"
date:   2026-09-07
image:  images/blog30/cover.webp
description: "Musk and Chess.com were counting different things. Solving chess was never about the tree's size, but about proving which branches you can skip."
tags: [essay, game-theory, graph-algorithms, reinforcement-learning]
---

*On the cover: the argument in question, 3 and 4 September 2026. Six million views between them, and both sides got a number right, which for that website is a record.*

Imagine you are a prosecutor and the charge is that chess, played perfectly, is a draw. Your judge has never seen a chessboard and will not take anything on trust. Every claim in the file has to be proved from the rules alone, and the defence gets to object to every single sentence. How thick is the file? Who has to be called as a witness, and, more to the point, who are you allowed to leave out?

Nobody in the six million views asked that, so hold it in your head while I set the scene.

On the third of September, Massimo posted one of those charts about how fast chess explodes: 20 moves to start with, over 400 after one move each, around 8,900 by the third, nearly 200,000 by the fourth, with a hand-drawn game tree underneath from the era when people drew these by hand. Elon Musk replied that the number of moves in chess that aren't utterly stupid is tiny, and that "chess will be fully solved one day".

There is already a mistake in those four numbers, and the next two days of argument were built on it. They count *orders in which moves can be played*, not distinct arrangements of the board. Play 1.Nf3 Nf6 2.Ng1 Ng8 and both sides are back exactly where they started, having achieved nothing whatsoever, and that counts as a fresh sequence. The [published counts](https://www.chessprogramming.org/Perft_Results) are 20, 400, 8,902 and 197,281, and every one of them is a count of sequences.

Chess.com then arrived with a bigger number. There are more possible chess games than atoms in the observable universe, by about forty orders of magnitude, and "to solve chess, you'd have to map them all".

Musk corrected them, and he was right to. Games and positions are different things, and legal positions come in about forty orders of magnitude *below* the atom count, not above. He added that a superintelligence will find ways to solve and compress the problem that we could not begin to follow, and signed off by noting he was arguing with a random intern at a chess website.

So one side was counting sequences, the other was counting arrangements, and both were sure the other had failed arithmetic. In courtroom terms, Chess.com was counting every order in which the witnesses could be called, Musk was counting the witnesses, and neither of them said a word about what the judge actually needs to see. This is the story of why a proof can be astronomically smaller than the tree it is a proof about, and why chess is still unsolved for a reason that has nothing to do with the size of the universe.

## Paths and nodes

Draw the game tree properly and most of the confusion goes away.

The root is the starting position. Every edge is a legal move and every node is the position you arrive at. A **game** is one path from the root down to a leaf where somebody is mated or the draw rules bite. A **position** is a node. The witness is the node. The path is just the story of how the witness got to the courthouse, and the judge does not care whether they took the bus.

Why do paths outnumber nodes so badly? Because different move orders land on the same arrangement of pieces, so many paths run through the same node. Chess programmers call this a **transposition**, and they call those counts from the opening post **perft**, short for performance test, which is what you run to check that a move generator has not lost its mind. The [wiki that publishes them](https://www.chessprogramming.org/Perft) says outright that what is counted is move paths.

- Paths, all the way down: about $10^{120}$, Shannon's estimate.
- Distinct nodes: about $4.82 \times 10^{44}$.
- Atoms in the observable universe: about $10^{80}$, for reference, since everybody insists on it.

Chess.com's forty orders of magnitude above the atoms is right, for paths. Musk's forty below is roughly right, for nodes, the real gap being nearer 36. That is two accurate numbers describing two different objects, fired at each other for two days. I have had arguments like that about whose turn it is to do the dishes, and they also did not end in a proof.

![Bar chart of six counts on a log axis, from checkers proof nodes at the bottom to Shannon's game count at the top](/images/blog30/number_ladder.png) *Figure 1: Every number anyone quoted, as orders of magnitude. The bottom bar is the only quantity on this chart that a human being has ever finished computing, and it took eighteen years. Source: Author*

The two big numbers are not even the same kind of number. Shannon's $10^{120}$ is a napkin, from [Programming a Computer for Playing Chess](https://vision.unipv.it/IA1/ProgrammingaComputerforPlayingChess.pdf) in 1950: take forty moves a side and about thirty options each, so a move-pair contributes $30 \times 30 \approx 10^3$, and forty of those gives $(10^3)^{40} = 10^{120}$. That is the entire derivation, with no error bar, because Shannon wanted to show brute force was hopeless and a napkin was enough for that. It is still quoted 75 years later as if someone had measured it, which tells you how much anyone has checked.

The node count is a real measurement, and it is the better story.

## Counting witnesses with darts

How do you count $10^{44}$ distinct chess positions when nobody has the list and nobody ever will? John Tromp did it the way you measure a lake with a wiggly shoreline. Draw a rectangle around it whose area you know exactly, throw darts at random, and count the fraction that land wet. Five percent wet means the lake is five percent of the rectangle, and you never had to trace the coast.

The rectangle here is a bigger, sloppier set: every way of arranging pieces on a board plus the extra state (whose move, castling rights, en passant), including arrangements no real game could ever produce. Its size is a closed-form product and comes to $N \approx 8.7 \times 10^{45}$. A short Haskell program prints it in under ten seconds, which is the last thing in this section that is fast.

Then comes the dart. You cannot sample uniformly from $10^{45}$ things by shuffling them, so you number them instead: an invertible **ranking**, a bijection between the integers $0 \ldots N-1$ and the arrangements. A random dart is now a random integer, which is free. Building that bijection is the real contribution of [Tromp's work](https://github.com/tromp/ChessPositionRanking), stitched together from fourteen smaller ranking functions with names like `sandwichRanking` and `epOppRanking`, and I refuse to believe the sandwich one was named soberly.

Then check each dart for legality, meaning some path from the root actually reaches it. Across two million samples, 5.53% came back legal, so the lake is 5.53% of the rectangle:

$$L = (4.82 \pm 0.03) \times 10^{44} \quad \text{at 95\% confidence}$$

Two million darts to pin down a number with 44 zeros in it, to within a percent. Statistics is a ridiculous discipline and I love it.

**NOTE:** the ranked objects are not quite positions. Tromp calls them urpositions, and one position can be hit by several ranks, so each hit is weighted by the inverse of that multiplicity. The average correction is about 0.98, small enough to skip in conversation and not small enough to skip in the code.

There is a sting in the legality check. Deciding whether a node is even reachable means [retrograde analysis](https://en.wikipedia.org/wiki/Retrograde_analysis), reasoning backwards about how a position could have arisen rather than forwards about what happens next, and that has been [proven PSPACE-hard](https://arxiv.org/abs/2010.09271) on arbitrarily large boards. So merely asking whether a witness could have been in the room is, in general, a hard problem in its own right.

One honest caveat before anyone quotes that at a party. Complexity classes describe families that grow with input size. Standard chess is 8x8 and finite, so formally it is a constant, solvable in $O(1)$ by a lookup table you would merely have to build first. The theorem says the difficulty is structural rather than a failure of imagination, and it says nothing about whether 8x8 chess is tractable.

## What a conviction actually needs

Now the part that decides the argument, and it has nothing to do with size.

Solving a game means more than finding the line both sides play when both play perfectly. That line is one path, and it would be worthless the instant your opponent stepped off it. Which they will, because they are not obliged to lose the way you planned.

A solution is a **strategy**, and it has to survive anything the other side does. There are two grades of it:

- A **weak solution** gives the value of the root (White wins, Black wins, or draw), plus a strategy that achieves that value against every defence.
- A **strong solution** gives perfect play from every node. The complete answer book, including for positions no sane player would ever reach.

People tie themselves up here because both readings of "perfect play" are true at once. A solution assigns one of three words to the root, and that single word is the both-play-perfectly answer. But what *earns* the word is a strategy covering every branch. The verdict is one word, the case file is the thing that entitles you to say it, and it is the case file we are arguing about.

## The shape of a case file

Here is why the file is a small fraction of the tree it settles, and it comes down to whose turn it is.

At nodes where the **defence** moves, you must have an answer to every edge. All of them, because the defence picks, and a hole in your file is an acquittal.

At nodes where **you** move, you need one edge that works. Find a reply that holds and every sibling edge falls out of the file, because you were never obliged to play them. You are the prosecution, so you get to choose which argument you make.

Branch wide on their turns, branch by one on yours, and that single asymmetry is the whole reason solving anything is possible at all.

![Three-level game tree with one solid blue edge at your nodes, three red edges at theirs, and dashed grey edges dropped](/images/blog30/proof_tree_asymmetry.png) *Figure 2: The proof keeps every edge on the opponent's turns and one edge on yours. Dashed grey edges are moves you are allowed to never think about, which is more than I can say for my own games. Source: Author*

How big does that make the file? Brace yourselves, there are exponents. Roughly,

$$|\text{proof}| \approx \sqrt{|\text{full tree}|}$$

specifically, if the branching factor is $b$ and the game runs $d$ plies deep, the full tree has $b^{d}$ leaves and the minimal proof tree has about

$$|P| \approx b^{d/2}$$

which is the same square-root bound Knuth and Moore proved for [alpha-beta pruning](https://www.sciencedirect.com/science/article/abs/pii/0004370275900193) in 1975.

Feel the exponents. Chess has $b \approx 35$ and a game runs about 80 ply, a ply being one move by one side. The full tree is $35^{80} \approx 10^{123}$, which is Shannon's napkin arrived at from a different direction. The square root is $35^{40} \approx 10^{62}$. Sixty orders of magnitude off the top, for free, from one observation about whose turn it is. I have never had a Tuesday go that well.

Now, $10^{62}$ is still ridiculous, but notice that it sits *above* the node count of $10^{44}$, which caps it, since a proof that revisits a position can look it up instead of re-deriving it. So the number that governs whether chess can be solved is somewhere below $10^{44}$, and exactly where is the question nobody can answer. That number, and not either of the two in the screenshots, is what decides whether Musk is right.

## Checkers, the one case anyone has closed

We have exactly one worked example, and it is the reason Musk's side of this is not silly.

Checkers has about $5 \times 10^{20}$ nodes. Jonathan Schaeffer's team at Alberta spent 18.5 years on it and announced in April 2007 that [checkers is solved](https://www.cs.mcgill.ca/~dprecup/courses/AI/Materials/checkers_is_solved.pdf): perfect play is a draw. Eighteen and a half years is long enough to start the project as a postdoc and finish it as somebody's dean.

The number to walk away with is $10^{14}$, which is how many nodes the proof actually touched, one in five million of the total. The rest was proved irrelevant and discarded, using proof-number search, an idea from [Victor Allis's 1994 thesis](http://fragrieu.free.fr/SearchingForSolutions.pdf) that keeps a running estimate of how many more nodes a proof still needs and heads for the cheapest one.

So mapping every path is not what solving takes, and the counterexample is not obscure. It is the one game anyone has ever finished, named in the thread by the person Chess.com was arguing with, two posts earlier.

## But Stockfish never loses

The obvious objection, and it deserves a real answer, because [AlphaZero](https://www.science.org/doi/10.1126/science.aar6404) is one of the better things to happen to this field. If an engine has not lost a game to a human in twenty years, isn't chess solved in every sense that matters?

AlphaZero has two parts. A network that looks at a single node and returns a rough score plus a hunch about which edges deserve attention, and a search that walks paths, but only the ones the hunch points down. Nothing is ever enumerated. The weights are a lossy compression of millions of self-played games, consulted instead of the tree.

The contrast in the paper is lovely: AlphaZero examined about 60,000 nodes a second against Stockfish's 60 million, and won. A thousandth as many nodes, because they were better ones. Stockfish is the detective who interviews the entire city, sixty million people a second, and still cannot tell you why it thinks the butler did it. AlphaZero just has a feeling about the butler.

**NOTE:** the widely circulated figures are 80,000 against 70 million, from the December 2017 preprint. The 2018 *Science* paper says 60,000 against 60 million. Both get quoted. Use the second.

And that is exactly why it is not a solution. Every leaf of that search bottoms out in a guess from a learned function, and nothing inside the system can tell you which guesses are wrong. A detective who has never lost a case is a wonderful thing to have on the payroll, but the judge still wants the file.

| What you have | Covers | Proves | Verdict |
|---|---|---|---|
| 7-piece tablebase | 7 pieces of 32 | Perfect play, provably | Exact, and almost empty |
| Stockfish | The whole tree | Nothing | Overwhelming, unverified |
| AlphaZero | The whole tree | Nothing | Same, with better instincts |
| Weak solution (checkers) | Whole tree from the root | The root's value | The only one ever finished |
| Strong solution | Every node | Everything | Nobody has one for chess |

## The seven-piece answer book

We do have real proof for chess, just not much of it.

Endgame tablebases are complete for every position with up to seven pieces on the board. The game starts with thirty-two. That is the entirety of formal knowledge about chess, and it took from Ken Thompson's five-piece work in the 1980s to the Lomonosov set in 2012 to get there.

A tablebase is not built for "seven pieces" as a lump. It is built per material combination: king and queen against king and rook is one file, king rook bishop against king rook is another, and the seven-piece set is every such combination. Some individual eight-piece endings are already done, mostly pawnless ones. The complete eight-piece set is not, and what is in the way is partly size and partly the order you are allowed to do things in.

![Line chart of tablebase positions by piece count, solid blue up to seven pieces, dashed red to eight, on a log axis](/images/blog30/tablebase_growth.png) *Figure 3: Nodes by piece count, log scale. Blue is finished, red has been running for years. Note where 32 would go, which is off the right of your screen and then off the right of the building. Source: Author*

Each extra piece multiplies the count by roughly a thousand, because the new piece can stand anywhere in every arrangement you already had. Seven pieces is 18.5 TB in the compact Syzygy encoding and was 140 TB in the original Lomonosov format. Eight lands in the petabytes, and the seven-piece set already does not fit on any laptop I have ever owned, including the one I told myself to buy for exactly this reason.

The ordering problem is subtler. These files are built backwards from checkmate, so a node's value needs the values of everything it can turn into. Captures drop you into a smaller material set and promotions drop you into a different one, so every eight-piece file sits on a stack of seven-piece files that must be finished first. Pawnless combinations go first precisely because promotion is not in their dependency graph.

## Suppose somebody handed you every node

Let's be generous to the optimists and hand them the full witness list. All $10^{44}$ of them, sitting on a disk, labelled. What is left to do?

The algorithm is the easy part, four lines that tablebase generation already runs:

1. Label the terminal nodes. Checkmate is a loss for the side to move, stalemate is a draw.
2. Sweep the set. A node is a win if **any** edge leads to a node labelled a loss for the opponent, and a loss if **every** edge leads to a win for them.
3. Repeat until a pass changes nothing.
4. Whatever is still unlabelled is a draw. Read off the root.

What kills it is plumbing. One label per node at two bits is about $2.5 \times 10^{43}$ bytes, against total human storage somewhere around $10^{23}$, so we are short by twenty orders of magnitude before anyone has written a line of code. Worse, this is not a stream you can chew through in chunks. Each sweep needs the predecessors of nodes scattered anywhere in the array, so it is random access across the whole thing, and that is already the binding constraint at seven pieces, where the bottleneck is I/O rather than arithmetic.

And then, because I could not resist, thermodynamics. Landauer's limit puts the cost of erasing a bit at $kT \ln 2 \approx 2.9 \times 10^{-21}$ J at room temperature. Writing $10^{44}$ bits once, at the floor, with zero overhead, is around $3 \times 10^{23}$ J, which is a few centuries of total human energy production for one pass, and forced wins in the seven-piece tables already run past 500 moves. (That arithmetic is mine. Treat it as a sanity check, not a citation.)

Also the premise was false. Nobody has the $10^{44}$ nodes. We have an estimate of how many there are, from two million darts.

## Conclusion

Musk might be right, and the strongest version of his argument is better than the one he made. He is claiming a weak solve, and weak solves genuinely do not need the full witness list. Checkers proves that. When he says the number of non-stupid moves is tiny, he is pointing at exactly the pruning that made Chinook possible, and everyone dunking on him with the atom count is refuting a claim he did not make.

Where it runs aground, for me, is his next sentence, the one about a superintelligence finding compressions we could not follow. A judge does not accept "trust me, the rest was irrelevant". Pruning has to be **proved** safe, and we have exactly one sound rule for dismissing branches of a game tree unexamined. Alpha-beta: proposed by John McCarthy at the Dartmouth workshop in 1956, written up by Hart and Edwards in 1961, published by Brudno in 1963, analysed by Knuth and Moore in 1975, four papers over nineteen years for one idea, and it discards edges that are provably irrelevant given the values already in hand. Everything a modern engine layers on top of it, null-move, late-move reductions, futility pruning, is a heuristic, a bet that a branch was not worth walking, which is why Stockfish is terrifying and why it proves nothing.

That is seventy years and one admissible rule. Maybe a machine finds the second one. There is no evidence that it will and none that it won't, and I notice that both sides of that thread were performing confidence about a question with no evidence on it.

So the tree was never the obstacle. Shannon knew in 1950 that you would never walk it, and everything since has been about deciding which parts you are allowed to skip. Chess stays unsolved not because the universe is too small to hold the file, but because nobody can yet prove to the judge which witnesses they never had to call.

And now you know. Fin.
