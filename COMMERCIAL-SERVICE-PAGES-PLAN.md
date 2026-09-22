# Estavo Commercial Pages Plan

Status: approved information-architecture direction for the next content and design pass  
Updated: 19 September 2026

This plan follows the commercial model confirmed by the product owner: **Estavo has two main products**.

1. **Estavo Market** — the free broker-facing market product.
2. **Estavo Sites** — the branded website product, supported by several focused commercial pages.

The homepage introduces both products. Every later page must clearly belong to one of them and lead to the correct product action.

The supplied FAQ documents are product-source material, not publish-ready instructions or copy. Exact numbers, prices and capabilities still pass through the claims gate in this document before publication.

---

## 1. Final product architecture

```text
Estavo homepage
├── Estavo Market
│   └── One detailed commercial page
│       ├── All market data
│       ├── Data collection and updates
│       ├── Search and comparison
│       ├── Brokers AI
│       ├── Branded PDF offers
│       └── Try free → brokers.estavo.space
│
└── Estavo Sites
    ├── Website for freelance brokers
    ├── Website for brokerage companies
    ├── AI for your clients
    ├── Meta integration
    └── 7,000 brokers sell your properties
        └── Every primary CTA → estavo-brokers.com/website/
```

This replaces the previous assumption that data, updates, AI, marketing and listings are separate top-level products.

---

## 2. Route plan

| Product family | Commercial page | Recommended route | Primary destination |
|---|---|---|---|
| Overview | Homepage | `/` and `/en.html` | Routes visitor to Market or Sites |
| Estavo Market | Market for brokers | `/market/` | `https://brokers.estavo.space/go/?ref=default-landing-page-market` |
| Estavo Sites | Website for freelancers | `/websites/` | `/website/` |
| Estavo Sites | Website for companies | `/enterprise/` | `/website/` |
| Estavo Sites | AI for clients | `/ai/` | `/website/` |
| Estavo Sites | Meta integration | `/meta/` | `/website/` |
| Estavo Sites | Broker network / property distribution | `/listings/` | `/website/` |

### Secondary routes

The following routes can continue to exist for SEO, support or proof, but they are not separate products:

- `/marketing/`: buyer activity and follow-up context inside Estavo Sites.
- `/pricing/`: commercial details across Market credit features and Sites additions.
- `/examples/`: prepared demonstrations.
- `/insights/`: editorial market information, linked back to Estavo Market.
- `/integrations/`: custom Data + AI integration for customers keeping an existing platform; presented as a separate enterprise service, not a third main product.

### Routes to consolidate

- `/data/` must no longer behave like an independent product page. Its public data/update story belongs on `/market/`.
- Any homepage section about market information, developers, projects, units, payment plans, data collection or updates must link to `/market/` or directly to its free trial CTA.
- Do not send broker-market visitors into a city-subscription story intended for Estavo Sites.

---

## 3. Conversion rules

### Estavo Market

All primary actions use free, immediate language:

- **جرّب Estavo Market مجانًا**
- **ابدأ البحث مجانًا**
- **افتح السوق مجانًا**
- **Try Estavo Market free**
- **Start searching free**

Every one of these actions goes to the configured `brokers.estavo.space` Market referral URL. Preserve the referral origin so `assets/js/referral.js` can carry attribution.

Do not route these CTAs to a contact form, pricing page or general product explainer.

### Estavo Sites

Every primary action across the five Sites commercial pages goes to:

```text
https://estavo-brokers.com/website/
```

Use action-specific labels while preserving the same destination:

- **اعمل موقعك مجانًا** / **Create your website free**
- **ابدأ موقع شركتك** / **Start your company website**
- **فعّل AI لعملاء موقعك** / **Add client AI to your website**
- **اربط موقعك بـ Meta** / **Connect your website to Meta**
- **اعرض وحداتك قدام شبكة البروكرز** / **Put your properties in front of the broker network**

The destination is shared because these capabilities start with creating/configuring an Estavo Site. The page explains the motivation; `/website/` performs the action.

Secondary links may explain pricing, scope or an alternative integration. They must never visually compete with the primary product action.

---

## 4. Homepage routing plan

The homepage should make the two-product distinction obvious before showing their capabilities.

### Hero and first decision

Lead with the parent Estavo promise: the Egyptian real-estate market under the customer's name,
supported by data, sales and marketing. The hero's primary action creates a website; the parallel
action opens the market free. Follow the proof strip with a connected marketing-network argument:
developers, units, resale, brokers and market news working through Estavo. Immediately follow that
illustration with market changes/updates, then broker-network distribution. The later services
directory exposes six concrete routes while preserving the two-product commercial model:

