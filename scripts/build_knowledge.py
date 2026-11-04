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
for stale in (ROOT / 'assets/css').glob('knowledge-*.css'):
    if stale.name != CSS_NAME:
        stale.unlink()
(ROOT / 'assets/css' / CSS_NAME).write_bytes(CSS)

# The guides share the main site shell. Header, drawer, footer, critical CSS
# and the analytics snippet are read from the same sources tools/build-pages.js
# uses, so a nav or tracking change lands here on the next build.
TOOLS = ROOT / 'tools'
PARTIALS = TOOLS / 'partials'
CRITICAL_CSS = (PARTIALS / 'critical.css').read_text(encoding='utf8')
_gtag = re.search(r'const GTAG = `([\s\S]*?)`;', (TOOLS / 'build-pages.js').read_text(encoding='utf8'))
if not _gtag or 'fbq(' not in _gtag.group(1):
    raise SystemExit('build_knowledge: GTAG (gtag + Meta Pixel) not found in tools/build-pages.js')
GTAG = _gtag.group(1)
MARKET_GO = 'https://brokers.estavo.space/go/?ref=default-landing-page-market'

def versioned(url):
    """Content-hashed asset URL, matching versioned() in tools/build-pages.js."""
    digest = hashlib.sha256((ROOT / url.lstrip('/')).read_bytes()).hexdigest()[:10]
    return f'{url}?v={digest}'

LABELS = {
    'en': dict(home='Home', hub='Selling tips & broker guides', hub_short='Selling tips',
               cta='Open Estavo Market free', contents='On this page', faq='Questions brokers ask',
               sources='Sources and evidence', related='Keep reading',
               by='By Estavo', date='Published 2 October 2026', editorial='How we research and write',
               editorial_title='Useful answers, clear evidence', editorial_body='These guides are practical editorial checklists, not promises of sales or investment returns. Product descriptions follow our reviewed support documentation. Research pages distinguish observed records from conclusions, name the collection date and link public sources. We publish aggregate findings, not raw customer or listing data. Examples are labeled. Send corrections to',
               guide='Practical guide', case_study='Research case study', report='Market evidence report',
               eyebrow='Broker community', hub_intro='Practical guides for brokers in Egypt: find suitable inventory, understand the buyer and send an offer they can decide from.',
               jump='Browse topics', breadcrumb='Breadcrumb',
               product_title='Put the research into your next offer.', product_body='Research projects and unit types and prepare a PDF offer under your name in Estavo Market. Completely free for now; confirm availability before booking.',
               summary='Read the aggregate evidence', example='Template · Example', more='More on Estavo', rights='Original analysis by Estavo. Public source links do not imply a partnership or endorsement.'),
    'ar': dict(home='الرئيسية', hub='نصايح البيع وأدلة البروكر', hub_short='نصايح البيع',
               cta='تصفح <bdi>Estavo Market</bdi> مجانًا', contents='في الدليل ده', faq='أسئلة البروكرز',
               sources='المصادر والأدلة', related='كمّل القراءة',
               by='إعداد إستاڤو', date='نُشر في 2 أكتوبر 2026', editorial='إزاي بنبحث ونكتب؟',
               editorial_title='إجابات مفيدة ودليل واضح', editorial_body='الأدلة دي قوائم عملية من إعدادنا، مش وعود بمبيعات أو عوائد. وصف المنتج مبني على وثائق الدعم المراجعة. صفحات البحث بتفصل السجلات المرصودة عن الاستنتاجات، وتوضح تاريخ الجمع وتربط بالمصادر العامة. بننشر نتائج مجمعة، مش بيانات عملاء أو إعلانات خام. الأمثلة متسمية بوضوح. ابعت التصحيحات على',
               guide='دليل عملي', case_study='دراسة بحثية', report='تقرير أدلة السوق',
               eyebrow='مجتمع البروكرز', hub_intro='أدلة عملية للبروكر في مصر: تلاقي المتاح المناسب، تفهم طلب العميل وتجهز عرض يساعده يقرر.',
               jump='تصفح الموضوعات', breadcrumb='مسار الصفحة',
               product_title='استخدم البحث في عرضك الجاي.', product_body='ابحث في المشاريع ونماذج الوحدات وجهّز عرض <bdi>PDF</bdi> باسمك على <bdi>Estavo Market</bdi>. مجاني بالكامل حاليًا، وأكّد المتاح قبل الحجز.',
               summary='اقرأ ملخص الأدلة المجمعة', example='قالب جاهز · مثال توضيحي', more='كمان في إستاڤو', rights='تحليل أصلي من إستاڤو. روابط المصادر العامة مش معناها شراكة أو تزكية.')
}

