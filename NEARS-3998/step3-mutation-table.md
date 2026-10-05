id | status | killed by | mutation
--- | --- | --- | ---
Q01 | KILLED-RED | location_permission_flow_test.dart | run: epoch bump removed
Q02 | KILLED-RED | location_permission_flow_test.dart | run: epoch bump by 2
Q03 | KILLED-RED | location_permission_flow_test.dart | run: extra epoch bump BEFORE checkInternet (offline run moves epoch)
Q04 | KILLED-RED | location_permission_flow_test.dart | run: internet branch inverted
Q05 | KILLED-RED | location_permission_flow_test.dart | run: offline return removed
Q06 | KILLED-RED | location_permission_flow_test.dart | run: alreadyOnPickMap dropped to resolveChain
Q07 | KILLED-RED | location_permission_flow_test.dart | run: alreadyOnPickMap forced true
Q08 | KILLED-RED | location_permission_flow_test.dart | run: page forced home
Q09 | KILLED-RED | location_permission_flow_test.dart | timeout arm: stale-epoch guard removed
Q10 | KILLED-RED | location_permission_flow_test.dart | timeout arm: epoch bump removed
Q11 | KILLED-RED | location_permission_flow_test.dart | timeout arm: analytics timeout event removed
Q12 | KILLED-RED | location_permission_flow_test.dart | timeout arm: precise true
Q13 | KILLED-RED | location_permission_dialog_pops_test.dart | timeout arm: dialog close removed
Q14 | KILLED-RED | location_permission_dialog_pops_test.dart | timeout arm: Get.back unconditional (isDialogOpen guard dropped)
Q15 | KILLED-RED | location_permission_flow_test.dart | timeout arm: alreadyOnPickMap not passed (forced false)
Q16 | SURVIVOR | - | timeout arm: fallback navigation doubled
Q17 | KILLED-RED | location_permission_flow_test.dart | read side: bound 7 s
Q18 | KILLED-RED | location_permission_flow_test.dart | read side: bound 5 s
Q19 | KILLED-RED | location_permission_flow_test.dart | tail side: bound 7 s
Q20 | KILLED-RED | location_permission_flow_test.dart | tail side: bound 5 s
Q21 | KILLED-RED | location_permission_flow_test.dart | constant bound 6001 ms (both sides)
Q22 | KILLED-RED | location_permission_flow_test.dart | rationale gate bound 2001 ms
Q23 | KILLED-RED | location_permission_flow_test.dart | rationale gate bound 1999 ms
Q25 | KILLED-RED | location_permission_flow_test.dart | resolve: epoch captured as constant 0
Q26 | KILLED-RED | location_permission_flow_test.dart | resume point 1 (after permission read) guard removed
Q27 | KILLED-RED | location_permission_flow_test.dart | resume point 2 (after requestPermission) guard removed
Q28 | KILLED-RED | location_permission_flow_test.dart | prompt result recording removed
Q29 | KILLED-RED | location_permission_flow_test.dart | requestPermission also for deniedForever
Q30 | KILLED-RED | location_permission_flow_test.dart | denied sentinel always plain denied
Q31 | KILLED-RED | location_permission_flow_test.dart | page home branch broken
Q32 | KILLED-RED | location_permission_flow_test.dart | resolveTail gets epoch+1
Q33 | KILLED-RED | location_permission_flow_test.dart | resolveTail alreadyOnPickMap dropped
Q34 | KILLED-RED | location_permission_flow_test.dart | tail catch: stale-epoch guard removed
Q35 | KILLED-RED | location_permission_flow_test.dart | tail catch: dialog close removed
Q36 | KILLED-RED | location_permission_dialog_pops_test.dart | tail catch: second Get.back
Q38 | KILLED-RED | location_permission_flow_test.dart | tail catch: fallback alreadyOnPickMap forced false
Q39 | KILLED-RED | location_permission_flow_test.dart | tail timeout arm: handler gets epoch+1 (never current)
Q40 | KILLED-RED | location_permission_flow_test.dart | tail timeout arm: alreadyOnPickMap forced false
Q41 | KILLED-RED | location_permission_flow_test.dart | read timeout arm: alreadyOnPickMap forced false
Q42 | KILLED-RED | location_permission_flow_test.dart | tail resume (service true) guard removed
Q43 | KILLED-RED | location_permission_flow_test.dart | tail resume (service false) guard removed
Q44 | KILLED-RED | location_permission_flow_test.dart | loader opened even when already on pick-map
Q45 | KILLED-RED | location_permission_flow_test.dart | post-fetch guard (.then) removed
Q46 | KILLED-RED | location_permission_flow_test.dart | onResolvedAddress: alreadyOnPickMap gate dropped
Q47 | KILLED-RED | location_permission_flow_test.dart | onResolvedAddress: latitude gate dropped
Q48 | KILLED-RED | location_permission_flow_test.dart | _locationCheck: requestService removed
Q49 | KILLED-RED | location_permission_flow_test.dart | service-off fallback: alreadyOnPickMap forced false
Q50 | KILLED-RED | location_permission_flow_test.dart | fallback: alreadyOnPickMap pass-through (skip) removed
Q51 | KILLED-RED | location_permission_flow_test.dart | fallback: canRoute true
Q52 | KILLED-RED | location_permission_flow_test.dart | rationale gate: result inverted
Q53 | KILLED-RED | location_permission_flow_test.dart | rationale gate catch: returns true
Q54 | KILLED-RED | location_permission_flow_test.dart | log: precise constant 0
Q55 | KILLED-RED | location_permission_flow_test.dart | log: source constant (prompt source not read)
Q56 | KILLED-RED | location_permission_flow_test.dart | log: section constant changed
Q57 | KILLED-RED | location_permission_flow_test.dart | log: screen constant changed
Q58 | KILLED-RED | location_permission_flow_test.dart | prompt result: AnalyticsService registered guard removed
Q59 | KILLED-RED | location_permission_flow_test.dart | granted precise inverted
Q60 | KILLED-RED | location_permission_flow_test.dart | deniedForever recorded as denied
Q61 | KILLED-RED | location_permission_flow_test.dart | denied recorded as timeout
Q63 | KILLED-RED | location_permission_flow_test.dart | checkPermission denied: snackbar removed
Q64 | KILLED-RED | location_permission_flow_test.dart | checkPermission deniedForever: dialog removed
Q65 | KILLED-RED | location_permission_flow_test.dart | checkPermission granted: onTap not invoked
Q70 | KILLED-RED | location_permission_flow_test.dart | facade seam bypass: resolveChain -> owner's own
Q71 | KILLED-RED | location_permission_flow_test.dart | facade seam bypass: resolveTail -> owner's own
Q72 | KILLED-RED | location_permission_flow_test.dart | facade seam bypass: readPermission -> owner's own
Q73 | KILLED-RED | location_permission_flow_test.dart | facade seam: checkInternet bypassed (always online)
Q74 | KILLED-RED | location_permission_flow_test.dart | facade seam: prompt source constant
Q75 | KILLED-RED | location_permission_flow_test.dart | facade seam: prompt source captured at construction
Q76 | KILLED-RED | location_permission_flow_test.dart | facade seam: currentLocation uses this instead of Get.find (instance identity)
Q77 | KILLED-RED | location_permission_flow_test.dart | facade seam: eager Get.find at construction
Q78 | KILLED-RED | location_permission_flow_test.dart | facade seam: onResolvedAddress uses this instead of Get.find
Q79 | KILLED-RED | location_permission_flow_test.dart | facade seam: logEvent no-op
Q80 | SURVIVOR | - | delegate made async+await: checkPermission
Q81 | SURVIVOR | - | delegate made await-first: resolvePermissionAndLocate
Q82 | KILLED-RED | location_permission_flow_test.dart | delegate drops alreadyOnPickMap: resolvePermissionAndLocate
Q83 | KILLED-RED | location_permission_flow_test.dart | delegate drops alreadyOnPickMap: resolveLocationAfterPermission
Q84 | KILLED-RED | location_permission_flow_test.dart | delegate epoch+1: resolveLocationAfterPermission
Q85 | KILLED-RED | location_permission_flow_test.dart | epoch-for-test getter constant 0
Q86 | KILLED-RED | location_permission_flow_test.dart | epoch read from a second owner instance
Q87 | SURVIVOR | - | readLocationPermission delegate bypasses owner (direct Geolocator, equivalent?)
Q88 | KILLED-RED | location_permission_flow_test.dart | call site navigateToLocationScreen: alreadyOnPickMap forced true
Q89 | KILLED-RED | location_permission_flow_test.dart | call site navigateToLocationScreen: run removed
Q90 | KILLED-RED | location_permission_flow_test.dart | call site _routeColdStart: alreadyOnPickMap dropped
Q91 | KILLED-RED | location_permission_flow_test.dart | call site _routeColdStart: gate inverted
Q92 | KILLED-RED | location_permission_flow_test.dart | call site enableLocationFromRationale: alreadyOnPickMap dropped
Q93 | KILLED-RED | location_permission_flow_test.dart | call site enableLocationFromRationale: run not awaited (finally resets source early)
Q94 | KILLED-RED | location_permission_flow_test.dart | enableLocationFromRationale: source reset removed
