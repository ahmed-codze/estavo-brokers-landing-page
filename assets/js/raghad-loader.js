(function () {
  "use strict";

  var disabledHosts = ["estavo-brokers.com", "www.estavo-brokers.com"];
  if (disabledHosts.indexOf(window.location.hostname) !== -1) return;

  function loadAssistant() {
    if (document.querySelector('script[src*="/raghad.js"]')) return;

    var sharedStyle = document.createElement("link");
    sharedStyle.rel = "stylesheet";
    sharedStyle.href = "assets/css/chatbot-shared.css?v=20260918-chat-ui";

    var assistantStyle = document.createElement("link");
    assistantStyle.rel = "stylesheet";
    assistantStyle.href = "assets/css/raghad.css?v=20260918-chat-feedback";

    var assistantScript = document.createElement("script");
    assistantScript.src = "assets/js/raghad.js?v=20260921-knowledge";
    assistantScript.dataset.disabledHosts = disabledHosts.join(",");
    assistantScript.dataset.endpoint = "https://api-staging-brokers.estavo.space/api/public/support/chat";
    assistantScript.dataset.supportUrl = "https://wa.me/201069528393";

    document.head.append(sharedStyle, assistantStyle);
    document.body.append(assistantScript);
  }

  if ("requestIdleCallback" in window) {
    window.requestIdleCallback(loadAssistant, { timeout: 2500 });
  } else {
    window.setTimeout(loadAssistant, 1200);
  }
})();
