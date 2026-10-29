"""Production engraving for the climbing group: same composition as the canvas
board (ruled sky, a great roof from the right, a climber hanging off its lip),
but every weight class is ONE <path> of short straight/quadratic subpaths with
integer coordinates, so the whole plate stays small enough to inline."""
import math, random, sys
from ink import inside, jitter, smooth, densify

rng = random.Random(14)
W, H = 1200, 340
def i(v): return str(int(round(v)))

def ruled(y0, y1, step, keep):
    """Horizontal ruled lines, broken into lengths, as one d-string per (main, alt) set."""
    main, alt = [], []
    for k, y in enumerate(range(y0, y1, step)):
        x = rng.uniform(0, 40)
        while x < W:
            L = rng.uniform(160, 420)
            if rng.random() < keep(y):
                x2 = min(W, x + L)
                seg = f"M{i(x)} {y}H{i(x2)}"
                (alt if k % 2 else main).append(seg)
            x += L + rng.uniform(6, 30)
    return "".join(main), "".join(alt)

def hatch_d(poly, angle, spacing, minlen=10, gap=.1, bow=1.2):
    """Parallel engraved strokes clipped to poly; each one a gently bowed quadratic."""
    a = math.radians(angle); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
    R = math.hypot(max(xs)-min(xs), max(ys)-min(ys))
    out = []
    o = -R
    while o < R:
        o += spacing * rng.uniform(.85, 1.15)
        run, t = [], -R
        while t <= R:
            x, y = cx + nx*o + dx*t, cy + ny*o + dy*t
            ok = inside(poly, x, y)
            if ok: run.append((x, y))
            if (not ok or t + 2.5 > R) and run:
                j = 0
                while j < len(run):
                    n = rng.randint(10, 40)
                    seg = run[j:j+n]
                    j += n + (rng.randint(1, 3) if rng.random() < gap else 0)
                    if len(seg) * 2.5 < minlen: continue
                    (x0, y0), (x1, y1) = seg[0], seg[-1]
                    b = rng.uniform(-bow, bow)
                    mx, my = (x0+x1)/2 + nx*b, (y0+y1)/2 + ny*b
                    out.append(f"M{i(x0)} {i(y0)}Q{i(mx)} {i(my)} {i(x1)} {i(y1)}")
                run = []
            t += 2.5
    return "".join(out)

# sky: ruled, thinning toward the top; the odd lines are dropped at phone width
sky, sky_alt = ruled(8, 300, 5, lambda y: .82 - (300 - y) / 700)

roof_lip = [(612,118),(604,132),(626,140),(700,134),(780,140),(860,128),(940,138),(1020,130),(1100,140),(1200,132)]
rock = [(612,0),(1200,0),(1200,132)] + roof_lip[::-1][:-1] + [(612,118)]
wall = [(1200,132),(1100,140),(1060,200),(1080,260),(1060,320),(1200,330)]
e2 = hatch_d(rock, 165, 3.2, 12) + hatch_d(wall, 95, 3.0, 10, .15)
e3 = hatch_d([(700,0),(1200,0),(1200,60),(900,70),(760,80)], 20, 3.2, 10)
lip = smooth(jitter(roof_lip, rng, .8, 5, 20))
e1 = "".join(f"M{x0} {y}Q{(x0+x1)//2} {y-4} {x1} {y+1}" for y, x0, x1 in [(300,0,520),(312,80,700),(322,0,980),(332,200,1060)])

# climber hanging off the lip at full stretch, feet cut loose
def limbs(head, neck, hip, hands, feet):
    segs = [([neck, ((neck[0]+hip[0])/2 - 2, (neck[1]+hip[1])/2), hip], "torso")]
    for h in hands:
        mx, my = (neck[0]+h[0])/2, (neck[1]+h[1])/2
        e = (mx + (h[1]-neck[1])*.18, my - (h[0]-neck[0])*.18)
        segs += [([neck, e], "thick"), ([e, h], "thin")]
    for ft in feet:
        mx, my = (hip[0]+ft[0])/2, (hip[1]+ft[1])/2
        k = (mx - (ft[1]-hip[1])*.2, my + (ft[0]-hip[0])*.2)
        segs += [([hip, k], "leg"), ([k, ft], "thin")]
    return segs
head = (690, 160)
segs = limbs(head, (694,170), (700,214), [(676,140),(712,138)], [(674,262),(724,256)])
def poly(p): return "M" + "L".join(f"{i(x)} {i(y)}" for x, y in p)
halo = "".join(poly(p) for p, w in segs)
rope = smooth(jitter([(700,214),(668,236),(640,280),(626,340)], rng, .5, 5, 20))
arrow = smooth([(478,106),(560,112),(640,128)])

svg = f'''<svg class="climb-art__svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
<g class="climb-art__plate">
<path class="eng eng--sky" d="{sky}"/>
<path class="eng eng--sky eng--alt" d="{sky_alt}"/>
<path class="eng eng--1" d="{e1}"/>
<path class="eng eng--2" d="{e2}"/>
<path class="eng eng--3" d="{e3}"/>
<path class="eng eng--lip" d="{lip}"/>
</g>
<g class="climb-art__figure">
<path class="climb-art__halo" stroke="none" d="{halo}"/>
<circle class="climb-art__halo" stroke="none" cx="{head[0]}" cy="{head[1]}" r="8"/>
<path class="climb-art__rope" d="{rope}"/>
<g class="climber">{"".join(f'<path class="climber--{w}" d="{poly(p) if len(p) == 2 else smooth(p)}"/>' for p, w in segs)}<circle class="climber__head" fill="currentColor" stroke="none" cx="{head[0]}" cy="{head[1]}" r="7.5"/></g>
</g>
<g class="climb-art__labels">
<path class="lab-arrow" d="{arrow}"/>
<text class="lab" fill="currentColor" stroke="none" x="420" y="112" transform="rotate(-4 420 112)" data-en="crux" data-ru="ключ">crux</text>
</g>
</svg>'''
sys.stdout.write(svg)
