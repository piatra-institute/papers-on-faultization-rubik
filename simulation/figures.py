"""Figures for *On Faultization: Rubik*. Each reads the results dict and
writes one PNG.

Palette (CVD-checked in a prior validation; line styles and direct labels as
secondary encoding): amber, green, blue, warm gray; red reserved for harm.
"""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#1a1a1a"
GRID = "#d9d9d9"
AMBER = "#b45309"
GREEN = "#15803d"
BLUE = "#2563eb"
GRAY = "#57534e"
RED = "#b3202c"


def _style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)


def plot_microscope(res: dict, path: str) -> None:
    comp = res["composition"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 3.9))
    # left: the exact distance shells
    shells = comp["shells"]
    d = np.arange(len(shells))
    ax1.bar(d, shells, color=BLUE, width=0.7)
    ax1.set_yscale("log")
    ax1.set_xticks(d)
    ax1.set_xlabel("exact distance from solved (half-turn metric)", fontsize=9)
    ax1.set_ylabel("states (log)", fontsize=9)
    ax1.set_title("the complete space: 3,674,160 states, diameter 11",
                  fontsize=10, color=INK)
    ax1.annotate("published shell table\nreproduced exactly",
                 (1.2, 3e5), fontsize=8, color=BLUE)
    _style(ax1)
    # right: where every state ends under strict local-correctness voting
    hist = comp["strict"]["final_score_histogram"]
    h = np.arange(8)
    colors = [GRAY] * 6 + [RED, GREEN]
    bars = ax2.bar(h, np.maximum(hist, 0.5), color=colors, width=0.7)
    ax2.set_yscale("log")
    ax2.set_xticks(h)
    ax2.set_xlabel("correct corners at the final attractor", fontsize=9)
    ax2.set_ylabel("starting states (log)", fontsize=9)
    ax2.set_title("the fate of every state under local correctness",
                  fontsize=10, color=INK)
    ax2.annotate("parity forbids\nexactly 6", (6, 2.2), fontsize=8, color=RED,
                 ha="center")
    basin = comp["strict"]["solved_basin"]
    ax2.annotate(f"solved: {basin} states\n(0.0017 percent)", (7, hist[7] * 3),
                 fontsize=8, color=GREEN, ha="center")
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_repairs(res: dict, path: str) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 3.9))
    # left: the noise curve
    noise = res["noise"]
    eps = [float(e) for e in noise["success_by_eps"]]
    suc = list(noise["success_by_eps"].values())
    ax1.plot(eps, suc, "-o", color=BLUE, lw=1.8, ms=4)
    be = noise["best_eps"]
    ax1.axvline(be, color=GREEN, lw=0.9, ls=":")
    ax1.annotate(f"interior optimum\nat eps {be}", (be + 0.02, noise["best_success"] * 0.75),
                 fontsize=8, color=GREEN)
    ax1.annotate("eps 1: random walk with a stop rule\nsolves everything eventually and\n"
                 f"{noise['random_walk_success']:.5f} within the horizon",
                 (0.52, max(suc) * 0.50), fontsize=7.5, color=RED)
    ax1.set_xlabel("action-noise rate eps", fontsize=9)
    ax1.set_ylabel(f"success within {noise['horizon']} steps", fontsize=9)
    ax1.set_title("noise as repair: exploration, priced", fontsize=10, color=INK)
    _style(ax1)
    # right: the deterministic variations against deletion
    labels = ["strict\nvoting", "plateau\nmoves", "one action\nof memory",
              "best weight\ndraw (of 48)", "3 voters\ndeleted (best)"]
    vals = [res["composition"]["strict"]["solved_basin"],
            res["composition"]["plateau"]["solved_basin"],
            res["memory"]["solved_basin"],
            res["weights"]["max_basin"],
            res["deletion"]["deterministic"]["3"]["max_basin"]]
    colors = [GRAY, GRAY, BLUE, AMBER, RED]
    ax2.bar(range(5), vals, color=colors, width=0.62)
    for i, v in enumerate(vals):
        ax2.annotate(f"{v:,}", (i, v), fontsize=8.5, ha="center", va="bottom",
                     color=INK, xytext=(0, 3), textcoords="offset points")
    ax2.set_xticks(range(5))
    ax2.set_xticklabels(labels, fontsize=7.5)
    ax2.set_ylabel("solved basin (states)", fontsize=9)
    ax2.set_ylim(0, max(vals) * 1.25)
    ax2.set_title("the deterministic dials, and what actually moves the basin",
                  fontsize=10, color=INK)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_faults(res: dict, path: str) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 3.9))
    # left: deletion, with and without the noise channel
    dele = res["deletion"]
    ks = [0, 1, 2, 3]
    det = [res["composition"]["plateau"]["solved_basin"]] + [
        dele["deterministic"][str(k)]["mean_basin"] for k in (1, 2, 3)]
    noisy = [dele["noisy_success_eps01"][str(k)] for k in ks]
    ax1.plot(ks, np.array(det) / res["constants"]["N_STATES"], "-o",
             color=GRAY, lw=1.6, ms=4, label="deterministic basin (fraction)")
    ax1.plot(ks, noisy, "-s", color=BLUE, lw=1.8, ms=4,
             label="success with eps 0.1 noise")
    ax1.set_yscale("log")
    imp = res["structural"]["impossible_fraction_UR"]
    ax1.axhline(1 - imp, color=RED, lw=0.9, ls="--")
    ax1.annotate(f"delete one face's moves instead: recovery\npossible from "
                 f"{100 * (1 - imp):.2f} percent of states\n(orbit of the survivors, exact)",
                 (1.0, (1 - imp) * 0.32), fontsize=7.5, color=RED, ha="center")
    ax1.set_ylim(top=(1 - imp) * 4)
    ax1.set_xticks(ks)
    ax1.set_xlabel("deleted agents (of 7)", fontsize=9)
    ax1.set_ylabel("recovery (log)", fontsize=9)
    ax1.set_title("deleting voters against deleting moves", fontsize=10,
                  color=INK)
    ax1.legend(frameon=False, fontsize=8, loc="center right")
    _style(ax1)
    # right: chimera ecology across splits
    splits = res["chimera"]["splits"]
    ms = list(range(8))
    n_comp = [splits[str(m)]["n_compromise_equilibria"] for m in ms]
    ax2.plot(ms, n_comp, "-o", color=AMBER, lw=1.8, ms=4,
             label="compromise equilibria neither faction encodes")
    both = all(splits[str(m)]["solved_is_equilibrium"]
               and splits[str(m)]["B_is_equilibrium"] for m in ms)
    ax2.annotate("at every split, both encoded targets\nremain equilibria; "
                 "the conflict is settled\nby basins, never by extinction"
                 if both else "", (3.5, min(n_comp) * 1.002),
                 fontsize=7.5, color=INK, ha="center")
    ax2.annotate(f"plateau arbitration at 4-3 restores\n"
                 f"{res['chimera']['plateau_43_n_cycles_gt1']:,} cycles "
                 f"(length up to {res['chimera']['plateau_43_max_cycle']})",
                 (3.5, max(n_comp) * 0.9985), fontsize=7.5, color=GRAY,
                 ha="center")
    ax2.set_xticks(ms)
    ax2.set_xlabel("agents keeping the solved target (of 7); the rest carry B",
                   fontsize=9)
    ax2.set_ylabel("compromise equilibria", fontsize=9)
    ax2.set_title("conflicting targets: ascent on a mixed potential",
                  fontsize=10, color=INK)
    ax2.legend(frameon=False, fontsize=8, loc="lower right")
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
