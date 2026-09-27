import json,re,sys
L=json.load(open(sys.argv[1]))['result']['data'].split('\n')
def hdr(i):
    while not re.search(r'Render\w+#',L[i]): i-=1
    return i
def ind(l): return len(l)-len(l.lstrip('│╎ ├└┬─ '))
def size_of(j):
    for x in L[j:j+30]:
        m=re.search(r'size: Size\(([\d.]+), ([\d.]+)\)',x)
        if m: return (float(m.group(1)),float(m.group(2)))
# section: RenderConstrainedBox 360x260 (rail SizedBox) -> report its parent Padding / Column
rail=[hdr(i) for i,l in enumerate(L) if 'size: Size(360.0, 260.0)' in l]
rail=sorted(set(rail))
print('rail boxes 360x260:',len(rail))
# walk up: nearest earlier headers with smaller indent
r=rail[0]; lvl=ind(L[r]); chain=[]
k=r
while k>0 and len(chain)<3:
    k-=1
    if re.search(r'Render\w+#',L[k]) and ind(L[k])<lvl:
        lvl=ind(L[k]); chain.append((re.search(r'Render\w+#\w+',L[k]).group(0),size_of(k)))
print('ancestors (padding, column, ...):',chain)
cells=sorted(set(hdr(i) for i,l in enumerate(L) if 'size: Size(160.0, 260.0)' in l and 'ConstrainedBox ← Container' in ''.join(L[hdr(i):i])))
print('cell Containers 160x260:',len(cells))
# inside first cell: collect vertical Flex children sizes (Expanded parts)
c=cells[0]; sib=[x for x in cells if x>c and ind(L[x])==ind(L[c])]; end=sib[0] if sib else c+4000
flex=[k for k in range(c,end) if 'RenderFlex#' in L[k] and any('direction: vertical' in x for x in L[k:k+12])]
if flex:
    f=flex[0]; fl=ind(L[f]); kids=[]
    for k in range(f+1,end):
        if re.search(r'Render\w+#',L[k]):
            if ind(L[k])<=fl: break
            kids.append((ind(L[k]),re.search(r'Render\w+#\w+',L[k]).group(0),size_of(k)))
    top=min(k[0] for k in kids); direct=[k for k in kids if k[0]==top]
    print('first vertical Flex', size_of(f),'direct children:',[(n,s) for _,n,s in direct])
