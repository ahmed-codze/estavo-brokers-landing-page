'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const { JSDOM } = require('jsdom');

const referral = require('../assets/js/website-referral.js');

const ESTAVO_PERSONAL_THEMES = [
    'modern_line', 'modern_axis', 'modern_frame', 'modern_signal', 'modern_studio',
    'monogram_stamp', 'monogram_block', 'monogram_orbit', 'monogram_grid', 'monogram_signature',
    'serif_editorial', 'serif_classic', 'serif_gallery', 'serif_column', 'serif_masthead',
];
const NEW_CAIRO = { id: 1, name_en: 'New Cairo', name_ar: 'القاهرة الجديدة' };
const NORTH_COAST = { id: 6, name_en: 'North Coast', name_ar: 'الساحل الشمالي' };
const CONTACT = {
    public_phone: '01012345678',
    whatsapp_phone: '+20 100 987 6543',
    facebook: 'facebook.com/ahmed.mansour',
    instagram: 'https://instagram.com/ahmed.mansour/',
};

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
            utm_adset: 'company-owners',
            utm_ad: 'finished-site-demo',
            fbclid: 'META_CLICK_123',
        },
        6748,
    );
    const url = new URL(destination);

    assert.equal(url.origin, 'https://brokers.estavo.space');
    assert.equal(url.pathname, '/website/create');
    assert.equal(url.searchParams.get('locale'), 'ar');
    assert.equal(url.searchParams.get('audience'), 'company');
    assert.equal(url.searchParams.get('for_user'), '6748');
    assert.equal(url.searchParams.get('ref'), 'partner-42');
    assert.equal(url.searchParams.get('utm_source'), 'facebook');
    assert.equal(url.searchParams.get('utm_campaign'), 'enterprise-launch');
    assert.equal(url.searchParams.get('utm_adset'), 'company-owners');
    assert.equal(url.searchParams.get('utm_ad'), 'finished-site-demo');
    assert.equal(url.searchParams.get('fbclid'), 'META_CLICK_123');
    assert.equal(
        url.searchParams.get('source'),
        'https://instagram.com/company?next=https://evil.example/redirect',
    );
});

test('builds a validated manual freelancer handoff with attribution', () => {
    const destination = referral.buildManualOnboardingUrl({
        name: '  أحمد منصور  ',
        theme: 'modern_line',
        cities: [NEW_CAIRO, NORTH_COAST, NEW_CAIRO],
        contact: CONTACT,
    }, 'ar', {
        ref: 'Partner-42',
        utm_source: 'facebook',
    });
    const url = new URL(destination);

    assert.equal(url.origin, 'https://brokers.estavo.space');
    assert.equal(url.pathname, '/website/create');
    const source = new URL(url.searchParams.get('source'));
    assert.equal(source.origin, 'https://estavo-brokers.com');
    assert.match(source.pathname, /^\/website\/manual-profile\.php\/[a-f0-9]{24,32}$/);
    assert.equal(source.searchParams.get('name'), 'أحمد منصور');
    assert.equal(source.searchParams.get('theme'), 'modern_line');
    assert.equal(source.searchParams.get('city_ids'), '1,6');
    assert.equal(source.searchParams.get('phone'), '+201012345678');
    assert.equal(source.searchParams.get('whatsapp'), '+201009876543');
    assert.equal(source.searchParams.get('facebook'), 'https://www.facebook.com/ahmed.mansour');
    assert.equal(source.searchParams.get('instagram'), 'https://www.instagram.com/ahmed.mansour/');
    assert.equal(source.searchParams.get('property_finder_choice'), 'later');
    assert.equal(source.searchParams.has('property_finder_url'), false);
    assert.equal(source.searchParams.has('city_names_en'), false);
    assert.equal(source.searchParams.has('city_names_ar'), false);
    assert.equal(url.searchParams.get('mode'), 'manual');
    assert.equal(url.searchParams.get('fresh_start'), '1');
    assert.equal(url.searchParams.get('audience'), 'individual');
    assert.equal(url.searchParams.get('name'), 'أحمد منصور');
    assert.equal(url.searchParams.get('theme'), 'modern_line');
    assert.equal(url.searchParams.get('city_ids'), '1,6');
    assert.equal(url.searchParams.get('locale'), 'ar');
    assert.equal(url.searchParams.get('ref'), 'partner-42');
    assert.equal(url.searchParams.get('utm_source'), 'facebook');
});

