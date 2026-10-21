# Mathematical audit: quotient energy, three-fibre, catalogs, mod-16, coverage logic

Auditor: read-only mathematical auditor; I did not write the manuscript.
Target: `paper/main.tex` (2587 lines, state of 2026-10-21).
Scope: lines 878-1144, 1145-1406, 1407-1669 and 1670-1916, plus 2206-2356
for logic only.
Sources under `quarantine/` were not needed. No doubt arose that the
manuscript text and hand re-derivation could not settle.

## Method

- I re-derived every statement and proof in scope by hand: hypotheses,
  algebra, parity and trace arguments, and index ranges.
- I checked numerical claims and identities with exact scripts in `review/`.
  Each script ran in the project venv under `ulimit -t`. Total CPU was
  about 50 s.
  - `audit_s47_arith.py`: examples at 8281, 4685, 9809, 6437, 7625 and
    3965, and the category counts 2499/642/1194/663 and 499/164/211/124.
    Everything matches.
  - `audit_s47_mod16.py`:
    - Theorem `thm:mod16` holds as an identity for random symmetric P on 16
      groups: C_3, C_5, C_7, C_9, C_11, C_13, C_15, C_21, C_25, C_27,
      C_3^2, C_5^2, C_3xC_9, C_3^3, C_5xC_3 and C_7xC_3. Every case gave
      divisibility by 8 and F(P) = D(defect/8) mod 2.
    - `eq:semilinear`, `eq:classzero`, the class-y/class-y^2 conjugacy and
      the elimination identity behind `eq:forced` were evaluated in
      F_2[x]/Phi_p. Pairs (p, h): (5,2), (13,6), (29,14), (29,2), (37,6),
      (37,18), (53,26), (61,10), (61,30), (101,10). All hold.
    - The Gram matrix Tr(theta_i theta_j) = 1 + [j = i+n] and the
      self-duality of the H-periods hold.
    - Exhaustive forced-fibre test at (5,2), (13,6), (29,14) and (37,18).
      Every full mod-16 solution with v not in K_2 has the predicted u, and
      it is unique. The test is nonvacuous: 4 such solutions at each of the
      first three.
    - The trace-filter identity `eq:trace-filter` holds for random P under
      the reading stated in item P-5 below.
  - `audit_s47_threefibre.py`: exhaustive count of tau-fixed symmetric pairs
    on H x C_3 for H = C_1, C_3, C_5, C_7, C_9, C_3xC_3, C_11 and C_13.
    The only pairs are the 4 at h = 1, as Theorem `se-thm-three` states.
  - `audit_s47_c3forcing.py`: the 3965 C_3 data are the unique solution of
    the run-count parametrization: Abar = (0,11,11), Bbar = (61,-1,-1),
    (k,r) = (65,33) and (33,18).
  - `audit_s47_qe.py`, `audit_s47_flags.py` and `audit_s47_fibre_flags.py`
    recompute five criteria with the FULL-modulus H_0 over all 663 eligible
    rows of `materials/coverage.csv`:
    - QE (exact knapsack over all m | t, m < t);
    - Fixed_fibre (2 in H_0 mod h);
    - Doubling_origin (formula `se-eq-origin-set`);
    - C2_uniform (3 || t and the pure 3-fibre in H_0);
    - Full_prime_fibre (p || t and the pure p-fibre in H_0, with p = 3 also
      counted).

    All five reproduce the recorded flags with 0 mismatches. The
    odd-multiplicity floor never fired where the exact knapsack was
    feasible. 4705 (m = 13) and 4525 (m = 31) are infeasible, as stated.
    This was a hypothesis check, not a data audit.

Not rerun (data, outside a logic audit):
- the 2561 and 8905 census counts (16384, 88/44/8, 1048576, 504/252);
- the length-80 factor-lattice enumeration;
- the 77-digit prime;
- the p = 101 exhaustive count (620 / 0);
- the saved 3965 outer word (weight 310, ranks 66/67, XOR of 35 rows,
  37/29 phases).

Two figures in this list were checked: the 56 Galois orbits per factor at
2561 (by a Burnside count, 1120/20 = 56) and the 2^20 = 1048576 allocations.

## Verdicts

### Exact quotient energy and coupled doubling cycles (878-1144)

