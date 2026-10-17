from h import *
import urllib.parse as up
R=[]
def chk(name, ok, detail=""):
    R.append((name,ok)); print(("PASS " if ok else "FAIL ")+name+(" :: "+str(detail) if detail else ""))
def allp(qs, ns="products", **kw):
    """fetch all pages limit=100, return (rows, totals list, first json)"""
    rows=[]; tots=[]; first=None; off=1
    while True:
        s,j,_=get(qs+f"&limit=100&offset={off}", **kw)
        assert s==200,(s,j)
        if first is None: first=j
        rows+=j[ns]; tots.append(j["total_items" if ns=="products" else "total_stores"])
        if len(j[ns])<100 or off>20: break
        off+=1
    return rows,tots,first
T="name=e%20a&with_filters=1"
base,tots,f0=allp(T)
print("base",len(base),tots, f0["total_items"])
chk("AC1 base total==rows", len(base)==f0["total_items"]==204)
def sel(q): return allp(T+"&"+q)
# min_rating
r,t,f=sel("products[min_rating]=4")
exp=[p for p in base if p["avg_rating"]>=4]
chk("AC1 products min_rating positive", {p["id"] for p in r}=={p["id"] for p in exp} and len(r)>0 and len(r)<len(base), (len(r),len(exp)))
chk("AC1 min_rating total==filtered, pages equal", set(t)=={len(r)} and f["total_items"]==len(r), t)
# discounted
r2,t2,f2=sel("products[discounted]=1")
exp2=[p for p in base if p["discount"]>0]
chk("AC1 discounted positive", {p["id"] for p in r2}=={p["id"] for p in exp2} and 0<len(r2)<len(base),(len(r2),len(exp2)))
# price
r3,t3,f3=sel("products[price_min]=5&products[price_max]=10")
exp3=[p for p in base if 5<=p["price"]<=10]
chk("AC1 price range positive", {p["id"] for p in r3}=={p["id"] for p in exp3} and 0<len(r3)<len(base),(len(r3),len(exp3)))
# category
cat=opts(f0,"products","category_ids"); print("cats",cat)
c=sorted(cat.items(), key=lambda kv: kv[1])[0][0] if cat else None
r4,t4_,f4=sel(f"products[category_ids]={c}")
chk("AC1 category positive count matches option count", len(r4)==cat[c],(c,len(r4),cat[c]))
# AND
r5,t5,f5=sel("products[min_rating]=4&products[discounted]=1&products[price_min]=1")
exp5={p["id"] for p in base if p["avg_rating"]>=4 and p["discount"]>0 and p["price"]>=1}
chk("AC1 AND of three", {p["id"] for p in r5}==exp5 and len(exp5)>0, (len(r5),len(exp5)))
r5b,_,_=sel("products[min_rating]=4&products[discounted]=1")
exp5b={p["id"] for p in base if p["avg_rating"]>=4 and p["discount"]>0}
chk("AC1 AND two", {p["id"] for p in r5b}==exp5b and len(exp5b)>0, len(exp5b))
# AC2 counts: whole matching set, not page 1
chk("AC2 counts above page size (positive control)", max(opts(f0,"products","category_ids").values())>10 or f0["filters"]["products"]["items"][1]["options"][0]["count"]>10, opts(f0,"products","min_rating"))
mr=opts(f0,"products","min_rating")["4"]; dc=opts(f0,"products","discounted")["1"]
chk("AC2 min_rating count == real set", mr==len([p for p in base if p["avg_rating"]>=4]), (mr))
chk("AC2 discounted count == real", dc==len(exp2),(dc))
# counts ignore own selection, reflect others
fm=opts(f,"products","min_rating")["4"]; 
chk("AC2 min_rating selected keeps own count (ignores own selection)", fm==mr,(fm,mr))
dcm=opts(f,"products","discounted")["1"]
chk("AC2 discounted count under rating selection == AND", dcm==len(exp5b),(dcm,len(exp5b)))
print("page1 limit10 counts same as limit100:", opts(get(T+"&limit=10&offset=1")[1],"products","min_rating"))
# totals identical across pages with selection limit=10
tt=[]; 
for off in (1,2,3,4):
    s,j,_=get(T+"&products[min_rating]=4&limit=10&offset=%d"%off); tt.append(j["total_items"]); 
chk("AC1 total_items identical across pages (limit10)", len(set(tt))==1 and tt[0]==len(r), tt)
# no dup/dropped paging
ids_pages=[]
for off in range(1,(len(r)//10)+2):
    s,j,_=get(T+"&products[min_rating]=4&limit=10&offset=%d"%off); ids_pages+=ids(j,"products")
chk("AC3 paging no dup/dropped", len(ids_pages)==len(set(ids_pages))==len(r) and set(ids_pages)=={p["id"] for p in r},(len(ids_pages),len(set(ids_pages)),len(r)))
# AC1 stores
sb,stt,fs0=allp(T,ns="stores")
print("stores base",len(sb),stt, keys(fs0,"stores"), {k:opts(fs0,"stores",k) for k in keys(fs0,"stores")})
chk("AC1 stores base total", len(sb)==fs0["total_stores"]==15)
r6,t6,f6=allp(T+"&stores[open_now]=1",ns="stores")
print("stores open_now",len(r6),t6,[ (s["id"],s["open"]) for s in r6]) 
chk("AC1 stores open_now positive", len(r6)==opts(fs0,"stores","open_now")["1"] and all(s["open"]==1 for s in r6) and len(r6)<len(sb),(len(r6),len(sb)))
chk("AC1 stores sel doesn't change products half", f6["total_items"]==204)
r7,t7,f7=allp(T+"&stores[min_rating]=4",ns="stores")
chk("AC1 stores min_rating", all(s["avg_rating"]>=4 for s in r7) and len(r7)==opts(fs0,"stores","min_rating")["4"],(len(r7)))
r8,t8,f8=allp(T+"&stores[delivery_type]=take_away",ns="stores")
chk("AC1 stores delivery_type", len(r8)==opts(fs0,"stores","delivery_type")["take_away"] and all(s["take_away"] for s in r8),(len(r8)))
r9,t9,f9=allp(T+"&stores[offers]=1&stores[open_now]=1",ns="stores")
print("stores AND", len(r9), opts(f9,"stores","offers"), opts(f9,"stores","open_now"))
r10,_,_=allp(T+"&stores[offers]=1",ns="stores")
exp={s["id"] for s in r10}&{s["id"] for s in r6}
chk("AC1 stores AND offers&open_now", {s["id"] for s in r9}==exp,(len(r9),len(exp)))
# store free_delivery zone1 m1
sbz1,_,fz1=allp("name=e%20a&with_filters=1&stores[free_delivery]=1",ns="stores",zone="[1]")
print("zone1 free_delivery stores", [(s["id"],s["free_delivery"]) for s in sbz1], opts(fz1,"stores","free_delivery"))
print(len(R), sum(1 for n,o in R if not o),"fails")
