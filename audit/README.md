# Audit reports for this manuscript

These are process-separated AI reviews of the manuscript in `paper/main.tex`,
not expert peer review. Each was a read-only review by a model session separate from the
session that wrote or edited the text.
They find errors; they do not certify that the mathematics is correct. Nothing
here replaces a referee who is an expert in cyclotomic fields and Turyn-type
sequences.

## What each report covers

| File | Scope |
|---|---|
| `AUDIT-S1-S3.md` | Mathematical audit of manuscript sections 1 to 3: scope and coverage, multiplier, averaging and prime-fibre obstructions, multiplier kernels and full conductor. Proofs re-derived by hand; numerical claims checked by scripts. Verdict per item, notation and hypothesis inconsistencies, and passages most worth an expert's reading. |
| `AUDIT-S4-S7.md` | Mathematical audit of sections 4 to 7: exact quotient energy and doubling cycles, the three-fibre obstruction, exact norm lattices and arithmetic transport, the quadratic mod-16 criterion and forced reconstruction, plus the logic (only) of the coverage argument. |
| `CLAIMS-AUDIT.md` | Claims and citation audit: counts recomputed from the coverage table, agreement of claims between the abstract, README and body, title and status, citations checked against locally held texts, and process language in reader-facing text. |
| `EQUIVALENCE-CHECK.md` | Check that the later wording-tightening edits did not change any mathematical statement: each changed hunk read against its original, with the one proof sentence that was changed examined separately. |
| `DISPOSITIONS.md` | The editor's record of what was done about each finding: applied, or deferred with the reason. |

## Limits of these records

- Line numbers in the reports refer to the manuscript as it stood on the
  review date, 21 October 2026. They may not match the final file.
- The reports mention helper scripts (`audit_*.py`) and the pre-tightening
  `.orig` text files. Those are not included in this repository, and the
  claims they supported are not independently re-checkable from this folder.
- Several findings were fixed after the reports were written; the reports are
  kept as written, not updated.
- The earlier research campaigns' proof audits are not included. They are
  identified only by SHA-256 in the table below, so that a reader who is given
  the original file can confirm that it is the one the manuscript's evidence map
  refers to. The IDs (M01 and so on) are the evidence-map labels used in the
  manuscript's accompanying materials. Several rows share an ID because one
  line of work had more than one audit record.

## Earlier proof audits, by hash only

