# WALK G: mixed basket gate cards: store 7 (pharmacy) closed -> store gate card + whole-store Remove; Cola stock 1 with qty 2 -> row stock card
source ./lib.sh
echo "# WALK G VAR=$VAR start $(date +%T)" >> $EV/steps.log
[ -f $EV/requests.txt ] || : > $EV/requests.txt
mysql -u root multi_food_db_s3993 -e "update stores set active=1 where id=7; update items set stock=103 where id=97; update items set stock=45 where id=98"
PRE_LAUNCH='mysql -u root multi_food_db_s3993 -e "update stores set active=0 where id=7; update carts set quantity=2 where user_id=2 and item_id=98; update items set stock=1 where id=98"' fresh mixed
settle 4 25; mark
snap G0-top; for i in 1 2 3; do swipe_rel 0.4; w 1.5; snap "G0-mid$i"; done; scroll_bottom; snap G0-bottom; reqlog "G0 gate cards (flag ON, store 7 closed, Cola stock 1 qty 2)"

# G1 whole-store Remove from the closed-store gate card (HealthCare Pharmacy), then from the out-of-stock card (Nears Mart)
revealL 'HealthCare Pharmacy, Store is closed now'; snap G1-before-store7-remove; mark
tap_near 'HealthCare Pharmacy, Store is closed now' 'Remove'; w 0.5; snap G1-store7-removed-a; settle 3 20; snap G1-store7-removed-b; reqlog "G1 whole-store Remove (closed pharmacy)"
scroll_top; snap G2-before-store1-remove
tap_near 'Nears Mart, Out of Stock' 'Remove'; w 0.5; snap G2-store1-removed-a; settle 3 20; snap G2-store1-removed-b; reqlog "G2 whole-store Remove (out-of-stock grocery)"
mysql -u root multi_food_db_s3993 -e "update stores set active=1 where id=7; update items set stock=45 where id=98"
errs > $EV/errs-G.txt
echo "# G done $(date +%T)" >> $EV/steps.log
