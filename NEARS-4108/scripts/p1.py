import sys; sys.path.insert(0,"/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad")
from q4108 import *
CP="Passw0rd!x1"; DP="Zx9#qLm!Tr7vB2"
def cv(ident, kind, tok="654321"):
    b={"verification_method":kind,"reset_token":tok}; b[kind]=ident; return b
def cr(ident, kind, tok="654321"):
    b=cv(ident,kind,tok); b.update(password=CP,confirm_password=CP); return b
def dv(p,tok="654321"): return {"phone":p,"reset_token":tok}
def dr(p,tok="654321"): return {"phone":p,"reset_token":tok,"password":DP,"confirm_password":DP}
print(reset_state())
section("S1 (a) side-by-side wrong valid-shape code: UNREG vs REGISTERED(no pending code)")
res={}
for cls,unreg,reg,kind in [("cust-email","nobody.4108@demo.com","michael.brown@demo.com","email"),("cust-phone","+101699999999","+101600000003","phone")]:
    for ep,fn in [("cust_verify",cv),("cust_reset",cr)]:
        u=req("%s UNREG"%cls,ep,fn(unreg,kind)); g=req("%s REG-nocode"%cls,ep,fn(reg,kind))
        res[(cls,ep)]=(sig(u),sig(g)); print("   IDENTICAL:",sig(u)==sig(g))
for ep,fn in [("dm_verify",dv),("dm_reset",dr)]:
    u=req("dm UNREG",ep,fn("+101799999999")); g=req("dm REG-nocode",ep,fn("+101700000003"))
    res[("dm",ep)]=(sig(u),sig(g)); print("   IDENTICAL:",sig(u)==sig(g))
print({k:(v[0]==v[1]) for k,v in res.items()})
section("S3 (g/m) non-ASCII + JSON-number identifiers: registered-looking vs unregistered")
print(reset_state())
for ep,fn in [("cust_verify",cv),("cust_reset",cr)]:
    a=req("non-ascii email REG-lookalike",ep,fn("jámes.wilson@demo.com","email")); b=req("non-ascii email UNREG",ep,fn("ñobody.4108@demo.com","email"))
    print("   IDENTICAL:",sig(a)==sig(b))
    for kind,reg,unreg in [("phone",101600000001,101699999999)]:
        a=req("json-number phone REG",ep,fn(reg,kind)); b=req("json-number phone UNREG",ep,fn(unreg,kind))
        print("   IDENTICAL:",sig(a)==sig(b))
    a=req("non-ascii phone REG-lookalike",ep,fn("+١٠١٦٠٠٠٠٠٠٠١","phone")); b=req("non-ascii phone UNREG",ep,fn("+١٠١٦٩٩٩٩٩٩٩٩","phone"))
    print("   IDENTICAL:",sig(a)==sig(b))
for ep,fn in [("dm_verify",dv),("dm_reset",dr)]:
    a=req("DM json-number phone REG",ep,fn(101700000003)); b=req("DM json-number phone UNREG",ep,fn(101799999999))
    print("   IDENTICAL:",sig(a)==sig(b))
print("cache keys now:", sel("select count(*) from cache where `key` like '%pwreset:attempts:%'"))
