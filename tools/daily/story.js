'use strict';
// Turns the edition's three real showcase units (one bedroom count) into the illustration story
// used by tools/build-market-art.py (and the HTML scenes). Every claim is
// derived from the data: the client's budget sits between the two cheaper
// units and the dearest one, so "2 matches + 1 alternative" holds; the best
// fit is the match with the lowest real down payment. Returns null when the
// edition cannot support a true story, and the approved example art stays.

const MONTHS = {
  ar: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'],
  en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
};
const FINISH = {
  fully_finished: ['تشطيب كامل', 'كامل', 'Fully finished', 'Full'],
  fully_finished_with_ac: ['تشطيب كامل', 'كامل', 'Fully finished', 'Full'],
  fully_finished_with_kitchen_cabinets: ['تشطيب كامل', 'كامل', 'Fully finished', 'Full'],
  fully_finished_with_ac_and_kitchen_cabinets: ['تشطيب كامل', 'كامل', 'Fully finished', 'Full'],
  semi_finished: ['نص تشطيب', 'نص تشطيب', 'Semi-finished', 'Semi'],
  core_and_shell: ['على المحارة', 'محارة', 'Core & shell', 'Core & shell'],
  not_finished: ['بدون تشطيب', 'بدون', 'Unfinished', 'None'],
  fully_furnished: ['مفروش', 'مفروش', 'Furnished', 'Furnished'],
  fully_furnished_with_ac: ['مفروش', 'مفروش', 'Furnished', 'Furnished'],
  flexi: ['فليكسي', 'فليكسي', 'Flexi', 'Flexi'],
};

// 7,990,000 -> "8.0M"; 480,000 -> "480K"; 1,446,000 -> "1.4M"
function money(v) {
  if (v >= 1e6) return (Math.round(v / 1e5) / 10).toFixed(1) + 'M';
  return Math.round(v / 1e4) * 10 + 'K';
}
const years = m => (m % 12 === 0 ? m / 12 : Math.round(m / 6) / 2);
const ar = { yrs: n => `${n} سنين`, upTo: n => `حتى ${n} سنين` };
const en = { yrs: n => `${n} yrs`, years: n => `${n} years` };

