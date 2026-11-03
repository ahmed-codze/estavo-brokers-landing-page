/* /roi/ — "Cash or installments?" explainer calculator.
   Progressive enhancement only: the HTML ships the default example
   (EGP 8,000,000 · 20% cash discount · 10% down · 8 years) already
   computed, and the sliders stay hidden until this script runs.

   The maths mirrors the app's unit-models/utils/npv.ts
   (calculatePaymentPlanCashFlow + calculatePaymentPlanNpvComparison),
   simplified to no bulk payments, no plan discount and installments
   starting 3 months from today:
   - monthly rate = 1.19^(1/12) − 1 (fixed 19% a year, like the app)
   - installments are quarterly: n = round(months / 3)
   - down = round(price × dp%), installment = round((price − down) / n)
   - plan value today = round(down + Σ installment / (1 + r)^(3i))
   - cash price = round(price × (1 − cash%))
   - cash is better when plan value today > cash price (difference > 0). */
(function () {
  'use strict';

  var ANNUAL_RATE = 0.19;
  var fmt = function (n) { return Math.round(n).toLocaleString('en-US'); };

  function compute(price, cashPct, dpPct, years) {
    var months = years * 12;
    var monthlyRate = Math.pow(1 + ANNUAL_RATE, 1 / 12) - 1;
    var n = Math.max(1, Math.round(months / 3));
    var planPrice = Math.round(price);
    var down = Math.round(planPrice * (dpPct / 100));
    var inst = Math.round((planPrice - down) / n);
    var pv = 0;
    for (var i = 1; i <= n; i += 1) pv += inst / Math.pow(1 + monthlyRate, i * 3);
    var npv = Math.round(down + pv);
    var cash = Math.round(price * (1 - cashPct / 100));
    return {
      planPrice: planPrice,
      down: down,
      inst: inst,
      n: n,
      total: down + inst * n,
      npv: npv,
      cash: cash,
      difference: Math.round(npv - cash),
    };
  }

  var AR = {
    years: function (y) { return y === 1 ? 'سنة' : y === 2 ? 'سنتين' : y <= 10 ? y + ' سنين' : y + ' سنة'; },
    nword: function (n) { return n >= 3 && n <= 10 ? 'أقساط' : 'قسط'; },
    cash: 'الكاش أوفر',
    plan: 'التقسيط أوفر',
  };
  var EN = {
    years: function (y) { return y === 1 ? '1 year' : y + ' years'; },
    cash: 'Cash is better',
    plan: 'Installments are better',
  };

  Array.prototype.forEach.call(document.querySelectorAll('[data-ro-calc]'), function (calc) {
    var t = calc.getAttribute('data-lang') === 'ar' ? AR : EN;
    var q = function (sel) { return calc.querySelector(sel); };
    var inputs = {
      price: q('[data-ro-in="price"]'),
      cash: q('[data-ro-in="cash"]'),
      dp: q('[data-ro-in="dp"]'),
      years: q('[data-ro-in="years"]'),
    };
    if (!inputs.price || !inputs.cash || !inputs.dp || !inputs.years) return;
    var set = function (sel, text) { var el = q(sel); if (el) el.textContent = text; };
    var bar = function (key, pct) { var el = q('[data-ro-bar="' + key + '"]'); if (el) el.style.setProperty('--w', pct.toFixed(2) + '%'); };
    var result = q('[data-ro-result]');

    function update() {
      var price = Number(inputs.price.value);
      var cashPct = Number(inputs.cash.value);
      var dpPct = Number(inputs.dp.value);
      var years = Number(inputs.years.value);
      var r = compute(price, cashPct, dpPct, years);
      var cashBetter = r.difference > 0;

      set('[data-ro-out="price"]', fmt(price));
      set('[data-ro-out="cash"]', cashPct + '%');
      set('[data-ro-out="dp"]', dpPct + '%');
      set('[data-ro-out="years"]', t.years(years));
      set('[data-ro-years-txt]', t.years(years));

      set('[data-ro-verdict]', cashBetter ? t.cash : t.plan);
      set('[data-ro-diff]', fmt(Math.abs(r.difference)));
      set('[data-ro-total]', fmt(r.total));
      set('[data-ro-cashprice]', fmt(r.cash));
      set('[data-ro-npv]', fmt(r.npv));
      set('[data-ro-down]', fmt(r.down));
      set('[data-ro-n]', String(r.n));
      set('[data-ro-inst]', fmt(r.inst));
      if (t.nword) set('[data-ro-nword]', t.nword(r.n));
      if (result) result.setAttribute('data-verdict', cashBetter ? 'cash' : 'plan');

      var max = Math.max(r.total, r.cash, r.npv) || 1;
      bar('total', (r.total / max) * 100);
      bar('cash', (r.cash / max) * 100);
      bar('npv', (r.npv / max) * 100);

      /* Range fill for the slider track. */
      Object.keys(inputs).forEach(function (k) {
        var el = inputs[k];
        var p = ((Number(el.value) - Number(el.min)) / (Number(el.max) - Number(el.min))) * 100;
        el.style.setProperty('--fill', p + '%');
      });
    }

    Object.keys(inputs).forEach(function (k) {
      inputs[k].addEventListener('input', update);
      inputs[k].addEventListener('change', function () {
        if (typeof window.gtag === 'function') window.gtag('event', 'prepared_sample_changed', { page: 'roi', position: 'calc_' + k });
      });
    });
    calc.classList.add('is-live');
    update();
  });
}());
