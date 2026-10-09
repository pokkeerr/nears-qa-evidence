import sys,re; sys.path.insert(0,"/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad")
from q4108 import *
CP="Passw0rd!x1"
def cv(i,t): return {"verification_method":"email","email":i,"reset_token":t}
def cr(i,t): b=cv(i,t); b.update(password=CP,confirm_password=CP); return b
section("S4 (g) case/trailing-space variants share ONE counter (REG james.wilson vs UNREG nobody.4108)")
print(reset_state())
for name,vars_ in [("REG",["JAMES.WILSON@demo.com","james.wilson@demo.com","james.wilson@demo.com ","James.Wilson@Demo.com","JAMES.wilson@demo.COM","james.wilson@demo.com"]),
                   ("UNREG",["NOBODY.4108@demo.com","nobody.4108@demo.com","nobody.4108@demo.com ","Nobody.4108@Demo.com","NOBODY.4108@demo.COM","nobody.4108@demo.com"])]:
    res=[]
    for i,v in enumerate(vars_):
        which=cv if i%2==0 else cr
        ep="cust_verify" if i%2==0 else "cust_reset"
        res.append(req("variant %s #%d %r"%(name,i+1,v),ep,which(v,"%06d"%(810001+i))))
    print(name,"statuses:",[r["status"] for r in res],"6th code:",res[5]["code"])
    log("variant-%s statuses=%s"%(name,[(r["status"],r["code"]) for r in res]))
print("distinct pwreset keys after both:", sel("select count(*) from cache where `key` like '%pwreset:attempts:customer_email:%' and `key` not like '%:block'"))
print(sel("select `key`,value from cache where `key` like '%pwreset:attempts:%'"))
log("variant cache keys:\n"+sel("select `key`,value from cache where `key` like '%pwreset:attempts:%'"))
section("S5 (h) vendor flow untouched (live)")
print(reset_state())
a=req("vendor REG wrong code","vendor_verify",{"email":"demo.store@gmail.com","reset_token":"123123"})
b=req("vendor UNREG wrong code","vendor_verify",{"email":"nobody.4108@demo.com","reset_token":"123123"})
log("vendor: registered->%s unregistered->%s (vendor flow is out of scope of NEARS-4108; pre-existing exists: validator behaviour)"%(sig(a),sig(b)))
