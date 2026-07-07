# NEARS-1017 QA progress

Device: emulator-5554 (locked). Worktree build @3a5010fe. Backend :8000 primary (Admin delta f19208a0..HEAD = empty, verified).

## AC1 — keys carry -z<zoneId> (zone 1, live)
Signed in customer@nears.com, zone 1 (Dhaka), active zone_id=1 (shared prefs verified).
cache_response rows (drift DB pull):
- featured:   /api/v1/stores/get-stores/all?featured=1&offset=1&limit=50--z1   (module-null landing fetch)
- store list: /api/v1/stores/get-stores/all?store_type=all&offset=1&limit=12-1-z1
- popular:    /api/v1/stores/popular?type=all-1-z1   (stray '}' of old key gone)
- latest:     /api/v1/stores/latest?type=all-1-z1
- top-offer:  /api/v1/stores/top-offer-near-me-1-z1
(5/7 live; recommended = /api/v1/stores/recommended returns 0 stores in BOTH zones (curl probe) -> rail self-suppresses, fetch UI-unreachable; visit-again = getVisitAgainStoreList has NO UI call site in this build (dead rail, pre-existing). Both keys verified via diff (identical cacheZoneSuffix() construct) + unit test pinning suffix.)
Runtime errors: clean (get_runtime_errors after sign-in + module homes).
## AC3 — same-zone cache-hit intact (zone 1, live, backend-down staging)
- App relaunched pointed at PRIVATE backend :8017 (dart-define API_HOST; shared :8000 untouched); :8017 killed to freeze the local-read render.
- Tampered row `...store_type=all&offset=1&limit=12-1-z1` payload: "Corner Grocer" -> "QA MARKER 1017 STORE" (device-local drift cache only).
- Entered Grocery module home with backend DOWN: banners/categories/flash-sale/item rails all rendered from cache; stores section rendered "QA MARKER 1017 STORE 20-40 0.4 km" = the DISK ROW rendered (marker exists only on disk) => write/read key symmetric incl. -z1 suffix. Shot: ac3-marker-cache-render.png.
- Client refresh dispatched + failed with PAIRED PII-safe log: `[FAIL] endpoint=/api/v1/stores/get-stores/all http_status=null type=ApiFailure ... correlation_id=...` (expected — backend deliberately down; not a silent failure).
- NOTE (architecture, pre-existing): local-first pattern ALWAYS dispatches a client refresh, so "[NET] absent" as written in the AC cannot hold on any surface; the cache-hit is proven by the marker render instead.
- Airplane-mode relaunch variant NOT achievable: splash config fetch is network-gated ("No internet connection" retry screen) — pre-existing app behavior, unrelated to this change.
## Regression-candidate found (pre-existing, NOT this ticket)
- Featured-list local reads written with custom `featuredHeader` (module-null landing, NEARS-976/686) NEVER hit: LocalClient.organize(local) compares `cachePartitionKey()` DEFAULT fingerprint vs stored custom-header fingerprint -> permanent silent miss (fail-safe: falls back to network). local_client.dart:93 vs :51. Proven live: featured marker on disk + backend down -> rail rendered in-memory/miss, store-list marker (symmetric header) rendered fine.
## AC1 addendum — recommended key live (staged /home/all 500 via local proxy on :8017)
Fallback rails fired; row written: `/api/v1/stores/recommended-1-z1` (payload `[]`, seed-empty) while featured row kept its 65,797-byte real payload under its OWN key — the exact pre-fix collision scenario (recommended clobbering featured's row) demonstrated fixed. 6/7 keys live; visit-again = dead UI call site (pre-existing), unit-test+diff verified.
## AC2 — key-layer cross-zone proof (zone switch + forged fingerprint-passing row)
- Switched via Set Location sheet to saved "Abu Dhabi - United Arab Emirates" → address re-resolves to containing micro-zone 400 (guide-documented). Zone-switch WIPE fired: all old rows (ids<=90) cleared (layer-1 demo).
- Landing featured rail rendered ZONE-2 stores (Abu Dhabi Fresh Market, Golden Wok, Spice Route Kitchen). Shot: ac2-landing-zone2.png. New keys: featured `...limit=50--z400`, store list `...limit=12-1-z400`.
- Forged row inserted: key `...limit=12-1-z1` (differs ONLY in zone suffix), header COPIED from the real z400 row (fingerprint-passing), first store renamed "QA MARKER 1017 STORE". Re-entered grocery home: 20 stores near you rendered REAL z2 names, marker count 0 (shot: ac2-grocery-z2-stores-no-marker.png).
- DB proof (two distinct-keyed rows coexisting): row 113 `...-z400` 69,070B clean (refreshed) + row 116 `...-z1` HAS-MARKER untouched/never read. Pre-fix these were ONE shared key -> the marker would have rendered. Saved: ac1-z2-keys.log.
## Regression sweep (bounded, light mode)
- Z1: module-choose landing, grocery home (banners/categories/flash-sale/item rails/stores), food home, AllStore featured screen, order-tracking screen — all rendered, ui_errors clean.
- Z2 (zone 400): landing + grocery home all sections rendered; store list 20 stores. Expected one-time cache miss per list after upgrade (old un-suffixed keys orphaned) — observed as normal refetch, not a bug.
- Logs: zero unexpected [ERR]/[FAIL]; all 30 [FAIL]=staged backend-down window, each paired+PII-safe with correlation ids.
## Automated backstop
flutter test (worktree): 1951/1951 All tests passed (includes new store_repository_cache_zone_key_test.dart).
