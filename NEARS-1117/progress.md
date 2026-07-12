# NEARS-1117 — Live QA [8], fix_cycle 0

**Verdict: PASS** · device `emulator-5556` (Android, sdk_gphone16k_arm64) · debug APK built from worktree
`/Users/Apple/Projects/nears-NEARS-1117-module-cache-key` @ branch `feat/NEARS-1117-module-cache-zone-key`
(base `feat/human-review` @ `50b436ae`) · light mode only (dark deferred).

Pre-flight: `useHttps=false` → `baseUrl = http://10.0.2.2:8000` (real local backend; `GET /api/v1/config` → 200).
Package `com.izzes.nears`. Backend up. DB read-only throughout.

## The proof of the fix (unit) + the proof it broke nothing (live)

A live zone-switch demo canNOT prove this fix (it passes pre-fix too — masked by `AddressHelper.clearCache()`
and by the `cachePartitionKey` fingerprint). So the fix itself is discharged by the mutation-checked unit suite,
and the live run is a regression gate. **Additionally**, a device-level probe DID demonstrate the fix directly:
the running app's drift cache DB shows the module row keyed by zone.

### On-device cache keys (drift DB `app_flutter/cache_response_new_db.sqlite`, table `cache_response`)

| App state | persisted address | module cache row |
|---|---|---|
| Zone 2 (Abu Dhabi) | `zone_id:400, zone_ids:[400,2]` | `/api/v1/module-z400` |
| Zone 1 (Demo/Dhaka) | `zone_id:1, zone_ids:[1]` | `/api/v1/module-z1` |
| Zone 2 again (round-trip) | `zone_id:400, zone_ids:[400,2]` | `/api/v1/module-z400` |

Distinct, zone-scoped, deterministic. Sibling NEARS-1017 store rows carry the same `-z<id>` suffix
(`/api/v1/stores/get-stores/all?...-z400`), consistent with the precedent.

## Per-AC results

| AC | Result | Evidence | Logs |
|---|---|---|---|
| AC1 — cache row keyed with active zone | **PASS** | Unit suite 10/10; **live on-device** row `/api/v1/module-z400` (zone 2) | clean |
| AC2 — zone 1 vs zone 2 resolve to different keys | **PASS** | Unit suite; **live** `-z400` (z2) vs `-z1` (z1) | clean |
| AC3 — same zone still HITS cache (no permanent miss) | **PASS** | Unit suite; **live**: cold boot renders grid in **3–4s with `module_net_fetches=0`** → painted from the `local` cache read before any network module fetch. 3× same-zone cold boots → exactly **one** module row, no churn/accumulation | clean |
| AC5-equiv — first launch, NO saved address (`-z` null path) | **PASS** | Fresh install (`pm clear`) + location permission revoked → `GET /api/v1/module` → **200** at onboarding with no saved address; no crash | clean |
| Regression — zone switch repaints grid, correct stores | **PASS** | see store-count matrix below | clean |
| Regression — zone round-trip (z1→z2→z1) | **PASS** | z1 back to 6/6/6, not z2's 20/5/5 | clean |
| Regression — boot perf | **PASS** | grid at 3–4s, 0 module fetches (cache hit). One-time extra fetch on first post-update boot observed = expected | clean |
| Regression — deep-link cold start | **PASS** | `VIEW http://6ammart-web.6amtech.com/store/2` → app reaches home, module grid rendered, 0 module fetches (cache hit) | clean |
| Regression — language switch | **PASS** | EN→AR: settings + grid localize, `GET /api/v1/module` refetch fires (expected — language is in the fingerprint, not the cacheId), cache key stays `/api/v1/module-z1` | clean |

## Store-count matrix — verified against live DB (read-only SELECT)

The module grid renders the SAME 3 tiles in both zones, so the grid alone cannot distinguish stale from fresh.
The store count is the tell. All app values match DB ground truth:

| Module | Zone 1 (app) | Zone 2 (app) | Zone 1 round-trip | DB (active) |
|---|---|---|---|---|
| Grocery & Food | 6 | **20** | 6 | z1=6 · z2=15 (+5 from overlapping zone 400) = 20 |
| Food & Restaurant | 6 | **5** | 6 | z1=6 · z2=5 |
| Pharmacy | 6 | **5** | 6 | z1=6 · z2=5 |

**Drift vs the spawn brief:** the brief expected zone-2 Grocery = 15. Actual = **20**, and it is correct.
`GET /api/v1/config/get-zone-id?lat=24.453884&lng=54.3773438` → `zone_id:"[400,2]"` — the Abu Dhabi point falls
inside **two** overlapping zones (Baqala Zone 37 `id=400` + Abu Dhabi `id=2`). 15 active (z2) + 5 active (z400) = 20.
The DB has ~90 Baqala zones (364–453) beyond the brief's 2-zone model. Not a defect.

## Automated backstop
- `~/Tools/flutter/bin/flutter test` (full UserApp suite) → **2293/2293 pass** (engineer's number confirmed).
- `~/Tools/flutter/bin/flutter test test/features/splash/splash_repository_cache_zone_key_test.dart` → **10/10 pass**.

## Checks NOT counted as evidence (stated plainly)
- **Offline cold boot** — inconclusive, discarded. The app gates home behind an "Oops! No internet connection"
  screen by design, so modules never render offline regardless of cache state. Cannot probe the module cache.
- **Throttled-network boot** (`adb emu network speed gsm`) — inconclusive, discarded. Emulator throttling does not
  apply to the host-loopback route (`10.0.2.2`), so the backend stayed fast and the test could not discriminate.
- An intermediate "zone 2 → 6/6/6" reading was a **navigation artifact of mine** (my taps failed and I re-read the
  same Grocery screen); confirmed against the persisted address, corrected, and re-measured via the "Switch module"
  control. It was NOT a product bug.
