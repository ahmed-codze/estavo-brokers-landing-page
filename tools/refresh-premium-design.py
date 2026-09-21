#!/usr/bin/env python3
"""Refresh active landing pages and their templates without rebuilding page copy.

Run after build-illustrations.py and refresh-mobile-art.py. Updates critical
CSS from source, hero vector scenes and icon assets; preserves links and page data.
"""
from pathlib import Path
import re
import json

ROOT=Path(__file__).resolve().parent.parent
CSS=ROOT/'assets/css/v3'

def div_end(source,start):
    depth=0
    for m in re.finditer(r'<div\b[^>]*>|</div\s*>',source[start:]):
        depth += -1 if m.group().startswith('</') else 1
        if depth==0:return start+m.end()
    raise ValueError('Unbalanced div')

EN_COPY={**json.loads((ROOT/'tools/illustration-copy-en.json').read_text()),**json.loads((ROOT/'tools/illustration-mobile-copy-en.json').read_text())}

def translate_markup(source):
    def translate(m):
        value=m.group(1).strip()
        if value not in EN_COPY:raise ValueError('Missing mobile translation: '+value)
        return '>'+EN_COPY[value]+'<'
    return re.sub(r'>([^<>]*[\u0600-\u06ff][^<>]*)<',translate,source)

def home_figure(name,english=False,prefix='assets'):
    home=(ROOT/'index.html').read_text()
    start=re.search(r'<div class="[^"]*\bes-'+name+r'-figure\b[^"]*"',home).start()
    fragment=home[start:div_end(home,start)]
    if english:
        fragment=translate_markup(fragment)
        fragment=re.sub(r'(estavo-[a-z-]+?)(-still)?(\.svg)',r'\1-en\2\3',fragment)
        fragment=re.sub(r'(icons/estavo-[a-z-]+)-en\.svg',r'\1.svg',fragment)
        for name in ['unit','ai','hero','service']:
            fragment=fragment.replace(f'estavo-{name}-scene-en.svg',f'estavo-{name}-scene.svg').replace(f'estavo-{name}-scene-en-still.svg',f'estavo-{name}-scene-still.svg')
    return fragment.replace('src="assets/','src="'+prefix+'/').replace('srcset="assets/','srcset="'+prefix+'/')

def vector_pictures(source):
    # Media selection happens in the HTML document, independently of SVG-image
    # animation preferences. Retain the original image as the ordinary fallback.
    source=re.sub(r'<picture class="es-vector-picture">\s*<source\b[^>]*>\s*(<img\b[^>]*>)\s*</picture>',r'\1',source)
    def picture(m):
        image=m.group()
        url=re.search(r'src="([^"]+)"',image)[1]
        still=url[:-4]+'-still.svg'
        return f'<picture class="es-vector-picture"><source media="(prefers-reduced-motion: reduce)" srcset="{still}" type="image/svg+xml" />{image}</picture>'
    return re.sub(r'<img\b[^>]*src="[^"]*/img/estavo-[a-z-]+\.svg"[^>]*>',picture,source)

def refresh_english_figures(source):
    for section_id,name,target in [('data-h','market','es-product-frame'),('maintain-h','updates','es-flow'),('view-site','brand-unified','es-product-frame'),('view-ai','conversation','es-product-frame'),('buyer-h','client','es-context-compare')]:
        section=re.search(r'<section\b[^>]*(?:aria-labelledby|id)="'+section_id+r'"[^>]*>',source)
        if not section:continue
        end=source.index('</section>',section.end())
        content=source[section.end():end]
        m=re.search(r'<div class="[^"]*\b(?:'+target+'|es-'+name+r'-figure)\b[^"]*"',content)
        if m:
            start=section.end()+m.start();last=div_end(source,start)
            source=source[:start]+home_figure(name,True)+source[last:]
    return source.replace('One project can be sold by 100 brokers.','Several brokers can sell the same project.')

def icon(name,prefix,cls='es-art-icon'):
    return f'<img class="{cls}" src="{prefix}/img/icons/estavo-{name}.svg" width="160" height="160" alt="" loading="lazy" decoding="async" />'

def hero_mobile_icon(name):
    paths={
        'website':'<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
        'assistant':'<path d="M5 4h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-8l-6 3v-3a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z"/><path d="M7 9h10M7 13h6"/>',
        'compare':'<path d="M4 5h16M4 12h16M4 19h16"/><circle cx="9" cy="5" r="2" fill="var(--es-white)"/><circle cx="15" cy="12" r="2" fill="var(--es-white)"/><circle cx="9" cy="19" r="2" fill="var(--es-white)"/>',
        'location':'<path d="M18 10c0 5-6 11-6 11S6 15 6 10a6 6 0 1 1 12 0Z"/><circle cx="12" cy="10" r="2"/>',
        'unit':'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M13 4v16M4 12h9M13 10h7"/>',
        'price':'<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
        'calendar':'<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M8 3v4M16 3v4M4 10h16M8 14h2M14 14h2"/>',
    }
    return f'<svg class="es-hero-detail-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</svg>'

