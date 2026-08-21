"""Orchestrator: reproduces every number and all three figures in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/*.png. The first run builds
the full transition tables (a few minutes of pure python, cached in
cache/); every experiment after that is exhaustive numpy over all
3,674,160 states. Deterministic throughout except the seeded weight draws;
a rerun reproduces every number bit for bit. A failed invariant fails the
run.
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    from figures import plot_microscope, plot_repairs, plot_faults
    plot_microscope(results, str(OUT / "figures" / "microscope.png"))
    plot_repairs(results, str(OUT / "figures" / "repairs.png"))
    plot_faults(results, str(OUT / "figures" / "faults.png"))

    c = results["composition"]
    print(f"shells reproduced, diameter {c['diameter']}")
    s = c["strict"]
    print(f"strict: basin {s['solved_basin']} ({s['solved_basin_pct']:.4f}%), "
          f"local optima {s['nontarget_fixed_points']} "
          f"({s['nontarget_fixed_pct']:.1f}%), parity hole at 6: "
          f"{s['final_score_histogram'][6]}")
    p = c["plateau"]
    print(f"plateau: basin {p['solved_basin']}, {p['n_attractors']} attractors, "
          f"max cycle {p['max_cycle_length']}, spectrum "
          + str({k: (v['attractors'], v['basin']) for k, v in p['spectrum'].items()}))
    print(f"memory: basin {results['memory']['solved_basin']} "
          f"({results['memory']['solved_basin_pct']:.2f}%)")
    n = results["noise"]
    print(f"noise: best eps {n['best_eps']} -> {n['best_success']:.3f}; "
          f"eps 0 -> {n['deterministic_success']:.5f}; "
          f"eps 1 -> {n['random_walk_success']:.5f}")
    d = results["deletion"]
    print("deletion det:", {k: round(v['mean_basin'], 1)
                            for k, v in d['deterministic'].items()},
          "noisy eps 0.1:", {k: round(v, 3)
                             for k, v in d['noisy_success_eps01'].items()})
    st = results["structural"]
    print(f"structural: orbit(U,R) {st['orbit_UR']} "
          f"({100 * st['orbit_UR_fraction']:.4f}%), orbit(U) {st['orbit_U']}")
    ch = results["chimera"]
    print(f"chimera vs B at distance {ch['target_B_state_distance']}:")
    for m, v in ch["splits"].items():
        print(f"  {m}A/{7 - int(m)}B: solved_eq {v['solved_is_equilibrium']}, "
              f"B_eq {v['B_is_equilibrium']}, equilibria {v['n_equilibria']}, "
              f"compromise {v['n_compromise_equilibria']}")
    print(f"  plateau 4-3: max cycle {ch['plateau_43_max_cycle']}, "
          f"cycles>1 {ch['plateau_43_n_cycles_gt1']}")
    r = results["retarget"]
    print(f"retarget: B basin {r['B']['basin']}, C basin {r['C']['basin']}, "
          f"conjugacy exact: {r['conjugacy_exact']}")
    w = results["weights"]
    print(f"weights: max {w['max_basin']}, median {w['median_basin']}, "
          f"homogeneous {w['homogeneous_basin']}")
    print("checks:", f"{sum(results['checks'].values())}/{len(results['checks'])}")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
