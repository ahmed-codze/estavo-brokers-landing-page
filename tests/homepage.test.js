'use strict';

/* Homepage contract — community positioning (3 November 2026).
   «كل اللي محتاجه كبروكر. في مكان واحد، بالذكاء الاصطناعي.»
   Encodes the rules that are easy to erode by hand: the nine-section
   story, one primary door (Market) with the website as the second,
   verified proof figures only, honest product truth (free for now,
   no ROI calculator, jobs need an account, the game does not),
   labelled examples, accessible hero tabs that work without JS,
   and analytics on deliberate clicks only. */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const MARKET = 'https://brokers.estavo.space/go/?ref=default-landing-page-market';
const WEBSITE = 'https://estavo-brokers.com/website/';
const PROOF = JSON.parse(fs.readFileSync(path.join(__dirname, '../tools/data/home-proof.json'), 'utf8'));
const MAP = JSON.parse(fs.readFileSync(path.join(__dirname, '../tools/data/egypt-map.json'), 'utf8'));
const FIXTURE = JSON.parse(fs.readFileSync(path.join(__dirname, '../tools/data/home-fixture.json'), 'utf8'));
const unit = (key) => FIXTURE.units.find((u) => u.key === key);
const money = (m) => `${m.toFixed(1)}M`;
const SECTIONS = ['home-hero', 'home-destinations', 'home-data', 'home-ai', 'home-website', 'home-today', 'home-integrations', 'home-faq', 'home-closing'];
const MONTHS = {
    ar: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'],
    en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
};
const text = (el) => el.textContent.replace(/\s+/g, ' ').trim();

function load(file) {
    const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
    return { html, doc: new JSDOM(html).window.document };
}

