# NEARS-469 QA progress (live)
device: emulator-5556 | branch: feat/NEARS-469-default-address-autoselect | sha: e137b0e4

## AC2 PASS (2026-06-27)
- Setup: logged-in session (secure-storage token) + 6ammart_user_address cleared; GPS=zone2(AbuDhabi).
- Cold launch -> auto-selected id=46 "Demo Zone — Dhaka" (zone1, highest id), NO "Hey Welcome Back" sheet.
- Log: get-zone-id?lat=23.81796&lng=90.36602 (id=46 coords) inZone=true; sectors_shown zone_id:1; handleRoute canRoute=false.
- Home: zone1 stores (Fresh Mart Grocery, Nears Mart, Organic Paradise); nav+running-order banner present.
- ui_errors clean, no [FAIL]/[ERR]. Shot: ac2-autoselect-zone1.png
- Note: literal "clear ALL app data + login" routes via access-location GPS resolve (existing fresh-login path, unchanged); the new auto-select branch fires for returning logged-in user w/ empty active address (reproduced by clearing only the addr pref, keeping session).

## AC4 PASS — tap "Deliver To: Home" bar -> "Set Location" picker opened (both saved addrs + Use Current Location + Set From Map). Logs clean. Shot: ac4-picker-opens.png
## AC6 PASS — picked id=45 Abu Dhabi -> get-zone-id lat24.45/lng54.37 inZone=true, update-zone; header "Deliver To: Home / Abu Dhabi"; zone2 stores (AbuDhabi Fresh Market id8, Organic Shop id9, Spice Route id49, Golden Wok id51 all zone_id=2). zone1 earlier = ids1/2/3. ui_errors clean. Shot: ac6-zone2-stores.png. DRIFT: spec zone2 range "8-23/30-34" incomplete (49/51 also zone2).

## AC1 PASS (core repro) — persisted active addr id=45 (Abu Dhabi). GPS set to London (-0.1276,51.5074) far from saved.
- Cold relaunch: NO "Hey Welcome Back" sheet/Scrim. Splash log: "route: initial route module=null" direct (hasUsableActiveAddress suppression path; no addr/list fetch, no GPS lookup at routing).
- Home zone-refresh used lat=24.453884&lng=54.3773438 (id=45 Abu Dhabi coords) NOT London -> persisted addr drives it, not GPS (bonus proven).
- Header "Deliver To: Home / Abu Dhabi"; zone2 stores; nav+banner present. ui_errors clean. Shot: ac1-remembered-no-sheet.png

## AC5 PASS — james.wilson@demo.com (0 saved in DB, confirmed)
- (a) NO DEAD-END: splash _forLoggedInUserRouteProcess -> empty persisted -> resolveLaunchLocationFromSavedAddresses -> address/list [200] empty -> needsManualPick -> navigateToLocationScreen('splash').
  - With in-zone GPS (Abu Dhabi): auto-resolved to home (no errors). Shot: ac5-location-set-home.png
  - With out-of-zone GPS (London): recovered to "Pick Location" map screen (manual pick flow), NOT blank/stuck. Shot: ac5-pick-location-no-deadend.png
  - The [FAIL] get-zone-id 404 in the London case = EXPECTED out-of-zone (deliberately induced), logged PII-safe per contract (endpoint path, ApiFailure sentinel, correlation_id), correctly recovered. NOT a defect, not NEARS-469 code.
- (b) SAVE-LOCATION FUNCTIONAL: Set Location screen shows "No saved address found" + Set From Map/Use Current Location; Set From Map -> Pick Location set the delivery location (Deliver To: Others) and returned home. No blank/stuck. Logs clean (get-zone-id 200 inZone=true, address/list 200, ui_errors empty).
- NOTE: actual checkout Place Order not exercisable at test time (~02:54; all zone stores closed until 08:00) — store-hours limit, unrelated to NEARS-469.

## AC3 PASS (best-effort, repro via shared-pref injection, NOT code injection)
- Corrupted 6ammart_user_address JSON ("id":null -> "id":nXll => unparseable).
- Cold relaunch: [WARN] msg="cached location parse failed: FormatException" (PII-safe, runtimeType only) x N; NO crash/[FAIL]/[ERR]/EXCEPTION/RangeError.
- getUserAddressFromSharedPref try/catch -> null -> fell through (needsManualPick -> navigateToLocationScreen -> in-zone GPS -> home). No blank, NO forced "Hey Welcome Back" picker. Shot: ac3-malformed-cache-fallthrough.png
- The [WARN] is deliberately-induced contract-compliant defensive logging, not a logs-first FAIL.
