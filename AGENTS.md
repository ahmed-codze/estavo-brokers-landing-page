# Estavo Brokers Landing Page — Brand, Content and Experience Handbook

This is the durable context document for any agent working in this directory. It explains what Estavo is, what this website is trying to accomplish, the decisions already made, why they were made, and how to extend the work without weakening the product story.

Read this file before changing public copy, information architecture, layouts, illustrations, motion, routes, or generated pages. For the detailed illustration specification, also read `DESIGN-GUIDELINES.md`.

Last consolidated from the working site: **19 September 2026**.

---

## 1. The short version

Estavo has **two main products**:

1. **Estavo Market** — the free broker-facing market product. It brings market data, Estavo's collection/update process, search, comparison, Brokers AI and branded PDF offers into one working experience.
2. **Estavo Sites** — the branded website product. Its commercial family covers websites for freelance brokers, websites for brokerage companies, AI for website visitors, Meta integration and distribution of the customer's properties to the Estavo Brokers network.

Custom Data + AI integration can support an existing platform, but it is a separately scoped enterprise service—not a third main product.

The master English proposition is:

> **Egypt’s real-estate market. Under your brand.**

The master Arabic proposition is:

> **السوق العقاري كله تحت اسمك.**

The strategic idea is not a flat catalogue of unrelated services. The maintained data is the foundation; Market lets brokers work with it, and Sites lets them present and activate it under their own name.

The visual equivalent is a product-data core connected to recognizable working surfaces. The product itself is the hero; stock property imagery and vague technology decoration are not.

---

## 2. What the brand must mean

### 2.1 Brand role

Estavo is the quiet infrastructure and practical working layer behind a broker’s business. It organizes changing project and unit information, then makes that information useful without asking the broker to surrender their identity to another consumer marketplace.

The brand should feel:

- informed, because the product understands the structure of property data;
- useful, because every section begins with a real broker or buyer task;
- calm, because property decisions already contain enough noise and pressure;
- honest, because data freshness, availability, prices, AI limits and commercial scope have boundaries;
- broker-enabling, because the broker’s name and relationship with the buyer remain visible;
- contemporary, because the system connects data, AI, websites and platforms without resorting to generic “future of real estate” language.

### 2.2 Brand promise

**Estavo maintains the property information; the customer chooses how to work with it.**

That promise has three layers:

1. **One maintained foundation:** developer, project, unit, price and payment-plan information for the cities in scope.
2. **Two clear products:** work with the market in Estavo Market, or present it under the customer's name with Estavo Sites.
3. **The customer remains in control:** their cities, their selected properties, their brand, their contact relationship, and a service scope agreed before sale.

### 2.3 Positioning boundaries

Estavo is:

- a maintained property-data and services business;
- a broker-facing property marketplace for search and comparison;
- a branded presentation layer for brokers and brokerages;
- property-aware AI tied to available information;
- an integration partner for existing platforms;
- a source of buyer context based on explicit statements and observed actions.

Estavo is not presented as:

- a generic property portal competing for the buyer relationship;
- a CRM replacement;
- a lead-scoring or buyer-intent oracle;
- a guaranteed source of live availability, returns or sales outcomes;
- an autonomous AI sales agent that replaces a team;
- a template-site agency whose primary product is web design;
- a repository of unverified listings, invented inventory or decorative dashboards.

### 2.4 Why “under your name” matters

Many brokers can have access to the same project. The commercial difference is often who owns the presentation and relationship. “Under your name” answers that tension: buyers see the broker’s or company’s identity, selected work and contact details. Estavo enables the experience without making Estavo the consumer-facing star.

Do not turn this into a white-label claim broader than the implemented service. Explain exactly where the broker’s identity appears: the website and buyer-facing AI experience, selected property presentation, and contact information.

---

## 3. Audiences and jobs to be done

### Independent broker

Needs to find relevant options quickly, compare the details that matter, send a credible link, and look established without manually building a data operation.

Primary routes: Estavo Market or the Estavo Sites page for freelance brokers.

### Brokerage company

Needs a shared, maintained information base; consistent presentation under the company name; useful tools for team members and buyers; and a defined commercial scope across cities and services.

Primary routes: the Estavo Sites page for brokerage companies, then its Client AI, Meta and property-distribution pages.

### Existing website or platform owner

Already has a customer experience and does not want to replace it. Needs selected data, AI, or both, with the field groups, cities, update method and integration method defined before implementation.

Primary routes: integrations, enterprise, data, AI.

### Buyer, as an indirect audience

The buyer needs to understand properties, ask questions and compare choices. This site does not primarily sell Estavo to the buyer; it sells the broker a better way to serve the buyer.

### Core jobs

- “Help me find options that match a real client request.”
- “Help me compare the details that will decide the choice.”
- “Keep project information current without my team repeatedly collecting it.”
- “Let me present my work professionally under my name.”
- “Let a buyer ask questions about the properties I present.”
- “Give my team context before they call, without pretending to know buyer intent.”
- “Put useful data or AI into the platform I already operate.”

