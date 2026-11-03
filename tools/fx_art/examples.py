"""Examples — "site carousel". Five broker websites as glass browser plates on a carousel arc
over a ring floor, the front one lit. Anchors: front, left, right.
"""
import math
from _lib import backdrop, plate, twins
from kit import (CYAN, ELEC, frag_browser, g, orbit, spin_ring)


def draw(c, rtl):
    backdrop(c, seed=121)
    c.add(orbit(c, 600, 640, 470, 120, color=ELEC, width=1.2, opacity=.7, ticks=60))
    c.add(spin_ring(c, 600, 680, 400, k=.27, color=CYAN, opacity=.5, dur=50))
    slots = [(-2, .62, .5), (2, .62, .5), (-1, .8, .78), (1, .8, .78), (0, 1, 1)]
    for i, (k, s, dim) in enumerate(slots):
        x = 600 + k * 255
        y = 420 - (2 - abs(k)) * 18
        pl, om, geo = plate(c, x, y, 360, 250, frag_browser, 'website', ELEC, s, 'bottom', -k * 5, rtl, .2 + .12 * i, glint=k == 0)
        c.add(g(pl, om, opacity=f'{dim:.2f}') if dim < 1 else g(pl, om))
        if k == 0:
            c.anchor('front', x, geo['top'] - 22, kind='label', side='above')


def scenes():
    return twins(draw)
