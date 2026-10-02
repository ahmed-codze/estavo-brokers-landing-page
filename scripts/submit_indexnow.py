#!/usr/bin/env python3
"""Notify participating search engines after the live pages and key file exist.

Key is supplied through INDEXNOW_KEY, never stored in this repository. Place the
verification file at the web root; this command checks it before submitting.
"""
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET
from urllib.parse import urlparse

root=Path(__file__).resolve().parent.parent
key=os.environ.get('INDEXNOW_KEY','')
if not re.fullmatch(r'[a-zA-Z0-9-]{8,128}',key):
    raise SystemExit('Supply a valid INDEXNOW_KEY in the environment.')
base='https://estavo-brokers.com'
key_location=base+'/'+key+'.txt'
verification=subprocess.run(['curl','--fail','--silent','--show-error','--max-time','25',key_location],capture_output=True)
if verification.returncode or verification.stdout.decode().strip()!=key:
    raise SystemExit('Live root verification file is missing or does not match; no URLs submitted.')
urls=[node.text for node in ET.parse(root/'sitemap.xml').getroot().findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
if not all(urlparse(url).netloc=='estavo-brokers.com' for url in urls):
    raise SystemExit('Sitemap contains an unexpected host; no URLs submitted.')
payload={'host':'estavo-brokers.com','key':key,'keyLocation':key_location,'urlList':urls}
with tempfile.TemporaryDirectory(prefix='estavo-indexnow-') as directory:
    file=Path(directory)/'payload.json'
    file.write_text(json.dumps(payload));file.chmod(0o600)
    response=subprocess.run(['curl','--silent','--show-error','--max-time','30','--output',str(Path(directory)/'response'),
                             '--write-out','%{http_code}','--header','Content-Type: application/json; charset=utf-8',
                             '--data-binary','@'+str(file),'https://api.indexnow.org/indexnow'],capture_output=True)
    status=response.stdout.decode().strip()
    if response.returncode or status not in ('200','202'):
        raise SystemExit('IndexNow submission failed (HTTP '+status+'); inspect service status before retrying.')
    print(json.dumps({'submitted_urls':len(urls),'http_status':int(status),'meaning':'URLs received; indexing and recommendations are not guaranteed.'}))
