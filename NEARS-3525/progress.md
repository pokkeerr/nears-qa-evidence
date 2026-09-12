# NEARS-3525 QA progress

## AC1/AC2 static check (re-confirmed)
- grep -rn "placeholder:" custom_image_widget.dart + 3 call sites: only hit is line42 CachedNetworkImage's own `placeholder:` builder param (unrelated identifier, not the removed field). 3 call sites: zero matches. Diff confirms all 4 files consistent, no leftover field/arg.

## Store screen (AC3 scope: cover photo placeholder)
- Logged in as ahmed.khan@demo.com (Fresh Mart Grocery)
- Navigated Home -> FAB (dashboard index 2) -> Store screen
- Screen renders store cover photo area, name "Fresh Mart Grocery", address "123 Market Street, Downtown" -- no crash, no red-screen
- App logs during nav: all [NET] 200, zero [FAIL]/[ERR]
- Evidence: store-screen.png

## AC3: Review card widget (item review thumbnail)
- Logged in as demo.store@gmail.com (Nears Mart, store_id=1)
- Menu -> Reviews -> item review cards render ("Rice 5kg", "Sample Product") with thumbnail + reviewer + date, no crash
- Logs clean (item/reviews http_status=200, zero [FAIL]/[ERR] around this nav)
- Evidence: review-card-screen.png

## Regression: Campaign details screen (QA Test Scope bullet, not a numbered AC)
- BLOCKED from live nav: Menu -> Campaign list is empty for every vendor tried (ahmed.khan@demo.com, demo.store@gmail.com)
- Root cause (read-only DB confirmed): campaign_widget.dart:92 `campaignModel.availableDateStarts!` null-checks a field
  that is NULL for every seeded `campaigns` row (ids 1-3 checked) -> [FAIL] framework_error TypeError on every list row build
- This crash is in campaign_widget.dart (list row), a file NOT touched by NEARS-3525's diff; crash trace never touches
  CustomImageWidget/placeholder. Pre-existing, unrelated -> filed as regression_bugs, not a task_bug (breaks_ac: false)
- campaign_details_screen.dart's one-line diff (drop `placeholder: Images.restaurantCover`) verified via static
  code review only (same trivial pattern as store_screen.dart + review_card_widget.dart, both live-verified clean)
- Evidence: bug-campaign-list-nullcheck-crash.png, bug-campaign-list-nullcheck-crash.log

## Automated backstop
- flutter test test/custom_image_widget_memcache_test.dart: 5/5 pass
- flutter test (full VendorApp suite): 420/420 pass, 0 fail
