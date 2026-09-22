# Estavo — Section & Graphic Design Guidelines

The hero and market data sections establish the product vocabulary. The
September 2026 refresh establishes the material, typography and motion rules
below for both homepages and the 22 active service pages. The homepage direction
is **Estavo products in motion**: recognisable product surfaces, restrained
line geometry and clear data relationships drawn only with the Estavo palette.
The homepage hero uses a flagship product composition: one large maintained
project record with an integrated navy blueprint, an open blue orbit and three
recognisable previews (brokerage website, AI chat and Market comparison). The
project record is the visual anchor; the smaller previews show where the same
data goes without competing with it.
The homepage hero uses only Estavo navy, blue and paper tones. Its solid connections carry masked light sweeps. The whole product composition drifts on a smooth 14-second loop; website, chat and Market surfaces float with staggered 12-second cycles. Solid connector curves animate in sync with each destination, keeping both ends attached. The compact mobile diagram floats as one group, keeping its connectors attached. Disable all component movement in still assets and reduced motion; no
extruded glyphs or dashed travel. Phone previews use a purpose-built `390×430`
SVG: the project record stays on the left, while website, AI and Market surfaces
form one clear destination rail. Preserve the desktop product identities while
shortening secondary copy and removing duplicate fields. The navy surface inside
the source record carries one furnished blueprint; the surrounding white record
holds only the key project attributes and three grouped output ports. Avoid a
four-field form, repeated room counts or extra captions inside the core. Use one
Estavo mark as the main data-record anchor.
The assistant preview is a literal AI chat widget: navy header, user question
bubble and AI loading message with animated typing dots. Chat avatars use a
distinct, symmetric four-point AI glyph, centred within their circular surfaces;
do not repeat the Estavo mark inside the chat. The response avatar aligns with
the loading bubble centre. Phone compositions omit the duplicate brand scene above the data core. Keep the loading label and all dots visible and stationary in reduced
motion. Each destination depicts its product: a brokerage company homepage with browser chrome, company navigation, a
broad home-finding headline, supporting copy, a property search and a flat residential facade, an AI chat widget and a searchable Market workspace. The Market preview shows region/unit filters, two example property rows, price and payment columns, selected checkboxes and a compare tray. Use ordinary example project names and per-unit price labels; avoid invented prices or inventory counts. The website
preview starts its property section below the banner; do not replace it with a
single-unit banner, unit card, a price/payment field grid or an isolated floor-plan tile. This hero-specific direction is implemented separately from the
shared scene vocabulary below. Rebuild this trial with
`python3 tools/build-illustrations.py --hero-only`,
`python3 tools/refresh-premium-design.py --home-hero-only` and
`sh tools/build-css.sh`.

The remaining homepage illustrations follow the same September 2026 system.
They use only navy, Estavo blue, pale blue and paper; native line icons replace
the dimensional icon pack; solid connectors replace dashed travel; and every
scene depicts the actual product structure named by its section. Market is a
search-and-compare workspace, updates are a review workflow, brand is a website
+ assistant + data connection, AI is a conversation with matching results,
client context is a call brief, ROI is a property-return analysis report, Meta is an
event-to-audience flow, and Brokers is a unit-distribution flow. Each scene
floats as one connected component on a slow loop so connector endpoints never
detach. Reduced motion and `*-still.svg` companions remain completely static.
Phone layouts are independently composed at `390×430`, keep the same argument,
remove secondary repetition and stay within roughly half a phone viewport.
Rebuild them with `python3 tools/build-home-illustrations-v2.py`, then run
`python3 tools/refresh-home-illustrations-v2.py`,
`python3 tools/refresh-premium-design.py --home-hero-only` and
`sh tools/build-css.sh`.

Product structure leads the illustration. Large architectural renders and photo-led hero
sections are excluded. The ROI/report family belongs to the detailed Market experience; it is
not part of the current homepage hub sequence.

---

## 1. The philosophy in one sentence

**Every graphic is an argument about the product, drawn from real product
structure — never decoration, never a stock illustration, never a list of
cards wearing a graphic's clothes.**

