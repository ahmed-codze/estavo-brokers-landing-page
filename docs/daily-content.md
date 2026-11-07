# Daily landing content

**Current status — live since 7 November 2026:** The home page (AR/EN) binds the daily edition **inside the approved cards only**: the Market card (three real unit types with price, area, beds, handover), the news card (launch ticker + headlines), the jobs card, and the six "from inside Estavo" stories (2 news, 2 launches, 2 jobs), plus the dated labels. No element is added or removed; a slot without fresh data keeps its authored example. The developers card changes only for developers that have a logo. Service pages are unchanged. Binding runs only when the publisher passes `LANDING_CACHE_DIR`, so a plain `npm run build` (and the committed HTML) stays the approved static version. Do not restore the rejected "Estavo selections" sections. The publisher copies the whole checkout (minus `.git`, `node_modules` and private state) and its signature includes the git HEAD, so a `git pull` triggers a rebuild on the next timer run (the server also has a post-merge hook that publishes immediately).

**Production layout (new-server):** API pool initialized 7 Nov 2026 (`storage/app/landing-content/` in `estavo-brokers-api-app-1`; hourly at :17). Landing: checkout `/home/codze/public/estavo/estavo-brokers-landing-page`, state `/srv/estavo/landing-editions`, nginx `root` → `/srv/estavo/landing-editions/current`, systemd `estavo-landing-daily.timer` (:27 Cairo, hourly retries).

Implemented 4 November 2026. The marketing surface is 32 pages: Arabic/English home plus 15 service routes. This work is prepared and verified locally; it does not change the production checkout, web-server root or installed production timers.

## Publication plan and contract

1. The API builds one bilingual edition for each **Africa/Cairo calendar day**, off the HTTP request path.
2. A static-host job downloads that small edition and its thumbnails once, validates them, and renders them into the HTML.
3. All 32 pages and their assets are built in a separate release directory. One atomic symlink rename publishes the completed release. Browsers make **zero daily-feed API calls**.
4. Hourly retries recover missed runs. Once today's edition exists, neither the API nor the static job reselects content. Dates are absolute, not misleading “today” labels on old news.

| Content | Daily maximum | Selection / public boundary |
| --- | ---: | --- |
| Projects | 3 | Projects corresponding to selected units |
| Unit models | 3 | Recently updated, popular when measured, then shuffled daily rotation |
| Developers / logos | 6 | Recently updated, popular when measured, then shuffled daily rotation |
| News summaries | 4 | Last 7 days; not pulled; approved articles and active sources |
| Launches | 3 | Published within 90 days; no private or non-publishable linked projects |
| Jobs | 4 | Approved Egyptian jobs with active source occurrences; published already and open through the edition's day |
| Game teaser | 1 | One prompt from a fixed 12-question subset; no answers or player data |

The inventory pool is initialized **once**, with at most 24 publishable projects, 24 unit models and 24 associated developers. It is persisted privately and never automatically refilled. Recency is relative to this pool. Popularity uses an existing, fresh 90-day aggregate, not raw visitor events; absent measurements never produce a “popular” label. The random part uses a deterministic shuffled cycle, shared by all visitors and languages. Game teasers do not repeat on adjacent days.

Published project permission, active public inventory, publication dates, listing status, soft deletion and brokerage ownership are checked again at build time. Revoking an item removes it from future editions without replacing its pool membership from the wider catalogue.

## Public API

- `GET https://api-brokers.estavo.space/api/public/landing-content`
- `GET https://api-brokers.estavo.space/api/public/landing-content/media/{sha256}.webp`

These routes are implemented in the sibling API repository. They require no account, API key, browser identity or cookie. The response is the same for every visitor. **Every query parameter is rejected**: no search, IDs, pagination, language, date, seed, size or origin URL. There is no history endpoint.

