# Estavo Commercial Landing-Page Briefs

These documents are the page-level content, conversion and art briefs for Estavo's two-product commercial architecture.

They are derived from:

- the current Arabic and English landing pages;
- `AGENTS.md`;
- `DESIGN-GUIDELINES.md`;
- `COMMERCIAL-SERVICE-PAGES-PLAN.md`;
- the Estavo Brokers, Sites, AI and Meta/Integrations FAQ documents supplied by the product owner.

The FAQ documents are source material, not publish-ready instructions. Every exact commercial claim still follows the validation notes in the relevant brief.

## Implementation prompt

Use [IMPLEMENTATION-PROMPT.md](IMPLEMENTATION-PROMPT.md) as the complete copy-paste task for the agent that will build the pages.

## Product architecture

```text
Homepage
├── Estavo Market
│   └── 01 — Market for brokers
│       └── All primary CTAs → brokers.estavo.space
│
└── Estavo Sites
    ├── 02 — Website for freelance brokers
    ├── 03 — Website for brokerage companies
    ├── 04 — AI for website clients
    ├── 05 — Meta integration
    └── 06 — Broker-network property distribution
        └── All primary CTAs → estavo-brokers.com/website/
```

## Brief index

| Brief | Public route | Product | Conversion destination |
|---|---|---|---|
| [01 — Estavo Market](01-estavo-market.md) | `/market/`, `/market/en.html` | Estavo Market | `https://brokers.estavo.space/go/?ref=default-landing-page-market` |
| [02 — Sites for freelancers](02-sites-freelancers.md) | `/websites/`, `/websites/en.html` | Estavo Sites | `https://estavo-brokers.com/website/` |
| [03 — Sites for companies](03-sites-companies.md) | `/enterprise/`, `/enterprise/en.html` | Estavo Sites | `https://estavo-brokers.com/website/` |
| [04 — Client AI](04-sites-client-ai.md) | `/ai/`, `/ai/en.html` | Estavo Sites | `https://estavo-brokers.com/website/` |
| [05 — Meta](05-sites-meta.md) | `/meta/`, `/meta/en.html` | Estavo Sites | `https://estavo-brokers.com/website/` |
| [06 — Broker network](06-sites-broker-network.md) | `/listings/`, `/listings/en.html` | Estavo Sites | `https://estavo-brokers.com/website/` |

## Shared page requirements

Every page must:

- make its product family explicit in the hero;
- contain one H1 and one dominant conversion action;
- send the primary CTA to the destination listed above;
- work in Arabic/RTL and English/LTR;
- use Cairo and the established navy/blue/paper visual system;
- use a product-specific desktop illustration and a separately composed mobile illustration;
- include a complete reduced-motion/still state;
- label illustrative examples visibly;
- avoid invented inventory, price, ROI, reach or advertising results;
- remain readable and actionable without JavaScript;
- pass `node tools/qa.js` after implementation.

## Shared CTA behavior

### Market pages

Use free, immediate language. Examples:

- جرّب <bdi>Estavo Market</bdi> مجانًا
- افتح السوق مجانًا
- Try Estavo Market free
- Start searching free

All primary actions go directly to the configured `brokers.estavo.space` referral URL.

### Sites pages

Use capability-specific language, but always begin the same Site-creation flow:

- اعمل موقعك مجانًا
- ابدأ موقع شركتك
- فعّل الـ AI على موقعك
- اربط موقعك بـ Meta
- اعرض وحداتك لشبكة البروكرز

All primary actions go to `https://estavo-brokers.com/website/`.

## Shared section rhythm

1. Outcome-led hero.
2. Recognizable customer problem.
3. Product workflow.
4. Included capabilities.
5. Control, scope and responsibility.
6. Commercial explanation.
7. Focused FAQ.
8. Repeated primary action.

The sequence is shared; the visual composition and argument must differ by page.
