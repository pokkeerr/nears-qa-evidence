#!/bin/bash
(crontab -l | grep -v "'/usr/bin/php' <ROOT>/Admin/public/artisan dm:disbursement") | crontab -
(crontab -l ; echo "59 23 * * 6 '/usr/bin/php' <ROOT>/Admin/public/artisan dm:disbursement") | crontab -
(crontab -l | grep -v "'/usr/bin/php' <ROOT>/Admin/public/artisan store:disbursement") | crontab -
(crontab -l ; echo "00 00 * * 0 '/usr/bin/php' <ROOT>/Admin/public/artisan store:disbursement") | crontab -