# Hub grouping: what a broker is trying to do, not the content type.
GROUP_ICONS = {'selling-tips': 'client-interest', 'developers-inventory': 'project', 'research': 'analysis'}

# Sibling community destinations shown before the hub's closing box.
RELATED = {
    'ar': [('/insights/', 'جديد السوق', 'أخبار وإطلاقات كل يوم'), ('/jobs/', 'الوظائف', 'وظائف القطاع العقاري'),
           ('/challenges/', 'ألعاب وتحديات', 'لعبة البروكرز'), ('/developers/', 'المطورين', 'ملفات المطورين ومشاريعهم')],
    'en': [('/insights/en.html', 'Market news', 'Daily news and launches'), ('/jobs/en.html', 'Jobs', 'Real-estate jobs in Egypt'),
           ('/challenges/en.html', 'Games & challenges', 'The brokers’ game'), ('/developers/en.html', 'Developers', 'Developer profiles and projects')],
}

GROUPS = [
    ('selling-tips', ['sell-more-properties', 'find-property-clients', 'match-client-property', 'property-pdf-offer'],
     {'ar': ('نصايح البيع', 'خطوات عملية من أول طلب العميل لحد عرض واضح يقرر منه.', '4 أدلة'),
      'en': ('Selling tips', 'Practical steps from the client’s first request to an offer they can decide from.', '4 guides')}),
    ('developers-inventory', ['find-developer-inventory', 'compare-payment-plans'],
     {'ar': ('المطورين والإنفنتوري', 'تلاقي المتاح وتتأكد منه، وتقارن خطط السداد بأمانة.', 'دليلين'),
      'en': ('Developers & inventory', 'Find and verify what is available, and compare payment plans honestly.', '2 guides')}),
    ('research', ['archived-listing-evidence', 'developer-offer-evidence', 'property-price-evidence-september-2026'],
     {'ar': ('أبحاث وتقارير', 'الأدلة اللي ورا طريقتنا في البحث، وحدود بيانات الأسعار.', 'دراستين وتقرير'),
      'en': ('Research', 'The evidence behind our method, and the limits of price data.', '2 studies and a report')}),
]
_grouped = [slug for _, slugs, _ in GROUPS for slug in slugs]
assert sorted(_grouped) == sorted(BY_SLUG), 'every article must sit in exactly one hub group'
HUB_ORDER = [BY_SLUG[slug] for slug in _grouped]

def esc(value):
    return html.escape(str(value), quote=True)

# Arabic pages: isolate Latin runs and percentages that sit in text nodes, so
# "PDF", "Estavo Market" or "84.5%" keep their order inside RTL prose.
_ENT = r'&(?:[A-Za-z]+|#\d+|#x[0-9A-Fa-f]+);'
_CH = rf"(?:[A-Za-z0-9@./’'-]|{_ENT})"
_BIDI = re.compile(rf"((?<![&#A-Za-z0-9])[A-Za-z]{_CH}*(?:\s+[A-Za-z0-9]{_CH}*)*)|(\d[\d,.]*%)")
_TRAIL = re.compile(rf"(?:[.,:;/’'-]|&#x27;|&#39;)+$")

