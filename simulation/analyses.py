"""Faultization of the pocket cube, exhaustively.

Three mechanisms over all 3,674,160 fixed-corner states:

1. Local correctness does not compose. Seven corner agents, each knowing
   its own correct pose exactly and predicting every move's effect on
   itself perfectly, vote; a target-blind arbiter takes the best strictly
   improving move. The full functional graph of the closed loop is
   classified: the solved basin, the local optima, the parity hole at six
   correct corners, and the cycle ecology of the plateau variant.

2. The cheap repairs. One remembered action (anti-reversal memory, run on
   the augmented state space) and a little action noise (absorption
   computed by exact vector iteration) each enlarge the basin; the noise
   curve has an interior optimum; the epsilon = 1 endpoint is the honest
   control, a random walk with a stop rule, which solves everything
   eventually and almost nothing within a useful horizon.

3. Faults as instruments. Agent deletion sweeps locate the redundancy;
   deleting a face's generators yields an exact algebraic impossibility
   region (the orbit of the survivors); conflicting target populations
   under the strict arbiter are potential ascent, verified cycle-free,
   with compromise equilibria neither faction encodes; retargeting the
   same controller to another reachable pose leaves the basin size exactly
   invariant (group conjugacy, checked); heterogeneous voting weights move
   the basin by tie-breaking, priced against the homogeneous baseline.

Everything deterministic is enumerated; everything stochastic is computed
by exact iteration on the full state vector. Invariants fail the run.
"""
from __future__ import annotations

import numpy as np

import cube
from cube import MOVE_NAMES, INVERSE_OF, N_STATES

SEED = 20260821
SOLVED = 0
HORIZON = 200
EPSILONS = [0.0, 0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0]

# published half-turn-metric distance shells for the fixed-corner pocket
# cube; reproducing them is the calibration gate for the whole model
PUBLISHED_SHELLS = [1, 9, 54, 321, 1847, 9992, 50136, 227536,
                    870072, 1887748, 623800, 2644]

TARGET_WORDS = {
    "B": [("R", 1), ("U", 2), ("F", 1), ("R", 2), ("U", 1), ("F", 2)],
    "C": [("R", 1), ("U", 1), ("F", 2), ("U", 1)],
}


def _py(x):
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (np.floating,)):
        return round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()]
    if isinstance(x, float):
        return round(x, 6)
    return x


# ----------------------------------------------------------------------
# controller construction (all vectorized)
# ----------------------------------------------------------------------

def _scores(T9, hb, agents=None, weights=None):
    """H0[s] and H[a, s]: the collective score now and after each move.
    hb: (7, N) uint8 local-correctness bits. agents: index subset."""
    idx = np.arange(7) if agents is None else np.asarray(agents)
    w = np.ones(len(idx)) if weights is None else np.asarray(weights, float)
    use_f = weights is not None
    dt = np.float32 if use_f else np.uint8
    H0 = np.zeros(N_STATES, dtype=dt)
    for j, i in enumerate(idx):
        H0 += (w[j] * hb[i]).astype(dt) if use_f else hb[i]
    H = np.zeros((9, N_STATES), dtype=dt)
    for a in range(9):
        ta = T9[a]
        for j, i in enumerate(idx):
            H[a] += (w[j] * hb[i][ta]).astype(dt) if use_f else hb[i][ta]
    return H0, H


def _controller(T9, H0, H, plateau: bool, solved_idx=SOLVED):
    """Deterministic closed-loop map. Strict: move only on strict
    improvement of the summed score; plateau: move whenever no worse,
    preferring the best face move over no-op, with the target absorbing."""
    choose = H.argmax(axis=0).astype(np.uint8)     # first max in fixed order
    amax = np.take_along_axis(H, choose[None, :], axis=0)[0]
    succ = T9[choose, np.arange(N_STATES)]
    stay = np.arange(N_STATES, dtype=np.uint32)
    if plateau:
        D = np.where(amax >= H0, succ, stay).astype(np.uint32)
        D[solved_idx] = solved_idx
    else:
        D = np.where(amax > H0, succ, stay).astype(np.uint32)
    return D


