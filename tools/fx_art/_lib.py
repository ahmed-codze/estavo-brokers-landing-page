"""Shared compositions for the page scenes (not a scene module itself: the runner skips _*.py).

Every page scene is 1200x900 (4:3, same stage ratio as home-deck) with an Arabic -rtl twin,
word-free; HTML labels are placed over the stage from assets/img/fx/anchors.json.
"""
from kit import (AMBER, CYAN, ELEC, MINT, WHITE, Bez, Scene, aurora, beam, comet_on, g, glow, holo_plate, node,
                 perspective_floor, stars)

W, H = 1200, 900


def backdrop(c, seed=5, floor=640, accent=ELEC, second=CYAN, avoid=None):
    """Local light + star field + perspective floor for a 1200x900 scene."""
    c.add(aurora(c, [(600, 430, 540, 380, accent, .24), (260, 220, 300, 220, second, .12),
                     (960, 260, 300, 220, ELEC, .12), (600, 820, 520, 120, accent, .18)]))
    c.add(stars(c, 0, 0, W, floor - 40, 44, seed=seed, twinkle=4, avoid=avoid))
    c.add(perspective_floor(c, 0, floor, W, H - floor, cols=22, rows=8, vy=floor - 260, opacity=.4))
    c.add(glow(c, 600, floor + 170, 460, 80, accent, .4))


def plate(c, cx, cy, w, h, frag, icon, accent=ELEC, s=1.0, port='top', skew=0, rtl=False, intro=.4, glint=False):
    pl, om, geo = holo_plate(c, cx, cy, w, h, frag, icon, accent, s, port, skew, rtl=rtl, intro=intro, glint=glint)
    return pl, om, geo


def link(c, a, b, color=ELEC, end=CYAN, bend=.5, vertical=False, draw=.9, comet=False, width=1.4, delay=0):
    """Beam between two points with a node at the end; optional travelling pulse."""
    (x0, y0), (x1, y1) = a, b
    if vertical:
        bz = Bez((x0, y0), (x0, y0 + (y1 - y0) * bend), (x1, y1 - (y1 - y0) * bend), (x1, y1))
    else:
        bz = Bez((x0, y0), (x0 + (x1 - x0) * bend, y0), (x1 - (x1 - x0) * bend, y1), (x1, y1))
    out = [beam(c, bz, color, width, end_color=end, a0=.85, a1=.95, draw=draw),
           c.intro(node(c, x1, y1, 2.6, end, 3.4), 'pop', draw + .8)]
    if comet:
        out.append(comet_on(c, bz, .5, color=end, size=.85, dur=3.4, delay=delay))
    return g(*out)


def twins(draw, name='hero', w=W, h=H):
    """Scene + Arabic twin."""
    return [Scene(name, w, h, lambda c: draw(c, False)), Scene(name + '-rtl', w, h, lambda c: draw(c, True))]