/* Relative route as each language writes it (English stays on English routes). */
const route = (r, lang) => (lang === 'ar' ? r : r.startsWith('guides/') ? r.replace(/^guides\//, 'guides/en/') : r.replace(/\/$/, '/en.html'));

for (const [file, L] of [
    ['index.html', {
        lang: 'ar', start: 'ابدأ مع إستاڤو مجانًا', explore: 'اكتشف إستاڤو', website: 'اعمل موقعك مجانًا', example: 'مثال توضيحي',
        eyebrow: 'إستاڤو · مجتمع البروكرز في مصر', h1: ['كل اللي محتاجه كبروكر.', 'في مكان واحد، بالذكاء الاصطناعي.'],
        tabs: ['جديد السوق', 'طلب عميل', 'كاش ولا تقسيط؟', 'الوظائف', 'ألعاب وتحديات'],
        free: /مجاني بالكامل حاليًا/, noCut: /من غير نسبة من عمولتك/, leadCap: 140,
    }],
    ['en.html', {
        lang: 'en', start: 'Start with Estavo free', explore: 'Explore Estavo', website: 'Create your website free', example: 'Example',
        eyebrow: 'Estavo · The broker community in Egypt', h1: ['Everything you need as a broker.', 'In one place, with AI.'],
        tabs: ['Market news', 'Client request', 'Cash or installments?', 'Jobs', 'Games & challenges'],
        free: /Completely free for now/, noCut: /No cut of your commission/, leadCap: 170,
    }],
]) {
    const ar = L.lang === 'ar';

    test(`${file}: keeps the first-load performance contract`, () => {
        const { html, doc } = load(file);
        assert.ok(Buffer.byteLength(html) < 125000, 'homepage HTML must stay below 125 KB');
        assert.equal(doc.querySelector('style#es-design-critical'), null, 'shared CSS must be cacheable, not duplicated inline');
        assert.ok(doc.querySelector('link[rel="stylesheet"][href*="home-critical.css"]'));
        assert.equal(doc.querySelector('link[href*="estavo-v3.css"]'), null, 'homepage must not download duplicate shared CSS');
        assert.equal(doc.querySelector('link[rel="prefetch"][as="document"]'), null, 'alternate language must not consume first-load bandwidth');

        const fontStylesheet = doc.querySelector('link[href*="fonts.googleapis.com/css2"]');
        assert.ok(fontStylesheet);
        assert.doesNotMatch(fontStylesheet.href, /ital,|wght@.*700|wght@.*300/, 'only the three used font weights may load');
        assert.equal(fontStylesheet.href.includes('family=IBM+Plex+Sans'), !ar);
        assert.equal(fontStylesheet.href.includes('family=Cairo'), ar);

        const logo = doc.querySelector('.es-header__logo img');
        assert.match(logo.getAttribute('src'), /estavo-brokers-logo-320\.webp$/);
        assert.equal(logo.getAttribute('decoding'), 'async');
        assert.ok(doc.querySelector('link[rel="preload"][as="image"][href$="estavo-brokers-logo-320.webp"]'));

        assert.equal(doc.querySelector('script[src*="/raghad.js"]'), null, 'assistant must keep its deferred loader');
        assert.ok(doc.querySelector('script[src*="raghad-loader.js"]'));
    });

    test(`${file}: exactly the nine community sections, in order, one H1`, () => {
        const { doc } = load(file);
        const ids = [...doc.querySelectorAll('main > section')].map((s) => s.id);
        assert.deepEqual(ids, SECTIONS);
        assert.equal(doc.querySelectorAll('h1').length, 1);
        assert.ok(doc.querySelector('#home-hero h1'));
        // Archived conversion blocks are gone with their sections.
        assert.equal(doc.querySelector('main template'), null);
        for (const id of ['home-market', 'home-request', 'home-client', 'home-growth', 'home-start-free']) {
            assert.equal(doc.getElementById(id), null, `${id} was retired`);
        }
    });

    test(`${file}: hero states the community promise with one primary door`, () => {
        const { doc } = load(file);
        const hero = doc.querySelector('#home-hero');
        assert.equal(text(hero.querySelector('.es-home-eyebrow')), L.eyebrow);
        const spans = [...hero.querySelectorAll('h1 > span')].map(text);
        assert.deepEqual(spans, L.h1, 'two lines; the second carries the gradient');
        const lead = text(hero.querySelector('.es-home-lead'));
        assert.ok(lead.length <= L.leadCap, `hero lead is ${lead.length} chars (about two lines)`);
        assert.match(lead, ar ? /المطورين.*أخبار السوق.*الوظائف.*AI.*موقع باسمك/ : /developer data.*market news.*jobs.*AI.*website under your name/);

        const links = [...hero.querySelectorAll('.es-home-actions a')];
        assert.equal(links.length, 2);
        assert.equal(links[0].href, MARKET);
        assert.equal(text(links[0]), L.start);
        assert.match(links[0].className, /es-home-btn--primary/);
        assert.equal(links[0].dataset.track, 'market_opened');
        assert.equal(links[0].dataset.position, 'hero');
        assert.equal(links[0].dataset.homeEvent, 'home_start_click');
        // The second action is a quiet in-page link, not a competing button.
        assert.equal(links[1].getAttribute('href'), '#home-destinations');
        assert.equal(text(links[1]), L.explore);
        assert.doesNotMatch(links[1].className, /es-home-btn/);

        const assure = text(hero.querySelector('.es-home-assure'));
        assert.match(assure, L.free);
        assert.match(assure, L.noCut);
        assert.match(assure, /6,600\+/);
    });

    test(`${file}: closing and sticky bar repeat the same Market door`, () => {
        const { doc } = load(file);
        const links = [...doc.querySelectorAll('#home-closing .es-home-actions a')];
        assert.equal(links.length, 2);
        assert.equal(links[0].href, MARKET);
        assert.equal(text(links[0]), L.start);
        assert.match(links[0].className, /es-home-btn--primary/);
        assert.equal(links[1].href, WEBSITE);
        assert.equal(text(links[1]), L.website);
        const sticky = [...doc.querySelectorAll('[data-home-sticky] a')];
        assert.equal(sticky.length, 1);
        assert.equal(sticky[0].href, MARKET);
        assert.equal(text(sticky[0]), L.start);
    });

    test(`${file}: hero shows the real product with soft 3D objects, never tabs`, () => {
        const { doc } = load(file);
        const pd = doc.querySelector('#home-hero .fxp-hero-art .pd');
        assert.ok(pd, 'product composition');
        assert.equal(pd.getAttribute('aria-hidden'), 'true', 'decorative; the copy carries the meaning');
        assert.equal(doc.querySelector('#home-hero [role="tablist"]'), null, 'no tabs (owner direction, 4 Nov 2026)');
        assert.ok(pd.querySelector('.pd-win img[src*="img/market/hero-"]'), 'real Market screen');
        assert.ok(pd.querySelector('.pd-phone img[src*="img/market/chat-mobile-"]'), 'real AI chat on a phone');
        assert.ok(pd.querySelectorAll('.pd-obj img[src*="img/3d/"]').length >= 4, 'soft 3D objects');
        pd.querySelectorAll('img').forEach((img) => {
            assert.ok(img.getAttribute('width') && img.getAttribute('height'), 'sized image');
            assert.equal(img.getAttribute('alt'), '');
        });
        for (const sel of ['#home-today', '#home-hero']) {
            assert.doesNotMatch(text(doc.querySelector(sel)), /\b\d{1,2} (يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر|January|February|March|April|May|June|July|August|September|October|November|December)/);
        }
    });

    test(`${file}: today board links every story to its own page, with example content only`, () => {
        const { doc } = load(file);
        const board = doc.querySelector('#home-today [data-home-today]');
        assert.match(text(board.querySelector('.es-home-today__head')), new RegExp(L.example));
        const stories = [...board.querySelectorAll('.es-home-story')];
        assert.equal(stories.length, 5);
        assert.equal(board.querySelectorAll('.es-home-story--lead').length, 1);
        const hrefs = stories.map((s) => s.querySelector('a').getAttribute('href'));
        assert.deepEqual(hrefs, ['insights/', 'insights/', 'jobs/', 'challenges/', 'guides/compare-payment-plans/'].map((r) => route(r, L.lang)));
        // The selling guide is a real, published guide.
        assert.ok(fs.existsSync(path.join(__dirname, '..', hrefs[4], 'index.html')), hrefs[4]);
        stories.forEach((s) => assert.ok(text(s.querySelector('.es-home-story__type')).length > 2));
        // Relative dates only inside examples; no live-looking calendar dates.
        for (const sel of ['#home-today', '#home-hero']) {
            assert.doesNotMatch(text(doc.querySelector(sel)), /\b\d{1,2} (يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر|January|February|March|April|May|June|July|August|September|October|November|December)/);
        }
    });

    test(`${file}: destinations cover every pillar with an icon and a benefit line`, () => {
        const { doc } = load(file);
        const tiles = [...doc.querySelectorAll('#home-destinations .es-home-dest')];
        assert.deepEqual(tiles.map((a) => a.getAttribute('href')),
            ['market/', 'market/#pdf-feature', 'developers/', 'insights/', 'jobs/', 'challenges/', 'websites/'].map((r) => (L.lang === 'ar' ? r : r.includes('#') ? r.replace('#', 'en.html#') : route(r, L.lang))));
        tiles.forEach((a) => {
            const orb = a.querySelector('.fxp-dest-orb');
            assert.ok(orb && orb.getAttribute('aria-hidden') === 'true', 'pillar icon is decorative');
            assert.ok(text(a.querySelector('.es-home-dest__name')).length > 2);
            assert.ok(text(a.querySelector('.es-home-dest__line')).length > 20);
        });
        const strip = doc.querySelector('#home-destinations .es-home-askstrip');
        assert.equal(strip.getAttribute('href'), route('broker-ai/', L.lang));
        assert.match(text(strip), ar ? /وفي كل خطوة: اسأل إستاڤو/ : /And at every step: ask Estavo/);
    });

    test(`${file}: data section carries the verified figures and their limits`, () => {
        const { doc } = load(file);
        const items = [...doc.querySelectorAll('#home-data [data-proof]')];
        assert.equal(doc.querySelectorAll('[data-proof]').length, items.length, 'one proof strip, in the data section');
        assert.equal(items.length, PROOF.figures.length);
        for (const item of items) {
            const figure = PROOF.figures.find((f) => f.key === item.dataset.proof);
            assert.ok(figure, item.dataset.proof);
            assert.ok(figure.display <= figure.verified, `${figure.key} rounds above ${figure.verified}`);
            const value = item.querySelector('.es-home-proof__value');
            // The final value ships in the HTML and is never animated through
            // intermediate (unverified) numbers. "+" only for a rounded-down floor.
            const plus = figure.display < figure.verified ? '+' : '';
            assert.equal(value.textContent.trim(), `${figure.display.toLocaleString('en-US')}${plus}`);
            assert.equal(value.dataset.count, undefined, 'no count-up hook');
        }
        // The snapshot date shown is the verified date in the config.
        const [y, m, d] = PROOF.verified_at.split('-').map(Number);
        const note = text(doc.querySelector('#home-data .es-home-proof__note'));
        assert.match(note, new RegExp(`\\b${d}\\b`));
        assert.match(note, new RegExp(`${y}`));
        assert.match(note, new RegExp(MONTHS[L.lang][m - 1]));
        // Unit models are labelled as such — never as individual or available units —
        // and the limits sit beside the figures.
        const units = doc.querySelector('[data-proof="units"] > span').textContent.trim();
        assert.equal(units, ar ? 'نموذج وحدة' : 'unit types');
        assert.match(text(doc.querySelector('[data-proof="areas"]')), ar ? /16 مدينة/ : /16 cities/);
        const limits = text(doc.querySelector('#home-data .es-home-proof__limits'));
        assert.match(limits, ar ? /مش وحدة متاحة/ : /not an available unit/);
        assert.match(limits, ar ? /مش لحظية/ : /not live/);
        assert.equal(doc.querySelectorAll('#home-data .es-home-steps li').length, 3, 'collected → reviewed → updated');
        const cta = doc.querySelector('#home-data .es-home-actions a');
        assert.equal(cta.getAttribute('href'), route('market/', L.lang));
        // Superseded / overstated figures must not reappear anywhere visible.
        assert.doesNotMatch(doc.querySelector('main').textContent, /30,000|7,000|26,169|2,412/);
    });

    test(`${file}: section graphics are real product compositions with soft 3D objects`, () => {
        const { doc } = load(file);
        const arts = [...doc.querySelectorAll('main figure.fxp-sec-art')];
        assert.deepEqual(arts.map((f) => f.closest('section').id), ['home-data', 'home-ai', 'home-website', 'home-integrations']);
        arts.forEach((f) => {
            assert.ok(f.querySelector('.pd .pd__scene'), 'product composition');
            const img = f.querySelector('img');
            assert.ok(img.getAttribute('width') && img.getAttribute('height'));
            assert.match(img.getAttribute('src'), /assets\/img\/(market|3d|estavo-|home)/);
        });
        assert.equal(doc.querySelector('main .es-home-browser, main .es-home-flow, main [data-home-tasks]'), null);
    });

    test(`${file}: every example surface is labelled`, () => {
        const { doc } = load(file);
        assert.ok(doc.querySelector('[data-home-today]').textContent.includes(L.example), 'today');
        doc.querySelectorAll('main figure.fxp-sec-art').forEach((f) => assert.ok(f.textContent.includes(L.example), f.closest('section').id));
    });



    test(`${file}: website section has one creation button, its timing and the plan boundary`, () => {
        const { doc } = load(file);
        const section = doc.querySelector('#home-website');
        const buttons = [...section.querySelectorAll('a.es-home-btn')];
        assert.equal(buttons.length, 1, 'no duplicate same-destination button');
        assert.equal(buttons[0].href, WEBSITE);
        assert.equal(text(buttons[0]), L.website);
        assert.equal(buttons[0].dataset.track, 'website_preview_started');
        const block = text(buttons[0].closest('.es-home-cta-block'));
        assert.match(block, ar ? /حوالي 5 دقايق/ : /about 5 minutes/);
        assert.doesNotMatch(block, /أقل من 5|under 5/);
        assert.match(block, ar ? /إنشاء الموقع الأساسي مجاني/ : /Creating the basic site is free/);
        assert.match(block, ar ? /المدن والـ ?AI وإمكانيات التسويق حسب الباقة/ : /Cities, AI and marketing features follow your plan/);
        // Capabilities as a journey, then the two audiences.
        assert.deepEqual([...section.querySelectorAll('.es-home-caps a')].map((a) => a.getAttribute('href')),
            ['ai/', 'marketing/', 'meta/'].map((r) => route(r, L.lang)));
        assert.deepEqual([...section.querySelectorAll('.es-home-audience a')].map((a) => a.getAttribute('href')),
            ['websites/', 'enterprise/'].map((r) => route(r, L.lang)));
        // The site is shown as the Sites illustration, labelled once as an example.
        const site = section.querySelector('figure.fxp-sec-art');
        assert.ok(site);
        assert.equal((site.textContent.match(new RegExp(L.example, 'g')) || []).length, 1, 'labelled once');
        // Website creation buttons share one label everywhere.
        doc.querySelectorAll(`a.es-home-btn[href="${WEBSITE}"]`).forEach((a) => assert.equal(text(a), L.website));
        const main = doc.querySelector('main');
        assert.equal(main.querySelector('a[href*="examples/"]'), null);
    });

    test(`${file}: integrations is a compact B2B door with AI as an optional branch`, () => {
        const { doc } = load(file);
        const section = doc.querySelector('#home-integrations');
        const a = section.querySelector('.es-home-actions a');
        assert.equal(a.getAttribute('href'), route('integrations/', L.lang));
        const art = section.querySelector('figure.fxp-sec-art');
        assert.ok(art && art.querySelector('.pd'));
        assert.match(text(section), ar ? /اختياري/ : /optional/i, 'AI stays an optional branch');
        assert.doesNotMatch(text(section), ar ? /فوري|في دقايق/ : /instant|in minutes/i, 'integration scope is agreed, never instant');
    });

    test(`${file}: illustrations invite no input they cannot handle`, () => {
        const { doc } = load(file);
        for (const fig of doc.querySelectorAll('main figure')) {
            assert.equal(fig.querySelector('input, textarea, select, button, a, [contenteditable], [tabindex]'), null);
        }
        // Only the comparison and the FAQ are disclosures — sections are not accordions.
        assert.equal(doc.querySelectorAll('main details').length, 1 + doc.querySelectorAll('#home-faq details').length);
        const details = doc.querySelector('#home-ai details.es-home-compare');
        assert.equal(details.open, false);
        assert.equal(text(details.querySelector(':scope > summary')), ar ? 'قارن كل التفاصيل' : 'Compare all details');
    });

    test(`${file}: copy keeps product truth`, () => {
        const { html, doc } = load(file);
        const main = doc.querySelector('main').textContent;
        assert.doesNotMatch(html, /testimonial|REPLACE_ME|شهادات عملائنا/i);
        // Free for now — never forever; no credits; no unbounded commission promise.
        assert.doesNotMatch(main, /للأبد|free forever|رصيد|credits?\b|100%/i);
        // Brokers get the NPV check, never an ROI / rental-yield calculator.
        assert.doesNotMatch(main, /العائد على الاستثمار|عائد إيجاري|rental yield|ROI calculator|returns calculator/i);
        // Jobs: no applying through Estavo, no verified employers, no counts.
        assert.doesNotMatch(main, /قدّم من خلال إستاڤو|apply through Estavo|one-click apply|verified (jobs|employers)/i);
        // Community is a destination, not a social network.
        assert.doesNotMatch(main, /feed|messag(e|ing) (other )?brokers|followers|متابعين|بوست/i);
        // Leads stay compact paragraphs: no questions, no lists.
        doc.querySelectorAll('main .es-home-lead').forEach((p) => {
            assert.doesNotMatch(p.textContent, /[؟?]/);
            assert.ok(p.textContent.trim().split(/\s+/).length <= 45, p.textContent.slice(0, 40));
        });
        assert.doesNotMatch(main, /Client Intelligence|Budget Range|CRM|مش مجرد/);
    });

    test(`${file}: homepage events are attached to deliberate links only`, () => {
        const { doc } = load(file);
        const events = [...doc.querySelectorAll('[data-home-event]')];
        assert.ok(events.length >= 12);
        events.forEach((el) => assert.equal(el.tagName, 'A'));
        const names = new Set(events.map((el) => el.dataset.homeEvent));
        for (const name of ['home_start_click', 'home_website_free_click', 'home_today_click', 'home_destination_click',
            'home_data_click', 'home_ai_request_demo_click', 'home_client_ai_click', 'home_client_insights_click',
            'home_meta_click', 'home_websites_click', 'home_enterprise_click', 'home_integrations_click']) {
            assert.ok(names.has(name), name);
        }
        // Existing funnel events keep firing alongside the new names.
        doc.querySelectorAll(`a[href="${MARKET}"][data-home-event]`).forEach((a) => assert.equal(a.dataset.track, 'market_opened'));
        doc.querySelectorAll(`a[href="${WEBSITE}"][data-home-event]`).forEach((a) => assert.equal(a.dataset.track, 'website_preview_started'));
    });

    test(`${file}: FAQ structured data mirrors the visible FAQ`, () => {
        const { doc } = load(file);
        const graph = JSON.parse(doc.querySelector('script[type="application/ld+json"]').textContent)['@graph'];
        const faq = graph.find((node) => node['@type'] === 'FAQPage');
        const visible = [...doc.querySelectorAll('#home-faq summary')].map(text);
        assert.deepEqual(faq.mainEntity.map((q) => q.name), visible);
        const answers = [...doc.querySelectorAll('#home-faq details > p')].map((p) => {
            const clone = p.cloneNode(true);
            clone.querySelectorAll('a').forEach((a) => a.remove());
            return text(clone);
        });
        assert.deepEqual(faq.mainEntity.map((q) => q.acceptedAnswer.text), answers);
        assert.equal(visible.length, 6, 'six entry questions');
        assert.doesNotMatch(visible.join(' '), /CRM|بيعمل إيه|What is Estavo|يعرف كل حاجة|know everything/i);
        assert.equal(doc.querySelectorAll('#home-faq details[open]').length, 0);
        assert.ok(doc.querySelector('#home-faq a[href^="privacy"]'), 'privacy policy linked from the FAQ');
        // The jobs/game answer states the real access model.
        assert.match(answers[5], ar ? /تسجيل مجاني.*من غير حساب/ : /free sign-up.*without an account/);
        // SoftwareApplication lists the community pillars.
        const app = graph.find((node) => node['@type'] === 'SoftwareApplication');
        assert.ok(app.featureList.length >= 8);
        assert.match(app.featureList.join(' '), ar ? /المطورين.*Estavo Daily.*كاش ولا تقسيط.*وظايف.*(ألعاب|الألعاب).*Brokers AI/ : /Developer.*Estavo Daily.*Cash or installments.*jobs.*Games.*Brokers AI/);
    });

    test(`${file}: metadata uses the community title`, () => {
        const { doc } = load(file);
        const routes = JSON.parse(fs.readFileSync(path.join(__dirname, '../tools/routes.json'), 'utf8'));
        const home = routes.routes.find((r) => r.key === 'home');
        assert.equal(doc.title, home[L.lang].title);
        assert.equal(doc.querySelector('meta[property="og:title"]').content, home[L.lang].title);
        assert.ok(doc.querySelector('meta[name="description"]').content.length > 60);
    });

    test(`${file}: navigation stays in sync with the global nav rules`, () => {
        const { doc } = load(file);
        const nav = doc.querySelector('.es-header').outerHTML + doc.querySelector('[data-drawer]').outerHTML;
        assert.doesNotMatch(nav, /examples\//);
        assert.match(nav, ar ? /فهم العميل/ : /Client understanding/);
        assert.doesNotMatch(nav, /مرتب|salary|Estavo Sites/);
        // Mascot slots stay empty until the final art exists (no reserved gap, no stand-in).
        assert.equal(doc.querySelectorAll('main .es-home-mascot').length, 0);
    });
}

test('click analytics: one deliberate click sends the legacy event and the home_* event once each', async () => {
    const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8')
        .replace(/<script[\s\S]*?<\/script>/gi, '');
    const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true, url: 'https://estavo-brokers.com/' });
    const { window } = dom;
    window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
    window.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
    const sent = [];
    window.gtag = (kind, name, props) => sent.push({ name, props });
    for (const file of ['assets/js/v3/estavo-v3.js', 'assets/js/home.js']) {
        window.eval(fs.readFileSync(path.join(__dirname, '..', file), 'utf8'));
    }
    window.document.dispatchEvent(new window.Event('DOMContentLoaded'));
    await new Promise((r) => setTimeout(r, 10));
    sent.length = 0;
    const link = window.document.querySelector('#home-hero a[data-track="market_opened"]');
    link.addEventListener('click', (e) => e.preventDefault());
    link.dispatchEvent(new window.MouseEvent('click', { bubbles: true, cancelable: true }));
    const names = sent.map((e) => e.name).sort();
    assert.deepEqual(names, ['home_start_click', 'market_opened']);
    sent.forEach((e) => assert.deepEqual(Object.keys(e.props).sort(), ['lang', 'position']));
    // Opening a disclosure or the FAQ is not a conversion event.
    sent.length = 0;
    window.document.querySelector('#home-ai details summary').dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
    window.document.querySelector('#home-faq summary').dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
    assert.deepEqual(sent, []);
    await new Promise((r) => setTimeout(r, 10));
    window.close();
});

test('mint stays an intelligence colour, never a CTA or badge', () => {
    const css = fs.readFileSync(path.join(__dirname, '../assets/css/home.css'), 'utf8');
    const rule = (selector) => {
        const match = css.match(new RegExp(`\\n${selector.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')} \\{([^}]*)\\}`));
        assert.ok(match, selector);
        return match[1];
    };
    for (const selector of ['.es-home-btn--primary', '.es-home-btn--secondary', '.es-home-badge']) {
        assert.doesNotMatch(rule(selector), /mint/, selector);
    }
});

test('homepage defers below-fold rendering and uses compact image assets', () => {
    const css = fs.readFileSync(path.join(__dirname, '../assets/css/home.css'), 'utf8');
    assert.match(css, /content-visibility:\s*auto/);
    assert.match(css, /contain-intrinsic-size:/);

    for (const asset of [
        'assets/logo/estavo-brokers-logo-320.webp',
        'assets/logo/estavo-mark-white-128.webp',
        'assets/logo/estavo-inverted-wordmark-400.webp',
    ]) {
        assert.ok(fs.statSync(path.join(__dirname, '..', asset)).size < 10000, `${asset} must stay below 10 KB`);
    }
});

test('homepage CSS/JS carry no testimonial remnants; future art backlog is mascot-only', () => {
    for (const file of ['assets/css/home.css', 'assets/js/home.js']) {
        assert.doesNotMatch(fs.readFileSync(path.join(__dirname, '..', file), 'utf8'), /testimonial/i, file);
    }
    for (const file of ['index.html', 'en.html']) {
        const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
        const backlog = [...html.matchAll(/backlog[^\n]*/gi)].map((m) => m[0]);
        backlog.forEach((line) => assert.match(line, /pose/i, `${file}: non-mascot backlog item: ${line}`));
        // The closing uses the transferred waving pose; no empty mascot slot reserves space.
        assert.match(html, /class="es-home-closing__mascot" src="assets\/img\/mascot\/estavo-guide-waving-200\.webp"/);
        assert.doesNotMatch(html, /es-home-mascot-slot|data-mascot-slot/);
    }
    assert.ok(fs.statSync(path.join(__dirname, '../assets/img/mascot/estavo-guide-waving-200.webp')).size < 25000);
    const agents = fs.readFileSync(path.join(__dirname, '../AGENTS.md'), 'utf8');
    const section = agents.split('### Remaining homepage art backlog')[1].split('\n#')[0]
        .split('\n').filter((line) => /^\d+\./.test(line));
    assert.ok(section.length >= 1);
    section.forEach((line) => assert.match(line, /pose/i, line));
    assert.doesNotMatch(section.join('\n'), /\b(map|icon|connector|rail|card|cluster|growth|signal|website visual|market visual)\b/i);
});

test('shared stylesheet references are versioned everywhere', () => {
    const pages = ['index.html', 'en.html'];
    for (const dir of fs.readdirSync(path.join(__dirname, '..'))) {
        for (const name of ['index.html', 'en.html']) {
            const p = path.join(dir, name);
            if (fs.existsSync(path.join(__dirname, '..', p)) && /estavo-v3\.css/.test(fs.readFileSync(path.join(__dirname, '..', p), 'utf8'))) pages.push(p);
        }
    }
    assert.ok(pages.length >= 24);
    for (const p of pages) {
        const html = fs.readFileSync(path.join(__dirname, '..', p), 'utf8');
        for (const m of html.matchAll(/(?:href|src)="([^"]*\/(?:estavo-v3|home|home-critical|commercial|market)\.(?:css|js))(\?v=[^"]*)?"/g)) {
            assert.ok(m[2], `${p}: ${m[1]} has no version`);
        }
    }
});

test('homepage icons are inlined so they render on any host or sub-folder', () => {
    for (const file of ['index.html', 'en.html']) {
        const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
        assert.doesNotMatch(html, /estavo-home\.svg#/, `${file} must not depend on an external sprite`);
        const used = new Set([...html.matchAll(/href="#(i-[a-z0-9-]+)"/g)].map((m) => m[1]));
        const defined = new Set([...html.matchAll(/<symbol id="(i-[a-z0-9-]+)"/g)].map((m) => m[1]));
        assert.ok(used.size >= 8, "sprite is wired (every used id is checked below)");
        used.forEach((id) => assert.ok(defined.has(id), `${file}: icon #${id} is not defined`));
        assert.equal((html.match(/id="es-home-icons"/g) || []).length, 1);
    }
});

test('built stylesheet is reproducible from its v3 modules (no build drift)', () => {
    const order = ['tokens', 'base', 'layout', 'controls', 'header-footer', 'components', 'illustrations',
        'motion', 'utilities', 'responsive', 'premium'];
    const script = fs.readFileSync(path.join(__dirname, '../tools/build-css.sh'), 'utf8');
    assert.match(script, new RegExp(`for module in ${order.join(' ')};`));
    const normalise = (css) => css.split('\n').filter((line) => line.trim() && !line.startsWith('/* ── ')).join('\n');
    const built = fs.readFileSync(path.join(__dirname, '../assets/css/estavo-v3.css'), 'utf8')
        .split('\n').slice(3).join('\n');
    const modules = order.map((m) => fs.readFileSync(path.join(__dirname, `../assets/css/v3/${m}.css`), 'utf8')).join('\n');
    assert.equal(normalise(built), normalise(modules), 'estavo-v3.css differs from its sources — run sh tools/build-css.sh');
    assert.match(fs.readFileSync(path.join(__dirname, '../assets/css/v3/premium.css'), 'utf8'), /\.es-sticky-cta \{/);
});

