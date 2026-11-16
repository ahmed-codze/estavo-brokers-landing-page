'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');
const { applyDaily } = require('../tools/daily/render');

// Exercise the same parse/serialize path used by production daily editions.
const edition = { snapshot_date: '2026-11-15', units: [], projects: [], developers: [], news: [], launches: [], jobs: [] };
for (const [file, lang] of [['index.html', 'ar'], ['en.html', 'en']]) {
  for (const prefix of ['tools/home/', '']) {
    test(`${prefix}${file}: sharing metadata survives daily publication`, () => {
      const source = fs.readFileSync(path.join(__dirname, '..', prefix + file), 'utf8');
      for (const html of [source, applyDaily(source, 'home', lang, edition)]) {
        const dom = new JSDOM(html);
        const { head, body } = dom.window.document;
        assert.ok(head.querySelector('title')?.textContent.trim());
        for (const property of ['og:title', 'og:description', 'og:url', 'og:image']) {
          assert.ok(head.querySelector(`meta[property="${property}"]`)?.content, property);
        }
        assert.equal(head.querySelector('meta[property="og:image"]').content, `https://estavo-brokers.com/assets/og/og-${lang}.jpg`);
        assert.ok(head.querySelector('meta[name="twitter:image"]'));
        assert.ok(head.querySelector('link[rel="canonical"]'));
        assert.equal(body.querySelectorAll('meta[property^="og:"]').length, 0);
        assert.equal(body.querySelectorAll('noscript img[src*="facebook.com/tr"]').length, 1);
        dom.window.close();
      }
    });
  }
}