def mobile_hero(prefix,english):
    title,unit,location,per_unit,payment_scope = ('Property data','3 rooms','Fifth Settlement','Per unit','Per project') if english else ('بيانات عقاراتك','٣ غرف','التجمع الخامس','حسب الوحدة','حسب المشروع')
    glyph=f'<img class="es-hero-ai-glyph" src="{prefix}/img/estavo-hero-ai-symbol.svg" width="24" height="24" alt="" decoding="async" />'
    return f'''<div class="es-hero-mobile-map es-hero-mobile-map--modern es-hero-mobile-map--compact">
      <svg class="es-hero-mobile-links" viewBox="0 0 360 286" preserveAspectRatio="none" aria-hidden="true"><g fill="none" stroke="#5c91c7" stroke-width="1.6" stroke-linecap="round"><path d="M151 76C160 76 155 72 164 72M151 190C160 190 155 213 164 213M78 274V286"/></g><g fill="#28567f"><circle cx="151" cy="76" r="2.5"/><circle cx="164" cy="72" r="2.5"/><circle cx="151" cy="190" r="2.5"/><circle cx="164" cy="213" r="2.5"/><circle cx="78" cy="286" r="2.5"/></g></svg>
      <div class="es-hero-record">
        <div class="es-hero-record-heading"><img class="es-hero-source-mark" src="{prefix}/logo/estavo-mark.svg" width="600" height="600" alt="" /><b><bdi>Estavo</bdi></b></div><small class="es-hero-compact-caption">{title}</small>
        <img class="es-hero-record-plan" src="{prefix}/img/estavo-hero-floorplan-dark.svg" width="240" height="200" alt="" decoding="async" />
        <div class="es-hero-record-main"><b>{'Apartment · 3 rooms' if english else 'شقة · ٣ غرف'}</b><span>{location}</span></div>
        <div class="es-hero-record-terms"><span><small>{'Price' if english else 'السعر'}</small><b>{per_unit}</b></span><span><small>{'Payment' if english else 'السداد'}</small><b>{payment_scope}</b></span></div>
      </div>
      <div class="es-hero-product-site">
        <div class="es-hero-website-nav"><b>{'Your website' if english else 'موقعك'}</b><small>{'Your brand' if english else 'بعلامتك'}</small></div>
        <div class="es-hero-website-banner"><span><b>{'Your next home' if english else 'بيتك القادم'}<br />{'starts here' if english else 'يبدأ هنا'}</b></span><img class="es-hero-website-visual" src="{prefix}/img/estavo-hero-residential-visual.svg" width="160" height="150" alt="" decoding="async" /><div class="es-hero-website-search"><span>{'City or area' if english else 'المدينة أو المنطقة'}</span><b>{'Search' if english else 'بحث'}</b></div></div>
        <div class="es-hero-website-section"><b>{'Properties' if english else 'العقارات'}</b><small>{'View all →' if english else 'عرض الكل ←'}</small></div>
      </div>
      <div class="es-hero-product-assistant">
        <div class="es-hero-chat-header"><span class="es-hero-ai-mark">{glyph}</span><b>{'AI chat' if english else 'مساعدك الذكي'}</b></div>
        <div class="es-hero-chat-question">{'Payment plans for 3 rooms?' if english else 'إيه خطط سداد شقة ٣ غرف؟'}</div>
        <div class="es-hero-chat-reply"><span>{'Comparing…' if english else 'بيجهّز المقارنة…'}</span><span class="es-hero-chat-typing"><i></i><i></i><i></i></span></div>
      </div>
      <div class="es-hero-product-market">
        <div class="es-hero-product-heading"><b><bdi>Estavo Market</bdi></b><small>{'Example' if english else 'مثال'}</small></div>
        <div class="es-hero-market-filters"><span>{location}<i aria-hidden="true">⌄</i></span><span>{unit}<i aria-hidden="true">⌄</i></span><span class="es-hero-market-search" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/></svg></span></div>
        <div class="es-hero-market-table"><div class="es-hero-market-columns"><span>{'Property' if english else 'المشروع والوحدة'}</span><span>{'Price' if english else 'السعر'}</span><span>{'Payment' if english else 'السداد'}</span><span></span></div>{''.join(f'<div class="es-hero-market-row"><span><b>{project}</b></span><span>{per_unit}</span><span>{term}</span><i class="es-hero-market-selected" aria-hidden="true">✓</i></div>' for project,term in [("Project A" if english else "مشروع أ","Plan A" if english else "خطة أ"),("Project B" if english else "مشروع ب","Plan B" if english else "خطة ب")])}</div>
        <div class="es-hero-market-compare"><span>{'2 selected' if english else 'اختياران للمقارنة'}</span><b>{'Compare' if english else 'قارن العقارات'}</b></div>
      </div>
    </div>'''

