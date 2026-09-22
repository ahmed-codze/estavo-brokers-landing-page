# Estavo Business and Design Page Refactor Plan

Status: implementation plan based on the completed `/market/` business-page pass  
Updated: 19 September 2026

This plan turns the lessons from the Market page into a controlled refactor of the rest of the site. Market is the quality reference, not a layout to duplicate. Every route keeps its own audience, business argument, proof, product demonstration and conversion action.

This document supplements `COMMERCIAL-SERVICE-PAGES-PLAN.md` and the briefs in `commercial-page-briefs/`. Those documents define product scope. This document defines how to execute the next refactor safely and consistently.

## 1. What the Market pass established

The Market page now provides the working standard:

1. A direct business promise in the hero.
2. A real product scene rather than a generic illustration.
3. Immediate proof directly below the hero.
4. A recognizable customer problem in the audience's language.
5. A visible product mechanism: ask, compare and send.
6. Product-specific examples and scenarios.
7. Contextual CTAs that name the next useful task.
8. Honest boundaries beside claims that need them.
9. Professional icons and motion that explain the workflow.
10. Complete Arabic/English, mobile, reduced-motion and no-JavaScript states.

The next pages must achieve the same commercial strength without repeating Market's copy, browser composition, proof numbers or section silhouettes.

## 2. Non-negotiable product architecture

Estavo has two main products:

- **Estavo Market:** the broker-facing market workspace. Primary CTA goes to the configured `brokers.estavo.space` Market URL.
- **Estavo Sites:** the branded website product. Primary CTAs across its focused pages go to `https://estavo-brokers.com/website/`.

Supporting pages explain pricing, examples, buyer context, insights or custom integration. They do not become additional top-level products.

## 3. Business plan

### 3.1 Business objective

Every route must perform one defined commercial job. A page is not successful because it contains all available features; it is successful when the intended visitor understands the value, trusts the mechanism and takes the correct next action.

The two conversion paths remain fixed:

```text
broker needs market information → Estavo Market → open/search free
broker or company needs a customer-facing property experience → Estavo Sites → create/configure a Site
```

Custom integration is a qualified conversation for organizations that already operate a platform. Supporting pages help the visitor choose or trust one of those paths.

### 3.2 Funnel role by page

| Page group | Funnel role | Business result |
|---|---|---|
| Market | Direct product acquisition | Broker opens the free Market product and starts a real request |
| Websites | Direct Sites acquisition | Freelance broker begins creating a branded website |
| Enterprise | Qualified Sites acquisition | Brokerage company begins a company-site conversation or setup |
| Client AI | Capability-led Sites acquisition | Visitor understands that Client AI starts with an Estavo Site |
| Meta | Capability-led Sites acquisition | Visitor understands account ownership and starts the Site flow |
| Listings | Distribution-led Sites acquisition | Broker creates a Site to publish and distribute eligible properties |
| Integrations | Qualified enterprise enquiry | Existing-platform owner provides enough context for scoping |
| Marketing | Supporting capability education | Visitor connects buyer context to the Estavo Sites proposition |
| Pricing | Decision support | Visitor selects the correct product before reviewing optional services |
| Examples | Proof and evaluation | Visitor moves from a relevant demonstration to its product action |
| Insights | Trust and return visits | Reader moves from sourced content into relevant Market context |
| Homepage | Product routing | Visitor chooses Market or Sites without interpreting internal service structure |

### 3.3 Business contract for every page

Before design begins, write a one-page business contract containing:

1. **Audience:** the exact role and situation.
2. **Job:** what the visitor is trying to accomplish now.
3. **Problem:** what currently makes that job slower, weaker or unclear.
4. **Proposition:** one sentence explaining how Estavo changes the work.
5. **Mechanism:** the product steps that make the proposition credible.
6. **Proof:** approved figures, product states, ownership facts or examples.
7. **Objections:** the questions preventing action.
8. **Boundaries:** what the product does not promise.
9. **Primary action:** one destination and route-specific CTA language.
10. **Measurement:** the events used to evaluate the page.

