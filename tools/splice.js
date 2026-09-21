#!/usr/bin/env node
/* ============================================================
   Estavo v3 — head/body splice helper

   index.html and en.html each carry a large inline critical-CSS
   block plus the old ng.css/ng.js wiring. Rebuilding the pages
   means replacing exact line ranges without disturbing the
   analytics, canonical, hreflang and Open Graph markup around
   them, which must survive byte-for-byte.

   This replaces a region delimited by two marker strings,
   failing loudly if a marker is missing or ambiguous, so an
   off-by-one can never silently corrupt the head.

   Usage:
     node tools/splice.js <file> <startMarker> <endMarker> <replacementFile>
     node tools/splice.js <file> --show <startMarker> <endMarker>
   ============================================================ */
'use strict';

const fs = require('fs');

function fail(msg) {
  console.error(`splice: ${msg}`);
  process.exit(1);
}

function findUnique(haystack, needle, label) {
  const first = haystack.indexOf(needle);
  if (first === -1) fail(`${label} marker not found: ${JSON.stringify(needle)}`);
  const second = haystack.indexOf(needle, first + needle.length);
  if (second !== -1) fail(`${label} marker is ambiguous (appears more than once): ${JSON.stringify(needle)}`);
  return first;
}

function main() {
  const args = process.argv.slice(2);
  const file = args[0];
  if (!file || !fs.existsSync(file)) fail(`no such file: ${file}`);

  const show = args[1] === '--show';
  const startMarker = show ? args[2] : args[1];
  const endMarker = show ? args[3] : args[2];
  const replacementFile = show ? null : args[3];

  const src = fs.readFileSync(file, 'utf8');
  const start = findUnique(src, startMarker, 'start');
  const endAt = findUnique(src, endMarker, 'end');
  if (endAt < start) fail('end marker appears before start marker');

  const end = endAt + endMarker.length;

  if (show) {
    const region = src.slice(start, end);
    console.log(`region: ${region.length} bytes, ${region.split('\n').length} lines`);
    console.log('--- first 3 lines ---');
    console.log(region.split('\n').slice(0, 3).join('\n'));
    console.log('--- last 3 lines ---');
    console.log(region.split('\n').slice(-3).join('\n'));
    return;
  }

  if (!replacementFile || !fs.existsSync(replacementFile)) {
    fail(`no such replacement file: ${replacementFile}`);
  }

  const replacement = fs.readFileSync(replacementFile, 'utf8');
  const out = src.slice(0, start) + replacement + src.slice(end);
  fs.writeFileSync(file, out);

  const removed = end - start;
  console.log(`${file}: replaced ${removed} bytes with ${replacement.length} bytes`);
}

main();
