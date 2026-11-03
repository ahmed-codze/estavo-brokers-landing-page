"""Estavo Signal illustration kit (pure Python stdlib, no fonts).

Scenes are word-free SVGs that sit inside a deep-navy `.fx-stage` (the stage CSS
paints aurora, grid and vignette; a scene carries only its own local light and is
transparent). Words live in HTML labels positioned over the stage by anchor %.

Scene module contract (tools/fx_art/<key>.py)
---------------------------------------------
    from kit import Scene, ...
    def scenes():
        return [Scene('deck', 1200, 900, draw_deck), Scene('deck-mobile', 390, 460, draw_mobile)]

    def draw_deck(c):            # c: Canvas
        c.add(aurora(c, [...]), glass(c, ...), ...)
        c.anchor('market', x, y)  # label anchor in px -> exported as % of width/height

`python3 tools/build-fx-art.py <key>` writes assets/img/fx/<key>-<scene>.svg (animated)
and <key>-<scene>-still.svg (same drawing, final state, zero animation CSS), checks both
parse and stay <= 60,000 bytes, and merges every scene's anchors into
assets/img/fx/anchors.json.

Direction: scenes are word-free, but chat/cards/lists have a start and an end. Ship a
'<scene>-rtl' variant (Arabic) that wraps those fragments in mirrored() (holo_plate takes
rtl=True); numerals and icons counter-flip so they stay readable. Charts keep LTR time.

Size discipline (60 KB budget): everything repeated is defined once and <use>d (glass
plates per accent, thumbs, orb bases, icons, glyphs, nodes, comets); halos share one
gradient per colour (intensity = element opacity). Check bytes after every change.

Every draw helper RETURNS an SVG string (so it can be wrapped in g()/transforms);
nothing is added to the canvas until you call c.add(...). Helpers that need
gradients/clips register them on the canvas (ids are scoped per file).

Motion rules: CSS @keyframes inside the SVG <style>, wrapped in
@media (prefers-reduced-motion: no-preference); transform / opacity / offset-distance
only; c.anim() returns '' on the still pass so the still is the final state.
No SVG blur filters anywhere: glow = radial-gradient halos + wide faint strokes.

API (all coordinates in px of the scene viewBox)
------------------------------------------------
Canvas(name, w, h, animated)       collects defs/css/body; .render() -> svg text
  c.add(*parts)                     append markup to the body
  c.uid(base)                       per-file scoped id
  c.lin(stops, x1,y1,x2,y2, user)   linear gradient -> 'url(#id)'  (stops: [(off, color, opacity)])
  c.rad(stops, cx,cy,r, fx,fy,user) radial gradient -> 'url(#id)'
  c.clip(markup) / c.mask(markup)   -> 'url(#id)'
  c.anim(decl, origin)              class name for an animated element ('' when still)
  c.kf(name, frames)                scoped @keyframes name
  c.anchor(name, x, y, **meta)      record a label anchor
el(tag, body, **attrs)              tiny element builder (cls->class, a_b->a-b)
g(*children, **attrs)               group
iso(x, y, z, o, s, k)               plan (x,y,z) -> screen point (k = vertical squash)
Bez(p0, p1, p2, p3) / quad(p0,c,p1) cubic bezier: .d(), .at(t), .angle(t)
ellipse_d(cx, cy, rx, ry, rot)      closed ellipse path (for offset-path orbits)
aurora(c, blobs, drift)             radial-gradient light blobs (cx,cy,rx,ry,color,opacity)
stars(c, x,y,w,h, n, seed, ...)     deterministic dot / star field, optional twinkle
iso_grid(c, cx,cy,rx,ry, step, k)   diamond floor grid fading radially to the horizon
perspective_floor(c, x,y,w,h, ...)  vanishing-point grid floor fading to the horizon
orbit(c, cx,cy,rx,ry, rot, ...)     tilted orbit ring, brighter at the front, optional ticks
spin_ring(c, cx,cy,r,k, ...)        dashed ring lying on the floor plane, rotating
ping(c, cx,cy,rx,ry, ...)           expanding/fading floor ring (animated only)
iso_disc(c, cx,cy,rx,ry,h, ...)     extruded cylinder tier (plinth)
iso_block(c, o, x,y,z,w,d,h, ...)   extruded iso box
light_column(c, cx,yb,yt,wb,wt)     vertical light shaft
glass(c, x,y,w,h, r, accent, ...)   holographic glass plate (thickness, rim, top light, glint)
node(c, x,y, r, color, halo)        glowing node (radial halo + core + white centre)
beam(c, bez, color, width, ...)     gradient light beam with glow under-stroke
comet(c, path_d, still_xy, angle, ...) pulse travelling along a visible path
orb(c, cx,cy, r, icon, accent)      icon orb tile (like .fx-orb)
icon(c, name, x,y, size, color)     sprite icon (assets/img/icons/estavo-fx.svg) as nested svg
mark(c, x,y, w, fill)               the Estavo mark (assets/logo/estavo-mark.svg)
mirrored(c, x, w, draw)             RTL: mirror a fragment box, numerals/icons stay readable
ai_glyph(c, cx,cy, size, fill)      Estavo's four-point AI glyph
hud(c, text, x,y, size, color, anchor) vector HUD numerals 0-9 . , M K Q Y % / : + - (no fonts)
bar(...) / lines(...)               skeleton text lines
holo_plate(c, cx,cy,w,h, frag, icon, accent, s, port, skew) glass plate + docked icon orb + fragment
plinth(c, cx,cy, s) / floating_mark(c, cx,y,w) / floating_glyph(c, cx,cy,size)  core pieces
rays(c, cx,cy, r0,r1, n) / particles(c, cx,yb,yt,w, n)  god rays / rising motes
glow(c, cx,cy, rx,ry, color, peak)  radial halo (standard gradient, opacity = intensity)
Fragments (draw a real product structure inside a box, dark glass context):
  frag_project(c,x,y,w,h, price, area, beds)  project card: photo-free thumb, specs, price chip
  frag_payment(c,x,y,w,h, down, bars)         down-payment block + quarterly installment ribbon
  frag_jobs(c,x,y,w,h)                         two stacked job cards
  frag_chat(c,x,y,w,h, prices)                question bubble + AI answer with 3 result chips
  frag_pdf(c,x,y,w,h)                          PDF page (fold, photo block, table)
  frag_browser(c,x,y,w,h)                      broker website in a browser frame + assistant
  frag_news(c,x,y,w,h)                         news rows on a timeline spine
  frag_game(c,x,y,w,h)                         game round: 5 pips, question, 4 options
  frag_developer(c,x,y,w,h)                    developer profile: logo slot, pin, phone, projects
  frag_compare(c,x,y,w,h)                      3-column comparison, best column in mint
  frag_calendar(c,x,y,w,h)                     month grid with a booked slot
  frag_launch(c,x,y,w,h, year)                 new launch plate with year chip
  frag_search(c,x,y,w,h)                       query field, filter chips, result rows
  frag_answer(c,x,y,w,h, rows, best, actions)  Brokers AI answer: question, rows, PDF/compare/calendar
write_scene(key, scene, out_dir)    writes animated + still files, returns stats
"""
import math
import random
import re
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
SPRITE_PATH = ROOT / 'assets/img/icons/estavo-fx.svg'
MARK_PATH = ROOT / 'assets/logo/estavo-mark.svg'

# ── Palette (mirrors --fx-* tokens in assets/css/fx.css) ───────────────
VOID = '#050f1e'
DEEP = '#0b2239'
RAISE = '#12304f'
BLUE = '#163e69'
ELEC = '#4f9cf0'
CYAN = '#7fdcff'
MINT = '#72e0bb'
AMBER = '#f6b955'
PAPER = '#fafcff'
INK = '#0f2236'
WHITE = '#ffffff'
GLASS_HI = '#2d67a3'
GLASS_MID = '#143a63'
GLASS_LO = '#0a2340'
EDGE = '#06172a'

LOOP_BUDGET = 7  # infinite animations per scene file; an <img> SVG repaints whole while any runs

ACCENT = {
    'market': ELEC, 'developers': ELEC, 'roi': MINT, 'jobs': ELEC, 'challenge': AMBER,
    'news': CYAN, 'guides': MINT, 'website': ELEC, 'enterprise': ELEC, 'client-ai': CYAN,
    'marketing': ELEC, 'meta-ads': ELEC, 'listings': ELEC, 'pricing': ELEC,
    'integrations': ELEC, 'broker-ai': CYAN, 'data': ELEC, 'examples': ELEC,
}


def f(v):
    """Compact number for SVG attributes (2 decimals under 10, else 1)."""
    if isinstance(v, str):
        return v
    v = float(v)
    s = f'{v:.2f}' if abs(v) < 10 else f'{v:.1f}' if abs(v) < 100 else str(int(round(v)))
    s = s.rstrip('0').rstrip('.') if '.' in s else s
    if s in ('-0', ''):
        s = '0'
    if s.startswith('0.'):
        s = s[1:]
    elif s.startswith('-0.'):
        s = '-' + s[2:]
    return s


def hx(col):
    """#aabbcc -> #abc when possible."""
    if isinstance(col, str) and len(col) == 7 and col[0] == '#' and col[1] == col[2] and col[3] == col[4] and col[5] == col[6]:
        return '#' + col[1] + col[3] + col[5]
    return col


def P(*xy):
    """'x,y x,y' point list from flat or paired numbers."""
    if len(xy) == 1:
        xy = xy[0]
    flat = []
    for p in xy:
        if isinstance(p, (tuple, list)):
            flat += list(p)
        else:
            flat.append(p)
    return ' '.join(f'{f(flat[i])},{f(flat[i + 1])}' for i in range(0, len(flat), 2))


def _attr_name(k):
    if k == 'cls':
        return 'class'
    if k == 'href':
        return 'href'
    return k.rstrip('_').replace('_', '-')


def el(tag, body=None, **a):
    attrs = ''.join(f' {_attr_name(k)}="{f(hx(v))}"' for k, v in a.items() if v is not None and v != '')
    if body is None or body == '':
        return f'<{tag}{attrs}/>'
    if isinstance(body, (list, tuple)):
        body = ''.join(b for b in body if b)
    return f'<{tag}{attrs}>{body}</{tag}>'


def g(*children, **a):
    body = ''.join(ch for ch in children if ch)
    if not body:
        return ''
    if not any(v not in (None, '') for v in a.values()):
        return body  # an attribute-less <g> changes nothing; skip it (bytes)
    return el('g', body, **a)


def tr(x, y, s=None):
    return f'translate({f(x)} {f(y)})' + (f' scale({f(s) if s >= .1 else round(s, 3)})' if s not in (None, 1) else '')


