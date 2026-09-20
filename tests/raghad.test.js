'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const { JSDOM } = require('jsdom');
const source = fs.readFileSync(path.join(__dirname, '../assets/js/raghad.js'), 'utf8');
const tick = () => new Promise(resolve => setImmediate(resolve));

function setup(locale = 'en', fetcher = async () => ({ ok: false, status: 503, json: async () => ({}) }), options = {}) {
    const dom = new JSDOM(`<!doctype html><html lang="${locale}"><body><div class="sticky-cta"></div></body></html>`, {
        url: options.url || 'https://estavo-brokers.com/website/', runScripts: 'outside-only',
    });
    const { window } = dom;
    const script = window.document.createElement('script');
    script.src = 'https://estavo-brokers.com/assets/js/raghad.js';
    if (options.disabledHosts) script.dataset.disabledHosts = options.disabledHosts;
    script.dataset.endpoint = 'https://api-brokers.estavo.space/api/public/support/chat';
    Object.defineProperty(window.document, 'currentScript', { value: script });
    window.fetch = fetcher;
    if (options.handoff) window.sessionStorage.setItem('estavo-raghad-language-handoff-v1', options.handoff);
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
    assert.equal(get('.raghad-sources'), null);
    assert.doesNotMatch(get('.raghad-message--assistant').textContent, /From the guide|من دليل/);
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
    assert.equal(requestSignal.aborted, false);
    get('.raghad-confirm-reset').click();
    assert.equal(requestSignal.aborted, true);
    resolve({ ok: true, json: async () => ({ message: 'Stale answer', conversation_token: 'old' }) });
    await tick();
    assert.equal(get('.raghad-messages').children.length, 0);
    assert.equal(get('.raghad-intro').hidden, false);
    assert.equal(get('.raghad-input').readOnly, false);
    assert.equal(get('.raghad-status').hidden, true);
    assert.equal(get('.raghad-input').value, '');
    dom.window.close();
});

test('business quick actions use the approved questions in both languages', () => {
    const expected = {
        ar: ['إيه هو استافو؟', 'ازاي الاقي انسب مشاريع ووحدات لعملائي؟', 'ازاي اعمل موقع عقاري ذكي باسمي؟'],
        en: ['What is Estavo?', 'How can I find the best projects and units for my clients?', 'How can I create a smart real estate website under my own name?'],
    };
    for (const locale of ['ar', 'en']) {
        const { dom } = setup(locale);
        assert.deepEqual(Array.from(dom.window.document.querySelectorAll('.raghad-starter'), button => button.textContent), expected[locale]);
        dom.window.close();
    }
});

test('quick actions clear immediately and show localized waiting feedback until the reply', async () => {
    for (const locale of ['ar', 'en']) {
        let resolve;
        let submitted;
        const { dom, get } = setup(locale, (url, options) => {
            submitted = JSON.parse(options.body).message;
            return new Promise(done => { resolve = done; });
        });
        const prompt = get('.raghad-starter').textContent;
        get('.raghad-starter').click();
        assert.equal(submitted, prompt);
        assert.equal(get('.raghad-input').value, '');
        assert.equal(get('.raghad-input').readOnly, true);
        assert.equal(get('.raghad-message--user p').textContent, prompt);
        assert.equal(get('.raghad-status').hidden, false);
        assert.match(get('.raghad-status').textContent, locale === 'ar' ? /رغد بتراجع/ : /Raghad is checking/);
        assert.equal(get('.raghad-thinking-dots').children.length, 3);
        assert.equal(get('.raghad-thinking-dots').getAttribute('aria-hidden'), 'true');
        resolve({ ok: true, json: async () => ({ message: 'Answer', conversation_token: 'signed', sources: [{ product: 'brokers' }, { product: 'ai' }] }) });
        await tick();
        assert.equal(get('.raghad-status').hidden, true);
        assert.equal(get('.raghad-input').value, '');
        assert.equal(get('.raghad-sources'), null);
        assert.equal(get('.raghad-message--assistant p').textContent, 'Answer');
        dom.window.close();
    }
});

test('a failed quick action restores the question for retry and stops the waiting feedback', async () => {
    let reject;
    const { dom, get } = setup('en', () => new Promise((resolve, fail) => { reject = fail; }));
    const prompt = get('.raghad-starter').textContent;
    get('.raghad-starter').click();
    assert.equal(get('.raghad-input').value, '');
    reject(new Error('Network unavailable'));
    await tick();
    assert.equal(get('.raghad-input').value, prompt);
    assert.equal(get('.raghad-input').readOnly, false);
    assert.equal(get('.raghad-status').hidden, true);
    assert.equal(get('.raghad-retry').hidden, false);
    dom.window.close();
});

