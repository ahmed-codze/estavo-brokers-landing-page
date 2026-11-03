"""Market data — "data strata". Four glass strata stacked over a plinth (developers, projects,
unit types, areas), a scan plane sweeping through them, beaming to one current project record.
Anchors: l1..l4, record.
"""
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, el, frag_project, g, glow, iso_disc, orb, ping)

LAYERS = ['developers', 'building', 'plan', 'map']


def draw(c, rtl):
    backdrop(c, seed=101)
    s = -1 if rtl else 1
    cx = 600 - s * 200
    for i in range(4):
        y = 700 - i * 110
        c.add(c.intro(g(iso_disc(c, cx, y, 230, 72, 12, rim=CYAN if i == 3 else ELEC, rim_op=.6)), 'rise', .15 + .15 * i))
        c.add(c.intro(orb(c, cx - s * 260, y, 22, LAYERS[i], ELEC), 'pop', .5 + .15 * i))
        c.anchor(f'l{i + 1}', cx - s * 300, y, kind='label', side='inside', align='end' if not rtl else 'start')
    scan_cls = c.anim('animation:' + c.kf('scan', '0%{transform:translateY(0);opacity:0}15%{opacity:1}85%{opacity:1}100%{transform:translateY(-360px);opacity:0}') + ' 5s ease-in-out infinite')
    c.add(g(el('ellipse', cx=cx, cy=720, rx=250, ry=80, fill=c.rad([(0, CYAN, .0), (.8, CYAN, .18), (1, CYAN, .5)]), stroke=CYAN, stroke_width=1.2, stroke_opacity=.7), cls=scan_cls))
    c.add(ping(c, cx, 700, 260, 82, CYAN, 1, 4))
    rx = 600 + s * 300
    c.add(link(c, (cx + s * 230, 370), (rx - s * 150, 400), CYAN, MINT, draw=1.2, comet=True))
    pl, om, geo = plate(c, rx, 400, 300, 200, lambda c_, x, y, w, h: frag_project(c_, x, y, w, h, '8.0M', '158', '3'),
                        'building', MINT, 1, 'left' if not rtl else 'right', 0, rtl, 1.1)
    c.add(pl, om)
    c.anchor('record', rx, geo['top'] - 22, kind='label', side='above')


def scenes():
    return twins(draw)
