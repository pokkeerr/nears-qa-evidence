# AC3 nets: 107 invocations, all rc=0, ONE FILE PER INVOCATION under mem-guard (--label s5qa --max-gb 6), /Users/Apple/Tools/flutter/bin/flutter test, on the tested worktree f694d1ac5
# list = engineer log section (e) table + the 3 new tests (107 rows; the share baseline file twice, second with --dart-define=WEB_HOSTED_URL=https://share-host.invalid); superset check: all 51 *_test.dart under UserApp/test that mention a moved name (grep -w) are in the list (0 missing)
# columns: n, file, define, rc, last progress line
1	baseline/store/store_catalog_requests_baseline_test.dart		rc=0	+16: All tests passed!
2	baseline/store/store_facade_scope_baseline_test.dart		rc=0	+11: All tests passed!
3	baseline/store/store_pagination_triggers_baseline_test.dart		rc=0	+12: All tests passed!
4	baseline/store/store_screen_load_order_baseline_test.dart		rc=0	+11: All tests passed!
5	baseline/store/store_screen_open_failures_baseline_test.dart		rc=0	+13: All tests passed!
6	baseline/store/store_discovery_lists_baseline_test.dart		rc=0	+20: All tests passed!
7	baseline/store/store_availability_edge_fixtures_baseline_test.dart		rc=0	+24: All tests passed!
8	baseline/store/store_availability_weekday_matrix_baseline_test.dart		rc=0	+10: All tests passed!
9	baseline/browse/category_facade_scope_baseline_test.dart		rc=0	+10: All tests passed!
10	baseline/browse/category_screen_scroll_trigger_baseline_test.dart		rc=0	+13: All tests passed!
11	baseline/browse/category_selection_sequence_baseline_test.dart		rc=0	+13: All tests passed!
12	baseline/browse/home_module_fanout_baseline_test.dart		rc=0	+17: All tests passed!
13	features/store/store_offers_chip_test.dart		rc=0	+10: All tests passed!
14	features/store/store_grid_error_retry_test.dart		rc=0	+10: All tests passed!
15	features/store/store_catalog_states_test.dart		rc=0	+10: All tests passed!
16	features/store/load_more_failure_part2_test.dart		rc=0	+11: All tests passed!
17	features/store/store_availability_policy_test.dart		rc=0	+92: All tests passed!
18	features/store/store_repository_error_flags_test.dart		rc=0	+6: All tests passed!
19	features/store/store_repository_zone_scoped_header_test.dart		rc=0	+10: All tests passed!
20	features/store/store_controller_distance_single_read_test.dart		rc=0	+11: All tests passed!
21	features/store/store_screen_search_controller_dispose_test.dart		rc=0	+1: All tests passed!
22	architecture/smart_management_only_builder_test.dart		rc=0	+10: All tests passed!
23	baseline/golden_manifest_check_test.dart		rc=0	+5: All tests passed!
24	baseline/store/store_share_baseline_test.dart		rc=0	+3 ~2: All tests passed!
25	baseline/store/store_offers_family_characterization_baseline_test.dart		rc=0	+33: All tests passed!
26	features/store/store_controller_test.dart		rc=0	+60: All tests passed!
27	features/store/store_controller_nearest_fallback_test.dart		rc=0	+6: All tests passed!
28	features/store/store_controller_open_first_pagination_test.dart		rc=0	+2: All tests passed!
29	features/store/nearest_store_origin_test.dart		rc=0	+5: All tests passed!
30	features/store/all_store_screen_error_retry_test.dart		rc=0	+4: All tests passed!
31	features/store/all_store_veg_chip_gate_test.dart		rc=0	+2: All tests passed!
32	features/store/load_more_failure_part1_test.dart		rc=0	+8: All tests passed!
33	features/store/load_more_failure_part3_test.dart		rc=0	+3: All tests passed!
34	features/store/store_offers_owner_test.dart		rc=0	+26: All tests passed!
35	features/store/store_offers_facade_wiring_test.dart		rc=0	+15: All tests passed!
36	features/store/store_offers_extraction_source_scan_test.dart		rc=0	+11: All tests passed!
37	features/load_more_error_rows_test.dart		rc=0	+10: All tests passed!
38	features/search/search_result_widget_test.dart		rc=0	+23: All tests passed!
39	common/widgets/item_view_body_retry_test.dart		rc=0	+2: All tests passed!
40	common/widgets/item_view_sliver_retry_test.dart		rc=0	+2: All tests passed!
41	common/widgets/item_view_favourites_uiux_test.dart		rc=0	+12: All tests passed!
42	features/splash/module_controller_part3_test.dart		rc=0	+30: All tests passed!
43	features/splash/module_controller_remove_module_header_test.dart		rc=0	+8: All tests passed!
44	baseline/launch_module/module_select_entries_baseline_test.dart		rc=0	+36: All tests passed!
45	golden/baseline_home_golden_test.dart		rc=0	+15: All tests passed!
46	features/home/all_store_filter_fastest_chip_test.dart		rc=0	+3: All tests passed!
47	features/home/all_store_filter_nearest_chip_test.dart		rc=0	+5: All tests passed!
48	features/home/all_store_filter_open_count_test.dart		rc=0	+2: All tests passed!
49	features/home/all_store_filter_row_height_test.dart		rc=0	+5: All tests passed!
50	features/home/buy_it_again_cold_cache_test.dart		rc=0	+4: All tests passed!
51	features/home/buy_it_again_module_switch_test.dart		rc=0	+1: All tests passed!
52	features/home/filter_view_sheet_test.dart		rc=0	+4: All tests passed!
53	features/home/food_home_composition_test.dart		rc=0	+26: All tests passed!
54	features/home/grocery_home_composition_test.dart		rc=0	+15: All tests passed!
55	features/home/home_controller_cold_open_salvage_test.dart		rc=0	+4: All tests passed!
56	features/home/home_controller_flash_sale_gate_test.dart		rc=0	+10: All tests passed!
57	features/home/home_controller_load_data_catch_test.dart		rc=0	+5: All tests passed!
58	features/home/home_controller_module_toctou_guard_test.dart		rc=0	+19: All tests passed!
59	features/home/home_controller_pin_test.dart		rc=0	+6: All tests passed!
60	features/home/home_controller_rental_no_gate_test.dart		rc=0	+7: All tests passed!
61	features/home/home_pinned_filter_header_budget_test.dart		rc=0	+3: All tests passed!
62	features/home/module_home_unserviceability_contract_test.dart		rc=0	+3: All tests passed!
63	features/home/module_view_single_module_spinner_test.dart		rc=0	+5: All tests passed!
64	features/home/pharmacy_home_composition_test.dart		rc=0	+21: All tests passed!
65	features/home/popular_store_view_closed_filter_test.dart		rc=0	+1: All tests passed!
66	features/home/single_store_hero_view_test.dart		rc=0	+6: All tests passed!
67	baseline/store/store_discovery_family_characterization_baseline_test.dart		rc=0	+72: All tests passed!
68	features/store/store_discovery_owner_test.dart		rc=0	+61: All tests passed!
69	features/store/store_discovery_facade_wiring_test.dart		rc=0	+17: All tests passed!
70	features/store/store_discovery_extraction_source_scan_test.dart		rc=0	+16: All tests passed!
71	features/store/store_catalog_tab_width_cap_test.dart		rc=0	+4: All tests passed!
72	features/store/store_screen_fab_scoped_rebuild_test.dart		rc=0	+4: All tests passed!
73	features/store/store_list_analytics_context_test.dart		rc=0	+1: All tests passed!
74	features/store/store_item_search_overflow_test.dart		rc=0	+6: All tests passed!
75	features/store/store_search_states_test.dart		rc=0	+5: All tests passed!
76	features/store/store_filter_nfilterchip_toggle_test.dart		rc=0	+2: All tests passed!
77	features/store/store_screen_cart_bar_test.dart		rc=0	+3: All tests passed!
78	features/store/store_details_distance_priming_test.dart		rc=0	+4: All tests passed!
79	features/store/store_details_get_notify_test.dart		rc=0	+3: All tests passed!
80	features/store/store_details_malformed_body_test.dart		rc=0	+12: All tests passed!
81	features/store/store_details_shimmer_test.dart		rc=0	+3: All tests passed!
82	features/search/search_load_more_controller_test.dart		rc=0	+15: All tests passed!
83	features/search/search_load_more_widget_test.dart		rc=0	+11: All tests passed!
84	baseline/flow/store_to_checkout_flow_baseline_test.dart		rc=0	+1: All tests passed!
85	baseline/item/item_catalog_list_search_reads_baseline_test.dart		rc=0	+52: All tests passed!
86	baseline/item/item_catalog_list_survivors_search_flag_baseline_test.dart		rc=0	+8: All tests passed!
87	baseline/item/item_catalog_lists_baseline_test.dart		rc=0	+23: All tests passed!
88	baseline/item/item_entry_points_search_cart_baseline_test.dart		rc=0	+10: All tests passed!
89	baseline/item/item_facade_scope_baseline_test.dart		rc=0	+16: All tests passed!
90	baseline/item/item_filter_notification_order_baseline_test.dart		rc=0	+12: All tests passed!
91	baseline/search/search_history_baseline_test.dart		rc=0	+16: All tests passed!
92	baseline/search/search_result_item_tap_baseline_test.dart		rc=0	+4: All tests passed!
93	baseline/search/search_result_states_baseline_test.dart		rc=0	+4: All tests passed!
94	baseline/search/search_suggestion_supersede_baseline_test.dart		rc=0	+9: All tests passed!
95	baseline/search/search_voice_baseline_test.dart		rc=0	+15: All tests passed!
96	baseline/store/store_catalog_family_characterization_baseline_test.dart		rc=0	+92: All tests passed!
97	common/widgets/paginated_list_view_test.dart		rc=0	+15: All tests passed!
98	features/category/category_controller_part1_test.dart		rc=0	+34: All tests passed!
99	features/category/category_controller_part2_test.dart		rc=0	+20: All tests passed!
100	features/category/category_grid_error_retry_test.dart		rc=0	+17: All tests passed!
101	features/global_search/global_suggestions_controller_test.dart		rc=0	+16: All tests passed!
102	features/search/search_screen_idle_filter_icon_test.dart		rc=0	+6: All tests passed!
103	features/search/search_suggestions_also_found_test.dart		rc=0	+17: All tests passed!
104	baseline/store/store_share_baseline_test.dart	--dart-define=WEB_HOSTED_URL=https://share-host.invalid	rc=0	+2 ~3: All tests passed!
105	features/store/store_catalog_owner_test.dart		rc=0	+46: All tests passed!
106	features/store/store_catalog_facade_wiring_test.dart		rc=0	+30: All tests passed!
107	features/store/store_catalog_extraction_source_scan_test.dart		rc=0	+25: All tests passed!
NETS_DONE

