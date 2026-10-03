# Motion & Graphics Direction — Estavo Landing Pages

A build guide for making the landing pages feel alive, in the modern
product-landing style (bold geometric shapes, layered depth, scroll-driven
motion, a visible "system" diagram as the hero).

**Scope:** `index.html`/`en.html`, `market/`, `websites/`, `enterprise/`.
**Audience:** whoever implements this — you, a frontend dev, or me.

---

## 0. Read this first: what you already have

The pages are *not* static. Before writing any new animation, know what the
codebase already ships, because most of the work is wiring, not building.

**Already implemented in `assets/js/v3/estavo-v3.js`:**

| Function | What it does | Wired up? |
|---|---|---|
| `initReveal` | IntersectionObserver fade+rise on `[data-reveal]` | ✅ 11 targets on home |
| `initReveal` (stagger) | Sequential children via `[data-reveal-stagger]` | ✅ 2 targets |
| `initWordReveal` | Per-word cascade on `.es-tagline-line` | ⚠️ 1 target only |
| `initArtMotion` | Pointer parallax on hero/brand figures | ✅ desktop, hover-capable only |
| `initFlowReveal` | SVG rail draw-on-entry (`.es-flow`) | ❌ no `.es-flow` in markup |
| `initCardTracks` | Horizontal snap carousels | ✅ used on some pages |

**Already implemented in `assets/css/estavo-v3.css`** — 16 keyframes including
`es-draw-link`, `es-draw-rail`, `es-figure-rise`, `es-figure-settle`,
`es-hero-composition-drift`, `es-hero-surface-float`, `es-waterfall-grow`,
`es-plan-scan`, `es-segment-breathe`, `es-vector-transfer`.

**The gap is not capability. It is application.** Several of these animations
are written, tested, and reachable — but no element in the HTML carries the
class or attribute that triggers them. Fixing that is step 1 and costs almost
nothing.

**Budget:** `estavo-v3.css` is 207 KB against a 625 KB cap enforced by the
reliability test. You have ~418 KB of headroom. This is not a constraint.

---

## 1. The direction, stated plainly

The reference style this guide targets has five traits. Each maps to a
concrete change here.

| Trait | What it means | Estavo translation |
|---|---|---|
| **Geometric shape language** | Circles, arcs, grids, dots used as *structure*, not decoration | The hub-and-spoke diagram is already this. Extend it into section backgrounds. |
| **Layered depth** | Foreground cards float above a receding background | Parallax on figures (exists), plus background shape layers (new) |
| **Scroll as the timeline** | Things assemble as you scroll, not all at once | Reveal exists — needs sequencing and more targets |
| **One living hero** | The hero demonstrates the product, it doesn't picture it | Port the Market page's live AI demo to the homepage |
| **Confident type motion** | Headlines arrive with intent | `initWordReveal` exists — use it on every section H2 |

**What this direction is NOT, for you:** neon gradients, glassmorphism,
floating 3D blobs, or dark-mode-first. Your buyer is a brokerage owner
deciding whether to put their brand on your infrastructure. Motion should read
as *engineered*, not *playful*. Keep navy/off-white. Add structure, not color.

---

## 2. The shape system

This is the biggest visual lever and it costs the least.

### 2.1 Primitives

Define four reusable background shapes as inline SVG or CSS. They are
decoration, so they always carry `aria-hidden="true"`.

```
┌─ dot-grid ─────┐  ┌─ arc ──────────┐  ┌─ rail ─────────┐  ┌─ ring ─────────┐
│ · · · · · · ·  │  │      ╭─────    │  │  ──────────    │  │      ╭───╮     │
│ · · · · · · ·  │  │    ╭─╯         │  │                │  │     │  ●  │    │
│ · · · · · · ·  │  │   ╭╯           │  │  ──────────    │  │      ╰───╯     │
└────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘
  section texture     section corner      connective tissue    orbit the core
```

- **dot-grid** — faint texture behind content-heavy sections. Already used on
  the enterprise hero; extend it.
- **arc** — a single large-radius stroke bleeding off one edge. Use at section
  transitions to imply continuity.
- **rail** — the connector lines in your hub diagram, extracted as a standalone
  element so sections can visually "link."
- **ring** — concentric circles around a focal element (the Estavo core, a
  stat, a CTA).

### 2.2 Rules

1. **Max two shape layers per section.** More reads as noise.
2. **Opacity ceiling 0.10** on off-white, **0.16** on navy. Shapes must never
   compete with text contrast.
3. **Shapes animate on entry, then stop.** A permanently drifting background
   is a motion-sickness and battery problem. Exception: the hero, which may
   hold a very slow drift (already implemented as `es-hero-composition-drift`).
4. **Never put a shape behind body copy** — only behind headings, figures, and
   whitespace. RTL Arabic has tighter letterforms than Latin; texture behind it
   hurts legibility more than you expect.