Every new section or feature should connect to at least one of these jobs.

---

## 4. Product model and approved vocabulary

### The data foundation

The approved hierarchy is **cities and areas → developers → projects → units**, with relevant prices, payment plans and project information. Use these concrete customer-facing terms.

Avoid internal abstractions such as “coverage,” “property record,” “data core,” “sample developer,” or “recorded activity” in public copy. Those phrases may be useful in code or this handbook, but they expose the implementation instead of explaining the customer value.

### Product and service names

| Concept | English | Arabic guidance |
|---|---|---|
| Brand | Estavo | إستاڤو in Arabic prose; keep official Latin marks where designed |
| Broker-facing product | Estavo Market | Keep as `<bdi>Estavo Market</bdi>` |
| Branded-site product | Estavo Sites | Keep as `<bdi>Estavo Sites</bdi>` where the product name is needed |
| Data | Market data / property data | بيانات السوق / بيانات العقارات |
| Website | Branded website / your website under your name | موقع باسمك / موقع يحمل اسمك |
| Broker AI capability | Brokers AI inside Estavo Market | `<bdi>Brokers AI</bdi>`; keep it with the Market story |
| Buyer AI capability | Client AI inside Estavo Sites | مساعد الـ `<bdi>AI</bdi>` لعملاء موقعك |
| Integration | Integrations / connect your platform | الربط بمنصتك |
| Broker inventory | Your own listings | عقاراتك الخاصة / وحداتك بحسب context |
| Buyer context | Buyers & marketing | العملاء والتسويق / إشارات العميل بحسب context |
| Editorial material | Market insights | أخبار وتحليلات السوق |

“The market” means the broad Egyptian property market. **Estavo Market** is the product name. Do not use the two interchangeably.

### Current commercial truths reflected by the site

- Estavo Market is positioned as free for brokers; the exact boundary of free browsing/tools must remain current and approved.
- Website creation is free.
- Market data collection and updates for brokers belong to the Estavo Market story, not a separate data product.
- Estavo Sites may have optional paid data, domain, AI, entry or integration services; exact terms require a current approved commercial source.
- AI pricing depends on the type and amount of use.
- Integration cost and timing depend on the agreed platform, data and service scope.
- A customer does not need a new website to use Market or to discuss an integration.

Do not add exact prices, limits, timeframes or inclusions unless a current approved commercial source is supplied. “Ready in around five minutes” is an existing website-onboarding proposition; preserve its explanation and do not silently generalize it to integration or data setup.

---

## 5. The content strategy

### 5.1 Communication order

The site deliberately moves through this logic:

1. **Name the outcome:** the market, usable under the customer’s brand.
2. **Establish the foundation:** organized project and unit information.
3. **Acknowledge the operational problem:** the market changes and someone must maintain it.
4. **Present two products:** free Estavo Market for the broker, or Estavo Sites under the customer's name.
5. **Show Sites capabilities as one product family:** freelancer/company website, Client AI, Meta and property distribution.
6. **Route by customer type:** Market user, freelance Site owner, brokerage company, or existing platform.
7. **Explain commercial scope:** free Market access, free Site creation and approved optional/usage-based services.
8. **Resolve objections:** FAQs describe limits, not just benefits.
9. **Close with a concrete next step:** open Market, create a website, or discuss enterprise/integration needs.

This sequence exists to prevent feature soup. It first creates one mental model, then lets each service inherit meaning from it.

### 5.2 Homepage story

The current bilingual homepages are `index.html` and `en.html`. They are hand-maintained published files, not emitted by `tools/build-pages.js`.

The intended homepage argument is:

- **Hero:** lead with the parent Estavo proposition, “the real-estate market under your name,” but give the visitor one primary next step: open Estavo Market. Website creation is a secondary text link for visitors already ready to build their branded presence.
- **Proof strip:** establish scale with the approved 30,000-unit and 7,000-broker figures, website-onboarding and update facts, and connect each fact to the broker task it enables. The other approved scale figures are 700 developers and 2,000 projects. Use these counts exactly, without a “+” qualifier. Do not put caveats inside the proof strip or use developer/project counts there.
- **Differentiation:** explain that Estavo organises market information behind the broker while the broker remains in front of the buyer. The network visual demonstrates sources flowing into Estavo and then into customer-controlled surfaces.
- **Market workflow:** start from a real buyer request, then show search, comparison, available updates and a branded offer as one working sequence. Estavo Market remains the primary conversion path.
- **Outcome proof:** describe the three broker outcomes—reaching relevant options, comparing decision inputs and sending under the broker's name—rather than presenting six co-equal service cards.
- **Website + Client AI:** present the branded website as the next stage for brokers who want buyers to browse and return under their brand. Keep the product illustration embedded and label it as an example rather than sending all proof to another page.
- **Companies/platforms:** give brokerage companies a dedicated dark band using the approved “less than one data-entry employee's salary” economic framing, with separate company and existing-platform routes.
- **FAQ and close:** place availability, network-reach and sales boundaries in the FAQ, then close with Estavo Market as the single primary action and website creation as a secondary link.

