/* ============================================================
   Estavo homepage — progressive enhancement

   The page is complete without this file: every figure ships in
   its final, resolved state. This script only:

     1. arms below-fold signature figures (hides their parts)
        while they are still off-screen, then plays them once
        on entry — never re-hides something already seen;
     2. adds homepage-specific analytics names alongside the
        shared data-track events (estavo-v3.js keeps sending
        market_opened / website_preview_started as before);
     3. sends passive section-view events (never conversions);
     4. shows the mobile sticky CTA only between the hero CTA
        and the closing CTA.

   The hero sequence is CSS-only and needs nothing from here.
   Each initialiser is isolated so one failure cannot hide
   content or stop the others.
   ============================================================ */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canObserve = "IntersectionObserver" in window;

  function all(selector, context) {
    return Array.prototype.slice.call((context || document).querySelectorAll(selector));
  }

  /* Same contract as estavo-v3.js: categorical properties only. */
  function track(name, props) {
    var payload = props || {};
    try {
      if (typeof window.gtag === "function") window.gtag("event", name, payload);
    } catch (e) { /* analytics never breaks the page */ }
    document.dispatchEvent(new CustomEvent("estavo:ui", { detail: { event: name, props: payload } }));
  }

  function safely(fn) {
    try { fn(); } catch (e) { /* leave the static final state in place */ }
  }

  /* Stagger indices are written as a custom property so the CSS
     can derive delays without per-item rules. */
  function index(selector, context) {
    all(selector, context).forEach(function (item, i) {
      item.style.setProperty("--i", String(i));
    });
  }

  /* Arm a figure only if it is entirely below the viewport; a
     figure already on screen is left exactly as rendered. */
  function playOnEntry(figure) {
    if (reduceMotion || !canObserve) return;
    var bounds = figure.getBoundingClientRect();
    if (bounds.top < window.innerHeight) return;

    figure.classList.add("is-armed");
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        figure.classList.add("is-playing");
        figure.classList.remove("is-armed");
        observer.disconnect();
        window.removeEventListener("beforeprint", settle);
      });
    }, { rootMargin: "0px 0px -15%", threshold: 0.2 });
    observer.observe(figure);

    function settle() {
      figure.classList.remove("is-armed");
      observer.disconnect();
      window.removeEventListener("beforeprint", settle);
    }
    window.addEventListener("beforeprint", settle, { once: true });
  }

  function initHomeMarketAssembly() {
    var figure = document.querySelector("[data-home-market]");
    if (!figure) return;
    index(".es-home-frag", figure);
    index(".es-home-map__project", figure);
    index(".es-home-map__node:not(.es-home-map__node--hub):not(.es-home-map__node--selected)", figure);
    playOnEntry(figure);
  }

  function initHomeRequestAnalysis() {
    var figure = document.querySelector("[data-home-request]");
    if (!figure) return;
    index(".es-home-ask .es-home-chip", figure);
    index(".es-home-prop", figure);
    playOnEntry(figure);
  }

  function initHomeWebsite() {
    var figure = document.querySelector("[data-home-site]");
    if (!figure) return;
    index(".es-home-listing", figure);
    playOnEntry(figure);
  }

  function initHomeClientSignals() {
    var signals = document.querySelector("[data-home-signals]");
    if (signals) {
      index(".es-home-signal, .es-home-step", signals);
      playOnEntry(signals);
    }
    var match = document.querySelector("[data-home-match]");
    if (match) {
      index(".es-home-interest", match);
      playOnEntry(match);
    }
  }

  function initHomeGrowthClusters() {
    var figure = document.querySelector("[data-home-clusters]");
    if (!figure) return;
    index(".es-home-dot", figure);
    playOnEntry(figure);
  }

  /* Proof strip: the verified final values ship in the HTML. On entry the
     numbers count up once from 85% (never from zero), then rest. */
  function initHomeProof() {
    var strip = document.querySelector("[data-home-proof]");
    if (!strip || reduceMotion || !canObserve) return;
    var values = all("[data-count]", strip);
    var format = function (n) { return Math.round(n).toLocaleString("en-US") + "+"; };

    var observer = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      observer.disconnect();
      strip.classList.add("is-playing");
      var start = null;
      function frame(now) {
        if (start === null) start = now;
        var t = Math.min(1, (now - start) / 900);
        var eased = 1 - Math.pow(1 - t, 3);
        values.forEach(function (el) {
          var target = Number(el.getAttribute("data-count"));
          el.textContent = format(target * (0.85 + 0.15 * eased));
        });
        if (t < 1) window.requestAnimationFrame(frame);
        else values.forEach(function (el) { el.textContent = format(Number(el.getAttribute("data-count"))); });
      }
      window.requestAnimationFrame(frame);
    }, { threshold: 0.5 });
    observer.observe(strip);
  }

  function initHomeEvents() {
    all("[data-home-event]").forEach(function (link) {
      link.addEventListener("click", function () {
        track(link.getAttribute("data-home-event"), {
          position: link.getAttribute("data-position") || "",
          lang: document.documentElement.lang || ""
        });
      });
    });

    if (!canObserve) return;
    var views = all("[data-home-view]");
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        track(entry.target.getAttribute("data-home-view"), { lang: document.documentElement.lang || "" });
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.4 });
    views.forEach(function (view) { observer.observe(view); });
  }

  /* One restrained bar on phones: hidden while the hero CTA or the
     closing CTA is on screen. raghad.js watches the .visible class
     on .sticky-cta and lifts its launcher accordingly. */
  function initHomeMobileCta() {
    var bar = document.querySelector("[data-home-sticky]");
    var hero = document.querySelector("#home-hero .es-home-actions");
    var closing = document.querySelector("#home-closing");
    if (!bar || !hero || !closing || !canObserve) return;

    var heroVisible = true;
    var closingVisible = false;

    function update() {
      var show = !heroVisible && !closingVisible;
      bar.classList.toggle("visible", show);
      bar.setAttribute("aria-hidden", show ? "false" : "true");
      var link = bar.querySelector("a");
      if (link) link.tabIndex = show ? 0 : -1;
    }

    new IntersectionObserver(function (entries) {
      heroVisible = entries[0].isIntersecting;
      update();
    }).observe(hero);

    new IntersectionObserver(function (entries) {
      closingVisible = entries[0].isIntersecting;
      update();
    }, { threshold: 0.15 }).observe(closing);

    update();
  }

  function init() {
    [
      initHomeMarketAssembly,
      initHomeRequestAnalysis,
      initHomeWebsite,
      initHomeClientSignals,
      initHomeGrowthClusters,
      initHomeProof,
      initHomeEvents,
      initHomeMobileCta
    ].forEach(safely);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
