# NEARS-874 QA progress — DeliveryApp mounted-guards
device: emulator-5556 | branch feat/NEARS-874-mounted-guards HEAD ac9daf6b
- login OK (delivery_man +971565656656) -> Home dashboard loaded (Balance 152 AED)
- AC2 home_screen checkPermission: home loaded, checkPermission ran, NO setState-after-dispose in log. shot 01-home-loaded.png
- AC3 custom_dropdown close: OPEN happy-path OK (2 options QA Bank Transfer/QA PayPal render), select closes overlay cleanly. shot 02-dropdown-open.png
  - FORCED dispose-mid-close 4x (open -> select(reverse start) -> hardware BACK pops route -> widget disposed): overlay CLEARED every round (no ghost on Withdraw Method screen), ZERO setState-after-dispose / FlutterError in log. Review finding (overlay-remove-before-guard) verified.
- AC2 aggressive Home lifecycle stress (bg/fg + tab hops): no dispose error. (am start relaunch re-fired pre-auth 401s -> logged out; artifact of stress method, re-login clean.)
