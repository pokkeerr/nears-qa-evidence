# NEARS-1482 QA progress (live, emulator-5554, worktree 5a2a03bb)

| AC | Verdict | Evidence | Logs |
|---|---|---|---|
| AC1 sampled sites render NEmptyState | PASS | cart(2 mounts), not-logged-in, no-internet, review, category | clean |
| AC2 Symbols glyphs render, no tofu | PASS (4/5 reachable) | montage-glyphs.png, montage-inbox.png | clean |
| AC3 retry-while-offline visible feedback | **FAIL** | ac3-retry-offline-toast.png (no toast) + assertion log | `_AssertionError _scaffolds.isNotEmpty` |
| AC3d retry after reconnect navigates | PASS | home reload, 200s | clean |
| AC3e splash override, no toast | PASS | 2x config refetch, no breadcrumb | clean |
| AC3f breadcrumb content-free | PASS | `[ERR] msg="error snackbar shown"` | PII-safe |
| AC4 RTL | PASS (toast copy unverifiable) | ac4-rtl-*.png | same assertion in ar |
| AC5 CTA wiring | PASS (add-address dead branch) | login CTA -> sign-in | clean |

Automated: flutter test test/common/widgets/ -> 219/219 pass (does NOT catch AC3; harness wraps in Scaffold).
