# NEARS-402 Checkout Reskin — QA progress checkpoint

- Device: emulator-5554 (Android)
- Branch: feat/NEARS-402-checkout @ 96dc47af
- Backend: http://10.0.2.2:8000 (live local, NOT demo)
- HARD RULES: never tap Place Order/Complete/Pay Now; DB read-only.

## AC verdicts (appended live as observed)

- [PASS] Automated backstop: flutter test checkout+payment = 55/55 green.
- [PASS] MATCH-1 app bar: navy bar + white centered "Checkout" + shopping_basket glyph (shot 13/14).
- [PASS] States/loading: CheckoutScreenShimmerView = NearsSkeleton blocks, NOT spinner (shot 13).
- [PASS] NON-BLANK render path (a) from cart: full form rendered logged-in (shot 14) — Delivery Type toggle, Review Items, address card (Google Map), Substitution Preferences, Total Amount + Place Order. No runtime errors.
- [PASS] Regression: substitution pref ("Notify me when it's back") carried from cart into checkout (shot 14).
- [OBSERVED] NotLoggedInScreen rendered correctly for logged-out user before login (shot 10) — themed "Please login to continue".
- [PASS] MATCH-2 address card (shot 16): section header "Delivery Address" + 96x96 Google map thumb + navy name "Home" + muted line "Demo Zone — Dhaka" + edit icon top-right + surfaced card. Name/Contact NearsInput fields below.
- [PASS] MATCH-3 Place Order footer (shot 14/16): white panel, rounded-top + upward shadow, "Total Amount" navy label + price navy, mint Place Order pill + arrow_forward. RENDER ONLY — not tapped.
- [PASS] Survivor Delivery Type toggle (shot 14/16): Home Delivery mint-fill active + navy text; Take Away inactive white.
- [PASS] Inherited Substitution Preferences (shot 14): radio rows, mint check on selected, navy text — unbroken.
- [PASS] Inherited Review Items + DeliveryEtaBanner (mint "Arriving in 20-40" pill) render themed.
- [PASS] Survivor Payment method bottom sheet (§4c, shot 19/20): brSheetTop rounded-32 sheet, "Choose Payment Method" navy heading, Total Bill, COD row. SELECTED state = mint-tint bg + mint border + mint check_circle (shot 20). Mint "Select" CTA. COD selection reveals Change Amount NearsInput. Dismissed without submitting.
- [PASS] Survivor Delivery Partner Tips (shot 18a): re-themed chips (Not now mint-active + amount chips) + Save-tip checkbox.
- [PASS] Survivor Additional note (shot 18a): DLS NearsInput "Ex: Please provide extra napkin".
- [PASS] Survivor Promo Code (shot 17): DLS card + Add Voucher mint link + Enter Promo Code NearsInput + mint Apply.
- [PASS] Inherited Order Summary (shot 18a): Subtotal/Discount/Tips/Delivery Fee rows, mint FREE badge, navy labels.
- [PASS] Inherited TimeSlot/Preference Time (shot 17): DLS settings tile + mint clock icon.
- [OBSERVED] Terms text simplification (shot 18a): RichText "I have read and agreed with Privacy Policy/T&C/Refund Policy" navy underlined, NO checkbox. Place Order CTA enabled (acceptTerms defaults true).
- [PASS] SmartManagement RE-OPEN gate: re-entered checkout from cart 2x — full form each time, never blank (shot 21).
- [PASS] SmartManagement BACKGROUND/RESUME gate: HOME then resume com.izzes.nears — Checkout re-rendered full form non-blank (shot 22). No runtime errors after resume cycle.
- [PASS-partial] Entry path (b) buy-now/single-store: all checkout entries route to the SAME CheckoutScreen widget (cart/campaign/prescription differ only by `page`/`storeId` arg); SmartManagement risk surface is identical & demonstrated via cart path + re-entry + resume. True storeId!=null variant is the pharmacy `prescription` flow (gated behind a prescription store + image upload) — not exercised end-to-end, but the shared screen rendered non-blank repeatedly. Item-detail "Add To Cart" routes via cart (no separate direct-to-checkout).
- [N/A] Entry path (c) guest checkout: backend config guest_checkout_status=0 (read-only SELECT) — guest checkout DISABLED in this env. Logged-out checkout correctly shows NotLoggedInScreen (shot 10), not blank/crash. Not reachable without DB mutation (forbidden). Not a code defect.
- [PASS] Dark mode (shot 29): app bar stays navy; cards flip to navyContainer; mint stays mint (ETA pill, substitution check, Home Delivery active toggle, Place Order CTA); Total Amount legible on dark footer; text adapts white/sky. Non-blank.
- [N/A live] Payment tail (digital-failed full+dialog, offline-payment, partial-pay/wallet): backend config has digital_payment=false, wallet_status=0, offline_payment_methods EMPTY, only cash_on_delivery=true. Payment sheet shows ONLY COD (shot 19). These screens are unreachable in this env without DB mutation (forbidden). Code-verified by phase-7 UX review (NearsAppBar/NearsBadge.closed semantic red/NearsPrimaryButton/NearsSkeleton/NearsEmptyState present) + automated tests green (offline_payment_parcel_focus_test, payment_controller_pin_test). Semantic-red brand rule verified in code, not live.
- [PASS] RTL/Arabic (shot 34, also dark): app bar mirrored (basket glyph left, title "الدفع"); ETA pill right; Review Items thumb right + "x1" badge left; substitution rows right-aligned w/ mint check on right; Delivery Type toggle mirrored; footer "المبلغ الإجمالي" + mint CTA "وضع النظام" with arrow mirrored. No overflow/clipping. Non-blank.
