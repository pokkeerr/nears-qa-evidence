# NEARS-417 QA progress (live)
device: emulator-5554 (Android 17/API 37) | branch feat/NEARS-417-search-input-dls @308a6710

## Live observations (Android emulator-5554, light mode)
- [PASS] pick-map pill renders as Nears pill (brPill rounded), filled state: location_on pin + address + trailing search glyph — 417-pill-filled-light.png
- [PASS] tapping the pill opens LocationSearchDialogWidget (focused search field, navy focus ring, keyboard) — 417-search-dialog-light.png
- backstop: search_location_widget_test.dart + nears_input_validator_test.dart + no_data_screen_test.dart = 16 tests PASS

## Parcel flow (highest-risk) — light mode
- [PASS] parcel Pickup-location pill renders as brPill (Sender Info tab) — 417-parcel-pickup-pill-light.png
- [PASS] pickup/destination toggle works: tapping Receiver Info tab (after sender validation) swaps to destination pill (setIsSender/setIsPickedUp fired) — 417-parcel-destination-pill-light.png
- [PASS] tapping destination pill (isEnabled-set) opens LocationSearchDialogWidget + fires setIsPickedUp side-effect; live geocode suggestions returned, NO runtime errors — 417-parcel-destination-dialog-light.png
- NOTE: sender form filled with throwaway in-memory values (QATester/501234567/qa.fixture@example.com) for tab navigation only; NO parcel order placed, NO DB write

## Dark mode
- [PASS] pick-map pill in dark: navyContainer fill, MINT location pin + white address + muted search glyph all legible — 417-pill-filled-dark.png
- [PASS] dark search dialog: navyContainer field, "Search Location" hint legible (textOnNavyDim), no contrast fail — 417-search-dialog-dark.png (UX F-3 dark-disabled-glyph fix confirmed)

## RTL (Arabic)
- [PASS] pick-map pill mirrors correctly under RTL: search glyph LEFT / location pin RIGHT, address legible, navy fill, mint pin (dark+RTL) — 417-pill-rtl-dark.png