- **Estavo Market:** explore and work with the market free.
- **Your website:** present and activate the market under the customer's name.
- **Client AI:** explain AI for website visitors separately.
- **Meta connection:** explain the marketing connection separately.
- **Market data and units:** route into the Market data proposition.
- **Market news and updates:** route into insights and Market updates.

The hero visual may still show the maintained data foundation feeding both destinations, but the
headline should describe Estavo itself rather than read like a product selector. Keep the compact
Market-versus-website conversion choice later in the page; do not headline it with a vague question.

### Sections that route to Estavo Market

The following homepage arguments all belong to `/market/`:

- all market information in one place;
- developers, projects, units, prices and payment plans;
- collecting information from fragmented sources;
- Estavo’s data organization and update process;
- searching from a real client request;
- comparing projects, units or payment plans;
- Brokers AI helping the broker work the request;
- creating a branded PDF offer;
- market news or data-driven analysis when the conversion action is “use the market.”

Each section can have its own CTA wording, but the conversion should remain “try/open Estavo Market free.”

### Sections that route to Estavo Sites

The following homepage arguments belong to the Sites family:

- present the same data under your own name;
- create a personal broker website;
- create a brokerage company website;
- let website visitors ask a client-facing AI;
- understand what a website visitor viewed or explicitly requested;
- connect permitted website events to Meta;
- add primary/resale properties and distribute them to brokers.

Homepage links may go to the relevant explanation page. The primary CTA on that page then goes to `/website/`.

### Remove the generic “many products” mental model

Do not present Market, website, AI, Meta, listings and integrations as six equal product cards. Use this hierarchy:

1. Choose **Market** or **Sites**.
2. Inside Sites, explore the capability relevant to the visitor.

---

## 5. Estavo Market commercial page

Route: `/market/`  
Audience: freelance brokers, salespeople and brokerage teams  
Source material: `Estavo_Brokers_FAQ.docx` and the Brokers AI portions of `Estavo_AI_FAQ_AR_EG_RTL.docx`

### Purpose

This one page must explain the complete free broker-market proposition. Separate pages for “data,” “updates” or “Brokers AI” would fragment the product and weaken the immediate free trial.

### Proposed hero

Arabic direction:

> السوق اللي محتاجه لطلب عميلك. مجانًا وفي مكان واحد.

English direction:

> The property market for your next client request. Free in one place.

Lead: browse organized project and unit information, compare the details that matter and use the broker tools when needed.

Primary CTA: **جرّب Estavo Market مجانًا / Try Estavo Market free**

### Section sequence

1. **The market, organized for the broker**
   - Developers, areas, projects, unit types, prices and payment plans where available.
   - Explain that browsing and ordinary market use are free.

2. **Instead of searching through scattered files**
   - WhatsApp updates, developer PDFs and messages converge into one searchable market surface.
   - Avoid dismissing those sources; the value is organization and speed of use.

3. **How Estavo collects and maintains the information**
   - Show source intake → review/structure → publication/update.
   - Describe the process honestly without “real-time” or universal-completeness claims.

4. **Start with the client request**
   - Area, budget, unit type, delivery and payment preference.
   - Exact matches versus clearly labelled alternatives.

5. **Compare what decides the choice**
   - Project and payment trade-offs, not a universal winner.
   - Final price/availability confirmation remains necessary.

6. **Brokers AI inside the Market experience**
   - Natural Arabic, English or mixed request.
   - Clarification when criteria are missing.
   - Grounded summaries, comparisons and draft replies.
   - Human review remains part of the workflow.

7. **Branded PDF offers**
   - Client-ready output with the broker’s name and contact details.
   - Not an official quotation or developer contract.

8. **What is free and what uses credits**
   - Free market browsing is the lead message.
   - AI/PDF credit details appear as optional product tools, after validation.

9. **FAQ**
   - Is Market free?
   - Is it a CRM?
   - Does it replace the broker?
   - Is every project included?
   - Are prices and availability real-time?
   - What do credits apply to?
   - Is the PDF an official developer document?

10. **Close**
   - Repeat one action: try Estavo Market free.

### Art direction

Build one wide broker workspace rather than feature cards:

```text
fragmented inputs → maintained Market data → client request → comparison → AI/PDF output
```

The product screen is the hero. The process of collection and maintenance appears later as its own connected editorial diagram. Mobile reduces the workflow to request → shortlist → offer without shrinking desktop UI.

### Link migration

Move or redirect these stories toward `/market/`:

