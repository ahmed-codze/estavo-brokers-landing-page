'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');
const { JSDOM } = require('jsdom');
const referral = require('../assets/js/website-referral.js');

const catalog = { data: { cities: [
    { id: 1, name: { en: 'New Cairo', ar: 'القاهرة الجديدة' }, units_count: 42 },
    { id: 6, name: { en: 'North Coast', ar: 'الساحل الشمالي' }, units_count: 10 },
] } };
const tick = () => new Promise(resolve => setImmediate(resolve));

async function openWizard(t, options = {}) {
    const locale = options.locale || 'en';
    const dom = new JSDOM(fs.readFileSync(path.join(__dirname, '../website/', locale === 'ar' ? 'index.html' : 'en.html'), 'utf8'), {
        url: `https://estavo-brokers.com/website/${locale === 'en' ? 'en.html' : ''}${options.query || ''}`,
    });
    t.after(() => dom.window.close());
    await new Promise(resolve => dom.window.document.addEventListener('DOMContentLoaded', resolve, { once: true }));
    const { window } = dom;
    const destinations = [];
    Object.entries(options.storage || {}).forEach(([key, value]) => window.sessionStorage.setItem(key, value));
    const facade = {
        location: { href: window.location.href, search: window.location.search, origin: window.location.origin, assign: url => destinations.push(url) },
        sessionStorage: options.blockStorage ? { getItem() { throw new Error('blocked'); }, setItem() { throw new Error('blocked'); } } : window.sessionStorage,
        fetch: options.fetch || (() => Promise.resolve({ ok: true, json: async () => catalog })),
        setTimeout: options.setTimeout || window.setTimeout.bind(window),
        clearTimeout: window.clearTimeout.bind(window),
        AbortController: window.AbortController,
        addEventListener: window.addEventListener.bind(window),
    };
    referral.bootstrap(facade, window.document);
    await tick();
    const document = window.document;
    const form = document.querySelector('[data-manual-form]');
    const input = (name, value) => {
        form.elements[name].value = value;
        form.elements[name].dispatchEvent(new window.Event('input', { bubbles: true }));
    };
    const next = () => document.querySelector('[data-manual-next]').click();
    const enter = name => form.elements[name].dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true }));
    const submit = () => form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
    const step = () => Number(form.querySelector('[data-manual-step]:not([hidden])').dataset.manualStep);
    const storage = () => Object.fromEntries(Object.keys(window.sessionStorage).map(key => [key, window.sessionStorage.getItem(key)]));
    return { window, document, form, destinations, input, next, enter, submit, step, storage };
}

async function reachContacts(wizard) {
    wizard.document.querySelector('[data-next-panel="manual"]').click();
    await tick();
    wizard.input('display_name', 'Mona Broker');
    wizard.enter('display_name');
    assert.equal(wizard.step(), 2);
    wizard.next();
    wizard.form.querySelector('input[name="cities"]').click();
    wizard.next();
    wizard.next();
    assert.equal(wizard.step(), 5);
}

test('both languages complete the keyboard flow and produce one validated handoff', async t => {
    for (const locale of ['ar', 'en']) {
        const wizard = await openWizard(t, { locale, query: '?ref=campaign&for_lead=71&parent_website=23&parent_customer=45&utm_source=facebook' });
        await reachContacts(wizard);
        wizard.submit();
        assert.equal(wizard.step(), 5);
        assert.equal(wizard.form.elements.public_phone.getAttribute('aria-invalid'), 'true');
        wizard.input('public_phone', '٠١٠ ١٢٣٤ ٥٦٧٨');
        wizard.form.querySelector('[data-whatsapp-same]').click();
        wizard.enter('public_phone');
        assert.equal(wizard.step(), 5);
        assert.equal(wizard.form.querySelectorAll('[data-manual-step]').length, 5);
        assert.equal(wizard.document.querySelector('#photo-title'), null);
        assert.equal(wizard.document.querySelector('[data-manual-next]').hidden, true);
        assert.equal(wizard.document.querySelector('[data-manual-submit]').hidden, false);
        wizard.submit();
        wizard.submit();
        assert.equal(wizard.destinations.length, 1);
        const url = new URL(wizard.destinations[0]);
        assert.equal(url.searchParams.get('locale'), locale);
        assert.equal(url.searchParams.get('for_lead'), '71');
        assert.equal(url.searchParams.get('parent_website'), '23');
        assert.equal(url.searchParams.get('parent_customer'), '45');
        assert.equal(url.searchParams.get('utm_source'), 'facebook');
        assert.equal(new URL(url.searchParams.get('source')).searchParams.get('whatsapp'), '+201012345678');
    }
});

