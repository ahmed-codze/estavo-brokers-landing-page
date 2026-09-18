# Estavo landing page

Static Arabic/English landing pages for Brokers and Sites. Publish the HTML and `assets/` directory through the site's existing hosting setup.

## Raghad support widget

Raghad appears on `index.html`, `en.html`, `website/index.html`, and `website/en.html`. The shared `assets/js/raghad.js` and `assets/css/raghad.css` use the page language, preserve the existing design, and keep the launcher above the bottom call-to-action bar.

The widget calls the Laravel API at `https://api-brokers.estavo.space/api/public/support/chat`. Configure a different environment with the script's `data-endpoint` attribute. `data-support-url` is the approved human-contact link; keep it in sync with the API's `RAGHAD_SUPPORT_URL`.

Deploy the corresponding API change and its private FAQ resources first. The API needs `CLOUD_FLARE_AI_GATE_WAY` and `CLOUDFLARE_ACCOUNT_ID` (see the API release guide). **Never add model credentials to this repository or the browser.** No npm dependency is needed to serve the site; jsdom is used only for tests.

The conversation is kept in tab memory only, and refresh/new chat clears it. The API returns an encrypted, expiring conversation token; the widget never sends a client-authored assistant/system history. Model text is rendered as text, not HTML. Failed requests preserve the draft, and support contact stays available when the model is unavailable.

The main page's automatic promotional modal is suppressed while the support panel is open. New asset URLs carry a version query because the hosting rules cache CSS/JS for one year; bump that version on changes to these assets.

## Tests

```sh
npm ci --ignore-scripts
npm test
```

The interaction tests cover Arabic keyboard navigation, retries, expired conversation tokens, new-chat cancellation, safe message rendering, duplicate submissions, and all four page integrations. Backend behavior and setup are documented in the API repository's `docs/RAGHAD_SUPPORT.md`.

For a local page preview, serve this directory over HTTP. Override `data-endpoint` to your local API when testing sends; otherwise the widget targets the production API. Do not publish local mock servers or test credentials.
