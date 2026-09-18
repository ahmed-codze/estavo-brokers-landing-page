'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const { JSDOM } = require('jsdom');
const source = fs.readFileSync(path.join(__dirname, '../assets/js/raghad.js'), 'utf8');
const tick = () => new Promise(resolve => setImmediate(resolve));

function setup(locale = 'en', fetcher = async () => ({ ok: false, status: 503, json: async () => ({}) })) {
    const dom = new JSDOM(`<!doctype html><html lang="${locale}"><body><div class="sticky-cta"></div></body></html>`, {
        url: 'https://estavo-brokers.com/website/', runScripts: 'outside-only',
    });
    const { window } = dom;
    const script = window.document.createElement('script');
    script.src = 'https://estavo-brokers.com/assets/js/raghad.js';
    script.dataset.endpoint = 'https://api-brokers.estavo.space/api/public/support/chat';
    Object.defineProperty(window.document, 'currentScript', { value: script });
    window.fetch = fetcher;
    window.eval(source);
    const get = selector => window.document.querySelector(selector);
    function send(message) {
        get('.raghad-input').value = message;
        get('.raghad-composer').dispatchEvent(new window.Event('submit', { cancelable: true, bubbles: true }));
    }
    return { dom, window, get, send };
}

test('launcher opens a labelled Arabic dialog, focuses input, and Escape restores focus', () => {
    const { dom, window, get } = setup('ar');
    assert.equal(get('#raghad-support').dir, 'rtl');
    get('.raghad-launcher').click();
    assert.equal(get('#raghad-panel').hidden, false);
    assert.equal(get('.raghad-launcher').getAttribute('aria-expanded'), 'true');
    assert.equal(window.document.activeElement, get('.raghad-input'));
    get('.raghad-input').dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    assert.equal(get('#raghad-panel').hidden, true);
    assert.equal(window.document.activeElement, get('.raghad-launcher'));
    assert.equal(get('.raghad-footer a').href, 'https://estavo-brokers.com/privacy.html');
    dom.window.close();
});

test('requests carry only user input and encrypted token; model markup stays inert', async () => {
    const calls = [];
    const { dom, get, send } = setup('en', async (url, options) => {
        calls.push({ url, options });
        return { ok: true, json: async () => ({
            message: '<img src=x onerror=alert(1)> 40 credits', conversation_token: `signed-${calls.length}`,
            sources: [{ product: 'brokers' }, { product: '<script>' }],
        }) };
    });
    send('How do credits work?');
    await tick();
    assert.equal(get('.raghad-message--assistant img'), null);
    assert.match(get('.raghad-message--assistant').textContent, /<img/);
    assert.match(get('.raghad-sources').textContent, /Estavo Brokers/);
    assert.equal(get('.raghad-input').value, '');
    send('And PDF offers?');
    await tick();
    assert.deepEqual(JSON.parse(calls[1].options.body), {
        message: 'And PDF offers?', locale: 'en', conversation_token: 'signed-1',
    });
    assert.equal(calls[0].options.credentials, 'omit');
    assert.equal(calls[0].options.cache, 'no-store');
    assert.equal(dom.window.localStorage.length, 0);
    assert.equal(dom.window.sessionStorage.length, 0);
    dom.window.close();
});

test('failure keeps the draft and retry replaces the failed bubble', async () => {
    let calls = 0;
    const { dom, get, send } = setup('en', async () => {
        calls++;
        return calls === 1
            ? { ok: false, status: 503, json: async () => ({}) }
            : { ok: true, json: async () => ({ message: 'Hello', conversation_token: 'valid' }) };
    });
    send('My question');
    await tick();
    assert.equal(get('.raghad-input').value, 'My question');
    assert.equal(get('.raghad-error').hidden, false);
    assert.equal(get('.raghad-send').disabled, false);
    send('My question');
    await tick();
    assert.equal(dom.window.document.querySelectorAll('.raghad-message--user').length, 1);
    assert.equal(get('.raghad-error').hidden, true);
    dom.window.close();
});

test('expired conversations reset the token and show a useful retry message', async () => {
    const calls = [];
    const { dom, get, send } = setup('en', async (url, options) => {
        calls.push(JSON.parse(options.body));
        return calls.length === 2
            ? { ok: false, status: 422, json: async () => ({ errors: { conversation_token: ['Expired'] } }) }
            : { ok: true, json: async () => ({ message: 'Hello', conversation_token: 'token' }) };
    });
    send('Hello'); await tick();
    send('Follow-up'); await tick();
    assert.match(get('.raghad-error').textContent, /expired/);
    send('Follow-up'); await tick();
    assert.equal(calls[2].conversation_token, null);
    dom.window.close();
});

test('new chat aborts pending work and ignores stale replies', async () => {
    let resolve;
    let requestSignal;
    const { dom, get, send } = setup('en', (url, options) => {
        requestSignal = options.signal;
        return new Promise(done => { resolve = done; });
    });
    send('Old question');
    assert.equal(get('.raghad-send').disabled, true);
    get('.raghad-reset').click();
    assert.equal(requestSignal.aborted, true);
    resolve({ ok: true, json: async () => ({ message: 'Stale answer', conversation_token: 'old' }) });
    await tick();
    assert.equal(get('.raghad-messages').children.length, 0);
    assert.equal(get('.raghad-intro').hidden, false);
    assert.equal(get('.raghad-input').readOnly, false);
    dom.window.close();
});

test('duplicate submissions, empty messages and overlong messages do not call the server', async () => {
    let calls = 0;
    let resolve;
    const { dom, get, send } = setup('en', () => {
        calls++;
        return new Promise(done => { resolve = done; });
    });
    send(' ');
    send('x'.repeat(2001));
    assert.equal(calls, 0);
    assert.match(get('.raghad-error').textContent, /too long/);
    send('Actual question'); send('Duplicate');
    assert.equal(calls, 1);
    resolve({ ok: true, json: async () => ({ message: 'Answer', conversation_token: 'valid' }) });
    await tick();
    dom.window.close();
});

test('rate limits and malformed success responses preserve a path to human support', async () => {
    for (const response of [
        { ok: false, status: 429, json: async () => ({}) },
        { ok: true, json: async () => ({ message: '', conversation_token: 'token' }) },
    ]) {
        const { dom, get, send } = setup('en', async () => response);
        send('Help'); await tick();
        assert.equal(get('.raghad-error').hidden, false);
        assert.equal(get('.raghad-human').href, 'https://wa.me/201069528393');
        assert.equal(get('.raghad-input').value, 'Help');
        dom.window.close();
    }
});

test('all four landing routes load the same widget with correct relative assets', () => {
    for (const name of ['index.html', 'en.html', 'website/index.html', 'website/en.html']) {
        const html = fs.readFileSync(path.join(__dirname, '..', name), 'utf8');
        const dom = new JSDOM(html, { url: `https://estavo-brokers.com/${name}` });
        const script = dom.window.document.querySelector('script[src*="raghad.js"]');
        const style = dom.window.document.querySelector('link[href*="raghad.css"]');
        assert.equal(new URL(script.src).pathname, '/assets/js/raghad.js');
        assert.equal(new URL(style.href).pathname, '/assets/css/raghad.css');
        assert.equal(script.dataset.endpoint, 'https://api-brokers.estavo.space/api/public/support/chat');
        dom.window.close();
    }
});
