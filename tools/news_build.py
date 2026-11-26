import json, sys, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=sys.argv[1]; R='/home/user/gta6channel/brand/fonts/'
W,H=1080,1920; PINK=(255,64,170); PURP=(40,14,60)
def F(n,b=800): return ImageFont.truetype(R+f'TikTokSans-{b}.ttf',n)
def italic(img,cy):
    return img.transform(img.size,Image.AFFINE,(1,0.21,-0.21*cy,0,1,0),Image.BICUBIC)
def headline(lines,cy,size=110):
    """big italic text, line colors: (text,color)"""
    L=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(L); f=F(size); y=cy-len(lines)*size//2
    mw=max(d.textlength(t,font=f) for t,c in lines)
    if mw>700: size=int(size*700/mw); f=F(size); y=cy-len(lines)*size//2
    for t,c in lines:
        w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=c,stroke_width=9,stroke_fill='black'); y+=int(size*1.0)
    return italic(L,cy)
def pill(text,y,keys=(),size=40,check=None):
    L=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(L); f=F(size)
    words=text.split(); tw=sum(d.textlength(x+' ',font=f) for x in words)-d.textlength(' ',font=f)
    extra=size if check else 0
    x0=(W-tw-extra)/2; d.polygon([(x0-34,y-10),(x0+tw+extra+30,y-10),(x0+tw+extra+18,y+size+18),(x0-46,y+size+18)],fill=PURP+(235,),outline=PINK,width=4)
    x=x0
    for wd in words:
        d.text((x,y),wd,font=f,fill=PINK if wd.strip('.,?!').upper() in keys else 'white'); x+=d.textlength(wd+' ',font=f)
    if check:
        cx,cy2,r=x+size*0.45,y+size*0.62,size*0.36
        if check=='✓': d.line([(cx-r,cy2),(cx-r*0.25,cy2+r*0.75),(cx+r,cy2-r*0.8)],fill=(90,230,120),width=8,joint='curve')
        else: d.line([(cx-r,cy2-r),(cx+r,cy2+r)],fill=(255,70,70),width=8); d.line([(cx-r,cy2+r),(cx+r,cy2-r)],fill=(255,70,70),width=8)
    return italic(L,y+size//2)
def tag(num,label):
    L=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(L); f=F(40); y=250; x=130
    w1=d.textlength(num,font=f); d.polygon([(x,y),(x+w1+40,y),(x+w1+28,y+58),(x-12,y+58)],fill=PURP); d.text((x+16,y+4),num,font=f,fill='white')
    x2=x+w1+52; w2=d.textlength(label,font=f); d.polygon([(x2,y),(x2+w2+40,y),(x2+w2+28,y+58),(x2-12,y+58)],fill=PINK); d.text((x2+16,y+4),label,font=f,fill='white')
    return italic(L,279)
def credit():
    L=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(L)
    for t,y,s in [('Clips: @fanum, @ishowspeed (Twitch)',1400,26),('Post: @MasonWaltemyer (X)',1436,26),('Fan page. Not affiliated with Rockstar Games.',1476,26)]:
        f=F(s,700); w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill='white',stroke_width=3,stroke_fill='black')
    return L
TWEET=("🚨 JUST IN: Rockstar FIRED GTA 6 narrative writer ███████████ 🚨\n\nAlexa was exposed for running a WOKE blog teaching women how to manipulate men and take advantage of them.\n\n"
 "She DELETED her X account after her posts sparked major backlash.\n\nGTA 6 has a HORRIBLE 5.7/10 user score on Metacritic.\n\nGTA went from Dan Houser to THAT\n\n🟣 13 YEARS for a piece of junk 🟣")
def tweet_card():
    cw=760; f=F(29,700); fb=F(30,800)
    body=TWEET.replace('🚨','').replace('🟣','').replace('Alexa was','She was').replace('███████████ ','[name hidden]')
    lines=[]
    for para in body.split('\n'):
        lines+= textwrap.wrap(para.strip(),44) if para.strip() else ['']
    h=150+len(lines)*38+40
    C=Image.new('RGBA',(cw,h),(0,0,0,0)); d=ImageDraw.Draw(C); d.rounded_rectangle((0,0,cw-1,h-1),28,fill=(255,255,255,250))
    av=Image.open(S+'/av.jpg').resize((84,84)); m=Image.new('L',(84,84),0); ImageDraw.Draw(m).ellipse((0,0,83,83),fill=255); C.paste(av,(28,30),m)
    d.text((128,36),'Mason',font=fb,fill='black'); d.ellipse((235,40,263,68),fill=(29,155,240)); d.line([(241,55),(247,61),(258,47)],fill='white',width=4)
    d.text((128,76),'@MasonWaltemyer · Nov 26',font=F(26,700),fill=(110,118,125)); d.text((cw-64,28),'X',font=F(46,800),fill='black')
    y=140
    for ln in lines:
        x=32
        if '[name hidden]' in ln:
            a,b=ln.split('[name hidden]'); d.text((x,y),a,font=f,fill='black'); x+=d.textlength(a,font=f)
            d.rounded_rectangle((x,y+4,x+230,y+34),6,fill=(20,20,20)); x+=236; d.text((x,y),b,font=f,fill='black')
        else: d.text((x,y),ln,font=f,fill='black')
        y+=38
    L=Image.new('RGBA',(W,H),(0,0,0,0)); sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((160,350,160+cw,350+h),28,fill=(0,0,0,150))
    L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); L.alpha_composite(C,(160,330)); return L,330+h
