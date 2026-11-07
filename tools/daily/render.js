'use strict';
// Daily bindings for the home page. Only text (and, when the edition has one,
// a local thumbnail) inside the approved cards changes; no element is added,
// removed or restyled. A slot without fresh data keeps its authored example.
// Binding happens only when the daily publisher passes LANDING_CACHE_DIR, so a
// plain `npm run build` keeps producing the approved static pages.
const path = require('path');
const { read } = require('./cache');
const { MEDIA } = require('./schema');

const MARK = '<meta name="estavo-content-mode" content="approved-examples">';
const MONTHS = {
  ar: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'],
  en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
};
const T = {
  ar: { data: 'بيانات إستاڤو', units: 'تحديثات الوحدات', unitsSub: 'نماذج وحدات من إستاڤو', from: 'يبدأ من', sqm: 'م²', area: 'المساحة', rooms: 'الغرف', handover: 'الاستلام', news: 'أخبار', newsType: 'جديد السوق · أخبار', launchType: 'إطلاق جديد', launchSum: p => `${p} · التفاصيل على صفحة الإطلاق جوه إستاڤو`, jobType: 'وظيفة مفتوحة', apply: 'التقديم على الإعلان الأصلي', today: 'النهارده', yesterday: 'امبارح', daysAgo: n => `من ${n} أيام`, full_time: 'دوام كامل', part_time: 'دوام جزئي', contract: 'عقد', internship: 'تدريب' },
  en: { data: 'Estavo data', units: 'Unit updates', unitsSub: 'Unit types from Estavo', from: 'from', sqm: 'm²', area: 'Area', rooms: 'Beds', handover: 'Handover', news: 'News', newsType: 'Market news', launchType: 'New launch', launchSum: p => `${p} · details on the launch page in Estavo`, jobType: 'Open job', apply: 'apply on the original listing', today: 'Today', yesterday: 'Yesterday', daysAgo: n => `${n} days ago`, full_time: 'Full time', part_time: 'Part time', contract: 'Contract', internship: 'Internship' },
};

function edition() {
  const dir = process.env.LANDING_CACHE_DIR;
  return dir ? read(path.resolve(dir)) : null;
}
const tr = (v, lang) => (v && typeof v === 'object' ? v[lang] || v.en || v.ar : v) || '';
const price = n => (n >= 1e6 ? (Math.round(n / 1e4) / 100).toString() + 'M' : Math.round(n / 1e3) + 'K');
const area = n => String(Math.round(n));
const place = s => String(s).replace(/,\s*Egypt$/i, '');
const clip = (s, max) => { s = String(s).replace(/\s+/g, ' ').trim(); if (s.length <= max) return s; const cut = s.slice(0, max); return cut.slice(0, Math.max(cut.lastIndexOf(' '), max * 0.6)).replace(/[،,.:;\s]+$/, '') + '…'; };
const latin = s => /^[\x20-\x7e]+$/.test(s);
function dayDiff(snapshot, iso) {
  const a = Date.parse(snapshot + 'T12:00:00Z');
  const b = Date.parse(new Intl.DateTimeFormat('en-CA', { timeZone: 'Africa/Cairo' }).format(new Date(iso)) + 'T12:00:00Z');
  return Math.max(0, Math.round((a - b) / 86400000));
}