Price-history, inflation, purchase-cost and real-return analysis belong on the detailed Market page, not the homepage.

English and Arabic do not need literal sentence-by-sentence translation, but they must preserve the same product truth, information hierarchy, promise strength and CTA destination.

### 5.3 Route map and purpose

Metadata, navigation labels and route-level descriptions live in `tools/routes.json`. Service-page body copy lives in `tools/pages/{route}.{ar|en}.html`. Generated outputs live at `/{route}/index.html` and `/{route}/en.html`.

| Route | Visitor question | Page promise | Primary next step |
|---|---|---|---|
| `/data/` | What information exists and who keeps it current? | Supporting/legacy route; its product story is consolidated into Estavo Market. | Try Estavo Market free. |
| `/market/` | Can I work a live client request with organized market information? | Free broker market access, data/update process, search, comparison, Brokers AI and PDF offers. | Try Estavo Market free. |
| `/websites/` | Can I have a professional property website as a freelance broker? | An Estavo Site under the broker's own name. | Create a website at `/website/`. |
| `/ai/` | Can AI help visitors on my property website? | Client AI searches and compares only the inventory allowed on that Estavo Site. | Create a website at `/website/`. |
| `/integrations/` | Can this work inside what I already have? | Select data/AI, cities, field groups and update scope for an existing platform. | Discuss the integration. |
| `/marketing/` | What will I know before following up? | Supporting Sites capability: contact details, stated preferences and viewed content as separate evidence. | Create a website at `/website/`. |
| `/meta/` | Can my site's property events connect to my Meta account? | A transparent, customer-owned Meta connection for permitted Estavo Site events. | Create a website at `/website/`. |
| `/listings/` | Can other brokers help sell properties from my site? | Publish eligible properties on the Estavo Site and distribute them to the broker network with customer-controlled commission. | Create a website at `/website/`. |
| `/insights/` | How do I follow changes in my areas? | Dated, sourced updates and analysis connected to the broker’s work. | Open relevant information or Market. |
| `/pricing/` | What is free and what determines cost? | Market and Sites commercial terms organized under the two-product model. | Try Market or create a Site. |
| `/enterprise/` | Can my brokerage company have an Estavo Site? | A company-branded website with shared inventory, team context and Sites capabilities. | Create a website at `/website/`. |
| `/examples/` | Can I see the product before choosing? | Prepared Market and Sites demonstrations. | Open the matching product. |

### 5.4 Page anatomy

A service page normally contains:

- one focused eyebrow, one H1 and one explanatory lead;
- a concrete product scene or example;
- an explanation of workflow, scope or responsibility;
- links to adjacent services only where they complete the reader’s task;
- FAQs that answer real objections and limits;
- a closing CTA whose label accurately names its destination.

Do not force every page into the exact same number of sections. Shared structure should create comprehension, not sameness.

---

## 6. Voice and tone

### 6.1 Voice attributes

**Specific, not inflated.** Say “compare payment plans” instead of “unlock powerful insights.” Name the property task, information and surface.

**Direct, not abrupt.** Start with the user’s work: “Start from your client’s request.” Avoid long company introductions.

**Confident, not absolute.** Explain what Estavo maintains and what the service can do. Do not promise perfect availability, guaranteed results, comprehensive national inventory or omniscient AI.

**Human, not cute.** The brand can be warm and conversational, especially in Egyptian Arabic, but it is dealing with high-value decisions. Avoid jokes, hype, emojis and breathless punctuation.

**Transparent, not defensive.** A useful limit increases trust: AI answers from the information available; when it does not know, it says so and hands over to the team.

**Broker-centered, not self-centered.** Prefer “your client,” “your work,” “your name,” and the action enabled. Use “Estavo” when ownership of data maintenance or a product name needs to be clear.

### 6.2 Writing pattern

The strongest Estavo copy usually follows:

> real situation → concrete capability → customer control or boundary

Example:

> A buyer asks about a project. Compare the available unit and payment details in one place, then present the options through the service that fits your work.

Headings should usually make one claim. Leads explain how it works. Supporting copy supplies evidence, scope or a boundary. CTAs name a real action.

### 6.3 English

- Use plain international English and short sentences.
- Prefer active verbs: search, compare, choose, review, present, connect, ask.
- Use “real-estate” when adjectival in established titles; keep usage consistent within a page.
- Use sentence case for headings and controls.
- Avoid venture/technology clichés: seamless, revolutionary, cutting-edge, ecosystem, leverage, supercharge, unlock, game-changing.
- Avoid vague business claims: better leads, smarter decisions, higher conversion, complete market, real-time data, unless they are defined and evidenced.

### 6.4 Arabic

Arabic public copy uses clear, contemporary Egyptian Arabic suited to a professional broker. It should sound spoken and direct, not bureaucratic Modern Standard Arabic and not slang-heavy banter.

