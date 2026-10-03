#!/usr/bin/env python3
"""Build the homepage Egypt map from Natural Earth and validated city coordinates.

Sources (public domain):
  Natural Earth 1:50m Admin 0 – Countries   ne_50m_admin_0_countries.geojson
  Natural Earth 1:50m Rivers + lake centrelines   ne_50m_rivers_lake_centerlines.geojson
  https://github.com/nvkelso/natural-earth-vector/tree/master/geojson

The Egyptian boundary follows the 22nd parallel with the Halaib triangle
inside Egypt, which is how the map must read for an Egyptian audience.

Usage:
  python3 tools/build-egypt-map.py countries.geojson rivers.geojson

Writes:
  assets/img/egypt-map.svg      standalone outline + Nile (reference / reuse)
  tools/data/egypt-map.json     geometry, nodes and label layout inlined by the homepage

Every city is validated before anything is written: it must fall inside the
outline (coastal cities within 0.12° of the coast) and Nile-valley cities
must lie within 0.12° of the Nile centreline. A wrong coordinate fails the build.
Geography is never mirrored for RTL; only label text follows the page language.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VIEW_W, VIEW_H = 640, 320
LAT0, LON0 = 31.70, 24.70                # north-west corner of the main frame
K = 28.0                                 # px per degree of latitude (main map)
COS = math.cos(math.radians(26.8))       # equirectangular correction at Egypt's mid-latitude
OFFSET = (10, 22)

# Greater Cairo lens: the same projection, magnified.
INSET = {'x': 330, 'y': 18, 'w': 300, 'h': 284, 'lon': 31.35, 'lat': 30.09, 'k': 345.0}
LENS = {'lon': (30.87, 31.84), 'lat': (29.92, 30.25)}

# tier "market": a market in estavo-brokers-api config/estavo_market_coverage.php.
# tier "ref":    a main Egyptian city shown for orientation only (outside coverage).
# check: in = inside the outline · coast = within 0.12° of the coast · nile = on the Nile
# label: (dx, dy, anchor) offset of the label anchor from the node in px; None = dot only.
CITIES = [
    # key              lat     lon     tier      ar                  en                check    label
    ('new-cairo',      30.020, 31.460, 'market', 'القاهرة الجديدة', 'New Cairo',       'in',    (-8, 14, 'end')),
    ('new-capital',    30.020, 31.760, 'market', 'العاصمة الإدارية', 'New Capital',     'in',    (22, 44, 'end')),
    ('sheikh-zayed',   30.045, 30.980, 'market', 'الشيخ زايد',       'Sheikh Zayed',    'in',    (0, -26, 'center')),
    ('october',        29.950, 30.925, 'market', '6 أكتوبر',          '6th of October',  'in',    (0, 24, 'center')),
    ('obour',          30.228, 31.475, 'market', 'العبور',           'Obour',           'in',    (0, -32, 'center')),
    ('shorouk',        30.120, 31.620, 'market', 'الشروق',           'Shorouk',         'in',    (-11, 0, 'end')),
    ('new-heliopolis', 30.160, 31.665, 'market', 'نيو هليوبوليس',    'New Heliopolis',  'in',    (0, -44, 'center')),
    ('badr',           30.137, 31.714, 'market', 'بدر',              'Badr',            'in',    (36, -26, 'end')),
    ('future-city',    30.065, 31.675, 'market', 'المستقبل',         'Future City',     'in',    (5, 32, 'center')),
    ('ain-sokhna',     29.600, 32.320, 'market', 'العين السخنة',     'Ain Sokhna',      'coast', (-10, 1, 'end')),
    ('north-coast',    30.830, 28.950, 'market', 'الساحل الشمالي',   'North Coast',     'coast', (0, 14, 'center')),
    ('alexandria',     31.200, 29.920, 'market', 'الإسكندرية',       'Alexandria',      'coast', (8, -24, 'center')),
    ('cairo',          30.044, 31.236, 'ref',    'القاهرة',          'Cairo',           'nile',  (0, -22, 'center')),
    ('port-said',      31.260, 32.300, 'ref',    'بورسعيد',          'Port Said',       'coast', (6, -16, 'center')),
    ('ismailia',       30.600, 32.270, 'ref',    'الإسماعيلية',      'Ismailia',        'in',    None),
    ('suez',           29.970, 32.530, 'ref',    'السويس',           'Suez',            'coast', None),
    ('damietta',       31.420, 31.810, 'ref',    'دمياط',            'Damietta',        'coast', None),
    ('mansoura',       31.040, 31.380, 'ref',    'المنصورة',         'Mansoura',        'in',    None),
    ('tanta',          30.790, 31.000, 'ref',    'طنطا',             'Tanta',           'in',    None),
    ('zagazig',        30.590, 31.500, 'ref',    'الزقازيق',         'Zagazig',         'in',    None),
    ('damanhur',       31.030, 30.470, 'ref',    'دمنهور',           'Damanhur',        'in',    None),
    ('matrouh',        31.350, 27.240, 'ref',    'مرسى مطروح',       'Marsa Matrouh',   'coast', (0, 16, 'center')),
    ('fayoum',         29.310, 30.840, 'ref',    'الفيوم',           'Fayoum',          'in',    None),
    ('beni-suef',      29.070, 31.100, 'ref',    'بني سويف',         'Beni Suef',       'nile',  None),
    ('minya',          28.110, 30.750, 'ref',    'المنيا',           'Minya',           'nile',  (-8, 0, 'end')),
    ('assiut',         27.180, 31.180, 'ref',    'أسيوط',            'Assiut',          'nile',  (-8, 0, 'end')),
    ('sohag',          26.560, 31.690, 'ref',    'سوهاج',            'Sohag',           'nile',  (-8, 2, 'end')),
    ('qena',           26.160, 32.720, 'ref',    'قنا',              'Qena',            'nile',  (8, -2, 'start')),
    ('luxor',          25.690, 32.640, 'ref',    'الأقصر',           'Luxor',           'nile',  (8, 2, 'start')),
    ('aswan',          24.090, 32.900, 'ref',    'أسوان',            'Aswan',           'nile',  (8, 0, 'start')),
    ('hurghada',       27.260, 33.810, 'ref',    'الغردقة',          'Hurghada',        'coast', (8, 4, 'start')),
    ('ras-sudr',       29.590, 32.710, 'ref',    'رأس سدر',          'Ras Sudr',        'coast', None),
    ('sharm',          27.920, 34.330, 'ref',    'شرم الشيخ',        'Sharm El Sheikh', 'coast', (8, -4, 'start')),
    ('arish',          31.130, 33.800, 'ref',    'العريش',           'Arish',           'coast', (8, -8, 'start')),
    ('kharga',         25.450, 30.550, 'ref',    'الخارجة',          'Kharga',          'in',    (-8, 0, 'end')),
]
SELECTED = 'new-cairo'


def in_lens(lon, lat):
    return LENS['lon'][0] <= lon <= LENS['lon'][1] and LENS['lat'][0] <= lat <= LENS['lat'][1]


def project(lon, lat):
    return (OFFSET[0] + (lon - LON0) * COS * K, OFFSET[1] + (LAT0 - lat) * K)


def project_inset(lon, lat):
    return (INSET['x'] + INSET['w'] / 2 + (lon - INSET['lon']) * COS * INSET['k'],
            INSET['y'] + INSET['h'] / 2 - (lat - INSET['lat']) * INSET['k'])


def rdp(points, eps):
    if len(points) < 3:
        return points
    (x1, y1), (x2, y2) = points[0], points[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1e-9
    index, dmax = 0, 0.0
    for i in range(1, len(points) - 1):
        x0, y0 = points[i]
        d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
        if d > dmax:
            index, dmax = i, d
    if dmax > eps:
        return rdp(points[:index + 1], eps)[:-1] + rdp(points[index:], eps)
    return [points[0], points[-1]]


def inside(lon, lat, ring):
    hit = False
    for i in range(len(ring)):
        (x1, y1), (x2, y2) = ring[i], ring[(i + 1) % len(ring)]
        if (y1 > lat) != (y2 > lat) and lon < (x2 - x1) * (lat - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


def distance(lon, lat, lines):
    def seg(a, b):
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((lon - ax) * dx + (lat - ay) * dy) / (dx * dx + dy * dy or 1e-12)))
        return math.hypot(lon - (ax + t * dx), lat - (ay + t * dy))
    return min(seg(l[i], l[i + 1]) for l in lines for i in range(len(l) - 1))


def path(points, closed=False):
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in points)
    return d + (' Z' if closed else '')


def main():
    countries = json.loads(Path(sys.argv[1]).read_text())
    rivers = json.loads(Path(sys.argv[2]).read_text())

    feature = next(f for f in countries['features'] if f['properties'].get('ADM0_A3') == 'EGY')
    geometry = feature['geometry']
    polygons = geometry['coordinates'] if geometry['type'] == 'MultiPolygon' else [geometry['coordinates']]
    ring = max((p[0] for p in polygons), key=len)
    assert min(lat for _, lat in ring) > 21.9, 'southern boundary must stay on the 22nd parallel'

    nile = []
    for f in rivers['features']:
        if f['properties'].get('name') == 'Nile':
            for part in f['geometry']['coordinates']:
                kept = [p for p in part if p[1] >= 21.9 and inside(p[0], p[1], ring)]
                if len(kept) > 1:
                    nile.append(kept)
    assert nile, 'Nile centreline missing from the rivers file'

    # Validate every city against real geometry before drawing anything.
    for key, lat, lon, _, _, _, check, _ in CITIES:
        coast, river = distance(lon, lat, [ring]), distance(lon, lat, nile)
        ok = {'in': inside(lon, lat, ring),
              'coast': inside(lon, lat, ring) or coast <= 0.12,
              'nile': inside(lon, lat, ring) and river <= 0.12}[check]
        assert ok, f'{key}: coordinate fails its {check} check (coast {coast:.3f}°, Nile {river:.3f}°)'

    projected = [project(lon, lat) for lon, lat in ring]
    far = max(range(len(projected)), key=lambda i: math.dist(projected[0], projected[i]))
    outline = rdp(projected[:far + 1], 0.45)[:-1] + rdp(projected[far:], 0.45)
    nile_main = [rdp([project(*p) for p in part], 0.4) for part in nile]
    nile_inset = [[project_inset(*p) for p in part if in_lens(p[0], p[1]) or LENS['lat'][0] - .3 <= p[1] <= LENS['lat'][1]]
                  for part in nile]
    nile_inset = [part for part in nile_inset if len(part) > 1]

    (lx0, ly0), (lx1, ly1) = project(LENS['lon'][0], LENS['lat'][1]), project(LENS['lon'][1], LENS['lat'][0])

    nodes = []
    for key, lat, lon, tier, ar, en, _, label in CITIES:
        layer = 'inset' if in_lens(lon, lat) else 'main'
        x, y = project_inset(lon, lat) if layer == 'inset' else project(lon, lat)
        node = {'key': key, 'tier': tier, 'layer': layer, 'lat': lat, 'lon': lon,
                'x': round(x, 1), 'y': round(y, 1), 'ar': ar, 'en': en, 'selected': key == SELECTED}
        if label:
            dx, dy, anchor = label
            node['label'] = {'x': round(x + dx, 1), 'y': round(y + dy, 1), 'anchor': anchor,
                             'px': round((x + dx) / VIEW_W * 100, 2), 'py': round((y + dy) / VIEW_H * 100, 2),
                             'leader': math.hypot(dx, dy) > 18}
        nodes.append(node)

    out = {
        'source': 'Natural Earth 1:50m Admin 0 – Countries and Rivers (public domain), ADM0_A3=EGY',
        'coverage_source': 'estavo-brokers-api config/estavo_market_coverage.php (markets); other points are main cities for reference',
        'viewBox': f'0 0 {VIEW_W} {VIEW_H}',
        'points': len(outline),
        'path': path(outline, True),
        'nile': [path(part) for part in nile_main],
        'nile_inset': [path(part) for part in nile_inset],
        'lens': {'x': round(lx0, 1), 'y': round(ly0, 1), 'w': round(lx1 - lx0, 1), 'h': round(ly1 - ly0, 1)},
        'inset': INSET,
        'nodes': nodes,
    }
    (ROOT / 'tools/data').mkdir(exist_ok=True)
    (ROOT / 'tools/data/egypt-map.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW_W} {VIEW_H}" width="{VIEW_W}" height="{VIEW_H}">\n'
           f'  <!-- Egypt outline and Nile. {out["source"]}. Generated by tools/build-egypt-map.py. -->\n'
           f'  <path d="{out["path"]}" fill="#f1f5f8" stroke="#47749a" stroke-width="1.5" stroke-linejoin="round"/>\n'
           + ''.join(f'  <path d="{d}" fill="none" stroke="#9fbad3" stroke-width="1.5"/>\n' for d in out['nile'])
           + '</svg>\n')
    (ROOT / 'assets/img/egypt-map.svg').write_text(svg)
    markets = sum(n['tier'] == 'market' for n in nodes)
    print(f'{len(ring)} → {len(outline)} outline points; Nile {sum(len(p) for p in nile)} pts; '
          f'{len(nodes)} validated cities ({markets} Estavo markets)')


if __name__ == '__main__':
    main()
