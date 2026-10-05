#!/usr/bin/env python3
"""QA-own mutation driver. SCRATCH worktree only. usage: mut.py [ids...]"""
import subprocess, sys, os, re, json, time
R = "/Users/Apple/Projects/nears-qa3998-mut/UserApp"
S = "/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/qa3998/"
F = "lib/features/location/controllers/location_permission_flow.dart"
C = "lib/features/location/controllers/location_controller.dart"
NEW = ["test/features/location/location_permission_flow_test.dart",
       "test/features/location/location_permission_dialog_pops_test.dart",
       "test/features/location/location_permission_entry_points_test.dart"]
NETS = ["test/baseline/location/location_permission_sequence_baseline_test.dart",
        "test/baseline/location/location_permission_gps_baseline_test.dart",
        "test/baseline/location/location_entry_point_routes_baseline_test.dart",
        "test/features/location/check_permission_late_location_check_test.dart",
        "test/features/location/location_permission_timeout_nears_3583_test.dart",
        "test/features/location/access_location_connectivity_race_test.dart",
        "test/features/location/access_location_pickmap_route_test.dart",
        "test/features/location/location_controller_part1_test.dart",
        "test/baseline/location/location_route_outcome_baseline_test.dart"]

M = []
def m(i, f, old, new, desc): M.append((i, f, old, new, desc))

