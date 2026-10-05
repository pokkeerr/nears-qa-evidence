# Walk table: base 14a8a12e9 vs tip ceef9de9d, same recipe (recipe.sh/recipe2.sh), 3 runs per build, EN + light, emulator-5554

Columns: get-zone-id requests per step window attributed by the logging proxy (wire counts, window markers), UI state equal = label+enabled+clickable dump identical (address text normalised), [FAIL] set equal = normalised [FAIL] line multiset identical in that window.

| step | get-zone-id req base [r1,r2,r3] | tip [r1,r2,r3] | ui state equal | [FAIL] set equal |
|---|---|---|---|---|
| R1_cold_fresh | [2, 2, 2] | [2, 2, 2] | 3/3 | 3/3 |
| R2a_drag_inzone | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R2b_drag_out_of_zone | [6, 6, 6] | [6, 6, 6] | 3/3 | 3/3 |
| R2c_fab_back_in_zone | [2, 1, 1] | [1, 1, 1] | 3/3 | 2/3 |
| R2d_fab_twice_ttl | [1, 1, 1] | [1, 1, 1] | 3/3 | 2/3 |
| R2e_zoom_restore | [2, 2, 2] | [2, 2, 2] | 3/3 | 3/3 |
| R2f_two_quick_drags | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R3_confirm_to_home | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R3b_dismiss_login_sheet | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R4_kill_relaunch_saved_addr | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R5_home_pull_refresh | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R6_chip_to_pickmap | [3, 2, 2] | [2, 1, 2] | 3/3 | 3/3 |
| R7a_zone500_drag | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R7b_zone_restored_drag | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R7c_back_to_home | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R7d_zone500_home_refresh | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R7e_zone_restored_home_refresh | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R8a_airplane_home_refresh | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R8b_airplane_off_try_again | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R9a_profile_login_screen | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R9b_signin | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R9c_home_after_login | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R10_home_after_login | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R11a_chip_sheet | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R11b_select_marina | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R12a_basket | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R12b_checkout | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R12c_change_select_addr | [0, 0, 0] | [0, 0, 0] | 3/3 | 3/3 |
| R12d_change_use_current_location | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R12e_back_to_home | [1, 1, 1] | [1, 1, 1] | 3/3 | 3/3 |
| R13_chip_select_dhaka | [1, 1, 1] | [1, 1, 1] | 1/3 | 3/3 |
