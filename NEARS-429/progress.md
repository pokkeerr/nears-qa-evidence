# NEARS-429 QA progress — UserApp NearsInput dark-mode contrast (fix-cycle 1)

Device: emulator-5554 (Android) | Branch: feat/NEARS-429-input-dark-contrast @ a820764c
baseUrl: http://10.0.2.2:8000 (real local backend, 302 on /admin — OK)

## Automated backstop
- flutter analyze lib/common/widgets/dls/nears_input.dart -> No issues found (0 new)
- flutter test nears_input_dark_contrast_test.dart -> 5/5 PASS (incl. focusColor=mint guard)

## Live AC checkpoints (appended as observed)
- [DARK] AC2 resting/floating label visible: edit-profile dark resting (05) - Name*/E-mail* float MINT, Phone* resting dim-white, hint dim-white. OBSERVED
- [DARK] AC1 typed text white: edit-profile typed "Customer NearsQATEST" white on navy (07). OBSERVED (reverted, no save)
- [DARK] AC3 trailing icon sky: email verify shield + phone badge visible (05/06). OBSERVED
- [DARK] AC4 focused mint ring+label: Name field focused -> 2px MINT ring + MINT floating label (06). OBSERVED <- fix-cycle-1 item
- [DARK/GLASS] AC7 glass typed white + focus mint: login email "qatest@@invalid" white, mint ring+label+icon (08/09). OBSERVED (reverted)
- [DARK/GLASS] AC5 error state: empty Sign In -> red border + "Enter email address or phone number" / "Please enter password" (10). OBSERVED. NOTE: red-on-navy msg contrast dim = known separate follow-up, not a fail.
- [DARK/GLASS] AC3 password eye trailing icon: visible + toggles; lock leading icon visible (11/12). OBSERVED (pwd reverted)
- [LIGHT] AC6 no-regression non-glass: edit-profile light -> focus ring+label NAVY (not mint), text DARK, fill off-white (16). OBSERVED <- light arm unchanged
- [LIGHT/GLASS] AC7 glass unchanged in light: login hero stays navy, mint focus ring/label/icon identical to dark (14). OBSERVED
- [REGRESSION DARK] Add Address screen non-glass NearsInput: Delivery Address focused -> mint ring+label, white text; resting fields dim-white hints/labels + sky icons. CLEAN (no save tapped)
