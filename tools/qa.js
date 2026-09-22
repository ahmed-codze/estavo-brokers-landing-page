#!/usr/bin/env node
/* ============================================================
   Estavo v3 — publication gate checks

   Static assertions over the built HTML. These encode the
   rules that are easy to violate by hand across the generated page family:

     1. No unapproved figures (Visual Theme Plan §4.6, §8.1).
     2. No inferred-intent labels (§8.6, Master Plan §7.7).
     3. Every illustrative sample carries a visible label
        (§4.1, Master Plan §7.1).
     4. Latin runs inside Arabic text are bidi-isolated (§7.4).
     5. Exactly one H1 per page (§13).
     6. Skip link present before nav (§13).
     7. No dead links: href="#" or empty (§4.3).
     8. Images declare width/height (§14).
     9. Public copy uses customer language, not internal
        "coverage/record/sample" vocabulary or placeholders.
    10. English pages keep visitors on English routes.
    11. Published navigation and assets do not depend on a
        domain-root deployment.

   Usage: node tools/qa.js [file ...]        (default: all HTML)
   Exit:  0 pass, 1 failures found
   ============================================================ */
'use strict';

const fs = require('fs');
const path = require('path');

/* Figures the plans name explicitly as forbidden, plus the
   scoring/intent vocabulary that turns behaviour into claims. */
const FORBIDDEN = [
  { re: /\b50,000\+/g, why: 'unapproved inventory count (§4.6)' },
  { re: /\b0\.9s\b/g, why: 'unapproved performance figure (Master Plan §13 step 4)' },
  { re: /\b12\.4K\b/g, why: 'unapproved reach figure (§4.6)' },
  { re: /تم تأهيله/g, why: 'AI-qualified claim without a defined product state (§8.1)' },
  { re: /\bQualified\b/g, why: 'inferred qualification label (§8.6)' },
  { re: /قربوا من الحجز/g, why: 'booking-readiness inference (§4.6, §8.6)' },
  { re: /مؤشر الاهتمام/g, why: 'interest score (§8.6)' },
  { re: /اتصل دلوقتي/g, why: 'next-step directive derived from views alone (§8.6)' },
  { re: /\bclose to booking\b/gi, why: 'booking-readiness inference (§4.6)' },
  { re: /\bintent score\b/gi, why: 'intent score (§8.6)' },
  /* Schema-level claims are just as public as body copy. */
  { re: /"aggregateRating"/g, why: 'fabricated review score in JSON-LD (§4.6, Master Plan §11)' },
  { re: /"ratingValue"/g, why: 'unapproved rating value in JSON-LD (§4.6)' },
  { re: /"price"\s*:\s*"0"/g, why: 'price claim without an approved commercial source (Master Plan §7.11)' },
  { re: /بتحتفظ بـ 100% من عمولتك/g, why: 'unbounded no-commission promise (Master Plan §7.4)' },
  { re: /keep 100% of your commission/gi, why: 'unbounded no-commission promise (Master Plan §7.4)' },
  /* Homepage language refactor: these terms expose internal
     architecture or unfinished content to the visitor. */
  { re: /سجل عقاري/g, why: 'internal record language; use المشروع or بيانات المشروع' },
  { re: /تغطية/g, why: 'internal coverage language; name the cities or projects instead' },
  { re: /عينة بيانات/g, why: 'laboratory-style sample language; use مثال when needed' },
  { re: /مطور تجريبي|مشروع تجريبي/g, why: 'visible placeholder identity' },
  { re: /نموذج توضيحي/g, why: 'visible placeholder/demo label; use مثال when needed' },
  { re: /نشاط مسجّل|نشاطه المسجّل/g, why: 'system language; describe what the buyer viewed' },
  { re: /\bcoverage\b/gi, why: 'internal coverage language; name the cities or projects instead' },
  { re: /sample (?:project|developer)/gi, why: 'visible placeholder identity' },
  { re: /(?:illustrative example|product demonstration)/gi, why: 'visible placeholder/demo label; use example' },
  { re: /recorded activity/gi, why: 'system language; describe what the buyer viewed' },
  { re: /\bproperty record\b/gi, why: 'internal record language; use project or unit data' },
  { re: /yourbrand\.example/gi, why: 'placeholder brand and domain' },
  { re: /\[(?:approved value|approved term|approved basis|company name|your entry)\]/gi, why: 'visible bracket placeholder' },
  { re: /\[(?:قيمة معتمدة|مدة معتمدة|أساس معتمد|اسم الشركة|من إدخالك)\]/g, why: 'visible bracket placeholder' },
];