# ---- owner: run()
m("Q01", F, "    _checkPermissionEpoch++;\n    await resolveChain(", "    await resolveChain(", "run: epoch bump removed")
m("Q02", F, "    _checkPermissionEpoch++;\n    await resolveChain(", "    _checkPermissionEpoch += 2;\n    await resolveChain(", "run: epoch bump by 2")
m("Q03", F, "    bool hasInternet = await checkInternet();\n    if (!hasInternet) {", "    _checkPermissionEpoch++;\n    bool hasInternet = await checkInternet();\n    if (!hasInternet) {", "run: extra epoch bump BEFORE checkInternet (offline run moves epoch)")
m("Q04", F, "    if (!hasInternet) {\n      AppLogger.failure(\n        const LocationNoInternetAbort(),", "    if (hasInternet) {\n      AppLogger.failure(\n        const LocationNoInternetAbort(),", "run: internet branch inverted")
m("Q05", F, "'location: _checkPermission aborted — no internet',\n      );\n      return;\n    }", "'location: _checkPermission aborted — no internet',\n      );\n    }", "run: offline return removed")
m("Q06", F, "await resolveChain(page, alreadyOnPickMap: alreadyOnPickMap);", "await resolveChain(page);", "run: alreadyOnPickMap dropped to resolveChain")
m("Q07", F, "await resolveChain(page, alreadyOnPickMap: alreadyOnPickMap);", "await resolveChain(page, alreadyOnPickMap: true);", "run: alreadyOnPickMap forced true")
m("Q08", F, "await resolveChain(page, alreadyOnPickMap: alreadyOnPickMap);", "await resolveChain('home', alreadyOnPickMap: alreadyOnPickMap);", "run: page forced home")
# ---- handleResolutionTimeout
m("Q09", F, "    if (!_isCurrentCheckPermission(epoch)) return;\n    _checkPermissionEpoch++;\n    AppLogger.failure(\n      const LocationPermissionResolutionTimeout(),", "    _checkPermissionEpoch++;\n    AppLogger.failure(\n      const LocationPermissionResolutionTimeout(),", "timeout arm: stale-epoch guard removed")
m("Q10", F, "    _checkPermissionEpoch++;\n    AppLogger.failure(\n      const LocationPermissionResolutionTimeout(),", "    AppLogger.failure(\n      const LocationPermissionResolutionTimeout(),", "timeout arm: epoch bump removed")
m("Q11", F, "    _logPermissionResult('timeout', precise: false);", "", "timeout arm: analytics timeout event removed")
m("Q12", F, "    _logPermissionResult('timeout', precise: false);", "    _logPermissionResult('timeout', precise: true);", "timeout arm: precise true")
m("Q13", F, "    if (Get.isDialogOpen ?? false) {\n      Get.back();\n    }\n    _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);\n  }\n\n  void _logPermissionResult", "    _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);\n  }\n\n  void _logPermissionResult", "timeout arm: dialog close removed")
m("Q14", F, "    if (Get.isDialogOpen ?? false) {\n      Get.back();\n    }\n    _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);\n  }\n\n  void _logPermissionResult", "    Get.back();\n    _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);\n  }\n\n  void _logPermissionResult", "timeout arm: Get.back unconditional (isDialogOpen guard dropped)")
m("Q15", F, "    _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);\n  }\n\n  void _logPermissionResult", "    _navigateToPickMapFallback(page, alreadyOnPickMap: false);\n  }\n\n  void _logPermissionResult", "timeout arm: alreadyOnPickMap not passed (forced false)")
m("Q16", F, "    _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);\n  }\n\n  void _logPermissionResult", "    _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);\n    _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);\n  }\n\n  void _logPermissionResult", "timeout arm: fallback navigation doubled")
# ---- bounds
m("Q17", F, "permission = await Geolocator.checkPermission().timeout(_checkPermissionTimeout);", "permission = await Geolocator.checkPermission().timeout(const Duration(seconds: 7));", "read side: bound 7 s")
m("Q18", F, "permission = await Geolocator.checkPermission().timeout(_checkPermissionTimeout);", "permission = await Geolocator.checkPermission().timeout(const Duration(seconds: 5));", "read side: bound 5 s")
m("Q19", F, ").timeout(_checkPermissionTimeout);\n      } on TimeoutException {", ").timeout(const Duration(seconds: 7));\n      } on TimeoutException {", "tail side: bound 7 s")
m("Q20", F, ").timeout(_checkPermissionTimeout);\n      } on TimeoutException {", ").timeout(const Duration(seconds: 5));\n      } on TimeoutException {", "tail side: bound 5 s")
m("Q21", F, "static const Duration _checkPermissionTimeout = Duration(seconds: 6);", "static const Duration _checkPermissionTimeout = Duration(milliseconds: 6001);", "constant bound 6001 ms (both sides)")
m("Q22", F, "static const Duration _rationaleGateReadTimeout = Duration(seconds: 2);", "static const Duration _rationaleGateReadTimeout = Duration(milliseconds: 2001);", "rationale gate bound 2001 ms")
m("Q23", F, "static const Duration _rationaleGateReadTimeout = Duration(seconds: 2);", "static const Duration _rationaleGateReadTimeout = Duration(milliseconds: 1999);", "rationale gate bound 1999 ms")
m("Q24", F, "      permission = await readPermission()\n          .timeout(_rationaleGateReadTimeout);", "      permission = await readPermission();", "rationale gate: bound removed") if False else None
# ---- resolvePermissionAndLocate
m("Q25", F, "    final int epoch = _checkPermissionEpoch;\n\n    LocationPermission permission;", "    final int epoch = 0;\n\n    LocationPermission permission;", "resolve: epoch captured as constant 0")
m("Q26", F, "    } on TimeoutException {\n      _handleResolutionTimeout(page, epoch, alreadyOnPickMap: alreadyOnPickMap);\n      return;\n    }\n    if (!_isCurrentCheckPermission(epoch)) return;\n", "    } on TimeoutException {\n      _handleResolutionTimeout(page, epoch, alreadyOnPickMap: alreadyOnPickMap);\n      return;\n    }\n", "resume point 1 (after permission read) guard removed")
m("Q27", F, "      permission = await Geolocator.requestPermission();\n      if (!_isCurrentCheckPermission(epoch)) return;\n", "      permission = await Geolocator.requestPermission();\n", "resume point 2 (after requestPermission) guard removed")
m("Q28", F, "      unawaited(_recordPermissionPromptResult(permission));", "", "prompt result recording removed")
m("Q29", F, "    if (permission == LocationPermission.denied) {\n      permission = await Geolocator.requestPermission();", "    if (permission == LocationPermission.denied || permission == LocationPermission.deniedForever) {\n      permission = await Geolocator.requestPermission();", "requestPermission also for deniedForever")
m("Q30", F, "        permission == LocationPermission.deniedForever\n            ? const LocationPermissionDeniedForever()\n            : const LocationPermissionDenied(),", "        const LocationPermissionDenied(),", "denied sentinel always plain denied")
m("Q31", F, "    } else if (page == 'home') {", "    } else if (page == 'homee') {", "page home branch broken")
m("Q32", F, "          epoch,\n          alreadyOnPickMap: alreadyOnPickMap,\n        ).timeout", "          epoch + 1,\n          alreadyOnPickMap: alreadyOnPickMap,\n        ).timeout", "resolveTail gets epoch+1")
m("Q33", F, "          epoch,\n          alreadyOnPickMap: alreadyOnPickMap,\n        ).timeout", "          epoch,\n        ).timeout", "resolveTail alreadyOnPickMap dropped")
m("Q34", F, "      } catch (_) {\n        if (!_isCurrentCheckPermission(epoch)) return;\n        AppLogger.failure(\n          const LocationFetchFailure(),", "      } catch (_) {\n        AppLogger.failure(\n          const LocationFetchFailure(),", "tail catch: stale-epoch guard removed")
m("Q35", F, "          'location: post-permission fetch failed — falling back to pick-map',\n        );\n        if (Get.isDialogOpen ?? false) {\n          Get.back();\n        }\n", "          'location: post-permission fetch failed — falling back to pick-map',\n        );\n", "tail catch: dialog close removed")
m("Q36", F, "          'location: post-permission fetch failed — falling back to pick-map',\n        );\n        if (Get.isDialogOpen ?? false) {\n          Get.back();\n        }\n", "          'location: post-permission fetch failed — falling back to pick-map',\n        );\n        if (Get.isDialogOpen ?? false) {\n          Get.back();\n          Get.back();\n        }\n", "tail catch: second Get.back")
m("Q37", F, "        AppLogger.failure(\n          const LocationFetchFailure(),\n          StackTrace.current,\n          'location: post-permission fetch failed", "        AppLogger.warn(\n          'location: post-permission fetch failed", "tail catch: failure log removed (paired AppLogger)") if False else None
m("Q38", F, "          'location: post-permission fetch failed — falling back to pick-map',\n        );\n        if (Get.isDialogOpen ?? false) {\n          Get.back();\n        }\n        _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);", "          'location: post-permission fetch failed — falling back to pick-map',\n        );\n        if (Get.isDialogOpen ?? false) {\n          Get.back();\n        }\n        _navigateToPickMapFallback(page, alreadyOnPickMap: false);", "tail catch: fallback alreadyOnPickMap forced false")
m("Q39", F, "      } on TimeoutException {\n        _handleResolutionTimeout(page, epoch, alreadyOnPickMap: alreadyOnPickMap);\n      } catch (_) {", "      } on TimeoutException {\n        _handleResolutionTimeout(page, epoch + 1, alreadyOnPickMap: alreadyOnPickMap);\n      } catch (_) {", "tail timeout arm: handler gets epoch+1 (never current)")
m("Q40", F, "      } on TimeoutException {\n        _handleResolutionTimeout(page, epoch, alreadyOnPickMap: alreadyOnPickMap);\n      } catch (_) {", "      } on TimeoutException {\n        _handleResolutionTimeout(page, epoch, alreadyOnPickMap: false);\n      } catch (_) {", "tail timeout arm: alreadyOnPickMap forced false")
m("Q41", F, "      _handleResolutionTimeout(page, epoch, alreadyOnPickMap: alreadyOnPickMap);\n      return;\n    }", "      _handleResolutionTimeout(page, epoch, alreadyOnPickMap: false);\n      return;\n    }", "read timeout arm: alreadyOnPickMap forced false")
# ---- resolveLocationAfterPermission
m("Q42", F, "    if (await _locationCheck()) {\n      if (!_isCurrentCheckPermission(epoch)) return;\n", "    if (await _locationCheck()) {\n", "tail resume (service true) guard removed")
m("Q43", F, "      // await, so\n" if False else "    } else {\n      // NEARS-1632-R2 (review fix cycle 2) — `_locationCheck()` is itself an\n      // await (location.serviceEnabled()/requestService()); its `false`\n      // resolution is a resume point just like its `true` sibling above and\n      // needs the same guard, not just the branch that reaches Get.dialog.\n      if (!_isCurrentCheckPermission(epoch)) return;\n", "    } else {\n", "tail resume (service false) guard removed")
m("Q44", F, "      if (!alreadyOnPickMap) {\n        unawaited(Get.dialog(const NSpinnerBox(), barrierDismissible: false));", "      if (true) {\n        unawaited(Get.dialog(const NSpinnerBox(), barrierDismissible: false));", "loader opened even when already on pick-map")
m("Q45", F, "      await currentLocation().then((\n        value,\n      ) {\n        if (!_isCurrentCheckPermission(epoch)) return;\n", "      await currentLocation().then((\n        value,\n      ) {\n", "post-fetch guard (.then) removed")
m("Q46", F, "        if (!alreadyOnPickMap &&\n            value.latitude != null) {", "        if (value.latitude != null) {", "onResolvedAddress: alreadyOnPickMap gate dropped")
m("Q47", F, "        if (!alreadyOnPickMap &&\n            value.latitude != null) {", "        if (!alreadyOnPickMap) {", "onResolvedAddress: latitude gate dropped")
m("Q48", F, "    if (!serviceEnabled) {\n      serviceEnabled = await location.requestService();\n    }", "", "_locationCheck: requestService removed")
m("Q49", F, "      _navigateToPickMapFallback(page, alreadyOnPickMap: alreadyOnPickMap);\n    }\n  }\n\n  Future<bool> _locationCheck", "      _navigateToPickMapFallback(page, alreadyOnPickMap: false);\n    }\n  }\n\n  Future<bool> _locationCheck", "service-off fallback: alreadyOnPickMap forced false")
# ---- helpers
m("Q50", F, "    if (alreadyOnPickMap) return;\n    unawaited(Get.toNamed(RouteHelper.getPickMapRoute(page, false)));", "    unawaited(Get.toNamed(RouteHelper.getPickMapRoute(page, false)));", "fallback: alreadyOnPickMap pass-through (skip) removed")
m("Q51", F, "RouteHelper.getPickMapRoute(page, false)));\n  }", "RouteHelper.getPickMapRoute(page, true)));\n  }", "fallback: canRoute true")
m("Q52", F, "      return permission == LocationPermission.denied;\n    } catch (_) {", "      return permission != LocationPermission.denied;\n    } catch (_) {", "rationale gate: result inverted")
m("Q53", F, "      return false;\n    }\n  }\n\n  // NEARS-1632 AC1", "      return true;\n    }\n  }\n\n  // NEARS-1632 AC1", "rationale gate catch: returns true")
m("Q54", F, "'precise': precise ? 1 : 0,", "'precise': 0,", "log: precise constant 0")
m("Q55", F, "'source': promptSource(),", "'source': 'os_prompt',", "log: source constant (prompt source not read)")
m("Q56", F, "'section': 'os_prompt',", "'section': 'body',", "log: section constant changed")
m("Q57", F, "'screen': 'location_rationale',", "'screen': 'location_prompt',", "log: screen constant changed")
m("Q58", F, "    if (!Get.isRegistered<AnalyticsService>()) return;\n    switch (permission) {", "    switch (permission) {", "prompt result: AnalyticsService registered guard removed")
m("Q59", F, "precise = await Geolocator.getLocationAccuracy() != LocationAccuracyStatus.reduced;", "precise = await Geolocator.getLocationAccuracy() == LocationAccuracyStatus.reduced;", "granted precise inverted")
m("Q60", F, "        _logPermissionResult('denied_forever', precise: false);", "        _logPermissionResult('denied', precise: false);", "deniedForever recorded as denied")
m("Q61", F, "        _logPermissionResult('denied', precise: false);\n    }", "        _logPermissionResult('timeout', precise: false);\n    }", "denied recorded as timeout")
m("Q62", F, "      case LocationPermissionOutcome.denied:\n        AppLogger.failure(", "      case LocationPermissionOutcome.denied:\n        AppLogger.failure(", "noop") if False else None
m("Q63", F, "        showCustomSnackBar('you_have_to_allow'.tr);", "", "checkPermission denied: snackbar removed")
m("Q64", F, "        unawaited(Get.dialog(const PermissionDialogWidget()));", "", "checkPermission deniedForever: dialog removed")
m("Q65", F, "      case LocationPermissionOutcome.granted:\n        onTap();", "      case LocationPermissionOutcome.granted:\n        break;", "checkPermission granted: onTap not invoked")
m("Q66", F, "  int get checkPermissionEpoch => _checkPermissionEpoch;", "  int get checkPermissionEpoch => _checkPermissionEpoch + 0 * 1 == 0 ? 0 : _checkPermissionEpoch;", "epoch getter hides epoch when zero? (equivalent-ish control)") if False else None
# ---- facade
m("Q70", C, "    resolveChain: resolvePermissionAndLocate,", "    resolveChain: _permissionFlow.resolvePermissionAndLocate,", "facade seam bypass: resolveChain -> owner's own")
m("Q71", C, "    resolveTail: resolveLocationAfterPermission,", "    resolveTail: _permissionFlow.resolveLocationAfterPermission,", "facade seam bypass: resolveTail -> owner's own")
m("Q72", C, "    readPermission: readLocationPermission,", "    readPermission: _permissionFlow.readLocationPermission,", "facade seam bypass: readPermission -> owner's own")
m("Q73", C, "    checkInternet: checkInternet,", "    checkInternet: () async => true,", "facade seam: checkInternet bypassed (always online)")
m("Q74", C, "    promptSource: () => _permissionPromptSource,", "    promptSource: () => 'os_prompt',", "facade seam: prompt source constant")
m("Q75", C, "    promptSource: () => _permissionPromptSource,", "    promptSource: _capturedPromptSource(),", "facade seam: prompt source captured at construction")
m("Q76", C, "    currentLocation: () => Get.find<LocationController>().getCurrentLocation(false),", "    currentLocation: () => getCurrentLocation(false),", "facade seam: currentLocation uses this instead of Get.find (instance identity)")
m("Q77", C, "    currentLocation: () => Get.find<LocationController>().getCurrentLocation(false),", "    currentLocation: _eagerCurrentLocation(),", "facade seam: eager Get.find at construction")
m("Q78", C, "    onResolvedAddress: (page, value) => _onPickAddressButtonPressed(\n      Get.find<LocationController>(),", "    onResolvedAddress: (page, value) => _onPickAddressButtonPressed(\n      this,", "facade seam: onResolvedAddress uses this instead of Get.find")
m("Q79", C, "    logEvent: _logEvent,", "    logEvent: (n, p) {},", "facade seam: logEvent no-op")
m("Q80", C, "  Future<void> checkPermission(Function onTap) =>\n      _permissionFlow.checkPermission(onTap);", "  Future<void> checkPermission(Function onTap) async =>\n      await _permissionFlow.checkPermission(onTap);", "delegate made async+await: checkPermission")
m("Q81", C, "  }) => _permissionFlow.resolvePermissionAndLocate(\n    page,\n    alreadyOnPickMap: alreadyOnPickMap,\n  );", "  }) async {\n    await _permissionFlow.resolvePermissionAndLocate(\n    page,\n    alreadyOnPickMap: alreadyOnPickMap,\n  );\n  }", "delegate made await-first: resolvePermissionAndLocate")
m("Q82", C, "  }) => _permissionFlow.resolvePermissionAndLocate(\n    page,\n    alreadyOnPickMap: alreadyOnPickMap,\n  );", "  }) => _permissionFlow.resolvePermissionAndLocate(\n    page,\n  );", "delegate drops alreadyOnPickMap: resolvePermissionAndLocate")
m("Q83", C, "  }) => _permissionFlow.resolveLocationAfterPermission(\n    page,\n    epoch,\n    alreadyOnPickMap: alreadyOnPickMap,\n  );", "  }) => _permissionFlow.resolveLocationAfterPermission(\n    page,\n    epoch,\n  );", "delegate drops alreadyOnPickMap: resolveLocationAfterPermission")
m("Q84", C, "  }) => _permissionFlow.resolveLocationAfterPermission(\n    page,\n    epoch,\n    alreadyOnPickMap: alreadyOnPickMap,\n  );", "  }) => _permissionFlow.resolveLocationAfterPermission(\n    page,\n    epoch + 1,\n    alreadyOnPickMap: alreadyOnPickMap,\n  );", "delegate epoch+1: resolveLocationAfterPermission")
m("Q85", C, "  int get checkPermissionEpochForTest => _permissionFlow.checkPermissionEpoch;", "  int get checkPermissionEpochForTest => 0;", "epoch-for-test getter constant 0")
m("Q86", C, "  int get checkPermissionEpochForTest => _permissionFlow.checkPermissionEpoch;", "  int get checkPermissionEpochForTest => LocationPermissionFlow(\n    locationServiceInterface: locationServiceInterface, checkInternet: checkInternet,\n    resolveChain: resolvePermissionAndLocate, resolveTail: resolveLocationAfterPermission,\n    readPermission: readLocationPermission, logEvent: _logEvent, promptSource: () => _permissionPromptSource,\n    currentLocation: () => getCurrentLocation(false), onResolvedAddress: (p, v) {},\n  ).checkPermissionEpoch;", "epoch read from a second owner instance")
m("Q87", C, "  Future<LocationPermission> readLocationPermission() =>\n      _permissionFlow.readLocationPermission();", "  Future<LocationPermission> readLocationPermission() =>\n      Geolocator.checkPermission();", "readLocationPermission delegate bypasses owner (direct Geolocator, equivalent?)")
# call sites
m("Q88", C, "        unawaited(_permissionFlow.run(page));", "        unawaited(_permissionFlow.run(page, alreadyOnPickMap: true));", "call site navigateToLocationScreen: alreadyOnPickMap forced true")
m("Q89", C, "        unawaited(_permissionFlow.run(page));", "", "call site navigateToLocationScreen: run removed")
m("Q90", C, "    unawaited(_permissionFlow.run(page, alreadyOnPickMap: true));\n  }", "    unawaited(_permissionFlow.run(page));\n  }", "call site _routeColdStart: alreadyOnPickMap dropped")
m("Q91", C, "    if (await _permissionFlow.shouldShowLocationRationale()) {", "    if (!await _permissionFlow.shouldShowLocationRationale()) {", "call site _routeColdStart: gate inverted")
m("Q92", C, "      await _permissionFlow.run(page, alreadyOnPickMap: true);\n    } finally {", "      await _permissionFlow.run(page);\n    } finally {", "call site enableLocationFromRationale: alreadyOnPickMap dropped")
m("Q93", C, "      await _permissionFlow.run(page, alreadyOnPickMap: true);\n    } finally {", "      unawaited(_permissionFlow.run(page, alreadyOnPickMap: true));\n    } finally {", "call site enableLocationFromRationale: run not awaited (finally resets source early)")
m("Q94", C, "      _permissionPromptSource = 'os_prompt';\n    }\n  }\n\n  // NEARS-3583: dismiss", "    }\n  }\n\n  // NEARS-3583: dismiss", "enableLocationFromRationale: source reset removed")

