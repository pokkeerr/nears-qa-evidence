# QA Evidence — NEARS-290

**Single-store Home (trimmed-hero, model b) · Verdict: ✅ PASS**

Fixture: zone-3 / store-59 (single-store) vs zone-2 (multi-store control). Each shot maps to an acceptance criterion.

### 1 — Single-store Home shows the trimmed navy hero
![Single-store Home hero](01_singlestore_home_hero.png)

### 2 — Bottom of Home: duplicate All-Stores surfaces suppressed
![No all-stores list at bottom](02_singlestore_bottom_no_allstores.png)

### 3 — Tapping the hero opens store 59 (no boot-time auto-nav)
![Store 59 via hero tap](03_store59_via_hero_tap.png)

### 4 — Cold start rests on Home (no navigation race)
![Cold start rests on Home](04_coldstart_rests_on_home.png)

### 5 — Control: multi-store zone 2 still shows All-Stores
![Multi-store zone 2 all-stores present](05_multistore_zone2_allstores_present.png)

### 6 — Checkout reachable in the single-store flow
![Single-store checkout](06_singlestore_checkout.png)

---
*Generated from `nears/docs/qa-evidence/NEARS-290/` under the public-repo scrub policy (no live secrets; verified clean).*
