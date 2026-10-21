# Equivalence check: tightened fragments vs review/*.orig (2026-10-21)

Read-only check. Method: `diff` hunk count, then `git diff --no-index --word-diff=plain`
on each pair, with every changed hunk read against the surrounding statement or proof.
No build was run. Label/ref/eqref/cite targets: identical sets in all five files. Only the
counts in symmetry-energy differ (+1 `\eqref{se-eq-slice1}`, +1 `\ref{lem:doubling}`), and
both targets exist.

## Hunk counts (`diff` hunks)

| file | hunks |
|---|---|
| early-theorems | 52 |
| conductor | 17 |
| symmetry-energy | 53 |
| catalogs | 25 |
| phase | 26 |
| total | 173 |

Verdicts. The split between categories is approximate, because some word-diff hunks
straddle categories.
- BROKEN: 0
- AUDIT FIX (in the assembly but not in `.orig`, traced to an AUDIT finding, checked correct): about 12
- WEAKENED-BUT-FINE / minor wording: 7 (listed below)
- EQUIVALENT: the rest, about 154

## T2 proof sentence (early-theorems.tex, proof of `early-t2`)

The new text reads: "This is impossible, because each coefficient of $X^{[\ell]}$ at a nonzero
position has two odd coordinates."

Verdict: CORRECT, and it is the fix that AUDIT-S1-S3 item 6 asked for. Each nonzero position
of $C_\ell$ has a fibre of $f_\ell=t/\ell$ positions, which is odd. None of them is the origin of
$C_t$, so every summand is $\pm1\pm i$. Both coordinates are therefore odd, and in particular
nonzero. Since $\ell\ge3$, there is a nonzero position, which contradicts
$X^{[\ell]}=Z_1\delta$. The old wording "every nonzero quotient coefficient" was a non sequitur:
a statement about coefficients that are already nonzero does not show that an off-origin
coefficient is nonzero.

## Audit fixes present in the assembly (intended; mathematics checked)

