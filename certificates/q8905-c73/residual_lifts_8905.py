"""Independent exact lifting and cyclic convolution of residual8905 results."""
import json
import signal
import sys
import time
from pathlib import Path

signal.alarm(180)
start = time.monotonic()
base = Path(__file__).parent
data = json.loads((base/'residual_8905.json').read_text())
ell, h, fiber, q = 73, 6, 61, 8905
cosets = data['cosets']
coset_index = {x:j for j,C in enumerate(cosets) for x in C}
degree_counts = {}
for s in data['residual_solutions']:
    stabilizer_size = sum(all(s['a'][coset_index[x*u%ell]]==s['a'][j]
                              and s['b'][coset_index[x*u%ell]]==s['b'][j]
                              for j,C in enumerate(cosets) for x in C)
                          for u in range(1,ell))
    degree = (ell-1)//stabilizer_size
    degree_counts[degree] = degree_counts.get(degree,0)+1
assert degree_counts == {1:4,2:4,3:12}
def convolution(a,b):
    return [sum(a[j]*b[(k-j)%ell] for j in range(ell)) for k in range(ell)]

unique = {}
for s in data['ray_survivors']:
    a,b = s['a'],s['b']
    u,v = s['factor']
    X,Y = s['augmentation']
    ca = [u*x-v*y for x,y in zip(a,b)]
    cb = [u*y+v*x for x,y in zip(a,b)]
    assert (X-h*sum(ca)) % ell == (Y-h*sum(cb)) % ell == 0
    A0,B0 = (X-h*sum(ca))//ell,(Y-h*sum(cb))//ell
    A,B = [A0]+[0]*(ell-1),[B0]+[0]*(ell-1)
    for j,C in enumerate(cosets):
        for c in C:
            A[c],B[c] = A0+ca[j],B0+cb[j]
    boxes = abs(A0)<=fiber-1 and max(map(abs,A[1:]))<=fiber and max(map(abs,B))<=fiber
    parities = A0%4==(fiber-1)%4 and all(x%2 for x in A[1:]) and all(x%2 for x in B)
    assert sum(A)==X and sum(B)==Y
    assert all(A[j]==A[-j%ell] and B[j]==B[-j%ell] for j in range(ell))
    norm = [x+y for x,y in zip(convolution(A,A),convolution(B,B))]
    assert norm==[q]+[0]*(ell-1)
    if boxes and parities:
        unique[(tuple(A),tuple(B))] = dict(A=A,B=B,augmentation=[X,Y])
assert len(unique)==12

P0 = {pow(x,3,ell) for x in range(1,ell)}
P = [P0,{2*x%ell for x in P0},{4*x%ell for x in P0}]
assert len(P0)==24 and set.union(*P)==set(range(1,ell))
A=[8]+[0]*(ell-1)
B=[21]+[0]*(ell-1)
for C,a,b in zip(P,[-7,-1,7],[11,-11,3]):
    for c in C:
        A[c],B[c]=a,b
assert (tuple(A),tuple(B)) in unique
stabilizer = [u for u in range(1,ell)
              if all(A[u*j%ell]==A[j] and B[u*j%ell]==B[j] for j in range(ell))]
assert set(stabilizer)==P0
orbit = set()
for u in range(1,ell):
    for sa in [-1,1]:
        for sb in [-1,1]:
            orbit.add((tuple(sa*A[u*j%ell] for j in range(ell)),
                       tuple(sb*B[u*j%ell] for j in range(ell))))
assert orbit == set(unique)
period_products = []
for C in P:
    row = []
    for D in P:
        raw=[0]*ell
        for x in C:
            for y in D:
                raw[(x+y)%ell]+=1
        assert all(len({raw[j] for j in F})==1 for F in P)
        row.append([raw[0]]+[raw[min(F)] for F in P])
    period_products.append(row)
out=dict(q=q,ell=ell,fiber=fiber,input_ray_triples=len(data['ray_survivors']),
         residual_field_degree_counts=degree_counts,
         exact_marginal_count=len(unique),equivalence_orbits=1,
         cubic_classes=[sorted(C) for C in P],period_products=period_products,
         representative=dict(origin=[8,21],A_nonzero_class_values=[-7,-1,7],
                             B_nonzero_class_values=[11,-11,3],augmentation=[sum(A),sum(B)],
                             A=A,B=B),
         stabilizer=stabilizer,all_marginals=list(unique.values()),
         seconds=time.monotonic()-start)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in {
    'cubic_classes','representative','all_marginals','stabilizer'}},indent=2))
