"""Hand-inked SVG path helpers: jittered polylines -> smooth cubic paths."""
import math, random

def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s

def densify(pts, step=7.0):
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(d / step))
        for i in range(1, n + 1):
            t = i / n
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    return out

class Wob:
    """Smooth 1-D noise from a few random sines."""
    def __init__(self, rng, amp, scale=40.0):
        self.terms = [(rng.uniform(0.5, 1.6) / scale, rng.uniform(0, 6.28), rng.uniform(.4, 1)) for _ in range(3)]
        self.amp = amp
    def __call__(self, s):
        return self.amp * sum(a * math.sin(fr * s + ph) for fr, ph, a in self.terms) / 1.6

def jitter(pts, rng, amp=1.6, step=7.0, scale=40.0):
    pts = densify(pts, step)
    w = Wob(rng, amp, scale)
    out, s = [], 0.0
    for i, (x, y) in enumerate(pts):
        if i:
            s += math.hypot(x - pts[i-1][0], y - pts[i-1][1])
        a, b = pts[max(0, i-1)], pts[min(len(pts)-1, i+1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        k = w(s) + rng.uniform(-amp, amp) * .15
        out.append((x + nx * k, y + ny * k))
    return out

def smooth(pts, tension=1.0):
    """Catmull-Rom through pts as a cubic Bezier path string."""
    if len(pts) < 3:
        return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
    d = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
    for i in range(len(pts) - 1):
        p0 = pts[max(0, i-1)]; p1 = pts[i]; p2 = pts[i+1]; p3 = pts[min(len(pts)-1, i+2)]
        c1 = (p1[0] + (p2[0]-p0[0]) / 6 * tension, p1[1] + (p2[1]-p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0]-p1[0]) / 6 * tension, p2[1] - (p3[1]-p1[1]) / 6 * tension)
        d.append(f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}")
    return "".join(d)

def stroke(pts, rng, amp=1.4, step=9.0, scale=40.0):
    return smooth(jitter(pts, rng, amp, step, scale))

def inside(poly, x, y):
    c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c

def hatch(poly, rng, angle_deg, spacing, minlen=10, gap=0.25, density=None, amp=.6):
    """Parallel strokes at angle, broken into pen-length pieces, kept inside poly.
    density(x, y) -> 0..1 probability a piece is drawn."""
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
    R = math.hypot(max(xs)-min(xs), max(ys)-min(ys))
    out = []
    o = -R
    while o < R:
        o += spacing * rng.uniform(.75, 1.3)
        run = []
        t = -R
        while t < R:
            t += 2.5
            x = cx + nx * o + dx * t; y = cy + ny * o + dy * t
            ok = inside(poly, x, y)
            if ok:
                run.append((x, y))
            if (not ok or t >= R) and run:
                # break the run into pen strokes with gaps
                i = 0
                while i < len(run):
                    n = rng.randint(4, 14)
                    seg = run[i:i+n]
                    i += n + (rng.randint(1, 4) if rng.random() < gap else 0)
                    if len(seg) * 2.5 < minlen:
                        continue
                    mx, my = seg[len(seg)//2]
                    if density and rng.random() > density(mx, my):
                        continue
                    sh = rng.uniform(-1.2, 1.2)
                    seg = [(px + nx * sh, py + ny * sh) for px, py in seg]
                    out.append(smooth(jitter([seg[0], seg[-1]], rng, amp, 6, 18)))
                run = []
    return out
