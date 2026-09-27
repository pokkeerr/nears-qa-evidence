# NEARS-3793 QA progress (fix_cycle 0) — emulator-5568, build com.izzes.nears.nears_nears_3793_unserved_copy from c0bc35369
- AC1 EN pick-map: PASS — Dubai → 5 rows "…, Not available yet" enabled=false; header "No service in these locations yet"; 0 "Outside your current area" (ac1-ac7-en-dump.xml, ac1-en-pickmap-unserved.png)
- AC1 dialog list: SOURCE-VERIFIED — LocationSearchDialogWidget's only live caller (select_location_view_widget.dart:442) passes filterServiceableZone=false → badge/header branch unreachable; pin test covers source
- AC2 AR: PASS — "غير متاح بعد" x5, header "الخدمة غير متوفرة في هذه المواقع بعد" (ac2-ac6-ar-dump.xml); native check pending owner
- AC3 served: PASS — Abu Dhabi mixed: Available rows enabled=true, selection sets field; pending state not live-capturable (resolves <1.2s) → widget test search_location_widget_test NEARS-3761 group passed
- AC4 saved address: PASS live (AR) — michael.brown Dhaka address shows "خارج منطقتك الحالية" (ac4-ar-saved-addresses.png)
- AC6 RTL: PASS — badges at end, description ellipsized, no overflow in logcat (ac2-ac6-ar-rtl-pickmap-unserved.png)
- AC7 semantics: PASS — content-desc ends ", Not available yet" / ", غير متاح بعد"
- AC print/orphan: PASS — diff has no print/AppLogger lines; old header value fully replaced in en/ar
- Automated: flutter test test/features/location/ → 364 passed
