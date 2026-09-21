#!/usr/bin/env node
/* ============================================================
   Estavo v3 — per-section measurement

   Reports the rendered height and resolved padding of every
   top-level section, so spacing is tuned against real numbers
   rather than arithmetic. Reuses the CDP plumbing in shot.js.

   Usage: node tools/measure.js <url> [width]
   ============================================================ */
'use strict';

const http = require('http');
const net = require('net');
const crypto = require('crypto');
const fs = require('fs');
const { spawn } = require('child_process');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9700 + Math.floor(Math.random() * 300);

function getJSON(path) {
  return new Promise((resolve, reject) => {
    const req = http.get({ host: '127.0.0.1', port: PORT, path }, (res) => {
      let body = '';
      res.on('data', (c) => { body += c; });
      res.on('end', () => { try { resolve(JSON.parse(body)); } catch (e) { reject(e); } });
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
          `GET ${u.pathname}${u.search} HTTP/1.1\r\nHost: ${u.host}\r\n` +
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
          reject(new Error('WebSocket upgrade refused')); return;
        }
        this.buf = this.buf.slice(end + 4);
        this.sock.removeListener('data', onHandshake);
        this.sock.on('data', (c) => { this.buf = Buffer.concat([this.buf, c]); this._drain(); });
        this._drain();
        resolve();
      };
      this.sock.on('data', onHandshake);
    });
  }

  _drain() {
    for (;;) {
      if (this.buf.length < 2) return;
      let len = this.buf[1] & 0x7f;
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
    if (data.length < 126) header = Buffer.from([0x81, 0x80 | data.length]);
    else if (data.length < 65536) {
      header = Buffer.alloc(4); header[0] = 0x81; header[1] = 0xfe;
      header.writeUInt16BE(data.length, 2);
    } else {
      header = Buffer.alloc(10); header[0] = 0x81; header[1] = 0xff;
      header.writeBigUInt64BE(BigInt(data.length), 2);
    }
    this.sock.write(Buffer.concat([header, mask, masked]));
    return new Promise((resolve) => this.pending.set(id, { resolve }));
  }

  close() { try { this.sock.destroy(); } catch (e) { /* ignore */ } }
}

const EXPR = `JSON.stringify({
  total: document.documentElement.scrollHeight,
  sections: [...document.querySelectorAll('main > section, main > .es-hero, footer')].map((s, i) => {
    const cs = getComputedStyle(s);
    return {
      i,
      cls: (s.className || s.tagName).toString().replace('es-section', '').trim() || s.tagName.toLowerCase(),
      h: Math.round(s.getBoundingClientRect().height),
      pt: Math.round(parseFloat(cs.paddingBlockStart)),
      pb: Math.round(parseFloat(cs.paddingBlockEnd))
    };
  })
})`;

async function main() {
  const [url, widthArg] = process.argv.slice(2);
  if (!url) { console.error('usage: node tools/measure.js <url> [width]'); process.exit(2); }
  const width = Number(widthArg || 1440);

  const chrome = spawn(CHROME, [
    '--headless=new', `--remote-debugging-port=${PORT}`, '--disable-gpu', '--no-sandbox',
    '--hide-scrollbars', '--no-first-run',
    '--user-data-dir=' + fs.mkdtempSync('/tmp/es-measure-'), 'about:blank',
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
    await ws.send('Emulation.setDeviceMetricsOverride', {
      width, height: 900, deviceScaleFactor: 1, mobile: width < 768,
    });
    await ws.send('Page.navigate', { url });
    await new Promise((r) => setTimeout(r, 2600));

    const res = await ws.send('Runtime.evaluate', { expression: EXPR, returnByValue: true });
    const data = JSON.parse(res.result.value);

    console.log(`  width=${width}  total=${data.total}px`);
    let padTotal = 0;
    for (const s of data.sections) {
      padTotal += s.pt + s.pb;
      console.log(`   ${String(s.i).padStart(2)} ${s.cls.slice(0, 30).padEnd(32)} h=${String(s.h).padStart(5)}  pad=${s.pt}/${s.pb}`);
    }
    const pct = Math.round((padTotal / data.total) * 100);
    console.log(`  section padding total: ${padTotal}px (${pct}% of page)`);
  } finally {
    if (ws) ws.close();
    chrome.kill();
  }
}

main().catch((e) => { console.error(e.message); process.exit(1); });