Three consequences that decide most design questions:

1. **The graphic must say something the copy doesn't.** The hero says "all
   market data, one source, used your way" — so the graphic *shows* an example
   Estavo data core connected to three recognisable product destinations. The market
   section says "stop hunting across WhatsApp, PDFs and websites" — so the
   graphic *shows* scattered sources converging into one screen. If you can
   delete the graphic and lose no meaning, it is decoration; redesign it.

   When the product action happens in one workspace, draw one workspace.
   Do not split an update review into three source cards, a floating approval
   gate and a separate result card. Use an internal activity rail, comparison
   area and review state so the composition reads as one real tool. Likewise,
   place a branded assistant and data connection inside the brokerage website
   they support instead of presenting them as unrelated destination cards.

2. **Premium starts with specificity.** Use recognisable product structures:
   a comparison table, a client brief, a floor plan, a calculation. Give those
   structures enough detail to be understood at first glance. Native line icons
   support the interface; comparisons, plans, charts and data carry the visual interest.

3. **Honesty is a design constraint.** Clearly labelled examples may use
   ordinary non-price values: `شقة · ٣ غرف`, `التجمع الخامس`, `٦ سنوات`.
   These describe an example, never actual inventory or commercial terms.
   Prices, percentages, returns, availability and market-wide counts require
   verified sources. Use `حسب الوحدة` or `حسب خطة السداد` where appropriate;
   reserve redaction for a meaningful price comparison, never every field.

---

## 2. Section anatomy (do not deviate)

Both reference sections use the same scaffolding:

```html
<section class="es-section [es-section--mist]" aria-labelledby="xxx-h">
  <div class="es-container es-split">
    <div class="es-copy" data-reveal>
      <span class="es-eyebrow">…</span>      <!-- category -->
      <h2 id="xxx-h">…</h2>                   <!-- the claim -->
      <p class="es-lead">…</p>                <!-- what it means -->
      <p><a class="es-text-link">… ←</a></p>  <!-- one next step -->
    </div>
    <div data-reveal>
      <div class="es-*-figure" aria-hidden="true">
        <picture class="es-vector-picture">
          <source media="(prefers-reduced-motion: reduce)"
                  srcset="assets/img/example-still.svg" type="image/svg+xml" />
          <img class="es-*-figure__vector" src="assets/img/example.svg" />
        </picture>
        <div class="es-*-mobile"> … </div>
      </div>
    </div>
  </div>
</section>
```

Rules:

- **Copy is the first child.** The narrower grid track comes first; the figure
  takes the wider one. The market section rebalances to `0.82fr / 1.18fr`
  above 64rem because a 1024×640 stage was unreadable in an even split.
- **Figures are `aria-hidden="true"`.** They are illustrations; the copy
  carries the meaning for assistive tech. Consequently they contain **no links
  and no buttons** — nothing in a figure may look interactive (see §5).
- **Alternate surfaces.** `es-section--mist` alternates with the default paper
  ground so adjacent sections separate without borders.
- **`data-reveal`** goes on both columns.

---

## 3. The two-composition contract (the most important rule)

> **One scalable vector stage for desktop, one purpose-built composition for
> mobile. Never shrink the desktop diagram onto a phone.**

This is stated in the code twice, and it is non-negotiable:

```
/* Below 768px it swaps for a purpose-built composition
   rather than shrinking (§7.3). */
/* Shown only below 768px, where the 1024-wide stage would
   shrink its labels past legibility. */
```

| | Desktop (≥768px) | Mobile (<768px) |
|---|---|---|
| Source | one SVG, `1024×900` (hero) / `1024×640` (sections) | purpose-built `390×430` hero and section SVGs |
| Swap | `.es-*-figure__vector { display: block }` | `display: none` → mobile block `display: grid` |
| Why | full detail, labels legible at size | labels stay ≥12px, layout re-thought for one column |

**Mobile is a redesign, not a reflow.** The homepage hero and each later
homepage section use separate 390px vector compositions. They preserve the
desktop argument while shortening labels and removing secondary detail. Never
shrink desktop UI labels onto a phone.

