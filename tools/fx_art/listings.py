"""Your own listings — "publish to the network". The broker's unit plate on a plinth sends
beams out to broker nodes spread over the floor network.
Anchors: unit, network.
"""
import math
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, frag_project, g, iso_grid, node, orb, ping, plinth)


def draw(c, rtl):
    backdrop(c, seed=161)
    c.add(iso_grid(c, 600, 680, 580, 180, step=34, opacity=.34))
    pm, geo = plinth(c, 600, 640, .8, pings=1)
    c.add(pm)
    pl, om, g2 = plate(c, 600, 380, 340, 220, lambda c_, x, y, w, h: frag_project(c_, x, y, w, h, '8.0M', '158', '3'),
                       'listings', ELEC, 1, 'bottom', 0, rtl, .2, glint=True)
    c.add(pl, om)
    c.anchor('unit', 600, g2['top'] - 22, kind='label', side='above')
    for i in range(9):
        a = math.radians(-20 + i * 25 + 180 * (i % 2))
        r = 330 + (i % 3) * 60
        x, y = 600 + r * math.cos(math.radians(i * 40 + 10)), 690 + r * .3 * math.sin(math.radians(i * 40 + 10))
        c.add(link(c, (600, 650), (x, y), ELEC, CYAN if i % 3 else MINT, draw=.9 + .06 * i, comet=i == 4, width=1.1))
        c.add(c.intro(orb(c, x, y - 26, 16, 'user', ELEC), 'pop', 1.2 + .06 * i))
    c.anchor('network', 600, 840, kind='label', side='below')


def scenes():
    return twins(draw)
