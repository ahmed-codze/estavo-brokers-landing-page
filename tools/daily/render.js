'use strict';

// Daily records must be bound inside reviewed artwork templates. Replacing
// whole scenes with generic cards changed their aspect ratios, overflowed the
// next section, and displaced hero artwork. Keep the approved compositions
// intact until those per-surface bindings have been visually verified.
// In particular, never inject a selections shelf or empty panels into a page.
function applyDaily(html) {
  return html.replace(/[ \t]+\n/g, '\n').replace('</head>', '<meta name="estavo-content-mode" content="approved-examples">\n</head>');
}
module.exports = { applyDaily };
