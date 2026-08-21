# NEARS-2316 QA-lite evidence

## Environment note
The spawn-provided worktree path
`/Users/Apple/Projects/nears-NEARS-2316-attachment-viewer-test-fix` does NOT exist on disk
(confirmed via `git worktree list` — no such entry, no branch
`feat/NEARS-2316-attachment-viewer-test-fix` in `git branch -a`). Git history shows
NEARS-2316's fix commits (`b05a5c8b`, merge `2c33ca01`, ledger-close `c66c12c3`) are already
merged into `feat/userapp-reskin2` (current primary tree HEAD `e048eea8`, worktree apparently
already reaped post-merge). Verification below was run live against that merged state in
`/Users/Apple/Projects/nears/UserApp`, which contains byte-identical fixed content
(confirmed: no `isRightMessage` in test file, `InkWell.at(4)`/`currentIndex 3` present,
`git show --stat b05a5c8b` / merge diff both show only the test file touched).

## AC1/2 - flutter test loads and passes
`~/Tools/flutter/bin/flutter test test/features/chat/attachment_viewer_dls_test.dart --reporter expanded`
Result: 32 visible tests, 30 pass, 2 fail (pre-existing, see below). Matches engineer's report exactly.
File LOADS (not a load-failure) - "loading ... attachment_viewer_dls_test.dart" then individual
test names stream, confirming >0 tests visible.

## AC3 - target test passes, isolation confirmed
Full run: "AC4 — lightbox entry and exit the desktop Dialog branch forwards the tapped index" -
counter advanced +8 -> +9 cleanly, no [E] marker = PASS.
Isolated run: `flutter test ... --plain-name "the desktop Dialog branch forwards the tapped index"`
-> "00:00 +1: All tests passed!" Not order-dependent.

## AC4 - flutter analyze zero undefined_named_parameter for target files
`~/Tools/flutter/bin/flutter analyze UserApp` filtered for undefined_named_parameter /
image_file_view_widget.dart / attachment_viewer_dls_test.dart: all matches are in
`UserApp/build/ios/SourcePackages/firebase_*` (vendored SDK build artifacts) - ZERO findings
in the two target files.

## AC5 - diff scope
`git show --stat b05a5c8b` and `git diff 32d8d09d..2c33ca01 --stat` (fix commit's own base..merge):
both show exactly ONE file changed - attachment_viewer_dls_test.dart, 9 insertions(+) 6 deletions(-).
No drift into image_file_view_widget.dart or image_file_view_overlay_test.dart.

## regression-candidate: disabledColor vs onSurfaceVariant drift (pre-existing, NOT NEARS-2316)
Two failures, both TestFailure assertion mismatches (not compile errors):
- "AC1 — thumbnail typography the PDF caption paints labelMd in disabledColor" (line 211,
  via `_expectToken`)
- "D2 — thumbnail glyphs on NIcon pdf / video / other tiles render NIcon, no raw Material Icon"
  (line 451)
Both: Expected Color(0.6196,0.6196,0.6196) [= kDisabled 0xFF9E9E9E, test fixture] vs
Actual Color(0.2863,0.2706,0.3098) [= colorScheme.onSurfaceVariant].
Confirmed root cause in lib/features/chat/widgets/image_file_view_widget.dart lines 65/69/72:
line 65 still reads `Theme.of(context).disabledColor` (background tint) but lines 69/72 read
`Theme.of(context).colorScheme.onSurfaceVariant` (icon + label color) - test fixtures
(kDisabled, line 39/324/410 in test file) were never updated for that split. Traced to
commit 1dcdbccf "fix(NEARS-1920): replace disabledColor with onSurfaceVariant for readable
text sites" via `git log -1 -- lib/features/chat/widgets/image_file_view_widget.dart`.
NOT part of NEARS-2316's AC1-3 scope; both fail identically before and after NEARS-2316's
fix (NEARS-2316 never touched these lines/assertions).

## Verdict: PASS
task_bugs: none. regression_bugs: 1 (see above), routed for separate ticket, not blocking
NEARS-2316.