| Item | Verdict | Note |
|---|---|---|
| Thm `se-thm-qe` (QE), 897-941 | OK | Fibre constancy, the class values and the converse are exact. The knapsack is exact. The A-origin set excludes O_0 (sum over i != 0), and the B-origin set includes O_0 with weight 1. The identity coefficient equals a sum of squares because -1 is in M. |
| Full quotient condition `se-eq-qf`, 943-957 | OK | The lag-r autocorrelation equals (A^2)_r by symmetry. |
| Cor `se-cor-floor`, 959-980 | MINOR | The mathematics is correct: d = max(0, w-R) for odd n, d = 0 otherwise, and O_0 is excluded from the A-origin multiset. Wording: "For each of S^A_c and S^B_c, consider its multiset of weights" (961). These are sets of sums; say "the multiset {N_i : c(i)=c} (i != 0 for A)". |
| m = 1 congruences `se-eq-augmentation` and the 8281/4685 examples, 982-999 | MINOR | All claims verified: orbit inventories; A(1) mod 20 = {0} and B(1) = +-1 mod 20 at 8281; A(1) = +-2 and B(1) in {+-1, +-3} mod 20 at 4685; neither representation is feasible. Wording: 8281 follows from the plain congruence with g = 10. Only 4685 needs the "sharpened" inventory, but the "For example" after "can be sharpened" (990) suggests both do. |
| 9809 floor, 4705 and 4525, 1001-1012 | OK | Weights fifteen 36s, one 4 and one 1. The origin omits the 1 for A. The floor is 17361. 4705 and 4525 are infeasible. |
| Thm `se-thm-runs`, 1024-1076 | MINOR | The run bounds, node and edge sums, sufficiency, and the equivalence "fixes every class iff 2 in I_m" (via the class of 1) are correct. Reference gap: the "only if" direction concerns rows that satisfy the equation only **mod 8**. It uses B_j = eps*B_0*A_j*A_{2j}, but Lemma `lem:doubling` (220-222) states the forward direction for exact pairs. Its proof uses the equation only mod 8, so the result holds. State that, e.g. "by the proof of Lemma 1.x, which uses (1.1) only modulo 8". |
| Origin set `se-eq-origin-set`, 1078-1092 | OK | sum of w_C*L_C = t/m - 1. Every r in [0, floor(L/2)] is attainable. |
| Cor `se-cor-fixed`, 1094-1111 | OK | Uses u in M (full modulus) with u = 2 mod h, as required, not a local group. All Fixed_fibre flags reproduce with the global H_0. |
| 6437 and 7625 examples, 1113-1143 | OK | 6437: |M| = 72, cycles (14,72), (2,18), (7,4), total 1072, eps = -1, and the exact minimum of |pi_3(B)_0| is 81. 7625: |M| = 40, 125 = -61^19 mod 3813, 125 is in M, 125 = 2 mod 123, eps = +1, and 123^2 > 7625. |

### A uniform obstruction to inversion of a three-element factor (1145-1406)

| Item | Verdict | Note |
|---|---|---|
| Lemma `se-lem-transfer` | OK | phi(Lambda) and (phi∘sigma)(Lambda) are roots of 3z^2 - 2phi(E)z - q. Distinct roots would have product -q/3, which is rational but not an integer because 3 does not divide q. Characters separate. No hypothesis on H is needed. |
| Lemma `se-lem-support` | OK | sigma_2 D - D = J - delta + 2Q. The + sign would give phi(Q) = 1/2. Fourier inversion gives E + sigma_2 E = 2 eps J, and D = eps 1_W follows because g/2 lies in 2W. |
| Thm `se-thm-three`, 1203-1343 | MINOR (notation only) | Every step was re-derived; the full chain is in the next subsection. Notation: the proof applies the doubling identity "at the nonzero coordinate (s,1)" (1322), while the same theorem writes C_3 multiplicatively ((g,y) to (g,y^{-1}), U + S(y+y^2)). Read multiplicatively, (s,1) is the identity slice, which gives the wrong equation. Write (s,y). |
| Cor `se-cor-involution` | MINOR | "an involution of G" (1347) must be an involutive **automorphism**. The proof uses that the fixed and anti-fixed sets are subgroups. |
| Cor `se-cor-prime` | OK | The excess 2(p-1)[h(p-4)+1] was re-derived. The p = 3 case reduces to the theorem. |
| CRT remark, 1387-1392 | OK | It correctly requires p not dividing h for cyclic t. The C2_uniform flags fire only when 3 || t (t mod 9 is 3 or 6), and they reproduce exactly. |
| Remark, 1394-1404 | MINOR | "removes any cyclicity or coprimality assumption on the complementary group" (1398-1399) is true for H x C_3. A reader may take it to cover C_t with 9 dividing t, which it does not (see 1387). Add "for groups of the form H x C_3". |

