"""The six small vignettes for the rest of the page — the plates' vocabulary
(ruled ground, bowed hatch strokes, one <path> per weight class, the stroke
figure on a --bg halo) at spot size, with no labels. See .vig in style.css.

    python3 vignettes.py still-life > still-life.svg

still-life (hero), runestone (§01), chain (§02), mirror (§04),
empty-chair (§05), chess-clock (footer; its hands are turned by main.js)."""
import math, random, sys, os
from ink import jitter, smooth, inside

def f(v): return str(int(round(v)))
def poly_d(p): return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in p) + "Z"
def line_d(a, b): return f"M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}"
def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
def ellipse(cx, cy, rx, ry, a0=0, a1=360, n=48, rot=0):
    r = math.radians(rot)
    pts = []
    for k in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * k / n)
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x*math.cos(r) - y*math.sin(r), cy + x*math.sin(r) + y*math.cos(r)))
    return pts


class Plate:
    KEYS = ("sky", "alt", "eng1", "shadow", "paper", "hatch", "line", "dot",
            "rope", "coil", "weak", "weakline", "halo", "torso", "thick", "leg", "thin", "faint")

    def __init__(self, W, H, seed):
        self.W, self.H = W, H
        self.rng = random.Random(seed)
        self.o = {k: [] for k in self.KEYS}
        self.heads, self.extra = [], []
        self.par = "xMidYMid meet"

    def ink(self, pts, amp=.4, step=8, scale=30):
        return smooth(jitter(pts, self.rng, amp, step, scale))

    def hatch(self, poly, angle, spacing, minlen=3, keep=None, bow=.9):
        rng = self.rng
        a = math.radians(angle); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
        cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
        R = math.hypot(max(xs)-min(xs), max(ys)-min(ys)) / 2 + 2
        d, o, st = [], -R, 1.4
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

    def solid(self, poly, angle, spacing, line="line", hatch="hatch", **kw):
        self.o["paper"].append(poly_d(poly))
        self.o[hatch].append(self.hatch(poly, angle, spacing, **kw))
        self.o[line].append(poly_d(poly))

    def ruled(self, y0, y1, keep, step=5):
        """The engraver's ruled ground. keep(x, y) -> probability a length is cut."""
        rng = self.rng
        for k, y in enumerate(range(y0, y1, step)):
            x = rng.uniform(0, 30)
            while x < self.W:
                L = rng.uniform(60, 220)
                if rng.random() < keep(x + L/2, y):
                    self.o["alt" if k % 2 else "sky"].append(f"M{int(x)} {y}H{int(min(self.W, x + L))}")
                x += L + rng.uniform(5, 24)

    def vignette(self, cx, cy, rx, ry, base=.8):
        """Ruling that fades out toward an oval edge: the old book vignette."""
        def keep(x, y):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            return max(0, base * (1 - d ** 1.4))
        return keep

    def ground(self, gy, x0, x1):
        self.o["eng1"].append("".join(
            f"M{f(a)} {f(y)}Q{f((a+b)/2)} {f(y-3)} {f(b)} {f(y+1)}"
            for y, a, b in [(gy, x0, x1), (gy + 7, x0 + 30, x1 - 20), (gy + 13, x0 + 10, x1 - 60)]))

    def person(self, head, spine, arms, legs, r=7.5):
        def P(p): return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in p)
        segs = [(spine, "torso")]
        for s, e, h in arms: segs += [([s, e], "thick"), ([e, h], "thin")]
        for hp, k, ft in legs: segs += [([hp, k], "leg"), ([k, ft], "thin")]
        for p, w in segs:
            d = smooth(p) if len(p) > 2 else P(p)
            self.o[w].append(d); self.o["halo"].append(d)
        self.heads.append((head, r))

    def svg(self):
        o = self.o
        def G(c, k): return f'<path class="{c}" d="{"".join(o[k])}"/>' if o[k] else ""
        heads = "".join(f'<circle class="plate__halo" stroke="none" cx="{f(x)}" cy="{f(y)}" r="{r+3}"/>' for (x, y), r in self.heads)
        headink = "".join(f'<circle class="person__head" cx="{f(x)}" cy="{f(y)}" r="{r}"/>' for (x, y), r in self.heads)
        return f'''<svg class="vig__svg" viewBox="0 0 {self.W} {self.H}" preserveAspectRatio="{self.par}" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
<g class="plate__ink">
{G("eng eng--sky", "sky")}
{G("eng eng--sky eng--alt", "alt")}
{G("eng eng--1", "eng1")}
{G("eng eng--1", "shadow")}
<path class="plate__paper" stroke="none" d="{"".join(o["paper"])}"/>
{G("eng eng--faint", "faint")}
{G("eng eng--2", "hatch")}
{G("eng eng--3", "line")}
{G("vig__weak", "weak")}
{G("vig__weakline", "weakline")}
<path class="plate__dot" stroke="none" d="{"".join(o["dot"])}"/>
</g>
<g class="plate__figure">
{G("plate__halo", "halo")}{heads}
<g class="person">{G("person--torso", "torso")}{G("person--thick", "thick")}{G("person--leg", "leg")}{G("person--thin", "thin")}{headink}</g>
{G("plate__rope", "rope")}
{G("plate__rope vig__coil", "coil")}
{"".join(self.extra)}
</g>
</svg>'''


