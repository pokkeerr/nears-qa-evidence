#!/bin/bash
Q=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s3/qa
while [ ! -f $Q/bewatch.stop ]; do
  if ! lsof -i :8494 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "$(date +%T) backend :8494 DEAD -> restarting" >> $Q/bewatch.log
    ( nohup bash $Q/startbe.sh >/dev/null 2>&1 < /dev/null & )
    sleep 4
  fi
  if ! lsof -i :8493 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "$(date +%T) proxy :8493 DEAD" >> $Q/bewatch.log
  fi
  sleep 2
done
