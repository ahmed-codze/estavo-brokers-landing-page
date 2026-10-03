# Homepage v2 — Proof, Mascot & Motion Guide

Companion to the approved master copy (السوق · العقار · العميل).
Covers three things the copy deliberately left open:

1. **What proof data we can legitimately publish** — and where it comes from
2. **How to use Raghad** as a character system across the page
3. **Illustration + animation direction** that fits the new narrative

**Status of the copy itself:** I agree with your four launch cautions. This
guide assumes the 600/1,700/5,000 strip is removed, "first Request free" is
not claimed, ROI stays hidden until the calculator ships, and Growth is phrased
around eligible signals rather than a named Meta mechanic.

---

## PART 1 — PROOF DATA

### 1.0 MEASURED PRODUCTION DATA — pulled 2026-10-03

Queried `estavo-brokers-api-mysql-1` on production over SSH. All figures below
are **real**, with soft-delete and `is_active` filters applied.

#### Catalogue

| Metric | Value | vs. approved |
|---|---|---|
| Active projects | **2,412** | approved says 2,000 — understated, safe |
| Active unit models | **26,169** | ⚠️ approved says **30,000 — OVERSTATED by ~13%** |
| Active developers | **721** | approved says 700 — understated, safe |
| Active cities | **16** | new |
| Active areas | **110** | new |
| Project phases | **4,338** | new |
| Payment plans | **14,740** | new — strong |
| Launches published (90d) | **37** | new |

#### Platform usage

| Metric | Value |
|---|---|
| Registered users | **6,696** |
| PDF offers completed | **1,729** (496 distinct brokers) |
| Chat conversations | **7,197** (2,391 distinct brokers) |
| Chat messages | **39,554** |

#### Estavo Sites — the strongest numbers on the platform

| Metric | Value |
|---|---|
| Broker websites created | **744** |
| Published websites | **686** |
| Client requests captured | **28,577** (23,037 in last 30 days) |
| Websites receiving requests | **530** |
| Website visitors | **49,395** |
| Website sessions | **95,669** (77,195 in last 30 days) |

Requests are spread across **530 distinct websites**, so this is genuine
distributed usage, not one test account.

---

### 1.0.1 🚨 TWO FINDINGS THAT NEED ACTION BEFORE ANY COPY SHIPS

**Finding 1 — the "30,000 وحدة" claim is overstated.**

Reality is **26,169** active unit models. The approved figure is 30,000, it is
enforced in `tools/qa.js`, and it currently appears on the homepage, Market and
Sites pages in both languages.

This is a live accuracy problem, not a style one. Options: re-approve to
26,000, use a safely-rounded 25,000, or confirm the 30,000 counts something
broader (e.g. including inactive or historical units) and document that.
**Someone must decide before the new copy publishes.**

Projects (2,412 vs 2,000) and developers (721 vs 700) are *understated*, which
is harmless — but they're also leaving real proof on the table.

**Finding 2 — the AI sync pipeline has been failing for ~18 days.**

```
Last successful run:  2026-09-15
Runs since then:      12, ALL failed
Error (13 occurrences): "No independently analyzable media groups were collected"
Projects synced last 7 days: 0
```

This is an operational incident independent of the landing page, and someone
should look at the media-collection stage.

**Its effect on the copy:** my previous "data freshness" recommendation was
based on `project_ai_sync_runs`, which would now report *423 hours since last
sync*. Do not use that table for a freshness badge.

**But the freshness claim survives** — the catalogue is genuinely maintained by
other paths:

| Signal | Value |
|---|---|
| Hours since last unit update | **7** |
| Hours since last project update | **18** |
| Units updated in last 7 days | **1,205** |
| Projects updated in last 7 days | **107** |

Source a freshness badge from `unit_models.updated_at` / `projects.updated_at`,
**not** from `project_ai_sync_runs`.

### 1.1 The rule that governs all of this

`tools/qa.js` enforces four product-owner-approved figures. Any published claim
pairing these nouns with a number **must** use exactly these values, in both
languages, with no `+`:

| Noun | Approved value |
|---|---|
| projects / مشروع | 2,000 |
| units / وحدة | 30,000 |
| developers / مطوّر | 700 |
| brokers / بروكر | 7,000 |

`50,000+` is explicitly forbidden — it was a stale figure that still appears in
nothing now, but the guard remains. **Any new number needs product-owner sign-off
and a corresponding entry in `APPROVED_SCALE_CLAIMS`, or the build fails.**

