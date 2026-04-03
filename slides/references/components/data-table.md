# Data Table

Styled table with spotlight row hover. Good for benchmarks, comparisons, specifications, or any tabular data. Renders as a bordered, rounded table with uppercase muted header row. Semantic cell classes (`bt-dataset`, `bt-source`, `bt-example`, `bt-limit`) are optional helpers for column styling; plain `<td>` with default styling works fine for simpler tables.

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
