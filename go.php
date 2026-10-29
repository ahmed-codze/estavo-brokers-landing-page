<?php
/**
 * Estavo Brokers — Referral Link Handler
 * ────────────────────────────────────────────────────────────────────────────
 * Handles clean referral URLs:  https://estavo-brokers.com/go/{slug}
 *
 * Flow:
 *  1. Validates the slug, or falls back to the default landing-page campaign.
 *  2. Sets an `est_ref` cookie on this domain (30 days, readable by JS).
 *  3. Redirects to the campaign landing page with ?ref={slug} — so the JS
 *     tracking script can immediately pick it up and rewrite all CTA links.
 *
 * .htaccess routes:  /go/{slug}  →  /go.php?slug={slug}
 */

// ── Configuration ─────────────────────────────────────────────────────────
const LANDING_ROOT  = 'https://estavo-brokers.com';
const COOKIE_DAYS   = 30;
const DEFAULT_SLUG   = 'default-landing-page';

// ── Read & validate slug ───────────────────────────────────────────────────
$rawSlug = $_GET['slug'] ?? $_GET['ref'] ?? '';
$slug = is_string($rawSlug) ? trim($rawSlug) : '';

if (!$slug || !preg_match('/^[a-z0-9][a-z0-9-]{0,28}[a-z0-9]$/i', $slug)) {
    $slug = DEFAULT_SLUG;
}

$slug = strtolower($slug);

// ── Set first-party cookie ─────────────────────────────────────────────────
// httponly = false so the landing-page JS can read it and rewrite CTA links.
setcookie('est_ref', $slug, [
    'expires'  => time() + (COOKIE_DAYS * 86400),
    'path'     => '/',
    'secure'   => true,
    'httponly' => false,
    'samesite' => 'Lax',
]);

// ── Redirect to landing page with ?ref= ───────────────────────────────────
// The referral.js script reads ?ref= on every page load and rewrites every
// "Try Now" / "Start Free Trial" link to carry the UTM params through to
// the platform (brokers.estavo.space).
$marketCampaigns = ['creative-1-trial-event', 'creative-2-trial-event', 'creative-3-trial-event', 'outbound-free-v01', 'outbound-free-v02', 'outbound-free-v03', 'outbound-free-v04'];
$landingPath = in_array($slug, $marketCampaigns, true) ? '/market/' : '/';
$params = ['ref' => $slug];
foreach ([
    'fbclid', 'gclid', 'ttclid', 'msclkid', 'twclid', 'li_fat_id', 'igshid',
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
    'utm_adset', 'utm_ad',
] as $key) {
    if (isset($_GET[$key]) && is_string($_GET[$key]) && $_GET[$key] !== '') {
        $params[$key] = $_GET[$key];
    }
}
$redirect = LANDING_ROOT . $landingPath . '?' . http_build_query($params, '', '&', PHP_QUERY_RFC3986);

header('Location: ' . $redirect, true, 302);

// Prevent caching so the redirect always fires fresh.
header('Cache-Control: no-store, no-cache, must-revalidate');
header('Pragma: no-cache');
exit;
