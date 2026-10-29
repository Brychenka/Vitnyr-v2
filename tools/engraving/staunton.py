"""The chess group's engraved plate: Staunton queen, knight and king on a ruled
ground, the knight forking the other two. Same vocabulary as engrave.py (the
climbing plate) so both share .plate in style.css: every weight class is ONE
<path>, coordinates rounded, so the plate stays small enough to inline.

    python3 staunton.py > plate.svg

Pieces are turned solids, engraved with meridian lines (denser on the shadow
side) and collar rings; the knight's head is a hand-placed profile hatched in
two directions. Pieces are filled with --bg (.plate__paper) so the ruled ground
stops at their edges, and their cast shadows are drawn before that fill."""
import math, random, sys
from ink import jitter, smooth, inside

rng = random.Random(21)
def f(v): return str(int(round(v)))
W, H = 1200, 340
GY = 318                       # the ground line the pieces stand on
out = {k: [] for k in ("sky", "alt", "ground", "shadow", "paper", "hatch", "ring", "line", "dot", "move", "lab")}

def poly_d(p): return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in p) + "Z"
def line_d(a, b): return f"M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}"
def ink(pts, amp=.6, step=8, scale=40): return smooth(jitter(pts, rng, amp, step, scale))

def hatch(poly, angle, spacing, minlen=4, keep=None, bow=.9):
    """Parallel engraved strokes clipped to poly, each a gently bowed quadratic."""
    a = math.radians(angle); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
    R = math.hypot(max(xs)-min(xs), max(ys)-min(ys)) / 2 + 2
    d, o, st = [], -R, 1.6
    while o < R:
        o += spacing * rng.uniform(.88, 1.12)
        run, t = [], -R
        while t <= R + st:
            x, y = cx + nx*o + dx*t, cy + ny*o + dy*t
            ok = t <= R and inside(poly, x, y)
            if ok: run.append((x, y))
            if not ok and run:
                j = 0
                while j < len(run):
                    n = rng.randint(14, 60)
                    seg = run[j:j+n]; j += n + (rng.randint(1, 3) if rng.random() < .08 else 0)
                    if len(seg) * st < minlen: continue
                    (x0, y0), (x1, y1) = seg[0], seg[-1]
                    if keep and not keep((x0+x1)/2, (y0+y1)/2): continue
                    b = rng.uniform(-bow, bow)
                    d.append(f"M{f(x0)} {f(y0)}Q{f((x0+x1)/2+nx*b)} {f((y0+y1)/2+ny*b)} {f(x1)} {f(y1)}")
                run = []
            t += st
    return "".join(d)

# ---- the ground: ruled like the climbing plate's sky, thinning upward; odd lines drop at phone width
for k, y in enumerate(range(8, 306, 5)):
    x = rng.uniform(0, 40)
    while x < W:
        L = rng.uniform(140, 420)
        if rng.random() < .82 - (306 - y) / 640:
            out["alt" if k % 2 else "sky"].append(f"M{int(x)} {y}H{int(min(W, x + L))}")
        x += L + rng.uniform(6, 30)
out["ground"].append("".join(f"M{x0} {y}Q{(x0+x1)//2} {y-3} {x1} {y+1}" for y, x0, x1 in [(GY, 0, 1200), (GY+8, 60, 1140), (GY+15, 0, 1000)]))

# ---- Staunton profiles: (height, radius) from the base up, in units of s px
def sphere(hc, r, n=8):
    return [(hc + r*math.sin(math.radians(a)), r*math.cos(math.radians(a))) for a in [-90 + 180*j/n for j in range(n+1)]]
BASE = [(0, 34), (5, 34), (6, 31), (10, 30), (12, 27), (16, 26), (18, 22)]
PROF = {
    "queen":  BASE + [(26, 17), (80, 11), (84, 18), (88, 18), (90, 12), (94, 14), (102, 20), (110, 22), (112, 18), (114, 8)] + sphere(118, 4)[4:],
    "king":   BASE + [(26, 18), (88, 12), (92, 19), (96, 19), (98, 13), (102, 15), (112, 20), (118, 20), (122, 12), (124, 0)],
    "knight": BASE + [(22, 22), (22, 0)],
}
KNIGHT = [(24, 0), (28, 14), (29, 28), (27, 42), (22, 54), (15, 64), (9, 71), (7, 80), (5, 90), (0, 81), (-6, 77),
          (-14, 72), (-22, 66), (-30, 58), (-37, 51), (-42, 45), (-45, 39), (-45, 34), (-42, 30), (-35, 29), (-28, 29),
          (-21, 31), (-15, 32), (-13, 27), (-16, 19), (-20, 10), (-23, 0)]

def rfun(prof):
    def r(h):
        for (h0, r0), (h1, r1) in zip(prof, prof[1:]):
            if h0 <= h <= h1:
                return r0 if h1 == h0 else r0 + (r1-r0)*(h-h0)/(h1-h0)
        return 0
    return r

