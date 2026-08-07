# NEARS-1607 QA progress

worktree: /Users/Apple/Projects/nears-NEARS-1607-splash-dls
branch: feat/NEARS-1607-splash-dls HEAD 560f4767
device: emulator-5554 (lock acquired)

## Static + test evidence
- AC1 grep LinearProgressIndicator = 0; NSpinner = 1 (confirmed at HEAD)
- AC2 grep SnackBar( = 0, showSnackBar = 0, ScaffoldMessenger = 0; NSnackBar = 1
- AC7 git diff --stat base..HEAD -- no_internet_screen.dart = EMPTY (zero changes)
- unit: splash_screen_dls_test.dart 13 pass; splash_location_prefetch_order_test.dart 6 pass
- MUTATION PROOF AC4: moving unawaited(_prefetchDeviceLocation()) after await _fetchConfigData -> 5/6 order tests RED. Instrument falsifiable. Tree reverted clean.

## Build freshness (PROVEN)
- device /data/app/.../base.apk md5 = 178ea3c42e9742d9796a272c358b4b70
- local  UserApp/build/app/outputs/flutter-apk/app-debug.apk md5 = 178ea3c42e9742d9796a272c358b4b70  (IDENTICAL)
- that APK's assets/flutter_assets/kernel_blob.bin contains "splash: location prefetch initiated" (x2),
  "splash: location prefetch skipped (permission not granted)" (x2), "splash: routing" (x2) -- strings introduced by THIS diff
- running pid emitted those exact lines at runtime

## Live results so far (emulator-5554, light mode, en)
- AC4 PASS (2 instruments):
  flutter run console, cold start #1 (perm NOT granted):
    [INFO] msg="splash: location prefetch initiated"  ->  [INFO] msg="splash: routing"
  adb logcat w/ timestamps, cold start #2 (perm GRANTED):
    05:09:54.453 splash: location prefetch initiated
    05:09:58.847 splash: routing                      (+4.394s AFTER initiation)
    05:10:04.193 splash: location prefetch completed   (+5.346s AFTER routing -> non-blocking)
  cold start #3 (perm granted): 05:14:39.838 initiated -> 05:14:41.885 routing -> 05:14:49.548 completed
- AC1 PASS: device-side frame capture f13-f16 -> bg #fcf9f8 (surfaceBg), navy #000080 brand lockup
  (y1304-1394) + a SEPARATE 92-100px (=32dp @ density 480/scale 3.0) navy #000080 element centred at
  cx=666..670 (screen centre 672) whose pixel count VARIES per frame (517/29/337/337) = animating ring.
  Not a bar. Visual read confirms circular arc spinner. exact hex #000080 = navy, not mint.
- AC5(c) PASS: fresh install cold start -> Choose Your Language -> Next -> onboarding ("Get Favorite Items")
- AC5(b) PASS: cold start w/ saved address -> dashboard (header "F93G+HW4 - Al Manhal - W15 01")
- AC6 (permission-denied half) PASS: cold start #1 logged
  'splash: location prefetch skipped (permission not granted)', NO OS dialog, routed onward normally
- logs: zero [ERR]/[FAIL] on all cold starts

## BASE A/B (same device emulator-5554, same scenario) -- SETTLES TWO SUSPECTED DEFECTS
Base APK built from 27c6bf2a; identity proven: kernel_blob.bin contains ZERO occurrences of
"splash: location prefetch initiated" / "splash: routing". Installed md5 dcc4dfc6... (HEAD is 178ea3c4...).

Scenario: onboarded, NO saved address, location permission REVOKED, cold start.
| build | outcome |
|---|---|
| BASE dcc4dfc6 | stays on splash indefinitely (empty a11y tree; #fcf9f8 + navy lockup) |
| HEAD 178ea3c4 | stays on splash indefinitely ("Loading..."/"تحميل..." + #fcf9f8 + navy lockup) |
=> IDENTICAL. The splash stall is PRE-EXISTING (untouched splash_route_helper.dart +
   location_controller.dart: `_checkPermission` early-returns on `!hasInternet`). NOT a regression
   of NEARS-1607. -> regression_bugs.

Arabic brand lockup (RTL), navy #000080 cluster in the lockup band:
| build/locale | x-range | width | px |
|---|---|---|---|
| BASE ar | 408-476 | 68 | 970 |
| HEAD ar | 408-476 | 68 | 970 |
| HEAD en | 408-756 | 348 | 2774 |
=> Arabic lockup renders PIN-ONLY (no "Nears" wordmark) IDENTICALLY at base and HEAD (same 970 px).
   PRE-EXISTING RTL asset defect; SvgPicture line untouched by this diff. -> regression_bugs.
   AC8's actual requirement ("lockup is NOT mirrored") is MET: mint pin-dot at x 428-456 (centre 442)
   in BOTH en and ar -- the pin stays on the left, no mirroring.

## Toasts (AC2/AC3/AC8)
- en success: "Connected", mint #00ff99 check glyph LEFT of text, NToast pill on #00003c  (uiautomator text + pixels)
- en error:   "No internet connection", #ffb4ab X glyph LEFT of text
- ar success: "متصل", mint check glyph RIGHT of text (RTL flip correct)
- ar error:   "لا يوجد اتصال بالإنترنت", #ffb4ab X glyph RIGHT of text (RTL flip correct)
- all four are the DLS NToast pill, NOT a Material SnackBar

## AC6
- services OFF: 'splash: location prefetch skipped (services off)' -> routing -> route: initial route. No dialog, no toast, zero [ERR]/[FAIL].
- permission revoked: 'splash: location prefetch skipped (permission not granted)' -> routing. No dialog.
