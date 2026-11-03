/* Estavo Signal — progressive enhancement for fx.css stages (optional; pages work without it).
   1. Off screen, stages/bands get .fx-is-offscreen (CSS pauses their ambient animation).
   2. Scene SVGs in <img> can't be paused from outside, so stage art marked [data-fx-swap] (on the
      <picture> or the <img>) follows the tools/build-fx-art.py file trio for every source:
      first time on screen -> x.svg (intro + loops) · off screen -> x-still.svg ·
      back on screen -> x-loop.svg with data-fx-swap="loop" (no intro replay), else x.svg again.
      The HTML may point at either x.svg or x-still.svg; reduced-motion <source>s are left alone.
   3. Fine pointer only: a soft spotlight follows the pointer and the art + labels shift a few px.
   Does nothing under prefers-reduced-motion (the <picture> reduced-motion source shows the still). */
(() => {
  const mq = (q) => window.matchMedia && window.matchMedia(q).matches;
  if (mq('(prefers-reduced-motion: reduce)')) return;
  const variant = (v, suffix) => v.replace(/([^\s,?#]+?)(?:-still|-loop)?\.svg/g, `$1${suffix}.svg`);
  const swap = (stage, on) => {
    const seen = stage.dataset.fxSeen === '1';
    stage.dataset.fxSeen = seen || on ? '1' : '';
    stage.querySelectorAll('[data-fx-swap]').forEach((art) => {
      const suffix = !on ? '-still' : (seen && art.dataset.fxSwap === 'loop' ? '-loop' : '');
      const els = art.matches('img') ? [art] : art.querySelectorAll('img, source');
      els.forEach((el) => {
        if (/reduce/.test(el.getAttribute('media') || '')) return;
        const attr = el.matches('source') ? 'srcset' : 'src';
        const v = el.getAttribute(attr) || '';
        const next = variant(v, suffix);
        if (next !== v) el.setAttribute(attr, next);
      });
    });
  };
  const live = document.querySelectorAll('.fx-stage, .fx-band');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        const on = e.isIntersecting;
        if (e.target.dataset.fxOn === String(on)) continue;
        e.target.dataset.fxOn = String(on);
        e.target.classList.toggle('fx-is-offscreen', !on);
        swap(e.target, on);
      }
    }, { rootMargin: '160px 0px' });
    live.forEach((el) => io.observe(el));
  }
  if (!mq('(hover: hover) and (pointer: fine)')) return;
  document.querySelectorAll('.fx-stage:not(.fx-stage--light):not([data-fx-still])').forEach((stage) => {
    const light = document.createElement('span');
    light.className = 'fx-stage__light';
    light.setAttribute('aria-hidden', 'true');
    stage.prepend(light);
    let raf = 0;
    let pt = null;
    const paint = () => {
      raf = 0;
      if (!pt) return;
      const r = stage.getBoundingClientRect();
      const x = pt.clientX - r.left;
      const y = pt.clientY - r.top;
      light.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      stage.style.setProperty('--fx-px', `${((x / r.width) - 0.5) * -10}px`);
      stage.style.setProperty('--fx-py', `${((y / r.height) - 0.5) * -8}px`);
    };
    stage.addEventListener('pointermove', (e) => {
      pt = e;
      if (!raf) raf = requestAnimationFrame(paint);
    }, { passive: true });
    stage.addEventListener('pointerenter', () => stage.classList.add('is-lit'));
    stage.addEventListener('pointerleave', () => {
      stage.classList.remove('is-lit');
      stage.style.setProperty('--fx-px', '0px');
      stage.style.setProperty('--fx-py', '0px');
    });
  });
})();