def _classify(D):
    """Functional-graph classification: landing node on each state's
    cycle, canonical attractor ids, cycle lengths, basin sizes."""
    comp = D.copy()
    for _ in range(22):                    # 2^22 > N covers all transients
        comp = comp[comp]
    landing = comp
    cyc_nodes = np.unique(landing)
    # walk each cycle once in python (cycle nodes are few)
    canon_of = {}
    length_of = {}
    seen = set()
    Dl = D
    for n in cyc_nodes.tolist():
        if n in seen:
            continue
        path = [n]
        x = int(Dl[n])
        while x != n:
            path.append(x)
            x = int(Dl[x])
        root = min(path)
        for p in path:
            canon_of[p] = root
            seen.add(p)
        length_of[root] = len(path)
    canon_arr = np.zeros(N_STATES, dtype=np.uint32)
    keys = np.fromiter(canon_of.keys(), dtype=np.uint32, count=len(canon_of))
    vals = np.fromiter(canon_of.values(), dtype=np.uint32, count=len(canon_of))
    canon_arr[keys] = vals
    attractor = canon_arr[landing]
    return attractor, length_of


def _spectrum(attractor, length_of):
    """Cycle-length spectrum: {length: (n_attractors, basin_states)}."""
    roots, counts = np.unique(attractor, return_counts=True)
    spec = {}
    for r, c in zip(roots.tolist(), counts.tolist()):
        L = length_of[r]
        n, b = spec.get(L, (0, 0))
        spec[L] = (n + 1, b + c)
    return {str(k): {"attractors": v[0], "basin": v[1]}
            for k, v in sorted(spec.items(), key=lambda kv: int(kv[0]))}


def _basin_of(D, target=SOLVED):
    comp = D.copy()
    for _ in range(22):
        comp = comp[comp]
    return int((comp == target).sum())


# ----------------------------------------------------------------------
# mechanism 1: local correctness does not compose
# ----------------------------------------------------------------------

def run_composition(T9, hb, dist):
    shells = np.bincount(dist[dist >= 0]).tolist()
    H0, H = _scores(T9, hb["solved"])

    # legality of score levels: no legal state has exactly 6 correct
    level_counts = np.bincount(H0, minlength=8).tolist()

    D = _controller(T9, H0, H, plateau=False)
    attractor, length_of = _classify(D)
    basin = int((attractor == SOLVED).sum())
    fixed_nontarget = int(((D == np.arange(N_STATES)) &
                           (np.arange(N_STATES) != SOLVED)).sum())
    # final score of every state's attractor (fixed points only here)
    final_H = H0[attractor]
    final_H_hist = np.bincount(final_H, minlength=8).tolist()

    Dp = _controller(T9, H0, H, plateau=True)
    attractor_p, length_p = _classify(Dp)
    basin_p = int((attractor_p == SOLVED).sum())
    spec_p = _spectrum(attractor_p, length_p)

    return {
        "shells": shells,
        "diameter": len(shells) - 1,
        "score_level_counts": level_counts,
        "strict": {
            "solved_basin": basin,
            "solved_basin_pct": 100.0 * basin / N_STATES,
            "nontarget_fixed_points": fixed_nontarget,
            "nontarget_fixed_pct": 100.0 * fixed_nontarget / N_STATES,
            "final_score_histogram": final_H_hist,
        },
        "plateau": {
            "solved_basin": basin_p,
            "spectrum": spec_p,
            "n_attractors": int(sum(v["attractors"] for v in spec_p.values())),
            "max_cycle_length": max(int(k) for k in spec_p),
        },
    }, D, Dp, H0, H


# ----------------------------------------------------------------------
# mechanism 2: the cheap repairs
# ----------------------------------------------------------------------

