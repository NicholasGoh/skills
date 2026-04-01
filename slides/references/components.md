# Component Catalog

Each component below includes its HTML structure and any CSS that must be added to the `<style>` block alongside the engine CSS in the template. Pick the components that fit your content. Mix and match freely.

All grid layouts should use the class `slide-grid` in addition to any component-specific class, so the responsive override in the template works.

---

## Table of Contents

1. [Title Slide](#1-title-slide) — Hero with heading, subtitle, and optional sidebar
2. [Two-Column with Sidebar](#2-two-column-with-sidebar) — Section label + heading left, content right
3. [Numbered List](#3-numbered-list) — Circled numbers with title + description
4. [Grade / Rating Cards](#4-grade--rating-cards) — Letter/icon + title + description rows
5. [Flow Steps](#5-flow-steps) — Numbered process sequence
6. [Principle / Checklist](#6-principle--checklist) — Numbered rows with pill status
7. [Risk / Feature Cards](#7-risk--feature-cards) — Bordered cards with tag, description, and mapped pills
8. [Data Table](#8-data-table) — Styled table with spotlight row hover
9. [Icon Cards](#9-icon-cards) — Cards with colored icon header + bullet list
10. [Sidebar Panel](#10-sidebar-panel) — Gray rounded box with labeled rows
11. [Stat Callouts](#11-stat-callouts) — Large number + label pairs

---

## 1. Title Slide

The opening slide. Two-column: left has tag line, h1, subtitle, and optional legend/method row. Right has a sidebar summary panel.

### HTML

```html
<section class="slide" id="slide-1">
    <div class="slide-inner">
        <div class="title-grid slide-grid">
            <div>
                <div class="tag-line reveal s1">
                    <span class="dot"></span>
                    <span class="text">CATEGORY LABEL</span>
                </div>
                <h1 class="reveal s2">Main<br>Heading</h1>
                <p class="title-subtitle desc reveal s3">Brief description of what this presentation covers and its scope.</p>

                <!-- Optional: method/legend row -->
                <div class="method-row reveal s4">
                    <div class="method-item">
                        <div class="icon primary"></div>
                        <div>
                            <div class="m-label">Category A</div>
                            <div class="m-desc">Short description</div>
                        </div>
                    </div>
                    <div class="method-item">
                        <div class="icon accent"></div>
                        <div>
                            <div class="m-label">Category B</div>
                            <div class="m-desc">Short description</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sidebar (see Sidebar Panel component) -->
            <div class="sidebar reveal s5 spot-group">
                <div class="sidebar-title">Summary</div>
                <!-- sidebar rows here -->
            </div>
        </div>
    </div>
    <span class="slide-num">01 / TOTAL</span>
</section>
```

### CSS

```css
.title-grid {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 4rem;
    align-items: center;
}

.title-subtitle {
    max-width: 460px;
    margin-bottom: 3vh;
}

.method-row {
    display: flex;
    gap: 1.5rem;
}

.method-item {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
}

.method-item .icon {
    width: 8px;
    height: 8px;
    border-radius: 2px;
    flex-shrink: 0;
    margin-top: 2px;
}

.method-item .icon.primary { background: var(--brand-navy); }
.method-item .icon.accent { background: var(--brand-red); }

.method-item .m-label {
    font-size: 0.75rem;
    color: var(--brand-black);
    font-weight: 500;
}

.method-item .m-desc {
    font-size: 0.7rem;
    color: var(--brand-muted);
    font-weight: 300;
}
```

---

## 2. Two-Column with Sidebar

The standard content slide layout. Left column has section label, h2, and description. Right column has the main content (list, cards, table, etc.).

### HTML

```html
<section class="slide alt" id="slide-N">
    <div class="slide-inner">
        <div class="content-grid slide-grid">
            <div>
                <p class="section-label reveal s1">Section Name</p>
                <h2 class="reveal s2">Slide<br>Title</h2>
                <p class="desc reveal s3">Supporting description that provides context for the content on the right.</p>
            </div>

            <div>
                <!-- Content component goes here -->
            </div>
        </div>
    </div>
    <span class="slide-num">0N / TOTAL</span>
</section>
```

### CSS

```css
.content-grid {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 4rem;
    align-items: start;
}
```

**Variant — wide sidebar** (for slides where the left description needs more room):
```css
.content-grid.wide-left {
    grid-template-columns: 1fr 320px;
}
```

---

## 3. Numbered List

Circled numbers with title + description. Good for rules, methodology steps, or criteria.

Use inside a Two-Column layout on the right side. Apply `spot-group` on the container and `spot-item` on each item.

### HTML

```html
<div class="rule-list spot-group">
    <div class="rule-item spot-item reveal s2">
        <div class="ri-icon">1</div>
        <div>
            <div class="ri-title">Rule Title</div>
            <div class="ri-desc">Description of this rule or criterion and how it applies.</div>
        </div>
    </div>
    <div class="rule-item spot-item reveal s3">
        <div class="ri-icon">2</div>
        <div>
            <div class="ri-title">Another Rule</div>
            <div class="ri-desc">Further explanation of this point.</div>
        </div>
    </div>
    <!-- more items... -->
</div>
```

### CSS

```css
.rule-list {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.rule-item {
    display: grid;
    grid-template-columns: 28px 1fr;
    gap: 1rem;
    padding: 1.2em 0;
    border-bottom: 1px solid var(--border);
    align-items: start;
}

.rule-item:last-child { border-bottom: none; }

.rule-item .ri-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    background: var(--brand-white);
    border: 1px solid var(--border);
    color: var(--brand-red);
}

/* On alt (gray) slides, icon background stays white */
.slide.alt .rule-item .ri-icon { background: var(--brand-white); }

.rule-item .ri-title {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--brand-black);
    margin-bottom: 0.2em;
}

.rule-item .ri-desc {
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--brand-muted);
    line-height: 1.6;
}
```

---

## 4. Grade / Rating Cards

Rows with a prominent letter/grade/icon and description. Good for rating scales, status levels, or categorized items.

### HTML

```html
<div class="grade-cards spot-group">
    <div class="grade-card spot-item reveal s2">
        <div class="gc-letter a">A</div>
        <div>
            <div class="gc-title">Excellent</div>
            <div class="gc-desc">Fully meets all requirements, no issues</div>
        </div>
    </div>
    <div class="grade-card spot-item reveal s3">
        <div class="gc-letter b">B</div>
        <div>
            <div class="gc-title">Good</div>
            <div class="gc-desc">Meets requirements with minor improvements needed</div>
        </div>
    </div>
    <!-- more grades... -->
</div>
```

### CSS

```css
.grade-cards {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.grade-card {
    display: grid;
    grid-template-columns: 52px 1fr;
    gap: 1rem;
    padding: 1.1em 0;
    border-bottom: 1px solid var(--border);
    align-items: baseline;
}

.grade-card:last-child { border-bottom: none; }

.grade-card .gc-letter {
    font-family: var(--font-heading);
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
}

/* Color each grade — adjust these to match your rating scheme */
.grade-card .gc-letter.a { color: #16a34a; }
.grade-card .gc-letter.b { color: #2563eb; }
.grade-card .gc-letter.c { color: #ca8a04; }
.grade-card .gc-letter.d { color: #ea580c; }
.grade-card .gc-letter.f { color: var(--brand-red); }
.grade-card .gc-letter.na { color: var(--brand-grey-100); }

.grade-card .gc-title {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--brand-black);
}

.grade-card .gc-desc {
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--brand-muted);
    line-height: 1.5;
    margin-top: 0.15em;
}
```

---

## 5. Flow Steps

Numbered process with red-accented step numbers. Good for workflows, timelines, or sequential processes.

### HTML

```html
<div class="flow-steps spot-group">
    <div class="flow-step spot-item reveal s2">
        <div class="fs-num">1</div>
        <div>
            <div class="fs-title">First Step</div>
            <div class="fs-desc">Description of what happens in this step.</div>
        </div>
    </div>
    <div class="flow-step spot-item reveal s3">
        <div class="fs-num">2</div>
        <div>
            <div class="fs-title">Second Step</div>
            <div class="fs-desc">Description of what happens next.</div>
        </div>
    </div>
    <!-- more steps... -->
</div>
```

### CSS

```css
.flow-steps {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.flow-step {
    display: grid;
    grid-template-columns: 40px 1fr;
    gap: 1rem;
    padding: 1.2em 0;
    border-bottom: 1px solid var(--border);
    align-items: start;
}

.flow-step:last-child { border-bottom: none; }

.flow-step .fs-num {
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--brand-red);
    background: var(--brand-white);
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border);
}

.flow-step .fs-title {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--brand-black);
    margin-bottom: 0.2em;
}

.flow-step .fs-desc {
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--brand-muted);
    line-height: 1.6;
}
```

---

## 6. Principle / Checklist

Numbered rows with status pills. Good for feature lists, governance principles, requirements, or any list where items have a status/category.

### HTML

```html
<div class="principle-list spot-group">
    <div class="pl-item active spot-item reveal s2">
        <div class="pl-num">01</div>
        <div class="pl-name">Active Item Name</div>
        <span class="pill primary">Active</span>
    </div>
    <div class="pl-item inactive spot-item reveal s3">
        <div class="pl-num">02</div>
        <div class="pl-name">Inactive Item Name</div>
        <span class="pill muted">Skipped</span>
    </div>
    <!-- more items... -->
</div>
```

### CSS

```css
.principle-list {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.pl-item {
    display: grid;
    grid-template-columns: 32px 1fr auto;
    gap: 0.8rem;
    padding: 0.75em 0;
    border-bottom: 1px solid var(--border);
    align-items: center;
}

.pl-item:last-child { border-bottom: none; }

.pl-item .pl-num {
    font-family: var(--font-heading);
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--brand-muted);
    text-align: center;
}

.pl-item.active .pl-num { color: var(--brand-red); }

.pl-item .pl-name {
    font-size: 0.82rem;
    font-weight: 400;
    color: var(--brand-black);
}

.pl-item.inactive .pl-name { color: var(--brand-muted); }
```

---

## 7. Risk / Feature Cards

Bordered cards with a tag, title, description, and optional pill row. Uses `.spot-card` for sibling-dim hover. Good for risks, features, highlights, or callouts.

### HTML

```html
<div>
    <div class="risk-card spot-card reveal s4">
        <div class="rc-header">
            <span class="rc-tag">Label 1</span>
            <span class="rc-title">Card Title</span>
        </div>
        <div class="rc-desc">Description of this item and why it matters.</div>
        <div class="rc-maps">
            <span class="rc-pill">Related A</span>
            <span class="rc-pill">Related B</span>
        </div>
    </div>

    <div class="risk-card spot-card reveal s5">
        <div class="rc-header">
            <span class="rc-tag">Label 2</span>
            <span class="rc-title">Another Card</span>
        </div>
        <div class="rc-desc">Another description.</div>
        <div class="rc-maps">
            <span class="rc-pill">Related C</span>
        </div>
    </div>
</div>
```

### CSS

```css
.risk-card {
    background: var(--brand-white);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.4em 1.3em;
    margin-bottom: 1rem;
}

.risk-card .rc-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.6em;
}

.risk-card .rc-tag {
    font-family: var(--font-heading);
    font-size: 0.6rem;
    font-weight: 600;
    color: var(--brand-dark-red);
    background: var(--brand-red-50);
    padding: 0.25em 0.5em;
    border-radius: 3px;
}

.risk-card .rc-title {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--brand-black);
}

.risk-card .rc-desc {
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--brand-muted);
    line-height: 1.6;
    margin-bottom: 0.6em;
}

.risk-card .rc-maps {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
}

.risk-card .rc-pill {
    font-size: 0.58rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    color: var(--brand-navy);
    background: var(--bg-header);
    padding: 0.25em 0.5em;
    border-radius: 3px;
}
```

---

## 8. Data Table

Styled table with spotlight row hover. Good for benchmarks, comparisons, specifications, or any tabular data.

### HTML

```html
<table class="bench-table spot-table reveal s4">
    <thead>
        <tr>
            <th>Column A</th>
            <th>Column B</th>
            <th>Column C</th>
            <th>Column D</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="bt-dataset"><a href="#">Dataset Name</a></td>
            <td class="bt-source"><a href="#">Source</a></td>
            <td class="bt-example">Example data point or description</td>
            <td class="bt-limit">Limitation or note</td>
        </tr>
        <!-- more rows... -->
    </tbody>
</table>
```

### CSS

```css
.bench-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
}

.bench-table th {
    font-family: var(--font-heading);
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--brand-muted);
    background: var(--brand-light-gray);
    padding: 0.7em 0.8em;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

.bench-table td {
    font-size: 0.72rem;
    font-weight: 300;
    color: var(--brand-black);
    padding: 0.8em;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
    line-height: 1.5;
}

.bench-table tr:last-child td { border-bottom: none; }

.bench-table .bt-dataset {
    font-family: var(--font-heading);
    font-size: 0.7rem;
    font-weight: 600;
    white-space: nowrap;
}

.bench-table .bt-dataset a {
    color: var(--brand-navy);
    text-decoration: none;
    border-bottom: 1px solid var(--bg-header);
}

.bench-table .bt-dataset a:hover { border-bottom-color: var(--brand-navy); }

.bench-table .bt-source {
    font-size: 0.65rem;
    color: var(--brand-muted);
    white-space: nowrap;
}

.bench-table .bt-source a {
    color: var(--brand-muted);
    text-decoration: none;
}

.bench-table .bt-source a:hover { color: var(--brand-navy); }

.bench-table .bt-example {
    font-size: 0.68rem;
    color: var(--brand-muted);
    font-style: italic;
}

.bench-table .bt-limit {
    font-size: 0.68rem;
    color: var(--brand-dark-red);
    font-weight: 400;
}
```

Table cells don't need the `bt-*` classes — those are semantic helpers. For simpler tables, plain `<td>` with default styling works fine.

---

## 9. Icon Cards

Cards with a colored icon square, title, and bullet list. Uses container hover dimming. Good for action items, plans, or categorized feature sets.

### HTML

```html
<div class="icon-cards">
    <div class="icon-card reveal s3">
        <div class="icon-card-header">
            <div class="icon-card-icon primary">&#9741;</div>
            <div class="icon-card-title">Card Title</div>
        </div>
        <ul>
            <li>First bullet point</li>
            <li>Second bullet point</li>
            <li>Third bullet point</li>
        </ul>
    </div>

    <div class="icon-card reveal s4">
        <div class="icon-card-header">
            <div class="icon-card-icon accent">&#9834;</div>
            <div class="icon-card-title">Another Card</div>
        </div>
        <ul>
            <li>Item one</li>
            <li>Item two</li>
        </ul>
    </div>
</div>
```

### CSS

```css
.icon-cards {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

.icon-card {
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    background: var(--brand-white);
    transition: border-color 0.25s ease, box-shadow 0.25s ease, opacity 0.25s ease;
}

.icon-card:hover {
    border-color: var(--brand-navy);
    box-shadow: 0 3px 12px rgba(26, 31, 93, 0.07);
}

.icon-cards:hover .icon-card:not(:hover) {
    opacity: 0.4;
}

.icon-card-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.6rem;
}

.icon-card-icon {
    width: 28px;
    height: 28px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    flex-shrink: 0;
}

.icon-card-icon.primary { background: var(--bg-header); color: var(--brand-navy); }
.icon-card-icon.accent { background: var(--brand-red-50); color: var(--brand-dark-red); }
.icon-card-icon.success { background: #E8F5E9; color: #2E7D32; }

.icon-card-title {
    font-family: var(--font-heading);
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--brand-navy);
}

.icon-card ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.icon-card li {
    font-size: 0.75rem;
    color: var(--brand-muted);
    line-height: 1.6;
    padding-left: 1em;
    position: relative;
}

.icon-card li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.55em;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: var(--brand-grey-100);
}
```

---

## 10. Sidebar Panel

A light-gray rounded box with a title and labeled rows. Used in title slides for summaries, or anywhere you need a compact reference panel.

### HTML

```html
<div class="sidebar spot-group">
    <div class="sidebar-title">Panel Title</div>
    <div class="p-row spot-row">
        <span class="p-label">Item Name</span>
        <span class="pill primary">Status</span>
    </div>
    <div class="p-row spot-row">
        <span class="p-label">Another Item</span>
        <span class="pill accent">Urgent</span>
    </div>
    <div class="p-row dimmed spot-row">
        <span class="p-label">Inactive Item</span>
        <span class="pill muted">Deferred</span>
    </div>
</div>
```

### CSS

```css
.sidebar {
    background: var(--brand-light-gray);
    border-radius: 10px;
    padding: 2em 1.8em;
}

.sidebar-title {
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--brand-muted);
    margin-bottom: 1.5em;
}

.p-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.65em 0;
    border-bottom: 1px solid var(--border);
}

.p-row:last-child { border-bottom: none; }

.p-row .p-label {
    font-size: 0.8rem;
    font-weight: 400;
    color: var(--brand-black);
}

.p-row.dimmed .p-label { color: var(--brand-muted); }
```

---

## 11. Stat Callouts

Large numbers with supporting labels. Good for KPIs, summary metrics, or score breakdowns. Arrange in a row or grid.

### HTML

```html
<div class="stat-row reveal s3">
    <div class="stat-item">
        <div class="stat-value">94%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-item">
        <div class="stat-value accent">3</div>
        <div class="stat-label">Critical Issues</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">B+</div>
        <div class="stat-label">Overall Grade</div>
    </div>
</div>
```

### CSS

```css
.stat-row {
    display: flex;
    gap: 3rem;
    margin: 2vh 0;
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-family: var(--font-heading);
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    color: var(--brand-navy);
    line-height: 1.1;
}

.stat-value.accent { color: var(--brand-red); }

.stat-label {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--brand-muted);
    margin-top: 0.5em;
}
```

---

## Deprioritised / Secondary Content

For secondary or deprioritised items shown in a sidebar or aside. Muted styling signals lower importance.

### HTML

```html
<div class="depri-sidebar">
    <div class="ds-title">Section Title</div>
    <div class="depri-item">
        <div class="di-name">Item Name</div>
        <div class="di-reason">Reason this is deprioritised or note</div>
    </div>
    <div class="depri-item">
        <div class="di-name">Another Item</div>
        <div class="di-reason">Another reason</div>
    </div>
    <div class="depri-source">Source: <a href="#" class="ref-link">Reference Link</a></div>
</div>
```

### CSS

```css
.depri-sidebar {
    padding-top: 0.5em;
}

.depri-sidebar .ds-title {
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--brand-muted);
    margin-bottom: 1.5em;
}

.depri-item {
    padding: 0.8em 0;
    border-bottom: 1px solid var(--border);
}

.depri-item:last-child { border-bottom: none; }

.depri-item .di-name {
    font-size: 0.82rem;
    font-weight: 400;
    color: var(--brand-muted);
    margin-bottom: 0.2em;
}

.depri-item .di-reason {
    font-size: 0.72rem;
    font-weight: 300;
    font-style: italic;
    color: var(--brand-grey-100);
    line-height: 1.5;
}

.depri-source {
    margin-top: 2em;
    font-size: 0.65rem;
    color: var(--brand-grey-100);
    letter-spacing: 0.05em;
}
```
