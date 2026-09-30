# NEARS-3937 QA progress (cycle 0) - emulator-5562 (Pixel_10_Pro_2 spare AVD), build 16d8bcbad debug
Backend: /Users/Apple/Projects/nears-NEARS-3937-total-unresolved-state @ 16d8bcbad (DB nears_qa_3937 copy)

- AC1 group surge failed: breakdown rows '—' + Retry/Edit Cart, sticky '—', site4 '—', Place Order disabled - PASS
- AC1 group pending (paused Retry): fee rows + Total skeleton, Place Order disabled - PASS (screenshot; uiautomator cannot dump during shimmer)
- AC1/AC2 group one store failed (store 1 zone 999999): Corner 1.00 resolved, Nears Mart failed, Total '—' (not 73.31) - PASS
- AC1 site3 Due Payment (partial pay, wallet 10): failed '—' at bill + sticky, pending skeleton, resolved 64.31 - PASS
- AC3 group: orders 91418 (43.78) + 91419 (30.53) = 74.31 == displayed Grand Total - PASS
- AC1 (a) single quote failed (module_zone renamed): fee row Retry, Total '—', site4 '—'; pending skeleton; server killed + Retry logs; restart + Retry -> 43.78 - PASS
- AC2 stale reset: re-entry frames never show prior 43.78 (skeleton -> '—') - PASS
- AC1 (b) single surge failed: fee row Retry, Total '—' - PASS; self-delivery-1 control shows real 53.78 - PASS
- AC1/AC2 (c) never-scheduled (proxy nulls store zone_id): fee row Retry (no '+ -1'), Total '—'; log once per entry; 3 taps -> 3 retry lines - PASS
- Layout 320dp x1.3 EN+AR: sticky row clean + RTL correct; fee-row failed shape overflows (pre-existing, NEARS-3877) - regression lane
- Site5 storeId (prescription) COD row: failed '—' + resolved 1.00 - PASS
- (e) single-row group + no-address group: not reachable on device -> unit pins
- AC3 single: order 91420 order_amount 43.78 == displayed Total - PASS
- Backstop: flutter test test/features/checkout -> 1198 passed, 0 failed