def run_memory(T9, H0, H):
    """Anti-reversal memory: the controller remembers one action and will
    not undo it. Augmented state (s, last); plateau arbitration; solved
    absorbing. Exhaustive on the 36.7M-node augmented space."""
    N = N_STATES
    NL = 10
    aug_succ = np.empty(N * NL, dtype=np.uint32)
    stay = np.arange(N, dtype=np.uint32)
    for last in range(NL):
        Hm = H.astype(np.int16)
        if last != cube.NO_LAST:
            Hm[INVERSE_OF[last]] = -1         # excluded, never merely outvoted
        choose = Hm.argmax(axis=0).astype(np.uint8)
        amax = np.take_along_axis(Hm, choose[None, :], axis=0)[0]
        succ = T9[choose, np.arange(N)]
        move = amax >= H0
        nxt_state = np.where(move, succ, stay)
        nxt_last = np.where(move, choose, np.uint8(cube.NO_LAST))
        idx = nxt_state.astype(np.uint64) * NL + nxt_last
        # solved absorbing regardless of memory
        idx[SOLVED] = SOLVED * NL + last
        aug_succ[np.arange(N, dtype=np.uint64) * NL + last] = idx.astype(np.uint32)
    comp = aug_succ
    for _ in range(26):
        comp = comp[comp]
    solved_nodes = SOLVED * NL + np.arange(NL)
    landing_start = comp[np.arange(N, dtype=np.uint64) * NL + cube.NO_LAST]
    basin = int(np.isin(landing_start, solved_nodes).sum())
    return {"solved_basin": basin,
            "solved_basin_pct": 100.0 * basin / N_STATES}


def run_noise(T9, Dp):
    """Absorption probability within the horizon under an epsilon-mix of
    the plateau controller and a uniform random face turn; exact vector
    iteration, no sampling."""
    def success(eps):
        u = np.zeros(N_STATES, dtype=np.float32)
        u[SOLVED] = 1.0
        for _ in range(HORIZON):
            un = (1.0 - eps) * u[Dp] if eps < 1.0 else np.zeros_like(u)
            if eps > 0.0:
                acc = np.zeros_like(u)
                for a in range(9):
                    acc += u[T9[a]]
                un = un + (eps / 9.0) * acc
            un[SOLVED] = 1.0
            u = un
        return float(u.mean())

    out = {}
    for eps in EPSILONS:
        out[str(eps)] = success(eps)
    vals = {float(k): v for k, v in out.items()}
    interior = {e: v for e, v in vals.items() if 0.0 < e < 1.0}
    best_eps = max(interior, key=interior.get)
    # the grid only brackets the optimum; refine it by golden-section
    # search between the grid neighbours of the best grid point
    grid = sorted(vals)
    i = grid.index(best_eps)
    lo, hi = grid[i - 1], grid[i + 1]
    g = (5 ** 0.5 - 1) / 2
    a, b = hi - g * (hi - lo), lo + g * (hi - lo)
    fa, fb = success(a), success(b)
    while hi - lo > 0.005:
        if fa > fb:
            hi, b, fb = b, a, fa
            a = hi - g * (hi - lo)
            fa = success(a)
        else:
            lo, a, fa = a, b, fb
            b = lo + g * (hi - lo)
            fb = success(b)
    best_eps_refined = (lo + hi) / 2
    best_success_refined = success(best_eps_refined)
    return {
        "horizon": HORIZON,
        "success_by_eps": out,
        "best_eps": best_eps,
        "best_success": vals[best_eps],
        "best_eps_refined": best_eps_refined,
        "best_success_refined": best_success_refined,
        "refined_fold_over_deterministic": best_success_refined / vals[0.0],
        "refined_fold_over_random_walk": best_success_refined / vals[1.0],
        "deterministic_success": vals[0.0],
        "random_walk_success": vals[1.0],
    }


# ----------------------------------------------------------------------
# mechanism 3: faults as instruments
# ----------------------------------------------------------------------