The JSON includes `schema_version`, `snapshot_date`, `timezone`, `generated_at`, `expires_at`, `revision` and the seven bounded arrays. It carries explicitly selected public fields, never serialized models, personal contacts, account tokens, full article bodies, game answer banks, private listing notes, or original media URLs. Detail links lead into Estavo; they do not grant access to other API resources.

Limits: 64 KiB JSON, at most nine WebP derivatives, each at most 100 KB; photos at most 560×360 and logos 160×160. The API only serves hashes listed in the current manifest. Derivatives are generated offline from an exact hostname allowlist, with public-IP validation, DNS pinning, no redirects, bounded downloads and bounded decoded image dimensions. Missing images become text monograms.

A shared 60 requests/minute/IP limiter covers the manifest and images. Responses have ETags/304 support and public cache headers. The manifest TTL ends at the next Cairo midnight at the latest; stale editions use a short TTL. Keep the API behind its existing trusted ingress. Apply an edge request-rate rule too if the API is exposed to substantial unauthenticated traffic; application throttling alone is not a volumetric traffic filter.

**Public means copyable.** A caller can save each day's selection and its small images. The fixed pool prevents this endpoint from eventually walking the full developer/project catalogue; it does not make already published material secret. Replacing the pool expands the cumulative public set and is an editorial operation. News and jobs can naturally accumulate over time. CDN/browser copies also survive until their TTL or explicit purge.

## Page content and usability

`tools/daily/render.js` binds the same edition to native catalogue/product scenes, homepage destination cards and its daily board, developer/logo examples, launch/news examples, game prompts, and an accessible content card on **every** page. Bilingual text comes from the same records; fallback source text is isolated with `bdi`. The Arabic game prompt remains marked Arabic on the English page.

Calculated payment-plan diagrams, simulated AI replies, invented client actions, sales-contact examples and API syntax remain **labelled explanatory examples**. Attaching a selected real project's name to a fictional price, payment plan, sales representative or AI answer would be false. These teaching surfaces remain separate from the dated public selection. Brand marks and product names do not rotate as though Estavo were a different company each day.

The implementation keeps existing product copy, CTAs, route destinations, referral attribution, layout direction, reduced-motion and no-JavaScript behavior. New real-data links use `data-keep-path` and explicit click events. Images are local, dimensioned, lazy-loaded and content-addressed; one image URL is reused throughout the site. No extra client-side fetch, spinner or content swap is introduced.

The local database used for verification contains real project images and developer logos, but no news, launch or careers projection. Those areas therefore show honest empty states in the current local edition. Production will populate them only when approved records exist. No invented vacancies, launch announcements or market headlines are substituted.

## Authoring and local commands

- Home source: `tools/home/index.html` and `tools/home/en.html`.
- Service source: `tools/pages/{route}.{ar,en}.html`.
- Shared page generation: `tools/build-pages.js`.
- Private daily cache: `.cache/landing/current.json` (ignored by Git).
- Selected public thumbnails: `assets/daily/{sha256}.webp`.

Use Node 22.12+ and `npm ci --include=dev`; jsdom is a **build/test** dependency, not a browser dependency.

```sh
# Production source, with a last-good fallback:
npm run daily:refresh
npm run build
npm test
node tools/qa.js

# Isolated clone API on port 81:
node tools/refresh-daily-content.js --local
npm run build

# Exercise the complete atomic pipeline locally:
node tools/publish-daily-edition.js --local
```

Serve the repository for normal local preview, or `.daily-releases/current` to inspect the atomic release. `--local` only allows `http://127.0.0.1:81`; an arbitrary endpoint override is intentionally unavailable. Do not serve the state-directory parent: it contains a private cache and rollback releases.

A missing, corrupt, future or >72-hour-old cache produces empty selection states when building. The source templates' historical headlines are never the no-cache fallback. Explicit scenarios remain labelled examples. The source copy is never rewritten by the scheduled production publisher.

## Production activation

Production remains on `main` in each repository. Merge and review both branch histories; preserve production hotfixes and server-local edits. These instructions are a deployment runbook, not evidence that production was deployed.

