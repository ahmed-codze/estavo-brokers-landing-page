'use strict';
const LIMITS = { projects: 3, units: 3, developers: 6, news: 4, launches: 3, jobs: 4, games: 1 };
const MEDIA = /^\/api\/public\/landing-content\/media\/([a-f0-9]{64})\.webp$/;
const cairoDay = (now = new Date()) => new Intl.DateTimeFormat('en-CA', { timeZone: 'Africa/Cairo', year: 'numeric', month: '2-digit', day: '2-digit' }).format(now);
function validate(data, now = new Date()) {
  const fail = () => { throw new Error('Invalid or expired landing edition'); };
  if (!data || data.schema_version !== 1 || data.timezone !== 'Africa/Cairo' || !/^\d{4}-\d{2}-\d{2}$/.test(data.snapshot_date) || !/^[a-f0-9]{64}$/.test(data.revision)) fail();
  const age = now - new Date(data.generated_at);
  if (!Number.isFinite(age) || age < -60000 || age > 72 * 3600000 || data.snapshot_date !== cairoDay(new Date(data.generated_at))) fail();
  const text = (v, max = 240) => { if (typeof v !== 'string' || v.length > max || /[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(v)) fail(); };
  const translated = (v) => { if (!v || typeof v !== 'object') fail(); text(v.ar); text(v.en); };
  const href = (v) => { text(v, 512); const u = new URL(v); if (u.origin !== 'https://brokers.estavo.space' || u.username || u.password || !['/register', '/games/exclusive'].includes(u.pathname)) fail(); };
  const media = (v) => { if (v !== null && !MEDIA.test(v)) fail(); };
  for (const [kind, limit] of Object.entries(LIMITS)) {
    const rows = data[kind];
    if (!Array.isArray(rows) || rows.length > limit || new Set(rows.map(r => r.key)).size !== rows.length) fail();
    for (const r of rows) {
      text(r.key, 64); href(r.href);
      if (['projects', 'developers', 'games'].includes(kind)) translated(r.name);
      if (['units', 'launches'].includes(kind)) translated(r.project);
      if (kind === 'projects') { translated(r.city); translated(r.developer); media(r.image); }
      if (kind === 'developers') media(r.logo);
      if (kind === 'units') { translated(r.type); if (!Number.isFinite(r.price_from) || r.price_from <= 0 || r.price_from > 1e12 || r.currency !== 'EGP' || !Number.isFinite(r.area_sqm) || r.area_sqm < 0 || r.area_sqm > 1e7 || !data.projects.some(p => p.key === r.project_key)) fail(); }
      if (['news', 'launches'].includes(kind)) translated(r.title);
      if (kind === 'news') {
        translated(r.summary);
        if (!Array.isArray(r.sources) || r.sources.length < 1 || r.sources.length > 3) fail();
        for (const s of r.sources) { text(s.name, 100); const u = new URL(s.url); if (u.protocol !== 'https:' || u.username || u.password) fail(); }
      }
      if (kind === 'jobs') for (const key of ['title', 'company', 'location', 'employment_type']) text(r[key], 160);
      if (kind === 'games') text(r.prompt, 180);
      if (['news', 'launches', 'jobs'].includes(kind) && (!Number.isFinite(Date.parse(r.published_at)) || Date.parse(r.published_at) > +now)) fail();
      if (kind === 'jobs' && r.valid_through && !Number.isFinite(Date.parse(r.valid_through))) fail();
      // Refuse accidental server-side over-sharing, even if the renderer would ignore it.
      const allowed = {
        projects: 'key name city developer image updated_at href',
        units: 'key project_key project type area_sqm bedrooms price_from currency delivery selection href',
        developers: 'key name logo selection href', news: 'key title summary published_at sources href selection',
        launches: 'key title project published_at href selection',
        jobs: 'key title company location employment_type published_at valid_through href selection',
        games: 'key name prompt href selection',
      }[kind].split(' ');
      if (Object.keys(r).some(k => !allowed.includes(k))) fail();
    }
  }
  if (!data.units.length || !data.projects.length || !data.developers.length) fail();
  return data;
}
module.exports = { validate, cairoDay, LIMITS, MEDIA };