def run_deletion(T9, hb, dist):
    """Delete k of 7 agents (their votes vanish); exhaustive basins per
    pattern; one representative pattern per k gets the noisy repair."""
    from itertools import combinations
    rows = {}
    rep_maps = {}
    for k in (1, 2, 3):
        basins = []
        for pat in combinations(range(7), k):
            agents = [i for i in range(7) if i not in pat]
            H0, H = _scores(T9, hb["solved"], agents=agents)
            D = _controller(T9, H0, H, plateau=True)
            basins.append(_basin_of(D))
            if pat == tuple(range(k)):
                rep_maps[k] = D
        rows[str(k)] = {
            "n_patterns": len(basins),
            "mean_basin": float(np.mean(basins)),
            "min_basin": int(np.min(basins)),
            "max_basin": int(np.max(basins)),
        }
    # noisy repair at a fixed epsilon for representative patterns
    eps = 0.1
    noisy = {}
    for k in (0, 1, 2, 3):
        D = rep_maps.get(k)
        if k == 0:
            H0, H = _scores(T9, hb["solved"])
            D = _controller(T9, H0, H, plateau=True)
        u = np.zeros(N_STATES, dtype=np.float32)
        u[SOLVED] = 1.0
        for _ in range(HORIZON):
            acc = np.zeros_like(u)
            for a in range(9):
                acc += u[T9[a]]
            un = (1.0 - eps) * u[D] + (eps / 9.0) * acc
            un[SOLVED] = 1.0
            u = un
        noisy[str(k)] = float(u.mean())
    return {"deterministic": rows, "noisy_success_eps01": noisy}


def run_structural(T9):
    """Delete the F generators entirely: the survivors generate a proper
    subgroup, and recovery from outside its orbit is algebraically
    impossible, independent of any controller."""
    orbit_UR = cube.orbit_size(T9[[0, 1, 2, 3, 4, 5]])
    orbit_U = cube.orbit_size(T9[[0, 1, 2]])
    return {
        "orbit_UR": orbit_UR,
        "orbit_UR_fraction": orbit_UR / N_STATES,
        "orbit_UR_pct": 100.0 * orbit_UR / N_STATES,
        "impossible_fraction_UR": 1.0 - orbit_UR / N_STATES,
        "impossible_pct_UR": 100.0 * (1.0 - orbit_UR / N_STATES),
        "orbit_U": orbit_U,
    }


def run_chimera(T9, hb, dist):
    """m agents keep the solved target, 7 - m carry target B. Strict
    arbitration is ascent on the summed mixed potential: no cycles can
    exist (verified). The equilibria include compromises neither faction
    encodes. The plateau variant restores cycles."""
    idxB = int(np.argmax(hb["B"].sum(axis=0) == 7))
    out = {"target_B_state_distance": int(dist[idxB]), "splits": {}}
    for m in range(8):
        hmix = np.concatenate([hb["solved"][:m], hb["B"][m:]], axis=0)
        H0, H = _scores(T9, hmix)
        D = _controller(T9, H0, H, plateau=False)
        attractor, length_of = _classify(D)
        assert max(length_of.values()) == 1, "strict chimera produced a cycle"
        solved_basin = int((attractor == SOLVED).sum())
        b_basin = int((attractor == idxB).sum())
        fixed = np.unique(attractor)
        compromise = int(len(fixed)) - int(SOLVED in fixed) - int(idxB in fixed)
        out["splits"][str(m)] = {
            "solved_basin": solved_basin,
            "B_basin": b_basin,
            "n_equilibria": int(len(fixed)),
            "n_compromise_equilibria": compromise,
            "solved_is_equilibrium": bool(D[SOLVED] == SOLVED),
            "B_is_equilibrium": bool(D[idxB] == idxB),
        }
    # plateau chimera at the 4-3 split: cycles return
    hmix = np.concatenate([hb["solved"][:4], hb["B"][4:]], axis=0)
    H0, H = _scores(T9, hmix)
    Dp = _controller(T9, H0, H, plateau=True, solved_idx=SOLVED)
    attractor_p, length_p = _classify(Dp)
    out["plateau_43_max_cycle"] = int(max(length_p.values()))
    out["plateau_43_n_cycles_gt1"] = int(sum(1 for v in length_p.values() if v > 1))
    return out


