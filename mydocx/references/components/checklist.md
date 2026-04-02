# Checklist

Status items with colored labels and descriptions. Uses a table with narrow status column and wide description column. Three built-in status styles: green (DONE), navy (TODO), red (RISK). Good for requirements tracking, audit items, onboarding checklists.

## JavaScript

```javascript
new Table({
  width: { size: PAGE.contentWidth, type: WidthType.DXA },
  columnWidths: [1200, 8160],
  rows: [
    // Header
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({
          borders,
          width: { size: 1200, type: WidthType.DXA },
          shading: { fill: BRAND.lightGray, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({
              text: "STATUS",
              font: "Arial",
              size: 16,
              bold: true,
              color: BRAND.muted,
              characterSpacing: 60,
            })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 8160, type: WidthType.DXA },
          shading: { fill: BRAND.lightGray, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({
              text: "ITEM",
              font: "Arial",
              size: 16,
              bold: true,
              color: BRAND.muted,
              characterSpacing: 60,
            })],
          })],
        }),
      ],
    }),
    // Completed item (green)
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 1200, type: WidthType.DXA },
          shading: { fill: "E8F5E9", type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: "DONE",
              font: "Arial",
              size: 16,
              bold: true,
              color: "2E7D32",
            })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 8160, type: WidthType.DXA },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({ text: "Set up development environment", size: 22 })],
          })],
        }),
      ],
    }),
    // Pending item (navy)
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 1200, type: WidthType.DXA },
          shading: { fill: BRAND.headerBg, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: "TODO",
              font: "Arial",
              size: 16,
              bold: true,
              color: BRAND.navy,
            })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 8160, type: WidthType.DXA },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({ text: "Complete onboarding training", size: 22 })],
          })],
        }),
      ],
    }),
    // At risk item (red)
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 1200, type: WidthType.DXA },
          shading: { fill: BRAND.red50, type: ShadingType.CLEAR },
          margins: pad,
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: "RISK",
              font: "Arial",
              size: 16,
              bold: true,
              color: BRAND.darkRed,
            })],
          })],
        }),
        new TableCell({
          borders,
          width: { size: 8160, type: WidthType.DXA },
          margins: pad,
          children: [new Paragraph({
            children: [new TextRun({ text: "Security review pending external audit", size: 22 })],
          })],
        }),
      ],
    }),
  ],
}),
```

The colored status column provides instant visual scanning. Add more status types by choosing appropriate fill colors:

| Status | Fill | Text Color |
|--------|------|------------|
| DONE | `E8F5E9` | `2E7D32` (green) |
| TODO | `BRAND.headerBg` | `BRAND.navy` |
| RISK | `BRAND.red50` | `BRAND.darkRed` |
| N/A | `BRAND.lightGray` | `BRAND.muted` |