def hero_figure(prefix,english):
    suffix='-en' if english else ''
    return f'''<div class="es-hero__figure" aria-hidden="true"><div class="es-hero-figure es-hero-figure--vector"><img class="es-hero-figure__vector" src="{prefix}/img/estavo-desktop-hero{suffix}.svg" alt="" width="1024" height="900" loading="eager" fetchpriority="high" decoding="async" />'''+mobile_hero(prefix,english)+'</div></div>'

def critical(prefix):
    modules=['tokens','base','layout','controls','header-footer','illustrations','responsive','premium']
    content='@layer reset, tokens, base, layout, components, motion, utilities;\n'+''.join((CSS/(m+'.css')).read_text() for m in modules)
    content=content.replace('../fonts/',prefix+'/fonts/')
    return f'<link rel="preconnect" href="https://fonts.googleapis.com" />\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&amp;display=swap" rel="stylesheet" />\n<style id="es-design-critical">\n{content}\n</style>'

def replace_critical(source,prefix):
    head,rest=source.split('</head>',1)
    head=re.sub(r'<style\b[^>]*>.*?</style>', '', head, flags=re.S)
    head=re.sub(r'<link\b[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com|plex-arabic-(?:400|500|600)\.woff2)[^>]*>', '',head)
    head=re.sub(r'<noscript>\s*</noscript>', '',head)
    return head.rstrip()+'\n'+critical(prefix)+'\n</head>'+rest

def choose_icon(copy):
    for words,name in [(['ai','assistant','مساعد','ذكاء'],'chat'),(['تحديث','review','مراجعة','آمن','verified'],'shield'),(['سعر','نمو','roi','price','growth','return'],'chart'),(['وحدة','unit','تفاصيل'],'plan'),(['ربط','integration','meta','network','بروكر'],'network'),(['عميل','customer','client','contact'],'profile'),(['مدينة','cities','منطقة','المناطق','location'],'map'),(['موقع','website','project','مشروع'],'building')]:
        if any(w in copy.lower() for w in words):return name
    return 'layers'

def refresh_icons(source,prefix):
    def card(m):
        following=source[m.end():m.end()+700]
        heading=re.search(r'<h3\b[^>]*>(.*?)</h3>',following,re.S)
        name=choose_icon(re.sub(r'<[^>]*>','',heading.group(1)) if heading else '')
        return '<span class="es-service-card__icon" aria-hidden="true">'+icon(name,prefix)+'</span>'
    source=re.sub(r'<span\b[^>]*class="es-service-card__icon"[^>]*>.*?</span>',card,source,flags=re.S)
    def glyph(m):
        svg=m.group()
        name='map' if 'pattern' in svg else 'plan' if 'rect' in svg else 'chart' if 'draw' in svg else 'building'
        return icon(name,prefix,'es-art-glyph es-premium-glyph')
    source=re.sub(r'<svg\b[^>]*class="es-art-glyph[^\"]*"[^>]*>.*?</svg>',glyph,source,flags=re.S)
    for kind,name in [('project','building'),('price','chart'),('plan','plan'),('units','layers')]:
        pattern=r'(<span class="es-update-event es-update-event--'+kind+r'">\s*)<svg\b[^>]*>.*?</svg>'
        source=re.sub(pattern,lambda m:m.group(1)+icon(name,prefix),source,flags=re.S)
    return source

