"""Exclusive challenge — "arena". A round arena floor with 5 round pips, players around it
(one is Estavo AI), the question plate floating at the centre, the AI judge glyph above,
amber trophy light. Anchors: question, judge, round, p1..p5, ai.
"""
import math
from _lib import backdrop, link, plate, twins
from kit import (AMBER, CYAN, ELEC, WHITE, floating_glyph, frag_game, g, glow, iso_disc, light_column, node, orb,
                 orbit, ping, rays, spin_ring)


def draw(c, rtl):
    backdrop(c, seed=51, accent=AMBER, second=AMBER)
    cx, cy = 600, 650
    c.add(c.intro(g(iso_disc(c, cx, cy, 380, 120, 22, rim=AMBER), iso_disc(c, cx, cy - 6, 250, 80, 10, rim=AMBER)), 'rise', .1))
    c.add(spin_ring(c, cx, cy - 10, 320, k=.315, color=AMBER, dash='3 9', opacity=.7, dur=40))
    c.add(ping(c, cx, cy - 10, 380, 120, AMBER, 1.2, 4.5))
    # 5 round pips on the inner ring (3 done)
    for i in range(5):
        a = math.radians(200 + i * 35)
        x, y = cx + 200 * math.cos(a) * (-1 if rtl else 1), cy - 6 + 64 * math.sin(a) * -1
        col = AMBER if i < 3 else '#3a5a7d'
        c.add(c.intro(node(c, x, y + 30, 5 if i == 2 else 4, col, 5), 'pop', .5 + .08 * i))
    c.anchor('round', cx, cy + 105, kind='label', side='below')
    # players around
    players = [(-330, -10), (-200, 80), (0, 105), (200, 80), (330, -10)]
    for i, (dx, dy) in enumerate(players):
        x = cx + (dx if not rtl else -dx)
        y = cy + dy - 40
        ai = i == 4
        c.add(c.intro(g(glow(c, x, y + 40, 46, 14, CYAN if ai else AMBER, .45),
                        orb(c, x, y, 24, 'ai-glyph' if ai else 'user', CYAN if ai else AMBER)), 'pop', .7 + .1 * i))
        c.anchor('ai' if ai else f'p{i + 1}', x, y + 44, kind='label', side='below')
    # question plate + judge
    c.add(light_column(c, cx, cy - 20, 250, 420, 80, AMBER, .22, '#ffe2a8'))
    pl, om, geo = plate(c, cx, 410, 340, 210, frag_game, 'question', AMBER, 1.0, 'bottom', 0, rtl, .4)
    c.add(pl, om)
    c.anchor('question', cx, geo['top'] - 22, kind='label', side='above')
    c.add(rays(c, cx, 150, 30, 220, n=11, color=AMBER, op=.14, start=-170, end=-10))
    c.add(orbit(c, cx, 170, 120, 26, color=AMBER, width=1, opacity=.55, ticks=36))
    c.add(c.intro(floating_glyph(c, cx, 140, 70), 'drop', 1.2))
    c.anchor('judge', cx + (170 if not rtl else -170), 140, kind='label', side='inside')


def scenes():
    return twins(draw)
