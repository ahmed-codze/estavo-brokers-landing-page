#!/usr/bin/env python3
"""Estavo Market landing page — vector illustrations.

Draws every product scene on /market/ as a standalone SVG, in Arabic (RTL)
and English (LTR), with a desktop and a phone composition each:

  hero (animated + still) · record · step-ask · step-find · step-send ·
  chat · pdf · change

Layouts are written in logical coordinates (x grows from the inline-start
edge) and mirrored for Arabic, so both languages share one drawing.
Fonts are IBM Plex Sans Arabic subsets embedded as WOFF2, icons are copied
from assets/img/icons/estavo-home.svg, so each file renders on its own.

The example data is the homepage fixture (tools/data/home-fixture.json):
B is best on lowest down payment, C is ready but 300K over budget.

Usage: python3 tools/build-market-art.py
Needs: python3 -m pip install fonttools brotli uharfbuzz
"""
import base64
import io
import re
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont
import uharfbuzz as hb

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/img/market'

# ── Palette: Estavo navy + Estavo blue ───────────────────────────────
NAVY = '#0b2239'
INK = '#0f2236'
BLUE = '#163e69'
MID = '#47749a'
MUTE = '#7d9ab4'
LINE = '#d3dfea'
SOFT = '#f0f5fa'
WASH = '#e6eef5'
MIST = '#f3f6f9'
WHITE = '#ffffff'
T2 = '#4b5e72'
T3 = '#6c7e92'
WARN = '#9a4d0b'
WARNBG = '#fdf5ec'
WARNLN = '#e5c39b'
ONDARK = '#d6e3f0'

ELEC = '#4f9cf0'   # electric accent: glows, flows and scans only (animated layer)
ANIM = False      # set per build: animated file or still companion

FONTS = {w: TTFont(ROOT / f'assets/fonts/plex-arabic-{w}.ttf', recalcTimestamp=False) for w in (400, 500, 600)}
CMAPS = {w: f.getBestCmap() for w, f in FONTS.items()}

SPRITE = (ROOT / 'assets/img/icons/estavo-home.svg').read_text()
SYMBOLS = {m.group(1): m.group(0) for m in re.finditer(r'<symbol id="([^"]+)"[\s\S]*?</symbol>', SPRITE)}

SPARK = 'M12 2.5c.6 4.6 2.9 6.9 7.5 7.5-4.6.6-6.9 2.9-7.5 7.5-.6-4.6-2.9-6.9-7.5-7.5 4.6-.6 6.9-2.9 7.5-7.5z'
TICKS = 'M1 6.5 3.6 9 9 3M6.4 8.4 7 9l5.4-6'


HB = {w: hb.Font(hb.Face(hb.Blob.from_file_path(str(ROOT / f'assets/fonts/plex-arabic-{w}.ttf')))) for w in (400, 500, 600)}


def tw(text, size, weight=400):
    """Shaped advance width (HarfBuzz), so Arabic joins are measured as rendered."""
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(HB[weight], buf, {'kern': True, 'liga': True})
    return sum(p.x_advance for p in buf.glyph_positions) * size / 1000


def wrap(runs, size, maxw):
    """Wrap [(text, weight)] runs into lines of runs no wider than maxw."""
    tokens = []
    for text, weight in runs:
        parts = text.split(' ')
        for i, p in enumerate(parts):
            if p:
                tokens.append((p, weight, i < len(parts) - 1))
    lines, cur, width = [], [], 0
    prev_spaced = True
    for word, weight, spaced in tokens:
        w = tw(word, size, weight)
        sp = tw(' ', size, weight)
        glued = not prev_spaced
        prev_spaced = spaced
        if glued and cur:
            cur.append((word, weight, spaced))
            width += w
            continue
        if cur and width + sp + w > maxw:
            lines.append(cur)
            cur, width = [], 0
        cur.append((word, weight, spaced))
        width += (sp if len(cur) > 1 else 0) + w
    if cur:
        lines.append(cur)
    out = []
    for line in lines:
        merged = []
        for i, (word, weight, spaced) in enumerate(line):
            text = word + (' ' if spaced and i < len(line) - 1 else '')
            if merged and merged[-1][1] == weight:
                merged[-1] = (merged[-1][0] + text, weight)
            else:
                merged.append((text, weight))
        out.append(merged)
    return out


def runs_width(runs, size):
    return sum(tw(t, size, w) for t, w in runs)


class Art:
    def __init__(self, W, H, lang, uid):
        self.W, self.H, self.lang, self.uid = W, H, lang, uid
        self.rtl = lang == 'ar'
        self.parts = []
        self.icons = set()
        self.chars = {400: set(), 500: set(), 600: set()}
        self.css = ''
        self.defs = []
        self.anim = ANIM
        self.n = 0

    # logical → physical
    def px(self, x, w=0):
        return round(self.W - x - w, 2) if self.rtl else round(x, 2)

    def add(self, s):
        self.parts.append(s)

    def open(self, cls='', style='', transform=''):
        attrs = ''
        if cls:
            attrs += f' class="{cls}"'
        if style:
            attrs += f' style="{style}"'
        if transform:
            attrs += f' transform="{transform}"'
        self.add(f'<g{attrs}>')

    def close(self):
        self.add('</g>')

    # ── motion helpers (no-ops in the still companion) ──
    def seq(self, cls, delay, style=''):
        if self.anim:
            self.open(cls, f'animation-delay:{delay}ms;{style}')
        else:
            self.open()

    def fx(self, s):
        if self.anim:
            self.add(s)

    def nid(self, p='i'):
        self.n += 1
        return f'{p}{self.uid}{self.n}'

    def type_open(self, x, y, w, h, delay, dur=900):
        """Typing reveal for a text run starting at logical x (mask grows from the reading start)."""
        if not self.anim:
            self.open()
            return
        mid = self.nid('m')
        origin = 'right' if self.rtl else 'left'
        self.defs.append(f'<mask id="{mid}"><rect class="ty" x="{self.px(x, w)}" y="{y}" width="{w}" height="{h}" fill="#fff" '
                         f'style="transform-origin:{origin} center;animation-delay:{delay}ms;animation-duration:{dur}ms"/></mask>')
        self.add(f'<g mask="url(#{mid})">')

    def ring(self, x, y, w, h, r, delay, color=None, sw=2):
        """Pulsing halo around a 'best' surface."""
        self.fx(f'<rect class="ring" x="{self.px(x, w)}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" '
                f'stroke="{color or ELEC}" stroke-width="{sw}" style="animation-delay:{delay}ms"/>')

    def caret(self, x, y, h, delay, color=None):
        self.fx(f'<rect class="bl" x="{self.px(x, 2)}" y="{y}" width="2" height="{h}" rx="1" fill="{color or BLUE}" style="animation-delay:{delay}ms"/>')

    def dots(self, x, y, delay, hide_after=900):
        """'Brokers AI is typing' bubble that shows, then gives way to the answer."""
        if not self.anim:
            return
        self.add(f'<g class="th" style="animation-delay:{delay}ms;animation-duration:{hide_after}ms">')
        self.rect(x, y, 58, 30, r=15, fill='#edf3f9', stroke='#d9e4ef')
        for k in range(3):
            self.add(f'<circle class="db" cx="{self.px(x + 17 + k * 12)}" cy="{y + 15}" r="3.2" fill="{MID}" style="animation-delay:{k * 150}ms"/>')
        self.add('</g>')

    def rect(self, x, y, w, h, r=0, fill='none', stroke=None, sw=1, dash=None, opacity=None, filt=None, extra=''):
        a = f'<rect x="{self.px(x, w)}" y="{round(y, 2)}" width="{round(w, 2)}" height="{round(h, 2)}"'
        if r:
            a += f' rx="{r}"'
        a += f' fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        if filt:
            a += f' filter="url(#{filt}-{self.uid})"'
        self.add(a + extra + '/>')

    def circle(self, cx, cy, r, fill='none', stroke=None, sw=1, opacity=None):
        a = f'<circle cx="{self.px(cx)}" cy="{cy}" r="{r}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        self.add(a + '/>')

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1, dash=None, opacity=None):
        a = f'<line x1="{self.px(x1)}" y1="{y1}" x2="{self.px(x2)}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        self.add(a + ' stroke-linecap="round"/>')

    def text(self, x, y, runs, size=15, fill=INK, weight=400, anchor='start', opacity=None):
        if isinstance(runs, str):
            runs = [(runs, weight)]
        if self.rtl:
            runs = [(t.replace(' · ', '\u200f · \u200f'), w) for t, w in runs]
        for t, w in runs:
            self.chars[w].update(t)
        a = f'<text x="{self.px(x)}" y="{round(y, 2)}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"'
        if self.rtl:
            a += ' direction="rtl"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        if len(runs) == 1:
            t, w = runs[0]
            self.add(f'{a} font-weight="{w}">{escape(t)}</text>')
        else:
            inner = ''.join(f'<tspan font-weight="{w}"{self._tfill(t)}>{escape(t)}</tspan>' for t, w in runs)
            self.add(f'{a}>{inner}</text>')

    def _tfill(self, t):
        return ''

    def lines(self, x, y, runs, size, maxw, fill=INK, lh=1.6, anchor='start', weight=400, bold_fill=None):
        """Wrapped paragraph; returns the y after the last line."""
        if isinstance(runs, str):
            runs = [(runs, weight)]
        for i, line in enumerate(wrap(runs, size, maxw)):
            if bold_fill:
                for t, w in line:
                    self.chars[w].update(t)
                a = f'<text x="{self.px(x)}" y="{round(y + i * size * lh, 2)}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"'
                if self.rtl:
                    a += ' direction="rtl"'
                inner = ''.join(
                    f'<tspan font-weight="{w}"' + (f' fill="{bold_fill}"' if w == 600 else '') + f'>{escape(t)}</tspan>'
                    for t, w in line)
                self.add(f'{a}>{inner}</text>')
            else:
                self.text(x, y + i * size * lh, line, size, fill, anchor=anchor)
        return y + (len(wrap(runs, size, maxw)) - 1) * size * lh

    def icon(self, name, x, y, size, color=BLUE, sw=None):
        self.icons.add(name)
        style = f'color:{color}'
        self.add(f'<use href="#ic-{name}" x="{self.px(x, size)}" y="{y}" width="{size}" height="{size}" style="{style}"/>')

    def spark(self, cx, cy, size, fill=WHITE):
        s = size / 24
        self.add(f'<path d="{SPARK}" fill="{fill}" transform="translate({self.px(cx) - 12 * s} {cy - 12 * s}) scale({s})"/>')

    def ticks(self, x, y, color=BLUE):
        self.add(f'<path d="{TICKS}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" transform="translate({self.px(x, 13)} {y})"/>')

    def arrow(self, x, y, size, color=MUTE):
        """Arrow pointing forward in the reading direction."""
        s = size / 24
        flip = f' translate({size} 0) scale(-1 1)' if not self.rtl else ''
        self.add(f'<g transform="translate({self.px(x, size)} {y}){flip} scale({s})"><path d="M19 12H5m6-6-6 6 6 6" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')

    def pill(self, x, y, label, size=12, fill=WHITE, stroke=LINE, color=T3, weight=500, h=None, pad=10, anchor_end=False, dash=None):
        w = tw(label, size, weight) + pad * 2
        h = h or size + 12
        if anchor_end:
            x = x - w
        self.rect(x, y, w, h, r=h / 2, fill=fill, stroke=stroke, dash=dash)
        self.text(x + w / 2, y + h / 2 + size * 0.36, label, size, color, weight, anchor='middle')
        return w

    def svg(self, title):
        defs = ''.join(
            SYMBOLS[n].replace(f'id="{n}"', f'id="ic-{n}"') for n in sorted(self.icons))
        defs += (
            f'<filter id="sh-{self.uid}" x="-20%" y="-20%" width="140%" height="160%">'
            f'<feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="{NAVY}" flood-opacity=".13"/>'
            f'<feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="{NAVY}" flood-opacity=".06"/></filter>'
            f'<filter id="ss-{self.uid}" x="-20%" y="-20%" width="140%" height="170%">'
            f'<feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="{NAVY}" flood-opacity=".12"/></filter>'
            f'<filter id="sd-{self.uid}" x="-20%" y="-20%" width="140%" height="160%">'
            f'<feDropShadow dx="0" dy="24" stdDeviation="26" flood-color="#000" flood-opacity=".32"/></filter>'
            f'<pattern id="dots-{self.uid}" width="18" height="18" patternUnits="userSpaceOnUse">'
            f'<circle cx="1.5" cy="1.5" r="1.1" fill="{BLUE}" opacity=".10"/></pattern>'
        )
        defs += ''.join(self.defs)
        css = 'text{font-family:MkPlex,"IBM Plex Sans Arabic",Arial,sans-serif;font-variant-numeric:tabular-nums}'
        css += font_css(self.chars)
        if self.anim:
            E = 'cubic-bezier(.22,.61,.36,1)'
            css += (
                '@keyframes r{from{opacity:0;transform:translateY(14px)}}'
                '@keyframes p{from{opacity:0;transform:scale(.86)}}'
                '@keyframes f{from{opacity:0}}'
                '@keyframes sw{0%{transform:translateX(0) skewX(-18deg);opacity:0}6%{opacity:1}40%{transform:translateX(var(--sw)) skewX(-18deg);opacity:1}41%,100%{transform:translateX(var(--sw)) skewX(-18deg);opacity:0}}'
                '@keyframes ring{0%{opacity:.75;transform:scale(1)}70%,100%{opacity:0;transform:scale(1.045)}}'
                '@keyframes pu{0%,100%{opacity:.4}50%{opacity:1}}'
                '@keyframes fl{to{stroke-dashoffset:-24}}'
                '@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}'
                '@keyframes ty{from{transform:scaleX(0)}}'
                '@keyframes pk{0%{transform:translate(0,0);opacity:0}12%{opacity:1}88%{opacity:1}100%{transform:translate(var(--dx),var(--dy));opacity:0}}'
                '@keyframes sc{0%{transform:translateY(0);opacity:0}10%{opacity:1}80%{opacity:1}100%{transform:translateY(var(--sd));opacity:0}}'
                '@keyframes th{0%{opacity:0}12%,80%{opacity:1}100%{opacity:0}}'
                '@keyframes db{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}'
                '@keyframes gl{0%,100%{opacity:.25}50%{opacity:.7}}'
                f'.r{{animation:r .62s {E} both}}'
                f'.p{{animation:p .42s {E} both;transform-box:fill-box;transform-origin:center}}'
                '.f{animation:f .6s ease-out both}'
                f'.sw{{animation:sw 7s {E} infinite both}}'
                '.ring{animation:ring 2.8s ease-out infinite both;transform-box:fill-box;transform-origin:center}'
                '.pu{animation:pu 2.4s ease-in-out infinite both}'
                '.fl{animation:fl 1.1s linear infinite}'
                '.bl{animation:bl 1.05s steps(1) infinite both}'
                '.ty{animation:ty .9s steps(30) both;transform-box:fill-box}'
                '.pk{animation:pk 5.5s linear infinite both}'
                f'.sc{{animation:sc 4.6s {E} infinite both}}'
                '.th{animation:th .9s ease both}'
                '.db{animation:db .9s ease-in-out infinite;transform-box:fill-box}'
                '.gl{animation:gl 3.2s ease-in-out infinite both}'
                '@media (prefers-reduced-motion:reduce){*{animation:none!important}.th{display:none}}'
            )
        body = '\n'.join(self.parts)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W} {self.H}" width="{self.W}" height="{self.H}" '
            f'role="img" lang="{self.lang}"><title>{escape(title)}</title>'
            f'<style>{css}</style><defs>{defs}</defs>\n{body}\n</svg>\n'
        )


