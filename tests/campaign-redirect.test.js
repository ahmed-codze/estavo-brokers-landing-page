'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');
const { JSDOM } = require('jsdom');
const root = path.join(__dirname, '..');
const script = fs.readFileSync(path.join(root, 'go/index.html'), 'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
function redirect(query) {
    let target;
    const location = { search: '?' + query, protocol: 'https:', replace: value => { target = value; } };
    vm.runInNewContext(script, { URLSearchParams, window: { location }, location, document: { cookie: '' } });
    return new URL(target);
}
test('acquisition links open Market and retain attribution through the Market CTA', () => {
    for (const slug of ['creative-1-trial-event', 'creative-2-trial-event', 'creative-3-trial-event', 'outbound-free-v01', 'outbound-free-v02', 'outbound-free-v03', 'outbound-free-v04']) {
        const query = new URLSearchParams({ ref: slug, fbclid: 'click+with/encoded?characters', utm_source: 'fb', utm_medium: 'paid_social', utm_campaign: 'campaign-id', utm_adset: 'adset-id', utm_ad: 'ad-id', utm_content: 'creative 3', utm_term: 'broker' });
        const target = redirect(query);
        assert.equal(target.pathname, '/market/');
        query.forEach((value, key) => assert.equal(target.searchParams.get(key), value));
        const dom = new JSDOM(fs.readFileSync(path.join(root, 'market/index.html'), 'utf8'), { url: target.href, runScripts: 'outside-only' });
        dom.window.eval(fs.readFileSync(path.join(root, 'assets/js/referral.js'), 'utf8'));
        dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded'));
        const cta = new URL(dom.window.document.querySelector('a[data-position="hero"][data-track="market_opened"]').href);
        assert.equal(cta.origin, 'https://brokers.estavo.space');
        query.forEach((value, key) => assert.equal(cta.searchParams.get(key), value));
        dom.window.close();
    }
});
test('other referrals retain the homepage without forwarding unrelated parameters', () => {
    const target = redirect('ref=partner-code&fbclid=CLICK&next=https://example.com&token=secret');
    assert.equal(target.origin, 'https://estavo-brokers.com');
    assert.equal(target.pathname, '/');
    assert.equal(target.searchParams.get('fbclid'), 'CLICK');
    assert.equal(target.searchParams.has('next'), false);
    assert.equal(target.searchParams.has('token'), false);
});
test('invalid referrals retain the default fallback', () => {
    const target = redirect('ref=%2F%2Fevil.example&fbclid=CLICK');
    assert.equal(target.searchParams.get('ref'), 'default-landing-page');
    assert.equal(target.pathname, '/');
    assert.equal(target.searchParams.get('fbclid'), 'CLICK');
});

test('direct Market campaigns retain attribution and a secure referral across tabs', () => {
    for (let creative = 1; creative <= 4; creative++) {
        const slug = `outbound-free-v0${creative}`;
        const query = new URLSearchParams({ref: slug, fbclid: 'META_CLICK', utm_source: 'meta', utm_medium: 'paid_social', utm_campaign: 'campaign-id', utm_id: 'campaign-id', utm_term: 'adset-id', utm_content: 'ad-id', utm_adset: 'adset-id', utm_ad: 'ad-id'});
        const html = fs.readFileSync(path.join(root, 'market/index.html'), 'utf8');
        const referral = fs.readFileSync(path.join(root, 'assets/js/referral.js'), 'utf8');
        const dom = new JSDOM(html, {url: `https://estavo-brokers.com/market/?${query}`, runScripts: 'outside-only'});
        dom.window.eval(referral);
        dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded'));
        const destination = new URL(dom.window.document.querySelector('a[data-position="hero"][data-track="market_opened"]').href);
        query.forEach((value, key) => assert.equal(destination.searchParams.get(key), value));
        const cookie = dom.cookieJar.getCookiesSync('https://estavo-brokers.com/')[0];
        assert.equal(cookie.key, 'est_ref');
        assert.equal(cookie.value, slug);
        assert.equal(cookie.maxAge, 30 * 86400);
        assert.equal(cookie.secure, true);
        assert.equal(cookie.sameSite, 'lax');
        const returning = new JSDOM(html, {url: 'https://estavo-brokers.com/market/', cookieJar: dom.cookieJar, runScripts: 'outside-only'});
        returning.window.eval(referral);
        returning.window.document.dispatchEvent(new returning.window.Event('DOMContentLoaded'));
        assert.equal(new URL(returning.window.document.querySelector('a[data-position="hero"][data-track="market_opened"]').href).searchParams.get('ref'), slug);
        returning.window.close();
        dom.window.close();
    }
});

test('direct referral rewriting still works when session storage is unavailable', () => {
    const dom = new JSDOM('<a href="https://brokers.estavo.space">Market</a>', {url: 'https://estavo-brokers.com/market/?ref=outbound-free-v03&fbclid=CLICK', runScripts:'outside-only'});
    Object.defineProperty(dom.window, 'sessionStorage', {get() { throw new Error('blocked'); }});
    dom.window.eval(fs.readFileSync(path.join(root, 'assets/js/referral.js'), 'utf8'));
    dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded'));
    const url = new URL(dom.window.document.querySelector('a').href);
    assert.equal(url.searchParams.get('ref'), 'outbound-free-v03');
    assert.equal(url.searchParams.get('fbclid'), 'CLICK');
    dom.window.close();
});
