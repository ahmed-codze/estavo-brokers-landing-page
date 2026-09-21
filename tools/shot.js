#!/usr/bin/env node
/* ============================================================
   Estavo v3 — narrow-viewport screenshots

   Headless Chrome floors --window-size at ~500 CSS px, so the
   320/360/390/430 widths the QA matrix requires (Visual Theme
   Plan v1 §19) cannot be reached with CLI flags alone.

   This drives the DevTools Protocol directly and calls
   Emulation.setDeviceMetricsOverride, which does honour narrow
   widths. Implemented with a hand-rolled WebSocket client so
   the repo needs no dependencies (there is no package.json).

   Usage:
     node tools/shot.js <url> <out.png> <width> [height] [--reduced] [--no-js] [--viewport]
     node tools/shot.js <url> --probe <width> [height] [--reduced] [--no-js]
   ============================================================ */
'use strict';

const http = require('http');
const net = require('net');
const crypto = require('crypto');
const fs = require('fs');
const { spawn } = require('child_process');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9222 + Math.floor(Math.random() * 400);

/* Pages use root-relative asset paths (/assets/...), which a
   file:// URL resolves against the filesystem root rather than
   the site root — so a subdirectory page loads completely
   unstyled and the screenshot is meaningless. Pass an http://
   URL (see tools/serve.sh) to capture what a user actually sees. */
function warnIfFileUrl(url) {
  if (url.startsWith('file://') && /\/[^/]+\/[^/]+\.html$/.test(url)) {
    console.error('  ⚠ subdirectory page over file:// — root-relative assets will not load.');
    console.error('    Serve the site and use an http:// URL instead.');
  }
}

