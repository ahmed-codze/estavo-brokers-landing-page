(function () {
  "use strict";

  var loader = document.currentScript;
  if (!loader) return;
  var assets = new URL("../", loader.src);
  var production = ["estavo-brokers.com", "www.estavo-brokers.com"].indexOf(window.location.hostname) !== -1;
  var endpoint = loader.dataset.endpoint || (production
    ? "https://api-brokers.estavo.space/api/public/support/chat"
    : "https://api-staging-brokers.estavo.space/api/public/support/chat");

  function loadAssistant() {
    if (document.querySelector('script[src*="/raghad.js"]')) return;

    var sharedStyle = document.createElement("link");
    sharedStyle.rel = "stylesheet";
    sharedStyle.href = new URL("css/chatbot-shared.css?v=20260918-chat-ui", assets).href;

    var assistantStyle = document.createElement("link");
    assistantStyle.rel = "stylesheet";
    assistantStyle.href = new URL("css/raghad.css?v=20260918-chat-feedback", assets).href;

    var assistantScript = document.createElement("script");
    assistantScript.src = new URL("js/raghad.js?v=20260921-knowledge", assets).href;
    assistantScript.dataset.endpoint = endpoint;
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
