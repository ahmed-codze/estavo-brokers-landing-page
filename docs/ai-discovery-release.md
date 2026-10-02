# Public broker knowledge release — 2 October 2026

## Content and evidence

Six original practical guides, two owner-authorized research case studies and one original market-evidence report are available in Arabic and English under `/guides/` and `/guides/en/`. Research studies are not customer testimonials. The report analyzes the September 30 additional collection; it is not a national price index or a forecast. Only aggregate metrics and selected public source URLs/hashes are published. Raw source files, customer/contact data, hidden inventory rows and internal support materials stay outside public assets.

Product statements follow the reviewed support package in the workspace (`docs/raghad`, including the September 23 correction). Specific references include brokers-001, brokers-009, brokers-046, brokers-067, brokers-100/101 and the distinction between Market and Sites in ai-004. Product features do not imply guaranteed leads or returns.

The evidence exporter checks summary counts against underlying observation counts and recurring groups. Public source files are linked, not redistributed. Source licensing and economic-price-date limitations remain visible in both languages.

## Rebuild and check

```sh
npm ci
npm run build:knowledge
npm run test:knowledge
python3 scripts/export_research_evidence.py ../estavo-roi-service/output/historical-prices-expanded-2026-09-30
npm test
```

The site remains static; no framework or build runtime is required in production. Keep `content/`, `scripts/`, `tests/`, `docs/`, node_modules and `.impeccable` out of the deployment manifest. The CSS filename is derived from its content hash. Only the current generated stylesheet should be deployed.

The existing website-referral suite has one pre-existing failure: it expects `website-referral.js?v=11`, while the unchanged website pages use `v=20260918-chat-ui`. Its other 13 checks pass. New content validation passes separately. Do not alter the deployed website-builder behavior merely to satisfy that stale version assertion.

## Search foundation

- All articles render complete text, sources, FAQs and links without JavaScript.
- Canonicals, reciprocal Arabic/English alternatives, social metadata and matching Article/Breadcrumb/FAQ markup are generated. Structured data does not guarantee AI selection or FAQ rich results.
- The sitemap includes 26 actual static pages; legacy product canonicals now point to their existing `.html` files rather than unresolved extensionless URLs.
- Existing menus and footers link the knowledge section. Signup links retain the existing referral handling and analytics account.
- Search crawlers inherit public access, while GPTBot and ClaudeBot training stay disabled.
- Google-Extended is allowed for public content to support Gemini grounding; this token also permits its covered Gemini training uses. It is independent of Google Search ranking.

## Publish and index

This landing repository currently has no GitHub Actions workflow. Push the reviewed source commit, then use an explicit, hash-checked static-file manifest to deploy to the existing landing web root. Back up changed files outside that root and verify pre-deploy hashes to avoid overwriting server drift. Preserve unrelated server content. Deploy assets before HTML and publish the sitemap after article files.

For IndexNow, generate the verification key outside the repository, deploy its `.txt` file at the site root, verify all live URLs, and run `scripts/submit_indexnow.py` with `INDEXNOW_KEY` supplied in the environment. Do not commit the key. HTTP 200 or 202 acknowledges receipt rather than indexing.

Owner-account follow-up: verify the domain and submit `/sitemap.xml` in Google Search Console and Bing Webmaster Tools, confirm inclusion in Google's generative AI features, and inspect CDN/WAF logs for verified crawler requests. Those account states cannot be inferred from robots.txt. Track referred trial registrations alongside search citations; no artificial rating or recommendation guarantee is included.

## Primary technical references

- https://developers.openai.com/api/docs/bots
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide?version=published
- https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended
- https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- https://www.indexnow.org/documentation
