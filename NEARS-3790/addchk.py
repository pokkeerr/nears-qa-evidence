import re, glob, subprocess, os
S=os.path.dirname(__file__); worst=None; n=0
for nf in sorted(glob.glob(S+'/n_*.txt')):
    png = S+'/s_'+os.path.basename(nf)[2:-4]+'.png'
    if not os.path.exists(png): continue
    txt=open(nf).read()
    nodes=[(tuple(map(int,m.groups()[:4])),m.group(5)) for m in re.finditer(r'bounds=\[(\d+),(\d+)\]\[(\d+),(\d+)\] label="(.*?)"\n(?=class=|\Z)', txt, re.S)]
    cards=[b for b,l in nodes if ('AED' in l or 'د.إ' in l) and (b[3]-b[1])>450 and b[3]<2700]
    adds=[b for b,l in nodes if l in ('Add To Cart','أضف إلى السلة')]
    for c in cards:
        for a in adds:
            if a[0]>=c[0]-2 and a[2]<=c[2]+2 and a[1]>=c[1] and a[3]<=c[3]:
                out=subprocess.run(['python3',S+'/measure.py',png,*map(str,c)],capture_output=True,text=True).stdout.splitlines()
                runs=[l for l in out if l.startswith('INK')]
                img=max(runs,key=lambda l: float(re.search(r'h=\s*([\d.]+)',l).group(1)))
                img_end=float(re.search(r'\.\.\s*([\d.]+)dp',img).group(1))
                a_end=(a[3]-c[1])/3
                n+=1; margin=img_end-a_end
                if worst is None or margin<worst[0]: worst=(margin,os.path.basename(nf))
print(f"cards with add control checked: {n}; min (imageBottom - addBottom) = {worst[0]:.1f}dp at {worst[1]}")