def _isolate(match):
    if match.group(2):
        return f'<bdi dir="ltr">{match.group(2)}</bdi>'
    run = match.group(1)
    tail = _TRAIL.search(run)
    cut = tail.start() if tail else len(run)
    return f'<bdi>{run[:cut]}</bdi>{run[cut:]}' if cut else run

def isolate_latin(markup):
    out = []; skip = 0
    for part in re.split(r'(<[^>]*>)', markup):
        if part.startswith('<'):
            tag = re.match(r'</?\s*([a-zA-Z0-9]+)', part)
            if tag and tag.group(1).lower() in ('bdi', 'script', 'style'):
                skip += -1 if part.startswith('</') else 1
            out.append(part)
        else:
            out.append(part if skip else _BIDI.sub(_isolate, part))
    return ''.join(out)

def route(lang, slug=''):
    return '/guides/' + ('en/' if lang == 'en' else '') + (slug + '/' if slug else '')

def relativize(doc, depth):
    """Root-style paths → depth-relative, like relativizeForServicePage() in build-pages.js."""
    up = '../' * depth
    doc = re.sub(r'\b(href|src|action)="/(?!/)', lambda m: f'{m.group(1)}="{up}', doc)
    return re.sub(r"url\((['\"]?)/(?!/)", lambda m: f'url({m.group(1)}{up}', doc)

def organization():
    return {'@type': 'Organization', '@id': BASE + '/#organization', 'name': 'Estavo',
            'alternateName': ['إستاڤو'], 'url': BASE + '/',
            'logo': BASE + '/assets/logo/Estavo%20Icon.png', 'description': 'Everything a real-estate broker in Egypt needs, in one place, with AI.',
            'email': 'support@estavo.space', 'areaServed': {'@type':'Country','name':'Egypt'}}

def schema(lang, article=None):
    url = BASE + route(lang, article['slug'] if article else '')
    labels = LABELS[lang]
    breadcrumbs = [{'@type':'ListItem','position':1,'name':labels['home'],'item':BASE+('/en.html' if lang=='en' else '/')},
                   {'@type':'ListItem','position':2,'name':labels['hub_short'],'item':BASE+route(lang)}]
    graph = [organization(), {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/', 'name':'Estavo','publisher':{'@id':BASE+'/#organization'},'inLanguage':['ar-EG','en']}]
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
                      'mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':a[lang]['title'],'url':BASE+route(lang,a['slug'])} for i,a in enumerate(HUB_ORDER)]}})
    graph.append({'@type':'BreadcrumbList','itemListElement':breadcrumbs})
    return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')

def shell_header(lang, slug):
    """Global header + drawer, with the language switch pointing at this guide's twin."""
    markup = (PARTIALS / f'header.{lang}.html').read_text(encoding='utf8')
    markup = markup.replace('<body class="es es-landing">', '<body class="es es-landing es-route-guides">', 1)
    hub = route(lang)
    current = 'page' if not slug else 'true'
    markup = markup.replace(f'href="{hub}"', f'href="{hub}" aria-current="{current}"')
    return switch_language(markup, lang, slug)

def shell_footer(lang, slug):
    return switch_language((PARTIALS / f'footer.{lang}.html').read_text(encoding='utf8'), lang, slug)

def switch_language(markup, lang, slug):
    # The partials hardcode the switch for /x/ ↔ /x/en.html pages.
    other = 'en' if lang == 'ar' else 'ar'
    old = 'href="en.html"' if lang == 'ar' else 'href="index.html"'
    return markup.replace(old, f'href="{route(other, slug)}"')

def market_button(lang, position):
    return (f'<a class="es-button es-button--primary kn-cta" href="{MARKET_GO}" data-track="market_opened" '
            f'data-position="{position}"><span>{LABELS[lang]["cta"]}</span></a>')

