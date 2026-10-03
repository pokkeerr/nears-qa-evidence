import math,sys
def hav(a,b,c,d,R=6371008.8):
    p1,p2=math.radians(a),math.radians(c); dp=p2-p1; dl=math.radians(d-b)
    h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))
def vinc(lat1,lon1,lat2,lon2):
    a=6378137.0; f=1/298.257223563; b=(1-f)*a
    L=math.radians(lon2-lon1)
    U1=math.atan((1-f)*math.tan(math.radians(lat1))); U2=math.atan((1-f)*math.tan(math.radians(lat2)))
    sU1,cU1,sU2,cU2=math.sin(U1),math.cos(U1),math.sin(U2),math.cos(U2)
    lam=L
    for _ in range(200):
        sl,cl=math.sin(lam),math.cos(lam)
        ss=math.sqrt((cU2*sl)**2+(cU1*sU2-sU1*cU2*cl)**2)
        if ss==0: return 0.0
        cs=sU1*sU2+cU1*cU2*cl; sig=math.atan2(ss,cs)
        sa=cU1*cU2*sl/ss; c2a=1-sa**2
        c2sm=cs-2*sU1*sU2/c2a if c2a!=0 else 0
        C=f/16*c2a*(4+f*(4-3*c2a))
        lp=lam
        lam=L+(1-C)*f*sa*(sig_c:=0) if False else L+(1-C)*f*sa*(sig+C*ss*(c2sm+C*cs*(-1+2*c2sm**2)))
        if abs(lam-lp)<1e-12: break
    u2=c2a*(a*a-b*b)/(b*b)
    A=1+u2/16384*(4096+u2*(-768+u2*(320-175*u2)))
    B=u2/1024*(256+u2*(-128+u2*(74-47*u2)))
    ds=B*ss*(c2sm+B/4*(cs*(-1+2*c2sm**2)-B/6*c2sm*(-3+4*ss**2)*(-3+4*c2sm**2)))
    return b*A*(sig-ds)
if __name__=="__main__":
    ulat,ulng=float(sys.argv[1]),float(sys.argv[2])
    for line in sys.stdin:
        sid,name,la,lo=line.rstrip('\n').split('\t')
        la,lo=float(la),float(lo)
        v=vinc(ulat,ulng,la,lo)/1000; h=hav(ulat,ulng,la,lo)/1000
        print(f"{sid}\t{name[:48]:48}\tvincenty={v:.4f}->{v:.1f}\thaversine={h:.4f}->{h:.1f}")