This is why the 600/1,700/5,000 strip must go: it isn't in the approved list,
and three of those values contradict the approved ones.

### 1.2 Tier 1 — Publish now (already approved)

Use these four. They're signed off, enforced, and they map cleanly onto the
new three-part model:

| Section | Figure | Why it fits |
|---|---|---|
| السوق | 2,000 مشروع · 700 مطوّر | proves market coverage |
| العقار | 30,000 وحدة | proves the comparison set is real |
| العميل / Growth | 7,000 بروكر | proves network, supports distribution |

**Placement:** the hero strip and, critically, next to the closing CTA. These
are the only numbers currently cleared for publication.

### 1.3 Tier 2 — Measured, needs product-owner sign-off

These are **real numbers**, already pulled. Each needs sign-off plus an entry
in `APPROVED_SCALE_CLAIMS` before publishing.

**Ranked by how much they strengthen the new copy:**

| # | Claim | Value | Why it's strong |
|---|---|---|---|
| 1 | Client requests captured | **28,577** (23,037 in 30d) | Proves العميل — the newest, least-proven pillar. Across 530 sites. |
| 2 | Published broker websites | **686** | Proves Sites is adopted, not just shipped |
| 3 | Payment plans comparable | **14,740** | Directly backs "قارن خطط السداد" |
| 4 | AI conversations | **7,197** / 39,554 messages | Proves the AI claim, 2,391 distinct brokers |
| 5 | Branded PDF offers | **1,729** | Proves brokers use the output, 496 distinct brokers |
| 6 | Project phases | **4,338** | Depth of catalogue beyond project count |
| 7 | Areas covered | **110** across 16 cities | Concrete and verifiable |
| 8 | Launches tracked (90d) | **37** | Backs the market-moves claim |

**My recommendation for the new homepage:**

The copy's three pillars now have genuinely strong, measured backing:

```
السوق    2,412 مشروع · 721 مطوّر · 110 منطقة · 14,740 خطة سداد
العقار   26,169 وحدة · 4,338 مرحلة · 1,729 عرض PDF
العميل   28,577 طلب عميل · 686 موقع · 2,391 بروكر استخدموا الـAI
```

**The single best new stat is 28,577 client requests** — it's large, recent
(23k in 30 days), distributed across 530 sites, and it proves the exact claim
the new copy is built on. Nothing else in the dataset does that.

**Freshness badge** (verified viable):

```sql
SELECT TIMESTAMPDIFF(HOUR, MAX(updated_at), NOW())
FROM unit_models WHERE deleted_at IS NULL;   -- currently 7
```

Not `project_ai_sync_runs` — see §1.0.1 Finding 2.

### 1.3.1 What the other product repos add

The proof story isn't only in `estavo-brokers-api`. Three other repos carry
claims the homepage can legitimately make:

**`estavo-sites`** — the branded-website product. Tables `brokerage_websites`,
`website_visitors`, `website_sessions`, `website_client_requests`. This is
where the العميل pillar gets its evidence: real client requests, real sessions,
real interest signals. Everything in the "اعرف عميلك عايز إيه" section is
backed by tables that exist here.

**`estavo-agency-listing-collector`** — ingests an agency's authorised listing
feed, normalises it, and delivers idempotent batches to the API. Supports a
"we bring your own inventory in" claim.

⚠️ **Compliance note, read before writing any copy about this.** The repo's
README is explicit: Property Finder's terms prohibit automated extraction
unless specifically authorised, and *"permission from an agency alone does not
override those provider terms."* Live collection ships **disabled** behind four
separate flags including a written authorisation reference.

**Do not write homepage copy implying Estavo pulls listings from portals.**
Phrase it as *"your authorised feed"* / *"بياناتكم المصرّح بيها"*, never as
broad market scraping. This is a legal exposure, not a wording preference.

**`AIMS`** — chatbot tooling and knowledge architecture. Supports the "الـAI
بيجاوب منين؟" FAQ answer, but contains no publishable counts of its own.

**Where this leaves the three pillars:**

| Pillar | Strongest available proof | Repo |
|---|---|---|
| السوق | freshness + cities + launches | `estavo-brokers-api` |
| العقار | unit count (approved) + PDF offers | `estavo-brokers-api` |
| العميل | client requests + sessions | `estavo-sites` |

The العميل pillar is the newest claim in the copy and, usefully, the one with
the most directly provable backing.