Established forms include:

- شغلك، عميلك، موقعك، باسمك
- دور وقارن
- اختار، اعرف، ضيف، كلمنا
- جوّه when the tone is conversational and the surface supports it

Preserve professional clarity. Avoid overly formal constructions when a shorter Egyptian phrase exists, but do not use jokes, exaggerated street language or ambiguous shortcuts.

Technical Latin runs inside RTL prose must be isolated with `<bdi>`, including `<bdi>AI</bdi>`, `<bdi>Estavo Market</bdi>`, `<bdi>Meta</bdi>` and `<bdi>WhatsApp</bdi>`.

Arabic is adaptation, not transliteration. Preserve the English meaning and claim strength, then write the sentence naturally for an Egyptian broker. Check line breaks and visual balance independently; Arabic display text needs more line height.

### 6.5 Preferred and forbidden language

| Prefer | Avoid | Why |
|---|---|---|
| available information | complete/live inventory | Availability and completeness require proof. |
| Estavo follows and publishes updates | always real-time | Describes a maintainable process. |
| what the buyer viewed / explicitly shared | intent score / qualified buyer | Observation is not inferred intent. |
| example | fake/sample/demo developer | Keeps examples honest without looking unfinished. |
| project/unit data | property record/data core | Customer language beats system language. |
| cities you work in | coverage | Concrete and understandable. |
| choose the services you need | all-in-one platform | Avoids forcing unrelated services into one claim. |
| AI based on available property data | AI that knows everything | States the knowledge boundary. |
| discuss the integration | connect instantly | Integration requires discovery and scope. |

The automated forbidden-copy checks in `tools/qa.js` are minimum safeguards, not a complete editorial review.

---

## 7. Claims, examples and data ethics

Honesty is part of the product design.

### Approved example policy

- Label illustrative product surfaces at component level with “Example” / “مثال”.
- Ordinary non-commercial values may make an example legible: area, room count, property type, or schematic payment duration.
- The request and displayed result must agree. Do not invent a preference the example user did not state.
- Use ordinary fictional project/company names only when needed; never let placeholder language look published.
- Separate broker-entered own listings from Estavo-maintained project data.

### Claims that require a verified, current source

- price or starting price;
- availability or inventory count;
- ROI, growth or yield percentage;
- advertising performance, reach or conversion;
- update frequency stated as a guaranteed interval;
- rankings, ratings or review counts;
- implementation time or usage limits beyond currently approved copy;
- city/project completeness;
- commission outcomes.

If a verified value is not available, change the visual or sentence so it demonstrates structure instead of fabricating proof. Use “حسب الوحدة” or “حسب خطة السداد” where appropriate. Redaction is useful only when a hidden price is materially part of a comparison, not as filler on every field.

### Buyer-context policy

Distinguish:

- what a buyer explicitly stated;
- what pages or properties they viewed;
- what comparisons or questions they performed;
- the team’s later interpretation.

The interface may summarize the first three. It must not label a person “qualified,” “ready to book,” “high intent,” or prescribe “call now” from behavior alone.

### AI policy in copy

- Tie answers to the projects and units available to the service.
- Show that the AI can clarify a request, compare information and hand over context.
- When information is missing, the approved behavior is to say it does not know and refer to the team.
- Never suggest the AI replaces a sales team, negotiates, guarantees correctness, or independently knows live availability.

---

## 8. Calls to action and journey design

A CTA is a promise. Its label and destination must agree.

### Primary actions

- **Try/open Estavo Market free** → the Market referral URL on `brokers.estavo.space`.
- **Create/start my Estavo Site** → `https://estavo-brokers.com/website/`.
- **Discuss an integration / tell us what your company needs** → the appropriate enquiry route or form.
- **Try an example** → a real prepared example, never a blank placeholder.

Every Market/data/update/Brokers-AI primary CTA uses the first destination. Every freelancer-site, company-site, Client-AI, Meta and broker-network primary CTA uses the second destination.

### CTA hierarchy

- One primary next step per decision context.
- Use a secondary action only when two audience paths are genuinely parallel, as in the homepage close.
- Text links are for learning more or moving to an adjacent service.
- Do not style illustration nodes as CTAs. Interactive affordances belong to the real page, not decorative diagrams.
- Do not use “Learn more” when a more specific label is available.

### Referral constraint

Platform links must retain the `https://brokers.estavo.space` origin where expected. `assets/js/referral.js` carries the active `?ref` slug forward; changing the origin can silently break attribution.

Current defaults in `tools/routes.json`:

- Market: `https://brokers.estavo.space/go/?ref=default-landing-page-market`
- Website in the current code: `https://brokers.estavo.space/go/?ref=default-landing-page` (must migrate to `https://estavo-brokers.com/website/` during the commercial-page implementation)
- WhatsApp: `https://wa.me/201069528393`

Treat `tools/routes.json` as canonical for routes, contact details, social links and shared metadata.