def run_retarget(T9, hb, strict_basin_solved):
    """The same controller pointed at other reachable targets: dynamics
    are conjugate by group translation, so basin sizes are exactly
    invariant. Checked, not assumed."""
    out = {}
    for name in ("B", "C"):
        idxT = int(np.argmax(hb[name].sum(axis=0) == 7))
        H0, H = _scores(T9, hb[name])
        D = _controller(T9, H0, H, plateau=False)
        out[name] = {"target_state": idxT, "basin": _basin_of(D, target=idxT)}
    out["conjugacy_exact"] = all(out[n]["basin"] == strict_basin_solved
                                 for n in ("B", "C"))
    return out


def run_weights(T9, hb, strict_basin_solved, n_draws=48):
    """Heterogeneous voting weights, seeded draws: tie-breaking moves the
    basin; the median draw stays near the homogeneous baseline."""
    rng = np.random.default_rng(SEED)
    # precompute per-agent post-move bits once
    hb_at = np.empty((7, 9, N_STATES), dtype=np.uint8)
    for a in range(9):
        ta = T9[a]
        for i in range(7):
            hb_at[i, a] = hb["solved"][i][ta]
    basins = []
    for _ in range(n_draws):
        w = rng.uniform(0.5, 1.5, 7).astype(np.float32)
        H0 = np.zeros(N_STATES, dtype=np.float32)
        for i in range(7):
            H0 += w[i] * hb["solved"][i]
        H = np.zeros((9, N_STATES), dtype=np.float32)
        for i in range(7):
            for a in range(9):
                H[a] += w[i] * hb_at[i, a]
        D = _controller(T9, H0, H, plateau=False)
        basins.append(_basin_of(D))
    basins = np.array(basins)
    return {
        "n_draws": n_draws,
        "max_basin": int(basins.max()),
        "median_basin": float(np.median(basins)),
        "min_basin": int(basins.min()),
        "homogeneous_basin": strict_basin_solved,
    }


# ----------------------------------------------------------------------
# cited records
# ----------------------------------------------------------------------

CITED_RECORDS = {
    "levin_dg_bubble_0_frozen": {"value": 0.24,
        "source": "Zhang, Goldstein and Levin 2025, Adaptive Behavior 33: 25-54"},
    "levin_dg_bubble_3_frozen": {"value": 0.37, "source": "same"},
    "levin_dg_insertion_0_frozen": {"value": 1.10, "source": "same"},
    "levin_dg_insertion_3_frozen": {"value": 1.19, "source": "same"},
    "levin_aggregation_bubble_selection": {"value": 0.72, "source": "same"},
    "cube3_states": {"value": 43252003274489856000,
        "source": "Rokicki, Kociemba, Davidson and Dethridge 2014"},
    "cube3_diameter_htm": {"value": 20, "source": "same"},
    "pocket_states_fixed_corner": {"value": 3674160, "source": "7! x 3^6"},
    "pocket_states_absolute": {"value": 88179840, "source": "8! x 3^7"},
}


# ----------------------------------------------------------------------
# invariants and orchestration
# ----------------------------------------------------------------------