# ---------------------------------------------------------------- 1. hero still life
def still_life():
    p = Plate(560, 360, 7)
    GY = 318
    p.ruled(10, GY - 4, p.vignette(290, 200, 300, 190, .75))
    p.ground(GY, 30, 540)
    # cast shadow to the left of everything
    p.o["shadow"].append(p.hatch([(60, GY), (500, GY), (470, GY - 10), (20, GY - 12)], 0, 2.4))
    # books, lying, English first and largest
    y = GY
    for w, h, dx in [(250, 30, 40), (226, 24, 52), (238, 27, 44)]:
        b = rect(dx, y - h, dx + w, y)
        p.solid(b, 0, 2.3, keep=lambda x, yy, b=b: x > b[0][0] + 26 or yy > b[2][1] - 6)
        # spine bands and the page block's lines on the fore-edge
        x0 = dx + 10
        p.o["line"].append(line_d((x0, y - h), (x0, y)) + line_d((x0 + 8, y - h), (x0 + 8, y)))
        p.o["eng1"].append("".join(line_d((dx + w - 4, yy), (dx + w - 30, yy)) for yy in range(int(y - h + 5), int(y - 3), 3)))
        y -= h
    top = y
    # the knight on the books
    s = 1.25; cx = 150
    knight = [(24, 0), (28, 14), (29, 28), (27, 42), (22, 54), (15, 64), (9, 71), (7, 80), (5, 90), (0, 81), (-6, 77),
              (-14, 72), (-22, 66), (-30, 58), (-37, 51), (-42, 45), (-45, 39), (-45, 34), (-42, 30), (-35, 29), (-28, 29),
              (-21, 31), (-15, 32), (-13, 27), (-16, 19), (-20, 10), (-23, 0)]
    base = [(0, 34), (5, 34), (6, 31), (10, 30), (12, 27), (16, 26), (18, 22), (22, 22), (22, 0)]
    right = [(cx + r*s, top - h*s) for h, r in base]
    outline = [(2*cx - x, yy) for x, yy in right] + right[::-1]
    p.o["paper"].append(poly_d(outline))
    p.o["hatch"].append(p.hatch(outline, 90, 2.6, keep=lambda x, yy: x > cx + 6))
    p.o["line"].append(poly_d(outline))
    head = [(cx + x*s*1.05, top - (22 + yy)*s*1.02) for x, yy in knight]
    hd = smooth(head + head[:1]) + "Z"
    p.o["paper"].append(hd)
    p.o["hatch"].append(p.hatch(head, 68, 2.8, keep=lambda x, yy: x > cx - 8*s or yy > top - 52*s))
    p.o["hatch"].append(p.hatch(head, 150, 3.2, keep=lambda x, yy: x > cx + 6*s))
    p.o["line"].append("".join(p.ink([(cx + (20 - 3*k)*s, top - (24 + 8*k)*s), (cx + (14 - 3*k)*s, top - (30 + 8*k)*s)], .3, 3, 10) for k in range(6)))
    p.o["line"].append(hd)
    ex, ey = cx - 16*s, top - 84*s
    p.o["dot"].append(f"M{f(ex-2.6)} {f(ey)}a2.6 1.9 0 1 0 5.2 0a2.6 1.9 0 1 0 -5.2 0")
    # chalk bag behind the coil
    bx, bw, bt = 446, 64, GY - 88
    bag = [(bx, GY - 2), (bx + bw, GY - 2), (bx + bw + 3, bt + 14), (bx + bw - 4, bt), (bx + 4, bt), (bx - 3, bt + 14)]
    p.solid(bag, 75, 2.6, keep=lambda x, yy: x > bx + bw * .45 or yy > GY - 22)
    p.o["paper"].append(poly_d(ellipse(bx + bw/2, bt + 2, bw/2 - 4, 6)))
    p.o["line"].append(smooth(ellipse(bx + bw/2, bt + 2, bw/2 - 4, 6)))
    p.o["line"].append(p.ink([(bx + 20, bt + 4), (bx + 14, bt - 16), (bx + 30, bt - 22)], .4, 4, 10))
    # coil of rope on the ground, in the target ink
    cx2, cy2 = 400, GY - 16
    coil = []
    for k in range(7):
        rx, ry = 92 - k*7, 22 - k*1.6
        pts = ellipse(cx2 + k*1.5, cy2 - k*3.2, rx, ry, -10 + k*20, 350 + k*20, 60)
        coil.append(smooth(jitter(pts, p.rng, .5, 6, 20)))
    p.o["paper"].append(poly_d(ellipse(cx2, cy2 - 8, 94, 30)))
    p.o["coil"].append("".join(coil))
    p.o["coil"].append(p.ink([(cx2 + 88, cy2 + 4), (cx2 + 112, cy2 + 12), (cx2 + 132, cy2 + 6)], .6, 6, 14))
    return p.svg()


