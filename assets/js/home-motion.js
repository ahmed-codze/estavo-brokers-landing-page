/* ============================================================
   Estavo homepage — motion layer (elevated pass, Nov 2026)

   Optional polish on top of a page that is already complete.
   Nothing here may hide content that a visitor could already
   see, and nothing runs with reduced motion.

     1. header: frosted when scrolled, hides on scroll down and
        returns on scroll up (never while the menu or a header
        control is in use);
     2. section copy reveals: eyebrow, heading words, lead and
        actions rise in once, but only for sections that start
        below the fold (same contract as home.js figures);
     3. pointer-only touches: magnetic primary buttons and a soft
        tilt on the website preview;
     4. desktop only: Lenis smooth scrolling and GSAP
        ScrollTrigger parallax on decorative light layers and
        figures. The libraries are self-hosted in assets/vendor
        and loaded after the page is interactive.

   Never animated (AGENTS.md §5.2): the H1, the CTAs' existence,
   and the proof numbers. Only transform and opacity change.
   ============================================================ */
(function () {
  "use strict";

  var mq = function (q) { return !!(window.matchMedia && window.matchMedia(q).matches); };
  var reduceMotion = mq("(prefers-reduced-motion: reduce)");
  var finePointer = mq("(hover: hover) and (pointer: fine)");
  var canObserve = "IntersectionObserver" in window;
  var VENDOR = "assets/vendor/";

  function all(selector, context) {
    return Array.prototype.slice.call((context || document).querySelectorAll(selector));
  }

  function safely(fn) {
    try { fn(); } catch (e) { /* the static page stays as rendered */ }
  }

  /* ── 1. Header ─────────────────────────────────────────── */
  function initHeader() {
    var header = document.querySelector(".es-home .es-header");
    if (!header) return;
    var lastY = window.scrollY;
    var travel = 0; /* signed distance since the direction last changed */
    var ticking = false;

    function busy() {
      var drawer = document.querySelector("[data-drawer]");
      return (drawer && !drawer.hidden) || header.contains(document.activeElement);
    }

    function update() {
      ticking = false;
      var y = window.scrollY;
      header.classList.toggle("is-scrolled", y > 8);
      if (!reduceMotion) {
        var delta = y - lastY;
        travel = (delta > 0) === (travel > 0) ? travel + delta : delta;
        if (y <= 320 || busy() || travel < -24) header.classList.remove("is-tucked");
        else if (travel > 48) header.classList.add("is-tucked");
      }
      lastY = y;
    }

    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    header.addEventListener("focusin", function () { header.classList.remove("is-tucked"); });
    update();
  }

  /* ── 2. Copy reveals ───────────────────────────────────── */

  /* Wrap each word of a heading's own text in a span so it can
     rise in sequence. <bdi> runs (Latin product names) move as one
     word. textContent is unchanged; words are never split into
     letters because Arabic letters join. */
  function splitWords(heading) {
    var n = 0;
    Array.prototype.slice.call(heading.childNodes).forEach(function (node) {
      if (node.nodeType === 3) {
        var parts = node.textContent.split(/(\s+)/);
        var frag = document.createDocumentFragment();
        parts.forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
          var w = document.createElement("span");
          w.className = "es-home-w";
          w.style.setProperty("--w", String(n++));
          w.textContent = part;
          frag.appendChild(w);
        });
        node.parentNode.replaceChild(frag, node);
      } else if (node.nodeType === 1) {
        node.classList.add("es-home-w");
        node.style.setProperty("--w", String(n++));
      }
    });
    heading.style.setProperty("--words", String(n));
  }

  function initReveals() {
    if (reduceMotion || !canObserve) return;
    var sections = all(".es-home-main > section:not(#home-hero)");
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-revealed");
        entry.target.classList.remove("is-reveal-armed");
        observer.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -12%", threshold: 0.08 });

    sections.forEach(function (section) {
      if (section.getBoundingClientRect().top < window.innerHeight) return;
      var heading = section.querySelector("h2");
      if (heading && !heading.querySelector(".es-home-w")) splitWords(heading);
      section.classList.add("is-reveal-armed");
      observer.observe(section);
    });

    /* Printing or a find-in-page jump must never meet hidden copy. */
    window.addEventListener("beforeprint", function () {
      sections.forEach(function (s) { s.classList.remove("is-reveal-armed"); });
    }, { once: true });
  }

  /* ── 3. Pointer touches ────────────────────────────────── */
  function initMagnetic() {
    if (reduceMotion || !finePointer) return;
    all(".es-home-main .es-home-btn--primary").forEach(function (btn) {
      var strength = 0.22;
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        var x = (e.clientX - (r.left + r.width / 2)) * strength;
        var y = (e.clientY - (r.top + r.height / 2)) * strength;
        btn.style.setProperty("--mx", x.toFixed(1) + "px");
        btn.style.setProperty("--my", y.toFixed(1) + "px");
      });
      btn.addEventListener("pointerleave", function () {
        btn.style.setProperty("--mx", "0px");
        btn.style.setProperty("--my", "0px");
      });
    });
  }

  function initTilt() {
    if (reduceMotion || !finePointer) return;
    all(".es-home-browser").forEach(function (el) {
      var max = 3;
      var frame = 0;
      el.classList.add("es-home-tilt");
      el.addEventListener("pointermove", function (e) {
        if (frame) return;
        frame = window.requestAnimationFrame(function () {
          frame = 0;
          var r = el.getBoundingClientRect();
          var px = (e.clientX - r.left) / r.width - 0.5;
          var py = (e.clientY - r.top) / r.height - 0.5;
          el.style.setProperty("--rx", (-py * max).toFixed(2) + "deg");
          el.style.setProperty("--ry", (px * max).toFixed(2) + "deg");
          el.style.setProperty("--gx", ((px + 0.5) * 100).toFixed(0) + "%");
          el.style.setProperty("--gy", ((py + 0.5) * 100).toFixed(0) + "%");
        });
      });
      el.addEventListener("pointerleave", function () {
        el.style.setProperty("--rx", "0deg");
        el.style.setProperty("--ry", "0deg");
      });
    });
  }

  /* ── 4. Desktop: Lenis + GSAP ScrollTrigger ────────────── */
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.async = false;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  /* Decorative light layers (aria-hidden, behind content) that the
     parallax moves. Added here so the HTML stays as approved. */
  function addAuras() {
    all("#home-hero, .es-home-band--navy").forEach(function (band) {
      if (band.querySelector(":scope > .es-home-aura")) return;
      var aura = document.createElement("div");
      aura.className = "es-home-aura";
      aura.setAttribute("aria-hidden", "true");
      band.insertBefore(aura, band.firstChild);
    });
  }

  function initSmoothAndParallax() {
    if (reduceMotion || !finePointer || !mq("(min-width: 64rem)")) return;
    if (!window.Promise) return;

    Promise.all([
      loadScript(VENDOR + "lenis-1.1.20.min.js"),
      loadScript(VENDOR + "gsap-3.12.5.min.js"),
      loadScript(VENDOR + "ScrollTrigger-3.12.5.min.js")
    ]).then(function () {
      var gsap = window.gsap;
      var ScrollTrigger = window.ScrollTrigger;
      if (!gsap || !ScrollTrigger) return;
      gsap.registerPlugin(ScrollTrigger);

      if (window.Lenis) {
        var lenis = new window.Lenis({
          lerp: 0.11,
          smoothWheel: true,
          anchors: true,
          /* Let the support chat, the menu and wide tables scroll natively. */
          prevent: function (node) {
            return !!(node && node.closest && node.closest(".raghad-scroll, [class*=\"raghad\"], [data-drawer], .es-home-disclosure__body"));
          }
        });
        lenis.on("scroll", ScrollTrigger.update);
        gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
        gsap.ticker.lagSmoothing(0);
        document.documentElement.classList.add("es-home-smooth");
      }

      /* Light layers drift slower than the page. */
      all(".es-home-aura").forEach(function (aura) {
        gsap.fromTo(aura, { yPercent: -6 }, {
          yPercent: 10,
          ease: "none",
          scrollTrigger: { trigger: aura.parentNode, start: "top bottom", end: "bottom top", scrub: true }
        });
      });

      /* Figures settle a few pixels as their section crosses the
         viewport: depth, never displacement of readable copy. */
      all("#home-data .es-home-market, #home-website .es-home-build, #home-integrations .es-home-flow").forEach(function (fig) {
        gsap.fromTo(fig, { y: 36 }, {
          y: -18,
          ease: "none",
          scrollTrigger: { trigger: fig, start: "top bottom", end: "bottom top", scrub: 0.6 }
        });
      });

      /* content-visibility sections change height as they render. */
      window.addEventListener("load", function () { ScrollTrigger.refresh(); }, { once: true });
    }).catch(function () { /* native scrolling stays */ });
  }

  function init() {
    safely(addAuras);
    [initHeader, initReveals, initMagnetic, initTilt].forEach(safely);
    /* Heavy libraries wait until the browser is idle. */
    var later = window.requestIdleCallback || function (fn) { return window.setTimeout(fn, 600); };
    later(function () { safely(initSmoothAndParallax); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