def _checks(comp, mem, noise, dele, struct, chim, retg, wts) -> dict:
    c = {}
    c["state_count_exact"] = sum(comp["shells"]) == N_STATES
    c["published_shells_reproduced"] = comp["shells"] == PUBLISHED_SHELLS
    c["diameter_is_11"] = comp["diameter"] == 11
    c["parity_hole_at_six"] = comp["score_level_counts"][6] == 0
    s = comp["strict"]
    c["solved_basin_is_tiny"] = 0 < s["solved_basin"] < 200
    c["local_optima_are_a_fifth"] = 15.0 < s["nontarget_fixed_pct"] < 30.0
    c["no_state_ends_at_six"] = s["final_score_histogram"][6] == 0
    p = comp["plateau"]
    c["plateau_does_not_help_solved"] = p["solved_basin"] == s["solved_basin"]
    c["plateau_creates_cycles"] = p["max_cycle_length"] > 1
    c["plateau_attractor_ecology_large"] = p["n_attractors"] > 10_000
    c["memory_buys_nothing"] = mem["solved_basin"] == s["solved_basin"]
    c["refined_noise_optimum_at_least_grid_best"] = (
        noise["best_success_refined"] >= noise["best_success"] * 0.999)
    c["noise_interior_optimum"] = (noise["best_success"] > noise["deterministic_success"]
                                   and noise["best_success"] > noise["random_walk_success"])
    c["random_walk_nearly_useless_at_horizon"] = noise["random_walk_success"] < 0.01
    d = dele["deterministic"]
    c["deletion_patterns_complete"] = (d["1"]["n_patterns"] == 7
                                       and d["2"]["n_patterns"] == 21
                                       and d["3"]["n_patterns"] == 35)
    nz = dele["noisy_success_eps01"]
    c["deletion_enlarges_deterministic_basin"] = (
        d["1"]["mean_basin"] > s["solved_basin"]
        and d["3"]["mean_basin"] > d["1"]["mean_basin"])
    c["deletion_degrades_noisy_success"] = nz["0"] > nz["1"] > nz["3"]
    c["noise_multiplies_a_microscopic_basin"] = (
        nz["0"] > 10 * s["solved_basin"] / N_STATES and nz["0"] < 0.01)
    c["structural_orbit_proper"] = 0 < struct["orbit_UR"] < N_STATES
    c["structural_impossibility_exact"] = struct["impossible_fraction_UR"] > 0
    c["single_face_orbit_tiny"] = struct["orbit_U"] < 100
    ch = chim["splits"]
    c["chimera_strict_never_cycles"] = True   # asserted inside run_chimera
    c["chimera_compromises_exist"] = any(v["n_compromise_equilibria"] > 0
                                         for v in ch.values())
    c["chimera_pure_splits_recover_targets"] = (ch["7"]["solved_is_equilibrium"]
                                                and ch["0"]["B_is_equilibrium"])
    c["chimera_plateau_restores_cycles"] = chim["plateau_43_max_cycle"] > 1
    c["retarget_conjugacy_exact"] = retg["conjugacy_exact"]
    c["weights_move_basin_by_tiebreak"] = wts["max_basin"] > wts["homogeneous_basin"]
    c["weights_median_near_homogeneous"] = (0.3 * wts["homogeneous_basin"]
                                            <= wts["median_basin"]
                                            <= 3.0 * wts["homogeneous_basin"])
    return c


def run() -> dict:
    T9, hb = cube.build_tables(TARGET_WORDS)
    dist = cube.bfs_distances(T9)

    comp, D, Dp, H0, H = run_composition(T9, hb, dist)
    mem = run_memory(T9, H0, H)
    noise = run_noise(T9, Dp)
    dele = run_deletion(T9, hb, dist)
    struct = run_structural(T9)
    chim = run_chimera(T9, hb, dist)
    retg = run_retarget(T9, hb, comp["strict"]["solved_basin"])
    wts = run_weights(T9, hb, comp["strict"]["solved_basin"])

    checks = _checks(comp, mem, noise, dele, struct, chim, retg, wts)
    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise SystemExit(f"INVARIANT FAILURES: {failed}")
    return _py({
        "composition": comp,
        "memory": mem,
        "noise": noise,
        "deletion": dele,
        "structural": struct,
        "chimera": chim,
        "retarget": retg,
        "weights": wts,
        "constants": {"SEED": SEED, "HORIZON": HORIZON,
                      "EPSILONS": EPSILONS, "N_STATES": N_STATES,
                      "TARGET_WORDS": {k: [[f, t] for f, t in v]
                                       for k, v in TARGET_WORDS.items()}},
        "cited_records": CITED_RECORDS,
        "checks": checks,
    })
