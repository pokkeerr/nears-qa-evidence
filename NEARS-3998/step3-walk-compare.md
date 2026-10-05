# NEARS-3998 step 3 - emulator walk, BASE 60a9cce5e vs TIP e9c074823 (English + light, emulator-5554, pkg com.izzes.nears)

Same recipe, same script, same emulator, same own backend (:8231, scratch DB). Screens compared by uiautomator label dumps (step3-uidump-*.txt), logs by the `flutter` logcat tag (stack-frame lines excluded: moved functions change class/file names by construction), FA by `location_permission_result` events (step3-fa-*.txt).

| step | observed (base == tip) |
| --- | --- |
| 1a revoke, cold start | rationale screen (Enable location / Not now); Enable -> REAL OS dialog (Precise/Approximate/While using/Only this time/Don't allow); Allow -> pick-map with resolved address + pin; FA granted/precise=1/source=rationale |
| 1a' Approximate grant | granted, precise=0, source=rationale (both builds) |
| 1b Not now | pick-map, no OS dialog, no permission event |
| 2 deny, deny | 1st deny: denied + [FAIL] LocationPermissionDenied -> pick-map; 2nd deny: denied_forever + [FAIL] LocationPermissionDeniedForever -> pick-map; FAB -> permission dialog ("You denied location permission forever...", Close/Dismiss/Settings) + [FAIL] "checkPermission - permission denied forever" |
| 3 grant + geo fix, cold start | straight to pick-map, no rationale, no OS dialog, auto-resolved address, inZone=true |
| 4 denied, FAB | OS dialog, Don't allow -> snackbar "You have to allow location permission to use your location" + [FAIL] LocationPermissionDenied "checkPermission - permission denied" + paired [ERR] "error snackbar shown" |
| 5 service off (location_mode 0) | Google "Device location / Location Accuracy" requestService prompt; left unanswered for 6 s: [FAIL] LocationPermissionResolutionTimeout "timed out after 6s" + FA result=timeout/source=os_prompt, pick-map stays; answered "No thanks" in time (5c): pick-map, no [FAIL] (the _locationCheck false branch) |
| 6 entry points | access-location "Use Current Location" (access_location_screen.dart:650 caller) -> home in zone 1; home address chip -> navigateToLocationScreen('home') -> pick-map; pick-map Confirm Location -> home (address save); splash with saved address -> home, destination=home |

Totals over 14 captured steps: [FAIL] lines base 5 == tip 5 (same reasons); FA permission events identical (4 + approx); `Get.find ... not found` lines 0 in both; no unhandled exception; the only `Exception: app_error` is the paired AppLogger.error under showCustomSnackBar in step 4, present in both.
Normalised flutter-line multisets equal for 13/14 steps; the 14th (s6c, pick-map opened from the home chip) differs by one `location: inZone=true` line: pick-map camera-idle geocode/zone call count varies run to run within EACH build (3 repeats: tip 1/6, 1/6, 1/2, 1/4, 1/4, 2/6 inZone/zone-id lines; base 1/4, 2/6, 2/6): GoogleMap timing noise, not the permission flow.
UNVERIFIABLE on emulator: address_bottom_sheet_widget.dart:87 caller (dashboard "Hey welcome back" sheet needs no usable persisted address while at the dashboard from splash; unreachable under the NEARS-469 launch decision); the "superseded call" arms and the hung-platform-channel read-timeout arm (need a hung channel; covered by the nets' fake-async tests).
