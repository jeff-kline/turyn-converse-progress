"""Exact, parity-restricted residual norm test for q=9265 at ell=113.

One process; stdlib only; proof of completeness in EXTENSIONS.md.
"""
import itertools
import json
import math
import signal
import sys
import time
from pathlib import Path

signal.alarm(180)
START = time.monotonic()
Q, ELL, N = 9265, 113, 109
H = {1, 4, 7, 16, 28, 30, 49, 64, 83, 85, 97, 106, 109, 112}
def cyclic_subgroup(p, modulus):
    out, x = set(), 1
    while x not in out:
        out.add(x)
        x = x*p % modulus
    return out

inversion = (1+4*((-2)*pow(4,-1,ELL) % ELL)) % (4*ELL)
decomposition = [cyclic_subgroup(p,4*ELL) for p in [5,17,109]]
intersection = set.intersection(*[D | {x*inversion % (4*ELL) for x in D}
                                  for D in decomposition])
assert H == {x % ELL for x in intersection if x % 4 == 1}
residue_degrees = {}
for p in [5,17,109]:
    x,f = p % ELL,1
    while x not in H:
        x,f = x*p % ELL,f+1
    residue_degrees[p] = f
assert residue_degrees == {5:8,17:8,109:1}
COSETS = []
unused = set(range(1, ELL))
while unused:
    C = {min(unused)*u % ELL for u in H}
    COSETS.append(C)
    unused -= C
d, h = len(COSETS), len(H)
assert d == 8 and h == 14
assert 8*ELL > d*N  # A parity vector has range at most 2.

def trace_square(a):
    return ELL*sum(x*x for x in a)-h*sum(a)**2

def square(a):
    """Direct exact cyclic convolution, then Phi_ell reduction."""
    expanded = [0]*ELL
    for x, C in zip(a, COSETS):
        for c in C:
            expanded[c] = x
    conv = [sum(expanded[j]*expanded[(k-j) % ELL]
                for j in range(ELL)) for k in range(ELL)]
    assert all(len({conv[c] for c in C}) == 1 for C in COSETS)
    return tuple(conv[min(C)]-conv[0] for C in COSETS)

def vectors(parity):
    out = []
    # Q(a)>=sum(a_i^2), so this range safely covers each minimum.
    bound = math.isqrt(d*N)
    for m in range(-bound, bound+1):
        if m % 2 != parity:
            continue
        # Exclude the full subset: the minimum is required to occur.
        for mask in range((1 << d)-1):
            a = tuple(m+2*((mask >> j) & 1) for j in range(d))
            tr = trace_square(a)
            if tr <= d*N:
                out.append((a, tr))
    assert len({a for a, _ in out}) == len(out)
    return out

def representations(n):
    out = []
    for a in range(-math.isqrt(n), math.isqrt(n)+1):
        b = math.isqrt(n-a*a)
        if a*a+b*b == n:
            out.extend([(a, b)] if b == 0 else [(a, b), (a, -b)])
    return out

av, bv = vectors(1), vectors(0)
bsquares = {}
for b, tr in bv:
    bsquares.setdefault(square(b), []).append(b)
solutions = []
for a, tr in av:
    target = tuple(-N-x for x in square(a))
    for b in bsquares.get(target, []):
        solutions.append((a, b))
assert all((tuple([-a]*d),tuple([-b]*d)) in solutions
           for a in [-3,3] for b in [-10,10])

gaussian_factors = [(u, v) for u, v in representations(Q//N) if u % 2 == 1]
augmentations = [(x, y) for x, y in representations(Q) if x % 2 == 0]
ray_survivors = []
for a, b in solutions:
    ar, br = h*sum(a) % ELL, h*sum(b) % ELL
    for u, v in gaussian_factors:
        gr, gi = (u*ar-v*br) % ELL, (u*br+v*ar) % ELL
        for x, y in augmentations:
            if (gr-x) % ELL == (gi-y) % ELL == 0:
                ray_survivors.append(dict(a=a, b=b, factor=[u, v],
                                          augmentation=[x, y]))
out = dict(q=Q, ell=ELL, residual=N, H=sorted(H), residue_degrees=residue_degrees,
           cosets=[sorted(c) for c in COSETS],
           parity_vector_counts=[len(av), len(bv)],
           residual_solution_count=len(solutions),
           nonrational_solution_count=sum(len(set(a))>1 or len(set(b))>1
                                         for a, b in solutions),
           residual_solutions=[dict(a=a, b=b) for a, b in solutions],
           gaussian_factors=gaussian_factors, augmentations=augmentations,
           ray_survivor_count=len(ray_survivors), ray_survivors=ray_survivors,
           seconds=time.monotonic()-START)
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()
                  if k not in {'cosets','residual_solutions','ray_survivors'}}, indent=2))
