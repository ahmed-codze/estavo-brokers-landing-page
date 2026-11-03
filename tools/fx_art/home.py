"""Homepage — "Command deck" (REFERENCE SCENE for every other page author).

Scenes (assets/img/fx/, each also as -still.svg; -rtl = Arabic, fragments mirrored)
  home-deck, home-deck-rtl                 1200x900  desktop hero for .fx-stage--hero
  home-deck-mobile, home-deck-mobile-rtl    390x480  phone composition: hub of 8 pillar
                                                     orbs + one featured Market record

Story: one Estavo core (the mark over a glowing plinth) feeds eight holo plates on its
orbit, one per pillar, each with its sprite icon docked on the core-facing edge (beams
end in it) and a tiny real product fragment. Example data = tools/data/home-fixture.json
(Project B: 8.0M, 1.2M down, 158 m2, 3 bedrooms, 2027; A/B/C prices 7.9 / 8.0 / 8.3).
Label the stage «مثال» / "Example" in HTML.

Label anchors (% of the art box; centre a .fx-stage__label on the point with
translate(-50%,-50%)). Back plates (website, challenge) take their label ABOVE, the rest
BELOW; all centred, so AR and EN share one geometry.
  home-deck(-rtl):  market 35.0/94.2 · broker-ai 65.0/94.2 · developers 13.8/75.7 ·
                    roi 86.2/75.7 · news 13.8/50.9 · jobs 86.2/50.9 ·
                    challenge 35.0/13.1 · website 65.0/13.1 · core 50.0/80.9 (optional)
  home-deck-mobile(-rtl): record 50.0/97.1 (under the featured plate) + one anchor per
                    orb (just below it) - on phones prefer only 'record'; the orbs read alone.
`python3 tools/build-fx-art.py home --list` prints the exact current numbers (also in
assets/img/fx/anchors.json).
"""
import math

from kit import (holo_plate, mirrored, glow, rays, particles, plinth, floating_mark, AMBER, CYAN, DEEP, ELEC, MINT, WHITE, Scene, ACCENT, aurora, beam, bar, comet,
                 comet_on, el, ellipse_d, ellipse_pt, f, frag_browser, frag_chat, frag_developer,
                 frag_game, frag_jobs, frag_news, frag_payment, frag_project, g, glass, iso_disc,
                 iso_grid, light_column, mark, MARK_H, MARK_W, node, orb, orbit, ping, signal,
                 spin_ring, stars, Bez, tr)

PW, PH, TH = 212, 138, 6          # plate size and slab thickness (local units)
PORT_R = 21                        # radius of the icon orb docked on the core-facing edge

# fragment box per port side (the orb intrudes on that edge)
BOX = {'top': (16, 28, PW - 32, PH - 42), 'bottom': (16, 14, PW - 32, PH - 42),
       'left': (28, 16, PW - 42, PH - 30), 'right': (14, 16, PW - 42, PH - 30)}
PORT = {'top': (PW / 2, 0), 'bottom': (PW / 2, PH + TH / 2), 'left': (0, PH / 2), 'right': (PW, PH / 2)}

FRAG = {
    'market': lambda c, x, y, w, h: frag_project(c, x, y, w, h, '8.0M', '158', '3', down=None),
    'broker-ai': lambda c, x, y, w, h: frag_chat(c, x, y, w, h),
    'developers': lambda c, x, y, w, h: frag_developer(c, x, y, w, h),
    'roi': lambda c, x, y, w, h: frag_payment(c, x + 4, y + 18, w - 8, h - 30),
    'news': lambda c, x, y, w, h: frag_news(c, x, y, w, h),
    'jobs': lambda c, x, y, w, h: frag_jobs(c, x, y, w, h),
    'challenge': lambda c, x, y, w, h: frag_game(c, x, y, w, h),
    'website': lambda c, x, y, w, h: frag_browser(c, x, y, w, h),
}
ICON = {'broker-ai': 'broker-ai', 'website': 'website', 'challenge': 'challenge'}


NO_MIRROR = {'roi'}  # charts keep their left-to-right time axis in Arabic too


def plate(c, key, cx, cy, s, port, skew=0, delay=0, dim=1.0, rtl=False, intro=None):
    """A pillar plate (kit.holo_plate) centred on (cx, cy). Returns (plate, port orb, geo).
    Only the featured Market plate carries the glass glint loop (loop budget)."""
    return holo_plate(c, cx, cy, PW, PH, FRAG[key], ICON.get(key, key), ACCENT.get(key, ELEC), s, port, skew,
                      port_r=PORT_R, delay=delay, dim=dim, thickness=TH, rtl=rtl and key not in NO_MIRROR,
                      glint=key == 'market', intro=intro)


# ── Desktop ────────────────────────────────────────────────────────────
CX = 600
RING = (600, 470, 470, 290)  # plate orbit (cx, cy, rx, ry)
TOP = (600, 548, 118, 39)    # top face of the plinth
MID = (600, 570, 156, 51)
BASE = (600, 594, 196, 64)

