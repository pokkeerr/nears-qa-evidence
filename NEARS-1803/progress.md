# NEARS-1803 — live QA progress log (phase [8], fix_cycle 0)

Worktree `/Users/Apple/Projects/nears-NEARS-1803-wallet-page-size`, branch
`feat/NEARS-1803-wallet-page-size`, HEAD `e6b9f8e0` (base `713b701e`).
Device `emulator-5558` (lock held for NEARS-1803). Account `michael.brown@demo.com`
(`users.id=3`). SDK `/Users/Apple/Tools/flutter` 3.41.9. Light mode only.

## Build freshness (two-stage)
- Stage 1 (pre-filter, md5 of the INSTALLED `com.izzes.nears` artifact):
  pre-install `22296a45abb84b5ad0f78ca76a7e7091` → post-install
  `e5c4d0422d6d35c83af68be6a7e769fd`, identical to the worktree-built
  `UserApp/build/app/outputs/flutter-apk/app-debug.apk`.
- Stage 2 (verdict, LIVE isolate over the Dart VM service): the running kernel's
  script for `wallet_repository.dart` reads
  `'...?offset=$offset&limit=$kWalletPageLimit&type=$sortingType'`, and
  `wallet_controller.dart` reads `int get maxPages => (popularPageSize! / kWalletPageLimit).ceil();`.
  Negative control on the same probe: zero hits for the pre-fix literal `limit=10`
  in that script — the instrument can come out two ways.
  (Expression evaluation `evaluate` is unavailable on this endpoint —
  "No compilation service available" — and a `const int` is inlined, so it has no
  runtime field; the running-kernel script read is the discriminating substitute.)

## Observations
| # | What | Result |
|---|------|--------|
| OBS-0 | Wallet first load, 4 real rows | 4 row nodes, matches DB (`user_id=3` has 4 rows) |
| OBS-A | Pull-to-refresh, wire read via `ext.dart.io` HTTP profile | exactly 2 requests: `wallet/transactions?offset=1&limit=10&type=all` + `customer/info` — no page 2 |
| OBS-B | Scroll to bottom, short list | 0 requests (`maxPages=ceil(4/10)=1`, `canLoadMore=false`) |
| OBS-C | Filter → Converted from Loyalty Point | 1 request `offset=1&limit=10&type=loyalty_point`; 2 rows rendered |
| OBS-D | Filter → All Transactions | 1 request `offset=1&limit=10&type=all`; 4 rows rendered |
| OBS-E | Fault proxy (`total_size` 4→25, rows padded), scroll | `offset=2` then `offset=3` emitted, `offset=4` NEVER; 2× `wallet list: reached end of pagination` |
| OBS-F | Clean build restored (md5 `e5c4d042…`), wallet re-entered | 4 real rows again; Add Fund dialog opens/closes clean |

Logs: `ui_errors` exit 0 (asserted), 44 matches in buffer — **all** from dead
foreign pids 14155/15894 at 18:03, zero from this run's pids (17961 / 20249 / 21051).