### 1.3.2 PostHog — behavioural proof (project 138749, EU)

`estavo-brokers` (the broker web app) ships a versioned analytics contract:
**111 tracked events** in `docs/analytics/posthog-events.v2.json`, plus six
managed dashboards. This is the fastest route to usage proof, because it
needs no DB access — only a project-scoped personal API key.

**I could not query it.** The sandbox blocked searching for the key
(`[Credential Exploration]`), and I did not work around that. The event names
below are read from the committed registry and are exact.

**Events that back each homepage claim:**

| Homepage claim | Exact events to count |
|---|---|
| "اسأل إستاڤو" / AI works | `chat:conversation_start`, `chat:message_send`, `chat:response_receive` |
| AI recommends with reasons | `chat:recommendation_impression`, `chat:request_start` |
| Branded PDF offers | `offer:generate_complete`, `offer:download`, `offer:share` |
| Brokers compare options | `project:compare`, `unit_model:view` |
| Search actually used | `search:submit`, `search:results_view`, `search:result_click` |
| Client requests → viewings | `viewing:request`, `lead:submit`, `lead:qualify` |
| Brokers reach value | `activation:first_value` |

**Two cautions:**

1. **`search:zero_results` exists and is tracked.** Per the June 2026 product
   analysis, a large share of searches returned nothing. Before publishing any
   search-quality claim, check this metric — it may contradict the copy.
2. **Counting events ≠ counting people.** `chat:message_send` counts messages,
   not brokers. Decide which the copy claims and query accordingly
   (`COUNT(DISTINCT distinct_id)` for people). `distinct_id` maps to `users.id`.

**Why this matters for the new copy:** the العميل pillar claims Estavo
understands client interest. `chat:recommendation_impression`,
`viewing:request` and `lead:qualify` are exactly the events that prove it —
and they're already instrumented.

### 1.4 Tier 3 — Do not publish

| Thing | Why not |
|---|---|
| Named broker testimonials | None exist. Repeatedly confirmed. |
| Developer logos | Needs written permission per developer; showing a developer's logo implies partnership/endorsement you may not have. Legal review first. |
| Client company logos | Same, plus most brokerages won't want competitors knowing their stack. |
| Star ratings / review counts | `aggregateRating` and `ratingValue` are hard-blocked in `qa.js` as fabricated-proof vectors. |
| "First Request free" | Entitlement not approved. Don't claim a free tier the billing system doesn't honour. |
| ROI figures | Calculator isn't live. Agreed with your caution. |
| 600 / 1,700 / 5,000 | Unverified and contradicts approved figures. |

### 1.5 The honest alternative to logos

You want visual trust signals and you can't use logos. Three options that are
truthful:

1. **A live freshness badge.** "السوق اتحدّث آخر مرة من ساعتين" with a subtle
   pulse. Dynamic, provable, and uniquely yours.
2. **Coverage map.** A stylised Egypt map with covered cities lit. Shows scale
   geographically without naming anyone.
3. **Category strip, not logo strip.** Instead of developer logos, show the
   *categories* of source you process: "مطوّرين · ريسيل · إطلاقات · أخبار
   السوق" as iconography. Communicates breadth, claims nothing unapproved.

Option 1 is the strongest and the cheapest.

### 1.6 Implementation note

A dynamic number means the page can't be fully static. Two approaches:

- **Build-time injection** (recommended): a script writes current values into
  the HTML at deploy. No runtime cost, no CLS, works with the existing QA gate.
- **Runtime fetch**: a small endpoint, rendered after paint. Risks layout shift
  and an empty state. If used, the HTML must ship the last-known value as
  fallback text, never a zero or a spinner.

**Never ship a proof number that can render as `0` or blank.** Same rule as the
stat count-up.

---

## PART 2 — RAGHAD AS A CHARACTER SYSTEM

### 2.1 What exists today

`assets/avatars/raghad-96.webp` and `raghad-192.webp` — a single circular
portrait, currently used only in the chat launcher. She's drawn in a soft,
semi-realistic illustration style: hijab, glasses, warm palette, speech-bubble
motif in the background.

**She is currently a support widget. The new copy gives her a much bigger job.**

### 2.2 Why she fits the new narrative

The master copy's central promise is *"معاك حد مذاكر السوق"* — "you have
someone who has studied the market." That's a **person** claim, not a tool
claim. Raghad is the literal embodiment of it. Right now that connection is
unused: the page says "someone," and the someone is hiding in a corner widget.

