"""Ask Estavo / Brokers AI — "Answer console" (REFERENCE SCENE for a NON-hub composition).

Scenes (assets/img/fx/, each also -loop.svg and -still.svg; -rtl = Arabic, answer mirrored)
  broker-ai-core(-rtl)          1200x900  desktop hero (4:3, same stage ratio as home-deck)
  broker-ai-core-mobile(-rtl)    390x540  phone composition (tool dock tray + answer plate)

Silhouette (deliberately NOT the home radial hub): a large chat-answer plate fills the front;
the six tools Brokers AI really uses stand in two docks on either side and feed the plate with
light beams (left: project search, compare, developers; right: new launches, book a viewing,
client PDF); a small AI glyph core hovers above and lights the plate from the top.

Example data (tools/data/home-fixture.json): the question is the HTML label «3 غرف في التجمع،
لحد 8 مليون، أقل مقدم» / "3 bedrooms in New Cairo, up to 8M, lowest down payment". Rows A 7.9M /
1.4M / 2028, B 8.0M / 1.2M / 2027 (best: lowest down payment, mint), C 8.3M / 1.5M / ready (price
amber: over the 8M cap). Label the stage «مثال» / "Example" (anchor `chat`).

Label anchors (% of the art box; centre a .fx-stage__label on the point):
  broker-ai-core(-rtl): search, compare, developers, launch, calendar, pdf = tool labels ABOVE
      their dock plate; question = centre of the question box - the label IS the bubble:
      meta w/h = box size in % of art width/height, allow 2 balanced lines (text-wrap:balance);
      chat = the example tag, top-start corner inside the answer plate.
  broker-ai-core-mobile(-rtl): question + chat as above; search … pdf = short labels UNDER the
      dock orbs (12px; use the short forms: بحث/Search, مقارنة/Compare, المطورين/Developers,
      إطلاقات/Launches, معاينة/Viewing, PDF).
`python3 tools/build-fx-art.py broker-ai --list` prints the exact numbers (also in anchors.json).
"""
import math

from kit import (CYAN, ELEC, MINT, WHITE, Bez, Scene, aurora, beam, comet_on, el, f, floating_glyph, frag_answer,
                 frag_calendar, frag_compare, frag_developer, frag_launch, frag_pdf, frag_search, g, glass, glow,
                 holo_plate, light_column, mirrored, node, orb, orbit, perspective_floor, rays, stars)

TW, TH = 176, 112  # tool plate (local units)
TOOLS_L = [  # key, icon, fragment, accent
    ('search', 'search', lambda c, x, y, w, h: frag_search(c, x, y, w, h), CYAN),
    ('compare', 'compare', lambda c, x, y, w, h: frag_compare(c, x, y, w, h), CYAN),
    ('developers', 'developers', lambda c, x, y, w, h: frag_developer(c, x, y, w, h), ELEC),
]
TOOLS_R = [
    ('launch', 'launch', lambda c, x, y, w, h: frag_launch(c, x, y, w, h, '2027'), ELEC),
    ('calendar', 'calendar', lambda c, x, y, w, h: frag_calendar(c, x + 8, y + 2, w - 16, h - 4), ELEC),
    ('pdf', 'pdf', lambda c, x, y, w, h: frag_pdf(c, x + w * .22, y, w * .56, h), ELEC),
]
# answer plate (desktop)
AX, AY, AW, AH = 300, 268, 600, 512