test('rejects incomplete or tampered manual website profiles', () => {
    assert.equal(referral.buildManualOnboardingUrl({ name: '', theme: 'modern_line', cities: [NEW_CAIRO], contact: CONTACT }, 'en', {}), null);
    assert.equal(referral.buildManualOnboardingUrl({ name: 'Jane', theme: 'hacked', cities: [NEW_CAIRO], contact: CONTACT }, 'en', {}), null);
    assert.equal(referral.buildManualOnboardingUrl({ name: 'Jane', theme: 'modern_line', cities: [], contact: CONTACT }, 'en', {}), null);
    assert.equal(referral.buildManualOnboardingUrl({ name: 'Jane', theme: 'modern_line', cities: [{ id: '../../bad', name_en: 'Bad' }], contact: CONTACT }, 'en', {}), null);
    assert.equal(referral.buildManualOnboardingUrl({ name: 'Jane', theme: 'modern_line', cities: [NEW_CAIRO] }, 'en', {}), null);
    assert.equal(referral.buildManualOnboardingUrl({ name: 'Jane', theme: 'modern_line', cities: [NEW_CAIRO], contact: { ...CONTACT, facebook: 'https://evil.example/jane' } }, 'en', {}), null);
});

test('carries a validated CRM customer through manual website creation', () => {
    const destination = referral.buildManualOnboardingUrl({
        name: 'Rehab Reda',
        theme: 'modern_line',
        cities: [NEW_CAIRO],
        contact: CONTACT,
    }, 'en', {}, '6748');
    const url = new URL(destination);

    assert.equal(url.searchParams.get('for_user'), '6748');
    assert.equal(url.searchParams.get('mode'), 'manual');
    assert.equal(referral.normalizeOwnerUserId('0'), null);
    assert.equal(referral.normalizeOwnerUserId('6748x'), null);
});

test('carries an unregistered CRM lead through both website creation paths', () => {
    const linked = new URL(referral.buildOnboardingUrl(
        'https://www.facebook.com/new.broker',
        'en',
        {},
        null,
        91,
    ));
    const manual = new URL(referral.buildManualOnboardingUrl({
        name: 'New Broker',
        theme: 'modern_line',
        cities: [NEW_CAIRO],
        contact: CONTACT,
    }, 'en', {}, null, 91));

    assert.equal(linked.searchParams.get('for_lead'), '91');
    assert.equal(linked.searchParams.has('for_user'), false);
    assert.equal(manual.searchParams.get('for_lead'), '91');
    assert.equal(manual.searchParams.has('for_user'), false);
});

test('normalizes Egyptian contacts and validates optional social profiles', () => {
    assert.equal(referral.normalizePhoneNumber('010 1234 5678'), '+201012345678');
    assert.equal(referral.normalizePhoneNumber('00201012345678'), '+201012345678');
    assert.equal(referral.normalizePhoneNumber('+971 50 123 4567'), '+971501234567');
    assert.equal(referral.normalizePhoneNumber('123'), null);
    assert.equal(referral.normalizeSocialProfile('facebook.com/jane.broker', 'facebook'), 'https://www.facebook.com/jane.broker');
    assert.equal(referral.normalizeSocialProfile('instagram.com/jane.broker/', 'instagram'), 'https://www.instagram.com/jane.broker/');
    assert.equal(referral.normalizeSocialProfile('', 'instagram'), '');
    assert.equal(referral.normalizeSocialProfile('https://evil.example/jane', 'instagram'), null);
});

test('only accepts an explicitly supplied Property Finder broker page', () => {
    const propertyFinderUrl = 'https://www.propertyfinder.eg/ar/broker/darak-madinaty-4316';
    assert.equal(
        referral.normalizePropertyFinderProfile('propertyfinder.eg/ar/broker/darak-madinaty-4316?ignored=1'),
        propertyFinderUrl,
    );
    assert.equal(referral.normalizePropertyFinderProfile('https://propertyfinder.eg/'), null);
    assert.equal(referral.normalizePropertyFinderProfile('https://evil.example/ar/broker/darak-4316'), null);

    const destination = referral.buildManualOnboardingUrl({
        name: 'Ahmed Mansour',
        theme: 'modern_line',
        cities: [NEW_CAIRO],
        property_finder_choice: 'connect',
        property_finder_url: propertyFinderUrl,
        contact: CONTACT,
    }, 'en', {});
    const source = new URL(new URL(destination).searchParams.get('source'));
    assert.equal(source.searchParams.get('property_finder_choice'), 'connect');
    assert.equal(source.searchParams.get('property_finder_url'), propertyFinderUrl);

    assert.equal(referral.buildManualOnboardingUrl({
        name: 'Ahmed Mansour',
        theme: 'modern_line',
        cities: [NEW_CAIRO],
        property_finder_choice: 'connect',
        property_finder_url: 'https://evil.example/broker/1',
        contact: CONTACT,
    }, 'en', {}), null);
});