def font_css(chars):
    css = ''
    for weight, used in chars.items():
        used = set(used) | set(' 0123456789')
        if not used:
            continue
        font = TTFont(ROOT / f'assets/fonts/plex-arabic-{weight}.ttf', recalcTimestamp=False)
        options = subset.Options()
        options.flavor = 'woff2'
        options.hinting = False
        options.desubroutinize = True
        sub = subset.Subsetter(options=options)
        sub.populate(text=''.join(sorted(used)))
        sub.subset(font)
        font.flavor = 'woff2'
        buf = io.BytesIO()
        font.save(buf)
        data = base64.b64encode(buf.getvalue()).decode()
        css += f'@font-face{{font-family:MkPlex;font-weight:{weight};src:url(data:font/woff2;base64,{data}) format("woff2")}}'
    return css


# ── Copy ─────────────────────────────────────────────────────────────
C = {
    'ar': {
        'brand': 'Estavo Market', 'example': 'مثال توضيحي',
        'city': 'التجمع', 'start_from': 'تبدأ من', 'unit_chip': 'شقة 3 غرف',
        'f_delivery': 'التسليم', 'f_area': 'مساحة الوحدة', 'f_down': 'المقدم', 'f_inst': 'التقسيط',
        'inst': 'حتى {n} سنين', 'inst_short': '7 سنين', 'area_v': '{n} م²', 'period': 'المدة',
        'best_short': 'أنسب لأولويته', 'alt_short': 'بديل · +300K', 'match': 'مطابق', 'over_note': 'فوق الميزانية',
        'ranked': 'مرتبة حسب أقل مقدم', 'units_from': 'الوحدات تبدأ من',
        'pills': ['التجمع', 'سكني'], 'phase': 'المرحلة 1 · استلام 2027', 'available': 'متاح',
        'nav': ['المعرض', 'خطط الدفع', 'نماذج الوحدات', 'الموقع', 'الملفات'], 'plan_tag': 'خطة سداد',
        'chat_title': 'مساعد إستاڤو', 'chat_sub': 'مستشارك الذكي', 'free_pill': 'مجاني',
        'ask_chip': 'اسأل العميل: الاستلام فارق معاه؟',
        'ud_title': 'تفاصيل الوحدة', 'ud_head': ('المواصفة', 'التفاصيل'),
        'ud_rows': [('نوع الوحدة', 'شقة 3 غرف'), ('السعر', '8.0M'), ('المساحة', '158 م²'), ('الغرف', '3'),
                    ('التشطيب', 'كامل'), ('المشروع', 'مشروع ب'), ('الاستلام', '2027')],
        'search': 'شقة 3 غرف في التجمع لحد 8M، والأهم أقل مقدم',
        'search_m': 'شقة 3 غرف في التجمع، أقل مقدم',
        'chips': ['التجمع', '3 غرف', 'حتى 8M', 'مقدم حتى 1.5M'], 'prio': 'الأولوية: أقل مقدم',
        'cols': ['المشروع', 'السعر', 'المقدم', 'السداد', 'الاستلام'],
        'units': {
            'B': ('ب', 'مشروع ب', '158 م² · تشطيب كامل', '8.0M', '1.2M', '7 سنين', '2027'),
            'A': ('أ', 'مشروع أ', '165 م² · نص تشطيب', '7.9M', '1.4M', '8 سنين', '2028'),
            'C': ('ج', 'مشروع ج', '180 م² · تشطيب كامل', '8.3M', '1.5M', '6 سنين', 'فوري'),
        },
        'best': 'أنسب لأولويته', 'over': 'بديل · فوق الميزانية بـ300K',
        'ai_label': 'Brokers AI', 'ai': 'مشروع ب أقل مقدم داخل الميزانية: 1.2M، أقل من أ بـ200K.',
        'pdf_t': 'عرض مشروع ب', 'pdf_s': 'باسمك ورقمك · جاهز للإرسال',
        'down': 'مقدم',
        'mini': 'السعر {price} · مقدم {down} · استلام {hand}',
        # record
        'rec_title': 'مشروع ب', 'rec_sub': 'التجمع · سكني',
        'fields': [('price', 'السعر', '8.0M'), ('down-payment', 'المقدم', '1.2M'), ('payment-period', 'خطة السداد', '7 سنين'),
                   ('delivery', 'الاستلام', '2027'), ('area', 'المساحة', '158 م²'), ('finishing', 'التشطيب', 'كامل')],
        'docs': [('details', 'البروشور'), ('location', 'الماستر بلان'), ('update', 'آخر تحديث')],
        # ask
        'msg_from': 'رسالة العميل',
        'msg': 'عايز شقة 3 غرف في التجمع لحد 8 مليون، والأهم المقدم يكون أقل حاجة، مش أكتر من مليون ونص.',
        'parsed': 'الشروط اللي اتفهمت',
        'crit': [('المنطقة', 'التجمع', ''), ('الغرف', '3', ''), ('السعر', 'حتى 8M', ''), ('المقدم', 'حتى 1.5M', ''),
                 ('الأولوية', 'أقل مقدم', 'prio'), ('الاستلام', 'مش محدد', 'open')],
        'ask': 'سؤال ناقص: «الاستلام فارق مع العميل؟»',
        # find
        'res_n': '3 نتايج', 'res_s': '2 مطابقين · 1 بديل',
        'res': [('B', 'مقدم 1.2M · 7 سنين · 2027', 'أنسب لأولويته', 'best'),
                ('A', 'مقدم 1.4M · 8 سنين · 2028', 'مطابق', 'plain'),
                ('C', 'مقدم 1.5M · 6 سنين · فوري', 'بديل · +300K', 'over')],
        # send
        'file_t': 'عرض مشروع ب', 'file_s': 'باسم: أحمد خالد · مستشار عقاري',
        'draft': 'أهلًا، ده عرض مشروع ب في التجمع: مقدم 1.2M وسداد على 7 سنين واستلام 2027. ولو تحب نقارنه بمشروع أ، أبعتلك الفرق.',
        'sent': 'جاهز للإرسال على WhatsApp',
        # chat
        'chat_t': 'Brokers AI', 'chat_s': 'جوّه Estavo Market',
        'me1': 'عايز 3 bedrooms في التجمع، budget لحد 8M والمقدم أقل حاجة.',
        'ai1': [('لقيت 2 مطابقين وبديل. الأنسب لأولويته ', 400), ('مشروع ب', 600), (': مقدم 1.2M، أقل من أ بـ200K.', 400)],
        'rows': [('ب', 'مقدم 1.2M · 7 سنين · 2027'), ('أ', 'مقدم 1.4M · 8 سنين · 2028')],
        'me2': 'والاستلام؟ العميل عايز قبل 2028.',
        'ai2': 'استلام ب في 2027، وأ في 2028. ومشروع ج جاهز بس فوق الميزانية بـ300K.',
        'acts': ['جهّز عرض PDF', 'اكتب رد للعميل'],
        'input': 'اسأل عن مشروع أو قارن...',
        # pdf
        'broker': 'أحمد خالد', 'role': 'مستشار عقاري', 'contact': 'واتساب · اتصال',
        'doc_k': 'عرض وحدة · التجمع', 'doc_t': 'مشروع ب · شقة 3 غرف',
        'doc_f': [('السعر', '8.0M'), ('المقدم', '1.2M'), ('السداد', '7 سنين'), ('الاستلام', '2027'), ('المساحة', '158 م²'), ('التشطيب', 'كامل')],
        'doc_foot': 'ملخص من Estavo Market · للمراجعة', 'callout': 'اسمك ورقمك',
        'wa_t': 'عرض مشروع ب', 'wa_s': 'PDF · صفحتين', 'wa_m': 'اتبعت',
        'rooms': ['نوم', 'نوم', 'رئيسية', 'معيشة', 'مطبخ'],
        # change
        'ch_t': 'تحديث · مشروع ب', 'ch_f': 'خطة السداد', 'before': 'قبل', 'after': 'بعد',
        'old': '8 سنين', 'new': '7 سنين', 'state': 'اتراجع واتنشر',
    },
    'en': {
        'brand': 'Estavo Market', 'example': 'Example',
        'city': 'New Cairo', 'start_from': 'Starting from', 'unit_chip': '3-bed apartment',
        'f_delivery': 'Delivery', 'f_area': 'Unit area', 'f_down': 'Down payment', 'f_inst': 'Installments',
        'inst': 'Up to {n} years', 'inst_short': '7 years', 'area_v': '{n} m²', 'period': 'Period',
        'best_short': 'Best fit', 'alt_short': 'Alternative · +300K', 'match': 'Match', 'over_note': 'Over budget',
        'ranked': 'ranked by lowest down payment', 'units_from': 'Units start from',
        'pills': ['New Cairo', 'Residential'], 'phase': 'Phase 1 · Handover 2027', 'available': 'Available',
        'nav': ['Gallery', 'Payment plans', 'Unit models', 'Location', 'Downloads'], 'plan_tag': 'Payment plan',
        'chat_title': 'ESTAVO ASSISTANT', 'chat_sub': 'Your smart assistant', 'free_pill': 'Free',
        'ask_chip': 'Ask the client: does handover timing matter?',
        'ud_title': 'Unit Details', 'ud_head': ('Specification', 'Details'),
        'ud_rows': [('Unit type', '3-bed apartment'), ('Price', '8.0M'), ('Area', '158 m²'), ('Bedrooms', '3'),
                    ('Finishing', 'Full'), ('Project', 'Project B'), ('Delivery', '2027')],
        'search': '3-bed in New Cairo up to 8M, lowest down payment',
        'search_m': '3-bed, New Cairo, lowest down payment',
        'chips': ['New Cairo', '3 bedrooms', 'Up to 8M', 'Down up to 1.5M'], 'prio': 'Priority: lowest down payment',
        'cols': ['Project', 'Price', 'Down', 'Plan', 'Handover'],
        'units': {
            'B': ('B', 'Project B', '158 m² · Fully finished', '8.0M', '1.2M', '7 yrs', '2027'),
            'A': ('A', 'Project A', '165 m² · Semi-finished', '7.9M', '1.4M', '8 yrs', '2028'),
            'C': ('C', 'Project C', '180 m² · Fully finished', '8.3M', '1.5M', '6 yrs', 'Ready'),
        },
        'best': 'Best fit for their priority', 'over': 'Alternative · 300K over budget',
        'ai_label': 'Brokers AI', 'ai': 'Project B has the lowest down payment within budget: 1.2M, 200K less than A.',
        'pdf_t': 'Project B offer', 'pdf_s': 'Your name and number · Ready to send',
        'down': 'down',
        'mini': '{price} · {down} down · {hand}',
        'rec_title': 'Project B', 'rec_sub': 'New Cairo · Residential',
        'fields': [('price', 'Price', '8.0M'), ('down-payment', 'Down payment', '1.2M'), ('payment-period', 'Payment plan', '7 years'),
                   ('delivery', 'Handover', '2027'), ('area', 'Area', '158 m²'), ('finishing', 'Finishing', 'Full')],
        'docs': [('details', 'Brochure'), ('location', 'Master plan'), ('update', 'Last update')],
        'msg_from': 'Client message',
        'msg': 'I want a 3-bedroom apartment in New Cairo, up to 8 million. The most important thing is the lowest down payment, no more than 1.5 million.',
        'parsed': 'Criteria understood',
        'crit': [('Area', 'New Cairo', ''), ('Bedrooms', '3', ''), ('Price', 'Up to 8M', ''), ('Down payment', 'Up to 1.5M', ''),
                 ('Priority', 'Lowest down', 'prio'), ('Handover', 'Not stated', 'open')],
        'ask': 'Missing question: "Does handover timing matter?"',
        'res_n': '3 results', 'res_s': '2 matches · 1 alternative',
        'res': [('B', '1.2M down · 7 yrs · 2027', 'Best fit', 'best'),
                ('A', '1.4M down · 8 yrs · 2028', 'Match', 'plain'),
                ('C', '1.5M down · 6 yrs · Ready', 'Alternative · +300K', 'over')],
        'file_t': 'Project B offer', 'file_s': 'By: Ahmed Khaled · Property consultant',
        'draft': "Hi, here's the Project B offer in New Cairo: 1.2M down, a 7-year plan and 2027 handover. If you'd like it compared with Project A, I'll send you the difference.",
        'sent': 'Ready to send on WhatsApp',
        'chat_t': 'Brokers AI', 'chat_s': 'inside Estavo Market',
        'me1': '3 bedrooms in New Cairo, budget up to 8M, lowest down payment possible.',
        'ai1': [('I found 2 matches and an alternative. The best fit for their priority is ', 400), ('Project B', 600), (': 1.2M down, 200K less than A.', 400)],
        'rows': [('B', '1.2M down · 7 yrs · 2027'), ('A', '1.4M down · 8 yrs · 2028')],
        'me2': 'And handover? The client wants it before 2028.',
        'ai2': 'B hands over in 2027 and A in 2028. C is ready, but 300K over budget.',
        'acts': ['Prepare a PDF offer', 'Draft a client reply'],
        'input': 'Ask about a project or compare...',
        'broker': 'Ahmed Khaled', 'role': 'Property consultant', 'contact': 'WhatsApp · Call',
        'doc_k': 'Unit offer · New Cairo', 'doc_t': 'Project B · 3-bedroom apartment',
        'doc_f': [('Price', '8.0M'), ('Down payment', '1.2M'), ('Plan', '7 years'), ('Handover', '2027'), ('Area', '158 m²'), ('Finishing', 'Full')],
        'doc_foot': 'Estavo Market summary · for review', 'callout': 'Your name and number',
        'wa_t': 'Project B offer', 'wa_s': 'PDF · 2 pages', 'wa_m': 'Sent',
        'rooms': ['Bed', 'Bed', 'Master', 'Living', 'Kitchen'],
        'ch_t': 'Update · Project B', 'ch_f': 'Payment plan', 'before': 'Before', 'after': 'After',
        'old': '8 years', 'new': '7 years', 'state': 'Reviewed and published',
    },
}


