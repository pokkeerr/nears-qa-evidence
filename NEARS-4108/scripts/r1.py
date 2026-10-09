import sys,re; sys.path.insert(0,"/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad")
from q4108 import *
OLD="123456789"; NEWC="NewPass#4108a"; NEWD="Zx9#qLm!Tr7vB2"; NEWC2="NewPass#4108b"
def tok_email(e,cb="user"): return sel("select token from password_resets where email='%s' and created_by='%s'"%(e,cb))
def tok_phone(p): return sel("select token from password_resets where phone='%s' and created_by='user'"%p)
def cv(ident,kind,t): b={"verification_method":kind,"reset_token":t}; b[kind]=ident; return b
def cr(ident,kind,t,pw): b=cv(ident,kind,t); b.update(password=pw,confirm_password=pw); return b
def dv(p,t): return {"phone":p,"reset_token":t}
def dr(p,t,pw): return {"phone":p,"reset_token":t,"password":pw,"confirm_password":pw}
def clog(ident,kind,pw): return {"login_type":"manual","email_or_phone":ident,"password":pw,"field_type":kind}
def dlog(p,pw): return {"phone":p,"password":pw}
section("R1 issue codes for positive set (michael email+phone, DM carlos) through the app's forgot-password")
req("forgot michael email","cust_forgot",{"verification_method":"email","email":"michael.brown@demo.com"})
req("forgot michael phone","cust_forgot",{"verification_method":"phone","phone":"+101600000003"})
req("forgot DM carlos","dm_forgot",{"phone":"+101700000003"})
TE=tok_email("michael.brown@demo.com"); TP=tok_phone("+101600000003"); TD=tok_email("carlos.rodriguez@demo.com","dm_api")
log("SELECTed tokens: michael email=%s phone=%s dm carlos=%s (read-only SELECT)"%(TE,TP,TD))
print("tokens:",TE,TP,TD)
def wrongfor(t): return "%06d"%((int(t)+1)%1000000 if int(t)<999999 else 0)
section("R1b side-by-side wrong code: registered-WITH-pending-code vs unregistered, all four endpoints")
res=[]
for kind,reg,unreg,t in [("email","michael.brown@demo.com","nobody.4108@demo.com",TE),("phone","+101600000003","+101699999999",TP)]:
    w=wrongfor(t)
    a=req("REG-WITH-CODE cust %s verify"%kind,"cust_verify",cv(reg,kind,w)); b=req("UNREG cust %s verify"%kind,"cust_verify",cv(unreg,kind,w)); res.append(sig(a)==sig(b)); print("   identical:",res[-1])
    a=req("REG-WITH-CODE cust %s reset"%kind,"cust_reset",cr(reg,kind,w,NEWC)); b=req("UNREG cust %s reset"%kind,"cust_reset",cr(unreg,kind,w,NEWC)); res.append(sig(a)==sig(b)); print("   identical:",res[-1])
w=wrongfor(TD)
a=req("REG-WITH-CODE DM verify","dm_verify",dv("+101700000003",w)); b=req("UNREG DM verify","dm_verify",dv("+101799999999",w)); res.append(sig(a)==sig(b)); print("   identical:",res[-1])
a=req("REG-WITH-CODE DM reset","dm_reset",dr("+101700000003",w,NEWD)); b=req("UNREG DM reset","dm_reset",dr("+101799999999",w,NEWD)); res.append(sig(a)==sig(b)); print("   identical:",res[-1])
print("ALL side-by-side identical:",all(res),res)
log("R1b all identical=%s %s"%(all(res),res))
print("password_resets rows still present (wrong codes keep row):"); print(sel("select email,phone,created_by,otp_hit_count from password_resets"))
section("R1c positive control: correct code verify=200 (counter released), then reset=200 + login with NEW pw, row cleared")
# customer email
l0=req("login michael OLD pw (control)","cust_login",clog("michael.brown@demo.com","email",OLD))
v=req("CORRECT verify cust email","cust_verify",cv("michael.brown@demo.com","email",TE))
r=req("CORRECT reset cust email","cust_reset",cr("michael.brown@demo.com","email",TE,NEWC))
print("row cleared (cust email):",repr(sel("select count(*) from password_resets where email='michael.brown@demo.com' and created_by='user'")))
l1=req("login michael OLD pw after reset","cust_login",clog("michael.brown@demo.com","email",OLD))
l2=req("login michael NEW pw","cust_login",clog("michael.brown@demo.com","email",NEWC))
# customer phone
v2=req("CORRECT verify cust phone","cust_verify",cv("+101600000003","phone",TP))
r2=req("CORRECT reset cust phone","cust_reset",cr("+101600000003","phone",TP,NEWC2))
print("row cleared (cust phone):",repr(sel("select count(*) from password_resets where phone='+101600000003' and created_by='user'")))
l3=req("login michael (phone) NEW2 pw","cust_login",clog("+101600000003","phone",NEWC2))
l3b=req("login michael NEW1 pw (now stale)","cust_login",clog("michael.brown@demo.com","email",NEWC))
# DM
d0=req("login DM carlos OLD pw (control)","dm_login",dlog("+101700000003",OLD))
dvv=req("CORRECT verify DM","dm_verify",dv("+101700000003",TD))
drr=req("CORRECT reset DM","dm_reset",dr("+101700000003",TD,NEWD))
print("row cleared (DM):",repr(sel("select count(*) from password_resets where email='carlos.rodriguez@demo.com' and created_by='dm_api'")))
d1=req("login DM OLD pw after reset","dm_login",dlog("+101700000003",OLD))
d2=req("login DM NEW pw","dm_login",dlog("+101700000003",NEWD))
print("SUMMARY statuses: verify email/phone/dm:",v["status"],v2["status"],dvv["status"]," reset:",r["status"],r2["status"],drr["status"])
print("logins old-before:",l0["status"],d0["status"]," old-after:",l1["status"],d1["status"]," new:",l2["status"],l3["status"],d2["status"])
print("counter rows after (released -> expect 0 values):"); print(sel("select right(`key`,12),value from cache where `key` like '%pwreset:attempts:%' and `key` not like '%:block'"))