---

## 4. Mobile composition patterns that work

Learned the hard way on the hero. Use these; avoid the failures listed.

**✅ Radial hub** — centre mark, nodes in the four quadrants, outputs in a row
below a divider. Reads as a diagram because it has a centre of gravity.
Implemented with explicit `grid-template-areas`:

```css
grid-template-areas:
  "topstart topend"
  "hub      hub"
  "botstart botend";
```

**✅ Converge-to-one** (market section) — scattered source chips → arrow →
single screen. The arrow carries the argument: *many sources, one screen.*

**❌ A vertical list with a line down the side.** This is the failure mode to
watch for. If your mobile composition is "items stacked in order," it is a
list, however you decorate it.

**❌ A 2-column grid with a centre spine.** There is no room at 390px for a
spine plus two label columns; connectors end up crossing ~108px of empty
column and dangling. If nodes need connecting, put the connector *through*
the glyph, or use quadrants and no connector at all.

---

## 5. Cards vs. nodes — the button trap

A graphic element that has **border + drop shadow + filled surface + an
icon-left/label-right row** is button anatomy. Repeat it four times and the
"graphic" reads as a menu.

- **Nodes in a diagram**: no border, no shadow, no filled panel. Circular
  glyphs, label beneath, transparent ground.
- **Cards**: reserved for things that are genuinely surfaces — a simulated
  screen (`.es-market-mobile__screen`), a source chip in a "before" state.
- **Keep interaction affordances inside the depicted product.** A contained
  website, search workspace or assistant may show its real controls. Diagram
  nodes and the surrounding illustration must not masquerade as page buttons.

---

## 6. Visual language

Use the tokens in `assets/css/v3/` — never raw hex in new components.

| Role | Token / value |
|---|---|
| Deep ground, hub fills | `--es-navy-950` `#0b2239`, `--es-navy-900` `#102b45` |
| Structure, icon strokes | `--es-blue-600` `#28567f`, `#285d8d` |
| **Connector lines** | `#5c91c7` at **42%**, 1–1.8px |
| Glyph outlines | `rgb(92 145 199 / 38%)` |
| Page ground | `--es-paper` `#fafcff` |
| Panel ground | `--es-white`, `--es-mist` `#f1f5f8` |
| Secondary structure / price redaction only | `#c3d5e8` |
| Positive accent / active connection on legacy service scenes only | `#72e0bb`, `#27a06f` (sparingly) |

Homepage illustrations do not use the green accent. Use Estavo blue for
selection, status and connection energy there.
When an illustration explicitly represents an external platform, its official
brand color may appear only in the platform mark and recognisable interface
chrome. The product surface and all data remain in the Estavo palette.

Geometry: `--es-radius-panel: 1rem`, `--es-radius-theatre: 1.25rem`.
Pills are status indicators, not substitute content.

**Browser framing must carry meaning.** A brokerage website may use a thin URL
bar because it clarifies that the surface is the broker's live site. Other
product surfaces use their own heading and a thin rule; do not add generic
three-dot window bars as decoration.

**Material:** `--es-art-paper` is a soft diagonal white-to-mist wash.
`--es-art-dark` adds a slate-lit edge within the navy palette. `--es-art-shadow` has a
wide ambient layer and a small contact layer; `--es-art-inner` adds a 1px
light edge on dark surfaces. Standalone SVGs mirror these approved tokens because
page variables cannot cross an image boundary. Homepage scenes use blue for
status, selected states and connection energy. Mint is limited to legacy service
scenes until those scenes move to this flat system.

**Stroke hierarchy:** 1.25px structure / 2px subject in vector coordinates.
Use lower opacity for construction lines; connectors need a visible endpoint.

