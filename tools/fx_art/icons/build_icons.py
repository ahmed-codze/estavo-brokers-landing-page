#!/usr/bin/env python3
"""Source of assets/img/icons/estavo-fx.svg (Estavo Signal icon sprite) + .fx-lab/icons.html.

Run: python3 tools/fx_art/icons/build_icons.py   (lives in a subfolder so build-fx-art.py ignores it)
Rules: 24px grid, every stroke 1.6 at full opacity (no stroke-width / opacity overrides);
the second tone is ONLY the duo fill layer (duo()/duo_circ()), which kit.icon() strips for mono use.
Each icon must stay readable at 16-20px: one idea per icon, at most ~6 strokes."""
import math, os, re

REPO = os.environ.get('FX_ICONS_REPO') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
D = 'style="fill:var(--fx-duo,currentColor);opacity:var(--fx-duo-o,.18);stroke:none"'


def f(n):
    s = f'{n:.2f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


def p(d, extra=''):
    return f'<path d="{d}"{(" " + extra) if extra else ""}/>'


def duo(d):
    return f'<path d="{d}" {D}/>'


def dot(x, y, r=1.15):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="currentColor" stroke="none"/>'


def circ(x, y, r, extra=''):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"{(" " + extra) if extra else ""}/>'


def duo_circ(x, y, r):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" {D}/>'


def glyph_d(cx, cy, r):
    k = r / 9
    P = lambda dx, dy: f'{f(cx + dx * k)} {f(cy + dy * k)}'
    return (f'M{P(0,-9)}C{P(1,-4)} {P(4,-1)} {P(9,0)}C{P(4,1)} {P(1,4)} {P(0,9)}'
            f'C{P(-1,4)} {P(-4,1)} {P(-9,0)}C{P(-4,-1)} {P(-1,-4)} {P(0,-9)}Z')


def glyph(cx, cy, r):
    return f'<path d="{glyph_d(cx, cy, r)}" fill="currentColor" stroke="none"/>'


def glyph_line(cx, cy, r):
    return duo(glyph_d(cx, cy, r)) + p(glyph_d(cx, cy, r))


def star_d(cx, cy, ro, ri, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180 / n)
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z'


def glyph_contains(cx, cy, r, x, y, pad):
    """Approximate: is (x,y) inside the four-point glyph grown by pad?"""
    dx, dy = abs(x - cx), abs(y - cy)
    k = r / 9
    # glyph boundary in first quadrant approx by curve (t): parametric bezier sample
    best = 1e9
    for i in range(41):
        t = i / 40
        bx = (3 * (1 - t) ** 2 * t * 1 + 3 * (1 - t) * t * t * 4 + t ** 3 * 9) * k
        by = ((1 - t) ** 3 * 9 + 3 * (1 - t) ** 2 * t * 4 + 3 * (1 - t) * t * t * 1) * k
        best = min(best, math.hypot(dx - bx, dy - by))
    # inside test: below the curve
    inside = False
    if dx <= 9 * k and dy <= 9 * k:
        # find curve y at dx
        for i in range(200):
            t = i / 199
            bx = (3 * (1 - t) ** 2 * t * 1 + 3 * (1 - t) * t * t * 4 + t ** 3 * 9) * k
            if bx >= dx:
                by = ((1 - t) ** 3 * 9 + 3 * (1 - t) ** 2 * t * 4 + 3 * (1 - t) * t * t * 1) * k
                inside = dy <= by
                break
    return inside or best < pad


