import json,subprocess,re,os,csv,io,sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
CYR=re.compile(r'[А-Яа-яЁё]')
import pathlib as _pl, os as _os, tempfile as _tf
_HERE=_pl.Path(__file__).resolve().parent; _DATA=_HERE/'data'; _REPO=_HERE.parent
idx=json.load(open(_DATA/'imgindex.json'))

def iconlike(b):
    w,h=b[2]-b[0]+1,b[3]-b[1]+1
    return 9<=w<=17 and 9<=h<=20 and w<=1.35*h and h<=1.35*w

def detect(im,thr=26):
    a=np.array(im.convert('RGB')).astype(int); g=a.mean(2)
    bgm=ndi.median_filter(g,size=9)
    ink=np.abs(g-bgm)>thr
    m=ndi.binary_closing(ink,structure=np.ones((1,5)))
    m=ndi.binary_dilation(m,structure=np.ones((1,7)))
    lab,n=ndi.label(m)
    comps=[]
    for k,sl in enumerate(ndi.find_objects(lab),1):
        sub=(lab[sl]==k)&ink[sl]
        if sub.sum()<4: continue
        ys,xs=np.where(sub)
        b=[sl[1].start+xs.min(),sl[0].start+ys.min(),sl[1].start+xs.max(),sl[0].start+ys.max()]
        comps.append(b)
    # merge diacritics / same-line fragments
    changed=True
    while changed:
        changed=False
        for i in range(len(comps)):
            for j in range(i+1,len(comps)):
                p,q=comps[i],comps[j]
                if iconlike(p) or iconlike(q) or (p[3]-p[1]+1)>30 or (q[3]-q[1]+1)>30: continue
                hp,hq=p[3]-p[1]+1,q[3]-q[1]+1
                yo=min(p[3],q[3])-max(p[1],q[1])+1
                xo=min(p[2],q[2])-max(p[0],q[0])+1
                gapx=max(q[0]-p[2],p[0]-q[2])
                gapy=max(q[1]-p[3],p[1]-q[3])
                same_line = yo>=0.6*min(hp,hq) and gapx<=max(7,0.7*max(hp,hq))
                diacritic = xo>=0.4*min(p[2]-p[0]+1,q[2]-q[0]+1) and gapy<=2 and min(hp,hq)<=0.45*max(hp,hq)
                if same_line or diacritic:
                    comps[i]=[min(p[0],q[0]),min(p[1],q[1]),max(p[2],q[2]),max(p[3],q[3])]; comps.pop(j); changed=True; break
            if changed: break
    return [c for c in comps if 3<=c[3]-c[1]+1<=34 and c[2]-c[0]+1>=6]

