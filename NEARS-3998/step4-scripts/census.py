import sys,re
sys.path.insert(0,'.')
from dartlex import *
def census(path):
    b=blank(open(path).read())   # comments+strings blanked
    calls=[m for m in re.finditer(r'(?<![\w.])update\s*\(',b)]
    bare=[];keyed=[]
    for m in calls:
        j=m.end()
        # find matching paren
        d=1;k=j
        while d>0:
            if b[k]=='(': d+=1
            elif b[k]==')': d-=1
            k+=1
        arg=b[j:k-1].strip()
        line=b.count('\n',0,m.start())+1
        (bare if arg=='' else keyed).append((line,arg))
    tearoffs=len(re.findall(r'(?<![\w.])update\s*(?=[,)\s]*[:,)]|\s*;)(?!\s*\()',b)) 
    return bare,keyed
if __name__=='__main__':
    for p in sys.argv[1:]:
        bare,keyed=census(p)
        print(p,'bare',len(bare),'keyed',len(keyed),[x[0] for x in bare])
