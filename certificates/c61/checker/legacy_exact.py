"""Class-group-free verification of all C61 ideal lattices, using exact arithmetic.

No PARI call, floating point, NumPy, class coordinates, or unit-group assumption.
Prime quotients are checked directly in the integral Gaussian-period ring.
Enumeration uses fraction-free LDL and rational interval bounds.
"""
import argparse
import json
import math
import resource
import signal
import sys
import time
from fractions import Fraction as F
from pathlib import Path

BASE = Path(__file__).resolve().parent
N = 20
Q = 8905
BOUND = 10


def rref(a, p):
    a = [[x % p for x in row] for row in a]
    pivots = []
    row = 0
    for col in range(len(a[0])):
        hit = next((k for k in range(row, len(a)) if a[k][col]), None)
        if hit is None:
            continue
        a[row], a[hit] = a[hit], a[row]
        inv = pow(a[row][col], -1, p)
        a[row] = [x*inv % p for x in a[row]]
        for k in range(len(a)):
            if k != row:
                c = a[k][col]
                a[k] = [(x-c*y) % p for x,y in zip(a[k],a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return a[:row], pivots


def annihilator(b, p):
    a, pivots = rref(list(zip(*b)), p)
    free = [j for j in range(N) if j not in pivots]
    null = []
    for j in free:
        v = [0]*N
        v[j] = 1
        for k,c in enumerate(pivots):
            v[c] = -a[k][j] % p
        null.append(v)
    return rref(null,p)


def matmul(a,b,p=None):
    bt = list(zip(*b))
    ans = [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]
    return ans if p is None else [[x % p for x in row] for row in ans]


def gram(b):
    cols = list(zip(*b))
    sr = [sum(c[:10]) for c in cols]
    si = [sum(c[10:]) for c in cols]
    g = [[0]*N for _ in range(N)]
    for j in range(N):
        for k in range(j,N):
            numerator = (122*sum(x*y for x,y in zip(cols[j],cols[k]))
                         - 12*(sr[j]*sr[k]+si[j]*si[k]))
            assert numerator % (2*Q) == 0
            g[j][k] = g[k][j] = numerator//(2*Q)
    return g


def ldl(g):
    """G=U^T diag(D) U; exact Bareiss pivots, no numerical factorization."""
    n = len(g)
    a = [row[:] for row in g]
    d, u = [], [[F(int(i==j)) for j in range(n)] for i in range(n)]
    previous = 1
    for k in range(n):
        pivot = a[k][k]
        assert pivot > 0
        d.append(F(pivot,previous))
        for j in range(k+1,n):
            u[k][j] = F(a[k][j],pivot)
        for i in range(k+1,n):
            for j in range(i,n):
                numerator = pivot*a[i][j]-a[i][k]*a[k][j]
                assert numerator % previous == 0
                a[i][j] = a[j][i] = numerator//previous
        previous = pivot
    return d,u,previous


def enumerate_short(d,u,bound=BOUND):
    n = len(d)
    if min(d) > bound:
        return [], 0
    z = [0]*n
    out = []
    nodes = 0

    def visit(k, remaining):
        nonlocal nodes
        nodes += 1
        if k < 0:
            if any(z):
                out.append(tuple(z))
            return
        center = sum((u[k][j]*z[j] for j in range(k+1,n)), F(0))
        radius_squared = remaining/d[k]
        den = center.denominator
        num = center.numerator
        span = math.isqrt(radius_squared.numerator*den*den//radius_squared.denominator)
        lower = -((span+num)//den)
        upper = (span-num)//den
        for value in range(lower,upper+1):
            term = d[k]*(F(value)+center)**2
            assert term <= remaining
            z[k] = value
            visit(k-1,remaining-term)
        z[k] = 0

    visit(n-1,F(bound))
    return out,nodes


def period_tensor():
    h = {pow(2,10*j,61) for j in range(6)}
    cosets = [sorted(pow(2,j,61)*a % 61 for a in h) for j in range(10)]
    assert sorted(a for c in cosets for a in c) == list(range(1,61))
    t = [[None]*10 for _ in range(10)]
    for j in range(10):
        for k in range(10):
            counts = [0]*61
            for a in cosets[j]:
                for b in cosets[k]:
                    counts[(a+b) % 61] += 1
            # 1 = -sum eta_j.
            t[j][k] = [counts[c[0]]-counts[0] for c in cosets]
            assert all(len({counts[x] for x in c}) == 1 for c in cosets)
    full = [[None]*N for _ in range(N)]
    for a in range(N):
        for b in range(N):
            ij = (a//10+b//10) % 2
            sign = -1 if a>=10 and b>=10 else 1
            v = [0]*N
            v[10*ij:10*ij+10] = [sign*x for x in t[a%10][b%10]]
            full[a][b] = v
    return full


def check_prime_quotients(data):
    tensor = period_tensor()
    pair_equations = []
    distinct = {5:set(),13:set(),137:set()}
    degrees = {5:0,13:0,137:0}
    assert len(data) == 14
    for p,f,b0,b1 in data:
        assert p in (5,13,137) and f == (1 if p==13 else 5)
        equations = []
        for b in (b0,b1):
            eq, piv = annihilator(b,p)
            assert len(eq) == f
            signature = tuple(map(tuple,eq))
            assert signature not in distinct[p]
            distinct[p].add(signature)
            degrees[p] += f
            # The quotient multiplication must factor through the projection eq.
            def proj(v):
                return [sum(x*y for x,y in zip(row,v)) % p for row in eq]
            qt = [[proj(tensor[a][b]) for b in piv] for a in piv]

            def mul(x,y):
                return [sum(x[s]*y[t]*qt[s][t][k]
                            for s in range(f) for t in range(f)) % p
                        for k in range(f)]
            columns = list(zip(*eq))
            for a in range(N):
                for b in range(N):
                    assert proj(tensor[a][b]) == mul(columns[a],columns[b])
            unit = proj([-1]*10+[0]*10)
            assert any(unit)

            def power(x,n):
                y = unit[:]
                while n:
                    if n & 1:
                        y = mul(y,x)
                    x = mul(x,x)
                    n //= 2
                return y
            eye = [[int(i==j) for j in range(f)] for i in range(f)]
            frobcols = [power(v,p) for v in eye]
            frob = list(map(list,zip(*frobcols)))
            iterate = eye
            for _ in range(f):
                iterate = matmul(iterate,frob,p)
            assert iterate == eye
            delta = [[frob[i][j]-eye[i][j] for j in range(f)] for i in range(f)]
            if f > 1:
                assert len(rref(delta,p)[1]) == f-1
            else:
                assert delta == [[0]]
            equations.append(eq)
        conjugate = [[x if j<10 else -x for j,x in enumerate(row)]
                     for row in equations[0]]
        assert rref(conjugate,p)[0] == equations[1]
        pair_equations.append((p,equations))
    assert degrees == {5:20,13:20,137:20}
    assert {p:len(v) for p,v in distinct.items()} == {5:4,13:20,137:4}
    return pair_equations


def check_membership(b,mask,pairs):
    for j,(p,choices) in enumerate(pairs):
        equations = choices[(mask>>j)&1]
        assert all(sum(row[k]*b[k][col] for k in range(N)) % p == 0
                   for row in equations for col in range(N))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot",action="store_true")
    parser.add_argument("--limit",type=int,default=16384)
    args = parser.parse_args()
    signal.alarm(1500)
    resource.setrlimit(resource.RLIMIT_CPU,(1200,1205))
    started = time.process_time()
    if args.pilot:
        reports = []
        for line in (BASE/"c61_lattice_pilot.log").read_text().splitlines():
            if line.startswith("PILOT_MATRIX="):
                mask, oldg,b = json.loads(line.split("=",1)[1])
                g = gram(b)
                assert all(g[i][j]*17810 == oldg[i][j] for i in range(N) for j in range(N))
                d,u,det = ldl(g)
                assert det == 61**18
                # Independently check factorization identity on this pilot.
                assert all(sum(d[k]*u[k][i]*u[k][j] for k in range(N)) == g[i][j]
                           for i in range(N) for j in range(N))
                vectors,nodes = enumerate_short(d,u)
                assert len(vectors) == (4 if mask==112 else 0)
                reports.append({"mask":mask,"count":len(vectors),"nodes":nodes,
                                "minimum_ldl_diagonal":str(min(d))})
        print(json.dumps({"pilot":reports,"cpu":time.process_time()-started},indent=2))
        return
    prime_data = json.loads((BASE/"c61_prime_lattices.json").read_text())
    pairs = check_prime_quotients(prime_data)
    print("All 28 prime quotient rings and conjugate pairs verified.",flush=True)
    positives = []
    total_nodes = 0
    count = 0
    with (BASE/"c61_lattice_full.jsonl").open() as stream:
        for line in stream:
            if count >= args.limit:
                break
            mask,b,reported,shortrows = json.loads(line)
            assert mask == count and len(b)==N and all(len(row)==N for row in b)
            assert all(type(x) is int for row in b for x in row)
            check_membership(b,mask,pairs)
            g = gram(b)
            d,u,det = ldl(g)
            assert det == 61**18  # proves |det B|=8905^10 from the exact Gram identity
            vectors,nodes = enumerate_short(d,u)
            total_nodes += nodes
            assert len(vectors) == reported
            reported_vectors = list(zip(*shortrows)) if shortrows else []
            signed = {tuple(v) for v in reported_vectors}
            signed |= {tuple(-x for x in v) for v in reported_vectors}
            assert set(vectors) == signed
            if vectors:
                values = [tuple(sum(b[i][j]*v[j] for j in range(N)) for i in range(N))
                          for v in vectors]
                positives.append([mask,[list(v) for v in sorted(values)]])
            count += 1
            if count % 1024 == 0:
                print(f"Verified {count}/16384; exact nodes={total_nodes}; CPU={time.process_time()-started:.2f}s",flush=True)
    assert count == args.limit
    if args.limit == 16384:
        certificate = json.loads((BASE/"c61_certificate.json").read_text())
        # Compare only after the independent exhaustive enumeration is finished.
        saved = {}
        for rec in certificate["weil_generators_period_coordinates"]:
            if isinstance(rec,dict):
                raise AssertionError("Inspect the portable schema before final comparison")
            mask,tors,a,b = rec
            saved.setdefault(mask,set()).add(tuple(a+b))
        assert {m:set(map(tuple,vs)) for m,vs in positives} == saved
    output = {"status":"COMPLETE" if count==16384 else "PARTIAL",
              "allocations":count,"prime_quotient_rings_verified":28,
              "positive_ideals":len(positives),"weil_vectors":sum(len(v) for _,v in positives),
              "exact_search_nodes":total_nodes,"cpu_seconds":time.process_time()-started,
              "positive_vectors":positives,
              "dependencies":"integral period ring and trace-AMGM lemma; no class group or units"}
    dest = BASE/("exact_lattice_check.json" if count==16384 else "exact_lattice_partial.json")
    dest.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({k:v for k,v in output.items() if k!="positive_vectors"},indent=2))


if __name__ == "__main__":
    main()
