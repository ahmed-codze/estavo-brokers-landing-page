/* /integrations/ — request form → WhatsApp, plus a sticky-CTA courtesy.
   Without JS the form still submits as GET to wa.me with the description
   textarea as `text`, so the enquiry reaches WhatsApp either way. With JS
   every field is composed into one readable message. */
(function () {
  'use strict';

  var WA = 'https://wa.me/201069528393';
  var form = document.querySelector('[data-ig-form]');

  if (form) {
    var ar = (document.documentElement.lang || 'ar').indexOf('ar') === 0;
    var area = form.querySelector('textarea[name="text"]');
    var hidden = document.createElement('input');
    hidden.type = 'hidden';
    hidden.name = 'text';
    if (area) area.removeAttribute('name');
    form.appendChild(hidden);

    var compose = function () {
      var lines = [ar ? 'طلب ربط داتا إستاڤو بمنصتي:' : 'Estavo data integration request:'];
      Array.prototype.forEach.call(form.querySelectorAll('[data-ig-key]'), function (field) {
        var value = (field.value || '').trim();
        if (value) lines.push(field.getAttribute('data-ig-key') + ': ' + value);
      });
      lines.push(ar ? '(من صفحة ربط الداتا)' : '(from the data integrations page)');
      return lines.join('\n');
    };

    form.addEventListener('submit', function (event) {
      var text = compose();
      hidden.value = text;
      /* The one enquiry event: fired here, after native `required` validation
         passed, never on a bare button or anchor click. Categorical props only. */
      var props = { position: 'form', lang: document.documentElement.lang || '' };
      try {
        if (typeof window.gtag === 'function') window.gtag('event', 'integration_enquiry_submitted', props);
      } catch (e) { /* analytics must never block the enquiry */ }
      try {
        document.dispatchEvent(new CustomEvent('estavo:ui', { detail: { event: 'integration_enquiry_submitted', props: props } }));
      } catch (e) { /* old browsers */ }
      event.preventDefault();
      var url = WA + '?text=' + encodeURIComponent(text);
      var win = null;
      try { win = window.open(url, '_blank'); } catch (e) { win = null; }
      if (win) {
        try { win.opener = null; } catch (e) { /* cross-origin */ }
      } else {
        window.location.href = url;
      }
    });
  }

  /* The phone sticky action steps aside while the form itself is visible. */
  var sticky = document.querySelector('[data-mk-sticky]');
  var request = document.getElementById('request');
  if (sticky && request && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      sticky.classList.toggle('ig-sticky-off', entries[0].isIntersecting);
    }, { rootMargin: '0px 0px -20% 0px' }).observe(request);
  }
}());
