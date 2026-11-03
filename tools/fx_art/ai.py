"""Client AI — "site assistant". The assistant plate on the broker's website answers a buyer;
buyer questions orbit it; beams pull answers only from the site's own listings (three
project plates behind). Anchors: assistant, q1..q3, inventory.
"""
import math
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, frag_chat, frag_project, g, orb, orbit)


def draw(c, rtl):
    backdrop(c, seed=131, accent=CYAN)
    s = -1 if rtl else 1
    for i, (dx, y, p) in enumerate(((-300, 230, '6.2M'), (0, 180, '8.0M'), (300, 230, '9.4M'))):
        pl, om, geo = plate(c, 600 + dx, y, 220, 140, lambda c_, a, b, w, h, pp=p: frag_project(c_, a, b, w, h, pp, '158', '3'),
                            'building', ELEC, .78, 'bottom', -dx / 60, rtl, .2 + .1 * i)
        c.add(g(pl, om, opacity='.85'))
        c.add(link(c, (600 + dx, y + 64), (600 + dx * .4, 470), ELEC, CYAN, vertical=True, draw=.8 + .1 * i, comet=i == 1))
        if i == 1:
            c.anchor('inventory', 600, geo['top'] - 22, kind='label', side='above')
    c.add(orbit(c, 600, 610, 420, 110, color=CYAN, width=1, opacity=.6, ticks=50))
    pl, om, geo = plate(c, 600, 610, 380, 260, frag_chat, 'client-ai', CYAN, 1, 'top', 0, rtl, .5, glint=True)
    c.add(pl, om)
    c.anchor('assistant', 600, geo['bottom'] + 26, kind='label', side='below')
    for i, a in enumerate((200, 330, 20)):
        x = 600 + 420 * math.cos(math.radians(a)) * s
        y = 610 + 110 * math.sin(math.radians(a))
        c.add(c.intro(orb(c, x, y, 22, 'message', MINT if i == 0 else ELEC), 'pop', 1 + .15 * i))
        c.anchor(f'q{i + 1}', x, y - 42, kind='label', side='above')


def scenes():
    return twins(draw)