**Typography:** use Cairo for page text in both languages, loaded at 400, 500,
600 and 700. Body text is regular 400; headings, labels and modest emphasis use
500. Reserve 600–700 for selective emphasis. Never synthesise large bold headings.
The page ramp caps hero headings at 64px, service H1s at 58px, section headings
at 41px and card headings at 23px, reached at roughly 1800px and above; a 1440px
stage lands near 56/52/37px. Phones use 31–38px hero headings, 26–30px
section headings and 16px body text. Keep Arabic display leading at 1.38–1.45.
The ramp lives only in the `--es-fs-*` tokens in `assets/css/v3/tokens.css`.
Set heading sizes from those tokens; a module that restates a `clamp()` re-breaks
the scale, because the last file concatenated by `tools/build-css.sh` wins.

Standalone SVGs use 28px display / 24px heading / 21px field or body / 19px
secondary / 17px metadata on a 1024px stage. Field labels are medium; values
are regular. Standalone SVGs keep their subsetted Plex regular and medium WOFF2
until their text is migrated, because image documents cannot inherit Cairo from
the page.
Phone compositions use 12px metadata, 14px fields and 18px titles.
Never assume an image inherits fonts. English graphics have their own
translated `*-en.svg` variants and font subsets.

**Estavo owns the visual language.** The source mark is the vector outline in
`assets/logo/estavo-mark.svg`, derived from the existing approved Estavo icon.
Use its connected e/s geometry once as the main data anchor. The homepage chat
widget uses the separate centred AI glyph described above. Product-specific
surfaces, illuminated solid connections and careful interface detail make the
homepage scenes distinct from stock vector templates. Blueprints and flat chart
bars remain useful supporting product detail. Detail should reward close
inspection while the overall silhouette remains clear. Native paths provide
the geometry; quiet fills and restrained inner edges provide material. Inline
glyph paths into standalone figures and scope every gradient/filter ID per
instance. Do not embed raster fills or depend on a third-party animation player.

**Product content leads.** Hero sections use layered product geometry,
comparisons, service selection or other product compositions. Never introduce a large
architectural render, photograph or decorative image as their centrepiece.
Native unit plans replace the prior architectural images throughout the
illustrations. Small property thumbnails may appear inside meaningful listing
examples elsewhere; they are supporting information rather than the page's
main visual. Previous generated image assets are unused drafts, not approved
hero art.

**Icons:** Homepage illustrations use small native line icons with one shared
stroke weight. The ten-vector family in `assets/img/icons/` remains available
to service-page scenes that have not yet moved to the flat system. Keep
ordinary controls as functional line icons. Do not wrap every graphic icon in a button tile.
The branded `chat` glyph means Estavo's assistant. The separate `messages`
glyph represents external conversation sources, including WhatsApp; never
label the Estavo assistant mark as an external provider.

Homepage service-choice cards do not use standalone category icons. Give each
card a compact crop of the product it opens: search-and-compare rows for
Market, a brokerage website banner for Websites, a question and active reply
for AI, and a data schema connected to existing systems for Integrations.
These crops use the same flat Estavo surfaces as the larger illustrations.

**Vary composition deliberately.** Shared material does not require shared
silhouettes. Adjacent illustrations must have different centres of gravity.

| Figure | Composition |
|---|---|
| Meta signals | Website events → Meta interest audience → Facebook property-post preview |
| Trusted marketing network | Developers, units, resale, brokers and market news → one Estavo network core |
| Client context | One lead profile → observed journey → focused pre-call brief and opening question |
| AI conversation | Customer question and clarification → matching property results |
| Brand unified | Branded brokerage website → assistant and current-platform data connection |
| ROI (Market page) | Price-history report → cost and inflation calculation → sell/hold context |
| Listings reach | Unit record → publishing channels → broker network activity and commission control |
| Market explorer / updates | Search workspace / change events → review gate → current record |
| Hero | Property-data core → brokerage website, AI chat and Market workspace |
| Pricing / enterprise hero | Shared Estavo core linked to service glyphs and readable native service selection |

The client-intelligence and listings sections use asymmetric split layouts on
desktop. Explanatory copy and the working product surface share the first row;
do not stack a centered introduction, full-width illustration and a second
explanation vertically. Listings steps belong in one connected process strip,
and its promotional offer is a compact banner. On phones, these elements stack
once in reading order without repeating headings or calls to action.