def layout(lang, body, article=None):
    l=LABELS[lang]; slug=article['slug'] if article else ''
    a=article[lang] if article else {'title':l['hub'],'description':l['hub_intro']}
    url=BASE+route(lang,slug); dir='rtl' if lang=='ar' else 'ltr'
    depth=route(lang,slug).count('/')-1
    doc = f'''<!DOCTYPE html>
<html lang="{lang}" dir="{dir}">
<head>
<meta charset="utf-8">
{GTAG}
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#fafcff">
<title>{esc(a['title'])} | Estavo</title>
<meta name="description" content="{esc(a['description'])}"><meta name="author" content="Estavo">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ar" href="{BASE+route('ar',slug)}">
<link rel="alternate" hreflang="ar-EG" href="{BASE+route('ar',slug)}">
<link rel="alternate" hreflang="en" href="{BASE+route('en',slug)}">
<link rel="alternate" hreflang="x-default" href="{BASE+route('ar',slug)}">
<meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:site_name" content="Estavo">
<meta property="og:title" content="{esc(a['title'])}"><meta property="og:description" content="{esc(a['description'])}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/og/og-{lang}.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{'إستاڤو — كل اللي محتاجه كبروكر في مكان واحد' if lang=='ar' else 'Estavo — everything you need as a broker, in one place'}">
<meta property="og:locale" content="{'ar_EG' if lang=='ar' else 'en_US'}"><meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@estavospace">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/logo/Estavo%20Icon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/logo/Estavo%20Icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/assets/css/{CSS_NAME}">
{CRITICAL_CSS}
<link rel="preload" as="style" href="{versioned('/assets/css/estavo-v3.css')}" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{versioned('/assets/css/estavo-v3.css')}"></noscript>
<script type="application/ld+json">{schema(lang,article)}</script>
</head>
{shell_header(lang, slug)}
{isolate_latin(body) if lang == 'ar' else body}
{shell_footer(lang, slug)}
<script src="{versioned('/assets/js/referral.js')}" defer></script>
<script src="{versioned('/assets/js/v3/estavo-v3.js')}" defer></script>
<link rel="stylesheet" href="{versioned('/assets/css/pd.css')}">
<link rel="stylesheet" href="{versioned('/assets/css/fx-site.css')}">
<script src="{versioned('/assets/js/pd.js')}" defer></script>
</body>
</html>
'''
    return relativize(doc, depth)

def product(lang, position):
    l=LABELS[lang]
    return f'<section class="product-note"><h2>{l["product_title"]}</h2><p>{l["product_body"]}</p>{market_button(lang, position)}</section>'

def breadcrumbs(lang, current=None):
    l=LABELS[lang]
    here=' aria-current="page"' if current=='hub' else ''
    trail=f'<a href="{"/en.html" if lang=="en" else "/"}">{l["home"]}</a><span aria-hidden="true">/</span><a href="{route(lang)}"{here}>{l["hub_short"]}</a>'
    return f'<nav class="breadcrumbs" aria-label="{l["breadcrumb"]}">{trail}</nav>'