# ---------------------------------------------------------------- 2. runestone
def runestone():
    p = Plate(360, 400, 11)
    GY = 360
    p.ruled(8, GY - 4, p.vignette(180, 220, 200, 210, .7))
    p.ground(GY, 10, 350)
    stone = [(96, GY), (84, 300), (82, 220), (92, 140), (112, 80), (146, 44), (190, 34), (230, 46), (258, 84), (272, 150), (276, 240), (268, 310), (262, GY)]
    st = jitter(stone, p.rng, 1.4, 6, 30)
    p.o["paper"].append(poly_d(st))
    # granite: long strokes following the stone's lean, heavy on the shadow (right) side
    p.o["hatch"].append(p.hatch(st, 96, 2.4, keep=lambda x, y: x > 212 + (y - 200) * .1))
    p.o["faint"].append(p.hatch(st, 98, 5.5, keep=lambda x, y: p.rng.random() < .35))
    p.o["line"].append(smooth(st + st[:1]))
    p.o["shadow"].append(p.hatch([(262, GY), (340, GY + 2), (330, GY - 8), (268, GY - 12)], 0, 2.4))
    # the carved band: two close lines following the stone's edge, runes ticked between them
    cx0, cy0 = 180, 210
    def inset(pts, k): return [(cx0 + (x - cx0) * k, cy0 + (y - cy0) * k) for x, y in pts]
    rim = [q for q in st if q[1] < GY - 26]
    outer, inner = inset(rim, .86), inset(rim, .79)
    p.o["line"].append(smooth(outer) + smooth(inner))
    ticks = []
    for k in range(2, len(outer) - 2, 3):
        (x0, y0), (x1, y1) = outer[k], inner[k]
        ticks.append(line_d((x0, y0), (x1, y1)))
        if k % 2: ticks.append(line_d((x0, y0), ((x0 + x1) / 2 + 3, (y0 + y1) / 2 - 3)))
    p.o["line"].append("".join(ticks))
    # the mark cut into the face: three grooves, the Y of Vitnyr; each groove is
    # two cut edges with the shadowed wall hatched along one side only
    def groove(a, b, w=11):
        ang = math.atan2(b[1] - a[1], b[0] - a[0]); nx, ny = -math.sin(ang), math.cos(ang)
        ends = lambda k: [(a[0] + nx*w*k, a[1] + ny*w*k), (b[0] + nx*w*k, b[1] + ny*w*k)]
        L, M, R = ends(.5), ends(.05), ends(-.5)
        body = [L[0], L[1], R[1], R[0]]
        p.o["paper"].append(poly_d(body))
        p.o["hatch"].append(p.hatch([L[0], L[1], M[1], M[0]], math.degrees(ang) + 90, 1.5))
        p.o["line"].append(p.ink(L + [R[1]] + R[::-1] + [L[0]], .15, 4, 10))
    groove((180, 200), (138, 140)); groove((180, 200), (222, 140)); groove((180, 212), (180, 296))
    return p.svg()


