# NEARS-427 QA progress (live, UserApp express)
Device: emulator-5554 | branch feat/NEARS-427-guest-track-empty-state @ 10692e6e
Backend: http://10.0.2.2:8000 (config HTTP 200)

## Backstop (pre-live)
- flutter analyze (2 changed files): No issues found -> AC8a PASS
- flutter test order_controller_test + guest_track_order_screen_test: 51/51 GREEN -> AC8b PASS
  - covers found-path (stepper+view-details), no-order (empty state, no CTA), in-flight spinner, flag transitions
- Seed DB: 0 is_guest=1 orders -> AC4 live not demonstrable (no mutation allowed); rely on widget-test found-path

## KEY REACHABILITY FINDING (live entry to the empty state)
- Backend track_order (Admin/.../Api/V1/OrderController.php:80-86): for a GUEST no-match it returns HTTP 404, never 200+null-order.
- Guest input widget (guest_track_order_input_view_widget.dart:312-321 mobile / 173-182 desktop) navigates to GuestTrackOrderScreen ONLY when response.isSuccess (==200). On 404 it stays on the input + "Not found" snackbar.
- Deep-link converter (link_converter_helper.dart) does NOT route /guest-track-order-screen (Unknown -> home).
- => The empty-state branch is NOT reachable through any current live UI path against this backend. It is correct defensive code for the screen's own initState re-fetch race / direct route, proven by the production-tree widget test.
- Live observable today: guest no-match -> snackbar + input screen (NOT an infinite spinner). The infinite-spinner bug lived on GuestTrackOrderScreen which the input widget no longer reaches on 404.

## Live demonstrations
- AC1/AC2 (empty-state render + Back): NOT live-reachable (above); proven by production-tree widget test (NearsEmptyState present, no spinner, no CTA) + code (icon=search_off_rounded, title=no_order_found, subtitle=no_order_found_guest_subtitle, actionText=back, onAction=Get.back).
- AC3 (spinner only in-flight): widget test "in-flight fetch shows a spinner, not the empty state" GREEN; live input never hangs (404 -> snackbar) [shot 02].
- AC4 (valid lookup -> stepper): NOT live-demonstrable (0 is_guest=1 seed orders; no DB mutation). Production-tree widget test "loaded WITH an order shows the stepper and the view-details CTA" GREEN.
- AC5 (authed tracking unaffected): grep proves isGuestTrackLoaded is referenced ONLY in guest_track_order_screen.dart (3 reads) + order_controller.dart (decl + 2 writes); ZERO refs in order_tracking_screen.dart. Live: authed login (customer@nears.com) -> My Orders list (filters All/Cancelled/Delivered/Ongoing/Parcel) + order #152 (store) + #154 (parcel) details render clean, no errors [shot 05]. No ongoing seed order => live order_tracking_screen stepper not exercised; flag-leak ruled out by code isolation.
- AC6 (dark): live on NearsEmptyState via Wallet History empty state, dark mode forced [shot 06b] — mint icon disc, white title, legible muted subtitle on navy. Identical widget to the guest empty state.
- AC7 (RTL/Arabic): live on NearsEmptyState via Wallet History empty state, AR+dark [shot 07] — layout mirrored (back arrow top-right, title right-aligned, filter chip left), AR title/subtitle centered, full, no truncation. AR "Back"=خلف is a known content follow-up (not a fail). Restored EN+light after [shot restored].
- AC8: analyze clean + 51/51 tests GREEN.

## Verdict: PASS (with documented live-reachability limitation on AC1/AC2/AC3/AC4 empty/found surface — covered by production-tree widget tests; AC6/AC7 demonstrated live on the identical NearsEmptyState component). Change is additive, isolated, breaks nothing.
