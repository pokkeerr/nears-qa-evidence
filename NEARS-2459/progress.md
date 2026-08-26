# NEARS-2459 QA progress

## AC1 [behav] UserApp chat header — PASS
- Device: emulator-5554, customer@nears.com, conv 46 "Demo Store" (vendor_id=1).
- Header renders "Demo Store" name + avatar, NAppBar single-line arm active (no subtitle row/phone text rendered at all).
- ui_errors: 0 matches, pid-scoped clean (13983, com.izzes.nears.nears_nears_2459_chat_header_live_smoke).
- Raw uiautomator dump grepped for literal "null" in text/content-desc: none found.
- Evidence: userapp-chat-header.png, userapp-chat-header-dump.xml.

## AC2 [behav] VendorApp chat header — PASS
- Device: emulator-5566, demo.store@gmail.com (vendor_id=1, "Demo Store"), Menu -> Conversation -> "Customer Nears" (same conv 46 counterpart, customer@nears.com / user_infos.id=3).
- Header renders "Customer Nears" name + avatar, no phone Text under the name (SizedBox.shrink() branch, per code at chat_screen.dart:90-93), composer ("Type a message") rendered, no crash.
- ui_errors: 0 matches, pid-scoped clean (32105, com.izzes.nearsvendor).
- Raw uiautomator dump grepped for literal "null" in text/content-desc: none found.
- Evidence: vendorapp-chat-header.png, vendorapp-chat-header-dump.xml.

## AC3 — not triggered (no crash/no raw-null artifact in either app).

## AC4 — confirmation-only, both ACs clean. No code changes made.
