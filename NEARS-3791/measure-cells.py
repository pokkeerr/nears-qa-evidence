import json,re,sys
lines=json.load(open(sys.argv[1]))['result']['data'].split('\n')
cells=[i for i,l in enumerate(lines) if 'size: Size(160.0, 260.0)' in l]
# cell containers are the ConstrainedBox<-Container ones
starts=[]
for i in cells:
    j=i
    while not re.search(r'Render\w+#',lines[j]): j-=1
    if any('creator: ConstrainedBox ← Container' in x for x in lines[j:i]): starts.append(j)
print('cells(160x260 Container):',len(starts))
for n,s in enumerate(starts[:2]):
    e=starts[n+1] if n+1<len(starts) else s+3000
    print('== cell',n)
    for k in range(s,e):
        if 'RenderParagraph#' in lines[k]:
            blk=lines[k:k+40]
            sz=next((x.strip().split('size: ')[1] for x in blk if 'size: Size' in x),'?')
            ml=next((x.strip().split('maxLines: ')[1] for x in blk if 'maxLines:' in x),'-')
            cw=next((m.group(1) for x in blk if 'constraints:' in x for m in [re.search(r'w(?:<=|=)([\d.]+)',x)] if m),'?')
            txt=[]
            for x in blk:
                m=re.search(r'"(.*)"',x)
                if m: txt.append(m.group(1))
            print(f'  {sz} maxw={cw} maxLines={ml} text={txt[:3]}')
    print('overflow in cell:', any('OVERFLOWING' in x for x in lines[s:e]))
