import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pathlib as _pl
_F=_pl.Path(__file__).resolve().parent/'data'/'fonts'
FONT=str(_F/'Roboto-Regular.ttf'); FONTM=str(_F/'Roboto-Medium.ttf')
SS=6
def _font(path,size): return ImageFont.truetype(path,max(1,int(round(size*SS))))
def text_w(t,size,path=FONT): return _font(path,size).getlength(t)/SS

def ring_mode(a,box,r=2):
    """dominant colour of the strips just left/right of the box (falls back to all sides)."""
    H,W=a.shape[:2]; x0,y0,x1,y1=box
    ys=slice(max(0,y0),min(H,y1+1)); parts=[]
    if x0-1>=0: parts.append(a[ys,max(0,x0-r):x0].reshape(-1,3))
    if x1+1<W: parts.append(a[ys,x1+1:min(W,x1+1+r)].reshape(-1,3))
    px=np.concatenate(parts) if parts else np.zeros((0,3),np.uint8)
    if len(px)==0:
        parts=[a[max(0,y0-r):y0,x0:x1+1].reshape(-1,3),a[y1+1:y1+1+r,x0:x1+1].reshape(-1,3)]
        px=np.concatenate([p for p in parts if len(p)]) if any(len(p) for p in parts) else np.array([[255,255,255]])
    q=(px//8).astype(int); key=q[:,0]*10000+q[:,1]*100+q[:,2]
    v,c=np.unique(key,return_counts=True); return px[key==v[c.argmax()]].mean(0)

def erase(a,box,pad,mode):
    """fill box with per-row interpolation between the pixels just left/right of it (handles gradients)."""
    H,W=a.shape[:2]; x0,y0,x1,y1=box
    X0,X1=max(0,x0-pad-1),min(W-1,x1+pad+1); Y0,Y1=max(0,y0-pad),min(H-1,y1+pad)
    for y in range(Y0,Y1+1):
        L=a[y,max(0,X0-2):X0].astype(float) if X0>0 else None
        R=a[y,X1+1:min(W,X1+3)].astype(float) if X1<W-1 else None
        lc=np.median(L,axis=0) if L is not None and len(L) else None
        rc=np.median(R,axis=0) if R is not None and len(R) else None
        def ok(c): return c is not None and np.abs(c-mode).sum()<120
        if ok(lc) and ok(rc) and np.abs(lc-rc).sum()<110:
            t=np.linspace(0,1,X1-X0+1)[:,None]; a[y,X0:X1+1]=(lc*(1-t)+rc*t)
        elif ok(lc): a[y,X0:X1+1]=lc
        elif ok(rc): a[y,X0:X1+1]=rc
        else: a[y,X0:X1+1]=mode

def ink_color(a,box,bg):
    x0,y0,x1,y1=box; reg=a[max(0,y0):y1+1,max(0,x0):x1+1].reshape(-1,3).astype(float)
    d=np.abs(reg-bg).sum(1)
    if len(d)==0: return np.array([0.,0.,0.])
    thr=np.percentile(d,88) if len(d)>20 else d.max()
    sel=reg[d>=max(thr,1)]
    return sel.mean(0) if len(sel) else np.array([0.,0.,0.])

def baseline_and_top(a,box,bg):
    x0,y0,x1,y1=box; reg=a[y0:y1+1,x0:x1+1].astype(float)
    d=np.abs(reg-bg).sum(2); ink=(d>60).sum(1)
    if ink.max()==0: return y1,y0
    strong=np.where(ink>=0.35*ink.max())[0]
    return y0+int(strong.max()),y0+int(strong.min())

def extend_box(a,box,mode,maxext=8):
    """grow the box over adjacent narrow glyphs (e.g. a trailing colon the OCR box missed)."""
    x0,y0,x1,y1=box; H,W=a.shape[:2]
    def ink(x): return 0<=x<W and (np.abs(a[y0:y1+1,x].astype(int)-mode).sum(1)>80).any()
    ox1=x1; x=x1+1
    while x1-ox1<maxext:
        f=None
        for dx in range(3):
            if ink(x+dx): f=x+dx; break
        if f is None: break
        w=0; xx=f
        while ink(xx) and w<12: w+=1; xx+=1
        if w>5: break
        x1=xx-1; x=x1+1
    ox0=x0; x=x0-1
    while ox0-x0<maxext:
        f=None
        for dx in range(3):
            if ink(x-dx): f=x-dx; break
        if f is None: break
        w=0; xx=f
        while ink(xx) and w<12: w+=1; xx-=1
        if w>5: break
        x0=xx+1; x=x0-1
    return (x0,y0,x1,y1)

def trim_icons(a,box,mode):
    """drop a leading/trailing checkbox- or arrow-like blob separated from the text by a clear gap."""
    x0,y0,x1,y1=box; reg=a[y0:y1+1,x0:x1+1].astype(int)
    ink=np.abs(reg-mode).sum(2)>80; cols=ink.any(0); G=4
    cl=[];s=None;gap=0;last=0
    for c,f in enumerate(cols):
        if f:
            if s is None: s=c
            last=c; gap=0
        elif s is not None:
            gap+=1
            if gap>=G: cl.append((s,last)); s=None
    if s is not None: cl.append((s,last))
    if len(cl)<2: return box
    def dims(c):
        sub=ink[:,c[0]:c[1]+1]; rows=np.where(sub.any(1))[0]; return c[1]-c[0]+1,rows.max()-rows.min()+1
    nx0,nx1=x0,x1
    w,hh=dims(cl[0])
    if 9<=w<=17 and w<=1.5*hh and cl[1][0]-cl[0][1]>=G: nx0=x0+cl[1][0]
    if len(cl)>=3:
        w,hh=dims(cl[-1])
        if 9<=w<=17 and w<=1.5*hh and cl[-1][0]-cl[-2][1]>=G: nx1=x0+cl[-2][1]
    return (nx0,y0,nx1,y1)

def retouch(img,items):
    """item: box,src,text,center,clip,maxw,bold,size,fg"""
    a=np.array(img.convert('RGB')).astype(np.uint8).copy(); H,W=a.shape[:2]
    plans=[]
    for it in items:
        x0,y0,x1,y1=[int(v) for v in it['box']]
        x0,y0=max(0,x0),max(0,y0); x1,y1=min(W-1,x1),min(H-1,y1)
        mode=ring_mode(a,(x0,y0,x1,y1),3)
        if not it.get('keep_box'):
            x0,y0,x1,y1=extend_box(a,(x0,y0,x1,y1),mode)
            x0,y0,x1,y1=trim_icons(a,(x0,y0,x1,y1),mode)
        fg=np.array(it['fg']) if it.get('fg') else ink_color(a,(x0,y0,x1,y1),mode)
        base,top=baseline_and_top(a,(x0,y0,x1,y1),mode)
        path=FONTM if it.get('bold') else FONT
        if it.get('size'): size=it['size']
        elif it.get('src'): size=(x1-x0+1)/max(0.1,text_w(it['src'],1,path))
        else: size=(base-top+1)/0.72
        # sanity: keep size consistent with measured cap/x height (avoid absurd width-fit results)
        hsize=(base-top+1)/0.72
        if it.get('src') and not it.get('size'): size=min(size,hsize*1.25); size=max(size,hsize*0.6)
        plans.append((it,mode,fg,base,size,path,(x0,y0,x1,y1)))
    for it,mode,fg,base,size,path,(x0,y0,x1,y1) in plans: erase(a,(x0,y0,x1,y1),it.get('pad',2),mode)
    out=Image.fromarray(a).convert('RGBA')
    layer=Image.new('RGBA',(W*SS,H*SS),(0,0,0,0)); dl=ImageDraw.Draw(layer)
    for it,mode,fg,base,size,path,(x0,y0,x1,y1) in plans:
        t=it.get('text','')
        if not t: continue
        clip=it.get('clip'); center=it.get('center')
        maxw=it.get('maxw') or ((x1-x0+1)*1.35 if center else min(W-3-x0,(x1-x0+1)*1.5))
        w=text_w(t,size,path)
        if not clip and w>maxw: size*=maxw/w; w=text_w(t,size,path)
        x=((x0+x1+1)/2-w/2) if center else x0
        if x<1: x=1
        f=_font(path,size)
        dl.text((x*SS,(base+1)*SS),t,font=f,fill=tuple(int(round(v)) for v in fg)+(255,),anchor='ls')
        if clip:  # cut off at the original field edge
            px=int((x1+2)*SS); 
            arr=np.array(layer); arr[int((y0-3)*SS):int((y1+5)*SS),px:,:]=0; layer=Image.fromarray(arr); dl=ImageDraw.Draw(layer)
    small=layer.resize((W,H),Image.LANCZOS); out.alpha_composite(small)
    return out.convert('RGB')
