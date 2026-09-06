# NEARS-3088 QA progress

- AC1 (facades exist + phpunit green): PASS — targeted test 3/3 (9 assertions), RentalRouteGuardTest 4/4, wider Rental|Gateway|Sms|OTP filter 52/52.
- AC2 (rental-guarded admin routes still 404): PASS — live HTTP against booted worktree server (rentalView, customer_trip_export, order_export?provider_id=1 all 404; non-rental order_export branch 200 CSV).
- AC3 (OTP/SMS fallback, no fatal): PASS — live tinker call (smsGatewayAvailable=false, sendViaSmsGateway='not_found', SMS_module's own pre-existing no-provider response) + live HTTP exercise via admin forgot-password -> otp-resent (200, {"otp_fail":"otp_fail"}, no [FAIL]/[ERR] in laravel.log).
- AC4 (admin boots): PASS — dashboard 200, title "Nears", no exception/fatal strings.
- AC5 (modules_statuses.json flip inert): PASS — `php artisan module:list` only shows AI/TaxModule (Rental/Gateways/Controller never enumerated, flag was already unreachable); no app code reads modules_statuses.json directly.
- AC6 (Helpers.php collateral): PASS — admin login, /api/v1/config, order export (non-rental) all clean.
- Zero-diff re-confirmation (Store/User/Expense/CashBackHistory/AdminSearchDefinitions/VendorSearchDefinitions/trip_payment_fail): PASS — all 0 lines of diff vs base 6d005c4a0.
- AC7 (phpstan.neon comment narrowed not widened): PASS by reading — comment updated to reference NEARS-3088, scope still `app` only. phpstan itself currently exits 1 with 4 STALE/unmatched baseline entries in app/helpers.php (byte-identical file + byte-identical baseline entries pre/post this diff) -- pre-existing drift from NEARS-1530, unrelated to this diff. Filed as regression-candidate.

Regression-candidates found (unrelated pre-existing bugs, filed as followups, NOT NEARS-3088 findings):
1. `/admin/addon/system-addons` redirect closure calls a wrong route name (`admin.system-addon.index` vs actual `admin.business-settings.system-addon.index`) -> 500. routes/admin.php closure untouched by this diff.
2. `/admin/business-settings/system-addon` -> AddonController::index()'s relative `scandir('Modules')` resolves against the built-in PHP server's cwd (`Admin/public`), not `Admin/` -> "No such file" 500. AddonController.php untouched by this diff.
3. phpstan-baseline.neon has 4 stale/unmatched entries for app/helpers.php (byte-identical to base) -- likely left over from NEARS-1530's trip_payment_success() removal, never re-synced.

Backend server torn down (kill -TERM on the ad-hoc `php artisan serve --port=8010`), account lock (emily.johnson@demo.com) released, evidence published.
