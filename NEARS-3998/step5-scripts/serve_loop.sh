#!/bin/bash
cd /Users/Apple/Projects/nears-NEARS-3998-u7-step5-suggestions/Admin
while [ ! -f /private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa/out/serve.stop ]; do
  PHP_CLI_SERVER_WORKERS=6 php artisan serve --host=127.0.0.1 --port=8334 >> /private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa/out/serve3.log 2>&1
  echo "serve exited rc=$? at $(date +%T)" >> /private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa/out/serve_restarts.log
  sleep 1
done
