#!/usr/bin/env python3
"""Build nine animated vector scenes with Plex typography and native geometry.

Run: python3 tools/build-illustrations.py
Font subsetting: python3 -m pip install fonttools brotli
The checked-in SVGs are standalone; browsers need no scripts or external fonts.
"""
from pathlib import Path
from html import escape
import base64
import io
import xml.etree.ElementTree as ET
import json
import re
import math
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/img'
NS = 'http://www.w3.org/2000/svg'
ICON_INSTANCE = 0
STILL_STYLE = '''<style>*{animation:none!important}.enter,.chartbar,.bar-deduction,.orbit,.float-object,.trace,.plan-scan,.review-check,.loop-weave,.core-breathe,.intent-wash,.phase-light,.rise,.lift-in,.sheen,.drift-slow,.drift-tilt,.halo-pulse{opacity:1!important;transform:none!important;stroke-dashoffset:0!important}.packet,.plan-scan,.loop-energy,.signal-runner,.spark,.ribbon-mote,.synapse,.answer-edge{display:none!important}</style>'''

def write_variants(name,svg):
    (OUT/f'estavo-{name}.svg').write_text(svg)
    (OUT/f'estavo-{name}-still.svg').write_text(svg.replace('</svg>',STILL_STYLE+'</svg>'))

def brand_mark(x,y,width=100,fill='#f5f9fc'):
    root=ET.parse(ROOT/'assets/logo/estavo-mark.svg').getroot()
    d=next(root.iter(f'{{{NS}}}path')).get('d')
    return f'<g transform="translate({x} {y}) scale({width/600})"><path d="{d}" fill="{fill}" fill-rule="evenodd"/></g>'

def infinity_path(rx=230,ry=78,shift=0):
    points=[]
    for i in range(121):
        t=i*math.tau/120
        points.append((rx*math.sin(t),ry*math.sin(2*t)+shift*math.cos(3*t)))
    return 'M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in points)+'Z'

def ribbon_surface(rx=230,ry=78):
    outer=[];inner=[]
    for i in range(161):
        t=i*math.tau/160
        x,y=rx*math.sin(t),ry*math.sin(2*t)
        dx,dy=rx*math.cos(t),2*ry*math.cos(2*t)
        length=math.hypot(dx,dy)
        width=10+5*math.sin(t)**2
        nx,ny=-dy/length*width,dx/length*width
        outer.append((x+nx,y+ny));inner.append((x-nx,y-ny))
    return 'M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in outer+inner[::-1])+'Z'

def knowledge_loop(x,y,scale=1,dark=False,label='Estavo',compact=False):
    # The brand's connected e/s is the anchor; the surrounding strands show
    # property knowledge being connected, rather than a generic AI mascot.
    s=f'<g transform="translate({x} {y}) scale({scale})">'
    s+='<ellipse cx="0" cy="0" rx="270" ry="173" fill="url(#knowledge-aura)"/>'
    s+='<ellipse class="halo-pulse" cx="0" cy="0" rx="214" ry="138" fill="url(#halo)"/>'
    surface=ribbon_surface()
    s+=f'<g class="loop-weave"><path transform="translate(0 7)" d="{surface}" fill="#0b2239" fill-opacity=".1"/><path d="{surface}" fill="url(#ribbon-satin)" fill-opacity=".82"/><path d="{surface}" fill="none" stroke="#d4ecfa" stroke-opacity=".38" stroke-width=".7"/></g>'
    # A travelling mote rides the ribbon: schematic connection, not live data.
    s+=f'<path d="{infinity_path()}" class="ribbon-mote" pathLength="128" fill="none" stroke="#bff0e0" stroke-width="5" stroke-linecap="round" opacity=".9"/>'
    for i,(shift,width,opacity) in enumerate([(-15,1.25,.18),(0,12,.15),(12,1.25,.25)]):
        d=infinity_path(230,78,shift)
        s+=f'<g class="loop-weave" style="animation-delay:{-i*2}s"><path d="{d}" fill="none" stroke="url(#knowledge-thread)" stroke-width="{width}" stroke-opacity="{opacity}"/></g>'
    d=infinity_path()
    s+=f'<path d="{d}" fill="none" stroke="url(#knowledge-thread)" stroke-width="3" stroke-opacity=".8"/>'
    s+=f'<path d="{d}" class="loop-energy" pathLength="100" fill="none" stroke="#72e0bb" stroke-width="4" stroke-linecap="round"/>'
    for i,(xx,yy) in enumerate([(-208,-39),(-182,77),(-75,-58),(112,69),(212,-32),(72,-68)]):
        s+=circle(xx,yy,11,'#193c56' if dark else '#e1edf5','stroke="#92bcd8" stroke-opacity=".4"')
        s+=circle(xx,yy,3,'#72e0bb',f'class="phase-light" style="animation-delay:{-i*1.6}s"')
    s+=circle(0,0,89,'#14334a' if dark else '#f1f6fa','fill-opacity=".9"')
    s+='<g class="core-breathe" filter="url(#shadow)">'
    s+=brand_mark(-78,-41,156,'#17364e' if dark else '#b6cbdc')
    s+=brand_mark(-78,-46,156,'#416a85' if dark else '#7295b1')
    s+=brand_mark(-78,-50,156,'url(#brand-pearl)' if dark else 'url(#brand-metal)')+'</g>'
    if not compact:s+=text(0,68,label,'light-label' if dark else 'label','middle')
    else:s+='<path d="M-23 63H23" fill="none" stroke="#72c9b2" stroke-opacity=".7" stroke-width="2"/>'
    return s+'</g>'

def process_route(d,phase=0,dark=False):
    base='light-line' if dark else 'structure'
    return path(d,base)+f'<path d="{d}" class="synapse" pathLength="100" fill="none" stroke="#72c9b2" stroke-width="2" stroke-linecap="round" style="animation-delay:{phase}s"/>'

def field_fragment(x,y,w,label,value,dark=False,phase=0,tilt=0,h=91):
    # A property field is a physical card, not a flat panel: a raised face on a
    # contact shadow, a lit top edge, and a mint reader rail that lights when
    # this field is connected. `tilt` gives stacked cards an off-axis plane so a
    # group of them reads as depth rather than as a menu (§5, §6).
    s=f'<g class="lift-in" style="animation-delay:{.12+phase*.12}s">'
    inner=f'<g transform="translate({x} {y})'+(f' rotate({tilt} {w/2} {h/2})' if tilt else '')+'">'
    inner+=f'<rect width="{w}" height="{h}" rx="15" fill="{"url(#deep-face)" if dark else "url(#card-face)"}" filter="url(#lift)" stroke="{"#ffffff" if dark else "#dbe7f2"}" stroke-opacity="{".16" if dark else ".9"}"/>'
    inner+=f'<rect x="1" y="1" width="{w-2}" height="{h/2}" rx="14" fill="url(#card-edge)" opacity="{".1" if dark else ".75"}"/>'
    inner+=f'<rect class="intent-wash" width="{w}" height="{h}" rx="15" fill="#72e0bb" fill-opacity=".09" style="animation-delay:{phase}s"/>'
    inner+=text(w-22,33,label,'muted' if dark else 'micro')
    inner+=text(w-22,70,value,'light-label' if dark else 'label')
    inner+=f'<rect x="14" y="17" width="3.4" height="{h-34}" rx="1.7" fill="#c8d9e8" fill-opacity="{".3" if dark else ".55"}"/>'
    inner+=f'<rect class="phase-light" x="14" y="17" width="3.4" height="{h-34}" rx="1.7" fill="url(#mint)" style="animation-delay:{phase}s"/>'
    return s+inner+'</g></g>'

def icon(x,y,size,name):
    # Inline real paths, with scoped paint servers. Figures remain pure vectors.
    global ICON_INSTANCE
    ICON_INSTANCE += 1
    source=(OUT/'icons'/f'estavo-{name}.svg').read_text()
    source=re.sub(r'^<svg[^>]*>|</svg>$|<title>.*?</title>', '', source)
    if name=='shield':
        source=source.replace('d="M61 79L76 93L105 62"','d="M61 79L76 93L105 62" class="review-check" pathLength="100"')
    prefix=f'icon-{ICON_INSTANCE}-'
    source=re.sub(r'id="([^"]+)"',lambda m:f'id="{prefix}{m[1]}"',source)
    source=re.sub(r'url\(#([^)]+)\)',lambda m:f'url(#{prefix}{m[1]})',source)
    return f'<g transform="translate({x} {y}) scale({size/160})">{source}</g>'

def floating_icon(x,y,size,name,delay=0):
    return f'<g transform="translate({x} {y})"><g class="float-object" style="animation-delay:{delay}s">'+icon(0,0,size,name)+'</g></g>'

def route(d,delay=0,dark=False):
    color='#72e0bb' if dark else '#47749a'
    return path(d,'light-line' if dark else 'structure') + f'<path d="{d}" class="packet" pathLength="100" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" style="animation-delay:{delay}s"/>'

def plate(x,y,w=220,h=154,scale=1,blueprint=True):
    # Project a physical sheet into an isometric plane, preserving furniture.
    s=f'<g transform="translate({x} {y}) scale({scale})"><g class="float-object">'
    for offset,fill in [(40,'#d6e3ed'),(22,'#315772'),(0,'#f5f9fc')]:
        s+=f'<g transform="translate(0 {offset}) matrix(1 .52 -1 .52 0 0)">'
        s+=f'<path d="M0 {h}H{w}V{h+9}H0Z" fill="'+('#193c56' if offset==22 else '#b5cadc')+'"/>'
        s+=f'<path d="M{w} 0V{h+9}H{w+7}V0Z" fill="'+('#0b2239' if offset==22 else '#c1d4e3')+'"/>'
        s+=rect(-6,-6,w+12,h+12,fill,4,'stroke="#ffffff" stroke-opacity=".65" stroke-width="1.25"')
        if offset==0 and blueprint:s+=plan(0,0)
        elif offset==22:
            for yy in [20,52,84,116]:s+=path(f'M8 {yy}H{w-8}','light-line')
        s+='</g>'
    return s+'</g></g>'

