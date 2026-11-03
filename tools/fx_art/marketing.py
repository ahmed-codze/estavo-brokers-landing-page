"""Buyers & marketing — "buyer trail". A buyer's path across the broker's website, drawn as a
glowing route on the floor: viewed project A, returned to project B twice, asked about
handover; the trail ends at a pre-call brief plate. No scores, no counts.
Anchors: a, b, ask, brief.
"""
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, Bez, beam, comet_on, frag_project, g, lines, glass, node, orb, ping)


def draw(c, rtl):
    backdrop(c, seed=141)
    s = -1 if rtl else 1
    X = lambda x: 600 + s * (x - 600)
    route = Bez((X(160), 760), (X(380), 600), (X(640), 820), (X(900), 640))
    c.add(beam(c, route, CYAN, 2.4, end_color=MINT, a0=.4, a1=1, draw=.3))
    c.add(comet_on(c, route, .6, color=MINT, size=1, dur=4))
    for i, t in enumerate((.12, .45, .75)):
        x, y = route.at(t)
        c.add(c.intro(node(c, x, y, 5, MINT if i == 1 else CYAN, 6), 'pop', .6 + .3 * i))
    c.add(ping(c, *route.at(.45), 50, 16, MINT, 1.2, 3.6))
    pa, oa, ga = plate(c, X(300), 330, 250, 160, lambda c_, x, y, w, h: frag_project(c_, x, y, w, h, '7.9M', '150', '3'),
                       'eye', ELEC, .85, 'bottom', 4 * s, rtl, .3)
    c.add(g(pa, oa, opacity='.8'))
    c.anchor('a', ga['cx'], ga['top'] - 20, kind='label', side='above')
    pb, ob, gb = plate(c, X(620), 300, 270, 170, lambda c_, x, y, w, h: frag_project(c_, x, y, w, h, '8.0M', '158', '3'),
                       'eye', MINT, .95, 'bottom', 0, rtl, .5, glint=True)
    c.add(pb, ob)
    c.anchor('b', gb['cx'], gb['top'] - 20, kind='label', side='above')
    for (px, py), t in (((X(300), 410), .12), ((X(620), 400), .45)):
        x, y = route.at(t)
        c.add(link(c, (px, py), (x, y), ELEC, CYAN, vertical=True, draw=1))
    c.add(c.intro(orb(c, X(760), 560, 24, 'question', CYAN), 'pop', 1.3))
    c.anchor('ask', X(760), 520, kind='label', side='above')
    brief = g(glass(c, X(940) - 130, 380, 260, 190, 16, MINT, 6, glint=False), lines(X(940) - 110, 420, [200, 160, 180, 120], h=6, gap=22))
    c.add(c.intro(brief, 'rise', 1.6))
    c.add(c.intro(orb(c, X(940), 380, 24, 'clipboard', MINT), 'pop', 1.9))
    c.anchor('brief', X(940), 600, kind='label', side='below')


def scenes():
    return twins(draw)
