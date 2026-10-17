from h import *
R=[]
def chk(name, ok, detail=""):
    R.append((name,ok)); print(("PASS " if ok else "FAIL ")+name+(" :: "+str(detail) if detail else ""))
# AC3 pruning: zone 417 all unrated -> min_rating absent (products + stores); free_delivery absent
s,j,_=get("name=e%20a&with_filters=1&limit=10&offset=1",zone="[417]")
chk("AC3 417 unrated: products min_rating absent", "min_rating" not in keys(j,"products"), keys(j,"products"))
chk("AC3 417 unrated: stores min_rating absent", "min_rating" not in keys(j,"stores"), keys(j,"stores"))
chk("AC3 417 no free_delivery option (stores+products)", "free_delivery" not in keys(j,"stores") and "free_delivery" not in keys(j,"products"))
# zone 2 positive control
s,j2,_=get("name=e%20a&with_filters=1&limit=10&offset=1",zone="[2]")
chk("AC3 zone2 positive control min_rating present", "min_rating" in keys(j2,"products") and "min_rating" in keys(j2,"stores"))
# zone1 positive control free delivery
s,j1,_=get("name=e%20a&with_filters=1&limit=10&offset=1",zone="[1]")
chk("AC3 zone1 free_delivery present", "free_delivery" in keys(j1,"stores") and "free_delivery" in keys(j1,"products"), opts(j1,"stores","free_delivery"))
# pruning under narrowing: select category with no discounted -> discounted absent?
s,jb,_=get("name=e%20a&with_filters=1&limit=10&offset=1")
cat=opts(jb,"products","category_ids")
# find category where discount count 0
found=None
for c in cat:
    s,jc,_=get(f"name=e%20a&with_filters=1&limit=10&offset=1&products[category_ids]={c}")
    if "discounted" not in keys(jc,"products") or "min_rating" not in keys(jc,"products"):
        found=(c,keys(jc,"products"),cat[c]); break
print("pruned-on-narrow example:",found)
chk("AC3 option pruned when zero under narrowing (min_rating/discounted)", found is not None)
# term with only non-veg: veg not a registry filter
chk("AC3 veg not a registry filter", all(k!="veg" and k!="type" for k in keys(jb,"products")))
# garbage 200
G=["stores=abc","stores[open_now][]=1","products[category_ids]=[1,%22x%22]","products[sort][]=x","products[min_rating]=banana","products[price_min]=abc&products[price_max]=-5","products=1","products[open_now]=true","stores[bogus]=1","products[bogus][a]=1","products[sort]=%00","products[category_ids][]=1&products[category_ids][]=zz","products[category_ids]=99999999","products[price_min]=1e999","products[price_min]=5&products[price_max]=1"]
G.append("products[open_now]="+"A"*10000); G.append("products[category_ids]="+",".join(str(i) for i in range(500)))
for g in G:
    s,j,_=get("name=e%20a&with_filters=1&limit=10&offset=1&"+g)
    chk("AC3 garbage 200: "+g[:50], s==200 and "total_items" in j, (s, j.get("total_items") if isinstance(j,dict) else j))
for lon,lat in [("1e999","24.4"),("54.3","124.45"),("abc","abc"),("0","0"),("54.3526","91")]:
    s,j,_=get("name=e%20a&with_filters=1&limit=10&offset=1&products[sort]=distance",lon=lon,lat=lat)
    chk(f"AC3/4 bad origin lon={lon} lat={lat} 200", s==200, (s, j["filters"]["products"]["sort"]["selected"] if s==200 and "filters" in j else None))
# unknown sort -> relevance
s,ju,_=get("name=e%20a&with_filters=1&limit=10&offset=1&products[sort]=banana")
s,jr,_=get("name=e%20a&with_filters=1&limit=10&offset=1")
chk("AC4 unknown products sort -> relevance order+selected", ids(ju,"products")==ids(jr,"products") and ju["filters"]["products"]["sort"]["selected"]=="relevance")
s,ju,_=get("name=e%20a&with_filters=1&limit=10&offset=1&stores[sort]=banana")
chk("AC4 unknown stores sort -> relevance", ids(ju,"stores")==ids(jr,"stores") and ju["filters"]["stores"]["sort"]["selected"]=="relevance")
# top-level sort ignored (must be in namespace)
s,jt,_=get("name=e%20a&with_filters=1&limit=10&offset=1&sort=price_asc")
chk("AC4 top-level sort ignored", ids(jt,"products")==ids(jr,"products"))
# sort continuity
def allids(qs, ns="products", **kw):
    rows=[]; off=1
    while True:
        s,j,_=get(qs+f"&limit=10&offset={off}", **kw)
        assert s==200
        rows+=j[ns]
        if len(j[ns])<10 or off>25: break
        off+=1
    return rows
base=allids("name=e%20a&with_filters=1")
for tok in ["relevance","price_asc","price_desc","rating","distance"]:
    rows=allids("name=e%20a&with_filters=1&products[sort]="+tok)
    idl=[r["id"] for r in rows]
    okset=set(idl)=={r["id"] for r in base} and len(idl)==len(set(idl))==len(base)
    if tok=="price_asc": ok_ord=[r["price"] for r in rows]==sorted(r["price"] for r in rows)
    elif tok=="price_desc": ok_ord=[r["price"] for r in rows]==sorted((r["price"] for r in rows),reverse=True)
    elif tok=="rating": ok_ord=[r["avg_rating"] for r in rows]==sorted((r["avg_rating"] for r in rows),reverse=True)
    else: ok_ord=True
    chk(f"AC4 products sort {tok} continuity+order across 21 pages", okset and ok_ord, (len(idl)))
srt=allids("name=e%20a&with_filters=1&stores[sort]=rating",ns="stores")
chk("AC4 stores rating sort desc", [s["avg_rating"] for s in srt]==sorted((s["avg_rating"] for s in srt),reverse=True), [s["avg_rating"] for s in srt])
srt=allids("name=e%20a&with_filters=1&stores[sort]=distance",ns="stores")
chk("AC4 stores distance asc", [s["distance"] for s in srt]==sorted(s["distance"] for s in srt), [round(s["distance"]) for s in srt])
rows=allids("name=e%20a&with_filters=1&products[sort]=distance")
print("distance products first", [(r["id"],r.get("distance")) for r in rows[:5]])
# distance withheld without origin
s,jn,_=get("name=e%20a&with_filters=1&limit=10&offset=1&products[sort]=distance&stores[sort]=distance",lon="0",lat="0")
print("no-origin sort opts", [o["value"] for o in jn["filters"]["products"]["sort"]["options"]], jn["filters"]["products"]["sort"]["selected"], [o["value"] for o in jn["filters"]["stores"]["sort"]["options"]], jn["filters"]["stores"]["sort"]["selected"])
chk("AC4 distance withheld without origin", "distance" not in [o["value"] for o in jn["filters"]["products"]["sort"]["options"]] and jn["filters"]["products"]["sort"]["selected"]=="relevance")
s,jn2,_=get("name=e%20a&with_filters=1&limit=10&offset=1",lon=None,lat=None)
chk("AC4 distance withheld with headers absent", "distance" not in [o["value"] for o in jn2["filters"]["products"]["sort"]["options"]])
print(len(R), "fails:", [n for n,o in R if not o])