### 3.4 Page-level commercial strategy

| Route | Main audience problem | Commercial proposition | Proof or trust device | Main objection to resolve |
|---|---|---|---|---|
| `/websites/` | Broker sends clients to scattered links or destinations carrying someone else's brand | One professional property destination under the broker's name | Visible identity, direct contact route and selected work in one site | “Will this actually look like my business, and what is free?” |
| `/enterprise/` | Company brand, inventory and team work are fragmented | One company property experience built on a governed shared foundation | Public brand connected to catalogue and team responsibilities | “Can this fit our existing process and users?” |
| `/ai/` | Buyers need help before a salesperson is available | Client AI helps visitors search and compare inside the customer's own site | One grounded conversation using only allowed site inventory | “Will it invent answers or expose other data?” |
| `/meta/` | Generic page events do not explain the property journey | Named, permitted property events can reach the customer's Meta account | Visible permission gate, named events and account ownership | “Who owns the account, data and budget?” |
| `/listings/` | A broker's own property has limited professional distribution | Add once, publish under the owner's name and distribute eligible inventory to brokers | Approved network figure, visible commission control and status management | “Who owns the lead, commission and deal?” |
| `/integrations/` | Organization needs Estavo capabilities without replacing its existing platform | Define the data or AI service around the platform already in use | Explicit scope, inputs, outputs and responsibility map | “Will this force a rebuild or an undefined project?” |
| `/marketing/` | Follow-up begins without enough context about what the buyer did or asked | Bring observed activity and explicit preferences into the next conversation | Clear distinction between viewed, asked and submitted information | “Are you guessing intent or tracking more than allowed?” |
| `/pricing/` | Visitor sees services before understanding which product they need | Choose Market or Sites first, then understand relevant optional services | Clear product split and terms beside each paid item | “What is actually free, optional or custom?” |
| `/examples/` | Visitor needs to see the product before acting | Prepared, labelled Market and Sites examples demonstrate real workflows | Complete examples with visible boundaries, not marketing mockups alone | “Is this a real workflow or only a visual concept?” |
| `/insights/` | Market updates are difficult to trust or connect to daily work | Dated and sourced editorial information linked to relevant Market context | Source, date, affected project/area and update type | “How current is this, and where did it come from?” |

### 3.5 CTA and measurement plan

Primary CTA events remain route-specific and include `data-position` for hero, workflow, output and close. Supporting interactions are measured separately and do not replace the main conversion.

Measure internally:

- primary CTA click-through by page, position, language and viewport;
- secondary demonstration-link use;
- reach of proof, workflow and closing sections;
- FAQ questions opened;
- completed destination handoff where attribution is available;
- mobile versus desktop drop-off;
- Arabic versus English conversion differences.

These measurements are operational analytics, not public performance claims.

## 4. Design plan

### 4.1 Design objective

The commercial family should feel like one Estavo system while making each page recognizable from its visual mechanism alone. Shared tokens create trust; route-specific compositions explain the business.

### 4.2 Shared page anatomy

Every core commercial route receives:

1. a product-family eyebrow;
2. a strong hero split between commercial copy and a recognizable product scene;
3. an immediate proof band;
4. an editorial problem section;
5. one large product-mechanism theatre;
6. a workflow or before/after transformation;
7. one output-focused section;
8. scope/commercial explanation;
9. focused FAQ;
10. strong closing CTA.

This is a shared reading rhythm, not a shared visual layout. Section order may change when the page's decision requires it.

### 4.3 Page-level visual concepts