### 2.3 CSS sketch

```css
/* Section-level shape layer. Sits under content, above background. */
.es-shape-layer {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}
.es-section { position: relative; }
.es-section > .es-container { position: relative; z-index: 1; }

.es-shape--dots {
  background-image: radial-gradient(circle, var(--es-line) 1px, transparent 1px);
  background-size: 28px 28px;
  opacity: .07;
}

/* Arc: draws itself once on entry, then holds. */
.es-shape--arc path {
  stroke-dasharray: var(--len);
  stroke-dashoffset: var(--len);
}
.is-visible .es-shape--arc path {
  animation: es-draw-rail 1.4s cubic-bezier(.22,.61,.36,1) forwards;
}
```

`es-draw-rail` already exists — reuse it rather than writing a new keyframe.

---

## 3. Motion system

### 3.1 The timing scale

Pick one scale and never deviate. Inconsistent easing is the main thing that
separates "designed" from "assembled."

| Token | Duration | Easing | Use |
|---|---|---|---|
| `--es-mo-fast` | 180ms | `cubic-bezier(.4,0,.2,1)` | hovers, button states |
| `--es-mo-base` | 420ms | `cubic-bezier(.22,.61,.36,1)` | element reveals |
| `--es-mo-slow` | 900ms | `cubic-bezier(.22,.61,.36,1)` | figure assembly, draws |
| `--es-mo-stagger` | 80ms | — | delay step between siblings |

Your existing stagger is 120ms, which drags on a 3-card row. **Drop it to
80ms.** Above ~100ms the eye reads it as "slow loading," not "choreography."

### 3.2 The scroll choreography

Each section should assemble in a fixed order. This is what makes a page feel
authored rather than animated.

```
1. shape layer draws      (0ms)      ← arc/rail, 900ms
2. eyebrow fades up       (120ms)    ← 420ms
3. heading words cascade  (200ms)    ← 55ms per word
4. body copy fades        (380ms)    ← 420ms
5. figure rises + settles (460ms)    ← 900ms
6. cards stagger in       (600ms+)   ← 80ms step
7. CTA fades last         (last)     ← 420ms
```

The CTA arriving **last** matters. It's the element you want the eye resting
on when motion stops.

### 3.3 Reduced motion is non-negotiable

Every animation added must be inert under `prefers-reduced-motion: reduce`.
The existing JS already checks this (`reduceMotion` guard at the top of each
init). Mirror it in CSS:

```css
@media (prefers-reduced-motion: reduce) {
  .es-shape-layer [class*="es-shape--"] { animation: none !important; }
  [data-reveal], [data-reveal-stagger] > * {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }
}
```

This is also an accessibility requirement, not a nicety — vestibular disorders
are triggered by exactly this kind of parallax and drift.

---

## 4. The hero

This is where the direction lives or dies.

### 4.1 Make it demonstrate, not depict

**Current state:** the homepage hero shows a *static picture* of an AI chat.
The Market page has a *live animated* demo driven by
`assets/js/market-landing.js`. That's backwards — the homepage takes the most
traffic.

**Action:** port the Market demo loop to the homepage hero. The code already
exists and already cycles two conversations with typing indicators. This is the
single highest-impact change in this document and it is mostly a copy job.

### 4.2 Assembly on load

The hero diagram should *build* in the first 1.2s, not appear complete:

```
t=0ms     backdrop + dot grid fade in
t=150ms   Estavo core circle scales 0.92 → 1
t=300ms   rails draw outward from core (es-draw-link, exists)
t=550ms   source cards arrive (stagger 80ms)
t=800ms   product surfaces arrive (stagger 80ms)
t=1100ms  AI chat starts typing
```

Cap total assembly at **1.2s**. Past that, visitors start scrolling through
your animation instead of watching it.

### 4.3 Keep the pointer parallax

`initArtMotion` already tilts `.es-hero__figure` ±2.4° on pointer move, and
correctly restricts itself to `(hover: hover) and (pointer: fine)`. Keep it.
Do not increase the angle — above ~4° it reads as a gimmick.

---

## 5. Section-by-section plan

### 5.1 Stat strip — the biggest wasted asset

Four approved figures (2,000 / 30,000 / 700 / 7,000) currently sit in a flat
row styled like a footnote.

**Make it a moment:**
- Count up from 0 on entry, 1.1s, ease-out. Stagger each stat by 80ms.
- `font-variant-numeric: tabular-nums` so digits don't jitter while counting.
- A faint ring shape behind each number.
- A thin rail connecting the four, drawn left-to-right (right-to-left in RTL).

**Critical:** render the final number in the HTML and animate *down* from it,
or set it immediately when `reduceMotion` is true. Never ship a stat that reads
"0" if JS fails — these are your proof numbers.

