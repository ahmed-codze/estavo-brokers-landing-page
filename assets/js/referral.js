/* ============================================================
   referral.js — Estavo Brokers Referral Tracking
   ============================================================
   Resolves the active referral slug (from ?ref= query param
   or the est_ref first-party cookie set by go.php), persists
   it in sessionStorage, and rewrites every platform CTA link
   so the referral is carried through to the sign-up page.

   Include ONCE in <head> or before </body> on all pages:
       <script src="assets/js/referral.js" defer></script>
   ============================================================ */

(function () {
    'use strict';

    // ── Configuration ────────────────────────────────────────────────────────
    var PLATFORM_ORIGIN = 'https://brokers.estavo.space';
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
    // Priority:  ?ref= param  >  est_ref cookie  >  sessionStorage
    var slug = getQP(QUERY_PARAM) || getCookie(COOKIE_NAME) || sessionStorage.getItem(SESSION_KEY);
    slug = isValidSlug(slug) ? slug.toLowerCase() : null;

    if (!slug) return; // No referral active — nothing to do.

    // Persist for the lifetime of this browser tab.
    sessionStorage.setItem(SESSION_KEY, slug);

    // ── Rewrite a single <a> element ─────────────────────────────────────────
    function rewriteLink(anchor) {
        var href = anchor.getAttribute('href');
        if (!href) return;

        var isPlatform = href.indexOf(PLATFORM_ORIGIN) === 0;
        if (!isPlatform) return;

        // Don't double-tag.
        if (href.indexOf('utm_campaign=') !== -1) return;

        try {
            var url = new URL(href);
            url.searchParams.set('utm_source', 'referral');
            url.searchParams.set('utm_medium', 'link');
            url.searchParams.set('utm_campaign', slug);
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
    if (typeof MutationObserver !== 'undefined') {
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
        }).observe(document.documentElement, { childList: true, subtree: true });
    }

})();
