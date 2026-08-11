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

================================================================================
## [8] FINAL GATE — fix cycle 4 verification (appended 2026-08-11, QA pass 4)
================================================================================
## Corroborations of the owner's own facts
- self-test 147/147, exit 0, 0 `^  FAIL ` lines, ok count 147 == printed total  -> CONFIRMED
- fence: all five protected files TRACKED and UNMODIFIED vs base (empty `git diff --name-only`) -> CONFIRMED
- worktree-prune.test.sh 47 assertions PASS -> CONFIRMED
- `git apply --check` on the wiring diff -> OK
- NEARS-1689 headline still names all four orphans (f92c5a30 21161505 31591f19 01b545c7) -> CONFIRMED
- diff is 4 NEW files, 2372 insertions, ZERO deletions, zero existing files touched

## Mutation matrix (fake-repo harness; positive control = unmutated copy 147 ok / 0 FAIL)
MUT-A  revert BOTH jq filters to $p[-1]                 -> 5 FAIL, all C16      (engineer's claim: 5, all C16)  MATCH
MUT-B  drop the --key + --evidence rejection            -> 5 FAIL, all C17      (engineer's claim: 5, all C17)  MATCH
MUT-C  restore the ANY-DEPTH base/base_ref exclusion    -> 4 FAIL, all C23      (BUG 7 pin, faithful)           MATCH
MUT-D  drop the exclusion entirely                      -> 9 FAIL incl. C23 control + C15 control + C15/C16
MUT-E  git-not-found path -> exit 0                     -> 1 FAIL, C24          (BUG 9 pin)                     MATCH
MUT-F  delete "the stale count is therefore a FLOOR"    -> 1 FAIL, C8           (BUG 12 pin)                    MATCH
=> C23 is pinned in BOTH directions; neither "exclude at any depth" nor "never exclude" survives the suite.

## BUG 7 — independent from-scratch repro (my own fixture, orphan commit at phases.9b.base)
PRE-FIX  (MUT-C)  unexamined=0  coverage: FULL     rc=0
POST-FIX (shipped) unexamined=1 coverage: PARTIAL  [base]  stale=0  rc=0
Matches the owner's own repro exactly. Exit deliberately unchanged and pinned by C23's assert_rc 0 + stale=0.

## Legacy escape (live)
(a) pure nothing-asserted + LEGACY=1        -> rc 0, verdict word still NOTHING-ASSERTED  (C9)
(a') same without LEGACY                    -> rc 4
(b) nothing-asserted + real stale residual  -> rc 4, "REFUSED: I-2 STALE (n_stale=1)"      (C14)

## Wiring handoff hashes (all four verified by applying into a scratch tree)
PRE  new-task.md     2596a31dad4068c6a2749e20de06ff341d604d4a / 39abcd00c4cd48f9ba5162238476e678  == live
PRE  workflow.json   2e3ba0b4e4374b9b0c78139aaf076701b53c4786 / 200ae9d61b2dfadc194fe05aaaa3fae4  == live
POST new-task.md     51a275ad35b9f4cac773bea042b89fd4c5cd44f8 / 659cb8850a01090f93b6ae3d32362e58  == applied
POST workflow.json   5b0ada60ad2affafa74a330ff456d76a5db35a2a / e0df6cffe53f7527dd64653016099033  == applied
post-apply: jq OK; "the same base-descent assert as" -> 0; is-ancestor survivors 1 (new-task.md) + 2 (workflow.json) + 1 (worktree-prune.sh) = the 4 intentional

## BUG 10 — the volatile number
`516 of 898` is GONE from all three applied sites. Replaced with
"dated measurement, 2026-08-11: 517 of 899 parseable, a figure that DRIFTS DAILY, so re-measure with the
census command in base-descent-check.sh's header rather than quoting this one". Reads dated-and-stale-able.
Independent re-measure today: 906 files / 900 parseable / 333 SHA / 518 branch-name — i.e. it HAS already
drifted by one since the dated measurement, which is exactly what the wording predicts. Framing honest.

## UNWIRED
Live grep finds only the 4 self-excluded files. W1 asserts it, and W1 is NOT a constant-true:
an accidental scratchpad copy of the guard reddened W1 during this pass ("the guard is no longer UNWIRED").

### Disposition of the fix-cycle-4 strike list (BUGS 7-12)
BUG 7  CLOSED — verified by independent from-scratch repro + MUT-C/MUT-D. See mutation-matrix.log.
BUG 8  CLOSED — all 5 'removed outright' rows re-checked against the shipped guard by grep:
         row 1 (five scenarios / truth table)      0 hits  TRUE
         row 2 (NEARS-1689 demo SHAs)              0 hits for all 6 probes  TRUE
         row 3 (review-lessons forensic para)      1 condensed successor at guard L91-95  PARTLY FALSE, row corrected
         row 4 (sibling-guard exit-4 rationale)    sentence LIVE at guard L126-132, reworded+kept,
                                                   now tagged [C4, C7, C24]; C4/C7/C24 each assert rc!=0  FALSE, row corrected
         row 5 (corpus counts in runtime output)   corpus numbers appear ONLY in the dated header
                                                   census (L217/227/229); positive-controlled  TRUE
       Both corrections are recorded in the doc's own table. The countermeasure held.
BUG 9  CLOSED — C24 pins it; MUT-E reddens exactly C24.
BUG 10 CLOSED — 516 of 898 gone from all 3 applied sites, replaced by a dated + re-measure form.
BUG 11 CLOSED IN CODE — EV_FIELD_COUNT=35 == real list length (C18). RESIDUAL IN THE DOC ONLY:
       solution doc §1 L53 still says 'the 32 names in EV_FIELDS'. Followup, not a gate finding —
       nothing gates on it and C18 keeps the runtime denominator honest. See followup-doc-32-denominator.log.
BUG 12 CLOSED — MUT-F reddens exactly C8; C13/C6B/C1 present.

### VERDICT: PASS. No reachable false green found. No claim the code does not honour, in the guard.
