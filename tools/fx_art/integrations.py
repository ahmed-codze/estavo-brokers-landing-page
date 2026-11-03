"""Data integrations — "data pipeline". The Estavo data core (a block wearing the mark) feeds
glowing pipes through an API gate into three partner platforms: a website, a search app and a
listings/CRM view. Anchors: core, api, site, app, crm.
"""
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, WHITE, frag_browser, frag_project, frag_search, g, glow, iso_block, mark, node, orb,
                 orbit, ping)


def draw(c, rtl):
    backdrop(c, seed=71)
    s = -1 if rtl else 1
    core_x = 600 - s * 330
    # data core: stacked strata blocks
    for i in range(4):
        b = iso_block(c, (core_x, 640 - i * 46), -70, -70, 0, 140, 140, 34,
                      top=['#2a5f97', '#2f6aa7', '#3577b8', '#4f9cf0'][i], left='#123a63', right='#0d2c4d')
        c.add(c.intro(b, 'rise', .1 + .1 * i))
    c.add(c.intro(g(glow(c, core_x, 470, 120, 50, CYAN, .5), mark(c, core_x - 50, 440, 100)), 'drop', .6))
    c.add(ping(c, core_x, 650, 190, 60, CYAN, 1.2, 4))
    c.anchor('core', core_x, 720, kind='label', side='below')
    # API gate
    gx, gy = 600, 460
    c.add(c.intro(g(orbit(c, gx, gy, 70, 70, color=CYAN, width=1.4, opacity=.8, ticks=36, glow=True),
                    orb(c, gx, gy, 30, 'api', CYAN)), 'pop', .9))
    c.anchor('api', gx, gy + 92, kind='label', side='below')
    c.add(link(c, (core_x + s * 80, 520), (gx - s * 72, gy), ELEC, CYAN, draw=1, comet=True))
    # partners
    px = 600 + s * 330
    parts = [(px, 220, frag_browser, 'website', 'site'), (px + s * 40, 450, frag_search, 'search', 'app'),
             (px, 680, lambda c_, x, y, w, h: frag_project(c_, x, y, w, h, '8.0M', '158', '3'), 'listings', 'crm')]
    for i, (x, y, fr, ic, key) in enumerate(parts):
        c.add(link(c, (gx + s * 72, gy), (x - s * 135, y), CYAN, MINT, draw=1.4 + .15 * i, comet=i == 0, delay=-1))
        pl, om, geo = plate(c, x, y, 250, 160, fr, ic, ELEC, .95, 'left' if not rtl else 'right', 0, rtl, 1.3 + .2 * i)
        c.add(pl, om)
        c.anchor(key, x, geo['top'] - 18, kind='label', side='above')


def scenes():
    return twins(draw)