test('language navigation during a pending request preserves the submitted question for retry', () => {
    const { dom, window, get, send } = setup('ar', () => new Promise(() => {}));
    send('Pending question');
    assert.equal(get('.raghad-input').value, '');
    const link = window.document.createElement('a');
    link.href = '/website/en.html';
    window.document.body.append(link);
    link.click();
    const handoff = window.sessionStorage.getItem('estavo-raghad-language-handoff-v1');
    const restored = setup('en', undefined, { url: link.href, handoff });
    assert.equal(restored.get('.raghad-input').value, 'Pending question');
    assert.equal(restored.get('.raghad-message--user p').textContent, 'Pending question');
    assert.equal(restored.get('.raghad-status').hidden, true);
    restored.dom.window.close();
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

test('only approved answer URLs become links, punctuation and hostile markup remain safe', async () => {
    const {dom, get, send} = setup('en', async () => ({ok:true,json:async()=>({
        message:'Buy https://brokers.estavo.space/credits. Help https://wa.me/201069528393 — https://brokers.estavo.space.evil.test/credits <img src=x onerror=alert(1)> javascript:alert(1)', conversation_token:'signed'
    })}));
    send('Links'); await tick();
    const links=[...get('.raghad-message--assistant').querySelectorAll('a')];
    assert.deepEqual(links.map(a=>a.href), ['https://brokers.estavo.space/credits','https://wa.me/201069528393']);
    assert.ok(links.every(a=>a.rel.includes('noopener') && a.target==='_blank'));
    assert.equal(get('.raghad-message--assistant img'),null);
    dom.window.close();
});

test('reset cancellation preserves the conversation and draft; confirmation clears them', async () => {
    const {dom, get, send} = setup('en', async()=>({ok:true,json:async()=>({message:'Answer',conversation_token:'signed'})}));
    send('Question'); await tick();
    get('.raghad-input').value='Unsent draft';
    get('.raghad-reset').click();
    assert.equal(get('.raghad-reset-prompt').hidden,false);
    get('.raghad-cancel-reset').click();
    assert.equal(get('.raghad-input').value,'Unsent draft');
    assert.equal(get('.raghad-messages').children.length,2);
    get('.raghad-reset').click(); get('.raghad-confirm-reset').click();
    assert.equal(get('.raghad-input').value,'');
    assert.equal(get('.raghad-messages').children.length,0);
    dom.window.close();
});

test('retry respects server cooldown and cannot be bypassed by Enter, starters or New chat', async () => {
    let calls=0;
    const {dom,get,send}=setup('en',async()=>{calls++;return {ok:false,status:429,headers:{get:()=> '3600'},json:async()=>({})};});
    send('Question'); await tick();
    assert.match(get('.raghad-error').textContent,/try again at/);
    assert.equal(get('.raghad-send').disabled,true);
    assert.equal(get('.raghad-retry').disabled,true);
    send('Attempt');
    get('.raghad-reset').click(); get('.raghad-confirm-reset').click();
    send('Attempt after reset');
    assert.equal(calls,1);
    dom.window.close();
});

test('cooldown expiry re-enables retry and preserves the failed draft', async () => {
    let now=Date.now();
    const {dom,window,get,send}=setup('en',async()=>({ok:false,status:429,headers:{get:()=> '1'},json:async()=>({})}));
    window.Date.now=()=>now;
    send('Question'); await tick(); now+=2000;
    await new Promise(resolve=>setTimeout(resolve,1100));
    assert.equal(get('.raghad-retry').disabled,false);
    assert.equal(get('.raghad-input').value,'Question');
    assert.match(get('.raghad-error').textContent,/now/);
    dom.window.close();
});

test('HTTP-date cooldowns are honored; missing timing uses a bounded cooldown', async () => {
    for(const header of [new Date(Date.now()+3600000).toUTCString(),null]) {
        const {dom,get,send}=setup('ar',async()=>({ok:false,status:429,headers:{get:()=>header},json:async()=>({})}));
        send('سؤال'); await tick();
        assert.equal(get('.raghad-send').disabled,true);
        assert.match(get('.raghad-error').textContent,/الساعة/);
        dom.window.close();
    }
});

test('in-widget language switch preserves conversation, draft and authenticated follow-up', async () => {
    const calls=[];
    const {dom,get,send}=setup('en',async(url,options)=>{calls.push(JSON.parse(options.body));return {ok:true,json:async()=>({message:'Answer',conversation_token:'signed'})};});
    send('Question'); await tick(); get('.raghad-input').value='سؤال تاني';
    get('.raghad-language').click();
    assert.equal(get('#raghad-support').dir,'rtl');
    assert.equal(get('.raghad-input').value,'سؤال تاني');
    assert.equal(get('.raghad-messages').children.length,2);
    send('سؤال تاني'); await tick();
    assert.equal(calls[1].locale,'ar'); assert.equal(calls[1].conversation_token,'signed');
    dom.window.close();
});

test('page language handoff restores same-tab chat and draft once, without ongoing storage', async () => {
    const {dom,window,get,send}=setup('ar',async()=>({ok:true,json:async()=>({message:'إجابة',conversation_token:'signed'})}));
    send('سؤال'); await tick(); get('.raghad-input').value='Unsent follow-up'; get('.raghad-launcher').click();
    const link=window.document.createElement('a');link.href='/website/en.html';window.document.body.append(link);
    window.document.addEventListener('click',event=>event.preventDefault()); link.click();
    const saved=window.sessionStorage.getItem('estavo-raghad-language-handoff-v1');assert.ok(saved);
    const restored=setup('en',undefined,{url:'https://estavo-brokers.com/website/en.html',handoff:saved});
    assert.equal(restored.get('.raghad-input').value,'Unsent follow-up');
    assert.equal(restored.get('.raghad-messages').children.length,2);
    assert.equal(restored.get('.raghad-panel').hidden,false);
    assert.equal(restored.window.sessionStorage.length,0);
    assert.equal(restored.window.localStorage.length,0);
    dom.window.close();restored.dom.window.close();
});

test('stale and wrong-route language handoffs are discarded',()=>{
    for(const state of [{at:Date.now()-120000,target:'/website/'},{at:Date.now(),target:'/en.html'}]) {
        const {dom,get,window}=setup('en',undefined,{handoff:JSON.stringify({...state,token:'old',draft:'old',transcript:[]})});
        assert.equal(get('.raghad-input').value,'');assert.equal(window.sessionStorage.length,0);dom.window.close();
    }
});

test('blocked session storage prevents language navigation from silently losing a draft',()=>{
    const {dom,window,get}=setup();get('.raghad-input').value='Keep me';
    Object.defineProperty(window,'sessionStorage',{get(){throw new Error('Storage unavailable');}});
    const link=window.document.createElement('a');link.href='/website/en.html';window.document.body.append(link);
    // Current document is English: switch to the Arabic route.
    link.href='/';
    const event=new window.MouseEvent('click',{bubbles:true,cancelable:true});link.dispatchEvent(event);
    assert.equal(event.defaultPrevented,true);assert.equal(get('.raghad-input').value,'Keep me');
    assert.match(get('.raghad-error').textContent,/language button/);dom.window.close();
});

test('both landing referral scripts preserve dynamic support deep links while tracking signup CTAs', async () => {
    for(const file of ['referral.js','website-referral.js']) {
        const {dom,window,get,send}=setup('en',async()=>({ok:true,json:async()=>({message:'https://brokers.estavo.space/credits',conversation_token:'signed'})}));
        const signup=window.document.createElement('a');signup.href='https://brokers.estavo.space/';window.document.body.append(signup);
        window.eval(fs.readFileSync(path.join(__dirname,'../assets/js',file),'utf8'));
        window.document.dispatchEvent(new window.Event('DOMContentLoaded'));
        send('Credits');await tick();await tick();
        assert.equal(get('.raghad-message--assistant a').href,'https://brokers.estavo.space/credits');
        assert.match(signup.href,/\/go\/\?ref=/);
        dom.window.close();
    }
});


test('production pause hides Raghad on listed hosts while previews remain available', () => {
    for (const host of ['estavo-brokers.com', 'www.estavo-brokers.com', 'preview.estavo.test']) {
        const { dom, get } = setup('en', undefined, {
            url: `https://${host}/`, disabledHosts: 'estavo-brokers.com,www.estavo-brokers.com',
        });
        assert.equal(Boolean(get('#raghad-support')), host === 'preview.estavo.test');
        dom.window.close();
    }
});
