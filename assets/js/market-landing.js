/* Estavo Market commercial page motion and prepared product demonstrations. */
(function () {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const heroBubbles = [...document.querySelectorAll('.hero .chat-bubble')];
  const heroThinking = document.querySelector('.hero .chat-thinking');
  if (heroBubbles.length) {
    const showHero = () => {
      heroBubbles.forEach((bubble) => bubble.classList.remove('show'));
      if (heroThinking) heroThinking.classList.remove('show');
      const sequence = [
        [heroBubbles[0], 250],
        [heroThinking, 850],
        [heroBubbles[1], 1550],
        [heroBubbles[2], 2300],
        [heroBubbles[3], 3050],
      ];
      sequence.forEach(([item, delay], index) => {
        window.setTimeout(() => {
          if (index === 2 && heroThinking) heroThinking.classList.remove('show');
          if (item) item.classList.add('show');
        }, reduced ? 0 : delay);
      });
    };
    showHero();
    if (!reduced) window.setInterval(showHero, 7800);
  }

  const demo = document.querySelector('.ai-demo-body');
  if (demo) {
    const isArabic = document.documentElement.lang === 'ar';
    const conversations = isArabic ? [
      {
        user: 'عميل عايز شقة ٣ غرف في القاهرة الجديدة وعايز يقارن مدة السداد.',
        answer: 'لقيت اختيارين مطابقين في المثال:',
        rows: [['اختيار أ', '١٤٥ م² · ٦ سنين'], ['اختيار ب', '١٥٢ م² · ٧ سنين']],
        summary: 'اختيار ب يضيف سنة تقسيط ومساحة ٧ م².',
        actions: ['شوف المقارنة', 'جهّز العرض'],
      },
      {
        user: 'قارن اختيار أ واختيار ب في المساحة ومدة السداد.',
        answer: 'دي المقارنة من بيانات المثال:',
        rows: [['اختيار أ', '١٤٥ م² · ٦ سنين'], ['اختيار ب', '١٥٢ م² · ٧ سنين']],
        summary: 'اختيار أ أقل مساحة؛ اختيار ب يدي سنة تقسيط إضافية.',
        actions: ['جهّز العرض', 'اسأل سؤال مكمل'],
      },
    ] : [
      {
        user: 'My client wants three bedrooms in New Cairo and needs to compare payment duration.',
        answer: 'I found two matches in this example:',
        rows: [['Option A', '145 m² · 6 years'], ['Option B', '152 m² · 7 years']],
        summary: 'Option B adds one payment year and 7 m².',
        actions: ['View comparison', 'Prepare a PDF'],
      },
      {
        user: 'Compare Option A and Option B for area and payment duration.',
        answer: 'Here is the comparison from the example data:',
        rows: [['Option A', '145 m² · 6 years'], ['Option B', '152 m² · 7 years']],
        summary: 'Option A is smaller; Option B adds one payment year.',
        actions: ['Prepare a PDF', 'Ask a follow-up'],
      },
    ];
    let conversationIndex = 0;

    const renderConversation = () => {
      const item = conversations[conversationIndex];
      conversationIndex = (conversationIndex + 1) % conversations.length;
      demo.replaceChildren();

      const user = document.createElement('div');
      user.className = 'demo-bubble user-msg';
      user.textContent = item.user;

      const thinking = document.createElement('div');
      thinking.className = 'demo-thinking';
      thinking.innerHTML = '<span></span><span></span><span></span>';

      const answer = document.createElement('div');
      answer.className = 'demo-bubble ai-msg';
      const label = document.createElement('span');
      label.className = 'ai-msg-label';
      if (isArabic) {
        const isolatedName = document.createElement('bdi');
        isolatedName.textContent = 'Brokers AI';
        label.appendChild(isolatedName);
      } else {
        label.textContent = 'Brokers AI';
      }
      answer.append(label, document.createTextNode(item.answer));

      const comparison = document.createElement('div');
      comparison.className = 'demo-comparison';
      item.rows.forEach(([name, value]) => {
        const row = document.createElement('span');
        const title = document.createElement('b');
        const detail = document.createElement('em');
        title.textContent = name;
        detail.textContent = value;
        row.append(title, detail);
        comparison.appendChild(row);
      });
      const summary = document.createElement('strong');
      summary.className = 'demo-summary';
      summary.textContent = item.summary;
      answer.append(comparison, summary);

      const actions = document.createElement('div');
      actions.className = 'demo-actions';
      item.actions.forEach((text) => {
        const chip = document.createElement('span');
        chip.className = 'demo-action-chip';
        chip.textContent = text;
        actions.appendChild(chip);
      });

      demo.append(user, thinking, answer, actions);
      const stages = [[user, 100], [thinking, 750], [answer, 1500], [actions, 2050]];
      stages.forEach(([node, delay], index) => {
        window.setTimeout(() => {
          if (index === 2) thinking.remove();
          node.classList.add('show');
        }, reduced ? 0 : delay);
      });
    };

    renderConversation();
    if (!reduced) window.setInterval(renderConversation, 7200);
  }

  document.querySelectorAll('.ba-tabs').forEach((tabs) => {
    const section = tabs.closest('.section-ba');
    tabs.querySelectorAll('.ba-tab').forEach((button) => {
      button.addEventListener('click', () => {
        tabs.querySelectorAll('.ba-tab').forEach((item) => {
          const selected = item === button;
          item.classList.toggle('active', selected);
          item.setAttribute('aria-selected', String(selected));
        });
        if (section) section.dataset.ba = button.dataset.tab;
      });
    });
  });
}());
