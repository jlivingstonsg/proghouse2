import json,subprocess,os,re,csv,io,sys
from PIL import Image
lang=sys.argv[1]
import pathlib as _pl, os as _os, tempfile as _tf
_HERE=_pl.Path(__file__).resolve().parent; _DATA=_HERE/'data'; _REPO=_HERE.parent
idx=json.load(open(_DATA/'imgindex.json')); CYR=re.compile(r'[А-Яа-яЁё]')
left={}
for i,rel in idx.items():
    p=_REPO/'img'/lang/rel
    if not p.exists(): continue
    im=Image.open(p).convert('RGB'); S=3
    big=im.resize((im.width*S,im.height*S),Image.LANCZOS); _tmp=_os.path.join(_tf.gettempdir(),'robocam_check_x.png'); big.save(_tmp)
    r=subprocess.run(['tesseract',_tmp,'stdout','-l','rus+eng','--psm','11','tsv'],capture_output=True,text=True)
    rows=list(csv.DictReader(io.StringIO(r.stdout),delimiter='\t',quoting=csv.QUOTE_NONE))
    ws=[(w['text'],float(w['conf']),int(w['left'])//S,int(w['top'])//S) for w in rows if w['level']=='5' and w['text'].strip() and CYR.search(w['text']) and float(w["conf"])>=50 and len(CYR.findall(w["text"]))>=4]
    if ws: left[i]=(rel.split('/')[-1],ws)
for i,(f,ws) in left.items(): print(i,f,[(t,x,y) for t,c,x,y in ws][:8])
print('images with remaining Russian:',len(left))
