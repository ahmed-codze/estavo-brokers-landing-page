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
const SECTIONS = ['home-hero', 'home-market', 'home-request', 'home-website', 'home-client',
    'home-growth', 'home-start-free', 'home-faq', 'home-closing'];

function load(file) {
    const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
    return { html, doc: new JSDOM(html).window.document };
}

for (const [file, labels] of [
    ['index.html', { market: 'اكتشف السوق مجانًا', website: 'اعمل موقعك مجانًا', example: 'مثال توضيحي' }],
    ['en.html', { market: 'Explore the market free', website: 'Create your website free', example: 'Example' }],
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

    test(`${file}: no unverified proof figures, ROI or testimonials are rendered`, () => {
        const { doc } = load(file);
        const main = doc.querySelector('main');
        const visible = main.cloneNode(true);
        visible.querySelectorAll('template').forEach((t) => t.remove());
        const text = visible.textContent;
        assert.doesNotMatch(text, /30,000|2,000|7,000|\b700\b|26,169/);
        assert.equal(doc.querySelector('#home-roi'), null, 'ROI must stay inside a <template>');
        assert.ok(main.querySelector('template[data-conversion-archive="roi-pending-calculator"]'));
        assert.doesNotMatch(text, /REPLACE_ME/);
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
