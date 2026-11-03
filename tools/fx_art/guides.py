"""Selling tips — "playbook". An open holo-book (two tilted glass pages) on a plinth; four step
orbs lift off it along an arc of light: find → compare → offer (PDF) → close.
Anchors: book, s1..s4.
"""
import math
from _lib import backdrop, link, twins
from kit import (CYAN, ELEC, MINT, Bez, beam, comet_on, g, glass, glow, lines, node, orb, plinth)

STEPS = ['search', 'compare', 'pdf', 'handshake']


def draw(c, rtl):
    backdrop(c, seed=81, accent=MINT)
    pm, geo = plinth(c, 600, 720, .85, pings=1)
    c.add(pm)
    # book: two pages tilted like an open book
    for side in (-1, 1):
        x = 600 + (0 if side > 0 else -250)
        page = g(glass(c, 0, 0, 250, 170, 12, MINT, 5, hud_corners=False),
                 lines(26, 30, [180, 150, 170, 120, 160, 90], h=5, gap=18),
                 transform=f'translate({x} 520) skewY({-12 * side}) ')
        c.add(c.intro(page, 'rise', .2 + (.1 if side > 0 else 0)))
    c.add(glow(c, 600, 600, 220, 60, MINT, .4))
    c.anchor('book', 600, 790, kind='label', side='below')
    pts = []
    for i in range(4):
        t = i / 3
        a = math.radians(205 - t * 230)
        x = 600 + math.cos(a) * 400
        y = 420 + math.sin(a) * -230
        if rtl:
            x = 1200 - x
        pts.append((x, y))
    arc = Bez((pts[0][0], pts[0][1] + 40), (pts[1][0], pts[1][1] - 60), (pts[2][0], pts[2][1] - 60), (pts[3][0], pts[3][1] + 40))
    c.add(beam(c, arc, MINT, 2, end_color=CYAN, a0=.6, a1=.9, draw=.6))
    c.add(comet_on(c, arc, .5, color=MINT, size=1, dur=4))
    for i, (x, y) in enumerate(pts):
        c.add(link(c, (600, 520), (x, y + 30), ELEC, CYAN, vertical=True, draw=.8 + .1 * i))
        c.add(c.intro(orb(c, x, y, 34, STEPS[i], MINT if i == 3 else ELEC), 'pop', 1 + .2 * i))
        c.anchor(f's{i + 1}', x, y + 60, kind='label', side='below')


def scenes():
    return twins(draw)
