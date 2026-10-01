#!/bin/bash
# flag.sh <0|1> : toggle cross_module_basket (id 228) on the COPY ONLY, clear the COPY's cache, read back.
set -e
V=$1
mysql -u root -e "update nears_qa_cartrow.business_settings set value='$V' where id=228 and \`key\`='cross_module_basket'"
(cd /Users/Apple/Projects/nears/Admin && DB_DATABASE=nears_qa_cartrow CACHE_DRIVER=database php artisan cache:clear >/dev/null)
echo "copy=$(mysql -u root -N -e 'select value from nears_qa_cartrow.business_settings where id=228') primary=$(mysql -u root -N -e 'select value from multi_food_db.business_settings where id=228') primary_cache_rows=$(mysql -u root -N -e 'select count(*) from multi_food_db.cache')"
echo "GET /api/v1/config cross_module_basket=$(curl -s -H 'moduleId: 1' -H 'zoneId: [2]' http://127.0.0.1:8101/api/v1/config | python3 -c 'import json,sys;print(json.load(sys.stdin).get("cross_module_basket"))')"