#### The three-fibre chain, step by step

1. The slice identities follow from the two C_3 characters.
2. |Z| + |Z'| = (h-1)/2, and eps D + D^2 + F^2 = c delta.
3. The F_2 cover count forces Z' empty and Z ⊔ 2Z = H \ 0, so c is odd and
   h = 1 mod 4. Then 4Z = Z, hence W = 2Z, 2W = Z and 4W = W.
4. The mod-4 sign rule `se-eq-signrule` was re-derived: with h = 4k+1,
   c = 6k+1 and 3k+1 = k+1 mod 2. c_W(s) is even with no diagonal term, and
   c_W(4s) = c_W(s), so sigma_4 E = E.
5. Lambda = U + S was checked coordinatewise. 4·(slice2) - (slice1) gives
   Lambda(3 Lambda - 2E) = q delta. The transfer lemma then gives
   sigma_4 S = S.
6. The doubling sign (-1)^{(3h-1)/2} = -1 and T = -F, V = F give
   F_s = F_0 S_s S_{2s}, hence F_{2s} = F_s and sigma_2(E)^2 = E^2.
7. The support lemma gives E(1) = eps h.
8. h^2 + 4f^2 = 6h - 1 gives (h-1)(h-5) <= 0, so h is 1 or 5. At h = 5,
   f^2 = 1 and v^2 = 28.
9. At h = 1 there are exactly 4 pairs.

No cyclicity is used: sigma_2, sigma_4 and characters exist on any odd
abelian H. An exhaustive check found no pairs for h = 3, 5, 7, 9 (both
groups), 11 and 13.

### Exact norm lattices and arithmetic transport (1407-1669)

| Item | Verdict | Note |
|---|---|---|
| Lemma `lem:period-trace` | OK | T = ell I - hJ, det = ell^{d-1}, the compositum O_L = O_K[i], the trace-form identity, and the bound h(d-1)+1 = ell-h. |
| Prop `prop:smallnorm` | MINOR | The proof is correct, including the parity costs 4h(d-1)+d and 4h(d-1)+4, the even-degree subfield Q(sqrt ell) and x = r sqrt(ell) with r in Z. Wording: "their combined cost is 8(ell-h)+d-4" (1469) should read "at least". |
| 8865 sketch, 1475-1482 | OK | Here ell = 31, h = 6, d = 5 (local group {1,5,6,25,26,30} recomputed), and dN = 25 = ell - h with d odd. The residues reconcile: the Gaussian integers of norm 985 have odd real parts +-27, +-29 and even real parts +-12, +-16 (= 36/3, 48/3), and these sets are disjoint mod 31. |
| Thm `thm:trace-minimal` | OK | N(I) = q^d, then AM-GM over the d conjugates of x xbar in L^+, using Tr_L = 2 Tr_{L^+}, which is left implicit. |
| Q_I integrality, det = ell^{2d-2}, allocation exhaustiveness | OK | x ybar / q lies in O_K[i]. The normalized length is at least d, with equality iff x xbar = q. |
| 8905 and 2561 census logic, 1522-1540 | OK (logic) | 72^2 + 61^2 = 16^2 + 93^2 = 8905, and the augmentations at C_61 and C_73 are incompatible. At 2561 the residues {+-21, +-17} are disjoint from the listed set, and 40/31 and 44/25 are the only representations. The local groups at 61 and 73 were recomputed. |
| Thm `thm:factor` | MINOR | The isometry and the mod-2 color are correct. The color map writes (alpha/b)·conj(rho(x)) (1553). This equals rho of the image only if rho is a ring homomorphism that commutes with conjugation (reduction modulo a conjugation-stable ideal) and extends to b^{-1}. That hypothesis is not stated. Either state it or write rho(xbar). |
| Thm `thm:ray-transport` | MINOR | Mathematically correct. I checked: (beta) = P/P_0 with beta = 1 mod* m (no real places); lambda_T conj(lambda_T) = N(beta) = p/p_0 > 0; the 1/p versus 1/p_0 normalization cancels; colors are preserved because (lambda-1)x lies in m at modulus primes and is integral elsewhere; Delta = N_{L/Q(i)}(beta) gives pi = pi_0 mod N; and the bijection z·pi to z·pi_0 holds. Wording: the statement does not say that the "allocation lattices" are those of norm p and p_0 (the I_p(T) of the proof). Also, N denotes the modulus integer, an ideal norm and the Gaussian norm in the same proof (1577, 1612-1613). |
| Cor `cor:ray-family` | OK | 197 = 14 mod 61 lies in H and 197 = 1 mod 4, so 197 splits completely. Norms give p = 197 mod 122, and splitting in Q(i) gives mod 244 (consistent with 1660). 61 divides t, and H(61) = H for both prime factors. The Chebotarev identification handles conjugates correctly through "some prime P". The claim is only positive natural density among primes, and q = 13p is counted by delta·Li(X/13). It makes no density claim among integers. |

