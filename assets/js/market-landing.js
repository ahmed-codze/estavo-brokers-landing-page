/* Estavo Market landing page — progressive enhancement only.
   Without JS every step, the default comparison and the whole chat are
   visible; this file adds the tabbed workflow, the priority switch, the
   staged chat reveal and the mobile sticky action. */
(function () {
  'use strict';

  var root = document.querySelector('[data-mk]');
  if (!root) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;
  var all = function (sel, scope) { return Array.prototype.slice.call((scope || document).querySelectorAll(sel)); };

  /* ── Workflow tabs ─────────────────────────────────────────── */
  all('[data-mk-tabs]', root).forEach(function (wrap) {
    var list = wrap.querySelector('[data-mk-tablist]');
    var tabs = all('[data-mk-tab]', wrap);
    var panels = all('[data-mk-panel]', wrap);
    if (!list || tabs.length !== panels.length) return;

    var STEP_MS = 6500;
    var timer = null;
    var current = 0;
    var autoDone = reduced;

    wrap.classList.add('is-enhanced');
    wrap.style.setProperty('--mk-step-ms', STEP_MS + 'ms');
    list.setAttribute('role', 'tablist');

    tabs.forEach(function (tab, i) {
      var key = tab.getAttribute('data-mk-tab');
      var panel = panels[i];
      tab.id = 'mk-tab-' + key;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', 'mk-panel-' + key);
      panel.id = 'mk-panel-' + key;
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
      panel.setAttribute('tabindex', '0');
    });

    function stopAuto() {
      autoDone = true;
      wrap.classList.remove('is-auto');
      if (timer) { window.clearTimeout(timer); timer = null; }
    }

    function select(index, focus) {
      current = index;
      tabs.forEach(function (tab, i) {
        var on = i === index;
        tab.setAttribute('aria-selected', String(on));
        tab.tabIndex = on ? 0 : -1;
        panels[i].hidden = !on;
        panels[i].classList.toggle('is-active', on);
      });
      if (focus) tabs[index].focus();
      if (!autoDone) schedule();
    }

    /* One pass through the three steps, then it rests on the last. */
    function schedule() {
      if (timer) window.clearTimeout(timer);
      if (current >= tabs.length - 1) { stopAuto(); return; }
      wrap.classList.remove('is-auto');
      void wrap.offsetWidth; // restart the progress bar
      wrap.classList.add('is-auto');
      timer = window.setTimeout(function () { select(current + 1, false); }, STEP_MS);
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { stopAuto(); select(i, false); });
      tab.addEventListener('keydown', function (event) {
        var rtl = document.documentElement.dir === 'rtl';
        var next = { ArrowRight: rtl ? -1 : 1, ArrowLeft: rtl ? 1 : -1, ArrowDown: 1, ArrowUp: -1 }[event.key];
        if (event.key === 'Home') next = -i;
        if (event.key === 'End') next = tabs.length - 1 - i;
        if (next === undefined) return;
        event.preventDefault();
        stopAuto();
        select((i + next + tabs.length) % tabs.length, true);
      });
    });

    ['pointerenter', 'focusin'].forEach(function (name) {
      wrap.addEventListener(name, function () {
        if (!autoDone && timer) { window.clearTimeout(timer); timer = null; wrap.classList.remove('is-auto'); }
      });
    });
    ['pointerleave', 'focusout'].forEach(function (name) {
      wrap.addEventListener(name, function (event) {
        if (autoDone || (event.relatedTarget && wrap.contains(event.relatedTarget))) return;
        schedule();
      });
    });

    autoDone = true;
    select(0, false);

    /* Start the auto pass only when the visitor can actually see it. */
    if (!reduced && hasIO) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          io.disconnect();
          autoDone = false;
          schedule();
        });
      }, { threshold: 0.45 });
      io.observe(wrap);
    }
  });

  /* ── Comparison priority ───────────────────────────────────── */
  all('[data-mk-board]', root).forEach(function (board) {
    var buttons = all('[data-mk-prio]', board);
    var reasons = all('[data-mk-reason]', board);
    board.classList.add('is-enhanced');
    buttons.forEach(function (button) {
      button.addEventListener('click', function () {
        var key = button.getAttribute('data-mk-prio');
        var rows = all('.mk-board__row[data-unit]', board);
        var before = rows.map(function (row) { return row.getBoundingClientRect().top; });
        board.setAttribute('data-priority', key);
        if (!reduced) {
          rows.forEach(function (row, i) {
            var shift = before[i] - row.getBoundingClientRect().top;
            if (!shift) return;
            row.animate([{ transform: 'translateY(' + shift + 'px)' }, { transform: 'none' }],
              { duration: 520, easing: 'cubic-bezier(.22,.61,.36,1)' });
          });
        }
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === button)); });
        reasons.forEach(function (r) { r.hidden = r.getAttribute('data-mk-reason') !== key; });
      });
    });
  });

  /* ── Illustrations: assemble when they come into view ────────
     The HTML ships the complete still SVGs (no-JS, reduced motion, print).
     With motion allowed, each picture is blanked until it scrolls into
     view, then its animated twin loads, so the scene assembles in front of
     the visitor instead of finishing off-screen. */
  var BLANK = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
  var arts = all('picture[data-mk-anim]', root);
  if (arts.length && !reduced && hasIO) {
    var setAll = function (pic, mode) {
      all('source, img', pic).forEach(function (el) {
        var attr = el.tagName === 'IMG' ? 'src' : 'srcset';
        if (!el.dataset.still) el.dataset.still = el.getAttribute(attr);
        var still = el.dataset.still;
        /* A transparent placeholder with the art's own proportions keeps the
           reserved box identical, so swapping in the animated file never shifts layout. */
        var blank = BLANK;
        var w = el.getAttribute('width'), h = el.getAttribute('height');
        if (w && h) blank = 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + ' ' + h + '"/>');
        el.setAttribute(attr, mode === 'blank' ? blank : mode === 'anim' ? still.replace('-still.svg', '.svg') : still);
      });
    };
    var artIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        artIO.unobserve(entry.target);
        setAll(entry.target, 'anim');
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.2 });
    arts.forEach(function (pic) {
      var box = pic.getBoundingClientRect();
      if (box.top < window.innerHeight && box.bottom > 0 && box.height > 0) {
        setAll(pic, 'anim');
        return;
      }
      setAll(pic, 'blank');
      artIO.observe(pic);
    });
    window.addEventListener('beforeprint', function () { arts.forEach(function (pic) { setAll(pic, 'still'); }); });
  }

  /* ── Mobile sticky action ──────────────────────────────────── */
  var sticky = root.querySelector('[data-mk-sticky]');
  if (sticky && hasIO) {
    var blockers = all('[data-position="hero"], [data-position="close"], .es-footer', document);
    var visible = new Set();
    var hero = document.getElementById('hero');
    var pastHero = false;
    var update = function () {
      sticky.classList.toggle('is-shown', pastHero && visible.size === 0);
    };
    var blockIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) visible.add(entry.target); else visible.delete(entry.target);
      });
      update();
    });
    blockers.forEach(function (el) { blockIO.observe(el); });
    if (hero) {
      new IntersectionObserver(function (entries) {
        pastHero = !entries[0].isIntersecting;
        update();
      }, { rootMargin: '-35% 0px 0px 0px' }).observe(hero);
    }
  }
}());
