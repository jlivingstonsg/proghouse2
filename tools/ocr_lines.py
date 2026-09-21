import json,subprocess,glob,os,re,csv,io
from PIL import Image
S=3
import pathlib as _pl, os as _os, tempfile as _tf
_HERE=_pl.Path(__file__).resolve().parent; _DATA=_HERE/'data'; _REPO=_HERE.parent
idx=json.load(open(_DATA/'imgindex.json'))
CYR=re.compile(r'[А-Яа-яЁё]')
out={}
for i,rel in idx.items():
    f=str(_REPO/'img'/rel)
    im=Image.open(f).convert('RGB')
    W,H=im.size
    if W<60: continue
    big=im.resize((W*S,H*S),Image.LANCZOS); tmp=_os.path.join(_tf.gettempdir(),f'robocam_ocr_{i}.png'); big.save(tmp)
    r=subprocess.run(['tesseract',tmp,'stdout','-l','rus+eng','--psm','11','tsv'],capture_output=True,text=True)
    rows=list(csv.DictReader(io.StringIO(r.stdout),delimiter='\t',quoting=csv.QUOTE_NONE))
    words=[]
    for w in rows:
        if w['level']!='5' or not w['text'].strip(): continue
        words.append(dict(x0=int(w['left'])/S,y0=int(w['top'])/S,x1=(int(w['left'])+int(w['width']))/S,y1=(int(w['top'])+int(w['height']))/S,t=w['text'],c=float(w['conf'])))
    # group words into lines (union-find: vertical overlap + small horizontal gap, any order)
    n=len(words); par=list(range(n))
    def find(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for i1 in range(n):
        for j1 in range(i1+1,n):
            p,q=words[i1],words[j1]
            ov=min(p['y1'],q['y1'])-max(p['y0'],q['y0']); hh=min(p['y1']-p['y0'],q['y1']-q['y0'])
            gap=max(q['x0']-p['x1'],p['x0']-q['x1'])
            if hh>0 and ov>=0.55*hh and gap<max(p['y1']-p['y0'],q['y1']-q['y0'])*1.4: par[find(i1)]=find(j1)
    groups={}
    for k,w in enumerate(words): groups.setdefault(find(k),[]).append(w)
    lines=[]
    for g in groups.values():
        lines.append(dict(x0=min(w['x0'] for w in g),y0=min(w['y0'] for w in g),x1=max(w['x1'] for w in g),y1=max(w['y1'] for w in g),w=g))
    res=[]
    for L in sorted(lines,key=lambda L:(L['y0'],L['x0'])):
        L['w'].sort(key=lambda w:w['x0']); txt=' '.join(w['t'] for w in L['w'])
        if CYR.search(txt): res.append(dict(box=[round(L['x0']),round(L['y0']),round(L['x1']),round(L['y1'])],text=txt,conf=round(sum(w['c'] for w in L['w'])/len(L['w']))))
    out[i]=dict(file=rel,size=[W,H],lines=res)
    os.remove(tmp)
json.dump(out,open(_DATA/'ocr'/'lines.json','w'),ensure_ascii=False,indent=0)
n=sum(len(v['lines']) for v in out.values()); print('images with ru text:',sum(1 for v in out.values() if v['lines']),'lines:',n)
