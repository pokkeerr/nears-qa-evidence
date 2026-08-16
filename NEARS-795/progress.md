# NEARS-795 — QA evidence (device pass, fix cycle 0)

Verdict: **PASS** (with the DeliveryApp live-observability gap recorded as NOT_RUN, cause
pre-existing and unrelated to this diff).

- Worktree `/Users/Apple/Projects/nears-NEARS-795-screen-view-route-name-leak`
- Branch `fix/NEARS-795-screen-view-route-name-leak` @ `0217f91c`
- Device `emulator-5556` (Pixel_10_Pro_2) — booted by QA; pool device `emulator-5554` was held
  by a foreign lane (`qa_lock_acquire` refused it: 2 foreign host drivers).
- Backend: local `php artisan serve :8000` against `multi_food_db` (read-only from QA).
- Instrument: `setprop debug.firebase.analytics.app <pkg>` + `setprop log.tag.FA VERBOSE` +
  `adb logcat -v time -s FA:V FA-SVC:V`.

## The instrument had to be repaired first (worth knowing for every future run)

`google-services.json` is **gitignored**, so a fresh worktree has none, the
`com.google.gms.google-services` gradle plugin never applies, and Firebase Analytics comes up
**disabled**:

    E/FA: Missing google_app_id. Firebase Analytics disabled.
    E/FA: Uploading is not possible. App measurement disabled

Every `screen_view` AC verified in a worktree without first copying that file in is vacuous —
the events never leave the app. Copied from the primary tree (gitignored, so the diff stays
clean) and re-ran. See `bug-worktree-missing-google-services.log`.

## AC1 [evt] — `screen_view` reports the route path only

UserApp, 35 real `screen_view` events, 14 distinct names, **zero containing `?`**
(`ac1-userapp-screen-view-names.log`). Six of those routes are BUILT with a query string in
`UserApp/lib/helper/route_helper.dart`:

| route (as built) | line | emitted `ga_screen` |
|---|---|---|
| `/store/<slug>?id=&page=&module=` | 267 | `/store/corner-grocer`, `/store/demo-store` |
| `/checkout?page=&store-id=&module=` | 332 | `/checkout` |
| `/track-order?id=&number=<phone>` | 334 | `/track-order` |
| `/order-placement-failed?reason=<encoded>` | 528 | `/order-placement-failed` |
| `/verification?page=&number=<phone>&email=&token=&pass=&login_type=&session=&user_model=` | 235 | `/verification` |
| `/store-review/<slug>?storeID=&storeName=&store=<full JSON>&module=` | 384 | `/store-review/demo-store` |

Two of those carry live PII/secrets in the query and were driven with real data:

- `/track-order` was opened on a real order; the route's `number=` param is the signed-in
  customer's phone. Emitted name: `/track-order`.
- `/verification` was reached through the real forgot-password flow with a registered phone;
  the screen itself displays `+971…` and the route's `number=` param is that phone. Emitted
  name: `/verification`. This is the ticket's own leak family.

`/store-review` is the NEARS-1726 case: that route name was 2,411 chars and Firebase silently
dropped the event. It now emits `/store-review/demo-store` (26 chars) and the FA log carries
**no** param-rejection/truncation warning — the event lands.

VendorApp: FA live, 3 events, all path-only (`ac1-vendorapp-screen-view-names.log`). None of
the three routes reachable in that session is built with a query, so VendorApp's live evidence
shows the extractor is wired and harmless, not that it strips. The query case there is
unit-covered.

DeliveryApp: **NOT_RUN live** — see the build collision below.

Detector honesty check: the grep used to claim "zero with a query" was positive-controlled
against a synthetic pre-fix line and matched it (`ac2-unnamed-routes-and-controls.log`).

## AC2 [behav] — null route name returns null, does not throw

Three unnamed routes driven live in UserApp (item-detail bottom sheet, notification-confirm
bottom sheet, Login/Sign-Up sheet). Each opened and dismissed; **no `screen_view` emitted** for
any of them; navigation continued normally afterwards (sign-in completed end-to-end,
`POST /api/v1/auth/login` 200, `login` analytics event fired). Framework-exception count across
the whole session: **0**. DeliveryApp booted, logged in, reached the dashboard: **0**.

## AC3 [behav] — malformed route name does not throw

No malformed route exists in the shipped apps to drive, so this is unit-level: the
`//[bad]/reset-password?…` case runs in all three suites and is **confirmed to enter the catch
branch** by the `[WARN] msg="screen_view: unparsable route name, using path fallback"` line
each suite emits. Behaviourally corroborated on device by the zero-exception counts above.

## AC4 [behav] — RED against the pre-fix extractor, then green

Not re-reproduced (already reproduced twice upstream). Green side re-run here:
UserApp 29/29, DeliveryApp 10/10, VendorApp 10/10 in `test/helper/analytics_service_test.dart`.

## Automated backstop

- UserApp `flutter test`: **4026 pass / 2 skip / 1 fail**. The single failure is the known
  pre-existing compile error `test/features/chat/attachment_viewer_dls_test.dart:162`
  (`No named parameter 'isRightMessage'`), confirmed by running that file alone.
- VendorApp `flutter test`: 151/151.
- DeliveryApp `flutter test`: 250/250.

## Regression sweep (UserApp, ~15 surfaces)

splash, on-boarding, language picker, sign-in, forgot-password, verification, home `/`,
module home, store page x2, item bottom sheet, cart, checkout, order-placement-failed,
track-order, profile/settings, store-review, notification sheet. No regression attributable to
this change.

## Findings (all pre-existing, none caused by this diff)

1. `bug-deliveryapp-google-services-build-collision.log` — DeliveryApp's Android debug build
   fails at `:app:mergeDebugResources` whenever `google-services.json` is present: duplicate
   `string/google_api_key`, one from the `resValue(...)` added by NEARS-893
   (`DeliveryApp/android/app/build.gradle.kts:72`) and one generated by the google-services
   plugin. Isolated by parking the file (build then succeeds) and re-adding it. Pre-existing:
   that gradle file is byte-identical between the worktree and the primary tree, and the
   primary tree's committed `google-services.json` is byte-identical too
   (md5 `ff395f06e19e28383f1805ac233b9c9b`). Consequence for this ticket: Firebase Analytics
   cannot be enabled for DeliveryApp on Android at all, so its `screen_view` behaviour is not
   observable in a running app.
2. `bug-order-place-403.log` — `POST /api/v1/customer/order/place` returns 403 for a
   verified, unblocked customer (user 6) with a single-store, in-zone, COD cart; the app lands
   on `/order-placement-failed`. Reproduced twice. This is what blocked live verification of
   `/order-successful`. The FE logging is correct (paired `[FAIL]` + snackbar); the **backend**
   emits no log line for the 403, which is a silent failure path on the BE side.
3. `bug-checkout-group-store-403.log` — a multi-store cart aborts group placement because
   `GET /api/v1/stores/details/17` returns 403 (that store is zone 2, the address is zone 1);
   the user sees only a generic error snackbar.

## Positive side-observation

The NEARS-564 correlation join works end-to-end: the app line
`[FAIL] endpoint=/api/v1/customer/order/place http_status=403 correlation_id=2459d22c-…`
joins to `Admin/storage/logs/laravel.log` entries carrying the same `correlation_id`.
