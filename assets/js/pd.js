/* Estavo product compositions (assets/css/pd.css) — progressive enhancement only.
   1. Arms each .pd stage and plays its intro (screens rise, 3D objects pop) when it enters.
   2. Swaps <img data-pd-anim="…svg"> to the animated product art at that moment.
   3. Pauses the objects' float while the stage is off screen.
   4. Fine pointer: the scene tilts a few degrees toward the pointer.
   Reduced motion or no IntersectionObserver: nothing runs, every stage stays complete and still. */
(() => {
  const mq = (q) => window.matchMedia && window.matchMedia(q).matches;
  if (mq('(prefers-reduced-motion: reduce)') || !('IntersectionObserver' in window)) return;
  const stages = [...document.querySelectorAll('.pd')];
  if (!stages.length) return;
  const play = (st) => {
    st.querySelectorAll('img[data-pd-anim]').forEach((img) => { img.src = img.dataset.pdAnim; img.removeAttribute('data-pd-anim'); });
    st.classList.add('is-in');
  };
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      const st = e.target;
      st.classList.toggle('is-off', !e.isIntersecting);
      if (e.isIntersecting && !st.classList.contains('is-in')) play(st);
    }
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
  stages.forEach((st) => { st.classList.add('is-armed'); io.observe(st); });

  if (!mq('(hover: hover) and (pointer: fine)')) return;
  stages.forEach((st) => {
    let raf = 0;
    st.addEventListener('pointermove', (e) => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0;
        const r = st.getBoundingClientRect();
        st.style.setProperty('--tx', ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
        st.style.setProperty('--ty', ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
      });
    });
    st.addEventListener('pointerleave', () => { st.style.setProperty('--tx', 0); st.style.setProperty('--ty', 0); });
  });
})();
