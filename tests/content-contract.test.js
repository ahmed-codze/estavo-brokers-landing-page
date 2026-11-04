'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');
const root = path.join(__dirname, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'tools/routes.json'), 'utf8'));
const clean = (s) => s.replace(/\s+/g, ' ').trim();

for (const lang of ['ar', 'en']) {
    test(`${lang}: generated header labels match their product destination`, () => {
        for (const route of manifest.routes.filter((r) => r.key !== 'home')) {
            const file = path.join(root, route.path, lang === 'ar' ? 'index.html' : 'en.html');
            const doc = new JSDOM(fs.readFileSync(file, 'utf8')).window.document;
            for (const a of doc.querySelectorAll('header a[data-track]')) {
                const label = clean(a.textContent);
                if (a.dataset.track === 'website_preview_started') {
                    assert.match(label, lang === 'ar' ? /موقع/ : /site/i, route.key);
                    assert.doesNotMatch(label, /Market|تصفح السوق/, route.key);
                }
                if (a.dataset.track === 'market_opened') {
                    assert.match(label, lang === 'ar' ? /السوق/ : /Market/, route.key);
                }
                if (a.dataset.track === 'integration_enquiry_submitted') {
                    assert.match(label, lang === 'ar' ? /الربط/ : /integration/i, route.key);
                }
            }
        }
    });

    test(`${lang}: service FAQ schema matches the published questions and answers`, () => {
        for (const route of manifest.routes.filter((r) => r.key !== 'home')) {
            const file = path.join(root, route.path, lang === 'ar' ? 'index.html' : 'en.html');
            const doc = new JSDOM(fs.readFileSync(file, 'utf8')).window.document;
            const schema = [...doc.querySelectorAll('script[type="application/ld+json"]')]
                .map((s) => JSON.parse(s.textContent)).find((s) => s['@type'] === 'FAQPage');
            if (!schema) continue;
            const section = doc.querySelector('#faq, .section-faq, section[aria-labelledby="faq-h"]');
            const visible = [...section.querySelectorAll('details')].map((item) => {
                const clone = item.cloneNode(true);
                const summary = clone.querySelector('summary');
                const name = clean(summary.textContent);
                summary.remove();
                clone.querySelectorAll('a').forEach((a) => a.remove());
                return { name, answer: clean(clone.textContent) };
            });
            assert.deepEqual(schema.mainEntity.map((q) => ({ name: q.name, answer: q.acceptedAnswer.text })), visible, route.key);
        }
    });
}
