# QA progress — NEARS-674 + NEARS-681 (feat/NEARS-674-loc-log-parse @790cfc1a, emulator-5554, light mode)
- backstop: flutter test test/features/location/ test/features/address/ -> 98 passed (incl. new zone-logging + numeric-parse tests)
- 681 AC1: PASS — fresh no-cache cold boot, 0 "cached user location parse failed" WARN; no userAddress key in prefs
- 674 AC1: PASS — cached lat/lng=0 -> home -> getZone(0,0) 404 -> [INFO] "no zone for empty coords" x2, 0 [FAIL] for get-zone-id, 0 Crashlytics
- 674 AC5: PASS — pick-map Abu Dhabi Mall -> getZone 200 inZone=true -> Login/Sign Up sheet -> login customer@nears.com -> home loaded w/ Abu Dhabi stores
- 674 AC3: PASS — real-coords (Dhaka 23.788) getZone 404 -> [FAIL] /get-zone-id (correlation_id) STILL fires; airplane transport -> [FAIL] config/cart/banners/module/stores
- 681 AC2: PASS — cached zone_ids=[2.0] double -> cold boot, 0 parse-fail WARN, getZone 200 inZone=true, zone-scoped Abu Dhabi stores, home loaded
- regression sweep: CLEAN — store profile renders (items/discount), no [FAIL]/[ERR]/EXCEPTION/overflow/parse-failed
- FOLLOWUP (regression_candidate, pre-existing): sibling getString(userAddress)! force-unwrap survives in language_repository.dart:19 (observed [WARN] _TypeError on no-cache boot), header_helper.dart:14, auth_repository.dart:148
