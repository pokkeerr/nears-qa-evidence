# NEARS-543 — QA progress checkpoint (phase 8, fix-cycle 0)

Build: worktree `feat/NEARS-543-geolocator-nmea-crash` @ 72835ce3
Device: emulator-5556 (API 37), UserApp `com.izzes.nears` PID 30816, baseUrl http://10.0.2.2:8000

| AC | Status | Evidence |
|----|--------|----------|
| AC1 native-crash on physical API30+ | DEFERRED (user Option A) | emulator cannot exercise the native NMEA/Fused frame |
| AC2 emulator happy path | PASS | mock fix 24.4539/54.3773 resolved; geocode-api 200; address -> "F93G+HW4 - Al Manhal, Abu Dhabi"; no crash. `ac2-use-current-location-resolved.png` |
| AC3 document emulator behavior | PASS | case (a): forceLocationManager resolved real mock fix. case (b) location OFF: graceful fallback to config latlng (Dhaka), out-of-zone 404 logged correctly, no crash. `ac3-no-fix-graceful-fallback.png`, `ac3-graceful-fallback-logs.log` |
| AC4 no regression | PASS | manual map address entry reverse-geocodes on drag (625 Mohammed Bin Khalifa St); store discovery loads Abu Dhabi stores after location set. `ac4-pickmap-search.png`, `ac4-store-discovery-abudhabi.png` |

Automated backstop: `flutter test test/features/location/` -> 52/52 pass incl. 2 new buildLocationSettings pins.

Native crash sweep (NmeaClient/NewStringUTF/Null-check/SIGSEGV/FATAL/ANR): 0 hits across full session.

Regression (pre-existing, unrelated): payment-failed response parse _TypeError (WARN). `bug-payment-failed-parse-typeerror.log`

VERDICT: PASS (over AC2/AC3/AC4; AC1 DEFERRED)