# ── Shared drawings ──────────────────────────────────────────────────
GREEN = '#7fa68c'
GREEN_D = '#5f8a70'


PHOTOS = {}


def photo_uri(key):
    if key not in PHOTOS:
        data = (ROOT / f'tools/data/market-photos/{key}.webp').read_bytes()
        PHOTOS[key] = 'data:image/webp;base64,' + base64.b64encode(data).decode()
    return PHOTOS[key]


PHOTO_FOR = {0: 'project-b', 1: 'project-a', 2: 'project-c'}


def photo(a, x, y, w, h, variant=0, r=0, rtop_only=True, key=None, sweep=0):
    """Embedded property photo (see tools/data/market-photos/provenance.json), clipped like the app's cards."""
    key = key or PHOTO_FOR[variant % 3]
    uid = f'{a.uid}p{len(a.defs)}'
    gx = a.px(x, w)
    if r:
        shape = (f'<path d="M{gx} {y + h}V{y + r}a{r} {r} 0 0 1 {r} -{r}h{w - 2 * r}a{r} {r} 0 0 1 {r} {r}V{y + h}z"/>' if rtop_only
                 else f'<rect x="{gx}" y="{y}" width="{w}" height="{h}" rx="{r}"/>')
        a.defs.append(f'<clipPath id="c{uid}">{shape}</clipPath>')
        a.add(f'<g clip-path="url(#c{uid})">')
    a.add(f'<image href="{photo_uri(key)}" x="{gx}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>')
    # soft bottom shade so pills and badges stay legible, like the app's image overlay
    a.defs.append(f'<linearGradient id="sh{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#021d39" stop-opacity=".28"/><stop offset=".35" stop-color="#021d39" stop-opacity="0"/></linearGradient>')
    a.add(f'<rect x="{gx}" y="{y}" width="{w}" height="{h}" fill="url(#sh{uid})"/>')
    if sweep and a.anim:
        a.defs.append(f'<linearGradient id="swg{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                      f'<stop offset=".5" stop-color="#fff" stop-opacity=".42"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
        a.add(f'<rect class="sw" x="{gx - w * .55}" y="{y - h * .2}" width="{w * .42}" height="{h * 1.4}" fill="url(#swg{uid})" '
              f'style="--sw:{w * 1.9:.0f}px;animation-delay:{sweep}ms"/>')
    if r:
        a.add('</g>')


def scene(a, x, y, w, h, variant=0, r=0, rtop_only=True):
    """Vector property 'photo': sky, buildings, trees. Drawn unmirrored inside a logical box."""
    uid = f'{a.uid}s{len(a.defs)}'
    gx = a.px(x, w)
    a.defs.append(
        f'<linearGradient id="sky{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#cfdeee"/><stop offset=".75" stop-color="#eef4fa"/></linearGradient>'
        f'<linearGradient id="gl{uid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#9dbad6"/><stop offset="1" stop-color="#6f93b7"/></linearGradient>')
    if r:
        rr = f'M{gx} {y + h}V{y + r}a{r} {r} 0 0 1 {r} -{r}h{w - 2 * r}a{r} {r} 0 0 1 {r} {r}V{y + h}z' if rtop_only else None
        clip = f'<clipPath id="c{uid}">' + (f'<path d="{rr}"/>' if rtop_only else f'<rect x="{gx}" y="{y}" width="{w}" height="{h}" rx="{r}"/>') + '</clipPath>'
        a.defs.append(clip)
        a.add(f'<g clip-path="url(#c{uid})">')
    a.add(f'<rect x="{gx}" y="{y}" width="{w}" height="{h}" fill="url(#sky{uid})"/>')
    k = w / 300
    g = f'<g transform="translate({gx} {y}) scale({k} {h / 170})">'
    g += '<circle cx="232" cy="38" r="22" fill="#ffffff" opacity=".55"/>'
    # far skyline
    g += '<path d="M0 118h22v-26h14v-14h18v40h12v-30h20v30h16v-48h22v48h18v-22h20v22h22v-36h18v36h26v-18h22v18h30v52H0z" fill="#bdd0e2"/>'
    if variant == 0:  # residential mid-rise with balconies (Project B)
        g += '<rect x="78" y="44" width="122" height="104" fill="#ffffff"/><rect x="200" y="58" width="36" height="90" fill="#dfe8f1"/>'
        g += '<rect x="74" y="38" width="130" height="8" rx="2" fill="#e8eef5"/>'
        for row in range(5):
            yy = 54 + row * 18
            g += f'<rect x="86" y="{yy}" width="106" height="10" rx="1.5" fill="url(#gl{uid})"/>'
            g += f'<rect x="84" y="{yy + 11}" width="110" height="3" rx="1" fill="#d4dfeb"/>'
            g += f'<rect x="206" y="{yy + 6}" width="24" height="8" rx="1" fill="#a9c1d9"/>'
        g += '<rect x="122" y="128" width="34" height="20" fill="#7d9ab4"/>'
    elif variant == 1:  # twin glass towers (Project A)
        for bx, bh in [(84, 112), (150, 96)]:
            g += f'<rect x="{bx}" y="{150 - bh}" width="56" height="{bh}" fill="url(#gl{uid})"/>'
            g += f'<rect x="{bx + 56}" y="{150 - bh + 8}" width="12" height="{bh - 8}" fill="#5b7fa3"/>'
            for row in range(int(bh / 12)):
                g += f'<rect x="{bx + 4}" y="{150 - bh + 6 + row * 12}" width="48" height="1.6" fill="#ffffff" opacity=".55"/>'
    else:  # low-rise townhouses (Project C, ready)
        for i, bx in enumerate([60, 128, 196]):
            g += f'<rect x="{bx}" y="96" width="60" height="52" fill="#f3ede3"/>'
            g += f'<path d="M{bx - 4} 98 {bx + 30} 74 {bx + 64} 98z" fill="#c9a886"/>'
            g += f'<rect x="{bx + 8}" y="108" width="16" height="14" rx="1" fill="url(#gl{uid})"/><rect x="{bx + 36}" y="108" width="16" height="14" rx="1" fill="url(#gl{uid})"/>'
            g += f'<rect x="{bx + 24}" y="128" width="12" height="20" fill="#8a6f55"/>'
    # ground, path, trees
    g += '<rect x="0" y="148" width="300" height="22" fill="#e3ebf2"/><path d="M0 156h300" stroke="#ffffff" stroke-width="2" opacity=".8"/>'
    for tx, s in [(30, 1), (58, .8), (252, 1.05), (276, .75)]:
        g += f'<rect x="{tx - 1.5}" y="{150 - 10 * s}" width="3" height="{12 * s}" fill="#7d6a58"/>'
        g += f'<circle cx="{tx}" cy="{150 - 18 * s}" r="{12 * s}" fill="{GREEN}"/><circle cx="{tx + 5 * s}" cy="{150 - 22 * s}" r="{7 * s}" fill="{GREEN_D}" opacity=".55"/>'
    g += '</g>'
    a.add(g)
    if r:
        a.add('</g>')


def mark(a, x, y, size=20, color=BLUE):
    s = size / 20
    a.add(f'<g transform="translate({a.px(x, size)} {y}) scale({s})" fill="none" stroke="{color}" stroke-width="2.4">'
          f'<circle cx="7" cy="10" r="5.2"/><circle cx="13" cy="10" r="5.2"/></g>')


def blueprint(a, x, y, w, h, r):
    cid = f'cp-{a.uid}'
    a.defs.append(f'<clipPath id="{cid}"><rect x="{a.px(x, w)}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>')
    a.rect(x, y, w, h, r=r, fill=NAVY)
    a.add(f'<g clip-path="url(#{cid})" fill="none">')
    for gx in range(int(x) + 20, int(x + w), 44):
        a.line(gx, y, gx, y + h, '#ffffff', 1, opacity=.05)
    for gy in range(int(y) + 20, int(y + h), 44):
        a.line(x, gy, x + w, gy, '#ffffff', 1, opacity=.05)
    a.add(f'<path d="M{a.px(x + w * .15)} {y + h} C {a.px(x + w * .35)} {y + h * .55}, {a.px(x + w * .55)} {y + h * .5}, {a.px(x + w)} {y + h * .22}" stroke="#fff" stroke-width="7" opacity=".06"/>')
    a.add(f'<path d="M{a.px(x + w * .62)} {y} C {a.px(x + w * .6)} {y + h * .4}, {a.px(x + w * .8)} {y + h * .7}, {a.px(x + w * .74)} {y + h}" stroke="#fff" stroke-width="4" opacity=".05"/>')
    a.add('</g>')
    for i, (fx, fy) in enumerate([(.86, .25), (.92, .6), (.78, .9)]):
        a.circle(x + w * fx, y + h * fy, 9, fill='#ffffff', opacity=.07)
        a.circle(x + w * fx, y + h * fy, 3.2, fill='#ffffff', opacity=.35)
        a.fx(f'<circle class="ring" cx="{a.px(x + w * fx)}" cy="{y + h * fy}" r="9" fill="none" stroke="{ELEC}" stroke-width="1.5" style="animation-delay:{900 + i * 700}ms;animation-duration:3.2s"/>')
    if a.anim:
        # data pulses running along the street grid
        a.add(f'<g clip-path="url(#{cid})">')
        lanes = [(x + 20 + 44 * k, y, 0, h) for k in (2, 5, 8)] + [(x, y + 20 + 44 * k, w, 0) for k in (3, 7, 10)]
        for i, (lx, ly, dx, dy) in enumerate(lanes):
            if (dx and ly > y + h) or (dy and lx > x + w):
                continue
            sdx = -dx if a.rtl else dx
            a.add(f'<circle class="pk" cx="{a.px(lx)}" cy="{ly}" r="2.6" fill="{ELEC}" '
                  f'style="--dx:{sdx:.0f}px;--dy:{dy:.0f}px;animation-delay:{600 + i * 830}ms;animation-duration:{4.6 + (i % 3) * 1.1:.1f}s"/>')
        a.add('</g>')


def badge(a, x_end, y, label, size=12, fill=BLUE, color=WHITE, stroke=None, h=24):
    w = tw(label, size, 600) + 22
    a.rect(x_end - w, y, w, h, r=h / 2, fill=fill, stroke=stroke)
    a.text(x_end - w / 2, y + h / 2 + size * .36, label, size, color, 600, anchor='middle')
    return w


def tag(a, x_end, y, c):
    return badge(a, x_end, y, c['example'], 12, WHITE, T3, stroke=LINE, h=24)


def city_pill(a, x, y, label, size=11.5):
    w = tw(label, size, 600) + 34
    a.rect(x, y, w, 24, r=12, fill=NAVY, opacity=.88)
    a.icon('location', x + 9, y + 5, 14, WHITE)
    a.text(x + 26, y + 16.5, label, size, WHITE, 600)
    return w


def unit_vals(c, key):
    mono, name, sub, price, down, plan, hand = c['units'][key]
    years = {'B': 7, 'A': 8, 'C': 6}[key]
    area = {'B': '158', 'A': '165', 'C': '180'}[key]
    return dict(mono=mono, name=name, price=price, down=down, hand=hand,
                inst=c['inst'].format(n=years), area=c['area_v'].format(n=area))


def project_card(a, x, y, w, c, key, variant, state='', img_h=None, compact=False):
    """The app's ProjectCard: 4:3-ish image, city pill, name, starting price, unit chip, 2x2 facts."""
    v = unit_vals(c, key)
    img_h = img_h or round(w * 0.56)
    body = 16 if not compact else 14
    facts_h = 2 * 46
    h = img_h + body + 22 + 8 + 18 + 30 + 14 + 30 + 14 + facts_h + body
    if state == 'best':
        a.rect(x - 5, y - 5, w + 10, h + 10, r=24, fill='none', stroke=BLUE, sw=5, opacity=.12)
        a.ring(x - 3, y - 3, w + 6, h + 6, 23, 1500)
    a.rect(x, y, w, h, r=20, fill=WHITE, stroke=BLUE if state == 'best' else LINE, sw=1.5 if state == 'best' else 1, filt='ss')
    photo(a, x + 1, y + 1, w - 2, img_h, variant, r=19, sweep=(1700 if state == 'best' else 0))
    city_pill(a, x + 12, y + 12, c['city'])
    if state == 'best':
        badge(a, x + w - 12, y + 12, c['best_short'], 11.5, BLUE, WHITE, h=24)
    elif state == 'over':
        badge(a, x + w - 12, y + 12, c['alt_short'], 11.5, WHITE, WARN, WARNLN, h=24)
    yy = y + img_h + body + 18
    a.text(x + body, yy, v['name'], 17 if not compact else 16, INK, 600)
    yy += 26
    a.text(x + body, yy, c['start_from'], 11.5, T3)
    yy += 28
    a.text(x + body, yy, v['price'], 23 if not compact else 21, BLUE, 600)
    if state == 'over':
        a.text(x + body + tw(v['price'], 23, 600) + 10, yy, c['over_note'], 11.5, WARN, 600)
    yy += 14
    a.pill(x + body, yy, c['unit_chip'], 11.5, SOFT, '#d7e2ee', BLUE, 600, h=26, pad=10)
    yy += 26 + 14
    a.line(x + body, yy, x + w - body, yy)
    yy += 12
    colw = (w - 2 * body) / 2
    facts = [('delivery', c['f_delivery'], v['hand']), ('area', c['f_area'], v['area']),
             ('down-payment', c['f_down'], v['down']), ('instalment', c['f_inst'], v['inst'])]
    for i, (ic, lab, val) in enumerate(facts):
        r_, k = divmod(i, 2)
        fx = x + body + k * colw
        fy = yy + r_ * 46
        a.icon(ic, fx, fy + 2, 15, MID)
        a.text(fx + 21, fy + 13, lab, 10.5, T3)
        key_hit = (state == 'best' and ic == 'down-payment')
        a.text(fx + 21, fy + 32, val, 13.5, BLUE if key_hit else (WARN if state == 'over' and ic == 'delivery' else INK), 600)
    return h


# ── Hero: the app's search results ───────────────────────────────────
def hero(lang, animated):
    c = C[lang]
    W, cw = 720, 676
    cardw = (cw - 24 * 2 - 18) / 2
    probe = Art(W, 10, lang, 'probe')
    card_h = project_card(probe, 0, 0, cardw, c, 'B', 0, 'best')
    top = 24
    body_top = top + 64
    cards_y = body_top + 16 + 34 + 18 + 26
    frame_h = cards_y - top + card_h + 26
    ai_lines = wrap([(c['ai'], 400)], 13.5, 300)
    ai_h = 52 + len(ai_lines) * 21 + 18 + 10 + 30 + 16
    ai_y = top + frame_h - 26
    H = round(ai_y + ai_h + 8)
    a = Art(W, H, lang, f'h{lang}')
    blueprint(a, 88, 96, W - 88, H - 96, 30)

    def grp(cls, delay):
        a.seq(cls, delay)

    grp('r', 60)
    a.rect(0, top, cw, frame_h, r=24, fill=MIST, stroke=LINE, filt='sh')
    a.rect(1, top + 1, cw - 2, 63, r=23, fill=WHITE)
    a.rect(1, top + 40, cw - 2, 24, fill=WHITE)
    a.line(1, top + 64, cw - 1, top + 64)
    mark(a, 22, top + 22, 22)
    a.text(52, top + 38, c['brand'], 15, BLUE, 600)
    sx = 200
    a.rect(sx, top + 13, cw - sx - 70, 38, r=19, fill=MIST, stroke=LINE)
    a.icon('request', sx + 14, top + 23, 18, MID)
    stw = tw(c['search'], 13.5, 500)
    a.type_open(sx + 38, top + 20, stw + 6, 24, 420, 1100)
    a.text(sx + 40, top + 37, c['search'], 13.5, INK, 500)
    a.close()
    a.caret(sx + 43 + stw, top + 23, 18, 1550)
    a.circle(cw - 38, top + 32, 19, fill=SOFT)
    a.icon('control', cw - 47, top + 23, 18, BLUE)
    a.close()

    x = 24
    for i, chip in enumerate(c['chips'] + [c['prio']]):
        last = i == len(c['chips'])
        grp('p', 300 + 50 * i)
        w = a.pill(x, body_top + 16, chip, 12.5, BLUE if last else WHITE, BLUE if last else LINE, WHITE if last else T2, 500 if not last else 600, h=32, pad=13)
        a.close()
        x += w + 8
    grp('r', 520)
    a.text(24, body_top + 16 + 34 + 26, [(c['res_n'], 600), ('  ·  ' + c['ranked'], 400)], 13, T2)
    a.close()

    grp('r', 640)
    project_card(a, 24, cards_y, cardw, c, 'B', 0, 'best')
    a.close()
    grp('r', 760)
    project_card(a, 24 + cardw + 18, cards_y, cardw, c, 'A', 1, '')
    a.close()

    # Brokers AI bubble floating out of the frame, linked to the card it recommends
    aw = 360
    ax = W - aw - 6
    if a.anim:
        bx = 24 + cardw * .62
        d = (f'M{a.px(ax)} {ai_y + 30} C {a.px(ax - 70)} {ai_y + 30}, {a.px(bx)} {ai_y + 56}, {a.px(bx)} {ai_y + 2}')
        a.seq('f', 1350)
        a.add(f'<path d="{d}" fill="none" stroke="{ELEC}" stroke-width="2" stroke-linecap="round" stroke-dasharray="5 7" class="fl"/>')
        a.add(f'<circle cx="{a.px(bx)}" cy="{ai_y + 2}" r="4" fill="{ELEC}"/>')
        a.add(f'<circle class="ring" cx="{a.px(bx)}" cy="{ai_y + 2}" r="8" fill="none" stroke="{ELEC}" stroke-width="1.5" style="animation-delay:1600ms;animation-duration:2.2s"/>')
        a.close()
    grp('r', 1100)
    a.rect(ax, ai_y, aw, ai_h, r=20, fill=WHITE, stroke=LINE, filt='sh')
    a.fx(f'<circle class="gl" cx="{a.px(ax + 30)}" cy="{ai_y + 28}" r="22" fill="{ELEC}"/>')
    a.circle(ax + 30, ai_y + 28, 15, fill=BLUE)
    a.spark(ax + 30, ai_y + 28, 16)
    a.text(ax + 54, ai_y + 33, c['ai_label'], 14, INK, 600)
    a.rect(ax + 16, ai_y + 52, aw - 32, len(ai_lines) * 21 + 18, r=14, fill=SOFT, stroke='#dbe5ef')
    for i, ln in enumerate(ai_lines):
        a.text(ax + 30, ai_y + 76 + i * 21, ln, 13.5, BLUE)
    cy = ai_y + 52 + len(ai_lines) * 21 + 18 + 10
    a.rect(ax + 16, cy, tw(c['acts'][0], 12, 600) + 52, 30, r=15, fill=BLUE)
    a.icon('pdf', ax + 26, cy + 7, 16, WHITE)
    a.text(ax + 48, cy + 20, c['acts'][0], 12, WHITE, 600)
    a.close()
    return a


def hero_mobile(lang, animated):
    c = C[lang]
    W, cw = 360, 344
    probe = Art(W, 10, lang, 'probe')
    card_h = project_card(probe, 0, 0, cw - 28, c, 'B', 0, 'best', compact=True)
    chips = c['chips'][2:] + [c['prio']]
    x, rows = 14, 1
    for chip in chips:
        w = tw(chip, 12, 500) + 22
        if x + w > 330:
            x, rows = 14, rows + 1
        x += w + 7
    cards_y = 60 + 12 + rows * 36 + 10
    a_row_y = cards_y + card_h + 14
    frame_h = a_row_y + 76 + 14
    ai_lines = wrap([(c['ai'], 400)], 12.5, 250)
    ai_h = 46 + len(ai_lines) * 19 + 16
    ai_y = frame_h - 10
    H = round(ai_y + ai_h + 6)
    a = Art(W, H, lang, f'hm{lang}')
    blueprint(a, 24, 70, W - 24, H - 70, 24)

    def grp(cls, delay):
        a.seq(cls, delay)

    grp('r', 60)
    a.rect(0, 0, cw, frame_h, r=20, fill=MIST, stroke=LINE, filt='sh')
    a.rect(1, 1, cw - 2, 59, r=19, fill=WHITE)
    a.rect(1, 36, cw - 2, 24, fill=WHITE)
    a.line(1, 60, cw - 1, 60)
    a.rect(14, 12, cw - 28, 36, r=18, fill=MIST, stroke=LINE)
    a.icon('request', 26, 21, 17, MID)
    mtw = tw(c['search_m'], 12.5, 500)
    a.type_open(48, 20, mtw + 6, 22, 380, 950)
    a.text(50, 35, c['search_m'], 12.5, INK, 500)
    a.close()
    a.caret(53 + mtw, 22, 17, 1350)
    a.close()
    x, y = 14, 72
    for i, chip in enumerate(chips):
        last = chip == c['prio']
        w = tw(chip, 12, 500) + 22
        if x + w > 330:
            x, y = 14, y + 36
        grp('p', 280 + 60 * i)
        a.pill(x, y, chip, 12, BLUE if last else WHITE, BLUE if last else LINE, WHITE if last else T2, 500, h=28, pad=11)
        a.close()
        x += w + 7
    grp('r', 560)
    project_card(a, 14, cards_y, cw - 28, c, 'B', 0, 'best', compact=True)
    a.close()
    grp('r', 700)
    v = unit_vals(c, 'A')
    a.rect(14, a_row_y, cw - 28, 76, r=16, fill=WHITE, stroke=LINE)
    photo(a, 24, a_row_y + 10, 76, 56, 1, r=10, rtop_only=False)
    a.text(112, a_row_y + 30, v['name'], 14.5, INK, 600)
    a.text(112, a_row_y + 54, [(v['price'], 600), ('  ·  ' + c['f_down'] + ' ' + v['down'], 400)], 12.5, T2)
    a.close()
    grp('r', 1000)
    aw = 300
    ax = W - aw - 4
    a.rect(ax, ai_y, aw, ai_h, r=18, fill=WHITE, stroke=LINE, filt='sh')
    a.fx(f'<circle class="gl" cx="{a.px(ax + 26)}" cy="{ai_y + 24}" r="19" fill="{ELEC}"/>')
    a.circle(ax + 26, ai_y + 24, 13, fill=BLUE)
    a.spark(ax + 26, ai_y + 24, 14)
    a.text(ax + 46, ai_y + 29, c['ai_label'], 13, INK, 600)
    for i, ln in enumerate(ai_lines):
        a.text(ax + 18, ai_y + 58 + i * 19, ln, 12.5, BLUE)
    a.close()
    return a


# ── Record: the app's project page ───────────────────────────────────
def record(lang, compact):
    c = C[lang]
    W = 360 if compact else 560
    pad = 18 if compact else 24
    band_h = 176 if compact else 168
    stat_cols = 2
    statw = ((W - 2 * pad - 24) - 10) / stat_cols
    price_card_h = 70 + 2 * 66 + 10 + 16
    pc_y = band_h - 44
    nav_y = pc_y + price_card_h + 18
    plan_y = nav_y + 38 + 16
    H = plan_y + 116 + pad
    a = Art(W, H, lang, f'rec{lang}{int(compact)}')
    a.defs.append(f'<clipPath id="pb-{a.uid}"><rect x="0" y="0" width="{W}" height="{H}" rx="22"/></clipPath>')
    a.rect(0, 0, W, H, r=22, fill=MIST, stroke=LINE)
    a.add(f'<g clip-path="url(#pb-{a.uid})">')
    a.seq('f', 40)
    a.rect(0, 0, W, band_h, fill=NAVY)
    a.add(f'<rect x="0" y="0" width="{W}" height="{band_h}" fill="url(#wd-{a.uid})"/>')
    if a.anim:
        a.defs.append(f'<linearGradient id="bs-{a.uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ELEC}" stop-opacity="0"/><stop offset=".5" stop-color="{ELEC}" stop-opacity=".22"/><stop offset="1" stop-color="{ELEC}" stop-opacity="0"/></linearGradient>')
        a.add(f'<rect class="sw" x="{-W * .5}" y="0" width="{W * .4}" height="{band_h}" fill="url(#bs-{a.uid})" style="--sw:{W * 1.6:.0f}px;animation-delay:1200ms;animation-duration:9s"/>')
    a.close()
    a.add('</g>')
    a.defs.append(f'<pattern id="wd-{a.uid}" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#fff" opacity=".08"/></pattern>')
    x = pad
    for i, p_ in enumerate(c['pills']):
        w = tw(p_, 11.5, 600) + 24 + (16 if i == 0 else 0)
        a.seq('p', 220 + i * 90)
        a.rect(x, pad, w, 26, r=13, fill=WHITE, opacity=.12)
        if i == 0:
            a.icon('location', x + 9, pad + 6, 14, WHITE)
        a.text(x + (27 if i == 0 else 12), pad + 17.5, p_, 11.5, WHITE, 600)
        a.close()
        x += w + 8
    tag(a, W - pad, pad + 1, c)
    a.seq('r', 380)
    a.text(pad, pad + 66, c['rec_title'], 26 if not compact else 23, WHITE, 600)
    a.text(pad, pad + 92, c['phase'], 12.5, ONDARK)
    a.close()
    # price card
    pcx, pcw = pad, W - 2 * pad
    a.seq('r', 600)
    a.rect(pcx, pc_y, pcw, price_card_h, r=18, fill=WHITE, filt='sh')
    a.text(pcx + 18, pc_y + 28, c['start_from'], 11.5, T3, 500)
    a.text(pcx + 18, pc_y + 58, '8.0M', 26, BLUE, 600)
    st_badge = c['available']
    bw_ = badge(a, pcx + pcw - 16, pc_y + 16, st_badge, 11, '#e7f4ec', '#1f7a45', h=24)
    a.fx(f'<circle class="ring" cx="{a.px(pcx + pcw - 16 - bw_ - 10)}" cy="{pc_y + 28}" r="5" fill="none" stroke="#22c55e" stroke-width="1.6" style="animation-delay:1300ms;animation-duration:2s"/>')
    a.fx(f'<circle cx="{a.px(pcx + pcw - 16 - bw_ - 10)}" cy="{pc_y + 28}" r="3" fill="#22c55e"/>')
    a.close()
    stats = [('delivery', c['f_delivery'], '2027'), ('area', c['f_area'], c['area_v'].format(n='158')),
             ('down-payment', c['f_down'], '1.2M'), ('instalment', c['f_inst'], c['inst'].format(n=7))]
    for i, (ic, lab, val) in enumerate(stats):
        r_, k = divmod(i, 2)
        sx = pcx + 12 + k * (statw + 10)
        sy = pc_y + 74 + r_ * 66
        a.seq('r', 780 + i * 90)
        a.rect(sx, sy, statw, 58, r=12, fill=MIST)
        a.rect(sx + 10, sy + 13, 32, 32, r=9, fill=SOFT)
        a.icon(ic, sx + 18, sy + 21, 16, BLUE)
        a.text(sx + 52, sy + 24, lab, 11, T3)
        a.text(sx + 52, sy + 44, val, 14.5, INK, 600)
        a.close()
    # section nav
    x = pad
    for i, lab in enumerate(c['nav'][:4 if compact else 5]):
        w = tw(lab, 12, 600) + 24
        if x + w > W - pad:
            break
        on = i == 1
        a.seq('p', 1150 + i * 70)
        a.rect(x, nav_y, w, 32, r=9, fill=BLUE if on else WHITE, stroke=None if on else LINE)
        a.text(x + w / 2, nav_y + 20.5, lab, 12, WHITE if on else T2, 600, anchor='middle')
        a.close()
        x += w + 6
    # payment plan card
    a.ring(pad - 2, plan_y - 2, W - 2 * pad + 4, 120, 20, 2000)
    a.seq('r', 1450)
    a.rect(pad, plan_y, W - 2 * pad, 116, r=18, fill=WHITE, stroke=BLUE, sw=1.4)
    tw_t = tw(c['plan_tag'], 10.5, 600) + 16
    a.rect(pad + 16, plan_y + 14, tw_t, 22, r=6, fill=SOFT)
    a.text(pad + 16 + tw_t / 2, plan_y + 29, c['plan_tag'], 10.5, BLUE, 600, anchor='middle')
    half = (W - 2 * pad) / 2
    a.text(pad + 18, plan_y + 76, '1.2M', 28, BLUE, 600)
    a.text(pad + 18, plan_y + 99, c['f_down'], 12, T3)
    a.line(pad + half, plan_y + 50, pad + half, plan_y + 102)
    a.text(pad + half + 18, plan_y + 76, c['inst_short'], 28, BLUE, 600)
    a.text(pad + half + 18, plan_y + 99, c['period'], 12, T3)
    a.close()
    return a


# ── Workflow steps ───────────────────────────────────────────────────
def canvas(a, h):
    a.rect(0, 0, a.W, h, r=18, fill=SOFT)
    a.add(f'<rect x="0" y="0" width="{a.W}" height="{h}" rx="18" fill="url(#dots-{a.uid})"/>')


def step_ask(lang, compact):
    c = C[lang]
    W = 360 if compact else 560
    p = 16 if compact else 26
    size = 14 if compact else 15
    bw = W * (0.84 if compact else 0.74)
    msg_lines = wrap([(c['msg'], 400)], size, bw - 36)
    msg_h = 44 + len(msg_lines) * size * 1.62
    # criteria chips layout (logical rows)
    cw = W - 2 * p
    chips = [(ic, f'{dt}: {dd}', kind) for (dt, dd, kind), ic in zip(c['crit'], ['location', 'unit', 'price', 'down-payment', 'analysis', 'delivery'])]
    rows, x, row = [], 16, []
    for ic, lab, kind in chips:
        w = tw(lab, 12.5, 600) + 46
        if row and x + w > cw - 16:
            rows.append(row); row, x = [], 16
        row.append((ic, lab, kind, x, w)); x += w + 8
    rows.append(row)
    card_y = p + msg_h + 16
    card_h = 54 + len(rows) * 42 + 16
    q_y = card_y + card_h + 14
    H = round(q_y + 38 + p)
    a = Art(W, H, lang, f'ask{lang}{int(compact)}')
    canvas(a, H)
    a.seq('r', 80)
    a.rect(p, p, bw, msg_h, r=18, fill=WHITE, filt='ss')
    a.rect(p, p + msg_h - 16, 16, 16, fill=WHITE)
    a.icon('message', p + 16, p + 13, 15, '#1f9d55')
    a.text(p + 38, p + 25, c['msg_from'], 12, T3, 600)
    for i, ln in enumerate(msg_lines):
        a.text(p + 18, p + 52 + i * size * 1.62, ln, size, INK)
    a.close()
    if a.anim:  # reading scan over the client's words
        cid = a.nid('k')
        a.defs.append(f'<clipPath id="{cid}"><rect x="{a.px(p, bw)}" y="{p}" width="{bw}" height="{msg_h}" rx="18"/></clipPath>'
                      f'<linearGradient id="g{cid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ELEC}" stop-opacity="0"/>'
                      f'<stop offset=".7" stop-color="{ELEC}" stop-opacity=".18"/><stop offset="1" stop-color="{ELEC}" stop-opacity=".55"/></linearGradient>')
        a.add(f'<g clip-path="url(#{cid})"><rect class="sc" x="{a.px(p, bw)}" y="{p - 26}" width="{bw}" height="28" fill="url(#g{cid})" '
              f'style="--sd:{msg_h + 20:.0f}px;animation-delay:500ms;animation-duration:3.8s"/></g>')
    # assistant bubble (app style)
    a.seq('r', 850)
    a.rect(p, card_y, cw, card_h, r=18, fill='#edf3f9', stroke='#d9e4ef')
    a.circle(p + 30, card_y + 27, 13, fill=BLUE)
    a.spark(p + 30, card_y + 27, 14)
    a.text(p + 52, card_y + 32, c['parsed'], 14.5, BLUE, 600)
    a.close()
    k_ = 0
    for r_, row in enumerate(rows):
        for ic, lab, kind, x, w in row:
            y = card_y + 50 + r_ * 42
            a.seq('p', 1150 + k_ * 150)
            k_ += 1
            if kind == 'prio':
                a.ring(p + x - 2, y - 2, w + 4, 38, 19, 2300)
                a.rect(p + x, y, w, 34, r=17, fill=BLUE)
                col = WHITE
            elif kind == 'open':
                a.rect(p + x, y, w, 34, r=17, fill='none', stroke=MUTE, dash='4 3')
                a.fx(f'<rect class="fl" x="{a.px(p + x, w)}" y="{y}" width="{w}" height="34" rx="17" fill="none" stroke="{ELEC}" stroke-width="1.4" stroke-dasharray="4 8"/>')
                col = MID
            else:
                a.rect(p + x, y, w, 34, r=17, fill=WHITE, stroke='#d6e1ec')
                col = BLUE
            a.icon(ic, p + x + 12, y + 9, 16, col)
            a.text(p + x + 34, y + 22, lab, 12.5, col, 600)
            a.close()
    # suggestion chip (app ActionChips)
    qw = min(cw, tw(c['ask_chip'], 12.5, 600) + 48)
    a.seq('r', 1150 + k_ * 150 + 250)
    a.rect(p, q_y, qw, 38, r=19, fill=WHITE, stroke='#d6e1ec', filt='ss')
    a.icon('message', p + 14, q_y + 11, 16, BLUE)
    a.text(p + 38, q_y + 24, c['ask_chip'], 12.5, BLUE, 600)
    a.close()
    return a


def mini_card(a, x, y, w, c, key, variant, state):
    v = unit_vals(c, key)
    img_h = round(w * 0.56)
    h = img_h + 14 + 22 + 18 + 26 + 12 + 2 * 44 + 10
    if state == 'best':
        a.rect(x - 4, y - 4, w + 8, h + 8, r=20, fill='none', stroke=BLUE, sw=5, opacity=.12)
        a.ring(x - 2, y - 2, w + 4, h + 4, 18, 1400)
    a.rect(x, y, w, h, r=16, fill=WHITE, stroke=BLUE if state == 'best' else (WARNLN if state == 'over' else LINE), sw=1.5 if state == 'best' else 1, dash='5 4' if state == 'over' else None)
    photo(a, x + 1, y + 1, w - 2, img_h, variant, r=15, sweep=(1600 if state == 'best' else 0))
    city_pill(a, x + 9, y + 9, c['city'], 10.5)
    yy = y + img_h + 24
    a.text(x + 12, yy, v['name'], 14.5, INK, 600)
    yy += 22
    a.text(x + 12, yy, c['units_from'], 10.5, T3)
    yy += 24
    a.text(x + 12, yy, v['price'], 18, BLUE if state != 'over' else WARN, 600)
    yy += 12
    for i, (lab, val) in enumerate([(c['f_down'], v['down']), (c['f_inst'], v['inst'])]):
        fy = yy + i * 44
        a.rect(x + 10, fy, w - 20, 38, r=9, fill=SOFT)
        a.text(x + 20, fy + 15, lab, 9.5, MID, 500)
        a.text(x + 20, fy + 31, val, 12.5, BLUE if (state == 'best' and i == 0) else INK, 600)
    lab = {'best': c['best_short'], 'plain': c['match'], 'over': c['alt_short']}[state]
    fill, color, stroke = {'best': (BLUE, WHITE, None), 'plain': (WHITE, T2, LINE), 'over': (WHITE, WARN, WARNLN)}[state]
    badge(a, x + w - 8, y + img_h - 32, lab, 10.5, fill, color, stroke, h=22)
    return h


def step_find(lang, compact):
    c = C[lang]
    W = 360 if compact else 560
    p = 16 if compact else 22
    items = [('B', 0, 'best'), ('A', 1, 'plain'), ('C', 2, 'over')]
    if compact:
        rh = 92
        H = p + 36 + 3 * (rh + 12) + p - 12
        a = Art(W, H, lang, f'find{lang}1')
        canvas(a, H)
        a.seq('f', 60)
        a.text(p + 4, p + 22, [(c['res_n'], 600), ('  ·  ' + c['res_s'], 400)], 14, INK)
        a.close()
        y = p + 38
        for i_, (key, var, st) in enumerate(items):
            v = unit_vals(c, key)
            a.seq('r', 300 + i_ * 170)
            if st == 'best':
                a.rect(p - 4, y - 4, W - 2 * p + 8, rh + 8, r=20, fill='none', stroke=BLUE, sw=5, opacity=.12)
                a.ring(p - 2, y - 2, W - 2 * p + 4, rh + 4, 18, 1300)
            a.rect(p, y, W - 2 * p, rh, r=16, fill=WARNBG if st == 'over' else WHITE, stroke=BLUE if st == 'best' else (WARNLN if st == 'over' else LINE), sw=1.5 if st == 'best' else 1, dash='5 4' if st == 'over' else None)
            photo(a, p + 10, y + 10, 96, rh - 20, var, r=10, rtop_only=False, sweep=(1500 if st == 'best' else 0))
            a.text(p + 118, y + 30, v['name'], 14.5, INK, 600)
            a.text(p + 118, y + 54, [(v['price'], 600)], 15, WARN if st == 'over' else BLUE)
            a.text(p + 118, y + 76, c['f_down'] + ' ' + v['down'] + ' · ' + v['inst'], 11.5, T3)
            lab = {'best': c['best_short'], 'plain': c['match'], 'over': c['alt_short']}[st]
            fill, color, stroke = {'best': (BLUE, WHITE, None), 'plain': (MIST, T2, None), 'over': (WHITE, WARN, WARNLN)}[st]
            badge(a, W - p - 10, y + 10, lab, 10.5, fill, color, stroke, h=22)
            a.close()
            y += rh + 12
        return a
    cw = (W - 2 * p - 2 * 12) / 3
    probe = Art(W, 10, lang, 'probe')
    ch = mini_card(probe, 0, 0, cw, c, 'B', 0, 'best')
    H = round(p + 40 + ch + p + 4)
    a = Art(W, H, lang, f'find{lang}0')
    canvas(a, H)
    a.seq('f', 60)
    a.text(p + 4, p + 22, [(c['res_n'], 600), ('  ·  ' + c['res_s'], 400)], 15, INK)
    a.close()
    for i, (key, var, st) in enumerate(items):
        a.seq('r', 300 + i * 170)
        mini_card(a, p + i * (cw + 12), p + 40, cw, c, key, var, st)
        a.close()
    return a


def pdf_page_thumb(a, x, y, w, h):
    a.rect(x, y, w, h, r=4, fill=WHITE)
    a.rect(x, y, w, h * .2, r=4, fill=BLUE)
    for i in range(4):
        a.rect(x + 4, y + h * .3 + i * h * .16, w - 8, h * .1, fill=SOFT if i % 2 == 0 else '#e1e9f1')


def step_send(lang, compact):
    c = C[lang]
    W = 360 if compact else 560
    p = 16 if compact else 26
    size = 13.5 if compact else 14.5
    fw = min(W - 2 * p, max(tw(c['file_s'], 12), tw(c['file_t'], 15, 600)) + 110)
    dw = W * (0.86 if compact else 0.74)
    d_lines = wrap([(c['draft'], 400)], size, dw - 36)
    d_h = 30 + len(d_lines) * size * 1.62
    H = round(p + 90 + 14 + d_h + 40 + p)
    a = Art(W, H, lang, f'send{lang}{int(compact)}')
    canvas(a, H)
    fx = W - p - fw
    a.seq('r', 100)
    a.rect(fx, p, fw, 90, r=16, fill=BLUE, filt='ss')
    pdf_page_thumb(a, fx + 14, p + 14, 48, 62)
    a.text(fx + 76, p + 36, c['file_t'], 15, WHITE, 600)
    a.text(fx + 76, p + 58, c['file_s'], 12, ONDARK)
    a.text(fx + 76, p + 76, 'PDF', 10.5, ONDARK, 600)
    a.close()
    dy = p + 104
    dx = W - p - dw
    a.seq('r', 650)
    a.rect(dx, dy, dw, d_h, r=18, fill=WHITE, stroke=LINE)
    a.rect(dx + dw - 16, dy + d_h - 16, 16, 16, fill=WHITE)
    a.line(dx + dw, dy + d_h - 16, dx + dw, dy + d_h, LINE)
    a.line(dx + dw - 16, dy + d_h, dx + dw, dy + d_h, LINE)
    a.close()
    for i, ln in enumerate(d_lines):
        lw = runs_width(ln, size)
        a.type_open(dx + 16, dy + 12 + i * size * 1.62, lw + 6, size * 1.62, 900 + i * 520, 520)
        a.text(dx + 18, dy + 28 + i * size * 1.62, ln, size, INK)
        a.close()
    sy = dy + d_h + 26
    a.seq('p', 900 + len(d_lines) * 520 + 200)
    a.ticks(W - p - 15, sy - 10, '#1f9d55')
    a.text(W - p - 22, sy, c['sent'], 12.5, T3, 500, anchor='end')
    a.close()
    return a


# ── Brokers AI: the app's chat window ────────────────────────────────
def chat(lang, compact):
    c = C[lang]
    W = 360 if compact else 540
    p = 16 if compact else 22
    size = 13.5 if compact else 14.5
    bmax = W * 0.8
    lh = size * 1.6
    cardw = (W - 2 * p - 12) / 2 if not compact else W * 0.66
    probe = Art(W, 10, lang, 'probe')
    mch = mini_card(probe, 0, 0, cardw, c, 'B', 0, 'best')

    blocks = []

    def me(text):
        ls = wrap([(text, 600)], size, bmax - 32)
        w = min(bmax, max(runs_width(l, size) for l in ls) + 34)
        blocks.append(('me', ls, w, 24 + len(ls) * lh))

    def ai(runs, extra=None):
        ls = wrap(runs, size, bmax - 32)
        blocks.append(('ai', ls, min(bmax, max(runs_width(l, size) for l in ls) + 34), 24 + len(ls) * lh, extra))

    me(c['me1'])
    ai(c['ai1'])
    blocks.append(('cards', None, W, mch + (22 if compact else 0)))
    if not compact:  # phones keep one exchange so the scene stays scannable
        me(c['me2'])
        ai([(c['ai2'], 400)])
    blocks.append(('chips', None, W, 40))
    head = 64
    body_h = sum(b[3] for b in blocks) + 12 * (len(blocks) - 1) + 2 * p
    H = round(head + body_h + 60 + p)
    a = Art(W, H, lang, f'chat{lang}{int(compact)}')
    a.rect(0, 0, W, H, r=28, fill='#fbfcfe', stroke='#dbe4ee')
    a.seq('f', 40)
    a.text(W / 2, 28, c['chat_title'], 13, BLUE, 600, anchor='middle')
    a.text(W / 2, 46, c['chat_sub'], 10.5, T3, anchor='middle')
    for k, ic in enumerate(['details', 'close']):
        cx = W - p - 20 - k * 48
        a.circle(cx, 32, 20, fill=WHITE, stroke='#dbe4ee')
        a.icon('update' if k == 0 else 'outside', cx - 9, 23, 18, BLUE)
    cr = tw(c['free_pill'], 10.5, 600) + 22
    a.rect(p, 20, cr, 24, r=12, fill=WHITE, stroke='#d6e1ec')
    a.text(p + cr / 2, 36, c['free_pill'], 10.5, BLUE, 600, anchor='middle')
    a.line(0, head, W, head, '#e3eaf2')
    a.close()
    y = head + p
    clock = 250
    for b in blocks:
        kind = b[0]
        if kind == 'ai':
            a.dots(p, y, clock, 900)
            clock += 850
        a.seq('p' if kind == 'chips' else 'r', clock)
        clock += {'me': 650, 'ai': 400, 'cards': 600, 'chips': 300}[kind]
        if kind == 'me':
            _, ls, w, h = b
            x = W - p - w
            a.rect(x, y, w, h, r=18, fill=BLUE)
            a.rect(x + w - 14, y + h - 14, 14, 14, fill=BLUE)
            for i, ln in enumerate(ls):
                a.text(x + 17, y + 27 + i * lh, ln, size, WHITE)
        elif kind == 'ai':
            _, ls, w, h, _e = b
            a.rect(p, y, w, h, r=18, fill='#edf3f9', stroke='#d9e4ef')
            a.rect(p + 1, y + h - 15, 14, 14, fill='#edf3f9')
            for i, ln in enumerate(ls):
                a.text(p + 17, y + 27 + i * lh, ln, size, BLUE)
        elif kind == 'cards':
            h = b[3]
            if compact:
                mini_card(a, p, y, cardw, c, 'B', 0, 'best')
                mini_card(a, p + cardw + 12, y, cardw, c, 'A', 1, 'plain')
                for k in range(3):
                    a.rect(W / 2 - 18 + k * 12 + (0 if k == 0 else 8), y + mch + 12, 16 if k == 0 else 6, 6, r=3, fill=BLUE if k == 0 else LINE)
            else:
                mini_card(a, p, y, cardw, c, 'B', 0, 'best')
                mini_card(a, p + cardw + 12, y, cardw, c, 'A', 1, 'plain')
        elif kind == 'chips':
            h = b[3]
            x = p
            for ic, act in zip(['pdf', 'message'], c['acts']):
                aw = tw(act, 12, 600) + 46
                a.rect(x, y, aw, 38, r=19, fill=WHITE, stroke='#d6e1ec')
                a.icon(ic, x + 13, y + 11, 16, BLUE)
                a.text(x + 35, y + 24, act, 12, BLUE, 600)
                x += aw + 8
        a.close()
        y += b[3] + 12
    iy = H - p - 58
    a.rect(p, iy, W - 2 * p, 58, r=20, fill=WHITE, stroke='#d6e1ec')
    a.text(p + 18, iy + 34, c['input'], 12.5, T3)
    a.caret(p + 14, iy + 20, 18, clock + 200)
    a.rect(W - p - 52, iy + 7, 44, 44, r=12, fill=BLUE)
    sx = a.px(W - p - 52, 44)
    a.add(f'<path d="M{sx + 14} {iy + 29}l17-8-6 17-3-6z" fill="#fff" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/>')
    return a


# ── Branded PDF: the real Unit Details page ──────────────────────────
def pdf(lang, compact):
    c = C[lang]
    W = 360 if compact else 540
    dw = 300 if compact else 372
    row_h = 30 if compact else 34
    rows = c['ud_rows']
    dh = 64 + 22 + 34 + len(rows) * row_h + 22 + 64 + 18
    top = 64
    H = top + dh + (128 if compact else 88)
    a = Art(W, H, lang, f'pdf{lang}{int(compact)}')
    a.rect(0, 110, W, H - 170, r=28, fill=WASH)
    dx = (W - dw) / 2
    cxp = a.px(dx + dw / 2)
    # back page: cover with property render
    rot_b = -6 if a.rtl else 5
    a.seq('f', 60)
    a.add(f'<g transform="rotate({rot_b} {cxp} {top + dh / 2}) translate({30 if a.rtl else -30} 10)">')
    a.rect(dx + 14, top + 16, dw - 28, dh - 32, r=6, fill=WHITE, filt='ss')
    photo(a, dx + 14, top + 16, dw - 28, (dh - 32) * .62, 0, r=6)
    a.rect(dx + 14, top + 16 + (dh - 32) * .62, dw - 28, 52, fill=BLUE)
    a.text(dx + 30, top + 16 + (dh - 32) * .62 + 32, c['rec_title'], 16, WHITE, 600)
    a.close()
    a.close()
    # front page: Unit Details
    a.seq('r', 260)
    a.add(f'<g transform="rotate(-1.2 {cxp} {top + dh / 2})">')
    a.rect(dx, top, dw, dh, r=6, fill=WHITE, filt='sh')
    a.defs.append(f'<clipPath id="dc-{a.uid}"><rect x="{a.px(dx, dw)}" y="{top}" width="{dw}" height="{dh}" rx="6"/></clipPath>')
    a.add(f'<g clip-path="url(#dc-{a.uid})">')
    a.rect(dx, top, dw, 64, fill=BLUE)
    a.close()
    a.text(dx + dw / 2, top + 40, c['ud_title'], 19, WHITE, 600, anchor='middle')
    ty = top + 64 + 22
    tx, tw_ = dx + 18, dw - 36
    half = tw_ * .48
    a.seq('f', 600)
    a.rect(tx, ty, tw_, 34, fill=BLUE)
    a.text(tx + 12, ty + 22, c['ud_head'][0], 12, WHITE, 600)
    a.text(tx + half + 12, ty + 22, c['ud_head'][1], 12, WHITE, 600)
    a.close()
    for i, (k, v) in enumerate(rows):
        ry = ty + 34 + i * row_h
        a.seq('f', 720 + i * 130)
        a.rect(tx, ry, tw_, row_h, fill='#f4f6f9' if i % 2 == 0 else WHITE)
        a.text(tx + 12, ry + row_h / 2 + 4.5, k, 12, T2)
        hi = i == 1
        a.text(tx + half + 12, ry + row_h / 2 + 4.5, v, 12.5 if hi else 12, BLUE if hi else INK, 600)
        a.close()
    a.line(tx + half, ty + 34, tx + half, ty + 34 + len(rows) * row_h, '#dde1ea')
    if a.anim:  # generation scan running down the table
        gid = a.nid('g')
        a.defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ELEC}" stop-opacity="0"/>'
                      f'<stop offset=".8" stop-color="{ELEC}" stop-opacity=".16"/><stop offset="1" stop-color="{ELEC}" stop-opacity=".7"/></linearGradient>')
        a.add(f'<rect class="sc" x="{a.px(tx, tw_)}" y="{ty + 34 - 22}" width="{tw_}" height="24" fill="url(#{gid})" '
              f'style="--sd:{len(rows) * row_h:.0f}px;animation-delay:{720}ms;animation-duration:4.4s"/>')
    # broker strip (closing details on the offer)
    by = ty + 34 + len(rows) * row_h + 22
    t_strip = 720 + len(rows) * 130 + 120
    a.seq('p', t_strip)
    a.rect(tx, by, tw_, 64, r=10, fill=SOFT)
    photo(a, tx + 12, by + 14, 36, 36, r=18, rtop_only=False, key='agent-omar')
    a.text(tx + 58, by + 28, c['broker'], 14, INK, 600)
    a.text(tx + 58, by + 47, c['role'], 11, T3)
    a.circle(tx + tw_ - 26, by + 32, 15, fill='#25d366')
    a.icon('message', tx + tw_ - 34, by + 24, 16, WHITE)
    a.close()
    a.close()
    a.close()
    # callout pointing at the broker strip
    cl_w = tw(c['callout'], 13, 600) + 28
    clx = W - cl_w - (6 if compact else 18)
    a.seq('p', t_strip + 300)
    if compact:
        # below the broker strip, pointing up, so it never covers table values
        cly = by + 58
        a.line(clx + cl_w / 2, cly, clx + cl_w / 2, cly + 26, BLUE, 1.5)
        a.circle(clx + cl_w / 2, cly, 3.5, fill=WHITE, stroke=BLUE, sw=1.5)
        a.rect(clx, cly + 26, cl_w, 32, r=16, fill=WHITE, stroke=BLUE, sw=1.5, filt='ss')
        a.text(clx + cl_w / 2, cly + 47, c['callout'], 13, BLUE, 600, anchor='middle')
    else:
        cly = by + 6
        a.rect(clx, cly - 52, cl_w, 32, r=16, fill=WHITE, stroke=BLUE, sw=1.5, filt='ss')
        a.text(clx + cl_w / 2, cly - 31, c['callout'], 13, BLUE, 600, anchor='middle')
        a.line(clx + cl_w / 2, cly - 20, clx + cl_w / 2, cly + 4, BLUE, 1.5)
        a.circle(clx + cl_w / 2, cly + 6, 3.5, fill=WHITE, stroke=BLUE, sw=1.5)
    a.close()
    # WhatsApp file bubble
    a.seq('r', t_strip + 600)
    ww = max(tw(c['wa_t'], 13.5, 600), tw(c['wa_s'], 11.5)) + 90
    wx = 6 if compact else 20
    wy = H - 96
    a.rect(wx, wy, ww, 82, r=14, fill='#e7fbe9', filt='sh')
    a.rect(wx + 10, wy + 10, ww - 20, 48, r=10, fill=WHITE)
    pdf_page_thumb(a, wx + 18, wy + 15, 28, 38)
    a.text(wx + 58, wy + 32, c['wa_t'], 13.5, INK, 600)
    a.text(wx + 58, wy + 50, c['wa_s'], 11.5, T3)
    a.ticks(wx + ww - 27, wy + 63, '#1f9d55')
    a.text(wx + ww - 32, wy + 73, c['wa_m'], 11, T3, anchor='end')
    a.close()
    return a


