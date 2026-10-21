# Claims and citation audit, 21 October 2026

Read-only audit. Counts were recomputed from materials/coverage.csv with the review .venv (sys.prefix != sys.base_prefix asserted).

## 1. Numbers: all VERIFIED

2499 rows (q = 5..9997, all q = 1 mod 4, 2499 distinct). Prime power 642; two-squares failures 1194; eligible 663; EXCLUDED_SELECTED_UNION 644; EXCLUDED_ADDITIONAL_RECORDED_ARGUMENT 11; OPEN_UNCONDITIONALLY 8 (3965, 4745, 5185, 5525, 6409, 7565, 7685, 8245). 644 + 11 = 655; 655 + 8 = 663. The 19 union survivors minus the 11 (909, 1845, 2561, 2665, 6137, 7461, 7929, 8865, 8905, 9245, 9265) leave the 8. Below 2000: 499 rows = 164 + 211 + 122 + 2, so 124 of 124 eligible are excluded, and Table tab:coverage matches. The 5185 row carries the GRH conditional note. The 198 to 132 figure matches main.tex lines 1844-1845 (a 66-variable elimination). README, abstract, section 1 and section 9 agree on every count.

## 2. Claim agreement: mismatches and overstatements

M1. Section 1 "We do not claim ... any infinite family of excluded q other than the ray-class family q=13p" contradicts the paper. Corollary cor:three (main.tex 849-870) shows t=3^a and t=5*3^a force q prime, and says "t=3^{4n+1}, n>=1, is excluded unconditionally". Section 8 (line 2047) calls this "an infinite parameter class". The sentence should say the other families are classical specializations and not claimed as new. NOVELTY-ASSESSMENT.md says the ray-class result "gives an infinite family" and does not mention the 3-power family.

M2. Principal-result count differs across surfaces. README, abstract and the section 1 table name two principal results (T4, C3 inversion). NOVELTY-ASSESSMENT.md lists three "Principal novelty candidate" rows (T4, C3, ray-class transport). Section 8's closing paragraph lists four strongest candidates (T4, C3, catalog transport, forced-fibre reconstruction).

M3. Mod-16 reconstruction. The section 1 table says "New; the prior-art comparison is incomplete". README lists it under "New here". NOVELTY-ASSESSMENT.md calls it a "strong contribution candidate", and section 8 says "No historical-novelty verdict is made" and "only a preliminary terminology search". Bare "New" is stronger than section 8 supports.

M4. The section 1 table says "new as stated" or "new" for kernel injectivity and full conductor, T1, the T2 nonvanishing step, ray-class transport and T4. Section 8 and NOVELTY-ASSESSMENT.md say "priority unresolved" or "candidate" for each. The section 1 definition of "new" (not found in sources checked) reconciles this only for a careful reader. Suggest "new in the sources checked" in the table cells. README's "(principal result)" and "Multiplier kernels" bullets have the same issue, mitigated by its closing caveat.

M5. Abstract and section 1: "they settle 655 of the 663". The 655 include 11 exclusions from earlier or case-specific certificates, 2 of them below 2000 (909, 1845). The 644-case union also uses O, T1, T2, T5, QE and others, not only "these results". Section 8 and NOVELTY say the count is coverage, not new exclusions. Suggest "the recorded criteria settle". Also, Table additional says "several use general criteria", so README's "earlier or case-specific certificates" label is loose.

M6. Abstract and README: "Both apply when t is squarefree, where earlier conductor tests say nothing." The paper has no section supporting this. It says only that for squarefree t the character-conductor minimality is "automatic" (line 848). The "earlier conductor tests" are not named. Add a pointer or soften.

M7. README omits O, T1, T2 and QE from both the "new" and "not new" lists. NOVELTY-ASSESSMENT.md treats O and T1/T2 as "priority unresolved". README's "Not new" list calls the odd-index fibre bound (T5) "a short corollary of standard counting", while NOVELTY and section 8 say "exact historical priority unresolved". Mild; "not new" is firmer than the sources.

M8. NOVELTY-ASSESSMENT.md says the doubling-cycle consequences follow from "an established project identity". Section 8 says the doubling relation was "derived in this project", and Lemma doubling is stated with no citation. "Established" suggests a literature precedent. Reword to "the identity proved in section 1".

No instance of "first", "solves" or worldwide minimality in a positive claim. Disclaimers are present and consistent in the abstract, section 1, section 8, README and NOVELTY.

## 3. Title, author, status and date: agree

Title "Progress on Turyn's converse: general symmetry theorems and coverage below 10,000" (README H1 matches main.tex 116-117). Draft, 21 October 2026, not released, in both. Author "Jeffery Kline" appears only in main.tex; README names none (the Kline v0.2.0 DOI link text matches Kline26). Not an inconsistency. paper/main.pdf exists, dated Oct 21 14:14; I did not check that it matches main.tex.