# ── Canvas ─────────────────────────────────────────────────────────────
class Canvas:
    def __init__(self, name, w, h, animated, mode=None):
        # mode: 'anim' (intro assembly + ambient loops), 'loop' (ambient loops only, for
        # re-entry after the scene was swapped back to its still) or 'still' (no CSS at all)
        self.mode = mode or ('anim' if animated else 'still')
        self.name, self.w, self.h = name, w, h
        self.animated = self.mode != 'still'
        self.intro_on = self.mode == 'anim'
        self.loops = 0  # infinite animations registered (budget: LOOP_BUDGET per scene)
        initials = ''.join(p[0] for p in re.split(r'[^a-z0-9]+', name.lower()) if p)[:3] or 'fx'
        b36 = '0123456789abcdefghijklmnopqrstuvwxyz'
        crc = zlib.crc32(name.encode())
        self.prefix = initials[:2] + b36[crc % 36] + b36[(crc // 36) % 36]  # 4 chars, unique per file name
        self._n = 0
        self.defs, self.parts = [], []
        self.base, self.motion, self.keyframes, self._anim = {}, {}, {}, {}
        self._cache = {}
        self.anchors = {}
        self.flip = 0  # >0 while drawing inside mirrored(): numerals/icons counter-flip

    # ids / defs
    def uid(self, base='i'):
        self._n += 1
        return f'{self.prefix}{base}{self._n:x}'

    def add(self, *parts):
        self.parts.extend(p for p in parts if p)

    def _cached(self, key, make):
        if key not in self._cache:
            self._cache[key] = make()
        return self._cache[key]

    @staticmethod
    def _stops(stops):
        out = []
        for s in stops:
            off, col = s[0], s[1]
            op = s[2] if len(s) > 2 else 1
            out.append(el('stop', offset=f(off), stop_color=hx(col), stop_opacity=None if op == 1 else f(round(op, 3)) if op >= .01 else '0'))
        return ''.join(out)

    def lin(self, stops, x1=0, y1=0, x2=0, y2=1, user=False):
        key = ('l', tuple(map(tuple, stops)), x1, y1, x2, y2, user)

        def make():
            i = self.uid('l')
            self.defs.append(el('linearGradient', self._stops(stops), id=i, x1=None if x1 == 0 else f(x1), y1=None if y1 == 0 else f(y1),
                                x2=None if (x2 == 1 and not user) else f(x2), y2=None if y2 == 0 else f(y2),
                                gradientUnits='userSpaceOnUse' if user else None))
            return f'url(#{i})'
        return self._cached(key, make)

    def rad(self, stops, cx=.5, cy=.5, r=.5, fx=None, fy=None, user=False):
        key = ('r', tuple(map(tuple, stops)), cx, cy, r, fx, fy, user)

        def make():
            i = self.uid('r')
            self.defs.append(el('radialGradient', self._stops(stops), id=i, cx=None if cx == .5 and not user else f(cx),
                                cy=None if cy == .5 and not user else f(cy), r=None if r == .5 and not user else f(r),
                                fx=None if fx is None else f(fx), fy=None if fy is None else f(fy),
                                gradientUnits='userSpaceOnUse' if user else None))
            return f'url(#{i})'
        return self._cached(key, make)

    def halo_fill(self, color):
        """The one standard halo gradient per colour; set intensity with element opacity (see glow())."""
        return self.rad([(0, color), (.42, color, .3), (1, color, 0)])

    def clip(self, markup):
        def make():
            i = self.uid('c')
            self.defs.append(el('clipPath', markup, id=i))
            return f'url(#{i})'
        return self._cached(('clip', markup), make)

    def mask(self, markup, user=True):
        i = self.uid('m')
        self.defs.append(el('mask', markup, id=i, maskUnits='userSpaceOnUse' if user else None,
                            x=0 if user else None, y=0 if user else None,
                            width=self.w if user else None, height=self.h if user else None))
        return f'url(#{i})'

    def define(self, key, markup_fn):
        """Put a reusable element in <defs> once; returns its id (markup_fn(id) -> markup)."""
        def make():
            i = self.uid('d')
            self.defs.append(markup_fn(i))
            return i
        return self._cached(('def', key), make)

    # animation layer
    def kf(self, name, frames):
        scoped = f'{self.prefix}-{name}'
        if self.animated:
            self.keyframes[scoped] = f'@keyframes {scoped}{{{frames}}}'
        return scoped

    def anim(self, decl, origin=None, base=None, supports=None):
        """Register `.cls{decl}` inside the reduced-motion guard; returns cls or '' (still).
        Identical declarations share one class (put per-instance delays in c.delay()).
        origin: 'center' (fill-box centre) or (x, y) in view-box px. base: rule applied
        outside the motion guard in the animated file only (e.g. hide a comet until it moves).
        supports: a CSS @supports condition the rule needs (e.g. offset-path)."""
        if not self.animated:
            return ''
        if 'infinite' in decl:
            self.loops += 1
        o = ''
        if origin == 'center':
            o = 'transform-box:fill-box;transform-origin:center;'
        elif isinstance(origin, tuple):
            o = f'transform-box:view-box;transform-origin:{f(origin[0])}px {f(origin[1])}px;'
        key = (o + decl, base, supports)
        if key in self._anim:
            return self._anim[key]
        cls = self.uid('a')
        self._anim[key] = cls
        self.motion.setdefault(supports, []).append(f'.{cls}{{{o}{decl}}}')
        if base:
            self.base.setdefault(base, []).append(f'.{cls}')
        return cls

    def delay(self, sec):
        """Inline style for a per-instance animation delay (None on the still pass)."""
        return f'animation-delay:{f(sec)}s' if self.animated and sec else None

    INTRO = {
        # one-shot entrance keyframes (fill-mode both; the element's own state is the end state)
        'rise': ('from{opacity:0;transform:translateY(34px) scale(.94)}60%{opacity:1}', '1.1s cubic-bezier(.2,.9,.3,1.12)', 'center'),
        'drop': ('from{opacity:0;transform:translateY(-40px) scale(.9)}', '1.2s cubic-bezier(.2,.9,.3,1.1)', 'center'),
        'pop': ('from{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.12)}to{transform:scale(1)}', '.7s cubic-bezier(.3,.7,.4,1)', 'center'),
        'fade': ('from{opacity:0}', '1.4s ease-out', None),
        'draw': ('from{stroke-dashoffset:1}', '1.1s cubic-bezier(.6,0,.3,1)', None),
    }

    def intro(self, markup, kind='rise', delay=0.0):
        """Wrap `markup` in a one-shot entrance (intro assembly). Only the 'anim' file gets it;
        the wrapper carries no transform attribute, so CSS transforms never fight SVG ones.
        kind: rise | drop | pop | fade | draw (draw: markup must be <path pathLength="1">s,
        see beam(..., draw=delay))."""
        if not self.intro_on or not markup:
            return markup
        frames, timing, origin = self.INTRO[kind]
        name = self.kf('in-' + kind, frames)
        extra = 'stroke-dasharray:1;' if kind == 'draw' else ''
        cls = self.anim(f'{extra}animation:{name} {timing} both', origin=origin)
        return el('g', markup, cls=cls, style=self.delay(delay))

    def anchor(self, name, x, y, **meta):
        self.anchors[name] = dict(x=round(100 * x / self.w, 2), y=round(100 * y / self.h, 2), **meta)

    def render(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" fill="none" stroke-linecap="round" stroke-linejoin="round">')
        out = [head, '<!-- Estavo Signal · generated by tools/build-fx-art.py · do not edit -->']
        if self.animated and self.motion:
            css = ''.join(','.join(sel) + '{' + decl + '}' for decl, sel in self.base.items())
            inner = ''.join(''.join(r) for k, r in self.motion.items() if k is None)
            inner += ''.join(f'@supports ({k}){{' + ''.join(r) + '}' for k, r in self.motion.items() if k is not None)
            css += '@media (prefers-reduced-motion:no-preference){' + inner + ''.join(self.keyframes.values()) + '}'
            out.append(f'<style>{css}</style>')
        if self.defs:
            out.append('<defs>' + ''.join(self.defs) + '</defs>')
        out.extend(self.parts)
        out.append('</svg>')
        return '\n'.join(out) + '\n'


@dataclass
class Scene:
    name: str
    width: int
    height: int
    draw: Callable
    notes: str = ''
    anchors: dict = field(default_factory=dict)


# ── Geometry ───────────────────────────────────────────────────────────
def iso(x, y, z=0, o=(0, 0), s=1, k=.5):
    """Plan coords -> screen. x runs down-right, y down-left, z up; k = vertical squash
    (k=.5 is 2:1 dimetric, .577 true iso; match the plinth ellipse ratio ry/rx)."""
    return (o[0] + (x - y) * s, o[1] + (x + y) * k * s - z * s)


class Bez:
    def __init__(self, p0, p1, p2, p3):
        self.p = [p0, p1, p2, p3]

    def at(self, t):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = self.p
        u = 1 - t
        return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
                u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)

    def angle(self, t):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = self.p
        u = 1 - t
        dx = 3 * u * u * (x1 - x0) + 6 * u * t * (x2 - x1) + 3 * t * t * (x3 - x2)
        dy = 3 * u * u * (y1 - y0) + 6 * u * t * (y2 - y1) + 3 * t * t * (y3 - y2)
        return math.degrees(math.atan2(dy, dx))

    def d(self):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = self.p
        return f'M{f(x0)} {f(y0)}C{f(x1)} {f(y1)} {f(x2)} {f(y2)} {f(x3)} {f(y3)}'

    @property
    def start(self):
        return self.p[0]

    @property
    def end(self):
        return self.p[3]


def quad(p0, c, p1):
    return Bez(p0, (p0[0] + 2 / 3 * (c[0] - p0[0]), p0[1] + 2 / 3 * (c[1] - p0[1])),
               (p1[0] + 2 / 3 * (c[0] - p1[0]), p1[1] + 2 / 3 * (c[1] - p1[1])), p1)


def ellipse_pt(cx, cy, rx, ry, t_deg, rot=0):
    t = math.radians(t_deg)
    x, y = rx * math.cos(t), ry * math.sin(t)
    r = math.radians(rot)
    return (cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r))


def ellipse_d(cx, cy, rx, ry, rot=0, start=90):
    """Closed ellipse path starting at parametric angle `start` (90 = front), clockwise."""
    a = ellipse_pt(cx, cy, rx, ry, start, rot)
    b = ellipse_pt(cx, cy, rx, ry, start + 180, rot)
    return (f'M{f(a[0])} {f(a[1])}A{f(rx)} {f(ry)} {f(rot)} 1 1 {f(b[0])} {f(b[1])}'
            f'A{f(rx)} {f(ry)} {f(rot)} 1 1 {f(a[0])} {f(a[1])}')


# ── Atmosphere ─────────────────────────────────────────────────────────
def aurora(c, blobs, drift=False):
    """blobs: [(cx, cy, rx, ry, color, opacity)]. Static by default: the .fx-stage aurora already
    drifts, and a drifting 1000px blob forces a full-image repaint every frame (loop budget)."""
    out = []
    for i, (cx, cy, rx, ry, col, op) in enumerate(blobs):
        fill = c.rad([(0, col), (.5, col, .38), (1, col, 0)])
        cls = ''
        if drift:
            name = c.kf(f'drift{i % 3}', [
                '0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(18px,-10px) scale(1.06)}',
                '0%,100%{transform:translate(0,0) scale(1);opacity:1}50%{transform:translate(-22px,8px) scale(.95);opacity:.8}',
                '0%,100%{transform:translate(0,0);opacity:.85}50%{transform:translate(10px,14px);opacity:1}'][i % 3])
            cls = c.anim(f'animation:{name} {18 + 3 * (i % 3)}s ease-in-out infinite', origin='center')
        out.append(g(el('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, cls=cls), opacity=f(op)))
    return g(*out)


def stars(c, x, y, w, h, n=60, seed=7, color=WHITE, r=(.5, 1.3), op=(.15, .55), twinkle=0, avoid=None):
    """Deterministic dot field; `avoid(px,py)->bool` skips points; twinkle = count that pulse.
    Dots are zero-length round-capped strokes bucketed by size/opacity (tiny output)."""
    rnd = random.Random(seed)
    buckets, tw = {}, []
    for i in range(n):
        px, py = x + rnd.random() * w, y + rnd.random() * h
        rr = r[0] + rnd.random() * (r[1] - r[0])
        o = op[0] + rnd.random() * (op[1] - op[0])
        if avoid and avoid(px, py):
            continue
        if i < twinkle:
            name = c.kf('twinkle', '0%,100%{opacity:.15}50%{opacity:1}')
            cls = c.anim(f'animation:{name} 4s ease-in-out infinite')
            dl = rnd.random() * -6
            tw.append(el('circle', cx=px, cy=py, r=rr * 1.3, fill=CYAN, opacity=f(min(1, o + .3)), cls=cls, style=c.delay(dl)))
        else:
            k = (round(rr * 2.5) / 2.5, round(o * 5) / 5)
            buckets.setdefault(k, []).append(f'M{f(px)} {f(py)}h0')
    out = [el('path', d=''.join(v), stroke=color, stroke_width=f(2 * k[0]), opacity=f(max(.1, k[1])))
           for k, v in sorted(buckets.items())]
    return g(*out) + ''.join(tw)


def iso_grid(c, cx, cy, rx, ry, step=32, k=.34, color=ELEC, opacity=.42, width=.8, fade=.62):
    """Diamond floor grid (plan lines at ±45° -> screen slopes ±k), radially faded."""
    lines = []
    span = rx + ry / k
    n = int(span / step) + 1
    for i in range(-n, n + 1):
        b = i * step * k
        for sgn in (1, -1):
            # y - cy = sgn*k*(x - cx) + b ; intersect with the ellipse
            m_ = sgn * k
            A = 1 / rx ** 2 + m_ ** 2 / ry ** 2
            B = 2 * m_ * b / ry ** 2
            C = b ** 2 / ry ** 2 - 1
            disc = B * B - 4 * A * C
            if disc <= 0:
                continue
            u1, u2 = (-B - disc ** .5) / (2 * A), (-B + disc ** .5) / (2 * A)
            lines.append(f'M{f(cx + u1)} {f(cy + m_ * u1 + b)}L{f(cx + u2)} {f(cy + m_ * u2 + b)}')
    m = c.mask(el('ellipse', cx=cx, cy=cy, rx=rx, ry=ry,
                  fill=c.rad([(0, WHITE, 1), (fade, WHITE, .45), (1, WHITE, 0)])))
    return g(el('path', d=''.join(lines), stroke=color, stroke_width=width, opacity=opacity), mask=m)


def perspective_floor(c, x, y, w, h, cols=14, rows=9, vx=None, vy=None, color=ELEC, opacity=.4, width=.8):
    """Grid floor: verticals converge on (vx, vy) above the band, horizontals tighten toward
    the horizon (top edge y), faded to transparent at the horizon."""
    vx = x + w / 2 if vx is None else vx
    vy = y - h * 1.2 if vy is None else vy
    d = []
    for i in range(cols + 1):
        bx = x - w * .5 + i * (2 * w / cols)
        t = (y - vy) / (y + h - vy)
        tx = vx + (bx - vx) * t
        d.append(f'M{f(tx)} {f(y)}L{f(bx)} {f(y + h)}')
    for j in range(1, rows + 1):
        yy = y + h * (j / rows) ** 1.9
        d.append(f'M{f(x)} {f(yy)}H{f(x + w)}')
    m = c.mask(el('rect', x=x, y=y, width=w, height=h,
                  fill=c.lin([(0, WHITE, 0), (.45, WHITE, .5), (1, WHITE, 1)])))
    return g(el('path', d=''.join(d), stroke=color, stroke_width=width, opacity=opacity), mask=m)


# ── Structures ─────────────────────────────────────────────────────────
def orbit(c, cx, cy, rx, ry, rot=0, color=ELEC, width=1, opacity=.6, dash=None, ticks=0, tick_len=5,
          back=.18, glow=True):
    """Orbit ring; vertical gradient makes the front arc brighter than the back."""
    stroke = c.lin([(0, color, back), (.55, color, .55), (1, CYAN, 1)])
    out = []
    if glow:
        out.append(el('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, stroke=stroke, stroke_width=width * 5, opacity=f(opacity * .14),
                      transform=f'rotate({f(rot)} {f(cx)} {f(cy)})' if rot else None))
    out.append(el('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, stroke=stroke, stroke_width=width, opacity=f(opacity),
                  stroke_dasharray=dash, transform=f'rotate({f(rot)} {f(cx)} {f(cy)})' if rot else None))
    if ticks:
        d = []
        for i in range(ticks):
            t = 360 * i / ticks
            p = ellipse_pt(cx, cy, rx, ry, t, rot)
            q = ellipse_pt(cx, cy, rx + tick_len, ry + tick_len * ry / rx, t, rot)
            d.append(f'M{f(p[0])} {f(p[1])}L{f(q[0])} {f(q[1])}')
        out.append(el('path', d=''.join(d), stroke=stroke, stroke_width=width, opacity=f(opacity * .9)))
    return g(*out)


def spin_ring(c, cx, cy, r, k=.34, color=CYAN, width=1.2, dash='2 7', opacity=.7, dur=None, reverse=False):
    """Dashed ring lying on the floor plane (circle squashed by k). Static unless `dur` is given
    (a rotation costs one loop of the scene's LOOP_BUDGET)."""
    cls = ''
    if dur:
        name = c.kf('spin' + ('r' if reverse else ''), f'to{{transform:rotate({"-" if reverse else ""}360deg)}}')
        cls = c.anim(f'animation:{name} {f(dur)}s linear infinite', origin='center')
    return el('g', el('circle', r=r, stroke=color, stroke_width=width, stroke_dasharray=dash, opacity=f(opacity),
                      vector_effect='non-scaling-stroke', cls=cls),
              transform=f'translate({f(cx)} {f(cy)}) scale(1 {f(k) if k >= .1 else k})')


def ping(c, cx, cy, rx, ry, color=CYAN, width=1.2, dur=3.6, delay=0):
    """Expanding, fading floor ring (animated file only)."""
    if not c.animated:
        return ''
    name = c.kf('ping', '0%{transform:scale(.55);opacity:0}15%{opacity:.9}100%{transform:scale(1.5);opacity:0}')
    cls = c.anim(f'animation:{name} {f(dur)}s ease-out {f(delay)}s infinite', origin='center', base='opacity:0')
    return el('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, stroke=color, stroke_width=width, cls=cls,
              vector_effect='non-scaling-stroke')


def iso_disc(c, cx, cy, rx, ry, h, top=None, side=None, rim=CYAN, rim_op=.85, edge=ELEC):
    """Cylinder tier: (cx, cy) is the centre of the TOP face."""
    top = top or c.rad([(0, '#1f4f82'), (.7, '#123659'), (1, '#0e2c4b')], cy=.4)
    side = side or c.lin([(0, '#16406b'), (.5, '#0c2745'), (1, '#071a2f')], 0, 0, 1, 0)
    side_d = (f'M{f(cx - rx)} {f(cy)}V{f(cy + h)}A{f(rx)} {f(ry)} 0 0 0 {f(cx + rx)} {f(cy + h)}'
              f'V{f(cy)}A{f(rx)} {f(ry)} 0 0 1 {f(cx - rx)} {f(cy)}Z')
    lip = f'M{f(cx - rx)} {f(cy + h)}A{f(rx)} {f(ry)} 0 0 0 {f(cx + rx)} {f(cy + h)}'
    rim_s = c.lin([(0, rim, .15), (.5, rim, rim_op), (1, rim, .15)], 0, 0, 1, 0)
    return g(
        el('path', d=side_d, fill=side),
        el('path', d=lip, stroke=edge, stroke_width=1, opacity=.55),
        el('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, fill=top),
        el('ellipse', cx=cx, cy=cy, rx=rx - .5, ry=ry - .5, stroke=rim_s, stroke_width=1.2),
    )


def iso_block(c, o, x, y, z, w, d, h, top='#2a5f97', left='#123a63', right='#0d2c4d', stroke=None, k=.5, s=1, sw=.8):
    """Extruded box in plan coords; visible faces: top, +y (left), +x (right)."""
    def p(px, py, pz):
        return iso(px, py, pz, o, s, k)
    t = [p(x, y, z + h), p(x + w, y, z + h), p(x + w, y + d, z + h), p(x, y + d, z + h)]
    lf = [p(x, y + d, z + h), p(x + w, y + d, z + h), p(x + w, y + d, z), p(x, y + d, z)]
    rf = [p(x + w, y, z + h), p(x + w, y + d, z + h), p(x + w, y + d, z), p(x + w, y, z)]
    kw = dict(stroke=stroke, stroke_width=sw if stroke else None, stroke_linejoin='round' if stroke else None)
    return g(el('polygon', points=P(lf), fill=left, **kw), el('polygon', points=P(rf), fill=right, **kw),
             el('polygon', points=P(t), fill=top, **kw))


def light_column(c, cx, yb, yt, wb, wt, color=ELEC, peak=.32, core=CYAN):
    fill = c.lin([(0, color, 0), (.6, color, peak * .5), (1, color, peak)])
    corefill = c.lin([(0, core, 0), (1, core, peak * 1.1)])
    return g(el('polygon', points=P(cx - wb / 2, yb, cx + wb / 2, yb, cx + wt / 2, yt, cx - wt / 2, yt), fill=fill),
             el('polygon', points=P(cx - wb * .18, yb, cx + wb * .18, yb, cx + wt * .1, yt, cx - wt * .1, yt), fill=corefill))


def glass(c, x, y, w, h, r=14, accent=ELEC, thickness=6, shadow=True, hud_corners=True, glint=False,
          glint_delay=0, glint_dur=9, strength=1.0, tint=None):
    """Holographic glass plate: floor glow, slab thickness, gradient body, inner top
    light, specular top line, gradient rim, HUD corner ticks and an animated glint."""
    # One definition per size, shared by every accent: the accent reaches the HUD corner ticks
    # through currentColor (color= on the <use>); the floor/inner glows stay electric.
    def build(i, x=0, y=0):
        out = []
        if shadow:
            out.append(glow(c, x + w / 2, y + h + thickness + 16, w * .5, 11 + h * .04, ELEC, .38))
        out.append(el('rect', x=x, y=y + thickness, width=w, height=h, rx=r, fill=EDGE,
                      stroke=c.lin([(0, ELEC, .05), (1, ELEC, .45)]), stroke_width=1))
        hi = tint or GLASS_HI
        out.append(el('rect', x=x, y=y, width=w, height=h, rx=r,
                      fill=c.lin([(0, hi, .72 * strength), (.45, GLASS_MID, .80), (1, GLASS_LO, .9)])))
        out.append(el('rect', x=x, y=y, width=w, height=h * .5, rx=r, fill=c.lin([(0, WHITE, .13), (1, WHITE, 0)])))
        out.append(glow(c, x + w * .3, y, w * .45, h * .55, ELEC, .22))
        out.append(el('rect', x=x + .5, y=y + .5, width=w - 1, height=h - 1, rx=r - .5,
                      stroke=c.lin([(0, WHITE, .62), (.3, CYAN, .5), (1, ELEC, .16)]), stroke_width=1.1))
        out.append(el('path', d=f'M{f(x + r)} {f(y + .8)}H{f(x + w - r)}', stroke=c.lin([(0, WHITE, 0), (.5, WHITE, .95), (1, WHITE, 0)], 0, 0, 1, 0),
                      stroke_width=1.2))
        if hud_corners:
            t, o = 9, 5
            d = (f'M{f(x - o)} {f(y - o + t)}V{f(y - o)}H{f(x - o + t)}'
                 f'M{f(x + w + o - t)} {f(y - o)}H{f(x + w + o)}V{f(y - o + t)}'
                 f'M{f(x + w + o)} {f(y + h + o - t)}V{f(y + h + o)}H{f(x + w + o - t)}'
                 f'M{f(x - o + t)} {f(y + h + o)}H{f(x - o)}V{f(y + h + o - t)}')
            out.append(el('path', d=d, stroke='currentColor', stroke_width=1.1, opacity=.55))

        return el('g', ''.join(out), id=i)
    key = ('glass', w, h, r, thickness, shadow, hud_corners, strength, tint)
    gid = c.define(key, build)
    out = [el('use', href=f'#{gid}', x=x or None, y=y or None, color=accent if hud_corners else None)]
    if glint and c.animated:
        cp = c.clip(el('rect', x=x, y=y, width=w, height=h, rx=r))
        name = c.kf('glint', '0%{transform:translateX(0)}22%,100%{transform:translateX(var(--gx))}')
        cls = c.anim(f'--gx:{f(w + 110)}px;animation:{name} {f(glint_dur)}s cubic-bezier(.45,0,.2,1) infinite')
        pid = c.define(('glint', w, h), lambda i: el('polygon', id=i, points=P(-70, h, -30, 0, 0, 0, -40, h),
                                                     fill=c.lin([(0, WHITE, 0), (.5, WHITE, .2), (1, WHITE, 0)])))
        band = el('use', href=f'#{pid}', x=x or None, y=y or None, cls=cls, style=c.delay(glint_delay))
        out.append(g(band, clip_path=cp))
    return g(*out)


def glow(c, cx, cy, rx, ry=None, color=ELEC, peak=.55, **a):
    """Radial-gradient halo (no blur filter). ry=None -> circle."""
    if ry is None:
        return el('circle', cx=cx or None, cy=cy or None, r=rx, fill=c.halo_fill(color), opacity=f(peak), **a)
    return el('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, fill=c.halo_fill(color), opacity=f(peak), **a)


def holo_plate(c, cx, cy, w, h, frag, icon_name, accent=ELEC, s=1.0, port='top', skew=0, port_r=21,
               delay=0, dim=1.0, r=16, thickness=6, pad=14, rtl=False, glint=False, intro=None):
    """A holo plate centred on (cx, cy): glass (w x h local units) scaled by s, skewY(skew deg)
    for carousel depth, with an icon orb 'docked' on the core-facing edge (port = top | bottom
    | left | right; beams should end at geo['port']). `frag(c, x, y, w, h)` draws the product
    fragment inside the box left free by the port. Returns (plate, port_orb, geo); add the
    port orb after the plate. rtl=True mirrors the fragment (see mirrored()).
    geo: cx, cy, w, h (screen px), top, bottom, port (x, y), acc."""
    tk = math.tan(math.radians(skew))
    inset = port_r * .62 + 8
    box = {'top': (pad, inset, w - 2 * pad, h - inset - pad), 'bottom': (pad, pad, w - 2 * pad, h - inset - pad),
           'left': (inset, pad, w - inset - pad, h - 2 * pad), 'right': (pad, pad, w - inset - pad, h - 2 * pad)}[port]
    pxy = {'top': (w / 2, 0), 'bottom': (w / 2, h + thickness / 2), 'left': (0, h / 2), 'right': (w, h / 2)}[port]

    def scr(px, py):
        lx, ly = (px - w / 2) * s, (py - h / 2) * s
        return cx + lx, cy + ly + lx * tk

    fr = mirrored(c, box[0], box[2], lambda: frag(c, *box)) if rtl else frag(c, *box)
    body = [glass(c, 0, 0, w, h, r, accent, thickness, glint=glint, glint_delay=delay), fr]
    t = f'translate({f(cx)} {f(cy)})' + (f' skewY({f(skew)})' if skew else '') + f' scale({s:.3f}) translate({f(-w / 2)} {f(-h / 2)})'
    plate = g(*body, transform=t, opacity=None if dim == 1 else f(dim))
    px, py = scr(*pxy)
    orb_mk = orb(c, px, py, port_r * s, icon_name, accent)
    if intro is not None:  # intro assembly: plate rises into place, then its port orb pops
        plate, orb_mk = c.intro(plate, 'rise', intro), c.intro(orb_mk, 'pop', intro + .45)
    geo = dict(cx=cx, cy=cy, w=w * s, h=h * s, top=cy - h * s / 2, bottom=cy + h * s / 2 + thickness * s,
               port=(px, py), acc=accent)
    return plate, orb_mk, geo


def node(c, x, y, r=3, color=CYAN, halo=4.5, core=WHITE, cls=''):
    """Glowing node: standard halo + coloured core + white centre (defined once per style)."""
    nid = c.define(('node', r, color, halo, core), lambda i: el('g', glow(c, 0, 0, r * halo, None, color, .55) +
                   el('circle', r=r, fill=color) + el('circle', r=r * .42, fill=core), id=i))
    return el('use', href=f'#{nid}', x=x, y=y, cls=cls)


def beam(c, bz, color=ELEC, width=1.4, glow=True, a0=.95, a1=.55, end_color=None, dash=None, draw=None):
    """Light beam along a Bez: wide faint under-stroke (glow) + gradient core line.
    draw=<delay s>: the beam draws on from its start during the intro (anim file only)."""
    (x0, y0), (x1, y1) = bz.start, bz.end
    dx, dy = x1 - x0, y1 - y0
    # shared bounding-box gradient per direction class (keeps files small)
    hx_, vy_ = abs(dx) >= .3 * abs(dy), abs(dy) >= .3 * abs(dx)
    gx1, gx2 = ((0, 1) if dx >= 0 else (1, 0)) if hx_ else (0, 0)
    gy1, gy2 = ((0, 1) if dy >= 0 else (1, 0)) if vy_ else (0, 0)
    grad = c.lin([(0, color, a0), (.5, end_color or color, (a0 + a1) / 2), (1, end_color or color, a1)], gx1, gy1, gx2, gy2)
    out = []
    pl = 1 if (draw is not None and c.intro_on and not dash) else None
    if glow:
        out.append(el('path', d=bz.d(), stroke=grad, stroke_width=width * 5, opacity=.13, pathLength=pl))
    out.append(el('path', d=bz.d(), stroke=grad, stroke_width=width, stroke_dasharray=dash, pathLength=pl))
    return c.intro(g(*out), 'draw', draw) if pl else g(*out)


def comet(c, path_d, still=None, color=CYAN, size=1.0, dur=3.6, delay=0, tail=22):
    """A pulse travelling along `path_d` (CSS offset-path). Still file: drawn at `still`
    = (x, y, angle_deg) or omitted when still is None."""
    def body():
        def build(i):
            s = size
            tailf = c.lin([(0, color, 0), (1, color, .95)])
            return el('g', glow(c, 0, 0, 9 * s, None, color, .7) +
                      el('ellipse', cx=-tail * s / 2, rx=tail * s / 2, ry=1.6 * s, fill=tailf) +
                      el('circle', r=2.3 * s, fill=WHITE), id=i)
        return el('use', href='#' + c.define(('comet', color, size, tail), build))
    if c.animated:
        name = c.kf('travel', '0%{offset-distance:0%;opacity:0}12%{opacity:1}82%{opacity:1}100%{offset-distance:100%;opacity:0}')
        cls = c.anim(f"offset-path:path('{path_d}');offset-rotate:auto;animation:{name} {f(dur)}s cubic-bezier(.5,0,.4,1) {f(delay)}s infinite",
                     base='opacity:0', supports="offset-path:path('M0 0')")
        return el('g', body(), cls=cls)
    if still is None:
        return ''
    x, y, a = still
    return body().replace('<use ', f'<use transform="translate({f(x)} {f(y)}) rotate({f(a)})" ', 1)


def comet_on(c, bz, t_still=.55, **kw):
    p = bz.at(t_still)
    return comet(c, bz.d(), (p[0], p[1], bz.angle(t_still)), **kw)


def rays(c, cx, cy, r0, r1, n=14, color=CYAN, op=.22, spread=2.2, start=-180, end=0, seed=3):
    """God rays: thin wedges fanning from (cx, cy) between angles start..end (deg, 0 = right,
    -90 = up), faded by one radial gradient. Pure fills, no filters."""
    rnd = random.Random(seed)
    d = []
    for i in range(n):
        a = math.radians(start + (end - start) * (i + .5) / n + rnd.uniform(-4, 4))
        w = math.radians(spread * rnd.uniform(.4, 1.2))
        p0 = (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        p1 = (cx + r1 * math.cos(a - w), cy + r1 * math.sin(a - w))
        p2 = (cx + r1 * math.cos(a + w), cy + r1 * math.sin(a + w))
        d.append(f'M{f(p0[0])} {f(p0[1])}L{f(p1[0])} {f(p1[1])}L{f(p2[0])} {f(p2[1])}Z')
    fill = c.rad([(0, color, 1), (.35, color, .5), (1, color, 0)], cx, cy, r1, user=True)
    return el('path', d=''.join(d), fill=fill, opacity=f(op))


def particles(c, cx, yb, yt, w, n=8, seed=4, color=CYAN, r=(.8, 1.8), dur=(5, 8), moving=False):
    """Motes in a light column (x within cx±w/2, from yb up to yt). Frozen at spread-out heights
    unless moving=True (rising + fading; each mote costs one loop of the budget)."""
    rnd = random.Random(seed)
    out = []
    rise = yb - yt
    name = c.kf('rise', f'0%{{transform:translateY(0);opacity:0}}15%{{opacity:1}}80%{{opacity:.8}}100%{{transform:translateY(-{f(rise)}px);opacity:0}}')
    for i in range(n):
        x = cx + rnd.uniform(-w / 2, w / 2)
        rr = rnd.uniform(*r)
        d = rnd.uniform(*dur)
        if c.animated and moving:
            cls = c.anim(f'animation:{name} {f(d)}s linear infinite', base='opacity:0')
            out.append(el('circle', cx=x, cy=yb, r=rr, fill=color, cls=cls, style=c.delay(-rnd.uniform(0, d))))
        else:
            rnd.uniform(0, 1)
            out.append(el('circle', cx=x, cy=yb - rise * (i + .5) / n, r=rr, fill=color, opacity=f(.35 + .5 * rnd.random())))
    return g(*out)


def plinth(c, cx, cy, s=1.0, top_light=True, pings=1):
    """The Estavo core plinth: 3 iso cylinder tiers, glowing top face, HUD ticks, rotating
    floor rings and ping rings. (cx, cy) = centre of the top face; s scales everything.
    Returns (markup, geometry dict with 'top', 'mid', 'base' ellipses (cx, cy, rx, ry))."""
    top = (cx, cy, 118 * s, 39 * s)
    mid = (cx, cy + 22 * s, 156 * s, 51 * s)
    base = (cx, cy + 46 * s, 196 * s, 64 * s)
    out = [glow(c, cx, cy + 76 * s, 300 * s, 96 * s, ELEC, .5)]
    for i in range(int(pings)):
        out.append(ping(c, cx, cy + 58 * s, 220 * s, 72 * s, CYAN if i % 2 == 0 else ELEC, dur=4.8, delay=2.4 * i))
    out.append(iso_disc(c, *base, 22 * s, rim=ELEC, rim_op=.7))
    tick = ''.join(f'M{f(cx + base[2] * math.cos(math.radians(a)))} {f(base[1] + 22 * s + base[3] * math.sin(math.radians(a)))}v{f(-7 * s)}'
                   for a in range(20, 161, 8))
    out.append(el('path', d=tick, stroke=CYAN, stroke_width=1, opacity=.45))
    out.append(iso_disc(c, *mid, 20 * s, rim=CYAN, rim_op=.75))
    tf = c.rad([(0, CYAN, .95), (.35, ELEC, .75), (.8, '#163e69'), (1, '#12345a')]) if top_light else None
    out.append(iso_disc(c, *top, 16 * s, top=tf, rim=WHITE, rim_op=.9))
    k = top[3] / top[2]
    out.append(spin_ring(c, cx, cy, 96 * s, k=k, color=WHITE, width=1.1, dash='2 9', opacity=.7))
    out.append(spin_ring(c, cx, cy, 70 * s, k=k, color=CYAN, width=1.4, dash='14 6 2 6', opacity=.85))
    return g(*out), dict(top=top, mid=mid, base=base)


def floating_mark(c, cx, y, w, depth=6):
    """The Estavo mark floating over the core: halo, stacked extrusion, white-to-cyan face,
    luminous outline, slow float + halo breath when animated. y = top of the mark."""
    mh = w * MARK_H / MARK_W
    mx = cx - w / 2
    float_cls = c.anim(f'animation:{c.kf("float", "0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}")} 7s ease-in-out infinite')
    out = [glow(c, cx, y + mh / 2, w * 1.17, w * .84, ELEC, .5), glow(c, cx, y + mh / 2, w * .56, w * .37, CYAN, .35)]
    ext = c.lin([(0, '#2f78c4'), (1, '#0f3358')])
    step = w / 107
    for i in range(depth, 0, -1):
        out.append(mark(c, mx, y + i * step, w, ext))
    out.append(mark(c, mx, y, w, c.lin([(0, WHITE), (.55, '#d8f1ff'), (1, '#8fd6ff')])))
    out.append(mark(c, mx, y, w, 'none', stroke=WHITE, stroke_width=3, stroke_opacity=.55))
    return g(*out, cls=float_cls)


def floating_glyph(c, cx, cy, size, ring=True):
    """Estavo's four-point AI glyph as a luminous core: halo, extrusion, white-to-cyan face,
    outline and a tilted halo ring passing behind and in front of it. (cx, cy) = centre."""
    float_cls = c.anim(f'animation:{c.kf("float", "0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}")} 7s ease-in-out infinite')
    out = [glow(c, cx, cy, size * 1.5, size * 1.3, ELEC, .55), glow(c, cx, cy, size * .7, size * .7, CYAN, .5)]
    rx, ry, rot = size * .95, size * .24, -14
    if ring:
        out.append(el('path', d=f'M{f(cx - rx)} {f(cy)}A{f(rx)} {f(ry)} 0 0 1 {f(cx + rx)} {f(cy)}', stroke=c.lin([(0, CYAN, .15), (.5, CYAN, .5), (1, CYAN, .15)]),
                      stroke_width=1.4, transform=f'rotate({rot} {f(cx)} {f(cy)})'))
    ext = c.lin([(0, '#2f78c4'), (1, '#0f3358')])
    step = size / 70
    for i in range(6, 0, -1):
        out.append(ai_glyph(c, cx, cy + i * step, size, ext))
    out.append(ai_glyph(c, cx, cy, size, c.lin([(0, WHITE), (.5, '#d8f1ff'), (1, '#7fdcff')])))
    out.append(ai_glyph(c, cx, cy, size, 'none', stroke=WHITE, stroke_opacity=.6, stroke_width=f(1.2 * 19 / size)))
    out.append(glow(c, cx, cy, size * .16, None, WHITE, .9))
    if ring:
        out.append(el('path', d=f'M{f(cx - rx)} {f(cy)}A{f(rx)} {f(ry)} 0 0 0 {f(cx + rx)} {f(cy)}',
                      stroke=c.lin([(0, CYAN, .2), (.5, WHITE, .95), (1, CYAN, .2)]), stroke_width=1.8, transform=f'rotate({rot} {f(cx)} {f(cy)})'))
        p = ellipse_pt(cx, cy, rx, ry, 70, rot)
        out.append(node(c, p[0], p[1], 2.4, CYAN, 3.5))
    return g(*out, cls=float_cls)


# ── Icons, marks, numerals ─────────────────────────────────────────────
_SYMBOLS = None


def _symbols():
    global _SYMBOLS
    if _SYMBOLS is None:
        text = SPRITE_PATH.read_text()
        _SYMBOLS = {m.group(1): m.group(2) for m in re.finditer(r'<symbol id="([^"]+)"[^>]*>([\s\S]*?)</symbol>', text)}
    return _SYMBOLS


def icon(c, name, x, y, size, color=WHITE, duo=None, duo_o=.3, sw=1.6, opacity=None):
    """Sprite icon `i-<name>` (or full id) drawn at (x, y) top-left, size px square.
    Each icon is copied once into <defs> as a <symbol>; every use is a <use>."""
    sid = name if name.startswith('i-') else f'i-{name}'
    inner = _symbols()[sid]
    if not duo:  # mono use: drop the duotone fill layer (smaller file, crisper at small sizes)
        inner = re.sub(r'<(path|circle|rect|ellipse)[^>]*style="fill:var\(--fx-duo[^"]*"[^>]*/>', '', inner)
    # (round caps/joins are inherited from the root <svg>)
    ref = c.define(('ico', sid, bool(duo)), lambda i: el('symbol', inner, id=i, viewBox='0 0 24 24', fill='none', stroke='currentColor'))
    style = f'--fx-duo:{hx(duo)};--fx-duo-o:{duo_o}' if duo else None
    t = None
    if c.flip % 2:  # counter-flip inside mirrored(): x -> -(x+size) under scale(-1 1)
        x, t = -(x + size), 'scale(-1 1)'
    return el('use', href=f'#{ref}', x=x, y=y, width=size, height=size, stroke_width=sw, color=hx(color), style=style, opacity=opacity,
              transform=t)


_MARK = None


def _mark_d():
    global _MARK
    if _MARK is None:
        _MARK = re.search(r'<path d="([^"]+)"', MARK_PATH.read_text()).group(1)
    return _MARK


MARK_W, MARK_H = 600, 347


def mark(c, x, y, w, fill=WHITE, **a):
    """Estavo mark, top-left at (x, y), width w (height = w * 347/600). Defined once, reused."""
    mid = c.define('mark', lambda i: el('path', id=i, d=_mark_d(), fill_rule='evenodd'))
    s = w / MARK_W
    return el('use', href=f'#{mid}', transform=f'translate({f(x)} {f(y)}) scale({s:.4f})', fill=fill, **a)


AI_D = 'M12 2.5C13.06 7.78 16.22 10.94 21.5 12C16.22 13.06 13.06 16.22 12 21.5C10.94 16.22 7.78 13.06 2.5 12C7.78 10.94 10.94 7.78 12 2.5Z'


def ai_glyph(c, cx, cy, size, fill=CYAN, **a):
    s = size / 19  # glyph spans 2.5..21.5
    return el('path', d=AI_D, transform=f'translate({f(cx - 12 * s)} {f(cy - 12 * s)}) scale({s:.4f})', fill=fill, **a)


# Monoline HUD glyphs on a 4 x 6 box (y down). (advance, path)
GLYPHS = {
    '0': (4, 'M0 2A2 2 0 0 1 4 2V4A2 2 0 0 1 0 4Z'),
    '1': (3, 'M.6 1.3 2.2 0V6'),
    '2': (4, 'M.1 1.6A1.95 1.75 0 0 1 4 1.8C4 3.2.4 4.3 0 6H4'),
    '3': (4, 'M.3 0H3.8L1.8 2.5A1.9 1.8 0 1 1 .1 5.2'),
    '4': (4, 'M3 6V0L0 4.2H4'),
    '5': (4, 'M3.7 0H.6L.2 2.7A2 1.8 0 1 1 .1 5.3'),
    '6': (4, 'M3.2.2C1.4 0 0 1.4 0 4M0 4A2 2 0 1 0 4 4A2 2 0 1 0 0 4'),
    '7': (4, 'M0 0H4L1.4 6'),
    '8': (4, 'M2 2.8A1.7 1.4 0 1 1 2 0A1.7 1.4 0 1 1 2 2.8A2 1.6 0 1 1 2 6A2 1.6 0 1 1 2 2.8'),
    '9': (4, 'M.8 5.8C2.6 6 4 4.6 4 2M4 2A2 2 0 1 0 0 2A2 2 0 1 0 4 2'),
    '.': (1, 'M.5 6H.51'),
    ',': (1, 'M.6 5.6.2 6.8'),
    ':': (1, 'M.5 1.8H.51M.5 5.6H.51'),
    'M': (4.6, 'M0 6V0L2.3 3.8 4.6 0V6'),
    'K': (3.8, 'M0 0V6M3.8 0 .1 3.6M1.5 2.3 3.8 6'),
    'Q': (4.4, 'M0 2A2 2 0 0 1 4 2V4A2 2 0 0 1 0 4ZM2.7 4.7 4.4 6.4'),
    'Y': (4, 'M0 0 2 3 4 0M2 3V6'),
    '%': (4.4, 'M0 6 4.4 0M.9 1.1H.91M3.5 4.9H3.51'),
    '/': (3, 'M0 6 3 0'),
    '+': (4, 'M2 1.2V4.8M.2 3H3.8'),
    '-': (3, 'M.2 3H2.8'),
    'x': (3.4, 'M.2 2.4 3.2 6M3.2 2.4.2 6'),
    'm': (5, 'M0 6V2.6M0 3.6A1.25 1.2 0 0 1 2.5 3.6V6M2.5 3.6A1.25 1.2 0 0 1 5 3.6V6'),
    ' ': (2, ''),
}


def hud_width(text, size, track=1.4):
    s = size / 6
    return sum((GLYPHS[ch][0] + track) for ch in text) * s - track * s


def hud(c, text, x, y, size=10, color=WHITE, anchor='start', sw=None, opacity=None, track=1.4):
    """Vector numerals (no fonts). (x, y) = baseline-left (or centre/end per anchor); size = cap height."""
    s = size / 6
    w = hud_width(text, size, track)
    if anchor == 'middle':
        x -= w / 2
    elif anchor == 'end':
        x -= w
    sw = sw or max(1.0, size * .15)
    parts, ax = [], 0
    for ch in text:
        adv, d = GLYPHS[ch]
        if d:
            gid = c.define(('glyph', ch), lambda i, d=d: el('path', id=i, d=d, stroke_linejoin='round'))
            parts.append(el('use', href=f'#{gid}', x=f(ax) if ax else None))
        ax += adv + track
    t = f'translate({f(x)} {f(y - size)}) scale({s:.3f})'
    if c.flip % 2:  # keep numerals readable inside a mirrored fragment
        t = f'translate({f(x + w)} {f(y - size)}) scale({-s:.3f} {s:.3f})'
    return el('g', ''.join(parts), transform=t, stroke=hx(color),
              stroke_width=f(sw / s), opacity=opacity)


def mirrored(c, x, w, draw):
    """RTL helper: draw() inside a horizontal mirror of the box [x, x+w]. Numerals (hud) and
    sprite icons counter-flip so they stay readable; layout (start/end) swaps. Use it for
    direction-sensitive fragments (chat, cards, lists) in -rtl scene variants."""
    c.flip += 1
    try:
        body = draw()
    finally:
        c.flip -= 1
    return el('g', body, transform=f'translate({f(2 * x + w)} 0) scale(-1 1)')


def bar(x, y, w, h=5, color=WHITE, op=.5, r=None):
    return el('rect', x=x, y=y, width=w, height=h, rx=h / 2 if r is None else r, fill=color, opacity=f(op))


def lines(x, y, widths, h=4.5, gap=8, color=WHITE, ops=(.78, .38, .3), end=False, box_w=None):
    """Skeleton text lines: round-capped strokes sharing one group (compact output)."""
    out = []
    for i, w in enumerate(widths):
        xx = x + (box_w - w) if end and box_w else x
        yy = y + i * gap + h / 2
        out.append(el('path', d=f'M{f(xx + h / 2)} {f(yy)}h{f(max(.01, w - h))}', opacity=f(ops[min(i, len(ops) - 1)])))
    return el('g', ''.join(out), stroke=color, stroke_width=f(h))


def chip(c, x, y, w, h, fill=ELEC, text=None, text_color=WHITE, size=None, stroke=None, op=1, glow=True):
    """Pill chip with optional HUD numerals centred."""
    out = []
    if glow and fill not in (None, 'none'):
        out.append(el('rect', x=x - 3, y=y - 3, width=w + 6, height=h + 6, rx=(h + 6) / 2, fill=fill, opacity=.16))
    out.append(el('rect', x=x, y=y, width=w, height=h, rx=h / 2, fill=fill if fill else 'none', stroke=stroke,
                  stroke_width=1 if stroke else None, opacity=None if op == 1 else f(op)))
    if text:
        sz = size or h * .46
        out.append(hud(c, text, x + w / 2, y + h / 2 + sz / 2, sz, text_color, 'middle'))
    return g(*out)


def signal(c, x, y, color=MINT, live=True):
    """Header status: glowing dot + 3 rising bars (end-anchored at x)."""
    out = [bar(x - 4 - i * 5, y + 4 - i * 2.5, 3, 4 + i * 2.5, WHITE, .28 + i * .14, 1) for i in range(3)]
    out.append(glow(c, x - 22, y + 4, 6, None, color, .6))
    if live:
        name = c.kf('blink', '0%,100%{opacity:1}50%{opacity:.35}')
        cls = c.anim(f'animation:{name} 2.4s ease-in-out infinite')
    else:
        cls = ''
    out.append(el('circle', cx=x - 22, cy=y + 4, r=2.4, fill=color, cls=cls))
    return g(*out)


def thumb(c, x, y, w, h, r=6, seed=1, accent=ELEC):
    """Photo-free project thumbnail: dusk gradient, sun, two iso towers in light lines.
    Defined once per (w, h, r, seed) at the origin and placed with <use>."""
    def build(i):
        x = y = 0
        cp = c.clip(el('rect', x=x, y=y, width=w, height=h, rx=r))
        sky = c.lin([(0, '#3b7fc4'), (.6, '#1b4b7c'), (1, '#0f2e50')])
        s = min(h / 56, w / 62)
        o = (x + w * .5, y + h - 2 * s)
        towers = (iso_block(c, o, -14, -2, 0, 16, 14, 36 + seed * 3, top='#8cc4f5', left='#2f679e', right='#1d4a78', k=.5, s=s) +
                  iso_block(c, o, 6, -16, 0, 14, 12, 24, top='#a9d5fa', left='#3a76b0', right='#24578a', k=.5, s=s))
        win = []
        for j in range(4):
            px, py = iso(-14 + 16, 3 + j * 2.8, 8 + j * 7, o, s, .5)
            win.append(f'M{f(px - 3 * s)} {f(py)}h{f(5 * s)}')
        return el('g', g(el('rect', x=x, y=y, width=w, height=h, fill=sky),
                 el('circle', cx=x + w * .78, cy=y + h * .3, r=h * .14, fill=c.rad([(0, '#fff3d6'), (.5, '#ffd99a', .8), (1, '#ffd99a', 0)])),
                 el('rect', x=x, y=y + h * .78, width=w, height=h * .22, fill='#0b2440', opacity=.6),
                 towers, el('path', d=''.join(win), stroke=CYAN, stroke_width=1, opacity=.8),
                 el('rect', x=x, y=y, width=w, height=h * .5, fill=c.lin([(0, WHITE, .14), (1, WHITE, 0)])),
                 clip_path=cp) + el('rect', x=x + .5, y=y + .5, width=w - 1, height=h - 1, rx=r, stroke=WHITE, stroke_opacity=.22), id=i)
    tid = c.define(('thumb', round(w, 1), round(h, 1), r, seed), build)
    return el('use', href=f'#{tid}', x=x, y=y)


# ── Fragments: real product structures ─────────────────────────────────
def frag_project(c, x, y, w, h, price='8.0M', area='158', beds='3', accent=ELEC, down='1.2M'):
    tw = min(w * .4, h * 1.1)
    out = [thumb(c, x, y, tw, h, 7, accent=accent)]
    tx = x + tw + 12
    rw = w - tw - 12
    out.append(lines(tx, y + 3, [rw * .82, rw * .55], h=5, gap=11))
    iy = y + 26
    out.append(icon(c, 'bed', tx, iy, 12, CYAN, sw=1.8))
    out.append(hud(c, beds, tx + 15, iy + 9.5, 7, WHITE, opacity=.85))
    out.append(icon(c, 'area', tx + 30, iy, 12, CYAN, sw=1.8))
    out.append(hud(c, area, tx + 45, iy + 9.5, 7, WHITE, opacity=.85))
    ch = 18
    out.append(chip(c, tx, y + h - ch, min(rw, 62), ch, fill=c.lin([(0, '#6db0ff'), (1, '#2f7fd8')]), text=price, size=8))
    if down and rw > 90:
        out.append(chip(c, tx + 70, y + h - ch, min(rw - 70, 50), ch, fill=None, stroke=MINT, text=down, text_color=MINT, size=7, glow=False))
    return g(*out)


def frag_payment(c, x, y, w, h, down='1.2M', n=12, accent=MINT):
    base = y + h
    out = [el('path', d=f'M{f(x)} {f(base)}H{f(x + w)}', stroke=WHITE, stroke_opacity=.25)]
    dw, dh = w * .17, h * .72
    out.append(el('rect', x=x, y=base - dh, width=dw, height=dh, rx=3, fill=c.lin([(0, MINT), (1, '#2fae86', .55)])))
    out.append(el('rect', x=x, y=base - dh, width=dw, height=2, rx=1, fill=WHITE, opacity=.7))
    out.append(chip(c, x - 2, base - dh - 18, dw + 18, 14, fill=None, stroke=MINT, text=down, text_color=MINT, size=6.5, glow=False))
    gx = x + dw + 6
    bw = (x + w - gx) / n
    pts = [(x + dw, base - dh)]
    for i in range(n):
        bh = h * .26
        bx = gx + i * bw
        out.append(el('rect', x=bx + bw * .18, y=base - bh, width=bw * .64, height=bh, rx=1.6,
                      fill=c.lin([(0, '#7fb8ff'), (1, ELEC, .35)])))
        pts.append((bx + bw * .5, base - dh - (h * .18) * (i + 1) / n - 2))
    d = 'M' + 'L'.join(f'{f(px)} {f(py)}' for px, py in [pts[0]] + [(p[0], base - h * .3 - (h * .55) * (i + 1) / n) for i, p in enumerate(pts[1:])])
    out.append(el('path', d=d, stroke=CYAN, stroke_width=1.4, stroke_linejoin='round', opacity=.9))
    out.append(hud(c, 'Q1', gx + bw * .5, base + 10, 5.5, WHITE, 'middle', opacity=.6))
    return g(*out)


def frag_jobs(c, x, y, w, h, accent=ELEC):
    """Jobs board: a job card (employer tile, title, location, the source site as a globe chip)
    with the arrow-up-right 'apply on the original site' button, and the next card behind it."""
    out = []
    ch = h * .7
    for k, (dx, dy, op) in enumerate(((14, 0, .45), (0, h - ch, 1))):
        cx, cy, cw = x + dx, y + dy, w - 14
        card = [el('rect', x=cx, y=cy, width=cw, height=ch, rx=9, fill='#0d2c4d',
                   stroke=c.lin([(0, WHITE, .42), (1, accent, .2)]), stroke_width=1)]
        if k == 0:  # back card: only its top strip shows
            card.append(el('rect', x=cx + 8, y=cy + 7, width=12, height=12, rx=3.5, fill='#2a5e95'))
            card.append(bar(cx + 26, cy + 10, cw * .38, 4.5, WHITE, .5))
            out.append(g(*card, opacity=f(op)))
            continue
        sq = 26
        card.append(el('rect', x=cx + 9, y=cy + 9, width=sq, height=sq, rx=7, fill=c.lin([(0, '#3a86d8'), (1, '#1a4f86')])))
        card.append(icon(c, 'briefcase', cx + 9 + sq * .18, cy + 9 + sq * .18, sq * .64, WHITE, sw=1.8))
        lx = cx + sq + 17
        card.append(bar(lx, cy + 12, (cw - sq - 60) * .9, 5, WHITE, .85))
        card.append(icon(c, 'pin', lx - 1, cy + 22, 11, CYAN, sw=2))
        card.append(icon(c, 'clock', lx + 15, cy + 22, 11, CYAN, sw=2, opacity=.75))
        # source chip: globe + host line
        sy = cy + ch - 21
        card.append(el('rect', x=cx + 9, y=sy, width=cw * .5, height=13, rx=6.5, fill=WHITE, fill_opacity=.06,
                       stroke=CYAN, stroke_opacity=.45))
        card.append(icon(c, 'globe', cx + 12, sy + 1.5, 10, CYAN, sw=2))
        card.append(bar(cx + 26, sy + 4.5, cw * .5 - 24, 4, WHITE, .45))
        # apply on the original site
        ax, ay, ar = cx + cw - 19, cy + ch - 19, 11
        card.append(glow(c, ax, ay, ar * 2, None, MINT, .3))
        card.append(el('circle', cx=ax, cy=ay, r=ar, fill=MINT))
        card.append(icon(c, 'arrow-up-right', ax - 7, ay - 7, 14, DEEP, sw=2.4))
        out.append(g(*card))
    return g(*out)


def frag_chat(c, x, y, w, h, rows=(('7.9M', '1.4M'), ('8.0M', '1.2M'), ('8.3M', '1.5M')), best=1, over=(2,)):
    """Brokers AI exchange. The broker's bubble carries the request as tokens (3 bedrooms, area,
    8M cap); the AI answers with price + down-payment pairs. Example = home fixture: B is best on
    the LOWEST DOWN PAYMENT (mint wallet chip), C's price is over the 8M cap (amber)."""
    out = []
    bh = 18
    bw = min(w * .66, 116)
    bx = x + w - bw
    out.append(el('rect', x=bx, y=y, width=bw, height=bh, rx=bh / 2, fill=c.lin([(0, '#3f8ce8'), (1, '#2363ad')])))
    out.append(icon(c, 'bed', bx + 9, y + 3, 12, WHITE, sw=1.8))
    out.append(hud(c, '3', bx + 24, y + 12.5, 7, WHITE))
    out.append(icon(c, 'pin', bx + 36, y + 3, 12, WHITE, sw=1.8))
    out.append(icon(c, 'wallet', bx + 52, y + 3, 12, MINT, sw=1.8))
    out.append(hud(c, '8M', bx + bw - 9, y + 12.5, 7, WHITE, 'end'))
    ay = y + bh + 7
    out.append(el('circle', cx=x + 8, cy=ay + 8, r=8, fill='#0d2c4d', stroke=CYAN, stroke_width=1))
    out.append(ai_glyph(c, x + 8, ay + 8, 9, CYAN))
    rx0, rw = x + 22, w - 22
    gap = 4
    rh = min(21, (y + h - ay - gap * (len(rows) - 1)) / len(rows))
    cw = 40
    for i, (price, down) in enumerate(rows):
        yy = ay + i * (rh + gap)
        hl, ov = i == best, i in over
        out.append(el('rect', x=rx0, y=yy, width=rw, height=rh, rx=6, fill=MINT if hl else '#0d2c4d', fill_opacity=.14 if hl else None,
                      stroke=MINT if hl else WHITE, stroke_opacity=None if hl else .14))
        out.append(chip(c, rx0 + 4, yy + (rh - 14) / 2, cw, 14, fill=None, stroke=AMBER if ov else '#6f95bf', text=price,
                        text_color=AMBER if ov else WHITE, size=6.5, glow=False))
        dx = rx0 + rw - 4 - cw
        out.append(icon(c, 'wallet', dx - 15, yy + rh / 2 - 6, 12, MINT if hl else CYAN, sw=1.9, opacity=None if hl else .6))
        out.append(chip(c, dx, yy + (rh - 14) / 2, cw, 14, fill=MINT if hl else None, stroke=None if hl else '#6f95bf', text=down,
                        text_color=DEEP if hl else WHITE, size=6.5, glow=hl))
        if hl:
            out.append(icon(c, 'check-circle', rx0 + cw + 10, yy + rh / 2 - 6, 12, MINT, sw=2))
    return g(*out)


def frag_pdf(c, x, y, w, h, accent=ELEC):
    fold = min(w, h) * .2
    d = f'M{f(x)} {f(y)}H{f(x + w - fold)}L{f(x + w)} {f(y + fold)}V{f(y + h)}H{f(x)}Z'
    out = [el('path', d=d, fill=c.lin([(0, '#f4f8fd'), (1, '#d9e6f3')])),
           el('path', d=f'M{f(x + w - fold)} {f(y)}V{f(y + fold)}H{f(x + w)}', fill='#b8cde3'),
           el('rect', x=x + 7, y=y + 8, width=w * .35, height=5, rx=2.5, fill=BLUE),
           thumb(c, x + 7, y + 18, w - 14, h * .34, 3)]
    ty = y + 22 + h * .34
    for i in range(3):
        out.append(el('rect', x=x + 7, y=ty + i * 8, width=w - 14, height=5, rx=1.5, fill=BLUE, opacity=f(.16 if i % 2 else .3)))
    out.append(el('rect', x=x + w - 24, y=y + h - 12, width=17, height=7, rx=2, fill=ELEC))
    return g(*out)


def frag_browser(c, x, y, w, h, accent=ELEC):
    """The broker's own website: browser frame, header with the broker's logo square, name and
    contact chip, a featured listing tile (photo-free thumb + 8.0M price chip), the site's AI
    assistant bubble."""
    out = [el('rect', x=x, y=y, width=w, height=h, rx=7, fill='#0a2340', stroke=WHITE, stroke_opacity=.24)]
    out.append(el('path', d=f'M{f(x)} {f(y + 13)}H{f(x + w)}', stroke=WHITE, stroke_opacity=.14))
    out.append(el('rect', x=x + w * .26, y=y + 3.5, width=w * .48, height=6.5, rx=3.25, fill=WHITE, opacity=.1))
    out.append(icon(c, 'lock', x + w * .26 + 2, y + 3.5, 6.5, MINT, sw=2.4))
    hy = y + 17
    out.append(el('rect', x=x + 5, y=hy, width=17, height=17, rx=5, fill=c.lin([(0, WHITE), (1, '#cfe6ff')])))
    out.append(icon(c, 'home', x + 7.5, hy + 2.5, 12, BLUE, sw=2.2))
    out.append(bar(x + 27, hy + 3.5, w * .34, 5, WHITE, .9))
    out.append(bar(x + 27, hy + 11, w * .2, 3.5, WHITE, .4))
    out.append(el('rect', x=x + w - 34, y=hy + 3, width=29, height=11, rx=5.5, fill=MINT, fill_opacity=.2, stroke=MINT, stroke_opacity=.7))
    out.append(icon(c, 'whatsapp-like', x + w - 25, hy + 4, 9, MINT, sw=2.2))
    ly = hy + 22
    lh = y + h - ly - 5
    tw = (w - 10) * .58
    out.append(thumb(c, x + 5, ly, tw, lh, 4, seed=1))
    out.append(chip(c, x + 9, ly + lh - 15, 38, 12, fill=c.lin([(0, '#6db0ff'), (1, '#2f7fd8')]), text='8.0M', size=6))
    cx_ = x + 9 + tw
    cw_ = x + w - 5 - cx_
    out.append(icon(c, 'bed', cx_, ly + 1, 10, CYAN, sw=2))
    out.append(hud(c, '3', cx_ + 12, ly + 9, 6, WHITE, opacity=.85))
    out.append(icon(c, 'area', cx_, ly + 14, 10, CYAN, sw=2))
    out.append(hud(c, '158', cx_ + 12, ly + 22, 6, WHITE, opacity=.85))
    ax, ay = x + w - 12, y + h - 12
    out.append(glow(c, ax, ay, 12, None, CYAN, .55))
    out.append(el('circle', cx=ax, cy=ay, r=8, fill=DEEP, stroke=CYAN, stroke_width=1.3))
    out.append(ai_glyph(c, ax, ay, 9, CYAN))
    out.append(el('rect', x=cx_, y=ay - 5.5, width=max(4, ax - 11 - cx_), height=11, rx=5.5, fill='#12355a', stroke=CYAN, stroke_opacity=.45))
    out.append(bar(cx_ + 4, ay - 1.5, max(2, (ax - 11 - cx_) * .6), 3, WHITE, .55))
    return g(*out)


def frag_news(c, x, y, w, h, accent=CYAN):
    """Market news stream: a dated spine (ticks, no dates) and three stories, each tagged by
    kind with an icon pill: launch (mint, newest), developer news, payment-plan change."""
    sx = x + 5
    out = [el('path', d=f'M{f(sx)} {f(y + 2)}V{f(y + h - 2)}', stroke=c.lin([(0, accent, .9), (1, accent, .12)]), stroke_width=1.3)]
    out.append(el('path', d=''.join(f'M{f(sx - 2.5)} {f(y + 4 + k * (h - 8) / 9)}h5' for k in range(10)), stroke=accent, stroke_width=1, opacity=.4))
    rh = h / 3
    tags = (('launch', MINT), ('developers', ELEC), ('installments', CYAN))
    for i, (ic, col) in enumerate(tags):
        ry = y + i * rh
        cy = ry + rh / 2
        out.append(el('circle', cx=sx, cy=cy, r=3.4 if i == 0 else 2.4, fill=col if i == 0 else accent, opacity=1 if i == 0 else .7))
        if i == 0:
            out.append(glow(c, sx, cy, 9, None, MINT, .5))
        px, pw, ph = x + 15, 30, rh - 9
        out.append(el('rect', x=px, y=cy - ph / 2, width=pw, height=ph, rx=ph / 2, fill=col, fill_opacity=.16 if i else .22,
                      stroke=col, stroke_opacity=.75 if i == 0 else .5))
        out.append(icon(c, ic, px + pw / 2 - ph * .36, cy - ph * .36, ph * .72, col if i else MINT, sw=2))
        lx = px + pw + 8
        lw = x + w - lx
        out.append(lines(lx, cy - 7, [lw * (.92 if i == 0 else .78), lw * .48], h=4.5, gap=9, ops=(.88 if i == 0 else .55, .3)))
    return g(*out)


def frag_game(c, x, y, w, h, accent=AMBER):
    """«إكسكلوسيف» round: round counter 3/5 with 5 pips, the round timer ring, the question card,
    and the judged answers: one exclusive answer (mint, 100), two players who gave the same answer
    (linked, 0 each) and one blank (0). Matches the real scoring rule."""
    out = [hud(c, '3/5', x, y + 8, 8, accent)]
    pw = 13
    px0 = x + hud_width('3/5', 8) + 8
    for i in range(5):
        out.append(el('rect', x=px0 + i * (pw + 3), y=y + 2.5, width=pw, height=4, rx=2, fill=accent if i < 3 else WHITE,
                      opacity=1 if i < 2 else .55 if i == 2 else .18))
    tr_, tx, ty = 8.5, x + w - 9, y + 5
    out.append(el('circle', cx=tx, cy=ty, r=tr_, stroke=WHITE, stroke_opacity=.2, stroke_width=2.2))
    out.append(el('circle', cx=tx, cy=ty, r=tr_, stroke=accent, stroke_width=2.2, pathLength=100, stroke_dasharray='64 100',
                  stroke_linecap='round', transform=f'rotate(-90 {f(tx)} {f(ty)})'))
    out.append(el('path', d=f'M{f(tx)} {f(ty - 4)}V{f(ty)}l2.6 1.8', stroke=WHITE, stroke_width=1.3, opacity=.85))
    qy = y + 18
    qh = h * .26
    out.append(el('rect', x=x, y=qy, width=w, height=qh, rx=7, fill='#0d2c4d', stroke=accent, stroke_opacity=.5))
    out.append(icon(c, 'question', x + 6, qy + qh / 2 - 6.5, 13, accent, sw=2))
    out.append(lines(x + 25, qy + qh / 2 - 6.5, [w * .62, w * .38], h=4.2, gap=8.5, ops=(.85, .4)))
    oy = qy + qh + 6
    ow, oh = (w - 8) / 2, (y + h - oy - 5) / 2
    for i in range(4):  # top: exclusive (mint) + blank; bottom: the same answer twice (amber, linked)
        ox = x + (i % 2) * (ow + 8)
        yy = oy + (i // 2) * (oh + 5)
        win, blank, rep_ = i == 0, i == 1, i >= 2
        col = MINT if win else AMBER if rep_ else WHITE
        out.append(el('rect', x=ox, y=yy, width=ow, height=oh, rx=oh / 2, fill=MINT if win else '#12355a', fill_opacity=.2 if win else None,
                      stroke=col, stroke_opacity=.55 if rep_ else None if win else .25, stroke_dasharray='3 3' if blank else None))
        if win:
            out.append(icon(c, 'crown', ox + 6, yy + oh / 2 - 6, 12, MINT, sw=2))
        elif rep_:
            out.append(bar(ox + 8, yy + oh / 2 - 2, ow * .36, 4, WHITE, .5))
        out.append(hud(c, '100' if win else '0', ox + ow - 8, yy + oh / 2 + 3.5, 7, MINT if win else AMBER if rep_ else WHITE, 'end',
                       opacity=None if win else .8 if rep_ else .45))
    ly = oy + oh + 5 + oh / 2
    out.append(el('path', d=f'M{f(x + ow - 3)} {f(ly)}H{f(x + ow + 11)}', stroke=AMBER, stroke_width=1.6, stroke_dasharray='2 2'))
    return g(*out)


def frag_developer(c, x, y, w, h, accent=ELEC):
    out = []
    r = h * .2
    cx, cy = x + r + 1, y + r + 1
    out.append(glow(c, cx, cy, r + 3, None, accent, .45))
    out.append(el('circle', cx=cx, cy=cy, r=r, fill='#0d2c4d', stroke=c.lin([(0, CYAN), (1, accent, .3)]), stroke_width=1.6))
    out.append(icon(c, 'building', cx - r * .55, cy - r * .55, r * 1.1, WHITE, sw=1.8, opacity=.85))
    lx = x + 2 * r + 12
    out.append(lines(lx, y + 3, [(w - 2 * r - 12) * .7], h=5.5, ops=(.85,)))
    out.append(icon(c, 'pin', lx - 1, y + 13, 10, CYAN, sw=2))
    out.append(bar(lx + 11, y + 16, (w - 2 * r - 12) * .35, 4, WHITE, .35))
    out.append(icon(c, 'phone', lx - 1, y + 26, 10, MINT, sw=2))
    for i in range(4):
        out.append(el('circle', cx=lx + 14 + i * 6, cy=y + 31, r=1.6, fill=WHITE, opacity=.5))
    ty = y + 2 * r + 10
    tw = (w - 12) / 3
    for i in range(3):
        out.append(thumb(c, x + i * (tw + 6), ty, tw, y + h - ty, 4, seed=0))
    return g(*out)


def frag_compare(c, x, y, w, h, best=1, accent=MINT):
    out = []
    cw = (w - 12) / 3
    for i in range(3):
        cx = x + i * (cw + 6)
        hl = i == best
        out.append(el('rect', x=cx, y=y, width=cw, height=h, rx=6, fill=MINT if hl else '#0d2c4d', fill_opacity=.14 if hl else None,
                      stroke=MINT if hl else WHITE, stroke_opacity=None if hl else .16, stroke_width=1.2 if hl else 1))
        out.append(el('rect', x=cx + 4, y=y + 4, width=cw - 8, height=h * .3, rx=3, fill='#2a5e95'))
        for j in range(3):
            out.append(bar(cx + 5, y + h * .3 + 10 + j * 8, (cw - 10) * (.8 - .15 * j), 3.5, MINT if (hl and j == 0) else WHITE, .8 if hl else .35))
    return g(*out)


def frag_calendar(c, x, y, w, h, accent=ELEC, pick=(3, 2)):
    out = [el('rect', x=x, y=y, width=w, height=9, rx=3, fill=ELEC, opacity=.55)]
    cols, rows = 7, 4
    cw, rh = w / cols, (h - 13) / rows
    for r_ in range(rows):
        for k in range(cols):
            px, py = x + k * cw + cw / 2, y + 13 + r_ * rh + rh / 2
            if (k, r_) == pick:
                out.append(el('circle', cx=px, cy=py, r=min(cw, rh) * .46, fill=MINT, opacity=.25))
                out.append(el('circle', cx=px, cy=py, r=min(cw, rh) * .46, stroke=MINT, stroke_width=1.2))
                out.append(el('circle', cx=px, cy=py, r=1.8, fill=MINT))
            else:
                out.append(el('circle', cx=px, cy=py, r=1.3, fill=WHITE, opacity=.35))
    return g(*out)


def frag_launch(c, x, y, w, h, year='2027', accent=ELEC):
    out = [thumb(c, x, y, w, h * .62, 6, seed=2)]
    out.append(chip(c, x + 5, y + 5, 22, 9, fill=MINT, op=.95))
    out.append(lines(x, y + h * .62 + 7, [w * .6], h=4.5, ops=(.8,)))
    out.append(chip(c, x + w - 40, y + h - 12, 40, 12, fill=None, stroke=CYAN, text=year, text_color=CYAN, size=6, glow=False))
    return g(*out)


def frag_search(c, x, y, w, h, accent=ELEC):
    """Project search: query field with search icon, 3 filter chips, two result rows."""
    out = [el('rect', x=x, y=y, width=w, height=18, rx=9, fill=WHITE, opacity=.95)]
    out.append(icon(c, 'search', x + 6, y + 4, 10, BLUE, sw=2.4))
    out.append(bar(x + 21, y + 7, w * .45, 4, BLUE, .45))
    cw = (w - 12) / 3
    for i in range(3):
        out.append(el('rect', x=x + i * (cw + 6), y=y + 24, width=cw, height=11, rx=5.5,
                      fill=ELEC if i == 0 else 'none', fill_opacity=.3 if i == 0 else None,
                      stroke=ELEC if i == 0 else WHITE, stroke_opacity=None if i == 0 else .25))
        out.append(bar(x + i * (cw + 6) + 7, y + 28, cw * .5, 3, WHITE, .7 if i == 0 else .35))
    ry0 = y + 42
    rh = (y + h - ry0 - 4) / 2
    for i in range(2):
        yy = ry0 + i * (rh + 4)
        out.append(el('rect', x=x, y=yy, width=w, height=rh, rx=5, fill='#0d2c4d', stroke=WHITE, stroke_opacity=.14))
        out.append(thumb(c, x + 3, yy + 3, rh * 1.3, rh - 6, 3, seed=i))
        out.append(lines(x + rh * 1.3 + 9, yy + rh / 2 - 5, [w * .38, w * .22], h=3.5, gap=7))
    return g(*out)


FIXTURE_ROWS = (  # home-fixture.json: (price, down payment, delivery, area m2); B best on lowest down payment, C over the 8M cap
    ('7.9M', '1.4M', '2028', '165'), ('8.0M', '1.2M', '2027', '158'), ('8.3M', '1.5M', None, '180'))


def frag_answer(c, x, y, w, h, rows=FIXTURE_ROWS, best=1, over=(2,), actions=('pdf', 'compare', 'calendar'), q_w=.7, u=1.0,
                cols=('delivery', 'price', 'down')):
    """Brokers AI answer plate content (example = home fixture).
    Top: the QUESTION ZONE on the end side: the art draws only the broker's avatar; the HTML
    label (`question` anchor, w/h meta = its box) IS the bubble, so there is never a double
    bubble. Below: the AI avatar and the answer: column icons (delivery key, price cash,
    down-payment wallet), three project rows (thumb, bedrooms + area numerals, delivery year or a
    'ready' key, price chip, down-payment chip) - B (best: lowest down payment) in mint with a
    check, C's price amber (over the 8M cap) - and the PDF / compare / viewing action pills.
    u scales every inner size (1 = desktop answer plate ~570 px wide; ~.6 on phones).
    Returns markup; the question box is in c.answer_q = (cx, cy, w, h)."""
    out = []
    qh = 64 * u
    av = 15 * u
    avx = x + w - av
    out.append(glow(c, avx, y + qh / 2, av * 2.4, None, ELEC, .45))
    out.append(el('circle', cx=avx, cy=y + qh / 2, r=av, fill='#16406b', stroke=CYAN, stroke_opacity=.55, stroke_width=1.2))
    out.append(icon(c, 'user', avx - av * .62, y + qh / 2 - av * .62, av * 1.24, WHITE, sw=1.8))
    qw = w * q_w
    qcx = avx - av - 10 * u - qw / 2
    c.answer_q = (qcx, y + qh / 2, qw, qh - 10 * u)
    # AI answer
    ay = y + qh + 12 * u
    ar = 18 * u
    out.append(glow(c, x + ar, ay + ar, ar * 1.9, None, CYAN, .45))
    out.append(el('circle', cx=x + ar, cy=ay + ar, r=ar, fill='#0d2c4d', stroke=CYAN, stroke_width=1.3))
    out.append(ai_glyph(c, x + ar, ay + ar, ar * 1.1, CYAN))
    bx = x + ar * 2 + 12 * u
    bw = x + w - bx
    bh = y + h - ay
    out.append(el('rect', x=bx, y=ay, width=bw, height=bh, rx=16 * u, fill='#0c2a49', stroke=WHITE, stroke_opacity=.15))
    out.append(el('path', d=f'M{f(bx + 16 * u)} {f(ay + .8)}H{f(bx + bw - 16 * u)}', stroke=WHITE, stroke_opacity=.25))
    pad = 14 * u
    # column geometry from the end edge
    chw, chh = 86 * u, 28 * u
    yw = 56 * u
    x_down = bx + bw - pad - chw
    x_price = x_down - 10 * u - chw
    x_year = x_price - 12 * u - yw
    colx = {'down': x_down + chw / 2, 'price': x_price + chw / 2, 'delivery': x_year + yw / 2}
    hy = ay + pad
    out.append(icon(c, 'sparkle', bx + pad, hy - 1 * u, 16 * u, CYAN, sw=1.8))
    out.append(bar(bx + pad + 22 * u, hy + 4 * u, bw * .26, 6 * u, WHITE, .75))
    cur = c.anim(f'animation:{c.kf("caret", "0%,49%{opacity:1}50%,100%{opacity:0}")} 1.1s steps(1) infinite')
    out.append(el('rect', x=bx + pad + 26 * u + bw * .26, y=hy, width=2.2 * u, height=14 * u, rx=1, fill=CYAN, cls=cur))
    for k, ic in (('delivery', 'key'), ('price', 'cash'), ('down', 'wallet')):
        out.append(icon(c, ic, colx[k] - 8 * u, hy - 1 * u, 16 * u, MINT if k == 'down' else CYAN, sw=1.8, opacity=None if k == 'down' else .8))
    out.append(el('path', d=f'M{f(bx + pad)} {f(hy + 24 * u)}H{f(bx + bw - pad)}', stroke=WHITE, stroke_opacity=.1))
    acts_h = 30 * u if actions else 0
    ry0 = hy + 34 * u
    n = len(rows)
    gap = 10 * u
    rh = min(78 * u, (ay + bh - pad - acts_h - (12 * u if actions else 0) - ry0 - (n - 1) * gap) / n)
    for i, (price, down, year, area) in enumerate(rows):
        yy = ry0 + i * (rh + gap)
        hl, ov = i == best, i in over
        if hl:
            out.append(glow(c, bx + bw / 2, yy + rh / 2, bw * .55, rh * .9, MINT, .2))
        out.append(el('rect', x=bx + pad * .6, y=yy, width=bw - pad * 1.2, height=rh, rx=11 * u, fill=MINT if hl else '#123a62',
                      fill_opacity=.13 if hl else .7, stroke=MINT if hl else WHITE, stroke_opacity=None if hl else .14,
                      stroke_width=1.5 if hl else 1))
        th = rh - 14 * u
        tw = th * 1.4
        tx = bx + pad * .6 + 7 * u
        out.append(thumb(c, tx, yy + 7 * u, tw, th, 6 * u, seed=i % 2))
        lx = tx + tw + 12 * u
        out.append(bar(lx, yy + rh * .28, min(x_year - lx - 14 * u, 120 * u), 6.5 * u, WHITE, .9 if hl else .62))
        sy = yy + rh * .7
        out.append(icon(c, 'bed', lx - 1 * u, sy - 10 * u, 13 * u, CYAN, sw=1.9))
        out.append(hud(c, '3', lx + 15 * u, sy + 1 * u, 8 * u, WHITE, opacity=.85))
        out.append(icon(c, 'area', lx + 28 * u, sy - 10 * u, 13 * u, CYAN, sw=1.9))
        out.append(hud(c, area, lx + 44 * u, sy + 1 * u, 8 * u, WHITE, opacity=.85))
        if hl:
            out.append(icon(c, 'check-circle', lx + 82 * u, sy - 11 * u, 15 * u, MINT, sw=2))
        cy_ = yy + rh / 2
        if year:
            out.append(hud(c, year, colx['delivery'], cy_ + 4.5 * u, 9 * u, WHITE, 'middle', opacity=.7))
        else:
            out.append(icon(c, 'key', colx['delivery'] - 8 * u, cy_ - 8 * u, 16 * u, MINT, sw=2))
        out.append(chip(c, x_price, cy_ - chh / 2, chw, chh, fill=None, stroke=AMBER if ov else '#6f95bf', text=price,
                        text_color=AMBER if ov else WHITE, size=11 * u, glow=False))
        if ov:  # over the client's 8M cap
            out.append(el('path', d=f'M{f(x_price + chw - 2 * u)} {f(cy_ - chh / 2 - 7 * u)}l{f(5 * u)} {f(7 * u)}h{f(-10 * u)}Z', fill=AMBER))
        out.append(chip(c, x_down, cy_ - chh / 2, chw, chh, fill=MINT if hl else None, stroke=None if hl else '#6f95bf', text=down,
                        text_color=DEEP if hl else WHITE, size=11 * u, glow=hl))
    if actions:
        py_ = ay + bh - pad - acts_h
        for i, a in enumerate(actions):
            pw_ = 66 * u
            px_ = bx + pad * .6 + i * (pw_ + 8 * u)
            out.append(el('rect', x=px_, y=py_, width=pw_, height=acts_h, rx=acts_h / 2, fill=CYAN, fill_opacity=.08, stroke=CYAN, stroke_opacity=.5))
            out.append(icon(c, a, px_ + 10 * u, py_ + acts_h / 2 - 8 * u, 16 * u, CYAN, sw=2))
            out.append(bar(px_ + 31 * u, py_ + acts_h / 2 - 2 * u, pw_ - 42 * u, 4 * u, CYAN, .45))
    return g(*out)


def orb(c, cx, cy, r, name, accent=ELEC, icon_color=WHITE, halo=True, ring=True):
    """Icon orb tile (navy core, gradient ring, top highlight, halo). The base is defined
    once per accent at r=20 and scaled; the icon is drawn upright on top."""
    def build(i):
        R = 20
        out = []
        if halo:
            out.append(glow(c, 0, 0, R * 2, None, accent, .4))
        out.append(el('circle', r=R, fill=c.rad([(0, '#21558c'), (.75, '#0f2f52'), (1, '#0b2239')], cy=.35)))
        if ring:
            out.append(el('circle', r=R - .7, stroke=c.lin([(0, CYAN), (.5, accent, .85), (1, accent, .15)], 0, 0, 1, 1), stroke_width=1.7))
        out.append(el('path', d=f'M{f(-R * .62)} {f(-R * .55)}A{f(R * .82)} {f(R * .82)} 0 0 1 {f(R * .62)} {f(-R * .55)}',
                      stroke=WHITE, stroke_opacity=.35, stroke_width=1.1))
        return el('g', ''.join(out), id=i)
    bid = c.define(('orb', accent, halo, ring), build)
    sz = r * 1.04
    return (el('use', href=f'#{bid}', transform=f'translate({f(cx)} {f(cy)}) scale({r / 20:.3f})') +
            icon(c, name, cx - sz / 2, cy - sz / 2, sz, icon_color, duo=accent, duo_o=.35, sw=1.7))


# ── Writer ─────────────────────────────────────────────────────────────
def write_scene(key, scene, out_dir):
    import xml.etree.ElementTree as ET
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    full = f'{key}-{scene.name}'
    stats = {'name': full, 'width': scene.width, 'height': scene.height}
    for mode, suffix in (('anim', ''), ('loop', '-loop'), ('still', '-still')):
        c = Canvas(full, scene.width, scene.height, mode != 'still', mode=mode)
        scene.draw(c)
        text = c.render()
        ET.fromstring(text)  # must parse
        if mode == 'still':
            assert '@keyframes' not in text and 'animation' not in text and '<style' not in text, f'{full}: still has animation'
            scene.anchors = c.anchors
        else:
            stats['loops'] = c.loops
            assert c.loops <= LOOP_BUDGET, f'{full}: {c.loops} looping animations (budget {LOOP_BUDGET})'
        (out_dir / f'{full}{suffix}.svg').write_text(text)
        stats[{'anim': 'animated_bytes', 'loop': 'loop_bytes', 'still': 'still_bytes'}[mode]] = len(text.encode())
    stats['anchors'] = scene.anchors
    return stats