def draw_core(c, rtl=False):
    c.add(aurora(c, [(600, 420, 520, 380, ELEC, .26), (600, 120, 300, 170, CYAN, .16), (170, 640, 240, 200, ELEC, .12),
                     (1030, 640, 240, 200, CYAN, .08)]))
    c.add(stars(c, 0, 0, 1200, 600, 46, seed=21, avoid=lambda x, y: 250 < x < 950 and y > 220))
    c.add(perspective_floor(c, 0, 640, 1200, 260, cols=22, rows=8, vy=380, opacity=.42))
    c.add(glow(c, 600, 820, 420, 70, ELEC, .45))

    # core: small glyph over a lens ring, light falling onto the answer plate
    gx, gy = 600, 132
    c.add(rays(c, gx, gy, 40, 260, n=11, color=CYAN, op=.13, start=-170, end=-10, seed=9))
    c.add(light_column(c, gx, AY + 4, gy + 30, 300, 60, CYAN, .22))
    c.add(orbit(c, gx, gy + 40, 150, 30, width=1.1, opacity=.55, ticks=40, tick_len=3))
    c.add(orbit(c, gx, gy + 40, 210, 44, width=.8, opacity=.3, dash='2 6', glow=False))
    c.add(c.intro(floating_glyph(c, gx, gy, 84), 'drop', .1))

    # docks + beams into the answer plate edges
    beams, plates, labels = [], [], []
    rows_y = [AY + 150, AY + 262, AY + 374]   # answer rows (beams land on the plate edge here)
    for side, tools in ((-1, TOOLS_L), (1, TOOLS_R)):
        for i, (key, ic, frag, acc) in enumerate(tools):
            s = (.9, .97, 1.04)[i]
            cx = 600 + side * (452 - 14 * i)
            cy = 330 + i * 176
            port = 'right' if side < 0 else 'left'
            skew = side * -(6 - i * 2)
            pl, om, geo = holo_plate(c, cx, cy, TW, TH, frag, ic, acc, s, port, skew, port_r=20, rtl=rtl,
                                     intro=.35 + .18 * i + (.09 if side > 0 else 0))
            plates.append((pl, om))
            ex, ey = geo['port']
            tx = AX if side < 0 else AX + AW
            ty = rows_y[i]
            bz = Bez((ex - side * 20, ey), (ex - side * 46, ey), (tx + side * 30, ty), (tx, ty))
            d0 = .9 + .18 * i
            beams.append(beam(c, bz, ELEC, 1.4, end_color=CYAN, a0=.9, a1=.95, draw=d0))
            beams.append(c.intro(node(c, tx, ty, 2.6, CYAN, 3.5), 'pop', d0 + .9))
            if i == 1:  # one pulse per dock
                beams.append(comet_on(c, bz, .5, color=CYAN, size=.9, dur=3.6, delay=-1.2 if side > 0 else 0))
            labels.append((key, geo['cx'], geo['top'] - 24))
    c.add(g(*beams))
    for pl, om in plates:
        c.add(pl, om)

    # the answer plate
    c.add(c.intro(g(glass(c, AX, AY, AW, AH, 24, CYAN, 9, glint=True, glint_delay=3, glint_dur=11),
                    _answer(c, AX + 26, AY + 30, AW - 52, AH - 56, rtl, u=1.0)), 'rise', .15))
    c.add(c.intro(orb(c, 600, AY, 24, 'broker-ai', CYAN), 'pop', .7))
    for key, x, y in labels:
        c.anchor(key, x, y, kind='label', side='above')
    qx, qy, qw, qh = c.answer_q_screen
    c.anchor('question', qx, qy, kind='label', side='inside', w=round(100 * qw / c.w, 2), h=round(100 * qh / c.h, 2))
    tx = AX + 26 + 58 if not rtl else AX + AW - 26 - 58
    c.anchor('chat', tx, AY + 30 + 32, kind='label', side='inside')


def _answer(c, x, y, w, h, rtl, u, **kw):
    """frag_answer, mirrored for Arabic; stores the question box in screen coordinates."""
    draw = lambda: frag_answer(c, x, y, w, h, u=u, **kw)
    out = mirrored(c, x, w, draw) if rtl else draw()
    qx, qy, qw, qh = c.answer_q
    if rtl:
        qx = 2 * x + w - qx
    c.answer_q_screen = (qx, qy, qw, qh)
    return out


# ── Mobile ─────────────────────────────────────────────────────────────
M_DOCK = ['search', 'compare', 'developers', 'launch', 'calendar', 'pdf']
M_ACC = {'search': CYAN, 'compare': CYAN}


