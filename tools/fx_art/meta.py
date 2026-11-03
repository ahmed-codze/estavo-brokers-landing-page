"""Meta connection — "signal to audience". Website events leave the broker's site plate as
pulses and travel to an audience ring of people nodes (the broker's own ad account).
No performance numbers. Anchors: site, events, audience.
"""
import math
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, frag_browser, g, glow, node, orb, orbit, ping, spin_ring)


def draw(c, rtl):
    backdrop(c, seed=151)
    s = -1 if rtl else 1
    px = 600 - s * 300
    pl, om, geo = plate(c, px, 420, 380, 270, frag_browser, 'website', ELEC, 1, 'right' if not rtl else 'left', 0, rtl, .2)
    c.add(pl, om)
    c.anchor('site', px, geo['top'] - 22, kind='label', side='above')
    ax, ay = 600 + s * 300, 500
    for r, op in ((160, .7), (110, .5), (60, .4)):
        c.add(orbit(c, ax, ay, r, r * .9, color=CYAN, width=1.1, opacity=op, glow=True))
    c.add(spin_ring(c, ax, ay, 190, k=.9, color=MINT, opacity=.5, dur=40))
    c.add(c.intro(orb(c, ax, ay, 32, 'meta-ads', CYAN), 'pop', .9))
    for i in range(8):
        a = math.radians(i * 45 + 20)
        c.add(c.intro(node(c, ax + 160 * math.cos(a), ay + 144 * math.sin(a), 4, MINT, 5), 'pop', 1.1 + .05 * i))
    c.add(ping(c, ax, ay, 200, 180, CYAN, 1, 4))
    c.anchor('audience', ax, ay + 200, kind='label', side='below')
    for i, dy in enumerate((-60, 0, 60)):
        c.add(link(c, (px + s * 200, 420 + dy), (ax - s * 160, ay + dy * .8), ELEC, CYAN, draw=.8 + .15 * i, comet=i == 1))
    c.anchor('events', 600, 380, kind='label', side='above')


def scenes():
    return twins(draw)