| Route | Hero composition | Main visual theatre | Signature motion | Mobile composition |
|---|---|---|---|---|
| `/websites/` | Broker identity controls beside a live personal property site | Name/logo/colors/contact flow into a shareable browser and buyer contact | Brand tokens assemble the site; contact path highlights | Identity card → site preview → contact action |
| `/enterprise/` | Company website centered between catalogue and team rails | Public site, governed inventory and sales handoff shown as one system | Approved changes move from admin to public site and team | Company site first, then inventory and team layers |
| `/ai/` | AI conversation visibly embedded inside the customer's branded site | Question → clarification → matching site results → handoff | Staged conversation with result-state transition | One conversation with two results and one handoff |
| `/meta/` | Estavo Site and customer Meta account separated by a permission gate | Named property events travel through consent/permissions into the owned account | Signal lines activate only after the gate state is shown | Vertical Site → permission → Meta sequence |
| `/listings/` | Owner-controlled property record at the center | Record branches to branded Site and professional broker-network view | Two outputs publish together; commission stays attached to network view | Compact Y-flow with owner record first |
| `/integrations/` | Existing platform remains visually dominant | Selected data/AI modules connect through a scoped interface to defined outputs | Connector paths animate after scope selection | Platform → selected service → output stack |
| `/marketing/` | Buyer journey timeline paired with salesperson follow-up | Viewed, asked and explicitly shared information form a concise context panel | Timeline events group into a handoff without intent scoring | Chronological events followed by one follow-up card |
| `/pricing/` | Two-product choice before any commercial detail | Market and Sites paths reveal their own optional services | Controlled product switch, no animated price gimmicks | Two stacked choices with progressive disclosure |
| `/examples/` | Market/Sites selector with a real prepared example visible immediately | Complete example viewer with context, states and boundaries | Tab/state transition only; examples remain inspectable | Product tabs above one full-width example |
| `/insights/` | Editorial lead story with source and date visible | Filterable update stream linked to project or area context | Restrained filter and timeline transitions | Lead item followed by compact sourced list |

### 4.4 Component plan

Extract and standardize:

- commercial hero shell;
- primary/secondary CTA with directional icon behavior;
- proof header, numeric proof and non-numeric proof variants;
- line-icon container and route icon set;
- editorial problem cards;
- product theatre frame;
- workflow steps and connection lines;
- before/after comparison;
- business-output panel;
- scope and limitation callout;
- FAQ and closing CTA;
- mobile horizontal track only where content benefits from comparison.

Keep route-specific:

- browser/site scenes;
- AI conversation states;
- Meta permission flow;
- listing distribution branch;
- enterprise team/inventory rail;
- integration connector diagram.

### 4.5 Responsive design plan

- **1728–1280:** full visual theatre, generous whitespace and connected diagrams.
- **1024–768:** collapse two-column scenes without shrinking desktop UI into illegibility.
- **390–320:** rewrite the visual composition as a short sequence; do not merely scale it down.
- Preserve CTA hierarchy and proof near the top at every size.
- Arabic and English line wrapping are reviewed separately.
- Horizontal scroll is permitted only for intentional labelled carousels.

### 4.6 Motion plan

Use three motion levels:

1. **Entry:** restrained reveals and approved number count-ups.
2. **Explanation:** sequence, connection or state transition demonstrating how the product works.
3. **Feedback:** button arrows, tabs, FAQ and hover/focus response.

Each page should have one signature explanatory animation. Reusing every Market animation would weaken page identity and performance.

For reduced motion, show final states with no delayed information. Without JavaScript, all core copy, proof, product examples and CTAs remain visible.

### 4.7 Design review deliverables per page

Before implementation approval, capture:

- desktop hero and immediate proof at 1440px;
- complete desktop page at 1440px;
- Arabic mobile page at 390px;
- English mobile page at 390px;
- 320px overflow probe;
- reduced-motion state;
- no-JavaScript first screen and full-page height;
- CTA destination and keyboard-focus check.

## 5. The shared business-page framework

Every commercial page uses the following decision sequence. The content and visual treatment must be unique to the route.

### 5.1 Hero: one commercial outcome