words=json.load(open(S+'/vo/words.json'))
# caption chunks of <=3 words, break on punctuation
chunks=[];cur=[]
for w in words:
    cur.append(w)
    if len(cur)==3 or w[0][-1] in '.,?!:"':
        chunks.append(cur);cur=[]
if cur:chunks.append(cur)
KEYS={'FIRED','WOKE','MANIPULATE','DELETED','HORRIBLE','5.7','JUNK','NONE','CONFIRMED','HARASSMENT','DIFFERENT','99','DRAMA','HOUSER','RUMORS','BREAKING','LUCIA','HATE'}
def scene(t):
    if t<7.0: return 'A'
    if t<34.7: return 'B'
    if t<42.4: return 'C'
    if t<50.5: return 'D'
    if t<54.4: return 'E'
    return 'F'
card,cardbot=tweet_card()
def base(sc):
    L=Image.new('RGBA',(W,H),(0,0,0,0))
    if sc=='A': L.alpha_composite(tag('!','RUMOR')); L.alpha_composite(headline([('BREAKING',(255,255,255)),('NEWS',PINK)],560,150)); L.alpha_composite(pill('GTA 6 WRITER FIRED?',830,keys=('FIRED?',),size=46))
    if sc=='B': L.alpha_composite(tag('1','THE VIRAL POST')); L.alpha_composite(card)
    if sc=='C': L.alpha_composite(tag('2','FACT CHECK')); L.alpha_composite(headline([('NOT',(255,255,255)),('CONFIRMED',(255,70,70))],560,130)); L.alpha_composite(pill('ROCKSTAR: NO COMMENT',830,size=42,check='✗'))
    if sc=='D': L.alpha_composite(tag('3','WHAT WE KNOW')); L.alpha_composite(pill('X ACCOUNT DELETED',520,keys=('DELETED',),size=44,check='✓')); L.alpha_composite(pill('AFTER HARASSMENT WAVE',620,keys=('HARASSMENT',),size=44,check='✓')); L.alpha_composite(pill('HATE HIT THE WRONG WOMAN',720,keys=('WRONG',),size=44,check='✓'))
    if sc=='E': L.alpha_composite(tag('4','CRITICS')); L.alpha_composite(headline([('99',(90,230,120)),('METACRITIC',(255,255,255))],560,150))
    if sc=='F': L.alpha_composite(headline([('REAL NEWS',(255,255,255)),('OR DRAMA?',PINK)],600,125))
    L.alpha_composite(credit()); return L
cache={}; seq=[]; t=0.0
pts=[]
for c in chunks: pts.append((c[0][1],c))
end=float(sys.argv[2])
items=[]
for i,(st,c) in enumerate(pts):
    en=pts[i+1][0] if i+1<len(pts) else end
    items.append((st,en,c))
if items[0][0]>0: items.insert(0,(0,items[0][0],None))
lst=open(S+'/ov/list.txt','w'); n=0
for st,en,c in items:
    sc=scene(st+0.01)
    if sc not in cache: cache[sc]=base(sc)
    L=cache[sc].copy()
    if c:
        txt=' '.join(x[0] for x in c).replace('"','').replace("'","").upper()
        y=cardbot+40 if sc=='B' else 1150
        y=max(y,1150) if sc!='B' else min(max(y,1150),1340)
        L.alpha_composite(pill(txt,y,keys=KEYS,size=44))
    # handle scene boundary inside chunk: split
    fn=f'{S}/ov/{n:03d}.png'; L.save(fn); lst.write(f"file '{fn}'\nduration {en-st:.3f}\n"); n+=1
lst.write(f"file '{fn}'\n"); lst.close(); print(n,'frames, card bottom',cardbot)
