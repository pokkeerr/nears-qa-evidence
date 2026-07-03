// NEARS-756 revert->behaviour proof (scratchpad, pure Dart, no product edit).
// Mirrors the exact operation the PRE-FIX code performed at three sites:
//   - initCall() loop:      offlineMethodList![selectedOfflineBankIndex]
//   - changesMethod():      offlineMethodList![selectedOfflineBankIndex]
//   - build() methodInfo:   offlineMethodList![selectedOfflineBankIndex]
// with a persisted index that survives on the singleton while the list is
// re-fetched shorter. Shows: pre-fix => RangeError; with clamp => safe.

void clamp(List list, int Function() get, void Function(int) set) {
  if (get() >= list.length) set(0);
}

void main() {
  // First visit: 3 methods, user selects index 2 (the 3rd). Index persists.
  int selectedOfflineBankIndex = 2;

  // Second visit: admin removed methods; re-fetched list shrank to length 1.
  final shrunk = ['method_9'];

  // --- PRE-FIX behaviour (no clamp) — the money-path RangeError ---
  try {
    final v = shrunk[selectedOfflineBankIndex]; // offlineMethodList![index]
    print('PRE-FIX: unexpectedly no throw -> $v');
  } catch (e) {
    print('PRE-FIX (no clamp): $e  <-- this is the NEARS-756 crash');
  }

  // --- POST-FIX behaviour (clampSelectedOfflineBankIndex then index) ---
  clamp(shrunk, () => selectedOfflineBankIndex, (v) => selectedOfflineBankIndex = v);
  print('POST-FIX: clamped index = $selectedOfflineBankIndex');
  final ok = shrunk[selectedOfflineBankIndex];
  print('POST-FIX: safe index -> $ok (no RangeError)');

  // --- Emptied-list case: clamp to 0, isNotEmpty guard shows empty-state ---
  int idx2 = 1;
  final emptied = <String>[];
  clamp(emptied, () => idx2, (v) => idx2 = v);
  print('EMPTIED: clamped index = $idx2, list.isEmpty = ${emptied.isEmpty} '
      '-> build() renders NearsEmptyState no_offline_method_available (no index)');

  // --- In-range case (AC2): index preserved ---
  int idx3 = 1;
  final full = ['m1', 'm2', 'm3'];
  clamp(full, () => idx3, (v) => idx3 = v);
  print('IN-RANGE (AC2): index unchanged = $idx3 (normal flow preserved)');
}
