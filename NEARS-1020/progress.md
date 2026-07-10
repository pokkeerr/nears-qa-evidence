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
