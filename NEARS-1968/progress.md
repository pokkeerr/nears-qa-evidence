# NEARS-1968 — QA progress (fix-cycle 1)

Device `emulator-5558` · UserApp **debug** · light mode · logged out (Guest User)
Worktree `/Users/Apple/Projects/nears-NEARS-1968-snackbar-live-region` @ `cfa1afce`

| # | AC | Result | Evidence |
|---|----|--------|----------|
| AC1 | GetX path — text present in the Android a11y tree at BASE? | **PREMISE FALSIFIED** — present at base | `measurements.log` §AC1, `ac1-getx-toast-BASE.png` |
| AC1 | ScaffoldMessenger path — text present at BASE? | **PREMISE FALSIFIED** — present at base, already a live region | `measurements.log` §AC1 |
| AC2 | GetX toast announces under TalkBack, exactly once | **MET** — base 0 utterances / fix 1 utterance, control live both runs | `measurements.log` §AC2, `ac1-getx-toast-fix.png` |

Regression sweep: ScaffoldMessenger unchanged (1 toast → 1 utterance, one live
region, one focus stop) · NEARS-1501 Scaffold-less no-internet fallback OK ·
zero visual change (identical pill bbox + colour) · RTL/Arabic OK.

Automated: `flutter test` on the two snackbar suites → +8 all passed.
