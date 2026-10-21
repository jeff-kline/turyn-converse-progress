"""Exact colored theta-prefix factor filter on certified benchmark inputs."""
import collections
import hashlib
import json
from pathlib import Path
import resource
import signal
import sys
import time

resource.setrlimit(resource.RLIMIT_CPU, (90, 90))
signal.alarm(120)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT/"checker"))
import check_c61 as c

start = time.process_time()
data = json.loads((ROOT/"solver/q2561/prime_lattices.json").read_text())
plans = {}
for p in (13, 197):
    pairs, action = c.prime_quotients([row for row in data if row[0] == p], p)
    plans[p] = (pairs, c.allocation_orbits(action))
catalog = {p: {} for p in plans}
representative_records = []
for line in (HERE/"bases.jsonl").open():
    p, rep, b = json.loads(line)
    pairs, orbits = plans[p]
    c.check_membership(b, rep, pairs)
    g = c.norm_gram(b, p)
    d, u, determinant = c.ldl(g)
    assert determinant == 61**18
    vectors, nodes = c.enumerate_short(d, u, 100)
    ambient = []
    for v in vectors:
        w = tuple(sum(b[i][j]*v[j] for j in range(20)) for i in range(20))
        length = sum(v[i]*g[i][j]*v[j] for i in range(20) for j in range(20))
        assert 10 <= length <= 100
        ambient.append((length, w))
    representative_records.append({"p": p, "rep": rep, "nodes": nodes,
                                   "vectors": len(ambient)})
    for mask, (rotation, conjugation) in orbits[rep].items():
        assert mask not in catalog[p]
        counts = collections.Counter()
        for length, w in ambient:
            z = c.rotate(w, rotation)
            if conjugation:
                z = c.conjugate(z)
            parity = sum((x % 2) << j for j, x in enumerate(z))
            counts[(length, parity, 6*sum(z[:10]) % 61,
                    6*sum(z[10:]) % 61)] += 1
        catalog[p][mask] = counts
assert all(len(catalog[p]) == 1024 for p in plans)
indices = {p: [j for j, row in enumerate(data) if row[0] == p] for p in plans}


def restrict(mask, p):
    return sum(((mask >> j) & 1) << k for k, j in enumerate(indices[p]))


def fingerprint(counts, bound, multiplier=None):
    if multiplier is None:
        return tuple(sorted((*key, n) for key, n in counts.items() if key[0] <= bound))
    u, v = multiplier
    # Start from J, conjugate, then multiply by rho(gamma)/b.
    transformed = collections.Counter()
    for (length, parity, x, y), n in counts.items():
        if length <= bound:
            transformed[(length, parity, (u*x+v*y) % 61, (v*x-u*y) % 61)] += n
    return tuple(sorted((*key, n) for key, n in transformed.items()))


cert = json.loads((ROOT/"checker/q2561.json").read_text())
producer = json.loads((ROOT/"solver/q2561/results.json").read_text())
assert cert["status"] == "COMPLETE_INDEPENDENT_EXACT_CHECK"
assert set(map(tuple, cert["parity_values"])) == {
    tuple(a+b) for _, a, b in producer["parity"]}
inverse = pow(197, -1, 61)
assert inverse == 48
controls = 0
for mask, a, b in producer["parity"]:
    multiplier = (inverse*6*sum(a) % 61, inverse*6*sum(b) % 61)
    left = fingerprint(catalog[13][restrict(mask, 13)], 100)
    right = fingerprint(catalog[197][restrict(mask, 197)], 100, multiplier)
    assert left == right, ("Known Weil solution lost", mask, multiplier)
    controls += 1
augmentations = [(x, y) for x in (-44, -40, 40, 44)
                 for y in (-31, -25, 25, 31) if x*x+y*y == 2561]
reports = []
for bound in (60, 70, 80, 90, 100):
    left_counts = collections.Counter(fingerprint(counts, bound)
                                      for counts in catalog[13].values())
    uncolored = {
        p: collections.Counter(tuple(sum(n for key, n in counts.items() if key[0] == length)
                                     for length in range(1, bound+1))
                               for counts in catalog[p].values())
        for p in plans}
    uncolored_matches = sum(n*uncolored[197][key] for key, n in uncolored[13].items())
    per_augmentation = []
    for x, y in augmentations:
        multiplier = (inverse*x % 61, inverse*y % 61)
        right_counts = collections.Counter(fingerprint(counts, bound, multiplier)
                                           for counts in catalog[197].values())
        matches = sum(n*right_counts[key] for key, n in left_counts.items())
        per_augmentation.append({"augmentation": [x, y], "surviving_allocations": matches})
    reports.append({"bound": bound, "uncolored_survivors": uncolored_matches,
                    "colored_types_left": len(left_counts),
                    "per_augmentation": per_augmentation})
out = {
    "status": "COMPLETE_COLORED_FACTOR_PILOT_PENDING_SEPARATE_AUDIT",
    "q": 2561, "factor_orbits_each": 56, "enumeration_bound": 100,
    "checked_parity_Weil_positive_controls": controls,
    "reports": reports, "representatives": representative_records,
    "cpu_seconds": time.process_time()-start,
    "max_rss_macos_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "limits": {"cpu": 90, "wall": 120},
    "isolated": True, "interpreter": sys.executable,
    "basis_sha256": hashlib.sha256((HERE/"bases.jsonl").read_bytes()).hexdigest(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "complete_benchmark_sha256": hashlib.sha256((ROOT/"checker/q2561.json").read_bytes()).hexdigest(),
}
(HERE/"colored100.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps({k: v for k, v in out.items() if k != "representatives"}, indent=2))
