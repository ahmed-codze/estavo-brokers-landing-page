# Landing Page Brief — Meta Integration for Estavo Sites

## Route and conversion

- Arabic route: `/meta/`
- English route: `/meta/en.html`
- Product: Estavo Sites
- Capability: Meta integration
- Primary conversion: `https://estavo-brokers.com/website/`
- Primary event: `website_preview_started`
- Optional categorical event after implementation: `meta_integration_selected`

The primary action creates/configures an Estavo Site. Use “Connect Meta” only when the resulting `/website/` flow genuinely reaches that configuration step.

## Why this page exists

The page explains the connection between property-specific activity on an Estavo Site and the customer's own Meta account. It exists separately because account ownership, permissions, privacy and advertising boundaries need more explanation than a homepage section can carry.

Estavo is not positioned as a marketing agency or media buyer.

## Audience

- Freelance broker running Meta ads.
- Brokerage marketing team.
- Company working with an external agency/media buyer.
- Existing Estavo Site owner who wants clearer property-event context.

## Core proposition

Arabic:

> اربط رحلة العميل على موقعك بحساب Meta بتاعك.

English:

> Connect the buyer journey on your website to your own Meta account.

## Hero

### Arabic

- Eyebrow: `Meta مع Estavo Sites`
- H1: `خلّي Meta يعرف العميل شاف مشروع إيه أو اختار منطقة إيه على موقعك.`
- Lead: `ابدأ موقعك باسمك، وبعدها ابعت تفاعلات واضحة—زي مشاهدة مشروع أو طلب تواصل—لحسابك على Meta. الحساب والميزانية والقرار يفضلوا عندك.`
- CTA: `اعمل موقعك واربط Meta`
- Supporting note: `إستاڤو مش وكالة إعلانات، وحسابك وميزانيتك يفضلوا تحت تحكمك.`

### English

- Eyebrow: `Meta with Estavo Sites`
- H1: `Let Meta know which project a buyer viewed or which area they selected on your website.`
- Lead: `Start your website under your name, then send clear events—such as a project view or contact request—to your Meta account. The account, budget and decisions stay yours.`
- CTA: `Create your site and connect Meta`
- Supporting note: `Estavo is not a media-buying agency. Your account and budget remain under your control.`

### Hero art

One brokerage website produces named property events. They pass through a visible consent/permission gate into a customer-owned Meta surface.

Use example events only if implemented:

- project viewed;
- area selected;
- property compared;
- contact submitted.

No fake reach, cost, conversion or performance charts.

## Page sections

### 1. مش مجرد Page View

Explain the difference between a generic visit and a permitted event with property context. The copy should describe additional structure, not claim the site “understands” a person's private intent.

English: `More context than a generic page view.`

### 2. الحساب والـ Assets بتوعك

State that the Meta Business, dataset/pixel and Ad Account belong to the customer. Connection does not transfer ownership to Estavo.

English: `Your Meta account remains yours.`

### 3. اشتغل مع الـ Agency أو Media Buyer بتاعك

The existing partner can continue to manage campaigns. Estavo supplies the approved connection/events; it does not replace daily campaign management.

English: `Keep the agency or media buyer you already work with.`

### 4. Audiences من سياق عقاري واضح

Subject to implementation and consent, organize audiences using transparent context such as selected area, viewed project or property type.

Do not use “people truly interested,” “qualified,” “high intent” or secret scoring.

English: `Build audiences from transparent property context.`

### 5. اعمل إعلان من الوحدة—لو الـ Workflow متاح

Include this section only after the direct-publishing flow is confirmed live.

Explain:

- customer selects a property already on the Site;
- customer chooses the permitted audience and budget;
- the ad is created/published through the connected account;
- Estavo does not spend or optimize autonomously.

English: `Move from a property on your site to an ad in your account.`

### 6. Signals قبل وبعد التواصل

Show an event timeline. A later sales-stage event must come from an explicit team/system status—not an inference from views. Never send raw chat text or sensitive/free-form buyer data in analytics parameters.

English: `Use explicit journey stages—not guessed intent.`

### 7. إستاڤو مش Marketing Agency

Clear boundary panel:

- no daily optimization;
- no autonomous budget decisions;
- no guaranteed leads or sales;
- campaign outcome also depends on creative, offer, budget, follow-up and market conditions.

English: `The connection supports your marketing team; it does not replace it.`

### 8. الخصوصية والموافقة

This is a full content section, not a footer note. Explain in plain language:

- what event categories can be sent;
- when consent/notice applies;
- who owns account permissions;
- minimum necessary data;
- retention/deletion route;
- no raw buyer conversation or phone number in event properties.

Final wording requires privacy/legal review.

### 9. FAQ

Recommended questions:

1. `الـ Meta Account بيكون بتاع مين؟`
2. `عندي Pixel وAgency بالفعل—ينفع يفضلوا؟`
3. `هل لازم أربط Meta عشان الموقع يشتغل؟`
4. `إيه نوع الأحداث اللي بتتبعت؟`
5. `هل Estavo بتدير الـ Campaigns والميزانية؟`
6. `هل الربط يضمن Leads أو مبيعات أفضل؟`
7. `أقدر أعمل إعلان من Estavo؟`
8. `هل Google Ads مدعوم؟`—publish the answer only after current product confirmation.

### 10. Closing conversion

- Arabic H2: `ابدأ بموقع يفهم سياق العقار، ويربطه بحسابك.`
- English H2: `Start with a property site that can connect meaningful events to your account.`
- CTA: `اعمل موقعك واربط Meta / Create your site and connect Meta`
- Destination: `/website/`.

## Visual system

- Sequence: Site → consent/permission gate → normalized events → Meta surface.
- Estavo navy/blue controls the data route.
- Official Meta color appears only in its mark or recognizable interface chrome.
- Motion: one soft sweep across an always-visible solid route.
- Mobile: three-event stack converges into one permission gate and one Meta output.

## SEO

- Arabic title direction: `ربط موقعك العقاري بـ Meta — Estavo Sites`
- English title direction: `Connect your property website to Meta — Estavo Sites`
- Description should state customer-owned account, property event context and no agency/performance guarantee.

## Claims requiring approval

- exact Meta products/assets connected;
- direct ad publishing;
- supported campaign objectives;
- audience creation/update behavior;
- events visible in Estavo admin;
- post-lead stage signals;
- included price/setup support;
- Google Ads support status;
- consent, data minimization, retention and deletion language.

## Acceptance criteria

- The page belongs clearly to Estavo Sites.
- The customer owns the Meta account, audience choice and budget.
- Privacy/consent is a first-class section.
- No inferred intent or performance promise appears.
- The primary CTA goes to `/website/`.
- Unconfirmed ad-publishing UI is not shown as live.
