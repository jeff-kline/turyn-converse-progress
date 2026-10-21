"""Exact finite comparison of projected and conductor-local multipliers.

Standalone stdlib implementation. No existence conclusion from group sizes.
"""
import json
import math
import time
import signal
from pathlib import Path

START = time.monotonic()

def factors(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out

def divisors(n):
    ds = [1]
    for p, e in factors(n).items():
        ds = [d*p**k for d in ds for k in range(e+1)]
    return sorted(ds)

def subgroup(p, modulus):
    out = set()
    a = 1
    while a not in out:
        out.add(a)
        a = a*p % modulus
    return out

def local_group(primes, d):
    groups = [subgroup(p, 4*d) for p in primes]
    m = set.intersection(*groups)
    plus = {u % d for u in m if u % 4 == 1}
    return plus | {(-u) % d for u in plus}

def orbit_sizes(d, group):
    unseen = set(range(d))
    sizes = []
    for j in range(d):
        if j not in unseen:
            continue
        orb = {j*u % d for u in group}
        sizes.append(len(orb))
        unseen.difference_update(orb)
    return sizes

def inspect(q):
    t = (q+1)//2
    primes = list(factors(q))
    vg = local_group(primes, t)
    rows = []
    for d in divisors(t):
        if d == 1:
            continue
        old = {u % d for u in vg}
        new = local_group(primes, d)
        assert old <= new
        oldsz = orbit_sizes(d, old)
        newsz = orbit_sizes(d, new)
        row = dict(q=q, t=t, d=d, h=t//d, global_image=len(old),
                   local_image=len(new), old_orbits=len(oldsz),
                   new_orbits=len(newsz))
        if len(old) != len(new):
            row['old_group'] = sorted(old)
            row['new_group'] = sorted(new)
        rows.append(row)
    return rows

def main():
    signal.alarm(180)
    targets = [65, 185, 1325, 1469, 1937, 5185, 8865, 8905, 9265,
               9185, 37825, 62305, 93721]
    target_rows = {q: inspect(q) for q in targets}
    improved = []
    tested = 0
    for q in range(5, 10001, 4):
        fac = factors(q)
        if len(fac) < 2 or any(p % 4 == 3 and e % 2 for p, e in fac.items()):
            continue
        tested += 1
        for row in inspect(q):
            if row['new_orbits'] < row['old_orbits']:
                improved.append(row)
        if time.monotonic()-START > 150:
            raise RuntimeError('150 second procedural guard exceeded')
    result = dict(qmax=10000, tested=tested, improved_nodes=len(improved),
                  improved_q=len({r['q'] for r in improved}),
                  targets=target_rows, improvements=improved,
                  seconds=time.monotonic()-START)
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in {'improvements', 'targets'}}, indent=2))
    print('Target improvements:')
    for q, rows in target_rows.items():
        print(q, [{k:v for k,v in r.items() if not k.endswith('_group')}
                  for r in rows if r['new_orbits'] < r['old_orbits']])
    print('First ten improved nodes:')
    for r in improved[:10]:
        print(r)

if __name__ == '__main__':
    main()
