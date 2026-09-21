#!/usr/bin/env python3
"""Install the six mobile compositions in the Arabic homepage, preserving surrounding copy."""
from pathlib import Path
import re
import importlib.util

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('art', ROOT / 'tools/build-illustrations.py')
art = importlib.util.module_from_spec(spec)
spec.loader.exec_module(art)

def plan(projected=False):
    if projected:
        return '<img class="es-art-unit-plan es-art-unit-plan--projected" src="assets/img/estavo-unit-scene.svg" width="460" height="285" alt="" loading="lazy" decoding="async" />'
    return '<svg class="es-art-unit-plan" viewBox="0 0 252 180" aria-hidden="true">'+art.plan(16,13,1)+'</svg>'

def architecture():
    return '<div class="es-art-listing-rows">'+''.join('<div class="es-art-listing-row">'+plan()+'<span><b>شقة · ٣ غرف</b><small>التجمع الخامس</small></span><span><small>خطة السداد</small><b>'+duration+'</b></span></div>' for duration in ['٦ سنوات','٥ سنوات'])+'</div>'

def icon(name):
    return f'<img class="es-art-icon" src="assets/img/icons/estavo-{name}.svg" width="160" height="160" alt="" loading="lazy" decoding="async" />'

def waterfall():
    s='<svg class="es-art-waterfall-v2" viewBox="0 0 280 184" aria-hidden="true"><defs><linearGradient id="es-mwf-growth" x2="0" y2="1"><stop stop-color="#244b65"/><stop offset="1" stop-color="#0b2239"/></linearGradient><linearGradient id="es-mwf-net" x2="0" y2="1"><stop stop-color="#a4ecd3"/><stop offset="1" stop-color="#72c9b2"/></linearGradient></defs><path d="M12 32H268M12 76H268M12 120H268M12 164H268" class="structure"/>'
    for i,(x,y,h) in enumerate([(20,32,132),(84,32,45),(148,77,40),(212,117,47)]):
        cls='es-vector-bar es-vector-bar--deduction' if i in [1,2] else 'es-vector-bar'
        front=['url(#es-mwf-growth)','#a9c6e2','#a9c6e2','url(#es-mwf-net)'][i]
        top=['#47749a','#d5e5f0','#d5e5f0','#bbf1df'][i]
        side=['#102b40','#769bb7','#769bb7','#58af95'][i]
        s+=f'<g class="{cls}" style="animation-delay:{i*.18}s"><rect x="{x}" y="{y}" width="44" height="{h}" rx="1" fill="{front}"/><path d="M{x} {y}L{x+5} {y-4}H{x+49}L{x+44} {y}Z" fill="{top}"/><path d="M{x+44} {y}L{x+49} {y-4}V{y+h-4}L{x+44} {y+h}Z" fill="{side}"/></g>'
    return s+'<path d="M69 28H89M133 73H153M197 113H217" class="subject" stroke-dasharray="3 4"/></svg>'

