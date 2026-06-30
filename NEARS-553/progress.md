# NEARS-553 QA progress (light mode only; dark deferred)
- Device emulator-5554; build = worktree feat/NEARS-553-checkout-prefill (uncommitted fix), API_HOST=10.0.2.2:8000
- AC1/AC2 (James Wilson, user1, no saved address) NATURAL checkout: Name='James Wilson', Phone='01600000001' (+1) => own profile. hasSavedDeliveryAddress=true (cache coords, null contact). shot=ac1-ac2-james-natural-form.png
- AC4 (James) stale-injected (Customer Nears/+971565811199, hasSaved=false): Name='James Wilson' Phone='01600000001'(+1) => own profile, stale REJECTED. shot=ac4-james-stale-injected-shows-own.png
- AC4 (Emily, user2) natural: Emily Johnson/01600000002(+1). stale-injected same Customer Nears => still Emily Johnson/01600000002 => own profile, NOT prior user, NOT Customer Nears. shots=ac4-emily-natural-form.png, ac4-emily-stale-injected-shows-own.png
- AC3 (Emily form): Name cleared->'' then typed 'QA Edited Name'; Phone cleared->'' then '0599887766'; fields enabled+focusable (not locked); values persist in controller (feeds placeOrderBody). Real order NOT placed (DB read-only). shot=ac3-name-edited.png
- AC5 (user6 Customer Nears profile) real saved address active w/ DISTINCT contact (Saved Person/+971559998888/Tower 1): hasSaved=true => form shows 'Saved Person'/559998888(+971) = ADDRESS contact, NOT profile. shot=ac5-saved-address-contact-wins.png
- LOGS: 0 PII (name/phone) values in app logs across all ACs. 1 pre-existing EXCEPTION setState-after-dispose in custom_text_field.dart:101 (UNMODIFIED file) on focus/back-nav => regression-candidate, non-blocking. bug log=bug-customtextfield-setstate-after-dispose.log
- AUTOMATED: flutter test test/features/checkout/ => All 104 tests passed (incl new checkout_contact_seed_test.dart).
- VERDICT: PASS
