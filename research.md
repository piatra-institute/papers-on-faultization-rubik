# Research

Findings tiered per research-pipeline.md. Every citation verified against Crossref or the standard bibliographic record before use; locators below and in sources.md. The seed chat (chats/chat.md) is a deep-research report that supplied the program, the fault taxonomy, the theoretical propositions, and a set of self-computed exhaustive numbers; its prose is not reused, and its computed numbers are treated as unverified claims to be reproduced or corrected by this paper's own computation (see Seed corrections).

## The precedent experiment (T1)

**Zhang, Goldstein and Levin (2025)**, Adaptive Behavior 33(1): 25–54 (10.1177/10597123241269740), "Classical sorting algorithms as a model of morphogenesis." The reconstruction that matters:

- What was decentralized: array entries became cell agents with (position, value, algotype), each in its own thread; a main thread activates, monitors, and kills; a global lock serializes swaps; a coin flip gates each lock acquisition. Distributed in action selection, with a global scheduler, a global lock, and a global termination monitor retained.
- Locality varies by algotype: cell-view Bubble is nearest-neighbor local; cell-view Insertion reads all cells to its left plus a global property of its right suffix; cell-view Selection carries explicit positional targets. Decentralized and local are different properties.
- Faults: frozen cells, passive (can be displaced) versus stuck (cannot move at all); arrays of 100, at 1 to 3 frozen cells. Reported final monotonicity errors differ by fault semantics, and the ranking of algorithms reverses between passive and stuck: robustness is fault-model-specific.
- Delayed gratification: a statistic built from decreases and later increases of sortedness; cell-view Bubble's mean rose from 0.24 with no frozen cells to 0.37 with 3; Insertion from 1.10 to 1.19; Selection showed no clear trend. The authors themselves note a random walker also moves away from targets and call for barrier-conditioned tests; they also state the implementation can be classified with random sorting algorithms and that there is no magic beyond the rules.
- Chimeric mixtures of algotypes all sorted; algotypes transiently clustered (peak aggregation 0.72 for Bubble with Selection); the follow-up analysis attributes much of the clustering to policy-speed differences. Opposite-direction mixtures reached stable macroscopic compromises.

What the experiment established: fault-model-specific robustness of distributed implementations, nonmonotonic problem-space trajectories, heterogeneous-policy completion, policy-correlated clustering, stable compromises under target conflict. What it did not establish: representation of future benefit, causal contribution of regressions to success, superiority over matched stochastic search. The neutral name for the headline effect is barrier-correlated nonmonotonic progress.

## The formal ancestor (T1)

- **Dijkstra (1974)**, CACM 17(11): 643–644 (10.1145/361179.361202): self-stabilization; convergence from arbitrary initial state plus closure, with no dedicated recovery routine. Recovery without a fault handler was formalized here, 5 decades before it could be offered as evidence of basal cognition.
- **Schneider (1993)**, ACM Computing Surveys 25(1): 45–67: the survey form of the concept.
- **Herman (1990)**, Information Processing Letters 35(2): 63–67: probabilistic self-stabilization; randomization creates convergence where deterministic symmetry forbids it; the license for calling stochastic convergence by its right name.
- **Ghosh, Gupta, Herman and Pemmaraju (1996)**, PODC: 45–54: fault containment; disruption radius and recovery cost should scale with the fault, a sharper metric than eventual recovery.
- **Lamport, Shostak and Pease (1982)**, TOPLAS 4(3): 382–401: the Byzantine frame for adversarial components.
- **Naor and Stockmeyer (1995)**, SIAM J. Computing 24(6): 1259–1277: what can be computed locally at all; **Angluin, Aspnes, Diamadi, Fischer and Peralta (2006)**, Distributed Computing 18: 235–253: population protocols; anonymity, symmetry, and scheduling decide computability, not just efficiency.

## The traditions the term must exceed (T1)

- **Avizienis, Laprie, Randell and Landwehr (2004)**, IEEE TDSC 1(1): 11–33: fault, error, failure; the dependability taxonomy the fault classes inherit.
- **Hsueh, Tsai and Iyer (1997)**, Computer 30(4): 75–82: fault injection.
- **Basiri et al. (2016)**, IEEE Software 33(3): 35–41: chaos engineering.
- **von Neumann (1956)**, in *Automata Studies*: reliable organisms from unreliable components.
- **Edelman and Gally (2001)**, PNAS 98(24): 13763–13768: degeneracy against redundancy; structurally different components with overlapping function.
- **Mordvintsev, Randazzo, Niklasson and Levin (2020)**, Distill (10.23915/distill.00023): growing neural cellular automata; regeneration is trained on damaged states, the standing caveat against "repair was never implemented."
- **Mitchell, Crutchfield and Hraber (1994)**, Physica D 75: 361–391: evolved emergent computation in cellular automata.
- **Kirkpatrick, Gelatt and Vecchi (1983)**, Science 220: 671–680; **Gammaitoni, Hänggi, Jung and Marchesoni (1998)**, Reviews of Modern Physics 70: 223–287: the two ordinary explanations for beneficial noise, annealing and stochastic resonance.

