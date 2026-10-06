#!/usr/bin/env python3
"""QA spot re-run of the step-3 mutation rows in a SCRATCH worktree (qa-tip, detached at TIP). Live worktree never touched.
usage: mut.py [name ...]   (default: all)"""
import os, subprocess, sys, re, json, time, shutil, filecmp

S3 = "/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s3"
Q = S3 + "/qa"
LIVE = "/Users/Apple/Projects/nears-NEARS-3993-u2-step3/UserApp"
SCR = S3 + "/qa-tip/UserApp"
OUT = Q + "/mut"
os.makedirs(OUT, exist_ok=True)
CACHE = "lib/features/cart/domain/helpers/cart_group_totals_cache.dart"
CTRL = "lib/features/cart/controllers/cart_controller.dart"
B = "test/baseline/cart/"
F_ = B + "cart_group_totals_key_freshness_baseline_test.dart"
S_ = B + "cart_group_totals_scope_baseline_test.dart"
E_ = B + "cart_group_totals_key_encoding_baseline_test.dart"
D_ = B + "cart_derivation_counts_baseline_test.dart"
R_ = B + "cart_screen_derivations_baseline_test.dart"
U_ = "test/features/cart/cart_group_totals_cache_test.dart"
PR_ = B + "cart_mutation_prime_read_baseline_test.dart"
OI_ = B + "cart_mutation_output_inputs_baseline_test.dart"
GP_ = B + "cart_grouping_pricing_basis_baseline_test.dart"

M = {
    "M1-never-hits": (CACHE, "if (entry != null && sameKey(entry.key, key)) {", "if (false && entry != null && sameKey(entry.key, key)) {", [D_, R_, S_]),
    "M2-never-invalidated": (CACHE, "if (entry != null && sameKey(entry.key, key)) {", "if (entry != null) {", [F_, PR_, OI_]),
    "M3-drop-row-quantity": (CACHE, "        ..add(row.quantity);", "        ;", [S_, U_]),
    "M4-drop-store-identity": (CACHE, "<Object?>[store, rows.length]", "<Object?>[rows.length]", [S_, U_]),
    "M5-drop-clock-part-on-hit": (CACHE, "if (entry.clockKey == null || sameKey(entry.clockKey!, clockKey())) {", "if (true) {", [F_, U_]),
    "M6-drop-digits": (CACHE, "discount.maxDiscount, digits()];", "discount.maxDiscount];", [F_, U_]),
    "M7-drop-list-length-prefix": (CACHE, "    key.add(list.length);\n    for (final E element in list) {", "    for (final E element in list) {", [E_, U_, F_]),
    "M8-static-cache": (CACHE, "  final Map<int, _Entry> _entries = <int, _Entry>{};", "  static final Map<int, _Entry> _entries = <int, _Entry>{};", [S_, E_, U_, F_]),
    "M9-server-basis-per-store": (CTRL, "final bool serverBasis = totals.every((t) => t.server != null);", "final bool serverBasis = totals.any((t) => t.server != null);", [S_, OI_, GP_]),
    "M10-retainOnly-noop": (CACHE, "    _entries.removeWhere((int id, _Entry _) => !keep.contains(id));", "    keep.length;", [S_, U_]),
    "M11-drop-item-price": (CACHE, "        item.price,\n        item.discount,", "        item.discount,", [F_, U_]),
    "M12-clock-race-check-dropped": (CACHE, "if (!clockRead || freshClock![0] == totals.server!.live) {", "if (true) {", [U_, F_]),
}

def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)

def run_test(f, tag, outname):
    cmd = ["python3", os.path.expanduser("~/.nears/bin/mem-guard.py"), "--label", "NEARS-3993-s3-qa-mut-" + tag, "--max-gb", "6", "--wait-s", "3600", "--",
           "/Users/Apple/Tools/flutter/bin/flutter", "test", f]
    p = subprocess.run(cmd, cwd=SCR, capture_output=True, text=True)
    txt = p.stdout + p.stderr
    open(outname, "w").write(txt)
    ok = bad = -1
    for l in txt.splitlines():
        m = re.match(r"^\d+:\d+ \+(\d+)(?: ~\d+)?(?: -(\d+))?", l)
        if m:
            ok = int(m.group(1)); bad = int(m.group(2) or 0)
    if "Some tests failed" not in txt and "All tests passed" not in txt:
        if "Failed to load" in txt or "Error:" in txt or "Compilation failed" in txt:
            return p.returncode, ok, bad, "LOADFAIL"
    return p.returncode, ok, bad, ("RED" if p.returncode else "GREEN")

def main():
    names = sys.argv[1:] or list(M)
    # unmutated green baseline of the scratch tree first (one cheap file)
    res = json.load(open(OUT + "/results.json")) if os.path.exists(OUT + "/results.json") else {}
    for n in names:
        rel, old, new, tests = M[n]
        path = os.path.join(SCR, rel); live = os.path.join(LIVE, rel)
        src = open(live).read()
        if src.count(old) != 1:
            res[n] = {"error": "old text count %d" % src.count(old)}; print(n, res[n]); continue
        # scratch tree must equal live before the mutation
        if not filecmp.cmp(path, live, shallow=False):
            shutil.copyfile(live, path)
        open(path, "w").write(src.replace(old, new))
        d = sh("git -C %s diff -U0 -- UserApp/%s" % (S3 + "/qa-tip", rel)).stdout
        open(OUT + "/diff-%s.txt" % n, "w").write(d)
        landed = bool(d.strip())
        rows = {}
        try:
            for t in tests:
                rc, ok, bad, kind = run_test(t, n, OUT + "/out-%s-%s.txt" % (n, os.path.basename(t)))
                rows[os.path.basename(t)] = {"rc": rc, "pass": ok, "fail": bad, "kind": kind}
        finally:
            shutil.copyfile(live, path)
        restored = filecmp.cmp(path, live, shallow=False)
        stat = sh("git -C %s diff --stat" % (S3 + "/qa-tip")).stdout.strip()
        res[n] = {"landed": landed, "rows": rows, "restored_bytes_equal": restored, "git_diff_stat_after_restore": stat}
        json.dump(res, open(OUT + "/results.json", "w"), indent=1)
        print(n, json.dumps(res[n]), flush=True)

main()