function getJSON(path) {
  return new Promise((resolve, reject) => {
    const req = http.get({ host: '127.0.0.1', port: PORT, path }, (res) => {
      let body = '';
      res.on('data', (c) => { body += c; });
      res.on('end', () => {
        try { resolve(JSON.parse(body)); } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
  });
}

async function waitForPort(tries = 80) {
  for (let i = 0; i < tries; i++) {
    try { return await getJSON('/json/version'); }
    catch (e) { await new Promise((r) => setTimeout(r, 125)); }
  }
  throw new Error('Chrome DevTools port never opened');
}

/* ── Minimal WebSocket client (RFC 6455, client-to-server
      frames masked, no extensions, no fragmentation). ────── */
class WS {
  constructor(url) {
    const u = new URL(url);
    this.seq = 0;
    this.pending = new Map();
    this.buf = Buffer.alloc(0);
    this.ready = new Promise((resolve, reject) => {
      const key = crypto.randomBytes(16).toString('base64');
      this.sock = net.connect(Number(u.port), u.hostname, () => {
        this.sock.write(
          `GET ${u.pathname}${u.search} HTTP/1.1\r\n` +
          `Host: ${u.host}\r\n` +
          'Upgrade: websocket\r\nConnection: Upgrade\r\n' +
          `Sec-WebSocket-Key: ${key}\r\nSec-WebSocket-Version: 13\r\n\r\n`
        );
      });
      this.sock.on('error', reject);
      const onHandshake = (chunk) => {
        this.buf = Buffer.concat([this.buf, chunk]);
        const end = this.buf.indexOf('\r\n\r\n');
        if (end === -1) return;
        if (!/HTTP\/1.1 101/.test(this.buf.slice(0, end).toString())) {
          reject(new Error('WebSocket upgrade refused'));
          return;
        }
        this.buf = this.buf.slice(end + 4);
        this.sock.removeListener('data', onHandshake);
        this.sock.on('data', (c) => this._onData(c));
        this._drain();
        resolve();
      };
      this.sock.on('data', onHandshake);
    });
  }

  _onData(chunk) {
    this.buf = Buffer.concat([this.buf, chunk]);
    this._drain();
  }

  _drain() {
    for (;;) {
      if (this.buf.length < 2) return;
      const b1 = this.buf[1];
      let len = b1 & 0x7f;
      let off = 2;
      if (len === 126) {
        if (this.buf.length < 4) return;
        len = this.buf.readUInt16BE(2); off = 4;
      } else if (len === 127) {
        if (this.buf.length < 10) return;
        len = Number(this.buf.readBigUInt64BE(2)); off = 10;
      }
      if (this.buf.length < off + len) return;
      const payload = this.buf.slice(off, off + len).toString();
      this.buf = this.buf.slice(off + len);
      let msg;
      try { msg = JSON.parse(payload); } catch (e) { continue; }
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        resolve(msg.result || {});
      }
    }
  }

  send(method, params) {
    const id = ++this.seq;
    const data = Buffer.from(JSON.stringify({ id, method, params: params || {} }));
    const mask = crypto.randomBytes(4);
    const masked = Buffer.alloc(data.length);
    for (let i = 0; i < data.length; i++) masked[i] = data[i] ^ mask[i % 4];

    let header;
    if (data.length < 126) {
      header = Buffer.from([0x81, 0x80 | data.length]);
    } else if (data.length < 65536) {
      header = Buffer.alloc(4);
      header[0] = 0x81; header[1] = 0xfe;
      header.writeUInt16BE(data.length, 2);
    } else {
      header = Buffer.alloc(10);
      header[0] = 0x81; header[1] = 0xff;
      header.writeBigUInt64BE(BigInt(data.length), 2);
    }

    this.sock.write(Buffer.concat([header, mask, masked]));
    return new Promise((resolve) => this.pending.set(id, { resolve }));
  }

  close() { try { this.sock.destroy(); } catch (e) { /* ignore */ } }
}

async function main() {
  const [url, out, widthArg, heightArg, ...flags] = process.argv.slice(2);
  if (!url || !out || !widthArg) {
    console.error('usage: node tools/shot.js <url> <out.png|--probe> <width> [height] [--reduced] [--no-js] [--viewport]');
    process.exit(2);
  }
  const width = Number(widthArg);
  const height = Number(heightArg || 900);
  const probe = out === '--probe';
  const reduced = flags.includes('--reduced');
  const noJs = flags.includes('--no-js');
  const viewportOnly = flags.includes('--viewport');
  warnIfFileUrl(url);

  const chrome = spawn(CHROME, [
    '--headless=new',
    `--remote-debugging-port=${PORT}`,
    '--disable-gpu',
    '--no-sandbox',
    '--hide-scrollbars',
    '--no-first-run',
    '--user-data-dir=' + fs.mkdtempSync('/tmp/es-chrome-'),
    'about:blank',
  ], { stdio: 'ignore' });

  let ws;
  try {
    await waitForPort();
    const targets = await getJSON('/json/list');
    const page = targets.find((t) => t.type === 'page') || targets[0];
    ws = new WS(page.webSocketDebuggerUrl);
    await ws.ready;

    await ws.send('Page.enable');
    await ws.send('Runtime.enable');

    if (reduced) {
      await ws.send('Emulation.setEmulatedMedia', {
        features: [{ name: 'prefers-reduced-motion', value: 'reduce' }],
      });
    }
    if (noJs) await ws.send('Emulation.setScriptExecutionDisabled', { value: true });

    /* The override is what CLI flags cannot do: a true narrow
       viewport, below Chrome's 500px window floor. */
    await ws.send('Emulation.setDeviceMetricsOverride', {
      width, height, deviceScaleFactor: 1, mobile: width < 768,
    });

    await ws.send('Page.navigate', { url });
    await new Promise((r) => setTimeout(r, 1200));

    /* IntersectionObserver only fires for elements inside the
       viewport, but captureBeyondViewport paints the whole page
       without scrolling — so reveal-on-scroll content would
       photograph blank. Walk the page once to trigger every
       observer, then return to the top before capturing. */
    if (!noJs) {
      await ws.send('Runtime.evaluate', {
        expression: `(async () => {
          const step = window.innerHeight * 0.8;
          const total = document.documentElement.scrollHeight;
          for (let y = 0; y < total; y += step) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 90));
          }
          window.scrollTo(0, 0);
          await new Promise(r => setTimeout(r, 350));
        })()`,
        awaitPromise: true,
      });
    }
    await new Promise((r) => setTimeout(r, 600));

    const metrics = await ws.send('Runtime.evaluate', {
      expression: `JSON.stringify({
        inner: window.innerWidth,
        scrollW: document.documentElement.scrollWidth,
        scrollH: document.documentElement.scrollHeight,
        overflow: document.documentElement.scrollWidth > window.innerWidth + 1
      })`,
      returnByValue: true,
    });
    const m = JSON.parse(metrics.result.value);

    if (probe) {
      console.log(JSON.stringify({ requested: width, reduced, noJs, ...m }));
    } else {
      const full = await ws.send('Page.captureScreenshot', {
        format: 'png', captureBeyondViewport: !viewportOnly,
      });
      fs.writeFileSync(out, Buffer.from(full.data, 'base64'));
      console.log(`${out}  requested=${width} inner=${m.inner} h=${m.scrollH}` +
        (m.overflow ? '  ⚠ HORIZONTAL OVERFLOW' : ''));
    }
  } finally {
    if (ws) ws.close();
    chrome.kill();
  }
}

main().catch((e) => { console.error(e.message); process.exit(1); });
