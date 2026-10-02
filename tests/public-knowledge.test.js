const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const { JSDOM } = require('jsdom');
const root = path.resolve(__dirname, '..');
const origin = 'https://estavo-brokers.com';
const articles = JSON.parse(fs.readFileSync(path.join(root, 'content/knowledge.json'), 'utf8'));
const route = (lang, slug = '') => '/guides/' + (lang === 'en' ? 'en/' : '') + (slug ? slug + '/' : '');
const readPage = (url) => fs.readFileSync(path.join(root, url, 'index.html'), 'utf8');
const localTarget = (pathname) => path.join(root, decodeURIComponent(pathname), pathname.endsWith('/') ? 'index.html' : '');

test('all six guides, two research studies and report have complete bilingual public pages', () => {
    assert.equal(articles.filter(a => a.kind === 'guide').length, 6);
    assert.equal(articles.filter(a => a.kind === 'case-study').length, 2);
    assert.equal(articles.filter(a => a.kind === 'report').length, 1);
    for (const lang of ['ar', 'en']) {
        for (const article of articles) {
            const url = route(lang, article.slug);
            const document = new JSDOM(readPage(url), { url: origin + url }).window.document;
            assert.equal(document.documentElement.lang, lang);
            assert.equal(document.documentElement.dir, lang === 'ar' ? 'rtl' : 'ltr');
            assert.equal(document.querySelector('h1').textContent, article[lang].title);
            assert.equal(document.querySelector('.answer').textContent, article[lang].answer);
            assert.equal(document.querySelector('link[rel=canonical]').href, origin + url);
            const alternate = document.querySelector(`link[hreflang=${lang === 'ar' ? 'en' : 'ar'}]`);
            assert.equal(alternate.href, origin + route(lang === 'ar' ? 'en' : 'ar', article.slug));
            const graph = JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent)['@graph'];
            const metadata = graph.find(node => node['@type'] === 'Article');
            assert.equal(metadata.headline, document.querySelector('h1').textContent);
            assert.equal(metadata.mainEntityOfPage['@id'], origin + url);
            const faq = graph.find(node => node['@type'] === 'FAQPage');
            assert.deepEqual(faq.mainEntity.map(q => q.name), [...document.querySelectorAll('#questions summary')].map(s => s.textContent));
            assert.ok(document.querySelectorAll('.prose > section').length >= 9);
            for (const link of document.querySelectorAll('a[href],link[rel=stylesheet],script[src],img[src]')) {
                const target = new URL(link.href || link.src, origin + url);
                if (target.origin !== origin) continue;
                assert.ok(fs.existsSync(localTarget(target.pathname)), `${url}: missing ${target.pathname}`);
                if (target.hash && target.pathname === url) assert.ok(document.getElementById(target.hash.slice(1)), `missing anchor ${target.hash}`);
            }
        }
        const hub = new JSDOM(readPage(route(lang))).window.document;
        assert.equal(hub.querySelectorAll('.topic-list li').length, 9);
        assert.ok(hub.getElementById('editorial'));
    }
});

test('sitemap points to existing files with canonical URLs and reciprocal language links', () => {
    const document = new JSDOM(fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8'), { contentType: 'text/xml' }).window.document;
    const urls = [...document.querySelectorAll('url > loc')].map(node => node.textContent);
    assert.equal(urls.length, 26);
    assert.equal(new Set(urls).size, urls.length);
    for (const value of urls) {
        const url = new URL(value);
        const target = localTarget(url.pathname);
        assert.ok(fs.existsSync(target), `sitemap missing ${url.pathname}`);
        const page = new JSDOM(fs.readFileSync(target, 'utf8'), { url: value }).window.document;
        assert.equal(page.querySelector('link[rel=canonical]').href, value);
    }
});

test('published research counts preserve scope, arithmetic and uncertainty', () => {
    const evidence = JSON.parse(fs.readFileSync(path.join(root, 'guides/evidence/september-2026.json'), 'utf8'));
    assert.equal(Object.values(evidence.by_category).reduce((a, b) => a + b, 0), evidence.records);
    assert.equal(evidence.records, 2268);
    assert.equal(evidence.archive.snapshots, 297);
    assert.equal(evidence.developer.recurring_offer_groups, 188);
    assert.equal(evidence.public_source_versions.length, 6);
    assert.equal(evidence.developer.change_flags_overlap, true);
    for (const metric of evidence.calculations) assert.equal(Math.round(metric.numerator / metric.denominator * 1000) / 10, metric.percent);
    for (const source of evidence.public_source_versions) {
        assert.match(source.sha256, /^[a-f0-9]{64}$/);
        assert.ok(source.url.startsWith('https://www.redseaway.co/'));
    }
    assert.ok(evidence.limitations.some(text => text.includes('not achieved transaction')));
    assert.ok(evidence.limitations.some(text => text.includes('unverified')));
    assert.ok(!JSON.stringify(evidence).includes('customer_phone'));
});

test('homepage navigation exposes guides and schema consistently names the Egyptian product', () => {
    for (const [filename, lang] of [['index.html', 'ar'], ['en.html', 'en']]) {
        const document = new JSDOM(fs.readFileSync(path.join(root, filename), 'utf8')).window.document;
        assert.ok(document.querySelector(`.nav-links a[href="${route(lang)}"]`));
        assert.ok(document.querySelector(`.nav-mobile a[href="${route(lang)}"]`));
        const graph = JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent)['@graph'];
        assert.equal(graph.find(node => node['@type'] === 'Organization').name, 'Estavo Brokers');
        assert.equal(graph.find(node => node['@type'] === 'SoftwareApplication').operatingSystem, 'Web');
    }
});

test('search discovery is allowed while internal files and training crawlers stay excluded', () => {
    const { execFileSync } = require('node:child_process');
    execFileSync('python3', ['-c', `
from pathlib import Path
from urllib.robotparser import RobotFileParser
parser=RobotFileParser()
parser.parse(Path('robots.txt').read_text().splitlines())
for bot in ['OAI-SearchBot','PerplexityBot','Claude-SearchBot','Googlebot','bingbot','Google-Extended']:
    assert parser.can_fetch(bot,'https://estavo-brokers.com/guides/')
    assert not parser.can_fetch(bot,'https://estavo-brokers.com/scripts/build_knowledge.py')
for bot in ['GPTBot','ClaudeBot','CCBot']:
    assert not parser.can_fetch(bot,'https://estavo-brokers.com/guides/')
`], { cwd: root });
});