/* Product-owner scale figures, confirmed 2026-09-22. Any published claim
   that pairs one of these nouns with a numeric value must use the same exact
   figure across Arabic and English. A leading/trailing plus is intentionally
   rejected: these are approved counts, not "more than" claims. */
const APPROVED_SCALE_CLAIMS = [
  { noun: '(?:units?|وحدات?|وحدة)', value: '30000', label: 'units / الوحدات' },
  { noun: '(?:developers?|مطوّ?رين?|مطوّ?ر)', value: '700', label: 'developers / المطورين' },
  { noun: '(?:brokers?|بروكرز?|بروكر)', value: '7000', label: 'brokers / البروكرز' },
  { noun: '(?:projects?|مشاريع|مشروع)', value: '2000', label: 'projects / المشاريع' },
];

/* A sample/demo surface must say so, in the page language. */
const SAMPLE_LABELS = [
  'مثال توضيحي', 'عينة بيانات بتاريخ', 'نموذج توضيحي', 'إحصاءات التغطية بتاريخ',
  'Illustrative example', 'Data sample as of', 'Coverage snapshot as of', 'Product demonstration',
];

/* Latin sequences that must be isolated when they sit in an
   RTL paragraph. Matches a run of Latin/digits of length >= 2. */
const LATIN_RUN = /[A-Za-z][A-Za-z0-9.&'-]{1,}(?:\s+[A-Za-z][A-Za-z0-9.&'-]{1,})*/g;

function stripTags(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<!--[\s\S]*?-->/g, ' ');
}