# ---------------------------------------------------------------- 3. the chain
def chain():
    p = Plate(900, 170, 5)
    p.ruled(6, 166, p.vignette(450, 86, 480, 110, .5))
    p.par = "xMidYMid slice"   # phones crop to the middle, where the weak link hangs
    def catenary(x): return 50 + 50 * (1 - ((x - 450) / 420) ** 2)
    n, x0, x1, weak = 13, 30, 870, 6
    for k in range(n):
        xa = x0 + (x1 - x0) * k / n; xb = x0 + (x1 - x0) * (k + 1) / n
        cx, cy = (xa + xb) / 2, (catenary(xa) + catenary(xb)) / 2
        ang = math.degrees(math.atan2(catenary(xb) - catenary(xa), xb - xa))
        is_weak = k == weak
        L = (xb - xa) * .92
        if k % 2 == 0:  # face-on: an oval ring with a hole, shaded under
            outer = ellipse(cx, cy, L / 2 + 14, 22, 0, 360, 48, ang)
            inner = ellipse(cx, cy, L / 2 - 6, 9, 0, 360, 36, ang)
            if is_weak:  # worn thin, a crack open on top: the weakest link
                outer = ellipse(cx, cy + 3, L / 2 + 16, 19, 0, 360, 48, ang + 7)
                p.o["paper"].append(poly_d(outer))
                p.o["weak"].append(p.hatch(outer, ang + 90, 2.0, keep=lambda x, y, cy=cy: y > cy - 2 and not inside(inner, x, y)))
                p.o["weakline"].append(smooth(jitter(outer, p.rng, .8, 5, 10)) + smooth(inner))
                gx, gy = cx + 8, cy - 18
                p.o["paper"].append(poly_d(rect(gx - 3, gy - 2, gx + 4, gy + 8)))
                p.o["weakline"].append(line_d((gx - 3, gy - 1), (gx - 1, gy + 7)) + line_d((gx + 4, gy - 1), (gx + 2, gy + 7)))
                continue
            p.o["paper"].append(poly_d(outer))
            p.o["hatch"].append(p.hatch(outer, ang + 90, 2.6, keep=lambda x, y, cy=cy: y > cy + 1 and not inside(inner, x, y)))
            p.o["line"].append(smooth(outer) + smooth(inner))
            p.o["paper"].append(poly_d(inner))
        else:  # edge-on: a bar with a rounded end, mostly in shadow
            bar = ellipse(cx, cy, L / 2 + 20, 7, 0, 360, 36, ang)
            p.o["paper"].append(poly_d(bar))
            p.o["hatch"].append(p.hatch(bar, ang + 90, 2.2, keep=lambda x, y, cy=cy: y > cy - 1.5))
            p.o["line"].append(smooth(bar))
    # pegs it hangs from
    for x in (x0 - 10, x1 + 10):
        peg = rect(x - 7, 26, x + 7, 72)
        p.solid(peg, 90, 2.0)
    return p.svg()


