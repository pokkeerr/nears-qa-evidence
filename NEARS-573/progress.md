# NEARS-573 QA progress (Admin-web browser RUM)

Worktree: /Users/Apple/Projects/nears-NEARS-573-adminweb-rum @ feat/NEARS-573-adminweb-rum
Panel boot: php artisan serve --port=8010 (admin /admin, vendor login)
Mode: light-only (dark deferred); Admin/store panels = utility 6amMart (no Stitch frame) -> 3b = render-integrity smoke only.

## Static pre-flight (verified before boot)
- config/rum.php: 4 env-gated keys, all default OFF. OK
- _rum.blade.php: meta correlation-id + window.__RUM_CONFIG + same-origin <script src> (no CDN). OK
- nears-rum.js: error + unhandledrejection handlers; PII-safe event; query-string stripped; capture-only default; keepalive + credentials:omit ship. OK
- admin layout includes partial rumPanel=admin; vendor layout rumPanel=store. OK
- .env.example: OPENOBSERVE_RUM_ENABLED/ENDPOINT/TOKEN/DEBUG all present, default off. OK
- NEARS-571 SetRequestId middleware + [FAIL] hook in bootstrap/app.php present (AC3 dependency). OK

## Per-AC live results

## LIVE RESULTS (observed 2026-06-22, panel @ :8010)

AC1 handler on BOTH panels:
- ADMIN: throw Error('rum-test-admin') + Promise.reject('rum-reject-admin') -> both captured. tag=[ERR], type/message/source/line/col/STACK/page_url present, panel=admin, correlation_id present. PASS
- STORE: throw Error('rum-test-store') captured, tag=[ERR], panel=store, correlation_id present. PASS
- console.debug('[ERR] nears-rum', {...}) breadcrumb fires only when DEBUG=true. PASS

AC1 PII + AC4 no user data:
- page_url ALWAYS query-stripped (navigated ?foo=bar&secret=... -> page_url=/admin). 0 leaks in page_url. PASS for page_url.
- typed PII into field (MYSECRETSEARCH-PII-9999) NOT present in any event. No cookie/localStorage in event. PASS for field/cookie/storage.
- ** GAP **: when a PAGE-INLINE script error fires on a URL carrying a query string, the browser-provided `source`/`stack` echo the FULL document URL incl. query (e.g. .../admin?token=LEAKME99SECRET). Handler passes evt.filename/err.stack verbatim (only length-clipped), no query strip on those fields. Confirmed SHIPPED over the wire (2/2 POST bodies leaked ?search=CUSTOMER-PHONE-0501234567 inside stack). page_url stays clean. -> AC4 PII guarantee for stack="code-locations only / no user data" NOT fully met. task_bug, latent until RUM enabled (default OFF, prod=NEARS-8).

AC2 env-gated default OFF + non-blocking:
- DEFAULT (enabled=false,debug=false): fired errors -> 0 debug breadcrumbs, 0 RUM network POST, page functional. PASS
- ENABLED=true + UNREACHABLE endpoint: 3 ship POSTs attempted, Authorization: Bearer <token>, NO Cookie header (credentials:omit), content-type json; 0 console errors (silent no-op), page works. PASS
- "appears in OpenObserve" = degraded-deferred (OO down + prod NEARS-8); verified snippet+config+capture+ship-attempt instead. NOTED.

AC3 server [FAIL] (571 hook covers admin web):
- 3 admin/* routes 500'd (category/update, attribute/edit, banner/edit, coupon/view) -> each ONE [FAIL] line in laravel-structured.log with tag=[FAIL], correlation_id == response X-Request-Id, exception class (context.type), message, endpoint path (query-stripped). PASS

AC5 no regression (render-integrity smoke, 3b):
- ADMIN dashboard/order-list/store-list/category-add-form render OK, RUM present, 0 snippet-origin console errors.
- STORE dashboard+pos render OK, RUM present, 0 snippet-origin errors.
- Pre-existing Firebase/jQuery pageerrors are baseline (snippet captures, not causes them). Layout change is additive @include only. PASS

AC6 confirm:
- No external/CDN <script src> added; RUM script same-origin asset(); only network = env-gated cfg.endpoint (no hardcoded URL). config/logging.php UNTOUCHED -> no new log channel. PASS

Automated backstop: vendor/bin/phpunit logging+correlation suite = 15/15 OK, 79 assertions (underpins AC3). No RUM-specific PHP tests (client-side JS).

VERDICT: FAIL — AC4 PII fence gap (query string leaks into source/stack of inline-script errors, ships when enabled). All other ACs PASS. Bug is in THIS change (task_bug, breaks_ac).
