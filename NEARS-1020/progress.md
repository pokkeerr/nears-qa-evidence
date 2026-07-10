# NEARS-1020 QA progress (cycle 0)
Device: emulator-5554 | Build: worktree feat/NEARS-1020-splash-integration @ 6eb0a840 (debug APK)
Backend: primary Admin, `php artisan serve :8000` (OTEL_SDK_DISABLED=true — see env note)

## Env note (drift)
Dev backend had ~1.1s/request floor: OpenTelemetry export retries to DOWN OpenObserve (localhost:5080)
on every request shutdown. Disabled via OTEL_SDK_DISABLED=true for the QA server process. Also
`php artisan serve` is single-threaded by default — QA ran with PHP_CLI_SERVER_WORKERS=8.

## AC checkpoints
- AC10 backstop: flutter test = 2009/2009 PASS. flutter analyze = 5 info lints, all pre-existing in untouched files. PASS
- AC1 (zone 1 multi-module, guest 12:15 + logged-in 12:19): sectors_shown fires BEFORE "initial route" line
  (prime-before-nav proven); chooser fully rendered; no "Service not available" text at any point; 1 nav. PASS
  Shots: ac1-zone1-module-chooser-resolved.png, ac6-loggedin-multimodule-resolved.png
- AC2 (airplane-after-config, SIGSTOP backend post-config; guest 12:13 + logged-in 12:21): deadline warn at
  +1.805s, fallback nav +1.82s (<2s), home+shimmer, NO NoInternetScreen, no stuck splash. PASS
  Shot: ac2-airplane-after-config-home-shimmer.png
- AC3 latch: 10+ cold opens sampled across resolve-wins / deadline-wins / dual-pass boots — exactly ONE
  "route: initial route" per boot every time; late resolutions log "prime skipped" (state-only). PASS
- AC4: deep-link cold start (VIEW intent) → deep-link machinery navigates, ZERO splash-resolver lines
  (bypass correct); notification path code-verified untouched (body!=null branch). PASS (with followup:
  pre-existing-looking [ERR] "error snackbar shown" + double nav on deep-link cold start — untouched path)
- AC6 out-of-zone (ocean coords): inZone=false, NO fallback warn (correctly resolved tier), settled
  "Service not available" + Change Location. PASS. Shot: ac6-outofzone-settled.png
- AC6 1-module-multi-store (zone 364, guest+logged-in): FAIL — bug 1 (unscoped module fetch).
- AC6 1-module-1-store (zone 3 directStore seam): FAIL — bug 1 (module 4 not even in unscoped list).
- AC7 analytics: sectors_shown fires once per zone BUT with unscoped count (3 instead of 1) on resolved
  boots; sector_auto_selected NEVER fires from resolver (bug 1). Home-machinery fallback events intact. FAIL
- AC8 logging: deadline / zoneFetchFailed(500, correlation-joined to BE laravel.log) / staleZoneMismatch
  warn lines all correct + attributed; PII clean (zone ids only, no coords; endpoint paths only). PASS
  (moduleFetchFailed + emptyZoneIds cells NOT-DEMONSTRABLE live: need endpoint-selective fault injection /
  contract-impossible; both unit-covered.)
- AC9: fallback boot auto-select fired once (NEARS-960/901 ✓); pull-to-refresh ×2 + back-nav → ZERO new
  sector events, module home stable; NEARS-469 no picker sheet on any launch. PASS
- AC5 web: worktree web boot fails early (uncaught promise error, zero API calls) — A/B vs base in progress.

## Bugs
1. bug-resolver-module-header-unscoped: _buildHeaders sends 'zone_id: 364' (name+format wrong; replaces
   _mainHeaders wholesale) → backend ignores → unscoped module list → wrong tier on 1-module zones →
   disarmAutoSelect + ModuleView length==1 spinner = PERMANENT STUCK SPINNER for fresh users in Baqala
   zones. Shots: bug-resolver-module-header-unscoped.png, bug-loggedin-zone364-stuck-spinner.png + .log
2. bug-dual-resolver-pass-per-boot: cache-then-network config → route() twice per warm boot → TWO
   resolveAndNavigate invocations (each own latch). Nav dedup only via GetX preventDuplicates; pass-2 tier
   work (event + selectModuleNavFree + markBootZoneFresh after consumption) still runs. .log artifact.

# NEARS-1020 QA progress (cycle 1 — delta re-QA of B1/B2 fix @ 5f9f5883)
Device: emulator-5554 | Build: worktree @ 5f9f5883 (fresh install, debug APK) | Backend: same :8000 (OTEL off, 8 workers)
Reused from cycle 0 (no overlap re-demo per delta rules): AC1/AC2/AC3/AC4/AC6-outofzone/AC8/AC9/AC10 PASS rows.

## Delta cells
- CELL1 AC6 zone-364 guest (13:33) + logged-in (13:38): module fetch SCOPED -> tier singleModuleHome ->
  Baqala module home RENDERS ("3 stores near you" + cards, NO stuck spinner). sector_auto_selected
  {module_id:1, zone_id:364} exactly once, resolver-fired BEFORE "route: initial route module=grocery-food";
  sectors_shown {sectors_count:1, zone_id:364} exactly once. 0 ERR/FAIL. PASS
  (cycle-0 bug-loggedin-zone364-stuck-spinner: FIXED)
- CELL2 AC6 zone-3 directStore seam (13:41): cold open -> "route: initial route module=qa-single-store-grocery",
  store surface renders (QA Staples); sector_auto_selected count = 0 (parity rule honored);
  sectors_shown {sectors_count:1, zone_id:3}; store_auto_opened {store_id:59} home-machinery path intact. PASS
- CELL3 AC7 analytics: sectors_shown zone-scoped everywhere — {3, zone 1} / {1, zone 364} / {1, zone 3},
  each exactly once per boot (dedup sentinel intact). Cycle-0 unscoped-count defect (3 in zone 364): FIXED. PASS
- CELL4 B1 wire: /api/v1/module captured via throwaway header-logging router on :8000 (product code untouched,
  artisan serve restored after) — carries zoneid: "[364]" (jsonEncode int list) + ALL default headers
  (moduleid, x-localization, x-request-id, traceparent, content-type); NO zone_id key. PASS
  Artifact: cycle1-b1-module-request-headers.jsonl (emulator GPS redacted)
- CELL5 B2 warm boot (boot3, zone 1): config cache pass-1 -> ONE get-zone-id + ONE /module from splash ->
  sectors_shown -> ONE "route: initial route"; config network pass-2 -> "splash-nav: duplicate boot resolution
  skipped (config cache+network chain)". Post-nav: exactly ONE get-zone-id (syncZoneData; home initState getZone
  SKIPPED = markBootZoneFresh consumed once). Counterfactual on fallback boot7: TWO post-nav get-zone-id
  (marker correctly not set on fallback). Cycle-0 bug-dual-resolver-pass-per-boot: FIXED. PASS
- CELL6 sweep: (a) fallback boot (backend SIGSTOP after cached config): deadline warn +1.809s, fallback nav
  +1.822s (<2s), NO NoInternetScreen, home machinery armed, recovers after resume. (b) zone-1 multi-module
  boot: chooser renders as cycle 0 (3 sectors + featured stores). PASS
- CELL7 backstop: flutter test 2012/2012 PASS ("All tests passed", +3 vs cycle-0 2009 = the new header-map/latch
  tests); flutter analyze = same 5 pre-existing info lints in untouched test files. PASS

VERDICT cycle 1: PASS — both cycle-0 task bugs fixed and demonstrated live; no new defects.
