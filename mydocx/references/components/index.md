# Component API Reference

All functions available via `C` (loaded in template.js as `const C = require("./components")`).

## Section Builders

Return complete section objects for the `sections` array.

### `C.coverPage({ title, subtitle?, date?, author?, org? })`
Full title page with navy title, red accent rule, metadata at bottom.

### `C.toc({ depth? })`
Auto-generated table of contents. `depth`: heading levels to include (default 3).

### `C.section(children, opts?)`
Content section with page setup. Auto-flattens children (no spread needed for array-returning functions).
Options: `headerFooter` (opts object or `C.headerFooter()` result), `landscape`, `margin`.

## Content Elements

Return elements for a section's `children` array.

### `C.heading(level, text)` &rarr; Paragraph
Heading paragraph. `level`: 1, 2, or 3.

### `C.body(text, opts?)` &rarr; Paragraph
Body text. Options: `size`, `color`, `bold`, `italics`, `alignment`, `spacing`.

### `C.executiveSummary(paragraphs, opts?)` &rarr; Array
Shaded panel with thick left accent bar. `paragraphs`: string, string[], or Paragraph[].
Options: `title` (default "Executive Summary"), `variant`: "info" | "warning" | "neutral".

### `C.dataTable(headers, rows, opts?)` &rarr; Table
`headers`: string[]. `rows`: string[][]. Auto-calculates equal column widths.
Options: `columnWidths` (DXA array summing to 9360), `lightHeader` (gray instead of navy).

### `C.bulletList(items)` &rarr; Array
`items`: string[] or `[{lead, text}]` for bold lead-in text.

### `C.numberedList(items)` &rarr; Array
`items`: string[].

### `C.callout(text, opts?)` &rarr; Table
Bordered box with thick left accent. Options: `type`: "info" | "warning" | "tip", `label`.

### `C.keyMetrics(metrics)` &rarr; Table
Large stat display row. `metrics`: `[{value, label, color?}]`. `color`: "navy" (default) or "red".

### `C.flowSteps(steps)` &rarr; Table
Numbered process steps. `steps`: `[{title, description, number?}]`. Auto-numbers with zero-padding.

### `C.twoColumn(left, right, opts?)` &rarr; Table
Side-by-side layout. `left`/`right`: string, string[], or Paragraph[].
Options: `leftHeader`, `rightHeader`, `widths` (default [4560, 4800]).

### `C.imageBlock(path, opts?)` &rarr; Array
Image with optional caption. Options: `width` (pt, default 468), `height` (pt), `caption`, `type`, `alt`, `title`, `name`.

### `C.checklist(items)` &rarr; Table
Status tracking. `items`: `[{status, text, label?}]`. `status`: "done" | "todo" | "risk" | "na".

### `C.signatureBlock(opts?)` &rarr; Array
Sign-off area. Options: `name`, `title`, `date`, `variant`: "full" | "approval" | "compact".

### `C.headerFooter(opts?)` &rarr; Object
Returns `{headers, footers, titlePage?}`. Pass to `C.section()` via `headerFooter` option, or spread into section manually.
Options: `title`, `org`, `confidential` (string, or false to hide), `noFirstPage`.

## Utilities

| Function | Returns | Purpose |
|----------|---------|---------|
| `C.spacer(before?)` | Paragraph | Empty paragraph with spacing (default 200) |
| `C.pageBreak()` | Paragraph | Page break |
| `C.rule(opts?)` | Paragraph | Horizontal rule via border. Options: `spacing`, `size`, `color` |
| `C.hCell(text, w)` | TableCell | Navy header cell for custom tables |
| `C.dCell(text, w, opts?)` | TableCell | Data cell. Options: `shaded` |
| `C.lCell(text, w)` | TableCell | Light gray label cell (uppercase, tracked) |
| `C.equalWidths(n)` | number[] | Divide PAGE.contentWidth into n equal columns |

## Example

```javascript
const hf = C.headerFooter({ title: "Q1 2026 Business Review", org: "Acme Corp" });

C.coverPage({ title: "Q1 2026 Business Review", subtitle: "Quarterly Performance Report", date: "March 2026", author: "Jane Smith", org: "Acme Corp" }),
C.toc(),
C.section([
  C.executiveSummary([
    "Revenue grew 18% YoY to $4.2M, driven by Enterprise Dashboard adoption.",
    "Three key risks identified: supply chain delays, competitor pricing, talent retention.",
  ]),
  C.heading(2, "Key Metrics"),
  C.keyMetrics([
    { value: "$4.2M", label: "Revenue" },
    { value: "+18%", label: "YoY Growth", color: "red" },
    { value: "142", label: "Employees" },
  ]),
  C.heading(2, "Product Launches"),
  C.dataTable(
    ["Product", "Launch Date", "Status"],
    [["Enterprise Dashboard", "January 2026", "GA"], ["Mobile SDK", "February 2026", "Beta"]],
  ),
  C.heading(2, "Risk Assessment"),
  C.callout("Supply chain delays may impact Q2 hardware shipments.", { type: "warning" }),
  C.heading(2, "Next Quarter Priorities"),
  C.flowSteps([
    { title: "APAC Expansion", description: "Open regional office and begin partner onboarding." },
    { title: "Hiring Sprint", description: "15 engineers across platform and infrastructure teams." },
    { title: "Ship v3.0", description: "Major release with new billing engine and API v2." },
  ]),
], { headerFooter: hf }),
```

For raw docx-js code alongside component calls, all docx classes (Paragraph, TextRun, Table, etc.) are available in create_doc.js. Design tokens are accessible via `C.BRAND` and `C.PAGE`. For advanced patterns not covered by component functions, see the individual component markdown files in this directory.
