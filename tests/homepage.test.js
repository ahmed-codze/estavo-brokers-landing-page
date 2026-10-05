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
const FIXTURE = JSON.parse(fs.readFileSync(path.join(__dirname, '../tools/data/home-fixture.json'), 'utf8'));
const unit = (key) => FIXTURE.units.find((u) => u.key === key);
const money = (m) => `${m.toFixed(1)}M`;
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
    test(`${file}: keeps the first-load performance contract`, () => {
        const { html, doc } = load(file);
        assert.ok(Buffer.byteLength(html) < 125000, 'homepage HTML must stay below 125 KB');
        assert.equal(doc.querySelector('style#es-design-critical'), null, 'shared CSS must be cacheable, not duplicated inline');
        assert.ok(doc.querySelector('link[rel="stylesheet"][href*="home-critical.css"]'));
        assert.equal(doc.querySelector('link[href*="estavo-v3.css"]'), null, 'homepage must not download duplicate shared CSS');
        assert.equal(doc.querySelector('link[rel="prefetch"][as="document"]'), null, 'alternate language must not consume first-load bandwidth');

        const fontStylesheet = doc.querySelector('link[href*="fonts.googleapis.com/css2"]');
        assert.ok(fontStylesheet);
        assert.doesNotMatch(fontStylesheet.href, /ital,|wght@.*700|wght@.*300/, 'only the three used font weights may load');
        assert.equal(fontStylesheet.href.includes('family=IBM+Plex+Sans'), labelKey === 'en');
        assert.equal(fontStylesheet.href.includes('family=Cairo'), labelKey === 'ar');

        const logo = doc.querySelector('.es-header__logo img');
        assert.match(logo.getAttribute('src'), /estavo-brokers-logo-320\.webp$/);
        assert.equal(logo.getAttribute('decoding'), 'async');
        assert.ok(doc.querySelector('link[rel="preload"][as="image"][href$="estavo-brokers-logo-320.webp"]'));

        assert.equal(doc.querySelector('script[src*="/raghad.js"]'), null, 'disabled production assistant must not download eagerly');
        assert.ok(doc.querySelector('script[src*="raghad-loader.js"]'));
    });

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
            // The final value ships in the HTML and is never animated through
            // intermediate (unverified) numbers.
            // "+" only when the shown floor is below the measured count (110 areas is exact).
            const plus = figure.display < figure.verified ? '+' : '';
            assert.equal(value.textContent.trim(), `${figure.display.toLocaleString('en-US')}${plus}`);
            assert.equal(value.dataset.count, undefined, 'no count-up hook');
        }
        // The snapshot date shown is the verified date in the config.
        const [y, , d] = PROOF.verified_at.split('-').map(Number);
        const note = doc.querySelector('.es-home-proof__note').textContent;
        assert.match(note, new RegExp(`${d}`));
        assert.match(note, new RegExp(`${y}`));
        assert.match(note, labelKey === 'ar' ? /أكتوبر/ : /October/);
        // The units figure counts unit models (types with price ranges), so it is
        // labelled as such — never as individual or available units.
        const units = doc.querySelector('[data-proof="units"] > span').textContent.trim();
        assert.equal(units, labelKey === 'ar' ? 'نموذج وحدة' : 'unit types');
        assert.doesNotMatch(units, /متاح|available/i);
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

    test(`${file}: website section has one creation button with its timing and free/paid note beside it`, () => {
        const { doc } = load(file);
        const links = [...doc.querySelectorAll('#home-website a')];
        assert.equal(links.length, 1, 'no duplicate same-destination button');
        assert.equal(links[0].href, WEBSITE);
        assert.equal(links[0].textContent.trim(), labels.website);
        const block = links[0].closest('.es-home-cta-block').textContent;
        // Timing matches the approved onboarding claim ("about five minutes"), not a guarantee.
        assert.match(block, labelKey === 'ar' ? /حوالي 5 دقايق/ : /about 5 minutes/);
        assert.doesNotMatch(block, /أقل من 5|under 5/);
        assert.match(block, labelKey === 'ar' ? /الموقع الأساسي مجاني/ : /basic website is free/);
        assert.match(block, labelKey === 'ar' ? /حسب الباقة أو الرصيد/ : /plan or credits/);
        const main = doc.querySelector('main');
        assert.equal(main.querySelector('a[href*="examples/"]'), null);
        assert.doesNotMatch(main.textContent, /شوف مثال لموقع|شوف موقع شغال|see an? (example|live) website/i);
    });

    test(`${file}: market map is the whole of Egypt with pins at the market coordinates only`, () => {
        const { doc } = load(file);
        const map = doc.querySelector('#home-market .es-home-map');
        assert.equal(map.querySelector('.es-home-map__land').getAttribute('d'), MAP.path, 'path from tools/data/egypt-map.json');
        assert.ok(MAP.points > 80, 'outline must be a real boundary, not a placeholder shape');
        assert.match(MAP.source, /Natural Earth/);
        assert.equal(map.querySelector('.es-home-map__svg').getAttribute('viewBox'), MAP.viewBox, 'the full country frame, not a crop');
        assert.ok(map.querySelector('.es-home-map__sea'));
        assert.ok(map.querySelectorAll('.es-home-map__neighbour').length >= 4);
        assert.ok(map.querySelectorAll('.es-home-map__nile').length >= 1);
        assert.ok(map.querySelectorAll('.es-home-map__water').length >= 1);
        // Exactly the Estavo Brokers main markets, unlabelled, with Sheikh Zayed picked.
        const keys = ['ain-sokhna', 'new-cairo', 'new-capital', 'north-coast', 'obour', 'october', 'red-sea', 'sheikh-zayed', 'shorouk'];
        assert.deepEqual(MAP.nodes.map((n) => n.key).sort(), keys);
        assert.equal(MAP.cities.length, 0, 'no secondary city points');
        assert.equal(map.querySelectorAll('.es-home-map__node').length, keys.length);
        assert.equal(map.querySelectorAll('.es-home-map__node--selected').length, 1);
        assert.equal(MAP.nodes.find((n) => n.selected).key, 'sheikh-zayed');
        assert.equal(map.querySelectorAll('.es-home-map__label, .es-home-map__city').length, 0, 'no names on the points');
        MAP.nodes.forEach((n) => assert.ok(n.lat > 21.3 && n.lat < 32.3 && n.lon > 24 && n.lon < 37.6, n.key));
        map.querySelectorAll('.es-home-map__node').forEach((pin) => assert.ok(pin.querySelector('use[href="#i-map-pin"]')));
        // Country pins sit at their true projected position.
        const country = [...map.querySelectorAll('.es-home-map__pins .es-home-map__node')];
        assert.equal(country.length, 3);
        for (const [pin, key] of country.map((p, i) => [p, ['north-coast', 'ain-sokhna', 'red-sea'][i]])) {
            const n = MAP.nodes.find((x) => x.key === key);
            assert.equal(parseFloat(pin.style.left).toFixed(2), n.px.toFixed(2), key);
            assert.equal(parseFloat(pin.style.top).toFixed(2), n.py.toFixed(2), key);
        }
        // Greater Cairo: a ring on the country map and an inset that reuses the same geography.
        const inset = map.querySelector('.es-home-map__inset');
        assert.equal(inset.querySelectorAll('.es-home-map__node').length, 6);
        assert.ok(inset.querySelector('.es-home-map__node--selected'));
        assert.ok(inset.querySelector('use[href="#es-home-map-land"]'));
        assert.ok(map.querySelector('.es-home-map__ring'));
        // One active project card for the selected market, with an illustrative update (no live date).
        const card = map.querySelector('.es-home-map__card');
        assert.match(card.querySelector('.es-home-map__card-head').textContent, labelKey === 'ar' ? /الشيخ زايد/ : /Sheikh Zayed/);
        assert.match(card.textContent, new RegExp(labels.example));
        assert.equal(card.querySelectorAll('.es-home-map__project').length, 1);
        assert.doesNotMatch(card.textContent, /\d{1,2} (أكتوبر|October)/, 'a synthetic update carries no live-looking date');
        const aria = map.querySelector('svg[role="img"]').getAttribute('aria-label');
        MAP.nodes.forEach((n) => assert.ok(aria.includes(n[labelKey]), n.key));
    });

    test(`${file}: every demonstration is labelled as an example`, () => {
        const { doc } = load(file);
        for (const selector of ['.es-home-intel', '[data-home-market]', '[data-home-request]',
            '[data-home-site]', '[data-home-signals]', '[data-home-clusters]']) {
            assert.ok(doc.querySelector(selector).textContent.includes(labels.example), selector);
        }
    });

    test(`${file}: request demo states its priority and ranks by it, with the shared fixture`, () => {
        const { doc } = load(file);
        const L = labelKey;
        const req = FIXTURE.request;
        // The ranking follows from the stated request: within budget, lowest down payment first.
        const inBudget = FIXTURE.units.filter((u) => u.price <= req.budget_max && u.down_payment <= req.down_payment_max);
        const best = inBudget.reduce((a, b) => (b.down_payment < a.down_payment ? b : a));
        assert.equal(req.priority, 'lowest_down_payment');
        assert.equal(best.key, FIXTURE.selected);
        const over = FIXTURE.units.filter((u) => u.price > req.budget_max);
        assert.deepEqual(over.map((u) => u.key), ['C']);
        const overBy = Math.round((unit('C').price - req.budget_max) * 1000);
        assert.equal(overBy, 300, 'C is exactly 300K over budget');
        assert.equal(Math.round((unit('A').down_payment - unit('B').down_payment) * 1000), 200);

        const request = doc.querySelector('#home-request');
        const chips = [...request.querySelectorAll('.es-home-chip')].map((c) => c.textContent.replace(/\s+/g, ' ').trim());
        assert.deepEqual(chips, L === 'ar'
            ? ['التجمع', '3 غرف', 'حتى 8M', 'مقدم حتى 1.5M', 'الأولوية لأقل مقدم']
            : ['New Cairo', '3 bedrooms', 'Up to EGP 8M', 'Down payment up to EGP 1.5M', 'Lowest down payment first']);
        // One option list for both layouts: B (selected) first, then A and C.
        const options = [...request.querySelectorAll('.es-home-options > .es-home-opt')];
        assert.equal(options.length, 3);
        assert.equal(request.querySelectorAll('.es-home-opt--best').length, 1);
        const pick = request.querySelector('.es-home-opt--best');
        assert.equal(options[0], pick, 'the selected option leads the list (first on phones)');
        assert.match(pick.textContent, new RegExp(unit('B')[L]));
        assert.match(pick.textContent, new RegExp(money(unit('B').price).replace('.', '\\.')));
        assert.match(pick.textContent, new RegExp(money(unit('B').down_payment).replace('.', '\\.')));
        const reason = pick.querySelector('.es-home-reason').textContent.trim();
        assert.equal(reason, L === 'ar' ? 'أقل مقدم بين الاختيارات داخل الميزانية' : 'Lowest down payment among the in-budget options');
        assert.doesNotMatch(reason, /استلام|delivery/i, 'delivery is flexible, so it is not the ranking reason');
        const alts = [...request.querySelectorAll('.es-home-opt--alt')].map((li) => li.textContent.replace(/\s+/g, ' '));
        assert.equal(alts.length, 2);
        // Each option carries its own facts (shown side by side on wide screens) and a reason.
        for (const [el, key] of options.map((o, i) => [o, ['B', 'A', 'C'][i]])) {
            const u = unit(key);
            const t = el.textContent.replace(/\s+/g, ' ');
            assert.match(t, new RegExp(money(u.price).replace('.', '\\.')), `${key} price`);
            assert.match(t, new RegExp(money(u.down_payment).replace('.', '\\.')), `${key} down payment`);
            assert.match(t, new RegExp(`${u.plan_years} `), `${key} plan`);
            assert.ok(el.querySelector('.es-home-reason'), `${key} has a visible reason`);
        }
        assert.ok(options[2].classList.contains('is-outside'));
        assert.match(alts[0], /7\.9M/);
        assert.match(alts[0], L === 'ar' ? /سعر إجمالي أقل · تقسيط أطول/ : /Lower total price · longer payment plan/);
        assert.match(alts[1], /8\.3M/);
        assert.match(alts[1], L === 'ar' ? /فوق الميزانية بـ ?300 ألف · مساحة أكبر/ : /EGP 300K over budget · more space/);
        // Full facts live in the comparison disclosure and match the fixture.
        const rows = [...request.querySelectorAll('.es-home-compare tbody tr')];
        const col = (i) => rows.map((r) => r.querySelectorAll('td')[i].textContent.trim());
        FIXTURE.units.forEach((u, i) => {
            const c = col(i).join(' | ');
            assert.match(c, new RegExp(money(u.price).replace('.', '\\.')), `${u.key} price`);
            assert.match(c, new RegExp(money(u.down_payment).replace('.', '\\.')), `${u.key} down payment`);
            assert.match(c, new RegExp(`${u.plan_years} `), `${u.key} plan`);
            assert.match(c, new RegExp(`${u.area_m2} m²`), `${u.key} area`);
            if (/^\d+$/.test(u.delivery)) assert.match(c, new RegExp(u.delivery), `${u.key} delivery`);
        });
        assert.match(request.querySelector('.es-home-compare').textContent, L === 'ar' ? /الاستلام مرن/ : /Delivery is flexible/);
        // No purchase probability, AI confidence or invented instalment amounts.
        assert.doesNotMatch(request.textContent, /%|confidence|احتمال|ثقة|قسط شهري|monthly instal/i);
    });

    test(`${file}: every surface that shows the example uses the same numbers`, () => {
        const { doc } = load(file);
        const B = unit('B');
        for (const selector of ['#home-hero .es-home-intel__result', '#home-request .es-home-opt--best',
            '#home-website .es-home-listing', '#home-client .es-home-match__unit']) {
            const text = doc.querySelector(selector).textContent;
            assert.match(text, new RegExp(B[labelKey]), selector);
            assert.match(text, /8\.0M/, selector);
            assert.match(text, /1\.2M/, selector);
        }
        // The hero states the priority instead of an unexplained 200K comparison.
        const hero = doc.querySelector('#home-hero .es-home-intel').textContent;
        assert.doesNotMatch(hero, /200/);
        assert.match(hero, labelKey === 'ar' ? /الأولوية لأقل مقدم/ : /lowest down payment first/);
    });

    test(`${file}: optional detail uses native disclosures that work without JavaScript`, () => {
        const { doc } = load(file);
        for (const [selector, summary] of [
            ['#home-request details.es-home-compare', labelKey === 'ar' ? 'قارن كل التفاصيل' : 'Compare all details'],
            ['#home-client details.es-home-reverse', labelKey === 'ar' ? 'عندك وحدة؟ شوف مين ممكن تناسبه' : 'Have a unit? See who it could suit'],
        ]) {
            const details = doc.querySelector(selector);
            assert.ok(details, selector);
            assert.equal(details.open, false, `${selector} is closed by default`);
            assert.equal(details.querySelector(':scope > summary').textContent.trim(), summary);
            assert.ok(details.querySelector('.es-home-disclosure__body').textContent.trim().length > 40, 'content ships in the HTML');
        }
        // Reverse matching shows compatibility with anonymous needs — no names, no certainty.
        const reverse = doc.querySelector('#home-client .es-home-reverse');
        assert.equal(reverse.querySelectorAll('.es-home-interest').length, 3);
        assert.match(reverse.textContent, new RegExp(labels.example));
        assert.doesNotMatch(reverse.textContent, /%|هيشتري|will buy|ready to buy|جاهز للشراء/i);
        // Only FAQ and these two are disclosures — sections themselves are not accordions.
        assert.equal(doc.querySelectorAll('main details').length, 2 + doc.querySelectorAll('#home-faq details').length);
    });

    test(`${file}: removed legacy fields and repeated copy stay removed`, () => {
        const { html, doc } = load(file);
        const main = doc.querySelector('main');
        // Obsolete Meta campaign fields (account/objective/budget) must not ship, hidden or not.
        assert.equal(main.querySelector('.es-home-campaign__info, .es-home-campaign__ad, .es-home-campaign__status'), null);
        assert.doesNotMatch(main.querySelector('#home-growth').textContent, /الهدف|طلبات تواصل|Objective|Lead form|متصل|Connected/);
        // Unofficial Meta/Facebook marks are not used until official assets are cleared.
        assert.doesNotMatch(html, /i-brand-meta|i-brand-facebook/);
        // Superseded components.
        assert.equal(main.querySelector('.es-home-signature, .es-home-outputs, .es-home-keys:not(template *), .es-home-tri, blockquote, .es-home-build__form, .es-home-closing__triangle, .es-home-lockup, .es-home-prop, .es-home-alts'), null);
        assert.doesNotMatch(main.textContent, /Tracking|Budget Range|Client Intelligence/);
        // A visit is not proof of growing interest: no unqualified "increased" claim.
        assert.doesNotMatch(main.querySelector('#home-client').textContent, /زاد|increased/i);
        // The suggestion is labelled as a suggestion.
        assert.match(main.querySelector('#home-client .es-home-suggest').textContent, labelKey === 'ar' ? /اقتراح/ : /Suggested/);
    });

    test(`${file}: homepage events are attached to deliberate links only`, () => {
        const { doc } = load(file);
        const events = [...doc.querySelectorAll('[data-home-event]')];
        assert.ok(events.length >= 8);
        events.forEach((el) => assert.equal(el.tagName, 'A'));
        const names = new Set(events.map((el) => el.dataset.homeEvent));
        for (const name of ['home_market_free_click', 'home_website_free_click', 'home_ai_request_demo_click',
            'home_client_insights_click', 'home_meta_click', 'home_pricing_click', 'home_enterprise_click',
            'home_integrations_click', 'home_resale_click']) {
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
        const answers = [...doc.querySelectorAll('#home-faq details > p')].map((p) => {
            const clone = p.cloneNode(true);
            clone.querySelectorAll('a').forEach((a) => a.remove());
            return clone.textContent.replace(/\s+/g, ' ').trim();
        });
        assert.deepEqual(faq.mainEntity.map((q) => q.acceptedAnswer.text), answers);
        assert.equal(visible.length, 4, 'four questions');
        assert.doesNotMatch(visible.join(' '), /CRM|بيعمل إيه|What is Estavo|يعرف كل حاجة|know everything/i);
        assert.equal(doc.querySelectorAll('#home-faq details[open]').length, 0);
        assert.ok(doc.querySelector('#home-faq a[href^="privacy"]'), 'privacy policy linked from the FAQ');
    });
}

