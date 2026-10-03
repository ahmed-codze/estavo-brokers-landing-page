# Estavo Homepage — Design & Motion Direction

Art direction for the new homepage built on the **السوق · العقار · العميل**
copy. Covers the visual system, the mascot, illustration, animation, and a
section-by-section build.

This is a **design brief**, not a spec sheet. Numbers used here are
illustrative of *scale and feel* — exact published figures get confirmed
separately before launch.

---

## 1. The idea in one line

> **Estavo is the colleague who has already read the whole market.**

Not a database. Not a dashboard. A *someone*. Every design decision below
serves that: the mascot is the someone, the illustrations are what she has
organised, and the motion is her thinking — assembling, connecting, resolving.

### The shape of the whole page

```
                 السوق  ──────┐
                               │
                 العقار  ──────┼──── ✦ AI ✦ ──── "أنهي عقار لأنهي عميل؟"
                               │
                 العميل  ──────┘
```

Three inputs, one intelligence, one answer. **This triangle is the brand
device.** It appears in the hero, recurs as a motif, and closes the page.
If someone remembers one image from the site, it should be this.

---

## 2. Brand system

### 2.1 Palette — what you already own

| Token | Value | Role |
|---|---|---|
| `--es-navy-950` | `#0b2239` | Deep bands, the "intelligence" colour |
| `--es-navy-900` | `#102b45` | Dark surfaces |
| `--es-ink` | `#13283c` | Primary text |
| `--es-blue-600` | `#28567f` | Structure, rails, diagram strokes |
| `--es-blue-500` | `#47749a` | Secondary strokes |
| `--es-mist` | `#f1f5f8` | Page background |
| `--es-paper` | `#fafcff` | Card surfaces |
| **`--es-art-mint`** | **`#72e0bb`** | **The signal colour — see below** |

**The mint is the most underused asset in the system.** It appears in only six
places. It should become the single, consistent marker for *"this is the AI
thinking"* — every intelligence moment on the page, and nothing else.

That gives the page a visual grammar a visitor learns in five seconds:

> Navy = structure · Blue = data · **Mint = intelligence** · White = your brand

Never use mint for a CTA, a border, or decoration. The moment it means two
things, it means nothing.

### 2.2 Typography

IBM Plex Sans / Plex Arabic. Keep it. Changes:

- **Headlines heavier.** The copy is punchy and short (*"الأرقام مبتكدبش"*).
  It needs weight 600, tighter tracking (`-0.02em`), and more size contrast
  against body copy than the page currently has.
- **Tabular numerals** (`font-variant-numeric: tabular-nums`) everywhere a
  number animates, or digits jitter while counting.
- **One editorial moment per page.** The closing *"أنهي عقار مناسب لأنهي عميل؟"*
  should be noticeably larger than anything else — the question the whole
  product answers.

### 2.3 Shape language

| Shape | Means | Where |
|---|---|---|
| **Circle** | Intelligence / processed | The AI core, Raghad's frame |
| **Rounded rect** | A thing — unit, project, card | Data surfaces |
| **Rail** (1–2px line) | Relationship | Everywhere — the signature element |
| **Dot** | A single signal | Client interest, activity |
| **Arc** | Continuity | Section transitions |

**Rails are the signature.** The product's claim is *connection between three
things*, so lines-between-things is the right visual argument. Existing
illustrations already use 1–2px strokes; keep that weight.

---

## 3. Raghad — the mascot system

### 3.1 Why she matters more than you're using her

The hero says *"معاك حد مذاكر السوق"* — **"you have someone."** Raghad is that
someone. Today she's a 96px circle in a chat launcher. That's the biggest
missed opportunity on the site: the page makes a *person* promise and hides
the person.

### 3.2 Pose set — six, no more

| Pose | Action | Section |
|---|---|---|
| **Studying** | Reading floating data cards, focused, slight lean in | Hero |
| **Presenting** | Open palm toward a comparison | السوق |
| **Weighing** | Holding two options, deciding | العقار / Request |
| **Listening** | Turned toward a client bubble, attentive | العميل |
| **Confident** | Beside a branded site, arms relaxed, proud | Sites |
| **Waving** | Warm, direct to camera | Close + launcher |

More than six and she becomes clip-art. Six is enough for a 9-section page
because she only appears in about half of them.

### 3.3 Rules

1. **One Raghad per viewport.** Two on screen breaks the illusion of a single
   assistant.
2. **She never overlaps body copy.** Margin, corner, or dedicated figure space.
3. **Three sizes only:** 96px (launcher) · 180px (section accent) · 320px (hero).
4. **She faces into the content.** On RTL that means facing left.
   **This must flip on the English pages** — mirror or redraw, don't just
   reposition. A character facing off-canvas pushes the eye away.