def service_hero(source,key,english,prefix):
    section=re.search(r'<section class="es-hero(?: es-service-hero)?"',source)
    if not section:return source
    source=source[:section.start()]+source[section.start():].replace('class="es-hero"','class="es-hero es-service-hero"',1)
    suffix='-en' if english else ''
    diagrams={'data':'market-explorer','market':'market-explorer','ai':'ai-conversation','marketing':'client-context','integrations':'brand-unified','websites':'brand-unified','examples':'brand-unified','listings':'listings-reach','insights':'roi-breakdown'}
    art=diagrams.get(key)
    if art:
        mobile=f'<img src="{prefix}/img/estavo-{art}-mobile{suffix}.svg" width="390" height="430" alt="" decoding="async" />'
        surface=' es-service-hero-art--client' if art=='client-context' else ''
        figure=f'<div class="es-service-hero-art es-service-hero-art--diagram{surface}" aria-hidden="true"><img src="{prefix}/img/estavo-{art}{suffix}.svg" width="1024" height="640" alt="" decoding="async" fetchpriority="high" /><div class="es-service-hero-mobile">{mobile}</div></div>'
    else:
        title='Services to match your business' if english else 'خدماتك، حسب شغلك'
        note='Example · your service selection' if english else 'مثال · اختيار خدماتك'
        services=[('map','Market data','Cities where you work'),('building','Your branded website','Your properties and identity'),('chat','Property assistant','From your property data')] if english else [('map','بيانات السوق','المدن اللي تشتغل فيها'),('building','موقع باسمك','عقاراتك وهويتك'),('chat','مساعد عقاري','من بيانات عقاراتك')]
        figure=f'<div class="es-service-hero-art es-service-configuration" aria-hidden="true"><p class="es-service-configuration__note">{note}</p><p class="es-service-configuration__title">{title}</p><img class="es-service-configuration__scene" src="{prefix}/img/estavo-service-scene.svg" width="640" height="184" alt="" decoding="async" />'+''.join('<div class="es-service-configuration__row">'+icon(n,prefix)+f'<span><b>{label}</b><small>{value}</small></span></div>' for n,label,value in services)+'</div>'
    current=re.search(r'<div class="es-service-hero-art\b',source[section.start():])
    if current:
        start=section.start()+current.start();end=div_end(source,start)
        return source[:start]+figure+source[end:]
    container=re.search(r'<div class="[^"]*\bes-container\b[^"]*">',source[section.start():])
    if not container:
        raise ValueError(f'Missing hero container for {key}')
    start=section.start()+container.start();end=div_end(source,start)
    return source[:end-6]+figure+source[end-6:]

def update_home(source,english):
    m=re.search(r'<div class="es-hero__figure"[^>]*>',source)
    if m:
        end=div_end(source,m.start());source=source[:m.start()]+hero_figure('assets',english)+source[end:]
    return refresh_english_figures(source) if english else source

def refresh_home_heroes():
    # A scoped preview refresh preserves all other figures, pages and head tags.
    for name, english in [('index.html', False), ('en.html', True)]:
        page=ROOT/name
        source=page.read_text()
        match=re.search(r'<div class="es-hero__figure"[^>]*>',source)
        if not match: raise ValueError('Missing homepage hero: '+name)
        fragment=vector_pictures(hero_figure('assets',english))
        source=source[:match.start()]+fragment+source[div_end(source,match.start()):]
        style=critical('assets').split('<style id="es-design-critical">',1)[1]
        source,count=re.subn(r'<style id="es-design-critical">.*?</style>',lambda _: '<style id="es-design-critical">'+style,source,flags=re.S)
        if count != 1: raise ValueError('Missing critical CSS: '+name)
        page.write_text(source)
    print('Updated Arabic and English homepage heroes and their critical CSS.')

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home-hero-only', action='store_true', help='Refresh only the two homepage heroes and critical CSS')
    args=parser.parse_args()
    if args.home_hero_only:
        refresh_home_heroes()
    else:
        routes=json.loads((ROOT/'tools/routes.json').read_text())['routes']
        files=[(ROOT/'index.html','home',False,'assets'),(ROOT/'en.html','home',True,'assets')]
        for route in routes:
            if route['key']=='home':continue
            directory=ROOT/route['path'].strip('/')
            for lang in ['ar','en']:
                files.append((directory/('index.html' if lang=='ar' else 'en.html'),route['key'],lang=='en','../assets'))
                template=ROOT/'tools/pages'/f"{route['key']}.{lang}.html"
                if template.exists():
                    text=template.read_text();text=service_hero(text,route['key'],lang=='en','/assets');text=refresh_icons(text,'/assets');text=vector_pictures(text);template.write_text(text)

        for file,key,english,prefix in files:
            if not file.exists():continue
            source=file.read_text()
            source=replace_critical(source,prefix)
            source=update_home(source,english) if key=='home' else service_hero(source,key,english,prefix)
            source=refresh_icons(source,prefix)
            source=vector_pictures(source)
            file.write_text(source)

        (ROOT/'tools/partials/critical.css').write_text(critical('/assets'))
        print(f'Updated {len(files)} active landing pages, source templates and shared critical CSS.')
