# NEARS-1016 QA progress (live checkpoints)

- setup: emulator-5556 (Pixel_10_Pro_2), lock acquired, worktree UserApp launched pid 43522, backend :8000 (primary tree, zero Admin delta), signed in customer@nears.com, zone-1 home populated. Logs clean so far.
- AC1 cold x3 / warm x3 / tab x3 / addr x3 recorded (cold1-3,warm1-3,tab1-3,addr1-3.mp4), end-state header OK each; AC4 ptr3 refetch proven (banners/module/stores NET). Consolidated log-verified pass all 4 paths: ZERO ERR/FAIL. ui_errors tooling gap found (threadtime format no-op).
- Detector v2 final: 0 empty-state frames across all in-zone videos (~19.6k frames); positive controls fire correctly. AC2 shimmer arcs proven (zoneswitch12 f163-275, rtl cold f557-588). AC3 via prefs-seeded out-of-zone stored location (debug run-as, device-local, no DB writes): settles empty + persists PTR/warm/cold + recovers. NEARS-960 zone-3 cold OK. Airplane OK w/ correct [FAIL] logging. RTL OK. flutter test running.
