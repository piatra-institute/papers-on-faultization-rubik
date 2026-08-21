# Brief

Written before research begins.

## Question

Fault tolerance asks whether a designed function survives damage. Turn the question around: what does damage reveal? When a centralized algorithm is deliberately decomposed into locally competent components and those components are deleted, frozen, miscalibrated, given conflicting goals, or denied information, the interesting outcome is neither survival nor failure. It is what the perturbation makes visible: where the competence actually resides, what the arbitration layer was silently contributing, which attractors the dynamics harbored all along, and at what scale a goal-directed description of the system starts paying its way. Is there a substrate on which this entire program can be run to completion, with every state enumerated, every attractor classified, and every claim of emergence audited against exact controls? The pocket cube has 3,674,160 reachable states. All of them fit in memory.

## Claim

Faultization, the use of controlled faults as instruments rather than stressors, becomes a real method only on a substrate where nothing can hide. The paper builds that substrate and runs the program. Five moves carry it:

1. **The definition, with its burden stated.** A faultization experiment is a tuple: decomposition, observability, actuation, communication, target representation, fault model, arbitration. Noise, fault, damage, local incompetence, and distributed partial competence are five different interventions. The method is distinct from fault injection, chaos engineering, lesion studies, and self-stabilization testing only when scale is an experimental variable, the arbiter is audited, matched search controls are run, and novelty is held out. Those criteria come from the failures of weaker studies, including the one reconstructed next.
2. **The sorting precedent, reconstructed.** The Levin group's self-sorting arrays are the direct ancestor: classical sorts decomposed into cell agents, frozen cells as faults, robustness and nonmonotonic progress reported, "delayed gratification" claimed. The reconstruction separates what the experiment established (fault-model-specific robustness, policy-correlated clustering, stable compromises under conflicting targets) from what it did not (representation of future benefit, causal detours, superiority over matched stochastic search), and notes that the implementation retained a global lock, a random scheduler, and nonlocal observation in two of three cell policies. The honest renaming of its headline effect is barrier-correlated nonmonotonic progress.
3. **The microscope.** The fixed-corner pocket cube is a group of 3,674,160 elements whose Cayley graph, distance oracle, and controller-induced dynamics can be computed exhaustively. Three small theorems set the rules of evidence. Reversible moves are no obstruction to attractors, because a state-dependent controller induces a many-to-one map. A random walk with a stop rule converges from every state almost surely, so universal convergence alone is nearly worthless as evidence of competence. And a spanning tree rooted at the target always defines a globally convergent feedback policy, so the group structure forbids nothing; every impossibility found under locality is a fact about information, not about the cube.
4. **Three exhaustive mechanisms.** First, local correctness does not compose: seven agents, each knowing its own correct pose exactly and predicting every move's effect on itself perfectly, collectively solve a fraction of the state space measured in parts per hundred thousand, and a fifth of the space is a local optimum where no agent will consent to move. The parity of the group even forbids exactly six of seven agents being satisfied, so the last step of collective success is always a two-agent coincidence. Second, the cheap repairs: one bit of anti-reversal memory and a few percent of action noise each enlarge the basin, the noise curve has an interior optimum, and both effects are ordinary exploration, priced against the random-walk control that solves everything eventually and almost nothing within any useful horizon. Third, faults as instruments: deletion curves locate the redundancy; deleting a generator produces an exact algebraic impossibility region, the cleanest possible separation of incompetence from impossibility; conflicting target populations under a strict arbiter are literally potential ascent, no cycles possible, with measured compromise states that neither faction encodes; and retargeting the same controller to any reachable configuration yields exactly the same basin size by group conjugacy, a perfect factorization of machinery from target that buys no competence whatsoever.
5. **The deflationary payoff, stated as the method's success.** Nothing in these experiments exceeds distributed optimization plus exploration, and the paper says so. That is the instrument working. The cube shows what the criteria for emergent collective agency would have to rule out, because it generates every deflationary explanation in exact, enumerable form: scheduler competence, arbiter leakage, annealing dressed as insight, redundancy dressed as robustness. A claim of emergent agency that cannot survive this microscope on 3.67 million states has no business being made about a tissue.

## Kind

**formal-model + exhaustive computation**; ships a simulation that is a real complete enumeration. `has_simulation: true`, `claims_target: results.json`.

The simulation implements the fixed-corner pocket cube (Kociemba corner conventions, 9 generators over U, R, F), validates against the published distance shells and diameter 11, and then computes, exhaustively where deterministic and by exact vector iteration where stochastic: the strict local-correctness controller's full functional graph; the plateau variant's attractor spectrum; the anti-reversal-memory controller on the augmented state space; the noise sweep with the random-walk-with-stop control; deletion of 1 to 3 of the 7 agents; the orbit of the surviving generators after structural damage; chimeric target populations at every split ratio with the no-cycle potential theorem verified; target reprogramming with the conjugacy invariance checked exactly; and heterogeneous voting weights over seeded draws. Every number in the paper is either a group-theoretic fact, a published anchor reproduced, or an exhaustively computed property of a fully specified controller.

## Constraint

The paper stands alone and cites no PIATRA paper; the term faultization is presented as proposed rather than established. The seed's own computed numbers (a 61-state basin, 758,286 local optima, a 145,953-attractor ecology) are treated as unverified until this paper's computation reproduces or corrects them, and the paper reports its own numbers. Levin's program is engaged critically and respectfully: the reconstruction distinguishes the experiments from their interpretation, and the paper's deflationary findings are presented as calibration for the criteria, never as a refutation of basal cognition at large. No anthropomorphic vocabulary without operational backing. Agency claims are graded on an explicit ladder and the cube is placed honestly on it.

## Cornerstone literature

Each with one job:

- **Zhang, Goldstein and Levin** — the precedent experiment, reconstructed exactly.
- **Levin; Fields and Levin** — the competency-architecture frame the method addresses.
- **Dijkstra; Schneider; Herman** — self-stabilization: convergence and closure, the nearest formal ancestor, including its probabilistic form.
- **Ghosh, Gupta, Herman and Pemmaraju** — fault containment, the refinement the cube metrics inherit.
- **Lamport, Shostak and Pease** — the Byzantine frame for adversarial agents.
- **Naor and Stockmeyer; Angluin et al.** — what locality can compute at all; the information-threshold program.
- **Avizienis et al.; Hsueh et al.; Basiri et al.** — fault, error, failure; fault injection; chaos engineering: the traditions the term must exceed.
- **von Neumann; Edelman and Gally** — reliability from unreliable parts; degeneracy against redundancy.
- **Mordvintsev et al.; Mitchell, Crutchfield and Hraber** — trained regeneration and evolved emergent computation, with the training-embeds-the-repair caveat.
- **Kirkpatrick et al.; Gammaitoni et al.** — the two ordinary explanations for beneficial noise.
- **Rosenblueth, Wiener and Bigelow; Ashby; Conant and Ashby** — purpose as feedback; the regulator theorem.
- **Dennett; Barandiaran, Di Paolo and Rohde; Bich and Bechtel** — the intentional stance, the enactive bar, and control mechanisms: the agency ladder's rungs.
- **Rokicki, Kociemba, Davidson and Dethridge; Korf; Joyner** — the cube's mathematics: God's number, pattern databases, the group.
