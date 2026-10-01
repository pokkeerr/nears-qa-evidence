# NEARS-1527 QA progress (phase 8, cycle 0)
- AC2 (zero-order sophie id 4, pre-staging): All=No orders yet + Shop Now [SELECTED All]; Ongoing=No ongoing orders (no Shop Now); Cancelled=No cancelled orders (no Shop Now). Logs: only expected Firebase-absent [FAIL]s (no google-services.json), no order-list [FAIL]/[ERR]. PASS
- Staged on nears_qa_1527: #167(processing)+#168(canceled) -> user 4. API proof on :8131: user 4 list=[168], running=[167] (copy-only data). Shared DB 167/168 still user 1 canceled.
- Cell1 Cancelled: "No cancelled orders" (not blank, no group card). PASS
- Cell2 All: "No orders yet" + Shop Now; Shop Now -> home (module home, Active Orders #167). PASS
- Cell3 date filter 3 Jul-1 Oct (matches #168): All + Cancelled -> "No results found" + Clear Filter; Clear Filter -> chip resets, unfiltered empty state. filter_empty_result fired 3x over All->Cancelled->Ongoing->Cancelled->All (once per distinct-tab entry, signature guard pre-existing NEARS-3655), no per-rebuild fire. PASS
- Cell4 Ongoing: ONE group card "Orders from multiple stores"; expanded #167 PROCESSING (orange), #168 CANCELLED (red error tone); View details #168 -> Order #168 screen, details 200. PASS
- Cell5/AC3 live: staged emily (id 2) on copy: 7 in-flight groups (one child kept pending/picked_up, rest canceled = 10 canceled children = page 1), + 15 oldest delivered orders of user 6 (ids 1-14,16) -> history total 25. API: offset1 = 10 group children, offset2 = #16..#6. App All tab: renders #16,#14,#13,#12... (page-2-only data) with exactly 2 GET /order/list; scroll -> 3rd GET and #5..#1 render (page-3-only data). No repeated offset-2 fetch. Cancelled = "No cancelled orders" after all pages; Ongoing = 7 group cards + 2 plain. PASS
- Cell8 james (id 1, unstaged after 167/168 moved): Cancelled shows ordinary cards (#91415, #91412, #91411...) + fully-cancelled group 30ba64b6 as ONE "Orders from multiple stores" card; All tab renders cards. No [FAIL]/[ERR]. PASS
- Cell3 module filter (emily, Cancelled, Grocery = only the 10 canceled in-flight children): "No results found" + Clear Filter; filter_empty_result fired once; Clear Filter -> "No cancelled orders". Fresh Cancelled entry: 3 GET /order/list (pages 1-3) then empty state. PASS
- Cell6 failed auto page fetch: not run live (optional); unit-pinned by test (f).
- Cell9 logging: no AppLogger line for unfiltered empty state; no 'order list auto page fetch failed'; only [FAIL]s are environmental Firebase/FCM (no google-services.json in worktree, by design). PASS
- Backstop: flutter test test/features/order/ -> 468/468 pass.

## Fix cycle 1 delta re-QA (build 4cee98c25, 2026-10-01, emulator-5600, backend primary Admin a3f6ce491 DB_DATABASE=nears_qa_1527 :8131 via QA delay proxy :8141)
- (a) AC1 sophie: All = "No orders yet"+Shop Now; Cancelled = "No cancelled orders"; Ongoing = group card, expanded #167 PROCESSING + #168 red CANCELLED badge (fc1-a-sophie-ongoing-group-168-badge.png). PASS
- (a) AC3 emily: All: GET list p1 (all hidden in-flight group members) -> exactly one auto p2 -> #16..#6 render; Cancelled: one p3 -> "No cancelled orders". PASS
- (b) emily, proxy held list?offset=2 12s: p2 #75 (list A) in flight 703.98-716.26; exit+re-enter My Orders -> p1 #77 replaced list at 710.96; #75 returned AFTER (superseded); list B p2 #79 returned 724.19. Rendered ids top->bottom 16,14,13,12,11,10,9,8,7,6,5,4,3,2,1 each once; no Retry/error node; next scroll -> one p3. (fc1-b-all-after-superseded-top-a11y.xml). PASS
- (f) during (b): no 'order list auto page fetch failed', no 'paginated list:' warn, no retry row. PASS
- (d) emily All (p3 by scroll): after pull-to-refresh x2 (each p1 -> one auto p2, sequential), scroll -> exactly one p3; ids 16..6,5..1 contiguous once each. PASS (james literal p2-by-scroll run follows)
- (c) james (12 running, 2 Ongoing pages): Home (rail limit=50 #133, 12 ids) -> My Orders (own limit=10 #200) -> Ongoing scroll -> one p2 (#202 172,171): 10 single cards + 1 group card (91110+91111), each id once = DB 12. Variant: dashboard limit=50 held 15s (#203) landed AFTER p2 (#206) -> dropped, still each id once. PASS
- (d) james All: p2 by scroll (#207 -> 91400); pull-to-refresh (offset=1 #208-#213); scroll -> p2 requested again (#214), 91400 present. PASS
- (e) staging on COPY: UPDATE orders SET user_id=2 WHERE id IN (91124..91127) (robert id5 -> 0 orders).
- (e) robert (0 orders on copy): All "No orders yet"+Shop Now, Ongoing "No ongoing orders", Cancelled "No cancelled orders"; one p1 each, no page>1. PASS
- (g) no stacking: every auto/scroll page request dispatched only after the prior one for the same list ended (AC3 p2 then p3; (b) one p2 per list A/B; (c)/(d) single p2). PASS
- Backstop: flutter test test/features/order/ test/common/widgets/paginated_list_view_test.dart -> 491 pass. DELTA VERDICT: PASS
