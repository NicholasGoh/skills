# Executive Summary

Shaded panel highlighting key findings, recommendations, or decisions. Uses a single-cell table with light background and a thick navy left border as an accent bar. The box effect works because docx-js doesn't support paragraph-level shading directly.

## JavaScript

```javascript
new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [new TextRun({ text: "Executive Summary" })],
}),
new Table({
  width: { size: PAGE.contentWidth, type: WidthType.DXA },
  columnWidths: [PAGE.contentWidth],
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders: {
            top: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border },
            bottom: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border },
            left: { style: BorderStyle.SINGLE, size: 6, color: BRAND.navy },
            right: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border },
          },
          shading: { fill: BRAND.headerBg, type: ShadingType.CLEAR },
          margins: { top: 160, bottom: 160, left: 200, right: 200 },
          width: { size: PAGE.contentWidth, type: WidthType.DXA },
          children: [
            new Paragraph({
              spacing: { after: 120 },
              children: [new TextRun({
                text: "Key finding or recommendation goes here. Keep it concise and actionable.",
                font: "Arial",
                size: 22,
                color: BRAND.black,
              })],
            }),
            new Paragraph({
              children: [new TextRun({
                text: "Additional context or supporting detail. Focus on what the reader needs to decide or act on.",
                font: "Arial",
                size: 22,
                color: BRAND.muted,
              })],
            }),
          ],
        }),
      ],
    }),
  ],
}),
```

The thick navy left border creates a visual accent bar that signals importance without being heavy. Replace the background (`headerBg`) with `red50` for warnings or `lightGray` for neutral summaries.

**Variant: Bulleted summary**

Replace the paragraphs inside the cell with bullet-formatted paragraphs for a list of key points:

```javascript
new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [new TextRun({ text: "Revenue increased 18% year over year", size: 22 })],
}),
new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [new TextRun({ text: "Three key risks identified for Q2", size: 22 })],
}),
new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  children: [new TextRun({ text: "Board approved APAC expansion timeline", size: 22 })],
}),
```
