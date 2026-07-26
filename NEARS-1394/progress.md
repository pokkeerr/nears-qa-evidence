# NEARS-1394 QA progress (fix_cycle 0)
Device: emulator-5556 (EN), emulator-5558 (RTL). Widgetbook: web-server :9323.
Preflight: backend 302 OK, baseUrl 10.0.2.2:8000 (dev), images bootstrapped 2073, grep-clean OK, 3 files deleted OK.

## Live findings (emulator-5556, com.izzes.nears, zone 2 Abu Dhabi)
- CODE spot-check: all migrated sites map per spec (discount→primary/mint, new→primary/navy, organic-solid→primary/navy gated organic==1&&grocery, organic-details→secondary). 3 files deleted, grep-clean, catalog+widgetbook updated. PASS.
- ORGANIC solid (navy/white/brPill): store8-02 (item_card grid Salt 1kg), store8-03 (item_widget list Salt 1kg), store8-01 (recommended rail). CORRECT. logs clean.
- DISCOUNT mint pill (mint fill/navy text "17.0% OFF"/brPill): item-details-04 (item_bottom_sheet Sparkling Water). CORRECT. logs clean.
- Uppercase transform working ("ORGANIC","17.0% OFF"). brPill on all. No overflow/truncation observed.
- Gate: Mango (no discount) shows no discount pill; Sugar 1kg (non-organic) shows no organic pill. PASS.
- NEW pill (primary/navy): host rail NewOnMartView self-suppressed (all seed stores CLOSED at ~3AM emu clock + single-store gate) → not live-reachable this run. Identical NBadge config to organic-solid (verified). Verify via widgetbook+code.
- Organic inline-soft (secondary tonal): full ItemDetailsScreen is deeplink-only since NEARS-422 (taps use modal sheet); demo deeplink host not app-verified → routes to Chrome. Verify via widgetbook+code.
- RED "12/16/19% OFF" priceOff badges on item_card = PRE-EXISTING status:error badge (NEARS-668), NOT this ticket's DiscountTag. Diagonal mint corner ribbon on item_widget list = NCornerRibbon (NEARS-1385), NOT this ticket.