1. Deploy the API code. Initialize the private bounded pool using `php artisan landing:content-build --initialize-pool`, review `storage/app/landing-content/pool.json`, and verify the manifest and a selected image without credentials. The API's existing Laravel scheduler will run `landing:content-build` at **:17 every hour**; the command itself publishes at most once per Cairo day. Do not configure a second Laravel scheduler.
2. Deploy the landing source and its build dependencies to the static build host. The example unit uses `/srv/estavo/landing-source` and user `estavo-landing`; adapt these paths/user to the real host. Create a writable state directory `/srv/estavo/landing-editions`, outside the public root.
3. Run `LANDING_STATE_DIR=/srv/estavo/landing-editions node tools/publish-daily-edition.js`. Require a successful complete edition before switching the existing vhost's document root to `/srv/estavo/landing-editions/current`. Preserve PHP handlers, onboarding proxies, TLS, redirects and other existing vhost rules. See `deploy/nginx/landing-daily-cache.conf` for the small cache/root additions, not a replacement vhost.
4. Install the provided `deploy/systemd/estavo-landing-daily.service` and `.timer` after adjusting paths. The timer runs at **:27 Africa/Cairo**, with hourly retries and catch-up after downtime. It cannot regenerate a successful day's content. `--rebuild` rebuilds page code with the same cached data, for a code deployment.
5. Verify `edition.json`, the API date, all 32 page meta dates, selected-image loading and the next timer firing. Alert if the edition is more than one day old, the job exits nonzero, or its output reports `last-good`/`unavailable`. Production activation was **not performed in this change**.

The API default `LANDING_CONTENT_ENABLED=true` serves only a prebuilt file; without initialization it returns 503 and never queries/generates on demand. `false` disables both public routes and scheduled generation. Use the API application user's existing storage ownership; never make private pool/cache directories web-accessible.

## Failure, withdrawal and rollback

- Network, schema, oversized JSON or thumbnail failure: keep the prior complete edition for up to 72 hours, with its original date. After that, a scheduled build publishes empty states. A failed page build never moves the public symlink.
- No qualifying news/jobs/launches: omit records and show an empty state, not an old sample disguised as current.
- Locks cover concurrent API builds, static downloads and static publication. A killed local process can leave a `.refresh-lock` or `.publish-lock`; check that no process is running before removing that **specific** lock. Never flush shared Redis.
- Three completed releases are retained privately. Roll back by atomically pointing `current` at a previous completed release. Do not expose the parent as a browsable archive. Referenced media is copied into each release; the private media cache prunes unreferenced derivatives after seven days.
- Urgent withdrawal is an exception to daily stability. Disable the API feed, remove only its `storage/app/landing-content/current.json`, remove only the static host's `cache/current.json`, and rebuild the static release into empty states. Purge the specific public manifest/HTML/media CDN URLs if necessary. Do not clear application-wide caches, media storage or user data. Previously saved public content cannot be recalled.

## Validation recorded locally

- 118 landing tests, including schema/XSS, bounded downloads, missing images, daily caching, Cairo/DST dates and all-page data coverage.
- 16 focused API tests / 156 assertions: unauthenticated identical responses with zero catalogue queries, 304s, 400/404/429/503 behavior, bounded selection, private/unpublished/sold inventory exclusion, non-refilling pool, publication/withdrawal policy, valid jobs, failure preservation and nonrepeating teaser rotation.
- Static QA: 32 pages, zero failures.
- Browser QA: 480 checks across 320, 360, 390, 1280, 1440, 1512 and 1728 pixels, normal/reduced motion and JavaScript disabled; zero horizontal-overflow failures. Desktop/mobile and deeper section screenshots inspected locally.
- Actual clone API: 200 without credentials, no cookies, ETag and rate-limit headers; complete static publication then unchanged repeat.

Reference behavior: [Laravel scheduling](https://laravel.com/framework/docs/12.x/scheduling), [HTTP cache directives](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control), and [OWASP SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).
