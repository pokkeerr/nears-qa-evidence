# NEARS-1658 QA progress (live, emulator-5556, APK md5 96fe174b4ec089c54e85b5939b481e09)

- AC7 store-19 reviews list, 5 rows, LTR — PASS (ac7-store19-reviews-ltr.png + ac7-reply-branch-ltr.png), logs clean
- AC3 primaryColor kept as colour (navy name, mint numeral) — PASS (same shots)
- AC4 taller-not-clipped — PASS with caveat (no live legacy baseline; token deltas computed statically)
- AC5 more/less — not live-exercisable (longest seeded comment 35 chars); covered by widget test
- AC6 RTL — mirroring + digit runs PASS; "date does not mirror" clause FALSE (bug-ac6-rtl-date-word-order.png)
- UX-2 item chip truncation — captured (bug-item-chip-fewer-chars-before-ellipsis.png)
- Automated: flutter test review_widget_dls_test.dart -> 9/9 passed
- Full-session log scan: 0 [FAIL], 0 [ERR], 0 RenderFlex/overflow across 480 lines
