(function () {
    'use strict';

    const script = document.currentScript;
    if (!script || document.getElementById('raghad-support')) return;
    const locale = document.documentElement.lang.startsWith('ar') ? 'ar' : 'en';
    const ar = locale === 'ar';
    const copy = ar ? {
        name: 'رغد', launch: 'اسأل رغد', role: 'مساعدة Estavo بالذكاء الاصطناعي',
        title: 'أهلًا، أقدر أساعدك في إيه؟',
        welcome: 'اسألني عن خدمات Estavo، الكريدتس، أو مشكلة بتقابلك. أنا هنا أساعدك تلاقي الإجابة.',
        prompts: ['إيه الفرق بين Brokers وSites؟', 'الكريدتس بتتحسب إزاي؟', 'عندي موقع بالفعل'],
        label: 'رسالتك لرغد', placeholder: 'اكتب سؤالك هنا…', send: 'إرسال', close: 'إغلاق المحادثة',
        reset: 'محادثة جديدة', human: 'تواصل مع فريق الدعم', thinking: 'رغد بتراجع سؤالك…',
        note: 'ما تبعتش كلمات سر أو بيانات دفع.', sources: 'من دليل',
        unavailable: 'مش قادرة أرد دلوقتي. جرّب تبعت رسالتك تاني أو تواصل مع فريق الدعم.',
        limited: 'وصلت لحد الرسائل المتاح حاليًا. استنى شوية وجرّب تاني، أو تواصل مع الدعم.',
        expired: 'المحادثة انتهت صلاحيتها. ابعت رسالتك تاني عشان نبدأ محادثة جديدة.',
        invalid: 'اكتب رسالة من 1 إلى 2000 حرف، وجرّب تاني.',
        tooLong: 'الرسالة طويلة. اختصرها لـ2000 حرف وجرب تاني.',
        you: 'أنت', privacy: 'الخصوصية',
    } : {
        name: 'Raghad', launch: 'Ask Raghad', role: 'Estavo AI support assistant',
        title: 'Hi, how can I help?',
        welcome: 'Ask me about Estavo products, credits, or a problem you’re having. Let’s find your answer.',
        prompts: ['Brokers or Sites: what’s the difference?', 'How do credits work?', 'I already have a website'],
        label: 'Your message to Raghad', placeholder: 'Type your question…', send: 'Send', close: 'Close conversation',
        reset: 'New chat', human: 'Contact the support team', thinking: 'Raghad is checking your question…',
        note: 'Please don’t share passwords or payment details.', sources: 'From the guide',
        unavailable: 'I can’t reply right now. Try sending your message again, or contact the support team.',
        limited: 'You’ve reached the current message limit. Please wait and try again, or contact support.',
        expired: 'This conversation has expired. Send your message again to start a new conversation.',
        invalid: 'Enter a message of 1 to 2,000 characters and try again.',
        tooLong: 'That message is too long. Please keep it under 2,000 characters.',
        you: 'You', privacy: 'Privacy',
    };
    const endpoint = script.dataset.endpoint || 'https://api-brokers.estavo.space/api/public/support/chat';
    const supportUrl = script.dataset.supportUrl || 'https://wa.me/201069528393';
    let token = null; // In-memory only; never persist chats/tokens in localStorage or analytics.
    let pending = false;
    let controller = null;
    let generation = 0;
    let failedBubble = null;

    function el(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text) node.textContent = text;
        return node;
    }

    function icon(name) {
        const paths = {
            close: 'm6 6 12 12M6 18 18 6',
            send: 'M12 19V5m-6 6 6-6 6 6',
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
    const launcher = button('raghad-launcher', copy.launch);
    launcher.prepend(portrait('raghad-launcher-portrait', 40));
    launcher.setAttribute('aria-expanded', 'false');
    launcher.setAttribute('aria-controls', 'raghad-panel');
    launcher.setAttribute('aria-haspopup', 'dialog');

    const panel = el('section', 'raghad-panel');
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
    identity.append(name, el('p', '', copy.role));
    const close = button('raghad-icon-button', copy.close, 'close');
    header.append(avatar, identity, close);
    const toolbar = el('div', 'raghad-toolbar');
    const human = el('a', 'raghad-human', copy.human);
    human.href = supportUrl;
    human.target = '_blank';
    human.rel = 'noopener noreferrer';
    const reset = button('raghad-reset', copy.reset);
    toolbar.append(human, reset);

    const scroll = el('div', 'raghad-scroll');
    const intro = el('div', 'raghad-intro');
    intro.append(el('h3', '', copy.title), el('p', '', copy.welcome));
    const starters = el('div', 'raghad-starters');
    copy.prompts.forEach(prompt => {
        const starter = button('raghad-starter', prompt);
        starter.addEventListener('click', () => { input.value = prompt; form.requestSubmit(); });
        starters.append(starter);
    });
    intro.append(starters);
    const messages = el('div', 'raghad-messages');
    messages.setAttribute('role', 'log');
    messages.setAttribute('aria-live', 'polite');
    messages.setAttribute('aria-relevant', 'additions');
    messages.setAttribute('aria-label', ar ? 'المحادثة مع رغد' : 'Conversation with Raghad');
    scroll.append(intro, messages);
    const status = el('p', 'raghad-status');
    status.setAttribute('role', 'status');
    const error = el('p', 'raghad-error');
    error.setAttribute('role', 'alert');
    error.id = 'raghad-error';
    error.hidden = true;

    const form = el('form', 'raghad-composer');
    const label = el('label', 'raghad-sr-only', copy.label);
    label.htmlFor = 'raghad-input';
    const input = el('textarea', 'raghad-input');
    input.id = 'raghad-input';
    input.name = 'message';
    input.maxLength = 2000;
    input.rows = 2;
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
    panel.append(header, toolbar, scroll, status, error, form, footer);
    root.append(panel, launcher);
    document.body.append(root);

    function setOpen(open) {
        panel.hidden = !open;
        root.dataset.raghadOpen = String(open);
        launcher.setAttribute('aria-expanded', String(open));
        if (open) input.focus({ preventScroll: true });
        else launcher.focus({ preventScroll: true });
    }
    launcher.addEventListener('click', () => setOpen(panel.hidden));
    close.addEventListener('click', () => setOpen(false));
    root.addEventListener('keydown', event => {
        if (event.key === 'Escape' && !panel.hidden) { event.preventDefault(); setOpen(false); }
    });

    function syncControls() {
        send.disabled = pending || !input.value.trim();
        input.readOnly = pending;
        starters.querySelectorAll('button').forEach(node => { node.disabled = pending; });
        form.setAttribute('aria-busy', String(pending));
        status.textContent = pending ? copy.thinking : '';
    }
    input.addEventListener('input', syncControls);
    input.addEventListener('keydown', event => {
        if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
            event.preventDefault();
            if (!pending) form.requestSubmit();
        }
    });

    function appendMessage(role, text, sources) {
        const bubble = el('div', `raghad-message raghad-message--${role}`);
        bubble.append(el('span', 'raghad-sr-only', role === 'user' ? copy.you : copy.name));
        const body = el('p', '', text);
        body.dir = 'auto'; // Text only: never render model-supplied HTML or link markup.
        bubble.append(body);
        const products = { brokers: 'Estavo Brokers', sites: 'Estavo Sites', ai: 'Estavo AI', integrations: 'Meta & Integrations' };
        const labels = [...new Set((sources || []).map(source => products[source.product]).filter(Boolean))];
        if (labels.length) bubble.append(el('p', 'raghad-sources', `${copy.sources}: ${labels.join(' · ')}`));
        messages.append(bubble);
        // Bound the DOM for long-lived tabs independently from model history.
        while (messages.children.length > 40) messages.firstElementChild.remove();
        scroll.scrollTop = scroll.scrollHeight;
        return bubble;
    }

    reset.addEventListener('click', () => {
        generation++;
        controller?.abort();
        token = null;
        pending = false;
        failedBubble = null;
        messages.replaceChildren();
        intro.hidden = false;
        error.hidden = true;
        input.value = '';
        syncControls();
        input.focus();
    });

    form.addEventListener('submit', async event => {
        event.preventDefault();
        const message = input.value.trim();
        if (pending || !message) return;
        if ([...message].length > 2000) {
            error.textContent = copy.tooLong;
            error.hidden = false;
            return;
        }
        failedBubble?.remove();
        failedBubble = null;
        error.hidden = true;
        intro.hidden = true;
        const bubble = appendMessage('user', message);
        pending = true;
        syncControls();
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
            input.value = '';
        } catch (failure) {
            if (requestGeneration !== generation) return;
            failedBubble = bubble;
            bubble.classList.add('raghad-message--failed');
            error.textContent = Object.values(copy).includes(failure.message) ? failure.message : copy.unavailable;
            error.hidden = false;
            // Keep the draft and old token so retry never adds a fabricated successful turn.
        } finally {
            clearTimeout(timer);
            if (requestGeneration === generation) {
                pending = false;
                syncControls();
            }
        }
    });

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
