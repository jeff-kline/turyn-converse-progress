# Audit dispositions (root agent, 2026-10-21)

## AUDIT-S1-S3 (Opus/xhigh): 0 ERROR, 8 MINOR — all applied
- O: H(m) allowed only at odd index.
- T2 wording "coefficient at a nonzero position".
- "Box bound" and "square subgroup" now defined at first use.
- T1 quotient corollary: the group on C_t′ is now explicit.
- T5 restates gcd(h,p)=1.
- B_p: the dangling r removed.
- DGS citation made uniform.
- FC: the 2-part reason corrected, and an internal sign proof added.
- D1: the s-preserves sentence clarified.
NOT applied (cosmetic): T5 reuses the letter f. It is local to the proof and defined there.

## AUDIT-S4-S7 (Opus/xhigh): 0 ERROR, 10 MINOR — 7 applied, 3 deferred as cosmetic
Applied:
- floor-corollary weights;
- run-count theorem cites the mod-8 doubling lemma;
- (s,1) changed to (s,y);
- "involutive automorphism";
- the 9∣t scope note;
- "at least";
- factor-matching ρ multiplicative and commuting with conjugation;
- H_0 changed to \mathcal H_0 in symmetry-energy;
- FC defined in §9.
Deferred (cosmetic, no logical effect): symbol reuse (T, N, R, ε, D across sections); the 3965 trace-filter
index conventions; and the 8281 example's optional extra detail.

## Tightening (Opus/high editors A, B)
Words cut: early-theorems −10.5%, conductor −5.5%, symmetry-energy −5.3%, catalogs −3.8%, phase −4.6%.
Editors report no statement changes. Equivalence check pending (review/EQUIVALENCE-CHECK.md).

## CLAIMS-AUDIT (Sonnet/medium): all numbers verified; 17/17 local citations verified; 8 mismatches — all fixed
1. "No infinite family other than 13p" → now names the classical three-power family as well.
2–4, 7. One status vocabulary across §1 Table 1, §8 Table 2, README and NOVELTY-ASSESSMENT.md:
   - principal results are exactly T4 and C_3 inversion;
   - "new" is defined once;
   - priority is unresolved for every result;
   - mod-16 is "new as stated; prior-art search incomplete".
5. "Settle 655" → "the arguments collected here exclude 655", with the 644/11 split in README.
6. Squarefree claim: §1 now explains it. T4 and C_3 need a prime dividing t exactly once, and FC is automatic for squarefree t.
8. Doubling identity: "Elementary characteristic-2 computation; not claimed as new".
DGS wording: "prime-power necessity" → "pose the prime-power conjecture".
Process language removed from §8, §9 and the appendices ("dossier", "project", "accepted", "draft",
"preserved research tree").

## EQUIVALENCE-CHECK (Opus/high): 173 hunks, 0 BROKEN; T2 fix correct. Suggestions 1,2,4,5,7 applied; 3 (harmless) and 6 (would reintroduce undefined o_r) not applied.