def shadow(cx, w, L):
    out["shadow"].append(hatch([(cx + w*.5, GY), (cx - w*.5, GY), (cx - w*.5 - L, GY - 4), (cx - w*.4 - L*1.05, GY - 9), (cx + w*.2, GY - 9)], 0, 2.6))

def piece(kind, cx, s):
    prof = PROF[kind]
    right = [(cx + r*s, GY - h*s) for h, r in prof]
    outline = [(2*cx - x, y) for x, y in right] + right[::-1]
    out["paper"].append(poly_d(outline))
    r = rfun(prof); hmax = max(h for h, _ in prof)
    # meridians of a turned piece, crowding toward the shadow (right) side
    for th in [-62, -40, -18, 4, 18, 30, 40, 49, 57, 64, 70, 76, 81, 86]:
        pts = [(cx + r(h)*s*math.sin(math.radians(th)) + rng.uniform(-.3, .3), GY - h*s) for h in [hmax*j/40 for j in range(41)] if r(h) > .6]
        if len(pts) > 3: out["hatch"].append("M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts))
    # collar rings: the front half of each ellipse at the profile's turning points
    out["ring"].append("".join("M" + "L".join(f"{f(cx + rr*s*math.cos(math.radians(a)))} {f(GY - h*s + rr*s*.16*math.sin(math.radians(a)))}" for a in range(0, 181, 15)) for h, rr in prof[1:-1]))
    out["line"].append(poly_d(outline))
    if kind == "king":
        t = GY - 124*s
        out["line"].append(line_d((cx, t + 2*s), (cx, t - 16*s)) + line_d((cx - 6*s, t - 9*s), (cx + 6*s, t - 9*s)))
    if kind == "queen":                       # the coronet's points
        t = GY - 110*s
        out["line"].append("M" + "L".join(f"{f(cx + x*s)} {f(t - (5*s if k % 2 else 0))}" for k, x in enumerate(range(-20, 21, 5))))
    if kind == "knight":
        head = [(cx + x*s*1.05, GY - (22 + y)*s*1.02) for x, y in KNIGHT]
        hd = smooth(head + head[:1]) + "Z"
        out["paper"].append(hd)
        out["hatch"].append(hatch(head, 68, 3.0*s/2.2, keep=lambda x, y: x > cx - 8*s or y > GY - 52*s))
        out["hatch"].append(hatch(head, 150, 3.4*s/2.2, keep=lambda x, y: x > cx + 6*s))
        out["line"].append("".join(ink([(cx + (20 - 3*k)*s, GY - (24 + 8*k)*s), (cx + (14 - 3*k)*s, GY - (30 + 8*k)*s)], .3, 3, 10) for k in range(6)))
        out["line"].append(hd)
        ex, ey, rx, ry = cx - 16*s, GY - 84*s, 2.2*s, 1.6*s
        out["dot"].append(f"M{f(ex-rx)} {f(ey)}a{f(rx)} {f(ry)} 0 1 0 {f(2*rx)} 0a{f(rx)} {f(ry)} 0 1 0 -{f(2*rx)} 0")

def arrow(pts, head=11):
    d = ink(pts)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    a = math.atan2(y1-y0, x1-x0)
    for sg in (-1, 1):
        b = a + math.pi + sg * .45
        d += line_d((x1, y1), (x1 + head*math.cos(b), y1 + head*math.sin(b)))
    out["move"].append(d)

Q, N, K = (480, 1.85), (650, 2.2), (820, 1.9)
shadow(Q[0], 34*Q[1]*1.4, 150); shadow(N[0], 34*N[1]*1.4, 170); shadow(K[0], 34*K[1]*1.4, 170)
for kind, (cx, s) in (("queen", Q), ("king", K), ("knight", N)):
    piece(kind, cx, s)
# the fork: two jumps out of the knight's one square
arrow([(664, 88), (704, 46), (770, 34), (816, 42)])
arrow([(636, 88), (600, 50), (540, 44), (494, 84)])
lab_arrow = ink([(392, 66), (424, 56), (470, 50)], .4)

def P(cls, key): return f'<path class="{cls}" d="{"".join(out[key])}"/>' if out[key] else ""
svg = f'''<svg class="plate__svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
<g class="plate__ink">
{P("eng eng--sky", "sky")}
{P("eng eng--sky eng--alt", "alt")}
{P("eng eng--1", "ground")}
{P("eng eng--1", "shadow")}
<path class="plate__paper" stroke="none" d="{"".join(out["paper"])}"/>
{P("eng eng--2", "hatch")}
{P("eng eng--1", "ring")}
{P("eng eng--3", "line")}
<path class="plate__dot" fill="currentColor" stroke="none" d="{"".join(out["dot"])}"/>
</g>
<g class="plate__figure">
<path class="plate__move" d="{"".join(out["move"])}"/>
</g>
<g class="plate__labels">
<path class="lab-arrow" d="{lab_arrow}"/>
<text class="lab" fill="currentColor" stroke="none" x="300" y="76" transform="rotate(-4 300 76)" data-en="the fork" data-ru="вилка">the fork</text>
</g>
</svg>'''
sys.stdout.write(svg)
