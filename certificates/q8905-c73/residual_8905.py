"""Exhaustive parity/trace residual norm137 certificate at conductor73.

The only nonstdlib dependency is pinned in residual-requirements.txt.
All arithmetic is integral; numpy accelerates bounded int64 matrix products.
"""
import os
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                 'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import itertools
import json
import math
import signal
import sys
import time
from pathlib import Path
import numpy as np

signal.alarm(180)
START = time.monotonic()
CPU_START = time.process_time()
Q, ELL, N, d, h = 8905, 73, 137, 12, 6
H = {1,8,9,64,65,72}
def cyclic_subgroup(p, modulus):
    out, x = set(), 1
    while x not in out:
        out.add(x)
        x = x*p % modulus
    return out

inversion = (1+4*((-2)*pow(4,-1,ELL) % ELL)) % (4*ELL)
decomposition = [cyclic_subgroup(p,4*ELL) for p in [5,13,137]]
intersection = set.intersection(*[D | {x*inversion % (4*ELL) for x in D}
                                  for D in decomposition])
assert H == {x % ELL for x in intersection if x % 4 == 1}
residue_degrees = {}
for p in [5,13,137]:
    x,f = p % ELL,1
    while x not in H:
        x,f = x*p % ELL,f+1
    residue_degrees[p] = f
assert residue_degrees == {5:12,13:12,137:1}
assert 32*ELL > d*N # Range8 impossible; even ranges at most6.
COSETS = []
unused = set(range(1, ELL))
while unused:
    C = {min(unused)*u % ELL for u in H}
    COSETS.append(C)
    unused -= C
assert len(COSETS) == d

def unique_permutations(counts, prefix=()):
    if len(prefix) == d:
        yield prefix
        return
    for j, count in enumerate(counts):
        if count:
            cc = list(counts)
            cc[j] -= 1
            yield from unique_permutations(cc, prefix+(j,))

def vectors():
    blocks = [[], []]
    domains = []
    bound = math.isqrt(d*N)
    for n0 in range(1,d+1):
        for n1 in range(d-n0+1):
            for n2 in range(d-n0-n1+1):
                ns = (n0,n1,n2,d-n0-n1-n2)
                S = sum(j*n for j,n in enumerate(ns))
                SS = sum(j*j*n for j,n in enumerate(ns))
                shifts = [m for m in range(-bound,bound+1)
                          if 4*ELL*SS-4*h*S*S+4*m*S+d*m*m <= d*N]
                if not shifts:
                    continue
                base = np.array(list(unique_permutations(ns)), dtype=np.int64)*2
                expected = math.factorial(d)//math.prod(math.factorial(n) for n in ns)
                assert len(base) == expected
                domains.append(dict(counts=ns, shifts=shifts, permutations=expected))
                for m in shifts:
                    blocks[m%2].append(base+m)
    result = [np.concatenate(blocks[parity]) for parity in [0,1]]
    for parity, block in enumerate(result):
        assert np.all(block % 2 == parity)
        assert np.all(ELL*(block*block).sum(axis=1)-h*block.sum(axis=1)**2 <= d*N)
        assert np.all(block.max(axis=1)-block.min(axis=1) <= 6)
    return result, domains

PAIRS = [(i,j) for i in range(d) for j in range(i,d)]
M = []
for i,j in PAIRS:
    raw = [0]*ELL
    for u in COSETS[i]:
        for v in COSETS[j]:
            raw[(u+v) % ELL] += 1
    assert all(len({raw[u] for u in C}) == 1 for C in COSETS)
    M.append([(raw[min(C)]-raw[0])*(1 if i==j else 2) for C in COSETS])
M = np.array(M, dtype=np.int64)
I = np.array([i for i,j in PAIRS])
J = np.array([j for i,j in PAIRS])

def squares(block):
    # Coefficients have abs <=46, raw convolution coefficients <155000,
    # and all intermediates are many orders below the int64 limit.
    assert np.max(np.abs(block)) <= 46
    result = (block[:,I]*block[:,J]) @ M
    trace = ELL*(block*block).sum(axis=1)-h*block.sum(axis=1)**2
    assert np.array_equal(-result.sum(axis=1),trace)
    return result

def direct_square(a):
    expanded = [0]*ELL
    for x,C in zip(a,COSETS):
        for c in C:
            expanded[c] = int(x)
    conv = [sum(expanded[j]*expanded[(k-j) % ELL] for j in range(ELL))
            for k in range(ELL)]
    assert all(len({conv[c] for c in C}) == 1 for C in COSETS)
    return tuple(conv[min(C)]-conv[0] for C in COSETS)

def representations(n):
    out = []
    for a in range(-math.isqrt(n), math.isqrt(n)+1):
        b = math.isqrt(n-a*a)
        if a*a+b*b == n:
            out.extend([(a,b)] if b==0 else [(a,b),(a,-b)])
    return out

(bv,av),domains = vectors()
assert (len(av),len(bv)) == (367578,377501)
print(json.dumps(dict(stage='vectors',counts=[len(av),len(bv)],
                      seconds=time.monotonic()-START)),flush=True)
bsquares = {}
for start in range(0,len(bv),4096):
    batch = squares(bv[start:start+4096])
    for offset,sq in enumerate(batch):
        bsquares.setdefault(sq.tobytes(),[]).append(start+offset)
solutions = []
for start in range(0,len(av),4096):
    batch = squares(av[start:start+4096])
    target = -N-batch
    for offset,sq in enumerate(target):
        for bi in bsquares.get(sq.tobytes(),[]):
            a = tuple(int(x) for x in av[start+offset])
            b = tuple(int(x) for x in bv[bi])
            # Independent direct-convolution validation of every survivor.
            assert all(x+y == -N for x,y in zip(direct_square(a),direct_square(b)))
            solutions.append((a,b))
gaussian_factors = [(u,v) for u,v in representations(Q//N) if u%2==1]
augmentations = [(x,y) for x,y in representations(Q) if x%2==0]
ray_survivors = []
for a,b in solutions:
    ar,br = h*sum(a)%ELL,h*sum(b)%ELL
    for u,v in gaussian_factors:
        gr,gi = (u*ar-v*br)%ELL,(u*br+v*ar)%ELL
        for x,y in augmentations:
            if (gr-x)%ELL == (gi-y)%ELL == 0:
                ray_survivors.append(dict(a=a,b=b,factor=[u,v],augmentation=[x,y]))
# Explicit positive controls: alpha=±11, beta=±4 have norm137.
assert all((tuple([-a]*d),tuple([-b]*d)) in solutions
           for a in [-11,11] for b in [-4,4])
out = dict(q=Q,ell=ELL,residual=N,H=sorted(H),residue_degrees=residue_degrees,
           cosets=[sorted(C) for C in COSETS],
           parity_vector_counts=[len(av),len(bv)],shape_domains=domains,
           unique_beta_squares=len(bsquares),residual_solution_count=len(solutions),
           nonrational_solution_count=sum(len(set(a))>1 or len(set(b))>1 for a,b in solutions),
           residual_solutions=[dict(a=a,b=b) for a,b in solutions],
           gaussian_factors=gaussian_factors,augmentations=augmentations,
           ray_survivor_count=len(ray_survivors),ray_survivors=ray_survivors,
           seconds=time.monotonic()-START,cpu_seconds=time.process_time()-CPU_START,
           numpy_version=np.__version__)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in {
    'cosets','shape_domains','residual_solutions','ray_survivors'}},indent=2))
