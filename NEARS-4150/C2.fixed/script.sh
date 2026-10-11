#!/bin/bash
(crontab -l | grep -v "'/usr/bin/php' <ROOT>/Admin/public/artisan dm:disbursement") | crontab -
(crontab -l ; echo "30 18 28-31 * * '/usr/bin/php' <ROOT>/Admin/public/artisan dm:disbursement") | crontab -
(crontab -l | grep -v "'/usr/bin/php' <ROOT>/Admin/public/artisan store:disbursement") | crontab -
(crontab -l ; echo "05 09 28-31 * * '/usr/bin/php' <ROOT>/Admin/public/artisan store:disbursement") | crontab -