- current `/data/` homepage links;
- market-update section links;
- Brokers AI links intended for salespeople;
- insights/analysis CTAs whose action is to use the market.

---

## 6. Estavo Sites family

Every page below explains one reason to create an Estavo Site. They share a common Site foundation but need different commercial arguments and hero scenes.

### Shared Sites foundation

All five pages can rely on these shared truths after validation:

- the customer-facing experience carries the broker’s or company’s identity;
- the site can present selected market data and the customer’s own properties;
- the experience supports mobile and bilingual use;
- the customer controls contact details and WhatsApp destination;
- the admin supports site/property management and relevant buyer context;
- optional capabilities start from the Estavo Site setup flow.

Do not repeat the full foundation on every page. Each page needs one short “Built on Estavo Sites” bridge and a consistent final CTA.

---

## 7. Website for freelance brokers

Route: `/websites/`  
Primary CTA: `/website/`

### Why it exists

A freelancer has a personal reputation but often sends clients links from developer sites, portals or social accounts where their own name disappears. This page sells one professional destination carrying their identity, selected work and direct contact.

### Proposed hero

> موقع عقاري باسمك. بدل ما تبعت عميلك لمكان عليه منافسينك.  
> A property website under your name—not a link that sends your buyer elsewhere.

CTA: **اعمل موقعك مجانًا / Create your website free**

### Sections

1. Your name, logo, colors, contact details and WhatsApp.
2. One link for projects, primary units and resale listings.
3. Select Estavo market data or add/manage your own properties.
4. Let buyers browse before being asked for contact details.
5. Add Client AI as the site grows.
6. See buyer context when a visitor becomes a lead.
7. Hosting, Estavo subdomain and custom-domain options.
8. FAQ: free base, ownership, mobile, language, inventory responsibility, custom domain and existing social channels.

### Art direction

One personal-brand setup flows into a live brokerage website and a buyer contacting the broker. The browser frame matters here because the website is the product. Use a personal broker identity, not a fictional enterprise dashboard.

---

## 8. Website for brokerage companies

Route: `/enterprise/`  
Primary CTA: `/website/`

### Why it exists

The company decision is different from the freelancer decision. A brokerage needs one company identity, shared inventory, managed market data, team access, buyer tools and an agreed operating scope.

### Proposed hero

> موقع شركتك، وداتا السوق وفريقك على نفس الأساس.  
> Your brokerage website, market data and team on one shared foundation.

CTA: **ابدأ موقع شركتك / Start your company website**

### Sections

1. Company brand and customer-facing property experience.
2. Cities, projects and company inventory in one governed catalogue.
3. Roles for owners, admins and salespeople according to actual supported permissions.
4. Client AI on the website and context handed to sales.
5. Meta connection for the company-owned account.
6. Resale distribution and commission control.
7. Existing platform alternative: cross-link to `/integrations/`.
8. Scope and commercial proposal for company-specific needs.
9. FAQ: company versus individual site, users/roles, existing CRM/site, branding, data responsibility and pricing basis.

### Art direction

Show one company system: branded public website at the center, with an inventory/admin rail and a team handoff. Avoid turning the figure into six unrelated service icons.

---

## 9. AI for your clients

Route: `/ai/`  
Product family: Estavo Sites  
Primary CTA: `/website/`

### Why it exists

This page is specifically about **Client AI on the customer’s Estavo Site**. Brokers AI belongs on the Estavo Market page. Management AI can appear as a supporting/future company capability only after product approval; it is not the main proposition here.

### Proposed hero

> AI يساعد عميلك يدور ويسأل ويقارن على موقعك إنت.  
> AI that helps buyers search, ask and compare on your own website.

CTA: **اعمل موقعك وفعّل الـ AI / Create your site and add AI**

### Sections

1. More than a generic live-chat box.
2. Uses only the projects and units allowed on that website.
3. Understands a natural request: area, budget, unit type and payment preference.
4. Asks for missing criteria instead of inventing them.
5. Compares available options and clearly identifies alternatives.
6. Does not force a lead form before helping.
7. Hands the conversation to WhatsApp or the sales team when wanted.
8. Carries the site’s brand, language and approved tone controls.
9. Explains missing information, final confirmation and human responsibility.
10. FAQ: data scope, language, branding, mistakes, availability, human handoff and usage model.

### Art direction

Keep the AI visibly inside a brokerage website. Show a buyer question, one clarification and matching results from that site’s allowed inventory. Do not use the Estavo mark as the customer-facing chat identity and do not show access to all Market data.

---

