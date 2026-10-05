# PD-S4-1 live probe and overtaken-response live probe (probe.sh), base 14a8a12e9 vs tip ceef9de9d, emulator-5554, EN + light

Recipe: logging proxy mode file switches get-zone-id. P1 = every 200 answer is held 25 s, the 404 is immediate: small in-zone drag, zoom out x4, 4 big swipes (out of zone), wait 32 s past the stale 200s. P2 = every get-zone-id answer held 6 s: guest home, pull-to-refresh (plain syncZoneData fetch in flight), 1.5 s later tap the address chip (pick-map opens, its marker fetch overtakes the plain one).

## pbase1
- P1_early: Service not available in this area | enabled=true | clickable=false ; Service not available in this area | enabled=false | clickable=false
- P1_stale200_then_out_of_zone: Service not available in this area | enabled=true | clickable=false ; Service not available in this area | enabled=false | clickable=false  | get-zone-id requests in window: 5
- P1b_restore: Confirm Location | enabled=true | clickable=true  | get-zone-id requests in window: 4
- P2b_plain_sync_overtaken_by_marker: Confirm Location | enabled=false | clickable=false  | get-zone-id requests in window: 2
- P2c_drag_inzone_after: Confirm Location | enabled=false | clickable=false  | get-zone-id requests in window: 1
- P2d_back_home_pull: Confirm Location | enabled=true | clickable=true  | get-zone-id requests in window: 4

## ptip1
- P1_early: Service not available in this area | enabled=true | clickable=false ; Service not available in this area | enabled=false | clickable=false
- P1_stale200_then_out_of_zone: Service not available in this area | enabled=true | clickable=false ; Service not available in this area | enabled=false | clickable=false  | get-zone-id requests in window: 5
- P1b_restore: Confirm Location | enabled=true | clickable=true  | get-zone-id requests in window: 4
- P2b_plain_sync_overtaken_by_marker: Confirm Location | enabled=false | clickable=false  | get-zone-id requests in window: 3
- P2c_drag_inzone_after: Confirm Location | enabled=false | clickable=false  | get-zone-id requests in window: 1
- P2d_back_home_pull: Confirm Location | enabled=true | clickable=true  | get-zone-id requests in window: 2