def orbit_d(cx, cy, rx, ry, rot, avoid=None, steps=120):
    """Ellipse as polyline segments, broken where `avoid(x,y)` is true."""
    a = math.radians(rot)
    segs, cur = [], []
    for i in range(steps + 1):
        t = 2 * math.pi * i / steps
        ex, ey = rx * math.cos(t), ry * math.sin(t)
        x = cx + ex * math.cos(a) - ey * math.sin(a)
        y = cy + ex * math.sin(a) + ey * math.cos(a)
        if avoid and avoid(x, y):
            if len(cur) > 1:
                segs.append(cur)
            cur = []
        else:
            cur.append((x, y))
    if len(cur) > 1:
        segs.append(cur)
    # merge wrap-around
    if len(segs) > 1 and segs[0][0] == segs[-1][-1] or (len(segs) > 1 and math.hypot(segs[0][0][0] - segs[-1][-1][0], segs[0][0][1] - segs[-1][-1][1]) < 1e-6):
        segs[0] = segs[-1] + segs[0][1:]
        segs.pop()
    out = []
    for s in segs:
        out.append('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in s[::2] + ([s[-1]] if len(s) % 2 == 0 else [])))
    return ''.join(out)


def orbit_point(cx, cy, rx, ry, rot, deg):
    a, t = math.radians(rot), math.radians(deg)
    ex, ey = rx * math.cos(t), ry * math.sin(t)
    return cx + ex * math.cos(a) - ey * math.sin(a), cy + ex * math.sin(a) + ey * math.cos(a)


I = {}

# ───────────────────────────── pillars ─────────────────────────────
PIN = 'M12 17.6c-3.1-2.9-5.3-5.8-5.3-8.6a5.3 5.3 0 0 1 10.6 0c0 2.8-2.2 5.7-5.3 8.6z'
I['market'] = [
    duo(PIN), p(PIN), circ(12, 9, 1.9),
    # radar floor: front ellipse + broken back ellipse + inner ring
    p('M3.5 18.6a8.5 2.6 0 0 0 17 0'),
    p('M3.5 18.6a8.5 2.6 0 0 1 4.9-2.36M20.5 18.6a8.5 2.6 0 0 0-4.9-2.36'),
    dot(17.6, 20.55, 1.1),
]

I['developers'] = [
    duo('M6.5 6h3.2v15H6.5z'),
    p('M6.5 21V6h3.2v15'),
    p('M6.5 11.5l3.2 3.2'),
    p('M2.8 6h18.4'),
    p('M8.1 6V2.6L3.4 6M8.1 2.6 19.8 6'),
    p('M3 6v2.8h3V6'),
    p('M16.8 6v4.2'),
    duo('M14.9 10.2h3.8v3.4h-3.8z'), p('M14.9 10.2h3.8v3.4h-3.8z'),
    p('M4 21h8.2'),
]

I['roi'] = [
    duo('M3.2 10.5a4.8 1.9 0 1 0 9.6 0a4.8 1.9 0 1 0-9.6 0z'),
    '<ellipse cx="8" cy="10.5" rx="4.8" ry="1.9"/>',
    p('M3.2 10.5v8c0 1.05 2.15 1.9 4.8 1.9s4.8-.85 4.8-1.9v-8'),
    p('M3.2 14.5c0 1.05 2.15 1.9 4.8 1.9s4.8-.85 4.8-1.9'),
    p('M18 20.5V4.2'), p('M14.6 7.6 18 4.2l3.4 3.4'),
]

CASE = 'M3 10a2.2 2.2 0 0 1 2.2-2.2h12.6A2.2 2.2 0 0 1 20 10v8.3a2.2 2.2 0 0 1-2.2 2.2H5.2A2.2 2.2 0 0 1 3 18.3z'
I['jobs'] = [
    duo('M2.5 11.2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v7.3a2 2 0 0 1-2 2h-8a2 2 0 0 1-2-2z'),
    p('M2.5 11.2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v7.3a2 2 0 0 1-2 2h-8a2 2 0 0 1-2-2z'),
    p('M6.3 9.2V7.8a1.3 1.3 0 0 1 1.3-1.3h1.8a1.3 1.3 0 0 1 1.3 1.3v1.4'),
    p('M2.5 14.2h12'),
    p('M17.6 9.8h3.9M17.6 13.6h3.9M17.6 17.4h2.4'),
    glyph(19.6, 4.6, 2.6),
]

CUP = 'M8 3.5h8v5.3a4 4 0 0 1-8 0z'
TROPHY = [
    duo(CUP), p(CUP),
    p('M8 5.3H6.3a1.85 1.85 0 0 0 0 3.7h2'),
    p('M16 5.3h1.7a1.85 1.85 0 0 1 0 3.7h-2'),
    p('M12 12.8V16'),
    p('M9.6 16h4.8l.9 4.5H8.7z'),
]
I['challenge'] = [
    duo_circ(12, 13.2, 7.6),
    p('M12.93 5.66A7.6 7.6 0 0 1 18.89 9.99M19.46 11.75A7.6 7.6 0 0 1 17.18 18.76M15.68 19.85A7.6 7.6 0 0 1 8.32 19.85M6.82 18.76A7.6 7.6 0 0 1 4.54 11.75M5.11 9.99A7.6 7.6 0 0 1 11.07 5.66'),
    p('M10 2.5h4M12 2.5v3'),
    glyph(12, 13.2, 3.6),
]

I['news'] = [
    p('M17.5 8.5h1.5a1.5 1.5 0 0 1 1.5 1.5v8a2.5 2.5 0 0 1-5 0V6A1.5 1.5 0 0 0 14 4.5H5A1.5 1.5 0 0 0 3.5 6v12A2.5 2.5 0 0 0 6 20.5h12'),
    duo('M6.5 8h5v4.5h-5z'), p('M6.5 8h5v4.5h-5z'),
    p('M6.5 15.8h6M6.5 18h4'),
]

I['guides'] = [
    duo('M12 6.5c1.7-1.3 4.5-2 9-1.7v13.5c-4.5-.3-7.3.4-9 1.7z'),
    p('M12 6.5C10.3 5.2 7.5 4.5 3 4.8v13.5c4.5-.3 7.3.4 9 1.7'),
    p('M12 6.5c1.7-1.3 4.5-2 9-1.7v13.5c-4.5-.3-7.3.4-9 1.7'),
    p('M12 6.5V20'),
    p('M5.6 9.4c1.3 0 2.4.2 3.6.6M5.6 12.8c1.3 0 2.4.2 3.6.6'),
    p('M14.8 15.4l1.9-3.1 1.8 1.2 1.2-3.4'),
    dot(14.8, 15.4, 1), dot(19.7, 10.1, 1.1),
]

WIN = 'M2.5 5a2 2 0 0 1 2-2h15a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2z'
I['website'] = [
    p(WIN), p('M2.5 7h19'), dot(5, 5, .8), dot(7.4, 5, .8),
    duo_circ(12, 14, 4.4), circ(12, 14, 4.4),
    '<ellipse cx="12" cy="14" rx="1.9" ry="4.4"/>', p('M7.6 14h8.8'),
]

I['enterprise'] = [
    duo('M3.5 21V5a1.5 1.5 0 0 1 1.5-1.5h6A1.5 1.5 0 0 1 12.5 5v16z'),
    p('M3.5 21V5a1.5 1.5 0 0 1 1.5-1.5h6A1.5 1.5 0 0 1 12.5 5v16'),
    p('M6.5 7.5h3M6.5 11h3M6.5 14.5h3'), p('M2.5 21h11'),
    p('M12.5 12 18 6.2M12.5 12h5.6M12.5 12l5.5 5.8'),
    dot(19.4, 5.4, 1.6), dot(19.8, 12, 1.6), dot(19.4, 18.6, 1.6),
]

BUB = 'M4.5 4h15A1.5 1.5 0 0 1 21 5.5v10a1.5 1.5 0 0 1-1.5 1.5h-9.7l-4.3 3.6V17h-1A1.5 1.5 0 0 1 3 15.5v-10A1.5 1.5 0 0 1 4.5 4z'
I['client-ai'] = [duo(BUB), p(BUB), glyph(12, 10.5, 4.3)]

MEGA = 'M3.5 10v4c0 .55.45 1 1 1H7l7.5 4.5v-15L7 9H4.5c-.55 0-1 .45-1 1z'
I['marketing'] = [
    duo(MEGA), p(MEGA),
    p('M7.3 15l1.4 5h2.4l-1.3-4.4'),
    p('M18 9.3l1.9-1.3M18.4 12h2.4M18 14.7l1.9 1.3'),
]

I['meta-ads'] = [
    circ(12, 12, 9.2),
    duo_circ(12, 12, 5.6),
    circ(12, 10.4, 1.7), p('M9.4 15.3a2.9 2.9 0 0 1 5.2 0'),
    dot(19.05, 6.09, 1.45), dot(3.36, 15.15, 1.45), dot(13.6, 21.06, 1.45),
]

I['listings'] = [
    duo('M8 8l6 3-6 3-6-3z'), p('M8 8l6 3-6 3-6-3z'),
    p('M2 14.5l6 3 6-3'), p('M2 18l6 3 6-3'),
    p('M14.8 9.2l5.7-5.7'), p('M15.8 3.5h4.7v4.7'),
]

TAG = 'M3 4.6V11a1.6 1.6 0 0 0 .47 1.13l8.4 8.4a1.6 1.6 0 0 0 2.26 0l6.4-6.4a1.6 1.6 0 0 0 0-2.26l-8.4-8.4A1.6 1.6 0 0 0 11 3H4.6A1.6 1.6 0 0 0 3 4.6z'
I['pricing'] = [duo(TAG), p(TAG), circ(7.6, 7.6, 1.5), p('M11.6 14.6l3.4-3.4')]

PLUG = 'M7.5 7.5h9v3.5a4.5 4.5 0 0 1-9 0z'
I['integrations'] = [
    duo(PLUG), p(PLUG), p('M10 3.5v4M14 3.5v4'),
    p('M12 15.5v2.3a2.7 2.7 0 0 0 2.7 2.7h3.3'), dot(19.6, 20.5, 1.3),
    p('M7.5 10.8H5'), dot(3.6, 10.8, 1.3), p('M16.5 10.8H19'), dot(20.4, 10.8, 1.3),
]

_g = (12, 12, 6.2)
def arc(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f'M{f(x0)} {f(y0)}A{f(r)} {f(r)} 0 {large} 1 {f(x1)} {f(y1)}'
I['broker-ai'] = [
    glyph_line(12, 12, 5.6),
    p(arc(12, 12, 9.2, -20, 200)),
    p(arc(12, 12, 9.2, 228, 302)),
    dot(12 + 9.2 * math.cos(math.radians(-49)), 12 + 9.2 * math.sin(math.radians(-49)), 1.5),
    dot(12 + 9.2 * math.cos(math.radians(214)), 12 + 9.2 * math.sin(math.radians(214)), .85),
]

I['data'] = [
    duo('M4 6a8 2.6 0 1 0 16 0a8 2.6 0 1 0-16 0z'),
    '<ellipse cx="12" cy="6" rx="8" ry="2.6"/>',
    p('M4 6v1.8c0 1.44 3.58 2.6 8 2.6s8-1.16 8-2.6V6'),
    p('M4 11.6v1.8c0 1.44 3.58 2.6 8 2.6s8-1.16 8-2.6v-1.8'),
    p('M4 17.2V19c0 1.44 3.58 2.6 8 2.6s8-1.16 8-2.6v-1.8'),
    dot(16.5, 8.3, .85),
]

FR = 'M3 9.5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'
I['examples'] = [
    p('M7 4.6V5.5M7 4.6a1.6 1.6 0 0 1 1.6-1.6H19.4A1.6 1.6 0 0 1 21 4.6v10.8a1.6 1.6 0 0 1-1.6 1.6h-.4'),
    duo(FR), p(FR),
    p('M3.4 17.6l3.8-3.9 3 3 1.9-1.9 3.6 3.6'), dot(12.7, 11.3, 1.25),
]

PILLARS = ['market', 'developers', 'roi', 'jobs', 'challenge', 'news', 'guides', 'website', 'enterprise',
           'client-ai', 'marketing', 'meta-ads', 'listings', 'pricing', 'integrations', 'broker-ai', 'data',
           'examples']

# ───────────────────────────── general ─────────────────────────────
I['search'] = [duo_circ(10.5, 10.5, 6.5), circ(10.5, 10.5, 6.5), p('M15.3 15.3 20.5 20.5')]
CL = 'M3 6.5A1.5 1.5 0 0 1 4.5 5h4A1.5 1.5 0 0 1 10 6.5v11A1.5 1.5 0 0 1 8.5 19h-4A1.5 1.5 0 0 1 3 17.5z'
CR = 'M14 6.5A1.5 1.5 0 0 1 15.5 5h4A1.5 1.5 0 0 1 21 6.5v11a1.5 1.5 0 0 1-1.5 1.5h-4a1.5 1.5 0 0 1-1.5-1.5z'
I['compare'] = [p('M4 8.5h14.5M15 5l3.5 3.5L15 12'), p('M20 15.5H5.5M9 12l-3.5 3.5L9 19'), dot(4, 8.5, 1.2), dot(20, 15.5, 1.2)]
DOC = 'M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z'
I['pdf'] = [duo(DOC), p(DOC), p('M14 3v5h5'), p('M8.5 12.5h7M8.5 15.5h7M8.5 18h4')]
I['calendar'] = [p('M3.5 7a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z'),
                 duo('M3.5 7a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2v2.5h-17z'),
                 p('M8 3v4M16 3v4M3.5 9.5h17'),
                 dot(8, 13.2, .95), dot(12, 13.2, .95), dot(8, 17, .95), dot(12, 17, .95), circ(16, 15.1, 1.6)]
I['clock'] = [duo_circ(12, 12, 9), circ(12, 12, 9), p('M12 7v5l3.3 2'), dot(12, 12, .9)]
PIN2 = 'M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z'
I['pin'] = [duo(PIN2), p(PIN2), circ(12, 10, 2.3)]
I['map'] = [duo('M8.5 4l7 2.5v13.5l-7-2.5z'), p('M3 6.5l5.5-2.5 7 2.5 5.5-2.5v13.5l-5.5 2.5-7-2.5L3 20z'),
            p('M8.5 4v13.5M15.5 6.5V20')]
I['plan'] = [p('M3.5 5a1.5 1.5 0 0 1 1.5-1.5h14A1.5 1.5 0 0 1 20.5 5v14a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 19z'),
             duo('M11 3.5h8A1.5 1.5 0 0 1 20.5 5v7H11z'),
             p('M11 3.5V9M11 12.5v8M11 12h2.5M17 12h3.5M3.5 13H7')]
I['bed'] = [p('M3 6v14M3 15.5h18M21 20v-6.5a2 2 0 0 0-2-2h-8.5v4'), duo('M10.5 11.5H19a2 2 0 0 1 2 2v2h-10.5z'),
            circ(6.8, 12.6, 1.8)]
I['area'] = [p('M3 8V4.5A1.5 1.5 0 0 1 4.5 3H8M16 3h3.5A1.5 1.5 0 0 1 21 4.5V8M21 16v3.5a1.5 1.5 0 0 1-1.5 1.5H16M8 21H4.5A1.5 1.5 0 0 1 3 19.5V16'),
             p('M8.5 15.5l7-7M11.5 8.5h4v4M8.5 11.5v4h4')]
I['filter'] = [p('M4 6h9M17.5 6H20M4 12h2.5M11 12h9M4 18h11M19.5 18h.5'),
               circ(15.2, 6, 2.2), circ(8.8, 12, 2.2), circ(17.2, 18, 2.2), duo_circ(8.8, 12, 2.2)]
I['check'] = [p('M5 12.5l4.5 4.5L19 7.5')]
I['check-circle'] = [duo_circ(12, 12, 9), circ(12, 12, 9), p('M8 12.3l2.8 2.8 5.2-5.4')]
I['close'] = [p('M6 6l12 12M18 6 6 18')]
I['arrow'] = [p('M4 12h16M14 6l6 6-6 6')]
I['arrow-up-right'] = [p('M7 17 17 7M8.5 7H17v8.5')]
I['external'] = [p('M18 13.5V19a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 4 19V8a1.5 1.5 0 0 1 1.5-1.5H11'),
                 p('M14 3.5h6.5V10M20.5 3.5 11 13')]
MSG = 'M4 5.5A1.5 1.5 0 0 1 5.5 4h13A1.5 1.5 0 0 1 20 5.5v9.5a1.5 1.5 0 0 1-1.5 1.5H9.3L5 20v-3.5h0A1 1 0 0 1 4 15.5z'
MSG = 'M5.5 4h13A1.5 1.5 0 0 1 20 5.5v9.5a1.5 1.5 0 0 1-1.5 1.5H9.3L5.5 19.8V16.5A1.5 1.5 0 0 1 4 15V5.5A1.5 1.5 0 0 1 5.5 4z'
I['message'] = [duo(MSG), p(MSG), p('M7.5 8.6h9M7.5 12h5.5')]
PH = 'M8.2 3.5H6A2 2 0 0 0 4 5.6C4.3 13.6 10.4 19.7 18.4 20a2 2 0 0 0 2.1-2v-2.2a1 1 0 0 0-.75-.97l-3.2-.8a1 1 0 0 0-.96.27l-1.4 1.4a12 12 0 0 1-5.5-5.5l1.4-1.4a1 1 0 0 0 .27-.96l-.8-3.2A1 1 0 0 0 8.2 3.5z'
I['phone'] = [duo(PH), p(PH)]
I['user'] = [duo_circ(12, 8, 3.7), circ(12, 8, 3.7), p('M4.5 20.5c.8-3.9 3.8-6 7.5-6s6.7 2.1 7.5 6')]
I['team'] = [duo_circ(12, 8.2, 3.1), circ(12, 8.2, 3.1), p('M6.5 19.8c.6-3.3 2.8-5.2 5.5-5.2s4.9 1.9 5.5 5.2'),
             circ(5.4, 9.8, 2.1), p('M2.4 17.4c.3-2 1.4-3.3 3-3.7'), circ(18.6, 9.8, 2.1), p('M21.6 17.4c-.3-2-1.4-3.3-3-3.7')]
SH = 'M12 3l7.5 3v5.5c0 4.6-3.1 8.3-7.5 9.5-4.4-1.2-7.5-4.9-7.5-9.5V6z'
I['shield'] = [duo(SH), p(SH), p('M8.8 12l2.2 2.2 4.2-4.4')]
I['lock'] = [duo('M5 12.5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z'),
             p('M5 12.5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z'),
             p('M8 10.5V7.5a4 4 0 0 1 8 0v3'), dot(12, 15, 1.2), p('M12 15.5v2')]
BOLT = 'M13.5 2.8 5 13.5h6.2l-.7 7.7L19 10.5h-6.2z'
I['bolt'] = [duo(BOLT), p(BOLT)]
I['sparkle'] = [glyph_line(10, 13.2, 7.2), glyph(18.6, 5.2, 2.9)]
I['chart-line'] = [p('M3.5 3.5v17h17'), duo('M7 15l3.5-4 3 2.5L19 7v13.5H7z'), p('M7 15l3.5-4 3 2.5L19 7'),
                   dot(10.5, 11, 1.05), dot(13.5, 13.5, 1.05), dot(19, 7, 1.25)]
I['chart-bar'] = [p('M3.5 20.5h17'), p('M5.5 13.8a.8.8 0 0 1 .8-.8h1.6a.8.8 0 0 1 .8.8v6.7h-3.2z'),
                  p('M10.4 9.3a.8.8 0 0 1 .8-.8h1.6a.8.8 0 0 1 .8.8v11.2h-3.2z'),
                  duo('M15.3 4.8a.8.8 0 0 1 .8-.8h1.6a.8.8 0 0 1 .8.8v15.7h-3.2z'),
                  p('M15.3 4.8a.8.8 0 0 1 .8-.8h1.6a.8.8 0 0 1 .8.8v15.7h-3.2z')]
I['trend-up'] = [p('M3 17l6-6 4 4 8-8'), p('M15 7h6v6'), dot(9, 11, 1.05), dot(13, 15, 1.05)]
WAL = 'M3.5 6.5v12a2 2 0 0 0 2 2h13a1.5 1.5 0 0 0 1.5-1.5V9a1.5 1.5 0 0 0-1.5-1.5h-13a2 2 0 0 1-2-2 2 2 0 0 1 2-2H17'
I['wallet'] = [duo('M3.5 6.5v12a2 2 0 0 0 2 2h13a1.5 1.5 0 0 0 1.5-1.5V9a1.5 1.5 0 0 0-1.5-1.5h-13a2 2 0 0 1-2-1z'),
               p(WAL), p('M20 11.5h-3.5a2 2 0 0 0 0 4H20'), dot(16.6, 13.5, .95)]
I['cash'] = [duo('M2.5 8a2 2 0 0 1 2-2h15a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2z'),
             p('M2.5 8a2 2 0 0 1 2-2h15a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2z'),
             circ(12, 12, 2.7), dot(6, 9.5, .95), dot(18, 14.5, .95)]
RIB = 'M2.5 9.5a2 2 0 0 1 2-2h15a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2z'
I['installments'] = [p('M15.5 5H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h5'), p('M17 9.2V7a2 2 0 0 0-2-2'), p('M3 9.5h11.5M7 3v4M13 3v4'),
                     dot(6.5, 13, .95), dot(10, 13, .95), dot(6.5, 16.2, .95),
                     duo_circ(16.8, 16.2, 4.7), circ(16.8, 16.2, 4.7), circ(16.8, 16.2, 1.9)]
I['key'] = [duo_circ(8, 15.5, 4.5), circ(8, 15.5, 4.5), p('M11.2 12.3 20 3.5M16.6 6.9l2.4 2.4M14.3 9.2l1.7 1.7'),
            dot(8, 15.5, 1.1)]
I['building'] = [duo('M15 9.5h3a1.5 1.5 0 0 1 1.5 1.5v10H15z'),
                 p('M5 21V5a1.5 1.5 0 0 1 1.5-1.5h7A1.5 1.5 0 0 1 15 5v16'),
                 p('M15 9.5h3a1.5 1.5 0 0 1 1.5 1.5v10'), p('M3 21h18'),
                 p('M8 7.5h3M8 11h3M8 14.5h3'), p('M9.5 21v-3')]
I['handshake'] = [
    duo('M2.5 9.4 5.1 8.5l2.3 7.2-2.6.9z'), p('M2.5 9.4 5.1 8.5l2.3 7.2-2.6.9z'),
    duo('M21.5 9.4l-2.6-.9-2.3 7.2 2.6.9z'), p('M21.5 9.4l-2.6-.9-2.3 7.2 2.6.9z'),
    p('M18 9.4 14.4 8.3a2.4 2.4 0 0 0-1.9.3L9.1 10.8a1.3 1.3 0 0 0 1.2 2.3l2.6-1.1 3.6 3.3'),
    p('M6.9 14.9l3.5 3.2a1.3 1.3 0 0 0 1.8 0l3.9-3.6'),
]
FLAG = 'M5 4.5h11.5l-2.5 4 2.5 4H5'
I['flag'] = [duo(FLAG + 'z'), p(FLAG), p('M5 21V3.5')]
BELL = 'M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15z'
I['bell'] = [duo(BELL), p(BELL), p('M10 21a2.2 2.2 0 0 0 4 0'), dot(18.8, 4.8, 1.7)]
I['live'] = [dot(12, 12, 2.1),
             p('M8.46 8.46a5 5 0 0 0 0 7.08M15.54 8.46a5 5 0 0 1 0 7.08'),
             p('M5.64 5.64a9 9 0 0 0 0 12.72M18.36 5.64a9 9 0 0 1 0 12.72')]
I['globe'] = [duo_circ(12, 12, 9), circ(12, 12, 9), '<ellipse cx="12" cy="12" rx="3.8" ry="9"/>', p('M3 12h18')]
I['link'] = [p('M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1.2 1.2'),
             p('M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1.2-1.2')]
I['api'] = [p('M7.5 6.5 2.5 12l5 5.5M16.5 6.5l5 5.5-5 5.5'), p('M9.6 12h4.8'), dot(9.2, 12, 1.25), dot(14.8, 12, 1.25)]
I['sync'] = [p('M19.5 10A7.8 7.8 0 0 0 5.6 7.2L4 9'), p('M4 4.8V9h4.2'),
             p('M4.5 14a7.8 7.8 0 0 0 13.9 2.8L20 15'), p('M20 19.2V15h-4.2')]
CLOUD = 'M7 18.5a4.5 4.5 0 0 1-.6-8.96 6 6 0 0 1 11.5 1.5 3.75 3.75 0 0 1-.65 7.46z'
I['cloud'] = [duo(CLOUD), p(CLOUD)]
I['play'] = [circ(12, 12, 9), duo('M10 8.4v7.2l6-3.6z'), p('M10 8.4v7.2l6-3.6z')]
I['timer'] = [duo_circ(12, 13.5, 7.5), circ(12, 13.5, 7.5), p('M10 2.8h4M12 2.8V6'), p('M12 13.5V9.6'),
              p('M18 7.4l1.4-1.4'), dot(12, 13.5, .9)]
I['question'] = [duo_circ(12, 12, 9), circ(12, 12, 9), p('M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.5'),
                 dot(12, 16.9, 1.05)]
I['trophy'] = TROPHY
I['medal'] = [p('M8.2 3 10.6 9M15.8 3l-2.4 6M8.2 3h7.6'), duo_circ(12, 15, 5.5), circ(12, 15, 5.5), glyph(12, 15, 2.6)]
I['target'] = [circ(12, 12, 9), circ(12, 12, 5.5), duo_circ(12, 12, 5.5), dot(12, 12, 1.6),
               p('M12 12 17.6 6.4'), p('M16.8 4.2v3h3')]
EYE = 'M2.5 12s3.5-6.5 9.5-6.5 9.5 6.5 9.5 6.5-3.5 6.5-9.5 6.5S2.5 12 2.5 12z'
I['eye'] = [duo(EYE), p(EYE), circ(12, 12, 3), dot(12, 12, 1)]
ST = star_d(12, 12.6, 9.6, 4.2)
I['star'] = [duo(ST), p(ST)]
I['layers'] = [duo('M12 3l9 4.5-9 4.5-9-4.5z'), p('M12 3l9 4.5-9 4.5-9-4.5z'), p('M3 12l9 4.5 9-4.5'), p('M3 16.5l9 4.5 9-4.5')]
I['grid'] = [p('M3.5 5A1.5 1.5 0 0 1 5 3.5h4A1.5 1.5 0 0 1 10.5 5v4A1.5 1.5 0 0 1 9 10.5H5A1.5 1.5 0 0 1 3.5 9z'),
             p('M13.5 5A1.5 1.5 0 0 1 15 3.5h4A1.5 1.5 0 0 1 20.5 5v4a1.5 1.5 0 0 1-1.5 1.5h-4A1.5 1.5 0 0 1 13.5 9z'),
             p('M3.5 15A1.5 1.5 0 0 1 5 13.5h4a1.5 1.5 0 0 1 1.5 1.5v4A1.5 1.5 0 0 1 9 20.5H5A1.5 1.5 0 0 1 3.5 19z'),
             duo('M13.5 15a1.5 1.5 0 0 1 1.5-1.5h4a1.5 1.5 0 0 1 1.5 1.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a1.5 1.5 0 0 1-1.5-1.5z'),
             p('M13.5 15a1.5 1.5 0 0 1 1.5-1.5h4a1.5 1.5 0 0 1 1.5 1.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a1.5 1.5 0 0 1-1.5-1.5z')]
I['route'] = [circ(6, 5.8, 2.3), p('M6 8.1v2.4a3 3 0 0 0 3 3h6a3 3 0 0 1 3 3v1.2'), duo_circ(18, 19.2, 2.3),
              circ(18, 19.2, 2.3)]
I['compass'] = [circ(12, 12, 9), duo('M15.8 8.2l-2 5.6-5.6 2 2-5.6z'), p('M15.8 8.2l-2 5.6-5.6 2 2-5.6z'), dot(12, 12, .9)]
SEND = 'M21 3l-6.5 18-4-7.5-7.5-4z'
I['send'] = [duo(SEND), p(SEND), p('M21 3 10.5 13.5')]
I['clipboard'] = [p('M8.5 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1.5'),
                  duo('M9 3.6a.6.6 0 0 1 .6-.6h4.8a.6.6 0 0 1 .6.6V6a.6.6 0 0 1-.6.6H9.6A.6.6 0 0 1 9 6z'),
                  p('M9 3.6a.6.6 0 0 1 .6-.6h4.8a.6.6 0 0 1 .6.6V6a.6.6 0 0 1-.6.6H9.6A.6.6 0 0 1 9 6z'),
                  p('M8.4 11.2l1.2 1.2 2-2.1M13.6 11.4h2.2M8.4 16l1.2 1.2 2-2.1M13.6 16.2h2.2')]
I['book'] = [duo('M5 5a2 2 0 0 1 2-2h12v15H7a2 2 0 0 0-2 1.5z'), p('M5 19.5V5a2 2 0 0 1 2-2h12v15H7a2 2 0 0 0-2 2 2 2 0 0 0 2 1H19v-3'),
             p('M9.5 7.5h5.5M9.5 10.5h3.5')]
BULB = 'M9 17v-1.2c0-1-.5-1.9-1.2-2.6A6 6 0 1 1 16.2 13.2c-.7.7-1.2 1.6-1.2 2.6V17z'
I['lightbulb'] = [duo(BULB), p(BULB), p('M9.6 20.2h4.8'), glyph(12, 9.4, 2.6)]
I['cpu'] = [p('M6 8a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z'),
            duo('M9.5 10.3a.8.8 0 0 1 .8-.8h3.4a.8.8 0 0 1 .8.8v3.4a.8.8 0 0 1-.8.8h-3.4a.8.8 0 0 1-.8-.8z'),
            p('M9.5 10.3a.8.8 0 0 1 .8-.8h3.4a.8.8 0 0 1 .8.8v3.4a.8.8 0 0 1-.8.8h-3.4a.8.8 0 0 1-.8-.8z'),
            p('M9.5 3v3M14.5 3v3M9.5 18v3M14.5 18v3M3 9.5h3M3 14.5h3M18 9.5h3M18 14.5h3')]
I['database'] = [duo('M4.5 5.5a7.5 2.5 0 1 0 15 0a7.5 2.5 0 1 0-15 0z'), '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.5"/>',
                 p('M4.5 5.5v13c0 1.38 3.36 2.5 7.5 2.5s7.5-1.12 7.5-2.5v-13'),
                 p('M4.5 12c0 1.38 3.36 2.5 7.5 2.5s7.5-1.12 7.5-2.5'), dot(16.3, 17.6, .9)]
I['feed'] = [dot(5.2, 18.8, 1.6), p('M4.5 11.5a8 8 0 0 1 8 8'), p('M4.5 4.5a15 15 0 0 1 15 15')]
I['briefcase'] = [duo(CASE), p(CASE),
                  p('M8.8 7.8V6.2a1.5 1.5 0 0 1 1.5-1.5h2.4a1.5 1.5 0 0 1 1.5 1.5v1.6'),
                  p('M3 13.4h17')]
# re-centre briefcase on 12 (CASE spans 3..20)
I['briefcase'] = [f'<g transform="translate(.5 0)">' + ''.join(I['briefcase']) + '</g>']
PAD = 'M7.5 7h9a4.5 4.5 0 0 1 4.4 3.6l.9 4.8a2.6 2.6 0 0 1-4.5 2.2L15.6 16H8.4l-1.7 1.6a2.6 2.6 0 0 1-4.5-2.2l.9-4.8A4.5 4.5 0 0 1 7.5 7z'
I['gamepad'] = [duo(PAD), p(PAD), p('M7.8 9.8v3.6M6 11.6h3.6'), dot(15.6, 10.6, 1), dot(17.6, 12.6, 1)]
CROWN = 'M4.2 18 3 8l5 3.8 4-6.3 4 6.3L21 8l-1.2 10z'
I['crown'] = [duo(CROWN), p(CROWN), p('M4.5 21h15')]
I['percent'] = [p('M19 5 5 19'), circ(7, 7, 2.5), circ(17, 17, 2.5), duo_circ(17, 17, 2.5)]
HOME = 'M5.5 9.3v10.2a1 1 0 0 0 1 1H10v-5.5h4v5.5h3.5a1 1 0 0 0 1-1V9.3'
I['home'] = [duo('M5.5 9.3 12 4l6.5 5.3v10.2a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1z'), p('M3.5 11 12 4l8.5 7'), p(HOME)]
WA = 'M6 3.5h12A2.5 2.5 0 0 1 20.5 6v9a2.5 2.5 0 0 1-2.5 2.5h-2.2l.8 3.2-4.4-3.2H6A2.5 2.5 0 0 1 3.5 15V6A2.5 2.5 0 0 1 6 3.5z'
HS = 'M9.6 7.2h-.9a.9.9 0 0 0-.9.95c.2 3.2 2.6 5.6 5.8 5.8a.9.9 0 0 0 .95-.9v-.9a.6.6 0 0 0-.42-.57l-1.2-.4a.6.6 0 0 0-.6.15l-.5.5a4.4 4.4 0 0 1-1.9-1.9l.5-.5a.6.6 0 0 0 .15-.6l-.4-1.2a.6.6 0 0 0-.58-.43z'
I['whatsapp-like'] = [duo(WA), p(WA), p(HS)]
ROCKET = 'M12 2.8c3 2 4.5 5.2 4.5 9V16h-9v-4.2c0-3.8 1.5-7 4.5-9z'
I['launch'] = [duo(ROCKET), p(ROCKET), circ(12, 9.5, 1.6), p('M7.5 12.8 5 15.3V19l2.5-1.6M16.5 12.8l2.5 2.5V19l-2.5-1.6'),
               p('M10.5 19l1.5 2.4 1.5-2.4')]
I['radar'] = [circ(12, 12, 9), circ(12, 12, 5), duo('M12 12V3a9 9 0 0 1 6.36 2.64z'),
              p('M12 12l6.36-6.36'), dot(12, 12, 1.15), dot(8.2, 9.2, 1.05), dot(15.6, 15.8, 1.05)]
_o = (12, 12, 10, 4.7, -25)
I['orbit'] = [duo_circ(12, 12, 2.3), circ(12, 12, 2.3), p(orbit_d(*_o)), dot(*orbit_point(*_o, 210), 1.4),
              dot(*orbit_point(*_o, 40), .9)]
I['qr'] = [p('M3.5 4.7a1.2 1.2 0 0 1 1.2-1.2h3.6a1.2 1.2 0 0 1 1.2 1.2v3.6a1.2 1.2 0 0 1-1.2 1.2H4.7a1.2 1.2 0 0 1-1.2-1.2z'),
           p('M14.5 4.7a1.2 1.2 0 0 1 1.2-1.2h3.6a1.2 1.2 0 0 1 1.2 1.2v3.6a1.2 1.2 0 0 1-1.2 1.2h-3.6a1.2 1.2 0 0 1-1.2-1.2z'),
           p('M3.5 15.7a1.2 1.2 0 0 1 1.2-1.2h3.6a1.2 1.2 0 0 1 1.2 1.2v3.6a1.2 1.2 0 0 1-1.2 1.2H4.7a1.2 1.2 0 0 1-1.2-1.2z'),
           dot(6.5, 6.5, 1.1), dot(17.5, 6.5, 1.1), dot(6.5, 17.5, 1.1),
           dot(15.3, 15.3, 1.05), dot(19.7, 15.3, 1.05), dot(17.5, 17.5, 1.05), dot(15.3, 19.7, 1.05), dot(19.7, 19.7, 1.05),
           dot(12, 5, .9), dot(12, 12, .9), dot(5, 12, .9), dot(19, 12, .9)]
I['download'] = [p('M12 3.5v11M7.5 10l4.5 4.5 4.5-4.5'), p('M4 15.5v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3')]
I['upload'] = [p('M12 14.5v-11M7.5 8 12 3.5 16.5 8'), p('M4 15.5v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3')]
PAL = 'M12 3a9 9 0 0 0 0 18c1.1 0 1.8-.8 1.8-1.8 0-.5-.2-.9-.5-1.3-.3-.3-.5-.8-.5-1.2 0-1 .8-1.8 1.8-1.8H17a4 4 0 0 0 4-4C21 6.6 17 3 12 3z'
I['palette'] = [duo(PAL), p(PAL), dot(7.4, 11.4, 1.25), dot(9.2, 7.3, 1.25), dot(14, 6.8, 1.25), dot(17, 10.2, 1.25)]
I['domain'] = [duo_circ(9, 9, 6), circ(9, 9, 6), '<ellipse cx="9" cy="9" rx="2.5" ry="6"/>', p('M3 9h12'),
               duo('M13.5 17a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1.5a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2z'),
               p('M13.5 17a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1.5a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2z'), p('M16.2 17.75h3')]
I['ai-glyph'] = [glyph(12, 12, 9.5)]

REQUIRED = PILLARS + '''search compare pdf calendar clock pin map plan bed area filter check check-circle close arrow arrow-up-right
external message phone user team shield lock bolt sparkle chart-line chart-bar trend-up wallet cash installments key building
handshake flag bell live globe link api sync cloud play timer question trophy medal target eye star layers grid route compass send
clipboard book lightbulb cpu database feed briefcase gamepad crown percent home whatsapp-like launch radar orbit qr download upload
palette domain ai-glyph'''.split()

TITLES = {}

def build():
    missing = [k for k in REQUIRED if k not in I]
    extra = [k for k in I if k not in REQUIRED]
    assert not missing, missing
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">',
           '<!-- Estavo Signal icon sprite · 24px grid · 1.6 stroke · currentColor · optional duotone layer (CSS custom properties fx-duo, fx-duo-o).',
           '     Generated by tools/fx_art/icons/build_icons.py (hand-tuned geometry). Usage: svg.fx-ico[aria-hidden] > use[href="assets/img/icons/estavo-fx.svg#i-jobs"] -->']
    for k in REQUIRED + extra:
        body = ''.join(x for x in I[k] if 'opacity="0"' not in x)
        out.append(f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
                   f'stroke-linecap="round" stroke-linejoin="round">{body}</symbol>')
    out.append('</svg>\n')
    os.makedirs(f'{REPO}/assets/img/icons', exist_ok=True)
    with open(f'{REPO}/assets/img/icons/estavo-fx.svg', 'w') as fh:
        fh.write('\n'.join(out))
    return REQUIRED + extra


def lab(ids):
    use = lambda i: f'<svg aria-hidden="true"><use href="../assets/img/icons/estavo-fx.svg#i-{i}"/></svg>'
    cells = ''.join(
        f'<div class="cell{" pillar" if i in PILLARS else ""}"><div class="row">'
        f'<span class="s24">{use(i)}</span><span class="s48">{use(i)}</span>'
        f'<span class="s24 dk">{use(i)}</span><span class="s48 dk">{use(i)}</span></div>'
        f'<code>{i}</code></div>' for i in ids)
    orbs = ''.join(f'<div class="orbcell"><span class="orb{" amber" if i=="challenge" else ""}{" mint" if i in ("roi","guides") else ""}{" cyan" if i in ("broker-ai","news","client-ai") else ""}">{use(i)}</span><code>{i}</code></div>' for i in PILLARS)
    kl = '<svg class="kl" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="2"/><circle cx="12" cy="12" r="10"/><rect x="4" y="4" width="16" height="16"/></svg>'
    zoom = ''.join('<div class="zgroup">' + ''.join(f'<div class="z">{kl}{use(i)}<code>{i}</code></div>' for i in ids[g:g+12]) + '</div>' for g in range(0, len(ids), 12))
    orbs_light = ''.join(f'<span class="orb light">{use(i)}</span>' for i in PILLARS)
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FX icon lab</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap">
<style>
:root{{--paper:#fafcff;--ink:#0f2236;--deep:#0b2239;--void:#050f1e;--blue:#163e69;--el:#4f9cf0;--cy:#7fdcff;--mint:#72e0bb;--amber:#f6b955}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:14px/1.4 Cairo,system-ui,sans-serif;padding:24px 28px}}
h1{{font-size:20px;margin:0 0 4px}}h2{{font-size:15px;margin:28px 0 10px;color:var(--blue)}}
.grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}}
.cell{{border:1px solid #e3ebf5;border-radius:12px;padding:8px 8px 6px;background:#fff}}
.cell.pillar{{border-color:#bcd5f2}}
.row{{display:grid;grid-template-columns:1fr 1.6fr 1fr 1.6fr;align-items:center;gap:0;border-radius:8px;overflow:hidden}}
.row span{{display:grid;place-items:center;height:62px;color:var(--blue);--fx-duo:var(--el);--fx-duo-o:.16}}
.row .dk{{background:var(--deep);color:#fff;--fx-duo:var(--cy);--fx-duo-o:.22}}
.s24 svg{{width:24px;height:24px}}.s48 svg{{width:48px;height:48px}}
code{{display:block;font:600 11px/1.6 ui-monospace,Menlo,monospace;color:#40607f;margin-top:4px;text-align:center}}
.orbs{{display:grid;grid-template-columns:repeat(9,1fr);gap:14px;background:radial-gradient(120% 140% at 20% 0%,#163e69 0%,var(--deep) 45%,var(--void) 100%);padding:26px;border-radius:24px}}
.orbcell{{display:grid;justify-items:center;gap:6px}}.orbcell code{{color:rgb(214 228 245/.76)}}
.orb{{--acc:var(--el);position:relative;width:64px;height:64px;border-radius:20px;display:grid;place-items:center;color:#fff;
 background:radial-gradient(70% 70% at 50% 30%,color-mix(in oklab,var(--acc) 26%,transparent),transparent 70%),linear-gradient(180deg,#12304f,#081a2e);
 box-shadow:inset 0 1px 0 rgb(255 255 255/.14),0 0 0 1px rgb(127 220 255/.06),0 10px 30px -8px color-mix(in oklab,var(--acc) 45%,transparent);
 --fx-duo:var(--acc);--fx-duo-o:.32}}
.orb::before{{content:"";position:absolute;inset:0;border-radius:inherit;padding:1.25px;background:conic-gradient(from 210deg,transparent 0 12%,var(--acc) 28%,#7fdcff 40%,transparent 58%,rgb(255 255 255/.18) 80%,transparent);
 -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}}
.orb svg{{width:28px;height:28px;position:relative;filter:drop-shadow(0 0 6px color-mix(in oklab,var(--acc) 70%,transparent))}}
.orb.amber{{--acc:var(--amber)}}.orb.mint{{--acc:var(--mint)}}.orb.cyan{{--acc:var(--cy)}}
.orb.light{{background:radial-gradient(70% 70% at 50% 25%,#ffffff,#eef5fd);color:var(--blue);box-shadow:inset 0 1px 0 #fff,0 8px 22px -10px rgb(22 62 105/.45),0 1px 2px rgb(22 62 105/.12);--fx-duo:var(--el);--fx-duo-o:.2}}
.orb.light svg{{filter:none}}
.zgroup{{display:grid;grid-template-columns:repeat(12,1fr);gap:6px;margin-bottom:6px;background:#fff;padding:6px}}
.z{{position:relative;display:grid;justify-items:center;padding-top:4px;color:var(--ink);--fx-duo:var(--el);--fx-duo-o:.16}}
.z>svg{{width:96px;height:96px;position:relative;z-index:1}}.z>svg.kl{{z-index:0}}.z .kl{{position:absolute;top:4px;left:50%;translate:-50% 0;fill:none;stroke:#e6403a;stroke-width:.08;opacity:.5;
 background-image:linear-gradient(#eef3fa 1px,transparent 1px),linear-gradient(90deg,#eef3fa 1px,transparent 1px);background-size:4px 4px}}
.lightrow{{display:flex;flex-wrap:wrap;gap:14px;padding:20px 0}}
.big{{display:flex;flex-wrap:wrap;gap:18px;color:var(--ink);--fx-duo:var(--el);--fx-duo-o:.16}}.big svg{{width:96px;height:96px}}
.inline{{font-size:16px;display:flex;flex-wrap:wrap;gap:6px 22px;color:var(--ink)}}.inline span{{display:inline-flex;align-items:center;gap:8px}}.inline svg{{width:20px;height:20px;color:var(--blue)}}
</style></head><body>
<h1>Estavo Signal · icon sprite ({len(ids)} icons)</h1><div>Each cell: 24px / 48px on paper, 24px / 48px on navy. Pillars outlined in blue.</div>
<h2>Pillar orb tiles (dark)</h2><div class="orbs">{orbs}</div>
<h2>Pillar orb tiles (paper)</h2><div class="lightrow">{orbs_light}</div>
<h2>All icons</h2><div class="grid">{cells}</div>
<h2>Zoom 72px on 24-grid (keylines)</h2>{zoom}<h2>Inline with text (20px)</h2><div class="inline">{''.join(f'<span>{use(i)}<span>{i}</span></span>' for i in ids[:30])}</div>
<h2>Pillars at 96px (grid check)</h2><div class="big">{''.join(use(i) for i in PILLARS)}</div>
</body></html>'''
    os.makedirs(f'{REPO}/.fx-lab', exist_ok=True)
    with open(f'{REPO}/.fx-lab/icons.html', 'w') as fh:
        fh.write(html)


if __name__ == '__main__':
    ids = build()
    lab(ids)
    print(len(ids), 'icons', os.path.getsize(f'{REPO}/assets/img/icons/estavo-fx.svg'), 'bytes')