# ── Update record ────────────────────────────────────────────────────
def change(lang, compact):
    c = C[lang]
    W = 360
    p = 22
    H = 236
    a = Art(W, H, lang, f'chg{lang}{int(compact)}')
    a.rect(0, 0, W, H, r=20, fill=WHITE, stroke=LINE)
    a.seq('f', 40)
    a.icon('update', p, p + 2, 18, BLUE)
    a.text(p + 26, p + 16, c['ch_t'], 15, BLUE, 600)
    tag(a, W - p, p - 2, c)
    a.text(p, p + 52, c['ch_f'], 13, T3)
    a.close()
    bw = (W - 2 * p - 44) / 2
    by = p + 68
    a.seq('r', 250)
    a.rect(p, by, bw, 72, r=12, fill=MIST)
    a.text(p + 14, by + 24, c['before'], 12, T3, 500)
    a.text(p + 14, by + 52, c['old'], 19, T3, 600)
    ow = tw(c['old'], 19, 600)
    a.line(p + 12, by + 46, p + 16 + ow, by + 46, T3, 1.6)
    a.close()
    a.seq('p', 650)
    a.arrow(p + bw + 10, by + 24, 24, ELEC if a.anim else MUTE)
    a.close()
    nx = p + bw + 44
    a.ring(nx - 2, by - 2, bw + 4, 76, 14, 1500)
    a.seq('p', 950)
    a.rect(nx, by, bw, 72, r=12, fill=BLUE)
    a.text(nx + 14, by + 24, c['after'], 12, ONDARK, 500)
    a.text(nx + 14, by + 52, c['new'], 19, WHITE, 600)
    a.close()
    a.seq('f', 1300)
    a.icon('check', p, H - p - 16, 16, BLUE)
    a.text(p + 24, H - p - 3, c['state'], 13, T2, 500)
    a.close()
    return a