# ---------------------------------------------------------------- 4. the mirror
def mirror():
    p = Plate(440, 380, 23)
    GY = 352
    p.ruled(8, GY - 4, p.vignette(220, 200, 250, 210, .72))
    p.ground(GY, 10, 430)
    # cheval glass: oval in a frame between two posts
    mx, my, rx, ry = 286, 170, 64, 118
    frame = ellipse(mx, my, rx + 9, ry + 9, 0, 360, 60)
    glass = ellipse(mx, my, rx, ry, 0, 360, 60)
    p.o["paper"].append(poly_d(frame))
    p.o["hatch"].append(p.hatch(frame, 90, 2.0, keep=lambda x, y: not inside(glass, x, y) and x > mx - 10))
    p.o["line"].append(smooth(frame) + smooth(glass))
    p.o["paper"].append(poly_d(glass))
    p.o["faint"].append(p.hatch(glass, 60, 6.5, minlen=10, keep=lambda x, y: (x - mx) > -20 and p.rng.random() < .55))
    for sx in (mx - rx - 18, mx + rx + 12):
        p.solid(rect(sx, 60, sx + 7, GY), 90, 2.0, keep=lambda x, y, sx=sx: x > sx + 3)
        p.solid(rect(sx - 22, GY - 6, sx + 30, GY), 0, 2.0)
    for sx in (mx - rx - 18, mx + rx + 12):
        p.o["dot"].append(f"M{sx - 1} {my}a4.5 4.5 0 1 0 9 0a4.5 4.5 0 1 0 -9 0")
    # the reflection, faint, inside the glass
    def P(pts): return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
    rhx, rhy = mx + 6, my - 52
    p.o["faint"].append(P([(rhx + 2, rhy + 9), (rhx + 4, rhy + 62)]) + P([(rhx + 2, rhy + 14), (rhx - 12, rhy + 40), (rhx - 8, rhy + 64)])
                        + P([(rhx + 3, rhy + 14), (rhx + 18, rhy + 40), (rhx + 16, rhy + 62)]) + P([(rhx + 4, rhy + 62), (rhx - 6, rhy + 104)])
                        + P([(rhx + 4, rhy + 62), (rhx + 14, rhy + 104)]))
    p.o["faint"].append(f"M{rhx - 7} {rhy}a7 7 0 1 0 14 0a7 7 0 1 0 -14 0")
    # the person, standing, facing the glass
    hx, hy = 130, 150
    p.person((hx, hy), [(hx + 2, hy + 11), (hx + 3, hy + 50), (hx + 2, hy + 92)],
             [((hx + 3, hy + 16), (hx - 12, hy + 52), (hx - 8, hy + 88)), ((hx + 3, hy + 16), (hx + 22, hy + 48), (hx + 30, hy + 76))],
             [((hx + 2, hy + 92), (hx - 8, hy + 148), (hx - 12, GY - 4)), ((hx + 2, hy + 92), (hx + 14, hy + 148), (hx + 20, GY - 4))], r=8.5)
    return p.svg()


# ---------------------------------------------------------------- 5. the empty chair
def empty_chair():
    p = Plate(640, 320, 41)
    GY = 300
    p.ruled(8, GY - 6, p.vignette(320, 170, 360, 200, .75))
    p.ground(GY, 20, 620)
    sy = 232
    def chair(seat_x0, seat_x1, back_x, lean, back_h=96):
        p.solid(rect(seat_x0, sy - 5, seat_x1, sy + 2), 0, 2.2)
        p.solid([(back_x - 4, sy), (back_x - 4 + lean, sy - back_h), (back_x + 3 + lean, sy - back_h), (back_x + 3, sy)], 92, 2.2)
        p.o["line"].append(line_d((seat_x0 + 3, sy + 2), (seat_x0 + 1, GY)) + line_d((seat_x1 - 3, sy + 2), (seat_x1 - 1, GY)))
    # the empty chair, pulled out from the table, a little turned toward the reader
    chair(88, 150, 90, -10)
    p.o["shadow"].append(p.hatch([(80, GY), (160, GY), (150, GY - 6), (70, GY - 8)], 0, 2.4))
    # the table
    top = [(196, 204), (452, 204), (464, 192), (208, 192)]
    p.solid(top, 0, 3.0, minlen=4, keep=lambda x, y: not (250 < x < 290 or 380 < x < 410) and p.rng.random() < .5)
    p.solid(rect(196, 204, 452, 212), 0, 2.2)
    for lx in (208, 436):
        p.solid(rect(lx, 212, lx + 8, GY), 90, 2.4, keep=lambda x, y, lx=lx: x > lx + 4)
    # two cups: one by the empty place, one by the coach
    for cx in (258, 392):
        p.solid(rect(cx - 7, 178, cx + 7, 196), 90, 2.2, keep=lambda x, y, cx=cx: x > cx)
        p.o["line"].append(f"M{cx + 7} 182C{cx + 15} 182 {cx + 15} 192 {cx + 7} 192")
        p.o["eng1"].append(p.ink([(cx - 2, 174), (cx + 2, 166), (cx - 2, 156)], .6, 3, 8))
    # the coach, seated, hands on the table, turned to the empty chair
    chair(486, 544, 542, 4)
    hx, hy = 506, 134
    p.person((hx, hy), [(522, 228), (518, 196), (510, 166), (506, 146)],
             [((508, 152), (484, 182), (448, 190)), ((510, 154), (494, 190), (440, 196))],
             [((522, 228), (468, 230), (472, 296))], r=8.5)
    p.o["thin"].append(line_d((472, 296), (458, 298)))
    p.o["halo"].append(line_d((472, 296), (458, 298)))
    return p.svg()


