# On Faultization: Rubik

Rubik. What Perturbation Reveals About the Scale of Competence in an Exactly Analyzable Collective.

Fault tolerance asks whether a designed function survives damage. We develop the reverse question under the proposed name faultization: decompose a centralized algorithm into locally competent parts, damage them deliberately, and use the damage to locate where competence resides and at what scale a goal-directed description becomes predictive. The pocket cube provides a substrate on which every alternative explanation can be enumerated: 3,674,160 reachable states, an exact distance oracle, and exhaustively computable controller dynamics. Seven corner agents, each knowing its correct pose and predicting every move's effect on itself, collectively solve 61 of 3,674,160 states (0.0017 percent), while 758,286 states (20.6 percent) are local optima in which no agent consents to move; in 72 percent of states no agent is satisfied, and the group's parity makes exactly 6 correct corners impossible. Lateral moves create 145,953 attractors and leave the basin at 61, as does one remembered action; the best of 48 random weightings reaches 136. Deleting 3 of the 7 voters raises the mean basin to 91.8, with patterns ranging from 19 to 260. Action noise at its optimal rate of 0.34 raises success within 200 steps 119-fold, to 0.0020. Deleting one face's moves makes recovery impossible from 99.2 percent of states, separating incompetence from impossibility. Under strict arbitration, conflicting targets define a mixed potential with no cycles, and both targets survive as equilibria among roughly 729,000 to 778,000 equilibria. Retargeting leaves the basin at 61 by group conjugacy. Together these deflationary results form a catalogue of cheaper explanations that claims of emergent collective agency must exclude.

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

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build on-faultization-rubik`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
