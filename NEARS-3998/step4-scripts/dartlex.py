import re,sys
def blank(src, keep_strings=False):
    """Blank comments (and string contents unless keep_strings) preserving length/newlines."""
    out=[];i=0;n=len(src)
    while i<n:
        c=src[i]
        if src.startswith('//',i):
            j=src.find('\n',i); j=n if j<0 else j
            out.append(' '*(j-i)); i=j
        elif src.startswith('/*',i):
            j=src.find('*/',i+2); j=n if j<0 else j+2
            seg=src[i:j]; out.append(re.sub(r'[^\n]',' ',seg)); i=j
        elif c in '\'"':
            # raw?
            raw = i>0 and src[i-1]=='r'
            q=src[i:i+3] if src[i:i+3] in ("'''",'"""') else c
            j=i+len(q)
            while j<n:
                if not raw and src[j]=='\\': j+=2; continue
                if src.startswith(q,j): break
                j+=1
            j=min(n,j+len(q))
            seg=src[i:j]
            if keep_strings: out.append(seg)
            else:
                out.append(q+re.sub(r'[^\n]',' ',seg[len(q):-len(q)])+q if len(seg)>=2*len(q) else seg)
            i=j
        else:
            out.append(c); i+=1
    return ''.join(out)

def class_body(src, name):
    b=blank(src)
    m=re.search(r'\bclass\s+'+name+r'\b[^{]*\{', b)
    s=m.end(); d=1;i=s
    while d>0:
        ch=b[i]
        if ch=='{': d+=1
        elif ch=='}': d-=1
        i+=1
    return b[s:i-1]

def heads(body):
    """depth-1 member heads of a class body (comments/strings already blanked)."""
    res=[];i=0;n=len(body);buf=[];par=0
    def skip_to(i,openc,closec):
        d=0
        while i<n:
            if body[i]==openc: d+=1
            elif body[i]==closec:
                d-=1
                if d==0: return i+1
            i+=1
        return i
    def skip_stmt(i):
        d=0
        while i<n:
            ch=body[i]
            if ch in '({[': d+=1
            elif ch in ')}]': d-=1
            elif ch==';' and d==0: return i+1
            i+=1
        return i
    while i<n:
        ch=body[i]
        if ch in '([': par+=1; buf.append(ch); i+=1; continue
        if ch in ')]': par-=1; buf.append(ch); i+=1; continue
        if par==0 and ch==';':
            res.append(''.join(buf)); buf=[]; i+=1; continue
        if par==0 and ch=='{':
            res.append(''.join(buf)); buf=[]; i=skip_to(i,'{','}'); continue
        if par==0 and body.startswith('=>',i):
            res.append(''.join(buf)); buf=[]; i=skip_stmt(i+2); continue
        if par==0 and ch=='=' and body[i+1:i+2] not in ('=','>') and body[i-1:i] not in ('=','!','<','>'):
            res.append(''.join(buf)); buf=[]; i=skip_stmt(i+1); continue
        buf.append(ch); i+=1
    out=[]
    for h in res:
        h=re.sub(r'\basync\*?\b','',h)
        h=re.sub(r'\s+',' ',h).strip()
        if h: out.append(h)
    return out

def name_of(h):
    h2=re.sub(r'@\w+(\([^)]*\))?\s*','',h)
    m=re.search(r'\bget\s+(\w+)',h2)
    if m: return m.group(1)
    m=re.search(r'\bset\s+(\w+)\s*\(',h2)
    if m: return m.group(1)
    m=re.match(r'^([\w.<>?,\s]*?)\boperator\b',h2)
    m=re.search(r'(\w+)\s*(<[^>]*>)?\s*\(',h2)
    if m: return m.group(1)
    m=re.findall(r'\w+',h2)
    return m[-1] if m else h2

def public(hs):
    r=[]
    for h in hs:
        nm=name_of(h)
        if nm.startswith('_') : 
            continue
        r.append(h)
    return r