---

## 9. Visual identity

### 9.1 Overall direction

The September 2026 direction is **Estavo products in motion**: recognizable product surfaces, precise line geometry, restrained depth and visible data relationships, built from the Estavo palette.

The design should feel like a calm, editorial product explanation—not a portal full of listing cards and not a neon AI startup. Product specificity creates the premium quality.

### 9.2 Palette

Use variables from `assets/css/v3/tokens.css`; do not introduce raw colors in page components.

| Role | Token | Current value |
|---|---|---|
| Deep brand ground | `--es-navy-950` | `#0b2239` |
| Raised navy | `--es-navy-900` | `#102b45` |
| Structural blue | `--es-blue-700` | `#163e69` |
| Primary Estavo blue | `--es-blue-600` | `#28567f` |
| Secondary blue | `--es-blue-500` | `#47749a` |
| Main ink | `--es-ink` | `#13283c` |
| Page ground | `--es-paper` | `#fafcff` |
| Panel ground | `--es-white` | `#ffffff` |
| Alternating surface | `--es-mist` | `#f1f5f8` |
| Secondary structure | `--es-mist-2` | `#e8eef3` |
| Positive accent | `--es-positive` | `#27a06f` |

Homepage illustrations use navy, Estavo blue, pale blue and paper. Green/mint is intentionally absent from the refreshed homepage art; it remains a restrained status accent in legacy service scenes until those are migrated. External brand color is allowed only where a third-party mark or recognizable interface genuinely requires it.

Why: a limited palette makes many data-heavy scenes read as one system and keeps the site from looking like a collection of unrelated SaaS templates.

### 9.3 Typography

- Page UI uses **Cairo** in Arabic and English, weights 400, 500, 600 and 700.
- The shared family makes bilingual pages feel like the same brand rather than two parallel designs.
- Body is normally 400; headings and labels use deliberate emphasis. Avoid indiscriminate heavy bold.
- Current premium caps are roughly 56px for homepage hero, 52px for service H1, 37px for section H2 and 22px for card H3.
- Phone ranges are roughly 31–38px hero, 26–30px section heading and 16px body.
- Arabic display leading is approximately 1.38–1.45; body copy uses generous leading around 1.85.
- Standalone SVG documents cannot inherit page fonts. Their current self-contained type system embeds subsetted Plex Arabic regular/medium files from `assets/fonts/`.

Why: the product contains dense data and two scripts. Readability, line rhythm and stable rendering matter more than a fashionable display face.

### 9.4 Layout and surfaces

- Maximum page container: `--es-container: 75rem`.
- Reading width: `--es-container-reading: 45rem`.
- Use generous but bounded section spacing from the token system.
- Alternate paper and mist sections to create rhythm without excessive borders.
- Use a small number of navy sections for emphasis; the buyer-context and closing moments benefit from contrast.
- Corners are controlled, not bubbly: 0.375rem controls, 0.5rem rows, 0.75rem panels and 1rem theatres in current tokens.
- Shadows use a broad ambient layer plus a small contact layer. Avoid floating glass cards everywhere.

Copy normally occupies the narrower side of a split; the working product scene gets the wider side. A figure is allowed more space because its labels must remain readable, not because art outranks content.

### 9.5 Logos, marks and icons

- Approved primary assets live in `assets/logo/`.
- The vector Estavo mark is `assets/logo/estavo-mark.svg`.
- Use the connected Estavo mark once as the main data/brand anchor in a scene.
- The AI chat avatar uses a distinct symmetric four-point AI glyph. Do not reuse the Estavo mark as every avatar.
- Homepage art uses native, flat line icons at one shared stroke weight.
- The dimensional icons in `assets/img/icons/` are legacy/service-scene assets, not the direction for new homepage illustrations.
- The `chat` mark represents Estavo’s assistant; `messages` represents external conversations. Do not swap their meanings.

### 9.6 Photography and property imagery

Do not use a large building render, stock skyline or lifestyle photograph as the central hero idea. Property photography makes the site look like an inventory portal and says nothing about the maintained-data model.

Small property thumbnails are acceptable inside a meaningful listing or website example. Native plans, comparison tables, charts and product surfaces should carry the main explanatory load.

Existing experimental raster assets are not automatically approved merely because they are in `assets/img/`.

---

## 10. Illustration system

The governing sentence is:

> **Every graphic is an argument about the product, drawn from real product structure.**

If removing a graphic loses no meaning, the graphic is decoration and should be redesigned.

### 10.1 Composition logic

| Scene | What it must demonstrate |
|---|---|
| Homepage hero | One maintained project-data source feeding two products: Market and Sites; Client AI appears inside the Sites experience, not as a third product. |
| Market explorer | A searchable broker marketplace with comparable inventory, not generic cards. |
| Market updates | Change events entering one review workflow and becoming a current record. |
| Brand unified | A brokerage website containing/connecting the assistant and current data. |
| AI conversation | Buyer question, useful clarification and matching property results. |
| Client context | Lead identity plus stated preferences and observed journey becoming a pre-call brief. |
| ROI | Price history, purchase inputs and inflation informing a real-return/sell-or-hold conversation. |
| Meta signals | Website events becoming an audience input, without a performance promise. |
| Listings reach | Broker-entered unit moving through controlled publishing/network steps. |
| Pricing/enterprise | Shared Estavo foundation connected to readable service selection. |

