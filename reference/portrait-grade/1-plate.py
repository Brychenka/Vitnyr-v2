import cv2,numpy as np
S='/private/tmp/claude-501/-Users-igor-Downloads-Vitnyr-site-v2/b3610828-2f2c-46ce-bd1d-00a6dbba87fb/scratchpad/'
P=S+'portrait/pro/'
src=cv2.imread(S+'../images/4.jpg').astype(np.float32)/255
A=cv2.imread(P+'alpha.png',0).astype(np.float32)/255
H,W=A.shape
# --- background plate: paint out the car and the sign, then defocus further
hard=(A>.02).astype(np.uint8)
kill=np.zeros((H,W),np.uint8)
kill[520:870,0:500]=1      # car
kill[610:720,1340:1920]=1  # BERLIN CITY + neighbour sign
kill=kill*(1-cv2.dilate(hard,np.ones((31,31),np.uint8)))
u8=(src*255).astype(np.uint8)
sm=cv2.resize(u8,(W//4,H//4),interpolation=cv2.INTER_AREA); km=cv2.resize(kill,(W//4,H//4),interpolation=cv2.INTER_NEAREST)
inp=cv2.inpaint(sm,km,9,cv2.INPAINT_TELEA)
inp=cv2.resize(inp,(W,H),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
kf=cv2.GaussianBlur(kill.astype(np.float32),(0,0),12)[...,None]
plate=src*(1-kf)+inp*kf
# the subject's area is filled by a mask-normalised blur of what surrounds it, so the defocus
# never drags the sweater (or a trunk-shaped blob) into the ground
keep=(1-cv2.dilate(hard,np.ones((25,25),np.uint8))).astype(np.float32)
sm4=lambda x:cv2.resize(x,(W//4,H//4),interpolation=cv2.INTER_AREA)
up=lambda x:cv2.resize(x,(W,H),interpolation=cv2.INTER_CUBIC)
k4=sm4(keep); p4=sm4(plate)
out=None
for sig in (80,30,12,5):
    num=cv2.GaussianBlur(p4*k4[...,None],(0,0),sig); den=cv2.GaussianBlur(k4,(0,0),sig)[...,None]
    est=num/np.maximum(den,1e-6)
    out=est if out is None else out*(1-np.clip(den*2.5,0,1))+est*np.clip(den*2.5,0,1)
fillp=up(out)
plate=plate*keep[...,None]+fillp*(1-keep[...,None])
plate=cv2.GaussianBlur(plate,(0,0),7)

np.save(P+'plate.npy',plate)
cv2.imwrite(P+'plate.jpg',cv2.resize((np.clip(plate,0,1)*255).astype(np.uint8),(1000,666)))
