"""Cash or installments — "payment ribbon" (direction-neutral: time runs left->right in both
languages, like every chart on the site).

A down-payment column then 12 quarterly installment columns marching away (fading with time);
a lens ring over the ribbon projects it down onto a shorter mint "value today" stack beside the
taller cash stack. Numbers = page example: 8.0M, 20% cash discount -> 6.4M; plan ~4.6M today.
Anchors: cash, today, down, plan, lens.
"""
from _lib import backdrop, link, plate, twins
from kit import (CYAN, ELEC, MINT, WHITE, frag_payment, g, glow, hud, iso_block, iso_grid, orbit, ping)


def draw(c, rtl):
    backdrop(c, seed=31, accent=MINT)
    c.add(iso_grid(c, 600, 640, 560, 150, step=36, opacity=.28, color=MINT))
    # ribbon: plan coords around origin (330, 560), s=.62
    o, s = (300, 600), .62
    dp = iso_block(c, o, 0, 0, 0, 70, 70, 190, top='#8af0cf', left='#2e9a7c', right='#23785f', s=s)
    c.add(c.intro(dp, 'rise', .2))
    for i in range(12):
        b = iso_block(c, o, 90 + i * 52, -i * 6, 0, 36, 36, 60, top='#5fd1ad' if i < 4 else '#3a9c86',
                      left='#1d5e55', right='#154a45', s=s)
        c.add(c.intro(g(b, opacity=f'{1 - i * .05:.2f}'), 'rise', .35 + .06 * i))
    c.anchor('down', 300, 430, kind='label', side='above')
    # lens over the ribbon
    lx, ly = 600, 300
    c.add(c.intro(g(glow(c, lx, ly, 170, 60, CYAN, .3),
                    orbit(c, lx, ly, 150, 44, color=CYAN, width=1.6, opacity=.85, ticks=48, tick_len=4),
                    orbit(c, lx, ly, 196, 58, color=MINT, width=.8, opacity=.4, dash='2 6', glow=False)), 'pop', 1.1))
    c.anchor('lens', lx, ly - 66, kind='label', side='above')
    # stacks: cash vs value today
    for x, h, top, left, right, val, col, key, d in ((840, 200, '#6a9fdc', '#1f4f86', '#173e6b', '6.4M', WHITE, 'cash', 1.5),
                                                       (990, 145, '#8af0cf', '#2e9a7c', '#23785f', '4.6M', MINT, 'today', 1.8)):
        blk = iso_block(c, (x, 720), -36, -36, 0, 72, 72, h, top=top, left=left, right=right, s=.9)
        top_y = 720 - h * .9 - 20
        parts = [blk, hud(c, val, x, top_y - 14, 20, col, 'middle')]
        if key == 'today':
            parts.insert(0, glow(c, x, 700, 110, 36, MINT, .5))
        c.add(c.intro(g(*parts), 'rise', d))
        c.anchor(key, x, top_y - 50, kind='label', side='above')
    c.add(ping(c, 990, 720, 90, 28, MINT, 1.2, 3.8))
    c.add(link(c, (lx + 150, ly), (990, 520), CYAN, MINT, bend=.6, draw=1.4, comet=True))
    pl, om, geo = plate(c, 290, 210, 280, 150, lambda c_, x, y, w, h: frag_payment(c_, x, y, w, h, '0.8M', 12),
                        'installments', MINT, .9, 'bottom', 0, False, .5)
    c.add(pl, om)
    c.anchor('plan', geo['cx'], geo['top'] - 20, kind='label', side='above')


def scenes():
    return twins(draw)
