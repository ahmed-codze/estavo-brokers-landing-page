#!/usr/bin/env python3
"""Build Estavo's line icon family; no external dependencies.

September 2026: the dimensional (isometric, gradient-filled,
drop-shadowed) icon pack was replaced by native line geometry.
The old pack fought the rest of the system — every other homepage
scene draws product structure in flat Estavo navy/blue strokes,
so six gradient blocks in the services grid read as clip art from
a different kit (DESIGN-GUIDELINES.md §6, "native line icons
replace the dimensional icon pack").

These are drawn on a 24-unit grid and scaled to the 160 viewBox
the markup already reserves, so no page markup has to change.
They are referenced as <img>, which cannot inherit currentColor,
so the stroke is the Estavo blue token value (--es-blue-600,
#28567f) written literally; the surrounding tile carries any
state colour. Stroke width stays optically even at the 40-60px
sizes the cards actually use.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/img/icons'
OUT.mkdir(exist_ok=True)

# Drawn at 24×24, then scaled ×(160/24) so the emitted viewBox
# still matches the width/height the existing markup declares.
SCALE = 160 / 24

# Each entry is plain path data in the 24-unit space. Keeping the
# geometry declarative (rather than hand-tuned 160-space numbers)
# is what keeps the family optically consistent.
DRAWINGS = {
    # Market data: a tower of stacked unit records.
    'building': '<path d="M3 21h18"/>'
                '<path d="M5 21V9l7-4 7 4v12"/>'
                '<path d="M9 21v-5h6v5"/>'
                '<path d="M9 10.5h2M13 10.5h2M9 13.5h2M13 13.5h2"/>',
    # Coverage: a pin over an area grid.
    'map': '<path d="M3 7.5 9 5l6 2.5L21 5v12l-6 2.5L9 17l-6 2.5z"/>'
           '<path d="M9 5v12M15 7.5v12"/>',
    # Project plan: a floor plate with rooms.
    'plan': '<rect x="3" y="4" width="18" height="16" rx="1.5"/>'
            '<path d="M3 11h8M11 4v16M11 15h10"/>',
    # Market news and analysis: trend over a baseline.
    'chart': '<path d="M4 20V4"/><path d="M4 20h16"/>'
             '<path d="M7.5 16v-4M12 16V8M16.5 16v-6"/>',
    # Client AI: a conversation, matching the diagram glyph.
    'chat': '<path d="M21 14a3 3 0 0 1-3 3H9l-5 3.5V6a3 3 0 0 1 3-3h11a3 3 0 0 1 3 3z"/>'
            '<path d="M8.5 9h7M8.5 12.5h4.5"/>',
    # Requests and replies: two stacked message surfaces.
    'messages': '<path d="M7 15H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v2"/>'
                '<path d="M9 9h10a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-2l-3 2.5V20H9a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2z"/>',
    # Organised data: stacked layers.
    'layers': '<path d="m12 3 9 4.5-9 4.5-9-4.5z"/><path d="m3 12 9 4.5 9-4.5"/>'
              '<path d="m3 16.5 9 4.5 9-4.5"/>',
    # Ownership and permissions.
    'shield': '<path d="M12 3 5 6v6c0 4.2 2.9 7.6 7 9 4.1-1.4 7-4.8 7-9V6z"/>'
              '<path d="m9 12 2 2 4-4"/>',
    # Distribution / Meta connection: a routed graph.
    'network': '<circle cx="12" cy="12" r="3"/><circle cx="5" cy="5" r="2"/>'
               '<circle cx="19" cy="5" r="2"/><circle cx="19" cy="19" r="2"/>'
               '<path d="M6.5 6.5 10 10M17.5 6.5 14 10M17.5 17.5 14 14"/>',
    # A broker's own branded presence.
    'profile': '<circle cx="12" cy="8" r="3.5"/>'
               '<path d="M4.5 20c.8-4 3.8-6 7.5-6s6.7 2 7.5 6"/>',
}

TEMPLATE = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 160" '
    'fill="none" stroke="#28567f" stroke-width="{stroke}" '
    'stroke-linecap="round" stroke-linejoin="round" role="img">'
    '<title>{name}</title>'
    '<g transform="scale({scale})">{drawing}</g>'
    '</svg>'
)

for name, drawing in DRAWINGS.items():
    # The group is scaled, so the declared stroke width is divided
    # by the same factor to land at the intended 1.5 units on the
    # 24-grid. (vector-effect on a <g> does not reach its children.)
    svg = TEMPLATE.format(
        name=name,
        scale=round(SCALE, 4),
        stroke=round(1.7 / SCALE, 4),
        drawing=drawing,
    )
    (OUT / f'estavo-{name}.svg').write_text(svg)

print(f'Built {len(DRAWINGS)} line icons.')
