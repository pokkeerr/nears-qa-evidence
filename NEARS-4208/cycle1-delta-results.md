# NEARS-4208 cycle 1 (delta re-QA) results

Build: worktree HEAD 1f4040cc1 (cycle-0 code + NDialog fix fa9a198b5/87ff6117d + merged 4190/4213/4214), UserApp debug APK built under mem-guard (label nears4208-qa2), emulator-5586, light mode, own backend :8742, twin multi_food_db_qa4208.

## AC3 matrix at 320dp x1.3 (wm size 480x1000, density 240, font_scale 1.3), logcat checked for `RenderFlex overflowed` after every variant: none in any pass

| Variant | EN | AR |
|---|---|---|
| Offer dialog two-action | Cancel [75,814][229,889], Move [251,814][405,889] (102.7dp x 50dp each); ink margins L/R 31/33 and 40/40 px (no clipping); Move tappable -> sheet | Cancel on the right [251,814][405,889], Move on the left [75,814][229,889]; ink margins 56/56 and 49/52 px; description scrolls (node moved 424 vs 464 after a swipe) while both buttons stay pinned; screenshot cycle1-ac3-ar-two-action-320dp-x1.3.png |
| Cancel-only (store with no slots) | Cancel / Wait present 102.7 x 50dp, Wait tappable (choice keep_waiting) | Cancel / Wait present |
| Reschedule-only (can_cancel=false) | Move / Wait present, Move opens sheet | Wait / Move present |
| Reschedule sheet | Confirm new time 288 x 52dp present, slots listed | Confirm present (432px), title and slots RTL |
| Empty sheet, can_cancel true | body "...You can cancel the order instead", Cancel Order 288dp present, opens reason picker | AR body + Cancel Order present |
| Empty sheet, can_cancel false | "No delivery time is available right now. Please try again later." and no Cancel | same, AR copy, no Cancel |
| Offer card | title/body/auto-cancel line + Reschedule link 144.7 x 44dp | AR card + link |
| Held card (can_reschedule true / false) | checking title, payment-safe body with later-time sentence + Reschedule link / "We'll update you soon", no link, no Cancel anywhere, no dialog | same in AR |
| Group view (2 children) | dialog per child, one at a time; flat card per child; Reschedule + Cancel Order per child (44dp) | same in AR |

Default-scale NDialog consumers (EN, scrim/back dismiss): menu Logout dialog renders (buttons 500 x 150px), back dismisses and stays signed in; delivery-partner registration "Your registration isn't finished" dialog renders (Discard / Save Draft), back and scrim tap both dismiss; order_details switch-to-COD NDialog is reachable only for parcel orders (`_buildParcelBottomView`; the bottom button on a normal order is commented out and the "Switch to COD" row in the payment section is a different non-dialog control), no parcel fixture on the twin: UNVERIFIABLE live.

## Money smoke on the merged bytes
- Wallet-paid 60.00 auto-cancel (order 93001): system / acceptance_timeout, +60.00 wallet, digital_received -60.00, stock +2, 1 order_refund row, 1 notification row.
- Reschedule business timezone: GET slots first slot list for order 93002, chose slot 16:01:00, PUT -> stored schedule_at 2026-10-21 16:01:00 (== slot), slot_start 16:00. Same slot sent as ISO UTC `2026-10-21T12:01:00Z` (order 93003) -> stored 16:01:00. `date_default_timezone_get()` is UTC in the CLI, the business timezone is Asia/Dubai: stored value equals the slot returned.
- Late accept after an offer (real placed COD order 93005, offered, then store `confirmed`): exactly ONE 4214 notice ("Your order is confirmed. Delivery is now promised by 10:01") and `eta_accept_*` stamped once; a second accept request added only the ordinary "Order Confirmed" status row, no second 4214 row.

## Tap path
FCM accepted the one deliberate push (`FCM Send Success status 200`, order 93301) but nothing arrived on the emulator within ~3 minutes: UNVERIFIABLE (see cycle1-real-push.log). No second push sent. Credentials re-blanked immediately.
