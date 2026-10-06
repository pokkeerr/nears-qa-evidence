#!/bin/bash
# fd.sh on|off : admin free delivery by order amount (scratch DB copy) + cache clear
if [ "$1" = on ]; then
  mysql -u root nears_qa_3993s4 -e "update business_settings set value='free_delivery_by_order_amount' where \`key\`='admin_free_delivery_option'; update business_settings set value='40' where \`key\`='free_delivery_over'"
else
  mysql -u root nears_qa_3993s4 -e "update business_settings set value='free_delivery_to_all_store' where \`key\`='admin_free_delivery_option'; update business_settings set value=NULL where \`key\`='free_delivery_over'"
fi
cd /private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s4/qa/base/Admin && php artisan cache:clear 2>&1 | tail -1
curl -s http://127.0.0.1:8593/api/v1/config | python3 -c "import sys,json;d=json.load(sys.stdin);print('admin_free_delivery =',d.get('admin_free_delivery'),'| cross_module_basket =',d.get('cross_module_basket'))"
