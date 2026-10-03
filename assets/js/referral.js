/* ============================================================
   referral.js — Estavo Brokers Referral Tracking
   ============================================================
   Resolves the active referral slug (from ?ref= query param
   or the est_ref first-party cookie set by go.php), persists
   it in sessionStorage, and rewrites every platform CTA link
   so the referral is carried through to the sign-up page.
   Falls back to "default-landing-page" when no referral is present,
   so all links point to https://brokers.estavo.space/go/?ref=default-landing-page.

   Include ONCE in <head> or before </body> on all pages:
       <script src="assets/js/referral.js" defer></script>
   ============================================================ */

(function () {
    'use strict';

    // ── Configuration ────────────────────────────────────────────────────────
    var PLATFORM_ORIGIN = 'https://brokers.estavo.space';
    // The Sites signup lives on the marketing domain, not the platform origin,
    // but it is a conversion destination too: ad click ids must reach it or the
    // whole free-website funnel is unattributable.
    var SITES_SIGNUP = 'https://estavo-brokers.com/website/';
    var COOKIE_NAME = 'est_ref';
    var SESSION_KEY = 'est_ref';
    var QUERY_PARAM = 'ref';

    // ── Helpers ──────────────────────────────────────────────────────────────
    function getCookie(name) {
        var m = document.cookie.match('(?:^|;\\s*)' + name + '=([^;]*)');
        return m ? decodeURIComponent(m[1]) : null;
    }

    function getQP(name) {
        try { return new URLSearchParams(window.location.search).get(name); } catch (e) { return null; }
    }

    function isValidSlug(s) {
        return typeof s === 'string' && /^[a-z0-9][a-z0-9-]{0,28}[a-z0-9]$/i.test(s);
    }

    // ── Resolve active referral slug ─────────────────────────────────────────
    // Priority:  ?ref= param  >  est_ref cookie  >  sessionStorage  >  default
    var DEFAULT_SLUG = 'default-landing-page';
    var slug = getQP(QUERY_PARAM) || getCookie(COOKIE_NAME) || sessionStorage.getItem(SESSION_KEY);
    slug = isValidSlug(slug) ? slug.toLowerCase() : DEFAULT_SLUG;

    // Persist for the lifetime of this browser tab.
    sessionStorage.setItem(SESSION_KEY, slug);

    // ── Capture ad click ids and campaign params ─────────────────────────────
    // These arrive on the LANDING url (e.g. /?fbclid=...), not on the outbound
    // CTA, so they must be captured here and replayed onto the platform link.
    // Without them the ad platform cannot attribute a signup to its click and
    // its optimiser is blind, so every downstream CPA figure is wrong.
    var ATTRIBUTION_PARAMS = [
        'fbclid', 'gclid', 'ttclid', 'msclkid', 'twclid', 'li_fat_id', 'igshid',
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
        'utm_adset', 'utm_ad'
    ];
    var ATTRIBUTION_KEY = 'est_attribution';

    function captureAttribution() {
        var stored = {};
        try { stored = JSON.parse(sessionStorage.getItem(ATTRIBUTION_KEY) || '{}'); } catch (e) { stored = {}; }
        var params;
        try { params = new URLSearchParams(window.location.search); } catch (e) { return stored; }
        var changed = false;
        ATTRIBUTION_PARAMS.forEach(function (key) {
            var value = params.get(key);
            // First touch wins: a later internal navigation without the param
            // must not erase the id the visitor actually arrived with.
            if (value && !stored[key]) { stored[key] = value; changed = true; }
        });
        if (changed) {
            try { sessionStorage.setItem(ATTRIBUTION_KEY, JSON.stringify(stored)); } catch (e) { /* storage blocked */ }
        }
        return stored;
    }

    var attribution = captureAttribution();

    // ── Rewrite a single <a> element ─────────────────────────────────────────
    function rewriteLink(anchor) {
        // Support destinations are deep links, not signup/referral calls to action.
        if (anchor.closest('#raghad-support')) return;
        var href = anchor.getAttribute('href');
        if (!href) return;

        var isPlatform = href.indexOf(PLATFORM_ORIGIN) === 0;
        var isSitesSignup = href.indexOf(SITES_SIGNUP) === 0;
        if (!isPlatform && !isSitesSignup) return;

        try {
            var url = new URL(href);

            // The Sites signup keeps its own path; it only needs the ad click
            // ids appended so the signup can be attributed to the click.
            if (isSitesSignup) {
                var siteQuery = new URLSearchParams(url.search);
                Object.keys(attribution).forEach(function (key) {
                    if (attribution[key] && !siteQuery.has(key)) siteQuery.set(key, attribution[key]);
                });
                var siteSearch = siteQuery.toString();
                url.search = siteSearch ? '?' + siteSearch : '';
                anchor.setAttribute('href', url.toString());
                return;
            }

            // Route through /go/?ref=<slug> — works for both named referrers
            // and the default fallback so every visit is tracked.
            url.pathname = '/go/';

            // Rebuild the query rather than assigning url.search directly:
            // overwriting it dropped every ad click id the visitor arrived
            // with, breaking attribution for the whole paid funnel.
            var out = new URLSearchParams();
            out.set(QUERY_PARAM, slug);
            Object.keys(attribution).forEach(function (key) {
                if (attribution[key]) out.set(key, attribution[key]);
            });
            url.search = '?' + out.toString();

            anchor.setAttribute('href', url.toString());
        } catch (e) { /* malformed href — leave as-is */ }
    }

    // ── Rewrite all existing links ────────────────────────────────────────────
    function rewriteAll() {
        document.querySelectorAll('a[href]').forEach(rewriteLink);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', rewriteAll);
    } else {
        rewriteAll();
    }

    // ── Watch for dynamically inserted links (any JS framework) ──────────────
    // Observe only <body> (not documentElement) to limit mutation scope.
    if (typeof MutationObserver !== 'undefined') {
        var _observeTarget = document.body || document.documentElement;
        new MutationObserver(function (mutations) {
            mutations.forEach(function (m) {
                m.addedNodes.forEach(function (node) {
                    if (node.nodeType !== 1) return;
                    if (node.tagName === 'A') rewriteLink(node);
                    if (node.querySelectorAll) {
                        node.querySelectorAll('a[href]').forEach(rewriteLink);
                    }
                });
            });
        }).observe(_observeTarget, { childList: true, subtree: true });
    }

})();
