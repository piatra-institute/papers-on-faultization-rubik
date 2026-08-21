"""The fixed-corner pocket cube, exhaustively.

Kociemba corner conventions on the 2x2x2 with the down-back-left corner
fixed: 7 moving corners, states = S7 x 3^6 = 3,674,160. Generators are the
9 face turns of U, R, F (quarter, half, inverse). This module builds the
full transition tables, the exact distance oracle by breadth-first search,
and the per-agent local-correctness bits for the solved target and for
arbitrary retargeted poses. Everything downstream is numpy gathers.

Tables are cached in simulation/cache/ (gitignored); a cold build takes a
few minutes of pure python, after which every experiment is vectorized.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

CACHE = Path(__file__).parent / "cache"

N_STATES = 3_674_160          # 7! * 3^6
N_ABSOLUTE = 88_179_840       # 8! * 3^7

# Kociemba corner order: URF=0 UFL=1 ULB=2 UBR=3 DFR=4 DLF=5 DBL=6 DRB=7.
# DBL (6) is the fixed corner; U, R, F never move it.
MOVING = [0, 1, 2, 3, 4, 5, 7]
SLOT_OF = {p: k for k, p in enumerate(MOVING)}

# replaced-by convention: position i receives the cubie from position cp[i],
# with orientation increment co[i] (mod 3).
CP = {
    "U": [3, 0, 1, 2, 4, 5, 6, 7],
    "R": [4, 1, 2, 0, 7, 5, 6, 3],
    "F": [1, 5, 2, 3, 0, 4, 6, 7],
}
CO = {
    "U": [0, 0, 0, 0, 0, 0, 0, 0],
    "R": [2, 0, 0, 1, 1, 0, 0, 2],
    "F": [1, 2, 0, 0, 2, 1, 0, 0],
}

# generator order fixed throughout the paper: U U2 U' R R2 R' F F2 F'
MOVE_NAMES = ["U", "U2", "U'", "R", "R2", "R'", "F", "F2", "F'"]
INVERSE_OF = [2, 1, 0, 5, 4, 3, 8, 7, 6]
NO_LAST = 9                   # memory symbol for "no previous action"

FACT = [1, 1, 2, 6, 24, 120, 720, 5040]
POW3 = [1, 3, 9, 27, 81, 243, 729]


def _apply(perm, ori, face):
    cp, co = CP[face], CO[face]
    return ([perm[cp[i]] for i in range(8)],
            [(ori[cp[i]] + co[i]) % 3 for i in range(8)])


def _encode(perm, ori) -> int:
    # slot permutation: slot k holds cubie SLOT_OF[perm[MOVING[k]]]
    p = [SLOT_OF[perm[q]] for q in MOVING]
    rank = 0
    avail = list(range(7))
    for k in range(6):
        j = avail.index(p[k])
        rank += j * FACT[6 - k]
        avail.pop(j)
    orank = 0
    for k in range(6):
        orank += ori[MOVING[k]] * POW3[k]
    return rank * 729 + orank


def _decode(idx: int):
    orank = idx % 729
    p = []
    avail = list(range(7))
    r = idx // 729
    for k in range(6):
        f = FACT[6 - k]
        j, r = divmod(r, f)
        p.append(avail.pop(j))
    p.append(avail[0])
    perm = [0] * 8
    perm[6] = 6
    for k, q in enumerate(MOVING):
        perm[q] = MOVING[p[k]]
    ori = [0] * 8
    o = orank
    total = 0
    for k in range(6):
        ori[MOVING[k]] = o % 3
        total += o % 3
        o //= 3
    ori[MOVING[6]] = (-total) % 3
    return perm, ori


def _target_pose(word):
    """Apply a move word (list of (face, times)) to the solved cube."""
    perm, ori = list(range(8)), [0] * 8
    for face, times in word:
        for _ in range(times):
            perm, ori = _apply(perm, ori, face)
    return perm, ori


def _hbits_for(perm_t, ori_t, perm, ori):
    """h_i = 1 iff cubie MOVING[i] sits where the target pose puts it,
    with the target's orientation."""
    # target position of cubie c: k with perm_t[k] == c
    pos_of = {perm_t[q]: q for q in range(8)}
    bits = []
    for i in range(7):
        c = MOVING[i]
        q = pos_of[c]
        bits.append(1 if (perm[q] == c and ori[q] == ori_t[q]) else 0)
    return bits


def build_tables(targets: dict[str, list] | None = None):
    """Return (T9, hbits dict). T9: uint32 array (9, N). hbits[name]:
    uint8 array (7, N). targets maps name -> move word; 'solved' is
    always included."""
    targets = dict(targets or {})
    targets.setdefault("solved", [])
    names = sorted(targets)
    key = "tables_" + "_".join(names)
    CACHE.mkdir(exist_ok=True)
    f_t9 = CACHE / "T9.npy"
    f_hb = {n: CACHE / f"hb_{n}.npy" for n in names}
    if f_t9.exists() and all(f.exists() for f in f_hb.values()):
        return np.load(f_t9), {n: np.load(f_hb[n]) for n in names}

    poses = {n: _target_pose(w) for n, w in targets.items()}
    tq = {face: np.empty(N_STATES, dtype=np.uint32) for face in "URF"}
    hb = {n: np.empty((7, N_STATES), dtype=np.uint8) for n in names}
    for idx in range(N_STATES):
        perm, ori = _decode(idx)
        for face in "URF":
            p2, o2 = _apply(perm, ori, face)
            tq[face][idx] = _encode(p2, o2)
        for n in names:
            pt, ot = poses[n]
            bits = _hbits_for(pt, ot, perm, ori)
            for i in range(7):
                hb[n][i, idx] = bits[i]

    T9 = np.empty((9, N_STATES), dtype=np.uint32)
    for fi, face in enumerate("URF"):
        q = tq[face]
        T9[3 * fi] = q
        T9[3 * fi + 1] = q[q]
        T9[3 * fi + 2] = q[q][q]
    np.save(f_t9, T9)
    for n in names:
        np.save(f_hb[n], hb[n])
    return T9, hb


def bfs_distances(T9: np.ndarray, start: int = 0) -> np.ndarray:
    """Exact distances from `start` under the 9 generators."""
    dist = np.full(N_STATES, -1, dtype=np.int8)
    dist[start] = 0
    frontier = np.array([start], dtype=np.uint32)
    d = 0
    while frontier.size:
        nxt = np.unique(T9[:, frontier].ravel())
        nxt = nxt[dist[nxt] == -1]
        d += 1
        dist[nxt] = d
        frontier = nxt
    return dist


def orbit_size(gens: np.ndarray, start: int = 0) -> int:
    """Size of the orbit of `start` under a subset of generator tables."""
    seen = np.zeros(N_STATES, dtype=bool)
    seen[start] = True
    frontier = np.array([start], dtype=np.uint32)
    while frontier.size:
        nxt = np.unique(gens[:, frontier].ravel())
        nxt = nxt[~seen[nxt]]
        seen[nxt] = True
        frontier = nxt
    return int(seen.sum())
