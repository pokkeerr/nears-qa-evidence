# NEARS-1861 — [8] QA progress checkpoint

commit under test: 6cfbfdf532d0b2762ea6ba9f5f6279f2f81c6b6a
base: feat/userapp-reskin2 @ 82bcaae1
fix_cycle: 0 (first pass)  ·  verdict: **BLOCKED** (device pool exhausted)

| AC | status | provenance | evidence |
|----|--------|-----------|----------|
| AC1 null-safe cacheId builders, no throw | **NOT_RUN (live)** / static-confirmed | STATIC only | scan: 7/7 force-unwraps gone, positive control at base = 7. Live repro (pop to sector picker mid fan-out) NOT executed — no device. |
| AC2 comparison sites guarded | **NOT_RUN (live)** / static-confirmed | STATIC only | Both sites read + confirmed non-null-gated, not naive `==`. Wishlist filter + COD webview NOT exercised — no device. |
| AC3 cacheId byte-identical for non-null module | **NOT_RUN (device half)** | inherited from build lane (unit) | Cache-survives-in-place-upgrade check NOT executed — needs a device holding pre-fix cache. THE load-bearing safety claim is device-unverified. |

Live checks NOT executed (all device-gated):
  1. AC1 repro — sector home -> pop to picker mid fan-out, watch logcat for _TypeError
  2. AC3 in-place upgrade cache-hit watch (adb install -r over a pre-fix build)
  3. AC2 wishlist filter still filters (keeps active sector, excludes others)
  4. AC2 COD maximumCodOrderAmount in payment webview [STATIC+DEVICE, no unit pin]
  5. flash-sale rail self-hide on empty sector / backend 500
  6. RTL/Arabic brands + banner rails, empty/error states

Blocker: all 3 pool devices held by live foreign `flutter run` lanes with no lock
files. Detail: bug-device-pool-exhausted.log

## Full first pass — 2026-08-15, emulator-5558, commit 11500328
- AC3 DEVICE (priority leg): PASS. Pre-upgrade baseline 28 cache keys captured on the
  installed PRE-FIX build (v3.8.0, firstInstallTime 2026-08-14). `adb install -r` of the
  fix debug APK preserved app data (firstInstallTime unchanged, login survived).
  Post-install pre-launch: 28/28 identical. After cold open + entering Food (module 2)
  and scrolling all rails: 28/28 keys identical, 0 added, 0 missing, 0 row-id changes,
  0 response rewrites. Rails rendered live data. logcat window 4187 lines / 89
  flutter-tagged / 0 error matches.
- AC1 pre-fix POSITIVE CONTROL captured (ac1-prefix-positive-control.log): the same
  repro threw `Null check operator used on a null value` at
  store_repository.dart:86:128 as UncaughtAsyncError on the pre-fix build.
- AC1 POST-FIX: PASS. 12 mid-flight pop-backs (3 sectors x 4 delays), 232 flutter-tagged
  lines, 0 errors. Same instrument that produced the pre-fix _TypeError.
- RTL/Arabic sweep: PASS. 6 further pop-backs in RTL, 131 flutter lines, 0 errors.
- Suite at 11500328: 4179 real tests, 4177 passed / 2 skipped / 0 failed / 443 suites.
- AC2 wishlist filter: NOT_RUN (Data DoR gap - no unclaimed account has cross-sector
  store favourites; only customer@nears.com has any, single-sector, and it is claimed
  by lane NEARS-1708).
- AC2 payment webview COD cap: NOT_RUN on device (reaching PaymentFailedDialog requires
  placing a real order = a write to the shared dev DB while 2 peer lanes are live).
  STATIC only.
- Flash-sale no-sale sector / backend-500: NOT_RUN (all 3 reachable sectors have an
  active flash sale in this seed; the 500 case needs the guide-9c proxy + a rebuild and
  a cold rail cache).
