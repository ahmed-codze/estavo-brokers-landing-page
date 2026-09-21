/* Shared commercial-page enhancement. Core content remains visible without JS. */
(function () {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = [...document.querySelectorAll('.reveal')];

  if (reduced || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('visible'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealItems.forEach((item) => observer.observe(item));
  }

  document.querySelectorAll('[data-commercial-proof], .market-proof').forEach((proof) => {
    if (reduced || !('IntersectionObserver' in window)) return;

    proof.classList.add('motion-ready');
    const counters = [...proof.querySelectorAll('[data-count]')];
    const numberFormatter = new Intl.NumberFormat('en-US');

    const animateCounter = (counter, index) => {
      const target = Number(counter.dataset.count);
      const duration = 1050 + (index * 140);
      const startedAt = performance.now();

      const tick = (now) => {
        const progress = Math.min((now - startedAt) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        counter.textContent = numberFormatter.format(Math.round(target * eased));
        if (progress < 1) window.requestAnimationFrame(tick);
      };

      window.requestAnimationFrame(tick);
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        proof.classList.add('is-visible');
        counters.forEach(animateCounter);
        observer.unobserve(proof);
      });
    }, { threshold: 0.25 });

    observer.observe(proof);
  });
}());
