"""Estavo Market — "market map". An iso map grid with project pins (small towers), a search
plate, a comparison plate and a news plate hovering over the map, linked to their pins.
Anchors: search, compare, news, map.
"""
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, frag_compare, frag_news, frag_search, g, iso_block, iso_grid, node, ping, spin_ring)

PINS = [(330, 600, 70), (470, 660, 110), (610, 590, 90), (760, 650, 130), (880, 590, 80), (540, 720, 60), (700, 730, 100)]


def draw(c, rtl):
    backdrop(c, seed=91)
    c.add(iso_grid(c, 600, 650, 560, 170, step=34, opacity=.4))
    towers = []
    for i, (x, y, h) in enumerate(PINS):
        towers.append(c.intro(g(spin_ring(c, x, y, 22, color=CYAN, opacity=.4),
                                iso_block(c, (x, y), -10, -10, 0, 20, 20, h * .6, top='#4f9cf0' if i == 3 else '#2a5f97', s=1)), 'rise', .2 + .06 * i))
    c.add(*towers)
    c.add(ping(c, 760, 650, 60, 20, MINT, 1.2, 3.6))
    s = -1 if rtl else 1
    items = [(600 - s * 330, 260, frag_search, 'search', CYAN, 'search', (470, 600)),
             (600, 200, frag_compare, 'compare', MINT, 'compare', (760, 570)),
             (600 + s * 330, 260, frag_news, 'news', CYAN, 'news', (880, 540))]
    for i, (x, y, fr, ic, acc, key, tgt) in enumerate(items):
        tx, ty = tgt
        if rtl:
            tx = 1200 - tx
        c.add(link(c, (x, y + 80), (tx, ty), ELEC, acc, vertical=True, draw=1 + .15 * i, comet=i == 1))
        pl, om, geo = plate(c, x, y, 280, 170, fr, ic, acc, .95, 'bottom', 0, rtl, .5 + .2 * i)
        c.add(pl, om)
        c.anchor(key, x, geo['top'] - 20, kind='label', side='above')
    c.anchor('map', 600, 800, kind='label', side='below')


def scenes():
    return twins(draw)
