/* Client AI hero — play the example conversation once, in order.

   The conversation is visible with or without this script. The CSS
   keeps every turn at its natural state by default and only uses
   `.is-playing` to replay them as an entrance (a `backwards` fill,
   so a turn is hidden only while its own animation is pending).
   That means a blocked script, a starved observer or a renderer
   that never scrolls all still show the complete conversation —
   this file only decides *when* the entrance runs. */
(function () {
  'use strict';

  var scene = document.querySelector('[data-ai-scene]');
  if (!scene) return;

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) {
    scene.classList.add('is-playing');
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-playing');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.35 });

  observer.observe(scene);
}());
