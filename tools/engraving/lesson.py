"""The English group's engraved plate: a lesson at a table, one person writing,
the other asking. Same vocabulary as engrave.py and staunton.py so all three
share .plate in style.css: the room is engraved, every weight class ONE <path>
with integer coordinates; the two people are the climbing plate's stroke figure
(.person) on a --bg halo.

    python3 lesson.py > plate.svg

The written line ("I am agree", am struck through in --ink-specimen) is its own
group, .plate__note: its words and strike are placed against each other, so on
phones the group is scaled as one instead of the words growing like .lab does."""
import math, random, sys
from ink import jitter, smooth, inside

rng = random.Random(41)
def f(v): return str(int(round(v)))
W, H = 1200, 340
GY = 318
out = {k: [] for k in ("sky", "alt", "paper", "eng1", "hatch", "line")}

def poly_d(p): return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in p) + "Z"
def line_d(a, b): return f"M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}"
def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
def ink(pts, amp=.3, step=8, scale=30): return smooth(jitter(pts, rng, amp, step, scale))

def hatch(poly, angle, spacing, minlen=3, keep=None, bow=.9):
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

def solid(poly, angle, spacing, **kw):
    """A drawn object: paper under it, engraved shading, outline."""
    out["paper"].append(poly_d(poly)); out["hatch"].append(hatch(poly, angle, spacing, **kw)); out["line"].append(poly_d(poly))

# ---- the wall: ruled like the other plates' skies, thinning upward; odd lines drop at phone width
for k, y in enumerate(range(8, GY - 8, 5)):
    x = rng.uniform(0, 40)
    while x < W:
        L = rng.uniform(140, 420)
        if rng.random() < .1 + .62*(y/GY):
            out["alt" if k % 2 else "sky"].append(f"M{int(x)} {y}H{int(min(W, x + L))}")
        x += L + rng.uniform(6, 30)
out["eng1"].append("".join(f"M{x0} {y}Q{(x0+x1)//2} {y-3} {x1} {y+1}" for y, x0, x1 in [(GY, 0, 1200), (GY+8, 60, 1140), (GY+15, 0, 1000)]))

# ---- the window, right; its glass a sparse diagonal at sky weight
out["paper"].append(poly_d(rect(920, 36, 1070, 232)))
out["hatch"].append(hatch([(1060, 46), (1070, 36), (1070, 232), (1060, 222)], 90, 2.2) + hatch(rect(920, 222, 1070, 232), 0, 2.2))
out["line"].append(poly_d(rect(920, 36, 1070, 232)) + poly_d(rect(930, 46, 1060, 222)) + line_d((995, 46), (995, 222)) + line_d((930, 134), (1060, 134)))
for px0, py0, px1, py1 in [(930, 46, 995, 134), (995, 46, 1060, 134), (930, 134, 995, 222), (995, 134, 1060, 222)]:
    out["eng1"].append(hatch(rect(px0 + 3, py0 + 3, px1 - 3, py1 - 3), 58, 7, minlen=8, keep=lambda x, y: rng.random() < .45))

# ---- books stacked on the floor, left
y = GY
for w, h, dx in [(96, 16, 0), (84, 12, 8), (90, 14, -4), (70, 11, 10)]:
    b = rect(196 + dx, y - h, 196 + dx + w, y)
    solid(b, 0, 2.4, keep=lambda x, yy, b=b: x > b[0][0] + 10); y -= h

# ---- two chairs facing each other across the table
def chair(seat_x0, seat_x1, back_x, lean):
    sy = 246
    solid(rect(seat_x0, sy - 5, seat_x1, sy + 2), 0, 2.2)
    solid([(back_x - 4, sy), (back_x - 4 + lean, 158), (back_x + 3 + lean, 158), (back_x + 3, sy)], 92, 2.2)
    out["line"].append(line_d((seat_x0 + 3, sy + 2), (seat_x0 + 1, GY)) + line_d((seat_x1 - 3, sy + 2), (seat_x1 - 1, GY)))
chair(362, 420, 364, -6)
chair(792, 850, 848, 2)

# ---- the table, its top seen a little from above; a notebook and a cup on it
top = [(470, 216), (746, 216), (758, 204), (482, 204)]
on_top = lambda x, y: not (514 < x < 616 or 682 < x < 704) and rng.random() < .5
solid(top, 0, 3.2, minlen=4, keep=on_top)
solid(rect(470, 216, 746, 224), 0, 2.2)
for lx in (482, 730):
    solid(rect(lx, 224, lx + 8, GY), 90, 2.4, keep=lambda x, y, lx=lx: x > lx + 4)
