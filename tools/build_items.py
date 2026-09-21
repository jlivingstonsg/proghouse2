import json,re,difflib,sys
from gloss import G
import pathlib as _pl, os as _os, tempfile as _tf
_HERE=_pl.Path(__file__).resolve().parent; _DATA=_HERE/'data'; _REPO=_HERE.parent
d=json.load(open(_DATA/'ocr'/'segs.json',encoding='utf-8'))
first=json.load(open(_DATA/'ocr'/'lines.json',encoding='utf-8'))
from PIL import Image
import segs as _segs
idx_=json.load(open(_DATA/'imgindex.json'))
_CY=re.compile(r'[А-Яа-яЁё]')
def _inter(a,b):
    w=min(a[2],b[2])-max(a[0],b[0]); h=min(a[3],b[3])-max(a[1],b[1])
    return max(0,w)*max(0,h)
for i_,v_ in first.items():
    if i_ not in d: continue
    im_=None
    for L in v_['lines']:
        if L['conf']<80 or len(_CY.findall(L['text']))<3: continue
        bx=L['box']; ar=max(1,(bx[2]-bx[0])*(bx[3]-bx[1]))
        covered=any(_CY.search(sg['text']) and _inter(bx,sg['box'])>0.3*ar for sg in d[i_]['segs'])
        if covered: continue
        if im_ is None: im_=Image.open(_REPO/'img'/idx_[i_]).convert('RGB')
        rb=_segs.refine(im_,[bx[0],bx[1],bx[2],bx[3]])
        d[i_]['segs'].append(dict(box=rb,text=L['text'],conf=L['conf'],words=[dict(t=L['text'],c=L['conf'],x0=rb[0],x1=rb[2])]))
    d[i_]['segs'].sort(key=lambda sg:(sg['box'][1]//6,sg['box'][0]))

CYR=re.compile(r'[А-Яа-яЁё]')
def norm(t):
    t=t.lower().replace('ё','е')
    t=re.sub(r'[^a-zа-я0-9 /.:]',' ',t)
    return re.sub(r'\s+',' ',t).strip()
KEYS={k:norm(k.replace('|',' ')) for k in G}
CENTER_KEYS={k for k in G if k.isupper()}|{"Отмена","Сохранить","Отмена|Сохранить","Удалить","Добавить","Удалить|Добавить","Да","Нет|Да","готово","Всегда","Только один раз","Приложение запрашивает","разрешение на включение","Bluetooth. Разрешить?"}
PILL_KEYS={"Начать управление...","Сервер RoboCam работает","Сервер RoboCam выключен","EV3 не подключен:","Подключено к EV3:","Робот не подключен:"}
PILL_FOLLOW={"Исследователь EV3"}
CLIP_KEYS={"Простой колёсный робот с упр"}
OVR={('54','11'):'Значение изменяющее мощность и угол за',('52','0'):('Программное обеспечение для учителя',1,6),('60','0'):('Программное обеспечение для учителя',2,6)}
def letters_upper(t):
    L=[c for c in t if c.isalpha()]
    return bool(L) and all(c.isupper() for c in L)

ALIAS={'otkjiohutb':'ОТКЛОНИТЬ','вобосат доступ':'"RoboCam" доступ','вобосат прямой':'"RoboCam" Прямой'}
def best(text):
    nt=norm(text); res=(0,None)
    for k,nk in KEYS.items():
        r=difflib.SequenceMatcher(None,nt,nk).ratio()
        if nt==nk: r=1.0
        if letters_upper(text)==letters_upper(k): r+=0.012
        if r>res[0]: res=(r,k)
    return res
def junk(w):
    t=w['t']; return (not CYR.search(t)) and len(t)<=3 and not re.fullmatch(r'[A-Za-z]{2,3}\d?',t) or len(t)==1

def match_seg(seg):
    words=seg['words']; cands=[]
    n=len(words)
    for a in range(0,min(3,n)):           # strip leading junk words
        if a and not all(junk(w) for w in words[:a]): break
        for b in range(0,min(2,n-a)):     # strip trailing junk words
            if b and not all(junk(w) for w in words[n-b:]): break
            sub=words[a:n-b] if b else words[a:]
            if not sub: continue
            t=' '.join(w['t'] for w in sub)
            r,k=best(t)
            # penalise stripping real-looking words
            pen=0.02*a+0.02*b
            cands.append((r-pen,r,k,a,b,sub))
    if not cands: return None
    cands.sort(key=lambda c:-c[0]); return cands[0]
def dedupe(its):
    def inter(a,c):
        w=min(a[2],c[2])-max(a[0],c[0]); h=min(a[3],c[3])-max(a[1],c[1]); return max(0,w)*max(0,h)
    def area(a): return max(1,(a[2]-a[0]+1)*(a[3]-a[1]+1))
    keep=[]
    for x in its:
        dup=None
        for j,y in enumerate(keep):
            if inter(x['box'],y['box'])>0.5*min(area(x['box']),area(y['box'])): dup=j; break
        if dup is None: keep.append(x); continue
        y=keep[dup]
        # prefer the item whose source text has the same letter case as the OCR'd text; then the tighter box
        sx=letters_upper(x['src'])==letters_upper(x['ocr']); sy=letters_upper(y['src'])==letters_upper(y['ocr'])
        if (sx and not sy) or (sx==sy and area(x['box'])<area(y['box'])): keep[dup]=x
    return keep

def build(minratio=0.84):
    items={}; unmatched=[]; weak=[]
    for i,v in d.items():
        W,H=v['size']; its=[]; prev_key=None
        for k,seg in enumerate(v['segs']):
            txt=' '.join(seg['text'].split())
            al=ALIAS.get(norm(txt))
            if len(CYR.findall(txt))<2 and not al: continue
            m=match_seg(seg)
            if al: m=(1,1.0,al,0,0,seg['words'])
            if (i,str(k)) in OVR or (i,k) in OVR:
                kk=OVR.get((i,k)) or OVR.get((i,str(k)))
                a_=b_=0
                if isinstance(kk,tuple): kk,a_,b_=kk
                m=(1,1.0,kk,a_,b_,seg['words'][a_:len(seg['words'])-b_ if b_ else None])
            if not m or m[1]<minratio:
                if len(CYR.findall(txt))>=3 and seg['conf']>=40: unmatched.append((i,k,seg['conf'],txt,seg['box']))
                continue
            _,r,key,a,b,sub=m
            if r<0.93: weak.append((i,k,round(r,2),txt,key))
            x0,y0,x1,y1=seg['box']
            if a: x0=int(round(sub[0]['x0']))
            if b: x1=int(round(sub[-1]['x1']))
            parts=key.split('|')
            en,sv=G[key]
            if len(parts)==1:
                its.append(dict(k=k,ocr=txt,box=[x0,y0,x1,y1],src=key,EN=en,SV=sv,center=(key in CENTER_KEYS) or (key in PILL_KEYS) or (key in PILL_FOLLOW and prev_key in PILL_KEYS),clip=key in CLIP_KEYS))
                prev_key=key
            else:
                # split into N parts at word boundaries
                ws=[w for w in sub if re.search(r'\w',w['t'])]; pos=0; bxs=[]
                for p in parts:
                    n1=len(p.split()); seg_w=ws[pos:pos+n1]; pos+=n1
                    if seg_w: bxs.append((int(round(seg_w[0]['x0'])),int(round(seg_w[-1]['x1']))))
                if len(bxs)!=len(parts):
                    bw=(x1-x0)//len(parts); bxs=[(x0+q*bw,x0+(q+1)*bw) for q in range(len(parts))]
                for p,(px0,px1),e,s_ in zip(parts,bxs,en.split('|'),sv.split('|')):
                    its.append(dict(k=k,ocr=txt,box=[px0,y0,px1,y1],src=p,EN=e,SV=s_,center=True,clip=False,tighten=True))
        items[i]=dedupe(its)
    return items,unmatched,weak
if __name__=='__main__':
    items,unmatched,weak=build()
    json.dump(items,open(_DATA/'ocr'/'items.json','w',encoding='utf-8'),ensure_ascii=False)
    print('images with items:',sum(1 for v in items.values() if v),'| items:',sum(len(v) for v in items.values()))
    print('\nWEAK matches (ratio<0.93):')
    for w in weak: print('  ',w)
    print('\nUNMATCHED Cyrillic segments:')
    for u in unmatched: print('  ',u)
