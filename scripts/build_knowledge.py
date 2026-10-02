#!/usr/bin/env python3
# coding: utf-8
"""Render the reviewed bilingual content as crawlable, no-JS-required HTML."""
import hashlib
import html
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://estavo-brokers.com'
DATE = '2026-10-02'
ARTICLES = json.loads((ROOT / 'content/knowledge.json').read_text(encoding='utf8'))
BY_SLUG = {a['slug']: a for a in ARTICLES}
CSS = (ROOT / 'content/knowledge.css').read_bytes()
CSS_NAME = 'knowledge-' + hashlib.sha256(CSS).hexdigest()[:12] + '.css'
(ROOT / 'assets/css' / CSS_NAME).write_bytes(CSS)

LABELS = {
    'en': dict(home='Home', hub='Broker guides', cta='Explore Estavo', switch='العربية', skip='Skip to content',
               contents='On this page', faq='Questions brokers ask', sources='Sources and evidence', related='Keep reading',
               by='By Estavo Brokers', date='Published 2 October 2026', editorial='How we research and write',
               editorial_title='Useful answers, clear evidence', editorial_body='These guides are practical editorial checklists, not promises of sales or investment returns. Product descriptions follow our reviewed support documentation. Research pages distinguish observed records from conclusions, name the collection date and link public sources. We publish aggregate findings, not raw customer or listing data. Illustrative examples are labeled. Send corrections to',
               guide='Practical guide', case_study='Research case study', report='Market evidence report',
               hub_title='Better answers for your next property conversation.', hub_intro='Practical guides for brokers in Egypt: find suitable inventory, understand the buyer and send an offer they can decide from.',
               guide_heading='Solve the everyday questions', study_heading='See the evidence behind the method', report_heading='Understand the limits of price data',
               product_title='Put the research into your next offer.', product_body='Estavo Market helps you research projects and units, compare available information and prepare a branded PDF Offer. Confirm current availability and final terms before booking.',
               summary='Read the aggregate evidence', rights='Original analysis by Estavo Brokers. Public source links do not imply a partnership or endorsement.', privacy='Privacy',terms='Terms'),
    'ar': dict(home='الرئيسية', hub='أدلة البروكر', cta='اكتشف استافو', switch='English', skip='انتقل للمحتوى',
               contents='في الدليل ده', faq='أسئلة البروكرز', sources='المصادر والأدلة', related='كمّل القراءة',
               by='إعداد استافو بروكرز', date='نُشر في 2 أكتوبر 2026', editorial='إزاي بنبحث ونكتب؟',
               editorial_title='إجابات مفيدة ودليل واضح', editorial_body='الأدلة دي قوائم عملية من إعدادنا، مش وعود بمبيعات أو عوائد. وصف المنتج مبني على وثائق الدعم المراجعة. صفحات البحث بتفصل السجلات المرصودة عن الاستنتاجات، وتوضح تاريخ الجمع وتربط بالمصادر العامة. بننشر نتائج مجمعة، مش بيانات عملاء أو إعلانات خام. الأمثلة التوضيحية متسمية بوضوح. ابعت التصحيحات على',
               guide='دليل عملي', case_study='دراسة بحثية', report='تقرير أدلة السوق',
               hub_title='إجابات أوضح لمكالمة العميل الجاية.', hub_intro='أدلة عملية للبروكر في مصر: تلاقي المتاح المناسب، تفهم طلب العميل وتجهز عرض يساعده يقرر.',
               guide_heading='حل أسئلة الشغل اليومية', study_heading='شوف الدليل وراء طريقة البحث', report_heading='افهم حدود بيانات الأسعار',
               product_title='استخدم البحث في عرضك الجاي.', product_body='استافو ماركت يساعدك تبحث في المشاريع والوحدات، تقارن المعلومات المتاحة وتجهز PDF Offer باسمك. أكد المتاح الحالي والشروط النهائية قبل الحجز.',
               summary='اقرأ ملخص الأدلة المجمعة', rights='تحليل أصلي من استافو بروكرز. روابط المصادر العامة مش معناها شراكة أو تزكية.', privacy='الخصوصية',terms='الشروط')
}