function buildStory(edition) {
  const rows = edition && Array.isArray(edition.showcase) ? edition.showcase : [];
  if (rows.length !== 3 || rows.some(r => !r.project?.ar || !r.project?.en)) return null;
  const s = [...rows].sort((a, b) => a.price_from - b.price_from);
  // Budget: the second price rounded up to 100K, strictly below the third.
  let budget = Math.ceil(s[1].price_from / 1e5) * 1e5;
  if (s[2].price_from <= budget) budget = s[1].price_from;
  if (s[2].price_from <= budget) return null;
  const [B, A] = s[0].down_payment <= s[1].down_payment ? [s[0], s[1]] : [s[1], s[0]];
  const C = s[2];
  if (A.down_payment === B.down_payment) return null; // "lower than A" must be true
  const cap = Math.ceil(Math.max(A.down_payment, B.down_payment) / 1e5) * 1e5;
  const over = money(C.price_from - budget);
  const diff = money(A.down_payment - B.down_payment);
  const [y, m, d] = edition.snapshot_date.split('-').map(Number);

  const per = u => {
    const f = FINISH[u.finishing] || null;
    const hand = { ar: u.ready ? 'فوري' : u.delivery ? u.delivery.slice(0, 4) : '—', en: u.ready ? 'Ready' : u.delivery ? u.delivery.slice(0, 4) : '—' };
    return {
      name: { ar: u.project.ar, en: u.project.en }, mono: { ar: [...u.project.ar.trim()][0], en: [...u.project.en.trim()][0].toUpperCase() },
      price: money(u.price_from), down: money(u.down_payment), yrs: years(u.installment_months), hand,
      area: String(Math.round(u.area_sqm)),
      finish: f ? { ar: f[0], arShort: f[1], en: f[2], enShort: f[3] } : { ar: '—', arShort: '—', en: '—', enShort: '—' },
    };
  };
  const b = per(B), a = per(A), c = per(C);
  // All three share one bedroom count (the client asked for "N rooms").
  const n = B.bedrooms;
  if (!rows.every(r => r.bedrooms === n) || n < 1 || n > 9) return null;
  const roomsAr = n === 1 ? 'غرفة' : n === 2 ? 'غرفتين' : `${n} غرف`;
  const flatAr = `شقة ${roomsAr}`;
  const bedEn = `${n}-bed`, bedroomEn = `${n}-bedroom`, bedroomsEn = n === 1 ? '1 bedroom' : `${n} bedrooms`;
  const city = { ar: B.city.ar, en: B.city.en };
  const latestHand = Math.max(...[B, A].map(u => (u.delivery ? Number(u.delivery.slice(0, 4)) : 0)));
  const want = latestHand ? latestHand + 1 : null;
  const L = edition.launches || [], N = edition.news || [];
  const launch = L[0] || null;
  const launchDate = launch ? new Date(launch.published_at) : null;
  const dateIn = (lang, dt) => `${dt.getUTCDate()} ${MONTHS[lang][dt.getUTCMonth()]}`;
  const headlines = lang => {
    const out = [];
    if (L[0]) out.push([lang === 'ar' ? 'إطلاق' : 'Launch', L[0].title[lang]]);
    for (const n of N) if (out.length < 3) out.push([lang === 'ar' ? 'أخبار' : 'News', n.title[lang]]);
    if (out.length < 3 && L[1]) out.push([lang === 'ar' ? 'إطلاق' : 'Launch', L[1].title[lang]]);
    return out;
  };
  const dailyItems = lang => {
    // Row icons follow the template: launch, update, project, investment.
    const out = [];
    const cat = lang === 'ar' ? { l: 'الإطلاقات', n: 'جديد السوق' } : { l: 'Launches', n: 'Market news' };
    if (L[0]) out.push([lang === 'ar' ? 'إطلاق' : 'Launch', L[0].title[lang], cat.l]);
    for (const n of N) if (out.length < 4) out.push([lang === 'ar' ? 'أخبار' : 'News', n.title[lang], cat.n]);
    for (const l of L.slice(1)) if (out.length < 4) out.push([lang === 'ar' ? 'إطلاق' : 'Launch', l.title[lang], cat.l]);
    return out;
  };

  const story = {
    data_label: { ar: `بيانات إستاڤو · ${d} ${MONTHS.ar[m - 1]}`, en: `Estavo data · ${MONTHS.en[m - 1]} ${d}` },
    story: { years: { B: b.yrs, A: a.yrs, C: c.yrs }, area: { B: b.area, A: a.area, C: c.area } },
    photos: { 'project-b': B.image, 'project-a': A.image, 'project-c': C.image },
    ar: {
      news: headlines('ar'), daily_items: dailyItems('ar'),
      ...(launch ? { launch_badge: 'إطلاق جديد', launch_name: launch.project.ar, launch_meta: `اتعلن ${dateIn('ar', launchDate)}` } : {}),
      // The before/after tile has no real plan history behind it: stays an example.
      upd_sub: 'مثال · خطة السداد',
      calc_b: `تقسيط ${ar.yrs(b.yrs)}`,
      city: city.ar, unit_chip: flatAr, inst_short: ar.yrs(b.yrs),
      alt_short: `بديل · +${over}`, pills: [city.ar, 'سكني'],
      phase: `${B.developer.ar} · استلام ${b.hand.ar}`,
      ud_rows: [['نوع الوحدة', /شقة/.test(B.type.ar) || !B.type.ar ? flatAr : B.type.ar], ['السعر', b.price], ['المساحة', `${b.area} م²`], ['الغرف', String(n)],
        ['التشطيب', b.finish.arShort], ['المشروع', b.name.ar], ['الاستلام', b.hand.ar]],
      search: `${flatAr} في ${city.ar} لحد ${money(budget)}، والأهم أقل مقدم`,
      search_m: `${flatAr} في ${city.ar}، أقل مقدم`,
      chips: [city.ar, roomsAr, `حتى ${money(budget)}`, `مقدم حتى ${money(cap)}`],
      units: {
        B: [b.mono.ar, b.name.ar, `${b.area} م² · ${b.finish.ar}`, b.price, b.down, ar.yrs(b.yrs), b.hand.ar],
        A: [a.mono.ar, a.name.ar, `${a.area} م² · ${a.finish.ar}`, a.price, a.down, ar.yrs(a.yrs), a.hand.ar],
        C: [c.mono.ar, c.name.ar, `${c.area} م² · ${c.finish.ar}`, c.price, c.down, ar.yrs(c.yrs), c.hand.ar],
      },
      over: `بديل · فوق الميزانية بـ${over}`,
      ai: `${b.name.ar} أقل مقدم داخل الميزانية: ${b.down}، أقل من ${a.name.ar} بـ${diff}.`,
      pdf_t: `عرض ${b.name.ar}`,
      rec_title: b.name.ar, rec_sub: `${city.ar} · سكني`,
      fields: [['price', 'السعر', b.price], ['down-payment', 'المقدم', b.down], ['payment-period', 'خطة السداد', ar.yrs(b.yrs)],
        ['delivery', 'الاستلام', b.hand.ar], ['area', 'المساحة', `${b.area} م²`], ['finishing', 'التشطيب', b.finish.arShort]],
      msg: `عايز ${flatAr} في ${city.ar} لحد ${money(budget)}، والأهم المقدم يكون أقل حاجة، مش أكتر من ${money(cap)}.`,
      crit: [['المنطقة', city.ar, ''], ['الغرف', String(n), ''], ['السعر', `حتى ${money(budget)}`, ''], ['المقدم', `حتى ${money(cap)}`, '']],
      res: [['B', `مقدم ${b.down} · ${ar.yrs(b.yrs)} · ${b.hand.ar}`, 'أنسب لأولويته', 'best'],
        ['A', `مقدم ${a.down} · ${ar.yrs(a.yrs)} · ${a.hand.ar}`, 'مطابق', 'plain'],
        ['C', `مقدم ${c.down} · ${ar.yrs(c.yrs)} · ${c.hand.ar}`, `بديل · +${over}`, 'over']],
      file_t: `عرض ${b.name.ar}`,
      draft: `أهلًا، ده عرض ${b.name.ar} في ${city.ar}: مقدم ${b.down} وسداد على ${ar.yrs(b.yrs)} واستلام ${b.hand.ar}. ولو تحب نقارنه بـ${a.name.ar}، أبعتلك الفرق.`,
      me1: `عايز ${n} bedrooms في ${city.ar}، لحد ${money(budget)} وأقل مقدم.`,
      ai1: [['لقيت 2 مطابقين وبديل. الأنسب لأولويته ', 400], [b.name.ar, 600], [`: مقدم ${b.down}، أقل من ${a.name.ar} بـ${diff}.`, 400]],
      rows: [[b.mono.ar, `مقدم ${b.down} · ${ar.yrs(b.yrs)} · ${b.hand.ar}`], [a.mono.ar, `مقدم ${a.down} · ${ar.yrs(a.yrs)} · ${a.hand.ar}`]],
      ...(want ? { me2: `والاستلام؟ العميل عايز قبل ${want}.` } : {}),
      ai2: `استلام ${b.name.ar} ${b.hand.ar}، و${a.name.ar} ${a.hand.ar}. و${c.name.ar} ${C.ready ? 'جاهز' : 'استلامه ' + c.hand.ar} بس فوق الميزانية بـ${over}.`,
      doc_k: `عرض وحدة · ${city.ar}`, doc_t: `${b.name.ar} · ${flatAr}`,
      doc_f: [['السعر', b.price], ['المقدم', b.down], ['السداد', ar.yrs(b.yrs)], ['الاستلام', b.hand.ar], ['المساحة', `${b.area} م²`], ['التشطيب', b.finish.arShort]],
      wa_t: `عرض ${b.name.ar}`,
    },
    en: {
      news: headlines('en'), daily_items: dailyItems('en'),
      ...(launch ? { launch_badge: 'New launch', launch_name: launch.project.en, launch_meta: `Announced ${dateIn('en', launchDate)}` } : {}),
      upd_sub: 'Example · payment plan',
      calc_b: `${b.yrs}-year installments`,
      city: city.en, inst_short: en.years(b.yrs),
      alt_short: `Alternative · +${over}`, pills: [city.en, 'Residential'],
      phase: `${B.developer.en} · Handover ${b.hand.en}`,
      ud_rows: [['Unit type', /apartment/i.test(B.type.en) || !B.type.en ? `${bedEn} apartment` : B.type.en], ['Price', b.price], ['Area', `${b.area} m²`], ['Bedrooms', String(n)],
        ['Finishing', b.finish.enShort], ['Project', b.name.en], ['Delivery', b.hand.en]],
      search: `${bedEn} in ${city.en} up to ${money(budget)}, lowest down payment`,
      search_m: `${bedEn}, ${city.en}, lowest down payment`,
      chips: [city.en, bedroomsEn, `Up to ${money(budget)}`, `Down up to ${money(cap)}`],
      units: {
        B: [b.mono.en, b.name.en, `${b.area} m² · ${b.finish.en}`, b.price, b.down, en.yrs(b.yrs), b.hand.en],
        A: [a.mono.en, a.name.en, `${a.area} m² · ${a.finish.en}`, a.price, a.down, en.yrs(a.yrs), a.hand.en],
        C: [c.mono.en, c.name.en, `${c.area} m² · ${c.finish.en}`, c.price, c.down, en.yrs(c.yrs), c.hand.en],
      },
      over: `Alternative · ${over} over budget`,
      ai: `${b.name.en} has the lowest down payment within budget: ${b.down}, ${diff} less than ${a.name.en}.`,
      pdf_t: `${b.name.en} offer`,
      rec_title: b.name.en, rec_sub: `${city.en} · Residential`,
      fields: [['price', 'Price', b.price], ['down-payment', 'Down payment', b.down], ['payment-period', 'Payment plan', en.years(b.yrs)],
        ['delivery', 'Handover', b.hand.en], ['area', 'Area', `${b.area} m²`], ['finishing', 'Finishing', b.finish.enShort]],
      msg: `I want a ${bedroomEn} apartment in ${city.en}, up to ${money(budget)}. The most important thing is the lowest down payment, no more than ${money(cap)}.`,
      crit: [['Area', city.en, ''], ['Bedrooms', String(n), ''], ['Price', `Up to ${money(budget)}`, ''], ['Down payment', `Up to ${money(cap)}`, '']],
      res: [['B', `${b.down} down · ${en.yrs(b.yrs)} · ${b.hand.en}`, 'Best fit', 'best'],
        ['A', `${a.down} down · ${en.yrs(a.yrs)} · ${a.hand.en}`, 'Match', 'plain'],
        ['C', `${c.down} down · ${en.yrs(c.yrs)} · ${c.hand.en}`, `Alternative · +${over}`, 'over']],
      file_t: `${b.name.en} offer`,
      draft: `Hi, here's the ${b.name.en} offer in ${city.en}: ${b.down} down, a ${b.yrs}-year plan and ${b.hand.en} handover. If you'd like it compared with ${a.name.en}, I'll send you the difference.`,
      me1: `${bedroomsEn} in ${city.en}, up to ${money(budget)}, lowest down payment.`,
      ai1: [['I found 2 matches and an alternative. The best fit for their priority is ', 400], [b.name.en, 600], [`: ${b.down} down, ${diff} less than ${a.name.en}.`, 400]],
      rows: [[b.mono.en, `${b.down} down · ${en.yrs(b.yrs)} · ${b.hand.en}`], [a.mono.en, `${a.down} down · ${en.yrs(a.yrs)} · ${a.hand.en}`]],
      ...(want ? { me2: `And handover? The client wants it before ${want}.` } : {}),
      ai2: `${b.name.en} hands over ${b.hand.en === 'Ready' ? 'now' : 'in ' + b.hand.en} and ${a.name.en} ${a.hand.en === 'Ready' ? 'now' : 'in ' + a.hand.en}. ${c.name.en} ${C.ready ? 'is ready' : 'hands over in ' + c.hand.en}, but ${over} over budget.`,
      doc_k: `Unit offer · ${city.en}`, doc_t: `${b.name.en} · ${bedroomEn} apartment`,
      doc_f: [['Price', b.price], ['Down payment', b.down], ['Plan', en.years(b.yrs)], ['Handover', b.hand.en], ['Area', `${b.area} m²`], ['Finishing', b.finish.enShort]],
      wa_t: `${b.name.en} offer`,
    },
  };
  return story;
}

module.exports = { buildStory, money };
