# Component Catalog

Pick the components that fit your content. Mix and match freely within the sections array.

Each component provides JavaScript code for the docx-js library. Insert component code into the `/* __SECTIONS__ */` marker in the template, combining section objects as needed. Components reference the template's shared helpers (`BRAND`, `PAGE`, `borders`, `noBorders`, `pad`, `thin`, `none`).

| # | Component | File | When to use |
|---|-----------|------|-------------|
| 1 | Cover Page | `cover-page.md` | Title page with branding, title, date, and author |
| 2 | Table of Contents | `table-of-contents.md` | Auto-generated navigation from heading levels |
| 3 | Executive Summary | `executive-summary.md` | Shaded panel with key findings or recommendations |
| 4 | Data Table | `data-table.md` | Structured data, comparisons, budgets, specs |
| 5 | Bullet List | `bullet-list.md` | Action items, requirements, features, any list |
| 6 | Callout Box | `callout-box.md` | Tips, warnings, notes, important callouts |
| 7 | Key Metrics | `key-metrics.md` | Large stat numbers, KPIs, performance highlights |
| 8 | Flow Steps | `flow-steps.md` | Processes, timelines, sequential procedures |
| 9 | Two-Column Layout | `two-column-layout.md` | Side-by-side comparisons, pros/cons, before/after |
| 10 | Image Block | `image-block.md` | Photos, diagrams, charts with captions |
| 11 | Checklist | `checklist.md` | Status items, requirements tracking, audit lists |
| 12 | Signature Block | `signature-block.md` | Approvals, sign-offs, author attribution |
| 13 | Header Footer | `header-footer.md` | Running header with title, footer with page numbers |
