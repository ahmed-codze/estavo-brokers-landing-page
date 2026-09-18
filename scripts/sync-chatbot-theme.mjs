/** Reuse the Brokers chatbot's actual presentation rules, without its app runtime.
 * Run with Node 22+: node --experimental-strip-types scripts/sync-chatbot-theme.mjs
 * The generated asset is committed; a standalone landing checkout can serve it.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const broker = path.resolve(root, '../estavo-brokers');
const css = fs.readFileSync(path.join(broker, 'src/index.css'), 'utf8');
const themePath = path.join(broker, 'src/shared/theme/colors.ts');
const vars = new Map();
globalThis.document = { querySelector: () => null };
const { applyColorTokens } = await import(pathToFileURL(themePath));
applyColorTokens({ style: { setProperty: (name, value) => vars.set(name, value) } });
function block(selector) {
    const start = css.indexOf(`${selector} {`);
    if (start < 0) throw new Error(`Missing upstream selector: ${selector}`);
    let depth = 0;
    for (let end = css.indexOf('{', start); end < css.length; end++) {
        if (css[end] === '{') depth++;
        if (css[end] === '}' && --depth === 0) return css.slice(start, end + 1);
    }
    throw new Error(`Unclosed selector: ${selector}`);
}
const tokensStart = css.indexOf(':root {', css.indexOf('Estavo Assistant — Shared Glass Surface System'));
const tokens = css.slice(tokensStart + 7, css.indexOf('}', tokensStart));
const selectors = ['.assistant-input-surface', '.estavo-assistant-workspace', '.estavo-assistant-notes .chat-bubble-assistant', '.estavo-assistant-notes .chat-bubble-user'];
const rules = selectors.map(selector => `#raghad-support ${block(selector)}`).join('\n\n');
const dependencies = new Set([...`${tokens}\n${rules}\n${fs.readFileSync(path.join(root, 'assets/css/raghad.css'), 'utf8')}`.matchAll(/var\((--color-[\w-]+)/g)].map(x => x[1]));
const colorRules = [...dependencies].map(key => {
    if (!vars.has(key)) throw new Error(`Missing upstream color: ${key}`);
    return `  ${key}: ${vars.get(key)};`;
}).join('\n');
const sha = createHash('sha256').update(css).update(fs.readFileSync(themePath)).digest('hex').slice(0, 16);
fs.writeFileSync(path.join(root, 'assets/css/chatbot-shared.css'), `/* Generated from Brokers src/index.css + shared/theme/colors.ts.\n * Source fingerprint: ${sha}. Run scripts/sync-chatbot-theme.mjs; do not hand-edit. */\n#raghad-support {\n${colorRules}\n  --estavo-blue: var(--color-brand-primary);\n${tokens}}\n\n${rules}\n\n${block('@keyframes estavoAssistantCardOpen')}\n`);
console.log('Synced Brokers chatbot surfaces and colors.');
