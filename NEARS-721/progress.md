# NEARS-721 QA progress — UserApp order-tracking poll crash fix

Build: worktree `nears-NEARS-721-tracking-poll`, branch `fix/NEARS-721-tracking-poll` (uncommitted vs 2b191c42).
Device: emulator-5556 (Android 17). Backend: local dev on :8000. Light mode only (dark deferred).

| AC | Status | Evidence |
|----|--------|----------|
| AC1 no crash + no freeze on transient poll failure | PASS | ac1-baseline-map-render.png, ac1-outage-map-persists.png, ac1-recovered-after-restore.png, ac1-ac5-poll-crash-absence.log — 7 failed ticks, map persisted, no empty-state flip, 200 recovery |
| AC2 genuine not-found still empty | PASS | ac2-genuine-404-contract.log — live 404 `{code:order,message:Not found}`; unchanged empty-state condition; unit test PASS |
| AC3 terminal states render | PASS | ac3-delivered-terminal.png (#154 delivered 200), ac3-canceled-terminal.png (#160 canceled 200) — both non-null, clean logs |
| AC4 automated backstop | PASS | flutter test test/features/order/ = 83 passed incl. new keep-last-model test |
| AC5 no Timer-zone null-check crash | PASS | ac1-ac5-poll-crash-absence.log — "Null check operator" hits = 0; ui_errors clean |

Regression sweep: My Orders list, order tracking (pending/delivered/canceled), login/logout, zone switch — no red screens/crashes.

Regression-candidate (pre-existing, non-blocking): bug-offline-geocode-nosuchmethod.log — cold fully-offline tracking open hangs on spinner via un-null-guarded geocode in LocationRepository; unrelated to this diff.

VERDICT: PASS.
