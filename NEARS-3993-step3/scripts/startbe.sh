#!/bin/bash
Q=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3993-s3/qa
cd $Q/../qa-base/Admin && exec -a qa3993srv $Q/qa3993srvbin -d pcre.jit=0 -S 127.0.0.1:8494 server.php >> $Q/serve.log 2>&1 < /dev/null
