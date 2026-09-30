# NEARS-3941 fix-cycle-2 delta matrix (qa_sha 8b2c042cc, emulator-5558, wm size 1080x2400; 320dp=density 540, 360dp=480)

price w = per-glyph a11y node span (device px); scale ratio = new/first (same glyph text => text scale). Sticky-row overflow log lines: 0 in every cell (only non-sticky lines: checkout_screen_shimmer_view.dart:53 (NEARS-3873), payment_method_bottom_sheet.dart, bottom_section.dart:399 due-payment body row, n_item_card.dart:1964 - all pre-existing per baseline).

| fix2 cell | first-run cell | price w px (new / first) | label slot px (new / first) | gap px | row-top->CTA px (new / first) | zero-bounds | off-screen | CTA |
|---|---|---|---|---|---|---|---|---|
| fix2-1b-nontax-4d-EN-320dp-1.0x | fix-E-nontax-4d-EN-320dp-1.0x | 456 / 456 | 448 / 448 | 41 | 311 / 311 | 0 | [] | True |
| fix2-1b-nontax-4d-EN-360dp-1.3x | fix-E-nontax-4d-EN-360dp-1.3x | 528 / 528 | 396 / 396 | 36 | 408 / 408 | 0 | [] | True |
| fix2-1b-nontax-4d-EN-360dp-1.0x | fix-E-nontax-4d-EN-360dp-1.0x | 405 / 405 | 519 / 519 | 36 | 276 / 276 | 0 | [] | True |
| fix2-1-nontax-4d-EN-320dp-1.3x | fix-E-nontax-4d-EN-320dp-1.3x | 536 / 586 | 368 / 318 | 41 | 459 / 580 | 0 | [] | True |
| fix2-7-nontax-3d-EN-320dp-1.3x | fix-A-nontax-3d-EN-320dp-1.3x | 533 / 533 | 371 / 371 | 41 | 459 / 459 | 0 | [] | True |
| fix2-7-nontax-3d-AR-320dp-1.3x | fix-K-nontax-3d-AR-320dp-1.3x | 466 / 466 | 438 / 438 | 41 | 473 / 473 | 0 | [] | True |
| fix2-4-nontax-4d-AR-320dp-1.3x | fix-H-nontax-4d-AR-320dp-1.3x | 527 / 527 | 377 / 377 | 41 | 473 / 473 | 0 | [] | True |
| fix2-5-taxincl-3d-AR-320dp-1.3x | fix-L-taxincl-3d-AR-320dp-1.3x | 466 / 466 | 438 / 438 | 41 | 607 / 607 | 0 | [] | True |
| fix2-2-taxincl-3d-EN-320dp-1.3x | fix-B-taxincl-3d-EN-320dp-1.3x | 533 / 533 | 371 / 371 | 41 | 520 / 520 | 0 | [] | True |
| fix2-7-nontax-3d-EN-320dp-1.0x | fix-A-nontax-3d-EN-320dp-1.0x | 410 / 410 | 495 / 495 | 40 | 311 / 311 | 0 | [] | True |
| fix2-7-nontax-3d-AR-320dp-1.0x | fix-K-nontax-3d-AR-320dp-1.0x | 358 / 358 | 547 / 547 | 40 | 321 / 321 | 0 | [] | True |
| fix2-4-nontax-4d-AR-320dp-1.0x | fix-H-nontax-4d-AR-320dp-1.0x | 405 / 405 | 500 / 500 | 40 | 321 / 321 | 0 | [] | True |
| fix2-5-taxincl-3d-AR-320dp-1.0x | fix-L-taxincl-3d-AR-320dp-1.0x | 358 / 358 | 547 / 547 | 40 | 375 / 375 | 0 | [] | True |
| fix2-7-nontax-3d-EN-360dp-1.3x | fix-A-nontax-3d-EN-360dp-1.3x | 474 / 474 | 450 / 450 | 36 | 408 / 408 | 0 | [] | True |
| fix2-7-nontax-3d-AR-360dp-1.3x | fix-K-nontax-3d-AR-360dp-1.3x | 415 / 415 | 509 / 509 | 36 | 312 / 312 | 0 | [] | True |
| fix2-4-nontax-4d-AR-360dp-1.3x | fix-H-nontax-4d-AR-360dp-1.3x | 469 / 469 | 455 / 455 | 36 | 312 / 312 | 0 | [] | True |
| fix2-5-taxincl-3d-AR-360dp-1.3x | fix-L-taxincl-3d-AR-360dp-1.3x | 415 / 415 | 509 / 509 | 36 | 432 / 432 | 0 | [] | True |
| fix2-2-taxincl-3d-EN-360dp-1.3x | fix-B-taxincl-3d-EN-360dp-1.3x | 474 / 474 | 450 / 450 | 36 | 462 / 462 | 0 | [] | True |
| fix2-7-nontax-3d-EN-360dp-1.0x | fix-A-nontax-3d-EN-360dp-1.0x | 364 / 364 | 560 / 560 | 36 | 276 / 276 | 0 | [] | True |
| fix2-7-nontax-3d-AR-360dp-1.0x | fix-K-nontax-3d-AR-360dp-1.0x | 319 / 319 | 605 / 605 | 36 | 285 / 285 | 0 | [] | True |
| fix2-3-duepay-4d-EN-320dp-1.3x | fix-F-duepay-4d-EN-320dp-1.3x | 536 / 586 | 368 / 318 | 41 | 459 / 459 | 0 | [] | True |
| fix2-6-duepay-4d-AR-320dp-1.3x | fix-I-duepay-4d-AR-320dp-1.3x | 527 / 527 | 377 / 377 | 41 | 473 / 473 | 0 | [] | True |
| fix2-2-taxincl-4d-EN-320dp-1.3x | - | 536 / - | 368 / - | 41 | 520 / - | 0 | [] | True |
| fix2-2-taxincl-4d-EN-360dp-1.3x | - | 528 / - | 396 / - | 36 | 462 / - | 0 | [] | True |
| fix2-2-taxincl-4d-EN-320dp-1.0x | - | 456 / - | 448 / - | 41 | 358 / - | 0 | [] | True |
| fix2-5-taxincl-4d-AR-320dp-1.3x | - | 527 / - | 377 / - | 41 | 675 / - | 0 | [] | True |
| fix2-5-taxincl-4d-AR-360dp-1.3x | - | 469 / - | 455 / - | 36 | 432 / - | 0 | [] | True |
| fix2-5-taxincl-4d-AR-320dp-1.0x | - | 405 / - | 500 / - | 40 | 375 / - | 0 | [] | True |