- Name the page's exact audience or job.
- Lead with the outcome, not the technology.
- Show the product in the context where the audience uses it.
- Use one primary CTA that completes the promise.
- Use no more than one secondary CTA, normally an in-page demonstration link.

### 5.2 Immediate proof

Place a proof section directly after the hero. Proof does not always mean large numbers.

Allowed proof formats:

- approved scale figures;
- concrete included capabilities;
- a short three-step operating model;
- customer control or ownership facts;
- dated examples or evidence.

Do not invent a metric because Market has a number strip. Every number needs a current approved source and a narrow QA allowance.

### 5.3 Customer problem

- Describe a real work problem before listing features.
- Use observable situations, not invented emotional claims.
- Keep the language natural to the specific audience: freelance broker, company owner, marketer, product team or buyer.

### 5.4 Product mechanism

Show how the product changes the work:

```text
input or customer situation → Estavo action → useful business output
```

The mechanism must be visible in the primary illustration or interaction. Avoid grids of generic feature cards when a process, handoff or comparison would explain the value better.

### 5.5 Business outcome

Connect capabilities to a practical result such as:

- a clearer client response;
- one branded destination;
- faster comparison;
- better follow-up context;
- controlled distribution;
- a defined integration scope.

Do not claim guaranteed sales, leads, campaign performance or time savings without evidence.

### 5.6 Contextual CTAs

CTA labels must name the next task. Avoid generic labels such as “Get started” or “Learn more.”

Use primary CTAs at four natural points where the page supports them:

1. hero;
2. after the main workflow or proof;
3. after the strongest product output;
4. closing section.

The wording may change with context, but the destination and conversion intent must remain consistent.

### 5.7 Objection handling

End with a focused FAQ covering scope, responsibility, ownership, pricing model and limitations. Do not repeat the page in FAQ form.

## 6. Copy and language gate

Copy is reviewed before visual implementation.

### Arabic

- Write the Arabic version for the audience; do not mechanically translate an English slogan.
- Use direct professional Egyptian Arabic without forcing slang.
- Prefer established audience language already used by the owner or validated live material.
- Do not publish invented expressions whose business meaning is unclear.
- Remove a sentence if it adds no useful product or commercial information.
- Wrap meaningful Latin runs in `<bdi>`.

### English

- Use direct international English and concrete verbs.
- Avoid generic SaaS language and inflated claims.
- Keep the business meaning aligned with Arabic without requiring literal parity.

### Copy review checklist

Before coding a page, approve a compact bilingual content map containing:

- audience;
- one-sentence proposition;
- hero headline and lead;
- proof facts;
- problem statements;
- workflow;
- CTA labels and destinations;
- commercial boundaries;
- FAQ questions.

Every unusual phrase must be traceable to an approved product fact, owner wording, established audience language or a clearly necessary explanatory bridge.

## 7. Visual and motion rules

### Shared family

Reuse the Estavo navy, blue, paper, typography, spacing, buttons, header and footer. Reuse interaction behavior where appropriate, not full page compositions.

### Route-specific visuals

Each page gets one recognizable visual argument:

- Market: working request, comparison and offer.
- Freelancer website: personal identity becoming a live property site.
- Company website: public brand connected to managed inventory and team work.
- Client AI: buyer conversation inside the customer's website.
- Meta: permitted property events passing through a control gate to the customer's account.
- Listings: one owner-controlled property branching to the website and broker network.
- Integrations: existing platform connected to a defined data/AI scope.
- Marketing: buyer journey and explicit request context passed into follow-up.
- Pricing: two-product commercial choice with optional services clearly separated.
- Examples: Market and Sites demonstrations organized as evidence.
- Insights: dated, sourced editorial content connected back to Market.

### Motion

Motion must explain state or sequence:

- count-up only for approved proof numbers;
- line drawing for relationships or signal paths;
- staged conversation for AI;
- controlled handoff for lead or team flows;
- branch animation for distribution;
- state changes for comparison, filtering or publishing.