## 4. Citations (checked against local texts)

VERIFIED (17)
- DGS71 Theorems 5.2-5.4: multiplier theorems for negacyclic C-matrices (5.2 characterization, 5.3 v-1 is a multiplier, 5.4 Hall-type). Section 6 does discuss the 1+p^k conjecture (6(3), questions (i) and (ii)), but as a conjecture. Section 8 line 1909 says "explicitly discuss prime-power necessity". Wording nit: say "conjecture".
- JP99 Result 3.8: multipliers m, p (m = p^k), p^i and q^j. Verified.
- JP99 Result 3.10 (Mann test): the multiplier t with t p^f = -1 mod w, and the empty second branch because k^2 - v^2 = 1. Verified.
- JP99 pp.344-347: the (m+1,2,m,(m-1)/2) RDS discussion starts p.344/345; Result 3.8 is on p.345; Results 3.9 and 3.10 and the search table are on pp.346-347. Verified.
- AJMP95 Result 1.8: hypotheses and conclusions (a) and (b), p^j <= mn/u. With |G| = 4t and u = 4d this gives t/d, as the paper states. Verified.
- AJMP95 Proposition 2.2: splitting (m+1,2,m,(m-1)/2) RDS do not exist, so the nonsplitting remark is right. Verified.
- Tan18 Theorem 4.3, Theorem 4.6 and Theorem 4.10 (orbit and multiplier-order reductions; Legendre decomposition in 4.3), and Definition 2.10 (the mu_q conventions). Verified in tan2016.txt.
- AJP90 Theorem 4.2 (inverse multiplier: primes dividing k-lambda1 divide n), Theorem 5.3 (square-free part 2, n a power of 2) and Theorem 6.5 (proper RDS with inverse multiplier has m = k = n*lambda). Verified in the OCR text (garbled but unambiguous) and in turyn-phase SOURCE-COMPARISON.md, which gives printed pp.49, 52-53 and 57.
- Tan26 Section 5: Z[i] character reduction. Verified in arXiv text. The paper's "Gaussian two-component formulation" is a fair paraphrase.
- Miller25: Theorem 1 with G = C_{p^e} x H, e >= 2, matches the paper's description.
- Sutherland21 Theorems 28.6 and 28.9, Section 28.4, Remark 28.12: confirmed through the quarantine catalog-arithmetic LITERATURE.md summary (page numbers 5, 6, 8). The lecture PDF itself was not opened. Counted as VERIFIED-via-notes.
- Gordon26, Tan26 and Miller25 metadata: matches checks/BIBLIOGRAPHY-METADATA.md and the local arXiv headers.

MISMATCH (0)

NOT-LOCAL (3)
- AJP91 theorem and parts (a)-(c), and the 1994 erratum details in section 8 ("replaces a scalar ... rejects equation (11), doubts part (c)"). The paper itself says the full 1991 text was not obtained. Only the quarantine notes support this.
- AV99 (q=425 settled): abstract and record only, as the bibliography says.
- AM01 theorem: unobtained, correctly flagged in the paper.

Bibliography metadata: Turyn65, Turyn72, DGS71, AJP90, AJP91, AJMP95, JP99, AV99, AM01, Schmidt99 and 02, LS05, LS16 and Tan18 match my knowledge of the journal, volume and pages. No obvious errors. Gordon26 (J. Algebraic Combin. 63, Art. 24) and AGZ21 (Cryptogr. Commun. 13, 775-789) are consistent with the notes but not checked by me against the journals. The metadata note says the Tan26 title and version were checked against arXiv. Schmidt99 and LS16 have no URL or DOI (harmless).

## 5. Process language in reader-facing text

paper/main.tex:
- "dossier": lines 1930, 2003, 2049.
- "project" as process language: 1931 (project-specific), 1943, 2002, 2020, 2040 ("Verified project result"), 2051, 2219 (caption "Project frontier").
- "accepted": 2219 ("all accepted unconditional exclusions"), 2233 ("previously accepted certificates"), 2251 ("accepted statements ... corrected proofs").
- "acceptance": 2246 ("distinguishes preservation from acceptance"), and 2331 in the appendix table ("later acceptance records control stale draft labels").
- "preserved research tree": 2244; "document assembly": 2200; "collection script": 2158ish.
- "AI reviewers" at 230 is a disclosure, not leakage.
- "lane": none. "agent": none. "accepted source": no exact phrase. "pass" (877, 1880) is mathematical use.

NOVELTY-ASSESSMENT.md: "project record" line 44; "Checked project result" line 23; "established project identity" line 20; "project-specific" line 18; "retained" lines 4, 53, 58, 63; "release handoff" link line 68 (RELEASE-HANDOFF.md is an internal process file and should not be linked from the public surface).

README.md: no hits for the listed terms. "this record" appears under the coverage table, which is harmless.