def esc(value):
    return html.escape(str(value), quote=True)

def route(lang, slug=''):
    return '/guides/' + ('en/' if lang == 'en' else '') + (slug + '/' if slug else '')

def organization():
    return {'@type': 'Organization', '@id': BASE + '/#organization', 'name': 'Estavo Brokers',
            'alternateName': ['إستاڤو بروكرز'], 'url': BASE + '/',
            'logo': BASE + '/assets/logo/Estavo%20Icon.png', 'description': 'AI tools for real estate brokers in Egypt.',
            'email': 'support@estavo.space', 'areaServed': {'@type':'Country','name':'Egypt'}}

def schema(lang, article=None):
    url = BASE + route(lang, article['slug'] if article else '')
    labels = LABELS[lang]
    breadcrumbs = [{'@type':'ListItem','position':1,'name':labels['home'],'item':BASE+('/en.html' if lang=='en' else '/')},
                   {'@type':'ListItem','position':2,'name':labels['hub'],'item':BASE+route(lang)}]
    graph = [organization(), {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/', 'name':'Estavo Brokers','publisher':{'@id':BASE+'/#organization'},'inLanguage':['ar-EG','en']}]
    if article:
        a=article[lang]
        breadcrumbs.append({'@type':'ListItem','position':3,'name':a['title'],'item':url})
        graph.append({'@type':'Article','@id':url+'#article','url':url,'headline':a['title'], 'description':a['description'],
                      'abstract':a['answer'],'inLanguage':'ar-EG' if lang=='ar' else 'en', 'datePublished':DATE,'dateModified':DATE,
                      'genre':labels[article['kind'].replace('-','_')], 'author':{'@id':BASE+'/#organization'},
                      'publisher':{'@id':BASE+'/#organization'}, 'mainEntityOfPage':{'@type':'WebPage','@id':url},
                      'image':BASE+'/assets/og/og-'+lang+'.jpg',
                      'citation':[{'@type':'CreativeWork','name':s[lang],'url':BASE+s['url'] if s['url'].startswith('/') else s['url']} for s in article['sources']]})
        graph.append({'@type':'FAQPage','@id':url+'#questions','inLanguage':'ar-EG' if lang=='ar' else 'en',
                      'mainEntity':[{'@type':'Question','name':f['question'],'acceptedAnswer':{'@type':'Answer','text':f['answer']}} for f in a['faq']]})
    else:
        graph.append({'@type':'CollectionPage','@id':url,'url':url,'name':labels['hub'],'inLanguage':'ar-EG' if lang=='ar' else 'en',
                      'mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':a[lang]['title'],'url':BASE+route(lang,a['slug'])} for i,a in enumerate(ARTICLES)]}})
    graph.append({'@type':'BreadcrumbList','itemListElement':breadcrumbs})
    return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')