test('keeps the largest allowed city selection inside the API source limit', () => {
    const cities = Array.from({ length: 50 }, (_, index) => ({
        id: index + 1,
        name_en: `Long English city name ${index + 1}`,
        name_ar: `مدينة طويلة ${index + 1}`,
    }));
    const destination = referral.buildManualOnboardingUrl({
        name: 'A'.repeat(80),
        theme: 'modern_line',
        cities,
        contact: CONTACT,
    }, 'en', {});
    const source = new URL(new URL(destination).searchParams.get('source'));

    assert.ok(source.toString().length <= 2048);
    assert.equal(source.searchParams.get('city_ids').split(',').length, 50);
});

test('accepts every implemented Estavo personal theme', () => {
    ESTAVO_PERSONAL_THEMES.forEach((theme) => {
        const profile = referral.normalizeManualProfile({
            name: 'Jane Broker',
            theme,
            cities: [NEW_CAIRO],
            contact: CONTACT,
        });

        assert.equal(profile.theme, theme);
    });
});

test('normalizes the live Estavo city catalog by canonical ID', () => {
    assert.deepEqual(referral.normalizeCityCatalog({ data: { cities: [
        { id: 6, name: { en: 'North Coast', ar: 'الساحل الشمالي' }, units_count: 47 },
        { id: 1, name: { en: 'New Cairo', ar: 'القاهرة الجديدة' }, units_count: 128 },
        { id: 6, name: { en: 'Duplicate', ar: 'مكرر' }, units_count: 99 },
        { id: 9, name: { en: 'Empty City', ar: 'مدينة فارغة' }, units_count: 0 },
        { id: 'bad', name: { en: 'Invalid' } },
    ] } }), [
        { ...NEW_CAIRO, units_count: 128 },
        { ...NORTH_COAST, units_count: 47 },
    ]);
});

test('keeps valid cities visible while an older cached catalog has no counts', () => {
    assert.deepEqual(referral.normalizeCityCatalog({ data: { cities: [
        { id: 1, name: { en: 'New Cairo', ar: 'القاهرة الجديدة' } },
    ] } }), [{ ...NEW_CAIRO, units_count: null }]);
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

test('classifies sources so the UI can explain the specific problem', () => {
    // Bare platform roots identify no company, so they must be sent back.
    ['facebook.com', 'https://facebook.com/', 'www.instagram.com', 'bayut.eg', 'https://propertyfinder.eg/']
        .forEach((value) => {
            assert.equal(
                referral.classifySource(value).reason,
                'platform-root',
                `${value} should be reported as a bare platform root`,
            );
        });

    // Real company pages on those same platforms must pass.
    ['instagram.com/acme', 'https://www.facebook.com/acme-realty', 'https://bayut.eg/en/companies/acme']
        .forEach((value) => {
            assert.equal(referral.classifySource(value).ok, true, `${value} should be accepted`);
        });

    assert.equal(referral.classifySource('').reason, 'empty');
    assert.equal(referral.classifySource('not a url').reason, 'malformed');

    // The classifier must never accept what normalizeSourceUrl rejects.
    ['javascript:alert(1)', 'http://localhost/x', 'https://127.0.0.1/x', 'https://user:pw@example.com/']
        .forEach((value) => {
            assert.equal(referral.classifySource(value).ok, false, `${value} must stay rejected`);
        });

    // A missing scheme is repaired rather than rejected.
    assert.equal(referral.classifySource('instagram.com/acme').url, 'https://instagram.com/acme');
});

test('the Arabic and English website builders expose link and manual handoffs', () => {
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
        assert.match(html, /assets\/js\/website-referral\.js\?v=20261005-crm-lead-owner/);
        assert.match(html, /assets\/css\/website-wizard\.css\?v=10/);
        assert.match(html, /data-website-wizard/);
        assert.match(html, /data-panel="audience"/);
        assert.doesNotMatch(html, /data-panel="personal-choice"/);
        assert.doesNotMatch(html, /data-source-kind="personal"/);
        assert.match(html, /data-panel="manual"/);
        assert.match(html, /name="display_name"/);
        assert.match(html, /name="theme"/);
        assert.match(html, /data-city-grid/);
        assert.match(html, /name="property_finder_choice" value="connect"/);
        assert.match(html, /name="property_finder_choice" value="none"/);
        assert.match(html, /name="property_finder_choice" value="later" checked/);
        assert.match(html, /name="property_finder_url"/);
        assert.match(html, /name="public_phone"/);
        assert.match(html, /name="whatsapp_phone"/);
        assert.match(html, /name="facebook_url"/);
        assert.match(html, /name="instagram_url"/);
        assert.doesNotMatch(html, /name="cities"/);
        assert.equal((html.match(/data-manual-step=/g) || []).length, 5, `${file} should expose the optional provider step`);
        const themes = [...html.matchAll(/name="theme" value="([^"]+)"/g)].map((match) => match[1]);
        assert.deepEqual(themes, ESTAVO_PERSONAL_THEMES, `${file} should offer the exact Estavo theme catalog`);
        assert.doesNotMatch(html, /data-review-name/);
    });

    assert.equal(fs.existsSync(path.join(__dirname, '..', 'website/manual-profile.php')), true);
    const wizardCss = fs.readFileSync(path.join(__dirname, '..', 'assets/css/website-wizard.css'), 'utf8');
    assert.match(wizardCss, /\.manual-actions \[hidden\] \{ display: none !important; \}/);
    assert.match(wizardCss, /\.theme-site-preview/);

    ['index.html', 'en.html'].forEach((file) => {
        const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');

        assert.doesNotMatch(html, /class="website-starter"/);
        assert.doesNotMatch(html, /assets\/js\/website-referral\.js/);
    });
});

