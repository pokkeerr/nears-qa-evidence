import json, subprocess, urllib.request, os, sys
S=os.path.dirname(os.path.abspath(__file__))
DB='multi_food_db_qa_bug3925'
BASE='http://127.0.0.1:8130/api/v1'
TOKEN=open(S+'/token').read().strip()
def sql(q, rows=False):
    r=subprocess.run(['mysql','-u','root',DB,'-N','-B','-e',q],capture_output=True,text=True)
    if r.returncode: raise Exception(r.stderr)
    return [l.split('\t') for l in r.stdout.splitlines()] if rows else r.stdout
def setting(key,val):
    v='NULL' if val is None else "'%s'"%val
    n=sql("select count(*) from business_settings where `key`='%s'"%key,True)[0][0]
    if n=='0': sql("insert into business_settings(`key`,value) values('%s',%s)"%(key,v))
    else: sql("update business_settings set value=%s where `key`='%s'"%(v,key))
    sql("delete from cache")
def seed(lines, module):
    sql("delete from carts where user_id=6 and is_guest=0 and module_id=%d"%module)
    for item,qty in lines:
        sql("insert into carts(user_id,module_id,item_id,is_guest,add_on_ids,add_on_qtys,item_type,price,quantity,variation,created_at,updated_at) values(6,%d,%d,0,'[]','[]','App\\\\Models\\\\Item',10,%d,'[]',now(),now())"%(module,item,qty))
def clear():
    sql("delete from carts where user_id=6 and is_guest=0")
def call(method,path,body=None,module=1,token=True):
    h={'Content-Type':'application/json','Accept':'application/json','moduleId':str(module),'zoneId':'[2]'}
    if token: h['Authorization']='Bearer '+TOKEN
    data=json.dumps(body).encode() if body is not None else None
    req=urllib.request.Request(BASE+path,data=data,headers=h,method=method)
    try:
        with urllib.request.urlopen(req) as r: return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b'{}')
COMMON={'payment_method':'cash_on_delivery','order_type':'delivery','address':'Tower 1, Abu Dhabi','latitude':24.453884,'longitude':54.3773438}
def item(iid):
    r=sql("select i.price,i.discount,i.discount_type,i.store_id,fsi.discount,fs.admin_discount_percentage,fs.vendor_discount_percentage from items i left join flash_sale_items fsi on fsi.item_id=i.id left join flash_sales fs on fs.id=fsi.flash_sale_id where i.id=%d"%iid,True)[0]
    return dict(price=float(r[0]),idisc=float(r[1]),idt=r[2],store=int(r[3]),fpct=None if r[4]=='NULL' else float(r[4]),adm=None if r[5]=='NULL' else float(r[5]),ven=None if r[6]=='NULL' else float(r[6]))
def rd(x,p=2):
    # half-up on the decimal repr like PHP round()
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(x)).quantize(Decimal(1).scaleb(-p),rounding=ROUND_HALF_UP))
def client_flash_discount(lines):
    """independent arithmetic: toFixed(sum(raw unit discount x qty)) for FLASH lines of one store."""
    raw=0.0
    for iid,q in lines:
        it=item(iid)
        if it['fpct'] is not None: raw+= it['price']*it['fpct']/100*q
    return raw, rd(raw)
def order_row(oid):
    cols="id,order_group_id,store_id,order_amount,total_tax_amount,delivery_charge,coupon_discount_amount,store_discount_amount,flash_admin_discount_amount,flash_store_discount_amount,dm_tips,additional_charge,extra_packaging_amount,ref_bonus_amount"
    r=sql("select %s from orders where id=%s"%(cols,oid),True)[0]
    return dict(zip(cols.split(','),[float(x) if x!='NULL' else None for x in r]))
def details(oid):
    return sql("select item_id,quantity,price,discount_on_item,discount_type,tax_amount from order_details where order_id=%s"%oid,True)

from decimal import Decimal as Dm, ROUND_HALF_UP
def dq(x): return Dm(str(x))
def q2(d): return d.quantize(Dm('0.01'),rounding=ROUND_HALF_UP)
def model(P,rawD,D,dlv,vat='0.05'):
    """exact decimal arithmetic: (shown, base)"""
    P,rawD,D,dlv,vat=dq(P),dq(rawD),dq(D),dq(dlv),dq(vat)
    shown=q2(P-D+(P-D)*vat+dlv); base=q2(P-rawD+(P-rawD)*vat+dlv)
    return float(shown),float(base),(P-D+(P-D)*vat+dlv)
