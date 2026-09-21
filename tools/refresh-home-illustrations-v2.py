#!/usr/bin/env python3
"""Replace legacy homepage mobile illustration markup with compact SVG scenes."""
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
SCENES={
 'market-explorer':'<div class="es-art-mobile ',
 'market-updates':'<div class="es-updates-mobile',
 'brand-unified':'<div class="es-art-mobile es-art-v2 es-art-v2--brand',
 'ai-conversation':'<div class="es-art-mobile es-art-v2 es-art-v2--conversation',
 'client-context':'<div class="es-art-mobile es-art-v2 es-art-v2--client',
 'roi-breakdown':'<div class="es-art-mobile es-art-v2 es-art-v2--roi',
 'meta-signals':'<div class="es-art-mobile es-art-v2 es-art-v2--signals',
 'listings-reach':'<div class="es-art-mobile es-art-v2 es-art-v2--reach',
}

def balanced_div_end(source,start):
    pos=start; depth=0
    while True:
        opening=source.find('<div',pos); closing=source.find('</div>',pos)
        if closing<0: raise ValueError('Unclosed mobile illustration div')
        if opening>=0 and opening<closing:
            depth+=1; pos=opening+4
        else:
            depth-=1; pos=closing+6
            if depth==0:return pos

def refresh(path,english=False):
    source=path.read_text()
    for name,marker in SCENES.items():
        anchor=source.find(f'estavo-{name}{"-en" if english else ""}.svg')
        start=source.find(marker,anchor)
        if start<0: # already refreshed
            continue
        end=balanced_div_end(source,start)
        suffix='-en' if english else ''
        markup=(f'<div class="es-home-art-mobile-flat"><picture class="es-vector-picture">'
                f'<source media="(prefers-reduced-motion: reduce)" srcset="assets/img/estavo-{name}-mobile{suffix}-still.svg" type="image/svg+xml" />'
                f'<img src="assets/img/estavo-{name}-mobile{suffix}.svg" width="390" height="430" alt="" loading="lazy" decoding="async" />'
                f'</picture></div>')
        source=source[:start]+markup+source[end:]
    path.write_text(source)

refresh(ROOT/'index.html',False)
refresh(ROOT/'en.html',True)
print('Replaced eight legacy mobile illustrations in Arabic and English homepages.')
