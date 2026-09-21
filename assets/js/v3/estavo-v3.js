/* ============================================================
   Estavo v3 — interactions

   Progressive enhancement only: every page is readable and
   every CTA reachable without this file.

   Rules this file obeys (Visual Theme Plan v1 §11.3):
     - No module creates product data.
     - Prepared examples live in the HTML, never generated here.
     - Interaction works with keyboard and touch.
     - Reduced motion and page visibility are respected.
     - Analytics receive event names and safe categorical
       properties, never raw customer requests or values.
   ============================================================ */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Signals to CSS that it may now hide things for animation.
     Set before first paint work so no content flashes. */
  root.classList.add("has-js");

  function all(selector, context) {
    return Array.prototype.slice.call((context || document).querySelectorAll(selector));
  }

  /* Categorical, non-identifying analytics only. Falls through
     to gtag when present; otherwise emits a DOM event so the
     page stays testable without a vendor. */
  function track(name, props) {
    var payload = props || {};
    try {
      if (typeof window.gtag === "function") {
        window.gtag("event", name, payload);
      }
    } catch (e) { /* analytics must never break the page */ }
    document.dispatchEvent(new CustomEvent("estavo:ui", {
      detail: { event: name, props: payload }
    }));
  }

  /* Content stays visible by default. Animate each section on entry;
     below-fold sections must not be consumed by a global load deadline. */
  function initReveal() {
    var items = all("[data-reveal], [data-reveal-stagger]");
    if (!items.length) return;

    function revealAll() {
      items.forEach(function (item) { item.classList.add("is-visible"); });
    }

    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealAll();
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8%", threshold: 0.12 });

    items.forEach(function (item) { observer.observe(item); });

    /* A missed observer callback must not delay visible content. Keep
       observing below the fold so later scrolling still has motion. */
    window.setTimeout(function () {
      items.forEach(function (item) {
        var bounds = item.getBoundingClientRect();
        if (bounds.top < window.innerHeight && bounds.bottom > 0) {
          item.classList.add("is-visible");
          observer.unobserve(item);
        }
      });
    }, 2500);

    /* Printing must never produce blank sections. */
    if (window.matchMedia) {
      var printQuery = window.matchMedia("print");
      if (printQuery.addEventListener) {
        printQuery.addEventListener("change", revealAll);
      }
    }
    window.addEventListener("beforeprint", revealAll);
  }

  /* A small camera movement gives the vector layers physical depth.
     It is decoration only; touch and reduced-motion readers see a stable scene. */
  function initArtMotion() {
    if (reduceMotion || !window.matchMedia ||
        !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    all(".es-hero__figure, .es-brand-unified-figure, .es-service-hero-art").forEach(function (scene) {
      scene.classList.add("es-art-stage");
      var pending = false;
      var pointerX = 0;
      var pointerY = 0;
      scene.addEventListener("pointermove", function (event) {
        var bounds = scene.getBoundingClientRect();
        pointerX = (event.clientX - bounds.left) / bounds.width - .5;
        pointerY = (event.clientY - bounds.top) / bounds.height - .5;
        if (pending) return;
        pending = true;
        window.requestAnimationFrame(function () {
          scene.style.setProperty("--art-rx", (-pointerY * 2.4).toFixed(2) + "deg");
          scene.style.setProperty("--art-ry", (pointerX * 2.4).toFixed(2) + "deg");
          pending = false;
        });
      }, { passive: true });
      scene.addEventListener("pointerleave", function () {
        scene.style.setProperty("--art-rx", "0deg");
        scene.style.setProperty("--art-ry", "0deg");
      });
    });
  }

  /* ── Flow rail draws once on entry ───────────────────── */
  function initFlowReveal() {
    var flows = all(".es-flow");
    if (!flows.length || reduceMotion || !("IntersectionObserver" in window)) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.setAttribute("data-flow-active", "");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.35 });

    flows.forEach(function (flow) { observer.observe(flow); });
  }

  /* ── Header: solutions menu + mobile drawer ──────────── */
  function initHeader() {
    var menu = document.querySelector("[data-menu]");
    if (menu) {
      var trigger = menu.querySelector("[data-menu-trigger]");
      var panel = menu.querySelector("[data-menu-panel]");

      if (trigger && panel) {
        var closeMenu = function () {
          panel.hidden = true;
          trigger.setAttribute("aria-expanded", "false");
        };

        trigger.addEventListener("click", function () {
          var open = trigger.getAttribute("aria-expanded") === "true";
          panel.hidden = open;
          trigger.setAttribute("aria-expanded", String(!open));
        });

        document.addEventListener("click", function (event) {
          if (!menu.contains(event.target)) closeMenu();
        });

        document.addEventListener("keydown", function (event) {
          if (event.key === "Escape") closeMenu();
        });
      }
    }

    var drawer = document.querySelector("[data-drawer]");
    var openBtn = document.querySelector("[data-drawer-open]");
    if (!drawer || !openBtn) return;

    var closeBtn = drawer.querySelector("[data-drawer-close]");
    var lastFocus = null;

    function focusables() {
      return all('a[href], button:not([disabled])', drawer);
    }

    function openDrawer() {
      lastFocus = document.activeElement;
      drawer.hidden = false;
      document.body.style.overflow = "hidden";
      openBtn.setAttribute("aria-expanded", "true");
      var f = focusables();
      if (f.length) f[0].focus();
    }

    function closeDrawer() {
      drawer.hidden = true;
      document.body.style.overflow = "";
      openBtn.setAttribute("aria-expanded", "false");
      /* Focus returns to the trigger, never to the page top (§10). */
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    openBtn.addEventListener("click", openDrawer);
    if (closeBtn) closeBtn.addEventListener("click", closeDrawer);

    all("a", drawer).forEach(function (link) {
      link.addEventListener("click", closeDrawer);
    });

    drawer.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeDrawer();
        return;
      }
      if (event.key !== "Tab") return;

      var f = focusables();
      if (!f.length) return;
      var first = f[0];
      var last = f[f.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }

  /* ── Tabs with full keyboard support ─────────────────── */
  function initTabs() {
    all("[data-tabs]").forEach(function (tabs) {
      var tabList = tabs.querySelector('[role="tablist"]');
      var triggers = all('[role="tab"]', tabs);
      if (!tabList || !triggers.length) return;

      function panelFor(trigger) {
        var id = trigger.getAttribute("aria-controls");
        return id ? document.getElementById(id) : null;
      }

      function activate(trigger, focus) {
        triggers.forEach(function (candidate) {
          var selected = candidate === trigger;
          var panel = panelFor(candidate);
          candidate.setAttribute("aria-selected", String(selected));
          candidate.tabIndex = selected ? 0 : -1;
          if (panel) panel.hidden = !selected;
        });

        if (focus) trigger.focus();
        track("brand_view_changed", {
          view: trigger.getAttribute("data-view") || trigger.id || ""
        });
      }

      triggers.forEach(function (trigger) {
        trigger.addEventListener("click", function () { activate(trigger, false); });

        trigger.addEventListener("keydown", function (event) {
          var current = triggers.indexOf(trigger);
          /* Arrow direction follows the writing direction. */
          var rtl = getComputedStyle(tabList).direction === "rtl";
          var next = current;

          if (event.key === "Home") next = 0;
          if (event.key === "End") next = triggers.length - 1;
          if (event.key === "ArrowRight") next = current + (rtl ? -1 : 1);
          if (event.key === "ArrowLeft") next = current + (rtl ? 1 : -1);

          if (next === current) return;
          event.preventDefault();
          next = (next + triggers.length) % triggers.length;
          activate(triggers[next], true);
        });
      });

      var initial = triggers.filter(function (trigger) {
        return trigger.getAttribute("aria-selected") === "true";
      })[0] || triggers[0];
      activate(initial, false);
    });
  }

  /* ── Prepared sample switcher ────────────────────────────
     Swaps between examples already present in the HTML. It
     never fabricates a result and never pretends to query a
     live source (§8.2, Master Plan §9). */
  function initPreparedSample() {
    all("[data-sample]").forEach(function (group) {
      var chips = all("[data-sample-request]", group);
      var panels = all("[data-sample-result]", group);
      if (!chips.length || !panels.length) return;

      function show(key, chip) {
        panels.forEach(function (panel) {
          panel.hidden = panel.getAttribute("data-sample-result") !== key;
        });
        chips.forEach(function (candidate) {
          candidate.setAttribute("aria-pressed", String(candidate === chip));
        });
        track("prepared_sample_changed", { sample: key });
      }

      chips.forEach(function (chip) {
        chip.addEventListener("click", function () {
          show(chip.getAttribute("data-sample-request"), chip);
        });
      });

      var initial = chips.filter(function (chip) {
        return chip.getAttribute("aria-pressed") === "true";
      })[0] || chips[0];
      show(initial.getAttribute("data-sample-request"), initial);
    });
  }

  /* ── Exclusive FAQ, keeping native <details> semantics ── */
  function initExclusiveDetails() {
    all("[data-exclusive-details]").forEach(function (group) {
      all("details", group).forEach(function (item) {
        item.addEventListener("toggle", function () {
          if (!item.open) return;
          all("details", group).forEach(function (other) {
            if (other !== item) other.open = false;
          });
        });
      });
    });
  }

  /* ── Carousel position, announced as text ────────────── */
  function initCardTracks() {
    all("[data-card-track]").forEach(function (track_) {
      var cards = Array.prototype.slice.call(track_.children);
      var statusId = track_.getAttribute("aria-describedby");
      var status = statusId ? document.getElementById(statusId) : null;
      var ticking = false;

      function update() {
        ticking = false;
        if (!cards.length || !status) return;

        var trackRect = track_.getBoundingClientRect();
        var centre = trackRect.left + (trackRect.width / 2);
        var closestIndex = 0;
        var closestDistance = Infinity;

        cards.forEach(function (card, index) {
          var rect = card.getBoundingClientRect();
          var cardCentre = rect.left + (rect.width / 2);
          var distance = Math.abs(cardCentre - centre);
          if (distance < closestDistance) {
            closestDistance = distance;
            closestIndex = index;
          }
        });

        status.textContent = (closestIndex + 1) + " / " + cards.length;
      }

      track_.addEventListener("scroll", function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(update);
      }, { passive: true });

      window.addEventListener("resize", update);
      update();
    });
  }

  /* ── Outbound CTA tracking ───────────────────────────── */
  function initTracking() {
    all("[data-track]").forEach(function (el) {
      el.addEventListener("click", function () {
        track(el.getAttribute("data-track"), {
          position: el.getAttribute("data-position") || "",
          lang: root.lang || ""
        });
      });
    });
  }

  function init() {
    initReveal();
    initFlowReveal();
    initArtMotion();
    initHeader();
    initTabs();
    initPreparedSample();
    initExclusiveDetails();
    initCardTracks();
    initTracking();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
