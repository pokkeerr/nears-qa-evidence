# NEARS-2359 QA-lite [m4] — progress checkpoint

Worktree: /Users/Apple/Projects/nears-NEARS-2359-pdf-tile-disabled-color
Branch: feat/NEARS-2359-pdf-tile-disabled-color
Device-free ticket (pure widget-test verification, no emulator surface).

## Diff scope confirmed
`git diff` on `UserApp/lib/features/chat/widgets/image_file_view_widget.dart`:
exactly 2 lines changed (2 insertions / 2 deletions) — PDF tile `NIcon.data(...)`
color and PDF caption `Text` style color, both reverted from
`Theme.of(context).colorScheme.onSurfaceVariant` to
`Theme.of(context).disabledColor`. Matches conductor-reported scope.

## Test run
`flutter test test/features/chat/attachment_viewer_dls_test.dart --reporter expanded`
Full output: `test-output.log` (this dir).

Result: `+32: All tests passed!` — 0 failures across all 32 cases.

- AC1 case "AC1 — thumbnail typography the PDF caption paints labelMd in
  disabledColor" (case index 0) — PASS. Test asserts `find.text('PDF')` paints
  `NearsText.labelMd` at `color: kDisabled` (source: test lines 313-334,
  `_expectToken(..., color: kDisabled)`).
- D2 case "D2 — thumbnail glyphs on NIcon pdf / video / other tiles render
  NIcon, no raw Material Icon" (case index 4) — PASS. Test table asserts the
  pdf tile's `NIcon.data` glyph (`Symbols.picture_as_pdf`, 34px) resolves to
  `kDisabled` (source: test lines 401-411).
- AC3 (no other tile regressed): read the full expanded output — every other
  case is green, including the adjacent, deliberately-untouched cases in the
  same groups:
  - "the file-extension caption paints labelMd and KEEPS navy" (docx caption,
    asserts `kPrimary`) — PASS, unchanged.
  - "the +N overflow label paints bodyMd" / "...stays white in DARK" (asserts
    `kWhite`) — PASS, unchanged.
  - video/other glyphs in the same D2 table (`Symbols.videocam`/`play_arrow`
    at `kWhite`, etc.) — PASS, unchanged.
  - All NEARS-1731/1732/1874/QA-1/AC2/AC4/AC5/AC7 groups (unrelated surfaces
    sharing the file) — all PASS, no incidental breakage.

`[FAIL] endpoint=null http_status=null type=ChatVideoInitFailure ...` lines
in the log are EXPECTED test output — they are the app's own AppLogger.failure
log lines that the NEARS-1732 video-failure test group asserts exist (paired
failure logging), not flutter-test failures. The suite's own +N counters and
final "All tests passed!" are the authoritative pass/fail signal, not grep on
`FAIL` text.

## Verdict: PASS