Rebuild icons: `python3 tools/build-premium-icons.py`.
Rebuild figures: `tools/build-illustrations.py` (requires `fonttools`,
`brotli`); font source and OFL licence live in `assets/fonts/`.
Phone compositions: `tools/refresh-mobile-art.py`; styles:
`assets/css/v3/illustrations.css` and `premium.css`. Run
`tools/refresh-premium-design.py` after the mobile builder to refresh both
homepages, service-page templates, generated service pages and critical CSS.
Rebuild production CSS with `sh tools/build-css.sh`. Critical CSS is generated
from the source modules; do not maintain a separate fork of the type ramp.

---

## 7. Motion

SVGs carry motion internally (they're `<img>` — page CSS cannot reach inside
them). Page-level motion and SVG motion have separate responsibilities:

1. **Scroll entrance:** top-level sections rotate between fade-up, logical-start,
   logical-end and soft-scale entrances. Keep travel within 24px (28px on dark
   panels), use an 800–900ms editorial ease, and stagger card rows at 90ms.
   Content is visible before enhancement. Never reveal all below-fold sections
   on a global timeout; keep observing them until entry.
2. **Homepage composition drift:** move each connected composition as one group
   by no more than 3px over 12–14 seconds. Connectors and endpoints live inside
   that group, so they never detach. Text remains stable relative to its surface.
3. **Connection energy:** the full solid route is always visible. A soft masked
   luminance sweep may travel across it; never use marching dashes, packets or a
   draw-on hairline. The sweep shows direction without pretending to be live data.
4. **Meaningful local motion:** typing dots may pulse inside the assistant and
   selected states may brighten. Do not animate every icon. Legacy service scenes
   may retain their prior sequence until they are rebuilt with this method.

Wrap animated geometry inside its static placement group. Animating a
`transform` on the same group as a positioning matrix replaces that matrix
and makes objects jump. Geometry-only SVGs carry their own motion rules;
inline mobile SVGs use the shared motion CSS. All motion is CSS-driven and
works in local file previews without an animation runtime.

Every animated standalone SVG has a generated `*-still.svg` companion with
motion explicitly disabled and the complete final geometry restored. HTML
`picture` sources select it for reduced motion. This is required: browser SVG
image documents can evaluate motion preferences separately from the page.
Test two rendered frames of the actual page image, not only a standalone SVG.
Keep picture wrappers at `display: contents` and their `source` elements at
`display: none`; otherwise sources become empty grid items and introduce gaps.

**Reduced motion is a hard requirement and the classic bug.** An entrance
using `animation: … both` that is merely cancelled leaves elements at
`opacity: 0` — an invisible page. Always restore the end state:

```css
@media (prefers-reduced-motion: reduce) {
  .thing { animation: none; opacity: 1; transform: none; }
  .packet, .plan-scan { display: none; }
}
```

---

## 8. Arabic / RTL rules

- **Line-height.** Display type needs more leading than Latin. `1.14` clipped
  descenders and the full stop in `اسمك.` at 37px; use `1.38–1.45` for display
  headings and `1.42` for section headings. Body copy uses `1.85`.
- **Logical properties flip.** `inset-inline-start` is the **right** edge in
  RTL. In a grid, the **first track is the rightmost**. Verify by measuring,
  not by reasoning — this caused four consecutive wrong-side bugs.
- **Prefer explicit grid areas** over flow-relative offsets for anything
  positional. They are unambiguous in both directions.
- **Wrap Latin runs** in `<bdi>`: `<bdi>WhatsApp</bdi>`, `<bdi>Estavo Market</bdi>`.
- **Keep labels single-line** where they sit in a grid; a label wrapping to two
  lines while its sibling doesn't is what makes a layout read as ragged.

---

## 9. Height & the fold

- **Desktop:** the hero fills exactly one fold —
  `min/max-block-size: calc(100svh - var(--es-header-h) - 1px)`. The `-1px` is
  the header's bottom border, which sits outside the token.