def layout(lang, body, article=None):
    l=LABELS[lang]; slug=article['slug'] if article else ''; other='en' if lang=='ar' else 'ar'
    a=article[lang] if article else {'title':l['hub'],'description':l['hub_intro']}
    url=BASE+route(lang,slug); dir='rtl' if lang=='ar' else 'ltr'
    home='/en.html' if lang=='en' else '/'
    # Existing first-party analytics configuration; no new account IDs or tracking dependencies.
    return f'''<!doctype html>
<html lang="{lang}" dir="{dir}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(a['title'])} | Estavo Brokers</title>
<meta name="description" content="{esc(a['description'])}"><meta name="author" content="Estavo Brokers">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="theme-color" content="#021d39">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ar" href="{BASE+route('ar',slug)}">
<link rel="alternate" hreflang="ar-EG" href="{BASE+route('ar',slug)}">
<link rel="alternate" hreflang="en" href="{BASE+route('en',slug)}">
<link rel="alternate" hreflang="x-default" href="{BASE+route('ar',slug)}">
<meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:site_name" content="Estavo Brokers">
<meta property="og:title" content="{esc(a['title'])}"><meta property="og:description" content="{esc(a['description'])}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/og/og-{lang}.jpg">
<meta property="og:image:alt" content="Estavo Brokers — AI tools for real estate brokers in Egypt">
<meta property="og:locale" content="{'ar_EG' if lang=='ar' else 'en_US'}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/logo/Estavo%20Icon.png"><link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/{CSS_NAME}">
<script type="application/ld+json">{schema(lang,article)}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NVFZMXPPLF"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-NVFZMXPPLF');</script>
<script src="/assets/js/referral.js?v=20260918-chat-ui" defer></script>
</head>
<body>
<a class="skip-link" href="#main">{l['skip']}</a>
<header class="site-header"><div class="header-inner"><a class="brand" href="{home}" aria-label="Estavo Brokers — {l['home']}"><img src="/assets/logo/Estavo%20Brokers%20Logo%20transparent.png" width="240" height="55" alt="Estavo Brokers"></a><nav aria-label="{'Main navigation' if lang=='en' else 'التنقل الرئيسي'}"><a href="{route(lang)}">{l['hub']}</a><a href="{route(other,slug)}" lang="{other}" hreflang="{other}">{l['switch']}</a><a class="button header-cta" href="https://brokers.estavo.space/go/?ref=default-landing-page">{l['cta']}</a></nav></div></header>
{body}
<footer class="site-footer"><div><p>Estavo Brokers · {'AI tools for real estate brokers in Egypt' if lang=='en' else 'أدوات الذكاء الاصطناعي للبروكرز العقاريين في مصر'}</p><nav aria-label="{'Footer' if lang=='en' else 'روابط الصفحة'}"><a href="{route(lang)}#editorial">{l['editorial']}</a><a href="/privacy{'-en' if lang=='en' else ''}.html">{l['privacy']}</a><a href="/terms{'-en' if lang=='en' else ''}.html">{l['terms']}</a><a href="mailto:support@estavo.space">support@estavo.space</a></nav><p class="small">© 2026 Estavo Brokers</p></div></footer>
</body></html>'''

def product(lang):
    l=LABELS[lang]
    return f'<section class="product-note"><h2>{l["product_title"]}</h2><p>{l["product_body"]}</p><a class="button" href="https://brokers.estavo.space/go/?ref=default-landing-page">{l["cta"]}</a></section>'

def article_page(article,lang):
    a=article[lang];l=LABELS[lang]
    sections=[(f'section-{i+1}',s['title'],s['html']) for i,s in enumerate(a['sections'])]
    toc=''.join(f'<li><a href="#{id}">{esc(title)}</a></li>' for id,title,_ in sections)
    toc+=f'<li><a href="#questions">{l["faq"]}</a></li><li><a href="#sources">{l["sources"]}</a></li>'
    prose=''.join(f'<section id="{id}"><h2>{esc(title)}</h2>{body}</section>' for id,title,body in sections)
    faq=''.join(f'<details><summary>{esc(f["question"])}</summary><p>{esc(f["answer"])}</p></details>' for f in a['faq'])
    sources=''.join(f'<li><a href="{esc(s["url"])}">{esc(s[lang])}</a></li>' for s in article['sources'])
    related=''.join(f'<li><a href="{route(lang,s)}">{esc(BY_SLUG[s][lang]["title"])}</a></li>' for s in article['related'])
    body=f'''<main id="main" class="article-shell"><nav class="breadcrumbs" aria-label="{'Breadcrumb' if lang=='en' else 'مسار الصفحة'}"><a href="{'/en.html' if lang=='en' else '/'}">{l['home']}</a><span aria-hidden="true">/</span><a href="{route(lang)}">{l['hub']}</a></nav>
<header class="article-header"><h1>{esc(a['title'])}</h1><p class="byline">{l['by']} · <time datetime="{DATE}">{l['date']}</time> · {l[article['kind'].replace('-','_')]}</p><p class="answer">{esc(a['answer'])}</p></header>
<div class="article-layout"><aside class="contents"><details open><summary>{l['contents']}</summary><nav aria-label="{l['contents']}"><ol>{toc}</ol></nav></details></aside><article class="prose" aria-label="{esc(a['title'])}">{prose}<section id="questions"><h2>{l['faq']}</h2>{faq}</section><section id="sources" class="sources"><h2>{l['sources']}</h2><ul>{sources}</ul><p class="small">{l['rights']}</p><p class="small"><a href="{route(lang)}#editorial">{l['editorial']}</a></p></section>{product(lang)}<section class="related"><h2>{l['related']}</h2><ul>{related}</ul></section></article></div></main>'''
    return layout(lang,body,article)

