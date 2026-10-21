# Certificates for the eleven additional exclusions

The coverage theorem in `paper/main.tex` (Table `tab:additional`) lists eleven
orders outside its uniform criteria: 909, 1845, 2561, 2665, 6137, 7461, 7929,
8865, 8905, 9245, 9265. This folder holds the smallest exact records found for
each, or a citation where the earlier archived paper already covers the order.

Scope. The files let a reader re-run the finite computations behind each
exclusion. They do not re-prove the theorems the exclusions rest on (see the
paper and `audit/`). Several rows depend on earlier campaign records that were
accepted, not recomputed from scratch; each row says which.

"Archive" below means the earlier paper's repository, version 0.2.0,
DOI [10.5281/zenodo.21776269](https://doi.org/10.5281/zenodo.21776269), tag
`v0.2.0` of `jeff-kline/turyn-converse`. The cited files
(`code/orbit_signature_scan.py`, `code/marginal_orbit_algebra.py`,
`AUDIT_LOG.md`) are byte-identical at that tag and at the later commit
`3341c9c` used for this work, which only records the v0.2.0 admission.
Proposition `prop:selfconj` is present in the paper at the tag.

## Per-order table

| q | Mechanism (one line) | Files or citation | How to check | Tool needed |
|---|---|---|---|---|
| 909 | Cited. Closed by the archive's hierarchy for multi-prime composite q <= 2000 (3^2 * 101). The archive's panel records the killing node as divisor 7, mechanism `constant_row_rational`; this paper labels the node the full-unit C7 Gaussian ray test. That the two labels describe the same obstruction is not shown here. | Archive: section "Closed orders" (`sec:results`) of `paper/main.tex`; `code/orbit_signature_scan.py`, table `PANEL_KILLS`, entry 909 -> (7, 2, "constant_row_rational"); `code/examples/scanner_existential_divisor_output.txt`. No data copied. | `check_certificates.py` also runs the C7 ray test independently. | Python standard library |
| 1845 | Cited. Self-conjugacy (inert tower): 3 divides q = 3^2*5*41 to an even power and ord_d(3) is odd for every divisor d > 1 of t = 923. | Archive: `paper/main.tex`, Proposition `prop:selfconj` (section "The self-conjugacy boundary"). The 13 self-conjugacy closures at q <= 2000 are listed in the archive's `AUDIT_LOG.md` (finding F2); 1845 is the last. No data copied. | `check_certificates.py` re-evaluates the condition. | Python standard library |
| 2561 | 13 * 197, t = 1281. Two exact certificates exist: (a) complete C61 census, no integral augmentation-compatible lift; (b) factor matching, 112 factor-lattice catalogs, no product allocation survives at length cutoff 80 for any of the eight signed augmentations. Shipped: (b), plus the residue contradiction from (a). The 105 MB census of (a) is not shipped. | `c61/` (factor-match, checker, inputs); `q2561-short/augmentation-residues.json` | `check_certificates.py` (1-2 minutes for this item), or run `c61/factor-match/colored100.py` after unpacking the `.gz` files in place. For `q2561-short`: the two residue sets mod 61 are disjoint; its parity-census residues come from the full census, which is not shipped, and the script only checks the norm-2561 side and the disjointness. | Python standard library |
| 2665 | 5*13*41. Complete C43 quotient-correlation census: no solution for any of the four augmentations. The C31 node was not evaluated (raw-size cap). | `q2665/q2665-probe-row.json` (recorded row); `local-ray/correlations.py` (census engine) | `check_certificates.py` calls `census(2665, 43)` and expects 0 solutions. That the engine's bounded enumeration is exhaustive rests on its audit record, not on this script. | Python standard library |
| 6137 | 17 * 19^2. Full local group at C11 (\|H\| = 10 = phi(11)) and no Gaussian ray U - V = 11(a+ib) with a, b odd and \|a\|, \|b\| <= 279. | `local-ray/` (engine; `ledger-rows.json` has the recorded row) | `check_certificates.py` | Python standard library |
| 7461 | 3^2 * 829. Same ray test at C7 (fibre 533). | `local-ray/` | `check_certificates.py` | Python standard library |
| 7929 | 3^2 * 881. Recorded degree-two period predicate at C13: the Q x Q(zeta_13)^H Gaussian-period join has no valid side vector (`no_side_vector`). This is not a quotient-census result; it comes from the archive's code, and only the recorded ledger row and one re-run transcript are shipped. | `q7929/q7929-ledger-row.json`, `q7929/rerun-output.txt` | From the archive's `code/` directory: `marginal_orbit_algebra.py 7929 --tp 13 --prime-subtorus-check` (transcript ends `UNSAT (no_side_vector)`). Script SHA-256 `545ce60b229edce195245189a06a095958dbeb0082da799c090938776d2a4e27`. Not run by `check_certificates.py`. | Archive code at the revision above and numpy 2.0.2 (its `requirements.txt`) |
| 8865 | 3^2 * 5 * 197, t = 4433. C31 node of degree 5: forced Gaussian factors leave residual norm 5; the small-norm rigidity bound makes the character value Gaussian; its even and odd coordinates are incompatible mod 31 with the augmentation. The script checks the numerical substitutions and the trace matrix; the algebraic inferences are in the paper. | `q8865/` | `check_certificates.py` (runs `check_8865.py`) | Python standard library |
| 8905 | 5*13*137. Complete C73 residual census gives 12 marginals forcing abs(augmentation) = (16, 93); complete C61 census gives 8 boxed marginals with abs(augmentation) = (72, 61). The two spectra are disjoint. | C73: `q8905-c73/`. C61: `c61/` (checker, the exported lattices for 8905, and the recorded checker output) | `check_certificates.py` runs the C61 checker (seconds) and the C73 lifting step. The C73 residual enumeration (`residual_8905.py`) needs numpy; only its recorded output is used by the checker. The exported C61 lattices were produced by PARI/GP, which is not shipped; the C61 checker verifies them with exact rational arithmetic and does not call PARI. | Python standard library to check; numpy to re-run `residual_8905.py`; PARI/GP only to regenerate the lattices (not shipped) |
| 9245 | 5 * 43^2. Same ray test at C23 (fibre 201). | `local-ray/` | `check_certificates.py` | Python standard library |
| 9265 | 5*17*109, t = 4633. C113 node of degree 8: residual norm 109; exhaustive domains of 642 odd and 627 even vectors; four residuals (+-3 +-10i); character and augmentation residues mod 113 are disjoint. Two independent scripts. | `q9265/` | `check_certificates.py` (runs both scripts) | Python standard library |

No order lacks a compact certificate, with two qualifications: 7929 is a
recorded predicate re-run with the archive's numpy code, and 909, 1845 are
citations of the archive.

## Running the checker

    python check_certificates.py          # all items, about 1.5 minutes
    python check_certificates.py --fast   # skips the 2561 factor-match run

It copies the tree to a temporary directory, unpacks the `.gz` files, and runs
the shipped scripts there. It prints one PASS or FAIL line per check. When the
folder was assembled, all 11 checks passed (2561 appears twice: factor-match
and residues). Not covered: 7929, and the numpy enumeration for the 8905 C73
node.

## Edits to shipped files

Shipped scripts are the research-tree scripts with these changes only: the line
`assert sys.prefix != sys.base_prefix` (a virtual-environment guard) was
removed; in `c61/checker/check_c61.py`, `BASE = ROOT.parent.parent` became
`BASE = ROOT` so the reference certificate is found under `c61/pursuit-02/`.
Four recorded JSON outputs had a local interpreter path replaced by a
placeholder. Large files are gzipped without other change. The scripts write
output next to themselves, which is why `check_certificates.py` runs them in a
temporary copy.

## Provenance

Original locations are relative to the root of the research tree
(`turyn-converse-2026-10-19`). "Extract" rows are single rows cut from a larger
JSON file, so no hash of the extract's source row exists; the source file is
the one named in the second column.

| Shipped file | Original location (relative to research-tree root) | Original SHA-256 | Shipped SHA-256 | Change |
|---|---|---|---|---|
| `c61/checker/check_c61.py` | `quarantine/c61-reusable-2026-10-20/checker/check_c61.py` | `333b7d1928039d36d3591fd1fe189e1b7d6269ff87abb18c5e8f55192d4b0ae0` | `4d601962841d11f8c35040d483a941aa9b50b8c778c084caee1831e7fa23b9e9` | venv-only assertion removed; BASE path set to ROOT |
| `c61/checker/legacy_exact.py` | `quarantine/c61-reusable-2026-10-20/checker/legacy_exact.py` | `62798e8af05118dcf77c2347ed5d302e6b6bb6cabbe172ad1599faffb40d0ab7` | `30ef78ed8c09297c5f0bc38151f18b249e5059a9334a7a455aa2f5e3d5450a0f` | venv-only assertion removed |
| `c61/checker/q2561.json.gz` | `quarantine/c61-reusable-2026-10-20/checker/q2561.json` | `a53f8992292b19edb5bd3c71ca1bbce59e0bfd9ece65f6734d3a45f1b9cde8bd` | `2249214e90f817d385dbbce0c3e769c62f668dfc3e12f89e02afb5e5309f2721` | gzip; local interpreter path removed from text |
| `c61/checker/q8905-final.json` | `quarantine/c61-reusable-2026-10-20/checker/q8905-final.json` | `e3d8a2088569632729d14493edf559e33473aa6d2be365f38efcfb9fe3c3d909` | `0a2b5847b6c26758e1c7e39b2f5262c2e21968b0e07d9c2e12f3a2109f8423ec` | local interpreter path replaced by a placeholder |
| `c61/solver/q8905/prime_lattices.json` | `quarantine/c61-reusable-2026-10-20/solver/q8905/prime_lattices.json` | `82d385526f1341853c78b5ba77a09a75acb3223fb7f34159bad36ae82c0e565a` | `82d385526f1341853c78b5ba77a09a75acb3223fb7f34159bad36ae82c0e565a` | byte-identical |
| `c61/solver/q8905/parameters.json` | `quarantine/c61-reusable-2026-10-20/solver/q8905/parameters.json` | `f48e9d79963da5beed30e630a5e36a7b8e907d97bebe4761d92af26210f73f96` | `f48e9d79963da5beed30e630a5e36a7b8e907d97bebe4761d92af26210f73f96` | byte-identical |
| `c61/solver/q8905/lattice-000.jsonl` | `quarantine/c61-reusable-2026-10-20/solver/q8905/lattice-000.jsonl` | `a17a8971e7278a5ef4a214c2b33fe5aad6c1b26c9c76d8e5a9bfeefb707783bd` | `a17a8971e7278a5ef4a214c2b33fe5aad6c1b26c9c76d8e5a9bfeefb707783bd` | byte-identical |
| `c61/solver/q8905/lattice-001.jsonl.gz` | `quarantine/c61-reusable-2026-10-20/solver/q8905/lattice-001.jsonl` | `d6beb253ebae7819abb59ed102275a75dcacf57d3ed6bf599e144c690913e90b` | `5ed4ff145a61e2dcf5f52add1827f910438aeca3eb1ecbfaf6a77830f538f01b` | gzip, content identical |
| `c61/solver/q8905/orbits.jsonl.gz` | `quarantine/c61-reusable-2026-10-20/solver/q8905/orbits.jsonl` | `ce74f6925e91ebb852c99dd6cab6c229c66dd266c310c850f6460eb039d864ef` | `17e3f01deb86e2c7dd38075cbe992247ac6b37e97cfffe72050b252c632f8c74` | gzip, content identical |
| `c61/solver/q2561/prime_lattices.json` | `quarantine/c61-reusable-2026-10-20/solver/q2561/prime_lattices.json` | `ed6988e1e5758cdd2c4e94f9416538616fe5593a287a20773873f59fa1c45245` | `ed6988e1e5758cdd2c4e94f9416538616fe5593a287a20773873f59fa1c45245` | byte-identical |
| `c61/solver/q2561/results.json.gz` | `quarantine/c61-reusable-2026-10-20/solver/q2561/results.json` | `310d40bdaeddb6f135af0c4c0b2bd26d26de57781195022db9f67c24c84015b5` | `e2e740a70bc8b93ede9c4dddf630ccc189a0231fab2f7d078e07df74c36fbba9` | gzip; local interpreter path removed from text |
| `c61/factor-match/bases.jsonl.gz` | `quarantine/c61-reusable-2026-10-20/factor-match/bases.jsonl` | `d04df8863e0badeb5c48fcec1adb9498e34152af055fccee285f244eb497d324` | `29f63d3abb738153305c8b4dcc131e54b3c73e0af1fb0f08a3dc87fcbeb55ebf` | gzip, content identical |
| `c61/factor-match/colored100.py` | `quarantine/c61-reusable-2026-10-20/factor-match/colored100.py` | `d3683edf9d78db34b22475c43eb2c58a39e18cbb97ba3c0c850e0c58fb082cfd` | `0a715c27ec919c4c26cb153985720158669a07eb6c8ccd2fd6d584afe8d3f585` | venv-only assertion removed |
| `c61/factor-match/colored100.json` | `quarantine/c61-reusable-2026-10-20/factor-match/colored100.json` | `b6c9414e72d4be7ddb732cdf53713a8f7dc8b72e99c7b4298f7ccf1b122e0742` | `105d7d44d965c04a761749fb2dee51c12ca99e121fb158df03e7eb8244411204` | local interpreter path replaced by a placeholder |
| `c61/pursuit-02/c61_certificate.json` | `pursuit-02/c61_certificate.json` | `8328571becee7f28bcaf41815dbc98a4bc292809e4a73efd364925a3cd02cc50` | `8328571becee7f28bcaf41815dbc98a4bc292809e4a73efd364925a3cd02cc50` | byte-identical |
| `q2561-short/augmentation-residues.json` | `quarantine/c61-reusable-2026-10-20/augmentation-residues.json` | `955e6cf06340efc622b5bf2a3c17fe24eede900418812d1154950e14bee4fa6d` | `955e6cf06340efc622b5bf2a3c17fe24eede900418812d1154950e14bee4fa6d` | byte-identical |
| `q8905-c73/residual_8905.py` | `pursuit-01/residual_8905.py` | `3fa53dd6d521140d89372b97645ba836deea774c9edc62f6a65851eaa9e1bc6f` | `cb5fc3feb280be87e1e01be698bb2e9f93a385d9808d4a7e12e5665df15474ac` | venv-only assertion removed |
| `q8905-c73/residual_8905.json` | `pursuit-01/residual_8905.json` | `9391e6fa4ef1bb371efa16a4690169a909f4151ec7da3719e1be6b08d8af90e4` | `9391e6fa4ef1bb371efa16a4690169a909f4151ec7da3719e1be6b08d8af90e4` | byte-identical |
| `q8905-c73/residual_lifts_8905.py` | `pursuit-01/residual_lifts_8905.py` | `272e4dba4967786809268c313ed03d073d01d456f85ded7f3fb53f750f010a7f` | `4683be8f7dbd42d32e2d07d6a2c3034dbf39445808a891909cffa78321e8d97d` | venv-only assertion removed |
| `q8905-c73/residual_lifts_8905.json` | `pursuit-01/residual_lifts_8905.json` | `6cfc5bdb321775a440252297740d22e9d395aafb899a10c976e08a1c25700500` | `6cfc5bdb321775a440252297740d22e9d395aafb899a10c976e08a1c25700500` | byte-identical |
| `q8865/check_8865.py` | `check_8865.py` | `140105c09af75bdbc1f0f3f806573992871bcfb054e2faa0f2920e67830cc85f` | `ff3a2d1cd8a29c9e49e5f158655aa24b82cfbe8d486c6a3e0155cbc951b50c35` | venv-only assertion removed |
| `q8865/check_8865.json` | `check_8865.json` | `1cec07d58e6772322cfad9d900c9c22b42fa6367a6295343373c02ae2bdfadeb` | `1cec07d58e6772322cfad9d900c9c22b42fa6367a6295343373c02ae2bdfadeb` | byte-identical |
| `q8865/local_multiplier_probe.py` | `local_multiplier_probe.py` | `ba9532c2057a0fd60dad73046d7aac61440646eb51b44f5fd783b6ce293b57e1` | `ba9532c2057a0fd60dad73046d7aac61440646eb51b44f5fd783b6ce293b57e1` | byte-identical |
| `q9265/independent_9265.py` | `pursuit-01/independent_9265.py` | `21de28c0ec2aa526dd785a80078e67751c41ddb6852caf36a1f12f98c713f974` | `45d410e3e1f921a6bb5cb7af6614d615c127eb5dddedb4eeb985bd0ff896dcda` | venv-only assertion removed |
| `q9265/independent_9265.json` | `pursuit-01/independent_9265.json` | `e6ee97ea8f60826d9f77d5452f4141e9a1a4e3c8162156e9b18871e34944791c` | `e6ee97ea8f60826d9f77d5452f4141e9a1a4e3c8162156e9b18871e34944791c` | byte-identical |
| `q9265/residual_9265.py` | `pursuit-01/residual_9265.py` | `464b8a955671d3db6fff49f6eb10e54211596165621eec75ecf2f0385becc964` | `08f731d0a3b982c495de9af240d85e01907a1fded68c8311bd2195f58190a7a2` | venv-only assertion removed |
| `q9265/residual_9265.json` | `pursuit-01/residual_9265.json` | `ab8c8a35cb4f0b52a920e7a195e99712cc6d4065611ec6d11115e3928247a219` | `ab8c8a35cb4f0b52a920e7a195e99712cc6d4065611ec6d11115e3928247a219` | byte-identical |
| `local-ray/correlations.py` | `pursuit-04/correlations.py` | `5b05595dc7d3b143dbe3b66f5664538c3a3188d6d3032cae6bf6c6b32e6a6d34` | `2df552f6a1c43c090f2710d658dc1e70220657679e01b73748056d47e56b3df1` | venv-only assertion removed |
| `q2665/q2665-probe-row.json` | `quarantine/prime-power-followup/frontier-probe-3500.json` | `n/a (derived)` | `1eb61672bd5301359436a5a30669f91c100e47872fc1c12eb4b67df10a753a21` | extract (row q=2665) |
| `q7929/q7929-ledger-row.json` | `quarantine/c61-reusable-2026-10-20/ledger-reviewed.json` | `n/a (derived)` | `8b265e1560868503ec13313ee6d7cfe8370b3ec9064eb5e11c90429735701bd8` | extract (row q=7929) |
| `local-ray/ledger-rows.json` | `quarantine/c61-reusable-2026-10-20/ledger-reviewed.json` | `n/a (derived)` | `fd9e2007db42bc633b6e524bc74384d0d99302cd2232fdbd4caccd5830692fe8` | extract (8 rows) |

Generated, not copied: `q7929/rerun-output.txt` is the output of the archive command above (SHA-256 `bb0426fba0e3886a21d4a3784c58097729baa751655aeeed5673c7e1c433f0f5`); `check_certificates.py` is new.
