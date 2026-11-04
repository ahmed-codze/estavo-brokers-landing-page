'use strict';
const { JSDOM } = require('jsdom');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { MEDIA } = require('./schema');
const ROOT = path.resolve(__dirname, '../..');
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels = {
  ar: { units:'من وحدات إستاڤو', projects:'مشاريع من إستاڤو', developers:'من دليل المطورين', news:'جديد السوق', launches:'إطلاقات منشورة', jobs:'وظائف القطاع العقاري', games:'إكسكلوسيف', edition:'مختارات إستاڤو', from:'يبدأ من', money:'ج.م', area:'م²', open:'شوف التفاصيل على إستاڤو', empty:'مفيش محتوى متاح في المختارات دي.', check:'افتح إستاڤو عشان تراجع آخر التفاصيل.', note:'مختارات بتاريخها، مش قائمة كاملة. راجع السعر والتوافر جوه إستاڤو.', recent:'أحدث تحديث', popular:'رائج ضمن المختارات', daily_rotation:'اختيار اليوم', sample:'مثال توضيحي لطريقة الاستخدام', challenge:'جرب السؤال مع زمايلك', source:'المصدر', date:'نسخة', pending:'المختارات بتتجهز. تقدر تدخل على إستاڤو مباشرة.' },
  en: { units:'From Estavo inventory', projects:'Projects on Estavo', developers:'From the developer directory', news:'Market news', launches:'Published launches', jobs:'Real-estate jobs', games:'Exclusive', edition:'Estavo selections', from:'From', money:'EGP', area:'m²', open:'View details on Estavo', empty:'No items available in this selection.', check:'Open Estavo to check the latest details.', note:'A dated selection, not the full catalogue. Check prices and availability in Estavo.', recent:'Recently updated', popular:'Popular in this selection', daily_rotation:'Daily pick', sample:'Example workflow', challenge:'Try this question with your team', source:'Source', date:'Edition', pending:'Selections are being prepared. You can open Estavo directly.' },
};
function renderer(data, lang) {
  const L = labels[lang], ar = lang === 'ar';
  const tr = o => typeof o === 'string' ? o : o?.[lang] || o?.[ar ? 'en' : 'ar'] || '';
  const date = d => String(d || data.snapshot_date).slice(0,10);
  const localImage = url => { const m = MEDIA.exec(url || ''); return m ? `/assets/daily/${m[1]}.webp` : null; };
  const picture = (url, name, logo = false) => localImage(url) ? `<img class="daily-${logo ? 'logo' : 'photo'}" src="${localImage(url)}" width="${logo ? 160 : 560}" height="${logo ? 160 : 360}" alt="" loading="lazy" decoding="async">` : `<span class="daily-monogram" aria-hidden="true">${esc([...tr(name)].slice(0,2).join(''))}</span>`;
  const reason = r => L[r.selection] || '';
  const cursors = {};
  function cards(kind, {links = false, max = 3, compact = false, offset = 0} = {}) {
    const eligible = data[kind].filter(r => kind !== 'jobs' || !r.valid_through || new Date(r.valid_through) > new Date());
    const start = offset % (eligible.length || 1);
    const rows = [...eligible.slice(start), ...eligible.slice(0,start)].slice(0,max);
    if (!rows.length) return `<div class="daily-empty"><span class="daily-empty__icon" aria-hidden="true">◎</span><b>${esc(L.empty)}</b><p>${esc(L.check)}</p></div>`;
    return rows.map((r) => {
      let title, body = '', media = '', meta = reason(r);
      if (kind === 'units') {
        const p = data.projects.find(p => p.key === r.project_key);
        title = tr(r.project); media = picture(p?.image, r.project);
        body = `<p><bdi>${esc(tr(r.type))}</bdi>${r.area_sqm ? ` · <bdi>${esc(r.area_sqm)} ${L.area}</bdi>` : ''}</p><strong class="daily-price">${L.from} <bdi>${new Intl.NumberFormat('en-US', {maximumFractionDigits:0}).format(r.price_from)} ${L.money}</bdi></strong>`;
      } else if (kind === 'projects') { title=tr(r.name); media=picture(r.image,r.name); body=`<p><bdi>${esc(tr(r.developer))}</bdi> · <bdi>${esc(tr(r.city))}</bdi></p>`; }
      else if (kind === 'developers') { title=tr(r.name); media=picture(r.logo,r.name,true); }
      else if (kind === 'news') { title=tr(r.title); meta=date(r.published_at); body=`<p><bdi>${esc(tr(r.summary))}</bdi></p><small>${esc(L.source)}: ${r.sources.map(s => links ? `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer"><bdi>${esc(s.name)}</bdi></a>` : `<bdi>${esc(s.name)}</bdi>`).join(' · ')}</small>`; }
      else if (kind === 'launches') { title=tr(r.title); meta=date(r.published_at); body=`<p><bdi>${esc(tr(r.project))}</bdi></p>`; }
      else if (kind === 'jobs') { title=r.title; meta=date(r.published_at); body=`<p><bdi>${esc(r.company)}</bdi></p><small><bdi>${esc(r.location)}</bdi> · <bdi>${esc(r.employment_type)}</bdi></small>`; }
      else { title=tr(r.name); meta=L.challenge; body=`<p class="daily-question" lang="ar" dir="rtl">${esc(r.prompt)}</p>`; }
      return `<article class="daily-card daily-card--${kind}${compact?' daily-card--compact':''}">${media}<div class="daily-card__body"><small class="daily-tag">${esc(meta)}</small><b class="daily-card__title"><bdi>${esc(title)}</bdi></b>${body}${links ? `<a class="daily-open" data-keep-path data-track="daily_content_opened" data-position="daily_${kind}" href="${esc(r.href)}">${L.open} <span aria-hidden="true">↗</span></a>` : ''}</div></article>`;
    }).join('');
  }
  function screen(kind, phone = false) {
    const offset = cursors[kind] || 0; cursors[kind] = offset + 1;
    return `<div class="daily-screen${phone?' daily-screen--phone':''}" data-daily-kind="${kind}" dir="${ar?'rtl':'ltr'}"><div class="daily-screen__head"><img class="daily-brand" src="/assets/logo/estavo-mark-white-128.webp" width="128" height="128" alt="" decoding="async"><div><b>${L[kind]}</b><small>${L.date} <bdi>${data.snapshot_date}</bdi></small></div><span class="daily-status" aria-hidden="true"></span></div><div class="daily-screen__cards">${cards(kind,{max:phone?1:kind==='developers'?4:2,compact:true,offset})}</div><p class="daily-screen__foot">${kind==='units'?L.note:L.check}</p></div>`;
  }
  function shelf(kind) {
    return `<aside class="daily-edition" data-daily-edition="${data.snapshot_date}" aria-label="${L.edition}"><div class="daily-edition__head"><b>${L.edition}</b>${/^\d{4}-\d{2}-\d{2}$/.test(data.snapshot_date) ? `<time datetime="${data.snapshot_date}">${data.snapshot_date}</time>` : `<span>${L.pending}</span>`}</div><div class="daily-edition__cards">${cards(kind,{links:true,max:kind==='developers'?3:1})}</div><p class="daily-edition__note">${L.note}</p></aside>`;
  }
  return {cards,screen,shelf,L};
}
function applyDaily(html, route, lang, data) {
  const dom = new JSDOM(html, {includeNodeLocations:true});
  const doc = dom.window.document, edits = [], touched = [];
  const primary = ({developers:'developers', insights:'news', jobs:'jobs', challenges:'games'})[route] || 'units';
  const { cards, screen, shelf, L } = renderer(data,lang);
  const replace = (el, value, inner=false) => {
    const loc = dom.nodeLocation(el); if (!loc) return;
    const start = inner ? loc.startTag.endOffset : loc.startOffset, end = inner ? loc.endTag?.startOffset : loc.endOffset;
    if (end == null || touched.some(([a,b]) => start < b && end > a)) return;
    touched.push([start,end]); edits.push({start,end,value});
  };
  // Native product scenes: all names, logos, cards and prices share one edition.
  doc.querySelectorAll('.pd-win, .pd-phone, .pd-doc').forEach(el => {
    if (el.querySelector('.pd-code')) return; // API syntax is documentation, not a data sample.
    const src = el.querySelector('img')?.getAttribute('src') || '';
    // Workflow diagrams contain calculated plans, fictional client actions and
    // generated answers. Never attribute those claims to a real selected unit.
    if (/chat-|pdf-|step-|estavo-(ai-conversation|meta-signals|client-context|brand-unified|listings-reach)/.test(src)) {
      replace(el, el.innerHTML + `<span class="daily-illustrative">${L.sample}</span>`, true);
      return;
    }
    let kind = primary;
    if (!['developers','jobs','challenges','insights'].includes(route)) {
      if (/daily-|change-/.test(src)) kind='news';
      else if (/record-/.test(src)) kind='projects';
    }
    const bar = el.querySelector('.pd-win__bar')?.outerHTML || '';
    replace(el, bar + screen(kind,el.classList.contains('pd-phone') || el.classList.contains('pd-doc')),true);
  });
  doc.querySelectorAll('.pd-code').forEach(el => replace(el, `<bdi dir="ltr">${el.innerHTML}</bdi>`,true));
  doc.querySelectorAll('.pd-chip').forEach(el => {
    if (route === 'challenges') return; // Verified game rules, not sample records.
    replace(el, `${L.edition}<small><bdi>${data.snapshot_date}</bdi></small>`,true);
  });
  // The accessible card beside the hero mirrors the decorative product scene.
  const heroCopy = doc.querySelector('.es-home-hero__copy, .jb-hero__copy, .es-hero__copy, .fxp-hero-copy, .mk-hero .mk-wrap > div, .service-hero .es-container > div');
  const mainHero = doc.querySelector('main section');
  const anchor = heroCopy || mainHero?.querySelector('h1')?.parentElement;
  if (anchor) {
    const loc = dom.nodeLocation(anchor);
    edits.push({start:loc.endTag.startOffset,end:loc.endTag.startOffset,value:shelf(primary)});
  }
  // Every homepage destination gets its matching daily data, including logos.
  const destKinds = ['units','units','developers','news','jobs','games','units'];
  doc.querySelectorAll('#home-destinations .dest-cover').forEach((el,i) => {
    const orb = el.querySelector('.fxp-dest-orb')?.outerHTML || '';
    replace(el, `<div class="dest-cover daily-destination" aria-hidden="true">${screen(destKinds[i]||'units')}${orb}</div>`);
  });
  const board = doc.querySelector('.es-home-today__grid');
  if (board) {
    const kinds=['news','launches','jobs','games'];
    replace(board, kinds.map(kind => `<div class="daily-board-group"><h3>${L[kind]}</h3>${cards(kind,{links:true,max:2}).replaceAll('data-track="daily_content_opened"','data-track="daily_content_opened" data-home-event="home_today_click"')}</div>`).join(''),true);
  }
  doc.querySelectorAll('.es-home-today__head .es-home-example').forEach(el => replace(el,`${L.edition} · ${data.snapshot_date}`,true));
  doc.querySelectorAll('.today-more, label[for="today-more"]').forEach(el => replace(el,''));
  // Detailed community cards must not imply fictitious vacancies or launches.
  doc.querySelectorAll('.ns-cards').forEach(el => replace(el, `<div class="daily-detail-grid" data-daily-kind="launches">${cards('launches',{links:true})}</div>`));
  doc.querySelectorAll('.ns-anat').forEach(el => replace(el, `<figure class="daily-detail-grid" data-daily-kind="news">${cards('news',{links:true,max:1})}<figcaption>${L.check}</figcaption></figure>`));
  doc.querySelectorAll('.dv-mini').forEach(el => replace(el, screen('developers'),true));
  // Caption any untouched educational diagrams explicitly; their arithmetic and
  // invented buyer identities must not be attached to live developer inventory.
  doc.querySelectorAll('figure.fxp-sec-art .pd-ex').forEach(el => replace(el,`${L.sample} · ${L.edition} ${data.snapshot_date}`,true));
  const css = fs.readFileSync(path.join(ROOT,'assets/css/daily-content.css'));
  const version = crypto.createHash('sha256').update(css).digest('hex').slice(0,10);
  const headEnd = html.indexOf('</head>');
  edits.push({start:headEnd,end:headEnd,value:`<link rel="stylesheet" href="/assets/css/daily-content.css?v=${version}">\n<meta name="estavo-content-date" content="${data.snapshot_date}">\n`});
  for (const e of edits.sort((a,b)=>b.start-a.start)) html=html.slice(0,e.start)+e.value+html.slice(e.end);
  dom.window.close();
  return html.replace(/[ \t]+\n/g, '\n').replace(/(src|href)="\/assets\//g, `$1="${route==='home'?'':'../'}assets/`);
}
module.exports={applyDaily,renderer,esc};
