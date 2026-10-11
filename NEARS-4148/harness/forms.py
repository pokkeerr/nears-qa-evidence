from html.parser import HTMLParser
class FormHarvest(HTMLParser):
    """collect (name,value) the way a browser would submit the form whose action contains `action_sub`"""
    def __init__(self, action_sub):
        super().__init__(); self.sub=action_sub; self.inform=False; self.fields=[]; self.sel=None; self.opts=[]; self.ta=None; self.tabuf=''
    def handle_starttag(self, tag, a):
        a=dict(a)
        if tag=='form': self.inform = self.sub in (a.get('action') or '')
        if not self.inform: return
        n=a.get('name')
        if tag=='input' and n:
            t=(a.get('type') or 'text').lower()
            if t in ('file','submit','button','image','reset'): return
            if t in ('checkbox','radio') and 'checked' not in a: return
            self.fields.append((n, a.get('value','on' if t=='checkbox' else '')))
        elif tag=='select' and n: self.sel=n; self.opts=[]
        elif tag=='option' and self.sel is not None: self.opts.append((a.get('value',''), 'selected' in a))
        elif tag=='textarea' and n: self.ta=n; self.tabuf=''
    def handle_data(self, d):
        if self.ta: self.tabuf+=d
    def handle_endtag(self, tag):
        if tag=='form': self.inform=False
        if tag=='select' and self.sel is not None:
            ch=[v for v,s in self.opts if s] or ([self.opts[0][0]] if self.opts else [])
            for v in ch: self.fields.append((self.sel, v))
            self.sel=None
        if tag=='textarea' and self.ta: self.fields.append((self.ta,self.tabuf)); self.ta=None
