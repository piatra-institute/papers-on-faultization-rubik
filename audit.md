# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-23 — prose revision

Prose rewritten against the house standards. Headings made descriptive (Introduction, The self-sorting array experiments, Self-stabilization and related theory, The pocket cube as a test substrate, Composition of local correctness, Deterministic and stochastic repairs, Faults as probes, A ladder of goal-directedness, Conditions for faultization as a method, Objections, Falsification, Conclusion, Reproducibility).

Corrections found during the pass:
  - The action-noise optimum was reported as "the interior optimum of epsilon 0.4", the best point of the grid {0, 0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1}. Golden-section refinement between the grid neighbours gives epsilon 0.341 with success within 200 steps of 0.00198 (grid best 0.001915). New fields noise.best_eps_refined, best_success_refined, refined_fold_over_deterministic (119.2) and refined_fold_over_random_walk (43.3), computed from unrounded values; invariant refined_noise_optimum_at_least_grid_best (28 invariants). The earlier "115-fold" and "42-fold" referred to the grid point and are replaced by 119 and 43 at the refined optimum; the grid value is still reported.
  - Chimera equilibrium counts were given as "roughly 730,000 to 780,000" and "roughly 750,000"; the exact range 728,698 to 777,584 is now stated.
  - The Objections section referred to "the seed intuitions this paper tested"; now "the initial hypotheses of this study".

## 2026-08-21 — v1, first full draft to publication

Scope: the entire paper, simulation, and evidence base, from the seed chat to publication.

Changes:
  - Sources: 28 entries verified against Crossref or the standard record. The seed is a deep-research report carrying its own exhaustive computations; every one of its numbers was treated as unverified until this paper's independent implementation reproduced or corrected it. Reproduced exactly: the 61-state basin, the 758,286 local optima, the complete plateau attractor spectrum (145,953 attractors with every per-length count matching), and the published distance shells. Corrected or replaced: the heterogeneous-weights figure (the seed's roughly 165 came from an unstated weight distribution; this paper's 48 seeded draws give max 136, median 64), the unverifiable prototype-timeline citation for the 2x2 diameter (replaced by this paper's own breadth-first search), and the Levin-paper statistics, which enter results.json as cited records.
  - Simulation design iterations logged: the anti-reversal memory controller initially zeroed the forbidden action's score rather than excluding it, so in all-zero-score states it could still undo the remembered action; fixed with a sentinel below every legal score, and the fixed controller's basin is exactly 61, which became the finding. Two predicted invariants were wrong in the measured direction and were rewritten to the measured truth with the honest consequence kept: memory does not enlarge the basin at all, and deleting voters raises the deterministic basin (mean 62.9, 69.8, 91.8 for 1, 2, 3 deletions) while lowering noisy success monotonically, one fault class with two opposite verdicts depending on the active repair channel. A factual slip in a draft sentence (the plateau ecology described as "three quarters of a million looping states") was caught against the enumeration and corrected to the attractor count.
  - The chimera experiment's strict-arbiter cycle-freeness is asserted inside the run (a potential-ascent theorem) and verified across all 8 splits; the striking measured facts, both encoded targets surviving as equilibria at every split among roughly 730,000 to 780,000 compromises, with the maximum at the balanced 4-3 split, were not predicted by the seed and are reported as found.
  - Voice: draft came in at 0 errors, 4 review-candidates; all 4 rewritten; "exactly" thinned 10 to 5 (the parity statement keeps its two), a 32-sentence run without a short sentence broken to 18.

Verification:
  - voice: 0 errors, 0 review-candidates
  - refs: 28 in-text keys, 28 bib entries, 0 missing, 0 unused
  - claims: 110 sim values, 16 decimal claims in prose, 0 without a match
  - build: 13 pages, no missing-character warnings
  - simulation: 27/27 invariants over all 3,674,160 states
  - check => PASS