# ---------------------------------------------------------------- 6. chess clock
def chess_clock():
    p = Plate(460, 300, 3)
    GY = 268
    p.ruled(8, GY - 4, p.vignette(230, 160, 260, 170, .55))
    p.ground(GY, 20, 440)
    # the case: a wedge seen from the front, slanted top face
    front = [(70, GY), (390, GY), (390, 110), (70, 110)]
    topf = [(70, 110), (390, 110), (372, 84), (88, 84)]
    p.solid(front, 0, 2.6, keep=lambda x, y: y > GY - 22 or x > 360)
    p.solid(topf, 0, 3.4, minlen=6, keep=lambda x, y: p.rng.random() < .55)
    p.o["shadow"].append(p.hatch([(30, GY), (390, GY), (380, GY - 8), (20, GY - 10)], 0, 2.4))
    # two plungers: Igor's down (he moved), yours up
    p.solid(rect(126, 74, 172, 84), 0, 2.0)
    p.solid(rect(142, 64, 156, 74), 90, 2.0)
    p.solid(rect(288, 56, 334, 66), 0, 2.0)
    p.solid(rect(304, 30, 318, 56), 90, 2.0, keep=lambda x, y: x > 311)
    p.solid(rect(300, 66, 322, 84), 90, 2.0, keep=lambda x, y: x > 312)
    # dials
    dials = []
    for cx, side in ((150, "igor"), (310, "you")):
        cy, r = 180, 52
        bezel = ellipse(cx, cy, r + 8, r + 8)
        face = ellipse(cx, cy, r, r)
        p.o["paper"].append(poly_d(bezel))
        p.o["hatch"].append(p.hatch(bezel, 90, 1.8, keep=lambda x, y, cx=cx, cy=cy: not inside(face, x, y) and x > cx - 6))
        p.o["line"].append(smooth(bezel) + smooth(face))
        p.o["paper"].append(poly_d(face))
        ticks = []
        for k in range(12):
            a = math.radians(k * 30)
            r0 = r - (10 if k % 3 == 0 else 6)
            ticks.append(line_d((cx + r0*math.sin(a), cy - r0*math.cos(a)), (cx + (r - 2)*math.sin(a), cy - (r - 2)*math.cos(a))))
        p.o["line"].append("".join(ticks))
        # the flag at five to twelve
        p.o["line"].append(f"M{cx + 6} {cy - r + 14}L{cx + 14} {cy - r + 24}L{cx + 6} {cy - r + 26}Z")
        dials.append((cx, cy, r, side))
    # hands: groups the page turns; the raised (right) side is yours and runs
    stopped = {"h": 10.13 * 30, "m": 8 * 6}     # Igor's side, stopped when he pressed
    for cx, cy, r, side in dials:
        rot = (lambda k: f' transform="rotate({stopped[k]:.0f} {cx} {cy})"') if side == "igor" else (lambda k: "")
        p.extra.append(
            f'<g class="vig__hand" data-hand="h" data-side="{side}" data-c="{cx} {cy}"{rot("h")}><path class="vig__handink" d="M{cx} {cy + 6}L{cx} {cy - r * .5:.0f}"/></g>'
            f'<g class="vig__hand" data-hand="m" data-side="{side}" data-c="{cx} {cy}"{rot("m")}><path class="vig__handink vig__handink--m" d="M{cx} {cy + 8}L{cx} {cy - r * .82:.0f}"/></g>'
            + (f'<g class="vig__hand" data-hand="s" data-side="{side}" data-c="{cx} {cy}"><path class="vig__handink vig__handink--s" d="M{cx} {cy + 10}L{cx} {cy - r * .86:.0f}"/></g>' if side == "you" else "")
            + f'<circle class="person__head" cx="{cx}" cy="{cy}" r="3.2"/>')
    return p.svg()


MAKERS = {"still-life": still_life, "runestone": runestone, "chain": chain,
          "mirror": mirror, "empty-chair": empty_chair, "chess-clock": chess_clock}

if __name__ == "__main__":
    sys.stdout.write(MAKERS[sys.argv[1]]())
