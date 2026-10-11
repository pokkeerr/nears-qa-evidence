#!/bin/bash
(crontab -l | grep -v "'/usr/bin/php' <ROOT>/Admin/public/artisan dm:disbursement") | crontab -

(crontab -l | grep -v "'/usr/bin/php' <ROOT>/Admin/public/artisan store:disbursement") | crontab -

