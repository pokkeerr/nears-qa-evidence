# NEARS-514 QA progress (live, emulator-5556, worktree af8ed2d2)

- Pre-flight: baseUrl=http://10.0.2.2:8000 (real local backend), config HTTP 200, cash_on_delivery=true. OK.
- i18n diff verified (en/ar): change_amount + helper key reworded exactly per spec.
- Render code: payment_method_bottom_sheet.dart L500 label `${change_amount.tr}(${currencyToken()})`, L508-510 helper key, NearsInput onChanged->setExchangeAmount->bring_change_amount (boundary wiring intact, no Dart change).
- Env note: COD only renders when cart store's zoneId matches the delivery-address zone whose zoneData.cash_on_delivery=true. Cross-zone cart (zone-2 store + zone-1 addr) collapses COD to SizedBox (pre-existing behaviour, not this change). Resolved by using Nears Mart (store 1, zone 1) item with zone-1 (Demo/Dhaka) address.

## AC results
- [PASS] AC-2a EN relabel: sheet shows "Cash on Delivery", label "Cash you'll pay with(AED)", helper "Need change? Enter the cash amount you'll pay with." — shot ac2a-en-relabel.png / 08-sheet-nearsmart.png
- [PASS] See Less/See More toggle: collapses (label+helper+field hidden, toggle->"See More") and re-expands correctly. shots 08 (expanded), tested live.
- [PASS] AC-2a boundary (field functional): tapped COD, field accepted value "50" (shot 10-amount-50.png). onChanged->setExchangeAmount->exchangeAmount; static map confirmed checkout_controller L1321 `bringChangeAmount: paymentMethodIndex==0 && exchangeAmount>0 ? exchangeAmount : null` -> place_order_body L278 data['bring_change_amount']. NO order placed (hard boundary respected).
- [PASS] AC-2a AR relabel (RTL): switched app to Arabic. Sheet shows "الدفع عند الاستلام" (COD), label "المبلغ النقدي الذي ستدفعه(د.إ.‏)", helper "هل تحتاج إلى فكة؟ أدخل المبلغ النقدي الذي ستدفعه." — exactly the new AR strings. RTL mirrored correctly (COD check on left, header right-aligned), NO truncation/overflow. shot 11-sheet-arabic.png
- [PASS] AR See Less/See More toggle works (عرض أقل <-> عرض المزيد).
- [PASS] Regression: no runtime errors (get_runtime_errors clean, ui_errors empty), no overflow/layout break, dark mode rendered cleanly throughout EN+AR. Field render guard `showChangeAmount && paymentMethodIndex==0` (sheet L473) gates field to COD — unchanged by this copy-only commit. NOTE: COD is the ONLY active payment method in this env (digital_payment=False, no active gateways, wallet=0), so live "switch to another method hides field" could not be exercised — verified by the static gate + the See Less collapse instead.
- [PASS] Automated backstop: flutter test test/features/checkout -> All 55 tests passed.

## Env / data notes (not defects in this change)
- COD visibility requires cart-store.zoneId to match a delivery-address zoneData entry whose cash_on_delivery=true. Pre-existing data has cross-zone carts (zone-2 Test Store items) + a stale "Demo Zone — Dhaka" saved address; both collapse COD. Used a fresh zone-1 current-location address + a Nears Mart (store 1, zone 1) item to get a valid COD checkout. This is pre-existing platform behaviour, NOT introduced by NEARS-514.