- **Width governs, height caps.** Size a figure by width so it stays inside its
  grid track; use `max-block-size` to keep it in the fold. Letting height drive
  width via `aspect-ratio` pushes the figure out of its track and clips it.
- **Mobile stays compact.** The homepage hero is approximately 450px high at
  phone widths. Each remaining homepage scene uses its own `390×430`
  composition instead of shrinking the desktop SVG. Preserve the same product
  argument, remove repeated metadata and avoid adding avoidable page length.
- **Never let a token lie.** `--es-header-h` claimed `4.25rem` while the header
  rendered at 141px (a square logo sized by width). Everything computed from it
  was wrong. If a token names a measurement, enforce it.

---

## 10. Verification — required before calling any design done

Rendering and measuring is not optional; several of these bugs were invisible
to code review and to a casual glance.

1. **Render at 1280 / 1440 / 1512 / 1728 and 390 / 360 / 320.**
2. **Measure, don't assume:** overflow past the fold, figure inside its grid
   track, no horizontal scroll at 320px.
3. **Look at the screenshot.** A geometry probe once reported `PERFECT` while
   connectors dangled 108px short — because it measured the wrong property.
   Numbers confirm; eyes decide.
4. **Test `prefers-reduced-motion`** and confirm everything is *visible*.
5. **Validate the SVG.** `xml.dom.minidom.parse()` it. Note: a literal `<img>`
   or `<g>` typed inside an SVG `<style>` comment is parsed as a tag and breaks
   the whole file silently — the browser renders nothing.
6. **Check both stylesheets.** Critical CSS is inlined across all 24 active
   pages and generated from the source modules. Run the premium refresh tool
   and CSS build after source changes; verify first paint without the async
   stylesheet as well as the fully loaded page.
7. **Check file previews too.** The homepage is often opened with `file://`.
   Fonts and standalone vector figures must remain readable in that mode.
8. **Verify motion at the moment of entry**, including a section reached more
   than 2.5 seconds after load. Reduced motion and JavaScript-off content must
   remain visible.

---

## 11. Content rules for graphics

- **Example fields may have non-price values.** Display `مثال` at the component
  level. Example room counts, areas and payment durations are not assertions
  about live inventory. Never invent prices, ROI percentages or availability.
- **Request and result must agree.** A request to compare payment plans may
  yield schematic five- and six-year rows. Show `قارن الخطط` in the request
  criteria; never infer an unmentioned six-year preference from that request.
- **ROI must read as a report.** Start with a recognisable unit price-history
  chart, show purchase cost and inflation as inputs to the real-return result,
  then connect that result to the sell-or-hold conversation. Label the whole
  surface as an example and never invent prices or projected percentages.
  Supporting cards use four different mini data views for price history,
  purchase payments, value growth and real return; never repeat one generic icon.
- **Estavo vocabulary is precise:** Areas / Projects / Units are specific terms.
  "السوق" only for the broad Egyptian market; "Estavo Market" is a product name.
- **Never show raw coordinates.** A map pin is the only location interface.
- **Label at component level**, never in a distant footnote.
- **Copy in a graphic is still copy.** Have it reviewed; don't invent claims to
  fill a layout.

---

## 12. Checklist for a new section

- [ ] The graphic makes an argument the copy alone doesn't make
- [ ] Desktop SVG + separate mobile composition (not a shrunk copy)
- [ ] Mobile composition has a shape — not a stacked list
- [ ] No element in the figure looks tappable
- [ ] Shared material and stroke hierarchy; composition differs from its neighbours
- [ ] Product vectors lead; no raster illustration or photo-led hero
- [ ] No three-dot window chrome or decorative skeleton bars
- [ ] Entrance and purposeful motion; reduced-motion restores the end state
- [ ] Example values labelled; commercial claims require verified data
- [ ] SVG typography is self-contained and inspected at rendered size
- [ ] RTL verified by measurement; Latin runs in `<bdi>`
- [ ] Fold respected on desktop; no h-scroll at 320px
- [ ] Rendered and **looked at**, at both ends of the range