# the 2 declared structural pins (bumped by the engineer, run unmodified by me): store_offers_extraction_source_scan_test +11 rc=0; store_discovery_extraction_source_scan_test +16 rc=0
# test files modified base..tested (git diff --name-status): only those 2 (M); all others A
A	UserApp/test/baseline/mutation-logs/NEARS-3996-step5.md
A	UserApp/test/baseline/store/store_catalog_family_characterization_baseline_test.dart
A	UserApp/test/baseline/support/store_catalog_support.dart
A	UserApp/test/features/store/store_catalog_extraction_source_scan_test.dart
A	UserApp/test/features/store/store_catalog_facade_wiring_test.dart
A	UserApp/test/features/store/store_catalog_owner_test.dart
M	UserApp/test/features/store/store_discovery_extraction_source_scan_test.dart
M	UserApp/test/features/store/store_offers_extraction_source_scan_test.dart

# the 2-file diff is exactly: literals 39->34, 42->37, 46->41 + title/reason/comment text (see below)
+//       Step 5 (StoreCatalogOwner): 34 = 39 - 6 moved + 1 port bridge.
-    test('control: the update() scan reads ids and skips a declaration; then no update id was added (base 48 id-less + 3 fab; tip 39 + 3 fab in the controller, 10 id-less in the owner, one of the 39 is the new port bridge)', () {
+    test('control: the update() scan reads ids and skips a declaration; then no update id was added (base 48 id-less + 3 fab; tip 34 + 3 fab in the controller, 10 id-less in the owner, one of the 34 is the step-4 port bridge)', (
-      expect(ctl.where((String a) => a.isEmpty).length, 39);
+      expect(ctl.where((String a) => a.isEmpty).length, 34);
-      expect(ctl.length, 42, reason: 'no other argument shape');
+      expect(ctl.length, 37, reason: 'no other argument shape');
-      // 39 + 10 - 1 = 48 is the base id-less count measured on the base lib (not an independent check); the port bridge itself is pinned by the wiring test's id-less update counts.
+      // 39 + 10 - 1 = 48 was the step-4 base id-less count; step 5 moved 6 more to StoreCatalogOwner and added its port bridge (34 = 39 - 6 + 1); 48 is the count measured on the base lib (not an independent check); the port brid
-    test('control: the update() scan reads ids and skips a declaration; then no update id was added (base 55 id-less + 3 fab; tip 39 + 3 fab in the controller, 8 id-less in the owner, two of the 39 are port bridges)', () {
+    test('control: the update() scan reads ids and skips a declaration; then no update id was added (base 55 id-less + 3 fab; tip 34 + 3 fab in the controller, 8 id-less in the owner, three of the 34 are port bridges)', () {
-      expect(ctl.where((String a) => a.isEmpty).length, 39);
+      expect(ctl.where((String a) => a.isEmpty).length, 34);
-      expect(ctl.length, 42, reason: 'no other argument shape');
+      expect(ctl.length, 37, reason: 'no other argument shape');
-      expect(ctl.where((String a) => a.isEmpty).length + own.length - 1, 46, reason: 'step-3 base id-less count 55, minus the 10 moved to StoreDiscoveryOwner in step 4, plus its port bridge (55 - 10 + 1)');
+      expect(ctl.where((String a) => a.isEmpty).length + own.length - 1, 41, reason: 'step-3 base id-less count 55, minus the 10 moved to StoreDiscoveryOwner in step 4 and the 6 moved to StoreCatalogOwner in step 5, plus their tw
