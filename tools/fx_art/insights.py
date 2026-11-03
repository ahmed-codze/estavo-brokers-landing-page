"""Market news — "news stream". A live source pulse on the floor feeds a rising stream of news
plates along a timeline spine; launch plates branch off. Anchors: daily, launch, project, live.
"""
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, frag_launch, frag_news, frag_project, g, glow, iso_disc, node, orb, ping, Bez, beam,
                 comet_on, signal)


def draw(c, rtl):
    backdrop(c, seed=61, accent=CYAN)
    sx = 600
    c.add(c.intro(iso_disc(c, sx, 760, 130, 42, 14), 'rise', .1))
    c.add(ping(c, sx, 756, 160, 52, CYAN, 1.2, 3.4))
    c.add(c.intro(orb(c, sx, 700, 28, 'live', MINT), 'pop', .3))
    c.anchor('live', sx, 800, kind='label', side='below')
    spine = Bez((sx, 670), (sx, 520), (sx, 300), (sx, 90))
    c.add(beam(c, spine, CYAN, 3, end_color=ELEC, a0=1, a1=.35, draw=.4))
    c.add(comet_on(c, spine, .4, color=MINT, size=1, dur=3))
    side = -1 if rtl else 1
    # main daily plate (big) + launch + project plates, alternating sides of the spine
    items = [(sx - side * 240, 560, frag_news, 'news', CYAN, 380, 230, 'daily'),
             (sx + side * 250, 380, lambda c_, x, y, w, h: frag_launch(c_, x, y, w, h, '2027'), 'launch', ELEC, 320, 180, 'launch'),
             (sx - side * 230, 200, lambda c_, x, y, w, h: frag_project(c_, x, y, w, h, '8.0M', '158', '3'), 'building', ELEC, 300, 170, 'project')]
    for i, (x, y, fr, ic, acc, w, h, key) in enumerate(items):
        port = 'right' if (x < sx) else 'left'
        c.add(link(c, (sx, y), (x + (w * .5 if x < sx else -w * .5) * (1 - i * .07), y), acc, acc, draw=.8 + .25 * i, width=2))
        pl, om, geo = plate(c, x, y, w, h, fr, ic, acc, 1 - i * .07, port, (4 if x < sx else -4), rtl, .6 + .25 * i, glint=i == 0)
        c.add(pl, om)
        c.anchor(key, x, geo['top'] - 20, kind='label', side='above')
        c.add(c.intro(node(c, sx, y, 4, CYAN, 5), 'pop', .7 + .25 * i))


def scenes():
    return twins(draw)
