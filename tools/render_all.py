import json,os,sys
from PIL import Image
from retouch import retouch
import segs as SG
from extras import EXTRA
import pathlib
_HERE=pathlib.Path(__file__).resolve().parent; _DATA=_HERE/'data'; _REPO=_HERE.parent
idx=json.load(open(_DATA/'imgindex.json')); items=json.load(open(_DATA/'ocr'/'items.json',encoding='utf-8'))
only=set(sys.argv[1:])
done=[]
for i,rel in idx.items():
    if only and i not in only: continue
    its=list(items.get(i,[]))
    # extras replace any auto items that overlap their boxes
    ex=EXTRA.get(i,[])
    def ov(a,b): return not(a[2]<b[0] or b[2]<a[0] or a[3]<b[1] or b[3]<a[1])
    its=[x for x in its if not any(ov(x['box'],e['box']) for e in ex)]+ex
    if not its: continue
    src=Image.open(_REPO/'img'/rel)
    for x in its:
        if x.get('tighten'): x['box']=SG.refine(src.convert('RGB'),x['box'])
    if i in ('12','31'):   # diagrams: one common font size, as in the originals
        import statistics
        from retouch import text_w
        sz=statistics.median([(x['box'][2]-x['box'][0]+1)/text_w(x['src'],1) for x in its if x.get('src') and x['src'].strip()])
        for x in its: x['size']=sz
    for lang in ('EN','SV'):
        spec=[dict(box=x['box'],src=x.get('src'),text=x[lang],center=x.get('center',False),clip=x.get('clip',False),maxw=x.get('maxw'),fg=x.get('fg'),size=x.get('size')) for x in its]
        out=retouch(src,spec)
        p=str(_REPO/'img'/lang.lower()/rel); os.makedirs(os.path.dirname(p),exist_ok=True)
        out.save(p) if p.endswith('.png') else out.save(p,quality=93)
    done.append(i)
print('rendered images:',len(done))
