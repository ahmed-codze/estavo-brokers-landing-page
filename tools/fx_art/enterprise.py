"""For companies — "HQ and team". A company HQ (iso tower cluster) under the shared Estavo data
core; branch and agent nodes around it, each linked to the same core.
Anchors: hq, core, team.
"""
import math
from _lib import backdrop, link, twins
from kit import (CYAN, ELEC, MINT, floating_mark, g, glow, iso_block, iso_grid, node, orb, ping)


def draw(c, rtl):
    backdrop(c, seed=171)
    c.add(iso_grid(c, 600, 660, 560, 170, step=34, opacity=.34))
    blocks = [(-60, -40, 120, 230), (40, -10, 90, 170), (-110, 30, 80, 120), (60, 60, 70, 90)]
    for i, (x, y, w, h) in enumerate(blocks):
        c.add(c.intro(iso_block(c, (600, 650), x, y, 0, w * .6, w * .6, h, top='#4f9cf0' if i == 0 else '#2a5f97', s=1), 'rise', .2 + .1 * i))
    c.anchor('hq', 600, 760, kind='label', side='below')
    c.add(c.intro(g(glow(c, 600, 220, 160, 60, CYAN, .45), floating_mark(c, 600, 170, 130)), 'drop', .7))
    c.anchor('core', 600, 150, kind='label', side='above')
    c.add(link(c, (600, 260), (600, 420), CYAN, CYAN, vertical=True, draw=1, comet=True))
    for i in range(6):
        a = math.radians(200 + i * 28 if i < 3 else -20 - (i - 3) * 28)
        x = 600 + 430 * math.cos(math.radians([200, 160, 230, -20, 20, -50][i]))
        y = 560 + 170 * math.sin(math.radians([200, 160, 230, -20, 20, -50][i]))
        c.add(link(c, (600, 240), (x, y - 30), ELEC, MINT if i in (1, 4) else CYAN, bend=.5, draw=1.1 + .08 * i, width=1))
        c.add(c.intro(orb(c, x, y, 22, 'team' if i in (1, 4) else 'user', ELEC), 'pop', 1.3 + .08 * i))
    c.add(ping(c, 600, 650, 200, 60, CYAN, 1, 4))
    c.anchor('team', 600 + 430 * math.cos(math.radians(20)), 560 + 170 * math.sin(math.radians(20)) + 44, kind='label', side='below')


def scenes():
    return twins(draw)