def article_page(article,lang):
    a=article[lang];l=LABELS[lang]
    sections=[(f'section-{i+1}',s['title'],s['html']) for i,s in enumerate(a['sections'])]
    toc=''.join(f'<li><a href="#{id}">{esc(title)}</a></li>' for id,title,_ in sections)
    toc+=f'<li><a href="#questions">{l["faq"]}</a></li><li><a href="#sources">{l["sources"]}</a></li>'
    tag=f'<span class="kn-example">{l["example"]}</span><blockquote>'
    prose=''.join(f'<section id="{id}"><h2>{esc(title)}</h2>{body.replace("<blockquote>", tag)}</section>' for id,title,body in sections)
    faq=''.join(f'<details><summary>{esc(f["question"])}</summary><p>{esc(f["answer"])}</p></details>' for f in a['faq'])
    sources=''.join(f'<li><a href="{esc(s["url"])}">{esc(s[lang])}</a></li>' for s in article['sources'])
    related=''.join(f'<li><a href="{route(lang,s)}">{esc(BY_SLUG[s][lang]["title"])}</a></li>' for s in article['related'])
    body=f'''<main id="main" class="kn kn-article"><div class="article-shell">{breadcrumbs(lang)}
<header class="article-header"><p class="kn-kind">{l[article['kind'].replace('-','_')]}</p><h1>{esc(a['title'])}</h1><p class="byline">{l['by']} · <time datetime="{DATE}">{l['date']}</time></p><p class="answer">{esc(a['answer'])}</p></header>
<div class="article-layout"><aside class="contents"><details open><summary>{l['contents']}</summary><nav aria-label="{l['contents']}"><ol>{toc}</ol></nav></details></aside><article class="prose" aria-label="{esc(a['title'])}">{prose}<section id="questions"><h2>{l['faq']}</h2>{faq}</section><section id="sources" class="sources"><h2>{l['sources']}</h2><ul>{sources}</ul><p class="small">{l['rights']}</p><p class="small"><a href="{route(lang)}#editorial">{l['editorial']}</a></p></section>{product(lang, 'article')}<section class="related"><h2>{l['related']}</h2><ul>{related}</ul></section></article></div></div></main>'''
    return layout(lang,body,article)

def hub_stage(lang):
    """Product + soft 3D composition (tools/data/guides-hero.<lang>.html, built with the site's pd.css)."""
    snippet = (ROOT / f'tools/data/guides-hero.{lang}.html').read_text().strip()
    return f'<div class="fxp-hero-art fxp-hero-art--below">{snippet}</div>'


def hub_page(lang):
    l=LABELS[lang];sections='';jump=''
    arrow='<span class="read-link" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-6-6 6 6-6 6"/></svg></span>'
    for gid,slugs,copy in GROUPS:
        title,lead,count=copy[lang]
        rows=''
        for slug in slugs:
            a=BY_SLUG[slug]
            kind='' if a['kind']=='guide' else f'<span class="kn-kind">{l[a["kind"].replace("-","_")]}</span>'
            rows+=f'<li><div>{kind}<h3><a href="{route(lang,slug)}">{esc(a[lang]["title"])}</a></h3><p>{esc(a[lang]["description"])}</p></div>{arrow}</li>'
        sections+=f'<section class="topic-group" id="{gid}" aria-labelledby="{gid}-title"><div class="topic-head"><h2 id="{gid}-title">{title}</h2><p>{lead}</p></div><ul class="topic-list">{rows}</ul></section>'
        icon=f'<svg class="kn-ico" aria-hidden="true"><use href="/assets/img/icons/estavo-home.svg#{GROUP_ICONS[gid]}"/></svg>'
        jump+=f'<a href="#{gid}">{icon}<b>{title}</b><small class="hub-jump__count">{count}</small><small class="hub-jump__lead">{lead}</small></a>'
    related=''.join(f'<a href="{href}"><b>{name}</b><small>{sub}</small></a>' for href,name,sub in RELATED[lang])
    body=f'''<main id="main" class="kn kn-hub"><header class="hub-header"><div class="hub-shell">{breadcrumbs(lang, 'hub')}<div class="hub-hero"><div class="hub-intro"><p class="kn-eyebrow">{l['eyebrow']}</p><h1>{l['hub']}</h1><p>{l['hub_intro']}</p></div><nav class="hub-jump" aria-label="{l['jump']}">{jump}</nav></div>{hub_stage(lang)}</div></header><div class="hub-shell">{sections}<section id="editorial" class="editorial"><h2>{l['editorial_title']}</h2><p>{l['editorial_body']} <a href="mailto:support@estavo.space">support@estavo.space</a>.</p><p><a href="/guides/evidence/september-2026.json">{l['summary']}</a></p></section><nav class="kn-more" aria-labelledby="kn-more-title"><h2 class="kn-more__title" id="kn-more-title">{l['more']}</h2><div class="kn-related">{related}</div></nav>{product(lang, 'hub')}</div></main>'''
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