test('generated campaign landing pages hand off to the matching website audience', () => {
    const expectations = [
        { route: 'websites', audience: 'individual' },
        { route: 'enterprise', audience: 'company' },
    ];

    expectations.forEach(({ route, audience }) => {
        ['index.html', 'en.html'].forEach((file) => {
            const html = fs.readFileSync(path.join(__dirname, '..', route, file), 'utf8');
            const destinations = [...html.matchAll(/href="(https:\/\/estavo-brokers\.com\/website\/[^\"]*)"/g)]
                .map((match) => new URL(match[1].replaceAll('&amp;', '&')));

            assert.ok(destinations.length > 1, `${route}/${file} should contain website CTAs`);
            destinations.forEach((url) => {
                assert.equal(url.searchParams.get('audience'), audience, url.toString());
            });
        });
    });
});

test('landing referral tracking preserves audience and complete Meta attribution', () => {
    const script = fs.readFileSync(path.join(__dirname, '../assets/js/referral.js'), 'utf8');
    const query = new URLSearchParams({
        utm_source: 'facebook',
        utm_campaign: 'website-acquisition',
        utm_adset: 'company-owners',
        utm_ad: 'finished-site-demo',
        fbclid: 'META_CLICK_123',
    });
    const dom = new JSDOM('<a id="cta" href="https://estavo-brokers.com/website/?audience=company">Start</a>', {
        url: `https://estavo-brokers.com/enterprise/?${query}`,
        runScripts: 'outside-only',
    });

    dom.window.eval(script);
    dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded'));
    const destination = new URL(dom.window.document.querySelector('#cta').href);

    assert.equal(destination.searchParams.get('audience'), 'company');
    query.forEach((value, key) => assert.equal(destination.searchParams.get(key), value, key));
    dom.window.close();
});

test('the website builders state the free/paid city truth (creation preview vs. activation)', () => {
    // Creation is free and the selected cities populate a preview (demo) site.
    // Activation clears that preview scope and grants one free city; more cities
    // depend on the plan (WebsiteDemoLifecycleService::activate + grantLiveScope).
    for (const [file, ar] of [['website/index.html', true], ['website/en.html', false]]) {
        const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
        const step = html.match(/aria-labelledby="cities-title"[\s\S]*?<p class="step-copy">([\s\S]*?)<\/p>/)[1];
        assert.match(step, ar ? /معاينة لموقعك/ : /preview of your website/);
        assert.match(step, ar ? /بتبدأ بمدينة واحدة مجانًا، وباقي المدن حسب الباقة/ : /one free city; more cities depend on your plan/);
        // Never promise every unit of every selected city on the free site.
        assert.doesNotMatch(html, ar ? /هنملأ موقعك بكل الوحدات/ : /fill your website with every unit/);
        assert.doesNotMatch(html, /مجاني 100%|100% free|مجاني بالكامل|completely free|كامل مجانًا|5 دقايق بس/);
        assert.match(html, ar ? /إنشاء الموقع مجاني/ : /Free to create/);
    }
});
