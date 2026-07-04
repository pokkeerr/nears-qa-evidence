# NEARS-957 QA progress — request log path-only (debug-console)

Device: emulator-5560 (DEBUG builds; [NET] compiled out in release). Backend: 127.0.0.1:8000 up.
Branch fix/NEARS-957-request-log-path-only @ b32e6e14. fix-cycle 0.

## Automated backstop (PASS)
- UserApp/test/api_client_no_pii_log_test.dart .......... 10/10 PASS (NEARS-957 path-only assertions incl.)
- DeliveryApp/test/api_client_redact_headers_test.dart .. 15/15 PASS
- VendorApp/test/api_client_redact_headers_test.dart .... 15/15 PASS

## Source backstop (PASS)
- `?? uri` in AppLogger.net/netRequest args: ZERO (all now `?? 'unknown'`) — F1 gate met.
- 15 `?? uri` residuals are all in AppLogger.failure endpoint: args (pre-existing NEARS-572/576/579 error path) -> low-sev followup, non-blocking.
- old `====> API Call/Response` lines: ZERO across 3 apps.
- maskTokenInUri: still DEFINED in Delivery/Vendor but no longer referenced in any log line (dead-ish helper, still unit-tested) — not a leak.

## Live [NET] observations

### UserApp (PASS) — 148 [NET] lines, all path-only
- AC1: stores/details/8, items/latest(?store_id&category_id), search/unified(?name) -> path only
- AC3: 0 leaks (?/token/lat/lng/store_id/category_id/name), 0 legacy ====> lines
- lat/lng GET: get-zone-id?lat=&lng= -> path only; special-char search 'tea&milk'/"O'Brien 100%" -> path only
- regression: 0 [FAIL]/[ERR]/[WARN], no red-screens

### DeliveryApp (PASS) — logged in DM Ali, 22 [NET] lines all path-only
- AC2: login/profile/current-orders/latest-orders/notifications/update-active-status/fcm (?token= stripped) req+resp path only
- AC4 (NEARS-921): record-location-data POST (coords in body) -> path only
- AC3: 0 leaks, 0 legacy ====>, 0 token=*** masked-uri lines, 0 [FAIL]/[ERR]
- NOTE: worktree missing gitignored google-services.json -> provisioned from primary tree (env, not code). Pre-existing: Delivery/Vendor Firebase.initializeApp() has no inline-options fallback (UserApp does) -> cold-start crash without json. Regression-candidate, non-blocking.

### VendorApp (PASS) — logged in vendor ahmed.khan, 18 [NET] lines all path-only
- AC2: login/profile/current-orders/completed-orders/notifications/fcm req+resp path-only; token in Authorization HEADER now NOT logged at all (old line logged redactHeaders); query (offset/limit) stripped
- AC2 multipart (update-profile): live-demo DECLINED (all VendorApp multipart = DB writes; read-only rule) -> verified by diff+unit+identical netRequest code path
- AC3: 0 leaks, 0 legacy ====>, 0 token=***, 0 [FAIL]/[ERR]

## VERDICT: PASS (AC1/AC2/AC3/AC4 all met; multipart leg code-path-verified). Firebase env gap flagged non-blocking.
