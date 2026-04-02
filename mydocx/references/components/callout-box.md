# Callout Box

Bordered box for tips, warnings, notes, or any content that needs visual separation from body text. Uses a single-cell table with a thick accent left border and light shading. The thick left border is the visual signature of this component.

## JavaScript

**Info callout (navy accent):**
```javascript
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
            left: { style: BorderStyle.SINGLE, size: 8, color: BRAND.navy },
            right: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border },
          },
          shading: { fill: BRAND.headerBg, type: ShadingType.CLEAR },
          margins: { top: 120, bottom: 120, left: 200, right: 200 },
          width: { size: PAGE.contentWidth, type: WidthType.DXA },
          children: [
            new Paragraph({
              spacing: { after: 80 },
              children: [new TextRun({
                text: "NOTE",
                font: "Arial",
                size: 16,
                bold: true,
                color: BRAND.navy,
                characterSpacing: 60,
              })],
            }),
            new Paragraph({
              children: [new TextRun({
                text: "This is important information the reader should be aware of.",
                font: "Arial",
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

**Warning callout (red accent):**

Replace navy references with red:
```javascript
left: { style: BorderStyle.SINGLE, size: 8, color: BRAND.red },
shading: { fill: BRAND.red50, type: ShadingType.CLEAR },
// Label text run:
text: "WARNING", color: BRAND.darkRed,
```

**Tip callout (neutral):**
```javascript
left: { style: BorderStyle.SINGLE, size: 8, color: BRAND.muted },
shading: { fill: BRAND.lightGray, type: ShadingType.CLEAR },
// Label text run:
text: "TIP", color: BRAND.muted,
```

Keep callout text concise. If the content is longer than a few sentences, it probably belongs in the main body rather than a callout. The label (NOTE, WARNING, TIP) is optional but helps scanning.
