import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
cfg=json.load(open(sys.argv[1])); out=cfg["out_dir"]; os.makedirs(out,exist_ok=True)
F="brand/fonts/TikTokSans-800.ttf"; f=lambda s: ImageFont.truetype(F,s)
W,H=1080,1350; IMH=900; YEL,RED,WHITE=(255,214,0),(255,59,48),(255,255,255)
def wrap(d,s,font,maxw):
    lines,cur=[], ""
    for w in s.split():
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)>maxw and cur: lines.append(cur); cur=w
        else: cur=t
    return lines+[cur]
def ctext(d,y,s,font,fill,maxw=900):
    for ln in wrap(d,s,font,maxw):
        d.text((W//2,y),ln,font=font,fill=fill,anchor="mt",stroke_width=5,stroke_fill=(0,0,0)); y+=int(font.size*1.15)
    return y
def box(d,y,s,font):
    w=d.textlength(s,font=font); p=22
    d.rounded_rectangle((W/2-w/2-p,y,W/2+w/2+p,y+font.size+28),20,fill=WHITE)
    d.text((W//2,y+14),s,font=font,fill=(0,0,0),anchor="mt"); return y+font.size+40
for i,sl in enumerate(cfg["slides"],1):
    src=Image.open(sl["img"]).convert("RGB")
    bgim=src.resize((int(src.width*H/src.height),H)).filter(ImageFilter.GaussianBlur(30))
    x=(bgim.width-W)//2; im=Image.blend(bgim.crop((x,0,x+W,H)),Image.new("RGB",(W,H)),0.6)
    top=src.resize((W,int(src.height*W/src.width))); y0=max(0,(top.height-IMH)//2)
    im.paste(top.crop((0,y0,W,y0+IMH)),(0,0)); d=ImageDraw.Draw(im)
    if sl.get("cover"):
        y=IMH-120
        for ln in sl["title"]: y=box(d,y,ln,f(68))
        y=ctext(d,y+40,sl["sub"],f(56),YEL)
    else:
        y=IMH-70; y=box(d,y,sl["num"]+".",f(56))
        y=ctext(d,y+10,sl["head"],f(58),YEL)
        y=ctext(d,y+14,sl["how"],f(40),WHITE)
        if sl.get("cta"): ctext(d,y+24,sl["cta"],f(50),RED)
    d.text((W//2,1262),sl["credit"].replace("🎥 ","Clip: "),font=f(30),fill=WHITE,anchor="mt",stroke_width=3,stroke_fill=(0,0,0))
    d.text((W//2,1302),"Fan page. Not affiliated with Rockstar Games.",font=f(24),fill=(200,200,200),anchor="mt",stroke_width=3,stroke_fill=(0,0,0))
    p=f"{out}/{i:02d}.jpg"; im.save(p,quality=92); print(p)