- early `early-o`: "$H=\mathcal H(m)$ when its index ... is odd" (AUDIT-S1-S3 #5). Correct: O assumes odd $d$.
- early `early-t1-quotient`: $\{u\bmod t':u\equiv1\pmod{h'}\}$ replaces "full $m$-fibre" (#10). Same group, now defined.
- early `early-t5`: "Let $t=hp$ with $\gcd(h,p)=1$" (#14). The hypothesis is restated, not changed.
- conductor `thm:fc` sign. The internal proof is now spelled out: the zero coefficient forces $k=0$; $z^u=z$ because $u\equiv1\pmod4$; parity separation gives $A(y^u)=\varepsilon A$ and $B(y^u)=\varepsilon B$; $B(1)$ is odd, so $\varepsilon=1$. Checked: $x^{tu}=x^t(x^{2t})^{(u-1)/2}=x^t$. "$k=0$" holds modulo $2t$, with the sign of $x^{2t}=-1$ absorbed into $\varepsilon$. Fine.
- conductor 2-part reason (#18). Correct, but terse: see minor item 6.
- conductor DGS cite harmonized to `Theorems~5.2--5.4`.
- symmetry-energy: floor-corollary multiset wording, the `lem:doubling` parenthetical in `se-thm-runs`, "involutive automorphism", and "$(s,y)$" for "$(s,1)$" (AUDIT-S4-S7, se-thm-three). Checked $(s,y)$: $A_{(s,y)}=S_s$, $A_{(2s,y^2)}=S_{2s}$ and $B_{(s,y)}=T_s=-F_s$, which give $F_s=F_0S_sS_{2s}$.
- symmetry-energy closing paragraph: "cyclic lengths with $9\mid t$ are not of this form and are not covered" (AUDIT-S4-S7 line 95). Correct. $H\times C_3$ with $H$ odd is cyclic only when $3\nmid|H|$, and then $v_3(t)=1$.
- catalogs `thm:factor`: $\rho$ multiplicative and commuting with conjugation (audit edit).

## Spot re-derivations behind EQUIVALENT verdicts (selection)

- T4: the "raw $\chi$-coefficient is $2(UD+VD')$". Checked from $D^*=\epsilon D$ and $\chi J=0$.
- T4: "commutative ring of characteristic two" is a correct gloss on $\mathbb F_2[C_h]$.
- O: "At most $2^{\omega(m)}$ terms are nonzero" replaces "Exactly ... can be". Same content, and more accurate.
- Remark `early-t2-boundary`: box bound $\sqrt q+\beta_\ell=3+1$, with $f_\ell=1$, $\beta_\ell=1$, $c_d|H|=4$. The $q=29$, $m=15$ restatement is the same fact.
- 4685: $\pm14\not\equiv\pm2$ and $\pm29\not\equiv\pm1,\pm3\pmod{20}$. Unchanged.
- 6437 total cycle size: $14\cdot72+2\cdot18+7\cdot4=1072$.
- `se-cor-prime`: the excess $2(p-1)[h(p-4)+1]$ re-expanded.
- `se-lem-support`: "the third" matches the three displayed conclusions.
- smallnorm: "at least $8(\ell-h)+d-4$" equals $8h(d-1)+d+4$ with $\ell=hd+1$. Adding "at least" is correct.
- 2561: residues $\{\pm21,\pm17\}\pmod{61}$ correspond to augmentations 40 and 44.
- cor:three: "lie in opposite classes $\pm1\pmod M$" replaces the old ordered "$+1,-1$". This is neutral, and slightly more accurate.
- phase trace filter: "Since $n$ is even" is the correct reason. $n$ equal bits sum to $0\ne1$.
- 3965 caveat: now stated once, after the rotations sentence. Nothing is lost. "Does not change Theorem~\ref{thm:coverage}" is kept.

## WEAKENED-BUT-FINE / minor wording (none breaks an argument)

1. early-theorems, opening paragraph. "Signed multipliers, which may negate one row, do not satisfy this hypothesis" overstates: a signed multiplier with both signs $+1$ does satisfy it. Fix: "do not in general satisfy" (or "need not satisfy").
2. early-theorems `early-novelty-scope`. "refine the older odd-index estimate" is a new attribution verb; the old text said "should be distinguished from". At odd $d$ the prime-power bound $m^2\le2d^2q$ coincides with O at $\omega=1$; what is new is even $d$ and the box bound. "Extend" would be more exact than "refine". The removed priority/novelty caveats follow the coordinator's policy (state it once in §1 and §8). Confirm that §1/§8 carry the T4 caveat ("inspected statements have not been shown to imply T4; historical coverage unresolved").
3. symmetry-energy, `se-thm-three` proof. "to obtain an exact multiplier" became "a multiplier". This is harmless: the context gives coefficientwise invariance.
4. phase, proof of `thm:forced`. In "These lie in $K_2$ because $n$ is even", the antecedent is singular ("a cube root of unity"), so "These" could be misread as $v,v^*$. Fix: "All cube roots of unity lie in $K_2$ because $n$ is even".
5. phase, $p=101$ paragraph. "two separate exhaustive implementations" became "two independent". This is a slightly stronger provenance claim. Revert to "separate" unless independence is documented.
6. conductor, 2-part sentence. "in Tan's definition the modulus is divisible by $4$ and every prime $r\mid q$ is odd" omits the operative step. Fix: append "so $r^{o_r}\equiv1\pmod4$" (the AUDIT-S1-S3 #18 wording).
7. catalogs, 2561. "504 signed norm generators, 252 satisfying parity, with real conductor residues ..." can now attach the residues to the 504. Fix: "...252 satisfying parity; these have real conductor residues".

## New symbols or ambiguity

No undefined symbol was introduced. The remark now defines $\chi_5$ and $J_5$ and the square subgroup in place. $\mathcal H_0$ in symmetry-energy matches the early-section definition. $\varepsilon$ and $k$ in the `thm:fc` proof are local. The audit's notation items that are still open ($f$ reused in T5; the overline triple use) were not in scope and are unchanged.