### 5.2 Break the visual monotony

Seven of nine homepage sections are the same composition on the same
background. Alternate the band treatment:

```
hero          off-white + full shape system
stat strip    off-white + rail
what you get  TINTED  (--es-mist)      ← change
Market        off-white + dot grid
how it works  NAVY    (inverted)        ← change
Sites         off-white + arc
enterprise    NAVY (already)
FAQ           off-white, no shapes
close         NAVY (already)
```

Two band changes give the page rhythm without touching content or the section
budget.

### 5.3 Differentiate the two card grids

Sections 3 and 5 are both "heading + three cards" and read as duplicates.
Make section 5 (`إزاي بتشتغل في ٣ خطوات`) a **numbered horizontal flow** with
a connecting rail and large step numerals, not a card grid. The `.es-flow`
CSS and `initFlowReveal` JS **already exist and are currently unused** — this
is wiring, not building.

### 5.4 Card hover

Currently flat. Add:

```css
.es-card {
  transition: transform var(--es-mo-fast), box-shadow var(--es-mo-fast);
}
@media (hover: hover) and (pointer: fine) {
  .es-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 1rem 2rem rgb(11 34 57 / 10%);
  }
}
```

Guard with `(hover: hover)` so touch devices don't get stuck hover states.

---

## 6. Fix first: the Sites section gap

Before any of the above — there is a **~640px blank area** in the Estavo Sites
section on desktop, where `estavo-brand-unified-still.svg` reserves its box
(1024×640) but the art does not appear in render. The asset returns HTTP 200,
so it is a render/lazy-load issue, not a missing file.

Reproduced across three separate captures at 1440px. **Do not ship motion work
on top of a visible hole.** Start by testing removal of `loading="lazy"` on
that one image, since it sits close enough to the fold to be eagerly loaded.

---

## 7. Performance guardrails

Motion that drops frames is worse than no motion.

| Rule | Why |
|---|---|
| Animate **only** `transform` and `opacity` | Anything else triggers layout/paint |
| Never animate `width`, `height`, `top`, `margin`, `filter` | Guaranteed jank |
| `will-change` only during animation, removed after | Permanent `will-change` leaks GPU memory |
| Cap concurrent animated elements at ~12 | Beyond that, low-end Android stutters |
| Hero assembly ≤ 1.2s | Longer and people scroll past it |
| Keep LCP < 2.5s | Motion must not delay first paint |

The hero is your LCP element. It already carries `fetchpriority="high"` and
must never become `loading="lazy"` — there is a QA rule enforcing exactly this.

---

## 8. Build order

Ordered by impact ÷ effort. Each step is independently shippable.

| # | Task | Effort | Why this order |
|---|---|---|---|
| 1 | Fix the Sites section gap | S | It's a visible defect |
| 2 | Stat strip count-up + rail | S | Biggest wasted asset, self-contained |
| 3 | Port live AI demo to homepage hero | M | Highest conversion impact; code exists |
| 4 | Wire `.es-flow` into section 5 | S | Kills the duplicate-grid problem; code exists |
| 5 | Two band changes (tint + navy) | S | Rhythm, pure CSS |
| 6 | Shape layer system | M | The actual "direction" |
| 7 | Hero assembly choreography | M | Polish once structure is right |
| 8 | Card hover + stagger retune to 80ms | S | Final polish |

Steps 1, 2, 4, 5 and 8 are all small and together change the page's character
substantially. Do those before anything speculative.

---

## 9. Constraints that override this guide

1. **QA gate** — `node tools/qa.js` must pass. It enforces section budgets
   (home 9 / market 9 / websites 8 / enterprise 8, all currently full), image
   `width`/`height` attributes, and forbids lazy-loading the hero.
2. **No new sections** without archiving an existing one into a `<template>`.
3. **RTL first** — every shape, stagger direction and rail must be authored
   with logical properties (`inset-inline-start`, not `left`). Test Arabic
   before English.
4. **No fabricated proof** — motion may not be used to animate testimonials,
   ratings or counts that are not real. The four approved figures are the only
   numbers available.
5. **Don't run `tools/build-pages.js`** until the uncommitted header-CTA work
   in `tools/partials/` is resolved — it currently breaks the gate.

---

## 10. How to verify

Do not trust code reading. For every change:

```bash
sh tools/serve.sh 8731 &
node tools/shot.js "http://127.0.0.1:8731/" out.png 1440 900   # full page
node tools/shot.js "http://127.0.0.1:8731/" out.png 390 844    # mobile
node tools/shot.js "http://127.0.0.1:8731/" --probe 320 568    # overflow check
node tools/qa.js && npm test
```

Then check it again with reduced motion forced on, and once with JS disabled
(`--no-js` on `shot.js`) — content must still be fully visible and readable.
