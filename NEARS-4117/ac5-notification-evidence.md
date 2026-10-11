# NEARS-4117 AC5-notification evidence (token scrubbed: last 6 chars only)

Honesty note (verbatim): this reproduces a STALE tray notification tapped after the status flipped, because no production emitter fires order_status to a DM for a returned order, Helpers.php:2844 gates on processing|handover.

Approval: advisor-product Tier B (runner-direct-4117-ac5-push-credential). Conditions: raw token of delivery_men id 1 only (no topic, no loop), production payload shape, at most 3 sends, own worktree backend, Admin/.env DB read only.
Credential: business_settings row 177 push_notification_service_file_content, project_id nears-1d39b (same as the app's google-services.json and the shared DB). Side effect: the first send minted an OAuth token that the app cached in the CLONE DB's cache table (fcm_oauth_access_token_nears-1d39b), clone only.

Token check: before (08:37:11 registration read) ...krY93k len 142 updated_at 2026-10-11 08:37:11; re-read immediately before each of the 3 sends: ...krY93k, updated_at unchanged. changed=false, so no other login rewrote it (no sign of a second device). Row id 5 (Test1) holds the same stale token, same emulator.

Command (token read inside php, never printed):
  php artisan tinker --execute='$t = \App\Models\DeliveryMan::find(1)->fcm_token; $r = \App\CentralLogics\Helpers::send_push_notif_to_device($t, ["title"=>"Order Notification","description"=>"ready for delivery","order_id"=>94173,"image"=>"","type"=>"order_status"]);'   (token=...krY93k)

| # | mode | send result | app log | GET order | rendered | back |
|---|------|-------------|---------|-----------|----------|------|
| 1 | FOREGROUND, fln tap (notification_helper.dart:48-54) | returned=true; laravel.log "FCM Send Success status 200 order_id 94173" 08:41:42 | 08:41:42 `fcm onMessage type=order_status` | 08:42:00 GET /api/v1/delivery-man/order x2, http_status=200 | Order Details 94173: "Return fee due (not collected)" + 5.00 AED (en-ac5-notif-foreground-94173-*.png) | back -> dashboard/initial route (Orders page shown) |
| 2 | BACKGROUND via HOME (onMessageOpenedApp, :138-145) | true; "FCM Send Success 200" 08:42:30 | `fcm onBackground type=order_status` 08:42:30; tap -> `fcm onOpenApp type=order_status` 08:42:44 | 08:42:44 + 08:42:45 GET order 200 | same neutral label (en-ac5-notif-background-94173-*.png) | back -> initial route |
| 3 | KILLED via kill_coldstart.sh (result=killed_stack_remove, stopped_flag=false, post_pid=none) -> getInitialMessage -> splash (main.dart:221-228, splash_screen.dart:116-119) | true; "FCM Send Success 200" 08:43:29 | FCM woke a new process (pid 20246, `fcm onBackground` 08:43:29); tap started a new Flutter engine at 08:43:44; no `fcm onOpenApp` line (so the getInitialMessage path, not onMessageOpenedApp) | 08:43:46 GET order 200 | same neutral label (en-ac5-notif-killed-94173-*.png) | back -> dashboard/initial route |

Not driven: dashboard assign-dialog entry (dashboard_screen.dart:87-93), cited by code only.
No [FAIL]/[ERR] app lines during any send. All four entries use Get.toNamed(getOrderDetailsRoute(id, fromNotification:true)) with no arguments, so the fallback constructor at route_helper.dart:159-162 was exercised (fromNotification true, isRunningOrder/orderIndex null) and rendered the same state as the list entries.