def hub_page(lang):
    l=LABELS[lang];sections=''
    for kind,heading in [('guide','guide_heading'),('case-study','study_heading'),('report','report_heading')]:
        rows=''.join(f'<li><div><h3><a href="{route(lang,a["slug"])}">{esc(a[lang]["title"])}</a></h3><p>{esc(a[lang]["description"])}</p></div><span class="read-link" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-6-6 6 6-6 6"/></svg></span></li>' for a in ARTICLES if a['kind']==kind)
        sections+=f'<section class="topic-group"><h2>{l[heading]}</h2><ul class="topic-list">{rows}</ul></section>'
    body=f'''<main id="main" class="hub-shell"><header class="hub-header"><h1>{l['hub_title']}</h1><p>{l['hub_intro']}</p><nav class="hub-jump" aria-label="{'Browse topics' if lang=='en' else 'تصفح الموضوعات'}"><a href="{route(lang,'find-developer-inventory')}">{'Find inventory' if lang=='en' else 'تلاقي المتاح'}</a><a href="{route(lang,'sell-more-properties')}">{'Improve your sales workflow' if lang=='en' else 'تحسّن خطوات البيع'}</a><a href="{route(lang,'property-price-evidence-september-2026')}">{'Read the research' if lang=='en' else 'تقرأ البحث'}</a></nav></header>{sections}<section id="editorial" class="editorial"><h2>{l['editorial_title']}</h2><p>{l['editorial_body']} <a href="mailto:support@estavo.space">support@estavo.space</a>.</p><p><a href="/guides/evidence/september-2026.json">{l['summary']}</a></p></section>{product(lang)}</main>'''
    return layout(lang,body)

def write_page(route_name,body):
    target=ROOT / route_name.lstrip('/') / 'index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(body,encoding='utf8')

for lang in ('ar','en'):
    write_page(route(lang),hub_page(lang))
    for article in ARTICLES:
        write_page(route(lang,article['slug']),article_page(article,lang))

# Preserve existing sitemap pages; add actual .html URLs for legacy static pages.
ns='http://www.sitemaps.org/schemas/sitemap/0.9';xhtml='http://www.w3.org/1999/xhtml'
ET.register_namespace('',ns);ET.register_namespace('xhtml',xhtml)
tree=ET.parse(ROOT/'sitemap.xml');root=tree.getroot()
for node in list(root):
    loc=node.find('{'+ns+'}loc')
    if loc is not None and '/guides/' in loc.text:
        root.remove(node);continue
    for child in node.iter():
        if child.tag=='{'+ns+'}loc' and child.text:
            child.text=re.sub(r'/(estavo-brokers(?:-en)?|what-is-estavo-brokers(?:-en)?)$',r'/\1.html',child.text)
        if 'href' in child.attrib:
            child.attrib['href']=re.sub(r'/(estavo-brokers(?:-en)?|what-is-estavo-brokers(?:-en)?)$',r'/\1.html',child.attrib['href'])
for slug in ['']+[a['slug'] for a in ARTICLES]:
    for lang in ('ar','en'):
        node=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=BASE+route(lang,slug)
        ET.SubElement(node,'{'+ns+'}lastmod').text=DATE
        for code,target in [('ar','ar'),('ar-EG','ar'),('en','en'),('x-default','ar')]:
            ET.SubElement(node,'{'+xhtml+'}link',{'rel':'alternate','hreflang':code,'href':BASE+route(target,slug)})
def indent(node, level=0):
    children=list(node)
    if children:
        node.text='\n'+'  '*(level+1)
        for child in children:
            indent(child, level+1)
        children[-1].tail='\n'+'  '*level
    node.tail='\n'+'  '*level
indent(root)
root.tail='\n'
tree.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
print(f'Rendered {len(ARTICLES)*2} articles and 2 hubs; stylesheet {CSS_NAME}')