Adjacent scenes should not all share the same silhouette. Common materials create family resemblance; composition should follow the task.

### 10.2 Desktop/mobile contract

Every major homepage illustration has two compositions:

- desktop SVG: usually `1024×640`, with a larger `1024×900` hero stage;
- mobile SVG: purpose-built at `390×430`.

Never shrink the desktop scene onto a phone. Mobile preserves the argument while removing repeated fields, shortening labels and changing geometry so text remains legible.

Useful mobile structures include radial hubs, converging sources and a single compact workspace. A vertical list with a decorative line is not a diagram.

### 10.3 Product-scene rules

- Draw recognizable structures: comparison rows, a client brief, a floor plan, calculation inputs, a browser-hosted brokerage website, or a chat exchange.
- Browser chrome is only used when “this is the broker’s website” carries meaning. Do not add generic three-dot window bars to every surface.
- Keep controls inside a depicted product. Diagram nodes outside it must not look tappable.
- Use one visual example label at the component level.
- Keep request and result content consistent.
- Make connector endpoints visible and attached.
- Scope SVG gradient/filter IDs per instance.
- Do not embed raster fills or require a third-party animation player.

### 10.4 Hero specifics

The hero composition contains:

- one large maintained project surface as the anchor;
- an integrated navy floor plan;
- a restrained open blue orbit/connection system;
- two recognizable product destinations: an Estavo Market comparison surface and an Estavo Site under the customer's brand;
- Client AI shown inside or attached to the Site surface, so it reads as a Sites capability rather than a third main product.

The record shows only key attributes and grouped output ports. Do not add a dense form, repeated room counts or captions that compete with the destinations. The Sites destination should read as a brokerage homepage with property search and its Client AI, not a single-unit advertisement. The Market destination should read as a searchable broker marketplace with comparable inventory, not a dashboard of invented metrics.

For the full geometry, content and animation constraints, `DESIGN-GUIDELINES.md` is authoritative.

---

## 11. Motion

Motion explains relationships and gives the product surfaces quiet life. It must never become the proposition.

### Approved motion layers

1. **Section entrance:** subtle fade/translate/scale when a section enters the viewport.
2. **Composition drift:** a connected scene moves as one group by only a few pixels over 12–14 seconds.
3. **Connection energy:** a soft luminance sweep travels over an always-visible solid connection.
4. **Meaningful local state:** typing dots or a selected state may pulse.
5. **Pointer depth:** a very small camera movement on fine-pointer devices only.

Do not use marching dashes, flying packets, constant icon motion, spinning logos, exaggerated parallax or animation that detaches a connector from its node.

Every animated SVG needs a complete `*-still.svg` companion. HTML selects the still asset under `prefers-reduced-motion: reduce`. Reduced motion must restore visible end states; cancelling an entrance while it is at `opacity: 0` is a failure.

The page must remain complete and usable with JavaScript disabled. `assets/js/v3/estavo-v3.js` is progressive enhancement only.

---

## 12. Interaction, accessibility and privacy

### Baseline requirements

- Exactly one H1 per page.
- A skip link appears before navigation.
- Semantic headings preserve reading order.
- Decorative illustrations are `aria-hidden="true"` or use empty `alt` text.
- Product meaning must also exist in adjacent prose; do not make an SVG the only source.
- All images declare intrinsic width and height.
- Keyboard focus is visible.
- Menus, drawers, tabs, prepared examples, FAQs and carousels retain keyboard semantics.
- The mobile drawer traps focus while open and returns it to its trigger.
- The full experience works at 320px without horizontal scrolling.
- English pages stay on English routes and Arabic pages stay on Arabic routes until the visitor switches language.

### RTL

- Use logical properties for flow, but measure the result; assumptions about start/end have caused real wrong-side bugs.
- Use explicit grid areas for positional diagrams.
- Remember that the first grid track is visually rightmost in RTL.
- Isolate Latin text in Arabic with `<bdi>`.
- Avoid a two-line label beside a single-line sibling where the grid expects equal rhythm.

### Analytics and privacy

`assets/js/v3/estavo-v3.js` tracks categorical UI events. It must never send raw buyer requests, field values, names, contact details or other identifying content.

Existing event vocabulary includes:

- `market_opened`
- `website_preview_started`
- `service_selected`
- `coverage_viewed` (legacy analytics name; avoid “coverage” in public copy)
- `ai_demo_completed`
- `integration_enquiry_submitted`
- `listing_flow_started`
- `pricing_city_selected`
- `prepared_sample_changed`
- `report_opened`
- `whatsapp`

