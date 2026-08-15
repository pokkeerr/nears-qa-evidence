# NEARS-1487 QA progress (live, appended as observed)

- device: emulator-5556 (Pixel_10_Pro_2), lock held via qa_lock_guard, anchor pid 76513
- build: worktree fix/NEARS-1487-subscription-retry @ dac9cdf4, debug APK
  --dart-define=API_HOST=10.0.2.2:8001; on-device md5 == host md5
  (62d800f7a9f271ad336862b0f4f228b2) -> APK identity PROVEN
- harness: selective relay 127.0.0.1:8001 -> :8000, rewrites redirect_link on
  /api/v1/vendor/business_plan only, gated by REWRITE_ON toggle
- harness defect found+fixed by QA (NOT a product bug): duplicate Host header
  caused upstream 400s; dict keys are case-sensitive.
- app state: zone 1 (Main Service Zone), logged in as user id 2 (emily.johnson)

## Observed results (live, emulator-5556)

AC1-primary (retry branch) - PASS, by identity:
  pre-submit  retryPackageIdFor(4116) = null   (baseline: pair NOT yet retained)
  real UI tap "Confirm" on /subscription-payment?store-id=4116&package-id=1
    -> POST /api/v1/vendor/business_plan (real), redirect_link injected to
       http://10.0.2.2:8001/subscription-fail?injected=NEARS-1487
    -> real PaymentScreen webview -> real order_service.paymentRedirect
    -> Get.offAllNamed -> /subscription-success?flag=fail&from_subscription=true&store_id=4116
  post-submit Get.isRegistered<BusinessController>() = true  (survives offAllNamed)
  post-submit retryPackageIdFor(4116) = 1      (pair SURVIVED offAllNamed)
  failure screen CTA label = "Try Again"
  tap -> route BECAME /subscription-payment?store-id=4116&package-id=1
         (same store 4116, same package 1) and the screen rendered
         ("You are one step away! Choose your business plan")
  falsifier: route unchanged at /subscription-success... = pre-fix behaviour
  logs in tap window: zero [FAIL]/[ERR]/exception lines

AC1-fallback + CROSS-STORE LEAK GUARD - PASS:
  pair still retained = (4116, pkg 1); pushed failure screen for store 4117
  CTA label = "Continue to Home Page" (NOT "Try Again") -> no cross-store leak
  tap -> /?module=grocery-food&from-splash=false (home). logs clean.
  unit-level: retryPackageIdFor(9999)=null, retryPackageIdFor(null)=null

AC2 - PASS (paired with the positives above; failure route replaced in both cases)

RTL/Arabic: حاول ثانية and المتابعة إلى الصفحة الرئيسية both render;
  AR fallback tap -> home; logs clean.
  Geometry: EN both states CTA centre 672,1600; AR both states 672,1636
  -> no layout shift BETWEEN states within a language.

Regression (untouched branches):
  SUCCESS branch "Continue to Home Page" -> home. clean.
  PopScope system-back from failure screen -> home. clean.

PRE-EXISTING DEFECT (not this ticket): POST /api/v1/vendor/business_plan
  returns 403 {"errors":{"message":"Permission denied"}} for a UserApp customer
  Passport token; authorizeStore() only matches vendor/vendor-employee
  auth_token. App logs paired [FAIL] with correlation_id (contract OK) but the
  user is left stuck on the payment screen.
