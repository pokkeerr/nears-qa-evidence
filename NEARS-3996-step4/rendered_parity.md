# Rendered parity base vs tip (EN + light, emulator-5554, own screenshots kept OUTSIDE the repo and OUTSIDE this gallery: no screenshot published, they show a customer profile)

Method: same label-driven op list replayed on both builds; a11y text = sorted unique labels from uiautomator; pixels = PIL difference, status bar (clock) cropped, |d|>24. Control: two screenshots of one static screen 4 s apart = 0 differing pixels. A flung scroll can end at different offsets, so pixel parity is only claimed for static (no fling) screens and for list ends; the only two non-zero static pairs differ in a single text strip that is the Flash Sale countdown line.

| screen (static, no fling except where noted) | a11y text base==tip | differing px (|d|>24, status bar cropped) | % |
|---|---|---|---|
| V1_module_select | text-equal | 0 | 0.0000% |
| V2_pharmacy_top | text-equal | 800 | 0.0209% |
| V3_grocery_top | text-equal | 0 | 0.0000% |
| V4_food_top | text-equal | 3089 | 0.0809% |
| V5_shop_top | text-equal | 0 | 0.0000% |
| V6_popular_all | text-equal | 0 | 0.0000% |
| V7_latest_all | text-equal | 0 | 0.0000% |
| V8_pharm_bottom (pharmacy list bottom after page 2) | TEXT-DIFF | 1314451 | 34.4129% |

## Same-state pairs from the full walk (a11y text equal AND pixel diff)
| P02_grocery_bottom | text-equal | 0.0000% | 0 |
| P03_food_bottom | text-equal | 0.0000% | 0 |
| P03_food_chip_All | text-equal | 0.0004% | 14 |
| P03_food_chip_Fastest | text-equal | 0.0003% | 12 |
| P03_food_chip_Nearest | text-equal | 0.0003% | 11 |
| P03_food_chip_Newly_joined | text-equal | 0.0002% | 7 |
| P03_food_chip_Popular | text-equal | 0.0004% | 14 |
| P04_shop_latest_all | text-equal | 0.0000% | 0 |
| P04_shop_latest_refreshed | text-equal | 0.0000% | 0 |
| P04_shop_popular_all | text-equal | 0.0000% | 0 |
| P04_shop_popular_refreshed | text-equal | 0.0000% | 0 |
| P08_latest_reenter | text-equal | 0.0000% | 0 |
| P08_popular_reenter1 | text-equal | 0.0000% | 0 |
| T3_after_retry | text-equal | 0.0000% | 0 |
| T3_failure | text-equal | 0.0000% | 0 |

## Full-list order (first-seen order while scrolling to the end, store-card names) identical base vs tip; the Closed Now divider sits at the same place

### food (base == tip,       15 entries)
```
Spice Route Kitchen (Abu Dhabi)
Noodle Bar (Abu Dhabi)
Golden Wok (Abu Dhabi)
Mediterranean Bites (Abu Dhabi)
NEARS-3709 QA Restaurant 1
NEARS-3709 QA Restaurant 2
NEARS-3709 QA Restaurant 3
NEARS-3709 QA Restaurant 4
NEARS-3709 QA Restaurant 5
NEARS-3709 QA Restaurant 6
NEARS-3709 QA Restaurant 7
NEARS-3709 QA Restaurant 8
NEARS-3709 QA Restaurant 9
--- Closed Now divider ---
NEARS-3709 QA Restaurant 10
```
### grocery (base == tip,       17 entries)
```
5.0
Fresh local
Fresh supermarket
Online market
Sk General Store
Smart Shopping
Vegan Market
Veggie Market
Eco Market\n3.4
Morning Mart
Fast Market\n4.2
Supermarket
Test Store\n5.0
NEARS600 Offers QA Store
NEARS600 Zero Offer QA Store
--- Closed Now divider ---
NEARS-3708 QA Null-Schedule Store
```
### pharmacy (base == tip,       30 entries; all open, no divider)
```
Fast Market
Pharmacy
MediQuick Pharmacy (Abu Dhabi)
MediQuick Pharmacy (Abu Dhabi), Abu Dhabi
Family Health Pharmacy (Abu Dhabi)
Family Health Pharmacy (Abu Dhabi), Abu Dhabi
Green Cross Pharmacy (Abu Dhabi)
Green Cross Pharmacy (Abu Dhabi), Abu Dhabi
City Care Chemist (Abu Dhabi)
City Care Chemist (Abu Dhabi), Abu Dhabi
NEARS-3679 QA Pharmacy Zero Items Store
NEARS-3679 pharmacy zero-item QA fixture
NEARS-3679 QA Pharmacy Few Items Store
NEARS-3679 pharmacy few-items QA fixture
NEARS-3711 QA Pharmacy 24h 1
NEARS-3711 pharmacy home store-merge QA fixture
NEARS-3711 QA Pharmacy 24h 2
NEARS-3711 QA Pharmacy 24h 3
NEARS-3711 QA Pharmacy 24h 4
NEARS-3711 QA Pharmacy 24h 5
NEARS-3711 QA Pharmacy 24h 6
NEARS-3711 QA Pharmacy 24h 7
NEARS-3711 QA Pharmacy 24h 10
NEARS-3711 QA Pharmacy 24h 8
NEARS-3711 QA Pharmacy 24h 9
NEARS-3711 QA Pharmacy 24h 11
NEARS-3711 QA Pharmacy 24h 12
NEARS-3711 QA Pharmacy 24h 13
NEARS-3711 QA Pharmacy 24h 14
NEARS-3711 QA Pharmacy 24h 15
```