Reuse a semantically correct event before inventing a near-duplicate. Add only categorical, non-identifying properties such as position, language or prepared-example key.

---

## 13. Technical source of truth

The site is static HTML with dependency-free build utilities. There is no package manifest or framework runtime.

### Edit these sources

| Concern | Source of truth |
|---|---|
| Shared route names, metadata, CTAs, contact/social data | `tools/routes.json` |
| Service-page body copy | `tools/pages/*.ar.html`, `tools/pages/*.en.html` |
| Shared service header/footer | `tools/partials/header.*.html`, `tools/partials/footer.*.html` |
| Design tokens | `assets/css/v3/tokens.css` |
| Component/layout/motion styles | `assets/css/v3/*.css` |
| Page behavior | `assets/js/v3/estavo-v3.js` |
| Illustration generation | `tools/build-illustrations.py`, `tools/build-home-illustrations-v2.py` |
| Illustration translation strings | `tools/illustration-copy-en.json`, `tools/illustration-mobile-copy-en.json` |
| Homepage published copy/layout | `index.html`, `en.html` |
| Detailed visual rules | `DESIGN-GUIDELINES.md` |
| Planned commercial-page expansion and claims gate | `COMMERCIAL-SERVICE-PAGES-PLAN.md` |
| Page-level copy, conversion and art briefs | `commercial-page-briefs/README.md` and its six linked briefs |
| Static publication checks | `tools/qa.js` |

### Generated outputs—do not hand-edit

- `assets/css/estavo-v3.css` is concatenated from `assets/css/v3/*.css`.
- Service outputs in `data/`, `market/`, `websites/`, `ai/`, `integrations/`, `marketing/`, `insights/`, `listings/`, `enterprise/`, `pricing/` and `examples/` are generated from `tools/pages/` plus shared partials.
- Most `assets/img/estavo-*.svg` files are generated by the illustration builders.
- `tools/partials/critical.css` and the inline critical styles are refreshed from the source modules by the premium refresh process.

If an output must change, find and change its source first. A direct edit will be lost during the next build and can create language drift.

### Route and repository boundaries

The current v3 marketing system consists of two homepages plus 22 generated service pages:

- `/index.html` and `/en.html` are the Arabic and English homepages;
- each of the 11 service directories in the route table contains Arabic `index.html` and English `en.html`.

Other files in this repository have related but different responsibilities:

- `/websites/` is the marketing page that explains the branded website service;
- `/website/` is the actual website-creation/onboarding experience, supported by `assets/css/website-wizard.css`, `assets/js/website-referral.js` and its own server-side/manual-profile flow;
- `go/` and `go.php` are referral/redirect infrastructure, not marketing-content templates;
- `privacy*`, `terms*`, `data-deletion*` and Google Calendar pages are legal or integration-support pages;
- `404.html` is the error route;
- `index.old.html` and `en.old.html` are retained historical snapshots, not authoring sources;
- `estavo-brokers*.html`, `what-is-estavo-brokers*.html` and other older standalone pages are outside the generated v3 service-page shell unless a task explicitly brings them into scope.

Do not assume that a similarly named directory is interchangeable. In particular, never send “create my website” traffic to the `/websites/` explainer when the promised action is the `/website/` flow or the configured referral URL.

### SEO and sharing contract

- Every public content page has one descriptive title and meta description in its own language.
- Arabic is the directory/default route; English uses `en.html`.
- Canonical URLs and `hreflang` pairs must stay aligned, including `x-default`.
- Open Graph and Twitter metadata reuse the page’s approved proposition and the language-specific `assets/og/og-ar.jpg` or `og-en.jpg` image.
- Structured data is subject to the same evidence rules as visible copy. Never add invented prices, ratings, availability or aggregate reviews to JSON-LD.
- `sitemap.xml`, `robots.txt` and `site.webmanifest` are publication assets; update them when a route or public identity changes.
- Keep page descriptions concrete. They should name the information and task, not repeat generic brand language.

The page builder escapes titles/descriptions before inserting them into markup. Preserve that behavior; raw ampersands or quotes in `<title>` and metadata can make the document invalid.

### Build order

Use only the steps relevant to the change, in this dependency order:

```sh
# Rebuild vector illustration families when their source changed.
python3 tools/build-illustrations.py
python3 tools/build-home-illustrations-v2.py

# Install/refresh generated art and shared critical treatment.
python3 tools/refresh-home-illustrations-v2.py
python3 tools/refresh-premium-design.py

# Regenerate the 22 bilingual service outputs after templates,
# routes, partials or shared critical CSS changed.
node tools/build-pages.js

# Rebuild the production stylesheet after any CSS module change.
sh tools/build-css.sh

# Run the static publication gate.
node tools/qa.js
```

Some illustration builds require `fonttools` and `brotli`. Do not rewrite a working generator merely to avoid installing its documented build dependency.

Serve the root for reliable previewing:

```sh
sh tools/serve.sh 8731
```

