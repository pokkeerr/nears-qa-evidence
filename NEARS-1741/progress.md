# NEARS-1741 — QA[8] live run (fix_cycle 0)

Worktree `/Users/Apple/Projects/nears-NEARS-1741-forget-pass`, branch
`feat/NEARS-1741-forget-pass-states`, HEAD `4d2c7bec` (feat `420c733c`), clean tree.
Device **emulator-5558** (pool), locked. Flutter **3.41.9** (`/Users/Apple/Tools/flutter`).
Build fresh in-worktree; APK md5 **34fa2a7ef282439e1fe18abd90a9ccd8** (local == installed).

## Freshness gate
| when | installed-APK md5 | live-isolate symbol probe |
|---|---|---|
| pre-drive | 34fa2a7e… | PASS (`_submitError` `_submitEpoch` `_submitErrorPanel` `_clearSubmitError` present; neg-control absent) |
| after AC1 loop | 34fa2a7e… | PASS |
| after desktop AC | 34fa2a7e… | PASS |

## Per-AC
| AC | status | evidence |
|---|---|---|
| AC1 recovery affordance | PASS | full loop: fault → panel above CTA (msg + Try Again), field editable, no auto-dismiss at 9s → pass-through → Try Again → Phone Verification |
| AC2 paired AppLogger.failure | PASS | `[FAIL] endpoint=/api/v1/auth/forgot-password http_status=null type=ApiFailure msg="forget-password request failed"` — PII-clean |
| AC3 loading verified + empty-state N/A | PASS | NSpinner in CTA mid-flight (screenshot); N/A recorded, screen owns no collection |
| AC4 NDivider ×2 (TextButton deferred) | PASS | both NDividers visually confirmed on the ≥1300dp branch; `grep -c TextButton` == 2 (accepted) |
| AC5 RTL + ≥44dp + semanticLabel | PASS | Arabic on-device, mirrored layout, Try Again 374×44dp, every clickable node labelled |
| AC6 no behavioral regression | PASS | edit clears panel; back mid-request no crash; empty field inline error; double-tap → 1 panel |
| ≥1300dp desktop branch | PASS | 1400×2400 dp achieved; snackbar fires, panel never renders; geometry reset verified |

Automated: `flutter test` (UserApp, in-worktree) → **+3190 ~2 -6**; all 6 NEARS-1741 tests pass;
the 6 failures are in untouched files (category, coupon ×3, dls_golden ×2).
