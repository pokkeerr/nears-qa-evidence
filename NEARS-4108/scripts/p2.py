import sys,re; sys.path.insert(0,"/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad")
from q4108 import *
CP="Passw0rd!x1"; DP="Zx9#qLm!Tr7vB2"
def cv(ident, kind, tok):
    b={"verification_method":kind,"reset_token":tok}; b[kind]=ident; return b
def cr(ident, kind, tok):
    b=cv(ident,kind,tok); b.update(password=CP,confirm_password=CP); return b
def dv(p,tok): return {"phone":p,"reset_token":tok}
def dr(p,tok): return {"phone":p,"reset_token":tok,"password":DP,"confirm_password":DP}
CL=[("cust-email","UNREG","nobody.4108@demo.com","email","cust"),("cust-email","REG","sophie.davis@demo.com","email","cust"),
    ("cust-phone","UNREG","+101699999999","phone","cust"),("cust-phone","REG","+101600000004","phone","cust"),
    ("dm","UNREG","+101799999999",None,"dm"),("dm","REG","+101700000003",None,"dm")]
def call(flow,which,ident,kind,tok,label):
    ep=flow+"_"+which
    if flow=="cust": body=(cv if which=="verify" else cr)(ident,kind,tok)
    else: body=(dv if which=="verify" else dr)(ident,tok)
    return req(label,ep,body)
def norm(m): return re.sub(r"\d+","N",m) if m else m
def run(name, plan):
    # plan: list of 7 endpoint choices ('verify'/'reset'); tokens vary per attempt (all wrong, valid-shape)
    section("S2 run %s plan=%s"%(name,plan)); print(reset_state())
    out={c[:3]:[] for c in CL}
    for i,which in enumerate(plan):
        for cls,reg,ident,kind,flow in CL:
            tok="%06d"%(700001+i)
            r=call(flow,which,ident,kind,tok,"%s %s %s #%d"%(name,cls,reg,i+1))
            out[(cls,reg,ident)].append(r)
    for cls in ("cust-email","cust-phone","dm"):
        u=[v for k,v in out.items() if k[0]==cls and k[1]=="UNREG"][0]; g=[v for k,v in out.items() if k[0]==cls and k[1]=="REG"][0]
        sameraw=[sig(a)==sig(b) for a,b in zip(u,g)]
        samenorm=[(a["status"],a["code"],norm(a["message"]))==(b["status"],b["code"],norm(b["message"])) for a,b in zip(u,g)]
        log("RESULT %s %s: positions identical(exact)=%s identical(modulo seconds/minutes digits)=%s statuses UNREG=%s REG=%s"%(name,cls,sameraw,samenorm,[x["status"] for x in u],[x["status"] for x in g]))
        print("RESULT",name,cls,"exact",sameraw,"norm",samenorm,"UNREG",[(x["status"],x["code"]) for x in u][5:],"REG",[(x["status"],x["code"]) for x in g][5:])
        print("   msgs UNREG:",[x["message"] for x in u][5:]," REG:",[x["message"] for x in g][5:])
    log("cache keys: "+sel("select `key`, value from cache where `key` like '%pwreset:attempts:%'"))
run("A(verify x6, then reset)",["verify"]*6+["reset"])
run("B(reset x6, then verify)",["reset"]*6+["verify"])
run("C(3 verify + 2 reset shared budget, 6th verify, 7th reset)",["verify"]*3+["reset"]*2+["verify","reset"])
print("DONE")
