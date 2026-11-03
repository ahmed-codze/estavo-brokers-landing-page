"""Jobs — "radar feed". A radar disc on the floor sweeps source nodes (job sites, careers
pages); beams carry what it finds into a clean feed column of job plates.
Anchors: radar, s1..s4 (sources), feed, apply.
"""
import math
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, el, frag_jobs, g, glow, iso_disc, node, orb, orbit, ping, spin_ring)


def draw(c, rtl):
    backdrop(c, seed=41)
    rx_c = 420 if not rtl else 780
    ry_c = 600
    c.add(c.intro(iso_disc(c, rx_c, ry_c, 300, 102, 18), 'rise', .1))
    rings = [orbit(c, rx_c, ry_c, r, r * .34, color=CYAN, width=.9, opacity=.5, glow=False) for r in (90, 170, 250)]
    c.add(c.intro(g(*rings), 'fade', .3))
    # sweep wedge: a circular wedge rotating inside a group squashed onto the floor plane
    sweep_cls = c.anim('animation:' + c.kf('sweep', 'to{transform:rotate(360deg)}') + ' 6s linear infinite', origin='0px 0px')
    wedge = el('path', d='M0 0 L290 0 A290 290 0 0 1 205 205 Z',
               fill=c.rad([(0, CYAN, .05), (1, CYAN, .4)], 0, 0, 290, user=True))
    c.add(g(g(wedge, cls=sweep_cls), transform=f'translate({rx_c} {ry_c}) scale(1 .34)'))
    c.add(ping(c, rx_c, ry_c, 300, 102, CYAN, 1.2, 4))
    srcs = [(-200, -40, 'globe'), (-60, 70, 'building'), (150, -55, 'globe'), (220, 50, 'building')]
    feed_x = 900 if not rtl else 300
    for i, (dx, dy, ic) in enumerate(srcs):
        x, y = rx_c + dx, ry_c + dy
        c.add(c.intro(g(glow(c, x, y, 40, 14, CYAN, .5), orb(c, x, y - 34, 20, ic, ELEC), node(c, x, y, 3, CYAN)), 'pop', .5 + .12 * i))
        c.anchor(f's{i + 1}', x, y - 64, kind='label', side='above')
    # beams to the feed
    for i, (dx, dy, _) in enumerate(srcs):
        c.add(link(c, (rx_c + dx, ry_c + dy - 34), (feed_x + (-150 if not rtl else 150), 230 + i * 120), ELEC, CYAN,
                   draw=1 + .1 * i, comet=i == 1))
    for i in range(3):
        pl, om, geo = plate(c, feed_x, 240 + i * 160, 280, 130, frag_jobs, 'briefcase', ELEC if i else MINT,
                            1 - i * .06, 'left' if not rtl else 'right', 0, rtl, .9 + .2 * i)
        c.add(pl, om)
        if i == 0:
            c.anchor('feed', feed_x, geo['top'] - 22, kind='label', side='above')
    c.anchor('radar', rx_c, ry_c + 140, kind='label', side='below')
    c.anchor('apply', feed_x, 770, kind='label', side='below')


def scenes():
    return twins(draw)
