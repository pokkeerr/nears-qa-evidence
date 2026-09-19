
## 8-fix4 (C8 delta, 2026-09-19, emulator-5554, sha c31b05f38, backend :8636)
- C8 live: NEARS3636EXP card (only card) shows "EXPIRES IN 2 DAY(S)" / AR "تنتهي خلال 2 يوم"; device clock 14:37 +04, expire_date "2026-09-21" -> 00:00 local = ~33h -> ceil(33/24)=2. Other 7 cards: no tag.
- EN 1.0x / AR 1.0x / AR 1.3x tag fully visible; EN 1.3x tag TRUNCATED "EXPIRES IN 2 ..." (reproduced twice) -> bug-c8-expiry-tag-truncated-en-1.3x.png
- Analytics: view_promotion expiring_count=1, coupon_apply_tapped coupon_id=21 expiring_soon=1 (multi-store basket -> routed to Basket, no apply).
- API raw expire_date id 21 = "2026-09-21" (date-only) -> c8-api-raw-expire-date.log
- Logs: 0 [FAIL]/[ERR]/RenderFlex since first Coupons load.
