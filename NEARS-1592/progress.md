# NEARS-1592 — live QA (fix_cycle 0) — VERDICT: PASS

Worktree `/Users/Apple/Projects/nears-NEARS-1592-dead-rail-common-condition`,
branch `feat/NEARS-1592-dead-rail-common-condition`, base `60dc1bc6`.
Device `emulator-5560` (1080x2340 px @ density 420 = 411x891 dp). **Light mode only** (dark deferred).
Flutter `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9. DB read-only. Shared backend never stopped.

## Anti-stale-APK chain (the ticket's declared trap)
| Step | md5 |
|---|---|
| Pre-existing (FOREIGN) APK already installed on 5560 | `7b9376025c6d52d80556c6cfaea19153` |
| Built from this worktree | `0ae06e71ba6cfed0fd3d913df1b808e5` |
| Re-read from `/data/app/.../base.apk` after install | `0ae06e71ba6cfed0fd3d913df1b808e5` (MATCH built, DIFFERS from foreign) |
| Fault-injection variant (`--dart-define=API_HOST=10.0.2.2:8791`) built / installed | `4a745692fea19865855be4e8d72e2f25` / same |
| Canonical rebuild reinstalled at end of run | `7d6a430d977648f91b11f65bc8e86ced` (debug APKs are NOT byte-reproducible; content re-probed, see below) |

**Falsifiable content probe** on each installed APK's `assets/flutter_assets/kernel_blob.bin`
(controls prove the probe can find things — a silently-broken probe would have shown 0 everywhere):

| Symbol | canonical `0ae06e71` | canonical `7d6a430d` |
|---|---|---|
| `CommonConditionView` (must be ABSENT) | 0 | 0 |
| `common_condition_view` (must be ABSENT) | 0 | 0 |
| CONTROL `PharmacyOtcRailView` | 5 | 5 |
| CONTROL `pharmacy_otc_rail` | 5 | — |
| CONTROL `ProductWithCategoriesView` | 6 | — |

Fault injection for the branch coverage: `nears_fault_proxy_1592.py` on 8791 -> `127.0.0.1:8000`,
three modes self-tested before use (`pass` 200 passthrough / `fail` 500 on `/api/v1/stores/get-stores*` /
`empty` 200 zero stores / `closed` upstream response rewritten to `active:false`).

## Per-AC results
| AC | Verdict | Evidence | Logs |
|---|---|---|---|
| AC1 `[ui]` file deleted, grep = 0 hits | **PASS** | file absent from worktree; `grep -rn CommonConditionView UserApp/lib UserApp/test` = **0**. Independently re-verified the unreachability claim at base: `git grep CommonConditionView 60dc1bc6 -- UserApp/` returns ONLY the class decl, its own ctor, a doc-comment mention and the test's `find.byType` — **zero constructor call sites**, so the widget could never mount. | n/a (static) |
| AC2 `[behav]` Pharmacy home unchanged | **PASS** | cold start on the checksum-verified build: Flash Sale (countdown + cards) -> Open Now/Open 24h chips -> Nearby Pharmacies (5 stores) -> `PharmacyOtcRailView` ("Shop OTC essentials" + 5 chips) -> host store list. No blank band or gap anywhere. `ac2-pharmacy-home-loaded.png`, `ac2-pharmacy-otc-rail.png` | **clean** |
| AC3 `[behav]` suite green | **PASS** | `flutter test` (3.41.9, this worktree) = **3177 pass / 2 skip / 6 fail** — byte-identical totals to the base `60dc1bc6` measurement. All 6 failures are in ONE untouched file, `test/helper/destination_resolver_test.dart`. Targeted `pharmacy_home_composition_test.dart` = **20/20 pass**. Test edit is exactly minimal: base group had 9 `findsNothing`, now 8; the ONLY removed assert is the `CommonConditionView` one. | n/a |
| AC4 `[ui]` i18n keys pruned-or-noted | **PASS** | both `common_condition` and `no_product_available` present exactly once in each of `en/ar/bn/es.json` (4/4); zero remaining `.tr` call sites for either in `UserApp/lib`; the doc note exists in `docs/apps/userapp/userapp-screen-inventory.md` and states the actual reason (inert unused keys, `no_product_available` is generic, a 2-key ad-hoc prune is the wrong shape vs a scripted orphan sweep). | n/a (static) |

## Blast-radius / TL QA points
| # | Point | Result | Note |
|---|---|---|---|
| 1 | Pharmacy home renders unchanged, no gap | **PASS** | `PharmacyNearbyView` + `PharmacyOtcRailView` + FlashSale all mount. `PharmacyPrescriptionCta` self-hides — dev DB `business_settings.prescription_order_status = 0`, the widget's own documented gate. Not this diff; see drift. |
| 2 | Cold-start skeleton -> content | **PASS** | at t~0.3s all four headings render as skeletons; content fills in; no missing/extra skeleton. `ac2-coldstart-skeleton.png` |
| 3 | OTC rail still interactive | **PASS** | tapped "Cold & Flu" -> Cold & Flu category listing (Throat Lozenges / Cold Relief Tablets / Cough Syrup / Nasal Spray) with sibling tabs. `ac2-otc-tap-result.png` |
| 4 | Arabic / RTL Pharmacy home | **PASS** | switched to عربى; OTC chip rail lays out right-to-left (first chip at x 936-1041 of 1080), rails intact, zero `RenderFlex`/`overflowed` lines. `ac2-pharmacy-home-rtl-arabic.png` |
| 5a | Nothing-open -> `PharmacyUrgentFallbackView` | **PASS** | proxy `closed` mode: "No pharmacy is open right now — here's the nearest one" + MediQuick CLOSED. `ac2-nothing-open-fallback.png` |
| 5b | Store-load failure -> `NearsErrorRetry` | **PASS** | proxy `fail` mode + cold cache: "Couldn't load stores. Pull down to refresh." / "Please check your connection and try again" / Retry — **with a paired `[FAIL]` log**, no silent failure path. `ac2-store-load-failed-retry.png` |
| 6 | Shop home `ProductWithCategoriesView` | **UNVERIFIABLE LIVE** | `isShop` = `moduleType == AppConstants.ecommerce`; the dev DB has NO `ecommerce` module (only grocery/food/pharmacy/parcel), so `ShopHomeScreen` is unreachable. Not rounded to PASS. Static: the diff removed a *consumer* of `MedicineItemCard`/`MedicineCardShimmer`, never their definitions; both still compile with their surviving consumers, and `ProductWithCategoriesView` is present in the shipped kernel (probe = 6). |

## Regression sweep (bounded, 6 surfaces, all light mode)
Pharmacy home (en) · Pharmacy home (ar/RTL) · OTC category listing · Grocery home · Food home ·
Settings/Language. All render; runtime log scan clean across the whole sweep (`ac2-log-scan.log`).
