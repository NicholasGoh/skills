# Data Table

Professional table with navy header row, thin borders, and alternating row shading. Good for comparisons, specifications, budgets, or any structured data.

## JavaScript

```javascript
new Table({
  width: { size: PAGE.contentWidth, type: WidthType.DXA },
  columnWidths: [3120, 3120, 3120], // Must sum to PAGE.contentWidth (9360)
  rows: [
    // Header row
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({
          borders,
          width: { size: 3120, type: WidthType.DXA },
          shading: { fill: BRAND.navy, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({
              text: "COLUMN A",
              font: "Arial",
              size: 18,
              bold: true,
              color: BRAND.white,
            })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 3120, type: WidthType.DXA },
          shading: { fill: BRAND.navy, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({
              text: "COLUMN B",
              font: "Arial",
              size: 18,
              bold: true,
              color: BRAND.white,
            })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 3120, type: WidthType.DXA },
          shading: { fill: BRAND.navy, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({
              text: "COLUMN C",
              font: "Arial",
              size: 18,
              bold: true,
              color: BRAND.white,
            })],
          })],
        }),
      ],
    }),
    // Data row (white)
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 3120, type: WidthType.DXA },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({ text: "Row 1 data", size: 22 })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 3120, type: WidthType.DXA },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({ text: "Value", size: 22 })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 3120, type: WidthType.DXA },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({ text: "Detail", size: 22 })],
          })],
        }),
      ],
    }),
    // Data row (shaded)
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 3120, type: WidthType.DXA },
          shading: { fill: BRAND.lightGray, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({ text: "Row 2 data", size: 22 })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 3120, type: WidthType.DXA },
          shading: { fill: BRAND.lightGray, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({ text: "Value", size: 22 })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 3120, type: WidthType.DXA },
          shading: { fill: BRAND.lightGray, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({ text: "Detail", size: 22 })],
          })],
        }),
      ],
    }),
  ],
}),
```

Alternate white and `lightGray` shading on data rows for readability. Navy header with white text provides strong visual anchoring. Adjust `columnWidths` for your data but ensure they sum to `PAGE.contentWidth` (9360 DXA).

**Width calculation:** For N equal columns: `Math.floor(PAGE.contentWidth / N)`. Distribute remainders to the last column. For mixed widths: allocate proportionally but always sum to 9360.

**Variant: Light header** (for less formal documents):

Replace the navy header shading with light gray and use dark text:
```javascript
shading: { fill: BRAND.lightGray, type: ShadingType.CLEAR },
// Text run:
color: BRAND.black, // instead of BRAND.white
```
