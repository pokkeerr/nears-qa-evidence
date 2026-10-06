# WALK M (step 3, fixed flag path, no bursts): staples save + add all, reorder, a variation row (store 2 Dove 250ml), an add-on row (restaurant item with add-ons, flag ON). usage VAR=tip|base
source ./lib.sh
echo "# WALK M VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
DB=nears_qa_3993s3
mysql -u root $DB -e "delete from customer_staple_items; delete from customer_staple_schedules where user_id=2; update orders set user_id=2 where id=91415" 2>> $EV/steps.log
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
# M1 staples save + add all (single store)
fresh 1store; settle 3 20; snap M0-basket
ui_tap "Profile" --exact >/dev/null 2>&1; w 3; for i in 1 2 3; do nodes | /usr/bin/grep -aq 'My Staples' && break; swipe_rel 0.3; sleep 1; done
mark; ui_tap "My Staples" >/dev/null 2>&1; w 4; snap M1-staples-empty
ui_tap "Save current cart" --exact >/dev/null 2>&1; w 3; snap M1-save-sheet
ui_tap "Save staple" --exact >/dev/null 2>&1; w 4; snap M1-staples-saved; reqlog "M1 staples save"
tapn 'Weekly staples*' 1; w 3; snap M1-staples-expanded
mark; ui_tap "Add all to cart" --exact >/dev/null 2>&1; w 4; settle 3 15; snap M1-after-add-all-a; w 2; snap M1-after-add-all-b; reqlog "M1 add all"
rowtap "Rice 5kg" "Increase quantity"; step "M1-rice-plus-after-add-all"; settle 2 10
rowtap "Rice 5kg" "Decrease quantity"; step "M1-rice-minus-after-add-all"; settle 2 10
# M2 reorder (order 91415 of store 1, one line of item 40, assigned to the walk user in the scratch DB)
fresh 1store; settle 3 20; mark
ui_tap "Profile" --exact >/dev/null 2>&1; w 3; ui_tap "My Orders" --exact >/dev/null 2>&1; w 4; snap M2-orders
ui_tap "Reorder" --exact >/dev/null 2>&1; w 5; settle 3 15; reqlog "M2 reorder"; snap M2-after-reorder-a; w 2; snap M2-after-reorder-b
rowtap "Chicken Tender Vegan" "Increase quantity"; step "M2-chicken-plus"; settle 2 10
rowtap "Chicken Tender Vegan" "Decrease quantity"; step "M2-chicken-minus"; settle 2 10
# M3 variation row (flag OFF): Rice (store 1) + Dove 250ml (store 2) + Banana
fresh variant; settle 3 20; mark; snap M3-top
rowtap "Dove Whitening Body Spray" "Increase quantity"; step "M3-dove-plus"; settle 2 10
rowtap "Dove Whitening Body Spray" "Decrease quantity"; step "M3-dove-minus"; settle 2 10
rowtap "Banana" "Increase quantity"; step "M3-banana-plus"; settle 2 10
rowtap "Dove Whitening Body Spray" "Remove Dove Whitening Body Spray"; w 1; tapn "Undo" 1; step "M3-dove-remove-undo"; settle 2 10
rowtap "Dove Whitening Body Spray" "Remove Dove Whitening Body Spray"; w 6; step "M3-dove-remove-final"
# M4 add-on row (flag ON, mixed): Rice (store 1), Double Bacon Burger + add-ons (store 4), Thin Crust Margherita (store 4)
bash $S/flag.sh on >> $EV/steps.log 2>&1; bash $S/fd.sh on >> $EV/steps.log 2>&1
fresh addon; settle 4 25; mark; snap M4-top
for i in 1 2 3; do swipe_rel 0.4; w 1.2; done; snap M4-mid; scroll_top
reveal "Double Bacon Burger" "Increase quantity"; rowtap "Double Bacon Burger" "Increase quantity"; step "M4-bacon-plus"; settle 2 10
rowtap "Double Bacon Burger" "Decrease quantity"; step "M4-bacon-minus"; settle 2 10
rowtap "Double Bacon Burger" "Decrease quantity"; step "M4-bacon-zero"; settle 2 10
bash $S/flag.sh off >> $EV/steps.log 2>&1; bash $S/fd.sh off >> $EV/steps.log 2>&1
errs > $EV/errs-M.txt
echo "# M done $(date +%T)" >> $EV/steps.log
