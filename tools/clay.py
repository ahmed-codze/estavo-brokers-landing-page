#!/usr/bin/env python3
"""Claymorphism material layer for the homepage illustrations.

Clay is a material, not a new visual vocabulary: the product structures,
palette roles and label sizes defined in DESIGN-GUIDELINES.md are unchanged.
What changes is how a surface catches light.

A clay surface has four parts, and all four are required or it reads as a
plain rounded box:

  1. a soft tinted body fill (never pure white — clay has hue)
  2. an inner highlight on the top-left edge
  3. an inner shadow on the bottom-right edge
  4. a wide, diffuse, colour-matched drop shadow beneath

Radii are deliberately large. Clay geometry is "squircle-adjacent": the
corner radius is a large fraction of the smaller side, which is why
`clay_radius()` scales with the box rather than using a fixed token.
"""

# Tinted clay bodies. Each is a light/base pair used as a vertical wash.
# The navy entries keep the Estavo deep ground; the pale entries extend
# --es-blue-100/#c3d5e8 into genuine surface fills, which is where clay's
# characteristic hue play comes from in this palette.
CLAY_BODIES = {
    'paper':  ('#ffffff', '#e4eef8'),
    'mist':   ('#f1f7fc', '#d8e6f3'),
    'pale':   ('#e0ecf8', '#c6dbee'),
    'blue':   ('#cfe1f4', '#a9c6e2'),
    'navy':   ('#14395a', '#08192b'),
    'navy2':  ('#1a4467', '#0b2239'),
    'accent': ('#356a96', '#28567f'),
}


def clay_radius(w, h, cap=44):
    """Clay corners are a large fraction of the smaller side, not a token.

    Capped so a big panel stays a panel instead of becoming a pill, and
    floored so small chips still read as clay rather than as sharp tiles.
    """
    return max(8, min(cap, round(min(w, h) * 0.30)))


def defs(scope='clay', navy_scene=False):
    """Emit the clay gradients and filters.

    Every id is scoped per instance because these SVGs are standalone
    documents that may be inlined together on one page; an unscoped
    `id="clay-lift"` would let the first document capture the rest.
    """
    g = []
    for name, (light, base) in CLAY_BODIES.items():
        g.append(
            f'<linearGradient id="{scope}-{name}" x1="0" y1="0" x2=".35" y2="1">'
            f'<stop stop-color="{light}"/><stop offset="1" stop-color="{base}"/>'
            f'</linearGradient>'
        )

    # The inflation filter. feDropShadow inside the alpha channel produces the
    # two inner edges; the outer term is a wide colour-matched ambient shadow.
    # Light comes from the top-left, consistently, on every surface.
    def inflate(sid, hi, hi_o, lo, lo_o, blur, dy, sd, amb_o, amb_col='#0b2239'):
        return (
            f'<filter id="{scope}-{sid}" x="-40%" y="-40%" width="185%" height="195%">'
            # inner highlight, top-left
            f'<feFlood flood-color="{hi}" flood-opacity="{hi_o}" result="hi"/>'
            f'<feComposite in="hi" in2="SourceAlpha" operator="in" result="hiClip"/>'
            f'<feOffset in="hiClip" dx="-{dy}" dy="-{dy}" result="hiOff"/>'
            f'<feGaussianBlur in="hiOff" stdDeviation="{blur}" result="hiBlur"/>'
            f'<feComposite in="hiBlur" in2="SourceAlpha" operator="in" result="hiIn"/>'
            # inner shadow, bottom-right
            f'<feFlood flood-color="{lo}" flood-opacity="{lo_o}" result="lo"/>'
            f'<feComposite in="lo" in2="SourceAlpha" operator="in" result="loClip"/>'
            f'<feOffset in="loClip" dx="{dy}" dy="{dy}" result="loOff"/>'
            f'<feGaussianBlur in="loOff" stdDeviation="{blur}" result="loBlur"/>'
            f'<feComposite in="loBlur" in2="SourceAlpha" operator="in" result="loIn"/>'
            # stack: body, then the two inner edges
            f'<feMerge result="body">'
            f'<feMergeNode in="SourceGraphic"/><feMergeNode in="loIn"/><feMergeNode in="hiIn"/>'
            f'</feMerge>'
            # wide ambient shadow beneath, colour-matched to the palette
            f'<feDropShadow in="body" dx="0" dy="{sd}" stdDeviation="{sd}" '
            f'flood-color="{amb_col}" flood-opacity="{amb_o}"/>'
            f'</filter>'
        )

    # Light surfaces: a bright white highlight and a navy-tinted inner shadow.
    g.append(inflate('puff', '#ffffff', .95, '#7ba3c6', .6, 5, 4, 16, .13))
    # Smaller elements need proportionally tighter light or they turn to mush.
    g.append(inflate('puff-sm', '#ffffff', .9, '#7ba3c6', .55, 2.5, 2, 7, .12))
    g.append(inflate('puff-xs', '#ffffff', .85, '#7ba3c6', .5, 1.4, 1.2, 4, .1))
    # Dark surfaces: the highlight is a cool slate lift, not white.
    g.append(inflate('puff-dark', '#4f86b3', .42, '#03101d', .8, 5, 4, 16, .2))
    g.append(inflate('puff-dark-sm', '#4f86b3', .38, '#03101d', .75, 2.5, 2, 7, .18))
    # Pressed / recessed: inner shadow only, for inputs and wells.
    g.append(
        f'<filter id="{scope}-press" x="-25%" y="-25%" width="150%" height="160%">'
        f'<feFlood flood-color="#6f96b8" flood-opacity=".6" result="p"/>'
        f'<feComposite in="p" in2="SourceAlpha" operator="in" result="pc"/>'
        f'<feOffset in="pc" dx="2" dy="2.5" result="po"/>'
        f'<feGaussianBlur in="po" stdDeviation="2.5" result="pb"/>'
        f'<feComposite in="pb" in2="SourceAlpha" operator="in" result="pin"/>'
        f'<feFlood flood-color="#ffffff" flood-opacity=".8" result="q"/>'
        f'<feComposite in="q" in2="SourceAlpha" operator="in" result="qc"/>'
        f'<feOffset in="qc" dx="-1.5" dy="-2" result="qo"/>'
        f'<feGaussianBlur in="qo" stdDeviation="2" result="qb"/>'
        f'<feComposite in="qb" in2="SourceAlpha" operator="in" result="qin"/>'
        f'<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="qin"/>'
        f'<feMergeNode in="pin"/></feMerge>'
        f'</filter>'
    )
    return ''.join(g)


def surface(x, y, w, h, body='paper', r=None, scope='clay', size='md', extra=''):
    """A clay surface: tinted body + inflation filter + generous radius."""
    if r is None:
        r = clay_radius(w, h)
    dark = body.startswith('navy') or body == 'accent'
    f = {'md': 'puff', 'sm': 'puff-sm', 'xs': 'puff-xs'}[size]
    if dark:
        f = 'puff-dark' if size == 'md' else 'puff-dark-sm'
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="url(#{scope}-{body})" filter="url(#{scope}-{f})" {extra}/>')


def well(x, y, w, h, body='mist', r=None, scope='clay', extra=''):
    """A recessed clay well: for inputs, tracks and inset areas."""
    if r is None:
        r = clay_radius(w, h)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="url(#{scope}-{body})" filter="url(#{scope}-press)" {extra}/>')
