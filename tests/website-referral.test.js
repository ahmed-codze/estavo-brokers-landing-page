'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const referral = require('../assets/js/website-referral.js');

test('normalizes supported social, provider, and official website URLs', () => {
    assert.equal(
        referral.normalizeSourceUrl(' instagram.com/estavo/#team '),
        'https://instagram.com/estavo/',
    );
    assert.equal(
        referral.normalizeSourceUrl('http://www.propertyfinder.eg/en/broker/company-123?listing=1'),
        'https://www.propertyfinder.eg/en/broker/company-123?listing=1',
    );
    assert.equal(
        referral.normalizeSourceUrl('https://www.bayut.eg/en/companies/company-123/#about'),
        'https://www.bayut.eg/en/companies/company-123/',
    );
    assert.equal(
        referral.normalizeSourceUrl('https://company.example.com/about'),
        'https://company.example.com/about',
    );
});

test('rejects unsafe and non-public source URLs', () => {
    [
        '',
        'javascript:alert(1)',
        'data:text/html,hello',
        'ftp://example.com/company',
        'localhost/company',
        'https://internal.local/company',
        'http://127.0.0.1/company',
        'http://2130706433/company',
        'https://[::1]/company',
        'https://user:secret@example.com/company',
        'https://example.com:8443/company',
        'not-a-public-host',
    ].forEach((value) => assert.equal(referral.normalizeSourceUrl(value), null, value));
});

test('always builds the handoff on the fixed Estavo onboarding endpoint', () => {
    const destination = referral.buildOnboardingUrl(
        'https://instagram.com/company?next=https://evil.example/redirect',
        'ar',
        {
            ref: 'Partner-42',
            utm_source: 'facebook',
            utm_campaign: 'enterprise-launch',
        },
    );
    const url = new URL(destination);

    assert.equal(url.origin, 'https://brokers.estavo.space');
    assert.equal(url.pathname, '/website/create');
    assert.equal(url.searchParams.get('locale'), 'ar');
    assert.equal(url.searchParams.get('ref'), 'partner-42');
    assert.equal(url.searchParams.get('utm_source'), 'facebook');
    assert.equal(url.searchParams.get('utm_campaign'), 'enterprise-launch');
    assert.equal(
        url.searchParams.get('source'),
        'https://instagram.com/company?next=https://evil.example/redirect',
    );
});

test('rejects unsupported locales and does not trust origin lookalikes', () => {
    assert.equal(
        referral.buildOnboardingUrl('https://instagram.com/company', 'fr', {}),
        null,
    );
    assert.equal(
        referral.isPlatformUrl('https://brokers.estavo.space/go/'),
        true,
    );
    assert.equal(
        referral.isPlatformUrl('https://brokers.estavo.space.evil.example/go/'),
        false,
    );
    assert.equal(
        referral.isPlatformUrl('https://brokers.estavo.space@evil.example/go/'),
        false,
    );
});

test('only the URL-only Arabic and English variants expose the website handoff', () => {
    const pages = [
        { file: 'website/index.html', locale: 'ar', input: 'website-source-ar' },
        { file: 'website/en.html', locale: 'en', input: 'website-source-en' },
    ];

    pages.forEach(({ file, locale, input }) => {
        const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
        const formCount = (html.match(/class="website-starter"/g) || []).length;

        assert.equal(formCount, 1, `${file} should contain one website starter`);
        assert.match(html, new RegExp(`class="website-starter" data-locale="${locale}"`));
        assert.match(html, /action="https:\/\/brokers\.estavo\.space\/website\/create"/);
        assert.match(html, new RegExp(`name="locale" value="${locale}"`));
        assert.match(html, new RegExp(`id="${input}" name="source"`));
        assert.match(html, new RegExp(`aria-describedby="${input}-hint ${input}-error"`));
        assert.match(html, new RegExp(`id="${input}-error" role="alert" aria-live="polite"`));
        assert.match(html, /maxlength="2048"/);
        assert.match(html, /assets\/js\/website-referral\.js/);
    });

    ['index.html', 'en.html'].forEach((file) => {
        const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');

        assert.doesNotMatch(html, /class="website-starter"/);
        assert.doesNotMatch(html, /assets\/js\/website-referral\.js/);
    });
});
