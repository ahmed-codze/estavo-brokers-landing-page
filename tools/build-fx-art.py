#!/usr/bin/env python3
"""Estavo Signal illustrations — runner.

Usage:
    python3 tools/build-fx-art.py            # every module in tools/fx_art/ (except kit.py)
    python3 tools/build-fx-art.py home broker-ai
    python3 tools/build-fx-art.py --list     # also print every label anchor

Each tools/fx_art/<key>.py exposes `scenes() -> list[kit.Scene]` (see kit.py docstring).
For each scene it writes three files into assets/img/fx/:
    <key>-<scene>.svg        intro assembly (one-shot) + ambient loops - swap in when first seen
    <key>-<scene>-loop.svg   ambient loops only - swap in when the scene RE-enters the viewport
    <key>-<scene>-still.svg  final state, no CSS - <img src>, no-JS, reduced motion, print,
                             and what to swap back to while the scene is off screen
It checks all three parse, keeps them <= 60,000 bytes, keeps looping animations within
kit.LOOP_BUDGET, and merges per-scene metadata into assets/img/fx/anchors.json:
    {width, height, ratio, own_floor, loops, anchors: {name: {x, y, kind, side, [w, h]}}}
x/y (and w/h) are % of the art box. own_floor=true: the scene draws its own floor grid, so
omit .fx-stage__floor on that stage. Pure stdlib; no fonts needed.
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = HERE / 'fx_art'
ROOT = HERE.parent
OUT = ROOT / 'assets/img/fx'
LIMIT = 60000  # bytes (strict reading of the 60 KB budget)

sys.dont_write_bytecode = True
sys.path.insert(0, str(ART))
import kit  # noqa: E402


def load(key):
    spec = importlib.util.spec_from_file_location(f'fx_art_{key.replace("-", "_")}', ART / f'{key}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    show = '--list' in argv
    keys = [a for a in argv if not a.startswith('--')]
    if not keys:
        keys = sorted(p.stem for p in ART.glob('*.py') if p.stem not in ('kit', '__init__') and not p.stem.startswith('_'))
    anchors_path = OUT / 'anchors.json'
    anchors = json.loads(anchors_path.read_text()) if anchors_path.exists() else {}
    failed = False
    for key in keys:
        for scene in load(key).scenes():
            st = kit.write_scene(key, scene, OUT)
            anchors[st['name']] = {'width': st['width'], 'height': st['height'],
                                   'ratio': round(st['width'] / st['height'], 4), 'own_floor': True,
                                   'loops': st['loops'], 'anchors': st['anchors']}
            big = max(st['animated_bytes'], st['loop_bytes'], st['still_bytes'])
            flag = '' if big <= LIMIT else f'  !! over {LIMIT} bytes'
            failed |= big > LIMIT
            print(f"{st['name']:<28} {st['width']}x{st['height']:<4} anim {st['animated_bytes']:>6} B"
                  f"  loop {st['loop_bytes']:>6} B  still {st['still_bytes']:>6} B  loops {st['loops']}{flag}")
            if show:
                for n, a in st['anchors'].items():
                    print(f"    {n:<18} x {a['x']:6.2f}%  y {a['y']:6.2f}%")
    OUT.mkdir(parents=True, exist_ok=True)
    anchors_path.write_text(json.dumps(dict(sorted(anchors.items())), indent=1, ensure_ascii=False) + '\n')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