COMPOSITIONS = {
 'es-signals-figure': '''<div class="es-art-mobile es-art-v2 es-art-v2--signals">
 <p class="es-art-example">مثال · تفاعلات على موقعك</p>
 <div class="es-art-events"><span>'''+icon('building')+'''<b>مشاهدة</b>مشروع في التجمع</span><span>'''+icon('map')+'''<b>بحث</b>شقة · ٣ غرف</span><span>'''+icon('chart')+'''<b>مقارنة</b>خطط السداد</span></div>
 <svg class="es-art-event-routes" viewBox="0 0 260 30" aria-hidden="true"><path d="M43 0V12H130V30M130 0V30M217 0V12H130"/><path d="M43 0V12H130V30M217 0V12H130V30" class="es-vector-packet" pathLength="100"/></svg>
 <div class="es-art-segment"><span class="es-art-segment__tag">التجمع الخامس · شقق</span><div>'''+icon('layers')+'''<b>اهتمامات</b><span>من موقعك</span></div></div>
 <p class="es-art-meta-output"><bdi>Meta</bdi><span>شرائح لاستخدامها في التسويق</span></p></div>''',
 'es-client-figure': '''<div class="es-art-mobile es-art-v2 es-art-v2--client">
 <p class="es-art-example">مثال · قبل المكالمة</p><div class="es-art-client-visual"><span class="es-art-client-avatar">'''+icon('chat')+'''<svg viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="36" fill="none" stroke="#a9c6e2" stroke-opacity=".2"/><circle cx="40" cy="40" r="36" class="es-vector-packet" pathLength="100"/></svg></span><p class="es-art-title">ابدأ من طلبه</p></div>
 <div class="es-art-brief"><div><span>المنطقة</span><b>التجمع الخامس</b></div><div><span>نوع الوحدة</span><b>شقة · ٣ غرف</b></div><div><span>السداد اللي قارن بينه</span><b>٦ سنوات</b></div><div><span>الميزانية</span><b>حسب ما شاركه</b></div></div>
 <div class="es-art-evidence"><span><b>شاف مشاريع</b>في التجمع</span><span><b>قارن السداد</b>ورجع للتفاصيل</span><span><b>سأل المساعد</b>عن ٣ غرف</span></div><p class="es-art-v2-foot">بيانات التواصل، ومعاها سياق المكالمة</p></div>''',
 'es-conversation-figure': """<div class="es-art-mobile es-art-v2 es-art-v2--conversation es-art-v2--estavo-ai">
 <p class="es-art-example">مثال · محادثة على موقعك</p><blockquote>عايز شقة ٣ غرف في التجمع الخامس وأقارن السداد</blockquote>
 <div class="es-art-ai-intent"><div><small>المنطقة</small><b>التجمع الخامس</b></div><div><small>نوع الوحدة</small><b>شقة · ٣ غرف</b></div><div><small>خطة السداد</small><b>قارن الخطط</b></div></div>
 <img class="es-art-ai-scene" src="assets/img/estavo-ai-scene.svg" width="540" height="260" alt="" loading="lazy" decoding="async" />
 <div class="es-art-ai-results"><p>اختيارات من عقاراتك</p><div><b>شقة · ٣ غرف</b><span>٦ سنوات</span></div><div><b>شقة · ٣ غرف</b><span>٥ سنوات</span></div></div><p class="es-art-v2-foot">السعر والتوافر من بيانات المشروع وقت السؤال</p></div>""",
 'es-brand-unified-figure': '''<div class="es-art-mobile es-art-v2 es-art-v2--brand"><div class="es-art-brand-site">
 <div class="es-art-brand-rule"><b>عقاراتك</b><span>موقع باسمك</span></div><p class="es-art-title">بنفس هويتك.</p><p class="es-art-example">مثال · شقق في التجمع الخامس</p>'''+architecture()+'''
 <div class="es-art-brand-assistant"><b>مساعد باسمك</b><span>عارف تفاصيل عقاراتك</span></div></div><div class="es-art-brand-data"><bdi>Estavo Market</bdi><span>نفس البيانات للبحث والمقارنة</span></div></div>''',
 'es-roi-figure': '''<div class="es-art-mobile es-art-v2 es-art-v2--roi"><p class="es-art-example">مثال · بدون أسعار أو نسب متوقعة</p><p class="es-art-title">إيه اللي بيتبقى من النمو؟</p>
 '''+waterfall()+'''
 <div class="es-art-waterfall-key"><span>النمو</span><span>التكلفة</span><span>التضخم</span><span>العائد</span></div><p class="es-art-v2-foot">بعد التكلفة وأثر التضخم، حسب بيانات الوحدة</p></div>''',
 'es-reach-figure': '''<div class="es-art-mobile es-art-v2 es-art-v2--reach"><div class="es-art-listing-detail">'''+plan(True)+'''<div><p class="es-art-example">مثال · وحدتك على موقعك</p><b>التجمع الخامس</b><span>شقة · ٣ غرف</span></div></div>
 <p class="es-art-v2-foot">نفس البيانات والعمولة اللي إنت بتحددها</p><div class="es-art-reach-orbit"><svg viewBox="0 0 240 240" aria-hidden="true"><path d="M120 0V240M0 120H240" class="structure"/><path d="M120 120V0M120 120H240M120 120V240M120 120H0" class="es-vector-packet" pathLength="100"/></svg><div><bdi>Estavo<br/>Brokers</bdi></div>'''+''.join('<span class="es-art-orbit-node">'+icon('profile')+'</span>' for _ in range(4))+'''</div><p class="es-art-v2-foot">وحدتك قدام شبكة أوسع</p></div>'''
}