## 10. Meta integration for Estavo Sites

New route: `/meta/`  
Product family: Estavo Sites  
Primary CTA: `/website/`

### Why it exists

This page explains how permitted activity on an Estavo Site can become structured signals for the customer’s own Meta account. It is not a general marketing page and Estavo is not positioned as a media-buying agency.

### Proposed hero

> اربط رحلة العميل على موقعك بحساب Meta بتاعك.  
> Connect the buyer journey on your website to your own Meta account.

CTA: **اعمل موقعك واربط Meta / Create your site and connect Meta**

### Sections

1. Property context beyond a generic page view.
2. Permitted events: viewed project, selected area, comparison or submitted contact—only where implemented.
3. Customer ownership of Meta Business, dataset/pixel and Ad Account.
4. Existing media buyer or agency can remain in control.
5. Audiences based on transparent property context, not secret “high-intent” scoring.
6. Ad creation from Estavo only if the live workflow is confirmed.
7. Customer chooses audience and budget; Estavo does not spend autonomously.
8. No guarantee of lead volume, sale or campaign improvement.
9. Privacy, consent, permissions, retention and deletion.
10. FAQ: account ownership, existing pixel/agency, required setup, data sent, budget control and supported ad platforms.

### Art direction

Show one Estavo Site sending permitted, named property events through a visible consent/permission gate into a customer-owned Meta surface. Meta color appears only in its mark/interface. Do not use fake campaign metrics.

---

## 11. 7,000 brokers sell your properties

Route: `/listings/`  
Product family: Estavo Sites  
Primary CTA: `/website/`

### Why it exists

This page sells a clear distribution advantage: add a resale property to the broker’s own site and make it available to the Estavo Brokers network with the commission controlled by the property owner/broker.

The “7,000 brokers” number is central to the planned proposition and was confirmed by the product owner on 22 September 2026.

### Proposed hero

> وحدتك على موقعك. وقدام 7,000 بروكر يساعدوك تبيعها.
> Your property on your website—and in front of 7,000 brokers who can help sell it.

If the count is not validated, use:

> وحدتك على موقعك. وقدام شبكة بروكرز أوسع.  
> Your property on your website—and across a wider broker network.

CTA: **اعمل موقعك واعرض وحداتك / Create your site and list your properties**

### Sections

1. Add the property once with clear details, images, status and contact.
2. Publish it on the broker’s branded Estavo Site.
3. Make eligible resale inventory visible to the Estavo Brokers network.
4. The customer sets the displayed commission.
5. Estavo distributes the opportunity; it does not take over the deal.
6. Update or remove the property when its status changes.
7. Optional managed data-entry service after price validation.
8. No guarantee of sale; the value is additional broker reach.
9. FAQ: eligibility, primary/resale distinction, commission, ownership of the lead/deal, updates, fees and network size.

### Art direction

Use one property record as the source. It branches to the owner’s branded website and a controlled broker-network view. Commission remains attached to the network version. The property owner stays visually central; Estavo is the distribution layer.

---

## 12. Supporting pages and redirects

### `/data/`

Preferred direction: consolidate its strongest content into `/market/`, then use either:

- a permanent redirect to `/market/`; or
- a short SEO-support page whose only primary action is “try Estavo Market free.”

Do not keep a parallel data product story.

### `/marketing/`

Keep only if buyer context needs a dedicated SEO/support page. Frame it as a capability of Estavo Sites and route its primary CTA to `/website/`. Its Meta section should link to `/meta/`.

### `/insights/`

Keep as editorial proof. Market-use CTAs go to the free Estavo Market product.

### `/pricing/`

Organize pricing under the two-product hierarchy:

- Estavo Market: free access first; optional credit tools second.
- Estavo Sites: free site foundation and approved optional/paid additions.
- Custom integration: scoped separately.

### `/examples/`

Group prepared examples under two tabs: Market and Sites. Each example keeps its product’s destination.

### `/integrations/`

Keep as a separately scoped enterprise service for organizations that already have a platform. It should not appear as a third main product alongside Market and Sites.

---

## 13. Commercial and claims validation gate

These facts appear in the supplied documents but require current owner confirmation before publication:

| Claim | Confirm with | Treatment |
|---|---|---|
| Estavo Market is free | Product + finance | Define which browsing/search/comparison capabilities are free and whether login limits apply. |
| 40 free credits every week | Product + finance | Confirm eligibility and reset behavior. |
| 2 credits per Brokers AI message | Product + finance | Confirm current charging logic. |
| 3 credits per PDF offer | Product + finance | Confirm generation/retry behavior. |
| Estavo collects/maintains market data | Data operations | Approve source/process wording; do not imply universal official status. |
| Contracts with developers | Legal/commercial | Approve the exact public formulation. |
| First Sites city is free continuously | Product + finance | Confirm account eligibility and included data. |
| Site, hosting and server are free indefinitely | Product + finance + operations | Define fair-use and suspension/support boundaries. |
| Custom domain prices | Finance | Confirm VAT, period, registration, renewal and customer-owned-domain rules. |
| First 25 units entered for EGP 200 | Finance + operations | Confirm scope and update responsibility. |
| 7,000 brokers | Product owner | Confirmed 22 September 2026; do not add a “+” qualifier. |
| Meta integration included at no separate charge | Product + finance | Confirm setup/support limits. |
| Direct ad publishing from Estavo | Product + Meta permissions review | Verify live workflow and supported states. |
| Client AI customization | Product | Confirm name, icon, tone and bilingual settings. |
| Company access to buyer chats/activity | Product + privacy/legal | Confirm notice, consent, roles, retention and deletion. |

### Never publish as written

- “High intent” or “qualified” inferred from browsing behavior.
- Guaranteed leads, sales or advertising performance.
- Real-time prices or availability.
- Every project/unit in Egypt.
- AI replacing a broker, senior salesperson or human confirmation.

Use observed actions, explicitly shared preferences and clear product boundaries instead.

---

## 14. Visual family

| Page | Main visual argument | Centre of gravity |
|---|---|---|
| Market | Scattered data becomes a working request, comparison and offer | Wide broker workspace |
| Freelancer Site | Personal identity becomes a live property website | Browser-hosted personal brand |
| Company Site | Shared inventory and team context power one company site | Public site plus governed admin rail |
| Client AI | Buyer asks, clarifies and receives matches inside the site | Conversation inside browser |
| Meta | Permitted site events travel to customer-owned Meta | Signal route and permission gate |
| Broker network | One property reaches the owner’s site and broker network | Property record with two controlled outputs |

Shared palette, typography and material create the family. Different product structures prevent the pages from becoming repeated cards with changed labels.

---

## 15. Implementation order

### Phase 0 — confirm facts

1. Approve Market free-access boundaries.
2. Keep the confirmed 7,000-broker count synchronized across all pages.
3. Validate credits, Sites pricing and optional services.
4. Confirm Meta capabilities and privacy contract.
5. Confirm which Client AI customization settings are live.

### Phase 1 — routing and shared navigation

1. Update `tools/routes.json` around the two-product hierarchy.
2. Add `/meta/`.
3. Make the main navigation lead with Estavo Market and Estavo Sites.
4. Move data/update navigation toward `/market/`.
5. Point all Sites-family primary CTAs to `/website/`.

### Phase 2 — Market page

1. Consolidate `/data/`, update, Brokers AI and PDF-offer content into `/market/`.
2. Build the free-first commercial narrative.
3. Send every primary CTA to `brokers.estavo.space`.
4. Decide redirect/SEO treatment for `/data/`.

### Phase 3 — Sites family

1. Refocus `/websites/` on freelancers.
2. Refocus `/enterprise/` on brokerage company websites.
3. Refocus `/ai/` on Client AI.
4. Build `/meta/`.
5. Expand `/listings/` around site-to-network distribution.
6. Update supporting marketing, pricing and examples pages.

### Phase 4 — visual production

1. Wireframe all six commercial heroes together.
2. Build separate desktop and mobile compositions.
3. Generate still/reduced-motion variants.
4. Reuse the homepage art system without repeating its exact silhouette.

### Phase 5 — verification

1. Build both languages from sources.
2. Run `node tools/qa.js`.
3. Render all required desktop/mobile widths.
4. Check CTA destinations and referral attribution.
5. Review every exact commercial value in the rendered page.
6. Complete privacy/legal review for Meta and Client AI.

---

## 16. Definition of done

- A visitor understands that Estavo has exactly two main products.
- All broker market/data/update paths lead to the single Estavo Market page.
- The Market page leads directly to a free product trial on `brokers.estavo.space`.
- Estavo Sites has five focused commercial pages for its five buyer motivations.
- Every Sites-family primary CTA leads to `/website/`.
- Brokers AI stays with Market; Client AI stays with Sites.
- Meta is a Sites capability, not a generic marketing product.
- The broker-network page preserves customer ownership of the property, commission and deal.
- Unsupported prices, counts, intent labels and performance claims do not ship.
- Arabic/English, desktop/mobile and animated/still versions remain aligned.