5. **Never beside disclaimers.** A friendly face next to "returns are not
   guaranteed" reads as minimising it.
6. **Not on the enterprise page hero.** Brokerage owners evaluating a
   company-wide system respond to system diagrams, not mascots.
7. **She never appears on broker-branded Sites.** Those pages belong to the
   broker's brand — that's the entire promise of the product.

### 3.4 Her relationship to mint

Raghad and the mint accent should feel connected. When she's "thinking," mint
appears — a glow in her frame, a mint dot on the card she's reading, mint rails
flowing from her toward the data. **She is the source of the intelligence
colour.** That single consistency does more brand work than any amount of
styling.

### 3.5 Technical

- **SVG**, not WebP — she scales 96→320px and needs recolouring for navy bands.
- Two palettes: warm (on mist) and a cooled/inverted variant (on navy). A warm
  character on navy looks like a sticker.
- ≤40 KB per pose. Lazy-load everything below the fold.
- Always declare `width`/`height` — the QA gate requires it.

### 3.6 Her motion

Restrained. An over-animated mascot reads as a children's app, which is wrong
for a tool a brokerage owner is evaluating.

- **Entry:** fade + 12px rise, 420ms. Nothing more.
- **Idle:** optional slow breathing scale (1.0 → 1.012, 4s). No blinking,
  no waving loops.
- **Hero only:** she may hold one prop that animates once — a card that flips,
  a chart that draws.
- **Reduced motion:** fully static.

---

## 4. Motion system

### 4.1 Timing scale

| Token | Duration | Easing | Use |
|---|---|---|---|
| `--es-mo-fast` | 180ms | `cubic-bezier(.4,0,.2,1)` | hover, button |
| `--es-mo-base` | 420ms | `cubic-bezier(.22,.61,.36,1)` | element reveal |
| `--es-mo-slow` | 900ms | `cubic-bezier(.22,.61,.36,1)` | assembly, draws |
| `--es-mo-stagger` | 80ms | — | sibling delay |

Current stagger is 120ms and drags on a three-card row. **Drop to 80ms.**

### 4.2 Section choreography

Every section assembles in the same order. Consistency is what makes it read
as *designed* rather than *animated*.

```
1. shape layer draws        0ms     900ms
2. eyebrow fades up       120ms     420ms
3. heading words cascade  200ms     55ms/word
4. body copy fades        380ms     420ms
5. figure rises + settles 460ms     900ms
6. cards stagger          600ms     80ms step
7. CTA fades LAST          last     420ms
```

The CTA arriving last matters — it's where the eye rests when motion stops.

### 4.3 Reuse what's already built

**Most of this is wiring, not building.** Already in the codebase:

| Asset | State |
|---|---|
| `initReveal` + stagger | ✅ live, 11 targets |
| `initWordReveal` | ⚠️ built, used on **1** element |
| `initArtMotion` (pointer parallax) | ✅ live on hero |
| `initFlowReveal` + `.es-flow` + `es-draw-rail` | ❌ **built, zero usages in HTML** |
| 16 keyframes incl. `es-draw-link`, `es-figure-rise`, `es-vector-transfer` | ✅ available |

The rail-drawing system is exactly what the triangle needs and it's sitting
unused. That's the cheapest win on the list.

### 4.4 Performance guardrails

- Animate **only** `transform` and `opacity`. Never `width`, `top`, `filter`.
- `will-change` only during animation, removed after.
- ≤12 concurrently animating elements.
- Hero assembly ≤1.2s — longer and people scroll past your animation.
- Hero is LCP: never `loading="lazy"` (QA-enforced).
- Every animation inert under `prefers-reduced-motion`.

---

## 5. Section-by-section

### 5.1 Hero — the one that matters

**Composition:** Raghad *studying* on one side, the triangle diagram on the
other, headline above. Not a dashboard screenshot.

**Assembly (≤1.2s):**
```
0ms     mist background + faint dot grid
150ms   AI core scales 0.92→1, mint pulse once
300ms   three rails draw outward (es-draw-link)
550ms   السوق / العقار / العميل nodes arrive, 80ms stagger
800ms   Raghad fades + rises
1100ms  AI chat begins typing
```

**Critical change:** the hero currently shows a *static picture* of an AI chat,
while the Market page has a *live animated* demo. That's backwards — the
homepage gets the most traffic. **Port the live demo.** The code exists in
`assets/js/market-landing.js`.

Keep the existing ±2.4° pointer parallax. Don't increase it.

### 5.2 Proof strip

Four figures. Make it a moment, not a footnote:

- Count up on entry, 1.1s, ease-out, 80ms stagger
- `tabular-nums` so digits don't jitter
- Faint ring behind each number
- A rail connecting all four, drawing right-to-left in RTL

**Must render the real number if JS fails.** Never let a proof figure show `0`.

### 5.3 السوق

Scattered cards — WhatsApp messages, PDFs, price lists — flying in and
snapping into one organised grid. Raghad *presenting*.

This is the strongest story on the page: chaos → order. Give it room.

### 5.4 اسأل إستاڤو

Live chat demo, mint accents on the AI side. Real typing rhythm, not a loop
that feels mechanical — vary the pauses.

### 5.5 Request analysis

A handwritten-feeling client note transforms into three ranked option cards,
rails connecting note → cards, with *reasons* labelled on each rail.
Raghad *weighing*.

**This is the product's core mechanic.** It deserves the most crafted
illustration on the page.

### 5.6 ROI

**Hold until the calculator ships.** Don't design a section around a feature
that isn't live.

### 5.7 Sites

Browser frame assembling, then the brand colour swapping to show it's *yours*.
Raghad *confident* beside it — then she steps back, because the point is the
broker's brand is in front.

### 5.8 العميل

Signal dots travelling along rails inward, converging on a client silhouette
that gradually resolves from outline to defined. Raghad *listening*.

The resolve-from-blur is the metaphor: you learn who they are.

### 5.9 العقار → العميل

Two-way arrows drawing in both directions between a unit card and client
profiles. Simple, fast, makes the bidirectional claim instantly legible.

### 5.10 Growth

Scattered dots clustering into recognisable groups. No Meta UI, no fake
dashboard — just the pattern-forming idea.

### 5.11 Triangle recap + close

Same device as the hero, simplified. **Reveal only, no re-assembly** — the
visitor has seen it; repeating the full animation is tiresome. Then the
editorial question at maximum size, Raghad *waving*, two CTAs.

---

## 6. Band rhythm

Seven of nine sections currently sit on the same background. Alternate:

```
hero             mist + full shape system
proof strip      mist + rail
السوق            TINTED  (--es-mist-2)     ← change
Market/AI        NAVY    (inverted)         ← change
Request          mist + arc
Sites            mist
العميل            NAVY                       ← change
Growth           mist
close            NAVY (already)
```

Three band changes give the page rhythm without touching content or the
section budget. Navy sections are where mint does the most work.

---

## 7. What to fix before any of this

**There is a ~640px blank gap in the Sites section on desktop** —
`estavo-brand-unified-still.svg` reserves its 1024×640 box but doesn't render.
Reproduced across multiple captures. The asset returns HTTP 200, so it's a
render/lazy-load issue.

**Don't layer motion onto a visible hole.** Fix first.

---

## 8. Build order

| # | Task | Effort |
|---|---|---|
| 1 | Fix the Sites section gap | S |
| 2 | Promote mint to the single intelligence colour | S |
| 3 | Proof strip count-up + rail | S |
| 4 | Port live AI demo to hero | M |
| 5 | Wire `.es-flow` into the triangle | M |
| 6 | Three band changes | S |
| 7 | Commission Raghad pose set (6, SVG, 2 palettes) | L |
| 8 | Hero assembly choreography | M |
| 9 | Section illustrations §5 | L |
| 10 | Stagger 120→80ms, card hover | S |

**1, 2, 3, 5, 6 and 10 need no new assets and no sign-off.** Together they
change the page's character substantially. Do them first; commission Raghad in
parallel since it's the long pole.

---

## 9. Constraints

1. **QA gate** (`node tools/qa.js`) must pass — section budgets are full
   (home 9), images need `width`/`height`, hero can't be lazy.
2. **New sections require archiving an existing one** into a `<template>`.
3. **RTL first.** Logical properties only (`inset-inline-start`, never `left`).
   Author in Arabic, then mirror.
4. **No fabricated proof.** Mockups showing data use "مشروع أ" and carry a
   visible `مثال` label.
5. **No developer logos** — no partnership agreements exist to support them.
   Names may appear inside a product UI frame as data, never under a
   "partners" heading.
6. **Don't run `tools/build-pages.js`** until the uncommitted header-CTA work
   in `tools/partials/` is resolved.

---

## 10. Verify every change

```bash
sh tools/serve.sh 8731 &
node tools/shot.js "http://127.0.0.1:8731/" out.png 1440 900   # desktop
node tools/shot.js "http://127.0.0.1:8731/" out.png 390 844    # mobile
node tools/shot.js "http://127.0.0.1:8731/" --probe 320 568    # overflow
node tools/qa.js && npm test
```

Then once more with reduced motion on, and once with `--no-js`: content must
stay fully visible and readable in both.
