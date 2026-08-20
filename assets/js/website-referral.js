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

    function showSourceError(input, errorElement, locale) {
        input.setAttribute('aria-invalid', 'true');
        errorElement.textContent = locale === 'ar'
            ? 'أدخل رابطًا عامًا صحيحًا لحساب شركتك أو موقعها، مثل https://instagram.com/company.'
            : 'Enter a valid public company profile or website URL, such as https://instagram.com/company.';
        errorElement.hidden = false;
        input.focus();
    }

    function clearSourceError(input, errorElement) {
        input.removeAttribute('aria-invalid');
        errorElement.textContent = '';
        errorElement.hidden = true;
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

        input.addEventListener('input', function () {
            if (input.hasAttribute('aria-invalid')) clearSourceError(input, errorElement);
        });

        form.addEventListener('submit', function (event) {
            event.preventDefault();
            var destination = buildOnboardingUrl(
                input.value,
                locale,
                readFormAttribution(form)
            );

            if (!destination) {
                showSourceError(input, errorElement, locale);
                return;
            }

            clearSourceError(input, errorElement);
            input.value = normalizeSourceUrl(input.value);
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
        isPlatformUrl: isPlatformUrl,
        isValidSlug: isValidSlug,
        normalizeSourceUrl: normalizeSourceUrl,
        sanitizeAttributionValue: sanitizeAttributionValue,
        bootstrap: bootstrap
    };
}));