### A quadratic mod-16 criterion and forced reconstruction (1670-1916)

| Item | Verdict | Note |
|---|---|---|
| Thm `thm:mod16` | OK | Re-derived in full; details in the next subsection. Also confirmed numerically on 16 cyclic and non-cyclic groups. |
| Orbit-quadratic remark, 1737-1746 | OK | eta is linear in the orbit bits (sum of x_i·|E_i|/2). The cross terms E_iE_j and E_iD E_j + E_jD E_i are correct. |
| Thm `thm:forced` | OK | Re-derived in full; details in the next subsection. It is an at-most-one statement, and 1774-1775 say so. |
| Prop `prop:residual` | OK | u^2 + alpha·u = beta, a_0 = d_0/(v v*), and the compatibility equation was derived (a_0^2 times the residual). The class-zero constant is floor(c/2) = 1. The class-y component is the conjugate of the class-y^2 component (checked numerically). A C-invariant component vanishing at zeta is 0 or J, and the C_3 projection decides which. |
| Remark 1851-1855 | OK | h = (p-1)/2 = 2 mod 4 and n = 2. The text claims no infinite exclusion family. |
| 3965 consequence, 1858-1868 | OK | p = 661 = 5 mod 8, h = 10, n = 66, and 2 reaches all 66 cosets of H. |H_0| = 10 and there are 199 orbits in cycles of length 132, 66 and 1. The C_3 forcing is unique (checked). |V| = 5·65 = 325 is odd and |U| = 10·33 = 330, and 198 - 66 = 132. 3965 stays open (1673-1674, 1871-1876, 2301, 2318). |
| Trace filter, 1878-1898 | MINOR | The identity is true. It holds for arbitrary normalized P, not only for solutions. The limitation argument is correct: summing over all n rotations gives 3|a||y| = |x||y| = 1, so the left sides are not all equal. Clarity: the text leaves several conventions implicit, as listed in item P-5. |

#### Details: Theorem `thm:mod16`

- The sign rule for Q and the formula for |Q| are correct, and p_0 and T_0
  are both even.
- The expansion gives the defect as 4[P^2 + Q^2 + P + alpha J - c delta].
  The half-numerator was checked in both cases e = 0 and e = 1.
- The symmetric-difference identity for W holds, and W(K_0)_s = c - 1.
- The cancellation of P_{s/2}P_s and the origin check (defect exactly 0
  at the origin) are both correct.

#### Details: Theorem `thm:forced`

- Hypotheses present: p = 5 mod 8, h = 2 mod 4, n even, and 2 generates
  F_p*/H. The condition p = 5 mod 8 is in fact implied by the other three.
- "2 generates mod C and 2^n C = -C": if 2 = gamma^m with gcd(m, n) = 1
  and n even, then m is odd and mn = n mod 2n.
- Trace counts: g - [j = i+n] for the C-periods and h - [i = j] for the
  H-periods, with an even zero contribution in both. (J+R)^2 = I.
- Tr(v) = |V| mod 2.
- The nonzero denominator: d_0 = 0 would make v/v* a cube root of unity.
  That root lies in F_4, which is inside K_2 because n is even, so the
  involution fixes it and inverts it. That forces v = v*, contradicting
  v not in K_2.
- The numerator v w + v* w* + v v* d_0 was re-derived.

### Coverage logic (2206-2356)

