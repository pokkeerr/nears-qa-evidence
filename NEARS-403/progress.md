# NEARS-403 QA progress checkpoint (live demonstration log)
- Device: emulator-5554 (Android 17/API37), QA SHA faf9d54d, branch feat/NEARS-403-order-success
- DB: delivered(26) + canceled(13) only — in-flight/refund states code-verified (DB read-only, no mutation)
- Login: customer@nears.com (id6, 39 orders)

| AC | result | evidence |
|----|--------|----------|
| Delivered chip=MINT (parcel #154) | PASS | 02-order154... AppBar mint chip, navy title, Get Help mint sticky |
| Canceled chip=RED (order #147) | PASS | 03-canceled... AppBar RED "Cancelled" chip — NOT mint |
| Cost breakdown light (order #147) | PASS | 04-canceled... Item/Discount/Free-pill/Total navy, Msg-to-Nears link |
| Delivered status hero+stepper (order #27) | PASS | 05-delivered... 5 mint nodes+checks, green delivered arrival, navy time, Review+GetHelp+Reorder sticky |
| Get-help/support sheet (HARD KEEP) | PASS | 06/07 themed sheet, NearsInput msg field accepts text, mint Send btn; reason-list empty (no seeded reasons); NOT sent |
| Cancel-reason dialog (HARD KEEP) | PASS(code) | unreachable live (no cancellable order in DB; DB read-only) — code-verified: Dialog DLS shell, NearsText, getOrderCancelReasons reason-list preserved, NearsSecondary/Primary btns; F-3 CustomTextField NOT swapped (should-fix residual) |
| Reorder render (HARD KEEP) | PASS | rendered in 02/03/05 sticky bar (mint+textOnMint); _handleReorder→ReorderHelper wired; NOT tapped (DB-safe) |
| F-1 DARK price contrast (order #151) | PASS | 09-dark... Total Amount + price values SKY blue (readable on navyContainer); Cancelled chip RED in dark too. NOTE: muted left labels (Item Price/Discount) dim — pre-existing muted-text contrast, not F-1 |
| DARK status hero+stepper (order #27) | PASS | 10-dark... 5 mint nodes+checks legible on navyContainer, stepper labels sky, delivered chip mint, green arrival, Order Tracking header readable. NOTE: order-date muted value dim (pre-existing) |
| RTL/Arabic order details (#152) | PASS | 12-arabic... fully mirrored (back chevron right, RTL-aligned labels/values), RED cancelled chip preserved, sticky Reorder+GetHelp mirrored, no overflow |
| Guest track INPUT no auth wall (HARD KEEP) | PASS | 13-guest... reached while LOGGED OUT; NearsSurfaceCard card, Order ID + UAE-phone NearsInputs, mint Track Order btn. Submit handler code-verified auth-free (fromGuestInput:true→trackOrder→guest screen, no isLoggedIn gate) |
| Guest track RESULT screen | PASS(code) | unreachable live: 0 is_guest=1 orders in DB + backend matches is_guest=1 only (correct backend design); creating one = order placement (forbidden). Code-verified: NearsAppBar/NearsSurfaceCard/GuestCustomStepperWidget/NearsPrimaryButton view_details, no auth gate |
| 4 success surfaces (carryover #16-19) | PASS(code) | unreachable live (DB-safe, no order placed). #16 order_successful_screen 0 legacy + warning img preserved; #17 dialog PopScope+PaymentFailed kept; #18 congrats NearsSurfaceCard+NearsPrimaryButton; #19 offline green check + red * note preserved + NearsSurfaceCard payment-info |
| Live map + LIVE pill + DriverCard | PASS(code) | unreachable live (0 in-flight orders w/ assigned online courier; DB-safe). Tracking/Pusher/Timer/map frozen per do_not_touch; INHERIT chrome verified clean in UX review |
| Automated backstop | PASS | flutter test order+checkout: +116 all passed (incl tracking_stepper_color_map_test) |
| Runtime errors (DTD) | clean | get_runtime_errors: none across all driven order screens |
| Regression sweep | clean | orders list, order-details(delivered/canceled/parcel), guest-track input, settings dark+RTL toggles — no overflow/red-screen |
