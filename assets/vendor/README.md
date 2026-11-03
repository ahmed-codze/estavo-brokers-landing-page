# Vendored libraries (homepage motion)

Self-hosted so the homepage has no runtime CDN dependency. Loaded only by
`assets/js/home-motion.js`, on wide screens with a fine pointer and no
reduced-motion preference. Source-map comments were removed (no maps shipped).

| File | Version | Source | Licence |
|---|---|---|---|
| `lenis-1.1.20.min.js` | lenis 1.1.20 | https://unpkg.com/lenis@1.1.20/dist/lenis.min.js | MIT |
| `gsap-3.12.5.min.js` | GSAP 3.12.5 | https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js | GSAP Standard License |
| `ScrollTrigger-3.12.5.min.js` | GSAP 3.12.5 | https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js | GSAP Standard License |

Downloaded 3 Nov 2026. To upgrade, replace the file under a new versioned name
and update the paths in `home-motion.js`.
