/* /challenges/ — Exclusive round demo (progressive enhancement only).
   Without JS the hero shows the revealed round and the standings stacked.
   With JS the three stages (answer → result → standings) become one card
   switched by the stepper; with motion allowed it plays through once when
   the card is first seen, then rests on the standings. */
(function () {
  'use strict';

  var round = document.querySelector('[data-ch-round]');
  if (!round) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var stepper = document.querySelector('[data-ch-stepper]');
  var panels = Array.prototype.slice.call(round.querySelectorAll('[data-ch-panel]'));
  var buttons = stepper ? Array.prototype.slice.call(stepper.querySelectorAll('[data-ch-go]')) : [];
  var clock = round.querySelector('[data-ch-clock]');
  var late = round.querySelector('[data-ch-late]');
  var count = round.querySelector('[data-ch-count]');
  var board = round.querySelector('[data-ch-board]');
  var timers = [];
  var ticking = null;

  function clearTimers() {
    timers.forEach(function (t) { window.clearTimeout(t); });
    timers = [];
    if (ticking) { window.clearInterval(ticking); ticking = null; }
  }

  function later(fn, ms) { timers.push(window.setTimeout(fn, ms)); }

  function resetAnswer() {
    if (clock) clock.textContent = '0:42';
    if (late) late.classList.remove('is-in', 'is-new');
    if (count) count.textContent = '3';
  }

  function playAnswer() {
    resetAnswer();
    if (reduced) {
      if (late) late.classList.add('is-in');
      if (count) count.textContent = '4';
      return;
    }
    var seconds = 42;
    ticking = window.setInterval(function () {
      seconds -= 1;
      if (clock) clock.textContent = '0:' + String(seconds).padStart(2, '0');
      if (seconds <= 38) { window.clearInterval(ticking); ticking = null; }
    }, 700);
    later(function () {
      if (late) late.classList.add('is-in', 'is-new');
      if (count) count.textContent = '4';
    }, 1600);
  }

  /* Standings: Mona overtakes Karim (FLIP) while her total counts up. */
  function playBoard() {
    if (reduced || !board || !board.animate) return;
    var mona = board.querySelector('[data-ch-row="mona"]');
    var karim = board.querySelector('[data-ch-row="karim"]');
    if (!mona || !karim) return;
    var shift = karim.getBoundingClientRect().top - mona.getBoundingClientRect().top;
    if (!shift) return;
    var ease = 'cubic-bezier(.22,.61,.36,1)';
    mona.animate([{ transform: 'translateY(' + (-shift) + 'px)' }, { transform: 'translateY(' + (-shift) + 'px)', offset: 0.45 }, { transform: 'none' }], { duration: 1400, easing: ease });
    karim.animate([{ transform: 'translateY(' + shift + 'px)' }, { transform: 'translateY(' + shift + 'px)', offset: 0.45 }, { transform: 'none' }], { duration: 1400, easing: ease });
    var total = mona.querySelector('[data-ch-from]');
    if (!total) return;
    var from = Number(total.getAttribute('data-ch-from'));
    var to = Number(total.textContent);
    var start = null;
    var step = function (now) {
      if (start === null) start = now;
      var p = Math.min(1, (now - start) / 600);
      total.textContent = String(Math.round(from + (to - from) * p));
      if (p < 1) window.requestAnimationFrame(step);
    };
    total.textContent = String(from);
    later(function () { window.requestAnimationFrame(step); }, 150);
  }

  function show(stage, animate) {
    clearTimers();
    round.setAttribute('data-stage', stage);
    round.classList.toggle('is-animating', Boolean(animate) && !reduced);
    panels.forEach(function (p) {
      var on = p.getAttribute('data-ch-panel') === stage;
      p.classList.toggle('is-on', on);
      p.setAttribute('aria-hidden', on ? 'false' : 'true');
    });
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-ch-go') === stage)); });
    if (stage === 'answer') playAnswer();
    if (stage === 'board' && animate) playBoard();
  }

  round.classList.add('is-enhanced');
  if (stepper) stepper.hidden = false;
  show('reveal', false);

  var auto = !reduced && 'IntersectionObserver' in window;
  function stopAuto() { auto = false; }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      stopAuto();
      show(b.getAttribute('data-ch-go'), true);
    });
  });

  if (auto) {
    var io = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      io.disconnect();
      if (!auto) return;
      show('answer', true);
      window.setTimeout(function () { if (auto) show('reveal', true); }, 3800);
      window.setTimeout(function () {
        if (!auto) return;
        auto = false;
        show('board', true);
      }, 3800 + 4400);
    }, { threshold: 0.5 });
    io.observe(round);
  }
}());