def refine(im,box):
    a=np.array(im.convert('RGB')).astype(int); x0,y0,x1,y1=box
    reg=a[y0:y1+1,x0:x1+1]
    q=(reg//8).reshape(-1,3); key=q[:,0]*10000+q[:,1]*100+q[:,2]
    vals,cnt=np.unique(key,return_counts=True); k=vals[cnt.argmax()]
    mode=reg.reshape(-1,3)[key==k].mean(0)
    d=np.abs(reg-mode).sum(2)>60
    if d.shape[1]>20:
        d&=(d.mean(1)<0.85)[:,None]
    if d.shape[0]>12:
        d&=(d.mean(0)<0.85)[None,:]
    ys,xs=np.where(d)
    if len(ys)<4: return box
    return [x0+int(xs.min()),y0+int(ys.min()),x0+int(xs.max()),y0+int(ys.max())]

def split_multiline(im,b):
    """tall boxes (icon + one or more text rows): drop a leading squarish icon and cut the rest into rows."""
    a=np.array(im.convert('RGB')).astype(int); x0,y0,x1,y1=b
    reg=a[y0:y1+1,x0:x1+1]
    q=(reg//8).reshape(-1,3); key=q[:,0]*10000+q[:,1]*100+q[:,2]
    vals,cnt=np.unique(key,return_counts=True); mode=reg.reshape(-1,3)[key==vals[cnt.argmax()]].mean(0)
    ink=np.abs(reg-mode).sum(2)>60; cols=ink.any(0)
    cl=[];st=None;gap=0;last=0
    for c,f in enumerate(cols):
        if f:
            if st is None: st=c
            last=c; gap=0
        elif st is not None:
            gap+=1
            if gap>=4: cl.append((st,last)); st=None
    if st is not None: cl.append((st,last))
    start=0
    if len(cl)>=2:
        w=cl[0][1]-cl[0][0]+1; sub=ink[:,cl[0][0]:cl[0][1]+1]; rr=np.where(sub.any(1))[0]; hh=rr.max()-rr.min()+1
        if 9<=w<=17 and w<=1.5*hh: start=cl[1][0]
    sub=ink[:,start:]; rows=sub.any(1); bands=[];r0=None;gap=0
    for r,f in enumerate(list(rows)+[False,False]):
        if f:
            if r0 is None: r0=r
            last=r; gap=0
        elif r0 is not None:
            gap+=1
            if gap>=2: bands.append((r0,last)); r0=None
    out=[]
    for r0,r1 in bands:
        if r1-r0+1<4: continue
        c=np.where(sub[r0:r1+1].any(0))[0]
        out.append([int(x0+start+c.min()),int(y0+r0),int(x0+start+c.max()),int(y0+r1)])
    return out or [b]

def ocr(im,box):
    x0,y0,x1,y1=box; h=y1-y0+1
    pad=2; cx0=max(0,x0-pad); cy0=max(0,y0-pad)
    crop=im.crop((cx0,cy0,min(im.width,x1+pad+1),min(im.height,y1+pad+1))).convert('RGB')
    s=max(3,min(9,int(round(44/h))))
    big=crop.resize((crop.width*s,crop.height*s),Image.LANCZOS)
    big=Image.fromarray(np.pad(np.array(big),((20,20),(20,20),(0,0)),mode='edge'))
    _tmp=_os.path.join(_tf.gettempdir(),'robocam_ocr_c.png'); big.save(_tmp)
    r=subprocess.run(['tesseract',_tmp,'stdout','-l','rus+eng','--psm','7','tsv'],capture_output=True,text=True)
    words=[]
    for row in csv.DictReader(io.StringIO(r.stdout),delimiter='\t',quoting=csv.QUOTE_NONE):
        if row['level']=='5' and row['text'].strip():
            l=(int(row['left'])-20)/s+cx0; rr=(int(row['left'])+int(row['width'])-20)/s+cx0
            words.append(dict(t=row['text'],c=float(row['conf']),x0=round(l,1),x1=round(rr,1)))
    txt=' '.join(w['t'] for w in words); conf=round(sum(w['c'] for w in words)/len(words)) if words else 0
    return txt,conf,words

if __name__=='__main__':
    only=set(sys.argv[1:]); out={}
    if (_DATA/'ocr'/'segs.json').exists(): out=json.load(open(_DATA/'ocr'/'segs.json',encoding='utf-8'))
    for i,rel in idx.items():
        if only and i not in only: continue
        im=Image.open(_REPO/'img'/rel).convert('RGB')
        if im.width<60: continue
        segs=[]
        b1=[refine(im,b) for b in detect(im)]
        def ovl(a,b):
            w=min(a[2],b[2])-max(a[0],b[0]); h=min(a[3],b[3])-max(a[1],b[1]); return max(0,w)*max(0,h)
        b2=[refine(im,b) for b in detect(im,13)]
        b2=[b for b in b2 if not any(ovl(b,c)>0.3*max(1,(b[2]-b[0])*(b[3]-b[1])) for c in b1)]
        allb=[]
        for b in b1+b2:
            allb+= split_multiline(im,b) if (b[3]-b[1]+1)>=22 else [b]
        for b in sorted(allb,key=lambda b:(b[1]//6,b[0])):
            t,c,ws=ocr(im,b); segs.append(dict(box=[int(v) for v in b],text=t,conf=int(c),words=ws))
        out[i]=dict(file=rel,size=list(im.size),segs=segs)
        print(i,rel.split('/')[-1],len(segs),flush=True)
    json.dump(out,open(_DATA/'ocr'/'segs.json','w'),ensure_ascii=False)
