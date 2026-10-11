# Estavo landing page

Static Arabic/English landing pages for Brokers and Sites. Publish the HTML and `assets/` directory through the site's existing hosting setup.

## Raghad support widget

Raghad appears on `index.html`, `en.html`, `website/index.html`, and `website/en.html`. The shared `assets/js/raghad.js` and `assets/css/raghad.css` use the page language, preserve the existing design, and keep the launcher above the bottom call-to-action bar.

All four routes use `assets/js/raghad-loader.js`, which enables guest access without sign-in. The public `estavo-brokers.com` and `www.estavo-brokers.com` hosts call `https://api-brokers.estavo.space/api/public/support/chat`; preview/staging hosts keep the staging API. Configure a local test API with the loader's `data-endpoint` attribute. The loader keeps the approved support link in sync with the API's `RAGHAD_SUPPORT_URL`.

Deploy the corresponding API change and its private FAQ resources first. The API needs `CLOUD_FLARE_AI_GATE_WAY` and `CLOUDFLARE_ACCOUNT_ID` (see the API release guide). **Never add model credentials to this repository or the browser.** No npm dependency is needed to serve the site; jsdom is used only for tests.

The conversation is kept in tab memory only, and refresh/new chat clears it. The API returns an encrypted, expiring conversation token; the widget never sends a client-authored assistant/system history. Model text is rendered as text, not HTML. Failed requests preserve the draft, and support contact stays available when the model is unavailable.

The main page's automatic promotional modal is suppressed while the support panel is open. New asset URLs carry a version query because the hosting rules cache CSS/JS for one year; bump that version on changes to these assets.

## Tests

```sh
npm ci --ignore-scripts
npm test
```

The interaction tests cover Arabic keyboard navigation, retries, expired conversation tokens, new-chat cancellation, safe message rendering, duplicate submissions, and all four page integrations. Backend behavior and setup are documented in the API repository's `docs/RAGHAD_SUPPORT.md`.

For a local page preview, serve this directory over HTTP. Override the loader's `data-endpoint` to your local API when testing sends; otherwise preview hosts target the staging API. Do not publish local mock servers or test credentials.
