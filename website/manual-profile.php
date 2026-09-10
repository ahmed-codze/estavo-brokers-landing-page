<?php

declare(strict_types=1);

// Server-rendered source document for a broker who has no public social page.
// The website-onboarding crawler reads this brief exactly like any other
// owner-supplied source; the random path keeps different brokers isolated.
header('X-Robots-Tag: noindex, nofollow, noarchive');
header('Cache-Control: public, max-age=86400');

$token = trim((string) ($_SERVER['PATH_INFO'] ?? ''), '/');
$name = trim((string) ($_GET['name'] ?? ''));
$themeKey = trim((string) ($_GET['theme'] ?? ''));
$locale = ($_GET['locale'] ?? 'en') === 'ar' ? 'ar' : 'en';
$cityIds = array_values(array_unique(array_filter(
    explode(',', (string) ($_GET['city_ids'] ?? '')),
    static fn (string $id): bool => preg_match('/\A[1-9][0-9]{0,9}\z/D', $id) === 1,
)));

$themes = [
    'modern_line' => ['#17324D', '#E8EEF3', '#2F6F8F', 'Modern Line'],
    'modern_axis' => ['#1F2937', '#E5E7EB', '#2563EB', 'Modern Axis'],
    'modern_frame' => ['#214E45', '#E3EEE9', '#C46B42', 'Modern Frame'],
    'modern_signal' => ['#312E81', '#E0E7FF', '#F05D3D', 'Modern Signal'],
    'modern_studio' => ['#5B3A52', '#F0E7EC', '#B45C7A', 'Modern Studio'],
    'monogram_stamp' => ['#1E3A5F', '#DCE6F1', '#C8553D', 'Monogram Stamp'],
    'monogram_block' => ['#111111', '#E7E5E4', '#C2410C', 'Monogram Block'],
    'monogram_orbit' => ['#365B51', '#E5EFEB', '#D17B55', 'Monogram Orbit'],
    'monogram_grid' => ['#0F3D4C', '#D9EAEE', '#E07A2F', 'Monogram Grid'],
    'monogram_signature' => ['#553C62', '#EDE6F0', '#A05F7B', 'Monogram Signature'],
    'serif_editorial' => ['#28302C', '#E8E7E1', '#8C5A3C', 'Serif Editorial'],
    'serif_classic' => ['#263B35', '#E5E3D8', '#8B633A', 'Serif Classic'],
    'serif_gallery' => ['#49323C', '#EEE6E3', '#A8684F', 'Serif Gallery'],
    'serif_column' => ['#263238', '#E6E2DA', '#9A5B3E', 'Serif Column'],
    'serif_masthead' => ['#3B2431', '#E9DED7', '#B46A3C', 'Serif Masthead'],
];
if (preg_match('/\A[a-f0-9]{24,32}\z/D', $token) !== 1
    || mb_strlen($name) < 2
    || mb_strlen($name) > 80
    || ! isset($themes[$themeKey])
    || $cityIds === []
    || count($cityIds) > 50) {
    http_response_code(404);
    exit('Profile not found.');
}

$theme = $themes[$themeKey];
$cities = array_map(
    static fn (string $cityId): string => ($locale === 'ar' ? 'مدينة Estavo رقم ' : 'Estavo city #').$cityId,
    $cityIds,
);
$escape = static fn (string $value): string => htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$title = $locale === 'ar' ? 'الملف المهني لـ '.$name : $name.' — real-estate advisor';
$description = $locale === 'ar'
    ? 'بروكر عقاري مستقل يعمل في '.implode('، ', $cities)
    : 'Independent real-estate advisor working in '.implode(', ', $cities);
$schema = json_encode([
    '@context' => 'https://schema.org',
    '@type' => 'Person',
    'name' => $name,
    'jobTitle' => $locale === 'ar' ? 'مستشار عقاري مستقل' : 'Independent real-estate advisor',
    'areaServed' => $cities,
], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
?>
<!doctype html>
<html lang="<?= $locale ?>" dir="<?= $locale === 'ar' ? 'rtl' : 'ltr' ?>">
<head>
    <meta charset="utf-8">
    <meta name="robots" content="noindex,nofollow,noarchive">
    <meta name="description" content="<?= $escape($description) ?>">
    <meta name="theme-color" content="<?= $theme[0] ?>">
    <title><?= $escape($title) ?></title>
    <script type="application/ld+json"><?= $schema ?></script>
</head>
<body>
    <main>
        <h1><?= $escape($name) ?></h1>
        <p><?= $escape($description) ?></p>
        <section aria-label="Brand preferences">
            <h2>Selected website identity</h2>
            <p>Public identity type: individual real-estate advisor.</p>
            <p>Selected Estavo personal brand theme: <?= $escape($theme[3]) ?>.</p>
            <p>personal_brand_theme: <?= $escape($themeKey) ?>.</p>
            <p>Theme colors: <?= $escape(implode(', ', array_slice($theme, 0, 3))) ?>.</p>
        </section>
        <section aria-label="Market coverage">
            <h2>Selected market coverage</h2>
            <ul><?php foreach ($cities as $city): ?><li><?= $escape($city) ?></li><?php endforeach; ?></ul>
        </section>
    </main>
</body>
</html>
