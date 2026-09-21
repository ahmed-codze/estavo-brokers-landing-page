#!/usr/bin/env node
/* ============================================================
   Estavo v3 — service page builder

   The eleven service destinations share one shell: head,
   analytics, header, drawer and footer are identical, and only
   the <main> content differs. Authoring that by hand 22 times
   would guarantee drift between languages and routes, so the
   shell is generated here from tools/routes.json and the page
   bodies in tools/pages/.

   Every page it emits must still pass tools/qa.js.

   Usage: node tools/build-pages.js
   ============================================================ */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const routes = JSON.parse(fs.readFileSync(path.join(__dirname, 'routes.json'), 'utf8'));
const SITE = 'https://estavo-brokers.com';

/* Commercial pages share the reading rhythm and interaction layer, while
   route assets remain responsible for the product demonstration. Keeping the
   manifest here prevents every commercial route from inheriting Market's
   browser, AI and PDF payload. */
const ROUTE_ASSETS = {
  market: {
    styles: ['/assets/css/commercial.css', '/assets/css/market.css'],
    scripts: ['/assets/js/commercial-page.js', '/assets/js/market-landing.js'],
  },
  websites: {
    styles: ['/assets/css/commercial.css', '/assets/css/pages/websites.css'],
    scripts: ['/assets/js/commercial-page.js'],
  },
  ai: {
    styles: ['/assets/css/commercial.css', '/assets/css/pages/ai.css'],
    scripts: ['/assets/js/commercial-page.js', '/assets/js/ai-conversation.js'],
  },
  listings: {
    styles: ['/assets/css/commercial.css', '/assets/css/pages/listings.css'],
    scripts: ['/assets/js/commercial-page.js'],
  },
  enterprise: {
    styles: ['/assets/css/commercial.css', '/assets/css/pages/enterprise.css'],
    scripts: ['/assets/js/commercial-page.js'],
  },
  meta: {
    styles: ['/assets/css/commercial.css', '/assets/css/pages/meta.css'],
    scripts: ['/assets/js/commercial-page.js'],
  },
};

function routeStyles(key) {
  return (ROUTE_ASSETS[key]?.styles || [])
    .map((href) => `    <link rel="stylesheet" href="${href}" />`)
    .join('\n');
}

function routeScripts(key) {
  return (ROUTE_ASSETS[key]?.scripts || [])
    .map((src) => `    <script src="${src}" defer></script>`)
    .join('\n');
}

/* Analytics markup is copied verbatim from the parent page so
   measurement stays consistent across every route. */
const GTAG = `    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NVFZMXPPLF"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('js', new Date());

        gtag('config', 'G-NVFZMXPPLF');
    </script>
    <!-- Meta Pixel Code -->
    <script>
        !function (f, b, e, v, n, t, s) {
            if (f.fbq) return; n = f.fbq = function () {
                n.callMethod ?
                    n.callMethod.apply(n, arguments) : n.queue.push(arguments)
            };
            if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
            n.queue = []; t = b.createElement(e); t.async = !0;
            t.src = v; s = b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t, s)
        }(window, document, 'script',
            'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '1693755678488065');
        fbq('track', 'PageView');
    </script>
    <noscript><img height="1" width="1" style="display:none"
            src="https://www.facebook.com/tr?id=1693755678488065&ev=PageView&noscript=1" /></noscript>
    <!-- End Meta Pixel Code -->`;

/* Titles and descriptions land inside attributes and <title>,
   so a raw & or quote would produce invalid markup. Two English
   titles legitimately contain "&" (Data & coverage, Buyers &
   marketing), so escaping is required, not optional. */