test('final validation returns to the invalid visible step and focuses the field', async t => {
    const wizard = await openWizard(t);
    await reachContacts(wizard);
    wizard.input('public_phone', '01012345678');
    wizard.input('whatsapp_phone', '01012345678');
    wizard.input('display_name', '');
    wizard.submit();
    assert.equal(wizard.step(), 1);
    assert.equal(wizard.document.activeElement, wizard.form.elements.display_name);
    assert.match(wizard.form.querySelector('[data-manual-error]').textContent, /Enter the name/);
    assert.equal(wizard.destinations.length, 0);
});

test('city timeout exposes retry, deduplicates pending requests, and recovers', async t => {
    let timeout;
    let calls = 0;
    const wizard = await openWizard(t, {
        setTimeout(callback, delay) { if (delay === 15000) timeout = callback; return 1; },
        fetch() {
            calls += 1;
            return calls === 1 ? new Promise(() => {}) : Promise.resolve({ ok: true, json: async () => catalog });
        },
    });
    const open = () => wizard.document.querySelector('[data-next-panel="manual"]').click();
    open();
    open();
    await tick();
    assert.equal(calls, 1);
    timeout();
    await tick();
    assert.equal(wizard.document.querySelector('[data-city-retry]').hidden, false);
    assert.match(wizard.document.querySelector('[data-city-status]').textContent, /Could not load/);
    wizard.document.querySelector('[data-city-retry]').click();
    await tick();
    assert.equal(calls, 2);
    assert.equal(wizard.form.querySelectorAll('input[name="cities"]').length, 2);
    assert.equal(wizard.document.querySelector('[data-city-grid]').hasAttribute('aria-busy'), false);
});

test('reload/language changes restore the same-tab draft without crossing customer contexts', async t => {
    const original = await openWizard(t, { query: '?for_lead=71&audience=individual' });
    await reachContacts(original);
    original.input('public_phone', '01012345678');
    original.form.querySelector('[data-whatsapp-same]').click();
    original.input('instagram_url', 'instagram.com/mona');
    const storage = original.storage();
    const restored = await openWizard(t, { locale: 'ar', query: '?for_lead=71&audience=individual', storage });
    assert.equal(restored.step(), 5);
    assert.equal(restored.document.querySelector('[data-panel="manual"]').hidden, false);
    assert.equal(restored.form.elements.display_name.value, 'Mona Broker');
    assert.equal(restored.form.elements.whatsapp_phone.value, '01012345678');
    assert.equal(restored.form.querySelector('input[name="cities"]').checked, true);
    assert.equal(restored.form.querySelector('[data-whatsapp-same]').checked, true);
    const other = await openWizard(t, { query: '?for_lead=72&audience=individual', storage });
    assert.equal(other.form.elements.display_name.value, '');
    assert.equal(other.step(), 1);
    const expired = Object.fromEntries(Object.entries(storage).map(([key, value]) => [key, key.startsWith('est_website_draft') ? JSON.stringify({ ...JSON.parse(value), savedAt: 0 }) : value]));
    const stale = await openWizard(t, { query: '?for_lead=71&audience=individual', storage: expired });
    assert.equal(stale.form.elements.display_name.value, '');
});

