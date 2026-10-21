#!/usr/bin/env python3
"""Independent check of the coverage claims of paper/main.tex (the recorded-coverage theorem of Sec. 1).

Standard library only (Python 3.9+).  Run from anywhere:

    python3 verify/verify_coverage.py [--limit N] [--q Q]

For every q = 1 (mod 4), 5 <= q < LIMIT (t = (q+1)/2, always odd) the script
computes the arithmetic predicates and re-implements, from the paper's theorem
statements, the uniform criteria O, FC, T1, T2, T4, T5, QE, C2_uniform,
Full_prime_fibre, Fixed_fibre, Doubling_origin.  It then compares them with
data/coverage.csv and re-derives the counts of the paper's coverage theorem.

A criterion "fires" at q when its hypotheses are satisfied by the guaranteed
multiplier group, so that a symmetric Turyn pair (A, B) of length t would be
excluded.  Nothing here uses the CSV when computing a flag; the CSV is read
only afterwards, for comparison.

Notation: t = (q+1)/2, eps = (-1)^((t-1)/2), H0 = H(t) the common multiplier
group of paper Section 2.1,
    H(m) = intersection over primes r | q of <r^e_r, -1> in (Z/m)^*,
    e_r = 1 if r = 1 (mod 4), 2 if r = 3 (mod 4).
"""

import argparse
import csv
import os
import sys
import time
from math import gcd, isqrt

# ---------------------------------------------------------------- arithmetic


def factorize(n):
    """Trial-division factorization -> dict prime -> exponent."""
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def is_prime_power(q):
    return len(factorize(q)) == 1


def is_sum_two_squares(q):
    return all(e % 2 == 0 for p, e in factorize(q).items() if p % 4 == 3)


def divisors(n):
    ds = [1]
    for p, e in factorize(n).items():
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return sorted(ds)


def omega(n):
    return len(factorize(n))


def phi(n):
    r = n
    for p in factorize(n):
        r = r // p * (p - 1)
    return r


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def mult_order(r, n):
    """Multiplicative order of r modulo n (gcd(r, n) = 1)."""
    if n == 1:
        return 1
    k, x = 1, r % n
    while x != 1:
        x = x * r % n
        k += 1
    return k


def cyc_group(r, e, m):
    """The subgroup <r^e, -1> of (Z/m)^*, as a set of residues."""
    g = pow(r, e, m)
    s = set()
    x = 1 % m
    while True:
        s.add(x)
        s.add((-x) % m)
        x = x * g % m
        if x == 1 % m:
            break
    return s


def common_group(q, m, qprimes):
    """H(m) of Section 2.1 (m coprime to q)."""
    H = None
    for r in qprimes:
        e = 1 if r % 4 == 1 else 2
        G = cyc_group(r, e, m)
        H = G if H is None else (H & G)
    return H


def orbits(H, n):
    """Orbits of the multiplicative group H (a set of residues) on Z/n.
    Returns (orbit id per residue, list of orbits as lists)."""
    oid = [-1] * n
    orbs = []
    for x in range(n):
        if oid[x] >= 0:
            continue
        o = sorted({x * h % n for h in H})
        k = len(orbs)
        for y in o:
            oid[y] = k
        orbs.append(o)
    return oid, orbs


# ------------------------------------------------------------- data per q


