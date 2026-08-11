# NEARS-1877 — live QA progress log

`RouteHelper.getRoute()` null-asserted `configModel` in the page builder, so a cold deep-link
red-screened. The fix returns a `_ConfigGate` when config is null.

## Builds under test

| Build | Commit | APK md5 | Device |
|---|---|---|---|
| BASE (unfixed) | fork point `c3960291` (2 lib files restored via `git show`) | `bc2378d757557e2a9d593827f1198860` | `emulator-5560` |
| HEAD (fixed) — session 1, measurement not completed | `dd239138` | `4e26fed26dced0b4137cacb2e032f256` | `emulator-5560` |
| HEAD (fixed) — session 2, **the measured one** | `dd239138`, tree clean | `802249a7631bacd1791540dbcccfd12b` | `emulator-5560` |

Session 2 rebuilt from the worktree at `dd239138` (`DIRTY=0`) and re-verified the md5 **on device**
(`pm path` → `md5sum` = `802249a7…`, matching the host artifact). The APK sitting in `build/` at
resume was a stale 06:07 artifact (`43864f1e…`) and was NOT used.

Flutter `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9 (pinned). Both `flutter build apk --debug`
from worktree `/Users/Apple/Projects/nears-NEARS-1877-getroute-config-gate`.
Backend: local `php artisan serve :8000`; app `baseUrl=http://10.0.2.2:8000`.
Geometry 1344x2992 @480dpi = 448x997 dp.

**Same-command fix-absence proof** for the BASE build: `grep -c _ConfigGate route_helper.dart` = 0 and
`grep -c config_fetch_threw splash_controller.dart` = 0, printed in the *same command* as the build.
Both APK md5s re-verified on-device before AND after each 30-attempt run — unchanged.
`firstInstallTime` (2026-08-08) != `lastUpdateTime` (05:33:43 BASE / 05:47:42 HEAD) on both.

## Instrument validity — PIXEL DETECTION ONLY

Log silence is **not** evidence on this surface (NEARS-1860, open). Controls, measured this run:

- **Positive control 0.968** on the known red screen `NEARS-1776/bug-base-redscreen-null-check-deeplink.png`;
  **0.992** on this run's own live red captures.
- **Negative control 0.000** on a normal rendered home screen (`warm2.png`, app logged in, zone Abu Dhabi).
- **Threshold 0.5.**

**NEARS-1860 reconfirmed first-hand:** across 30 BASE attempts that each produced a full-screen red
`ErrorWidget` at red-fraction 0.992, **0/30 produced any `[FAIL]`/`[ERR]`/`Null check`/`Exception`
line in `logcat -s flutter`.** Three instruments report clean during a full-screen crash.

## Repro recipe (per attempt) — reused verbatim from NEARS-1776

1. `am force-stop com.izzes.nears`
2. `run-as com.izzes.nears rm -f app_flutter/cache_response_new_db.sqlite` (surgical config-cache
   miss; keeps login + address, avoids the `pm clear` validity trap)
3. `logcat -c`
4. `am start -a VIEW -c BROWSABLE -p com.izzes.nears -d 'https://6ammart-web.6amtech.com/store/demo-store?id=1&page=store&module=grocery-food'`
5. wait 22 s → raw `screencap` → red-fraction detector; `logcat -d -s flutter`

Strictly sequential, ONE device — two devices against one single-threaded `php artisan serve`
serialise requests and fake clean attempts.

## AC1 — measured result

| Build | attempts | navigated to store route | config 200 afterwards | RED screens | rate |
|---|---|---|---|---|---|
| BASE `c3960291` (unfixed) | 30 | 30/30 | 30/30 | **30** | **100 %** |
| HEAD `dd239138` (fixed) — run A | 30 | 27/30 | 26/30 | **0** | **0 %** |
| HEAD `dd239138` (fixed) — run B (probe) | 12 | 12/12 | 12/12 | **0** | **0 %** |

**42 cold attempts on the fixed build produced zero red screens.** Max red-fraction observed
`0.030` against a threshold of `0.5`; the positive control on the same detector is `0.968`.
Zero `[FAIL]`/`[ERR]`/`Null check operator` lines across all 42 logs.

The measured BASE rate is 100 %, slightly above the ticket's 29/30 comparator on `5ab0de66` —
the surgical cache-miss makes the null window deterministic.

### "Not red" is not "arrived" — the frames were classified, not assumed

A blank frame and a stranded spinner are also not red, so every frame was fingerprinted rather
than counted as a pass on red-absence alone. Run A's 30 frames fell into three clusters:

- 23 frames — the fully rendered store screen (~352 colour buckets).
- 4 frames (6, 18, 26, 30) — the store screen caught **mid-load**; `analytics: view_store
  {store_id: 1}` had already fired in each, so these are arrivals, not strands.
- 3 frames (25, 27, 29) — the app was still in **cold start** at the 22 s mark (attempt 27 logged
  `app_open` 19 s after process start; the emulator degraded late in the run). The deep link had
  not been processed yet, so these observe the property **neither way**. Not failures, not passes.

