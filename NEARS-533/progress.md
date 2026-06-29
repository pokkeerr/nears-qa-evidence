# NEARS-533 QA progress — banner mojibake regen

Device: emulator-5554 | Build: dacc541b (feat/NEARS-533-banner-mojibake-regen) | Backend: 127.0.0.1:8000

- AC1 (id22 zone2 clean em-dash, VISUAL): PASS — served PNG d-ecc510bd18.png HTTP 200, full-res read shows "Save big this week — Organic Shop", clean em-dash, no Ã/Â/â€".
- AC2 (store_wise zone2 clean): PASS — id21 "Fresh deals near you — Abu Dhabi Fresh Market", id23 "Top picks for your tower — Eorange", clean.
- AC3 (new non-ASCII generated): PASS — `banners:regen-images --title="عرض خاص — Café 50%"` → /tmp/nears533-sample.png; em-dash + Café accents clean; Arabic isolated/unshaped (accepted).
- AC4 (all 6 render clean, Arabic unshaped accepted): PASS — id18/19/20 zone1 + id21/22/23 zone2 all clean em-dashes.
- Cache-bust: pm clear com.izzes.nears (full data wipe + fresh onboarding) → zero stale cache.
- Device runtime: zone-2 home + Grocery module home, ui_errors clean, /storage/ images fetch fresh (HTTP 200).
- Unit: DemoBannerImageRenderTest 4/4 (14 assertions).
- DB titles clean UTF-8 (contract-impact none confirmed).
- FINDING (non-blocking, reskin-scope): reskinned UserApp home does NOT render the dynamic banner carousel — cache DB shows 0 /storage/banner/ fetches across the home flow; static "Your neighborhood store" hero replaced it. NOT a 533 defect.
