/* "Try Estavo free" popup + phone sticky bar, on every page (markup from tools/partials/try.*.html).
   Popup: once per visit, only after real engagement (40% scrolled and 12s, or desktop exit intent
   after 8s); never after the visitor already clicked a free CTA; not again for 3 days once closed.
   Accessible dialog: focus moves to the CTA, Tab is trapped, Esc / backdrop / buttons close, focus returns.
   Sticky bar (phones): appears after the hero, hides near the footer and while the popup is open.
   No JS: nothing shows (the page's own CTAs remain). */
(function () {
  'use strict';
  var pop = document.querySelector('[data-try-pop]');
  var bar = document.querySelector('[data-try-sticky]');
  if (!pop && !bar) return;
  var store = function (kind, key, value) {
    try {
      var s = kind === 'local' ? window.localStorage : window.sessionStorage;
      if (value === undefined) return s.getItem(key);
      s.setItem(key, value);
    } catch (e) { return null; }
    return null;
  };
  var ev = function (name, extra) {
    if (typeof window.gtag === 'function') {
      var p = { page: location.pathname, lang: document.documentElement.lang };
      for (var k in extra || {}) p[k] = extra[k];
      window.gtag('event', name, p);
    }
  };
  var FREE = 'a[href*="brokers.estavo.space"], a[href*="estavo-brokers.com/website"]';
  var converted = function () { return store('session', 'try-converted') === '1'; };
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest(FREE);
    if (a) store('session', 'try-converted', '1');
  }, true);

  /* ── popup ── */
  var DAY = 864e5, opened = false, lastFocus = null;
  // /market/ has its own popup; never show two
  var eligible = !!pop && !document.querySelector('[data-mk-pop]') && !store('session', 'try-shown') &&
    (Date.now() - Number(store('local', 'try-closed') || 0) > 3 * DAY);
  var started = Date.now();
  var card = pop && pop.querySelector('.try-pop__card');
  var focusables = function () { return card.querySelectorAll('a[href], button'); };
  var onKey = function (e) {
    if (e.key === 'Escape') return close('escape');
    if (e.key !== 'Tab') return;
    var f = focusables(), first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  };
  function open(reason) {
    if (opened || !eligible || converted()) return;
    opened = true; eligible = false;
    store('session', 'try-shown', '1');
    lastFocus = document.activeElement;
    pop.hidden = false;
    document.documentElement.classList.add('try-pop-open');
    requestAnimationFrame(function () { pop.classList.add('is-open'); });
    var cta = pop.querySelector('.try-pop__cta'); if (cta) cta.focus({ preventScroll: true });
    document.addEventListener('keydown', onKey);
    ev('try_popup_shown', { trigger: reason });
  }
  function close(how) {
    if (!opened) return;
    opened = false;
    pop.classList.remove('is-open');
    document.documentElement.classList.remove('try-pop-open');
    document.removeEventListener('keydown', onKey);
    store('local', 'try-closed', String(Date.now()));
    setTimeout(function () { pop.hidden = true; }, 250);
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    ev('try_popup_closed', { how: how });
  }
  if (pop) {
    pop.querySelectorAll('[data-try-close]').forEach(function (b) { b.addEventListener('click', function () { close('button'); }); });
    pop.querySelectorAll(FREE).forEach(function (a) { a.addEventListener('click', function () { setTimeout(function () { close('cta'); }, 0); }); });
  }
  var check = function () {
    if (!eligible) return;
    var doc = document.documentElement;
    var scrolled = (window.scrollY + window.innerHeight) / Math.max(doc.scrollHeight, 1);
    if (scrolled > 0.4 && Date.now() - started > 12000) open('scroll');
  };
  if (eligible) {
    window.addEventListener('scroll', check, { passive: true });
    setInterval(check, 2000);
    if (window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      document.addEventListener('mouseout', function (e) {
        if (!e.relatedTarget && e.clientY <= 0 && Date.now() - started > 8000) open('exit');
      });
    }
  }

  /* ── phone sticky bar ── */
  if (bar && !document.querySelector('[data-mk-sticky], [data-home-sticky]')) {
    var footer = document.querySelector('.es-footer');
    var update = function () {
      var past = window.scrollY > window.innerHeight * 0.7;
      var nearFoot = footer && footer.getBoundingClientRect().top < window.innerHeight;
      var show = past && !nearFoot && !opened;
      if (show && bar.hidden) bar.hidden = false;
      bar.classList.toggle('is-on', show);
    };
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  } else if (bar) {
    bar.remove();
  }
})();
