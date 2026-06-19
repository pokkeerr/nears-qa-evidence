# NEARS-528 QA progress — remove guest track-order (FE + BE)

Branch `feat/NEARS-528-remove-guest-track` @ 9384ddbc | device emulator-5554 | build com.izzes.nears

| AC | Verdict | Evidence |
|----|---------|----------|
| AC-1 authed track survives flag rename (no infinite spinner) | PASS | 04b-track-loaded.png — order_tracking_screen renders map + stepper (Order Placed active → Delivered), Delivery Partner card; isTrackLoaded gate works |
| AC-2 logged-out My Orders = NotLoggedInScreen | PASS | 06-guest-myorders-notloggedin.png "You are not logged in / Login"; 07-login-screen.png Login→Sign In; post-login callback reloaded authed list |
| AC-3 guest Track Order gone | PASS | route deleted, files deleted, 0 lib/test refs, no menu entry |
| AC-4 backend authed-only (401 guest/unauth, 200 own) | PASS | backend-track-auth-gate.log — phpunit 4/4 + live curl 401/401/200/404 |
| AC-5 compiles + runs clean; grep 0 | PASS | grep 0 matches; app booted clean; no Flutter errors all session |

Regression: authed My Orders All/Ongoing/Cancelled/Delivered/Parcel all load (08-authed-myorders-relogin.png); order 158 details open (03).

Automated: phpunit TrackOrderAuthGuard 4/4; flutter order_controller + order_tracking_screen tests 46/46.

regression_bug (PRE-EXISTING, not NEARS-528): stale running-order banner after logout → order_details_screen infinite spinner on 401. See bug-running-order-banner-guest-spinner.{png,log}.
