#!/bin/bash
# observe.sh <label> <req_line_marker> <logcat_HH:MM:SS local marker>
# Appends everything to observations.txt and prints it.
B=/Users/Apple/.nears/qa/NEARS-3977/baseline; Q=/Users/Apple/.nears/qa/NEARS-3977/qa-c0
{
echo "################ $1  (observed $(date -u +%H:%M:%S)Z)"
echo "--- requests (cart endpoints) since line $2:"
sed -n "$(( $2 + 1 )),\$p" $B/requests.jsonl | python3 $Q/reqfmt.py
echo "--- app log (NET/analytics/FAIL/ERR/WARN, excl. semantics assertion noise) since $3:"
awk -v t="$3" '$2>=t' $Q/logcat.log | /usr/bin/grep -a ' flutter :' | /usr/bin/grep -a -v 'framework_error' | /usr/bin/grep -a -E '\[NET\]|analytics|\[FAIL\]|\[ERR\]|\[WARN\]|\[EVT\]' | /usr/bin/grep -a -v -E 'NET\] (GET )?endpoint=/api/v1/(items|stores|categories|banners|campaigns|flash-sales|customer/suggested)' | cut -c19-300
echo "--- semantics framework_error count since $3: $(awk -v t="$3" '$2>=t' $Q/logcat.log | /usr/bin/grep -a -c 'framework_error library')"
echo "--- FA Logging event since $3:"
awk -v t="$3" '$2>=t' $Q/logcat.log | /usr/bin/grep -a 'Logging event' | /usr/bin/grep -a -E 'cart|quantity' | cut -c19-500
echo "--- DB:"
mysql -u root -N -e "select id,item_id,quantity,variation,module_id,updated_at from nears_qa_cartrow.carts where user_id=6 and is_guest=0 order by id" | sed 's/^/  /'
echo "--- display:"
python3 $Q/dump.py | /usr/bin/grep -E 'Tones|^\[9[0-9]{2},399\]' | /usr/bin/grep -v Remove | sed 's/^/  /'
} 2>&1 | tee -a $Q/observations.txt