Then use `http://127.0.0.1:8731/`. Subdirectory pages and root-style asset paths are not reliably represented by arbitrary `file://` previews.

---

## 14. Agent workflow

### Before changing content

1. Identify the audience and job.
2. State the claim the section or page needs to make.
3. Identify which source file owns the copy.
4. Check both languages and the matching route metadata.
5. Check whether the claim needs commercial/data approval.
6. Decide the CTA and verify that its destination exists.

### Before changing visuals

1. Write the product argument in one sentence.
2. Identify the real product structure that can demonstrate it.
3. Design desktop and mobile as separate compositions.
4. Plan the still/reduced-motion state at the same time as motion.
5. Confirm whether the asset is generated and edit its generator.
6. Re-read `DESIGN-GUIDELINES.md` for the exact figure constraints.

### Before changing structure or code

1. Preserve no-JavaScript readability.
2. Preserve route/language pairing, referral propagation and analytics semantics.
3. Edit modules/templates, not generated artifacts.
4. Rebuild in dependency order.
5. Test the changed surface and all generated dependants.

### Definition of done

- The page still communicates the maintained-data foundation.
- Copy names a real customer task and does not overclaim.
- Arabic and English preserve the same truth and destination.
- Every example is visibly labelled and internally consistent.
- No invented prices, availability, performance or intent appears.
- The CTA label matches its destination.
- Desktop and mobile art remain legible and semantically equivalent.
- Reduced motion, keyboard use and no-JavaScript reading work.
- No horizontal overflow exists at 320px.
- The changed pages pass `node tools/qa.js`.
- Screenshots were visually reviewed, not only measured.

---

## 15. Required visual QA matrix

Render the affected pages at:

- desktop: 1280, 1440, 1512 and 1728px;
- mobile: 390, 360 and 320px;
- both Arabic/RTL and English/LTR;
- ordinary motion and `prefers-reduced-motion: reduce`.

Check:

- desktop hero stays within one fold where intended;
- figure width remains inside its grid track;
- type is not clipped, especially Arabic punctuation/descenders;
- labels remain readable at rendered size;
- connectors terminate at their subjects;
- no product illustration appears tappable unless it truly is;
- lazy loading does not delay the hero/LCP asset;
- below-fold reveal still works when reached later;
- content remains visible with JavaScript disabled and when printed;
- all SVGs parse and render, including still companions;
- the page has no horizontal scroll at 320px.

Use `tools/shot.js` and `tools/measure.js` when appropriate. Measurements confirm constraints; screenshots decide whether the composition actually reads.

---

## 16. Anti-patterns and the reason behind them

### Generic proptech hero

**Do not:** use a skyline, glass tower, smiling agent, glowing globe or abstract AI brain.

**Why:** it could belong to any company and hides Estavo’s actual differentiator—the maintained data flowing into the broker’s chosen surface.

### Feature-card wallpaper

**Do not:** turn every idea into a bordered icon card.

**Why:** repeated card anatomy makes the page feel like a menu and prevents the visitor from seeing relationships or workflow.

### Dashboard theatre

**Do not:** fill screens with decorative charts, fake totals and generic window chrome.

**Why:** specificity builds trust only when the interface demonstrates a real task. Unverified numbers actively damage trust.

### Shrunk desktop diagrams

**Do not:** scale a 1024px SVG until it technically fits 390px.

**Why:** labels become illegible and the hierarchy collapses. Mobile requires a new composition.

### AI overclaiming

**Do not:** call buyers qualified, imply purchase readiness, or present AI answers beyond available data.

**Why:** observed behavior and available data do not justify those conclusions.

### Literal bilingual copying

**Do not:** translate word for word or force the same line breaks.

**Why:** English and Arabic have different rhythm, direction and professional idiom. They need equivalent meaning, not identical syntax.

### Generated-file patches

**Do not:** fix only a published service HTML file or bundled stylesheet.

**Why:** the next generation step will erase the change and reintroduce drift.

### Motion as decoration

**Do not:** animate all icons or send dashed packets around the page.

**Why:** it competes with reading, makes the product feel less credible and creates accessibility debt.

---

## 17. Decision hierarchy when instructions conflict

Use this order:

1. Verified product/commercial truth and legal/privacy obligations.
2. Accessibility and correct bilingual behavior.
3. This handbook’s brand and content strategy.
4. `DESIGN-GUIDELINES.md` for detailed visual implementation.
5. `tools/routes.json`, templates and source modules for current implementation facts.
6. Existing generated output.

If implementation and this handbook disagree because the product has changed, update the source implementation and this document together. Do not quietly preserve a known contradiction.

---

## 18. Final test for any new idea

Before shipping, an agent should be able to answer all five questions in one short paragraph:

1. Which broker problem does this solve?
2. Which maintained information or product workflow makes it possible?
3. Why is this under the customer’s control or brand?
4. What is the honest boundary of the claim?
5. What exact action should the visitor take next?

If those answers are vague, the idea is not ready for the site.
