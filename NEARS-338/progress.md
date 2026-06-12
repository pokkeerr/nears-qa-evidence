# NEARS-338 QA progress — 2026-06-11T20:41:10Z
- AC1 PASS: All Orders (history) fling-to-bottom → offset=1,2,3,4 each fired (app debugPrint '====> API Response: [200] /api/v1/customer/order/list?offset=N&limit=10' via logcat, observed 00:45:50/00:46:38/00:46:47/00:46:56); bottom shows oldest orders #1/#2/#3 → all 36 rendered. Shots 01,02.
- AC4 PASS: 5x jitter cycles + 2 extra flings at very bottom → offset counts remained exactly 1 each (1,2,3,4).
- AC2 PASS: scrolled to page-3 region; orders #23/#24/#25/#26 reachable; opened #25 -> detail "Delivered, Order #25" (full tracking timeline) and #26 -> "Delivered, Order #26". Shot 03.
- AC3 PASS (bounded by data): Ongoing chip renders single PENDING order #152, no crash, no spurious requests; page-2 live check N/A (account has 1 running order <10).  Shot 04.
- AC5 PASS: pull-to-refresh re-fired offset=1 (model reset); subsequent scroll re-paginated offset=2. Cancelled chip toggle THEN scroll (original bug path) → offset=3 @00:50:52, offset=4 @00:51:01, each once; filter active (cancelled-only cards) and applies over full loaded set (old canceled #21 from page 3 visible). Shots 05,06.
- SWEEP home (grocery) bottom stores list: PASS — get-stores offset=1,2 exactly once each (18 stores/limit 12), no errors. Shot 07.
- SWEEP store screen item list (Abu Dhabi Fresh Market, 15 items): PASS — items/latest store_id=8 offset=1,2 exactly once each. 
- SWEEP store item search: FAIL — REPRODUCED 2/2: fling through page boundary fires items/search offset=2 TWICE (00:58:18.792+00:58:21.679; again 01:03:42.910+01:03:45.182); second response double-appends page 2 -> user-visible DUPLICATE cards (Honey 500g rendered at y339 and y2257 same screen). Root cause: _PaginatedListViewState._paginate's optimistic _offsetList add is wiped by build() re-sync from stale widget.offset (model still page 1); scroll tick landing after _isLoading=false but before model-synced rebuild re-opens the guard; the new >=max-200 trigger window makes this race reachable (pre-change exact-equality could not refire after append). Shots 08,09,10.
- SWEEP flash-sale details: N/A — entry not reachable: FlashSaleViewWidget renders nothing on grocery home (zone 2) although GET /api/v1/flash-sales (zoneId [2], moduleId 1) returns active published sale id=1 with zone-2 items (215/251/186). Pre-existing; filed regression_bug.
- SWEEP chat list: PASS — Profile -> Talk to Nears! -> Conversation List loads message/list offset=1, renders 1 conversation, no errors. Conversation screen (reverse list): PASS load — message/details offset=1, 1 msg; older-messages page-2 N/A (seed has 1 message).
- Dark mode spot on orders: PASS — switch checked=true, My Orders renders dark surfaces/readable text/mint accents (shot 11), no errors.
- Automated backstop: flutter test (worktree UserApp) — 709 tests ALL PASSED (includes new paginated_list_view_test.dart).
- DTD get_runtime_errors: none for entire session.

# NEARS-338 DELTA re-QA (fix cycle 2) — 2026-06-12, emulator-5556, worktree @ c786be20 (fix 807ad296)
- REPRO ATTEMPT 1 PASS: store 8 (Abu Dhabi Fresh Market) in-store search name=a (15 results, Honey 500g on page 2) → fling through boundary + jitter: items/search offset=1 ONCE, offset=2 ONCE; Honey 500g rendered exactly 1x; ui_errors clean. Shot 12.
- REPRO ATTEMPT 2 PASS: full flow repeated (exit search, re-enter, new session): offset=1 ONCE, offset=2 ONCE; Honey 1x; no errors. Shot 13. Duplicate-fetch race NOT reproducible post-fix (was 2/2 repro pre-fix).
- ORDERS SMOKE history fling PASS: order/list offset=1,2,3,4 each fired EXACTLY once; bottom = oldest #1/#2/#3 (36 history orders, total_size:36 in response, DB cross-check 25 delivered+11 canceled). Extra bottom flings refire NOTHING. Shot 14.
- ORDERS SMOKE pull-to-refresh PASS (risky edge): refresh re-fired offset=1 once (session reset); subsequent scroll RE-paginated offset=2,3,4 each exactly once back to oldest #1. No duplicate fetches, no stuck pagination.
- ORDERS SMOKE Cancelled toggle PASS: refresh-to-page-1 then Cancelled chip then scroll (original bug path) → offset=2,3 fired once each; cancelled-only cards incl. old #21 from a later page; 0 non-cancelled leak; ui_errors clean. Shot 15.
- SWEEP home stores list (zone 2 grocery, "18 stores near you", limit 12) PASS: get-stores/all offset=1 and offset=2 each fired exactly once across the page boundary; ui_errors clean. Shot 16.
- SWEEP chat page-2: N/A — seed unchanged since cycle 0 (1 conversation, 1 message; DB read-only check); page-2 unreachable, same Data-DoR note as cycle 0.
- Automated backstop: flutter test (worktree UserApp @ c786be20) — 711 tests ALL PASSED (709 prior + 2 new race-repro/session-reset tests from 807ad296).
- DTD get_runtime_errors over the whole delta session: ONE pre-existing rendering error — RenderFlex overflowed by 25px right in lib/common/widgets/item_shimmer.dart:59 (loading-skeleton Row; last touched 06cb996c, NOT in NEARS-338 diff) → regression_bug lane, does not affect verdict.
- DELTA VERDICT: PASS — duplicate-fetch race fixed (0/2 repro, was 2/2); orders pagination + refresh-reset + Cancelled-toggle clean; home sweep clean.
