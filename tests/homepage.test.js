'use strict';

/* Homepage contract (السوق · العقار · العميل refactor, 2026-10-03).
   Encodes the launch rules that are easy to erode by hand: the section
   budget, the two free entry points, no unverified proof figures, no ROI
   before the calculator ships, and analytics on deliberate clicks only. */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const MARKET = 'https://brokers.estavo.space/go/?ref=default-landing-page-market';
const WEBSITE = 'https://estavo-brokers.com/website/';
const PROOF = JSON.parse(fs.readFileSync(path.join(__dirname, '../tools/data/home-proof.json'), 'utf8'));
const MAP = JSON.parse(fs.readFileSync(path.join(__dirname, '../tools/data/egypt-map.json'), 'utf8'));
const SECTIONS = ['home-hero', 'home-market', 'home-request', 'home-website', 'home-client',
    'home-growth', 'home-start-free', 'home-faq', 'home-closing'];

function load(file) {
    const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
    return { html, doc: new JSDOM(html).window.document };
}

for (const [file, labels, labelKey] of [
    ['index.html', { market: 'اكتشف السوق مجانًا', website: 'اعمل موقعك مجانًا', example: 'مثال توضيحي' }, 'ar'],
    ['en.html', { market: 'Explore the market free', website: 'Create your website free', example: 'Example' }, 'en'],
]) {
    test(`${file}: exactly the nine homepage sections, in order`, () => {
        const { doc } = load(file);
        const ids = [...doc.querySelectorAll('main > section')].map((s) => s.id);
        assert.deepEqual(ids, SECTIONS);
        assert.equal(doc.querySelectorAll('h1').length, 1);
        assert.ok(doc.querySelector('#home-hero h1'));
    });

    test(`${file}: hero and closing offer both free doors, Market first`, () => {
        const { doc } = load(file);
        for (const id of ['home-hero', 'home-closing']) {
            const links = [...doc.querySelectorAll(`#${id} .es-home-actions a`)];
            assert.equal(links[0].href, MARKET);
            assert.equal(links[0].textContent.trim(), labels.market);
            assert.match(links[0].className, /es-home-btn--primary/);
            assert.equal(links[1].href, WEBSITE);
            assert.equal(links[1].textContent.trim(), labels.website);
        }
        const sticky = doc.querySelector('[data-home-sticky] a');
        assert.equal(sticky.href, MARKET);
        assert.equal(doc.querySelectorAll('[data-home-sticky] a').length, 1);
    });

    test(`${file}: proof strip shows the configured verified figures, never rounded up`, () => {
        const { doc } = load(file);
        const items = [...doc.querySelectorAll('#home-hero [data-proof]')];
        assert.equal(items.length, PROOF.figures.length);
        for (const item of items) {
            const figure = PROOF.figures.find((f) => f.key === item.dataset.proof);
            assert.ok(figure, item.dataset.proof);
            assert.ok(figure.display <= figure.verified, `${figure.key} rounds above ${figure.verified}`);
            const value = item.querySelector('.es-home-proof__value');
            // The final value ships in the HTML so no-JS readers see the real proof.
            assert.equal(value.textContent.trim(), `${figure.display.toLocaleString('en-US')}+`);
            assert.equal(Number(value.dataset.count), figure.display);
        }
        // Superseded / overstated figures must not reappear anywhere visible.
        const visible = doc.querySelector('main').cloneNode(true);
        visible.querySelectorAll('template').forEach((t) => t.remove());
        assert.doesNotMatch(visible.textContent, /30,000|7,000|26,169|2,412/);
    });

    test(`${file}: ROI is prepared but not rendered, and exposes no methodology`, () => {
        const { doc } = load(file);
        const template = doc.querySelector('template[data-conversion-archive="roi-pending-calculator"]');
        assert.ok(template);
        assert.equal(template.dataset.featureState, 'unavailable');
        assert.equal(doc.querySelector('#home-roi'), null, 'ROI must stay inside a <template>');
        const roi = template.content.textContent;
        assert.doesNotMatch(roi, /formula|weight|coefficient|model|معادلة|وزن|أوزان|معامل|%|[=×÷]/i);
        assert.doesNotMatch(roi, /\d+(\.\d+)?\s*(%|M\b|مليون)/, 'no sample ROI numbers');
    });

    test(`${file}: testimonials are gone completely`, () => {
        const { html } = load(file);
        assert.doesNotMatch(html, /testimonial|REPLACE_ME|شهادات عملائنا/i);
    });

    test(`${file}: website section sends both CTAs to creation, never to examples`, () => {
        const { doc } = load(file);
        const links = [...doc.querySelectorAll('#home-website .es-home-copy a')];
        assert.equal(links.length, 2);
        links.forEach((a) => assert.equal(a.href, WEBSITE));
        const main = doc.querySelector('main');
        assert.equal(main.querySelector('a[href*="examples/"]'), null);
        assert.doesNotMatch(main.textContent, /شوف مثال لموقع|شوف موقع شغال|see an? (example|live) website/i);
    });

    test(`${file}: market map is the real Egypt outline with validated city points`, () => {
        const { doc } = load(file);
        const land = doc.querySelector('#home-market .es-home-map__land');
        assert.ok(land);
        assert.equal(land.getAttribute('d'), MAP.path, 'map path must come from tools/data/egypt-map.json');
        assert.ok(MAP.points > 80, 'outline must be a real boundary, not a placeholder shape');
        assert.match(MAP.source, /Natural Earth/);
        assert.ok(doc.querySelectorAll('#home-market .es-home-map__nile').length >= 1, 'Nile drawn from Natural Earth');
        // Every city is drawn; markets and reference cities are visually distinct tiers.
        const markets = MAP.nodes.filter((n) => n.tier === 'market');
        const refs = MAP.nodes.filter((n) => n.tier === 'ref');
        assert.ok(markets.length >= 10 && refs.length >= 15, 'main cities across Egypt are plotted');
        assert.equal(doc.querySelectorAll('.es-home-map__node--ref').length, refs.length);
        assert.equal(doc.querySelectorAll('.es-home-map__node:not(.es-home-map__node--ref)').length, markets.length);
        assert.equal(doc.querySelectorAll('.es-home-map__node--selected').length, 1);
        // Coordinates stay inside Egypt's real extent (the generator also checks them against the outline).
        MAP.nodes.forEach((n) => {
            assert.ok(n.lat > 22 && n.lat < 31.7 && n.lon > 24.6 && n.lon < 37, n.key);
        });
        const labels = [...doc.querySelectorAll('.es-home-map__label:not(.es-home-map__label--caption)')]
            .map((li) => li.textContent.trim());
        assert.deepEqual(labels.sort(), MAP.nodes.filter((n) => n.label).map((n) => n[labelKey]).sort());
        // Every city name is available to assistive tech, labelled or not.
        const aria = doc.querySelector('.es-home-map').getAttribute('aria-label');
        MAP.nodes.forEach((n) => assert.ok(aria.includes(n[labelKey]), n.key));
        assert.ok(doc.querySelector('.es-home-map__legend'));
    });

    test(`${file}: every demonstration is labelled as an example`, () => {
        const { doc } = load(file);
        for (const selector of ['.es-home-intel', '[data-home-market]', '[data-home-request]',
            '[data-home-site]', '[data-home-signals]', '[data-home-clusters]']) {
            assert.ok(doc.querySelector(selector).textContent.includes(labels.example), selector);
        }
    });

    test(`${file}: request demo flags the over-budget option in text, consistently`, () => {
        const { doc } = load(file);
        const cards = [...doc.querySelectorAll('.es-home-prop')];
        assert.equal(cards.length, 3);
        assert.equal(doc.querySelectorAll('.es-home-prop--best').length, 1);
        const outside = doc.querySelector('.es-home-prop--outside');
        assert.match(outside.textContent, /8\.3M/);
        assert.match(outside.querySelector('.es-home-reason').textContent, /300/);
    });

    test(`${file}: homepage events are attached to deliberate links only`, () => {
        const { doc } = load(file);
        const events = [...doc.querySelectorAll('[data-home-event]')];
        assert.ok(events.length >= 8);
        events.forEach((el) => assert.equal(el.tagName, 'A'));
        const names = new Set(events.map((el) => el.dataset.homeEvent));
        for (const name of ['home_market_free_click', 'home_website_free_click', 'home_ai_request_demo_click',
            'home_client_insights_click', 'home_meta_click', 'home_pricing_click', 'home_enterprise_click',
            'home_resale_click']) {
            assert.ok(names.has(name), name);
        }
        // Existing funnel events keep firing alongside the new names.
        doc.querySelectorAll(`a[href="${MARKET}"][data-home-event]`)
            .forEach((a) => assert.equal(a.dataset.track, 'market_opened'));
    });

    test(`${file}: FAQ structured data mirrors the visible FAQ`, () => {
        const { doc } = load(file);
        const graph = JSON.parse(doc.querySelector('script[type="application/ld+json"]').textContent)['@graph'];
        const faq = graph.find((node) => node['@type'] === 'FAQPage');
        const visible = [...doc.querySelectorAll('#home-faq summary')].map((s) => s.textContent.replace(/\s+/g, ' ').trim());
        assert.deepEqual(faq.mainEntity.map((q) => q.name), visible);
        assert.equal(doc.querySelectorAll('#home-faq details[open]').length, 0);
    });
}

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

test('homepage CSS/JS carry no testimonial remnants; future art backlog is mascot-only', () => {
    for (const file of ['assets/css/home.css', 'assets/js/home.js']) {
        assert.doesNotMatch(fs.readFileSync(path.join(__dirname, '..', file), 'utf8'), /testimonial/i, file);
    }
    for (const file of ['index.html', 'en.html']) {
        const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
        const backlog = [...html.matchAll(/backlog[^\n]*/gi)].map((m) => m[0]);
        assert.ok(backlog.length >= 2, `${file} keeps the mascot slots documented`);
        backlog.forEach((line) => assert.match(line, /pose/i, `${file}: non-mascot backlog item: ${line}`));
    }
    const agents = fs.readFileSync(path.join(__dirname, '../AGENTS.md'), 'utf8');
    const section = agents.split('### Remaining homepage art backlog')[1].split('\n#')[0]
        .split('\n').filter((line) => /^\d+\./.test(line)).join('\n');
    assert.equal(section.split('\n').length, 3, 'backlog lists exactly the three mascot poses');
    assert.doesNotMatch(section, /\b(map|icon|connector|rail|card|cluster|growth|signal|website visual|market visual)\b/i);
    assert.match(section, /pose/i);
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