Avoid decorative motion that competes with the message. Every animated state needs a static reduced-motion equivalent and useful no-JavaScript content.

### Icons

- Use one consistent custom line-icon style.
- Use icons to identify business concepts, not as decoration beside every sentence.
- Replace ambiguous symbols with recognizable project, document, website, person, signal, permission, property and team icons.

## 8. Page-by-page execution summary

| Route | Audience and business job | Proof immediately after hero | Main demonstration | Primary CTA language |
|---|---|---|---|---|
| `/websites/` | Freelance broker needs one professional destination under their name | Own name, one shareable link, direct contact | Brand setup becomes a live mobile/desktop property site, then a buyer contacts the broker | Create your website free / اعمل موقعك مجانًا |
| `/enterprise/` | Brokerage company needs one governed brand and working foundation | Company brand, shared catalogue, team access | Public company site connected to an admin/inventory rail and sales handoff | Start your company website / ابدأ موقع شركتك |
| `/ai/` | Site owner wants buyers to search and ask before contacting sales | Uses site inventory, asks clarifying questions, supports handoff | Buyer question → clarification → matching site results → WhatsApp/sales handoff | Create your site and add AI / اعمل موقعك وفعّل الـ AI |
| `/meta/` | Site owner or marketer needs clearer permitted property-event context | Customer-owned account, named events, customer-controlled budget | Site events → consent/permission gate → customer's Meta account | Create your site and connect Meta / اعمل موقعك واربط Meta |
| `/listings/` | Broker/company wants more reach for its own eligible properties | Approved 7,000-broker figure, commission control, no sale guarantee | Property record branches to branded site and broker-network view | Create your site and list properties / اعمل موقعك واعرض وحداتك |
| `/integrations/` | Organization already has a website or application | Existing platform stays, scope is defined, implementation is agreed | Existing system → selected data/AI service → defined outputs | Discuss your integration / كلمنا عن الربط |
| `/marketing/` | Salesperson needs useful context before follow-up | What the buyer viewed, asked and explicitly shared | Buyer journey timeline becomes a concise follow-up view | Add buyer context to your site / ضيف سياق العميل لموقعك |
| `/pricing/` | Visitor needs to understand what is free and what is optional | Market, Sites and custom integration separated clearly | Product choice first, then the relevant optional services | Choose Market or create a Site / اختار السوق أو اعمل موقعك |
| `/examples/` | Visitor wants evidence before committing | Two clear product families and labelled demonstrations | Market/Sites switcher with complete prepared examples | Open Market or create a Site / افتح السوق أو اعمل موقعك |
| `/insights/` | Broker wants useful, attributable market updates | Source, publication date and affected area/project | Editorial card → update detail → relevant Market context | Open the related Market view / افتح التفاصيل في السوق |

### Homepage

Refactor after the core commercial routes are stable. The homepage should introduce the Estavo parent promise, make the two-product model obvious and route visitors to the relevant detailed page. It must not flatten every capability into an equal product card.

### `/data/`

Keep as a migration route only. Consolidated data/update content belongs to Market. Preserve language-correct canonical and redirect behavior.

## 9. Technical refactor before page production

Market currently has a dedicated stylesheet and script. Do not copy those files for every route.

### 9.1 Extract shared commercial primitives

Create a shared commercial layer for:

- hero/action layout;
- button and CTA icon behavior;
- proof-section structure;
- section headings and editorial spacing;
- business cards and comparison rows;
- FAQ and closing CTA;
- shared responsive behavior;
- shared reduced-motion rules.

Suggested files:

```text
assets/css/commercial.css
assets/js/commercial-page.js
```

Keep Market-specific browser, AI, PDF and availability scenes in `market.css` and `market-landing.js`.

### 9.2 Add route-level asset manifests

Replace the Market-only conditional in `tools/build-pages.js` with a route asset map. Each route may load:

- shared commercial CSS/JS;
- one route stylesheet;
- one route script only when its demonstration requires it.

