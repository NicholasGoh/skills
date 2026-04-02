# Two-Column Layout

Side-by-side content using a borderless table. Good for comparisons, pros/cons, before/after, or any content that benefits from parallel viewing.

## JavaScript

```javascript
new Table({
  width: { size: PAGE.contentWidth, type: WidthType.DXA },
  columnWidths: [4560, 4800], // Slightly unequal for visual interest
  rows: [
    // Header row
    new TableRow({
      children: [
        new TableCell({
          borders: { ...noBorders, bottom: { style: BorderStyle.SINGLE, size: 2, color: BRAND.navy } },
          width: { size: 4560, type: WidthType.DXA },
          margins: { top: 80, bottom: 120, left: 0, right: 200 },
          children: [new Paragraph({
            children: [new TextRun({
              text: "LEFT HEADING",
              font: "Arial",
              size: 18,
              bold: true,
              color: BRAND.navy,
              characterSpacing: 60,
            })],
          })],
        }),
        new TableCell({
          borders: { ...noBorders, bottom: { style: BorderStyle.SINGLE, size: 2, color: BRAND.navy } },
          width: { size: 4800, type: WidthType.DXA },
          margins: { top: 80, bottom: 120, left: 200, right: 0 },
          children: [new Paragraph({
            children: [new TextRun({
              text: "RIGHT HEADING",
              font: "Arial",
              size: 18,
              bold: true,
              color: BRAND.navy,
              characterSpacing: 60,
            })],
          })],
        }),
      ],
    }),
    // Content row
    new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          width: { size: 4560, type: WidthType.DXA },
          margins: { top: 160, bottom: 120, left: 0, right: 200 },
          children: [
            new Paragraph({
              spacing: { after: 120 },
              children: [new TextRun({
                text: "Content for the left side. Works well for the current state, existing approach, or the 'before' in a comparison.",
                size: 22,
                color: BRAND.black,
              })],
            }),
          ],
        }),
        new TableCell({
          borders: noBorders,
          width: { size: 4800, type: WidthType.DXA },
          margins: { top: 160, bottom: 120, left: 200, right: 0 },
          children: [
            new Paragraph({
              spacing: { after: 120 },
              children: [new TextRun({
                text: "Content for the right side. Use for the proposed state, new approach, or the 'after' in a comparison.",
                size: 22,
                color: BRAND.black,
              })],
            }),
          ],
        }),
      ],
    }),
  ],
}),
```

The navy bottom border on headers and generous margins between columns create clean visual separation without heavy borders. Adjust column widths as needed, keeping the sum at `PAGE.contentWidth`.

**Variant: Flowing multi-column** (newsletter-style, text wraps across columns):
```javascript
// In section properties (not a table — text flows naturally)
column: { count: 2, space: 720, equalWidth: true, separate: true },
```
Use this when text should flow continuously. Use the table approach above when left and right content are independent blocks.

**Variant: Three columns** (for feature comparisons):
```javascript
columnWidths: [3120, 3120, 3120], // Equal thirds
```
