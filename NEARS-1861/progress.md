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
