# Implementation notes for verify_coverage.py

Status after the full run (q < 10000, 2499 parameters): every one of the eleven
criteria agrees with `data/coverage.csv` on every row (0 disagreements).
The script was written from the theorem statements in `paper/main.tex` only; the
CSV was read after the criteria were written and used only for comparison.

## Reading choices (paper leaves these implicit)

| Item | Reading used | Why |
|---|---|---|
| H(m), H0 | H(m) = intersection over primes r\|q of <r^e, -1> in (Z/m)^*, e=1 for r=1 mod 4, e=2 for r=3 mod 4; H0 = H(t) | Eq. (early-common-group) verbatim |
| O | every divisor m>1 of t, H = H(m) (local group), needs odd index d, fires on m^2 > 2^(2w-1) d^2 q | the O theorem says "one may take H = H(m)"; Sec 2.1 says quotient tests may use the larger local group |
| T2 | every m = l^a, 1<=a<=v_l(t), H = H(m); fires if either branch of the min is violated; decided in exact integer arithmetic | H(m) is the largest admissible H, and for even d any subgroup keeps c_d = 2, for odd d a subgroup of odd index only shrinks |H| |
| T1 | the theorem proper: t = h m, gcd(h,m)=1, m>1, F_m = {u = 1 mod h} contained in H0, violation of the T1 inequality | the key T1 names Theorem 2.4. The "Quotient version of T1" (the quotient corollary of T1, W = t/t' > 1, F in H(t')) is computed separately as `T1q` and does not enter the T1 flag |
| T4 | p>=7, v_p(t)=1, index [F_p : H0 cap F_p] <= 2 | "Consequently" clause of the T4 theorem |
| T5 | v_p(t)=1, k = [F_p : H0 cap F_p] odd, p > k^2+k+1 | consequence clause of the T5 theorem (only the exact index matters: an odd-index subgroup inside H0 cap F_p forces k to be the index) |
| FC | fires when B_p < a for some p^a \|\| t, B_p as printed (order modulo 4 rad(t)) | the FC theorem, equivalent to F(4t,q) != 4t |
| QE | M = H0, applied at every divisor m of t (m = 1 is the augmentation test), exact feasibility of the quotient-energy equation by bitset DP | the QE theorem; the energy-floor corollary (energy floor) is a relaxation of the exact test, so it is not coded separately |
| Fixed_fibre | every divisor h>1 of t (no coprimality), 2 in the image of H0 mod h, violation of [1+eps(h-1)]^2 <= q | the fixed-fibre corollary, "no coprimality assumption" |
| Doubling_origin | every m \| t, h = t/m; doubling cycles of H0-orbits inside mZ/t minus 0, r_C in 0..floor(L_C/2) independent; fires if no attainable value 1+eps(h-1-4 sum w_C r_C) has square <= q | the origin-coefficient set equation of Sec. 4.1 and the sentence after it |
| Full_prime_fibre | prime p with v_p(t)=1 and F_p contained in H0 (index 1), t != 3, includes p = 3 | the full prime-fibre corollary + the paragraph after the full prime-fibre corollary; for p=3 the pure fibre has order 2 |
| C2_uniform | 3 \|\| t, t>3, and the involution u (u = 1 mod t/3, u = -1 mod 3) lies in H0 | the coordinate-free corollary: in C_t an involution has exactly three anti-fixed elements only in this case (count = product of p^a over components where u = -1) |

Mapping C2_uniform and Full_prime_fibre to the two CSV keys is an inference from
the data pattern, not from the paper: the CSV never has C2_uniform without
Full_prime_fibre, which matches "C2 = Theorem 5.1 at p=3, Full_prime_fibre = the full prime-fibre corollary for every p". The
implementations were written from the theorem statements and then found to agree.

Not implemented: the simultaneous quotient-signature theorem (the simultaneous-signature theorem, the
"doubling-cycle" coupling across quotients). It is not in the paper's list of
members of the selected union, and the union already reaches 644 without it.

## Disagreements found

None in the final script. History:

1. First draft evaluated criteria only at prime powers and eligible q. The CSV also
   carries criterion flags on all 1194 two-squares failures. Fixed by evaluating all
   2499 rows (criteria are pure arithmetic of q; not a mathematical issue).
2. First draft of T1 included the quotient corollary (the quotient corollary of T1) in the T1 flag. That
   produced 4 extra firings below 1000 (q = 657, 725, 833, 845, all with a
   proper quotient t' | t, W in {3, 7, 9}, F inside H(t')) that the CSV does not
   mark T1. Diagnosis: reading ambiguity, not a CSV error and not a bug: the
   corollary is a different, correct statement (the proof of T1 goes through with
   the stated coefficient bounds), but the CSV key T1 is the theorem proper.
   Resolution: T1 flag = theorem proper; `T1q` reported separately. Over all
   q < 10000 the union is 644 with or without the corollary (checked by the script).

## Extra checks run during development (not all in the summary)

* Mutation test: removing one flag from a copy of the CSV makes the script exit 1 and
  name the row.
* Worked examples of the paper reproduced: q=4453 (T1, m=17), 4141 (T5, p=19,k=3),
  305 (FC at p=3), 8281 (QE at m=1), 4685 (QE at m=1), 9809 (QE at m=9),
  4705 (QE at m=13), 4525 (QE at m=31), 6437 (doubling origin at m=3),
  7625 (fixed fibre, h=123), 3965 (nothing fires).
* Leave-one-out on the union (eligible q): dropping T4 loses {2925, 6005, 6885, 8469}; dropping QE
  loses 20; dropping Doubling_origin loses {6437}; dropping any of O, FC, T1, T2, T5,
  C2_uniform, Full_prime_fibre or Fixed_fibre alone loses nothing (they overlap).
