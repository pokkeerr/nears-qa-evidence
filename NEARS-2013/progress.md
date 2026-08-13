# NEARS-2013 — live QA evidence log

Device `emulator-5556` (Pixel_10_Pro_2, lock held for NEARS-2013). Light mode only
(dark deferred). Build type: **debug APK** (`flutter build apk --debug`), installed
with `adb install -r` and launched with `am start` — no attached Flutter client.

## Builds under test (stale-APK ruled out by APK CONTENT HASH, not timestamps alone)

| half | source tree | local APK md5 | on-device md5 (`pm path` + `md5sum`) | match |
|---|---|---|---|---|
| RED (pre-fix) | `/Users/Apple/Projects/nears-NEARS-2013-BASE-redhalf/UserApp` @ detached `12b1bcb2` | `442e1662ab1dad026492aa3c959c4872` | `442e1662ab1dad026492aa3c959c4872` | yes |
| GREEN (fixed) | `/Users/Apple/Projects/nears-NEARS-2013-category-fetch-error/UserApp` @ `893a054e` | `18e925cdb8b0226871aa1f89fd56247e` | `18e925cdb8b0226871aa1f89fd56247e` | yes |

Both also show `firstInstallTime` (2026-08-11 05:56:53) != `lastUpdateTime`
(03:04:52 red / 03:28:49 green). Source control: `categoryListFetchFailed` appears
0x in the BASE tree's controller+screen and 6x/1x in the fixed tree's.

## Induction

Airplane mode / `svc wifi disable` CANNOT reach this defect — see finding below.
Used a host-side selective fault injector on port **8001** (a separate process; the
shared `php artisan serve` on :8000 is never touched, so no peer lane is affected),
with both APKs built `--dart-define=API_HOST=10.0.2.2:8001`.

Injector control pair, re-measured at each use:

- `PASS`  — `/api/v1/categories` 200; `/home/all` `categories` slice = list(5)
- `FAIL`  — `/api/v1/categories` connection dropped (000); `/home/all` still 200 with
  banners/campaigns/popular_stores/latest_stores/recommended_stores intact but its
  `categories` slice nulled; `/api/v1/config` still 200 (proves selective, not dead)
- `DELAY` — `/api/v1/categories` 200 after 25.1s (measured)

Cold cache reached by `pm clear` + testing on a module whose `/categories` had never
succeeded (the cache key is `categoryUri + moduleId`), reached via an in-app module
switch (`switchModule` -> `clearCategoryList()`).

## Results

| item | result | evidence |
|---|---|---|
| RED: pre-fix shimmer | endless | `red-01`, `red-02` — 34 nodes/6 labelled, no error copy, still animating at T+246s |
| AC1 fixed | PASS | `green-01` — "Something went wrong"/"Please try again"/"Retry", static (3 identical frames) |
| AC2 retry | PASS | `green-02` — rail + grid both load after a real re-fetch |
| R1 empty list | PASS | "No category found", not the error state |
| R4 module switch | PASS | shimmer during in-flight window, 0 stale-error matches |
| R5 Arabic/RTL | PASS | `green-03` — حدث خطأ ما / يرجى المحاولة مرة أخرى / أعد المحاولة, nav mirrored |
| R3a Home | PASS | renders normally under the same failure |
| R3b store_screen | see note | `note-02` — full-page shimmer with the injector OFF; unattributed |
