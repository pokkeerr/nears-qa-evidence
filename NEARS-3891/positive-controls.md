# NEARS-3891 — positive controls (sandboxed phpunit, untouched tree)

Wrapper (every phpunit run in this worktree): `cd Admin && bash <scratchpad>/sandbox-phpunit.sh [args]`.
It first requires a sandboxed `curl https://example.com` to be SIGKILLed (rc 137, else refuses to run), then
`exec sandbox-exec -p '(version 1) (allow default) (deny network-outbound (remote tcp "*:80") (remote tcp "*:443") (with send-signal SIGKILL))' vendor/bin/phpunit --configuration phpunit.xml ...`.
A test that opens tcp 80/443 kills the whole phpunit process: exit 137.

## Untouched tree (base 53b314d4a + nothing), throwaway `ZzNears3891ControlTest` (deleted, not delivered)
Config via `push_notification_service_file_content_conf` override (generated RSA key, no DB row, no real credentials), no Http fake unless stated.

| Path | Control test | Setup | Exit |
|---|---|---|---|
| `Helpers::sendNotificationToHttp` FCM POST (Helpers.php ~1876-1979) | `test_ctl_helpers_send_fcm` | oauth token pre-cached so only `fcm.googleapis.com` is reached | 137 |
| `Helpers::getAccessToken` OAuth (Helpers.php ~2000) | `test_ctl_helpers_oauth` | no cache | 137 |
| `NotificationTrait::sendNotificationToHttp` FCM POST (~179-214) | `test_ctl_trait_send_fcm` | `oauth2.googleapis.com` faked 200, FCM host unfaked | 137 |
| `NotificationTrait::getAccessToken` OAuth (~216-243) | `test_ctl_trait_oauth` | no fake | 137 |
| Kreait singleton `firebase.messaging` via `FirebaseController::subscribeToTopic` (`POST /subscribeToTopic`) | `test_ctl_firebase_singleton` | acting as Admin, no rebinding | 137 |

Not a false positive: with `CTL_FAKE=1` (Http::fake on both hosts + `firebase.messaging` bound to a Mockery double) the same five tests under the same wrapper: `OK (5 tests)`, exit 0.
Existing FCM test with its own Http::fake, same wrapper: `Nears2464HelpersSendNotificationPiiTest` -> `OK (5 tests, 35 assertions)`, exit 0.

## Guarded tree (this branch), same five control tests, no fakes, same wrapper
All five exit 0 (default responder answers the Http:: paths; the singleton is an inert double, the controller returns 500 from the double's rejection, no egress).

## Egress not reachable via Http:: (found by the guarded full run)
`AdminRouteSmokeTest::test_every_named_admin_get_route_never_500s` was KILLED (137) at route `admin.report.generate-statement`: mPDF `WriteHTML()` fetches `fonts.googleapis.com` and `cdnjs.cloudflare.com` stylesheets over its own curl (order-transaction-statement.blade.php:209-210). Bisected with a throwaway per-route probe. Fix-cycle 1: no skip; the test calls `refuseRawCurlEgress()` so the route stays in the sweep (executed 359, route returns 200 text/html); `AdminRouteSmokeTest` OK (3 tests), exit 0.

## Full sandboxed run (guarded tree, final)
`cd Admin && bash sandbox-phpunit.sh --log-events-text <file>` -> exit 1, NO sandbox kill (no 137): `Tests: 3030, Assertions: 20793, Failures: 1, PHPUnit Deprecations: 1, Skipped: 1` in 07:11, peak memory 993MB (phpunit.xml limit 1024M).
The single failure is `ConfigContractTest::test_decimal_precision_is_two_not_whole_dirhams` (NEARS-2019 "EXPECTED RED" seed-DB contract, unrelated). Deprecation (`HotTableFilterIndexMigrationTest` doc-comment metadata) and skip (`TestDbIsolationTest`) are pre-existing.
Earlier guarded full runs were killed twice, each time by non-`Http::` egress: `AdminRouteSmokeTest` @ `admin.report.generate-statement` and `DmEarningInvoiceTest::test_returns_pdf_for_token_owner` (both mPDF font/CSS fetch). First non-killed run also surfaced 2 scan failures (`VendorRegister403DiagnosisTest`, `api.pwnedpasswords.com`) and 2 risky tests (fixed).
Mutation checks (proof test): scan predicate off -> P3, P4, P3b red; TestCase wiring off -> P3b red; spy branch off -> P4 red; logger listener off -> P3, P3b red.

## Fix-cycle 1 full sandboxed run (final)
exit 1, no 137. `Tests: 3033, Assertions: 20806, Failures: 1, PHPUnit Deprecations: 1, Skipped: 1`; only failure = `ConfigContractTest` (NEARS-2019, pre-existing). Recording proof: `test_p1b` (partial Http::fake + unfaked push -> `assertSent` fcm/oauth, `assertSentCount(2)`); mutation (record call off) -> P1b red. SEC-1 proof `test_p7`/`test_p7b` (2 calls, inherited `no_proxy=*` ignored, env restored); mutations (no_proxy unset off -> P7 red; already-armed guard off -> P7b red). 49 anti-shadow/push/assert*Sent files all exit 0.
