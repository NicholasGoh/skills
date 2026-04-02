# Data Table

Styled table with spotlight row hover. Good for benchmarks, comparisons, specifications, or any tabular data.

## HTML

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

## CSS

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

Table cells don't need the `bt-*` classes; those are semantic helpers. For simpler tables, plain `<td>` with default styling works fine.