LAYOUT = [  # key, theta (deg from front, clockwise), scale, port side, skewY
    ('broker-ai', 22.5, 1.14, 'top', 4), ('roi', 67.5, 1.02, 'left', 7), ('jobs', 112.5, 1.0, 'left', 6),
    ('website', 157.5, .9, 'bottom', -3), ('challenge', 202.5, .9, 'bottom', 3), ('news', 247.5, 1.0, 'right', -6),
    ('developers', 292.5, 1.02, 'right', -7), ('market', 337.5, 1.14, 'top', -4),
]


def rim_pt(e, px, py):
    cx, cy, rx, ry = e
    a = math.atan2((py - cy) / ry, (px - cx) / rx)
    return cx + rx * math.cos(a), cy + ry * math.sin(a)


def draw_deck(c, rtl=False):
    rcx, rcy, rrx, rry = RING
    tcx, tcy, trx, try_ = TOP
    c.add(aurora(c, [(600, 400, 500, 360, ELEC, .30), (900, 200, 320, 210, CYAN, .12),
                     (300, 660, 320, 170, MINT, .07), (600, 610, 330, 95, ELEC, .38)]))
    c.add(stars(c, 0, 0, 1200, 900, 34, seed=11,
                avoid=lambda x, y: ((x - 600) / 330) ** 2 + ((y - 420) / 260) ** 2 < 1))
    c.add(iso_grid(c, 600, 618, 580, 250, step=50, k=.33, opacity=.55))

    c.add(orbit(c, 600, 482, 548, 350, rot=-6, width=.8, opacity=.32, dash='1 7', glow=False))
    c.add(orbit(c, rcx, rcy, rrx, rry, width=1.2, opacity=.6, ticks=32, tick_len=4))
    c.add(orbit(c, 600, 520, 330, 172, width=1, opacity=.45, dash='3 6', glow=False))

    # intro assembly order: core first, then front plates, sides, back plates (nearest first)
    order = {'market': 0, 'broker-ai': 0, 'developers': 1, 'roi': 1, 'news': 2, 'jobs': 2, 'challenge': 3, 'website': 3}
    plates = {}
    for i, (key, th, s, port, sk) in enumerate(LAYOUT):
        t = math.radians(th)
        px, py = rcx + rrx * math.sin(t), rcy + rry * math.cos(t)
        plates[key] = plate(c, key, px, py, s, port, sk, dim=.92 if port == 'bottom' else 1, rtl=rtl,
                            intro=.5 + .22 * order[key] + (.08 if px > CX else 0))

    behind, over = [], []          # beams drawn behind / in front of the core
    for i, (key, (mk, pm, geo)) in enumerate(plates.items()):
        ex, ey = geo['port']
        acc = geo['acc']
        sgn = 1 if ex > CX else -1
        lane = behind
        if ey < 320:               # back plates: rise from the top face, behind the mark
            sx, sy = rim_pt(TOP, ex, ey - 400)
            sx = 600 + sgn * 52
            sy = tcy - try_ * .62
            bz = Bez((sx, sy), (sx + sgn * 20, sy - 170), (ex, ey + 150), (ex, ey))
        elif ey < 640:             # side plates: from the mid tier rim, sweeping out
            sx, sy = rim_pt(MID, ex, ey + 40)
            bz = Bez((sx, sy), (sx + sgn * 120, sy + 6), (ex - sgn * 120, ey), (ex, ey))
            lane = over
        else:                      # front plates: from the base rim, dropping forward
            sx, sy = rim_pt(BASE, ex, ey + 260)
            bz = Bez((sx, sy), (sx + sgn * 20, sy + 40), (ex, ey - 70), (ex, ey))
            lane = over
        hue = acc if acc != ELEC else CYAN
        d0 = .35 + .22 * order[key]
        lane.append(beam(c, bz, ELEC, 1.5, end_color=hue, a0=.95, a1=.8, draw=d0))
        pulse = {'market': (4.0, 0), 'broker-ai': (4.4, -2.2), 'website': (4.8, -1.1)}.get(key)
        if pulse:  # three pulses, one per depth band (loop budget)
            lane.append(comet_on(c, bz, .6, color=hue, size=.9, dur=pulse[0], delay=pulse[1]))
        lane.append(c.intro(node(c, sx, sy, 2, CYAN, 3.5), 'pop', d0))
    c.add(g(*behind))
    for key in ('website', 'challenge'):
        c.add(plates[key][0], plates[key][1])

    # core: rays, plinth, light column with rising motes, floating mark
    c.add(rays(c, 600, 380, 60, 430, n=10, color=CYAN, op=.16, start=-170, end=-10))
    pl, _ = plinth(c, tcx, tcy, 1.0)
    c.add(pl)
    c.add(light_column(c, tcx, tcy, 236, 170, 104, ELEC, .34))
    c.add(particles(c, tcx, tcy - 6, 250, 120, n=5, seed=4))
    c.add(c.intro(floating_mark(c, 600, 318, 214), 'drop', .05))
    c.add(glow(c, 600, tcy - 2, 58, 12, WHITE, .55))

    c.add(g(*over))
    for key in ('jobs', 'news', 'roi', 'developers', 'broker-ai', 'market'):
        c.add(plates[key][0], plates[key][1])

    for key, (mk, pm, geo) in plates.items():
        if geo['cy'] < 300:
            c.anchor(key, geo['cx'], geo['top'] - 26, kind='label', side='above')
        else:
            c.anchor(key, geo['cx'], geo['bottom'] + 28, kind='label', side='below')


