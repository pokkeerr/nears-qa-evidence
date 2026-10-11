import sys, json, os, subprocess, uuid, urllib.request, urllib.error
# usage: run_cases.py <label> <port> <worktree_admin> <offset> <cases.json> <out.jsonl>
label, port, admin, off, cases_f, out_f = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6]
DB="multi_food_db_qa4124"
TOK={"dm2":"<DM2_FAKE_CLONE_TOKEN>","dm1":"<DM1_FAKE_CLONE_TOKEN>","bad":"not-a-real-token","none":None}
def sql(q):
    return subprocess.check_output(["mysql","-u","root","-N","--batch",DB,"-e",q],text=True).strip()
def snap(oid):
    r=sql("select concat_ws('|',order_status,ifnull(payment_method,'<NULL>'),payment_status) from orders where id=%d"%oid)
    t=sql("select count(*) from order_transactions where order_id=%d"%oid)
    return {"row":r or "<absent>","tx_count":int(t)}
logs=[os.path.join(admin,"storage/logs/laravel.log"),os.path.join(admin,"storage/logs/laravel-structured.log")]
def sizes(): return [os.path.getsize(p) if os.path.exists(p) else 0 for p in logs]
def tail_since(offs, rid):
    res={}
    for p,o in zip(logs,offs):
        with open(p,"rb") as f:
            f.seek(o); data=f.read().decode("utf8","replace")
        res[os.path.basename(p)]=[l for l in data.splitlines() if "courier order refused" in l or rid in l]
    return res
cases=json.load(open(cases_f))
out=open(out_f,"w")
for c in cases:
    oid=c["id"]; real = oid+off if oid<90000000 else oid
    tok=TOK[c.get("tok","dm2")]
    rid=str(uuid.uuid4())
    before=snap(real); offs=sizes()
    h={"Content-Type":"application/json","Accept":"application/json","X-Request-Id":rid}
    if tok: h["Authorization"]="Bearer "+tok
    body=json.dumps({"order_id":real,"status":c.get("status","paid")}).encode()
    req=urllib.request.Request("http://127.0.0.1:%s/api/v1/delivery-man/update-payment-status"%port,data=body,headers=h,method="PUT")
    try:
        with urllib.request.urlopen(req,timeout=60) as r: code=r.status; txt=r.read().decode(); echo=r.headers.get("X-Request-Id")
    except urllib.error.HTTPError as e: code=e.code; txt=e.read().decode(); echo=e.headers.get("X-Request-Id")
    after=snap(real); lg=tail_since(offs,rid)
    rec={"case":c["name"],"label":label,"port":port,"order_id":real,"token":c.get("tok","dm2"),"request_id_sent":rid,"request_id_echoed":echo,"http":code,"body":txt[:300],"before":before,"after":after,"log_lines":lg}
    out.write(json.dumps(rec)+"\n"); out.flush()
    warn=[l for l in lg["laravel.log"] if "courier order refused" in l]
    print("%-34s id=%-9d tok=%-4s HTTP %s | %s tx=%d -> %s tx=%d | WARN(own rid)=%d"%(c["name"],real,c.get("tok","dm2"),code,before["row"],before["tx_count"],after["row"],after["tx_count"],len([l for l in warn if rid in l])))
