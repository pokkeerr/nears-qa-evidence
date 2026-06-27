# NEARS-478 QA progress — remove "Deliver To" body row

- Build: worktree feat/NEARS-478-remove-deliver-to-body-row @ ed29cc3d (base), 1 uncommitted file module_view.dart
- Device: emulator-5556 · UserApp built+ran from worktree · light mode
- Account: customer@nears.com (2 saved addresses: zone1 Demo/Dhaka + zone2 Abu Dhabi)

| AC | Verdict | Evidence | Logs |
|----|---------|----------|------|
| AC1 no body address-card row | PASS | 01,04,05 — single appbar "Deliver To" node only; no Abu Dhabi card in body; holds zone1+zone2+RTL | clean |
| AC2 appbar selector → picker → switch re-renders | PASS | 02 sheet, 03 zone2 render; get-zone-id 200; bidirectional switch z1<->z2 | clean |
| AC3 no orphan gap / clean flow | PASS | 01,03,04 — sector list flows to carousel cleanly, mirrors guest baseline 00 | clean |
| AC4 banner/sector/carousel regression | PASS | 04 banner carousel (3 LIMITED OFFER), Grocery sector nav works, Recommended renders | clean |

- Guest baseline (block-less, already shipping): 00
- Arabic/RTL light-mode home clean: 05
- No ui_errors / runtime errors / [FAIL]/[ERR] across the whole flow.
- Verdict: PASS