# ── Mobile ─────────────────────────────────────────────────────────────
M_ORDER = ['broker-ai', 'roi', 'jobs', 'website', 'challenge', 'news', 'developers', 'market']
M_C, M_R = (195, 196), 142   # upright halo ring (centre, radius)


def draw_mobile(c, rtl=False):
    """Phone: the Estavo mark floats inside an upright halo ring; the eight pillar orbs sit on
    the ring, each with room for a 12px HTML label directly under it; the Market orb feeds one
    featured project record below (the maintained data is the reason to trust Estavo)."""
    cx, cy = M_C
    c.add(aurora(c, [(195, 196, 200, 190, ELEC, .3), (320, 60, 110, 80, CYAN, .12), (80, 470, 150, 70, MINT, .07)]))
    c.add(stars(c, 0, 0, 390, 540, 34, seed=5, r=(.4, 1.1), avoid=lambda x, y: (x - cx) ** 2 + (y - cy) ** 2 < 175 ** 2))
    c.add(iso_grid(c, 195, 380, 220, 70, step=24, k=.33, opacity=.4))
    c.add(glow(c, cx, cy, 150, None, ELEC, .35))
    c.add(orbit(c, cx, cy, M_R, M_R, width=1.2, opacity=.62, ticks=72, tick_len=3))
    c.add(orbit(c, cx, cy, M_R - 34, M_R - 34, width=.8, opacity=.32, dash='2 6', glow=False))
    c.add(orbit(c, cx, cy + 4, 112, 24, rot=-10, width=1, opacity=.45, glow=False))
    c.add(rays(c, cx, cy, 30, 128, n=14, color=CYAN, op=.1, start=-180, end=180, seed=8))

    pos, beams, orbs = {}, [], []
    for i, key in enumerate(M_ORDER):
        th = math.radians(22.5 + 45 * i)
        ox, oy = cx + M_R * math.sin(th), cy + M_R * math.cos(th)
        pos[key] = (ox, oy)
        acc = ACCENT.get(key, ELEC)
        ux, uy = (ox - cx) / M_R, (oy - cy) / M_R
        bz = Bez((cx + ux * 70, cy + uy * 70), (cx + ux * 92, cy + uy * 92), (ox - ux * 40, oy - uy * 40), (ox - ux * 21, oy - uy * 21))
        d0 = .5 + .07 * i
        beams.append(beam(c, bz, ELEC, 1.1, end_color=acc if acc != ELEC else CYAN, a0=.4, a1=.9, draw=d0))
        if key in ('market', 'website'):
            beams.append(comet_on(c, bz, .6, color=CYAN, size=.55, dur=3.4, delay=-1.7 * (key == 'website'), tail=12))
        orbs.append(c.intro(orb(c, ox, oy, 21, ICON.get(key, key), acc), 'pop', d0 + .45))
        c.anchor(key, ox, oy + 21 + 15, kind='label', side='below')
    c.add(g(*beams))
    c.add(c.intro(floating_mark(c, cx, cy - 36, 118), 'drop', .05))
    c.add(*orbs)

    # featured record: Market orb -> project plate
    mx_, my_ = pos['market']
    px, py, pw, ph = 46, 428, 298, 78
    bz = Bez((mx_, my_ + 22), (mx_, my_ + 58), (px + 46, py - 26), (px + 46, py))
    c.add(beam(c, bz, CYAN, 1.2, a0=.9, a1=.8, draw=1.2), c.intro(node(c, px + 46, py, 2.2, CYAN, 3.5), 'pop', 2))
    fp = lambda: frag_project(c, px + 12, py + 11, pw - 24, ph - 22, '8.0M', '158', '3')
    c.add(c.intro(g(glass(c, px, py, pw, ph, 14, ELEC, 5, glint=True, glint_delay=2.5),
                    mirrored(c, px + 12, pw - 24, fp) if rtl else fp()), 'rise', 1.0))
    c.anchor('record', 195, py + ph + 5 + 18, kind='label', side='below')


def scenes():
    return [Scene('deck', 1200, 900, draw_deck), Scene('deck-rtl', 1200, 900, lambda c: draw_deck(c, True)),
            Scene('deck-mobile', 390, 540, draw_mobile), Scene('deck-mobile-rtl', 390, 540, lambda c: draw_mobile(c, True))]
