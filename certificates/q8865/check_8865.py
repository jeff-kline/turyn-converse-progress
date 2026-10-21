"""Exact arithmetic checks for the q=8865 proof draft, no floating point.

The general algebraic-number-theory inferences are proved in SMALL-NORM.md;
this checks all numerical substitutions and the period trace matrix directly.
"""
import itertools
import json
import math
import sys
from pathlib import Path
from local_multiplier_probe import subgroup, local_group

q, ell = 8865, 31
assert q == 3**2 * 5 * 197
assert (q+1)//2 == 11*13*31
H = sorted(local_group([3, 5, 197], ell))
assert len(H) == 6 and 30 in H
cosets = []
seen = set()
for j in range(1, ell):
    if j not in seen:
        C = sorted({j*h % ell for h in H})
        seen.update(C)
        cosets.append(C)
assert len(cosets) == 5

# Full cyclotomic trace Tr_Q(zeta_31)/Q(zeta_31^a) is 30 at a=0 and -1 otherwise.
# Divide by |H|=6 for the trace from K.
gram = [[sum(30 if (a+b) % ell == 0 else -1 for a in A for b in B)//6
         for B in cosets] for A in cosets]
assert gram == [[31*(i==j)-6 for j in range(5)] for i in range(5)]

def residue_degree_K(p):
    a, f = p % ell, 1
    while a not in H:
        a = a*p % ell
        f += 1
    return f

degrees = {p: residue_degree_K(p) for p in [3,5,197]}
assert degrees == {3:5, 5:1, 197:5}
assert 14**2+1 == 197
assert 985*9 == q
reps = [(a,b) for a in range(-math.isqrt(985), math.isqrt(985)+1)
        for b in range(-math.isqrt(985), math.isqrt(985)+1) if a*a+b*b == 985]
even = sorted({a for a,b in reps if a % 2 == 0})
odd = sorted({a for a,b in reps if a % 2 == 1})
assert even == [-16,-12,12,16]
assert odd == [-29,-27,27,29]
assert not ({a % ell for a in even} & {b % ell for b in odd})

# Finite sanity check of the general trace bound (proof is not this enumeration).
min_trace = None
norm5 = []
vectors = list(itertools.product(range(-2,3), repeat=5))
small = []
for a in vectors:
    tr = 31*sum(x*x for x in a)-6*sum(a)**2
    if len(set(a)) > 1:
        min_trace = tr if min_trace is None else min(min_trace, tr)
    if tr <= 25:
        small.append((a,tr))
assert min_trace == 25
out = dict(q=q, t=(q+1)//2, quotient=ell, quotient_fiber=143,
           multiplier_H=H, period_cosets=cosets, trace_gram=gram,
           residue_degrees=degrees, nonrational_trace_lower_bound=25,
           residual_norm=5, gaussian_norm_after_dividing_3=985,
           augmentation_even_values=even, component_odd_values=odd,
           even_residues=sorted({a%31 for a in even}),
           odd_residues=sorted({a%31 for a in odd}),
           residue_intersection=[], finite_trace_check_vectors=len(vectors),
           finite_trace_minimum=min_trace)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
