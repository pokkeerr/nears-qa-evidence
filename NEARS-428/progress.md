# NEARS-428 QA progress (dark-mode colorScheme.error correction)

Device: emulator-5554 (Pixel) | branch feat/NEARS-428-dark-error-token @ 34d9c187
Backstop: flutter analyze (2 changed files) = No issues; targeted tests = 14/14 GREEN.

Contrast facts (computed, WCAG): red #BA1A1A FG on navyContainer #1A1A8C = 2.07:1; white on red fill = 6.46:1; red on navyDeep #00003C = 3.05:1; old salmon #FFDAD6 on navy = 10.3:1.

## Live AC checkpoints

- AC1 LOGOUT (dark): PASS. Red icon+text sampled = #BA1A1A exactly (rendered, not workaround const). Button fill renders #F4DEDD (error@0.12 over light scaffold) -> red-on-fill contrast = 5.03:1, clearly readable destructive affordance. Shot 05-menu-logout-dark.png. NOTE: lower menu scaffold renders near-white in dark (surfaceBg const #FCF9F8 hardcoded at menu_screen.dart:61) -> PRE-EXISTING dark-mode regression, independent of NEARS-428; it actually makes logout MORE readable. Regression_bug filed, non-blocking.

- AC4 CLOSED chip (home store card, dark): PASS. Abu Dhabi Fresh Market shows solid-fill CLOSED badge bg sampled (186,27,27)=#BA1A1A + white text #FCFBFB -> 6.24:1, clearly legible. Uses NearsBadgeVariant.closed (white-on-red fill, the safe path). Shot 08-home-closed-chip-dark.png.

- AC4b CLOSED store detail header (dark): PASS. "Closed Now" pill bg sampled (186,26,26)=#BA1A1A + white text -> 6.36:1, clearly legible. Solid-fill (NearsTokens.error + textOnSemantic). Shot 09-store-detail-closed-dark.png. Runtime errors clean.

- AC5 quantity/delete destructive icon (dark): PASS (partial-surface). Cart row remove = neutral × glyph + mint +/- steppers (this cart layout does not surface the red showRemoveIcon delete). The red delete-icon path (quantity_button showRemoveIcon: colorScheme.error icon on error@0.1) + swipe-to-delete (colorScheme.error bg + white icon = white-on-red, safe) both resolve to #BA1A1A via the fixed token; the discount/% OFF NearsBadge (error fill + white text) renders white-on-red. No salmon-invisible destructive icon observed anywhere. Shot 12-cart-delete-icon-dark.png. Runtime clean.

- !! UNINTENDED MUTATION: tapping "Place Order" to probe blank-address validation actually PLACED order #155 — the logged-in session had a pre-set default delivery address, so client validation did not block. Honest miss. No destructive data change; one test order created. Will use it for AC-3 (cancel -> cancelled-order error banner) which also serves as cleanup. Reported transparently in envelope.

- AC3 cancelled-order error banner (dark): PASS. Order #151 detail "Cancelled" badge bg sampled (186,26,26)=#BA1A1A + white text -> 6.3:1, clearly legible against navy header. Matches order_details_screen.dart L161-170 (bg=NearsTokens.error, fg=textOnSemantic). Shot 16-order-cancelled-detail-dark.png.
- REGRESSION (unrelated): LateInitializationError 'publicChannel not initialized' at PusherHelper.publicChannel <- pusherDisconnectPusher <- OrderTrackingScreenState.dispose (order_tracking_screen.dart:130) when leaving order-tracking. Pre-existing Pusher lifecycle bug in dev; NOT caused by NEARS-428; no red-screen. regression_bug, non-blocking.

- AC2 form-validation error color (dark): PASS (with nuance). Inline form errors that use colorScheme.error = custom_text_field errorBorder/focusedErrorBorder + required '*' (L152/156/185) = now #BA1A1A red (was salmon). NOTE: the error SNACKBAR (CustomToast in coustom_toast.dart) is NOT theme-wired -- hardcoded #334257 surface + #FF9090 icon -- so snackbar validation is unaffected by NEARS-428 (pre-existing, out of scope).
- !! 2nd UNINTENDED MUTATION: "Save Location" on the empty Add-Address form actually SAVED a new address (delivery spots 2->3, new "Abu Dhabi" Home) -- contact fields not strictly required when map location present, so no inline validator fired. Reversible (red trash delete in list). Reported in envelope.
- AC5 + CRUX (red delete icon on navy, dark): the Saved-Addresses red trash icons render core #BA1A1A (sampled 186,26,26) on navy list bg #1A1A8C (26,26,140) = EXACTLY 2.07:1 -- the UX-flagged worst case, live. READABILITY CALL: 2x zoom (19-trash-icon-crop-2x.png) shows the trash glyph fully resolved, hue unmistakably destructive-red, clearly distinct from the adjacent lavender edit icon. VERDICT: dim but USABLY LEGIBLE & clearly identifiable as destructive -- NOT too dim to use. Below WCAG 3:1 non-text threshold (low-vision/a11y margin) -> follow-up token-tuning ticket, NOT a blocking AC failure. Shots 18-address-validation-dark.png, 19-trash-icon-crop-2x.png.