def text(x, y, value, cls='body', anchor='end'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{escape(value)}</text>'

def rect(x, y, w, h, fill='url(#paper)', radius=16, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" {extra}/>'

def path(d, cls='structure', extra=''):
    return f'<path d="{d}" class="{cls}" {extra}/>'

def line(x1, y1, x2, y2, cls='structure'):
    return path(f'M{x1} {y1}H{x2}' if y1 == y2 else f'M{x1} {y1}L{x2} {y2}', cls)

def circle(x, y, r, fill, extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'

def plan(x, y, scale=1, dark=False):
    color = '#a9c6e2' if dark else '#28567f'
    s=f'<g transform="translate({x} {y}) scale({scale})" style="color:{color}">'
    s+=rect(0,0,220,154,'#ffffff08' if dark else '#f6f9fc',4)
    for xx,ww,fill in [(9,73,'#dfebf3'),(87,56,'#e8eff5'),(148,63,'#e2eee9')]:
        s+=rect(xx,9,ww,56,'#ffffff09' if dark else fill,0)
    s+=rect(9,71,125,74,'#ffffff09' if dark else '#edf3f7',0)
    s+=rect(139,71,72,74,'#ffffff06' if dark else '#e5edf3',0)
    furniture=''
    for xx,ww in [(20,43),(96,34),(157,37)]:
        furniture+=rect(xx,19,ww,36,'#ffffff15' if dark else '#fff',2,'stroke="currentColor" stroke-opacity=".4" stroke-width="1"')
        furniture+=path(f'M{xx} 30H{xx+ww}M{xx+ww/2} 19V30','structure','style="stroke:currentColor"')
        furniture+=rect(xx+4,22,ww/2-6,5,'#bfd5e6',1)
        furniture+=rect(xx+ww/2+2,22,ww/2-6,5,'#bfd5e6',1)
    furniture+=rect(18,82,52,16,'#ffffff15' if dark else '#d6e5ef',3,'stroke="currentColor" stroke-opacity=".3"')
    furniture+=rect(18,103,15,29,'#ffffff15' if dark else '#d6e5ef',3,'stroke="currentColor" stroke-opacity=".3"')
    furniture+=rect(44,109,23,15,'#ffffff15' if dark else '#fff',3,'stroke="currentColor" stroke-opacity=".3"')
    furniture+=rect(96,101,24,25,'#ffffff15' if dark else '#fff',8,'stroke="currentColor" stroke-opacity=".3"')
    for xx,yy in [(91,105),(121,105),(100,95),(100,127)]:furniture+=rect(xx,yy,7,7,'#a9c6e24d',2)
    furniture+=path('M150 86H178V137H150M150 96H178M150 111H178M165 86V137M191 91H203V116H191ZM191 125H203V137H191Z','structure','style="stroke:currentColor"')
    furniture+=circle(157,123,3,'none','stroke="currentColor" stroke-opacity=".4"')
    furniture+=circle(170,123,3,'none','stroke="currentColor" stroke-opacity=".4"')
    s+=furniture
    s+=path('M8 8H212V146H8ZM84 8V65M145 8V65M8 69H42M63 69H100M121 69H158M179 69H212M136 69V101M136 124V146M184 69V146','subject','style="stroke:currentColor"')
    s+='<path d="M42 69V48A21 21 0 0 1 63 69M100 69V48A21 21 0 0 1 121 69M158 69V48A21 21 0 0 1 179 69M136 101H159A23 23 0 0 1 136 124" fill="none" stroke="currentColor" stroke-opacity=".3" stroke-width="1.25"/>'
    s+='<g class="plan-scan">'+rect(10,70,200,9,'#72e0bb18',0)+'<path d="M10 79H210" fill="none" stroke="#72c9b2" stroke-width="1" stroke-opacity=".5"/></g>'
    return s+'</g>'

DEFS = '''<defs>
<linearGradient id="paper" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fff"/><stop offset="1" stop-color="#f1f5f8"/></linearGradient>
<linearGradient id="navy" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#163e59"/><stop offset="1" stop-color="#0b2239"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff0f"/><stop offset="1" stop-color="#ffffff03"/></linearGradient>
<linearGradient id="architecture" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#e8f0f6"/><stop offset="1" stop-color="#d0dfea"/></linearGradient>
<linearGradient id="mint" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#9beacf"/><stop offset="1" stop-color="#72c9b2"/></linearGradient>
<linearGradient id="bar-face" x2="0" y2="1"><stop stop-color="#c4d9e8"/><stop offset="1" stop-color="#8eafc7"/></linearGradient>
<linearGradient id="knowledge-thread" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#47749a"/><stop offset=".48" stop-color="#82b7d9"/><stop offset="1" stop-color="#72c9b2"/></linearGradient>
<radialGradient id="core-surface" cx=".25" cy=".12" r="1"><stop stop-color="#315d7b"/><stop offset=".55" stop-color="#12334c"/><stop offset="1" stop-color="#061c31"/></radialGradient>
<radialGradient id="knowledge-aura"><stop stop-color="#7baed0" stop-opacity=".2"/><stop offset=".55" stop-color="#7baed0" stop-opacity=".07"/><stop offset="1" stop-color="#7baed0" stop-opacity="0"/></radialGradient>
<linearGradient id="ribbon-satin" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#163e59"/><stop offset=".27" stop-color="#6c9dbc"/><stop offset=".47" stop-color="#a2ccdf"/><stop offset=".65" stop-color="#315d79"/><stop offset="1" stop-color="#72bda9"/></linearGradient>
<linearGradient id="brand-metal" x1="0" y1="0" x2=".5" y2="1"><stop stop-color="#254c68"/><stop offset=".35" stop-color="#477b9d"/><stop offset=".46" stop-color="#193d58"/><stop offset="1" stop-color="#061c31"/></linearGradient>
<linearGradient id="brand-pearl" x1="0" y1="0" x2=".4" y2="1"><stop stop-color="#fff"/><stop offset=".45" stop-color="#d7edf9"/><stop offset="1" stop-color="#8bb7d3"/></linearGradient>
<radialGradient id="aura"><stop stop-color="#5c91c7" stop-opacity=".16"/><stop offset="1" stop-color="#5c91c7" stop-opacity="0"/></radialGradient>
<filter id="shadow" x="-25%" y="-25%" width="150%" height="160%"><feDropShadow dy="16" stdDeviation="18" flood-color="#0b2239" flood-opacity=".09"/><feDropShadow dy="2" stdDeviation="2" flood-color="#0b2239" flood-opacity=".07"/></filter>
<!-- Material layer (§6): depth comes from stacked light, not one shared drop
     shadow. `lift` is the near-field card shadow with a wider ambient term;
     `contact` is the tight shadow that sits an object on its ground. -->
<filter id="lift" x="-35%" y="-35%" width="180%" height="190%"><feDropShadow dy="26" stdDeviation="30" flood-color="#0b2239" flood-opacity=".1"/><feDropShadow dy="6" stdDeviation="7" flood-color="#0b2239" flood-opacity=".07"/><feDropShadow dy="1" stdDeviation="1" flood-color="#0b2239" flood-opacity=".06"/></filter>
<filter id="contact" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dy="7" stdDeviation="6" flood-color="#0b2239" flood-opacity=".14"/></filter>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<!-- Field surfaces read as glass on paper: a cool vertical wash, a lit top
     edge and a faint inner floor. Angled so stacked cards do not look flat. -->
<linearGradient id="card-face" x1="0" y1="0" x2=".35" y2="1"><stop stop-color="#ffffff"/><stop offset=".55" stop-color="#f7fafd"/><stop offset="1" stop-color="#e9f0f7"/></linearGradient>
<linearGradient id="card-edge" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff" stop-opacity=".95"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
<linearGradient id="deep-face" x1="0" y1="0" x2=".3" y2="1"><stop stop-color="#1b4360"/><stop offset=".5" stop-color="#102b45"/><stop offset="1" stop-color="#081d31"/></linearGradient>
<!-- A travelling specular band; used on the ribbon and on comparison edges. -->
<linearGradient id="sheen-band" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#ffffff" stop-opacity="0"/><stop offset=".45" stop-color="#eaf7ff" stop-opacity=".75"/><stop offset=".55" stop-color="#eaf7ff" stop-opacity=".75"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
<radialGradient id="halo" cx=".5" cy=".5"><stop stop-color="#8fd8ff" stop-opacity=".3"/><stop offset=".6" stop-color="#72c9b2" stop-opacity=".1"/><stop offset="1" stop-color="#72c9b2" stop-opacity="0"/></radialGradient>
<radialGradient id="mint-orb" cx=".32" cy=".26"><stop stop-color="#d8fff2"/><stop offset=".55" stop-color="#84dcc0"/><stop offset="1" stop-color="#3f9a80"/></radialGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#5c91c7" stroke-opacity=".07" stroke-width="1.25"/></pattern>
<style>
text{font-family:ArtPlex,Arial,sans-serif;fill:#0b2239;font-weight:400;font-size:21px}
.display{font-size:28px;font-weight:500}.title{font-size:24px;font-weight:500}.body{font-size:21px}.label{font-size:21px;font-weight:500}.small{font-size:19px;fill:#47749a}.micro{font-size:17px;fill:#47749a}.white{fill:#f5f9fc}.muted{fill:#a9c6e2}.mint{fill:#72e0bb}.light-title{font-size:24px;font-weight:500;fill:#f5f9fc}.light-display{font-size:28px;font-weight:500;fill:#f5f9fc}.light-label{font-size:21px;font-weight:500;fill:#f5f9fc}
.structure{fill:none;stroke:#5c91c7;stroke-opacity:.32;stroke-width:1.25;stroke-linecap:round;stroke-linejoin:round}.subject{fill:none;stroke:#28567f;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.light-line{fill:none;stroke:#a9c6e2;stroke-opacity:.22;stroke-width:1.25}.flow{fill:none;stroke:#72e0bb;stroke-opacity:.55;stroke-width:2;stroke-dasharray:3 9}.enter{animation:enter .7s both}.late{animation-delay:.16s}.later{animation-delay:.3s}
@keyframes enter{from{transform:translateY(12px)}to{transform:none}}
.chartbar,.bar-deduction{transform-box:fill-box;transform-origin:center bottom}.bar-deduction{transform-origin:center top}.orbit{transform-box:fill-box;transform-origin:center}.packet{stroke-dasharray:4 96;stroke-dashoffset:0}
.intent-wash{transform-box:fill-box;transform-origin:left center}.synapse,.answer-edge{stroke-dasharray:100;stroke-dashoffset:0}.loop-energy{stroke-dasharray:9 91;stroke-dashoffset:0}.core-breathe{transform-box:fill-box;transform-origin:center}
@media(prefers-reduced-motion:no-preference){.loop-weave{animation:loop-weave 16s ease-in-out infinite}.loop-energy{animation:loop-energy 16s linear infinite}.core-breathe{animation:core-breathe 16s ease-in-out infinite}.synapse{animation:synapse 16s ease-in-out infinite both}.intent-wash{animation:intent-wash 16s ease-in-out infinite both}.answer-edge{animation:answer-edge 16s ease-in-out infinite}.phase-light{animation:phase-light 16s ease-in-out infinite}}
@keyframes loop-weave{0%,100%{transform:none}30%{transform:translateY(-8px) scaleY(1.08)}65%{transform:translateY(8px) scaleY(.92)}}
@keyframes loop-energy{to{stroke-dashoffset:-200}}@keyframes core-breathe{0%,100%{transform:none}38%{transform:scale(1.025)}}
@keyframes synapse{0%,8%{stroke-dashoffset:100;opacity:.15}35%,78%{stroke-dashoffset:0;opacity:.8}100%{stroke-dashoffset:0;opacity:.15}}
@keyframes intent-wash{0%,12%,100%{transform:scaleX(.04);opacity:.15}35%,72%{transform:scaleX(1);opacity:1}90%{transform:scaleX(1);opacity:.15}}
@keyframes answer-edge{0%,36%{stroke-dashoffset:100;opacity:.15}66%,88%{stroke-dashoffset:0;opacity:.8}100%{stroke-dashoffset:0;opacity:.15}}
@keyframes phase-light{0%,100%{opacity:.25}35%,65%{opacity:1}}
/* Secondary motion (§7.4). Energy comes from depth and staged arrival, never
   from anything that reads as live data: text never moves, nothing counts, and
   travel stays small. Every class here is listed in STILL_STYLE so the -still
   companions restore the finished state (§7, the classic reduced-motion bug). */
.rise,.lift-in,.drift-slow,.drift-tilt,.halo-pulse,.sheen{transform-box:fill-box;transform-origin:center}
.spark,.ribbon-mote{stroke-dasharray:3 61;stroke-dashoffset:0}
@media(prefers-reduced-motion:no-preference){
.rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}
.lift-in{animation:lift-in 1s cubic-bezier(.2,.7,.2,1) both}
.drift-slow{animation:drift-slow 11s ease-in-out infinite}
.drift-tilt{animation:drift-tilt 14s ease-in-out infinite}
.halo-pulse{animation:halo-pulse 9s ease-in-out infinite}
.sheen{animation:sheen 16s ease-in-out infinite both}
.spark{animation:spark 6s linear infinite}
.ribbon-mote{animation:ribbon-mote 9s linear infinite}
}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes lift-in{from{opacity:0;transform:translateY(22px) scale(.975)}to{opacity:1;transform:none}}
@keyframes drift-slow{0%,100%{transform:translateY(-4px)}50%{transform:translateY(4px)}}
@keyframes drift-tilt{0%,100%{transform:translateY(-3px) rotate(-.5deg)}50%{transform:translateY(3px) rotate(.5deg)}}
@keyframes halo-pulse{0%,100%{opacity:.45;transform:scale(.97)}50%{opacity:1;transform:scale(1.03)}}
@keyframes sheen{0%,18%{opacity:0;transform:translateX(-38%)}34%,52%{opacity:1}70%,100%{opacity:0;transform:translateX(38%)}}
@keyframes spark{0%{stroke-dashoffset:64;opacity:0}12%,82%{opacity:1}100%{stroke-dashoffset:-64;opacity:0}}
@keyframes ribbon-mote{0%{stroke-dashoffset:128;opacity:0}14%,80%{opacity:.9}100%{stroke-dashoffset:-128;opacity:0}}
@media(prefers-reduced-motion:reduce){.rise,.lift-in,.drift-slow,.drift-tilt,.halo-pulse,.sheen{animation:none;opacity:1;transform:none}.spark,.ribbon-mote{display:none}}
@media(prefers-reduced-motion:no-preference){.flow{animation:flow 5s linear infinite}.chartbar,.bar-deduction{animation:bar 1.3s cubic-bezier(.2,.7,.2,1) both}.orbit{animation:glow 6s ease-in-out infinite}.float-object{animation:float-object 8s ease-in-out infinite}.trace{stroke-dasharray:800;stroke-dashoffset:800;animation:trace 1.6s .2s both}.packet{animation:transfer 5s linear infinite}.plan-scan{animation:plan-scan 7s ease-in-out infinite}.review-check{stroke-dasharray:100;stroke-dashoffset:100;animation:trace 1.4s .7s both}}
@keyframes flow{to{stroke-dashoffset:-48}}@keyframes bar{from{transform:scaleY(.04)}to{transform:none}}@keyframes glow{50%{opacity:.45}}@keyframes float-object{50%{transform:translateY(-5px)}}@keyframes trace{to{stroke-dashoffset:0}}
@keyframes transfer{0%{stroke-dashoffset:100;opacity:0}8%,88%{opacity:1}100%{stroke-dashoffset:0;opacity:0}}@keyframes plan-scan{0%,100%{transform:translateY(-55px)}50%{transform:translateY(55px)}}
@media(prefers-reduced-motion:reduce){.enter,.flow,.chartbar,.bar-deduction,.orbit,.float-object,.trace,.plan-scan,.review-check{animation:none;opacity:1;transform:none;stroke-dashoffset:0}.packet,.plan-scan{display:none}}
@media(prefers-reduced-motion:reduce){.loop-weave,.core-breathe,.intent-wash,.answer-edge,.synapse,.phase-light{animation:none;opacity:1;transform:none;stroke-dashoffset:0}.loop-energy{display:none}}
</style></defs>'''

def font_css(svg):
    characters = ''.join(''.join(t.itertext()) for t in ET.fromstring(svg).iter(f'{{{NS}}}text'))
    css = ''
    for weight in [400, 500]:
        font = TTFont(ROOT / f'assets/fonts/plex-arabic-{weight}.ttf', recalcTimestamp=False)
        options = subset.Options()
        options.flavor = 'woff2'
        sub = subset.Subsetter(options=options)
        sub.populate(text=characters)
        sub.subset(font)
        font.flavor = 'woff2'
        buf = io.BytesIO()
        font.save(buf)
        data = base64.b64encode(buf.getvalue()).decode()
        css += f'@font-face{{font-family:ArtPlex;font-style:normal;font-weight:{weight};src:url(data:font/woff2;base64,{data}) format("woff2")}}'
    return css

def save(name, title, description, body, height=640, defs=None, width=1024):
    svg = f'<svg xmlns="{NS}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="art-title art-desc"><title id="art-title">{title}</title><desc id="art-desc">{description}</desc>{DEFS if defs is None else defs}{body}</svg>'
    svg = svg.replace('<style>', '<style>' + font_css(svg), 1)
    write_variants(name,svg)
    translations=json.loads((ROOT/'tools/illustration-copy-en.json').read_text())
    def translated(match):
        value=match.group(2)
        if re.search('[\u0600-\u06ff]',value) and value not in translations:
            raise ValueError('Missing English illustration copy: '+value)
        return match.group(1)+escape(translations.get(value,value))+match.group(3)
    english=re.sub(r'(<text\b[^>]*>)(.*?)(</text>)',translated,svg)
    if name == 'desktop-hero':
        english=english.replace('Apartment · 3 rooms', '3-room apartment')
    english=re.sub(r'(<title\b[^>]*>).*?(</title>)',r'\1Estavo '+name.replace('-',' ')+r'\2',english)
    english=re.sub(r'(<desc\b[^>]*>).*?(</desc>)',r'\1Example product interface and data visualization; no verified prices or availability are asserted.\2',english)
    english=re.sub(r'@font-face\{[^}]*\}', '',english)
    english=english.replace('<style>','<style>'+font_css(english),1)
    write_variants(name+'-en',english)

def signals():
    s = '<g class="enter">' + rect(24, 28, 976, 584, 'url(#navy)', 24, 'stroke="#ffffff30" stroke-width="1"')
    s += rect(24, 28, 976, 584, 'url(#grid)', 24)
    s += text(948, 93, 'من التفاعل إلى شريحة اهتمام', 'light-display')
    s += text(948, 131, 'مثال · تفاعلات على موقعك', 'muted')
    s += line(602, 160, 948, 160, 'light-line')
    rows = [('مشاهدة', 'صفحة مشروع في التجمع الخامس'), ('بحث', 'شقة · ٣ غرف'), ('مقارنة', 'خطط سداد مختلفة')]
    for i, (label, value) in enumerate(rows):
        y = 204 + i * 100
        s += circle(930, y-7, 5, 'url(#mint-orb)') + text(905, y, label, 'light-label')
        s += text(905, y+34, value, 'muted') + line(606, y+56, 948, y+56, 'light-line')
        s += route(f'M605 {y+12}C510 {y+12} 490 309 427 309',-i*1.6,True)
        s += icon(533,y-36,68,['building','map','chart'][i])
    s += text(940, 552, 'مشاهدة · بحث · مقارنة', 'muted')
    s += '</g><g class="enter late">'
    s += circle(307, 309, 180, 'url(#aura)')
    for r in [150, 118, 88]:
        s += circle(307, 309, r, 'none', 'stroke="#a9c6e2" stroke-opacity=".18" stroke-width="1.25"')
    s += '<circle cx="307" cy="309" r="118" class="packet" pathLength="100" fill="none" stroke="#72e0bb" stroke-width="2" style="animation-duration:12s"/>'
    s += circle(307, 309, 86, 'url(#glass)', 'stroke="#ffffff30"')
    s += brand_mark(268,253,78)
    s += text(307, 331, 'اهتمامات', 'light-title', 'middle') + text(307, 364, 'من موقعك', 'muted', 'middle')
    for i,(x,y) in enumerate([(193,262),(353,169),(430,363),(247,447),(161,355)]):
        s += f'<g class="drift-slow" style="animation-delay:{-i*1.7}s">'
        s += circle(x,y,5,'url(#mint-orb)','class="orbit"') + circle(x,y,11,'none','stroke="#72e0bb" stroke-opacity=".25"') + '</g>'
    s += text(307, 151, 'التجمع الخامس · شقق', 'light-label', 'middle')
    s += route('M307 461V495',-3,True)
    s += text(307, 541, 'Meta', 'light-display', 'middle') + text(307, 574, 'لاستخدامها في التسويق', 'muted', 'middle')
    s += '</g>'
    save('meta-signals', 'التفاعلات تصنع شرائح اهتمام', 'مثال: مشاهدة مشروع والبحث عن شقة في التجمع الخامس ومقارنة السداد تتجمع في شريحة وتنتقل إلى Meta. لا يظهر تقييم للعميل.', s)

def client():
    # This scene's copy is light-on-dark (light-display / light-title / muted),
    # but its only ground was a translucent glass rect over the page's paper —
    # near-white text on near-white, so most labels were invisible. §6 gives
    # this figure a dark field; paint one, then keep the glass panels as lit
    # surfaces on top of it.
    s = rect(20, 22, 984, 596, 'url(#navy)', 24, 'stroke="#ffffff30" stroke-width="1"')
    s += rect(20, 22, 984, 596, 'url(#grid)', 24)
    s += rect(20, 22, 984, 596, 'url(#glass)', 24, 'stroke="#ffffff26"')
    s += '<g class="enter">' + text(944, 91, 'ابدأ من طلبه', 'light-display')
    s += text(944, 129, 'مثال · سياق العميل قبل المكالمة', 'muted')
    s += line(516, 162, 944, 162, 'light-line')
    for y,label,value in [(210,'المنطقة','التجمع الخامس'),(300,'نوع الوحدة','شقة · ٣ غرف'),(390,'السداد اللي قارن بينه','أكتر من خطة')]:
        s += text(944,y,label,'muted') + text(944,y+41,value,'light-title')
    s += rect(516, 480, 428, 88, 'url(#glass)', 12, 'stroke="#ffffff26"')
    s += text(920, 516, 'الميزانية', 'muted') + text(920, 551, 'حسب ما شاركه العميل', 'light-label')
    s += line(470, 74, 470, 568, 'light-line') + '</g><g class="enter late">'
    s += text(418, 96, 'التفاصيل ورا الطلب', 'light-title')
    s += circle(245,302,169,'url(#aura)')
    for d,delay in [('M126 197C116 250 143 286 188 307',0),('M340 196C343 251 316 279 296 295',-1.8),('M351 406C305 413 300 367 270 341',-3.5),('M320 306H467',-2.5)]:s+=route(d,delay,True)
    s += knowledge_loop(245,302,.57,True,'Estavo')
    for x,y,name,label in [(66,128,'building','مشاهدة'),(283,129,'chart','مقارنة'),(294,342,'chat','المساعد')]:
        s+=icon(x,y,112,name)+text(x+56,y+108,label,'muted','middle')
    s += text(245,497,'طلب واضح','light-title','middle')
    s += text(245,536,'بيانات التواصل','muted','middle') + text(245,574,'ومعاها سياق المكالمة','muted','middle')
    s += '</g>'
    save('client-context', 'ابدأ المكالمة من طلب العميل', 'مثال لملخص عميل يبحث عن شقة ثلاث غرف في التجمع الخامس وقارن دفعات ست سنوات، مع تفاصيل التصفح والمحادثة. لا توجد بيانات شخصية أو أسعار أو تقييم اهتمام.', s)

def conversation():
    s=rect(24,24,976,592,'url(#navy)',24,'stroke="#ffffff30"')
    s+=text(952,77,'المساعد يفهم طلبه، من بياناتك','light-display')
    s+=text(952,113,'مثال · محادثة على موقعك','muted')
    s+=rect(55,144,913,110,'url(#glass)',16,'stroke="#a9c6e2" stroke-opacity=".22"')
    s+=text(940,177,'طلب العميل','muted')
    s+=text(940,210,'عايز شقة ٣ غرف في التجمع الخامس','light-label')
    s+=text(940,240,'وأقارن خطط السداد المتاحة','muted small')
    s+=brand_mark(83,171,58)
    s+=text(113,226,'Estavo AI','muted','middle')
    for i,(x,w,k,v) in enumerate([(56,278,'المنطقة','التجمع الخامس'),(350,300,'نوع الوحدة','شقة · ٣ غرف'),(666,300,'خطة السداد','قارن الخطط')]):
        s+=field_fragment(x,268,w,k,v,True,i)
    for d,phase in [('M195 359V379Q195 393 237 403',0),('M500 359V371Q500 400 318 419',1),('M816 359V375Q816 388 353 435',2)]:s+=process_route(d,phase,True)
    s+=knowledge_loop(254,465,.65,True,'Estavo AI')
    s+=process_route('M409 465H523',3,True)
    s+=text(252,596,'اختيارات من عقاراتك','muted','middle')
    s+=rect(537,373,431,207,'url(#paper)',16,'stroke="#ffffff" stroke-opacity=".6"')
    s+='<path d="M553 390H952V565H553Z" class="answer-edge" pathLength="100" fill="none" stroke="#72c9b2" stroke-width="1.5"/>'
    s+=text(940,414,'تفاصيل قابلة للمقارنة','label')
    s+=text(940,447,'التجمع الخامس · شقق','small')
    s+=line(562,466,941,466)
    for y,duration in [(502,'خطة سداد أ'),(551,'خطة سداد ب')]:
        s+=text(940,y,'شقة · ٣ غرف','label')+text(709,y,duration,'label')
        s+=circle(574,y-7,4,'#27a06f',f'class="phase-light" style="animation-delay:{-(y-500)/20}s"')
    save('ai-conversation','طلب العميل يتحول لاختيارات من بياناتك','مثال توضيحي: المساعد يربط سؤال العميل بالمنطقة ونوع الوحدة والسداد، ثم يعرض تفاصيل وحدات قابلة للمقارنة من بيانات العقارات. لا يوجد تقييم آلي للعميل أو توقع سعر أو ادعاء توافر.',s)


def brand():
    s = '<ellipse cx="560" cy="350" rx="460" ry="290" fill="url(#aura)"/>'
    s += '<g class="enter">' + rect(304, 38, 674, 524, 'url(#card-face)', 18, 'filter="url(#lift)" stroke="#dbe7f2" stroke-opacity=".9"')
    s += text(942, 88, 'عقاراتك', 'title') + text(340, 85, 'موقع باسمك', 'small', 'start') + line(340, 111, 942, 111)
    s += text(942, 163, 'مكان جديد. بنفس هويتك.', 'display')
    s += text(942, 201, 'مثال · شقق في التجمع الخامس', 'small')
    for y,duration in [(226,'خطة سداد أ'),(332,'خطة سداد ب')]:
        s += rect(340,y,598,90,'#ffffff80',10,'stroke="#d4e1ec"') + plan(355,y+10,.43)
        s += text(914,y+32,'شقة · ٣ غرف','label') + text(914,y+65,'التجمع الخامس','small')
        s += text(638,y+33,'خطة السداد','micro') + text(638,y+66,duration,'label')
    # 32px below the callout put this line under the callout's lift shadow
    # (dy 26 / blur 30), which read as crowding even though nothing overlapped.
    s += text(942, 590, 'المشروع · الوحدة · السعر · السداد', 'small') + '</g>'
    s += '<g class="enter late">'
    s+=knowledge_loop(174,279,.48,False,compact=True)
    s += text(174, 419, 'بيانات واحدة', 'label','middle')
    s+=route('M282 285H318',-1)
    s+=route('M275 361V441H367',-3)
    s += text(54, 491, 'Estavo Market', 'label', 'start') + text(54, 529, 'ابحث وقارن', 'small', 'start')
    s += '</g><g class="enter later">'
    # The callout used to start at y=416, six pixels inside the second listing
    # row (which ends at 422), so it covered that row's plan and crowded the
    # caption below. It now sits clear of both: 438..534, caption moved to 566.
    s += rect(378, 438, 564, 96, 'url(#deep-face)', 16, 'filter="url(#lift)" stroke="#ffffff30"')
    s += circle(901,469,7,'url(#mint-orb)') + text(878,479,'مساعد باسمك، عارف عقاراتك','light-label')
    s += text(910,517,'من سؤال العميل لتفاصيل الوحدة','muted')
    s += text(970, 612, 'هويتك واحدة · البيانات واحدة · طرق الاستخدام مختلفة', 'small') + '</g>'
    save('brand-unified', 'هوية واحدة وبيانات واحدة', 'مثال لواجهة موقع عقاري باسمك تعرض وحدات ومخططات وخطط سداد ومساعد مرتبط بنفس البيانات وEstavo Market للبحث والمقارنة.', s)

def roi():
    s = '<g class="enter">' + brand_mark(64,49,64,'#28567f') + text(958, 73, 'إيه اللي بيتبقى من النمو؟', 'display')
    s += text(958, 114, 'مثال · شكل الحساب، بدون أسعار أو نسب متوقعة', 'small')
    # The ground plane the columns stand on, plus a soft ambient wash so the
    # extruded bars read as objects on a surface rather than flat rectangles.
    s += '<ellipse cx="516" cy="512" rx="470" ry="86" fill="url(#aura)"/>'
    s += '<path d="M71 499L922 499L964 538L113 538Z" fill="#d6e3ed" opacity=".25"/>'
    s += text(940, 201, 'النمو في القيمة − التكلفة − أثر التضخم', 'label')
    for y in [258,318,378,438,498]: s += line(85,y,931,y)
    bars=[(112,258,240,'url(#navy)','النمو في القيمة'),(328,258,84,'url(#bar-face)','التكلفة'),(544,342,72,'url(#bar-face)','أثر التضخم'),(760,414,84,'url(#mint)','العائد الحقيقي')]
    for i,(x,y,h,fill,label) in enumerate(bars):
        motion='bar-deduction' if i in [1,2] else 'chartbar'
        # No filter on the bar group: a drop-shadow filter region around an
        # extruded column renders as a rectangular smear, not a contact shadow.
        # The extrusion faces and the ground plane carry the depth instead.
        s+=f'<g class="{motion}" style="animation-delay:{i*.18}s">'
        s+=rect(x,y,126,h,fill,3)
        s+=f'<path d="M{x} {y}L{x+12} {y-9}H{x+138}L{x+126} {y}Z" fill="'+(['#47749a','#d5e5f0','#d5e5f0','#bbf1df'][i])+'"/>'
        s+=f'<path d="M{x+126} {y}L{x+138} {y-9}V{y+h-9}L{x+126} {y+h}Z" fill="'+(['#102b40','#769bb7','#769bb7','#58af95'][i])+'"/>'
        s+=f'<path d="M{x+2} {y+1}H{x+125}V{y+h-2}" fill="none" stroke="#fff" stroke-opacity=".25"/>'
        s+='</g>'+text(x+63,559,label,'label','middle')
    s += path('M250 249H340M466 333H556M682 405H772','subject trace','stroke-dasharray="4 6" style="stroke:#47749a;stroke-width:1.25"')
    s += text(391,304,'−','title','middle') + text(607,386,'−','title','middle')
    s += '</g>' + text(950, 615, 'النتيجة حسب بيانات الوحدة وتكلفتها وفترة الاحتفاظ', 'small')
    save('roi-breakdown', 'من النمو إلى العائد الحقيقي', 'رسم حسابي توضيحي بلا أسعار أو نسب: عمود النمو الكلي ثم عمودان معلّقان لخصم التكلفة والتضخم ثم عمود العائد المتبقي على نفس خط الأساس. الأحجام ليست توقعات استثمارية.', s)

def reach():
    s = '<ellipse cx="366" cy="307" rx="360" ry="292" fill="url(#aura)"/>'
    s += '<g class="enter">' + rect(662, 56, 320, 515, 'url(#card-face)', 18, 'filter="url(#lift)" stroke="#dbe7f2" stroke-opacity=".9"')
    s += text(948, 104, 'وحدتك. بنفس تفاصيلها.', 'title') + text(948,144,'مثال · على موقع باسمك','small')
    s += '<ellipse cx="820" cy="320" rx="129" ry="50" fill="#0b2239" opacity=".04"/>'
    s += '<g class="drift-tilt">' + plate(794,185,scale=.67) + '</g>'
    s += text(948,402,'التجمع الخامس','title') + text(948,446,'شقة · ٣ غرف','label')
    s += line(694,468,948,468) + text(948,510,'السعر وخطة السداد','small') + text(948,545,'العمولة اللي إنت بتحددها','small')
    s += '</g><g class="enter late">'
    s += route('M656 306H464',-1.4)
    for r in [136,225]: s += circle(330,305,r,'none','stroke="#5c91c7" stroke-opacity=".19" stroke-width="1.25"')
    nodes=[(142,166),(329,80),(512,171),(562,337),(459,492),(248,521),(103,375)]
    for i,(x,y) in enumerate(nodes):
        s += process_route(f'M330 305L{x} {y}',i)
        s += floating_icon(x-44,y-46,88,'profile',-i)
        if i in [0,2,4,6]: s += plan(x-29,y+46,.26)
    s += circle(330,305,100,'url(#core-surface)','filter="url(#shadow)" stroke="#ffffff40"')
    s += '<path d="M249 259A94 94 0 0 1 382 226" fill="none" stroke="#b3d1e6" stroke-opacity=".45" stroke-width="2"/>'
    s += brand_mark(276,256,108) + text(330,355,'Brokers','light-title','middle')
    s += text(330,620,'نفس الوحدة · نفس البيانات · شبكة أوسع','small','middle') + '</g>'
    save('listings-reach', 'وحدتك تنتقل إلى شبكة بروكرز', 'مثال لوحدة ثلاث غرف في التجمع الخامس على موقعك، تنتقل بنفس البيانات والعمولة إلى شبكة البروكرز. لا يظهر عدد مستخدمين أو عمولة مفترضة.', s)

# Hero uses its own flat geometry and motion vocabulary. Shared scenes retain
# their existing materials until they are individually redesigned.
HERO_DEFS = r'''<defs>
<linearGradient id="hero-route" x1="0" x2="1"><stop stop-color="#5c91c7" stop-opacity=".1"/><stop offset="1" stop-color="#5c91c7" stop-opacity=".65"/></linearGradient>
<linearGradient id="hero-core" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#173a55"/><stop offset=".52" stop-color="#102b45"/><stop offset="1" stop-color="#0b2239"/></linearGradient>
<radialGradient id="hero-aura"><stop stop-color="#dcecf5" stop-opacity=".92"/><stop offset=".58" stop-color="#e8f2f8" stop-opacity=".42"/><stop offset="1" stop-color="#f7fafc" stop-opacity="0"/></radialGradient>
<pattern id="hero-blueprint-grid" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" fill="none" stroke="#a9c6e2" stroke-opacity=".07" stroke-width="1"/></pattern>
<linearGradient id="hero-light"><stop stop-color="white" stop-opacity="0"/><stop offset=".5" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
<mask id="hero-sweep" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="820"><rect class="hero-sweep" x="-320" y="0" width="300" height="820" fill="url(#hero-light)"/></mask>
<filter id="hero-lift" x="-25%" y="-25%" width="160%" height="175%"><feDropShadow dy="22" stdDeviation="28" flood-color="#0b2239" flood-opacity=".09"/><feDropShadow dy="3" stdDeviation="4" flood-color="#0b2239" flood-opacity=".07"/></filter>
<style>
text{font-family:ArtPlex,Arial,sans-serif;fill:#0b2239;font-size:21px;font-weight:400}
.display{font-size:28px;font-weight:500}.light-display{font-size:28px;font-weight:500;fill:#f5f9fc}.light-title{font-size:24px;font-weight:500;fill:#f5f9fc}.title{font-size:24px;font-weight:500}.label{font-size:21px;font-weight:500}.small{font-size:19px;fill:#47749a}.micro{font-size:17px;fill:#47749a}.white{fill:#f5f9fc}.muted{fill:#a9c6e2}.hero-icon{fill:none;stroke:#28567f;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}.hero-icon-light{stroke:#a9c6e2}
.hero-route{fill:none;stroke:url(#hero-route);stroke-width:2;stroke-linecap:round}
.hero-energy{fill:none;stroke:#5c91c7;stroke-width:3;stroke-linecap:round}
.hero-orbit{transform-origin:290px 388px}
.hero-blueprint-scan{opacity:.45;transform-box:fill-box;transform-origin:center}.hero-data-glow{transform-box:fill-box;transform-origin:center}.hero-live-line{transform-box:fill-box;transform-origin:left center}
@media(prefers-reduced-motion:no-preference){.hero-sweep{animation:hero-sweep 12s cubic-bezier(.4,0,.2,1) infinite}.hero-orbit{animation:hero-orbit 12s ease-in-out infinite}.hero-status{animation:hero-status 12s ease-in-out infinite}.hero-typing-dot{animation:hero-typing 1.4s ease-in-out infinite}}
@media(prefers-reduced-motion:no-preference){
.hero-composition{animation:hero-composition-drift 14s ease-in-out infinite}
.hero-card-website{animation:hero-card-website 12s ease-in-out -1s infinite}
.hero-card-chat{animation:hero-card-chat 12s ease-in-out -5s infinite}
.hero-card-market{animation:hero-card-market 12s ease-in-out -9s infinite}
.hero-blueprint-scan{animation:hero-blueprint-scan 8s ease-in-out infinite}.hero-data-glow{animation:hero-data-glow 9s ease-in-out infinite}.hero-live-line{animation:hero-live-line 8s ease-in-out infinite}
}
@keyframes hero-composition-drift{0%,100%{transform:translate(-3px,3px)}50%{transform:translate(3px,-3px)}}
@keyframes hero-card-website{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes hero-card-chat{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes hero-card-market{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes hero-sweep{0%,12%{transform:translateX(0)}80%,100%{transform:translateX(1400px)}}
@keyframes hero-orbit{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}
.hero-typing-dot{opacity:.55}
@keyframes hero-typing{0%,70%,100%{opacity:.3;transform:translateY(0)}35%{opacity:1;transform:translateY(-2px)}}
@keyframes hero-status{0%,15%,100%{opacity:.45}45%,75%{opacity:1}}
@keyframes hero-blueprint-scan{0%,100%{transform:translateY(-54px);opacity:.12}50%{transform:translateY(54px);opacity:.58}}
@keyframes hero-data-glow{0%,100%{opacity:.42;transform:scale(.97)}50%{opacity:.9;transform:scale(1.03)}}
@keyframes hero-live-line{0%,15%,100%{transform:scaleX(.18);opacity:.3}45%,75%{transform:scaleX(1);opacity:1}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.hero-energy{display:none}}
</style></defs>'''

def hero_route(d):
    # A complete solid connection remains visible under a masked light sweep.
    return f'<path d="{d}" class="hero-route"/><path d="{d}" class="hero-energy" mask="url(#hero-sweep)"/>'

# Rotationally symmetric four-point AI glyph. Its optical centre is (12, 12),
# so placement depends on the avatar centre, not the Estavo mark's art bounds.
HERO_AI_SYMBOL = '<path d="M12 3C13 8 16 11 21 12C16 13 13 16 12 21C11 16 8 13 3 12C8 11 11 8 12 3Z" fill="#f5f9fc"/>'

def hero_ai_symbol(cx,cy,size):
    return f'<g class="hero-ai-symbol" transform="translate({cx-size/2} {cy-size/2}) scale({size/24})">{HERO_AI_SYMBOL}</g>'

def hero_detail_icon(x,y,name,size=22,light=False):
    # Compact stroke-led symbols clarify individual interface fields.
    shapes={
        'location':'<path d="M18 10c0 5-6 11-6 11S6 15 6 10a6 6 0 1 1 12 0Z"/><circle cx="12" cy="10" r="2"/>',
        'unit':'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M13 4v16M4 12h9M13 10h7"/>',
        'price':'<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 9h1M17 15h1"/>',
        'calendar':'<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M8 3v4M16 3v4M4 10h16M8 14h2M14 14h2M8 17h2"/>',
        'website':'<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
        'assistant':'<path d="M5 4h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-8l-6 3v-3a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z"/><path d="M7 9h10M7 13h6"/>',
        'compare':'<path d="M4 5h16M4 12h16M4 19h16"/><circle cx="9" cy="5" r="2" fill="#ffffff"/><circle cx="15" cy="12" r="2" fill="#ffffff"/><circle cx="9" cy="19" r="2" fill="#ffffff"/>',
        'bed':'<path d="M3 18V7M21 18v-6H3M6 12V8h5v4M11 9h7a3 3 0 0 1 3 3M3 16h18"/>',
        'check':'<path d="m5 12 4 4L19 6"/>',
    }
    return f'<g transform="translate({x} {y}) scale({size/24})" class="hero-icon{ " hero-icon-light" if light else ""}">{shapes[name]}</g>'

def hero_plan(x,y,w=240,h=200,dark=False,integrated=False):
    # Schematic three-bedroom apartment: doors, windows, kitchen, furniture
    # and circulation are drawn at a shared 240 x 200 scale.
    ground,room,ink,furniture = ('#173a55','#204760','#a9c6e2','#47749a') if dark else ('#f1f5f8','#ffffff','#28567f','#d5e5ef')
    geometry=f'''<rect width="240" height="200" rx="12" fill="{ground}"/>
    <g fill="{room}"><path d="M22 22H100V82H22Z"/><path d="M106 22H174V82H106Z"/><path d="M180 22H218V113H180Z"/><path d="M22 88H100V174H22Z"/><path d="M106 88H174V174H106Z"/></g>
    <g fill="{furniture}">
      <rect x="34" y="32" width="46" height="34" rx="3"/><rect x="116" y="32" width="42" height="34" rx="3"/><rect x="33" y="104" width="45" height="38" rx="3"/>
      <rect x="117" y="139" width="45" height="15" rx="4"/><rect x="151" y="119" width="11" height="25" rx="3"/><rect x="124" y="117" width="18" height="12" rx="3"/>
      <path d="M186 30H211V39H194V61H186Z"/><rect x="187" y="77" width="23" height="19" rx="4"/>
    </g>
    <g fill="none" stroke="{ink}" stroke-linecap="round" stroke-linejoin="round">
      <path d="M22 22H218V174H22Z" stroke-width="3"/>
      <path d="M103 22V65M103 80V111M103 133V174M177 22V103M177 125V174M22 85H66M86 85H125M145 85H177" stroke-width="2.5"/>
      <path d="M103 65H88M88 65a15 15 0 0 0 15 15M66 85V65M66 65a20 20 0 0 1 20 20M125 85V65M125 65a20 20 0 0 1 20 20M177 103H199M199 103a22 22 0 0 1-22 22M103 111H125M125 111a22 22 0 0 1-22 22" stroke-width="1" opacity=".55"/>
      <path d="M40 38H53V45H40ZM59 38H72V45H59ZM123 38H135V45H123ZM140 38H152V45H140ZM39 111H52V119H39ZM58 111H71V119H58" stroke-width="1" opacity=".6"/>
      <path d="M117 149H162M155 119V139M187 43h6M187 51h6M197 33h8M194 81v10" stroke-width="1" opacity=".6"/>
      <path d="M43 180H80M121 180H158M38 16H80M117 16H159M224 44V76" stroke-width="3"/>
      <path d="M185 174V153M185 153a21 21 0 0 1 21 21" stroke-width="1" opacity=".6"/>
    </g>'''
    if integrated:
        geometry=geometry.replace(f'<rect width="240" height="200" rx="12" fill="{ground}"/>','')
    return f'<g transform="translate({x} {y}) scale({w/240} {h/200})">{geometry}</g>' 

def hero_residential_visual(x,y,w=160,h=150):
    # Front elevation, not an isometric icon or a unit floor plan. Windows,
    # balcony rails, entrance and paving make this a residential website visual.
    geometry = '<rect width="160" height="150" rx="8" fill="#dcecf5"/><circle cx="126" cy="26" r="13" fill="#f5f9fc"/><path d="M0 119H160V150H0Z" fill="#c0d7e8"/><path d="M15 117V54H62V29H139V117Z" fill="#f5f9fc"/><path d="M62 29H139V35H62ZM15 54H62V60H15Z" fill="#28567f"/><path d="M72 43H94V63H72ZM105 43H128V63H105ZM72 76H94V96H72ZM105 76H128V96H105ZM25 68H49V88H25Z" fill="#47749a"/><path d="M82 43V63M116 43V63M82 76V96M116 76V96M37 68V88" stroke="#a9c6e2" stroke-width="1.5"/><path d="M67 64H134M67 97H134M21 89H54" stroke="#28567f" stroke-width="2"/><path d="M69 59V65M77 59V65M85 59V65M93 59V65M101 59V65M109 59V65M117 59V65M125 59V65M133 59V65M69 92V98M85 92V98M101 92V98M117 92V98M133 92V98" stroke="#28567f" stroke-width="1"/><path d="M25 103H49V117H25Z" fill="#28567f"/><path d="M37 103V117M54 117H144M11 124H145M34 132H127" stroke="#a9c6e2" stroke-width="2"/><path d="M21 137H67L54 150H0Z" fill="#e8f2f8"/><path d="M148 93V121M7 102V122" stroke="#28567f" stroke-width="2"/><circle cx="148" cy="89" r="8" fill="#5c91c7"/><circle cx="7" cy="99" r="6" fill="#5c91c7"/>'
    return f'<g transform="translate({x} {y}) scale({w/160} {h/150})">{geometry}</g>'

def hero(include_supporting=True):
    s=text(76,78,'بيانات واحدة · باسمك','display','start')+text(76,115,'مثال · التجمع الخامس','small','start')
    s+='<g class="hero-composition"><g class="hero-orbit"><path d="M142 190C-12 244 10 504 168 580C302 645 515 576 561 438" fill="none" stroke="#dcecf5" stroke-width="54" stroke-linecap="round"/><path d="M142 190C-12 244 10 504 168 580" fill="none" stroke="#5c91c7" stroke-opacity=".32" stroke-width="54" stroke-linecap="round"/></g>'
    # Three adjacent ports make the data source a shared core. Each route
    # leaves the same dock, rather than unrelated edges of a listing card.
    for name,d in [('website','M520 362C558 362 544 254 574 254'),('chat','M520 402C577 402 572 479 632 479'),('market','M520 442C563 442 529 620 529 676Q529 708 558 708')]:
        s+=f'<g class="hero-link-{name}">'+hero_route(d)+'</g>'
    s+='<g class="hero-data-core">'
    s+=rect(80,226,424,368,'#dce7ef',24)
    s+=rect(64,242,440,372,'#102b45',24)
    s+=rect(484,340,52,124,'#173a55',18)
    s+='<path d="M90 243H478" stroke="#47749a" stroke-opacity=".5"/>'
    # The brand leads; property attributes remain secondary to the blueprint.
    s+=brand_mark(386,258,92,'#f5f9fc')
    s+=text(90,292,'Estavo','light-display','start')+text(90,321,'بيانات عقاراتك','small muted','start')
    s+=rect(80,344,214,172,'url(#hero-blueprint-grid)',0)
    s+=hero_plan(84,343,204,170,True,True)
    s+=text(478,368,'مشروع أ','micro muted')+text(478,408,'٣ غرف','title white')
    s+=text(478,444,'القاهرة الجديدة','micro muted')
    # A single compact commercial strip sits under the integrated blueprint.
    s+='<path d="M88 534H478M292 549V579" stroke="#a9c6e2" stroke-opacity=".18"/>'
    s+=text(478,558,'السعر','micro muted')+text(478,585,'حسب الوحدة','body white')
    s+=hero_detail_icon(247,544,'calendar',17,True)+text(235,558,'خطة السداد','micro muted')+text(264,585,'حسب المشروع','body white')
    for y in [362,402,442]:
        s+=circle(520,y,7,'#102b45','stroke="#a9c6e2" stroke-width="1.75"')+circle(520,y,2,'#a9c6e2','class="hero-status"')
    s+='</g><g class="hero-card-website">'
    # A brokerage company homepage: browser chrome, company navigation,
    # a broad home-finding headline and property search over a residential visual.
    s+=rect(574,84,390,294,'#ffffff',20,'stroke="#dce7ef" stroke-width="1.5"')
    s+='<path d="M594 85H944Q963 85 963 104V111H575V104Q575 85 594 85Z" fill="#f1f5f8"/>'
    for x in [590,601,612]: s+=circle(x,98,2.5,'#a9c6e2')
    s+=text(940,104,'موقعك','micro')+text(773,103,'yourcompany.com','micro','middle').replace('class="micro"','class="micro" style="font-size:12px"')
    s+=text(940,143,'شركتك العقارية','label').replace('class="label"','class="label" style="font-size:18px"')
    s+=text(716,141,'العقارات','micro').replace('class="micro"','class="micro" style="font-size:13px"')
    s+=text(590,141,'عنّا','micro','start').replace('class="micro"','class="micro" style="font-size:13px"')
    s+=rect(590,157,358,172,'#102b45',10)
    s+=hero_residential_visual(599,169,128,120)
    for y,copy in [(191,'بيتك القادم'),(222,'يبدأ هنا')]:
        s+=text(934,y,copy,'title white').replace('class="title white"','class="title white" style="font-size:22px"')
    s+=text(934,249,'اكتشف عقارات تناسبك','micro muted').replace('class="micro muted"','class="micro muted" style="font-size:14px"')
    s+=rect(602,286,334,31,'#ffffff',6)
    s+=rect(607,291,58,21,'#28567f',4)
    s+=text(636,306,'بحث','micro white','middle').replace('class="micro white"','class="micro white" style="font-size:13px"')
    s+=hero_detail_icon(910,293,'location',15)+text(900,307,'المدينة أو المنطقة','micro').replace('class="micro"','class="micro" style="font-size:13px"')
    s+=text(940,361,'اكتشف العقارات','label').replace('class="label"','class="label" style="font-size:18px"')
    s+=text(590,359,'عرض الكل ←','micro','start').replace('class="micro"','class="micro" style="font-size:13px"')
    s+=circle(574,254,4,'#28567f')+'</g><g class="hero-card-chat">'
    # A literal AI chat widget: branded header, user question and an assistant
    # message with typing activity. It is an illustrative loading state.
    s+=rect(632,394,336,208,'#ffffff',20,'stroke="#dce7ef" stroke-width="1.5"')
    s+='<path d="M652 394H948Q968 394 968 414V452H632V414Q632 394 652 394Z" fill="#102b45"/>'
    s+=circle(666,423,17,'#173a55')+hero_ai_symbol(666,423,24)
    s+=text(698,429,'AI','micro white','start')+text(944,431,'مساعدك الذكي','label white')
    s+=rect(696,465,252,57,'#e8f2f8',12)
    s+='<path d="M938 516L948 528L932 522" fill="#e8f2f8"/>'
    s+=text(934,489,'إيه خطط السداد','small')+text(934,514,'لشقة ٣ غرف؟','small')
    s+=circle(666,561.5,14,'#102b45')+hero_ai_symbol(666,561.5,20)
    s+=rect(687,541,259,41,'#f1f5f8',12)
    s+=text(934,567,'بيجهّز المقارنة…','micro')
    for i,x in enumerate([703,713,723]):
        s+=circle(x,562,2.5,'#5c91c7',f'class="hero-typing-dot" style="animation-delay:{i*.16}s"')
    s+=circle(632,479,4,'#28567f')+'</g><g class="hero-card-market">'
    # Market is the broker's searchable inventory workspace. Two selected
    # example results expose property details, prices and payment plans together.
    s+=rect(558,614,406,242,'#ffffff',20,'stroke="#dce7ef" stroke-width="1.5"')
    s+=text(940,649,'Estavo Market','title')
    s+=text(582,646,'مثال · بحث ومقارنة','micro','start').replace('class="micro"','class="micro" style="font-size:12px"')
    for x,w,copy in [(788,152,'التجمع الخامس'),(635,143,'شقة · ٣ غرف')]:
        s+=rect(x,666,w,26,'#f1f5f8',6,'stroke="#dce7ef"')
        s+=text(x+w-12,684,copy,'micro').replace('class="micro"','class="micro" style="font-size:13px"')
        s+=f'<path d="m{x+10} 676 4 4 4-4" fill="none" stroke="#47749a" stroke-width="1.5" stroke-linecap="round"/>'
    s+=rect(582,666,43,26,'#28567f',6)
    s+='<g fill="none" stroke="#f5f9fc" stroke-width="1.5" stroke-linecap="round"><circle cx="601" cy="677" r="4"/><path d="m604 680 4 4"/></g>'
    for x,copy in [(940,'المشروع والوحدة'),(783,'السعر'),(684,'السداد')]:
        s+=text(x,712,copy,'micro').replace('class="micro"','class="micro" style="font-size:12px"')
    s+='<path d="M582 721H940M582 765H940M582 805H940" stroke="#dce7ef"/>'
    for y,project,price,term in [(744,'مشروع أ','حسب الوحدة','خطة سداد أ'),(783,'مشروع ب','حسب الوحدة','خطة سداد ب')]:
        s+=text(940,y,project,'label').replace('class="label"','class="label" style="font-size:16px"')
        s+=text(940,y+15,'شقة · ٣ غرف','micro').replace('class="micro"','class="micro" style="font-size:12px"')
        s+=text(783,y+5,price,'body').replace('class="body"','class="body" style="font-size:14px"')
        s+=text(684,y+5,term,'body').replace('class="body"','class="body" style="font-size:14px"')
        s+=rect(584,y-8,14,14,'#28567f',3)
        s+=f'<path d="m587 {y-1} 3 3 5-6" fill="none" stroke="#f5f9fc" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
    s+=rect(582,814,358,28,'#e8f2f8',6)
    s+=text(926,833,'اختياران للمقارنة','micro').replace('class="micro"','class="micro" style="font-size:13px"')
    s+=rect(588,818,86,20,'#28567f',4)
    s+=text(631,832,'قارن العقارات','micro white','middle').replace('class="micro white"','class="micro white" style="font-size:12px"')
    s+=circle(558,708,4,'#28567f')+'</g></g>'
    s+=text(76,719,'نفس العقارات.','title','start')+text(76,754,'على موقعك، وفي كل مقارنة.','small','start')
    save('desktop-hero','بيانات عقاراتك تصل إلى ثلاثة منتجات','مثال توضيحي: سجل عقار واحد يصل إلى موقعك ومساعدك ومقارنة خطط السداد. نتائج Market ومخطط الشقة أمثلة توضيحية وليست وحدات متاحة.',s,900,HERO_DEFS)
    write_variants('hero-residential-visual',f'<svg xmlns="{NS}" viewBox="0 0 160 150" role="img"><title>Residential architecture website visual</title>{hero_residential_visual(0,0)}</svg>')
    write_variants('hero-ai-symbol',f'<svg xmlns="{NS}" viewBox="0 0 24 24" role="img"><title>AI assistant</title>{HERO_AI_SYMBOL}</svg>')
    for name,dark in [('hero-floorplan',False),('hero-floorplan-dark',True)]:
        write_variants(name,f'<svg xmlns="{NS}" viewBox="0 0 240 200" role="img"><title>Illustrative three-bedroom apartment plan</title>{hero_plan(0,0,240,200,dark,dark)}</svg>')
    mobile=f'<svg xmlns="{NS}" viewBox="0 90 1024 510" role="img"><title>Shared property data, under your brand</title>{HERO_DEFS}{hero_scene(True)}</svg>'
    write_variants('hero-scene',mobile)
    if not include_supporting:
        return
    ai_scene=f'<svg xmlns="{NS}" viewBox="0 0 540 260" role="img"><title>Estavo property request processing</title>{DEFS}{ai_geometry()}</svg>'
    write_variants('ai-scene',ai_scene)
    unit=f'<svg xmlns="{NS}" viewBox="0 0 460 285" role="img"><title>Layered furnished unit plan</title>{DEFS}<ellipse cx="234" cy="225" rx="180" ry="45" fill="#0b2239" opacity=".045"/>{plate(194,24,scale=1.03)}</svg>'
    write_variants('unit-scene',unit)
    services=knowledge_loop(320,93,.46,False,compact=True)
    for i,(x,name) in enumerate([(65,'map'),(508,'building')]):
        services+=process_route(f'M{x+42} 94H{214 if not i else 426}',i)
        services+=icon(x,47,85,name)
    write_variants('service-scene',f'<svg xmlns="{NS}" viewBox="0 0 640 184" role="img"><title>Estavo property data, website and assistant</title>{DEFS}{services}</svg>')

def premium_hero(include_supporting=True):
    """A hero-sized product story: rich enough to lead, quiet enough to scan."""
    s='<g class="hero-composition">'

    # A broad atmosphere and open orbit give the composition scale without
    # adding more interface chrome.
    s+=f'<ellipse class="hero-data-glow" cx="274" cy="445" rx="286" ry="344" fill="url(#hero-aura)"/>'
    s+='<g class="hero-orbit">'
    s+='<path d="M160 119C-2 252 6 617 218 778" fill="none" stroke="#dcecf5" stroke-width="42" stroke-linecap="round"/>'
    s+='<path d="M160 119C-2 252 6 617 218 778" fill="none" stroke="#5c91c7" stroke-opacity=".25" stroke-width="2" stroke-linecap="round"/>'
    s+='</g>'

    # One substantial project record. The architectural plan makes the source
    # recognisable as property data rather than a generic software dashboard.
    s+='<g class="hero-data-core">'
    s+=rect(42,98,486,688,'#ffffff',30,'filter="url(#hero-lift)" stroke="#dce7ef" stroke-width="1.5"')
    s+=rect(42,98,486,9,'#28567f',5)
    s+=brand_mark(72,137,62,'#102b45')
    s+=text(500,160,'بيانات مشروع واحدة','title')+text(500,193,'مثال توضيحي · بعد المراجعة','micro')

    # The project itself is the visual anchor: plan, identity and location on
    # one deep surface, with no repeated field grid.
    s+=rect(70,226,430,252,'url(#hero-core)',20)
    s+=f'<rect x="70" y="226" width="430" height="252" rx="20" fill="url(#hero-blueprint-grid)"/>'
    s+=hero_plan(88,266,202,168,True,True)
    s+='<path class="hero-blueprint-scan" d="M96 349H282" stroke="#dcecf5" stroke-opacity=".7" stroke-width="2"/>'
    s+='<path d="M310 254V449" stroke="#a9c6e2" stroke-opacity=".18"/>'
    s+=text(472,276,'المشروع','micro muted')+text(472,313,'مشروع أ','light-display')
    s+=text(472,351,'المنطقة','micro muted')+text(472,384,'القاهرة الجديدة','light-title')
    s+=rect(326,408,146,42,'#ffffff',10,'fill-opacity=".08" stroke="#ffffff" stroke-opacity=".12"')
    # Reserve a real icon/text gutter; the English unit label is wider than
    # its Arabic counterpart and must not sit under the floor-plan glyph.
    s+=hero_detail_icon(338,419,'unit',18,True)
    s+=text(462,435,'شقة · ٣ غرف','small white').replace('class="small white"','class="small white" style="font-size:16px"')

    s+=text(498,523,'بيانات المشروع بعد المراجعة','label')
    s+=rect(70,550,202,94,'#f7fafc',14,'stroke="#dce7ef"')+hero_detail_icon(88,570,'calendar',22)
    s+=text(252,579,'السداد','micro')+text(252,615,'حسب المشروع','label')
    s+=rect(288,550,212,94,'#f7fafc',14,'stroke="#dce7ef"')+hero_detail_icon(306,570,'price',22)
    s+=text(480,579,'السعر','micro')+text(480,615,'حسب الوحدة','label')
    s+=line(70,680,500,680)
    s+=circle(484,724,6,'#28567f','class="hero-status"')+text(466,731,'نفس البيانات في كل خدمة','small')
    s+=rect(70,752,270,4,'#dce7ef',2)+rect(70,752,188,4,'#5c91c7',2,'class="hero-live-line"')
    s+='</g>'

    # Three ports leave the same maintained record and travel to recognisable
    # Estavo product surfaces.
    routes=[
        ('website','M528 286C566 286 558 194 596 194'),
        ('chat','M528 442C568 442 566 422 604 422'),
        ('market','M528 642C566 642 554 674 580 674'),
    ]
    for name,d in routes:
        s+=f'<g class="hero-link-{name}">'+hero_route(d)+'</g>'

    # Website: a real branded homepage crop, not a label card.
    s+='<g class="hero-card-website">'
    s+=rect(596,76,382,238,'#ffffff',22,'filter="url(#hero-lift)" stroke="#dce7ef" stroke-width="1.5"')
    s+=rect(596,76,382,42,'#f1f5f8',22)+rect(596,98,382,20,'#f1f5f8',0)
    for x in [618,630,642]:s+=circle(x,97,3,'#a9c6e2')
    s+=text(950,104,'موقع باسمك','micro')
    s+=rect(614,136,346,142,'#102b45',14)
    s+=hero_residential_visual(626,150,130,112)
    s+='<path d="M774 152V262" stroke="#a9c6e2" stroke-opacity=".2"/>'
    s+=text(938,166,'مشاريعك','label white')+text(938,192,'باسمك','small white')
    s+=rect(800,207,138,6,'#47749a',3)
    s+=rect(794,232,144,28,'#ffffff',7)+rect(806,242,64,6,'#a9c6e2',3)+rect(892,239,34,11,'#28567f',5)
    s+=circle(596,194,5,'#28567f')+'</g>'

    # AI: one question and one preparing answer are enough to establish the
    # product, while the navy header gives it a distinct silhouette.
    s+='<g class="hero-card-chat">'
    s+=rect(604,346,350,188,'#ffffff',22,'filter="url(#hero-lift)" stroke="#dce7ef" stroke-width="1.5"')
    s+=rect(604,346,350,54,'#102b45',22)+rect(604,378,350,22,'#102b45',0)
    s+=circle(632,373,17,'#28567f')+hero_ai_symbol(632,373,20)
    s+=text(930,382,'مساعدك الذكي','label white')
    s+=rect(736,418,196,39,'#e8f2f8',10)+text(916,444,'قارن خطط السداد','micro')
    s+=rect(626,473,278,38,'#f1f5f8',10)
    for i,x in enumerate([650,662,674]):s+=circle(x,492,3,'#5c91c7',f'class="hero-typing-dot" style="animation-delay:{i*.16}s"')
    s+=rect(698,488,184,6,'#d5e5ef',3)
    s+=circle(604,422,5,'#28567f')+'</g>'

    # Market: compact filters and two real project rows make this recognisable
    # without shrinking a full dashboard into the hero.
    s+='<g class="hero-card-market">'
    s+=rect(580,574,404,242,'#ffffff',22,'filter="url(#hero-lift)" stroke="#dce7ef" stroke-width="1.5"')
    s+=circle(616,614,20,'#e8f2f8')+hero_detail_icon(604,602,'compare',24)
    s+=text(956,619,'Estavo Market','label')+text(956,647,'بحث ومقارنة للسوق','micro')
    s+=rect(604,666,356,38,'#f7fafc',9)+rect(616,677,104,16,'#e8f2f8',5)+rect(730,677,92,16,'#e8f2f8',5)+rect(836,675,110,20,'#28567f',6)
    for y,name,term in [(728,'مشروع أ','خطة سداد أ'),(766,'مشروع ب','خطة سداد ب')]:
        s+=text(944,y,name,'label')+text(752,y,term,'micro')+rect(620,y-13,14,14,'#28567f',3)+f'<path d="m623 {y-6} 3 3 5-6" fill="none" stroke="#f5f9fc" stroke-width="1.5" stroke-linecap="round"/>'
    s+=circle(580,674,5,'#28567f')+'</g>'
    s+='</g>'

    save('desktop-hero','بيانات واحدة لثلاث طرق استخدام','مثال توضيحي لبيانات مشروع واحدة تصل إلى موقع باسمك ومساعد ذكي وEstavo Market.',s,900,HERO_DEFS)

    # Purpose-built phone scene: the same hierarchy in three compact outputs,
    # without shrinking the 1024px desktop labels into illegibility.
    mobile='<g class="hero-composition">'
    mobile+=f'<ellipse class="hero-data-glow" cx="112" cy="218" rx="124" ry="190" fill="url(#hero-aura)"/>'
    mobile+=rect(16,22,180,386,'#ffffff',20,'filter="url(#hero-lift)" stroke="#dce7ef" stroke-width="1.5"')
    mobile+=rect(16,22,180,6,'#28567f',3)
    mobile+=brand_mark(30,45,39,'#102b45')
    mobile+=text(182,62,'بيانات واحدة','label').replace('class="label"','class="label" style="font-size:14px"')
    mobile+=text(182,83,'مشروع أ','micro')
    mobile+=rect(30,101,152,132,'url(#hero-core)',13)
    mobile+=f'<rect x="30" y="101" width="152" height="132" rx="13" fill="url(#hero-blueprint-grid)"/>'
    mobile+=hero_plan(39,117,134,99,True,True)
    mobile+='<path class="hero-blueprint-scan" d="M43 164H169" stroke="#dcecf5" stroke-opacity=".65" stroke-width="1.5"/>'
    mobile+=text(178,260,'القاهرة الجديدة','micro')
    mobile+=rect(30,275,152,45,'#f7fafc',9,'stroke="#dce7ef"')
    mobile+=hero_detail_icon(40,286,'unit',18)+text(174,301,'شقة · ٣ غرف','label').replace('class="label"','class="label" style="font-size:14px"')
    mobile+=rect(30,329,152,30,'#f7fafc',8)+hero_detail_icon(40,335,'calendar',16)+text(174,349,'حسب المشروع','micro').replace('class="micro"','class="micro" style="font-size:12px"')
    mobile+=rect(30,367,152,30,'#f7fafc',8)+hero_detail_icon(40,373,'price',16)+text(174,387,'حسب الوحدة','micro').replace('class="micro"','class="micro" style="font-size:12px"')

    for name,d in [('website','M196 105C208 105 202 75 216 75'),('chat','M196 214H216'),('market','M196 327C208 327 204 350 216 350')]:
        mobile+=f'<g class="hero-link-{name}">'+hero_route(d)+'</g>'

    mobile+='<g class="hero-card-website">'
    mobile+=rect(216,24,158,108,'#ffffff',14,'stroke="#dce7ef" stroke-width="1.5"')
    mobile+=text(360,50,'موقع باسمك','label').replace('class="label"','class="label" style="font-size:14px"')
    mobile+=rect(230,66,130,50,'#102b45',8)+hero_residential_visual(236,71,51,40)
    mobile+=rect(298,76,52,5,'#f5f9fc',3)+rect(306,88,44,4,'#a9c6e2',2)+rect(298,99,52,9,'#ffffff',3)
    mobile+=circle(216,75,3.5,'#28567f')+'</g>'

    mobile+='<g class="hero-card-chat">'
    mobile+=rect(216,154,158,120,'#ffffff',14,'stroke="#dce7ef" stroke-width="1.5"')
    mobile+=rect(216,154,158,36,'#102b45',14)+rect(216,176,158,14,'#102b45',0)
    mobile+=circle(236,172,11,'#28567f')+hero_ai_symbol(236,172,14)
    mobile+=text(360,177,'مساعدك الذكي','label white').replace('class="label white"','class="label white" style="font-size:14px"')
    mobile+=rect(244,203,116,25,'#e8f2f8',7)+text(352,220,'قارن خطط السداد','micro').replace('class="micro"','class="micro" style="font-size:9.5px"')
    mobile+=rect(230,238,112,22,'#f1f5f8',7)
    for i,x in enumerate([244,252,260]):mobile+=circle(x,249,2,'#5c91c7',f'class="hero-typing-dot" style="animation-delay:{i*.16}s"')
    mobile+=circle(216,214,3.5,'#28567f')+'</g>'

    mobile+='<g class="hero-card-market">'
    mobile+=rect(216,296,158,112,'#ffffff',14,'stroke="#dce7ef" stroke-width="1.5"')
    mobile+=circle(235,317,12,'#e8f2f8')+hero_detail_icon(228,310,'compare',14)
    mobile+=text(360,322,'Estavo Market','label').replace('class="label"','class="label" style="font-size:14px"')
    mobile+=text(360,342,'بحث ومقارنة','micro').replace('class="micro"','class="micro" style="font-size:11px"')
    mobile+=rect(230,353,130,18,'#f7fafc',5)+rect(238,359,42,5,'#a9c6e2',3)+rect(308,357,44,9,'#28567f',4)
    mobile+=text(352,390,'مشروع أ','micro')+rect(234,379,10,10,'#28567f',2)
    mobile+=circle(216,350,3.5,'#28567f')+'</g></g>'
    save('mobile-hero','بيانات واحدة لثلاث طرق استخدام','نسخة هاتف مختصرة توضح بيانات مشروع واحدة تصل إلى موقع باسمك ومساعد ذكي وEstavo Market.',mobile,430,HERO_DEFS,390)
    write_variants('hero-ai-symbol',f'<svg xmlns="{NS}" viewBox="0 0 24 24" role="img"><title>AI assistant</title>{HERO_AI_SYMBOL}</svg>')
    if not include_supporting:
        return

    ai_scene=f'<svg xmlns="{NS}" viewBox="0 0 540 260" role="img"><title>Estavo property request processing</title>{DEFS}{ai_geometry()}</svg>'
    write_variants('ai-scene',ai_scene)
    unit=f'<svg xmlns="{NS}" viewBox="0 0 460 285" role="img"><title>Layered furnished unit plan</title>{DEFS}<ellipse cx="234" cy="225" rx="180" ry="45" fill="#0b2239" opacity=".045"/>{plate(194,24,scale=1.03)}</svg>'
    write_variants('unit-scene',unit)

def hero_scene(compact=False):
    # Geometry only: the phone's real fields and product previews live in HTML.
    s='<g class="hero-orbit"><path d="M240 208C85 221 77 449 267 504C451 557 703 492 831 302" fill="none" stroke="#dcecf5" stroke-width="60" stroke-linecap="round"/><path d="M240 208C85 221 77 449 267 504" fill="none" stroke="#5c91c7" stroke-opacity=".35" stroke-width="60" stroke-linecap="round"/></g>'
    s+=hero_route('M472 323C620 323 600 240 746 240')
    s+=hero_route('M472 371C640 371 622 470 758 470')
    s+=rect(270,248,202,202,'#102b45',48)+brand_mark(306,284,130)
    s+=hero_plan(746,162,164,128)
    s+=rect(758,414,172,110,'#ffffff',20)
    s+='<path d="M786 442H838M786 470H902M786 497H861" stroke="#28567f" stroke-width="3" stroke-linecap="round"/><path d="M855 442H902" stroke="#5c91c7" stroke-width="3" stroke-linecap="round"/>'
    return s

def ai_geometry():
    s=knowledge_loop(254,128,.84,True,compact=True)
    for i,(x,y) in enumerate([(47,54),(57,174),(454,113)]):
        s+=circle(x,y,12,'#e1edf5','stroke="#92bcd8" stroke-opacity=".5"')
        s+=circle(x,y,4,'#72c9b2',f'class="phase-light" style="animation-delay:{-i*2}s"')
    for d,phase in [('M60 54C133 54 134 104 171 105',0),('M70 174C123 174 134 144 171 144',1),('M337 128H441',3)]:s+=process_route(d,phase)
    return s


def explorer():
    s='<ellipse cx="650" cy="355" rx="385" ry="275" fill="url(#aura)"/>'
    s+='<g class="enter">'+rect(278,34,712,571,'url(#card-face)',20,'filter="url(#lift)" stroke="#dbe7f2" stroke-opacity=".9"')
    s+=brand_mark(751,57,45,'#28567f')+text(952,78,'Estavo Market','title')+text(312,78,'مثال · البحث والمقارنة','micro','start')+line(312,99,952,99)
    s+=rect(309,119,651,181,'#edf3f7',12,'stroke="#d4e1ec"')
    for x,label,value in [(934,'المنطقة','التجمع الخامس'),(644,'نوع الوحدة','شقة · ٣ غرف')]:
        s+=text(x,156,label,'micro')+text(x,195,value,'title')
    s+=line(340,223,932,223)+icon(336,236,48,'chart')
    s+=text(932,264,'السعر وخطة السداد','label')+text(649,264,'تفاصيل قابلة للمقارنة','small')
    s+=text(945,340,'التجمع الخامس · شقق','label')+text(320,340,'تفاصيل قابلة للمقارنة','micro','start')
    s+=line(310,361,958,361)
    xs=[940,763,590,412]
    for x,v in zip(xs,['المكان','الوحدة','السعر','السداد']): s+=text(x,395,v,'small')
    for y,vals in [(439,['التجمع الخامس','٣ غرف','حسب الوحدة','خطة سداد أ']),(488,['التجمع الخامس','٣ غرف','حسب الوحدة','خطة سداد ب'])]:
        for x,v in zip(xs,vals):s+=text(x,y,v,'body')
        s+=line(310,y+17,958,y+17)
    s+=circle(929,549,4,'#27a06f')+text(910,558,'بيانات المشروع بعد المراجعة','small')
    s+=path('M314 574L344 560L380 567L414 536L447 541L480 518','subject trace')+'</g>'
    for i,(name,label,sub) in enumerate([('messages','WhatsApp','محادثات'),('plan','PDF','مخططات'),('building','Web','صفحات متفرّقة')]):
        y=102+i*180;s+='<g class="enter late">'+floating_icon(50,y-10,135,name,-i*2)+text(118,y+126,label,'label','middle')+text(118,y+156,sub,'micro','middle')+'</g>'
        s+=route(f'M183 {y+50}H216Q244 {y+50} 244 319H274',-i*1.7)
    save('market-explorer','من مصادر متفرّقة إلى مقارنة واضحة','مثال لصفحة بحث عقاري تعرض المنطقة ونوع الوحدة ووحدات ثلاث غرف وخطط سداد خمس وست سنوات، دون أسعار أو ادعاء توافر. المصادر تتجمع في نفس المقارنة.',s)

def updates():
    s='<ellipse cx="400" cy="360" rx="370" ry="270" fill="url(#aura)"/>'
    s+='<g class="enter">'+rect(34,56,511,544,'url(#card-face)',20,'filter="url(#lift)" stroke="#dbe7f2" stroke-opacity=".9"')
    s+=text(506,99,'بيانات السوق بعد التحديث','title')+text(506,128,'مثال · الأسعار محجوبة','micro')
    s+=rect(63,149,452,139,'#edf3f7',12) + plan(75,163,.69)
    s+=text(490,194,'نوع الوحدة','micro')+text(490,236,'شقة · ٣ غرف','label')
    s+=text(505,324,'التجمع الخامس','label')+text(65,324,'المشروع والمنطقة','micro','start')
    s+=rect(283,355,131,153,'#e6f4ef',10)
    for x,v in [(502,'البيانات'),(401,'الحالي'),(199,'السابق')]:s+=text(x,378,v,'micro')
    s+=text(504,420,'السعر','label')+rect(310,409,79,7,'#a8becf',4)+rect(122,409,77,7,'#c7d5df',4)
    s+=text(504,466,'السداد','label')+text(402,466,'خطة حالية','label')+text(199,466,'خطة سابقة','small')
    s+=path('M224 455H266M257 450L266 455L257 460','subject')
    s+=line(64,515,512,515)+circle(486,549,4,'#27a06f','class="orbit"')+text(466,557,'تحديث بعد مراجعة البيانات','small')+'</g>'
    s+=icon(552,251,154,'shield')+text(630,433,'مراجعة إستاڤو','label','middle')+text(630,465,'نتأكد قبل التحديث','small','middle')
    s+=process_route('M581 338H551',3)
    for i,(name,label,sub) in enumerate([('building','مشروع جديد','المشروع والمنطقة'),('chart','سعر اتعدّل','السعر قبل وبعد'),('plan','السداد اتغيّر','المقدّم وفترة التقسيط')]):
        y=48+i*177;s+='<g class="enter late">'+floating_icon(797,y-6,116,name,-i*2)+text(961,y+111,label,'label')+text(961,y+143,sub,'micro')+'</g>'
        s+=route(f'M809 {y+49}C733 {y+49} 735 338 690 338',-i*1.6)
    save('market-updates','التغييرات تمر بالمراجعة','مثال لتغييرات مشروع وسعر وخطة سداد تتجمع في مراجعة ثم تظهر في مقارنة السابق والحالي، مع مخطط الوحدة. الأسعار محجوبة.',s)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hero-only', action='store_true', help='Rebuild only the homepage hero and its motion variants')
    args = parser.parse_args()
    if args.hero_only:
        premium_hero(include_supporting=False)
    else:
        signals(); client(); conversation(); brand(); roi(); reach(); premium_hero(); explorer(); updates()
    for asset in OUT.glob('estavo-*.svg'):
        ET.parse(asset)
    print('Built homepage hero variants; SVG parsing passed.' if args.hero_only else 'Built nine animated vector scenes and bilingual variants; SVG parsing passed.')
