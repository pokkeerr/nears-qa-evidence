# NEARS-1921 QA-lite [m4] progress

Scope: comment-only DLS change, no live-app UI surface. In-scope AC per live ticket (post-split, Ready): AC1 only. AC2 (real centring fix, 40->48 + padding) is PARKED/out of scope — not tested against a live behavior, only used here as the "regression guard" instruction from the QA spawn (verify no test/golden regression from the comment edit).

## AC1 — comment correction
Read packages/nears_dls/lib/components/nappbar/n_appbar.dart lines 355-377 (the _backButtonWidth doc comment) directly from the worktree.
Confirmed: no longer claims "true optical center" is reached; states measured offset table (4 rows, exact match to ticket table) and both causes (asymmetric padding start:space4/end:space2; 40-vs-48 IconButton footprint under Material3 kMinInteractiveDimension).
Verdict: MET.

## Regression guard (spawn's AC2 instruction)
- `git diff --stat feat/userapp-reskin2..HEAD` -> 1 file changed, 26 insertions(+), 10 deletions(-), packages/nears_dls/lib/components/nappbar/n_appbar.dart only.
- Full diff reviewed line-by-line: every changed line is a `//` or `///` comment. No golden files, no test files, no functional/token lines touched.
- `_backButtonWidth = 24 + NearsTokens.space2 * 2` (line 377) and the Container padding block (lines 165-168, start: space4/end: space2) are byte-identical to base — confirmed unchanged, present only as diff context, never as +/- lines.
- Ran `~/Tools/flutter/bin/flutter test` (pinned SDK 3.41.9) in packages/nears_dls: 1580 tests, 1580 passed, 0 failed. n_appbar_golden_test.dart and n_appbar_test.dart (components) both ran and passed (verified via grep on full log, no FAILED/Exception markers anywhere in the 1582-line log).
Verdict: MET (no regression).
