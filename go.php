<?php
/**
 * Estavo Brokers — Referral Link Handler
 * ────────────────────────────────────────────────────────────────────────────
 * Handles clean referral URLs:  https://estavo-brokers.com/go/{slug}
 *
 * Flow:
 *  1. Validates the slug.
 *  2. Sets an `est_ref` cookie on this domain (30 days, readable by JS).
 *  3. Redirects to the landing page root with ?ref={slug} — so the JS
 *     tracking script can immediately pick it up and rewrite all CTA links.
 *
 * .htaccess routes:  /go/{slug}  →  /go.php?slug={slug}
 */

// ── Configuration ─────────────────────────────────────────────────────────
const LANDING_ROOT  = 'https://estavo-brokers.com';
const COOKIE_DAYS   = 30;

// ── Read & validate slug ───────────────────────────────────────────────────
$slug = isset($_GET['slug']) ? trim($_GET['slug']) : '';

if (!$slug || !preg_match('/^[a-z0-9][a-z0-9-]{0,28}[a-z0-9]$/i', $slug)) {
    // Unknown or malformed slug — land on homepage without attribution.
    header('Location: ' . LANDING_ROOT . '/', true, 302);
    exit;
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
$redirect = LANDING_ROOT . '/?ref=' . rawurlencode($slug);

header('Location: ' . $redirect, true, 302);

// Prevent caching so the redirect always fires fresh.
header('Cache-Control: no-store, no-cache, must-revalidate');
header('Pragma: no-cache');
exit;
