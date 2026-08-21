# On Faultization: Rubik

What Perturbation Reveals About the Scale of Competence in an Exactly Analyzable Collective. Fault tolerance asks whether a designed function survives damage; faultization, the method this paper proposes and runs to completion, uses damage as an instrument for locating where competence resides and at what scale a goal-directed description begins to predict. The substrate is the fixed-corner pocket cube: 3,674,160 states, all enumerated, with the published distance shells reproduced digit for digit as the calibration gate. Seven corner agents that each know their own correct pose and predict every move's effect on themselves perfectly collectively solve 61 states, a basin of 0.0017 percent; 758,286 states are local optima where no agent will consent to move; at 72 percent of states no agent is satisfied at all, and the group's parity forbids exactly 6 of 7 agents from ever being content. The intuitive repairs fail exhaustively: lateral moves create an ecology of 145,953 attractors with cycles up to length 4 and leave the basin at 61, one remembered action leaves it at 61, and the best of 48 heterogeneous weight draws reaches 136 by tie-breaking. Damage is what moves the basin: deleting 3 of 7 voters raises the mean basin to 91.8 with the best pattern at 260 and the worst at 19, while under action noise the same deletions lower success monotonically, one fault class with two opposite verdicts. Noise itself multiplies success 115-fold at its interior optimum and the product is still 0.0019 within 200 steps, against 0.000046 for the random walk with a stop rule. Deleting one face's moves strands a corner: recovery becomes algebraically impossible from 99.2 percent of states, the exact boundary between incompetence and impossibility. Conflicting target populations under strict arbitration are cycle-free ascent on a mixed potential with roughly 750,000 compromise equilibria at every split and both encoded targets always surviving; retargeting the same controller to any reachable pose leaves the basin at 61 by group conjugacy, a perfect machinery-target factorization that buys no competence. Every result is deflationary, and that is the instrument working: the exhaustive substrate produces the complete catalog of cheaper explanations that any claim of emergent collective agency, on any substrate, must defeat.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

The first run builds the full transition tables in a few minutes of pure python (cached, gitignored); every experiment is then exhaustive numpy over all 3,674,160 states, deterministic except the seeded weight draws, bit for bit on rerun. Twenty-seven invariant checks fail the run loudly if broken, among them: the exact reproduction of the published distance shells and diameter 11; the parity hole at 6 correct corners, in the state space and in every outcome; the equality of the strict, plateau, and memory basins at 61; the interior noise optimum beating both endpoint controls; the monotone rise of deterministic deletion basins against the monotone fall of noisy ones; the exact orbit of the surviving generators after structural damage; the provable absence of cycles in strict-arbitration chimeras; and the exact conjugacy of retargeted basins.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build on-faultization-rubik`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
