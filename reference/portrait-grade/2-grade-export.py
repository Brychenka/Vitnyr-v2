import cv2,numpy as np
S='/private/tmp/claude-501/-Users-igor-Downloads-Vitnyr-site-v2/b3610828-2f2c-46ce-bd1d-00a6dbba87fb/scratchpad/'
P=S+'portrait/pro/'
src=cv2.imread(S+'../images/4.jpg').astype(np.float32)/255
A=cv2.imread(P+'alpha.png',0).astype(np.float32)/255
plate=np.load(P+'plate.npy')
X0,Y0,CW=280,40,1020; CH=CW*5//4
cr=lambda x:x[Y0:Y0+CH,X0:X0+CW]
src,A,plate=cr(src),cr(A),cr(plate); A3=A[...,None]
_a=np.clip(A3,.06,1); _F=np.clip((src-(1-A3)*plate)/_a,0,1)
_w=np.clip((A3-.9)/.08,0,1)          # solid interior keeps the original pixels untouched
src=src*_w+_F*(1-_w)
def hx(h): h=h.lstrip('#'); return np.array([int(h[4:6],16),int(h[2:4],16),int(h[0:2],16)],np.float32)/255
BG,FG,AM,GR=hx('EFEBE3'),hx('1D2224'),hx('B07C24'),hx('3D6543')
DBG,DFG,DGR=hx('171310'),hx('F2EFE8'),hx('4C7A52')
rng=np.random.default_rng(3)
def save(n,img,w=960):
    u=(np.clip(img,0,1)*255+.5).astype(np.uint8)
    cv2.imwrite(P+n+'.jpg',cv2.resize(u,(w,w*5//4),interpolation=cv2.INTER_AREA),[cv2.IMWRITE_JPEG_QUALITY,86])
def lum(x): return .2126*x[...,2]+.7152*x[...,1]+.0722*x[...,0]
def smooth(t): return t*t*(3-2*t)
def gmap(t,stops):
    t=np.clip(t,0,1)[...,None]; out=np.zeros(t.shape[:2]+(3,),np.float32)
    for (a,ca),(b,cb) in zip(stops,stops[1:]):
        k=np.clip((t-a)/(b-a),0,1); out+=((t>=a)&(t<b)).astype(np.float32)*(ca*(1-k)+cb*k)
    out+=(t>=stops[-1][0]).astype(np.float32)*stops[-1][1]
    return out
def hue_pull(img,src_h,dst_h,width,amt,sat=1.0):
    hsv=cv2.cvtColor(img.astype(np.float32),cv2.COLOR_BGR2HSV)
    h=hsv[...,0]; d=((h-src_h+180)%360)-180; w=np.clip(1-np.abs(d)/width,0,1)*amt
    hsv[...,0]=(h+(((dst_h-h+180)%360)-180)*w)%360; hsv[...,1]*=1-(1-sat)*w
    return cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
def bgr_h(c): return cv2.cvtColor(c[None,None].astype(np.float32),cv2.COLOR_BGR2HSV)[0,0]
hAM,hGR=bgr_h(AM)[0],bgr_h(GR)[0]
def paper_levels(img,lo,hi):
    # black point -> the site's ink, white point -> the site's paper: the photo can never be
    # darker than the type or brighter than the page it sits on
    return lo+(hi-lo)*np.clip(img,0,1)
def grain(shape,amt,scale=1.0):
    g=rng.normal(0,1,shape[:2]).astype(np.float32)
    if scale!=1: g=cv2.GaussianBlur(g,(0,0),scale)*scale*1.6
    return g[...,None]*amt

# ---------- A  Editorial colour: the magazine grade ----------
def editorial(dark=False):
    s=np.clip(src,0,1)
    s=hue_pull(s,30,hAM,28,.45,.92)               # camel knit toward the brand amber, a touch quieter
    s=hue_pull(s,105,hGR,55,.8,.62)                # leaves and hedge toward the brand green, muted
    L=lum(s)[...,None]; s=L+(s-L)*.88             # 12% off the saturation overall
    b=np.clip(plate,0,1); b=hue_pull(b,105,hGR,70,.9,.5); Lb=lum(b)[...,None]
    b=Lb+(b-Lb)*.5; b=.4+(b-.45)*.55               # ground: quieter and flatter than the subject
    img=s*A3+b*(1-A3)
    img=np.clip((img-.03)/.97,0,1)**.95
    img=smooth(img)*.35+img*.65                    # soft S curve
    img=paper_levels(img,FG*1.0,BG) if not dark else paper_levels(img,DBG*1.2+.01,DFG*.97)
    return np.clip(img+grain(img.shape,.018,.8),0,1)
import os
R='/Users/igor/Downloads/Vitnyr/site-v2/.claude/worktrees/agent-aa7cb30d6ef8875c6/assets/portrait/'
u=(np.clip(editorial(),0,1)*255+.5).astype(np.uint8)
for w,n,q in ((960,'igor@2x.jpg',72),(480,'igor.jpg',82)):
    cv2.imwrite(R+n,cv2.resize(u,(w,w*5//4),interpolation=cv2.INTER_AREA),[cv2.IMWRITE_JPEG_QUALITY,q,cv2.IMWRITE_JPEG_PROGRESSIVE,1,cv2.IMWRITE_JPEG_OPTIMIZE,1])
    print(n,os.path.getsize(R+n))
raise SystemExit

# ---------- B  Green ground: Igor in colour, the world in the target ink ----------
def greenground(dark=False):
    s=hue_pull(np.clip(src,0,1),30,hAM,28,.4,.95); L=lum(s)[...,None]; s=L+(s-L)*.9
    lb=lum(plate); lb=(lb-lb.min())/(np.percentile(lb,99.5)-lb.min()); lb=np.clip(lb,0,1)**.8*.72
    if not dark: g=gmap(lb,[(0,FG*.9+GR*.1),(.55,GR),(1,GR*.35+BG*.65)])
    else:        g=gmap(lb,[(0,DBG),(.6,DGR*.9),(1,DGR*.5+DFG*.5)])
    img=s*A3+g*(1-A3)
    img=smooth(np.clip(img,0,1))*.3+img*.7
    img=paper_levels(img,FG,BG) if not dark else paper_levels(img,DBG*1.2+.01,DFG*.97)
    return np.clip(img+grain(img.shape,.02,.8),0,1)
save('B-green-ground',greenground()); save('B-green-ground-dark',greenground(True))


def base_colour():
    s_=np.clip(src,0,1)
    s_=hue_pull(s_,30,hAM,28,.45,.92); s_=hue_pull(s_,105,hGR,55,.8,.62)
    L=lum(s_)[...,None]; return L+(s_-L)*.88
# ---------- E  Studio backdrop in the page's own paper ----------
def backdrop(dark=False):
    s_=base_colour()
    if not dark: bd=BG*.93+FG*.07
    else: bd=DBG*.9+DFG*.1
    # a faint tonal fall-off from the real ground, so it reads as a lit backdrop, not a flat cut-out
    Lp=lum(plate); Lp=cv2.GaussianBlur(Lp,(0,0),40); Lp=(Lp-Lp.mean())/(Lp.std()+1e-6)
    b=bd[None,None]*(1+Lp[...,None]*.025)
    img=s_*A3+b*(1-A3)
    img=smooth(np.clip(img,0,1))*.3+img*.7
    img=paper_levels(img,FG,BG) if not dark else paper_levels(img,DBG*1.2+.01,DFG*.97)
    img=np.where(A3>0,img,b)  # backdrop stays exactly the tint
    return np.clip(img+grain(img.shape,.014,.8),0,1)
save('E-backdrop',backdrop()); save('E-backdrop-dark',backdrop(True))
# ---------- F  Green block: the target ink as a flat poster ground ----------
def block(dark=False):
    s_=base_colour()
    bd=GR if not dark else DGR*.85
    Lp=lum(plate); Lp=cv2.GaussianBlur(Lp,(0,0),50); Lp=(Lp-Lp.mean())/(Lp.std()+1e-6)
    b=bd[None,None]*(1+Lp[...,None]*.03)
    img=s_*A3+b*(1-A3)
    img=smooth(np.clip(img,0,1))*.25+img*.75
    img=paper_levels(img,FG,BG) if not dark else paper_levels(img,DBG*1.2+.01,DFG*.97)
    return np.clip(img+grain(img.shape,.014,.8),0,1)
save('F-green-block',block()); save('F-green-block-dark',block(True))
# ---------- G  Toned print: charcoal-to-paper silver print, amber in the mids, a trace of real colour ----------
def toned(dark=False):
    s_=base_colour(); b=plate
    Lb=lum(b)[...,None]; b=Lb+(b-Lb)*.5; b=.45+(b-.45)*.6
    img=s_*A3+b*(1-A3)
    L=lum(img); L=np.clip((L-.03)/.9,0,1); L=smooth(L)*.4+L*.6
    lo,hi=(FG,BG) if not dark else (DBG*1.2+.01,DFG*.97)
    ramp=lo[None,None]*(1-L[...,None])+hi[None,None]*L[...,None]
    mid=(4*L*(1-L))[...,None]
    ramp=ramp*(1-mid*.28)+AM*mid*.28*(ramp.mean(-1,keepdims=True)/AM.mean())
    chroma=img-lum(img)[...,None]
    img=ramp+chroma*.35
    return np.clip(img+grain(img.shape,.02,.8),0,1)
save('G-toned-print',toned()); save('G-toned-print-dark',toned(True))