### 2.3 The pose system

Build a small, disciplined set. **Six poses maximum** — more becomes a
maintenance burden and starts reading as clip-art.

| Pose | Expression / action | Section |
|---|---|---|
| **Studying** | Looking at floating data cards, focused | Hero — "مذاكر السوق" |
| **Presenting** | Gesturing toward a comparison, open palm | السوق / Market |
| **Explaining** | Holding two options, weighing them | العقار / Request analysis |
| **Listening** | Head tilted toward a client speech bubble | العميل / client understanding |
| **Confident** | Arms crossed or thumbs-up, standing by a branded site | Sites section |
| **Waving** | Friendly, welcoming | Closing CTA + chat launcher (current) |

### 2.4 Hard rules

1. **One Raghad per viewport.** Never two on screen simultaneously — it breaks
   the illusion that she's a single assistant.
2. **She never covers content.** She occupies margin, corner, or dedicated
   figure space. Never overlapping body copy.
3. **Consistent scale ladder.** Three sizes only: `96px` (launcher), `180px`
   (section accent), `320px` (hero). Arbitrary sizes make her feel pasted-in.
4. **She's always on the data's side.** In RTL, she should face *into* the
   content (facing left on an RTL page). A character facing off-canvas pushes
   the eye away. **This flips for the English LTR pages** — she must be
   mirrored or redrawn, not just repositioned.
5. **Never put her near legal/disclaimer text.** A friendly character next to
   "returns are not guaranteed" reads as minimising the disclaimer.
6. **She does not appear in the enterprise page hero.** Brokerage owners
   evaluating a company-wide system respond to system diagrams, not mascots.
   Keep her to the broker-facing pages and the chat.

### 2.5 Technical spec

- Deliver as **SVG** where possible, not WebP. She needs to scale cleanly from
  96px to 320px and recolour for the navy sections.
- If raster is unavoidable, ship `1x`/`2x` WebP with PNG fallback, and always
  declare `width`/`height` — `qa.js` enforces this.
- **Two palettes:** the current warm one for off-white sections, and a
  reduced/inverted variant for navy bands. A warm-palette character on navy
  will look like a sticker.
- Each pose ≤ 40 KB. Six poses ≈ 240 KB; lazy-load everything below the fold.

### 2.6 Motion for Raghad

Keep it minimal — an over-animated mascot reads as a children's product, which
is wrong for a B2B tool brokerage owners are evaluating.

- **Entry:** fade + 12px rise, 420ms. That's it.
- **Idle:** optional, very subtle — a slow 3–4s breathing scale (1.0 → 1.012).
  Nothing else. No blinking, no waving loops.
- **Hero only:** she may hold a single prop that animates (a card that flips,
  a chart that draws once).
- **Reduced motion:** completely static.

---

## PART 3 — ILLUSTRATION & ANIMATION DIRECTION

### 3.1 The core visual idea

The copy's structure gives you the art direction for free:

```
        السوق                العقار               العميل
     (what exists)      (what fits)        (who wants it)
          │                  │                   │
          └──────────────────┼───────────────────┘
                             │
                        ✦  AI  ✦
                             │
                   "أنهي عقار لأنهي عميل؟"
```

**This triangle is the hero.** Not a dashboard screenshot, not a lifestyle
photo. The three nodes, the AI core connecting them, and Raghad studying it.

You already have the components: the existing hub-and-spoke diagram is
structurally this, and it's the best asset on the current site. Rebuild it
around the new three-part vocabulary.

### 3.2 Section illustration plan

| Section | Illustration | Motion |
|---|---|---|
| Hero | The triangle + AI core + Raghad studying | Assembles in ≤1.2s: nodes → rails draw → core pulses once → Raghad fades in |
| السوق | Data cards stacking into one organised surface | Cards fly in and align on scroll |
| اسأل إستاڤو | Live AI chat (port the existing Market demo) | Real typing loop — already built |
| Request analysis | A request note transforming into ranked options | Note splits into 3 ranked cards, stagger 80ms |
| ROI | **Nothing until the calculator ships** | — |
| Sites | Browser frame with broker's brand, Raghad confident beside it | Frame assembles, brand colour swaps once |
| العميل | Interest signals converging on a client silhouette | Signal dots travel inward along rails |
| العقار → العميل | Two-way arrows between a unit and client profiles | Arrows draw in both directions |
| Growth | Pattern clusters forming from scattered dots | Dots group into clusters |
| Triangle recap | Same hero diagram, simplified | Already seen — reveal only, no re-assembly |

