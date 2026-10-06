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
     4. shows the mobile Market bar only while no other Market
        CTA, the footer, the menu, the support chat or the
        on-screen keyboard needs that space.

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
    playOnEntry(figure);
  }

  function initHomeRequestAnalysis() {
    var figure = document.querySelector("[data-home-request]");
    if (!figure) return;
    index(".es-home-ask .es-home-chip", figure);
    index(".es-home-opt", figure);
    playOnEntry(figure);
  }

  function initHomeWebsite() {
    var figure = document.querySelector("[data-home-site]");
    if (!figure) return;
    playOnEntry(figure);
  }

  function initHomeClientSignals() {
    var signals = document.querySelector("[data-home-signals]");
    if (signals) {
      index(".es-home-sig", signals);
      playOnEntry(signals);
    }
  }

  function initHomeGrowthClusters() {
    var figure = document.querySelector("[data-home-clusters]");
    if (!figure) return;
    index(".es-home-dot", figure);
    playOnEntry(figure);
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

  /* One restrained bar on phones. It never sits on top of another
     visible Market CTA (hero, market, start-free, closing) or the
     footer, and steps aside while the menu drawer, the support chat
     or the on-screen keyboard needs the space. raghad.js watches the
     .visible class on .sticky-cta and lifts its launcher. Focused
     controls are kept clear of it by scroll-padding in home.css. */
  function initHomeMobileCta() {
    var bar = document.querySelector("[data-home-sticky]");
    if (!bar || !canObserve) return;

    /* In-page Market CTAs only: the header button is always on screen and
       sits at the opposite edge, so it does not compete with the bar. */
    var blockers = all("main [data-track=\"market_opened\"]")
      .concat(all(".es-footer"));
    var onScreen = new Set();
    var typing = false;

    function overlayOpen() {
      var drawer = document.querySelector("[data-drawer]");
      return (drawer && !drawer.hidden) ||
        !!document.querySelector("[data-raghad-open=\"true\"]");
    }

    function update() {
      var show = onScreen.size === 0 && !typing && !overlayOpen();
      bar.classList.toggle("visible", show);
      bar.setAttribute("aria-hidden", show ? "false" : "true");
      var link = bar.querySelector("a");
      if (link) link.tabIndex = show ? 0 : -1;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) onScreen.add(entry.target);
        else onScreen.delete(entry.target);
      });
      update();
    });
    blockers.forEach(function (el) { observer.observe(el); });

    function isField(el) {
      return el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
    }
    document.addEventListener("focusin", function (event) { typing = isField(event.target); update(); });
    document.addEventListener("focusout", function () { typing = false; update(); });

    new MutationObserver(update).observe(document.body, {
      subtree: true, attributes: true, attributeFilter: ["hidden", "data-raghad-open"]
    });

    update();
  }

  function init() {
    [
      initHomeMarketAssembly,
      initHomeRequestAnalysis,
      initHomeWebsite,
      initHomeClientSignals,
      initHomeGrowthClusters,
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
