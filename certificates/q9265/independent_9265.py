"""Independent period-structure-constant checker for q=9265.

Construct the multiplier group rather than accepting its listed elements;
enumerate vectors by subset cardinality and exact trace; use a period
multiplication tensor instead of full-row cyclic convolution.
"""
import itertools
import json
import math
import signal
import sys
import time
from pathlib import Path
signal.alarm(120)
start = time.monotonic()
ell, q, residual = 113, 9265, 109
assert q == 5*17*109 and (q+1)//2 == 41*113

def cyc(a, modulus):
    out, x = set(), 1
    while x not in out:
        out.add(x)
        x = x*a % modulus
    assert x == 1
    return out

modulus = 4*ell
s = next(x for x in range(1, modulus) if x % 4 == 1 and x % ell == ell-1)
groups = []
for p in (5,17,109):
    D = cyc(p, modulus)
    groups.append(D | {x*s % modulus for x in D})
H = {x % ell for x in set.intersection(*groups) if x % 4 == 1}
cosets = []
seen = set()
for x in range(1, ell):
    if x not in seen:
        C = sorted(x*u % ell for u in H)
        cosets.append(C)
        seen.update(C)
h, d = len(H), len(cosets)
assert (h,d) == (14,8)
degrees = {}
for p in (5,17,109):
    z, f = p % ell, 1
    while z not in H:
        z, f = z*p % ell, f+1
    degrees[p] = f
assert degrees == {5:8,17:8,109:1}

# Each eta_j eta_k has integral period coefficients. The constant term
# is replaced by -sum eta_i. This implements Phi_ell=0 exactly.
tensor = []
for C in cosets:
    row = []
    for D in cosets:
        counts = [0]*ell
        for a in C:
            for b in D:
                counts[(a+b) % ell] += 1
        assert all(len({counts[c] for c in E}) == 1 for E in cosets)
        row.append(tuple(counts[E[0]]-counts[0] for E in cosets))
    tensor.append(row)

def square(a):
    result = [0]*d
    for j in range(d):
        for k in range(j,d):
            scale = a[j]*a[k]*(1 if j == k else 2)
            for i in range(d):
                result[i] += scale*tensor[j][k][i]
    return tuple(result)

def trace(a):
    return ell*sum(x*x for x in a)-h*sum(a)**2

# Q>=ell*(max-min)^2/2. Here d*N=872<8*ell=904, so a
# vector of uniform parity can only contain m and m+2. Its mean lies in
# [-sqrt(N),sqrt(N)], so |m|<=ceil(sqrt(N))+2 is safe.
assert d*residual < 8*ell
bound = math.isqrt(residual)+3
def enumerate_vectors(parity):
    result = []
    for r in range(d):  # r=d would not realize m as the minimum
        offsets = list(itertools.combinations(range(d), r))
        for m in range(-bound,bound+1):
            if m % 2 != parity:
                continue
            tr = d*m*m+4*r*m+4*r*(ell-h*r)
            if tr > d*residual:
                continue
            for S in offsets:
                a = tuple(m+2*(j in S) for j in range(d))
                assert trace(a) == tr
                result.append(a)
    return result

av, bv = enumerate_vectors(1), enumerate_vectors(0)
assert len(av) == len(set(av)) == 642
assert len(bv) == len(set(bv)) == 627
table = {}
for b in bv:
    table.setdefault(square(b), []).append(b)
solutions = []
for a in av:
    for b in table.get(tuple(-residual-v for v in square(a)), []):
        solutions.append((a,b))
assert len(solutions) == 4
assert all(len(set(a)) == len(set(b)) == 1 for a,b in solutions)
assert {(-a[0],-b[0]) for a,b in solutions} == {
    (x,y) for x in (-3,3) for y in (-10,10)}

# A genuine non-Gaussian positive control: the quadratic Gauss sum.
# H lies in the squares; chi is constant on each H-coset.
gauss = tuple(1 if pow(C[0],(ell-1)//2,ell) == 1 else -1 for C in cosets)
assert len(set(gauss)) == 2
assert square(gauss) == (-ell,)*d
assert trace(gauss) == d*ell
assert all(x % 2 == 1 for x in gauss)
assert square((-3,)*d) == (-9,)*d

# Once rationality is established, the parity and ell-ray force an
# even coordinate and an odd coordinate of norm q to agree mod ell.
even, odd = set(), set()
for x in range(math.isqrt(q)+1):
    y = math.isqrt(q-x*x)
    if x*x+y*y == q:
        for z in (x,-x,y,-y):
            (even if z % 2 == 0 else odd).add(z % ell)
assert not even & odd
out = dict(q=q,ell=ell,H=sorted(H),degrees=degrees,
    vectors=[len(av),len(bv)],solutions=len(solutions),
    gaussian_solutions=sorted([[-a[0],-b[0]] for a,b in solutions]),
    positive_nonrational_control=dict(norm=ell,period_vector=gauss),
    even_residues=sorted(even),odd_residues=sorted(odd),intersection=[],
    seconds=time.monotonic()-start)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
