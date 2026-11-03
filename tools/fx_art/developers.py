"""Developers — "developer constellation".

One developer profile plate stands on a plinth in front; beams fan out behind it to the
developer's projects, each a project plate standing over a pin on an iso map grid, plus a
sales-contact orb and a news orb. Anchors: profile, p1..p4, contact, news.
"""
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, frag_developer, frag_project, g, iso_grid, node, orb, ping, plinth, spin_ring)

PROJECTS = [  # cx, cy, price, area, beds, scale, skew
    (250, 300, '6.2M', '142', '2', .86, 6),
    (470, 210, '8.0M', '158', '3', .8, 3),
    (730, 210, '9.4M', '176', '3', .8, -3),
    (950, 300, '11.8M', '210', '4', .86, -6),
]


def draw(c, rtl):
    backdrop(c, seed=11)
    c.add(iso_grid(c, 600, 560, 560, 150, step=36, opacity=.34))
    # pins under each project on the map grid
    pins = []
    for i, (x, y, *_r) in enumerate(PROJECTS):
        py = y + 190
        pins.append(g(spin_ring(c, x, py, 26, color=CYAN, opacity=.5), node(c, x, py, 3.2, CYAN, 4.2)))
        if i == 1:
            pins.append(ping(c, x, py, 36, 12, CYAN, 1, 4.2))
    c.add(c.intro(g(*pins), 'fade', .2))

    # plinth + developer profile plate
    pm, geo = plinth(c, 600, 700, .9, pings=0)
    c.add(pm)
    beams = []
    for i, (x, y, *_r) in enumerate(PROJECTS):
        beams.append(link(c, (600, 520), (x, y + 70), ELEC, CYAN, vertical=True, bend=.55, draw=.8 + .12 * i,
                          comet=i == 2, delay=-i))
    c.add(*beams)
    for i, (x, y, price, area, beds, s, sk) in enumerate(PROJECTS):
        pl, om, _ = plate(c, x, y, 220, 150, lambda c_, a, b, w, h, p=price, ar=area, bd=beds: frag_project(c_, a, b, w, h, p, ar, bd),
                          'building', ELEC, s, 'bottom', sk, rtl, .35 + .12 * i)
        c.add(pl, om)
        c.anchor(f'p{i + 1}', x, y - 150 * s / 2 - 18, kind='label', side='above')
    pl, om, geo = plate(c, 600, 560, 300, 200, frag_developer, 'developers', CYAN, 1.0, 'top', 0, rtl, .15, glint=True)
    c.add(pl, om)
    c.anchor('profile', 600, geo['bottom'] + 30, kind='label', side='below')
    # contact + news satellites
    for key, ic, x, y, acc in (('contact', 'phone', 300, 600, MINT), ('news', 'news', 900, 600, CYAN)):
        c.add(link(c, (600 + (1 if x > 600 else -1) * 150, 590), (x, y), acc, acc, draw=1.4))
        c.add(c.intro(orb(c, x, y, 26, ic, acc), 'pop', 1.6))
        c.anchor(key, x, y + 46, kind='label', side='below')


def scenes():
    return twins(draw)