if __name__ == "__main__":
    ids = set(sys.argv[1:])
    M = [x for x in M if x]
    res = open(S + "mut_results.jsonl", "a")
    def run(files):
        for f in files:
            lbl = "NEARS-3998-s3-qa-mut-" + os.path.basename(f)[:-5]
            p = subprocess.run(["python3", os.path.expanduser("~/.nears/bin/mem-guard.py"), "--label", lbl, "--max-gb", "6", "--wait-s", "3600", "--",
                                "/Users/Apple/Tools/flutter/bin/flutter", "test", "--reporter", "compact", f], cwd=R, capture_output=True, text=True)
            out = (p.stdout + p.stderr)
            if p.returncode != 0:
                kind = "COMPILE" if re.search(r"Failed to load|Compilation failed|Error: ", out) else "RED"
                return f, p.returncode, kind
        return None, 0, "GREEN"
    for (i, f, old, new, desc) in M:
        if ids and i not in ids: continue
        path = os.path.join(R, f)
        src = open(path).read()
        n = src.count(old)
        if n != 1:
            rec = {"id": i, "desc": desc, "status": "ABORT-old-count=%d" % n}
            res.write(json.dumps(rec) + "\n"); res.flush(); print(rec); continue
        # helper stubs for Q75/Q77 need a tiny extra helper; inject as needed
        new_src = src.replace(old, new, 1)
        if "_capturedPromptSource()" in new:
            new_src = new_src.replace("  Future<void> checkPermission(Function onTap) =>", "  String Function() _capturedPromptSource() { final s = _permissionPromptSource; return () => s; }\n\n  Future<void> checkPermission(Function onTap) =>", 1)
        if "_eagerCurrentLocation()" in new:
            new_src = new_src.replace("  Future<void> checkPermission(Function onTap) =>", "  Future<AddressModel> Function() _eagerCurrentLocation() { final c = Get.find<LocationController>(); return () => c.getCurrentLocation(false); }\n\n  Future<void> checkPermission(Function onTap) =>", 1)
        open(path, "w").write(new_src)
        d = subprocess.run(["git", "diff", "-U0", "--", f], cwd=R, capture_output=True, text=True).stdout
        landed = len(d.strip()) > 0
        try:
            if not landed:
                rec = {"id": i, "desc": desc, "status": "ABORT-not-landed"}
            else:
                red_file, rc, kind = run(NEW)
                stage = "new"
                if kind == "GREEN":
                    red_file, rc, kind = run(NETS); stage = "nets"
                rec = {"id": i, "desc": desc, "file": f, "status": ("KILLED-" + kind) if kind != "GREEN" else "SURVIVOR",
                       "by": red_file, "stage": stage if kind != "GREEN" else "none", "rc": rc, "diff": d[-600:]}
        finally:
            subprocess.run(["git", "checkout", "--", f], cwd=R)
        chk = subprocess.run(["git", "diff", "--stat"], cwd=R, capture_output=True, text=True).stdout.strip()
        rec["restored_clean"] = (chk == "")
        res.write(json.dumps(rec) + "\n"); res.flush()
        print(i, rec["status"], rec.get("by"), "clean" if rec["restored_clean"] else "DIRTY!", flush=True)
