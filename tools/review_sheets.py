import json,os,sys
from PIL import Image, ImageDraw, ImageFont
import pathlib as _pl, os as _os, tempfile as _tf
_HERE=_pl.Path(__file__).resolve().parent; _DATA=_HERE/'data'; _REPO=_HERE.parent
OUTDIR=sys.argv[1] if len(sys.argv)>1 else _os.path.join(_tf.gettempdir(),'robocam-review')
idx=json.load(open(_DATA/'imgindex.json'))
ids=[i for i in idx if (_REPO/'img'/'en'/idx[i]).exists()]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15)
S=1.45; per=5; cw=int(225*S)+8; ch=int(400*S)+22; n=0
os.makedirs(OUTDIR,exist_ok=True)
for f in os.listdir(OUTDIR): os.remove(os.path.join(OUTDIR,f))
for s in range(0,len(ids),per):
    chunk=ids[s:s+per]; sheet=Image.new('RGB',(per*cw,2*ch),'white'); d=ImageDraw.Draw(sheet)
    for k,i in enumerate(chunk):
        for r,lang in enumerate(('en','sv')):
            im=Image.open(_REPO/'img'/lang/idx[i]).convert('RGB'); im=im.resize((int(im.width*S),int(im.height*S)),Image.LANCZOS)
            if im.width>cw-8: im.thumbnail((cw-8,ch-24))
            sheet.paste(im,(k*cw+4,r*ch+20)); d.text((k*cw+4,r*ch+2),f'#{i} {lang.upper()} {idx[i].split("/")[-1][:16]}',fill='red',font=font)
    sheet.save(os.path.join(OUTDIR,f'r{n:02d}.png')); n+=1
print(n,'sheets in',OUTDIR)
