# Knowledge extension documentation

Documentation pass: 2 October 2026. Scope: the bilingual static knowledge hub and articles under `guides/`. This is an ordinary extension of the incumbent identity, with no approved durable system change. This note records observed implementation; it does not establish a replacement design system. `PRODUCT.md` and `.impeccable/knowledge-surface.md` retain their respective product and Read-surface authority.

## Incumbent authority and palette

`assets/css/styles.css` remains the source for the incumbent visual identity: navy `--blue: #021d39`, purple `--purple: #33123b`, paper `--bg: #fafbfc`, warm surface `--off-white: #f4f4f0`, white, Cairo, and a `1152px` container. Its radius vocabulary includes `12px`, `20px` and `24px`, with navy-tinted shadows for the landing page's elevated components.

`content/knowledge.css` inherits that palette through local aliases: `--ink: #021d39`, `--accent: #33123b`, `--paper: #fafbfc`, `--surface: #f4f4f0`, `--white: #fff`, and `--max: 1152px`. Read-surface additions are muted text `#465568` and divider `#d9dfe5`. The knowledge surface is flat, using borders and warm panels rather than landing-page shadows. This is a surface-specific treatment, not a prohibition on the incumbent's shadows or gradients.

## Typography and hierarchy

Both languages use Cairo with a sans-serif fallback; generated documents request weights 400, 600 and 700. Desktop body is `400 17px/1.85`; mobile body is `16px/1.85`. Arabic prose has line-height `2`. Desktop h1 is `2.75rem`, line-height `1.35`, with `-.025em` tracking; Arabic article h1 is `2.5rem` with no tracking. Mobile h1 is `2rem`. Desktop h2/h3 are `1.6rem`/`1.2rem`, becoming `1.35rem`/`1.1rem` on mobile. The answer lead is `1.18rem/1.8`, reduced to `1.08rem` on mobile; bylines are `.85rem`, reduced to `.78rem`.

The hub has a single headline, introduction and topic links followed by ruled editorial lists. Articles lead with breadcrumbs, title, dated organizational byline and a direct answer before the contents/prose area. Prose is capped at `72ch`; sources, related reading and a specific Estavo action follow the answer and substantive content. Checklists, explicitly illustrative examples, source periods and limitations remain visible prose, rather than hidden interaction-dependent material.

## Layout, components and responsive behavior

Shell padding is `32px 28px 80px` inside the `1152px` container. The desktop article grid has a `230px` contents rail, a fluid prose column and `64px` gap. The rail is sticky at `30px`. At `900px`, the rail becomes `190px` with `30px` gap and the header action is hidden. At `680px`, the article becomes a column with `34px` gap, a static native collapsible contents list before the prose, and shell padding `25px 20px 48px`. Contents starts open in the generated HTML; the reader can collapse it without JavaScript.

The header is `94px` minimum height on desktop and `80px` on mobile. The existing transparent Estavo Brokers logo is reused. The reviewer-requested logo sizing correction is present in source: the brand container is `196px` wide on desktop and at most `140px` on mobile; its image fills the container with `height: 40px`, `object-fit: cover` and centered positioning. This describes the current source, not a new global logo rule.

Action links are navy, white-text anchors with `12px` corners, `12px 23px` padding and `48px` minimum height; hover changes to purple. Warm quote and product panels also use `12px` corners. Hub navigation indicators are now inline `24px` SVG arrows with `aria-hidden="true"`; RTL rotates them by 180 degrees. The reviewer-requested replacement of Unicode arrows is present in generated hub HTML.

Tables use semantic captions, headers and tabular numerals. Their local wrappers use `overflow-x: auto` and inline overscroll containment; cells retain minimum widths (`100px`, mobile `105px`) so the table can scroll within its frame. Source wrappers have no explicit `tabindex`; this pass does not claim a separately tested keyboard-scroll affordance for these frames.

## Routes and progressive behavior

The Arabic hub is `/guides/`; English is `/guides/en/`. Nine article slugs have parallel static `index.html` routes in each language: `sell-more-properties`, `find-developer-inventory`, `match-client-property`, `compare-payment-plans`, `property-pdf-offer`, `find-property-clients`, `archived-listing-evidence`, `developer-offer-evidence` and `property-price-evidence-september-2026`. The public evidence summary is `/guides/evidence/september-2026.json`.

Generated pages set `lang` and `dir`, canonical and reciprocal language alternatives, ordinary anchors and crawlable server-served content. JSON-LD describes the organization/site and relevant article, FAQ and breadcrumb content. Analytics and referral enhancement scripts are present, but article reading, contents anchors, language switching, FAQs and product links have a complete native HTML path without them.

Keyboard-oriented source behavior includes a skip link, `3px` purple `:focus-visible` outlines with `5px` offset on anchors and summaries, and native `details`/`summary` controls. Logical padding, alignment and RTL direction support both languages. Reduced-motion CSS removes smooth scrolling and button transitions. Print CSS removes navigation, rail and promotional/related blocks, simplifies prose layout and exposes table overflow. These are source observations; print output and assistive-technology behavior were not independently exercised in this documentation pass.

## Evidence checked and limits

Read `reference/document.md`, the extension finishing instructions in `reference/new-work.md`, and `reference/degraded/documenter.md` for the documentation contract. Checked `PRODUCT.md`, `.impeccable/knowledge-surface.md`, incumbent `assets/css/styles.css`, complete `content/knowledge.css`, route inventory, sampled generated English hub/payment-plan article and Arabic research article, and the generator's use of the knowledge stylesheet. Verified corrected logo rules and SVG arrow markup against current source.

Reviewed the existing `.impeccable/review/browser-checks.json`: English desktop hub/article at `1440px`, Arabic mobile hub/article at `390px`, matching body scroll widths, `94px`/`80px` header heights, and a recorded no-JavaScript payment-plan excerpt with three native details controls. Those records support the tested samples; they are not a claim that every route, browser, keyboard flow or table interaction was retested after the final correction. No additional visual loop or detector was run for this documentation handoff.

Pre-existing documentation drift: root `DESIGN.md` is absent. It was not created, and `.impeccable/design.json` was not synthesized, because this pass has no approved system change and its write boundary is this note only. Existing source remains visual authority. Local token aliases, a flatter Read composition and different responsive breakpoints are recorded as extension facts, not promoted into universal rules. No defect or reviewer refusal is canonized as incumbent identity.
