#!/bin/bash
# flag.sh on|off : cross_module_basket in the SCRATCH DB copy + cache clear
v=0; [ "$1" = on ] && v=1
mysql -u root nears_qa_3993s5 -e "update business_settings set value='$v' where \`key\`='cross_module_basket'" || exit 1
cd /private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s5/qa/base/Admin && php artisan cache:clear 2>&1 | tail -1
curl -s http://127.0.0.1:8593/api/v1/config | python3 -c "import sys,json;print('config cross_module_basket =',json.load(sys.stdin).get('cross_module_basket'))"
