# NEARS-397 QA progress (fix_cycle 1) — live checkpoints

Device: emulator-5554 (Android 17 / API 37, sdk gphone16k arm64)
Branch: feat/NEARS-397-home-redesign @ c7f15967
Backend: http://10.0.2.2:8000 (local, up)

## AC checkpoints (append-as-observed)

### Verified (live, Demo Zone — Dhaka, grocery + module dashboard)
- AC1 Banner photo-hero: PASS — 21:9 carousel, navy "LIMITED OFFER" eyebrow (discount variant=navy bg/white text, NOT red — verified in NearsBadge + live), headline, mint Claim Deal CTA, pagination dots, brand-hero fallback in code. Tap routed to store screen exactly once (single Back returned home; AbsorbPointer kills double-nav). Photo-hero present on module-dashboard for all module cards. shots 01,02,03
- AC2 Category chips: PASS — 64x64 circular photo chips (BoxShape.circle), all 3 module types migrated (CategoryView/Pharmacy/Food), circular shimmer (no square jump), tap routed to category screen, See All present. shots 04,05
- AC3 Featured Stores rail: PASS — full-cover _RecommendedStoreCard, name+address+chevron bottom, NEW pill (new store, no rating), overlay badges top-start, NO floating logo, vertical stack, View All only when >3, self-hides empty (recommended=1 store here). shot 09
- AC4 Flash Sale: PASS — horizontal scroll ~176px cards, RED -% discount badge (priceOff), name, price+struck, mint + add button -> live add put Banana in cart (basket badge "1", stepper swapped in), LIVE badge + ticking countdown (04d 19:xx), See All, NO outer wrapper. shots 06,07,08,09
- AC5 Search pill: PASS — white rounded-full pill, NO mic, navy cart button. shot 09
- Automated backstop: flutter test = 902 passed, 0 failed (exit 0).
