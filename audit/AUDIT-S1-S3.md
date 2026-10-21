# Audit of main.tex sections 1-3 (lines 145-877)

Read-only mathematical audit of the assembled manuscript, dated 2026-10-21.
The scope is §1 "Scope and verified coverage", §2 "Multiplier, averaging,
and prime-fibre obstructions" and §3 "Multiplier kernels and full conductor".
Each proof was re-derived by hand from the manuscript text. Numerical claims
were checked with
`review/audit_s13_checks.py`, run under the project venv with `ulimit -t 600`
(about 7.7 CPU-minutes). Source correction files (lanes A, A2, A3, B) were
read only to settle doubts.

**Totals: OK 12, MINOR 8, ERROR 0.**

## 1. Verdicts by item

| # | Item (lines) | Verdict | Notes |
|---|---|---|---|
| 1 | Thm `coverage` and the §1 counts (157-180) | OK | Recomputed: 2499 parameters = 642 prime powers + 1194 non-two-squares + 663 in E. The prime-power and two-squares classes do not overlap. All eight listed q lie in E. 644 + 11 = 655 and 19 - 11 = 8 agree with the proof at 2240-2257. The underlying record was not re-audited because it is out of scope. |
| 2 | Conventions §1.1 (183-216) | OK | ZZ* = A^2 + B^2 under symmetry; X is even and Y is odd; projected-entry parity and bounds hold. The origin condition f-1 (mod 4) follows from pairing the nonzero fibre elements, each pair contributing ±2. |
| 3 | Lemma `doubling` and its proof (219-247) | OK | Both directions re-derived by hand. Coefficient at 2g: a_g + a_{2g} + b_g = c[g=0] + l. The sign rule follows. In the converse, both supports have even size because A and B are symmetric with zero at the origin. The b-formula, the exact defect 4[...] and the vanishing of the bracket mod 2 all check. Numerically, the forward rule holds on every symmetric pair at t = 5, 7, 9, 13, 15 (4/12/12/12/16 pairs). The mod-8 converse had 0 failures in 1560 random symmetric A over 13 group orders. |
| 4 | Prop D1 and its proof (298-358) | MINOR | The mathematics is correct. The lift u~ = 1 (mod 4) is what makes the sign +1. Restricting <r,s> to automorphisms fixing i gives <r^{e_r}, -1>. E has algebraic-integer values at every character, including the trivial one. Integrality comes from mE_j and qE_j in Z[i] with gcd(m,q) = 1. Then E E* = δ, symmetry gives a = 0 and augmentation gives ε = 1. Wording issue at 338-340: "Both σ_r and s therefore preserve the r-primary part." s preserves it because s(α) = α, not as a consequence of the Frobenius sentence. The citation range also differs from line 823 (see §2 of this report). |
| 5 | Thm O and its proof (375-406) | MINOR | Bound re-derived: Y_1 = S/d, \|S\| ≥ √2 at odd d, c_e(1) = μ(e), 2^ω nonzero terms. At line 383, "In particular one may take H = H(m)" is valid only when [(Z/m)^× : H(m)] is odd, and the text should say so. |
| 6 | Thm T2 and its proof (411-464) | MINOR | Correct. The unit-sum identity uses the C_ℓ origin, so the fibre is t/ℓ. There are two Ramanujan terms. If S = 0, equality in the triangle inequality makes every order-ℓ character value equal Z_1, which forces X^[ℓ] = Z_1 δ; that is impossible because the off-origin coefficients are odd. S has the parity of d, so \|S\| ≥ 2 at even d. Both bounds and the "equivalently" forms check. The prime-power hypothesis is used exactly at the two-term reduction, and the source confirms it is needed (S = 0 at q = 29, m = 15). Wording: at line 456, "every nonzero quotient coefficient" should be "every coefficient at a nonzero position". At line 441, "the preceding proof" means the proof of O. H ≤ (Z/m)^× is assumed implicitly at 413. |
| 7 | Remark `early-t2-boundary` (466-477) | MINOR | The numbers are right. χ_5^2 + (J-2δ)^2 = 9δ was checked. H = {1,4}, d = 2, and min(4.8, 3+1) = 4 is attained. All 16 pairs at t = 15 have S = 0 for H(15) = {±1} (verified). Terminology: "box bound" is never defined (it is the √q + β_ℓ term), and "square subgroup" is used before its definition at 563. |
| 8 | Thm T1 and its proof (482-523) | OK | Decomposition into gcd classes, ψ(e_d) = μ(m/d), Parseval on C_h, 2^w surviving terms, and \|E_0\| ≤ 2^w - 1 all check. The arithmetic use of F_m ≤ H_0 correctly uses the global group. |
| 9 | Silent-case paragraph (525-531) | OK | The inequality reduces to m ≤ 4^w - (2^w - 1)/h. For w = 1 that is m ≤ 3. For w = 2 it is m = 15 with h ≥ 3, which becomes h ≥ 7 once h must be coprime to 15. w ≥ 3 never holds. A brute-force run over odd m < 4000 and odd coprime h < 400 finds silent m only in {3, 15}, with h ∈ {7, 11, 13, ...} at m = 15. |
| 10 | Cor `early-t1-quotient` (533-547) | MINOR | The bound is right, including \|E_0\| ≤ (2^w - 1)W + (W - 1) = 2^w W - 1. The phrase "full m-fibre" on C_{t'} is undefined: F_m was defined relative to t at 485. Write it as {u mod t' : u ≡ 1 (mod h')}. |
| 11 | Example q = 4453 (549-557) | OK | Checked: 61·73 ≡ -1 (mod 2227); the orders of 61 are 16 mod 17 and 5 mod 131; \|H_0\| = 160; F_17 ⊆ H_0; RHS = 1045. Optional: T4 also excludes 4453 (index 1 at p = 17), as the lane-A2 corrections record. |
| 12 | Thm T4 and its proof (559-669) | OK | Every step re-derived. The Legendre decomposition with exactly one of S_j, D_j a sign holds. So do the identities J^2 = pJ, χJ = 0, χ* = εχ and χχ* = pδ - J, and the symmetry relations U* = U, D* = εD. The χ-coefficient is 2(UD + VD'). The energy count ‖U‖^2 + ‖V‖^2 = n_A + n_B - 1 + 2η + 4k is correct, including the origin terms in both η cases, and gives (p+1)M = 2h + 2η + 4k and k ≤ M - η. In the mod-2 step, U-bar = D-bar + δ and V-bar = D'-bar, which give D_A = 2(D_A Δ D_B), \|D_A ∩ D_B\| = n_B/2 and n_A + n_B ≤ 3h/2 (using n_B ≤ h). Since h is odd, M ≥ (h+1)/2, and the result is (p-7)h + (p-3) ≤ 0. Numerically, no F_p^{(2)}-fixed pairs exist at (h,p) = (1,7), (1,13), (3,7), (9,7). |
| 13 | Threshold and sign remark (671-683) | OK | The p = 5 boundary is stated correctly. At p = 5 the inequality reads -2h + 2 ≤ 0, so it never gives a contradiction. The t = 5 pair is F_5^{(2)}-fixed (4 such pairs, verified), and the nonsquare 2 negates A. The text claims nothing about p = 5 with h > 1; for information, there are 0 fixed pairs at (h,p) = (3,5) and (11,5). |
| 14 | Thm T5 and its proof (688-724) | MINOR | Correct. Ā_j = α_j + f s_j with s_j odd. The energy inequality reduces to h(f - k - 2) ≤ -1, which gives f ≤ k + 1. The statement does not restate gcd(h,p) = 1, which it inherits from 562. f is reused as the orbit size (p-1)/k, whereas at 211 and 368 it is the fibre size, and the projection here has fibre size p. |
| 15 | T5 numerics (726-737) | OK | Bounds p ≤ 3, 13, 31 at k = 1, 3, 5 check. <5> mod 13 = {1,5,8,12}. Enumeration finds exactly 12 symmetric pairs at t = 13, all K_3-fixed and none fixed by the full squares subgroup. The slack is 2(h-1)(k+1), checked symbolically over a grid. For 4141: \|H_0\| = 72 and \|H_0 ∩ F_19\| = 6, so the index is 3. The image of H_0 mod 19 is all of (Z/19)^× (index 1), which shows why the warning at 735-737 is needed. |
| 16 | Thm `kernel` and its proof (766-798) | OK | Orbit j + hp^{b+s}Z of length p^{a-b-s}; characters of full p-order annihilate every non-fixed orbit. Each of the h·φ(p^b) characters of C_N, covering every cofactor character, lifts to one of full p-order p^a. Parseval over all of C_N gives (p-1)q ≤ p(2N-1), and (p-1)(2Np-1) - p(2N-1) = 2Np(p-2) + 1. The corollary argument (an element of prime order p forces the b = a-1 kernel) is right. Small cases (t = 9, 25, 27, 45, 49) satisfy the inequality as claimed, and the t = 9 pairs are not {1,4,7}-fixed. |
| 17 | Definition of B_p and F (800-807) | MINOR | The formula is right. By lifting-the-exponent, v_p(r^{o}-1) = v_p(r^{p-1}-1) + v_p(o) whenever ord_p(r) ∣ o. With o = ord_{4rad t}(r), this matches Schmidt's F(m,n) as I recall its definition; using 4 rad t versus 8 rad t does not change v_p for odd p. As a sanity check, F(4t,q) = 4t holds at every prime power q < 10^4, where pairs exist. F(612,305) = 204 was recomputed. Wording: "and a prime r ∣ q" dangles, since r is bound by the max. Tan's Definition 2.10 was not checked against the source. |
| 18 | Thm `fc` and its proof (808-841) | MINOR | Correct: v_p(d_r) = v_p(ord_{4rad t} r); LTE generation of the units ≡ 1 mod p^{b_r}; the common powers mod 4t; the substitution with y = -x^2 and z = x^t (y^t = 1, z^2 = -1, disjoint parity supports). See the notes after this table. |
| 19 | Cor `three` and its proof (843-863) | OK | B_3 ≤ β + e(h). r ≡ ±1 mod 3^β, so r and s lie in opposite classes mod M, with minimal odd sizes 2M - 1 and 2M + 1, and min(a,β) ≥ a - e(h). As a sanity check, no composite prime power q < 2·10^5 with 3 ∣ t violates the bound. |
| 20 | Examples after the corollary (864-875) | OK | h = 7, 13 force primality for a ≥ 4, and h = 11 for a ≥ 2. 3^{4n+1} ≡ 3 (mod 5), so 5 ∣ q. F(612,305) = 204, φ(204) = 64 and 204^2/64 = 650.25 ≥ 305. |

**Notes on item 18 (Thm `fc`).**

- **2-part (836-837).** The 2-part reason is imprecise. The correct reason is 4 ∣ m_r, so r^{o_r} ≡ 1 (mod 4); o_r can be odd, so "v_2(r^2 - 1) ≥ 3" is not the operative fact.
- **Sign (832).** "Since u ≡ 1 (mod 4), its normalized sign is positive" rests only on the citation. An internal one-line proof is available:
  1. The unique zero coefficient forces shift 0.
  2. z^u = z, so c(x^u) = εc(x) splits into A(y^u) = εA and B(y^u) = εB.
  3. Augmentation of B is odd, so ε = +1.

  I suggest adding it.

## 2. Cross-reference, notation and hypothesis inconsistencies

All \ref/\eqref targets in 145-877 exist, and there are no duplicate labels (checked by grep).

1. **Citation (321 vs 823).** DGS is cited as "Theorems 5.2–5.4" at 321 and "Theorems 5.2 and 5.4" at 823. The lane-A record cites "DGS 5.3/5.4/(5.10)". Harmonize against the page image.
2. **Group identity (184-185 vs 282).** §1 writes 0 for the group identity and δ for the group-ring identity. §2 says "the identity group element is denoted by δ".
3. **Letter m (186 vs 290, 298).** σ_m with m a unit in §1; in §2 the unit is u and m is a divisor of t.
4. **Inversion notation (187-188 vs 282-283).** §1 uses X^{(-1)} for inversion and X* for the adjoint; §2 uses * for inversion on real rows. This is consistent but redundant.
5. **"Nonzero coefficient" (368, 456).** It means "coefficient at a nonzero position".
6. **Hypothesis (383).** H = H(m) is allowed only when its index is odd.
7. **Implicit assumptions in T2 (413, 441).** H ≤ (Z/m)^× is implicit, and "preceding proof" means the proof of O.
8. **Undefined or early terms (472-473).** "Box bound" is never defined, and "square subgroup" is used before its definition at 563.
9. **Undefined fibre (535-536).** "Full m-fibre" on C_{t'} has no definition; F_m at 485 is defined relative to t.
10. **Symbol f (211, 368, 689).** f is the fibre size in §1 and §2.3 but the orbit size (p-1)/k in T5.
11. **Hypothesis (692-694).** T5 relies on gcd(h,p) = 1 from 562 without restating it.
12. **Overline (335, 645, 709).** It denotes complex conjugation in D1, reduction mod 2 in T4, and fibre projection in T5.
13. **Exponent a (793).** "Orders p^{a-1}" reuses a as a per-prime exponent; write p^{a_p - 1}.
14. **Dangling quantifier (800).** "and a prime r ∣ q" is left dangling.
15. **2-part reason (836-837).** See item 18.
16. **Reused letters.** S (orbit sum, S_j, "type S"), M (type-S count at 619, 3^{min(a,β)} at 856), E/F (T1 sums vs field-descent F and the set 𝓔), d (index, divisor, character order) and Z (A + iB at 206 vs Z_e at 397). These are local, but a careful reader will stumble.
17. **H_0 versus local groups.** The text respects the rule that H(m) may be larger than the image of H_0 mod m (307-311):
    - Local groups are used only for quotient statements: O and T2 (X^[m] fixed by H ≤ (Z/m)^×), and implicitly the T1 quotient corollary.
    - Every fibre subgroup of (Z/t)^× is tested against H_0: T1 at 497, T4 at 576, T5 at 701.
    - 735-737 correctly warns against using the image mod 19 at 4141; that image has index 1.
18. **Source corrections carried into the text.** Lane A corrections 1-3 appear at 525-531, 673-674 and 310-311. The lane-B boundary findings (fibre t/ℓ; S = 0 at m = 15, q = 29) appear at 474-476. The lane-A3 value \|H_0\| = 72 at 4141 is consistent with the stated intersection of order 6.

## 3. Passages most worth an expert's reading

1. **D1 (318-358), with the DGS application in Thm `fc` (822-836).**
   - Both rely on classical multiplier theory, and the manuscript's citations disagree.
   - The Galois step (r-primary parts preserved by σ_r and s) is compressed.
   - The sign and normalization in fc rest on one phrase.

   I found them correct, but this is where a specialist's check of the DGS statement (theorem numbers and normalization) matters most.
2. **T4 (571-669).** This is the paper's strongest novelty candidate. I verified every line, including the origin terms and the mod-2 support identity. An expert should confirm the argument and assess whether the Legendre decomposition plus the characteristic-two support identity appears in the multiplier or difference-set literature.
