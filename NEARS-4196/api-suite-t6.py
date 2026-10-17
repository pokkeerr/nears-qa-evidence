from h import *
import subprocess
R=[]
def chk(name, ok, detail=""):
    R.append((name,ok)); print(("PASS " if ok else "FAIL ")+name+(" :: "+str(detail) if detail else ""))
def sql(q): return subprocess.run(["mysql","-u","root","-N","multi_food_db_qa4196","-e",q],capture_output=True,text=True).stdout.strip()
# category forms
base=lambda extra,**kw: get("name=e%20a&with_filters=1&limit=100&offset=1"+extra,**kw)
c1=ids(base("&products[category_ids]=6,7")[1],"products")
c2=ids(base("&products[category_ids]=[6,7]")[1],"products")
c3=ids(base("&products[category_ids][]=6&products[category_ids][]=7")[1],"products")
c4=ids(base("&products[category_ids]=%5B6%2C7%5D")[1],"products")
chk("AC1 category_ids CSV == JSON == array", set(c1)==set(c2)==set(c3)==set(c4) and len(c1)>0,(len(c1),len(c2),len(c3),len(c4)))
# parent roll-up zone 2: parents 3 and 6 on 'milk'? use ground truth via data-checker numbers with broad term? use SQL
print("categories 3/6 parent", sql("select id,parent_id,name from categories where id in (3,6,7) or parent_id in (3,6) limit 20"))
for term in ["milk"]:
    s,j,_=get(f"name={term}&with_filters=1&limit=50&offset=1&products[category_ids]=6")
    print(term,"cat6 total", j["total_items"], opts(j,"products","category_ids"))
# parent roll-up via 'e a' zone 2: category counts for parent vs child
s,jb,_=get("name=e%20a&with_filters=1&limit=10&offset=1")
cats=opts(jb,"products","category_ids")
par=sql("select id,parent_id from categories where id in (%s)"%",".join(cats.keys()))
print("cat parent map:", par.replace("\n","; "))
# find parent with children in options
rows=[l.split("\t") for l in par.split("\n")]
ch={}
for i,p in rows:
    if p not in ("0","NULL"): ch.setdefault(p,[]).append(i)
print("parents with child options:", ch)
for p,kids in ch.items():
    if p in cats:
        sp,jp,_=get(f"name=e%20a&with_filters=1&limit=100&offset=1&products[category_ids]={p}")
        sk,jk,_=get(f"name=e%20a&with_filters=1&limit=100&offset=1&products[category_ids]={','.join(kids)}")
        chk(f"AC3 parent {p} selects children (parent set ⊇ children set)", set(ids(jk,'products'))<=set(ids(jp,'products')) and cats[p]==jp['total_items'], (cats[p],jp['total_items'],jk['total_items']))
# zone-2 milk
s,j,_=get("name=milk&with_filters=1&limit=50&offset=1")
chk("fixture milk total 15", j["total_items"]==15)
s,jo,_=get("name=milk&with_filters=1&limit=50&offset=1&products[open_now]=1")
chk("AC1 milk open_now 11, option 11", jo["total_items"]==11 and opts(jo,"products","open_now")=={"1":11}, jo["total_items"])
chk("AC1 milk closed fixture ids dropped", not (set(ids(jo,"products"))&{91152,91153,91154,91155}))
# kill switch
print("filters.enabled config:", sql("select key_name,value from business_settings where key_name like 'filters%'"))
# above-N 50-zone
zones=sql("select id from zones where status=1 order by id limit 50").split("\n")
zh="["+",".join(zones)+"]"
print("zones",len(zones))
s,jn,_=get("name=e%20a&with_filters=1&limit=10&offset=1",zone=zh)
print(s, jn["total_items"], jn["total_stores"], jn["filters"]["products"]["counts_omitted"], jn["filters"]["stores"]["counts_omitted"])
pr=jn["filters"]["products"]
print([ (i["key"], [o["count"] for o in i["options"]][:3], i.get("bounds")) for i in pr["items"]])
chk("AC2/8 above-N counts_omitted true, counts null, list complete", pr["counts_omitted"] is True and all(o["count"] is None for i in pr["items"] for o in i["options"]) and len(jn["products"])==10 and jn["total_items"]>5000, jn["total_items"])
s,jn2,_=get("name=e%20a&with_filters=1&limit=10&offset=1&products[min_rating]=4",zone=zh)
print("above-N selection total", jn2["total_items"], len(jn2["products"]))
print(len(R),"fails",[n for n,o in R if not o])
