# NEARS-1806 — QA progress (fix-cycle 2, delta re-QA)
Tip 534d9093 · base 9f66bfe4 · worktree /Users/Apple/Projects/nears-NEARS-1806-base-descent
HERMETIC: no device, no lock, no app, no screenshots.

- BUG 1 CLOSED — legacy escape refuses on residual; NEARS-1689 9b exit 4 (was 0), WARN names I-2 STALE (n_stale=4). Mutation MUT-1 (gate off) -> 6 FAILs; MUT-2 (always refuse) -> 4 FAILs.
- BUG 1 C14C class CLOSED — BASE-ADVANCED under rc 4 refuses; pinned + mutation-covered.
- BUG 2 PARTIALLY CLOSED — object-key orphans now break coverage FULL (MUT-3 -> 2 FAILs). But the "UPPER BOUND" framing is FALSE: array-element SHAs skipped by BOTH harvest and tally. -> BUG 5.
- BUG 3 CLOSED — no dangling assertion survives; AC3 re-grounded on inline header; all 3 remaining review-lessons.json mentions carry an explicit NOT-COMMITTED caveat.
- BUG 4 CLOSED — --all-runs marked "Not implemented ... exits 2 (USAGE)".
- NEW BUG 5 (Medium-High) — unexamined is not an upper bound; false green constructible.
- NEW BUG 6 (Medium) — --key + --evidence: exit 3 -> exit 0 PASS over a run-file orphan.
- Self-floor 86, load-bearing (deleting 1 assertion -> 85 -> FAIL exit 1).
- UNWIRED still true and still stated.
- Fence held on all 5 protected files. worktree-prune.test.sh 47 PASS.

---

# NEARS-1806 — QA progress (fix-cycle 3, FINAL delta re-QA)
Tip 5442b06d · base 9f66bfe4 · worktree /Users/Apple/Projects/nears-NEARS-1806-base-descent
HERMETIC: no device, no lock, no app, no screenshots. Verdict: **FAIL** (strike-list, not a rebuild).

## Corroborated (all independently re-run, not taken from the envelope)
- Self-test **126/126**, exit 0, **0** `^  FAIL ` lines; `ok` count 126 == printed total. Floor `>=125` holds.
- Tombstones only: `manufacture a green` / `UPPER BOUND` appear 4x in the guard, every one labelled FALSE and citing C14/C16; **0** occurrences in runtime output on BOTH the normal and `BASE_DESCENT_LEGACY=1` paths.
- Headline intact: `--key NEARS-1689 --phase 9b` names all **4** orphans (01b545c7, 21161505, 31591f19, f92c5a30), `stale=4`, exit 4. `LEGACY=1` also exit 4, WARN names `I-2 STALE (n_stale=4)`.
- `worktree-prune.test.sh` **47 PASS**. Fence held: change-set touches only 4 files, none protected.

## BUG 5 (array SHAs) — CLOSED, measurement reproduced independently
Old keying (`$p|last`) vs new (nearest string ancestor), on the real run files:
  NEARS-1364 2->4 · NEARS-1252 0->5 · NEARS-1253 0->3 · NEARS-1441 0->2 · NEARS-1444 0->2  (exact match)
MUT-A (revert both jq blocks to `$p|last`) -> **5 C16 FAILs**. Pin is load-bearing.

## The exit-4 attribution TESTED (schema gap, not inertness) — CONFIRMED
All five still exit 4. Supplying only the missing run-file field flips them:
  1252/1253/1441/1444 + `--base-ref main` -> **exit 0 PASS**, assertions_made 7/5/4/4.
  1364 + `--base <its own base_sha>` + `--base-ref main` -> **exit 0 PASS**, assertions_made 6.
  (1364 with `--base-ref feat/init-storybook` -> exit 5 BASE-ADVANCED — a real finding, correct.)
=> the guard genuinely asserts on real data (I-1 descent + 2-5 evidence SHAs per file). The exit 4
   is the run-file schema (no `base_ref`; 1364 records `base_sha`, not `base`). Attribution stands.

## BUG 6 (--key + --evidence) — CLOSED, rejection COMPLETE
Exit 2 on all four forms: `--key K --evidence X`, positional `K --evidence X`,
`--evidence X --key K` (order-independent, it is a post-parse check), and `--base S --key K --evidence X`.
MUT-B (remove the rejection) -> **5 C17 FAILs**, first one `expected exit 2, got 0` — the exact
false green BUG 6 described. Reject-vs-union: ENDORSED (exit 2 cannot read as green; usage already
scoped `--evidence` to run-file-free mode; the wiring diff never combines them — verified).

## Census in the header — re-measured, EXACT
905 files / 899 parseable · base=SHA 333 · branch-name 517 · none 49 · 475 distinct SHA-bearing key
names (437 excluding agent|session) · commits 65 + branch_commits 12 + commit_shas 8 = 85 occ /
83 distinct / 80 resolve · all 85 are ARRAY elements. Every number in the census block checks out.

## UNWIRED — still true AND now asserted
W1 greps the repo for a caller (excluding guard, suite, unapplied diff, solution doc, qa-evidence)
and passes. AC1 still NOT implemented: the executable code uses `merge-base --is-ancestor` (L453);
the AC1 form appears only in header prose as the trap. Cycle 3 widened EV_FIELDS (an I-2 harvest
change) and widened the equivalence pin from one fixture (P2) to four (EQ) — neither touches AC1.

## NEW findings (the strike-list)
- **BUG 7 (Medium)** nested `base`/`base_ref` key => SHA in NEITHER tally; demonstrated
  `coverage: FULL`, `unexamined=0`, exit 0 over an orphan. 93 values / 82 files in the corpus
  (70 NEARS-*), but ZERO live orphans today — latent, not firing. Guard L288-291 and L542-544
  claim the opposite ("never neither"). -> bug-nested-base-key-invisible-to-both-tallies.log
- **BUG 8 (Medium)** the claim-audit table records the sibling-guard exit-4 rationale as "removed
  outright"; it is still at guard L121-122, unpinned. -> bug-claim-audit-row-false-sibling-rationale.log
- **BUGS 9-12 (Low)** git-absent exit-4 prints no tally (2nd undocumented exception); "516 of 898"
  survives 3x in the wiring diff + the solution doc and is now 517 of 899; stale "32" denominator in
  comments (live 35); "FLOOR, not a total" / "DEGRADED" / the [7]-[8] matrix row carry no pins.
  -> bug-minor-unpinned-and-stale-claims.log
