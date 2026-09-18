(function () {
    'use strict';

    const script = document.currentScript;
    if (!script || document.getElementById('raghad-support')) return;
    let locale = document.documentElement.lang.startsWith('ar') ? 'ar' : 'en';
    let ar = locale === 'ar';
    function translations(ar) { return ar ? {
        name: 'رغد', launch: 'اسأل رغد', role: 'مساعدة Estavo بالذكاء الاصطناعي',
        title: 'أهلًا، أقدر أساعدك في إيه؟',
        welcome: 'اسألني عن خدمات Estavo، الكريدتس، أو مشكلة بتقابلك. أنا هنا أساعدك تلاقي الإجابة.',
        prompts: ['إيه الفرق بين Brokers وSites؟', 'الكريدتس بتتحسب إزاي؟', 'عندي موقع بالفعل'],
        label: 'رسالتك لرغد', placeholder: 'اكتب سؤالك هنا…', send: 'إرسال', close: 'إغلاق المحادثة',
        reset: 'محادثة جديدة', human: 'تواصل مع فريق الدعم', thinking: 'رغد بتراجع سؤالك…',
        note: 'ما تبعتش كلمات سر أو بيانات دفع.',
        unavailable: 'مش قادرة أرد دلوقتي. جرّب تبعت رسالتك تاني أو تواصل مع فريق الدعم.',
        limited: 'وصلت لحد الرسائل المتاح حاليًا. استنى شوية وجرّب تاني، أو تواصل مع الدعم.',
        expired: 'المحادثة انتهت صلاحيتها. ابعت رسالتك تاني عشان نبدأ محادثة جديدة.',
        invalid: 'اكتب رسالة من 1 إلى 2000 حرف، وجرّب تاني.',
        tooLong: 'الرسالة طويلة. اختصرها لـ2000 حرف وجرب تاني.',
        you: 'أنت', privacy: 'الخصوصية', language: 'English', retry: 'حاول تاني',
        resetTitle: 'نبدأ محادثة جديدة؟', resetNote: 'ده هيمسح المحادثة الحالية والرسالة اللي بتكتبها.', confirm: 'امسح وابدأ', cancel: 'كمّل المحادثة',
        ready: 'تقدر تبعت رسالتك دلوقتي.', retryAt: 'تقدر تحاول تاني الساعة', retryIn: 'تقدر تحاول تاني بعد', seconds: 'ثانية',
        handoff: 'مش قادرة أحفظ المحادثة أثناء تغيير الصفحة. تقدر تغيّر لغة الشات من زر اللغة فوق من غير ما تفقد رسالتك.',
    } : {
        name: 'Raghad', launch: 'Ask Raghad', role: 'Estavo AI support assistant',
        title: 'Hi, how can I help?',
        welcome: 'Ask me about Estavo products, credits, or a problem you’re having. Let’s find your answer.',
        prompts: ['Brokers or Sites: what’s the difference?', 'How do credits work?', 'I already have a website'],
        label: 'Your message to Raghad', placeholder: 'Type your question…', send: 'Send', close: 'Close conversation',
        reset: 'New chat', human: 'Contact the support team', thinking: 'Raghad is checking your question…',
        note: 'Please don’t share passwords or payment details.',
        unavailable: 'I can’t reply right now. Try sending your message again, or contact the support team.',
        limited: 'You’ve reached the current message limit. Please wait and try again, or contact support.',
        expired: 'This conversation has expired. Send your message again to start a new conversation.',
        invalid: 'Enter a message of 1 to 2,000 characters and try again.',
        tooLong: 'That message is too long. Please keep it under 2,000 characters.',
        you: 'You', privacy: 'Privacy', language: 'العربية', retry: 'Try again',
        resetTitle: 'Start a new chat?', resetNote: 'This clears your current conversation and unsent message.', confirm: 'Clear and start', cancel: 'Keep chatting',
        ready: 'You can send your message now.', retryAt: 'You can try again at', retryIn: 'You can try again in', seconds: 'seconds',
        handoff: 'Your browser could not keep this chat while changing pages. Use the language button above to switch the chat language without losing your message.',
    };
    }
    let copy = translations(ar);
    const endpoint = script.dataset.endpoint || 'https://api-brokers.estavo.space/api/public/support/chat';
    const supportUrl = script.dataset.supportUrl || 'https://wa.me/201069528393';
    let token = null; // Memory only, except a one-use, same-tab language-navigation handoff.
    let pending = false;
    let pendingMessage = null;
    let controller = null;
    let generation = 0;
    let failedBubble = null;
    let retryUntil = 0;
    let cooldownTimer = null;
    let errorKind = null;
    const HANDOFF_KEY = 'estavo-raghad-language-handoff-v1';
    const transcript = [];
    const MAX_HANDOFF_BYTES = 180000;
    const allowedLinks = new Set(['https://brokers.estavo.space/credits', supportUrl]);

    function el(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text) node.textContent = text;
        return node;
    }

    function icon(name) {
        const paths = {
            close: 'm6 6 12 12M6 18 18 6',
            send: 'M22 2 11 13m11-11-7 20-4-9-9-4 20-7',
            reset: 'M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z',
        };
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('viewBox', '0 0 24 24');
        svg.setAttribute('fill', 'none');
        svg.setAttribute('stroke', 'currentColor');
        svg.setAttribute('stroke-width', '1.8');
        svg.setAttribute('stroke-linecap', 'round');
        svg.setAttribute('stroke-linejoin', 'round');
        svg.setAttribute('aria-hidden', 'true');
        const path = document.createElementNS(svg.namespaceURI, 'path');
        path.setAttribute('d', paths[name]);
        svg.append(path);
        return svg;
    }

    function button(className, label, iconName) {
        const node = el('button', className, iconName ? null : label);
        node.type = 'button';
        if (iconName) {
            node.setAttribute('aria-label', label);
            node.title = label;
            node.append(icon(iconName));
        }
        return node;
    }

    function portrait(className, size) {
        const image = el('img', className);
        image.src = new URL('../avatars/raghad-96.webp', script.src).href;
        image.srcset = `${image.src} 96w, ${new URL('../avatars/raghad-192.webp', script.src).href} 192w`;
        image.sizes = `${size}px`;
        image.width = size;
        image.height = size;
        image.alt = ''; // The adjacent name already identifies Raghad.
        image.decoding = 'async';
        return image;
    }

    const root = el('div', 'raghad-support');
    root.id = 'raghad-support';
    root.dir = ar ? 'rtl' : 'ltr';
    root.lang = locale;
    root.dataset.raghadOpen = 'false';
    const launcher = button('raghad-launcher', '');
    launcher.prepend(portrait('raghad-launcher-portrait', 40));
    const launcherLabel = el('span', '', copy.launch);
    launcher.append(launcherLabel);
    launcher.setAttribute('aria-expanded', 'false');
    launcher.setAttribute('aria-controls', 'raghad-panel');
    launcher.setAttribute('aria-haspopup', 'dialog');

    const panel = el('section', 'raghad-panel estavo-assistant-workspace');
    panel.id = 'raghad-panel';
    panel.hidden = true;
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'false');
    panel.setAttribute('aria-labelledby', 'raghad-title');
    const header = el('header', 'raghad-header');
    const avatar = portrait('raghad-avatar', 48);
    const identity = el('div', 'raghad-identity');
    const name = el('h2', '', copy.name);
    name.id = 'raghad-title';
    const roleLabel = el('p', '', copy.role);
    identity.append(name, roleLabel);
    const close = button('raghad-icon-button', copy.close, 'close');
    const headerControls = el('div', 'raghad-header-controls');
    const language = button('raghad-language', copy.language);
    const reset = button('raghad-reset raghad-icon-button', copy.reset, 'reset');
    headerControls.append(language, reset, close);
    header.append(avatar, identity, headerControls);
    const toolbar = el('div', 'raghad-toolbar');
    const human = el('a', 'raghad-human', copy.human);
    human.href = supportUrl;
    human.target = '_blank';
    human.rel = 'noopener noreferrer';
    toolbar.append(human);

    const scroll = el('div', 'raghad-scroll estavo-assistant-notes');
    const intro = el('div', 'raghad-intro');
    const introTitle = el('h3', '', copy.title);
    const introCopy = el('p', '', copy.welcome);
    intro.append(portrait('raghad-intro-portrait', 96), introTitle, introCopy);
    const starters = el('div', 'raghad-starters');
    function renderStarters() {
        starters.replaceChildren();
        copy.prompts.forEach(prompt => {
            const starter = button('raghad-starter', prompt);
            starter.addEventListener('click', () => { input.value = prompt; form.requestSubmit(); });
            starters.append(starter);
        });
    }
    renderStarters();
    intro.append(starters);
    const messages = el('div', 'raghad-messages');
    messages.setAttribute('role', 'log');
    messages.setAttribute('aria-live', 'polite');
    messages.setAttribute('aria-relevant', 'additions');
    messages.setAttribute('aria-label', ar ? 'المحادثة مع رغد' : 'Conversation with Raghad');
    scroll.append(intro, messages);
    const status = el('p', 'raghad-status');
    status.setAttribute('role', 'status');
    status.hidden = true;
    const thinkingDots = el('span', 'raghad-thinking-dots');
    thinkingDots.setAttribute('aria-hidden', 'true');
    for (let i = 0; i < 3; i++) thinkingDots.append(el('span', ''));
    const thinkingLabel = el('span', '');
    status.append(thinkingDots, thinkingLabel);
    const error = el('p', 'raghad-error');
    error.setAttribute('role', 'alert');
    error.id = 'raghad-error';
    const recovery = el('div', 'raghad-recovery');
    const retry = button('raghad-retry', copy.retry);
    retry.hidden = true;
    retry.addEventListener('click', () => form.requestSubmit());
    recovery.append(error, retry);
    error.hidden = true;

    const form = el('form', 'raghad-composer assistant-input-surface');
    const label = el('label', 'raghad-sr-only', copy.label);
    label.htmlFor = 'raghad-input';
    const input = el('textarea', 'raghad-input');
    input.id = 'raghad-input';
    input.name = 'message';
    input.maxLength = 2000;
    input.rows = 1;
    input.dir = 'auto';
    input.placeholder = copy.placeholder;
    input.setAttribute('aria-describedby', 'raghad-note raghad-error');
    const send = button('raghad-send', copy.send, 'send');
    send.type = 'submit';
    send.disabled = true;
    form.append(label, input, send);
    const footer = el('div', 'raghad-footer');
    const note = el('span', '', copy.note);
    note.id = 'raghad-note';
    const privacy = el('a', '', copy.privacy);
    privacy.href = new URL(ar ? '../../privacy.html' : '../../privacy-en.html', script.src).href;
    privacy.target = '_blank';
    privacy.rel = 'noopener noreferrer';
    footer.append(note, privacy);
    const resetPrompt = el('div', 'raghad-reset-prompt');
    resetPrompt.hidden = true;
    resetPrompt.setAttribute('role', 'group');
    resetPrompt.setAttribute('aria-labelledby', 'raghad-reset-title');
    const resetTitle = el('h3', '', copy.resetTitle);
    resetTitle.id = 'raghad-reset-title';
    const resetNote = el('p', '', copy.resetNote);
    const resetActions = el('div', 'raghad-reset-actions');
    const cancelReset = button('raghad-cancel-reset', copy.cancel);
    const confirmReset = button('raghad-confirm-reset', copy.confirm);
    resetActions.append(cancelReset, confirmReset);
    resetPrompt.append(resetTitle, resetNote, resetActions);
    scroll.append(resetPrompt, status, recovery);
    panel.append(header, toolbar, scroll, form, footer);
    root.append(panel, launcher);
    document.body.append(root);

    function setOpen(open) {
        panel.hidden = !open;
        root.dataset.raghadOpen = String(open);
        launcher.setAttribute('aria-expanded', String(open));
        if (open) { updateViewport(); input.focus({ preventScroll: true }); }
        else launcher.focus({ preventScroll: true });
    }
    launcher.addEventListener('click', () => setOpen(panel.hidden));
    close.addEventListener('click', () => setOpen(false));
    root.addEventListener('keydown', event => {
        if (event.key === 'Escape' && !panel.hidden) {
            event.preventDefault();
            if (!resetPrompt.hidden) { resetPrompt.hidden = true; reset.focus(); }
            else setOpen(false);
        }
    });

    function syncControls() {
        const cooling = retryUntil > Date.now();
        send.disabled = pending || cooling || !input.value.trim();
        retry.disabled = pending || cooling;
        retry.hidden = error.hidden || errorKind === 'handoff';
        input.readOnly = pending;
        starters.querySelectorAll('button').forEach(node => { node.disabled = pending || cooling; });
        form.setAttribute('aria-busy', String(pending));
        status.hidden = !pending;
        thinkingLabel.textContent = pending ? copy.thinking : '';
    }
    input.addEventListener('input', () => { syncControls(); growInput(); });
    function growInput() {
        input.style.height = 'auto';
        input.style.height = `${Math.min(input.scrollHeight || 24, root.dataset.compact === 'true' ? 48 : 88)}px`;
    }
    input.addEventListener('keydown', event => {
        if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
            event.preventDefault();
            if (!pending) form.requestSubmit();
        }
    });

    function appendMessage(role, text, sources) {
        const bubble = el('div', `raghad-message raghad-message--${role} chat-bubble-${role}`);
        transcript.push({ role, text, sources: sources || [] });
        bubble.append(el('span', 'raghad-sr-only', role === 'user' ? copy.you : copy.name));
        const body = el('p', '');
        if (role === 'assistant') appendLinkedText(body, text);
        else body.textContent = text;
        body.dir = 'auto'; // Text only: never render model-supplied HTML or link markup.
        bubble.append(body);
        messages.append(bubble);
        // Bound the DOM for long-lived tabs independently from model history.
        while (messages.children.length > 40) { messages.firstElementChild.remove(); transcript.shift(); }
        // Start long answers at their beginning, not at their last line.
        scroll.scrollTop = role === 'assistant' ? Math.max(0, bubble.offsetTop - 12) : scroll.scrollHeight;
        return bubble;
    }

    reset.addEventListener('click', () => {
        if (!transcript.length && !input.value.trim()) return;
        resetPrompt.hidden = false;
        scroll.scrollTop = scroll.scrollHeight;
        cancelReset.focus();
    });
    cancelReset.addEventListener('click', () => { resetPrompt.hidden = true; input.focus(); });
    confirmReset.addEventListener('click', () => {
        generation++;
        controller?.abort();
        token = null;
        pending = false;
        pendingMessage = null;
        failedBubble = null;
        messages.replaceChildren();
        transcript.length = 0;
        resetPrompt.hidden = true;
        intro.hidden = false;
        error.hidden = true;
        errorKind = null;
        input.value = '';
        growInput();
        if (retryUntil > Date.now()) showLimit();
        syncControls();
        input.focus();
    });

    form.addEventListener('submit', async event => {
        event.preventDefault();
        const message = input.value.trim();
        if (pending || retryUntil > Date.now() || !message || !resetPrompt.hidden) return;
        if ([...message].length > 2000) {
            error.textContent = copy.tooLong;
            error.hidden = false;
            return;
        }
        if (failedBubble) { failedBubble.remove(); transcript.pop(); }
        failedBubble = null;
        error.hidden = true;
        errorKind = null;
        intro.hidden = true;
        const bubble = appendMessage('user', message);
        pending = true;
        pendingMessage = message;
        input.value = '';
        growInput();
        syncControls();
        scroll.scrollTop = scroll.scrollHeight;
        const requestGeneration = ++generation;
        controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 50000);
        try {
            const response = await fetch(endpoint, {
                method: 'POST', credentials: 'omit', cache: 'no-store',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({ message, locale, conversation_token: token }),
                signal: controller.signal,
            });
            const data = await response.json().catch(() => ({}));
            if (requestGeneration !== generation) return;
            if (!response.ok) {
                if (response.status === 429) {
                    const value = response.headers?.get('Retry-After');
                    const seconds = value && /^\d+$/.test(value) ? Number(value) : null;
                    const resetAt = seconds !== null ? Date.now() + seconds * 1000 : Date.parse(value || '');
                    retryUntil = Number.isFinite(resetAt) && resetAt > Date.now() ? resetAt : Date.now() + 60000;
                    errorKind = 'limited';
                    clearInterval(cooldownTimer);
                    cooldownTimer = setInterval(updateCooldown, 1000);
                }
                if (response.status === 422 && data.errors?.conversation_token) token = null;
                throw new Error(response.status === 429 ? copy.limited
                    : response.status === 422 && data.errors?.conversation_token ? copy.expired
                    : response.status === 422 ? copy.invalid : copy.unavailable);
            }
            if (typeof data.message !== 'string' || !data.message.trim()
                || typeof data.conversation_token !== 'string' || !data.conversation_token) {
                throw new Error(copy.unavailable);
            }
            token = data.conversation_token;
            appendMessage('assistant', data.message, Array.isArray(data.sources) ? data.sources : []);
        } catch (failure) {
            if (requestGeneration !== generation) return;
            input.value = message;
            growInput();
            failedBubble = bubble;
            bubble.classList.add('raghad-message--failed');
            error.textContent = Object.values(copy).includes(failure.message) ? failure.message : copy.unavailable;
            error.hidden = false;
            if (errorKind === 'limited') showLimit();
            scroll.scrollTop = scroll.scrollHeight;
            // Restore the submitted question and keep the old token for a safe retry.
        } finally {
            clearTimeout(timer);
            if (requestGeneration === generation) {
                pending = false;
                pendingMessage = null;
                syncControls();
            }
        }
    });

    function appendLinkedText(parent, text) {
        // Only trusted configured destinations become links; arbitrary model HTML stays text.
        const pattern = /https:\/\/[^\s<>"']+/g;
        let end = 0;
        for (const match of text.matchAll(pattern)) {
            parent.append(document.createTextNode(text.slice(end, match.index)));
            const raw = match[0];
            const url = raw.replace(/[).,;!?،؛]+$/u, '');
            if (allowedLinks.has(url)) {
                const link = el('a', '', url);
                link.href = url; link.target = '_blank'; link.rel = 'noopener noreferrer';
                parent.append(link, document.createTextNode(raw.slice(url.length)));
            } else parent.append(document.createTextNode(raw));
            end = match.index + raw.length;
        }
        parent.append(document.createTextNode(text.slice(end)));
    }

    function showLimit() {
        const timing = `${copy.retryAt} ${new Intl.DateTimeFormat(locale, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', second: '2-digit' }).format(retryUntil)}.`;
        const text = `${ar ? 'وصلت لحد الرسائل.' : 'You’ve reached the message limit.'} ${timing} ${ar ? 'تقدر تتواصل مع الدعم دلوقتي.' : 'You can contact support now.'}`;
        // Avoid announcing the changing timer every second to screen readers.
        if (error.textContent !== text) error.textContent = text;
        error.hidden = false;
    }
    function updateCooldown() {
        if (retryUntil > Date.now()) {
            if (errorKind === 'limited') showLimit();
        } else {
            clearInterval(cooldownTimer); cooldownTimer = null; retryUntil = 0;
            if (errorKind === 'limited') { error.textContent = copy.ready; errorKind = 'ready'; }
        }
        syncControls();
    }
    language.addEventListener('click', () => {
        locale = ar ? 'en' : 'ar'; ar = locale === 'ar'; copy = translations(ar);
        root.dir = ar ? 'rtl' : 'ltr'; root.lang = locale;
        launcherLabel.textContent = copy.launch;
        name.textContent = copy.name; roleLabel.textContent = copy.role;
        human.textContent = copy.human; language.textContent = copy.language;
        for (const [node, text] of [[close, copy.close], [reset, copy.reset], [send, copy.send]]) {
            node.setAttribute('aria-label', text); node.title = text;
        }
        label.textContent = copy.label; input.placeholder = copy.placeholder;
        note.textContent = copy.note; privacy.textContent = copy.privacy;
        privacy.href = new URL(ar ? '../../privacy.html' : '../../privacy-en.html', script.src).href;
        introTitle.textContent = copy.title; introCopy.textContent = copy.welcome;
        resetTitle.textContent = copy.resetTitle; resetNote.textContent = copy.resetNote;
        cancelReset.textContent = copy.cancel; confirmReset.textContent = copy.confirm;
        retry.textContent = copy.retry;
        messages.setAttribute('aria-label', ar ? 'المحادثة مع رغد' : 'Conversation with Raghad');
        renderStarters();
        if (errorKind === 'limited') showLimit();
        else if (!error.hidden) error.textContent = errorKind === 'handoff' ? copy.handoff : errorKind === 'ready' ? copy.ready : copy.unavailable;
        syncControls(); growInput();
    });

    function updateViewport() {
        const view = window.visualViewport;
        const height = view?.height || window.innerHeight;
        root.style.setProperty('--raghad-view-height', `${height}px`);
        root.style.setProperty('--raghad-view-top', `${view?.offsetTop || 0}px`);
        root.dataset.compact = String(height <= 540);
        root.dataset.keyboard = String(height < window.innerHeight - 120);
        growInput();
    }
    window.addEventListener('resize', updateViewport);
    window.visualViewport?.addEventListener('resize', updateViewport);
    window.visualViewport?.addEventListener('scroll', updateViewport);
    updateViewport();

    // Preserve only explicit same-origin language navigation. One-use handoff is
    // consumed and removed immediately on arrival; never written to analytics/localStorage.
    const languageRoutes = new Map([['/', 'ar'], ['/index.html', 'ar'], ['/en.html', 'en'], ['/website/', 'ar'], ['/website/index.html', 'ar'], ['/website/en.html', 'en']]);
    document.addEventListener('click', event => {
        const link = event.target.closest?.('a[href]');
        if (!link || event.defaultPrevented || event.button > 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.target === '_blank') return;
        const target = new URL(link.href, location.href);
        if (target.origin !== location.origin || !languageRoutes.has(target.pathname) || languageRoutes.get(target.pathname) === document.documentElement.lang.slice(0, 2)) return;
        if (!transcript.length && !input.value.trim() && retryUntil <= Date.now()) return;
        try {
            const data = JSON.stringify({ at: Date.now(), target: target.pathname, token, transcript, draft: pending ? pendingMessage : input.value, failed: Boolean(failedBubble || pending), retryUntil, open: !panel.hidden });
            if (data.length > MAX_HANDOFF_BYTES) throw new Error('Handoff too large');
            sessionStorage.setItem(HANDOFF_KEY, data);
        } catch {
            event.preventDefault(); setOpen(true); errorKind = 'handoff';
            error.textContent = copy.handoff; error.hidden = false; retry.hidden = true;
            scroll.scrollTop = scroll.scrollHeight;
        }
    });
    try {
        const saved = sessionStorage.getItem(HANDOFF_KEY);
        sessionStorage.removeItem(HANDOFF_KEY);
        if (saved && saved.length <= MAX_HANDOFF_BYTES) {
            const state = JSON.parse(saved);
            if (state.target === location.pathname && Date.now() - state.at < 60000 && state.at <= Date.now()
                && Array.isArray(state.transcript) && state.transcript.length <= 40
                && state.transcript.every(row => ['user', 'assistant'].includes(row.role) && typeof row.text === 'string' && row.text.length <= 6000)
                && typeof state.draft === 'string' && state.draft.length <= 4000
                && (state.token === null || (typeof state.token === 'string' && state.token.length <= 40000))) {
                token = state.token;
                for (const row of state.transcript) appendMessage(row.role, row.text, Array.isArray(row.sources) ? row.sources : []);
                input.value = state.draft;
                intro.hidden = transcript.length > 0;
                if (state.failed) { failedBubble = messages.lastElementChild; failedBubble?.classList.add('raghad-message--failed'); }
                if (Number.isFinite(state.retryUntil) && state.retryUntil > Date.now()) {
                    retryUntil = state.retryUntil; errorKind = 'limited'; showLimit();
                    cooldownTimer = setInterval(updateCooldown, 1000);
                }
                if (state.open) setOpen(true);
                syncControls(); growInput();
            }
        }
    } catch { /* Storage may be disabled; the widget still works in memory. */ }

    // Keep the launcher above the existing bottom CTA, including its mobile layout.
    const sticky = document.querySelector('.sticky-cta');
    function positionAboveCta() {
        const visible = sticky && sticky.classList.contains('visible') && !sticky.classList.contains('dismissed');
        root.style.setProperty('--raghad-bottom', `${visible ? sticky.getBoundingClientRect().height + 16 : 20}px`);
    }
    if (sticky) {
        new MutationObserver(positionAboveCta).observe(sticky, { attributes: true, attributeFilter: ['class'] });
        if (window.ResizeObserver) new ResizeObserver(positionAboveCta).observe(sticky);
    }
    positionAboveCta();
}());
