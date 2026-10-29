const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const { JSDOM } = require('jsdom');
const root = path.resolve(__dirname, '..');

test('public pages exclude the retired phone and preserve valid search metadata', () => {
    for (const entry of fs.readdirSync(root, { recursive: true })) {
        if (!entry.endsWith('.html') || entry.startsWith('node_modules/')) continue;
        const html = fs.readFileSync(path.join(root, entry), 'utf8');
        assert.doesNotMatch(html, /(?:\+?20)?(?:0)?109[\s-]*990[\s-]*3814/, entry);
        const document = new JSDOM(html).window.document;
        for (const script of document.querySelectorAll('script[type="application/ld+json"]')) {
            assert.doesNotThrow(() => JSON.parse(script.textContent), entry);
        }
    }
});
