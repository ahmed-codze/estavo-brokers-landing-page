#!/usr/bin/env python3
"""Build the homepage market map from Natural Earth and validated pin coordinates.

Sources (public domain), Natural Earth 1:50m:
  ne_50m_admin_0_countries.geojson   Egypt and its neighbours
  ne_50m_rivers_lake_centerlines.geojson   the Nile
  ne_50m_lakes.geojson   Lake Nasser
https://github.com/nvkelso/natural-earth-vector/tree/master/geojson

The map is the whole of Egypt (real outline, 22nd-parallel border with Halaib
inside) with unlabelled pins for the Estavo Brokers main markets. One market is
selected; the page attaches its projects card to that pin.

Usage:
  python3 tools/build-egypt-map.py countries.geojson rivers.geojson lakes.geojson

Writes:
  assets/img/egypt-map.svg      full-country outline (reference / reuse)
  tools/data/egypt-map.json     path, pins and label layout inlined by the homepage

Every pin is validated before anything is written: it must fall inside the
outline (coastal pins within 0.12° of the coast). A wrong coordinate fails the
build, as does a label that would leave the map. Geography is never mirrored.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Frame: the whole country plus enough sea and neighbouring land to read as a real map.
PAD = 0
LON0, LON1 = 24.00, 37.60
LAT0, LAT1 = 32.30, 21.30
NEIGHBOURS = ['LBY', 'SDN', 'ISR', 'PSX', 'JOR', 'SAU']
COS = math.cos(math.radians(26.8))         # equirectangular correction at Egypt's mid-latitude
VIEW_W = 640
K = (VIEW_W - 2 * PAD) / ((LON1 - LON0) * COS)   # px per degree of latitude
VIEW_H = round((LAT0 - LAT1) * K + 2 * PAD)

# Exactly the Estavo Brokers main markets (product decision, 2026-10-03) — no
# other cities. "Red Sea" is pinned at Hurghada, the coast's hub.
# check: in = inside the outline · coast = within 0.12° of the coast
# Pins are unlabelled on the map; names live in the accessible label.
PINS = [
    # key              lat     lon     ar                  en                check    label
    ('sheikh-zayed',   30.045, 30.980, 'الشيخ زايد',       'Sheikh Zayed',   'in',    None),
    ('october',        29.950, 30.925, '6 أكتوبر',          '6th of October', 'in',    None),
    ('new-cairo',      30.020, 31.460, 'القاهرة الجديدة', 'New Cairo',      'in',    None),
    ('new-capital',    30.020, 31.760, 'العاصمة الإدارية', 'New Capital',    'in',    None),
    ('shorouk',        30.120, 31.620, 'الشروق',           'Shorouk',        'in',    None),
    ('obour',          30.228, 31.475, 'العبور',           'Obour',          'in',    None),
    ('north-coast',    30.830, 28.950, 'الساحل الشمالي',   'North Coast',    'coast', None),
    ('ain-sokhna',     29.600, 32.320, 'العين السخنة',     'Ain Sokhna',     'coast', None),
    ('red-sea',        27.260, 33.810, 'البحر الأحمر',     'Red Sea',        'coast', None),
]
# Only the Estavo Brokers main markets are drawn (product decision, 2026-10-04):
# no secondary city points.
CITIES = []
SELECTED = 'sheikh-zayed'


def project(lon, lat):
    return (PAD + (lon - LON0) * COS * K, PAD + (LAT0 - lat) * K)


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


def coast_distance(lon, lat, ring):
    def seg(a, b):
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((lon - ax) * dx + (lat - ay) * dy) / (dx * dx + dy * dy or 1e-12)))
        return math.hypot(lon - (ax + t * dx), lat - (ay + t * dy))
    return min(seg(ring[i], ring[(i + 1) % len(ring)]) for i in range(len(ring)))


def pct(x, y):
    return round(x / VIEW_W * 100, 2), round(y / VIEW_H * 100, 2)


def simplify(points):
    far = max(range(len(points)), key=lambda i: math.dist(points[0], points[i]))
    return rdp(points[:far + 1], 0.5)[:-1] + rdp(points[far:], 0.5)


def main():
    countries = json.loads(Path(sys.argv[1]).read_text())
    feature = next(f for f in countries['features'] if f['properties'].get('ADM0_A3') == 'EGY')
    geometry = feature['geometry']
    polygons = geometry['coordinates'] if geometry['type'] == 'MultiPolygon' else [geometry['coordinates']]
    ring = max((p[0] for p in polygons), key=len)
    assert min(lat for _, lat in ring) > 21.9, 'southern boundary must stay on the 22nd parallel'

    for key, lat, lon, _, _, check, _ in PINS:
        coast = coast_distance(lon, lat, ring)
        ok = inside(lon, lat, ring) if check == 'in' else (inside(lon, lat, ring) or coast <= 0.12)
        assert ok, f'{key}: coordinate fails its {check} check (coast {coast:.3f}°)'
        assert LAT1 < lat < LAT0 and LON0 < lon < LON1, f'{key}: outside the map frame'

    def to_path(points, closed=True):
        pts = simplify([project(lon, lat) for lon, lat in points]) if closed else rdp([project(lon, lat) for lon, lat in points], 0.5)
        return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + (' Z' if closed else ''), len(pts)

    d, points = to_path(ring)

    neighbours = []
    for f in countries['features']:
        if f['properties'].get('ADM0_A3') in NEIGHBOURS:
            g = f['geometry']
            for poly in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]):
                outer = poly[0]
                if any(LON0 - 3 < lon < LON1 + 3 and LAT1 - 3 < lat < LAT0 + 3 for lon, lat in outer) and len(outer) > 3:
                    neighbours.append(to_path(outer)[0])

    rivers = json.loads(Path(sys.argv[2]).read_text())
    nile_lines = [[p for p in part if p[1] >= 21.9]
                  for f in rivers['features'] if f['properties'].get('name') == 'Nile'
                  for part in f['geometry']['coordinates']]
    nile_lines = [l for l in nile_lines if len(l) > 1]

    def near(lon, lat, lines):
        def seg(a, b):
            (ax, ay), (bx, by) = a, b
            dx, dy = bx - ax, by - ay
            t = max(0, min(1, ((lon - ax) * dx + (lat - ay) * dy) / (dx * dx + dy * dy or 1e-12)))
            return math.hypot(lon - (ax + t * dx), lat - (ay + t * dy))
        return min(seg(l[i], l[i + 1]) for l in lines for i in range(len(l) - 1))

    cities = []
    for key, lat, lon, ar, en, check in CITIES:
        ok = {'in': inside(lon, lat, ring),
              'coast': inside(lon, lat, ring) or coast_distance(lon, lat, ring) <= 0.12,
              'nile': inside(lon, lat, ring) and near(lon, lat, nile_lines) <= 0.12}[check]
        assert ok, f'{key}: coordinate fails its {check} check'
        x, y = project(lon, lat)
        px, py = pct(x, y)
        cities.append({'key': key, 'lat': lat, 'lon': lon, 'px': px, 'py': py, 'ar': ar, 'en': en})

    nile = [to_path([p for p in part if p[1] >= LAT1], closed=False)[0]
            for f in rivers['features'] if f['properties'].get('name') == 'Nile'
            for part in f['geometry']['coordinates'] if sum(p[1] >= LAT1 for p in part) > 1]

    lakes = json.loads(Path(sys.argv[3]).read_text())
    water = []
    for f in lakes['features']:
        if f['properties'].get('name') in ('Lake Nasser', 'Dead Sea'):
            g = f['geometry']
            for poly in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]):
                water.append(to_path(poly[0])[0])

    pins = []
    for key, lat, lon, ar, en, _, label in PINS:
        x, y = project(lon, lat)
        px, py = pct(x, y)
        pin = {'key': key, 'lat': lat, 'lon': lon, 'x': round(x, 1), 'y': round(y, 1), 'px': px, 'py': py,
               'ar': ar, 'en': en, 'selected': key == SELECTED}
        if label:
            dx, dy, anchor = label
            lx, ly = pct(x + dx, y + dy)
            assert 3 <= lx <= 97 and 5 <= ly <= 95, f'{key}: label leaves the map'
            pin['label'] = {'px': lx, 'py': ly, 'anchor': anchor}
        pins.append(pin)

    out = {
        'source': 'Natural Earth 1:50m Admin 0 – Countries (public domain), ADM0_A3=EGY',
        'coverage_source': 'Estavo Brokers main markets (product owner, 2026-10-03)',
        'viewBox': f'0 0 {VIEW_W} {VIEW_H}',
        'points': points,
        'neighbours': neighbours,
        'nile': nile,
        'lakes': water,
        'path': d,
        'nodes': pins,
        'cities': cities,
    }
    (ROOT / 'tools/data').mkdir(exist_ok=True)
    (ROOT / 'tools/data/egypt-map.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW_W} {VIEW_H}" width="{VIEW_W}" height="{VIEW_H}">\n'
           f'  <!-- Egypt, neighbours, Nile and Lake Nasser. {out["source"]}. Generated by tools/build-egypt-map.py. -->\n'
           f'  <rect width="{VIEW_W}" height="{VIEW_H}" fill="#dceaf5"/>\n'
           + ''.join(f'  <path d="{n}" fill="#eef1f4" stroke="#c9d3dc" stroke-width="1"/>\n' for n in neighbours)
           + f'  <path d="{d}" fill="#fafcff" stroke="#47749a" stroke-width="1.5" stroke-linejoin="round"/>\n'
           + ''.join(f'  <path d="{w}" fill="#dceaf5" stroke="#9fbad3" stroke-width="1"/>\n' for w in water)
           + ''.join(f'  <path d="{r}" fill="none" stroke="#8fb3d1" stroke-width="1.5"/>\n' for r in nile)
           + '</svg>\n')
    (ROOT / 'assets/img/egypt-map.svg').write_text(svg)
    print(f'{len(ring)} → {points} outline points; {len(neighbours)} neighbour shapes; Nile {len(nile)} parts; viewBox {out["viewBox"]}; {len(pins)} validated pins (selected: {SELECTED})')


if __name__ == '__main__':
    main()
