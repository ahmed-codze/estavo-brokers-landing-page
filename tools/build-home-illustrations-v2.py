#!/usr/bin/env python3
"""Build the eight non-hero homepage illustrations in the flat Estavo system."""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("estavo_builder", ROOT / "tools/build-illustrations.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

DEFS = r'''<defs>
<linearGradient id="route" x1="0" x2="1"><stop stop-color="#5c91c7" stop-opacity=".16"/><stop offset="1" stop-color="#5c91c7" stop-opacity=".72"/></linearGradient>
<linearGradient id="soft-sweep"><stop stop-color="white" stop-opacity="0"/><stop offset=".5" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
<mask id="sweep" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="640"><rect class="scene-sweep" x="-300" width="260" height="640" fill="url(#soft-sweep)"/></mask>
<style>
text{font-family:ArtPlex,Arial,sans-serif;fill:#0b2239;font-size:21px;font-weight:400}.display{font-size:28px;font-weight:500}.title{font-size:24px;font-weight:500}.label{font-size:21px;font-weight:500}.small{font-size:19px;fill:#47749a}.micro{font-size:17px;fill:#47749a}.white{fill:#f5f9fc}.muted{fill:#a9c6e2}.mini{fill:none;stroke:#28567f;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}.mini-light{stroke:#a9c6e2}.route{fill:none;stroke:url(#route);stroke-width:2;stroke-linecap:round}.energy{fill:none;stroke:#5c91c7;stroke-width:3;stroke-linecap:round}.float-a,.float-b,.float-c{transform-box:fill-box;transform-origin:center}.typing{opacity:.45}
@media(prefers-reduced-motion:no-preference){.scene-sweep{animation:sweep 11s cubic-bezier(.4,0,.2,1) infinite}.scene-float{animation:scene-float 13s ease-in-out infinite}.typing{animation:typing 1.4s ease-in-out infinite}}
@keyframes sweep{0%,12%{transform:translateX(0)}82%,100%{transform:translateX(1500px)}}@keyframes float-a{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}@keyframes float-b{0%,100%{transform:translateY(0)}50%{transform:translateY(6px)}}@keyframes float-c{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}@keyframes typing{0%,70%,100%{opacity:.3;transform:translateY(0)}35%{opacity:1;transform:translateY(-2px)}}
@keyframes scene-float{0%,100%{transform:translateY(3px)}50%{transform:translateY(-3px)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.energy{display:none}.typing{opacity:.55;transform:none}}
</style></defs>'''

def panel(x,y,w,h,dark=False,r=20):
    fill='#102b45' if dark else '#ffffff'; stroke='#274b68' if dark else '#dce7ef'
    return b.rect(x,y,w,h,fill,r,f'stroke="{stroke}" stroke-width="1.5"')

def divider(x1,y1,x2,y2,dark=False):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{"#a9c6e2" if dark else "#dce7ef"}" stroke-opacity="{.2 if dark else 1}"/>'

def route(d):
    return f'<path d="{d}" class="route"/><path d="{d}" class="energy" mask="url(#sweep)"/>'

def icon(x,y,name,size=24,light=False):
    shapes={
      'search':'<circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/>',
      'building':'<path d="M5 21V5h14v16M8 9h2M14 9h2M8 13h2M14 13h2M10 21v-4h4v4"/>',
      'file':'<path d="M6 3h8l4 4v14H6Z"/><path d="M14 3v5h5M9 12h6M9 16h6"/>',
      'web':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/>',
      'check':'<path d="m5 12 4 4L19 6"/>',
      'chat':'<path d="M4 4h16v12H9l-5 4Z"/><path d="M8 9h8M8 12h5"/>',
      'person':'<circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 4-7 8-7s7 2 8 7"/>',
      'eye':'<path d="M3 12s3-5 9-5 9 5 9 5-3 5-9 5-9-5-9-5Z"/><circle cx="12" cy="12" r="2"/>',
      'chart':'<path d="M4 20V4M4 20h16M7 16l4-5 3 2 5-7"/>',
      'link':'<path d="M9 15 7 17a4 4 0 0 1-6-6l3-3a4 4 0 0 1 6 0M15 9l2-2a4 4 0 0 1 6 6l-3 3a4 4 0 0 1-6 0M8 12h8"/>',
      'shield':'<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6Z"/><path d="m8 12 3 3 5-6"/>',
    }
    return f'<g transform="translate({x} {y}) scale({size/24})" class="mini{" mini-light" if light else ""}">{shapes[name]}</g>'

def meta_mark(x,y,width=64,color='#0866ff'):
    """The official Meta glyph, normalized from its 24px brand viewBox."""
    scale=width/24
    d='M6.915 4.03c-1.968 0-3.683 1.28-4.871 3.113C.704 9.208 0 11.883 0 14.449c0 .706.07 1.369.21 1.973a6.624 6.624 0 0 0 .265.86 5.297 5.297 0 0 0 .371.761c.696 1.159 1.818 1.927 3.593 1.927 1.497 0 2.633-.671 3.965-2.444.76-1.012 1.144-1.626 2.663-4.32l.756-1.339.186-.325c.061.1.121.196.183.3l2.152 3.595c.724 1.21 1.665 2.556 2.47 3.314 1.046.987 1.992 1.22 3.06 1.22 1.075 0 1.876-.355 2.455-.843a3.743 3.743 0 0 0 .81-.973c.542-.939.861-2.127.861-3.745 0-2.72-.681-5.357-2.084-7.45-1.282-1.912-2.957-2.93-4.716-2.93-1.047 0-2.088.467-3.053 1.308-.652.57-1.257 1.29-1.82 2.05-.69-.875-1.335-1.547-1.958-2.056-1.182-.966-2.315-1.303-3.454-1.303zm10.16 2.053c1.147 0 2.188.758 2.992 1.999 1.132 1.748 1.647 4.195 1.647 6.4 0 1.548-.368 2.9-1.839 2.9-.58 0-1.027-.23-1.664-1.004-.496-.601-1.343-1.878-2.832-4.358l-.617-1.028a44.908 44.908 0 0 0-1.255-1.98c.07-.109.141-.224.211-.327 1.12-1.667 2.118-2.602 3.358-2.602zm-10.201.553c1.265 0 2.058.791 2.675 1.446.307.327.737.871 1.234 1.579l-1.02 1.566c-.757 1.163-1.882 3.017-2.837 4.338-1.191 1.649-1.81 1.817-2.486 1.817-.524 0-1.038-.237-1.383-.794-.263-.426-.464-1.13-.464-2.046 0-2.221.63-4.535 1.66-6.088.454-.687.964-1.226 1.533-1.533a2.264 2.264 0 0 1 1.088-.285z'
    return f'<path d="{d}" transform="translate({x} {y}) scale({scale})" fill="{color}"/>'

def facebook_mark(x,y,width=32,color='#0866ff'):
    """The official Facebook glyph, normalized from its 24px brand viewBox."""
    scale=width/24
    d='M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z'
    return f'<path d="{d}" transform="translate({x} {y}) scale({scale})" fill="{color}"/>'

def stage_route(x1,x2,y):
    """A short directional connector between the three marketing stages."""
    return route(f'M{x1} {y}H{x2}')+f'<path d="M{x2+8} {y-6}L{x2} {y}l8 6" fill="none" stroke="#5c91c7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'

def chip(x,y,w,label,dark=False):
    return b.rect(x,y,w,32,'#173a55' if dark else '#f1f5f8',7)+b.text(x+w-12,y+22,label,'micro '+('muted' if dark else '' if False else ''))

def header(x,y,w,title,note='',dark=False):
    s=b.text(x+w-20,y+31,title,'label '+('white' if dark else ''))
    if note:s+=b.text(x+20,y+29,note,'micro '+('muted' if dark else ''),'start')
    return s+divider(x+20,y+47,x+w-20,y+47,dark)

def source_card(x,y,label,sub,kind):
    s=f'<g class="float-a">{panel(x,y,154,116)}{icon(x+18,y+18,kind,26)}'
    s+=b.text(x+136,y+69,label,'label')+b.text(x+136,y+94,sub,'micro')+'</g>'
    return s

def market_desktop():
    s=b.text(52,54,'مصادر السوق','display','start')
    for i,(label,sub,kind) in enumerate([('WhatsApp','محادثات','chat'),('PDF','مخططات','file'),('مواقع','صفحات متفرّقة','web')]):
        y=82+i*156;s+=source_card(42,y,label,sub,kind)+route(f'M196 {y+58}C238 {y+58} 226 320 270 320')
    s+=f'<g class="float-b">{panel(270,54,712,532)}'+header(270,54,712,'Estavo Market','مثال · البحث والمقارنة')
    s+=chip(782,120,168,'التجمع الخامس')+chip(598,120,168,'شقة · ٣ غرف')+b.rect(548,120,38,32,'#28567f',7)+icon(555,124,'search',24,True)
    s+=b.text(950,190,'نتائج البحث','title')+b.text(298,190,'اختياران للمقارنة','micro','start')+divider(298,207,954,207)
    for y,name,location,price,term in [(238,'مشروع أ','القاهرة الجديدة · شقة','حسب المشروع','خطة سداد'),(323,'مشروع ب','القاهرة الجديدة · شقة','حسب المشروع','خطة سداد')]:
        s+=b.rect(298,y,656,68,'#f7fafc',10,'stroke="#dce7ef"')+b.rect(914,y+18,18,18,'#28567f',4)+icon(911,y+15,'check',24,True)
        s+=b.text(890,y+28,name,'label')+b.text(890,y+52,location,'micro')+b.text(610,y+28,price,'body')+b.text(410,y+28,term,'body')
    s+=b.rect(298,423,656,54,'#e8f2f8',9)+b.text(930,456,'اختياران للمقارنة','small')+b.rect(312,433,128,34,'#28567f',7)+b.text(426,456,'قارن العقارات','micro white')
    s+=b.text(950,530,'بيانات المشروع بعد المراجعة','micro')+divider(298,500,954,500)+'</g>'
    return s

def updates_desktop():
    s=f'<g class="float-a">{panel(42,54,940,532)}'
    s+=b.text(958,94,'مراجعة إستاڤو','title')+b.text(66,91,'تغييرات السوق','small','start')+divider(66,116,958,116)
    # A single review workspace: incoming changes remain part of the product,
    # instead of becoming three detached icon cards connected to a gate.
    s+=b.rect(66,140,250,414,'#f7fafc',14,'stroke="#dce7ef"')
    s+=b.text(292,176,'تغييرات السوق','label')+b.circle(88,169,15,'#28567f')+b.text(88,176,'٣','micro white','middle')
    s+=f'<path d="M92 219V423" stroke="#a9c6e2" stroke-width="2"/>'
    events=[('مشروع جديد','المشروع والمنطقة','building'),('سعر اتعدّل','السعر قبل وبعد','chart'),('السداد اتغيّر','المقدّم وفترة التقسيط','file')]
    for i,(label,sub,kind) in enumerate(events):
        y=205+i*96
        if i==2:s+=b.rect(78,y-11,226,78,'#e8f2f8',10)
        s+=b.circle(92,y+18,7,'#5c91c7')+icon(112,y+5,kind,24)+b.text(288,y+25,label,'label')+b.text(288,y+50,sub,'micro')
        if i<2:s+=divider(112,y+70,288,y+70)
    s+=b.rect(78,480,226,50,'#102b45',10)+icon(92,493,'shield',22,True)+b.text(288,510,'بعد المراجعة','micro white')

    s+=b.text(950,160,'مثال تحديث مشروع','label')+b.text(950,196,'مشروع أ','title')+b.text(950,224,'القاهرة الجديدة · شقة ٣ غرف','small')
    s+=b.hero_plan(354,151,152,116,False,True)+divider(344,250,954,250)
    s+=b.text(720,280,'السابق','micro','middle')+b.text(500,280,'الحالي','micro','middle')
    rows=[('السعر','قبل المراجعة','بعد المراجعة'),('خطة السداد','خطة سابقة','خطة حالية'),('حالة الوحدات','متاحة','محدودة')]
    for i,(label,old,new) in enumerate(rows):
        y=296+i*68
        s+=b.rect(344,y,610,56,'#f7fafc' if i!=1 else '#e8f2f8',9)
        s+=b.text(930,y+34,label,'micro')+b.text(720,y+34,old,'small','middle')+b.text(500,y+34,new,'label','middle')
        s+=f'<path d="M628 {y+28}H578m9-7-9 7 9 7" fill="none" stroke="#5c91c7" stroke-width="2"/>'
    s+=b.rect(344,510,610,44,'#102b45',9)+icon(362,520,'check',20,True)+b.text(936,538,'مثال توضيحي · تحديث بعد المراجعة','micro white')+'</g>'
    return s

def brand_desktop():
    s=f'<g class="float-a">{panel(32,46,960,548)}'
    # One browser surface contains the website, its assistant and the data sync.
    s+=b.rect(32,46,960,46,'#f1f5f8',20)+b.rect(32,70,960,22,'#f1f5f8',0)
    for x in [58,74,90]:s+=b.circle(x,68,4,'#a9c6e2')
    s+=b.text(968,76,'موقع باسمك','label')+b.text(512,75,'yourcompany.com','micro','middle')+divider(52,92,972,92)
    s+=b.text(956,126,'شركتك العقارية','label')+b.text(754,126,'العقارات','micro')+b.text(646,126,'عنّا','micro')
    s+=b.rect(56,146,568,244,'#102b45',12)+b.hero_residential_visual(74,162,190,210)
    s+=b.text(600,190,'بيتك القادم','title white')+b.text(600,223,'يبدأ هنا','title white')+b.text(600,258,'اكتشف عقارات تناسبك','micro muted')
    s+=b.rect(286,316,312,48,'#ffffff',9)+icon(548,328,'search',20)+b.text(536,346,'التجمع الخامس','micro')

    s+=b.rect(648,146,318,244,'#ffffff',12,'stroke="#dce7ef"')+b.rect(648,146,318,56,'#102b45',12)+b.rect(648,186,318,16,'#102b45',0)
    s+=icon(670,162,'chat',24,True)+b.text(946,180,'مساعد باسمك','label white')
    s+=b.rect(680,220,266,56,'#e8f2f8',11)+b.text(930,246,'إيه خطط سداد شقة ٣ غرف؟','micro')
    s+=b.rect(704,296,242,50,'#f1f5f8',11)+b.text(930,326,'بيجهّز المقارنة…','micro')
    for i,x in enumerate([720,732,744]):s+=b.circle(x,326,3,'#5c91c7',f'class="typing" style="animation-delay:{i*.16}s"')

    s+=b.rect(56,414,910,150,'#f7fafc',14,'stroke="#dce7ef"')
    s+=b.text(940,449,'بيانات واحدة','label')
    # Keep the supporting line inside its own right-hand copy column in both
    # directions; the English translation is materially wider than Arabic.
    s+=b.text(940,478,'نفس البيانات في منصتك','micro').replace('class="micro"','class="micro" style="font-size:15px"')
    s+=b.rect(76,437,220,80,'#102b45',11)+icon(94,456,'link',24,True)+b.text(278,468,'Estavo Data API','label white')+b.text(278,494,'منصتك الحالية','micro muted')
    s+=b.rect(326,437,382,38,'#ffffff',8)+b.text(690,462,'المشروع · الوحدة · السعر · السداد','micro')
    s+=b.rect(326,489,382,38,'#e8f2f8',8)+icon(340,497,'check',20)+b.text(692,514,'بعد المراجعة','micro')
    s+='</g>'
    return s

def conversation_desktop():
    s=b.text(54,54,'محادثة تفهم الطلب','display','start')
    s+=f'<g class="float-a">{panel(42,84,438,492)}'+header(42,84,438,'مساعدك الذكي','AI')
    s+=b.rect(126,157,326,77,'#e8f2f8',14)+b.text(430,187,'عايز شقة ٣ غرف','small')+b.text(430,216,'في التجمع الخامس','small')
    s+=b.rect(68,264,326,95,'#f1f5f8',14)+b.text(90,294,'تمام — إيه خطة السداد المناسبة؟','small','start')+b.text(90,329,'مدة أقصر ولا أطول؟','small','start')
    s+=b.rect(184,388,268,54,'#e8f2f8',14)+b.text(430,421,'قارن خطط السداد','small')
    s+=b.rect(68,473,326,68,'#f1f5f8',14)+b.text(90,502,'بيبحث في عقاراتك…','micro','start')
    for i,x in enumerate([90,102,114]):s+=b.circle(x,522,3,'#5c91c7',f'class="typing" style="animation-delay:{i*.16}s"')
    s+='</g>'+route('M480 330C532 330 520 330 570 330')
    s+=f'<g class="float-b">{panel(570,84,412,492)}'+header(570,84,412,'اختيارات من عقاراتك','مطابقة الطلب')
    s+=chip(594,150,174,'التجمع الخامس')+chip(782,150,174,'٣ غرف')
    for y,name,term in [(208,'مشروع أ','خطة سداد أ'),(342,'مشروع ب','خطة سداد ب')]:
        s+=b.rect(594,y,362,112,'#f7fafc',12,'stroke="#dce7ef"')+b.hero_plan(608,y+13,114,86)+b.text(938,y+34,name,'label')+b.text(938,y+62,'شقة · ٣ غرف','micro')+b.text(938,y+91,term,'small')
    s+=b.rect(594,492,362,51,'#e8f2f8',9)+b.text(938,524,'السعر حسب بيانات كل وحدة','micro')+'</g>'
    return s

def client_desktop():
    # Three observed signals flow into one concise call brief. The dark section
    # remains visible around the composition, so there is no dashboard-sized
    # white slab competing with the headline.
    s='<g class="float-a">'
    s+=b.circle(388,320,118,'none','stroke="#5c91c7" stroke-opacity=".18" stroke-width="24"')
    s+=b.circle(388,320,64,'#173a55','stroke="#47749a" stroke-width="1.5"')
    s+=b.text(388,313,'إشارات','micro muted','middle')+b.text(388,340,'العميل','label white','middle')

    signals=[('بحث عن شقة','شقة · ٣ غرف','search'),('شاف مشاريع','التجمع الخامس','eye'),('قارن السداد','أكتر من خطة','chart')]
    for i,(label,value,kind) in enumerate(signals):
        y=128+i*146
        s+=panel(42,y,260,88,True,14)+icon(62,y+25,kind,24,True)
        s+=b.text(278,y+35,label,'label white')+b.text(278,y+65,value,'micro muted')
        s+=route(f'M302 {y+44}C342 {y+44} 340 320 324 320')

    s+=route('M452 320H520')
    s+=f'<g class="float-b">{panel(520,92,462,456,False,20)}'
    s+=b.text(954,135,'ملخص قبل المكالمة','title')+b.text(546,132,'من تفاعلات العميل','micro','start')+divider(546,154,956,154)
    s+=b.rect(546,178,410,76,'#f7fafc',12)+icon(566,202,'person',26)
    s+=b.text(930,204,'طلب العميل','micro')+b.text(930,235,'شقة · ٣ غرف في التجمع الخامس','label')
    s+=b.text(930,292,'الاهتمام الأوضح','micro')
    s+=b.rect(546,308,410,74,'#e8f2f8',12)+icon(566,331,'chart',26)
    s+=b.text(930,336,'خطط السداد','label')+b.text(930,365,'قارن أكتر من خطة','micro')
    s+=b.text(930,424,'ابدأ المكالمة من هنا','micro')
    s+=divider(546,442,956,442)
    s+=icon(566,468,'chat',24)+b.text(930,483,'اسأله عن خطة السداد المناسبة','label')
    s+=b.text(930,516,'ابدأ من اهتمامه بدل ما تبدأ من الصفر.','micro')
    s+='</g></g>'
    return s

def roi_desktop():
    s=f'<g class="float-a">{panel(42,54,940,532)}'
    s+=b.text(958,94,'حساب العائد','title')+b.text(66,91,'مثال · بدون أسعار أو نسب متوقعة','small','start')+divider(66,116,958,116)

    # Price history is shown as a real analysis surface instead of a generic bar.
    s+=b.rect(66,140,574,300,'#f7fafc',14,'stroke="#dce7ef"')
    s+=b.text(616,178,'تاريخ الأسعار','label')+b.text(90,176,'من وقت الشراء إلى الآن','micro','start')
    for y in [228,282,336,390]:s+=f'<path d="M96 {y}H610" stroke="#dce7ef" stroke-width="1"/>'
    s+=f'<path d="M112 360C174 344 214 351 270 320S370 292 420 270S520 214 590 202L590 390H112Z" fill="#dcecf5" fill-opacity=".75"/>'
    s+=f'<path d="M112 360C174 344 214 351 270 320S370 292 420 270S520 214 590 202" fill="none" stroke="#28567f" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    for i,(x,y) in enumerate([(112,360),(205,344),(300,306),(420,270),(510,228),(590,202)]):
        s+=b.circle(x,y,6,'#ffffff','stroke="#5c91c7" stroke-width="3"'+(' class="typing"' if i==5 else ''))
    s+=b.text(112,420,'وقت الشراء','micro','middle')+b.text(590,420,'الآن','micro','middle')

    # The right rail explains the arithmetic without inventing monetary values.
    s+=b.rect(662,140,296,300,'#102b45',14)+b.text(934,178,'العائد الحقيقي','label white')+b.text(686,176,'حساب توضيحي','micro muted','start')
    calc=[('النمو في القيمة',214,190,'#5c91c7'),('تكلفة الشراء',272,132,'#a9c6e2'),('أثر التضخم',330,92,'#d5e5ef')]
    for label,y,w,color in calc:
        s+=b.text(934,y,label,'micro muted')+b.rect(686,y+12,238,12,'#173a55',6)+b.rect(686,y+12,w,12,color,6)
    s+=divider(686,374,934,374,True)+b.text(934,410,'العائد الحقيقي','label white')+b.rect(686,394,124,24,'#e8f2f8',7)+b.text(748,412,'الناتج','micro','middle')

    # Decision strip connects the calculation to the broker's actual conversation.
    s+=b.rect(66,462,892,92,'#e8f2f8',12)+b.text(934,493,'قارن البيع والاحتفاظ','label')+b.text(934,524,'النتيجة حسب بيانات الوحدة وتكلفتها وفترة الاحتفاظ','micro')
    s+=b.rect(90,480,124,52,'#ffffff',8)+b.text(152,511,'البيع','label','middle')
    s+=b.rect(230,480,124,52,'#ffffff',8)+b.text(292,511,'الاحتفاظ','label','middle')
    s+=f'<path d="M376 506H548" stroke="#5c91c7" stroke-width="2"/><circle cx="462" cy="506" r="7" fill="#28567f"/>'
    s+='</g>'
    return s

def company_desktop():
    """A brokerage Site, governed inventory rail and explicit team handoff."""
    s=f'<g class="float-a">{panel(34,46,956,548)}'
    s+=b.rect(34,46,956,44,'#f1f5f8',20)+b.rect(34,68,956,22,'#f1f5f8',0)
    for x in [58,74,90]:s+=b.circle(x,68,4,'#a9c6e2')
    s+=b.text(966,75,'موقع الشركة','label')+b.text(512,74,'yourcompany.com','micro','middle')+divider(54,90,970,90)

    # Public website surface.
    s+=b.rect(56,112,590,280,'#ffffff',14,'stroke="#dce7ef"')
    s+=b.rect(56,112,590,54,'#102b45',14)+b.rect(56,148,590,18,'#102b45',0)
    s+=b.text(620,145,'شركتك العقارية','label white')+b.text(364,144,'العقارات','micro muted')+b.text(260,144,'عنّا','micro muted')
    s+=b.rect(76,184,550,128,'#102b45',10)+b.hero_residential_visual(90,194,142,108)
    s+=b.text(606,218,'بيتك القادم','title white')+b.text(606,250,'يبدأ هنا','title white')+b.rect(366,270,220,26,'#ffffff',7)+icon(548,272,'search',20)+b.text(536,290,'التجمع الخامس','micro')
    s+=b.text(620,345,'وحدات مختارة باسم الشركة','label')
    for x in [76,250,424]:
        s+=b.rect(x,360,152,18,'#e8f2f8',6)+b.rect(x,384,104,5,'#a9c6e2',3)

    # Governed company inventory rail.
    s+=b.rect(668,112,300,280,'#102b45',14)+b.text(944,148,'إدارة الوحدات','label white')+b.text(692,146,'الشركة','micro muted','start')+divider(692,164,944,164,True)
    for i,(title,note) in enumerate([('بيانات السوق بعد التحديث','بعد مراجعة إستاڤو'),('بيانات عقاراتك','مملوكة للشركة')]):
        y=184+i*92
        s+=b.rect(692,y,252,72,'#173a55',10)+icon(708,y+22,'building' if i==0 else 'file',22,True)
        s+=b.text(928,y+30,title,'label white').replace('class="label white"','class="label white" style="font-size:16px"')+b.text(928,y+56,note,'micro muted')
    s+=b.rect(692,354,252,24,'#e8f2f8',7)+icon(700,357,'check',18)+b.text(930,371,'جاهز للمتابعة','micro')

    # The buyer's explicit request moves to the company team.
    s+=b.rect(56,416,912,146,'#f7fafc',14,'stroke="#dce7ef"')
    s+=b.text(944,450,'تسليم لفريق المبيعات','label')+b.text(80,448,'حسب ما شاركه العميل','micro','start')+divider(80,468,944,468)
    s+=b.rect(80,490,346,48,'#e8f2f8',9)+icon(94,502,'chat',20)+b.text(410,519,'طلب العميل الصريح','label')
    s+=route('M446 514H566')+b.rect(586,490,358,48,'#ffffff',9,'stroke="#dce7ef"')+icon(602,502,'person',20)+b.text(928,519,'فريق المبيعات','label')
    s+='</g>'
    return s

def signals_desktop():
    # Three numbered stages explain the outcome without implying a lead score:
    # website actions -> a configured Meta audience -> a relevant Facebook ad.
    s=f'<g class="float-a">{panel(42,54,940,532)}'
    s+=b.text(958,94,'من تفاعل العميل إلى إعلان يناسبه','title')
    s+=meta_mark(66,70,38)+facebook_mark(114,72,34)+b.text(162,91,'مثال توضيحي','small','start')+divider(66,116,958,116)

    # Website signals are concrete events rather than generic source cards.
    s+=b.rect(686,140,272,414,'#f7fafc',14,'stroke="#dce7ef"')
    s+=b.rect(902,154,38,26,'#e8f2f8',13)+b.text(921,174,'١','micro','middle')
    s+=b.text(884,176,'تفاعلات العميل','label')+icon(706,155,'web',25)
    events=[('مشاهدة مشروع','صفحة مشروع','eye'),('بحث عن شقة','شقة · ٣ غرف','search'),('مقارنة سداد','خطط السداد','chart')]
    for i,(label,sub,kind) in enumerate(events):
        y=204+i*82
        s+=b.rect(704,y,236,66,'#ffffff',9,'stroke="#dce7ef"')+icon(718,y+19,kind,23)
        s+=b.text(920,y+27,label,'label')+b.text(920,y+51,sub,'micro')
    s+=b.rect(704,468,236,60,'#e8f2f8',9)+b.text(920,493,'نفس العميل','micro')+b.text(920,517,'سياق أوضح لاهتمامه','label')

    # The audience is visibly a Meta destination, not an abstract score card.
    s+=stage_route(686,652,338)
    s+=b.rect(420,166,232,344,'#102b45',14)
    s+=b.rect(438,184,38,26,'#173a55',13)+b.text(457,204,'٢','micro muted','middle')
    s+=meta_mark(506,184,60,'#78a9dc')+b.text(536,260,'جمهور مخصص','label white','middle')+b.text(536,290,'مبني على تفاعلات موقعك','micro muted','middle')
    s+=b.circle(536,350,52,'#173a55','stroke="#5c91c7" stroke-width="2"')+icon(524,338,'person',24,True)
    s+=chip(448,422,176,'التجمع الخامس · شقق',True)
    s+=b.rect(448,468,176,25,'#e8f2f8',7)+b.text(536,486,'جاهز لحملاتك','micro','middle')

    # A Facebook post makes the downstream use immediately recognisable.
    s+=stage_route(420,386,338)
    s+=b.rect(66,140,320,414,'#ffffff',14,'stroke="#dce7ef"')
    s+=facebook_mark(84,154,34)+b.text(126,167,'Facebook','label','start')+b.text(126,190,'إعلان أقرب لاهتمامه','micro','start')
    s+=b.rect(330,154,38,26,'#e8f2f8',13)+b.text(349,174,'٣','micro','middle')
    s+=b.rect(84,214,284,188,'#102b45',10)+b.hero_residential_visual(96,226,122,164)
    # The facade and the message are separate columns. Explicit type sizes
    # prevent the longer English copy from drifting over the artwork.
    s+=b.text(350,250,'عقار يناسب بحثك','label white').replace('class="label white"','class="label white" style="font-size:18px"')
    s+=b.text(350,278,'في التجمع الخامس','micro muted').replace('class="micro muted"','class="micro muted" style="font-size:16px"')
    s+=b.rect(238,324,112,34,'#ffffff',7)+b.text(294,347,'اعرف المزيد','micro','middle')
    s+=b.text(368,435,'اكتشف تفاصيل المشروع','label')+b.text(368,463,'مرتبط باهتمام العميل','micro')
    s+=divider(84,480,368,480)+icon(92,496,'eye',20)+b.text(120,512,'مشاهدة','micro','start')+icon(266,496,'chat',20)+b.text(294,512,'تواصل','micro','start')
    s+='</g>'
    return s

def reach_desktop():
    # One distribution workspace shows where the record is published and what
    # brokers do with it. This replaces the generic hub-and-spokes diagram.
    s=f'<g class="float-a">{panel(42,54,940,532)}'
    s+=b.text(958,94,'توزيع الوحدة','title')+b.text(66,91,'مثال · نفس الوحدة وقنوات بيع أوسع','small','start')+divider(66,116,958,116)

    # Source record remains visible while distribution settings change.
    s+=b.rect(66,140,274,414,'#102b45',14)
    s+=b.text(316,176,'وحدتك','label white')+b.text(90,174,'نفس التفاصيل','micro muted','start')
    # Keep a clear gutter between the plan and the detail column in both
    # Arabic and the longer English translation.
    s+=b.hero_plan(88,212,92,86,True,True)
    s+=b.text(316,226,'شقة · ٣ غرف','label white').replace('class="label white"','class="label white" style="font-size:16px"')+b.text(316,255,'التجمع الخامس','micro muted')
    s+=divider(90,338,316,338,True)
    s+=b.text(316,371,'السعر','micro muted')+b.text(316,400,'حسب الوحدة','label white')
    s+=b.text(316,443,'العمولة','micro muted')+b.text(316,474,'اللي إنت بتحددها','label white')
    s+=b.rect(90,505,226,28,'#173a55',7)+icon(98,509,'check',18,True)+b.text(304,523,'جاهزة للتوزيع','micro muted')

    # Two destinations make the promise in the copy explicit.
    s+=b.text(950,160,'منشورة في','label')
    for x,title,kind in [(356,'موقعك','web'),(654,'Estavo Brokers','link')]:
        s+=b.rect(x,180,284,84,'#f7fafc',11,'stroke="#dce7ef"')+icon(x+18,198,kind,26)
        s+=b.text(x+260,210,title,'label')+b.text(x+260,240,'نفس بيانات الوحدة','micro')
        s+=b.rect(x+18,232,42,18,'#e8f2f8',9)+b.circle(x+49,241,7,'#28567f','class="typing"')

    s+=b.text(950,304,'نشاط شبكة البروكرز','label')+b.text(364,302,'مثال','micro','start')+divider(356,320,958,320)
    activities=[('شاف تفاصيل الوحدة','مشاهدة'),('حفظ الوحدة','اهتمام'),('طلب التواصل','متابعة')]
    for i,(action,state) in enumerate(activities):
        y=336+i*60
        s+=b.rect(356,y,602,50,'#f7fafc' if i!=2 else '#e8f2f8',9)
        s+=b.circle(926,y+25,14,'#ffffff','stroke="#a9c6e2"')+icon(914,y+13,'person',24)
        s+=b.text(896,y+31,action,'label')+b.text(560,y+31,state,'micro')
        s+=b.rect(378,y+16,96,18,'#ffffff',9)+b.text(426,y+30,'بروكر','micro','middle')
    s+=b.rect(356,526,602,28,'#102b45',7)+icon(370,531,'check',18,True)+b.text(944,545,'نفس الوحدة · نفس البيانات · شبكة أوسع','micro white')
    s+='</g>'
    return s

def mobile_scene(kind):
    # Mobile keeps the desktop argument but removes repeated labels and columns.
    if kind=='market-explorer':
        return b.text(18,27,'مصادر السوق','label','start')+''.join(panel(16+i*120,43,110,57)+icon(24+i*120,56,k,18)+b.text(116+i*120,76,l,'micro').replace('class="micro"','class="micro" style="font-size:14px"') for i,(l,k) in enumerate([('WhatsApp','chat'),('PDF','file'),('مواقع','web')]))+route('M71 100V121H195')+route('M191 100V121H195')+route('M311 100V121H195')+panel(16,121,358,278)+header(16,121,358,'Estavo Market','بحث ومقارنة')+chip(32,181,156,'التجمع الخامس')+chip(202,181,156,'٣ غرف')+''.join(b.rect(32,y,326,58,'#f7fafc',8,'stroke="#dce7ef"')+b.text(344,y+25,n,'label')+b.text(344,y+47,price+' · '+term,'micro') for y,n,price,term in [(230,'مشروع أ','حسب المشروع','خطة سداد'),(300,'مشروع ب','حسب المشروع','خطة سداد')])+b.rect(32,370,326,16,'#e8f2f8',5)
    if kind=='market-updates':
        s=panel(16,18,358,394)+header(16,18,358,'مراجعة إستاڤو','تغييرات السوق')
        # Changes are tabs inside one review surface, not three disconnected cards.
        for i,(label,kind) in enumerate([('مشروع جديد','building'),('سعر اتعدّل','chart'),('السداد اتغيّر','file')]):
            x=32+i*108
            s+=b.rect(x,80,98,44,'#e8f2f8' if i==2 else '#f7fafc',8,'stroke="#dce7ef"')+b.text(x+49,107,label,'micro','middle').replace('class="micro"','class="micro" style="font-size:12px"')
        s+=b.text(352,154,'مثال تحديث · مشروع أ','label')+b.text(352,178,'القاهرة الجديدة · شقة ٣ غرف','micro')+divider(32,190,358,190)
        for i,(label,old,new) in enumerate([('السعر','قبل المراجعة','بعد المراجعة'),('خطة السداد','خطة سابقة','خطة حالية'),('حالة الوحدات','متاحة','محدودة')]):
            y=202+i*55
            s+=b.rect(32,y,326,48,'#f7fafc' if i!=1 else '#e8f2f8',7)+b.text(346,y+19,label,'micro')
            s+=b.text(276,y+39,old,'micro','middle').replace('class="micro"','class="micro" style="font-size:14px"')+b.text(132,y+39,new,'label','middle').replace('class="label"','class="label" style="font-size:17px"')
            s+=f'<path d="M221 {y+34}H183m8-6-8 6 8 6" fill="none" stroke="#5c91c7" stroke-width="1.7"/>'
        s+=b.rect(32,370,326,28,'#102b45',7)+icon(40,375,'check',18,True)+b.text(348,390,'مثال توضيحي · بعد المراجعة','micro white').replace('class="micro white"','class="micro white" style="font-size:14px"')
        return s
    if kind=='brand-unified':
        s=panel(16,18,358,394)
        s+=b.rect(16,18,358,38,'#f1f5f8',20)+b.rect(16,39,358,17,'#f1f5f8',0)
        s+=b.text(356,43,'موقع باسمك','label')+b.text(32,42,'yourcompany.com','micro','start').replace('class="micro"','class="micro" style="font-size:12px"')+divider(32,57,358,57)
        s+=b.rect(32,74,326,126,'#102b45',10)+b.hero_residential_visual(40,82,105,108)
        s+=b.text(344,106,'بيتك القادم','label white')+b.text(344,133,'يبدأ هنا','label white')+b.text(344,161,'اكتشف عقارات تناسبك','micro muted')
        # The assistant is a separate product surface below the website hero,
        # not an overlapping floating card.
        s+=b.rect(46,214,298,96,'#ffffff',11,'stroke="#dce7ef"')+b.rect(46,214,298,34,'#102b45',11)+b.rect(46,236,298,12,'#102b45',0)
        s+=icon(58,221,'chat',18,True)+b.text(332,237,'مساعد باسمك','micro white')
        s+=b.rect(68,257,264,24,'#e8f2f8',7)+b.text(320,274,'إيه خطط سداد شقة ٣ غرف؟','micro').replace('class="micro"','class="micro" style="font-size:13px"')
        s+=b.rect(98,287,234,17,'#f1f5f8',6)+b.text(320,300,'بيجهّز المقارنة…','micro').replace('class="micro"','class="micro" style="font-size:12px"')
        s+=b.rect(32,326,326,54,'#f7fafc',9,'stroke="#dce7ef"')+icon(44,340,'link',20)+b.text(346,348,'Estavo Data API','micro')+b.text(346,370,'نفس البيانات في منصتك','micro')
        return s
    if kind=='company-site':
        s=panel(16,18,358,394)
        s+=b.rect(16,18,358,38,'#f1f5f8',18)+b.rect(16,39,358,17,'#f1f5f8',0)+b.text(356,43,'موقع الشركة','label')+b.text(32,42,'yourcompany.com','micro','start').replace('class="micro"','class="micro" style="font-size:12px"')+divider(32,57,358,57)
        s+=b.rect(32,74,326,118,'#102b45',10)+b.hero_residential_visual(42,82,98,100)+b.text(344,105,'شركتك العقارية','label white')+b.text(344,134,'وحدات مختارة باسم الشركة','micro muted')+b.rect(208,154,126,22,'#ffffff',6)+icon(306,155,'search',18)+b.text(296,170,'التجمع الخامس','micro')
        s+=b.rect(32,208,326,88,'#102b45',10)+b.text(344,232,'إدارة الوحدات','label white')
        s+=b.rect(48,246,140,34,'#173a55',7)+b.text(178,268,'بيانات السوق بعد التحديث','micro muted').replace('class="micro muted"','class="micro muted" style="font-size:11px"')
        s+=b.rect(202,246,140,34,'#173a55',7)+b.text(332,268,'بيانات عقاراتك','micro muted').replace('class="micro muted"','class="micro muted" style="font-size:11px"')
        s+=b.rect(32,312,326,70,'#f7fafc',9,'stroke="#dce7ef"')+b.text(344,334,'تسليم لفريق المبيعات','label').replace('class="label"','class="label" style="font-size:16px"')+b.text(48,333,'حسب ما شاركه العميل','micro','start').replace('class="micro"','class="micro" style="font-size:11px"')
        s+=b.rect(48,348,112,22,'#e8f2f8',6)+b.text(152,364,'طلب العميل الصريح','micro').replace('class="micro"','class="micro" style="font-size:11px"')+route('M168 359H216')+b.rect(224,348,118,22,'#ffffff',6,'stroke="#dce7ef"')+b.text(334,364,'فريق المبيعات','micro').replace('class="micro"','class="micro" style="font-size:11px"')
        return s
    if kind=='ai-conversation':
        s=panel(16,18,358,394)+header(16,18,358,'مساعدك الذكي','AI')
        s+=b.rect(94,80,264,61,'#e8f2f8',11)+b.text(344,106,'عايز شقة ٣ غرف','micro')+b.text(344,130,'في التجمع الخامس','micro')
        s+=b.rect(32,158,280,62,'#f1f5f8',11)+b.text(48,185,'إيه خطة السداد المناسبة؟','micro','start')+b.text(48,208,'مدة أقصر ولا أطول؟','micro','start')
        s+=b.rect(130,237,228,41,'#e8f2f8',11)+b.text(344,263,'قارن خطط السداد','micro')
        s+=b.text(352,316,'اختيارات من عقاراتك','label')
        for y,name,term in [(331,'مشروع أ','خطة سداد أ'),(370,'مشروع ب','خطة سداد ب')]:
            s+=b.rect(32,y,326,32,'#f7fafc',7,'stroke="#dce7ef"')+b.text(344,y+22,name+' · '+term,'micro')
        return s
    if kind=='client-context':
        # The section heading already carries the story. Start directly with
        # the three signals so the phone composition stays quiet and legible
        # on the dark section background.
        s=''
        for i,(label,kind) in enumerate([('بحث','search'),('مشاهدة','eye'),('مقارنة','chart')]):
            x=32+i*108
            s+=panel(x,24,98,60,True,10)+icon(x+10,42,kind,18,True)+b.text(x+88,58,label,'micro white').replace('class="micro white"','class="micro white" style="font-size:11px"')
            s+=route(f'M{x+49} 84V108')
        s+=panel(32,108,326,252,False,16)
        s+=b.text(342,140,'ملخص قبل المكالمة','label')+b.text(48,138,'من تفاعلاته','micro','start')+divider(48,154,342,154)
        s+=b.rect(48,170,294,54,'#f7fafc',9)+icon(60,185,'person',19)+b.text(330,192,'شقة · ٣ غرف','label').replace('class="label"','class="label" style="font-size:15px"')+b.text(330,214,'التجمع الخامس','micro')
        s+=b.rect(48,238,294,54,'#e8f2f8',9)+icon(60,253,'chart',19)+b.text(330,261,'خطط السداد','label').replace('class="label"','class="label" style="font-size:15px"')+b.text(330,283,'قارن أكتر من خطة','micro')
        s+=divider(48,308,342,308)+icon(60,321,'chat',19)+b.text(330,336,'اسأله عن خطة السداد المناسبة','label').replace('class="label"','class="label" style="font-size:15px"')
        return s
    if kind=='roi-breakdown':
        s=panel(16,18,358,394)+b.text(356,50,'حساب العائد','label')+b.text(32,48,'مثال','micro','start')+divider(32,64,358,64)
        # Keep the same analysis story on a phone: price history, the
        # deductions, then the actual sell/hold decision.
        s+=b.rect(32,80,326,154,'#f7fafc',10,'stroke="#dce7ef"')
        s+=b.text(344,106,'تاريخ الأسعار','micro')+b.text(46,105,'من وقت الشراء إلى الآن','micro','start').replace('class="micro"','class="micro" style="font-size:13px"')
        for y in [140,174,208]:s+=f'<path d="M48 {y}H342" stroke="#dce7ef" stroke-width="1"/>'
        s+=f'<path d="M52 201C86 192 112 196 145 179S205 171 236 151S296 126 338 119L338 214H52Z" fill="#dcecf5" fill-opacity=".78"/>'
        s+=f'<path d="M52 201C86 192 112 196 145 179S205 171 236 151S296 126 338 119" fill="none" stroke="#28567f" stroke-width="3" stroke-linecap="round"/>'
        for i,(x,y) in enumerate([(52,201),(111,194),(174,172),(236,151),(288,132),(338,119)]):
            s+=b.circle(x,y,4,'#ffffff','stroke="#5c91c7" stroke-width="2"'+(' class="typing"' if i==5 else ''))
        s+=b.rect(32,250,326,104,'#102b45',10)
        for i,(label,width) in enumerate([('النمو في القيمة',108),('تكلفة الشراء',72),('أثر التضخم',48)]):
            y=271+i*22
            s+=b.text(342,y,label,'micro muted').replace('class="micro muted"','class="micro muted" style="font-size:13px"')
            s+=b.rect(52,y-10,116,7,'#173a55',4)+b.rect(52,y-10,width,7,['#5c91c7','#a9c6e2','#d5e5ef'][i],4)
        s+=divider(48,326,342,326,True)+b.text(342,347,'العائد الحقيقي','micro white').replace('class="micro white"','class="micro white" style="font-size:14px"')+b.rect(52,332,116,16,'#e8f2f8',5)+b.text(110,345,'الناتج','micro','middle').replace('class="micro"','class="micro" style="font-size:12px"')
        s+=b.rect(32,366,326,32,'#e8f2f8',8)+b.text(344,386,'قارن البيع والاحتفاظ','micro').replace('class="micro"','class="micro" style="font-size:14px"')+b.rect(48,371,62,22,'#ffffff',6)+b.text(79,387,'البيع','micro','middle').replace('class="micro"','class="micro" style="font-size:12px"')+b.rect(118,371,72,22,'#ffffff',6)+b.text(154,387,'الاحتفاظ','micro','middle').replace('class="micro"','class="micro" style="font-size:12px"')
        return s
    if kind=='meta-signals':
        s=panel(16,18,358,394)+b.text(358,50,'من التفاعل للإعلان','label')+meta_mark(32,29,28)+facebook_mark(70,30,26)+divider(32,64,358,64)
        s+=b.rect(314,76,30,22,'#e8f2f8',11)+b.text(329,93,'١','micro','middle')+b.text(304,94,'تفاعلات موقعك','micro')
        for i,(label,kind) in enumerate([('مشاهدة مشروع','eye'),('بحث عن شقة','search'),('مقارنة سداد','chart')]):
            x=32+i*108
            s+=b.rect(x,104,98,38,'#f7fafc',7,'stroke="#dce7ef"')+icon(x+7,114,kind,18)+b.text(x+90,128,label,'micro').replace('class="micro"','class="micro" style="font-size:10.5px"')
        s+=f'<path d="M195 142V155m-5-5 5 5 5-5" fill="none" stroke="#5c91c7" stroke-width="2"/>'
        s+=b.rect(32,160,326,78,'#102b45',10)+b.rect(314,169,30,22,'#173a55',11)+b.text(329,186,'٢','micro muted','middle')+meta_mark(48,174,42,'#78a9dc')+b.text(304,184,'جمهور مخصص','label white')+b.text(342,211,'التجمع الخامس · شقق','micro muted')+b.rect(224,215,118,15,'#e8f2f8',7)+b.text(283,227,'جاهز للاستخدام','micro','middle').replace('class="micro"','class="micro" style="font-size:11px"')
        s+=f'<path d="M195 238V251m-5-5 5 5 5-5" fill="none" stroke="#5c91c7" stroke-width="2"/>'
        s+=b.rect(32,256,326,138,'#ffffff',10,'stroke="#dce7ef"')+facebook_mark(44,267,24)+b.text(76,284,'Facebook','micro','start')+b.rect(314,265,30,22,'#e8f2f8',11)+b.text(329,282,'٣','micro','middle')
        s+=b.rect(44,298,122,82,'#102b45',8)+b.hero_residential_visual(51,304,74,69)
        s+=b.text(342,309,'إعلان أقرب لاهتمامه','micro').replace('class="micro"','class="micro" style="font-size:13px"')+b.text(342,334,'اكتشف تفاصيل المشروع','label').replace('class="label"','class="label" style="font-size:15px"')+b.text(342,359,'مرتبط باهتمام العميل','micro').replace('class="micro"','class="micro" style="font-size:13px"')+b.rect(210,366,128,20,'#e8f2f8',6)+b.text(274,381,'اعرف المزيد','micro','middle').replace('class="micro"','class="micro" style="font-size:12px"')
        return s
    if kind=='listings-reach':
        s=panel(16,18,358,394)+b.text(356,50,'توزيع الوحدة','label')+b.text(32,48,'مثال','micro','start')+divider(32,64,358,64)
        s+=b.rect(32,80,326,82,'#102b45',10)+b.hero_plan(44,90,72,62,True,True)
        s+=b.text(344,105,'شقة · ٣ غرف','label white')+b.text(344,130,'التجمع الخامس','micro muted')+b.text(344,151,'العمولة اللي إنت بتحددها','micro muted')
        s+=b.text(352,190,'منشورة في','micro')
        for x,title,kind in [(32,'موقعك','web'),(200,'Estavo Brokers','link')]:
            s+=b.rect(x,202,158,50,'#f7fafc',8,'stroke="#dce7ef"')+icon(x+10,215,kind,20)+b.text(x+146,225,title,'micro').replace('class="micro"','class="micro" style="font-size:12px"')+b.circle(x+146,241,4,'#28567f','class="typing"')
        s+=b.text(352,282,'نشاط شبكة البروكرز','label')
        for i,(action,state) in enumerate([('شاف تفاصيل الوحدة','مشاهدة'),('حفظ الوحدة','اهتمام'),('طلب التواصل','متابعة')]):
            y=296+i*31
            s+=b.rect(32,y,326,26,'#e8f2f8' if i==2 else '#f7fafc',6)+icon(40,y+4,'person',18)+b.text(346,y+19,action,'micro').replace('class="micro"','class="micro" style="font-size:14px"')+b.text(132,y+19,state,'micro','middle').replace('class="micro"','class="micro" style="font-size:12px"')
        s+=b.rect(32,396,326,8,'#102b45',4)
        return s
    return panel(16,18,358,150)+header(16,18,358,'وحدتك','نفس التفاصيل')+b.hero_plan(32,77,106,78)+b.text(354,96,'شقة · ٣ غرف','label')+b.text(354,124,'التجمع الخامس','micro')+route('M195 168V195')+panel(111,195,168,88,True)+b.text(195,230,'Estavo Brokers','label white','middle')+b.text(195,258,'توزيع الوحدة','micro muted','middle')+route('M195 283V310')+''.join(panel(x,310,106,78)+icon(x+8,326,'person',18)+b.text(x+96,343,'بروكر','micro')+b.text(x+96,365,'تفاصيل الوحدة','micro') for x in [16,142,268])

SCENES={
 'market-explorer':market_desktop,
 'market-updates':updates_desktop,
 'brand-unified':brand_desktop,
 'company-site':company_desktop,
 'ai-conversation':conversation_desktop,
 'client-context':client_desktop,
 'roi-breakdown':roi_desktop,
 'meta-signals':signals_desktop,
 'listings-reach':reach_desktop,
}

def roi_card_visual(name):
    """A small, content-specific product crop for each ROI input card."""
    if name=='roi-price-history':
        s=b.rect(4,4,232,96,'#f7fafc',12,'stroke="#dce7ef"')
        for y in [30,52,74]:s+=f'<path d="M22 {y}H218" stroke="#dce7ef"/>'
        s+=f'<path d="M24 78C52 70 66 73 91 61S130 55 150 42S188 30 216 23L216 84H24Z" fill="#dcecf5"/>'
        s+=f'<path d="M24 78C52 70 66 73 91 61S130 55 150 42S188 30 216 23" fill="none" stroke="#28567f" stroke-width="3" stroke-linecap="round"/>'
        for i,(x,y) in enumerate([(24,78),(66,72),(108,56),(150,42),(184,32),(216,23)]):s+=b.circle(x,y,3.5,'#ffffff','stroke="#5c91c7" stroke-width="2"'+(' class="typing"' if i==5 else ''))
        return s
    if name=='roi-purchase-cost':
        s=b.rect(4,4,232,96,'#f7fafc',12,'stroke="#dce7ef"')
        s+=f'<path d="M24 52H216" stroke="#a9c6e2" stroke-width="3" stroke-linecap="round"/>'
        for i,x in enumerate([28,69,110,151,192,216]):
            s+=b.circle(x,52,7,'#28567f' if i in [0,5] else '#ffffff','stroke="#5c91c7" stroke-width="2"')
            if i<5:s+=b.rect(x+10,45,24 if i==0 else 22,14,'#dcecf5' if i<3 else '#a9c6e2',7)
        s+=b.rect(24,20,74,12,'#28567f',6)+b.rect(106,20,50,12,'#a9c6e2',6)+b.rect(164,20,52,12,'#d5e5ef',6)
        s+=f'<path d="M28 71V82M216 71V82" stroke="#28567f" stroke-width="2"/>'
        return s
    if name=='roi-value-growth':
        s=b.rect(4,4,232,96,'#f7fafc',12,'stroke="#dce7ef"')
        s+=b.rect(30,57,54,27,'#a9c6e2',8)+b.rect(156,24,54,60,'#28567f',8)
        s+=f'<path d="M95 70C118 70 124 41 146 41m-12-10 12 10-12 10" fill="none" stroke="#5c91c7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        s+=b.rect(30,20,54,8,'#dce7ef',4)+b.rect(156,10,54,8,'#dce7ef',4)
        return s
    s=b.rect(4,4,232,96,'#102b45',12,'stroke="#274b68"')
    s+=b.rect(22,22,72,14,'#5c91c7',7)+b.rect(22,45,54,12,'#a9c6e2',6)+b.rect(22,66,38,10,'#d5e5ef',5)
    s+=f'<path d="M109 20V82" stroke="#47749a" stroke-width="1"/>'
    s+=f'<path d="M126 52H151m-8-8 8 8-8 8" fill="none" stroke="#a9c6e2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    s+=b.rect(164,25,52,55,'#f5f9fc',9)+b.rect(174,64,32,6,'#5c91c7',3)+b.circle(190,45,9,'#28567f','class="typing"')
    return s

def service_card_visual(name):
    """Small product previews for the four homepage service cards."""
    if name=='service-market':
        s=b.rect(4,4,232,116,'#ffffff',12,'stroke="#dce7ef"')
        s+=b.rect(4,4,232,24,'#f1f5f8',12)+b.rect(4,16,232,12,'#f1f5f8',0)
        for x in [18,28,38]:s+=b.circle(x,16,2.5,'#a9c6e2')
        s+=b.rect(18,37,88,15,'#e8f2f8',5)+b.rect(112,37,66,15,'#f1f5f8',5)+b.rect(184,37,34,15,'#28567f',5)
        for y in [61,84]:
            s+=b.rect(18,y,200,18,'#f7fafc',5,'stroke="#dce7ef"')+b.rect(26,y+5,9,9,'#28567f',3)+b.rect(44,y+6,62,4,'#a9c6e2',2)+b.rect(142,y+6,56,4,'#d5e5ef',2)
        s+=b.rect(18,107,200,6,'#dcecf5',3)+b.rect(18,107,76,6,'#5c91c7',3)
        return s
    if name=='service-website':
        s=b.rect(4,4,232,116,'#ffffff',12,'stroke="#dce7ef"')
        s+=b.rect(4,4,232,22,'#f1f5f8',12)+b.rect(4,15,232,11,'#f1f5f8',0)
        for x in [18,28,38]:s+=b.circle(x,15,2.5,'#a9c6e2')
        s+=b.rect(14,34,212,68,'#102b45',8)+b.hero_residential_visual(22,42,76,54)
        s+=b.rect(114,43,92,8,'#f5f9fc',4)+b.rect(126,58,80,5,'#a9c6e2',3)+b.rect(116,74,90,16,'#ffffff',5)+b.rect(178,78,24,8,'#28567f',4)
        s+=b.rect(14,108,78,5,'#28567f',3)+b.rect(98,108,54,5,'#a9c6e2',3)+b.rect(158,108,68,5,'#d5e5ef',3)
        return s
    if name=='service-ai':
        s=b.rect(4,4,232,116,'#ffffff',12,'stroke="#dce7ef"')
        s+=b.rect(4,4,232,30,'#102b45',12)+b.rect(4,20,232,14,'#102b45',0)
        s+=f'<path d="M22 12l3 6 6 3-6 3-3 6-3-6-6-3 6-3Z" fill="#f5f9fc"/>'
        s+=b.rect(70,42,148,25,'#e8f2f8',8)+b.rect(92,49,108,4,'#5c91c7',2)+b.rect(124,57,76,4,'#a9c6e2',2)
        s+=b.rect(22,75,178,25,'#f1f5f8',8)+b.rect(42,82,116,4,'#47749a',2)
        for i,x in enumerate([174,184,194]):s+=b.circle(x,90,2.5,'#5c91c7',f'class="typing" style="animation-delay:{i*.16}s"')
        s+=b.rect(22,106,196,7,'#dcecf5',4)+b.rect(22,106,82,7,'#28567f',4)
        return s
    s=b.rect(4,4,232,116,'#ffffff',12,'stroke="#dce7ef"')
    s+=b.rect(14,16,104,84,'#102b45',9)
    for i,w in enumerate([72,58,80,48]):
        y=28+i*16
        s+=b.rect(26,y,w,5,'#a9c6e2' if i else '#f5f9fc',3)+b.circle(104,y+2.5,3,'#5c91c7')
    s+=f'<path d="M118 42C138 42 136 28 154 28M118 58H154M118 74C138 74 136 90 154 90" fill="none" stroke="#5c91c7" stroke-width="2" stroke-linecap="round"/>'
    for i,(y,w) in enumerate([(17,66),(49,58),(81,66)]):
        s+=b.rect(154,y,w,22,'#f7fafc',6,'stroke="#dce7ef"')+b.rect(164,y+7,w-30,4,'#28567f' if i==1 else '#a9c6e2',2)+b.circle(210,y+11,3,'#28567f' if i==1 else '#5c91c7','class="typing"' if i==1 else '')
    s+=b.rect(14,106,206,7,'#e8f2f8',4)+b.rect(14,106,148,7,'#5c91c7',4)
    return s

def main():
    for name,fn in SCENES.items():
        b.save(name, name.replace('-',' '), 'Flat product-specific Estavo interface with illustrative example data.', '<g class="scene-float">'+fn()+'</g>', 640, DEFS)
        b.save(name+'-mobile', name.replace('-',' ')+' mobile', 'Compact mobile version of the same product illustration.', '<g class="scene-float">'+mobile_scene(name)+'</g>', 430, DEFS, 390)
    for name in ['roi-price-history','roi-purchase-cost','roi-value-growth','roi-real-return']:
        b.save(name, name.replace('-',' '), 'Small product-specific ROI metric visualization.', '<g class="scene-float">'+roi_card_visual(name)+'</g>', 104, DEFS, 240)
    for name in ['service-market','service-website','service-ai','service-integrations']:
        b.save(name, name.replace('-',' '), 'Compact product preview for a homepage service card.', '<g class="scene-float">'+service_card_visual(name)+'</g>', 124, DEFS, 240)
    print('Built nine product scenes plus ROI and service-card product visuals.')

if __name__ == '__main__':
    main()
