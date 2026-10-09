import sys; sys.path.insert(0,"/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad")
from q4108 import *
section("R0 delta re-QA: firebase_otp_verification flipped off via Admin panel; issue codes via app's forgot-password")
a=req("forgot REG cust email james","cust_forgot",{"verification_method":"email","email":"james.wilson@demo.com"})
b=req("forgot REG cust phone emily","cust_forgot",{"verification_method":"phone","phone":"+101600000002"})
c=req("forgot REG DM david","dm_forgot",{"phone":"+101700000002"})
d=req("forgot UNREG cust email","cust_forgot",{"verification_method":"email","email":"nobody.4108@demo.com"})
print("uniform:",sig(a)==sig(d))
print(sel("select id,email,phone,created_by,otp_hit_count,created_at, 'token=<read>' from password_resets"))