out["paper"].append(poly_d([(518, 213), (606, 213), (612, 207), (524, 207)]))
out["line"].append(poly_d([(518, 213), (606, 213), (612, 207), (524, 207)]))
out["eng1"].append(line_d((565, 213), (568, 207)))
solid(rect(686, 192, 700, 210), 90, 2.2, keep=lambda x, y: x > 693)
out["line"].append("M700 196C708 196 708 206 700 206")

# ---- the two people: the climbing plate's figure, seated
fig, halo, heads = [], [], []
def P(p): return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in p)
def person(head, spine, arms, legs):
    segs = [(spine, "torso")]
    for s, e, h in arms: segs += [([s, e], "thick"), ([e, h], "thin")]
    for hp, k, ft in legs: segs += [([hp, k], "leg"), ([k, ft], "thin")]
    for p, w in segs:
        d = smooth(p) if len(p) > 2 else P(p)
        fig.append((w, d))
    heads.append(head)
# the student, bent over the page, writing
person((464, 156), [(404, 240), (414, 210), (432, 182), (448, 166)],
       [((446, 170), (478, 198), (532, 204)), ((444, 170), (460, 208), (504, 212))],
       [((404, 240), (458, 242), (454, 312))])
fig += [("thin", P([(454, 312), (468, 314)])), ("thin", line_d((532, 204), (540, 210)))]
# the coach, upright, one hand open toward the page
person((790, 146), [(810, 240), (806, 208), (798, 180), (794, 162)],
       [((794, 166), (762, 196), (728, 180)), ((796, 168), (782, 206), (742, 214))],
       [((810, 240), (756, 242), (760, 312))])
fig += [("thin", P([(760, 312), (746, 314)])), ("thin", line_d((728, 180), (716, 172)) + line_d((728, 180), (714, 178)))]
halo = [d for w, d in fig]

# the coach's question reaches the struck word
move = ink([(708, 166), (670, 136), (630, 122), (602, 120)], .6, 8, 40)
(x0, y0), (x1, y1) = (630, 122), (602, 120)
a = math.atan2(y1-y0, x1-x0)
for sg in (-1, 1):
    b = a + math.pi + sg * .45
    move += line_d((x1, y1), (x1 + 11*math.cos(b), y1 + 11*math.sin(b)))

strike = ink([(512, 106), (552, 103)], .3, 4, 10)
leader = ink([(540, 122), (548, 160), (556, 200)], .3, 8, 30)
q_arrow = ink([(742, 62), (774, 96), (788, 132)], .3)

def G(cls, key): return f'<path class="{cls}" d="{"".join(out[key])}"/>' if out[key] else ""
by_w = {}
for w, d in fig: by_w.setdefault(w, []).append(d)
svg = f'''<svg class="plate__svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
<g class="plate__ink">
{G("eng eng--sky", "sky")}
{G("eng eng--sky eng--alt", "alt")}
<path class="plate__paper" stroke="none" d="{"".join(out["paper"])}"/>
{G("eng eng--1", "eng1")}
{G("eng eng--2", "hatch")}
{G("eng eng--3", "line")}
</g>
<g class="plate__figure">
<path class="plate__halo" stroke="none" d="{"".join(halo)}"/>
{"".join(f'<circle class="plate__halo" stroke="none" cx="{x}" cy="{y}" r="11"/>' for x, y in heads)}
<g class="person">{"".join(f'<path class="person--{w}" d="{"".join(ds)}"/>' for w, ds in by_w.items())}{"".join(f'<circle class="person__head" fill="currentColor" stroke="none" cx="{x}" cy="{y}" r="8.5"/>' for x, y in heads)}</g>
<path class="plate__move" d="{move}"/>
</g>
<g class="plate__labels">
<path class="lab-arrow lab-arrow--dash" d="{leader}"/>
<path class="lab-arrow" d="{q_arrow}"/>
<text class="lab" fill="currentColor" stroke="none" x="650" y="50" text-anchor="middle" transform="rotate(-3 650 50)" data-en="a state or an action?" data-ru="состояние или действие?">a state or an action?</text>
<g class="plate__note">
<text class="lab lab--note" fill="currentColor" stroke="none" x="488" y="112" transform="rotate(-3 488 112)">I</text>
<text class="lab lab--note" fill="currentColor" stroke="none" x="514" y="111" transform="rotate(-3 514 111)">am</text>
<text class="lab lab--note" fill="currentColor" stroke="none" x="562" y="108" transform="rotate(-3 562 108)">agree</text>
<path class="plate__strike" d="{strike}"/>
</g>
</g>
</svg>'''
sys.stdout.write(svg)