test('blocked draft storage does not interrupt setup, and editing WhatsApp unchecks same-number', async t => {
    const wizard = await openWizard(t, { blockStorage: true });
    await reachContacts(wizard);
    wizard.input('public_phone', '01012345678');
    wizard.form.querySelector('[data-whatsapp-same]').click();
    wizard.input('whatsapp_phone', '01112345678');
    assert.equal(wizard.form.querySelector('[data-whatsapp-same]').checked, false);
    wizard.input('public_phone', '01212345678');
    assert.equal(wizard.form.elements.whatsapp_phone.value, '01112345678');
    wizard.next();
    wizard.submit();
    assert.equal(wizard.destinations.length, 1);
});

test('company link guidance does not trap focus and preserves campaign handoff', async t => {
    const wizard = await openWizard(t, { query: '?audience=company&utm_campaign=launch' });
    const input = wizard.document.querySelector('input[name="source"]');
    const back = wizard.document.querySelector('[data-panel="link"] [data-back-panel]');
    input.value = 'facebook.com';
    back.focus();
    input.dispatchEvent(new wizard.window.Event('blur'));
    assert.equal(wizard.document.activeElement, back);
    assert.equal(input.getAttribute('aria-invalid'), 'true');
    input.value = 'facebook.com/company';
    wizard.document.querySelector('.website-starter').dispatchEvent(new wizard.window.Event('submit', { cancelable: true }));
    const destination = new URL(wizard.destinations[0]);
    assert.equal(destination.searchParams.get('audience'), 'company');
    assert.equal(destination.searchParams.get('utm_campaign'), 'launch');
});

test('Arabic/Persian digits and pasted directional markers normalize to a dialable number', () => {
    assert.equal(referral.normalizePhoneNumber('\u2066+٢٠ ١٠١٢٣٤٥٦٧٨\u2069'), '+201012345678');
    assert.equal(referral.normalizePhoneNumber('۰۱۰۱۲۳۴۵۶۷۸'), '+201012345678');
    assert.equal(referral.normalizePhoneNumber('٠١٠bad١٢٣٤٥٦٧٨'), null);
});

test('manual profile JSON-LD cannot escape its script element through the broker name', t => {
    const probe = spawnSync('php', ['--version'], { encoding: 'utf8' });
    if (probe.error && probe.error.code === 'ENOENT') return t.skip('PHP CLI is required for the server-rendered profile regression.');
    const name = '</script><script>alert(1)</script>';
    const php = `$_SERVER['PATH_INFO'] = '/abcdef0123456789abcdef01'; $_GET = json_decode($argv[1], true); require $argv[2];`;
    const result = spawnSync('php', ['-r', php, JSON.stringify({ name, theme: 'modern_line', city_ids: '1' }), path.join(__dirname, '../website/manual-profile.php')], { encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr);
    const dom = new JSDOM(result.stdout);
    t.after(() => dom.window.close());
    assert.equal(dom.window.document.scripts.length, 1);
    assert.equal(JSON.parse(dom.window.document.scripts[0].textContent).name, name);
    assert.equal(dom.window.document.querySelector('h1').textContent, name);
});


test('floating help follows active wizard panels without scroll observers', async t => {
    for (const locale of ['ar', 'en']) {
        const wizard = await openWizard(t, { locale });
        const active = () => wizard.document.body.getAttribute('data-website-wizard-active');
        assert.notEqual(active(), 'true');
        await reachContacts(wizard);
        assert.equal(active(), 'true');
        wizard.document.querySelector('[data-panel="manual"] [data-back-panel]').click();
        assert.equal(active(), 'false');
        wizard.document.querySelector('[data-next-panel="link"]').click();
        assert.equal(active(), 'true');
        wizard.document.querySelector('[data-panel="link"] [data-back-panel]').click();
        assert.equal(active(), 'false');
        const restored = await openWizard(t, { locale, query: '?audience=individual' });
        assert.equal(restored.document.body.getAttribute('data-website-wizard-active'), 'true');
    }
});
