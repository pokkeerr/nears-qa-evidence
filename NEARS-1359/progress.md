# NEARS-1359 NQtyStepper — QA progress (light, emulator-5554)
- AC1 cart stepper: PASS — Whole Milk 6→7 (increase), 7→6 (decrease), decrement-to-0 removed the line (3→2). mint circles/navy glyphs. logs clean. shots 03,04
- AC2 item-card compactWhenZero: PASS — compact + at qty0 (Tomatoes/Watermelon/Sugar); Red Apples qty1 = expanded −/1/+ row, same grid. smaller circles h32. shots 02,05,06
- AC5 a11y: cart stepper exposes "Increase quantity"/"Decrease quantity" nodes (PASS). item-card labels merged into NSurfaceCard onTap node (pre-existing structural) — followup.
- boots clean, ui_errors empty throughout.
- AC3 RTL: pending on 5556
- AC4 dark: DEFERRED (golden-covered) — not booted
