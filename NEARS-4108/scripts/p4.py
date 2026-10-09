import sys,statistics; sys.path.insert(0,"/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad")
from q4108 import *
CP="Passw0rd!x1"; DP="Zx9#qLm!Tr7vB2"
def body(ep,ident,tok):
    if ep.startswith("cust"):
        b={"verification_method":"email","email":ident,"reset_token":tok}
        if ep=="cust_reset": b.update(password=CP,confirm_password=CP)
        return b
    b={"phone":ident,"reset_token":tok}
    if ep=="dm_reset": b.update(password=DP,confirm_password=DP)
    return b
section("S6 (k) timing class: wrong-code, 10 REG-nocode vs 10 UNREG per endpoint (host busy with other sessions' flutter tests; noisy)")
R={"cust_verify":("michael.brown@demo.com","nobody.4108@demo.com"),"cust_reset":("michael.brown@demo.com","nobody.4108@demo.com"),
   "dm_verify":("+101700000003","+101799999999"),"dm_reset":("+101700000003","+101799999999")}
summary={}
for ep,(reg,unreg) in R.items():
    tr=[];tu=[]
    for rnd in range(2):
        reset_state()
        for i in range(5):
            tok="%06d"%(900001+rnd*10+i)
            tr.append(req("timing REG %s r%d.%d"%(ep,rnd,i),ep,body(ep,reg,tok))["t"])
            tu.append(req("timing UNREG %s r%d.%d"%(ep,rnd,i),ep,body(ep,unreg,tok))["t"])
    summary[ep]=(statistics.median(tr),statistics.median(tu),min(tr),min(tu),max(tr),max(tu))
    s="TIMING %s: REG median=%.3fs UNREG median=%.3fs ratio=%.2f (min %.3f/%.3f max %.3f/%.3f)"%((ep,)+summary[ep][:2]+(summary[ep][0]/summary[ep][1],)+summary[ep][2:])
    log(s); print(s)