## The agency ladder (T1)

- **Rosenblueth, Wiener and Bigelow (1943)**, Philosophy of Science 10(1): 18–24: purpose as negative feedback.
- **Ashby (1956)**, *An Introduction to Cybernetics*; **Conant and Ashby (1970)**, Int. J. Systems Science 1(2): 89–97: every good regulator is a model of its system.
- **Dennett (1987)**, *The Intentional Stance*: goal language licensed by predictive utility.
- **Barandiaran, Di Paolo and Rohde (2009)**, Adaptive Behavior 17(5): 367–386: the enactive bar: individuality, normativity, asymmetry; a software cube does not clear it.
- **Bich and Bechtel (2022)**, Adaptive Behavior 30(5): 389–407: control mechanisms as the middle vocabulary.
- **Levin (2022)**, Frontiers in Systems Neuroscience 16: 768201: the TAME framework; **Fields and Levin (2022)**, Entropy 24(6): 819: competency in navigating arbitrary spaces as the invariant.

## The cube's mathematics (T1)

- **Rokicki, Kociemba, Davidson and Dethridge (2014)**, SIAM Review 56(4): 645–670: God's number is 20 in the half-turn metric for the 3×3×3; 43,252,003,274,489,856,000 states.
- **Korf (1997)**, AAAI-97: 700–705: pattern databases; the centralized control condition.
- **Joyner (2008)**, *Adventures in Group Theory* (Johns Hopkins): the cube group at textbook level.
- Pocket cube facts recomputed in this paper's simulation rather than cited: 3,674,160 fixed-corner states (7! × 3^6), 88,179,840 absolute states (8! × 3^7), half-turn-metric diameter 11 with the published distance shells (1, 9, 54, 321, 1,847, 9,992, 50,136, 227,536, 870,072, 1,887,748, 623,800, 2,644). Reproducing this table is the simulation's calibration gate.

## Theoretical propositions carried by the paper (T1, proved in text or verified by computation)

1. **No open-loop collapse**: a fixed move sequence is a permutation of the state set and cannot map two states to one; no universal solving word exists.
2. **The trivial-solver control**: a random walk with a stop-at-target rule converges from every state almost surely; universal convergence alone is therefore nearly worthless as evidence of competence.
3. **The spanning-tree possibility**: a globally informed feedback policy with the target as unique attractor always exists on a finite connected graph; every locality-induced failure is an information fact, not a group-structure fact.
4. **Reversibility is no obstruction**: state-dependent controllers induce many-to-one maps; attractors, basins, and cycles are available despite bijective generators.
5. **Closure needs a no-op**: if a face must turn every step, the solved state cannot be absorbing.
6. **Strict potential ascent cannot cycle**: an arbiter that only accepts strict improvements of a summed local potential admits no cycles of length above 1; every chimera equilibrium under it is a local maximum of the potential.
7. **Conjugacy of retargeting**: a fully target-relative controller retargeted to any reachable configuration has dynamics conjugate by group translation; basin sizes are exactly invariant.
8. **The parity hole**: no legal state has exactly 6 of the 7 moving corners correct; the group's permutation and orientation constraints force the seventh.

## Seed corrections

- The seed's exhaustive numbers (solved basin 61 of 3,674,160; 758,286 strict-controller fixed points; final-correct-corner distribution; plateau ecology of 145,953 attractors with cycles of lengths 1 to 4; heterogeneous-weight basin about 165) are its own computations, not literature. This paper recomputes all of them from a fully specified controller and reports its own numbers; agreement is noted where it occurs and this paper's numbers govern where it does not.
- The seed's claim that the 2×2 half-turn diameter is 11 and quarter-turn 14 matches the standard record; the paper relies on its own breadth-first search for the former and does not use the latter.
- The seed cites an arXiv item for the 2×2 diameter; the paper instead treats the shell table as a reproduced computational anchor, and cites Rokicki et al. only for the 3×3×3 result.
- Bongard was not an author of the sorting study; the seed itself notes this and the paper follows.
- The seed's Sacco, Sakthivadivel and Levin topological-constraints item is real but peripheral here; dropped to keep the bibliography load-bearing.
- The Levin-paper statistics quoted in prose (0.24 to 0.37; 1.10 to 1.19; aggregation 0.72; the frozen-cell error table) enter results.json as cited records with the paper as source.
