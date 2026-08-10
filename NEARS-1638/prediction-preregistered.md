# NEARS-1638 — PRE-REGISTERED PREDICTION (written BEFORE any device measurement)

Written: 2026-08-10, device clock 13:22 +04, before `flutter run` completed.
Device: emulator-5558 (5554 rejected: 587680 KB free = ~574 MB, below the 800 MB floor;
5556 + 5560 locked by live pids 86430 / 39147).

## Shape under test (read from packages/nears_dls/lib/elements/inkwell/n_ink_well.dart, buildContent)
Semantics(label: p.semanticLabel, button: onTap != null)
  -> Material(color: Colors.transparent)
     -> InkWell(onTap, borderRadius: 0)
        -> Padding(EdgeInsets.zero)
           -> Center -> NIcon('info')   ~24dp, undecorated

This matches the NEARS-963 ledger shape `a11y-icon-label-needs-larger-decorated-tap-box-android`
exactly (zero padding, transparent Material, no BoxDecoration, icon-sized box).

## Prediction: OUTCOME A
I predict the info button's AccessibilityNodeInfo will carry a NON-EMPTY content-desc = "Info".

Reasoning: `Semantics(label:..., button:true)` directly wrapping an `InkWell` is the canonical
Flutter a11y idiom; the ancestor annotation and the InkWell's tap fragment are compatible and
compile to a single node. I know of no size/decoration dependence in Flutter's semantics
compiler. I therefore expect the NEARS-963 lesson to be NARROWED by this run.

Secondary predictions (all falsifiable in the same dump):
- P2: the same node is clickable="true".
- P3: validity control — sibling Back button shows content-desc="Back" (non-empty).
- P4: title "Refer and Earn" still announces as its own node (no absorption).
- P5: after switching to Arabic, content-desc = "معلومات" exactly (not "Info").
- P6: `ui_find "Info"` resolves exit 0 (it previously could not resolve this button at all).

## What would falsify me (Outcome B)
content-desc="" on the info node WHILE Back reads "Back" in the SAME dump.
If Back is ALSO empty -> instrument failure, not an AC failure; re-run on another device.