def replace_div(source, start, replacement):
    depth=0
    for match in re.finditer(r'<div\b[^>]*>|</div\s*>',source[start:]):
        depth += -1 if match.group().startswith('</') else 1
        if depth==0:
            return source[:start]+replacement+source[start+match.end():]
    raise ValueError('Unbalanced div')

html=(ROOT/'index.html').read_text()
for figure, composition in COMPOSITIONS.items():
    match=re.search(r'<div class="[^"]*\b'+figure+r'\b[^"]*"',html)
    if not match: raise ValueError('Missing figure '+figure)
    mobile=re.search(r'<div class="es-art-mobile\b',html[match.start():])
    html=replace_div(html, match.start()+mobile.start(), composition)

# Existing market mobile art keeps its composition, replacing decorative bars with legible values.
values={'المنطقة · نوع الوحدة':'التجمع الخامس · شقة','المنطقة · المطوّر':'التجمع الخامس','المشروع · المنطقة':'التجمع الخامس','نوع الوحدة · المساحة':'شقة · ٣ غرف','الوحدة':'شقة · ٣ غرف','المطوّر':'حسب المشروع','المشروع':'المشروع المختار','المنطقة':'التجمع الخامس','نوع الوحدة':'شقة · ٣ غرف','المساحة':'حسب الوحدة','التشطيب':'حسب الوحدة','خطة السداد':'٦ سنوات','السعر':'حسب الوحدة','المقدّم':'حسب خطة السداد','فترة التقسيط':'٦ سنوات'}
def field(match):
    body=match.group(0)
    label=re.search(r'<b>(.*?)</b>',body)
    if label and ('<i' in body or 'class="es-art-value"' in body):
        value=values.get(label.group(1),'حسب بيانات المشروع')
        body=re.sub(r'<i(?: class="[^"]*")?></i>', '',body)
        body=re.sub(r'<span class="es-art-value">.*?(?:</span>|$)', '',body)
        body=body.replace('</b>','</b><span class="es-art-value">'+value+'</span>',1)
    return body
html=re.sub(r'<span class="es-art-field">(?:<b>.*?</b>)(?:<span class="es-art-value">.*?</span>|<i[^>]*></i>)*</span>',field,html,flags=re.S)
# Source chips are documents, not loading screens.
html=re.sub(r'(<b>(?:WhatsApp|PDF|Web)</b>)<i></i><i class="is-short"></i>',r'\1',html)
html=html.replace('<b><bdi>WhatsApp</bdi></b><i></i><i class="is-short"></i>', '<b><bdi>WhatsApp</bdi></b><span class="es-art-source-label">محادثات</span>')
html=html.replace('<span>المنطقة · نوع الوحدة</span><i></i>', '<span>التجمع الخامس · شقة</span>')
head='<p class="es-art-head"><b><bdi>Estavo Market</bdi></b><span></span></p>'
html=html.replace(head,head.replace('<span></span>','<span>مثال · البحث والمقارنة</span>'))
# The stronger update composition keeps its geometry; its metadata is real-shaped text.
html=html.replace('class="es-updates-mobile__caption">تغييرات السوق','class="es-updates-mobile__caption">مثال · تغييرات السوق')
def update_fact(match):
    value=values.get(match.group(1),'حسب المشروع')
    if match.group(1)=='السعر': return match.group(0)
    return '<span class="es-update-fact"><b>'+match.group(1)+'</b><span class="es-art-value">'+value+'</span></span>'
html=re.sub(r'<span class="es-update-fact"><b>(.*?)</b><i[^>]*></i></span>',update_fact,html)
html=html.replace('السابق<i></i>', 'السابق<b>٥ سنوات</b>').replace('التحديث الحالي<i></i>','التحديث الحالي<b>٦ سنوات</b>')
html=html.replace('آخر تحديث <i></i>', 'آخر تحديث حسب مراجعة البيانات')
(ROOT/'index.html').write_text(html)
print('Installed six mobile compositions and replaced existing market field bars.')
