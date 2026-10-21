"""Re-check the shipped certificates (standard library only).

Usage:  python check_certificates.py [--fast]
  --fast skips the 2561 factor-match run (about 1-2 minutes of CPU).
Shipped scripts are run in a temporary copy so the shipped files stay
untouched; .gz files are unpacked there. The 8905 C73 enumeration
(q8905-c73/residual_8905.py) needs numpy and is NOT run here; the shipped
residual_8905.json is used as its recorded output. Order 7929 needs the
archived v0.2.0 code and numpy and is not run here (see README.md).
This script does not re-prove the mathematics; it re-executes the finite
computations behind each exclusion and asserts their stated outcomes.
"""
import gzip, json, math, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "local-ray"))
import correlations as c  # shipped copy of the audited quotient engine

results = []


def report(q, what, ok):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  q={q:<5} {what}")


def ord_mod(a, m):
    k, x = 1, a % m
    while x != 1:
        x, k = x * a % m, k + 1
    return k


def self_conjugacy(q):
    """Proposition (inert tower) of the archived paper, case (ii)."""
    t = (q + 1) // 2
    divs = [d for d in range(1, t + 1) if t % d == 0]
    for l, k in c.factor(q).items():
        if l % 4 == 3 and (k % 2 == 1 or all(ord_mod(l, d) % 2 == 1 for d in divs if d > 1)):
            return True
    return False


def full_unit_ray(q, P):
    """Prime P | t with full local group and no Gaussian ray U - V = P(a+ib)."""
    t, f = (q + 1) // 2, (q + 1) // 2 // P
    if len(c.local_group(q, P)) != P - 1:
        return False
    eo = c.reps(q)
    oe = {(sx * y, sy * x) for x, y in eo for sx in (-1, 1) for sy in (-1, 1)}
    for x, y in eo:
        for u, v in oe:
            if (x - u) % P == 0 and (y - v) % P == 0:
                a, b = (x - u) // P, (y - v) // P
                if a % 2 and b % 2 and abs(a) <= f and abs(b) <= f:
                    return False
    return True


def staged(tmp):
    dst = Path(tmp) / "work"
    shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns("check_certificates.py"))
    for gz in list(dst.rglob("*.gz")):
        with gzip.open(gz, "rb") as s, open(gz.with_suffix(""), "wb") as d:
            shutil.copyfileobj(s, d)
        gz.unlink()
    return dst


def run(cwd, *args):
    subprocess.run([sys.executable, *args], cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def load(p):
    return json.loads(Path(p).read_text())


def main():
    fast = "--fast" in sys.argv
    report(1845, "self-conjugacy (inert tower) obstruction", self_conjugacy(1845))
    for q, P in ((909, 7), (6137, 11), (7461, 7), (9245, 23)):
        report(q, f"full-unit Gaussian ray test at C{P}", full_unit_ray(q, P))
    r = c.census(2665, 43)
    report(2665, "complete C43 quotient census has no solution, 4 augmentations",
           r["normalized_count"] == 0 and len(r["joins"]) == 4)
    with tempfile.TemporaryDirectory() as tmp:
        w = staged(tmp)
        run(w / "q8865", "check_8865.py")
        d = load(w / "q8865/check_8865.json")
        report(8865, "C31: even/odd residues disjoint, trace minimum 25, norm-5 residual",
               d["residue_intersection"] == [] and d["finite_trace_minimum"] == 25)
        run(w / "q9265", "independent_9265.py")
        run(w / "q9265", "residual_9265.py")
        a, b = load(w / "q9265/independent_9265.json"), load(w / "q9265/residual_9265.json")
        report(9265, "C113: 4 residuals, residues disjoint, ray survivors 0",
               a["solutions"] == 4 and a["intersection"] == []
               and b["ray_survivor_count"] == 0 and b["residual_solution_count"] == 4)
        run(w / "q8905-c73", "residual_lifts_8905.py")
        lifts = load(w / "q8905-c73/residual_lifts_8905.json")
        run(w / "c61", "checker/check_c61.py", "--case", "solver/q8905", "--q", "8905",
            "--streams", "solver/q8905/lattice-000.jsonl", "solver/q8905/lattice-001.jsonl",
            "--output", "out8905.json", "--require-local-invariance")
        o = load(w / "c61/out8905.json")
        spec61 = {tuple(x) for x in o["absolute_augmentation_spectrum"]}
        spec73 = {(abs(m["augmentation"][0]), abs(m["augmentation"][1]))
                  for m in lifts["all_marginals"]}
        report(8905, f"C61 spectrum {sorted(spec61)} vs C73 spectrum {sorted(spec73)} disjoint; "
               "C61 8 marginals; C73 12 marginals",
               not (spec61 & spec73) and o["boxed_marginal_count"] == 8
               and lifts["exact_marginal_count"] == 12)
        if not fast:
            run(w / "c61", "factor-match/colored100.py")
            reps = load(w / "c61/factor-match/colored100.json")["reports"]
            ok = all(sum(x["surviving_allocations"] for x in rep["per_augmentation"]) == 0
                     for rep in reps if rep["bound"] >= 80)
            report(2561, "factor-match: 0 surviving allocations at cutoffs 80, 90, 100", ok)
    ar = load(HERE / "q2561-short/augmentation-residues.json")
    X = {tuple(p) for p in ar["augmentation_residue_pairs_mod61"]}
    Wl = {tuple(p) for p in ar["complete_parity_Weil_residue_pairs_mod61"]}
    norms = [(x, y) for x in range(-50, 51) for y in range(-50, 51)
             if x * x + y * y == 2561 and x % 2 == 0 and y % 2 == 1]
    report(2561, "augmentation residues mod 61 disjoint from parity-census residues",
           not (X & Wl) and {(x % 61, y % 61) for x, y in norms} == X
           and sorted(map(tuple, ar["complete_signed_augmentations"])) == sorted(norms))
    print(f"{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
