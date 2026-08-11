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
