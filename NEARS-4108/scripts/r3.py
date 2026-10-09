import sys,time,subprocess,datetime; sys.path.insert(0,"/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad")
from q4108 import *
issued=datetime.datetime.strptime(sel("select min(created_at) from password_resets where email='james.wilson@demo.com'"),"%Y-%m-%d %H:%M:%S")
target=issued+datetime.timedelta(minutes=16,seconds=30)
while datetime.datetime.now()<target: time.sleep(10)
def hk(scope,ident):
    out=subprocess.run(["php","artisan","tinker","--execute","echo hash_hmac('sha256', strtolower(rtrim('%s',' ')), config('app.key'));"%ident],cwd=ADMIN,capture_output=True,text=True).stdout.strip().splitlines()[-1]
    return "laravel_cachepwreset:attempts:%s:%s"%(scope,out)
def cnt(scope,ident):
    k=hk(scope,ident); return sel("select value from cache where `key`='%s'"%k) or "(key absent = 0 claims)"
CP="Passw0rd!x1"; DP="Zx9#qLm!Tr7vB2"
def cv(i,k,t): b={"verification_method":k,"reset_token":t}; b[k]=i; return b
def cr(i,k,t): b=cv(i,k,t); b.update(password=CP,confirm_password=CP); return b
section("R4 REAL expiry: codes issued %s, tested at %s (>15 min later); no created_at edits"%(issued,datetime.datetime.now()))
log(sel("select email,phone,created_by,created_at,timestampdiff(second,created_at,now()) from password_resets where created_by in ('user','dm_api') and (email in ('james.wilson@demo.com','david.miller@demo.com') or phone='+101600000002')"))
cases=[("cust-email james","customer_email","james.wilson@demo.com","email",sel("select token from password_resets where email='james.wilson@demo.com' and created_by='user'"),"email='james.wilson@demo.com' and created_by='user'"),
       ("cust-phone emily","customer_phone","+101600000002","phone",sel("select token from password_resets where phone='+101600000002' and created_by='user'"),"phone='+101600000002' and created_by='user'"),
       ("dm david","dm_phone","+101700000002",None,sel("select token from password_resets where email='david.miller@demo.com' and created_by='dm_api'"),"email='david.miller@demo.com' and created_by='dm_api'")]
for name,scope,ident,kind,t,where in cases:
    before=cnt(scope,ident); log("%s counter before: %s"%(name,before))
    if kind:
        a=req("%s CORRECT-but-EXPIRED verify"%name,"cust_verify",cv(ident,kind,t)); b=req("%s CORRECT-but-EXPIRED reset"%name,"cust_reset",cr(ident,kind,t))
    else:
        a=req("%s CORRECT-but-EXPIRED verify"%name,"dm_verify",{"phone":ident,"reset_token":t}); b=req("%s CORRECT-but-EXPIRED reset"%name,"dm_reset",{"phone":ident,"reset_token":t,"password":DP,"confirm_password":DP})
    after=cnt(scope,ident); row=sel("select count(*) from password_resets where "+where)
    msg="RESULT %s verify=%s/%s/%r reset=%s/%s/%r row_kept=%s counter before=%s after=%s"%(name,a["status"],a["code"],a["message"],b["status"],b["code"],b["message"],row,before,after)
    log(msg); print(msg)
l=[req("login james OLD pw (unchanged)","cust_login",{"login_type":"manual","email_or_phone":"james.wilson@demo.com","password":"123456789","field_type":"email"}),
   req("login emily OLD pw (unchanged)","cust_login",{"login_type":"manual","email_or_phone":"+101600000002","password":"123456789","field_type":"phone"}),
   req("login DM david OLD pw (unchanged)","dm_login",{"phone":"+101700000002","password":"123456789"})]
print("logins with old pw (password NOT changed by expired reset):",[x["status"] for x in l])
print("DONE")