| ID | Subject | SHA-256 of the audit or check record |
|---|---|---|
| M01 | Foundations and small norms | `f783f24e2b594fa3de838ebfe00d41800e9917e14946d47d4790e751818153a3` |
| M02 | Early exact exclusions and parity rigidity | `14caa426f50c28c99bc552666c3dccabab10565dfdbf552d8df3a8f8d0b4bd30` |
| M02 | Early exact exclusions and parity rigidity | `c581a7530d30d655b3ef09b6c6c2d5bf56d3c2d3f0dba9f8270d2c180a94c3d6` |
| M03 | 8905 exact C61 certificate | `c87ecd048c6da3ffd4bcab945874ed9c7466659fefab087adf46b83affdfaa45` |
| M03 | 8905 exact C61 certificate | `069b08d6894ac6ce570b9b476ddaa2e558bd383d455080cbbcf185772c040ec6` |
| M04 | Local arithmetic row-sum criteria | `2fe53d80608db1015d3f201af7d1fa4a66c9b381dfec93699b333fe62232ccae` |
| M04 | Local arithmetic row-sum criteria | `bc49c445d6a7ffe6f36f4a6a83abebcb0eb95c51a5055dc406b36d49f294674b` |
| M05 | Prime-power quotient criterion | `ffa2474b480b89e1294e9ec634630f6b03976da645ca19f73c0491b2ef0b8131` |
| M06 | Accepted baseline ledger | `7c30cd80bcfe6fe975752fe4748475cd9195ef6ce0ba529886e74c7526f51db5` |
| M06 | Accepted baseline ledger | `4fa8939b1ae8ba7b308d167f79ce65295db4994e431cf2cfab861781503e9680` |
| M06 | Accepted baseline ledger | `5517937da862a0ad13e36dcb43fe93d534fb3afdd62c81a713148ad9c48bd253` |
| M07 | Reusable C61 solver and factor catalogs | `47c5ce27638e7c76d9b6ddf60f47642327245581472469fa95e31d2fb73982d5` |
| M07 | Reusable C61 solver and factor catalogs | `b55f9fe5c54b7eacf5aab3a52f583b2af3abcccef7864a5167d2c7fc1f74ba90` |
| M08 | Arithmetic catalog transport | `feacd538403f0fc9147bbdef42b9b199096351a3e4638065cf5bf07a969f8240` |
| M08 | Arithmetic catalog transport | `9ab7d3e73df7667b45060b9d73799cf5dd115f512bfe61c80261c58e8fb6bb7b` |
| M09 | Odd-index averaging and three-power scope | `0b42df0c8fd7777f36ed088e69a92553534162ea2d9efa6ef8dff0d75e81f50c` |
| M09 | Odd-index averaging and three-power scope | `58f671196f9bf712c1ea39b7aac13c59540700c7e7e3564907ac20f8dba77efb` |
| M10 | Full-conductor structural extension | `39f2cc4eeefc0e8ddc52f8f21ab30cfd5a3b893cda1258fd0ee297814ca241f5` |
| M10 | Full-conductor structural extension | `4c2b2bd050d6aba464e6563a530b55e93b5074d5c916abaeebea5dea0e05534b` |
| M11 | Mann and later-source comparisons | `6f254a46ce1dda9559e5c1db5536471d254d110437d65a48652a23e17a6025d8` |
| M12 | Prime-fibre generalizations | `a1113f1d67a48e87633978fa1a5a6e530a8c1ef5a9f1d4e4c0ddb0a173586ebd` |
| M12 | Prime-fibre generalizations | `4aa6b2c14c2912d888383cca39d4903b45c93a797021e957a2d25265b391bdfa` |
| M12 | Prime-fibre generalizations | `694e328d1b2a6932b7aead3f5f91943d8bb5cf007bb39f38556383da9285b020` |
| M12 | Prime-fibre generalizations | `f0080727bca7d91639ba500aab11611fb383ca92459d09f4588cc4d98a407c4e` |
| M12 | Prime-fibre generalizations | `525828739c79ecc86689cdd961e9eaa289fb250108f6d473f12882ed3591226d` |
| M12 | Prime-fibre generalizations | `03418986723b2acb61e4aa45b6c51a95fa50f86d3b93445a338321b6bfb174e2` |
| M14 | Quotient-energy and three-fibre antecedents | `e07b7347c6017cdf5372321c6c9b230fd4bbd9ce0edf95a72f9ca889628e9bda` |
| M14 | Quotient-energy and three-fibre antecedents | `7cf759a4a7c608b2692ce56673d56a54dea09ec151f5e6783aee4bacfd8c0f81` |
| M14 | Quotient-energy and three-fibre antecedents | `67988ea814e611e12a376f626479acff28e3393618bed2f92a30dc7dd01d164f` |
| M14 | Quotient-energy and three-fibre antecedents | `4b94d54ef0c4da2f31697aa0a569802fc4186f288fac5012a16d2a7d690da72b` |
| M16 | Abelian three-fibre theorem and final coverage | `477faa7f1bc4dad465746255cbc6339875cfeb284697c1bb1c548a256b999734` |
| M16 | Abelian three-fibre theorem and final coverage | `848e770f8c9a94232214f4db9e97860c92185b22ee76a879d12b7e3daba87740` |
| M16 | Abelian three-fibre theorem and final coverage | `bb62b7d971656df242cfb9ecc37f819e26791f3076b6a7e9c2bceff8a1cf8c83` |
| M17 | Quadratic mod16 and reconstruction | `b8271e5a8cd42d9cd33bd774e749b0b7b4933ea05856c023110c7fa41edf878d` |
| M17 | Quadratic mod16 and reconstruction | `77f60fcd1b781c442d686b7a1698972a4c6896c2842f2fbb40c176f4c0fce0b6` |
| M11 | Earlier novelty comparison | `518c67c5b49d418b244104282adc56922488dce0bdf332996e408230ea514925` |
