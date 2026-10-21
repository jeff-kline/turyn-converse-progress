# Progress on Turyn's converse: general symmetry theorems and coverage below 10,000

**Status: version 0.1.0 admitted October 21, 2026.**
The immutable release is tagged
[`v0.1.0`](https://github.com/jeff-kline/turyn-converse-progress/releases/tag/v0.1.0)
and archived at the version DOI
[`10.5281/zenodo.23545780`](https://doi.org/10.5281/zenodo.23545780).
The concept DOI
[`10.5281/zenodo.23545779`](https://doi.org/10.5281/zenodo.23545779)
resolves to the latest archived version. Admission under the
[public research standard](https://jeff-kline.github.io/posts/research-program/index.html)
is a release decision, not peer review or a correctness certificate. The
archive passed provider-byte verification, and the living metadata and
public-site listing passed the admission gate. Files inside the tag still
call themselves a release candidate; the tag is unchanged by design.
See [ADMISSION.md](ADMISSION.md).

Jeffery Kline

A symmetric Turyn pair of odd length $t$ is a pair of symmetric $\pm1$
sequences, one with a zero at the origin, whose periodic autocorrelations add
to $q=2t-1$ at shift zero and to zero at every other shift. Turyn constructed
such pairs whenever $q$ is a prime power and asked whether the converse holds;
it remains open.

This paper proves restrictions on the symmetries such a pair can have and
combines them with classical multiplier theorems. Two results are central:

- If a prime $p\ge7$ divides $t$ exactly once, no pair is fixed by the
  decimations that act as squares on the $p$-component and trivially on the rest.
- On any group $H\times C_3$ with $H$ abelian of odd order, no pair is fixed
  by inverting the $C_3$ factor unless $H$ is trivial.

Both apply when $t$ is squarefree, where earlier conductor tests say nothing.
Together with exact quotient tests, norm-lattice certificates, earlier
results, and a ray-class transport that excludes an infinite family $q=13p$,
they exclude 655 of the 663 parameters $q<10000$ that are not prime powers, satisfy
$q\equiv1\pmod 4$, and are sums of two squares. Eight remain open: 3965, 4745,
5185, 5525, 6409, 7565, 7685, 8245. A mod-16 identity reduces 3965 from 198 to
132 unknown signs but does not settle it.

## What is new

The earlier paper ([Kline, v0.2.0](https://doi.org/10.5281/zenodo.21776269))
excluded many composite orders below 2000 by quotient methods. Multiplier
theorems (Delsarte–Goethals–Seidel), field descent and contraction counting are
classical. New here:

- **Index-two prime fibres (principal result).** If a prime $p\ge7$ divides
  $t$ exactly once, no pair is fixed by the squares acting on the
  $p$-component. The proof plays a mod-2 support identity against the energy
  identity.
- **Inverting a $C_3$ factor (principal result).** On $H\times C_3$ with $H$
  odd abelian, no pair is fixed by inverting $C_3$ unless $H$ is trivial. No
  cyclicity or size hypothesis is needed.
- **Multiplier kernels.** The exact stabilizer of a pair injects modulo
  $\mathrm{rad}(t)$, which forces full conductor $F(4t,q)=4t$ and a sharp cofactor threshold.
- **Ray-class transport.** One certified incompatibility at $q=2561$ is carried to
  infinitely many $q=13p$.
- **Mod-16 reconstruction.** In a stated arithmetic class, one fibre
  determines another uniquely. Our prior-art search here is incomplete.
- **Further bounds.** An odd-index averaging bound, an all-index
  prime-power bound with a nonvanishing step, and a full-unit fibre bound.
- **Coverage.** A 2499-row ledger with an explicit eight-order frontier.

Not new: the common multiplier group specializes known multiplier theorems;
the three-power family follows from the published field-descent bound; the
quotient-energy and doubling-cycle tests apply the classical contraction
method; the odd-index fibre bound is a short corollary of standard counting.
The 655 exclusions measure coverage; 644 come from the uniform criteria, 11
from earlier or case-specific certificates, and many orders were excluded
before. "New" means not found in the sources we checked; priority is
unresolved for every result. Section 8 and Table 2 of
the [paper](paper/main.pdf) give the comparisons and list the sources we could
not obtain, chiefly Arasu–Ma (2001).

## Earlier work

Delsarte, Goethals and Seidel (1971) and Jungnickel and Pott (1999) study this
same existence question as negacyclic conference matrices and as cyclic
relative difference sets with parameters $(2t,2,q,t-1)$. Arasu, Jungnickel,
Ma and Pott give the Mann-type parity tests that overlap our conductor
criterion. Tan, Schmidt, and Leung–Schmidt supply the field-descent and
orbit-energy methods we specialize. Section 8 of the paper records exactly
which statements each source covers.

## Coverage below 10000

| Parameters $q\equiv1\pmod4$, $5\le q<10000$ | Count |
|---|---:|
| All | 2499 |
| Prime powers (pairs exist) | 642 |
| Not a sum of two squares (no pair) | 1194 |
| Remaining, eligible | 663 |
| Excluded by the uniform criteria | 644 |
| Excluded by earlier or case-specific certificates | 11 |
| Open | 8 |

Below 2000 every eligible parameter is excluded (124 of 124). The exclusion at
5185 known so far assumes GRH, so 5185 is counted as open. "Open" refers to this
record, not to the whole literature.

## Contents

- [Paper (PDF)](paper/main.pdf) and its [LaTeX source](paper/main.tex)
- [Per-order coverage, all 2499 parameters](data/coverage.csv)
- [Verification script](verify/), which recomputes every uniform criterion from
  its definition and checks the counts above
- [Certificates](certificates/) for the eleven case-specific exclusions
- [Review records](audit/) for this manuscript
- [Corrections policy and version history](CORRECTIONS.md)

## Build and check

The verifier needs only Python 3.9 or later and its standard library:

```sh
python3 verify/verify_coverage.py
```

Its expected output is in `verify/expected-output.txt`. To typeset the paper:

```sh
cd paper && pdflatex main.tex && pdflatex main.tex && pdflatex main.tex
```

## Verification and responsibility

The proofs and programs were developed with AI assistance. Each principal
result had an isolated failure search, a separate proof audit, and an
arithmetic check by a separately written program. The assembled manuscript
then had two more mathematical audits, a claims and citation audit, and an
equivalence check after editing (see `audit/`). These are AI reviews, not
expert peer review. The author is responsible for the content.

## License and citation

GPL-3.0-only; see `LICENSE`. Citation metadata is in `CITATION.cff`.
