import sys,subprocess
sys.path.insert(0,'/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa/scan')
from dartlex import *
def listing(src):
    hs=heads(class_body(src,'LocationController'))
    return hs, public(hs)
if __name__=='__main__':
    src=open(sys.argv[1]).read()
    hs,pub=listing(src)
    print(len(hs),len(pub),file=sys.stderr)
    for p in pub: print(p)
