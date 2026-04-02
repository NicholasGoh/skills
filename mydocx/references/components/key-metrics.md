# Key Metrics

Large stat numbers with labels, displayed in a borderless table row. Good for KPIs, dashboards, performance highlights, or any numbers that need visual prominence at a glance.

## JavaScript

```javascript
new Table({
  width: { size: PAGE.contentWidth, type: WidthType.DXA },
  columnWidths: [3120, 3120, 3120], // Equal thirds
  rows: [
    new TableRow({
      children: [
        // Metric 1
        new TableCell({
          borders: noBorders,
          width: { size: 3120, type: WidthType.DXA },
          margins: { top: 120, bottom: 120, left: 120, right: 120 },
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              spacing: { after: 40 },
              children: [new TextRun({
                text: "$4.2M",
                font: "Arial",
                size: 48,
                bold: true,
                color: BRAND.navy,
              })],
            }),
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({
                text: "REVENUE",
                font: "Arial",
                size: 16,
                bold: true,
                color: BRAND.muted,
                characterSpacing: 60,
              })],
            }),
          ],
        }),
        // Metric 2
        new TableCell({
          borders: noBorders,
          width: { size: 3120, type: WidthType.DXA },
          margins: { top: 120, bottom: 120, left: 120, right: 120 },
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              spacing: { after: 40 },
              children: [new TextRun({
                text: "+18%",
                font: "Arial",
                size: 48,
                bold: true,
                color: BRAND.red,
              })],
            }),
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({
                text: "YOY GROWTH",
                font: "Arial",
                size: 16,
                bold: true,
                color: BRAND.muted,
                characterSpacing: 60,
              })],
            }),
          ],
        }),
        // Metric 3
        new TableCell({
          borders: noBorders,
          width: { size: 3120, type: WidthType.DXA },
          margins: { top: 120, bottom: 120, left: 120, right: 120 },
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              spacing: { after: 40 },
              children: [new TextRun({
                text: "142",
                font: "Arial",
                size: 48,
                bold: true,
                color: BRAND.navy,
              })],
            }),
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({
                text: "EMPLOYEES",
                font: "Arial",
                size: 16,
                bold: true,
                color: BRAND.muted,
                characterSpacing: 60,
              })],
            }),
          ],
        }),
      ],
    }),
  ],
}),
```

Use navy for neutral metrics and red for growth/change indicators. For 2 or 4 metrics, adjust `columnWidths` accordingly (always summing to `PAGE.contentWidth`).

**Variant: With top border** for visual grounding:
```javascript
// Replace noBorders on cells with:
borders: {
  top: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border },
  bottom: none, left: none, right: none,
},
```

**Variant: Two metrics** (wider, more impact):
```javascript
columnWidths: [4680, 4680], // Half each
// Use size: 56 for even larger numbers
```
