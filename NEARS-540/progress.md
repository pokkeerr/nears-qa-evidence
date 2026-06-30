# NEARS-540 QA progress (live checkpoint)
device: emulator-5556 | branch feat/NEARS-540-deliveryvendor-price-locale @ c996a099
- AC5 flutter test DeliveryApp: PASS (+75 all passed)
- AC5 flutter test VendorApp: PASS (+78 all passed)
- AC1 DeliveryApp EN: PASS — dashboard Balance "150 AED", earnings cards "0 AED"; My Earning total "0 AED"; logs clean (no overflow). shots: ac1-delivery-en-dashboard.png, ac1-delivery-en-earning.png
- REGRESSION-CANDIDATE (pre-existing, not in diff): DeliveryApp My Earning statement list fails to parse — EarningReportModel.fromJson int-vs-String? at earning_report_model.dart:27; endpoint 200 but list shows "0 Result Found". Logged via Crashlytics (not silent). log: bug-delivery-earning-report-parse.log
- AC2 DeliveryApp AR: PASS — dashboard Balance "د.إ.‏ 150", earnings "د.إ.‏ 0" (glyph prefix, byte-identical pre-PR); logs clean. shot: ac2-delivery-ar-dashboard.png
- AC3 VendorApp EN: dashboard Total Earning "350 AED"; Wallet Withdrawable "250 AED"/Pending "0 AED"/Withdrawn "100 AED"/Total "350 AED" (all convertPrice, AED suffix); logs clean, no overflow. shots: ac3-vendor-en-dashboard.png, ac3-vendor-en-wallet.png
  - ITEM-CARD price/struck/discount-tag surfaces BLOCKED live by pre-existing ItemModel.fromJson parse bug (item_model.dart:32 offset int-vs-String?) -> item list empty. Not in diff. Verified instead by unit tests (convertDiscountAmount: "10.0AED off" EN, glyph AR, "%" percent, free text). bug: bug-vendor-itemlist-parse.log
- AC4 VendorApp AR: Wallet glyph "د.إ.‏ 250/0/100/350" (byte-identical pre-PR); logs clean. shot: ac4-vendor-ar-wallet.png
