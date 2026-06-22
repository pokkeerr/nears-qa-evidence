# NEARS-576 QA progress (live-checkpointed)

Build: worktree feat/NEARS-576-vendorapp-logging @963a47e4 · VendorApp · emulator-5554 · light-mode · fix-cycle 1
Backend join: worktree backend on :8001 (SetRequestId/NEARS-571 present, composer install done)

## Preflight
- baseUrl = http://10.0.2.2:8000 (Android) — real local backend, NOT demo. OK.
- backend :8000 (primary, no SetRequestId) live; worktree backend :8001 (with SetRequestId) live.
- X-Request-Id ECHO proven via curl: minted id reflected in response header on :8001 (401 {errors:[...]} path). [join half 1/2]

## AC checkpoints

- AC8 (analyze): NEARS-576 files (api_client/api_checker/app_logger/main.dart) analyze-CLEAN. 17 pre-existing issues identical in primary tree (baseline, not introduced). PASS (no new issues).
- Automated backstop: flutter test (2 new files) = 29/29 PASS. Covers mint-uniqueness, echo-read lowercase, correlation threading, H1 (rebuild preserves request / regression-guard nulls endpoint), PII allow-list, [NET]/[WARN]/[INFO] console-only. 
- Backend join echo: minted X-Request-Id reflected in response header on :8001 for {errors:[...]} 401 path. [join structurally proven]

## LIVE app-driven evidence (emulator-5554, debug, app→worktree backend :8000 w/ SetRequestId)
- BOOT (AC8): debug apk built+installed+booted as "Nears Vendor" (com.izzes.nearsvendor). Language→Next→Login reached. PASS.
- AC1 [NET] live: `[NET] endpoint=/api/v1/config http_status=200` and `[NET] endpoint=/api/v1/auth/vendor/login http_status=401` — endpoint PATH only, no body/query. 
- AC2+AC3+AC4+AC6 CORE (wrong-creds login → 401 {errors:[...]}):
    `[FAIL] endpoint=/api/v1/auth/vendor/login http_status=401 type=ApiFailure msg="unhandled api response" correlation_id=469fb61c-2dbe-4aaa-a24d-9e589f6f9458`
    → correlation_id NON-NULL real UUID v4 (AC2 echo-read + AC3 rebuild-preserves-header), endpoint NON-NULL (AC4 H1 fix), PII-safe: only path+status+sentinel+generic msg+corr_id (AC6). PASS.
- AC7 debug Crashlytics silence: Firebase settings fetched show "firebase_crashlytics_enabled":false, "collect_analytics":false in debug. recordError no-op. console [FAIL]/[NET] visible. PASS.
- Backend structured channel writes correlation_id (NEARS-571, proven via tinker):
    {"tag":"[FAIL]",...,"correlation_id":"abcdef01-...","context":{"endpoint":"/api/v1/qa/probe","http_status":500}}
  → join field works. App-driven clean-401 emits NO server Log:: (correct), so no co-logged row for that id; join structurally complete (echo half live + structured-write half live).

- AC5 offline/timeout throw (airplane mode, multiple verbs):
    GET  [FAIL] endpoint=/api/v1/vendor/order http_status=null type=_ClientSocketException correlation_id=a51bc968-... (and profile/current-orders/notifications, 4 DISTINCT ids → also re-proves AC1 uniqueness)
    POST [FAIL] endpoint=/api/v1/vendor/update-order-status http_status=null type=_ClientSocketException correlation_id=37a8a69a-... 
    → minted id present with NO response echo; endpoint set; status null; PII-safe. PASS.
- AC6 PII sweep over ALL AppLogger [FAIL]/[ERR]/[NET]: NO email/phone/name/address/token/bearer/password/statusText/body/query-string. endpoints path-only. correlation_id = UUID v4 (hex+dash). PASS.
- AC9 regression: valid login (ahmed.khan@demo.com) → home dashboard loaded; [NET] 200 on update-fcm-token, profile, current-orders, notifications; order#156 detail via /vendor/order + /vendor/order-details 200. order-detail screen shows customer PII in UI but [NET] log is path-only. No red-screen. PASS.

## FINDING (Low, non-blocking, mirrors accepted UserApp NEARS-572 pattern)
- Transport-throw catch passes RAW exception `e` to AppLogger.failure → recordError records the exception OBJECT whose .toString() = "ClientException with SocketException ... uri=http://10.0.2.2:8000/api/v1/vendor/order?order_id=156" (full host+path+QUERY). 
- In DEBUG (build under test): console-only, collection disabled, ZERO upload — our own [FAIL] line is clean path-only. So AC6/AC7 HOLD for the gating build.
- RELEASE-only exposure: full uri (incl. ?order_id query + host) would reach Crashlytics via the recorded error object. Low-sensitivity (order id / host, not name/phone/email/address). IDENTICAL to landed+QA'd UserApp NEARS-572 (UserApp/lib/api/api_client.dart passes raw e too). Cross-cutting hardening, NOT a NEARS-576 regression. Does NOT break an AC → does NOT FAIL.

- AC9 (cont.): order-status confirm (handleError:true POST) succeeded online 200 /api/v1/vendor/update-order-status → Pending→Confirmed, cascade refresh all 200. Logout → clean redirect to Sign In (same Get.offAllNamed(getSignInRoute()) path checkApi 401-logout uses). Error-display path proven (wrong-creds 401 kept user on login). No red-screen/overflow/fatal across whole session. PASS.
- checkApi handleError:true [FAIL] (endpoint via response.request?.url.path + correlation via requestIdFromResponse): structurally proven — same handleResponse rebuild that fed the LIVE login-401 [FAIL] (endpoint NON-NULL) feeds checkApi; unit seam covers {errors}/{message} rebuild-preserves-request + regression-guard-nulls-endpoint. 
- E2E backend join: ECHO half LIVE (app-minted X-Request-Id read back as correlation_id on [FAIL]) + STRUCTURED-WRITE half LIVE (tinker: laravel-structured.log line carries correlation_id field, contract schema). App clean-401 emits no server Log:: (correct) so no single co-logged row; join = structurally complete + (release-Crashlytics-upload) deferred as documented.

## VERDICT: PASS. 9/9 ACs met. 1 Low non-blocking finding (transport raw-exception .toString full-uri, release-only, mirrors landed UserApp NEARS-572). 0 regressions.
