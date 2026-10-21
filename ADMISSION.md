# Admission record

**Current verdict: NOT YET ADMITTED**

**Release state: CANDIDATE**

**Version:** 0.1.0

**Immutable tag:** `v0.1.0` (not yet created)

**Version DOI:** none yet. Zenodo will mint one when the GitHub Release is published.

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
| P1 prior work and credit | PARTIAL | Paper §8 and Table 2: a bounded comparison with exact theorem numbers, all 17 local citations verified (`audit/CLAIMS-AUDIT.md`). Open: Arasu–Ma 2001 (publisher HTTP 403), the full 1991 Mann paper, and a targeted search for the mod-16 reconstruction. These are named in the paper, and "new" is defined as "not found in the checked sources". |
| A1 claim and artifact consistency | PASS (candidate) | Two mathematical audits of the assembled manuscript found 0 errors; all minor fixes are applied. A claims audit found 8 mismatches, all fixed. An equivalence check of the edits found 0 broken hunks. The title, abstract, introduction, README and CITATION agree. Dispositions: `audit/DISPOSITIONS.md`. |
| R1 release and stewardship | PARTIAL | GPL-3.0-only license, `CITATION.cff`, `CORRECTIONS.md` and `MANIFEST.sha256` are present. A clean-copy build and `verify/verify_coverage.py` (exit 0; output matches the expected file) both pass, and `certificates/check_certificates.py` passes 11/11. Still to come: the tag, the Zenodo archive and DOI, provider byte identity, and the site listing. |

## Residual risks

- All reviews are process-separated AI reviews, not expert peer review.
- The certificate for 7929 is an inherited predicate that needs numpy. The C73 half
  of 8905 uses a recorded enumeration (`certificates/README.md`).
- The verifier checks that the uniform criteria agree with the stated theorems and the
  data. It does not re-prove the theorems.
