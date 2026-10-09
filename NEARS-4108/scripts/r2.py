import sys,re,time; sys.path.insert(0,"/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad")
import q4108
from q4108 import *
def rq(label,ep,body):
    r=req(label,ep,body)
    if r["status"]==429:
        log("   (429 = throttle:auth limiter, not the lockout; no attempt spent; waiting 65s and retrying once)"); print("   429 limiter -> retry in 65s"); time.sleep(65); q4108._glob.clear(); q4108._hist.clear()
        r=req(label+" (retry)",ep,body)
    return r
def tok_email(e,cb="user"): return sel("select token from password_resets where email='%s' and created_by='%s'"%(e,cb))
def tok_phone(p): return sel("select token from password_resets where phone='%s' and created_by='user'"%p)
def cv(ident,kind,t): b={"verification_method":kind,"reset_token":t}; b[kind]=ident; return b
def cr(ident,kind,t,pw="NewPass#4108c"): b=cv(ident,kind,t); b.update(password=pw,confirm_password=pw); return b
def dv(p,t): return {"phone":p,"reset_token":t}
def dr(p,t,pw="Zx9#qLm!Tr7vB2"): return {"phone":p,"reset_token":t,"password":pw,"confirm_password":pw}
def wrongfor(t): return "%06d"%(((int(t)+1)%1000000))
section("R2 customer-email verify=200 with correct code (redo, the first try hit the 429 limiter)")
rq("forgot robert email","cust_forgot",{"verification_method":"email","email":"robert.taylor@demo.com"})
T=tok_email("robert.taylor@demo.com"); log("SELECTed robert email token=%s"%T)
v=rq("CORRECT verify cust email (robert)","cust_verify",cv("robert.taylor@demo.com","email",T))
print("verify email 200 expected:",v["status"],v["message"])
section("R3 block with a real pending code: 6 wrong -> 405; the CORRECT code during the block -> 405 on verify and reset; row kept")
for name,kind,ident,fg,flow,tokf in [("cust-email robert","email","robert.taylor@demo.com",None,"cust",lambda:T),
                                      ("cust-phone sophie","phone","+101600000004",{"verification_method":"phone","phone":"+101600000004"},"cust",lambda:tok_phone("+101600000004")),
                                      ("dm ali",None,"+971565656656",{"phone":"+971565656656"},"dm",lambda:tok_email("ali.hassan@demo.com","dm_api"))]:
    if fg: rq("forgot "+name,"cust_forgot" if flow=="cust" else "dm_forgot",fg)
    t=tokf(); log("SELECTed %s token=%s"%(name,t)); w=wrongfor(t)
    outs=[]
    for i in range(6):
        if flow=="cust": r=rq("%s wrong #%d"%(name,i+1),"cust_verify" if i%2==0 else "cust_reset",(cv(ident,kind,w) if i%2==0 else cr(ident,kind,w)))
        else: r=rq("%s wrong #%d"%(name,i+1),"dm_verify" if i%2==0 else "dm_reset",(dv(ident,w) if i%2==0 else dr(ident,w)))
        outs.append((r["status"],r["code"]))
    if flow=="cust":
        a=rq("%s CORRECT code during block (verify)"%name,"cust_verify",cv(ident,kind,t)); b=rq("%s CORRECT code during block (reset)"%name,"cust_reset",cr(ident,kind,t))
    else:
        a=rq("%s CORRECT code during block (verify)"%name,"dm_verify",dv(ident,t)); b=rq("%s CORRECT code during block (reset)"%name,"dm_reset",dr(ident,t))
    key="phone='%s'"%ident if kind=="phone" else ("email='%s'"%ident if kind=="email" else "email='ali.hassan@demo.com'")
    rows=sel("select count(*) from password_resets where %s"%key)
    print("RESULT",name,"wrong statuses",outs,"| correct during block: verify",a["status"],a["code"],"reset",b["status"],b["code"],"| row kept:",rows)
    log("RESULT %s wrong=%s correct-during-block verify=%s/%s reset=%s/%s row_kept=%s"%(name,outs,a["status"],a["code"],b["status"],b["code"],rows))
