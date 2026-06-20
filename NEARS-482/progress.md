# NEARS-482 QA progress (checkpoint log)
- Device: emulator-5554 (lock held)
- Backend: 127.0.0.1:8000 (200), queue:work running
- baseUrl: http://10.0.2.2:8000 (local, useHttps=false) — PASS pre-flight
- Automated backstop: flutter test api_client_utf8_decode_test.dart -> 6/6 PASS
- Wire-encoding finding: backend \u-escapes ALL non-ASCII (rawHighBytes=0); Latin-1==UTF-8 output on escaped data

## Live observations (checkpoint)
- Home banner EN (zone 2): app-rendered title "Organic Shop"/"Abu Dhabi Fresh Market", "LIMITED OFFER", "Claim Deal" all CLEAN (01-home-banner-en.png). AC1 app-layer text = clean.
- AC3 finding: reskinned _PhotoHeroCard (banner_view.dart) is a clean Column [badge -> headline Text -> Claim Deal], NO app-rendered subtitle. NO app-layer z-overlap.
- ROOT-CAUSE FINDING: the mojibaked "Save big this week â  Organic Shop" monospace text is BAKED INTO the backend banner PNG (storage/banner/d-ecc510bd18.png), NOT app-rendered. NEARS-482 (JSON decode) cannot affect image pixels. The live clean app title visually overlaps the baked-in image text -> what looks like overlap+mojibake is image-sourced.
- Wire finding: backend \u-escapes ALL non-ASCII (banner title id=22 = "Save big this week — Organic Shop"); Latin-1==UTF-8 on escaped data, so seeded API data does not reproduce app-layer mojibake.
- App-rendered non-ASCII that DOES render clean live: currency "د.إ." (RTL), em-dash in "Demo Zone — Dhaka" address chip, "QA fixture — authed ongoing" order field (10-order-details-en.png).

## Final per-AC results
- AC1 (home banner clean): app-rendered title/badge/CTA CLEAN (01-home-banner-en.png). CAVEAT: a separate baked-into-PNG mojibake exists on the banner image (bug, out of NEARS-482 scope).
- AC2 (store-page offers): store page + offer/discount/store-name text render clean EN+AR (22-store-page-arabic.png, 31-search-results-en.png).
- AC3 (z-overlap): NO app-layer z-overlap. Reskinned _PhotoHeroCard is a clean Column, no app subtitle. The apparent "overlap" is the live clean title over the baked-in image text. RESOLVED / not-reproducible at app layer.
- AC4 (EN+AR non-ASCII): EN+AR both verified. App-rendered Arabic clean throughout (20-settings-arabic.png, 21-home-banner-arabic.png, 22-store-page-arabic.png); em-dash "Demo Zone — Dhaka" clean (30-addresses-en.png); currency د.إ. RTL clean. Decode-equivalence + raw-UTF8 repro proven at the exact handleResponse/decodeRefreshBody path (OLD Latin-1 -> mojibake, NEW UTF-8 -> clean).

## Regression sweep (clean)
- order details (10), my orders/authed token path (11), saved addresses (30), search results (31), notifications inbox (32) — all clean, no runtime errors (ui_errors + Dart MCP get_runtime_errors both empty).
- Token-refresh decode path: authenticated endpoints (My Orders, order #158 tracking) render -> session intact; unit test #5 covers decodeRefreshBody.

## Automated backstop
flutter test test/api_client_utf8_decode_test.dart -> 6/6 PASS (Arabic round-trip, emoji/accented campaign title, ASCII unchanged, empty body, token-refresh decode, source-wiring pin).

## VERDICT: PASS (fix correct + no regressions). 1 regression_bug filed: baked-in banner-image mojibake (backend asset, out of scope).
