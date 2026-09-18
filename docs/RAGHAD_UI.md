# Raghad UI

The public support widget uses the existing Brokers chatbot presentation system. `assets/css/chatbot-shared.css` is generated from the actual rules in `estavo-brokers/src/index.css` and color tokens in `src/shared/theme/colors.ts`. It reuses workspace surfaces, composer surface, message bubbles, opening motion, and palette. The matching lightweight header/composer uses the normal chatbot icon paths. Raghad retains its supplied portrait and support identity.

`ChatWindow.tsx` cannot be imported directly into this static page: it depends on React routing, translations, account credits, property selectors, PDF operations, and application hooks. The landing adapter avoids those dependencies; it does not claim to use the same React component.

To refresh the shared styles from the sibling Brokers checkout (Node 22+):

```sh
node --experimental-strip-types scripts/sync-chatbot-theme.mjs
npm test
```

Commit the generated CSS so standalone deployments need no sibling repo or Node build. Load it before `raghad.css`. The source fingerprint identifies the upstream input. Do not hand-edit generated CSS.

## Interaction behavior

- Approved credits/support URLs render as safe anchors. Arbitrary model HTML remains plain text. Both referral scripts exempt the widget so destination links are not rewritten to signup.
- 429 responses honor Retry-After seconds or HTTP-date, show local retry time, and disable submission until then. Missing timing uses a 60-second client cooldown; the server still decides whether the next request is allowed. New chat does not reset a known cooldown.
- New chat requires confirmation only when a draft/thread exists. Cancel and Escape preserve it. Confirm aborts pending work; late replies cannot repopulate the reset thread.
- In-widget language switching preserves in-memory state. Explicit same-origin landing-language navigation uses a one-use sessionStorage handoff, consumed/removed on arrival and accepted for 60 seconds only. It is bounded and never uses localStorage or analytics. If browser storage fails, navigation is stopped and the in-widget language control is offered. Ordinary refresh still starts a new in-memory thread.
- Compact layouts use visualViewport dimensions/offsets, keep controls reachable, and place errors/retry inside the scrollable conversation. Physical mobile keyboard behavior still needs device validation.
- Supporting text is 12px+ and primary controls/Privacy have at least 44px touch targets.

## Validation and release

Run `npm test`; the suite includes transport safety, cooldowns, reset cancellation, both language paths, and referral integration. `tmp/raghad-ui-preview.py` in the workspace is a local-only browser fixture server, never a production asset. Use it for deterministic long answers/errors without paid requests.

The API remains Laravel → Cloudflare AI Gateway → OpenAI BYOK. This UI release changes no provider or knowledge settings. Publish the changed HTML, both referral scripts, widget JS/CSS, and generated shared CSS to the existing server root; purge the exact landing and asset URLs. Preserve other site files.
