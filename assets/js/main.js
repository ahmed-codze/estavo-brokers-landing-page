/* ============================================================
   main.js — Estavo Brokers Landing Page
   Pure JS, no framework
   ============================================================ */

(function () {
    'use strict';

    /* ─── Utility ─────────────────────────────────────────── */
    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
    const on = (el, ev, fn, opt) => el && el.addEventListener(ev, fn, opt);

    /* ─── PostHog stub (safe if not loaded) ──────────────── */
    const track = (event, props = {}) => {
        if (window.posthog && typeof posthog.capture === 'function') {
            posthog.capture(event, props);
        }
    };

    /* ─── Language detection ──────────────────────────────── */
    function detectLang() {
        const lang = navigator.language || navigator.userLanguage || 'en';
        return lang.toLowerCase().startsWith('ar') ? 'ar' : 'en';
    }

    /* ─── Navbar ──────────────────────────────────────────── */
    function initNavbar() {
        const nav = $('.nav');
        if (!nav) return;

        const onScroll = () => {
            nav.classList.toggle('scrolled', window.scrollY > 40);
        };

        on(window, 'scroll', onScroll, { passive: true });
        onScroll();

        // Hamburger
        const hamburger = $('.nav-hamburger');
        const mobileMenu = $('.nav-mobile');

        if (hamburger && mobileMenu) {
            on(hamburger, 'click', () => {
                const isOpen = hamburger.classList.toggle('open');
                mobileMenu.classList.toggle('open', isOpen);
                document.body.style.overflow = isOpen ? 'hidden' : '';
            });

            // Close on link click
            $$('a', mobileMenu).forEach(link => {
                on(link, 'click', () => {
                    hamburger.classList.remove('open');
                    mobileMenu.classList.remove('open');
                    document.body.style.overflow = '';
                });
            });
        }

        // Smooth scroll for nav links
        $$('.nav-links a, .nav-mobile a').forEach(link => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('#')) {
                on(link, 'click', (e) => {
                    e.preventDefault();
                    const target = $(href);
                    if (target) {
                        const top = target.getBoundingClientRect().top + window.scrollY - 72;
                        window.scrollTo({ top, behavior: 'smooth' });
                    }
                });
            }
        });
    }

    /* ─── Scroll Reveal ───────────────────────────────────── */
    function initScrollReveal() {
        const els = $$('.reveal');
        if (!els.length) return;

        const io = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        els.forEach(el => io.observe(el));
    }

    /* ─── AI Chat Demo ────────────────────────────────────── */
    function initAIDemo() {
        const demo = $('.ai-demo-body');
        if (!demo) return;

        const lang = document.documentElement.lang === 'ar' ? 'ar' : 'en';

        const conversations = {
            en: [
                {
                    user: 'I have a client looking for a 2-bed in New Cairo, mid-range budget.',
                    thinking: true,
                    ai: {
                        label: 'Estavo AI',
                        lines: [
                            '<strong>Found a few good options for you.</strong>',
                            '⭐ <strong>Best fit: compound in New Cairo</strong>',
                            '&nbsp;&nbsp;&nbsp;Good location · flexible payment plan',
                            '<em>Closest to what your client is looking for.</em>',
                            '<em>Have another option if the focus is investment.</em>'
                        ],
                        actions: ['Show all options', 'Create PDF offer']
                    }
                },
                {
                    user: 'Client wants a villa with a private garden in 6th of October.',
                    thinking: true,
                    ai: {
                        label: 'Estavo AI',
                        lines: [
                            '<strong>Found villas with private gardens in 6th of October.</strong>',
                            '• One compound — spacious, garden included',
                            '• Another option — garden + pool, higher budget',
                            '<em>Want me to compare both payment plans?</em>'
                        ],
                        actions: ['Compare plans', 'Show availability']
                    }
                },
                {
                    user: 'Which New Capital projects have the most flexible payment plans?',
                    thinking: true,
                    ai: {
                        label: 'Estavo AI',
                        lines: [
                            '<strong>Most flexible plans in New Capital right now:</strong>',
                            '• Compound A — low down payment, long installment',
                            '• Compound B — similar plan, closer to delivery',
                            '<em>Both work well for clients who want manageable monthly payments.</em>'
                        ],
                        actions: ['Show all plans', 'Create PDF comparison']
                    }
                },
                {
                    user: 'Are there ready-to-move units in El Tagamoa?',
                    thinking: true,
                    ai: {
                        label: 'Estavo AI',
                        lines: [
                            '<strong>Ready units available in El Tagamoa.</strong>',
                            '• Compound in the area — immediate delivery, finished',
                            '• Another option — limited availability, larger units',
                            '<em>Want to filter by size or budget?</em>'
                        ],
                        actions: ['Filter options', 'Show payment plans']
                    }
                },
                {
                    user: 'Looking for mid-size units in Sheikh Zayed with installments.',
                    thinking: true,
                    ai: {
                        label: 'Estavo AI',
                        lines: [
                            '<strong>Mid-size units with installments in Sheikh Zayed:</strong>',
                            '• Compound A — comfortable plan, good location',
                            '• Compound B — similar size, lower down payment',
                            '<em>Which one fits your client better — location or payment flexibility?</em>'
                        ],
                        actions: ['Compare both', 'Show availability in 6th of October']
                    }
                }
            ],
            ar: [
                {
                    user: 'عندي عميل عايز شقة في التجمع بميزانية متوسطة.',
                    thinking: true,
                    ai: {
                        label: 'مستشار إستاڤو',
                        lines: [
                            '<strong>لقيتلك شوية اختيارات مناسبة.</strong>',
                            '⭐ <strong>الأفضل: مشروع في التجمع — موقع مميز وخطة مريحة</strong>',
                            '<em>ده الأقرب للي العميل بيدور عليه.</em>',
                            '<em>عندي اختيار تاني أقوى لو الهدف استثمار.</em>'
                        ],
                        actions: ['اعرض باقي الاختيارات', 'اعمل عرض PDF']
                    }
                },
                {
                    user: 'عايز أعرف أكتر المشاريع مرونة في الدفع في العاصمة الإدارية.',
                    thinking: true,
                    ai: {
                        label: 'مستشار إستاڤو',
                        lines: [
                            '<strong>أكتر المشاريع مرونة في الدفع دلوقتي:</strong>',
                            '• كمبوند أ — مقدم مريح وتقسيط طويل',
                            '• كمبوند ب — خطة مشابهة وأقرب للتسليم',
                            '<em>الاتنين مناسبين للعميل اللي بيدور على قسط شهري معقول.</em>'
                        ],
                        actions: ['اعرض كل الخطط', 'اعمل مقارنة PDF']
                    }
                },
                {
                    user: 'في وحدات استلام فوري في التجمع؟',
                    thinking: true,
                    ai: {
                        label: 'مستشار إستاڤو',
                        lines: [
                            '<strong>في وحدات استلام فوري في التجمع.</strong>',
                            '• كمبوند في المنطقة — تسليم فوري وتشطيب كامل',
                            '• اختيار تاني — متاح بس وحدات أكبر',
                            '<em>تحب نفلتر حسب المساحة أو الميزانية؟</em>'
                        ],
                        actions: ['فلتر الاختيارات', 'اعرض خطط السداد']
                    }
                },
                {
                    user: 'عميل عايز فيلا بحديقة خاصة في أكتوبر.',
                    thinking: true,
                    ai: {
                        label: 'مستشار إستاڤو',
                        lines: [
                            '<strong>لقيتلك فيلات بحدائق خاصة في أكتوبر.</strong>',
                            '• كمبوند أ — مساحة واسعة وحديقة',
                            '• كمبوند ب — حديقة + حمام سباحة، ميزانية أعلى',
                            '<em>تحب أقارنلك خطط الدفع للاتنين؟</em>'
                        ],
                        actions: ['قارن الخطط', 'اعرض المتاح']
                    }
                },
                {
                    user: 'وحدات متوسطة المساحة في الشيخ زايد بتقسيط.',
                    thinking: true,
                    ai: {
                        label: 'مستشار إستاڤو',
                        lines: [
                            '<strong>وحدات متوسطة بتقسيط في الشيخ زايد:</strong>',
                            '• كمبوند أ — خطة مريحة وموقع كويس',
                            '• كمبوند ب — نفس المساحة ومقدم أقل',
                            '<em>الأولوية للعميل — الموقع ولا مرونة الدفع؟</em>'
                        ],
                        actions: ['قارن الاتنين', 'اعرض المتاح في أكتوبر']
                    }
                }
            ]
        };

        const msgs = conversations[lang] || conversations.en;
        let running = false;

        function createUserBubble(text) {
            const el = document.createElement('div');
            el.className = 'demo-bubble user-msg';
            el.textContent = text;
            return el;
        }

        function createThinking() {
            const el = document.createElement('div');
            el.className = 'demo-thinking';
            el.innerHTML = '<span></span><span></span><span></span>';
            return el;
        }

        function createAIBubble(data) {
            const el = document.createElement('div');
            el.className = 'demo-bubble ai-msg';
            let html = `<span class="ai-msg-label">${data.label}</span>`;
            data.lines.forEach(line => {
                html += `<div class="result-item">${line}</div>`;
            });
            el.innerHTML = html;
            return el;
        }

        function createActions(data) {
            const el = document.createElement('div');
            el.className = 'demo-actions';
            data.actions.forEach(action => {
                const btn = document.createElement('span');
                btn.className = 'demo-action-chip';
                btn.textContent = action;
                el.appendChild(btn);
            });
            return el;
        }

        function delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        let convIndex = Math.floor(Math.random() * msgs.length);

        async function runConversation() {
            if (running) return;
            running = true;

            // Clear the chat panel and pick one conversation
            demo.innerHTML = '';
            const msg = msgs[convIndex];
            convIndex = (convIndex + 1) % msgs.length;

            // User bubble
            const userBubble = createUserBubble(msg.user);
            demo.appendChild(userBubble);
            await delay(80);
            userBubble.classList.add('show');
            demo.scrollTop = demo.scrollHeight;

            await delay(700);

            // Thinking
            const thinking = createThinking();
            demo.appendChild(thinking);
            await delay(80);
            thinking.classList.add('show');
            demo.scrollTop = demo.scrollHeight;

            await delay(1600);

            // Remove thinking, show AI bubble
            thinking.remove();

            const aiBubble = createAIBubble(msg.ai);
            demo.appendChild(aiBubble);
            await delay(80);
            aiBubble.classList.add('show');
            demo.scrollTop = demo.scrollHeight;

            await delay(500);

            // Action chips
            const actions = createActions(msg.ai);
            demo.appendChild(actions);
            await delay(80);
            actions.classList.add('show');
            demo.scrollTop = demo.scrollHeight;

            // Hold, then start next conversation
            await delay(3500);
            running = false;
            runConversation();
        }

        // Start when demo is visible
        const io = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                runConversation();
                io.disconnect();
            }
        }, { threshold: 0.3 });

        const demoSection = demo.closest('.section-ai');
        if (demoSection) io.observe(demoSection);
    }

    /* ─── Hero Chat Animation ─────────────────────────────── */
    function initHeroChat() {
        const bubbles = $$('.chat-bubble');
        const thinking = $('.chat-thinking');
        if (!bubbles.length) return;

        let step = 0;
        const sequence = [
            { show: 0, delay: 500 },
            { show: 'thinking', delay: 300 },
            { show: 1, delay: 1200, hidethinking: true },
            { show: 2, delay: 400 },
            { show: 3, delay: 1000 }
        ];

        function reset() {
            bubbles.forEach(b => b.classList.remove('show'));
            if (thinking) thinking.classList.remove('show');
        }

        async function run() {
            reset();
            await new Promise(r => setTimeout(r, 600));

            for (const s of sequence) {
                await new Promise(r => setTimeout(r, s.delay));
                if (s.show === 'thinking') {
                    if (thinking) thinking.classList.add('show');
                } else {
                    if (s.hidethinking && thinking) thinking.classList.remove('show');
                    if (bubbles[s.show]) bubbles[s.show].classList.add('show');
                }
            }

            setTimeout(run, 4000);
        }

        run();
    }

    /* ─── FAQ Accordion ───────────────────────────────────── */
    function initFAQ() {
        $$('.faq-item').forEach((item, idx) => {
            // Listen to the native toggle event of <details>
            on(item, 'toggle', () => {
                const isOpen = item.open;

                if (isOpen) {
                    // Close all other FAQ items when one opens
                    $$('.faq-item').forEach(otherItem => {
                        if (otherItem !== item && otherItem.open) {
                            otherItem.open = false;
                        }
                    });

                    // Track the event
                    track('landing_faq_expanded', {
                        question_index: idx + 1,
                        lang: document.documentElement.lang
                    });
                }
            });
        });
    }

    /* ─── Stat Counters ───────────────────────────────────── */
    function initCounters() {
        const stats = $$('.count');
        if (!stats.length) return;

        const io = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                const target = parseInt(el.dataset.target, 10);
                const dur = 2500; // 2.5 seconds for smooth animation
                const start = performance.now();

                function update(now) {
                    const progress = Math.min((now - start) / dur, 1);
                    // Easing function for smooth acceleration and deceleration
                    const ease = progress < 0.5
                        ? 4 * progress * progress * progress
                        : 1 - Math.pow(-2 * progress + 2, 3) / 2;

                    const currentValue = Math.floor(ease * target);

                    // Format with commas (always use English numerals)
                    const displayValue = currentValue.toLocaleString('en-US');

                    el.textContent = displayValue;

                    if (progress < 1) {
                        requestAnimationFrame(update);
                    } else {
                        // Final value
                        const finalValue = target.toLocaleString('en-US');
                        el.textContent = finalValue;
                    }
                }

                requestAnimationFrame(update);
                io.unobserve(el);
            });
        }, { threshold: 0.3 });

        stats.forEach(el => {
            io.observe(el);
        });
    }

    /* ─── Before/After Tabs (mobile) ─────────────────────── */
    function initBeforeAfter() {
        $$('.ba-tabs').forEach(tabs => {
            const btns = $$('.ba-tab', tabs);
            const section = tabs.closest('.section-ba');

            btns.forEach(btn => {
                on(btn, 'click', () => {
                    btns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    const val = btn.dataset.tab;
                    if (section) section.dataset.ba = val;
                });
            });
        });
    }

    /* ─── Carousel (Use Cases) ────────────────────────────── */
    function initCarousel() {
        $$('.usecases-carousel').forEach(carousel => {
            const dots = $$('.carousel-dot');
            let isDown = false;
            let startX = 0;
            let scrollLeft = 0;

            on(carousel, 'mousedown', e => {
                isDown = true;
                carousel.classList.add('dragging');
                startX = e.pageX - carousel.offsetLeft;
                scrollLeft = carousel.scrollLeft;
            });

            on(carousel, 'mouseleave', () => { isDown = false; carousel.classList.remove('dragging'); });
            on(carousel, 'mouseup', () => { isDown = false; carousel.classList.remove('dragging'); });
            on(carousel, 'mousemove', e => {
                if (!isDown) return;
                e.preventDefault();
                const x = e.pageX - carousel.offsetLeft;
                carousel.scrollLeft = scrollLeft - (x - startX) * 1.5;
            });

            // Touch scroll — native handles it
            // Update dots
            const updateDots = () => {
                const cards = $$('.usecase-card', carousel);
                if (!dots.length || !cards.length) return;
                const cardW = cards[0].offsetWidth + 24;
                const idx = Math.round(carousel.scrollLeft / cardW);
                dots.forEach((d, i) => d.classList.toggle('active', i === idx));
            };

            on(carousel, 'scroll', updateDots, { passive: true });

            dots.forEach((dot, i) => {
                on(dot, 'click', () => {
                    const cards = $$('.usecase-card', carousel);
                    if (!cards[i]) return;
                    carousel.scrollTo({ left: cards[i].offsetLeft - 24, behavior: 'smooth' });
                });
            });

            if (dots.length) dots[0].classList.add('active');
        });
    }

    /* ─── Sticky CTA Bar ──────────────────────────────────── */
    function initStickyCTA() {
        const bar = $('.sticky-cta');
        if (!bar) return;

        // Check if dismissed in this session
        if (sessionStorage.getItem('estavo-sticky-dismissed') === '1') {
            bar.classList.add('dismissed');
            return;
        }

        const hero = $('.hero');
        const io = new IntersectionObserver((entries) => {
            bar.classList.toggle('visible', !entries[0].isIntersecting);
        }, { threshold: 0.1 });

        if (hero) io.observe(hero);

        const dismiss = $('.sticky-cta-dismiss', bar);
        if (dismiss) {
            on(dismiss, 'click', () => {
                bar.classList.remove('visible');
                bar.classList.add('dismissed');
                sessionStorage.setItem('estavo-sticky-dismissed', '1');
            });
        }
    }

    /* ─── CTA Click Tracking ──────────────────────────────── */
    function initTracking() {
        const lang = document.documentElement.lang || 'en';

        // Section visibility tracking
        const sections = {
            '#hero': 'hero',
            '#problem': 'problem',
            '#ai-expert': 'ai_expert',
            '#pillars': 'pillars',
            '#before-after': 'before_after',
            '#how-it-works': 'how_it_works',
            '#use-cases': 'use_cases',
            '#pdf-feature': 'pdf_feature',
            '#availability': 'availability',
            '#positioning': 'positioning',
            '#social-proof': 'social_proof',
            '#cta': 'cta',
            '#faq': 'faq'
        };

        const sectionIO = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const id = '#' + entry.target.id;
                const name = sections[id];
                if (name) {
                    track('landing_section_viewed', { section: name, lang });
                    sectionIO.unobserve(entry.target);
                }
            });
        }, { threshold: 0.4 });

        Object.keys(sections).forEach(sel => {
            const el = $(sel);
            if (el) sectionIO.observe(el);
        });

        // CTA clicks
        $$('[data-track]').forEach(el => {
            on(el, 'click', () => {
                const data = el.dataset;
                track('landing_cta_clicked', {
                    cta: data.track,
                    position: data.position || 'unknown',
                    lang
                });
            });
        });

        // Scroll depth
        const depths = { 25: false, 50: false, 75: false, 100: false };
        on(window, 'scroll', () => {
            const pct = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            Object.keys(depths).forEach(d => {
                if (!depths[d] && pct >= +d) {
                    depths[d] = true;
                    track('landing_scroll_depth', { depth: d + '%', lang });
                }
            });
        }, { passive: true });
    }

    /* ─── Language Toggle ─────────────────────────────────── */
    function initLangToggle() {
        $$('.nav-lang, .footer-lang-toggle').forEach(toggle => {
            on(toggle, 'click', (e) => {
                const currentLang = document.documentElement.lang;
                const newLang = currentLang === 'ar' ? 'en' : 'ar';
                track('landing_language_switched', { from: currentLang, to: newLang });

                // If element is an anchor with href, let the browser navigate (SEO friendly).
                if (toggle.tagName === 'A' && toggle.getAttribute('href')) return;

                // Fallback for non-anchor toggles.
                const target = newLang === 'ar' ? '/' : '/en.html';
                window.location.href = target;
            });
        });
    }

    /* ─── Init All ────────────────────────────────────────── */
    function init() {
        initNavbar();
        initScrollReveal();
        initHeroChat();
        initAIDemo();
        initFAQ();
        initCounters();
        initBeforeAfter();
        initCarousel();
        initStickyCTA();
        initTracking();
        initLangToggle();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
