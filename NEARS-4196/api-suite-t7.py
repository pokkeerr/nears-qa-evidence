from h import *
TK=open("tok.txt").read()
import subprocess,time
def sql(q): return subprocess.run(["mysql","-u","root","-N","multi_food_db_qa4196","-e",q],capture_output=True,text=True).stdout.strip()
R=[]
def chk(name, ok, detail=""):
    R.append((name,ok)); print(("PASS " if ok else "FAIL ")+name+(" :: "+str(detail) if detail else ""))
def n(): return int(sql("select count(*) from customer_search_logs"))
print(sql("show columns from customer_search_logs").replace("\n"," | ")[:300])
def delta(qs, **kw):
    a=n(); s,j,_=get(qs,auth=TK,**kw); time.sleep(0.3); return n()-a, s
T="name=zzqterm&limit=10&offset=1"
print("plain unflagged", delta(T))
print("plain flagged", delta(T+"&with_filters=1"))
print("flagged + products sel", delta(T+"&with_filters=1&products[min_rating]=4"))
print("flagged + stores sel", delta(T+"&with_filters=1&stores[open_now]=1"))
print("flagged + products sort", delta(T+"&with_filters=1&products[sort]=price_asc"))
print("flagged + stores sort", delta(T+"&with_filters=1&stores[sort]=rating"))
print("flagged + relevance sort explicit (default)", delta(T+"&with_filters=1&products[sort]=relevance"))
print("flagged + garbage sel", delta(T+"&with_filters=1&products[min_rating]=banana"))
print("flagged + unknown sort", delta(T+"&with_filters=1&products[sort]=banana"))
print("unflagged with selection params", delta(T+"&products[min_rating]=4"))
print("search rows:", sql("select * from customer_search_logs order by id desc limit 3"))
# cache table keys
print("cache keys with term:", sql("select count(*) from cache where `key` like '%zzqterm%' or `key` like '%milk%'"))
print("cache keys recent search:", sql("select `key` from cache where `key` like '%search%' limit 10"))
