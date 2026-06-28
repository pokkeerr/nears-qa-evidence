# NEARS-621 QA progress (live, emulator-5554, zone1=Dhaka/zone2=AbuDhabi)
- Backend: worktree served on :8000 (oauth keys synced from primary). Endpoint GET /api/v1/search/unified 200 OK.
- BLOCKER FOUND: unified results list does not render. search_result_widget.dart:282 shrinkWrap ListView fails 'hasSize' paint assertion on EVERY search. Items(N)/Stores(M) headers show, rows blank, Stores section unpainted. Evidence: bug-blank-results-list.png/.log

## FINAL: FAIL
- PASS: AC1,2,3 (network single/debounce/min-char), AC7 (loading skeleton), AC8 (error+[FAIL]), AC13 (analytics)
- FAIL: AC4,5,6,9,12,14 ; UNVERIFIABLE: AC10,11 (blocked by render blocker)
- Task bugs: (1) BLOCKER results list hasSize paint @search_result_widget.dart:282 (2) stores gate module-scoped (3) widget tests false-green
- Regression: clean (idle chips, suggestions, popular cats, voice, filter)
- Comment posted id 11032. Gallery: github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-621
- Env restored: primary backend :8000; device lock released; app left Arabic/zone2.

## Cycle 2 RE-QA (2026-06-28, emulator-5554, build @8f2c3af4) — PASS
- TB-1 PRIMARY: organic/zone1 -> Items(3)+Stores(1) rows PAINT; milk/zone2 RTL -> Items(13) rows paint. runtime_errors CLEAN (no hasSize / RenderShrinkWrappingViewport paint assertion). FIXED.
- TB-2: chemist/zone2 Pharmacy(5-store module) -> Stores(1) City Care Chemist SHOWN (density gate removed); Items(0) "No items found". FIXED.
- TB-4: clear field -> idle (Last Search + Suggestions + Popular Categories); no stale Items/Stores header. FIXED.
- AC4 counts match; AC5 no-items; AC6 tiramisu/zone1 Food Items(3)+Stores(0)"No stores found"; AC9 See All 5->8 in place; AC10 item tap->detail; AC11 store tap->store; AC12 RTL mirrored + no_stores_found Arabic.
- AC1 single unified round-trip; AC2 debounce (1 unified call/commit); AC3 min-char (no unified at 1 char); AC7 skeleton wired (load <500ms, code-confirmed); AC8 error UI + paired [FAIL] log + Retry recovers; AC13 analytics search event PII-safe (Firebase debug-disabled).
- Regression: idle chips/suggestions/popular categories/filter sheet OK. 
- REGRESSION BUG (pre-existing, NOT 621): cart_count_view.dart:64 RenderFlex overflow 36px (44px-constrained quantity stepper); independent of unified search; search results render clean.
