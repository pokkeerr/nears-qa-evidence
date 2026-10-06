#!/usr/bin/env python3
# hdr.py <var> <tag-substring>... : compact per-snapshot digest (header subtotals, row qty, minimum caption, summary Items Total / Discount / Total, Proceed present)
import os,re,sys
S=os.path.dirname(os.path.abspath(__file__))
P=re.compile(r'clickable=(\w+) bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label="(.*)"')
def labels(path):
    out=[]
    for l in open(path):
        m=P.search(l)
        if m and m.group(6): out.append(m.group(6))
    return out
def digest(path):
    L=labels(path); heads=[]; rows=[]; mins=[]; summ={}
    i=0
    while i<len(L):
        s=L[i]
        if re.match(r'^⁦[0-9.,]+ AED⁩$',s) and i>0 and not L[i-1].startswith('Delivery') and '\\n' not in L[i-1] and not re.match(r'^(Delivery Fee|Discount|ETA)',L[i-1]):
            heads.append((L[i-1][:28],s.strip('⁦⁩')))
        m=re.match(r'^(.*?)\\n.*\\n(\d+)$',s)
        if m and 'AED' in s: rows.append((m.group(1)[:20],m.group(2)))
        if s.startswith('Minimum order'): mins.append(re.sub('[⁦⁩]','',s))
        if s in('Items Total','Total') or s=='Discount':
            j=i+1; acc=''
            while j<len(L) and len(L[j])<=6 and not L[j].startswith('Total') and L[j] not in('Discount',): acc+=L[j]; j+=1
            if s=='Discount' and j-1>=i+1 and L[i+1].startswith('−'): acc=L[i+1]
            summ[s]=re.sub('[⁦⁩ ]|AED','',acc)
        i+=1
    return {'heads':heads,'rows':rows,'min':mins,'sum':summ,'proceed':'Proceed to Checkout' in L}
if __name__=='__main__':
    var=sys.argv[1]; subs=sys.argv[2:]
    d=f"{S}/evidence/walk-{var}"
    for f in sorted(os.listdir(d)):
        if f.endswith('.txt') and re.match(r'\d+-',f) and (not subs or any(x in f for x in subs)):
            r=digest(f"{d}/{f}")
            print(f[:-4][:46].ljust(46),'H',r['heads'][:3],'R',r['rows'][:6],'M',[m[:34] for m in r['min'][:2]],'S',r['sum'])