class Param:
    """Arithmetic data of one parameter q."""

    def __init__(self, q):
        self.q = q
        self.t = (q + 1) // 2
        self.qprimes = sorted(factorize(q))
        self.tf = factorize(self.t)
        self.tdivs = divisors(self.t)
        self.eps = -1 if ((self.t - 1) // 2) % 2 else 1
        self._H = {}

    def H(self, m):
        if m not in self._H:
            self._H[m] = common_group(self.q, m, self.qprimes)
        return self._H[m]

    @property
    def H0(self):
        return self.H(self.t)

    def fibre_in(self, group, n, h):
        """The elements of `group` (residues mod n, h | n) that are 1 mod h."""
        return [u for u in group if u % h == 1 % h]


# --------------------------------------------------------------- criteria
# Each returns (fired, detail string).


def crit_O(P):
    """Odd-index averaging (O), Sec. 2.2: for m | t, m > 1, H = H(m) of odd index d, firing when
    m^2 > 2^(2 omega(m) - 1) d^2 q."""
    hits = []
    for m in P.tdivs:
        if m == 1:
            continue
        H = P.H(m)
        d = phi(m) // len(H)
        if d % 2 == 1 and m * m > 2 ** (2 * omega(m) - 1) * d * d * P.q:
            hits.append("m=%d d=%d" % (m, d))
    return bool(hits), "; ".join(hits)


def crit_T2(P):
    """Prime-power quotient bound (T2), Sec. 2.2: m = l^a | t (l odd prime), H = H(m), d = phi(m)/|H|,
    c_d = sqrt2 (d odd) / 2 (d even).  Inequality
        c_d |H| <= min{ 2 sqrt(q) (1 - 1/l),  sqrt(q) + beta_l }
    violated.  Everything is decided in exact integer arithmetic."""
    q = P.q
    hits = []
    for l, a in P.tf.items():
        f = P.t // l
        beta2 = (f - 1) ** 2 + f * f
        for k in range(1, a + 1):
            m = l ** k
            Hn = len(P.H(m))
            d = phi(m) // Hn
            c2 = 2 if d % 2 else 4  # c_d^2
            x2 = c2 * Hn * Hn  # (c_d |H|)^2
            # first bound violated: x > 2 sqrt(q)(l-1)/l
            v1 = x2 * l * l > 4 * q * (l - 1) ** 2
            # second bound violated: x > sqrt(q) + beta
            s = x2 + q - beta2
            v2 = x2 > q and s > 0 and s * s > 4 * x2 * q
            if v1 or v2:
                hits.append("m=%d d=%d |H|=%d%s%s" % (
                    m, d, Hn, " [chord]" if v1 else "", " [box]" if v2 else ""))
    return bool(hits), "; ".join(hits)


def crit_T1(P, quotient=False):
    """Full-unit fibre bound (T1), Sec. 2.3: t = h m, gcd(h, m) = 1, m > 1, F_m = {u = 1 mod h}
    contained in H0 (so both rows are fixed by D1); a violation of
        q = 2hm - 1 <= (2h-1) 4^w + (2^w - 1)^2,   w = omega(m),
    excludes a pair.  The theorem proper is the case t' = t, W = 1 below.

    With quotient=True also the 'Quotient version of T1' (the corollary after T1) is
    used: t' | t, W = t/t', t' = h' m, F_m' = {u mod t' : u = 1 mod h'} in
    H(t'), violation of q <= (2h'-1) 4^w W^2 + (2^w W - 1)^2.
    The flag key T1 means the theorem proper (quotient=False); the corollary is
    reported separately (see NOTES.md)."""
    q = P.q
    hits = []
    for tp in P.tdivs:
        W = P.t // tp
        if tp == 1 or (not quotient and W != 1):
            continue
        Hl = P.H(tp)
        for m in divisors(tp):
            if m == 1 or gcd(m, tp // m) != 1:
                continue
            hp = tp // m
            w = omega(m)
            rhs = (2 * hp - 1) * 4 ** w * W * W + (2 ** w * W - 1) ** 2
            if q <= rhs:
                continue
            # the fibre group {1 + hp*j} (units mod m) must lie in H(t')
            ok = all((1 + hp * j) % tp in Hl
                     for j in range(m) if gcd(1 + hp * j, m) == 1)
            if ok:
                hits.append("t'=%d h'=%d m=%d W=%d" % (tp, hp, m, W))
    return bool(hits), "; ".join(hits)


def prime_fibre_data(P):
    """For every prime p with p || t: (p, h, |F_p cap H0|, index k)."""
    out = []
    H0 = P.H0
    for p, e in P.tf.items():
        if e != 1:
            continue
        h = P.t // p
        n = sum(1 for u in H0 if u % h == 1 % h)
        out.append((p, h, n, (p - 1) // n))
    return out


def crit_T4(P):
    """Index-two prime-fibre theorem (T4), Sec. 2.4: t = h p, p >= 7 prime, v_p(t) = 1, and the index
    [F_p : H0 cap F_p] <= 2 (F_p = units = 1 mod h, of order p-1)."""
    hits = ["p=%d k=%d" % (p, k) for p, h, n, k in prime_fibre_data(P)
            if p >= 7 and k <= 2]
    return bool(hits), "; ".join(hits)


def crit_T5(P):
    """Odd-index prime-fibre bound (T5), Sec. 2.5: k = [F_p : H0 cap F_p] odd and p > k^2 + k + 1
    (v_p(t) = 1; gcd(h, p) = 1)."""
    hits = ["p=%d k=%d" % (p, k) for p, h, n, k in prime_fibre_data(P)
            if k % 2 == 1 and p > k * k + k + 1]
    return bool(hits), "; ".join(hits)


def crit_FC(P):
    """Full-conductor necessity (FC), Sec. 3: F(4t, q) = 4t is necessary, where for p^a || t
        B_p = max_{r | q} [ v_p(r^(p-1) - 1) + v_p(ord_{4 rad t}(r)) ],
        F = 4 prod p^min(a, B_p).
    Fires when F != 4t, i.e. B_p < a for some p."""
    rad = 1
    for p in P.tf:
        rad *= p
    hits = []
    for p, a in P.tf.items():
        B = max(vp(pow(r, p - 1) - 1, p) + vp(mult_order(r, 4 * rad), p)
                for r in P.qprimes)
        if B < a:
            hits.append("p=%d a=%d B_p=%d" % (p, a, B))
    return bool(hits), "; ".join(hits)


def crit_prime_fibre(P):
    """Full prime-fibre obstruction (Full_prime_fibre), Sec. 5: for an odd prime p with v_p(t) = 1,
    t = h p, a pair fixed by every automorphism that is trivial on C_h and a
    unit on C_p exists only for (p, h) = (3, 1).  Here that automorphism group
    is F_p = {u mod t : u = 1 mod h}; fires when F_p <= H0 (index 1) and
    t != 3.  p = 3 is the C_3-inversion theorem of Section 5 (fibre of order 2)."""
    hits = ["p=%d" % p for p, h, n, k in prime_fibre_data(P)
            if k == 1 and P.t != 3]
    return bool(hits), "; ".join(hits)


def crit_C2(P):
    """Full three-fibre obstruction and its coordinate-free corollary
    (C2_uniform), Sec. 5: an involutive automorphism
    tau of C_t with exactly three elements g with tau(g) = -g cannot fix a
    pair unless |G| = 3.  In C_t an involution u (u^2 = 1) acts as +-1 on
    each p^a-component and the number of anti-fixed elements is the product of
    p^a over the components where u = -1.  Exactly three means: 3 || t,
    u = -1 mod 3 and u = +1 mod t/3.  Fires when this u lies in H0, t > 3."""
    if P.tf.get(3, 0) != 1 or P.t == 3:
        return False, ""
    h = P.t // 3
    # CRT: u = 1 mod h, u = 2 mod 3
    u = next(x for x in range(1, P.t) if x % h == 1 % h and x % 3 == 2)
    return u in P.H0, "u=%d" % u


# ---- quotient energy (Sec. 4) and the doubling-based tests (Sec. 4.1)


def qe_feasible(P, m):
    """Exact quotient-energy condition for M = H0 and the quotient C_m:
    do there exist X_c in S^A_c, Y_c in S^B_c with
    sum_c |c| (X_c^2 + Y_c^2) = q ?   Returns True when feasible."""
    q, t = P.q, P.t
    H0 = P.H0
    oid, orbs = orbits(H0, t)
    Im = {u % m for u in H0}
    cid, corbs = orbits(Im, m)
    # group the full orbits by quotient class
    wA = [[] for _ in corbs]
    wB = [[] for _ in corbs]
    for i, o in enumerate(orbs):
        x = o[0]
        c = cid[x % m]
        N = len(o) // len(corbs[c])
        if x != 0:
            wA[c].append(N)
        wB[c].append(N)
    R = isqrt(q)

    def signed_sums(ws):
        if not ws:
            return [0]
        T = sum(ws)
        mask = 1 << T
        for w in ws:
            mask = (mask << w) | (mask >> w)
        return [s for s in range(-min(R, T), min(R, T) + 1)
                if (mask >> (T + s)) & 1]

    full = (1 << (q + 1)) - 1
    reach = 1  # bit e set <=> energy e attainable by the classes so far
    for c, cl in enumerate(corbs):
        size = len(cl)
        XA = sorted({s * s for s in signed_sums(wA[c])})
        YB = sorted({s * s for s in signed_sums(wB[c])})
        vals = sorted({size * (a + b) for a in XA for b in YB if size * (a + b) <= q})
        if not vals:
            return False
        new = 0
        for v in vals:
            new |= reach << v
        reach = new & full
        if not reach:
            return False
    return bool((reach >> q) & 1)


def crit_QE(P):
    """Exact quotient-energy criterion (QE), Sec. 4, M = H0, applied at every divisor m | t (m = 1 gives
    the augmentation test; the odd-multiplicity energy floor is a
    relaxation of this exact test and adds nothing)."""
    hits = [str(m) for m in P.tdivs if not qe_feasible(P, m)]
    return bool(hits), "m=" + ",".join(hits) if hits else ""


def doubling_cycles_above_zero(P, m, oid, orbs):
    """Cycles of the doubling permutation on the nonzero H0-orbits that lie
    above the origin class of Z/m (orbits inside m Z/t), as (L_C, w_C)."""
    t = P.t
    seen = set()
    cycles = []
    for i, o in enumerate(orbs):
        x = o[0]
        if x == 0 or x % m != 0 or i in seen:
            continue
        L, j = 0, i
        while j not in seen:
            seen.add(j)
            L += 1
            j = oid[2 * orbs[j][0] % t]
        cycles.append((L, len(o)))
    return cycles


def crit_fixed_fibre(P):
    """Fixed origin fibre corollary (Fixed_fibre), Sec. 4.1: h | t, the image of H0 mod h contains 2.
    Then pi_m(B)_0 = B_0 [1 + eps (h-1)] and a pair needs [1+eps(h-1)]^2 <= q.
    No coprimality of h and m = t/h is assumed.  Fires on a violation."""
    q = P.q
    hits = []
    for h in P.tdivs:
        if h == 1:
            continue
        if any(u % h == 2 % h for u in P.H0) and (1 + P.eps * (h - 1)) ** 2 > q:
            hits.append("h=%d" % h)
    return bool(hits), "; ".join(hits)


def crit_doubling_origin(P):
    """Origin-coefficient set of Sec. 4.1 (Doubling_origin): for every m | t the projected origin
    coefficient of B is 1 + eps [ h - 1 - 4 sum_C w_C r_C ], h = t/m, with
    0 <= r_C <= floor(L_C/2) independent over the doubling cycles C of H0-orbits
    above the origin (B_0 = 1 normalised), and it must satisfy value^2 <= q.
    Fires when no admissible r makes value^2 <= q."""
    q, eps = P.q, P.eps
    oid, orbs = orbits(P.H0, P.t)
    hits = []
    for m in P.tdivs:
        h = P.t // m
        if h == 1:
            continue
        cyc = doubling_cycles_above_zero(P, m, oid, orbs)
        mask = 1  # attainable values of S = sum w_C r_C
        for L, w in cyc:
            new = 0
            for r in range(L // 2 + 1):
                new |= mask << (w * r)
            mask = new
        ok = False
        for S in range(mask.bit_length()):
            if (mask >> S) & 1 and (1 + eps * (h - 1 - 4 * S)) ** 2 <= q:
                ok = True
                break
        if not ok:
            hits.append("m=%d" % m)
    return bool(hits), "; ".join(hits)


CRITERIA = ["O", "FC", "T1", "T2", "T4", "T5", "QE", "C2_uniform",
            "Full_prime_fibre", "Fixed_fibre", "Doubling_origin"]


def evaluate(q):
    """-> (flags dict, detail dict, extra dict)."""
    P = Param(q)
    flags, det, extra = {}, {}, {}
    flags["O"], det["O"] = crit_O(P)
    flags["FC"], det["FC"] = crit_FC(P)
    flags["T1"], det["T1"] = crit_T1(P)
    extra["T1q"], extra["T1q_detail"] = crit_T1(P, quotient=True)
    flags["T2"], det["T2"] = crit_T2(P)
    flags["T4"], det["T4"] = crit_T4(P)
    flags["T5"], det["T5"] = crit_T5(P)
    flags["QE"], det["QE"] = crit_QE(P)
    flags["C2_uniform"], det["C2_uniform"] = crit_C2(P)
    flags["Full_prime_fibre"], det["Full_prime_fibre"] = crit_prime_fibre(P)
    flags["Fixed_fibre"], det["Fixed_fibre"] = crit_fixed_fibre(P)
    flags["Doubling_origin"], det["Doubling_origin"] = crit_doubling_origin(P)
    return flags, det, extra


# ------------------------------------------------------------------ driver

FRONTIER = {3965, 4745, 5185, 5525, 6409, 7565, 7685, 8245}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--limit", type=int, default=10000)
    ap.add_argument("--q", type=int, help="print per-criterion details for one q")
    ap.add_argument("--csv", default=None, help="path to coverage.csv")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    csv_path = args.csv or os.path.join(here, "..", "data", "coverage.csv")

    if args.q is not None:
        q = args.q
        if q % 4 != 1 or q < 5:
            sys.exit("q must be 1 mod 4 and >= 5")
        print("q=%d t=%d prime_power=%s sum_two_squares=%s" %
              (q, (q + 1) // 2, is_prime_power(q), is_sum_two_squares(q)))
        P = Param(q)
        print("q factorization: %s; t factorization: %s; eps=%d; |H0|=%d" %
              (factorize(q), factorize(P.t), P.eps, len(P.H0)))
        flags, det, extra = evaluate(q)
        for c in CRITERIA:
            print("  %-17s %-5s %s" % (c, flags[c], det[c]))
        print("  (T1 incl. quotient corollary 2.5: %s %s)" % (extra["T1q"], extra["T1q_detail"]))
        return 0

    rows = {}
    with open(csv_path, newline="") as fh:
        for r in csv.DictReader(fh):
            rows[int(r["q"])] = r

    t0 = time.time()
    ok = True
    qs = [q for q in range(5, args.limit, 4)]
    n_all = len(qs)
    arith_bad = []
    elig, ppow, sos = [], [], []
    comp = {c: [0, 0, []] for c in CRITERIA}  # agree, disagree, examples
    fired = {}
    t1q = {}
    for q in qs:
        pp, ts, el = is_prime_power(q), is_sum_two_squares(q), None
        el = (not pp) and ts
        if pp:
            ppow.append(q)
        if ts:
            sos.append(q)
        if el:
            elig.append(q)
        row = rows.get(q)
        if row is None:
            arith_bad.append((q, "missing from CSV"))
            continue
        if (str(pp), str(ts), str(el)) != (row["prime_power"], row["sum_two_squares"], row["eligible"]):
            arith_bad.append((q, "predicate mismatch"))
        # criteria are evaluated at EVERY parameter (the CSV also records
        # flags on the 1194 two-squares failures); only the eligible ones
        # enter the union.
        flags, det, extra = evaluate(q)
        fired[q] = {c for c in CRITERIA if flags[c]}
        t1q[q] = extra["T1q"]
        csvflags = set(f for f in row["criterion_flags"].split(";") if f)
        unknown = csvflags - set(CRITERIA)
        if unknown:
            arith_bad.append((q, "unknown CSV flag keys %s" % sorted(unknown)))
        for c in CRITERIA:
            if flags[c] == (c in csvflags):
                comp[c][0] += 1
            else:
                comp[c][1] += 1
                if len(comp[c][2]) < 8:
                    comp[c][2].append((q, "mine=%s csv=%s %s" % (flags[c], c in csvflags, det[c])))

    elig_set = set(elig)
    union = {q for q in elig if fired[q]}
    union2000 = {q for q in union if q < 2000}
    union_t1q = {q for q in elig if fired[q] or t1q[q]}
    pp_fired = {q: sorted(fired[q]) for q in ppow if fired[q]}

    out = []
    P_ = out.append
    P_("Independent verification of coverage below %d" % args.limit)
    P_("parameters q = 1 mod 4, 5 <= q < %d: %d" % (args.limit, n_all))
    P_("prime powers: %d; sum of two squares: %d; failing two-squares: %d" %
       (len(ppow), len(sos), n_all - len(sos)))
    P_("eligible (not prime power, sum of two squares): %d" % len(elig))
    P_("predicate agreement with CSV (prime_power, sum_two_squares, eligible): %s" %
       ("all %d rows agree" % n_all if not arith_bad else "%d PROBLEMS" % len(arith_bad)))
    P_("")
    P_("criterion agreement with CSV flags, all %d rows" % n_all)
    P_("  %-17s %8s %8s %8s" % ("criterion", "agree", "disagree", "fires"))
    for c in CRITERIA:
        nf = sum(1 for q in fired if c in fired[q])
        P_("  %-17s %8d %8d %8d" % (c, comp[c][0], comp[c][1], nf))
    P_("")
    P_("union of the criteria over eligible q:")
    P_("  below %d: %d" % (args.limit, len(union)))
    if args.limit >= 2000:
        P_("  below 2000: %d" % len(union2000))
    # additional recorded exclusions: read from the CSV status column
    addl = sorted(q for q, r in rows.items()
                  if q < args.limit and r["status"] == "EXCLUDED_ADDITIONAL_RECORDED_ARGUMENT")
    resid = sorted(elig_set - union - set(addl))
    P_("additional recorded exclusions read from CSV status: %d" % len(addl))
    P_("eligible - union - additional: %d members: %s" % (len(resid), resid))
    P_("  equals the eight stated frontier parameters: %s" % (set(resid) == FRONTIER))
    P_("  additional recorded exclusions are all eligible and outside the union: %s" %
       (set(addl) <= elig_set and not (set(addl) & union)))
    P_("union with the quotient corollary of T1 added: %d (%s)" %
       (len(union_t1q), "unchanged" if union_t1q == union else "CHANGED"))
    P_("prime-power control: %d prime powers, criteria firing at any: %d" %
       (len(ppow), len(pp_fired)))

    checks = []
    full = args.limit >= 10000
    checks.append(("predicates match CSV", not arith_bad))
    for c in CRITERIA:
        checks.append(("criterion %s matches CSV" % c, comp[c][1] == 0))
    checks.append(("prime-power control", not pp_fired))
    checks.append(("quotient corollary of T1 does not change the union", union_t1q == union))
    checks.append(("every CSV EXCLUDED_SELECTED_UNION row is in the union and conversely",
                   union == {q for q, r in rows.items() if q < args.limit and r["status"] == "EXCLUDED_SELECTED_UNION"}))
    if full:
        checks.append(("|union| = 644", len(union) == 644))
        checks.append(("|union below 2000| = 122", len(union2000) == 122))
        checks.append(("|eligible| = 663", len(elig) == 663))
        checks.append(("11 additional recorded exclusions", len(addl) == 11))
        checks.append(("frontier = the eight stated parameters", set(resid) == FRONTIER))
    P_("")
    for name, good in checks:
        P_("  [%s] %s" % ("ok" if good else "FAIL", name))
    ok = all(g for _, g in checks)
    for c in CRITERIA:
        for q, msg in comp[c][2]:
            P_("  DISAGREE %s q=%d: %s" % (c, q, msg))
    for q, msg in arith_bad[:10]:
        P_("  PROBLEM q=%d: %s" % (q, msg))
    P_("")
    P_("RESULT: %s" % ("ALL CHECKS PASSED" if ok else "MISMATCH FOUND"))
    print("\n".join(out))
    sys.stderr.write("runtime: %.1f s\n" % (time.time() - t0))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