TITLES = {
    'hero': {'ar': 'مثال توضيحي: طلب عميل ونتايج مرتبة حسب أولويته في Estavo Market',
             'en': 'Example: a client request and results ranked by its priority in Estavo Market'},
    'record': {'ar': 'مثال توضيحي: بيانات مشروع في Estavo Market', 'en': 'Example: project data in Estavo Market'},
    'step-ask': {'ar': 'مثال توضيحي: رسالة عميل والشروط اللي اتفهمت منها', 'en': 'Example: a client message and the criteria understood'},
    'step-find': {'ar': 'مثال توضيحي: نتيجتين مطابقتين وبديل', 'en': 'Example: two matches and one alternative'},
    'step-send': {'ar': 'مثال توضيحي: عرض PDF ورد جاهز للعميل', 'en': 'Example: a PDF offer and a ready client reply'},
    'chat': {'ar': 'مثال توضيحي: محادثة مع Brokers AI', 'en': 'Example: a conversation with Brokers AI'},
    'pdf': {'ar': 'مثال توضيحي: عرض PDF عليه اسم البروكر', 'en': 'Example: a PDF offer carrying the broker\'s name'},
    'change': {'ar': 'مثال توضيحي: تحديث خطة سداد', 'en': 'Example: a payment-plan update'},
}