Suggested structure:

```text
assets/css/pages/websites.css
assets/css/pages/enterprise.css
assets/css/pages/ai.css
assets/css/pages/meta.css
assets/css/pages/listings.css
assets/css/pages/integrations.css

assets/js/pages/websites.js
assets/js/pages/enterprise.js
assets/js/pages/ai.js
assets/js/pages/meta.js
assets/js/pages/listings.js
assets/js/pages/integrations.js
```

Supporting pages should use the shared layer without receiving unnecessary JavaScript.

### 9.3 Preserve source/generated boundaries

- Author page content in `tools/pages/*.ar.html` and `tools/pages/*.en.html`.
- Generate route HTML through `tools/build-pages.js`.
- Do not hand-edit generated route files.
- Keep unrelated working-tree changes untouched.

## 10. Implementation sequence

Refactor and approve one page at a time. Do not rewrite every route before reviewing the first Sites page.

### Phase 0 — freeze the Market reference

1. Save desktop and mobile reference screenshots in both languages.
2. Record current CTA destinations, analytics events and approved claims.
3. Mark shared versus Market-specific CSS/JS.

### Phase 1 — build the shared commercial layer

1. Extract shared primitives without changing Market's rendered appearance.
2. Add the route asset manifest.
3. Rebuild and visually compare Market before and after extraction.

### Phase 2 — pilot with `/websites/`

1. Approve the bilingual copy map.
2. Build the freelancer-specific hero and proof section.
3. Build the personal-brand-to-live-site demonstration.
4. Add contextual CTAs and focused FAQ.
5. Complete full QA and owner review.

The approved Websites page becomes the Sites-family reference, while Market remains the Market-family reference.

### Phase 3 — core Sites pages

Implement separately in this order:

1. `/ai/` — conversation and handoff interaction.
2. `/listings/` — property-to-network distribution and approved proof count.
3. `/enterprise/` — company site, inventory and team structure.
4. `/meta/` — permissions, ownership and event flow; privacy review required.

### Phase 4 — supporting commercial pages

1. `/integrations/`
2. `/marketing/`
3. `/pricing/`
4. `/examples/`
5. `/insights/`

### Phase 5 — homepage and route consolidation

1. Update homepage routing after final commercial propositions are stable.
2. Confirm `/data/` migration behavior.
3. Check header, drawer, footer and sitemap consistency.
4. Remove obsolete duplicate page-specific CSS only after visual parity is proven.

## 11. Per-page execution checklist

For each route:

1. Compare the current local page with any approved live/reference material.
2. Write and approve the bilingual content map.
3. Confirm every product fact and exact figure.
4. Define one visual thesis and its mobile composition.
5. Implement source templates, route CSS and only necessary JavaScript.
6. Add contextual CTA labels while preserving the required destination.
7. Build generated pages.
8. Run route QA and full-site QA.
9. Verify Arabic and English at 320, 360, 390, 1280, 1440, 1512 and 1728 pixels.
10. Verify reduced motion, no JavaScript, keyboard operation and no horizontal overflow.
11. Review the entire Arabic page for natural audience language before approval.
12. Capture final reference screenshots before starting the next route.

## 12. Acceptance criteria

A page is complete only when:

- its audience and business outcome are clear in the first screen;
- proof follows the hero and uses only approved facts;
- the main visual demonstrates the page's product mechanism;
- every primary CTA is useful, contextual and reaches the correct destination;
- Arabic reads naturally and contains no unexplained invented phrasing;
- the page does not look like Market with different text;
- motion improves understanding and has static fallbacks;
- claims and limitations appear in the correct context;
- both languages pass static QA and the full viewport matrix;
- the page remains useful without JavaScript.

## 13. Rollout rule

Complete, review and approve one route before starting the next. Feedback from each completed page updates the shared commercial layer, but page-specific visual decisions remain local. This prevents a weak pattern from being multiplied across the whole site.