Run B settled it: sampling at **22 s and again at 45 s** with a11y text captured at both,
**12/12 reached the store screen with real content** (`Mango`, `10% OFF`, `21 AED`), including one
attempt still blank at 22 s that had arrived by 45 s. Slow start, not a terminal state.

### Positive on-device proof that the fix was the code under test

`route: config gate kicking config fetch` — a string that exists only in the `_ConfigGate` added by
this branch — appears in **42 of 42** attempt logs. The gate was genuinely on the path every time
and the outcome was the store screen. Stronger attribution than the md5 alone, which only proves
which file was installed.

## AC2 — non-store `getRoute` entry

Cold deep-link to `/refer-and-earn?code=QA1877` (funnels through `getRoute(byPuss: true, …)`, a
different `_configuredRoute` branch than the store path). Gate engaged, `ReferAndEarnScreen`
rendered ("Invite your friends & businesses", "Copy"). red-fraction `0.001`, no `[FAIL]`, no
`Null check`.

## AC3 — a config failure must not strand the user

The dev backend is **shared with live peer QA sessions**, so it was NOT stopped. The backend was
made unreachable **device-side only** (airplane mode) — the solution doc explicitly allows "or the
config endpoint unreachable".

| Kind | Copy rendered | How reached |
|---|---|---|
| `noInternet` | "No internet connection" / "Oops!" / "Try Again" | airplane mode, cold deep-link |
| `generic` | "Sorry, something went wrong" | **live corrupt cache row** (`f1-live-corrupt-cache-failure.log`) |
| `timeout` | not live-triggered | see caveat below |

- **Retry recovers.** Network restored → one Retry tap → store screen fully rendered.
- **Double-tap fires ONE fetch.** The first attempt via the label driver was invalid — its two taps
  landed 2.5 s apart (driver latency), which never races the latch. Repeated with both taps in a
  single shell round-trip during a genuine ~0.8 s in-flight window: **2 taps → exactly 1
  `GET /api/v1/config`** (exact-match count; a naive grep over-counts because `/api/v1/config` is a
  prefix of `/api/v1/config/geocode-api`).
- **Caveat, stated not hidden:** the `timeout` arm was not live-triggered. It shares one
  compile-time-exhaustive switch with the two arms that were demonstrated.

## Warm path (36 routes funnel through this helper)

- **Structural, verified first-hand:** `_configModel` is assigned at exactly **one** site and is
  never reset to null, so once config lands `_ConfigGate` is never constructed again. The diff is
  **862 insertions / 0 deletions** — the original body became `_configuredRoute` by inserting a
  function header above it, so the warm path is byte-identical logic behind one non-null check.
- **Live:** across warm in-app navigation and a warm store deep-link, **0 gate constructions,
  0 errors, 0 RenderFlex overflows**, and the store rendered directly with no spinner flicker.

## Force-update and maintenance gates still fire

Both gates live inside `_configuredRoute`, the **only** exit from the gate — `_ConfigGate` returns
`_configuredRoute(...)`, never `navigateTo` directly. A deep link cannot walk past them. Unit pin
`maintenance mode returns UpdateScreen(isUpdate: false)` is green. **A live flip was NOT performed**
— it would require writing `maintenance_mode` / `app_minimum_version_android` in `business_settings`,
and QA is read-only on the DB.

## UX review's three device-only items

1. **Un-clipped, centred, correct background in a pushed route** — 0 overflow errors; all four
   corners *and* centre measure `(252,249,248)` = `NearsTokens.surfaceBg` `0xFFFCF9F8`, an opaque
   full-bleed page background, checked against the token source rather than assumed. Visual
   confirmation: icon, headline, subtext and CTA centred, nothing cut off, navy icon + mint CTA.
2. **No double-frame flash under real latency** — the gate's loading and failure states both paint
   `surfaceBg`; the destination body measures `(251,251,253)`, a delta of `(1,2,5)`. Under an 800 ms
   induced per-packet latency the observed progression was launch → splash → transition → store,
   with no theme discontinuity. **Honest limit:** `screencap` cadence (~1 s) cannot resolve a single
   frame, so what is verified is the *mechanism* the reviewer worried about (background mismatch),
   not a frame-by-frame capture.
3. **RTL / Arabic** — `NEmptyState`'s first mid-route appearance renders correctly in `ar`:
   "أُووبس!" / "لا يوجد اتصال بالإنترنت" / "حاول ثانية", right-to-left, un-clipped, correct tokens.

## Automated backstop

`flutter test` (UserApp, `dd239138`, tree clean): **+3471 ~2 -4**, matching the engineer's recorded
HEAD figure. The 4 failures are `category_screen_back_button` ×1 and `coupon_controller` ×3,
confirmed by running those two files directly (`-4`, accounting for all four). **Neither file touches
`route_helper.dart` or `splash_controller.dart`** — that is the honest check, rather than comparing
failure names at an identical count. Changed-surface pins 20/20 green (including the maintenance-mode
pin); the NEARS-1776 pin is green.

**Race timing, read off attempt 3's log:** route built at `05:36:29.906`
("deep link: navigating to store route"), `GET /api/v1/config` dispatched `05:36:30.080`,
`http_status=200` only at `05:36:31.000` — a ~1.1 s window in which `getRoute` dereferenced a
null config.