def draw_mobile(c, rtl=False):
    W = 390
    c.add(aurora(c, [(195, 80, 200, 120, CYAN, .18), (195, 330, 230, 200, ELEC, .26), (40, 200, 120, 120, ELEC, .1)]))
    c.add(stars(c, 0, 0, W, 300, 26, seed=3, r=(.4, 1.1), avoid=lambda x, y: 20 < x < 370 and 110 < y < 300))
    c.add(perspective_floor(c, 0, 470, W, 70, cols=12, rows=4, vy=380, opacity=.4))
    # core
    gx, gy = 195, 40
    c.add(rays(c, gx, gy, 16, 100, n=9, color=CYAN, op=.12, start=-170, end=-10, seed=4))
    c.add(orbit(c, gx, gy + 20, 80, 14, width=1, opacity=.55, ticks=28, tick_len=2.5))
    c.add(c.intro(floating_glyph(c, gx, gy, 36), 'drop', .1))
    # dock tray: 2 rows x 3 tool orbs on light rails, labels under each orb
    tx, ty, tw, th = 18, 82, 354, 170
    c.add(light_column(c, gx, ty + 4, gy + 16, 120, 24, CYAN, .2))
    c.add(c.intro(glass(c, tx, ty, tw, th, 18, ELEC, 5, strength=.75), 'rise', .2))
    cols = [tx + tw * (k + .5) / 3 for k in range(3)]
    rows = [ty + 40, ty + 118]
    for k, ry in enumerate(rows):
        c.add(beam(c, Bez((cols[0] - 40, ry), (cols[0], ry), (cols[2], ry), (cols[2] + 40, ry)), ELEC, 1, end_color=CYAN,
                   a0=.35, a1=.35, draw=.5 + .1 * k))
    feeds = []
    for i, key in enumerate(M_DOCK):
        ox, oy = cols[i % 3], rows[i // 3]
        if rtl:
            ox = 2 * gx - ox  # tools read in the page direction
        c.add(c.intro(orb(c, ox, oy, 19, key, M_ACC.get(key, ELEC)), 'pop', .45 + .08 * i))
        c.anchor(key, ox, oy + 33, kind='label', side='below')
    # beams: tray -> answer plate
    ax, ay, aw, ah = 14, 280, 362, 248
    for k, dx in enumerate((-110, 0, 110)):
        sx, sy = gx + dx, ty + th + 6
        bz = Bez((sx, sy), (sx, sy + 12), (gx + dx * .5, ay - 14), (gx + dx * .5, ay))
        feeds.append(beam(c, bz, CYAN if k == 1 else ELEC, 1.3 if k == 1 else 1, end_color=MINT if k == 1 else CYAN, a0=.85, a1=.95, draw=.8))
        feeds.append(c.intro(node(c, gx + dx * .5, ay, 2.2, CYAN, 3.2), 'pop', 1.6))
        if k == 1:
            feeds.append(comet_on(c, bz, .5, color=MINT, size=.6, dur=2.8, tail=10))
    c.add(g(*feeds))
    c.add(c.intro(g(glass(c, ax, ay, aw, ah, 18, CYAN, 6, glint=True, glint_delay=2.5),
                    _answer(c, ax + 12, ay + 16, aw - 24, ah - 28, rtl, u=.62, q_w=.72)), 'rise', .3))
    qx, qy, qw, qh = c.answer_q_screen
    c.anchor('question', qx, qy, kind='label', side='inside', w=round(100 * qw / c.w, 2), h=round(100 * qh / c.h, 2))
    tx_ = ax + 12 + 30 if not rtl else ax + aw - 12 - 30
    c.anchor('chat', tx_, ay + 16 + 18, kind='label', side='inside')


def scenes():
    return [Scene('core', 1200, 900, draw_core), Scene('core-rtl', 1200, 900, lambda c: draw_core(c, True)),
            Scene('core-mobile', 390, 540, draw_mobile), Scene('core-mobile-rtl', 390, 540, lambda c: draw_mobile(c, True))]