test('balance pass: each section answers its question visibly, without opening anything', () => {
    for (const [file, ar] of [['index.html', true], ['en.html', false]]) {
        const { doc } = load(file);
        const lead = (id) => doc.querySelector(`#${id} .es-home-lead`).textContent.replace(/\s+/g, ' ');
        // Hero: names the AI, the market data, the properties and client interest on the website.
        assert.match(lead('home-hero'), ar ? /داتا السوق والعقارات واهتمام عملاءك.*بالـ ?AI.*لكل طلب وليه/ : /market data, the properties you sell and client interest.*AI.*why/);
        // Market: what Estavo maintains, in three compact groups, and the work it replaces.
        assert.match(lead('home-market'), ar ? /يجمع.*ويتابع تحديثاتها.*برايس ليست/ : /maintains the project information it covers.*price list/);
        assert.equal(doc.querySelector('#home-market ul:not(.es-home-market__docs)'), null, 'no extra key list in Market');
        // Request: the client can explain it on the broker's site; reasons are explained.
        assert.match(lead('home-request'), ar ? /الفرق في السعر والمقدم والسداد والاستلام.*وليه كل اختيار مناسب أو لأ/ : /differences in price, down payment, payment plan and delivery.*fits or doesn't/);
        // Website: what the site provides, including the assistant.
        assert.match(lead('home-website'), ar ? /وحداتك الخاصة.*يشرح طلبه للـ ?AI.*ويتواصل معاك/ : /your own properties.*explain what they need to the AI.*contact you/);
        // Client: both directions stated in visible text, not only inside the disclosure.
        assert.match(lead('home-client'), ar ? /اللي العميل قاله بتفاعله على موقعك وبمواصفات العقارات/ : /what the client told you with their activity on your website and the properties/);
        const both = doc.querySelector('#home-client .es-home-both-ways');
        assert.ok(both && !both.closest('details'));
        assert.equal(both.textContent.trim(), ar ? 'من العميل للعقار. ومن العقار للعملاء المناسبين.' : 'From client to property. From property to the clients it may suit.');
        // Growth: understanding → what to promote → Meta.
        assert.match(lead('home-growth'), ar ? /اختيار العقارات والرسائل.*Meta/ : /choose what you advertise and how you message it.*Meta/);
        // Start free: the company / platform profile is one line beside the free doors.
        assert.match(doc.querySelector('#home-start-free .es-home-business').textContent, ar ? /شركة أو منصة/ : /company or an existing platform/);
        const routes = [...doc.querySelectorAll('#home-start-free .es-home-routes a')].map((a) => a.textContent.trim());
        assert.deepEqual(routes, ar ? ['شوف الأسعار', 'حلول الشركات', 'الربط بمنصتك', 'شبكة الريسيل']
            : ['See pricing', 'Company solutions', 'Platform integrations', 'Resale network']);
        // Leads stay compact paragraphs: no lists or rhetorical questions inside them.
        doc.querySelectorAll('main .es-home-lead').forEach((p) => {
            assert.doesNotMatch(p.textContent, /[؟?]/);
            assert.ok(p.textContent.trim().split(/\s+/).length <= 45, p.textContent.slice(0, 40));
        });
        // No retired vocabulary.
        assert.doesNotMatch(doc.querySelector('main').textContent, /مصدر الـ ?Intelligence|Client Intelligence|Budget Range|CRM|مش مجرد/);
    }
});

test('the Request action names what its destination is', () => {
    for (const [file, ar] of [['index.html', true], ['en.html', false]]) {
        const { doc } = load(file);
        const a = doc.querySelector('#home-request .es-home-section-foot a');
        // /market/#ai-expert explains Brokers AI; it is not a working analysis entry.
        assert.match(a.getAttribute('href'), /^market\/(en\.html)?#ai-expert$/);
        assert.equal(a.textContent.trim(), ar ? 'شوف إزاي إستاڤو يحلل الطلب' : 'See how Estavo analyses a request');
    }
});

test('market map: the selected pin is joined to its card by geometry from the map data', () => {
    for (const file of ['index.html', 'en.html']) {
        const { doc } = load(file);
        const map = doc.querySelector('#home-market .es-home-map');
        const x = parseFloat(map.style.getPropertyValue('--sel-x'));
        const y = parseFloat(map.style.getPropertyValue('--sel-y'));
        assert.ok(x > 0 && x < 1 && y > 0 && y < 1, `${file}: selected pin fractions`);
        // Matches the rendered inset pin: inset box + pin offset inside it.
        const inset = map.querySelector('.es-home-map__inset');
        const pin = inset.querySelector('.es-home-map__node--selected');
        const fx = (parseFloat(inset.style.left) + parseFloat(pin.style.left) * parseFloat(inset.style.width) / 100) / 100;
        assert.ok(Math.abs(fx - x) < 0.002, `${file}: connector x follows the pin (${fx} vs ${x})`);
        assert.ok(map.querySelector('.es-home-map__link[aria-hidden="true"]'));
        assert.match(map.querySelector('.es-home-map__update').textContent, /خطة السداد اتحدّثت|Payment plan updated/);
    }
});

test('website and client figures: illustrative, non-interactive, evidence kept apart', () => {
    for (const [file, ar] of [['index.html', true], ['en.html', false]]) {
        const { doc } = load(file);
        const site = doc.querySelector('#home-website figure');
        // A real-looking site: brand, contact destination, property facts, the site's assistant.
        assert.ok(site.querySelector('.es-home-brand'));
        assert.ok(site.querySelector('.es-home-browser__contact'));
        assert.equal(site.querySelectorAll('.es-home-listing__facts div').length, 4);
        assert.equal(site.querySelectorAll('.es-home-bubble--client').length, 1);
        assert.match(site.querySelector('.es-home-bubble--ai').textContent, ar ? /ميزانيتك والمقدم/ : /budget and available down payment/);
        // Nothing in an illustration invites input it cannot handle.
        for (const fig of doc.querySelectorAll('main figure')) {
            assert.equal(fig.querySelector('input, textarea, select, button, a, [contenteditable], [tabindex]'), null);
        }
        assert.equal((site.textContent.match(ar ? /مثال توضيحي/g : /Example/g) || []).length, 1, 'labelled once');
        // Client: what was said, what was observed, then Estavo's reading.
        const fig = doc.querySelector('#home-client [data-home-signals]');
        assert.ok(fig.querySelector('.es-home-evidence--said'));
        assert.equal(fig.querySelectorAll('.es-home-evidence--seen .es-home-sig').length, 4);
        assert.match(fig.querySelector('.es-home-suggest').textContent, ar ? /مقارنة الاستلام بين أ وب/ : /handover comparison of A and B/);
        // The finished website is the visual; setup details live in the caption only.
        assert.equal(site.querySelector('.es-home-build__src'), null);
        assert.match(site.querySelector('figcaption').textContent, ar ? /الاسم واللوجو والمدن/ : /name, logo and the cities/);
        assert.doesNotMatch(fig.textContent, /جاهز|عاجل|ready to buy|urgent|%/i);
        // Reverse matching gives concrete reasons; the immediate-handover need is only partly compatible.
        const partial = doc.querySelector('#home-client .es-home-interest.is-partial').textContent;
        assert.match(partial, /2027/);
    }
});

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

test('homepage defers below-fold rendering and uses compact image assets', () => {
    const css = fs.readFileSync(path.join(__dirname, '../assets/css/home.css'), 'utf8');
    assert.match(css, /content-visibility:\s*auto/);
    assert.match(css, /contain-intrinsic-size:/);

    for (const asset of [
        'assets/logo/estavo-brokers-logo-320.webp',
        'assets/logo/estavo-mark-white-128.webp',
        'assets/logo/estavo-inverted-wordmark-400.webp',
    ]) {
        assert.ok(fs.statSync(path.join(__dirname, '..', asset)).size < 10000, `${asset} must stay below 10 KB`);
    }
});

test('homepage CSS/JS carry no testimonial remnants; future art backlog is mascot-only', () => {
    for (const file of ['assets/css/home.css', 'assets/js/home.js']) {
        assert.doesNotMatch(fs.readFileSync(path.join(__dirname, '..', file), 'utf8'), /testimonial/i, file);
    }
    for (const file of ['index.html', 'en.html']) {
        const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
        const backlog = [...html.matchAll(/backlog[^\n]*/gi)].map((m) => m[0]);
        backlog.forEach((line) => assert.match(line, /pose/i, `${file}: non-mascot backlog item: ${line}`));
        // The closing uses the transferred waving pose; no empty mascot slot reserves space.
        assert.match(html, /class="es-home-closing__mascot" src="assets\/img\/mascot\/estavo-guide-waving-200\.webp"/);
        assert.doesNotMatch(html, /es-home-mascot-slot|data-mascot-slot/);
    }
    assert.ok(fs.statSync(path.join(__dirname, '../assets/img/mascot/estavo-guide-waving-200.webp')).size < 25000);
    const agents = fs.readFileSync(path.join(__dirname, '../AGENTS.md'), 'utf8');
    const section = agents.split('### Remaining homepage art backlog')[1].split('\n#')[0]
        .split('\n').filter((line) => /^\d+\./.test(line));
    assert.ok(section.length >= 1);
    section.forEach((line) => assert.match(line, /pose/i, line));
    assert.doesNotMatch(section.join('\n'), /\b(map|icon|connector|rail|card|cluster|growth|signal|website visual|market visual)\b/i);
});

test('graphics: compact hero model, client insight, growth pattern, consistent CTAs and nav', () => {
    for (const [file, ar] of [['index.html', true], ['en.html', false]]) {
        const { doc } = load(file);
        // Hero: a compact market/property/client model — three labels, no sub-paragraphs.
        const nodes = [...doc.querySelectorAll('#home-hero .es-home-fw__nodes li > b')].map((n) => n.textContent.trim());
        assert.deepEqual(nodes, ar ? ['السوق', 'العقار', 'العميل'] : ['Market', 'Property', 'Client']);
        // Each area names what it holds in one short line, not a paragraph.
        doc.querySelectorAll('#home-hero .es-home-fw__nodes small').forEach((n) => assert.ok(n.textContent.trim().split(/\s+/).length <= 4));
        // The hero is an overview: one result line and its reason, not the full fact grid.
        assert.equal(doc.querySelector('#home-hero .es-home-facts'), null);
        assert.equal(doc.querySelector('#home-hero figcaption'), null, 'no second explanation under the model');
        assert.equal(doc.querySelectorAll('#home-hero .es-home-micro').length, 1, 'positioning signature appears once');
        // Client: four signals (2×2) → one insight panel with an interest and a labelled suggestion.
        const signals = doc.querySelectorAll('#home-client .es-home-sig');
        assert.equal(signals.length, 4);
        signals.forEach((sig) => assert.ok(sig.querySelector('.es-home-sig__icon svg')));
        assert.equal(doc.querySelectorAll('#home-client .es-home-insight').length, 1);
        // Three layers: what happened (evidence) → what Estavo understood → what it suggests.
        const read = doc.querySelectorAll('#home-client .es-home-insight .es-home-insight__read');
        assert.equal(read.length, 1);
        assert.match(read[0].textContent, ar ? /مهتم بمشروع ب/ : /Interest in Project B/);
        const suggest = doc.querySelector('#home-client .es-home-suggest');
        assert.ok(suggest && !suggest.closest('.es-home-insight'), 'the suggestion is its own layer');
        assert.match(suggest.textContent, ar ? /^اقتراح/ : /^Suggested next information/);
        assert.doesNotMatch(doc.querySelector('#home-client').textContent, ar ? /اليوم \d/ : /Day \d/, 'no day-by-day timeline');
        // Growth: one prominent pattern, two secondary, a small Meta destination with no audience size.
        assert.equal(doc.querySelectorAll('#home-growth .es-home-cluster--key').length, 1);
        assert.equal(doc.querySelectorAll('#home-growth .es-home-cluster').length, 3);
        const panel = doc.querySelector('#home-growth .es-home-campaign');
        assert.match(panel.textContent, /Meta/);
        // The panel is information for a campaign, not an automatically created audience.
        assert.equal(panel.querySelector('.es-home-campaign__title').textContent.trim(), ar ? 'معلومات لحملتك' : 'Insights for your campaign');
        assert.doesNotMatch(panel.textContent, /جمهور|audience/i);
        assert.doesNotMatch(panel.textContent, /\b\d{2,}(,\d{3})*\s*(people|users|شخص|مستخدم)/i);
        assert.match(doc.querySelector('#home-growth .es-home-control').textContent, ar ? /تحت تحكمك/ : /under your control/);
        // Website creation buttons share one label everywhere.
        doc.querySelectorAll('a.es-home-btn[href="https://estavo-brokers.com/website/"]')
            .forEach((a) => assert.equal(a.textContent.trim(), ar ? 'اعمل موقعك مجانًا' : 'Create your website free'));
        // Start free: two equal free cards, paid scope in one line, other routes as compact links.
        assert.equal(doc.querySelectorAll('#home-start-free .es-home-free-card').length, 2);
        assert.equal(doc.querySelectorAll('#home-start-free .es-home-btn').length, 2);
        const routes = [...doc.querySelectorAll('#home-start-free .es-home-routes a')].map((a) => a.getAttribute('href').split('/')[0]);
        assert.deepEqual(routes, ['pricing', 'enterprise', 'integrations', 'listings']);
        // Primary navigation: no Examples; the client page is "understanding"; no salary comparison.
        const nav = doc.querySelector('.es-header').outerHTML + doc.querySelector('[data-drawer]').outerHTML;
        assert.doesNotMatch(nav, /examples\//);
        assert.match(nav, ar ? /فهم العميل/ : /Client understanding/);
        assert.doesNotMatch(nav, /مرتب|salary|Estavo Sites/);
    }
});

test('click analytics: one deliberate click sends the legacy event and the home_* event once each', async () => {
    const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8')
        .replace(/<script[\s\S]*?<\/script>/gi, '');
    const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true, url: 'https://estavo-brokers.com/' });
    const { window } = dom;
    window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
    window.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
    const sent = [];
    window.gtag = (kind, name, props) => sent.push({ name, props });
    for (const file of ['assets/js/v3/estavo-v3.js', 'assets/js/home.js']) {
        window.eval(fs.readFileSync(path.join(__dirname, '..', file), 'utf8'));
    }
    window.document.dispatchEvent(new window.Event('DOMContentLoaded'));
    await new Promise((r) => setTimeout(r, 10));
    sent.length = 0;
    const link = window.document.querySelector('#home-hero a[data-track="market_opened"]');
    link.addEventListener('click', (e) => e.preventDefault());
    link.dispatchEvent(new window.MouseEvent('click', { bubbles: true, cancelable: true }));
    const names = sent.map((e) => e.name).sort();
    assert.deepEqual(names, ['home_market_free_click', 'market_opened']);
    // Payloads are categorical only.
    sent.forEach((e) => assert.deepEqual(Object.keys(e.props).sort(), ['lang', 'position']));
    // Opening a disclosure or the FAQ is not a conversion event.
    sent.length = 0;
    window.document.querySelector('#home-request details summary').dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
    window.document.querySelector('#home-faq summary').dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
    assert.deepEqual(sent, []);
    await new Promise((r) => setTimeout(r, 10)); // let pending observers settle before teardown
    window.close();
});

test('shared stylesheet references are versioned everywhere', () => {
    const pages = ['index.html', 'en.html'];
    for (const dir of fs.readdirSync(path.join(__dirname, '..'))) {
        for (const name of ['index.html', 'en.html']) {
            const p = path.join(dir, name);
            if (fs.existsSync(path.join(__dirname, '..', p)) && /estavo-v3\.css/.test(fs.readFileSync(path.join(__dirname, '..', p), 'utf8'))) pages.push(p);
        }
    }
    assert.ok(pages.length >= 24);
    for (const p of pages) {
        const html = fs.readFileSync(path.join(__dirname, '..', p), 'utf8');
        for (const m of html.matchAll(/(?:href|src)="([^"]*\/(?:estavo-v3|home|home-critical|commercial|market)\.(?:css|js))(\?v=[^"]*)?"/g)) {
            assert.ok(m[2], `${p}: ${m[1]} has no version`);
        }
    }
});

test('homepage icons are inlined so they render on any host or sub-folder', () => {
    for (const file of ['index.html', 'en.html']) {
        const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
        assert.doesNotMatch(html, /estavo-home\.svg#/, `${file} must not depend on an external sprite`);
        const used = new Set([...html.matchAll(/href="#(i-[a-z0-9-]+)"/g)].map((m) => m[1]));
        const defined = new Set([...html.matchAll(/<symbol id="(i-[a-z0-9-]+)"/g)].map((m) => m[1]));
        assert.ok(used.size >= 15, "sprite is wired (every used id is checked below)");
        used.forEach((id) => assert.ok(defined.has(id), `${file}: icon #${id} is not defined`));
        assert.equal((html.match(/id="es-home-icons"/g) || []).length, 1);
    }
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
