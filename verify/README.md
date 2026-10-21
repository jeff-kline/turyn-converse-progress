# Coverage verification

`verify_coverage.py` re-derives the finite coverage record of the paper
(`paper/main.tex`, recorded-coverage theorem and Section "Coverage, certificates,
and reproducibility") from the theorem statements, and compares it with
`data/coverage.csv`.

## Run

    python3 verify/verify_coverage.py            # full run, q < 10000
    python3 verify/verify_coverage.py --limit 2000
    python3 verify/verify_coverage.py --q 3965   # per-criterion detail for one q

Python 3.9+, standard library only. Expected runtime: 30 to 50 seconds for the
full run on one core (measured 32 s and 47 s). Exit status 0 only if every check passes. The
output of a full run is in `expected-output.txt` (runtime is printed to stderr and
not part of it).

## What it checks

For each q = 1 mod 4, 5 <= q < 10000, with t = (q+1)/2:

* whether q is a prime power, a sum of two squares, eligible (neither of these fails);
* the eleven criteria of the CSV key set, each computed from the paper's statements,
  never from the CSV:

| Key | Paper statement |
|---|---|
| (H0) | common multiplier group, Sec. 2.1 (D1) |
| O | odd-index averaging, Sec. 2.2 |
| T2 | prime-power quotient bound, Sec. 2.2 |
| T1 | full-unit fibre bound, Sec. 2.3 (theorem proper) |
| T4 | index-two prime-fibre theorem and its H0 corollary, Sec. 2.4 |
| T5 | odd-index prime-fibre bound, Sec. 2.5 |
| FC | full-conductor necessity, Sec. 3 |
| QE | exact quotient-energy criterion, Sec. 4 (every divisor m of t) |
| Fixed_fibre | fixed origin fibre corollary, Sec. 4.1 |
| Doubling_origin | origin-coefficient set under doubling cycles, Sec. 4.1 |
| C2_uniform | full three-fibre obstruction / coordinate-free form, Sec. 5 |
| Full_prime_fibre | full prime-fibre obstruction, Sec. 5 |

Then:

1. each flag is compared with the CSV on all 2499 rows (agreements, disagreements);
2. the union over eligible q is 644 below 10000 and 122 below 2000;
3. the 11 "additional recorded" exclusions are read from the CSV `status` column, and
   eligible minus union minus those 11 is exactly {3965, 4745, 5185, 5525, 6409, 7565, 7685, 8245};
4. control: no criterion fires at any of the 642 prime powers (a firing would
   contradict Turyn's construction);
5. the paper's "quotient version of T1" does not change the union.

Where the paper leaves a convention open, the reading used is stated in a comment
at the criterion and in `NOTES.md`.

## What it does not check

* The 11 case-specific certificates (`certificates/`: Gaussian augmentation-ray tests,
  norm lattices, the C_61 census, and so on). Their status is taken from the CSV.
* The proofs of the theorems. The script tests whether each theorem's firing condition
  holds; it does not test that the theorem is true.
* The simultaneous quotient-signature theorem (Sec. 4.1), which is not in the paper's
  selected union.
* Any claim that the eight frontier parameters are open in the whole literature, or the
  GRH-conditional status of 5185.
