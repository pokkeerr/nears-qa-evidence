# NEARS-404 QA progress (fix-cycle 1) — checkpoint log

- Ticket: NEARS-404 Profile / menu hub (UserApp), branch feat/NEARS-404-profile @4b02cc50
- Device: emulator-5554 (Android), booting UserApp from primary tree
- Started: see owner.json

## Code pre-flight (verified from source @4b02cc50)
- baseUrl -> http://10.0.2.2:8000 (Android, useHttps=false) — real local backend. Backend up (config 200). PASS
- NearsColors.navy / NearsTokens.navy = #000080. NearsTokens.error = #BA1A1A (brand-red). errorSurface = #FFDAD6 (salmon).
- F-01 fix present: logout bg + icon + label use NearsTokens.error (#BA1A1A), theme-invariant (menu_screen.dart 684/690/694). PASS-code
- F-02 fix present: logout icon = NearsIcon('logout') not Icons.logout_rounded (line 690). PASS-code
- F-04 fix present: eyebrow strip Container has decoration{color fill + bottom BorderSide(outlineVariant)} (411-428); dark uses navyGlass. PASS-code
- createdAt null-safe: joined line gated on createdAt != null (251-261). PASS-code

## Live AC verdicts (appended as observed)

### GUEST state (light) — observed live
- Hero: "Guest User", "For more personalised & smooth experience." + "Log in/ Sign up" CTA. No joined line. PASS (AC7 guest)
- NO stat row, NO Promotional group, NO logout button (guest). PASS (AC7)
- GENERAL: My Orders, My Staples, Edit Profile, My Address, Settings (5 rows). PASS
- EARNINGS: Join as a Delivery Partner, Open Vendor (DM+Vendor on, refer OFF -> refer row hidden, group still renders 2 rows, no gap). PASS (config matrix)
- HELP & SUPPORT: Talk to Nears!, Help & Support, Terms & Conditions, Privacy Policy, Refund Policy (refund row shown; cancellation+shipping hidden -> no gap, refund is last visible row). PASS (config matrix)
- Shots: 01-guest-hero-light.png, 02-guest-support-light.png

### Config matrix (seeded zone 1, read-only DB + /config API confirm)
- loyalty_point_status=0, wallet_status=0, ref_earning_status=0 -> loyalty/wallet stat tiles + promotional rows hidden; refer-earn row hidden. Matches live.
- toggle_dm_registration=1, toggle_store_registration=1 -> DM+Vendor rows shown. Matches live.
- refund row shown / cancellation+shipping hidden -> dividers re-chain, no placeholder gap. Matches live.
- Un-flippable states (would need DB mutation) code-confirmed: getters read SplashController.configModel; rows in `if(flag)` collection-if so hidden rows leave NO widget (no gap). NOT mutated per DB-safety.

### LOGGED-IN state (light) — observed live (customer@nears.com)
- Hero: navy gradient (#00003C->#000080), 96px avatar + white ring + MINT verified badge chip, "Customer Nears" + "Joined 14 May, 2026" subtitle, moon theme-toggle top-right. Visual-confirmed shot 03. PASS (AC1 composition, AC9 joined)
- Stat row: single "Orders / 39" tile overlapping hero bottom; loyalty+wallet hidden (config=0) -> NO gap, tile fills width. PASS (AC6 stat tiles, AC1 stat row)
- 4 grouped cards w/ tinted eyebrow bands + bottom hairlines + chevrons: GENERAL(5), PROMOTIONAL ACTIVITY(Coupon only), EARNINGS(DM+Vendor), HELP&SUPPORT(Talk/Help/Terms/Privacy/Refund). PASS (AC1, F-04 eyebrow bands)
- Logout button present (logged-in only). PASS (AC7)
- Login from guest CTA refreshed header to real name/avatar/joined. No runtime errors. PASS (AC7 login refresh)
- Shots: 03-loggedin-hero-light.png (visual-read confirmed), 04-loggedin-logout-light.png

### DARK mode — observed live (CRITICAL guards)
- NEARS-167 GUARD: hero STAYS NAVY (#000080 gradient), NOT mint. CRITICAL PASS. Shot 05 (visual-read).
- Theme toggle flipped moon->sun. PASS (AC theme toggle)
- F-01 dark logout: Logout button icon+label = clear BRAND-RED (#BA1A1A), fully legible (was near-invisible salmon). PASS. Shot 06 (visual-read).
- F-04 eyebrow bands in dark: tinted strips (navyGlass) + bottom hairlines perceptible on navyContainer cards (GENERAL/PROMOTIONAL/EARNINGS/HELP&SUPPORT). PASS.
- Stat card + settings cards on navyContainer; mint icon chips legible. PASS (AC dark mode)
- Divider re-chain in dark: EARNINGS Open Vendor last (no trailing divider), HELP&SUPPORT Refund last (no trailing divider). PASS.
- Shots: 05-loggedin-hero-dark.png, 06-loggedin-logout-dark.png (both visual-read confirmed)

### Row routing (logged-in, spot-checked live)
- My Orders -> All Orders list (real orders). PASS
- My Staples -> staples screen (Weekly staples, reminders, Add all to cart). PASS
- Edit Profile -> Update Profile. PASS
- My Address -> Saved Addresses / Add New Address. PASS
- Settings -> Settings (Notification, Language, Version). PASS
- Coupon -> Coupon screen. PASS
- Talk to Nears! -> Conversation List (AI assistant). PASS
- Help & Support -> opened (route fires). PASS
- Terms & Conditions -> Terms screen. PASS
- Privacy Policy -> Privacy screen. PASS
- Refund Policy (config-gated) -> Refund screen. PASS
- Join as a Delivery Partner -> Delivery Partner Registration. PASS
- Open Vendor -> Vendor Registration. PASS
- Theme toggle reverses dark->light correctly. PASS

### Logout flow — observed live
- Tap Logout -> ConfirmationDialog "Are you sure you want to log out?" (No/Yes). PASS. Shot 07.
- Confirm Yes -> session cleared, returned to GUEST Profile (Guest User + login CTA, no stat row, no Promotional, no logout). PASS. Shot 08.
- No runtime errors. Guest<->logged-in round trip works.

### Guest after logout (re-verify guest hide rules)
- Guest hero returned: "Guest User" + "For more personalised & smooth experience." + "Log in/ Sign up". No joined, no logout, no coupon. PASS.

### RTL / Arabic — observed live (visual-read shot 09)
- Hero navy in RTL, "مستخدم ضيف" centered, mint login CTA full-width. PASS.
- Chevrons MIRRORED (point left), icon chips at logical END (left), labels right-aligned. PASS.
- Eyebrow band labels (عام/الأرباح) at logical start (top-right of cards). PASS.
- No clipped labels in tiles/headers. Bottom nav reversed. PASS.
- Shot: 09-guest-rtl-arabic.png (visual-read confirmed)

### Automated backstop + regression
- flutter test menu feature: 26 passed (menu_screen_reskin_test + menu_controller_pin_test). GREEN.
- flutter test test/common (shared DLS): 52 passed (NearsSettingsTile/StatCard/Icon etc). GREEN.
- Running app: no runtime errors (DTD get_runtime_errors clean).
- Blast radius (git diff HEAD~2..HEAD): menu_screen.dart (target), portion_widget.dart (deleted - retired as planned), nears_icon.dart (+1 line: additive 'logout'->Symbols.logout key, zero blast).
- Adjacent surfaces exercised live, no breakage: Edit Profile, My Orders, My Address, Settings, Coupon, My Staples, registration screens.
- REGRESSION: CLEAN.

### F-03 (cosmetic, should-fix from UX review) — note
- UX review F-03: stat-row overlap was -space5 (20px) vs frame -mt-6 (24px). Cycle-1 commit set offset to const Offset(0,-NearsTokens.space6) (=-24px) per code line 85. Now matches frame. Visually confirmed overlap in shots 03/05. PASS.
