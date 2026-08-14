# NEARS-1526 QA evidence — Wallet PopScope `didPop` guard

Worktree `/Users/Apple/Projects/nears-NEARS-1526-wallet-pop-guard`, branch
`fix/NEARS-1526-wallet-pop-guard`, commit `8aa4295e` (base `25ab3769`).
Device: **emulator-5558** (`sdk_gphone16k_arm64`, Android 16, gestural nav).
Flutter SDK: **3.41.9** (pinned, `/Users/Apple/Tools/flutter`).

**Entry mechanism (stated, because it is part of the evidence):** real FCM push via
`Helpers::send_push_notif_to_device($token, ['type' => 'add_fund', ...])` from
`php artisan tinker` in the PRIMARY `Admin/` tree; `$token` read read-only from
`users.cm_firebase_token`. Backend returned `send_result=true` on all three sends.
Foreground `onMessage` -> local notification -> tap ->
`Get.toNamed(RouteHelper.getWalletRoute(fromNotification: true))`.
**No DB write was made by QA.**

## Build modes

| leg | build | why |
|---|---|---|
| P1 / P2 primary | **release** (`flutter build apk --release` + `adb install -r`) | the only mode where the real user-facing outcome (cleared stack) is observable; `Navigator._debugLocked` asserts are compiled out |
| P3 second leg | **debug** (`flutter run --debug`) | the only mode where the `AppLogger` console channel (`if (kDebugMode)`) is live, so the logs-first gate has teeth |

## Pins

| pin | build | result | evidence |
|---|---|---|---|
| P1 — BACK from notification-Wallet lands on the screen the user was on | release | **PASS** — Order Details #164, not Home | p1-01, p1-02, p1-03 |
| P1 — same | debug | **PASS** — Order Details #164 | p3-debug-01, p3-debug-02 |
| P2 — a second BACK continues normal back-navigation | release | **PASS** — My Orders; app alive (pid 5605) | p2-01 |
| P2 — same | debug | **PASS** — My Orders; app alive (pid 9198) | (a11y dump) |
| P4 — repro does not depend on `trackOrder` polling | release | **PASS** — Settings (no polling) beneath Wallet, back-gesture returned to Settings | reg3-02 |

**Positive control that `fromNotification` really was `true`** (this run, same entry):
the Wallet app-bar arrow from that same screen went to **Home** — the branch that only
executes when `widget.fromNotification == true`. See `control-appbar-back-goes-home.png`.
Without this the P1 pass would be unfalsifiable.

## Regression sweep

| # | check | result | evidence |
|---|---|---|---|
| 1 | Wallet reached normally (Profile -> My Wallet, `fromNotification:false`), BACK | PASS — returns to Profile | reg1-01, reg1-02 |
| 2 | Wallet via post-payment return (`fundStatus`) | **NOT_RUN** — needs a completed digital payment; the `Gateways` nwidart module is absent by design | reg2-01 |
| 3 | RTL/Arabic swipe-back on notification-Wallet | PASS — behaves as system BACK, returns to Settings | reg3-01, reg3-02 |
| 4 | Wallet renders (balance / add fund / transaction history) | PASS — 25 AED, Add Fund, Filter, 2 transactions with dates | reg4-01 |

## Logs

- **debug leg (sensitive):** 931-line run log, **183** `[NET]`/`[INFO]` AppLogger lines
  present (channel-alive positive control), **0** matches for
  `[FAIL]` / `[ERR]` / `EXCEPTION CAUGHT` / `Failed assertion` / `_debugLocked` / `overflowed by`.
- **release leg (insensitive by design):** `AppLogger` console output is `if (kDebugMode)` and
  is compiled out; `ui_errors` 0 matches, no `AndroidRuntime` crash from the app process.

## Automated backstop (re-run on the committed bytes)

- `flutter test test/features/wallet/` -> **74/74 passed**
- `flutter test` (full UserApp) -> **3852 passed, 2 skipped, 0 failed**