def main():
    global ANIM
    OUT.mkdir(parents=True, exist_ok=True)
    written = []

    def build(name, fn, args, title):
        """Animated file plus its '-still' companion (no-JS, reduced motion, print)."""
        global ANIM
        for animated, suffix in ((True, ''), (False, '-still')):
            ANIM = animated
            art = fn(*args)
            path = OUT / f'{name}{suffix}.svg'
            path.write_text(art.svg(title))
            written.append((path.name, art.W, art.H, path.stat().st_size))
        ANIM = False

    for lang in ('ar', 'en'):
        build(f'hero-{lang}', hero, (lang, True), TITLES['hero'][lang])
        build(f'hero-mobile-{lang}', hero_mobile, (lang, True), TITLES['hero'][lang])
        for key, fn in [('record', record), ('step-ask', step_ask), ('step-find', step_find),
                        ('step-send', step_send), ('chat', chat), ('pdf', pdf)]:
            build(f'{key}-{lang}', fn, (lang, False), TITLES[key][lang])
            build(f'{key}-mobile-{lang}', fn, (lang, True), TITLES[key][lang])
        build(f'change-{lang}', change, (lang, False), TITLES['change'][lang])

    for name, w, h, size in written:
        print(f'  {name:36} {w}x{h}  {size / 1024:.1f} KB')
    print(f'\n{len(written)} SVG(s) written to {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
