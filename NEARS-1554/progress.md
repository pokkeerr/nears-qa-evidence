# NEARS-1554 — QA progress log (live checkpoint)

## Build identity (established BEFORE any observation)
| build | tree | commit | APK md5 |
|---|---|---|---|
| PRE-FIX | /Users/Apple/Projects/nears-qa-1554-prefix (detached) | 49dc8961 | 07bdcfd720c14007f7d3c7802038e9a2 |
| POST-FIX | /Users/Apple/Projects/nears-NEARS-1554-campaign-nullguard | eb3fe6b0 | 352f54904aae77c2d4c5e24c5d1c10cc |

md5s differ. Content probe (kernel_blob.bin, occurrence counts via `grep -oa`):

| probe | pre | post | verdict |
|---|---|---|---|
| `module!.id!}` (pre-fix operator) | 6 | 4 | **-2** = the two fixed lines |
| `module?.id}` (post-fix operator) | 6 | 8 | **+2** = the two fixed lines |
| comment `module can go null mid-flight` | 0 | 1 | fix-only |
| comment `same null-module window` | 0 | 1 | fix-only |
| POSITIVE CONTROL `basicCampaignUri` | 5 | 5 | probe can find things |
| NEGATIVE CONTROL `zzzNotInAnyBuildzzz` | 0 | 0 | probe does not hallucinate |
| provenance `nears-qa-1554-prefix` path | 1119 | 0 | correct tree |
| provenance `nears-NEARS-1554-...` path | 0 | 1119 | correct tree |

## PREDICTION — recorded BEFORE the live repro is executed
**PRE-FIX build, steps 1-5:** on Android back during an in-flight `refreshHomeData`
fan-out, `removeModule()` sets module null; the stale guard at home_controller.dart:276
has already passed, so the unawaited `getBasicCampaignList(true)` (hc:305) and the
awaited `getItemCampaignList(true)` (inside the Future.wait) reach the repository and
throw `_TypeError: Null check operator used on a null value` at
campaign_repository.dart:25 / :39. Nothing in CampaignController / CampaignService /
CampaignRepository catches it (verified by grep: zero try/catch in the chain), so it
reaches `PlatformDispatcher.onError` -> `handleUncaughtAsyncError` (main.dart:111) and
prints `[FAIL] ... type=UncaughtAsyncError`, booked NON-FATAL (returns true).
Expected: **no red screen, no process death**, campaign rails silently skip the refresh.

**POST-FIX build, identical steps:** no `_TypeError`, no `UncaughtAsyncError` line
naming campaign_repository.dart; the cacheId simply interpolates the literal `null`
and the fetch proceeds.

Validity requirement: the same capture window must show a NON-ZERO count of
flutter-tag log lines, else the instrument is broken and absence proves nothing.

## Preconditions verified live (backend up, HTTP 200)
- `config.module` = None -> the back-button `removeModule()` branch is reachable. OK
- zone 1 module list = 5 modules -> `moduleList.length != 1` satisfied. OK
- baseUrl = `http://10.0.2.2:8000` (real local backend, not a demo host). OK
- 6 active modules in DB (Food id=2 present; Food/Shop mount the campaign views). OK

## Automated backstop (device-free) — COMPLETE
- POST-FIX `campaign_repository_module_null_cache_test.dart`: **6/6 PASS**.
- FALSIFIABILITY CONTROL (same test copied into the PRE-FIX tree, run, then deleted;
  never committed): **5 of 6 FAIL** with `Null check operator used on a null value` at
  campaign_repository.dart **25:104**, **25:100**, **39:93** — the exact lines the
  ticket names. T6 (happy path, valid module id) **PASSES on pre-fix too**, proving the
  suite is not trivially red and that the happy path was never broken.

## Device pool state at run time (differs from the brief — see report)
- emulator-5556 LOCKED live by NEARS-1749 (pid 28462)
- emulator-5558 LOCKED live by NEARS-1718 (pid 86430)
- emulator-5562 LOCKED live by NEARS-1749 (pid 28462)
- emulator-5554 free but 627,704 KB; after reclaiming its stale UserApp install
  815,140 KB, after cache trim 815,992 KB — still **3,208 KB below the 819,200 KB
  floor**, so NOT acquired.

## RESULT — predicted vs actual

**AC1 — PASS.** Prediction was met exactly, and better than expected: the log carries a
real stack frame.

PRE-FIX (emulator-5556, installed md5 07bdcfd720c14007f7d3c7802038e9a2):
- CONTROL (pull-to-refresh, NO back): validity 29 flutter-tag lines / 28 [NET]; **0 [FAIL]**.
- REPRO (pull-to-refresh THEN Android back during the fan-out): validity 58 flutter-tag
  lines / 32 [NET]; **1 [FAIL]**:
  `[FAIL] endpoint=null http_status=null type=UncaughtAsyncError msg="uncaught async error (_TypeError)"`
  with the adjacent record:
  `#0 CampaignRepository._getBasicCampaignList (campaign_repository.dart:25:100)`
  `#1 CampaignRepository.getList (campaign_repository.dart:18:20)`
- App PID unchanged across the error, screen = sector picker, no red screen. Non-fatal, as stated.

POST-FIX (emulator-5562, installed md5 352f54904aae77c2d4c5e24c5d1c10cc), identical steps:
validity 35 flutter-tag lines / 34 [NET]; [FAIL]=0, UncaughtAsyncError=0, _TypeError=0,
campaign_repository frames=0.

**The absence is not vacuous** — the ordered [NET] timelines are identical for 15 steps,
including steps 13-15 (`/banners`, `/module`, `/stores/get-stores/all`) which are exactly
the calls `removeModule()` fires, proving module WAS null at that point. They diverge only
at step 16: PRE-FIX emits the [FAIL]; POST-FIX emits
`[NET] GET /api/v1/campaigns/basic -> http_status=200`. The previously-throwing line
provably executed and succeeded.

**AC2 — PASS (with a scoped unverifiable, see below).**
- Full-page section-header union on Food home is **identical** on both builds (10/10).
  An apparent "Most Popular Items" difference was chased down and proved to be scroll
  offset from differing screen heights, not a regression.
- Cache continuity: post-fix installed OVER pre-fix app data, cold start -> campaigns/*
  network calls = 0 on BOTH builds (cache HIT both times). cacheId unchanged for a
  non-null id; no one-time empty rail.
- Regression sweep (3 modules x enter/refresh/back): 213 flutter-tag lines scanned,
  24 campaign fetches all HTTP 200, 0 [FAIL]/[ERR]/exception/overflow.

## Populated-rail render — UNVERIFIABLE in this environment (data/mount gap, pre-existing)
- `MiddleSectionBannerView` (basic-campaign carousel) is mounted **only** in
  `shop_home_screen.dart`; no active module has module_type ecommerce/shop
  (seed types: grocery/food/pharmacy/parcel) -> Shop home is unreachable.
- Item campaigns are **empty for every zone x module** probed (6 combinations) ->
  `JustForYouView` correctly renders nothing (`just_for_you_view.dart:22` empty guard),
  so the "view all campaigns" screen has **no UI entry point**.
- Not caused by this ticket; not a regression. Reported as followups, DB left read-only.
