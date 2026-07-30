# NEARS-885 QA progress (fix-cycle 0)
Device: emulator-5556 (reclaimed dead-pid lock from NEARS-887). Worktree build.
- AC1 getZone removed (grep zero residual refs) — PASS
- AC2 ZoneResponseModel + zoneUri removed, ZoneData kept — PASS
- AC3 flutter analyze 4 pre-existing only (0 introduced); assembleDebug OK; app launched — PASS
- AC4 registration screen reached live; getZoneList() init fetch -> /api/v1/zone/list -> 200 live; dropdown gates on zoneList!=null (populated); loading-getter no-op confirmed by code — PASS
- Regression smoke: AddressController.loading permanently-false = no UI effect (dropdown reads zoneList; submit spinner reads authController.isLoading) — no stuck loader — clean
- Automated: flutter test 188 passed
- Pre-existing unrelated [FAIL]: record-location-data(null), update-fcm-token(403) on home dashboard — properly logged, not silent, unrelated to deletion