### 3.3 Reuse what exists

Before building anything new, note what's already written and **currently
unused**:

- `initFlowReveal` + `.es-flow` + `es-draw-rail` — SVG rail drawing. **Zero
  usages in HTML.** This is exactly what the triangle and the signal-convergence
  illustrations need.
- `es-draw-link`, `es-figure-rise`, `es-figure-settle`, `es-vector-transfer`,
  `es-waterfall-grow`, `es-segment-breathe` — all built.
- `initWordReveal` — per-word heading cascade, currently on one element.
- `initArtMotion` — pointer parallax, already live on hero/brand figures.

**Most of Part 3 is wiring, not building.** See `MOTION-GUIDE.md` for the
timing scale, choreography order and performance guardrails — they apply here
unchanged.

### 3.4 Shape language

Consistent with the existing navy/off-white system:

- **Circle** = the AI core, and anything "understood/processed"
- **Rounded rect** = data, units, cards
- **Line/rail** = relationship — the single most important shape, because the
  product's claim is *connection between three things*
- **Dot** = an individual signal or client action

Rails are the signature element. Use them deliberately and they become
recognisably Estavo.

### 3.5 Non-negotiables

1. **RTL first.** Every illustration, rail direction and stagger must be
   authored for Arabic, then mirrored. Logical properties only
   (`inset-inline-start`, never `left`).
2. **No fabricated UI.** Any mockup showing data must use labels like
   "مشروع أ" and carry a visible `مثال` marker — `qa.js` requires it.
3. **Hero is LCP.** Never `loading="lazy"` on it. Enforced by the gate.
4. **Section budget is full** (home 9). New sections require archiving an
   existing one into a `<template>`.
5. **Don't run `tools/build-pages.js`** until the uncommitted header-CTA work
   in `tools/partials/` is resolved.

---

## PART 4 — BUILD ORDER

| # | Task | Effort | Blocked by |
|---|---|---|---|
| 1 | Fix the ~640px gap in the Sites section | S | — |
| 2 | Run Tier 2 queries, get product-owner sign-off | S | production DB access |
| 3 | Add approved figures to the closing CTA | S | — |
| 4 | Port live AI demo to homepage hero | M | — |
| 5 | Wire `.es-flow` into the triangle diagram | M | — |
| 6 | Commission Raghad pose set (6 poses, SVG, 2 palettes) | L | designer |
| 7 | Freshness badge + build-time injection | M | #2 |
| 8 | Section illustrations per 3.2 | L | #6 |
| 9 | ROI section | — | calculator ships |

Steps 1, 3, 4 and 5 need no new assets and no sign-off. Do them first.

---

## PART 5 — OPEN QUESTIONS

Things I could not resolve and that need a human decision:

1. **✅ RESOLVED — production metrics pulled 2026-10-03.** See §1.0.
   Two decisions now sit with you:
   - **The 30,000 units figure is overstated** (real: 26,169). Re-approve,
     round down, or document what 30,000 counts. Blocks publishing.
   - **The AI sync pipeline has failed for ~18 days.** Operational, not a copy
     issue, but it invalidates `project_ai_sync_runs` as a freshness source.

1b. **PostHog** — project 138749, 111 events instrumented. Still unqueried;
   the sandbox blocked locating the key. The MySQL numbers cover most proof
   needs, so this is now optional rather than blocking. It would add funnel
   and activation data the DB can't show.

2. **Developer logo rights** — does any agreement permit showing developer
   logos? If yes, that changes the trust strategy substantially.

2b. **Listing-source wording** — confirm with legal how the agency-feed
   ingestion may be described publicly, given the Property Finder constraint
   in §1.3.1. This blocks any copy about importing a broker's existing
   inventory.
3. **Raghad's scope** — is she an Estavo-brand character, or does she appear on
   broker-branded Sites too? If the latter, she competes with the broker's own
   brand, which contradicts "إنت وبراندك قدام العميل."
4. **Free entitlements** — the copy's "ابدأ مجانًا" section needs the exact
   free/paid split confirmed against billing before publishing.
5. **English mascot** — does Raghad work for the English pages, or does the
   English audience need a different treatment? Her design is specifically
   Egyptian; that's a strength in Arabic and an open question in English.
