# NEARS-4245 QA progress (HEAD 7fac88733, emulator-5554, own backend :8245, light mode, EN)
Evidence file: search-events-capture.log (search / search_results_load_more mirror lines + FA-SVC "Logging event" lines + the one induced [FAIL]).
Raw logcat not published (unscoped); typed terms used: zephyrtest, milk, ghee, fre, fr, desi (never present in any search event line).

- AC1 PASS: 8 module-Search submits (typed x4 incl. zero-result, history chip, suggestion, category tile): key set = result_count, store_count_returned, has_results, module_id, zone_id, screen, section, search_type, segment. 0 hits for search_term|typed_query|query_hash|typed strings.
- AC2 PASS: query "fr" (21 items, page size 20) scroll -> search_results_load_more {screen, section, page:2, trigger:scroll, segment:all, result_count:20}; no term.
- AC3 PASS: in-store search ghee -> {result_count:1, store_count_returned:0, has_results:1, module_id:1, zone_id:364}; zero-result -> has_results 0 still fires; empty submit -> error snackbar, no event; backend down -> [FAIL] items/search, no event.
- AC4 PASS: results, typeahead suggestion, recents list/chip, segments (Stores/Items), filter sheet (category Cheese 30 -> 3), dashboard Search tab; term reaches API (customer_search_logs rows ghee/fr/Dairy & Eggs, read-only SELECT).
- AC5 PASS (backstop): flutter test absence+analytics_service_test: +120 All passed.
- AC6 PASS: doc matches code and live shapes.
