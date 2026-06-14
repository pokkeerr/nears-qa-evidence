# NEARS-394 QA progress (live checkpoints)

- [PASS] Boot + no blank: Splash -> address-select -> Home rendered, no runtime errors. (00,01)
- [OBSERVE] Home store cards: "Recommended For You" + "See All" header; store cards w/ "Closed Now" badges. (02)
- [PASS] Store detail + item detail render; items, discount/NEW badges. (03,04)
- [PASS] NearsQtyStepper = mint circles, increments work; Add To Cart = mint primary; "In Stock" badge = GREEN. (04,05)
- [PASS] Basket renders w/ items, steppers, summary, Proceed to Checkout. (06)
- [PASS][CRITICAL] Checkout NOT blank (SmartManagement.onlyBuilder intact): Deliver To, Review Items, Place Order, Total Amount all render. (07)
- [PASS] Profile/menu tab renders (My Orders, Settings, etc). (08)
- [PASS] My Orders: navy appbar, NearsFilterChip selected=navy, badges DELIVERED=green/CANCELLED=red, REORDER=mint, VIEW DETAILS=secondary. (09)
- [PASS] Dark mode: Home renders, Closed Now=RED, borderless cards legible, See All=mint, navy text dark-safe. (11,12,13)
- [PASS] Dark store detail + item cards: mint + circles, "All" filter chip mint, View Cart mint, badges correct. (14,15)
- [PASS] RTL/Arabic: chevrons mirror left, icons/text mirror to logical start/end, no clipping; Closed Now=red, See All=mint. (16,17)
- [NOTE] Locale switch reset theme toggle to light (ThemeController/prefs, untouched by Phase 0) — pre-existing, not a regression of this change.
- [PASS] Update Profile form (2nd SmartManagement surface) renders, NOT blank: inputs, verified badges green, Update=mint. (18)
- [PASS] English restored; app left clean.
