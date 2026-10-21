# Admission record

**Current verdict: ADMITTED**

**Release state: ADMITTED**

**Version:** 0.1.0

**Immutable tag:** `v0.1.0` (tag object `17d9b8d60db943c1b7f15eb63da760a303960164`)

**Tagged commit:** `2ac74ae889b0827ea54f9a35b9a17472e64a5f70`

**Version DOI:** [`10.5281/zenodo.23545780`](https://doi.org/10.5281/zenodo.23545780)

**Concept DOI:** [`10.5281/zenodo.23545779`](https://doi.org/10.5281/zenodo.23545779)

**Admission date:** 2026-10-21

This is the live gate record for release 0.1.0. It applies Jeff Kline's
[public research standard](https://jeff-kline.github.io/posts/research-program/index.html),
version 0.4 draft. Admission under that standard is a project release decision.
It is not peer review, a correctness certificate, or proof of global novelty.

Status vocabulary: `PASS`, `PARTIAL`, `FAIL`, and `N/A`.

## Principal claim and boundary

Let `t` be odd and `q = 2t - 1`. Turyn constructed symmetric Turyn pairs when
`q` is a prime power; the converse is open. This paper proves two principal results:
- No pair is fixed by the square subgroup of the fibre at a prime `p >= 7`
  dividing `t` exactly once.
- No pair on `H x C_3`, with `H` odd abelian, is fixed by inverting the `C_3`
  factor unless `H` is trivial.
Further uniform criteria, earlier results and certificates exclude 655 of the 663
eligible non-prime-power `q < 10000`. Eight remain open, the smallest 3965. The
exclusion at 5185 known so far assumes GRH and is not counted.

## Gates

| Gate | Status | Evidence |
|---|---|---|
| P1 prior work and credit | PARTIAL | Paper §8 and Table 2 give a bounded comparison with exact theorem numbers; all 17 local citations were verified (`audit/CLAIMS-AUDIT.md`). Named residuals: Arasu–Ma 2001 (publisher HTTP 403), the full 1991 Mann paper, and a targeted prior-art search for the mod-16 reconstruction. "New" means "not found in the checked sources". |
| A1 claim and artifact consistency | PASS | Two mathematical audits of the assembled manuscript found 0 errors, and their minor fixes are applied. A claims audit found 8 mismatches, all fixed. An equivalence check of the edits found 0 broken hunks. The title, abstract, introduction, README, CITATION, Zenodo record and site entry agree. |
| R1 release and stewardship | PASS | GPL-3.0-only; `CITATION.cff`; `CORRECTIONS.md`; `MANIFEST.sha256`. A clean-copy build passes, `verify/verify_coverage.py` exits 0 with byte-identical expected output, and `certificates/check_certificates.py` passes 11/11. Tag `v0.1.0`. The Zenodo archive (GitHub integration), downloaded, is byte-identical to the pinned GitHub tag zipball: 1,221,964 bytes, SHA-256 `0341d4e0ed4a8e7d5fbb249e6043d474493aad1ca0bd999bf167e7dbf6421aed`, provider MD5 `7349c82f25be66dcc7dc04616b437e17`. Site listing published (see below). |

## Archive record

- Zenodo record 23545780: title, creator, version `v0.1.0`, date 2026-10-21,
  license GPL-3.0, resource type software, related identifier the `v0.1.0` tree.
- The archived-state release audit passed 11/11 on the unchanged tagged tree.
- A secondary `git archive` of the tag has SHA-256
  `b75e4e00938fcba33030942116f279074909b9582df39bd6eb940aba1ca7aeae`. It is a
  determinism check only and is not expected to equal the provider zipball.

## Public listing

The landing page at https://jeff-kline.github.io lists this release as
"Progress on Turyn's converse". The title links to this repository and a
separate link gives the version DOI.

## Residual risks

- All reviews are process-separated AI reviews, not expert peer review.
- The certificate for 7929 is an inherited predicate that needs numpy, and the
  C73 half of 8905 uses a recorded enumeration (`certificates/README.md`).
- The verifier checks that the uniform criteria agree with the stated theorems
  and the data. It does not re-prove the theorems.
- The files in tag `v0.1.0` describe themselves as a release candidate. That
  wording is kept because the tag is immutable.
