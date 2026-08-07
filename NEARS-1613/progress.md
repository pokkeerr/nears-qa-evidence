# NEARS-1613 — cycle-2 delta QA progress

Device `emulator-5560` (1080x2340 @420 = 411x891 dp, NOT the 448x997 pool geometry).
Canonical APK md5 `1af5aaae88198092ae9e8b74b990cd37` (built from `git archive 002b87ac`,
SDK /Users/Apple/Tools/flutter 3.41.9, `--dart-define=API_HOST=10.0.2.2:8099`).
Installed base.apk md5 == canonical byte-for-byte.

## AC3 (literal form) — PASS  [observed 07:14-07:22 local]
- APK-CHECK before: MATCH · after: MATCH
- Fault armed on `/api/v1/customer/loyalty-point/transactions` ONLY.
  Positive control: transactions=503, /customer/info=401 passthrough.
- Screen: points card `LOYALTY POINTS / 199` intact (DB 199.000), `Point History`
  header at y=1084, `Something went wrong / Please try again / Retry` BELOW it
  (y=1571-1790). No full-body error.
- Proxy on load: `FAULT 503 .../loyalty-point/transactions` + `PASS 200 /customer/info`.
- Logs: 2 paired `[FAIL]` lines for the transactions endpoint (ApiFailure sentinel,
  path only, no payload/token). No `[FAIL]` for /customer/info.
- Retry tap (fault cleared): customer/info requests = **0**, transactions = **1** (200).
  List rendered 3 rows (-1, -50, +250) == DB rows id 7/6/1. Points card still 199.
  0 `[FAIL]`/`[ERR]` after recovery.
- Evidence: cycle2-ac3-list-fail-profile-ok.png

## AC1 (screen-level) — PASS  [observed 07:19-07:21 local]
- APK-CHECK before: MATCH · after render: MATCH · after recovery: MATCH
- Fault armed on `/api/v1/customer/info` ONLY. Positive control: info=503,
  config=200 (splash boots), transactions=401 (not faulted).
- Cold start (force-stop + relaunch, login persisted) => ProfileController fresh,
  `userInfoModel` genuinely null. This is the only way the compound guard can fire:
  `getUserInfo()` sets `_userInfoLoadFailed=true` but never nulls `_userInfoModel`.
- Loyalty screen: full-body NearsErrorRetry -- `Something went wrong` (y=1306),
  `Please try again` (y=1386), `Retry` (y=1526). No points card, no Point History.
  16 labelled-tree nodes vs 24-25 healthy => whole body replaced.
- NOT a skeleton at any wait length: identical tree at T+8s and T+35s.
- Visual (1 sanctioned image read): navy #000080 app bar, grey disc + navy cloud-off
  icon, mint #00FF99 full-width Retry with navy label. Light mode.
- Proxy: `/customer/info` FAULT 503 x3 while transactions returned PASS 200 --
  proves the full-body error is driven by the null profile, not the list.
- Logs: 2 paired `[FAIL]` lines for /customer/info (ApiFailure sentinel, path only).
- Recovery (fault cleared, Retry tapped): exactly 1 `/customer/info` 200 + 1
  transactions 200; app pid 10319 unchanged => SAME SESSION, no restart.
  Points card 199 + all 3 history rows rendered. 0 `[FAIL]`/`[ERR]`.
- Evidence: cycle2-ac1-fullbody-error.png

## DB integrity
Read-only throughout (SELECT/SHOW only). Baseline re-verified unchanged at end:
user 3 loyalty_point=199.000, wallet_balance=151.000, 3 loyalty transactions.

