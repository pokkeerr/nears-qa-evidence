import json,urllib.request,urllib.error,uuid,subprocess,os
DB="multi_food_db_qa4124"; admin="/Users/Apple/Projects/nears-NEARS-4124-courier-paid-flag-cod-only/Admin"
def sql(q): return subprocess.check_output(["mysql","-u","root","-N","--batch",DB,"-e",q],text=True).strip()
log=admin+"/storage/logs/laravel.log"; slog=admin+"/storage/logs/laravel-structured.log"
def call(step,body):
    rid=str(uuid.uuid4()); off=os.path.getsize(log); soff=os.path.getsize(slog)
    h={"Content-Type":"application/json","Accept":"application/json","X-Request-Id":rid,"Authorization":"Bearer <DM2_FAKE_CLONE_TOKEN>"}
    method,path,payload=step
    req=urllib.request.Request("http://127.0.0.1:8474/api/v1/delivery-man/"+path,data=json.dumps(payload).encode(),headers=h,method=method)
    try:
        with urllib.request.urlopen(req,timeout=60) as r: code=r.status; txt=r.read().decode()
    except urllib.error.HTTPError as e: code=e.code; txt=e.read().decode()
    new=open(log,"rb").read()[off:].decode("utf8","replace").splitlines()
    refused=[l for l in new if "courier order refused" in l]
    errs=[l for l in new if "production.ERROR" in l or "[FAIL]" in l or "[ERR]" in l]
    row=sql("select concat_ws('|',order_status,payment_method,payment_status,ifnull(delivery_man_id,'NULL')) from orders where id=96001")
    tx=sql("select count(*) from order_transactions where order_id=96001")
    print("%-28s HTTP %s %s | row=%s tx=%s | courier-refused-WARN=%d FAIL/ERR lines=%d"%(path+" "+str(payload.get('status','')),code,txt[:110],row,tx,len(refused),len(errs)))
    for l in errs: print("   ERRLINE",l[:240])
for s in [("PUT","accept-order",{"order_id":96001}),("PUT","update-order-status",{"order_id":96001,"status":"picked_up"}),("PUT","update-order-status",{"order_id":96001,"status":"delivered"}),("PUT","update-payment-status",{"order_id":96001,"status":"paid"})]:
    call(s,s[2])
