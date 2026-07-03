# NEARS-723 QA progress checkpoint
device: emulator-5556 (Android) | branch fix/NEARS-723-guest-loader | worktree nears-NEARS-723-guest-loader
- automated backstop: flutter test test/features/checkout/ => 119/119 PASS; new guest-loader file 3/3 PASS
- preflight: baseUrl=http://10.0.2.2:8000 (real local backend, up). App booted from worktree on emulator-5556, pid 1838, ZERO runtime errors, clean [FAIL]/[ERR] logs.
- BLOCKER on live guest UI: business_settings guest_checkout_status=0 -> GuestDeliveryAddress unreachable live (checkout_screen.dart:229-231 gate). NOT mutating shared DB (read-only rule). Data/config DoR gap.
- Live getZone proof: in-coverage 200 zone_id[400,2] (success path); out-of-coverage 404 "Service not available" (the stuck-loader failure branch). Both real+reproducible.
- AC1 loader-closes-on-failure: widget test drives REAL GuestDeliveryAddress, asserts Get.isDialogOpen==false after getZone failure => PASS (test+codepath+live-endpoint).
- AC2 success no double-pop: code-path (single Get.back() in finally pops only dialog route) => PASS.
- AC3 empty-zone no RangeError: widget test takeException()==null, loader closes once => PASS.
- AC4 TypeAhead onSelected empty-zone: widget test no RangeError, seeds addr zoneId=0 => PASS.
- AC6 map onPicked regression: 2 onPicked builders guard isNotEmpty (code-path) + zone_guard guest map-pick tests green.
