"""Pricing — "three plinths". Three glowing plinths of increasing height, one per way to use
Estavo Sites (start free, grow with cities/AI, company), each crowned by its icon orb.
No prices inside the art. Anchors: t1, t2, t3.
"""
from _lib import backdrop, twins
from kit import (CYAN, ELEC, MINT, g, glow, iso_disc, light_column, orb, ping)


def draw(c, rtl):
    backdrop(c, seed=181)
    tiers = [(330, 1, 'website', MINT), (600, 2, 'bolt', CYAN), (870, 3, 'enterprise', ELEC)]
    if rtl:
        tiers = [(1200 - x, n, ic, a) for x, n, ic, a in tiers]
    for i, (x, n, ic, acc) in enumerate(tiers):
        base = 720
        parts = []
        for k in range(n):
            parts.append(iso_disc(c, x, base - k * 60 - 30, 130 - k * 14, 42 - k * 4, 30, rim=acc, rim_op=.7))
        top = base - n * 60
        parts.append(light_column(c, x, top + 10, top - 200, 160, 60, acc, .22))
        parts.append(glow(c, x, top, 120, 40, acc, .5))
        c.add(c.intro(g(*parts), 'rise', .2 + .2 * i))
        c.add(c.intro(orb(c, x, top - 110, 36, ic, acc), 'pop', .8 + .2 * i))
        c.anchor(f't{i + 1}', x, top - 170, kind='label', side='above')
    c.add(ping(c, tiers[1][0], 720, 150, 48, CYAN, 1.2, 4))


def scenes():
    return twins(draw)