| Item | Verdict | Note |
|---|---|---|
| Thm `thm:coverage` and its proof; Tables `tab:coverage`, `tab:additional`, `tab:open` | OK | The categories are disjoint: 642 + 1194 + 663 = 2499 (no prime power fails the two-squares test), 644 + 11 = 655, 655 + 8 = 663, and 663 - 644 = 19. The list of 19 minus the 11 in Table 2 equals exactly the 8 open values. Below 2000: 164 + 211 + 124 = 499 and 122 + 2 = 124. 5185 stays open unconditionally, with GRH kept separate (172, 2303, 2312). 3965 stays open. Not one CSV row rests on C2_uniform alone. 20 rest on QE alone, 4 on T4 alone and 1 on Doubling_origin alone. |

## Summary counts

- OK: 23 (6 quotients, 4 three-fibre, 6 catalogs, 6 phase, 1 coverage).
  This includes the 8905/2561 census logic, marked "OK (logic)".
- MINOR: 10 (3 quotients, 3 three-fibre, 3 catalogs, 1 phase).
- ERROR: 0.

## Cross-reference, notation and hypothesis inconsistencies

1. **Line 892**: "$H_0$" versus the definition "$\mathcal H_0$" at 307.
   Use one symbol.
2. **Line 2233**: the abbreviation **FC** is never defined. Theorem
   `thm:fc` ("Full-conductor necessity", about line 808) carries no "; FC"
   tag, whereas O, T1, T2, T4 and T5 are tagged in their theorem names.
3. **Lines 1031 and 1075**: the "only if" direction rests on the mod-8
   forward direction of `lem:doubling`, which is stated only for exact
   pairs (row `se-thm-runs` above).
4. **Lines 1212, 1222 and 1322**: multiplicative C_3 (y, y^{-1}) is mixed
   with additive coordinates (s,1). Section `sec:phase` (1753) uses
   additive coordinates (0,1), (0,2) with y as the group-ring generator.
   Harmonize.
5. Symbol reuse:
   - **Section `sec:catalogs`**: T is the trace Gram matrix (1423, 1504)
     and also a selection set (1589). N is an integer (1450), the ray
     modulus (1577) and a norm (1496, 1612-1613).
   - **Section `sec:phase`**: R is D^{-1}P (1696) and also the exchange
     matrix (1788).
   - Across sections: eps/epsilon has four meanings (D1 Gaussian unit,
     (-1)^{(t-1)/2}, -S_0, 1-2e), and D means sigma_2 in some places and
     (E - eps delta)/2 in others. Each is defined locally, so this is a
     readability issue only.
6. **Line 1347**: "involution" should be "involutive automorphism".
7. **Line 1553**: unstated hypotheses on the residue map rho
   (multiplicative, conjugation-equivariant, b invertible).
8. **Lines 1398-1399**: "removes any ... coprimality assumption" needs
   "for H x C_3". For cyclic C_t, the 9 | t case is not covered (1387 is
   correct).
9. **Lines 1879-1885 (P-5)**: the trace filter leaves these conventions
   unstated:
   - outer orbits are ordered by (x,1) to (-2x,1) mod C;
   - x_i x_{i+n} is summed over i < n;
   - z is cyclic mod n;
   - y_i sits on the H-coset of x_i.

   The identity was verified under exactly this reading.
10. **Line 1469**: "is" should be "is at least". **Lines 990-994**: the
    8281 example does not need the sharpened inventory.

All `\ref`/`\eqref` targets used in the scoped lines resolve to existing
labels.

## Passages most worth an expert's reading

1. **Theorem `se-thm-three`, lines 1269-1330: the sign rule mod 4 and the
   sigma_4 transfer.** This is the new uniform argument, and it supersedes a
   bounded enumeration. I re-derived every step and confirmed it
   exhaustively for h <= 13. The delicate points are the reduction of
   `se-eq-divided` modulo 4, the use of P(F) = 2k = 0 mod 2, and the choice
   of Lambda = U + S, which makes the quadratic relation
   Lambda(3 Lambda - 2E) = q delta exact.
2. **Theorem `thm:factor` with Theorem `thm:ray-transport` and Corollary
   `cor:ray-family`, lines 1543-1654.**
   - The proofs are correct. The infinite family, however, rests on a
     length-80 color-count mismatch certificate at 2561, carried through
     the conventions of the color map: rho, conjugation, and the joining
     multiplier alpha/p mod 61.
   - Because those conventions are under-specified in the statement (item 7
     above), an expert should confirm that the certificate's colors are
     exactly those the theorem transports.
   - That certificate is data and was not rerun here.
