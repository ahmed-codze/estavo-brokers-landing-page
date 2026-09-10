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
    var CATALOG_ENDPOINT = 'https://api-brokers.estavo.space/api/website-onboarding/catalog?catalog_version=3';
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
        var theme = typeof profile.theme === 'string' ? profile.theme.trim() : '';
        var allowedThemes = [
            'modern_line', 'modern_axis', 'modern_frame', 'modern_signal', 'modern_studio',
            'monogram_stamp', 'monogram_block', 'monogram_orbit', 'monogram_grid', 'monogram_signature',
            'serif_editorial', 'serif_classic', 'serif_gallery', 'serif_column', 'serif_masthead'
        ];
        var seenCityIds = [];
        var cities = (Array.isArray(profile.cities) ? profile.cities : []).map(function (city) {
            if (!city || typeof city !== 'object') return null;
            var id = Number(city.id);
            if (!Number.isInteger(id) || id < 1 || seenCityIds.indexOf(id) !== -1) return null;
            var nameEn = typeof city.name_en === 'string' ? city.name_en.trim().slice(0, 120) : '';
            var nameAr = typeof city.name_ar === 'string' ? city.name_ar.trim().slice(0, 120) : '';
            if (!nameEn && !nameAr) return null;
            seenCityIds.push(id);
            return { id: id, name_en: nameEn, name_ar: nameAr };
        }).filter(Boolean).slice(0, 50);

        if (name.length < 2 || allowedThemes.indexOf(theme) === -1 || !cities.length) {
            return null;
        }
        return { name: name, theme: theme, cities: cities };
    }

    function normalizeCityCatalog(payload) {
        var rows = payload && payload.data && Array.isArray(payload.data.cities)
            ? payload.data.cities
            : [];
        var countsById = {};
        var profile = normalizeManualProfile({
            name: 'Catalog',
            theme: 'modern_line',
            cities: rows.map(function (city) {
                var names = city && city.name && typeof city.name === 'object' ? city.name : {};
                var id = Number(city && city.id);
                var hasCount = city && (
                    Object.prototype.hasOwnProperty.call(city, 'units_count')
                    || Object.prototype.hasOwnProperty.call(city, 'unit_models_count')
                );
                var rawCount = city && Object.prototype.hasOwnProperty.call(city, 'units_count')
                    ? city.units_count
                    : city && city.unit_models_count;
                var count = Number(rawCount);
                if (Number.isInteger(id) && id > 0 && countsById[id] === undefined) {
                    countsById[id] = hasCount && Number.isInteger(count) && count >= 0
                        ? count
                        : null;
                }
                return {
                    id: id,
                    name_en: names.en,
                    name_ar: names.ar
                };
            })
        });
        return profile ? profile.cities.map(function (city) {
            return {
                id: city.id,
                name_en: city.name_en,
                name_ar: city.name_ar,
                units_count: countsById[city.id]
            };
        }).filter(function (city) {
            // Older cached API responses did not include counts. Keep their
            // valid cities visible during a staggered deployment; the
            // versioned, no-store request below immediately fetches counts.
            return city.units_count === null || city.units_count > 0;
        }).sort(function (left, right) {
            var leftCount = Number.isInteger(left.units_count) ? left.units_count : -1;
            var rightCount = Number.isInteger(right.units_count) ? right.units_count : -1;
            return rightCount - leftCount;
        }) : [];
    }

    function buildManualOnboardingUrl(profile, locale, attribution) {
        var normalizedProfile = normalizeManualProfile(profile);
        var normalizedLocale = normalizeLocale(locale);
        if (!normalizedProfile || !normalizedLocale) return null;

        // The existing onboarding service starts from a public source URL. Give
        // every manual brief its own crawlable Estavo profile instead of
        // arriving with no source and accidentally resuming the latest website.
        var token = '';
        var cryptoObject = typeof globalThis !== 'undefined' ? globalThis.crypto : null;
        if (cryptoObject && typeof cryptoObject.getRandomValues === 'function') {
            var bytes = new Uint8Array(12);
            cryptoObject.getRandomValues(bytes);
            token = Array.prototype.map.call(bytes, function (value) {
                return value.toString(16).padStart(2, '0');
            }).join('');
        } else {
            token = String(Date.now()) + Math.random().toString(16).slice(2, 14);
        }
        token = token.replace(/[^a-f0-9]/gi, '').slice(0, 32).padEnd(24, '0');
        var profileUrl = new URL('/website/manual-profile.php/' + token, 'https://estavo-brokers.com');
        profileUrl.searchParams.set('name', normalizedProfile.name);
        profileUrl.searchParams.set('theme', normalizedProfile.theme);
        profileUrl.searchParams.set('city_ids', normalizedProfile.cities.map(function (city) { return city.id; }).join(','));
        profileUrl.searchParams.set('locale', normalizedLocale);

        var destination = new URL(ONBOARDING_PATH, PLATFORM_ORIGIN);
        destination.searchParams.set('source', profileUrl.toString());
        destination.searchParams.set('mode', 'manual');
        destination.searchParams.set('fresh_start', '1');
        destination.searchParams.set('audience', 'individual');
        destination.searchParams.set('name', normalizedProfile.name);
        destination.searchParams.set('theme', normalizedProfile.theme);
        destination.searchParams.set('city_ids', normalizedProfile.cities.map(function (city) { return city.id; }).join(','));
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
            if (name === 'manual') loadCityCatalog();
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
        var stepCount = 3;
        var error = form.querySelector('[data-manual-error]');
        var next = form.querySelector('[data-manual-next]');
        var previous = form.querySelector('[data-manual-prev]');
        var submit = form.querySelector('[data-manual-submit]');
        var cityGrid = form.querySelector('[data-city-grid]');
        var cityStatus = form.querySelector('[data-city-status]');
        var cityRetry = form.querySelector('[data-city-retry]');
        var cityCatalogLoaded = false;

        function renderCities(cities) {
            cityGrid.textContent = '';
            cities.forEach(function (city) {
                var option = documentObject.createElement('label');
                option.className = 'city-option';
                var input = documentObject.createElement('input');
                input.type = 'checkbox';
                input.name = 'cities';
                input.value = String(city.id);
                input.dataset.nameEn = city.name_en;
                input.dataset.nameAr = city.name_ar;
                var chip = documentObject.createElement('span');
                chip.className = 'city-chip';
                var cityName = documentObject.createElement('span');
                cityName.className = 'city-name';
                cityName.textContent = (locale === 'ar' ? city.name_ar : city.name_en)
                    || city.name_en
                    || city.name_ar;
                var cityCount = documentObject.createElement('small');
                cityCount.className = 'city-count';
                cityCount.textContent = city.units_count === null
                    ? (locale === 'ar' ? 'وحدات Estavo متاحة' : 'Estavo inventory available')
                    : (locale === 'ar'
                        ? new Intl.NumberFormat('ar-EG').format(city.units_count) + ' وحدة متاحة'
                        : city.units_count + (city.units_count === 1 ? ' unit available' : ' units available'));
                chip.appendChild(cityName);
                chip.appendChild(cityCount);
                option.appendChild(input);
                option.appendChild(chip);
                cityGrid.appendChild(option);
            });
        }

        function loadCityCatalog() {
            if (cityCatalogLoaded) return;
            cityStatus.textContent = locale === 'ar' ? 'بنحمّل مدن Estavo…' : 'Loading Estavo cities…';
            cityRetry.hidden = true;
            if (typeof windowObject.fetch !== 'function') {
                cityStatus.textContent = locale === 'ar' ? 'تعذر تحميل المدن. حاول تاني.' : 'Could not load cities. Try again.';
                cityRetry.hidden = false;
                return;
            }
            windowObject.fetch(CATALOG_ENDPOINT, {
                headers: { Accept: 'application/json' },
                cache: 'no-store'
            })
                .then(function (response) {
                    if (!response.ok) throw new Error('City catalog request failed.');
                    return response.json();
                })
                .then(function (payload) {
                    var cities = normalizeCityCatalog(payload);
                    if (!cities.length) throw new Error('City catalog is empty.');
                    renderCities(cities);
                    cityCatalogLoaded = true;
                    var countsKnown = cities.every(function (city) {
                        return Number.isInteger(city.units_count);
                    });
                    var total = cities.reduce(function (sum, city) {
                        return sum + (city.units_count || 0);
                    }, 0);
                    cityStatus.textContent = countsKnown
                        ? (locale === 'ar'
                            ? new Intl.NumberFormat('ar-EG').format(total) + ' وحدة متاحة في المدن دي بأسعار Estavo الحالية.'
                            : total + ' available units across these cities, with current Estavo prices.')
                        : '';
                })
                .catch(function () {
                    cityStatus.textContent = locale === 'ar' ? 'تعذر تحميل المدن. حاول تاني.' : 'Could not load cities. Try again.';
                    cityRetry.hidden = false;
                });
        }

        cityRetry.addEventListener('click', loadCityCatalog);

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
        }

        next.addEventListener('click', function () {
            if (validateStep(currentStep)) showStep(currentStep + 1);
        });
        previous.addEventListener('click', function () { showStep(currentStep - 1); });
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            if (!validateStep(1) || !validateStep(3)) return;
            var theme = form.querySelector('input[name="theme"]:checked');
            var destination = buildManualOnboardingUrl({
                name: form.elements.display_name.value,
                theme: theme && theme.value,
                cities: selectedCities().map(function (input) {
                    return {
                        id: input.value,
                        name_en: input.dataset.nameEn,
                        name_ar: input.dataset.nameAr
                    };
                })
            }, locale, attribution);
            if (!destination) {
                error.textContent = locale === 'ar'
                    ? 'تعذر تجهيز بيانات موقعك. راجع اختياراتك وحاول تاني.'
                    : 'We could not prepare your website details. Review your choices and try again.';
                return;
            }
            windowObject.location.assign(destination);
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
        CATALOG_ENDPOINT: CATALOG_ENDPOINT,
        ONBOARDING_PATH: ONBOARDING_PATH,
        buildOnboardingUrl: buildOnboardingUrl,
        buildManualOnboardingUrl: buildManualOnboardingUrl,
        normalizeManualProfile: normalizeManualProfile,
        normalizeCityCatalog: normalizeCityCatalog,
        isPlatformUrl: isPlatformUrl,
        isValidSlug: isValidSlug,
        normalizeSourceUrl: normalizeSourceUrl,
        classifySource: classifySource,
        isBarePlatformRoot: isBarePlatformRoot,
        sanitizeAttributionValue: sanitizeAttributionValue,
        bootstrap: bootstrap
    };
}));