function bind(html, lang, d) {
  const { JSDOM } = require('jsdom');
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  const t = T[lang];
  const q = (sel, root = doc) => root.querySelector(sel);
  const qa = (sel, root = doc) => [...root.querySelectorAll(sel)];
  // Writes text; Latin-only strings on the Arabic page stay isolated in <bdi>.
  const put = (el, text, isolate = lang === 'ar' && latin(text)) => {
    if (!el) return;
    el.textContent = '';
    if (isolate) { const b = doc.createElement('bdi'); b.textContent = text; el.appendChild(b); } else el.textContent = text;
  };
  const ltr = (el, text) => { if (!el) return; el.textContent = ''; const b = doc.createElement('bdi'); b.setAttribute('dir', 'ltr'); b.textContent = text; el.appendChild(b); };
  const [y, m, dd] = d.snapshot_date.split('-').map(Number);
  const month = `${t.data} · ${MONTHS[lang][m - 1]} ${y}`;
  const dayLabel = `${t.data} · ${dd} ${MONTHS[lang][m - 1]} ${y}`;
  const touched = new Set();

  // Market card: three real unit types with their real price, area and handover.
  const inv = q('.dc--inv');
  const rows = inv ? qa('.mk-row', inv) : [];
  if (inv && d.units.length >= rows.length && rows.length) {
    put(q('.dc-inv__head b', inv), t.units, false);
    put(q('.dc-inv__head small', inv), t.unitsSub, false);
    rows.forEach((row, i) => {
      const u = d.units[i];
      put(q('b', row), `${tr(u.type, lang)} · ${tr(u.project, lang)}`, false);
      const small = q('small', row); small.textContent = ''; const b = doc.createElement('bdi'); b.setAttribute('dir', 'ltr'); b.textContent = area(u.area_sqm); small.append(b, ' ' + t.sqm);
      ltr(q('strong', row), price(u.price_from));
      put(q('em', row), t.from, false);
    });
    const on = rows.findIndex(r => r.classList.contains('is-on'));
    const u = d.units[on < 0 ? 0 : on];
    const cells = qa('.dc-plan > span:not(.dc-plan__bars)', inv);
    if (cells.length === 3) {
      const facts = [[t.area, area(u.area_sqm) + ' ' + t.sqm], [t.rooms, u.bedrooms ? String(u.bedrooms) : '—'], [t.handover, u.delivery ? u.delivery.slice(0, 4) : '—']];
      cells.forEach((c, i) => { put(q('small', c), facts[i][0], false); ltr(q('b', c), facts[i][1]); });
    }
    const project = d.projects.find(p => p.key === u.project_key);
    const thumb = q('.dc-thumb', inv);
    if (thumb && project?.image) { thumb.setAttribute('src', 'assets/daily/' + MEDIA.exec(project.image)[1] + '.webp'); thumb.setAttribute('width', '560'); thumb.setAttribute('height', '360'); }
    touched.add(inv);
  }

  // Developers card: only developers that have a logo, so a name never sits under someone else's logo.
  const devs = q('.dc--devs');
  const withLogo = d.developers.filter(x => x.logo);
  if (devs && withLogo.length) {
    qa('.dv-logo', devs).forEach((slot, i) => {
      const dev = withLogo[i]; if (!dev) return;
      const img = q('img', slot); img.setAttribute('src', 'assets/daily/' + MEDIA.exec(dev.logo)[1] + '.webp');
      put(q('small', slot), tr(dev.name, lang));
      if (slot.classList.contains('is-on')) put(q('.dv-sel b', devs), tr(dev.name, lang));
    });
    touched.add(devs);
  }

  // News card: launch names in the ticker, the latest headlines in the rows.
  const feed = q('.dc--newsfeed');
  if (feed) {
    const ticker = qa('.nw-ticker > span', feed).slice(1);
    ticker.forEach((s, i) => { if (d.launches[i]) put(s, tr(d.launches[i].project, lang)); });
    qa('.nw-row', feed).forEach((row, i) => {
      const n = d.news[i]; if (!n) return;
      const em = q('em', row); put(em, t.news, false); em.className = 't-price';
      put(q('b', row), clip(tr(n.title, lang), lang === 'ar' ? 62 : 70));
    });
    if (d.news.length || d.launches.length) touched.add(feed);
  }

  // Jobs card.
  const board = q('.dc--board');
  if (board) {
    qa('.jb-row', board).forEach((row, i) => {
      const j = d.jobs[i]; if (!j) return;
      put(q('i', row), (j.company.trim()[0] || 'S').toUpperCase(), false);
      put(q('b', row), j.title, true);
      put(q('small', row), `${place(j.location)} · ${t[j.employment_type] || j.employment_type.replace(/_/g, ' ')}`);
      const ago = dayDiff(d.snapshot_date, j.published_at);
      put(q('em', row), ago === 0 ? t.today : ago === 1 ? t.yesterday : t.daysAgo(ago), false);
    });
    if (d.jobs.length) touched.add(board);
  }

  // Dated label on every card that now carries this edition.
  for (const card of touched) { const ex = q('.dc-ex', card.closest('.dest-cover')); if (ex) ex.textContent = month; }

  // "From inside Estavo" stories: two news, two launches, two jobs.
  const stories = { news: qa('.es-home-story--news'), launch: qa('.es-home-story--launch'), jobs: qa('.es-home-story--jobs') };
  const setType = (story, text) => { const p = q('.es-home-story__type', story); const icon = q('svg', p); p.textContent = ''; if (icon) p.appendChild(icon); p.append(text); };
  stories.news.forEach((s, i) => {
    const n = d.news[i]; if (!n) return;
    setType(s, t.newsType);
    put(q('.es-home-story__title', s), tr(n.title, lang));
    put(q('.es-home-story__sum', s), clip(tr(n.summary, lang), lang === 'ar' ? 80 : 90));
  });
  stories.launch.forEach((s, i) => {
    const l = d.launches[i]; if (!l) return;
    setType(s, t.launchType);
    put(q('.es-home-story__title', s), tr(l.title, lang));
    put(q('.es-home-story__sum', s), t.launchSum(tr(l.project, lang)));
  });
  stories.jobs.forEach((s, i) => {
    const j = d.jobs[i]; if (!j) return;
    setType(s, `${t.jobType} · ${place(j.location)}`);
    const h = q('.es-home-story__title', s); h.textContent = '';
    for (const [k, part] of [j.title, j.company].entries()) { if (k) h.append(' · '); const b = doc.createElement('bdi'); b.textContent = part; h.appendChild(b); }
    put(q('.es-home-story__sum', s), `${t[j.employment_type] || j.employment_type.replace(/_/g, ' ')} · ${t.apply}`, false);
  });
  const head = q('.es-home-today__head .es-home-example');
  if (head && (d.news.length || d.launches.length || d.jobs.length)) head.textContent = dayLabel;

  let out = dom.serialize();
  dom.window.close();
  out = out.replace('</head>', `<meta name="estavo-daily-edition" content="${d.snapshot_date}">\n</head>`);
  return out;
}

function applyDaily(html, key, lang, data) {
  let out = html;
  const d = data === undefined ? (key === 'home' ? edition() : null) : data;
  if (key === 'home' && d && (lang === 'ar' || lang === 'en')) out = bind(out, lang, d);
  return out.replace(/[ \t]+\n/g, '\n').replace('</head>', MARK + '\n</head>');
}
module.exports = { applyDaily };
