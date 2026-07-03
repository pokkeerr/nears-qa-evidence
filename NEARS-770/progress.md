# NEARS-770 QA progress (device emulator-5560, worktree HEAD a8486f79)

- AC1 (valid deep link resolves + [INFO] no URI): PASS (live)
  evidence: [INFO] msg="deep link stream event, hasPrevious=false"; navigated to Refer&Earn; REFTEST123 x0 in app log
- AC2 (malformed link onError [FAIL] type-only, no URI, no crash): PASS (live + tests)
  evidence: [FAIL] type=DeepLinkStreamFailure msg="deep-link: initAppLinksStream error (FormatException)"; sentinel-only Crashlytics echo; REFTEST123 x0; pid alive
- AC3 (API [NET] path-only, single occurrence): PASS (live)
  evidence: [NET] endpoint=/api/v1/search/unified http_status=200 (x1), order/track + get-zone-id path-only (query stripped)
- Automated: flutter test 2 files -> 13/13 pass
- Regression: ~20+ endpoints across module/search/deeplink/order surfaces, all 200 path-only, zero [FAIL]/[ERR]
- Followup(non-blocking): app_links plugin native Log.d prints raw URI at Android layer (3rd-party, not app code, not Crashlytics)