function checkFile(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const body = stripTags(raw);
  const failures = [];
  const isRtl = /<html[^>]*dir="rtl"/.test(raw);
  const rel = path.relative(path.join(__dirname, '..'), file).replaceAll(path.sep, '/');

  // 1 + 2. Forbidden figures and inferred-intent vocabulary.
  for (const { re, why } of FORBIDDEN) {
    // The Market scale strip is the only approved use of this figure.
    // Product owner supplied the current figure for both Market locales on 2026-09-19.
    const approvedMarketUnitPdfCount = /^market\/(?:index|en)\.html$/.test(rel)
      && re.source === '\\b50,000\\+';
    if (approvedMarketUnitPdfCount) continue;
    const hits = body.match(re);
    if (hits) failures.push(`${hits.length}x "${hits[0]}" — ${why}`);
  }

  // Scale-claim consistency. Allow up to two descriptive words between the
  // number and noun (for example, "30,000 comparable units").
  const number = '[+]?\\d{1,3}(?:,\\d{3})*(?:\\+)?';
  const word = '[A-Za-z؀-ۿ-]+';
  for (const claim of APPROVED_SCALE_CLAIMS) {
    const pair = new RegExp(
      `(${number})(?:\\s+${word}){0,2}\\s+${claim.noun}|` +
      `${claim.noun}(?:\\s+${word}){0,2}\\s+(${number})`,
      'gi'
    );
    for (const match of body.matchAll(pair)) {
      const displayed = match[1] || match[2];
      const normalized = displayed.replaceAll(',', '').replaceAll('+', '');
      if (normalized !== claim.value || displayed.includes('+')) {
        failures.push(
          `scale claim "${match[0].trim()}" must use ${Number(claim.value).toLocaleString('en-US')} ${claim.label}`
        );
      }
    }
  }

  // 3. Any placeholder bracket must be accompanied by a label.
  if (/\[قيمة معتمدة\]|\[approved value\]|\[مدة معتمدة\]|\[approved term\]/.test(body)) {
    const labelled = SAMPLE_LABELS.some((l) => body.includes(l));
    if (!labelled) {
      failures.push('placeholder values present with no sample/demo label (§4.1)');
    }
  }

  // 4. Bidi isolation for Latin runs in RTL prose. Only text
  //    nodes inside the body are considered; attributes and
  //    already-isolated <bdi>/[dir] spans are removed first.
  if (isRtl) {
    const bodyOnly = raw.slice(raw.indexOf('<body'));
    const withoutIsolated = stripTags(bodyOnly)
      .replace(/<bdi[\s\S]*?<\/bdi>/gi, ' ')
      .replace(/<[^>]*\bdir="ltr"[^>]*>[\s\S]*?<\/[a-z]+>/gi, ' ')
      .replace(/<[^>]+>/g, ' ');

    const arabicLines = withoutIsolated
      .split(/\n+/)
      .filter((line) => /[؀-ۿ]/.test(line));

    const bare = new Set();
    for (const line of arabicLines) {
      const runs = line.match(LATIN_RUN) || [];
      for (const run of runs) {
        if (run.trim().length > 2) bare.add(run.trim());
      }
    }
    if (bare.size) {
      failures.push(
        `${bare.size} un-isolated Latin run(s) in Arabic text — wrap in <bdi> (§7.4): ` +
        Array.from(bare).slice(0, 6).join(' | ')
      );
    }
  }

  // 5. Exactly one H1.
  const h1s = (raw.match(/<h1\b/gi) || []).length;
  if (h1s !== 1) failures.push(`${h1s} <h1> elements, expected exactly 1 (§13)`);

  // 6. Skip link.
  if (!/class="[^"]*es-skip-link/.test(raw)) {
    failures.push('missing skip link before navigation (§13)');
  }

  // 7. Dead links.
  const dead = (raw.match(/href="(#|)"/g) || []).length;
  if (dead) failures.push(`${dead} dead link(s) href="#" or empty (§4.3)`);

  // Root-relative local paths fail when the site is previewed
  // from its project folder or deployed below a URL prefix.
  const rootRelative = raw.match(/\b(?:href|src|action)="\/(?!\/)/g) || [];
  const rootRelativeCss = raw.match(/url\((?:['"]?)\//g) || [];
  if (rootRelative.length + rootRelativeCss.length) {
    failures.push(
      `${rootRelative.length + rootRelativeCss.length} root-relative local path(s) — use depth-aware relative paths`
    );
  }

  // 7b. English navigation must not silently switch the visitor
  //     back to the Arabic default for a bilingual service route.
  const isEnglish = /<html[^>]*lang="en"/.test(raw);
  if (isEnglish) {
    const arabicServiceLinks = raw.match(
      /href="\/(?:data|market|websites|ai|integrations|marketing|insights|listings|enterprise|pricing|examples)\/"/g
    ) || [];
    if (arabicServiceLinks.length) {
      failures.push(`${arabicServiceLinks.length} English-page link(s) point to Arabic service routes`);
    }
  }

  // 8a. Unescaped ampersands in head attributes produce invalid
  //     markup; two English titles legitimately contain "&".
  const headEnd = raw.indexOf('</head>');
  if (headEnd > 0) {
    const head = raw.slice(0, headEnd);
    const rawAmp = (head.match(/content="[^"]*&(?!amp;|lt;|gt;|quot;|#\d+;)[^"]*"/g) || []).length;
    const titleAmp = /<title>[^<]*&(?!amp;|lt;|gt;|quot;|#\d+;)/.test(head) ? 1 : 0;
    if (rawAmp + titleAmp) {
      failures.push(`${rawAmp + titleAmp} unescaped "&" in head title/meta — invalid markup`);
    }
  }

  // 8. Images must reserve space.
  const imgs = raw.match(/<img\b[^>]*>/gi) || [];
  const unsized = imgs.filter((t) => !(/\bwidth=/.test(t) && /\bheight=/.test(t)));
  if (unsized.length) {
    failures.push(`${unsized.length} <img> without width/height — layout shift (§14)`);
  }

  // The homepage product scene is the LCP image. Lazy-loading it
  // contradicts fetchpriority="high" and delays the first useful view.
  const heroImage = imgs.find((t) => /class="[^"]*es-hero-figure__vector/.test(t));
  if (heroImage && !/loading="eager"/.test(heroImage)) {
    failures.push('homepage hero image must use loading="eager" — LCP regression');
  }

  // Commercial conversion buttons must complete the action their labels promise.
  const route = rel.split('/')[0];

  // Conversion pages need enough detail to answer the decision, but not a
  // product-manual-length journey. Archived supporting sections live in
  // <template> blocks and do not count toward the visible funnel.
  const conversionPage = rel === 'index.html' || rel === 'en.html' ? 'home' : route;
  const visibleSectionBudget = {
    home: 9,
    data: 1,
    market: 9,
    websites: 8,
    ai: 7,
    integrations: 7,
    marketing: 6,
    meta: 7,
    insights: 5,
    listings: 7,
    enterprise: 8,
    pricing: 5,
    examples: 4,
  }[conversionPage];
  if (visibleSectionBudget) {
    const withoutArchivedSections = raw.replace(/<template\b[\s\S]*?<\/template>/gi, '');
    const visibleSections = (withoutArchivedSections.match(/<section\b/gi) || []).length;
    if (visibleSections > visibleSectionBudget) {
      failures.push(`${visibleSections} visible sections, conversion budget is ${visibleSectionBudget}`);
    }
  }

  const expectedDestination = ['data', 'market', 'insights'].includes(route)
    ? 'https://brokers.estavo.space/go/?ref=default-landing-page-market'
    : ['websites', 'enterprise', 'ai', 'marketing', 'meta', 'listings'].includes(route)
      ? 'https://estavo-brokers.com/website/'
      : null;
  if (expectedDestination) {
    const conversionButtons = [...raw.matchAll(/<a\b[^>]*href="([^"]+)"[^>]*class="[^"]*(?:es-button--primary|es-button--light)[^"]*"[^>]*data-position="(?:hero|workflow|close)"[^>]*>/gi)];
    if (!conversionButtons.length) {
      failures.push('missing hero/workflow/close conversion button');
    }
    const wrong = conversionButtons.filter((m) => m[1] !== expectedDestination);
    if (wrong.length) {
      failures.push(`${wrong.length} conversion button(s) do not use the required route destination`);
    }
  }

  // The persistent action must reinforce the page's decision instead of
  // pulling a Market visitor into Sites (or an integration visitor into a
  // self-service product). Homepage is intentionally handled separately.
  const expectedHeaderDestination = expectedDestination || (route === 'integrations' ? '#request' : null);
  if (expectedHeaderDestination) {
    const headerButton = raw.match(/<a\b[^>]*href="([^"]+)"[^>]*data-position="header"[^>]*>/i);
    if (!headerButton) {
      failures.push('missing persistent header conversion action');
    } else if (headerButton[1] !== expectedHeaderDestination) {
      failures.push(`header conversion points to ${headerButton[1]}, expected ${expectedHeaderDestination}`);
    }
  }

  // The confirmed speed proposition applies to initial website creation only.
  // Keep it visible in the main content of every Sites-family decision page,
  // while page copy explains that optional setup follows its own scope.
  if (['websites', 'ai', 'marketing', 'meta', 'listings'].includes(route)) {
    const main = raw.match(/<main\b[\s\S]*?<\/main>/i)?.[0] || '';
    if (!/(?:around five minutes|حوالي ٥ دقايق)/i.test(main)) {
      failures.push('Sites page must state the around-five-minute website starting point in main content');
    }
  }

  // Owner-approved acquisition story (2026-09-20): the individual Site must
  // contrast with assembling technical/data teams, while the company Site
  // must carry the approved operating-cost comparison. Keep these promises
  // explicit instead of allowing the pages to drift back into feature lists.
  if (route === 'websites') {
    const hasIndividualPositioning = isRtl
      ? /فريق تقني[^<]{0,80}فريق داتا/.test(body)
      : /without (?:a|the) tech or data team/i.test(body);
    if (!hasIndividualPositioning) {
      failures.push('individual Sites page is missing the approved no-tech/data-team positioning');
    }
  }
  if (route === 'enterprise') {
    const hasCompanyCostPositioning = isRtl
      ? /أقل من (?:تكلفة )?مرتب موظف/.test(body)
      : /less than (?:the cost of one data-entry salary|the salary of one data-entry employee)/i.test(body);
    if (!hasCompanyCostPositioning) {
      failures.push('company Sites page is missing the approved one-data-entry-salary comparison');
    }
  }

  // /data/ is retained only as an inbound migration route.
  if (route === 'data') {
    if (!/<meta name="robots" content="noindex, follow"/.test(raw)) {
      failures.push('/data/ migration route must be noindex, follow');
    }
    if (!/<link rel="canonical" href="https:\/\/estavo-brokers\.com\/market\/(?:en\.html)?"/.test(raw)) {
      failures.push('/data/ migration route must canonicalise to the matching Market page');
    }
  }

  // The header/drawer is authored once in tools/partials/header.*.html
  // and inlined into the generated routes. The two homepages are NOT
  // generated, so their copy is maintained by hand and has drifted
  // before (different menu label, a different primary CTA). Compare the
  // parts that carry meaning rather than whole markup, since the
  // homepage legitimately uses relative paths where the partial uses
  // root-relative ones.
  if (rel === 'index.html' || rel === 'en.html') {
    const partialFile = path.join(
      __dirname, 'partials', rel === 'index.html' ? 'header.ar.html' : 'header.en.html'
    );
    if (fs.existsSync(partialFile)) {
      const partial = fs.readFileSync(partialFile, 'utf8');
      const signature = (text) => {
        const header = text.slice(
          text.indexOf('<header class="es-header">'),
          text.indexOf('<main') === -1 ? text.length : text.indexOf('<main')
        );
        return {
          // Nav/drawer destinations, normalised to ignore path depth
          // and the .html suffix the English pages carry.
          links: [...header.matchAll(/href="([^"]+)"/g)]
            .map((m) => m[1].replace(/^\.?\/?/, '').replace(/en\.html$/, '').replace(/^index\.html$/, ''))
            .filter((h) => !h.startsWith('assets')),
          // Conversion tracking on the header and drawer buttons.
          tracks: [...header.matchAll(/data-track="([^"]+)"/g)].map((m) => m[1]),
        };
      };
      const page = signature(raw);
      const source = signature(partial);
      if (page.links.join('|') !== source.links.join('|')) {
        failures.push('header links differ from tools/partials/header.*.html — re-sync the homepage header');
      }
      if (page.tracks.join('|') !== source.tracks.join('|')) {
        failures.push('header conversion tracking differs from tools/partials/header.*.html');
      }
    }
  }

  return failures;
}

function main() {
  const root = path.join(__dirname, '..');
  let files = process.argv.slice(2);

  if (!files.length) {
    const roots = ['index.html', 'en.html'];
    const dirs = ['data', 'market', 'websites', 'ai', 'integrations', 'marketing', 'meta',
      'insights', 'listings', 'enterprise', 'pricing', 'examples'];
    files = roots.map((f) => path.join(root, f));
    for (const d of dirs) {
      for (const f of ['index.html', 'en.html']) {
        const p = path.join(root, d, f);
        if (fs.existsSync(p)) files.push(p);
      }
    }
  }

  let total = 0;
  let checked = 0;

  for (const file of files) {
    if (!fs.existsSync(file)) continue;
    checked++;
    const failures = checkFile(file);
    const rel = path.relative(root, file);
    if (failures.length) {
      total += failures.length;
      console.log(`\n✗ ${rel}`);
      failures.forEach((f) => console.log(`    ${f}`));
    } else {
      console.log(`✓ ${rel}`);
    }
  }

  console.log(`\n${checked} file(s) checked, ${total} failure(s).`);
  process.exit(total ? 1 : 0);
}

main();
