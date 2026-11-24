#!/usr/bin/env python3
"""Stamp every local asset reference in i/index.html with ?v=<content hash>.

Static files on estavo-brokers.com are cached for 30 days as immutable, so the
invite page must change the URL whenever a file changes. Run after editing any
image, video or the page: python3 tools/version-invite-assets.py
"""
import hashlib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'i' / 'index.html'
REF = re.compile(r'(?<![\w/.-])((?:\.\./(?:assets|partners)/|img/|video/)[A-Za-z0-9_%./ -]+?\.(?:webp|png|svg|jpg|mp4))(\?v=[0-9a-f]{8})?(?=["\')\s,])')


def stamp(match: re.Match) -> str:
    ref = match.group(1)
    path = (PAGE.parent / ref.replace('%20', ' ')).resolve()
    if not path.is_file():
        raise SystemExit(f'missing asset: {ref}')
    return f'{ref}?v={hashlib.sha256(path.read_bytes()).hexdigest()[:8]}'


html = PAGE.read_text(encoding='utf-8')
out, count = REF.subn(stamp, html)
PAGE.write_text(out, encoding='utf-8')
print(f'stamped {count} asset references')
