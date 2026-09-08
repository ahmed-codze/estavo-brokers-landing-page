/* ============================================================
   website-referral.js — referral tracking + website onboarding

   Keeps Estavo referral/UTM attribution on platform CTAs and sends
   website-starter forms to one fixed, trusted onboarding endpoint.
   ============================================================ */

(function (root, factory) {
    'use strict';

    var api = factory();

    if (typeof module === 'object' && module.exports) {
        module.exports = api;
    }

    if (root && root.document) {
        api.bootstrap(root, root.document);
    }
}(typeof window !== 'undefined' ? window : null, function () {
    'use strict';

    var PLATFORM_ORIGIN = 'https://brokers.estavo.space';
    var ONBOARDING_PATH = '/website/create';
    var COOKIE_NAME = 'est_ref';
    var SESSION_KEY = 'est_ref';
    var QUERY_PARAM = 'ref';
    var DEFAULT_SLUG = 'default-landing-page';
    var ATTRIBUTION_FIELDS = [
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_content',
        'utm_term'
    ];
    var MAX_SOURCE_LENGTH = 2048;
    var MAX_ATTRIBUTION_LENGTH = 160;

    function getCookie(documentObject, name) {
        var match = documentObject.cookie.match('(?:^|;\\s*)' + name + '=([^;]*)');
        if (!match) return null;

        try {
            return decodeURIComponent(match[1]);
        } catch (error) {
            return null;
        }
    }

    function getQueryParameter(search, name) {
        try {
            return new URLSearchParams(search).get(name);
        } catch (error) {
            return null;
        }
    }

    function safeStorageGet(storage, key) {
        try {
            return storage ? storage.getItem(key) : null;
        } catch (error) {
            return null;
        }
    }

    function safeStorageSet(storage, key, value) {
        try {
            if (storage) storage.setItem(key, value);
        } catch (error) {
            // Storage can be unavailable in private browsing or embedded pages.
        }
    }

    function getSessionStorage(windowObject) {
        try {
            return windowObject.sessionStorage;
        } catch (error) {
            return null;
        }
    }

    function isValidSlug(value) {
        return typeof value === 'string'
            && /^[a-z0-9](?:[a-z0-9-]{0,28}[a-z0-9])?$/i.test(value);
    }

    function sanitizeAttributionValue(value) {
        if (typeof value !== 'string') return null;
        var normalized = value.replace(/[\u0000-\u001f\u007f]/g, '').trim();
        return normalized ? normalized.slice(0, MAX_ATTRIBUTION_LENGTH) : null;
    }

    function isIpv4(hostname) {
        if (!/^\d{1,3}(?:\.\d{1,3}){3}$/.test(hostname)) return false;
        return hostname.split('.').every(function (part) {
            return Number(part) >= 0 && Number(part) <= 255;
        });
    }

    function normalizeSourceUrl(value) {
        if (typeof value !== 'string') return null;
        var trimmed = value.trim();
        if (!trimmed || trimmed.length > MAX_SOURCE_LENGTH) return null;

        var candidate = /^[a-z][a-z\d+.-]*:/i.test(trimmed)
            ? trimmed
            : 'https://' + trimmed;

        try {
            var url = new URL(candidate);
            var hostname = url.hostname.toLowerCase().replace(/\.$/, '');
            var hasForbiddenHost = !hostname
                || !hostname.includes('.')
                || hostname === 'localhost'
                || hostname.endsWith('.localhost')
                || hostname.endsWith('.local')
                || isIpv4(hostname)
                || hostname.indexOf(':') !== -1;

            if (
                (url.protocol !== 'https:' && url.protocol !== 'http:')
                || hasForbiddenHost
                || url.username
                || url.password
                || (url.port && url.port !== '443')
            ) {
                return null;
            }

            url.protocol = 'https:';
            url.hostname = hostname;
            url.hash = '';
            return url.toString();
        } catch (error) {
            return null;
        }
    }

    // Platform roots that identify no specific company. Pasting one of these
    // means the broker gave us the site, not their own page on it.
    var PLATFORM_ROOTS = [
        'facebook.com', 'fb.com', 'm.facebook.com',
        'instagram.com', 'propertyfinder.eg', 'propertyfinder.ae',
        'bayut.eg', 'bayut.com', 'olx.com.eg', 'linkedin.com',
        'tiktok.com', 'youtube.com', 'x.com', 'twitter.com'
    ];

    function isBarePlatformRoot(normalizedUrl) {
        try {
            var url = new URL(normalizedUrl);
            var host = url.hostname.toLowerCase().replace(/^www\./, '');
            if (PLATFORM_ROOTS.indexOf(host) === -1) return false;

            // A company page always carries a path or a query that names it.
            var path = url.pathname.replace(/\/+$/, '');
            var meaningful = path && path !== '' && path !== '/';
            return !meaningful && !url.search;
        } catch (error) {
            return false;
        }
    }

    // Classifies input so the UI can explain the specific problem instead of
    // showing one generic error. Never loosens normalizeSourceUrl's rules.
    function classifySource(value) {
        var raw = typeof value === 'string' ? value.trim() : '';
        if (!raw) return { ok: false, reason: 'empty' };

        var normalized = normalizeSourceUrl(raw);
        if (!normalized) return { ok: false, reason: 'malformed' };
        if (isBarePlatformRoot(normalized)) {
            return { ok: false, reason: 'platform-root', url: normalized };
        }
        return { ok: true, url: normalized };
    }

    function normalizeLocale(value) {
        return value === 'ar' || value === 'en' ? value : null;
    }

    function buildOnboardingUrl(source, locale, attribution) {
        var normalizedSource = normalizeSourceUrl(source);
        var normalizedLocale = normalizeLocale(locale);
        if (!normalizedSource || !normalizedLocale) return null;

        // The destination is deliberately constructed from constants. Neither
        // the pasted URL nor a query parameter can change its origin or path.
        var destination = new URL(ONBOARDING_PATH, PLATFORM_ORIGIN);
        destination.searchParams.set('source', normalizedSource);
        destination.searchParams.set('locale', normalizedLocale);

        var referral = attribution && attribution.ref;
        if (isValidSlug(referral)) {
            destination.searchParams.set(QUERY_PARAM, referral.toLowerCase());
        }

        ATTRIBUTION_FIELDS.forEach(function (field) {
            var value = sanitizeAttributionValue(attribution && attribution[field]);
            if (value) destination.searchParams.set(field, value);
        });

        return destination.toString();
    }

    function normalizeManualProfile(profile) {
        if (!profile || typeof profile !== 'object') return null;
        var name = typeof profile.name === 'string'
            ? profile.name.replace(/[\u0000-\u001f\u007f]/g, '').trim().slice(0, 80)
            : '';
        var palette = typeof profile.palette === 'string' ? profile.palette.trim() : '';
        var allowedPalettes = [
            'navy-gold', 'forest-sand', 'charcoal-copper',
            'blue-sky', 'burgundy-cream', 'slate-white'
        ];
        var cities = Array.isArray(profile.cities) ? profile.cities : [];
        cities = cities.filter(function (city, index) {
            return typeof city === 'string'
                && /^[a-z0-9-]{2,40}$/.test(city)
                && cities.indexOf(city) === index;
        }).slice(0, 12);

        if (name.length < 2 || allowedPalettes.indexOf(palette) === -1 || !cities.length) {
            return null;
        }
        return { name: name, palette: palette, cities: cities };
    }

    function buildManualOnboardingUrl(profile, locale, attribution) {
        var normalizedProfile = normalizeManualProfile(profile);
        var normalizedLocale = normalizeLocale(locale);
        if (!normalizedProfile || !normalizedLocale) return null;

        var destination = new URL(ONBOARDING_PATH, PLATFORM_ORIGIN);
        destination.searchParams.set('mode', 'manual');
        destination.searchParams.set('audience', 'individual');
        destination.searchParams.set('name', normalizedProfile.name);
        destination.searchParams.set('palette', normalizedProfile.palette);
        destination.searchParams.set('cities', normalizedProfile.cities.join(','));
        destination.searchParams.set('locale', normalizedLocale);

        var referral = attribution && attribution.ref;
        if (isValidSlug(referral)) destination.searchParams.set(QUERY_PARAM, referral.toLowerCase());
        ATTRIBUTION_FIELDS.forEach(function (field) {
            var value = sanitizeAttributionValue(attribution && attribution[field]);
            if (value) destination.searchParams.set(field, value);
        });
        return destination.toString();
    }

    function isPlatformUrl(href, baseUrl) {
        try {
            return new URL(href, baseUrl || PLATFORM_ORIGIN).origin === PLATFORM_ORIGIN;
        } catch (error) {
            return false;
        }
    }

    function setHiddenField(documentObject, form, name, value) {
        if (!value) return;

        var input = form.querySelector('input[name="' + name + '"]');
        if (!input) {
            input = documentObject.createElement('input');
            input.type = 'hidden';
            input.name = name;
            form.appendChild(input);
        }
        input.value = value;
    }

    function readFormAttribution(form) {
        var attribution = {};
        [QUERY_PARAM].concat(ATTRIBUTION_FIELDS).forEach(function (field) {
            var input = form.querySelector('input[name="' + field + '"]');
            if (input) attribution[field] = input.value;
        });
        return attribution;
    }

    function trustedFormLocale(form, documentObject) {
        var declaredLocale = form.getAttribute('data-locale');
        if (normalizeLocale(declaredLocale)) return declaredLocale;

        var localeInput = form.querySelector('input[name="locale"]');
        var inputLocale = localeInput && localeInput.value;
        if (normalizeLocale(inputLocale)) return inputLocale;

        return documentObject.documentElement.lang === 'ar' ? 'ar' : 'en';
    }

    // Reason-specific guidance. Each message tells the broker what to do next
    // instead of restating that the value was rejected.
    var SOURCE_MESSAGES = {
        ar: {
            empty: 'حط لينك الصفحة الأول — Facebook أو Instagram أو Property Finder أو Bayut أو موقعك.',
            malformed: 'اللينك ده مش واضح. جرّب لينك صفحتك على Facebook أو Instagram، أو لينك موقعك.',
            'platform-root': 'محتاجين لينك صفحتك نفسها، مش الموقع الرئيسي.',
            ok: '✓ تمام، لقينا الصفحة — نقدر نبدأ منها.'
        },
        en: {
            empty: 'Add your page link first — Facebook, Instagram, Property Finder, Bayut, or your website.',
            malformed: 'That link is not clear. Try your Facebook or Instagram page, or your website.',
            'platform-root': 'We need a link to your page itself, not the platform homepage.',
            ok: '✓ Got it, we found the page — we can start from here.'
        }
    };

    function messagesFor(locale) {
        return SOURCE_MESSAGES[locale] || SOURCE_MESSAGES.en;
    }

    function showSourceError(input, errorElement, locale, reason) {
        var copy = messagesFor(locale);
        input.setAttribute('aria-invalid', 'true');
        errorElement.textContent = copy[reason] || copy.malformed;
        errorElement.hidden = false;
        errorElement.classList.remove('is-ok');
        input.focus();
    }

    function showSourceSuccess(input, errorElement, locale) {
        input.removeAttribute('aria-invalid');
        errorElement.textContent = messagesFor(locale).ok;
        errorElement.hidden = false;
        errorElement.classList.add('is-ok');
    }

    function clearSourceError(input, errorElement) {
        input.removeAttribute('aria-invalid');
        errorElement.textContent = '';
        errorElement.hidden = true;
        errorElement.classList.remove('is-ok');
    }

    function prepareWebsiteForm(windowObject, documentObject, form) {
        if (form.getAttribute('data-website-starter-ready') === 'true') return;

        var input = form.querySelector('input[name="source"]');
        if (!input) return;

        var locale = trustedFormLocale(form, documentObject);
        var errorId = input.getAttribute('aria-errormessage');
        var errorElement = errorId ? documentObject.getElementById(errorId) : null;

        if (!errorElement) {
            errorElement = documentObject.createElement('p');
            errorElement.id = input.id + '-error';
            errorElement.className = 'website-starter-error';
            errorElement.setAttribute('role', 'alert');
            errorElement.setAttribute('aria-live', 'polite');
            errorElement.hidden = true;
            form.appendChild(errorElement);
            input.setAttribute('aria-errormessage', errorElement.id);
        }

        form.setAttribute('action', PLATFORM_ORIGIN + ONBOARDING_PATH);
        form.setAttribute('method', 'get');
        form.setAttribute('data-website-starter-ready', 'true');

        // Typing clears whatever verdict was on screen, so guidance never
        // contradicts what the broker is currently editing.
        input.addEventListener('input', function () {
            if (!errorElement.hidden) clearSourceError(input, errorElement);
        });

        // Confirm as soon as they finish, rather than making them press the
        // button to discover the link was fine all along.
        function reviewValue() {
            if (!input.value.trim()) return;

            var verdict = classifySource(input.value);
            if (verdict.ok) {
                input.value = verdict.url;
                showSourceSuccess(input, errorElement, locale);
            } else {
                showSourceError(input, errorElement, locale, verdict.reason);
            }
        }

        input.addEventListener('blur', reviewValue);
        input.addEventListener('paste', function () {
            windowObject.setTimeout(reviewValue, 0);
        });

        form.addEventListener('submit', function (event) {
            event.preventDefault();

            var verdict = classifySource(input.value);
            if (!verdict.ok) {
                showSourceError(input, errorElement, locale, verdict.reason);
                return;
            }

            var destination = buildOnboardingUrl(
                input.value,
                locale,
                readFormAttribution(form)
            );

            if (!destination) {
                showSourceError(input, errorElement, locale, 'malformed');
                return;
            }

            clearSourceError(input, errorElement);
            input.value = verdict.url;
            windowObject.location.assign(destination);
        });
    }

    function prepareWebsiteWizard(windowObject, documentObject, wizard, attribution) {
        if (wizard.getAttribute('data-wizard-ready') === 'true') return;
        wizard.setAttribute('data-wizard-ready', 'true');

        var locale = normalizeLocale(wizard.getAttribute('data-locale')) || 'en';
        var panels = Array.prototype.slice.call(wizard.querySelectorAll('[data-panel]'));
        var sourceKind = 'company';
        var linkCopy = {
            ar: {
                company: {
                    title: 'هات <span class="accent">لينك شركتك</span>',
                    copy: 'فيسبوك، إنستجرام، موقعك القديم، Property Finder أو Bayut — أي واحد منهم يكفي.',
                    placeholder: 'facebook.com/your-company'
                },
                personal: {
                    title: 'هات لينك <span class="accent">صفحتك</span>',
                    copy: 'الصق لينك صفحة الفيسبوك الشخصية أو المهنية اللي بتعرض عليها شغلك.',
                    placeholder: 'facebook.com/your-profile'
                }
            },
            en: {
                company: {
                    title: 'Paste your <span class="accent">company link</span>',
                    copy: 'Facebook, Instagram, your old website, Property Finder or Bayut — any one works.',
                    placeholder: 'facebook.com/your-company'
                },
                personal: {
                    title: 'Paste your <span class="accent">Facebook page</span>',
                    copy: 'Use the personal or professional Facebook page where you show your real-estate work.',
                    placeholder: 'facebook.com/your-profile'
                }
            }
        };

        function showPanel(name) {
            panels.forEach(function (panel) {
                panel.hidden = panel.getAttribute('data-panel') !== name;
            });
            var active = wizard.querySelector('[data-panel="' + name + '"]');
            var focusTarget = active && active.querySelector('input:not([type="hidden"]), button');
            if (focusTarget) windowObject.setTimeout(function () { focusTarget.focus(); }, 0);
        }

        function configureLinkPanel(kind) {
            sourceKind = kind === 'personal' ? 'personal' : 'company';
            var copy = linkCopy[locale][sourceKind];
            wizard.querySelector('[data-link-title]').innerHTML = copy.title;
            wizard.querySelector('[data-link-copy]').textContent = copy.copy;
            wizard.querySelector('.website-starter-input').placeholder = copy.placeholder;
            var back = wizard.querySelector('[data-panel="link"] [data-back-panel]');
            back.setAttribute('data-back-panel', sourceKind === 'personal' ? 'personal-choice' : 'audience');
        }

        wizard.querySelectorAll('[data-next-panel]').forEach(function (button) {
            button.addEventListener('click', function () {
                var destination = button.getAttribute('data-next-panel');
                if (destination === 'link') {
                    configureLinkPanel(button.getAttribute('data-source-kind') || 'company');
                }
                showPanel(destination);
            });
        });
        wizard.querySelectorAll('[data-back-panel]').forEach(function (button) {
            button.addEventListener('click', function () {
                showPanel(button.getAttribute('data-back-panel'));
            });
        });

        var form = wizard.querySelector('[data-manual-form]');
        if (!form) return;
        var currentStep = 1;
        var stepCount = 4;
        var error = form.querySelector('[data-manual-error]');
        var next = form.querySelector('[data-manual-next]');
        var previous = form.querySelector('[data-manual-prev]');
        var submit = form.querySelector('[data-manual-submit]');

        function selectedCities() {
            return Array.prototype.slice.call(form.querySelectorAll('input[name="cities"]:checked'));
        }

        function validateStep(step) {
            error.textContent = '';
            if (step === 1 && form.elements.display_name.value.trim().length < 2) {
                error.textContent = locale === 'ar' ? 'اكتب الاسم اللي تحب يظهر على موقعك.' : 'Enter the name you want displayed on your website.';
                form.elements.display_name.focus();
                return false;
            }
            if (step === 3 && !selectedCities().length) {
                error.textContent = locale === 'ar' ? 'اختار مدينة واحدة على الأقل.' : 'Choose at least one city.';
                return false;
            }
            return true;
        }

        function updateReview() {
            var palette = form.querySelector('input[name="palette"]:checked');
            var paletteLabel = palette && palette.nextElementSibling.querySelector('.palette-name').textContent;
            var cityLabels = selectedCities().map(function (input) {
                return input.nextElementSibling.textContent.trim();
            });
            form.querySelector('[data-review-name]').textContent = form.elements.display_name.value.trim();
            form.querySelector('[data-review-palette]').textContent = paletteLabel;
            form.querySelector('[data-review-cities]').textContent = cityLabels.join(locale === 'ar' ? '، ' : ', ');
        }

        function showStep(step) {
            currentStep = Math.max(1, Math.min(stepCount, step));
            form.querySelectorAll('[data-manual-step]').forEach(function (section) {
                section.hidden = Number(section.getAttribute('data-manual-step')) !== currentStep;
            });
            form.querySelectorAll('[data-progress]').forEach(function (dot) {
                dot.classList.toggle('is-active', Number(dot.getAttribute('data-progress')) <= currentStep);
            });
            form.querySelector('[data-step-count]').textContent = locale === 'ar'
                ? currentStep + ' من ' + stepCount
                : currentStep + ' of ' + stepCount;
            previous.hidden = currentStep === 1;
            next.hidden = currentStep === stepCount;
            submit.hidden = currentStep !== stepCount;
            error.textContent = '';
            if (currentStep === stepCount) updateReview();
        }

        next.addEventListener('click', function () {
            if (validateStep(currentStep)) showStep(currentStep + 1);
        });
        previous.addEventListener('click', function () { showStep(currentStep - 1); });
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            if (!validateStep(1) || !validateStep(3)) return;
            var palette = form.querySelector('input[name="palette"]:checked');
            var destination = buildManualOnboardingUrl({
                name: form.elements.display_name.value,
                palette: palette && palette.value,
                cities: selectedCities().map(function (input) { return input.value; })
            }, locale, attribution);
            if (destination) windowObject.location.assign(destination);
        });
    }

    function bootstrap(windowObject, documentObject) {
        function start() {
            var search = windowObject.location.search;
            var sessionStorage = getSessionStorage(windowObject);
            var candidateSlug = getQueryParameter(search, QUERY_PARAM)
                || getCookie(documentObject, COOKIE_NAME)
                || safeStorageGet(sessionStorage, SESSION_KEY);
            var slug = isValidSlug(candidateSlug)
                ? candidateSlug.toLowerCase()
                : DEFAULT_SLUG;
            var attribution = {
                ref: slug,
                utm_source: getQueryParameter(search, 'utm_source') || 'referral',
                utm_medium: getQueryParameter(search, 'utm_medium') || 'link',
                utm_campaign: getQueryParameter(search, 'utm_campaign') || slug,
                utm_content: getQueryParameter(search, 'utm_content'),
                utm_term: getQueryParameter(search, 'utm_term')
            };

            safeStorageSet(sessionStorage, SESSION_KEY, slug);

            function rewriteLink(anchor) {
                var href = anchor.getAttribute('href');
                if (!href || !isPlatformUrl(href, windowObject.location.href)) return;

                try {
                    var url = new URL(href, windowObject.location.href);
                    url.pathname = '/go/';
                    url.search = '?' + QUERY_PARAM + '=' + encodeURIComponent(slug);
                    url.hash = '';
                    anchor.setAttribute('href', url.toString());
                } catch (error) {
                    // Leave malformed links untouched.
                }
            }

            function prepareForm(form) {
                setHiddenField(documentObject, form, QUERY_PARAM, slug);
                ATTRIBUTION_FIELDS.forEach(function (field) {
                    setHiddenField(
                        documentObject,
                        form,
                        field,
                        sanitizeAttributionValue(attribution[field])
                    );
                });
                prepareWebsiteForm(windowObject, documentObject, form);
            }

            documentObject.querySelectorAll('a[href]').forEach(rewriteLink);
            documentObject.querySelectorAll('form.website-starter').forEach(prepareForm);
            documentObject.querySelectorAll('[data-website-wizard]').forEach(function (wizard) {
                prepareWebsiteWizard(windowObject, documentObject, wizard, attribution);
            });

            if (typeof windowObject.MutationObserver !== 'undefined' && documentObject.body) {
                new windowObject.MutationObserver(function (mutations) {
                    mutations.forEach(function (mutation) {
                        mutation.addedNodes.forEach(function (node) {
                            if (node.nodeType !== 1) return;
                            if (node.tagName === 'A') rewriteLink(node);
                            if (node.matches && node.matches('form.website-starter')) prepareForm(node);
                            if (node.querySelectorAll) {
                                node.querySelectorAll('a[href]').forEach(rewriteLink);
                                node.querySelectorAll('form.website-starter').forEach(prepareForm);
                            }
                        });
                    });
                }).observe(documentObject.body, { childList: true, subtree: true });
            }
        }

        if (documentObject.readyState === 'loading') {
            documentObject.addEventListener('DOMContentLoaded', start, { once: true });
        } else {
            start();
        }
    }

    return {
        PLATFORM_ORIGIN: PLATFORM_ORIGIN,
        ONBOARDING_PATH: ONBOARDING_PATH,
        buildOnboardingUrl: buildOnboardingUrl,
        buildManualOnboardingUrl: buildManualOnboardingUrl,
        normalizeManualProfile: normalizeManualProfile,
        isPlatformUrl: isPlatformUrl,
        isValidSlug: isValidSlug,
        normalizeSourceUrl: normalizeSourceUrl,
        classifySource: classifySource,
        isBarePlatformRoot: isBarePlatformRoot,
        sanitizeAttributionValue: sanitizeAttributionValue,
        bootstrap: bootstrap
    };
}));