function esc(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function criticalCss() {
  return fs.readFileSync(path.join(__dirname, 'partials', 'critical.css'), 'utf8');
}

function partial(name) {
  return fs.readFileSync(path.join(__dirname, 'partials', name), 'utf8');
}

/* Keep the persistent conversion action aligned with the page's intent.
   Market/editorial visitors should not see a competing Sites button, while
   integration visitors need the enquiry on the page rather than a product
   detour. The homepage keeps the default Sites action and presents Market as
   its parallel hero action. */
function header(route, lang) {
  const isAr = lang === 'ar';
  const marketRoutes = new Set(['data', 'market', 'insights']);
  const action = marketRoutes.has(route.key)
    ? {
        href: routes.cta.market,
        track: 'market_opened',
        label: isAr ? 'جرّب <bdi>Estavo Market</bdi> مجانًا' : 'Try Estavo Market free',
        shortLabel: isAr ? 'افتح السوق' : 'Open Market',
      }
    : route.key === 'integrations'
      ? {
          href: '#request',
          track: 'integration_enquiry_submitted',
          label: isAr ? 'كلمنا عن الربط' : 'Discuss an integration',
          shortLabel: isAr ? 'تواصل معنا' : 'Contact us',
        }
      : route.key === 'enterprise'
        ? {
            href: routes.cta.website,
            track: 'website_preview_started',
            label: isAr ? 'ابدأ موقع شركتك' : 'Start your company website',
            shortLabel: isAr ? 'موقع شركتك' : 'Company site',
          }
      : {
          href: routes.cta.website,
          track: 'website_preview_started',
          label: isAr ? 'اعمل موقعك مجانًا · حوالي ٥ دقايق' : 'Create your site free · ~5 min',
          shortLabel: isAr ? 'ابدأ مجانًا' : 'Start free',
        };

  const defaultLabel = isAr
    ? 'اعمل موقعك مجانًا · حوالي ٥ دقايق'
    : 'Create your site free · ~5 min';
  const defaultShortLabel = isAr ? 'ابدأ مجانًا' : 'Start free';

  return partial(`header.${lang}.html`)
    .replaceAll(routes.cta.website, action.href)
    .replaceAll('website_preview_started', action.track)
    .replaceAll(defaultLabel, action.label)
    .replaceAll(defaultShortLabel, action.shortLabel);
}

/* Published service pages live one directory below the site root.
   Keep authoring templates readable with root-style paths, then
   emit depth-aware relative paths so navigation and assets work
   both on the production domain and in a local folder preview. */
function relativizeForServicePage(doc) {
  return doc
    .replace(/\b(href|src|action)="\/(?!\/)/g, '$1="../')
    .replace(/url\((['"]?)\//g, 'url($1../');
}

function head(opts) {
  const { lang, dir, canonical, altUrl, ogImage, ogLocale, altLocale } = opts;
  const title = esc(opts.title);
  const description = esc(opts.description);
  const isAr = lang === 'ar';
  const styles = routeStyles(opts.key);
  return `<!DOCTYPE html>
<html lang="${lang}" dir="${dir}">

<head>
    <meta charset="UTF-8" />
${GTAG}
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#0b2239" />
    <meta name="author" content="Estavo" />

    <title>${title}</title>
    <meta name="description" content="${description}" />

    <meta name="robots" content="${opts.noindex ? 'noindex, follow' : 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1'}" />

    <link rel="canonical" href="${canonical}" />
    <link rel="alternate" hreflang="${isAr ? 'ar' : 'en'}" href="${canonical}" />
    <link rel="alternate" hreflang="${isAr ? 'en' : 'ar'}" href="${altUrl}" />
    <link rel="alternate" hreflang="x-default" href="${isAr ? canonical : altUrl}" />

    <meta property="og:site_name" content="Estavo" />
    <meta property="og:title" content="${title}" />
    <meta property="og:description" content="${description}" />
    <meta property="og:image" content="${SITE}/assets/og/${ogImage}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="${ogLocale}" />
    <meta property="og:locale:alternate" content="${altLocale}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="${canonical}" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@estavospace" />
    <meta name="twitter:title" content="${title}" />
    <meta name="twitter:description" content="${description}" />
    <meta name="twitter:image" content="${SITE}/assets/og/${ogImage}" />

    <link rel="icon" type="image/png" sizes="32x32" href="/assets/logo/Estavo%20Icon.png" />
    <link rel="shortcut icon" href="/assets/logo/Estavo%20Icon.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/logo/Estavo%20Icon.png" />
    <link rel="manifest" href="/site.webmanifest" />

${styles}
${criticalCss()}

    <link rel="preload" as="style" href="/assets/css/estavo-v3.css"
        onload="this.onload=null;this.rel='stylesheet'" />
    <noscript>
        <link rel="stylesheet" href="/assets/css/estavo-v3.css" />
    </noscript>
</head>
`;
}

function buildPage(route, lang) {
  const isAr = lang === 'ar';
  const meta = route[lang];
  const bodyFile = path.join(__dirname, 'pages', `${route.key}.${lang}.html`);
  if (!fs.existsSync(bodyFile)) return null;

  const canonicalPath = route.canonical_to || route.path;
  const canonical = isAr ? `${SITE}${canonicalPath}` : `${SITE}${canonicalPath}en.html`;
  const altUrl = isAr ? `${SITE}${canonicalPath}en.html` : `${SITE}${canonicalPath}`;

  const scripts = routeScripts(route.key);
  const doc = head({
    key: route.key,
    lang,
    dir: isAr ? 'rtl' : 'ltr',
    title: meta.title,
    description: meta.description || meta.blurb || meta.title,
    canonical,
    altUrl,
    ogImage: isAr ? 'og-ar.jpg' : 'og-en.jpg',
    ogLocale: isAr ? 'ar_EG' : 'en_US',
    altLocale: isAr ? 'en_US' : 'ar_EG',
    noindex: Boolean(route.canonical_to),
  })
    + header(route, lang)
    + '\n    <main id="main">\n'
    + fs.readFileSync(bodyFile, 'utf8')
    + '\n    </main>\n'
    + partial(`footer.${lang}.html`)
    + `
    <script src="/assets/js/referral.js" defer></script>
${scripts ? `${scripts}\n` : ''}    <script src="/assets/js/v3/estavo-v3.js" defer></script>
</body>

</html>
`;

  const outDir = path.join(ROOT, route.path.replace(/^\//, ''));
  const outFile = path.join(outDir, isAr ? 'index.html' : 'en.html');
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(outFile, relativizeForServicePage(doc));
  return path.relative(ROOT, outFile);
}

function main() {
  const written = [];
  for (const route of routes.routes) {
    if (route.key === 'home') continue;
    for (const lang of ['ar', 'en']) {
      const out = buildPage(route, lang);
      if (out) written.push(out);
    }
  }
  written.forEach((w) => console.log(`  ${w}`));
  console.log(`\n${written.length} page(s) written.`);
}

main();
