"""Estavo Sites — "site hologram". The broker's website projected as a large glass browser
plate over a plinth, with its building blocks on light rails around it: name & logo, colours,
domain, the site assistant, and the WhatsApp-style contact where the lead lands.
Anchors: site, brand, palette, domain, assistant, contact.
"""
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, frag_browser, frag_chat, g, glow, light_column, orb, plinth)


def draw(c, rtl):
    backdrop(c, seed=111)
    pm, geo = plinth(c, 600, 760, .95, pings=0)
    c.add(pm)
    c.add(light_column(c, 600, 750, 640, 360, 300, ELEC, .2))
    pl, om, g2 = plate(c, 600, 420, 520, 360, frag_browser, 'website', ELEC, 1, 'bottom', 0, rtl, .2, glint=True)
    c.add(pl, om)
    c.anchor('site', 600, g2['top'] - 22, kind='label', side='above')
    s = -1 if rtl else 1
    sats = [('brand', 'user', 600 - s * 420, 230, ELEC), ('palette', 'palette', 600 - s * 470, 430, ELEC),
            ('domain', 'domain', 600 - s * 420, 630, ELEC), ('contact', 'whatsapp-like', 600 + s * 430, 640, MINT)]
    for i, (key, ic, x, y, acc) in enumerate(sats):
        c.add(link(c, (x, y), (600 - (s if x * s < 600 * s else -s) * 262, y if 250 < y < 600 else (260 if y < 250 else 590)), acc, acc, draw=.9 + .1 * i, comet=key == 'contact'))
        c.add(c.intro(orb(c, x, y, 28, ic, acc), 'pop', .7 + .12 * i))
        c.anchor(key, x, y + 50, kind='label', side='below')
    pa, oa, ga = plate(c, 600 + s * 430, 330, 240, 170, frag_chat, 'client-ai', CYAN, .9, 'bottom', 0, rtl, 1.1)
    c.add(pa, oa)
    c.anchor('assistant', ga['cx'], ga['top'] - 20, kind='label', side='above')


def scenes():
    return twins(draw)
