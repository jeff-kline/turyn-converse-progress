"""Complete boxed correlation joins on a specified multiplier quotient.

Assumes the group is justified mathematically; checks every returned pair by
direct cyclic convolution. Uses only exact stdlib arithmetic.
"""
import argparse
import itertools
import json
import math
from pathlib import Path
import resource
import signal
import sys
import time


def cyclic(g, m):
    assert math.gcd(g, m) == 1
    out, x = set(), 1
    while x not in out:
        out.add(x)
        x = x * g % m
    return out


def factor(n):
    ans = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            ans[p] = ans.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        ans[n] = 1
    return ans


def local_group(q, m):
    # P1/P2's local group for an odd prime power m.
    if q <= 1 or q % 4 != 1:
        raise ValueError("q must exceed 1 and be 1 modulo 4")
    if m <= 1 or m % 2 == 0 or len(factor(m)) != 1:
        raise ValueError("the local multiplier theorem requires an odd prime power")
    if ((q+1)//2) % m:
        raise ValueError("the quotient modulus must divide t=(q+1)/2")
    groups = []
    for p in factor(q):
        c = cyclic(pow(p, 1 if p % 4 == 1 else 2, m), m)
        groups.append(c | {-x % m for x in c})
    return set.intersection(*groups)


def orbit_data(m, group):
    unseen = set(range(m))
    orbits = []
    while unseen:
        orb = sorted({min(unseen) * h % m for h in group})
        orbits.append(orb)
        unseen.difference_update(orb)
    assert orbits[0] == [0]
    owner = {x: i for i, orb in enumerate(orbits) for x in orb}
    tensor = []
    for oa in orbits:
        row = []
        for ob in orbits:
            counts = [0] * m
            for a in oa:
                for b in ob:
                    counts[(a+b) % m] += 1
            assert all(len({counts[x] for x in orb}) == 1 for orb in orbits)
            row.append(tuple(counts[orb[0]] for orb in orbits))
        tensor.append(row)
    return orbits, tensor


def square(c, tensor):
    n = len(c)
    out = [0] * n
    for i in range(n):
        for j in range(i, n):
            z = c[i] * c[j] * (1 if i == j else 2)
            for k in range(n):
                out[k] += z * tensor[i][j][k]
    return tuple(out)


def expand(c, orbits, m):
    out = [0] * m
    for value, orb in zip(c, orbits):
        for j in orb:
            out[j] = value
    return out


def direct_pair(a, b, q):
    n = len(a)
    return all(sum(a[j] * a[(k-j) % n] + b[j] * b[(k-j) % n]
                   for j in range(n)) == (q if k == 0 else 0)
               for k in range(n))


def reps(q):
    out = []
    for x in range(0, math.isqrt(q)+1, 2):
        y = math.isqrt(q-x*x)
        if y*y == q-x*x:
            out.append((x,y))
    return out


def candidates(q, f, sizes, total, real):
    domains = []
    for size in sizes[1:]:
        bound = min(f, math.isqrt(q // size))
        domains.append(tuple(v for v in range(-bound, bound+1) if v % 2))
    raw = math.prod(map(len, domains))
    rows = []
    for c in itertools.product(*domains):
        origin = total - sum(size*v for size,v in zip(sizes[1:], c))
        if real:
            if abs(origin) > f-1 or (origin-f+1) % 4:
                continue
        elif abs(origin) > f or origin % 2 != 1:
            continue
        energy = origin*origin + sum(size*v*v for size,v in zip(sizes[1:], c))
        if energy <= q:
            rows.append((origin,)+c)
    return rows, raw


def census(q, m):
    t = (q+1)//2
    assert t % m == 0
    f = t//m
    group = local_group(q,m)
    orbits, tensor = orbit_data(m,group)
    sizes = list(map(len,orbits))
    target = (q,)+(0,)*(len(orbits)-1)
    joins, solutions = [], []
    for x,y in reps(q):
        aa, raw_a = candidates(q,f,sizes,x,True)
        bb, raw_b = candidates(q,f,sizes,y,False)
        amap = {}
        for a in aa:
            amap.setdefault(square(a,tensor),[]).append(a)
        count = 0
        for b in bb:
            bs = square(b,tensor)
            want = tuple(z-v for z,v in zip(target,bs))
            for a in amap.get(want,()):
                av, bv = expand(a,orbits,m), expand(b,orbits,m)
                assert direct_pair(av,bv,q)
                assert sum(av) == x and sum(bv) == y
                solutions.append({"augmentation":[x,y],"A":a,"B":b})
                count += 1
        joins.append({"augmentation":[x,y],"raw_A":raw_a,"raw_B":raw_b,
                      "bounded_A":len(aa),"bounded_B":len(bb),
                      "distinct_A_squares":len(amap),"solutions":count})
    return {"q":q,"t":t,"modulus":m,"fiber":f,"group":sorted(group),
            "orbits":orbits,"sizes":sizes,"multiplication_tensor":tensor,
            "joins":joins,"solutions":solutions,
            "normalized_count":len(solutions),
            "signed_count":sum((2 if z["augmentation"][0] else 1)*2
                               for z in solutions)}


def main():
    resource.setrlimit(resource.RLIMIT_CPU,(120,120))
    signal.alarm(180)
    args = argparse.ArgumentParser()
    args.add_argument("--q",type=int,default=2105)
    args.add_argument("--moduli",type=int,nargs="+",required=True)
    args.add_argument("--output",type=Path,required=True)
    a = args.parse_args()
    start = time.process_time()
    out = [census(a.q,m) for m in a.moduli]
    usage = resource.getrusage(resource.RUSAGE_SELF)
    result = {"censuses":out,"cpu_seconds":time.process_time()-start,
              "process_cpu":usage.ru_utime+usage.ru_stime,
              "max_rss_bytes_macos":usage.ru_maxrss,"interpreter":sys.executable}
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"censuses":[{k:v for k,v in z.items()
                       if k not in {"multiplication_tensor","solutions","orbits","group"}}
                       for z in out],
                     "cpu_seconds":result["cpu_seconds"],
                     "max_rss_bytes_macos":usage.ru_maxrss},indent=2))


if __name__ == "__main__":
    main()
