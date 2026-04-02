# Flow Steps

Numbered process steps displayed as a vertical sequence. Uses a two-column table: narrow left for red step numbers, wide right for content. Good for workflows, timelines, onboarding steps, or any sequential procedure.

## JavaScript

```javascript
new Table({
  width: { size: PAGE.contentWidth, type: WidthType.DXA },
  columnWidths: [800, 8560],
  rows: [
    // Step 1
    new TableRow({
      children: [
        new TableCell({
          borders: { ...noBorders, bottom: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border } },
          width: { size: 800, type: WidthType.DXA },
          margins: { top: 120, bottom: 120, left: 0, right: 80 },
          verticalAlign: VerticalAlign.TOP,
          children: [new Paragraph({
            children: [new TextRun({
              text: "01",
              font: "Arial",
              size: 28,
              bold: true,
              color: BRAND.red,
            })],
          })],
        }),
        new TableCell({
          borders: { ...noBorders, bottom: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border } },
          width: { size: 8560, type: WidthType.DXA },
          margins: { top: 120, bottom: 120, left: 80, right: 0 },
          verticalAlign: VerticalAlign.TOP,
          children: [
            new Paragraph({
              spacing: { after: 60 },
              children: [new TextRun({
                text: "Step Title",
                font: "Arial",
                size: 24,
                bold: true,
                color: BRAND.black,
              })],
            }),
            new Paragraph({
              children: [new TextRun({
                text: "Description of what happens in this step and any relevant details.",
                font: "Arial",
                size: 22,
                color: BRAND.muted,
              })],
            }),
          ],
        }),
      ],
    }),
    // Step 2
    new TableRow({
      children: [
        new TableCell({
          borders: { ...noBorders, bottom: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border } },
          width: { size: 800, type: WidthType.DXA },
          margins: { top: 120, bottom: 120, left: 0, right: 80 },
          verticalAlign: VerticalAlign.TOP,
          children: [new Paragraph({
            children: [new TextRun({
              text: "02",
              font: "Arial",
              size: 28,
              bold: true,
              color: BRAND.red,
            })],
          })],
        }),
        new TableCell({
          borders: { ...noBorders, bottom: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border } },
          width: { size: 8560, type: WidthType.DXA },
          margins: { top: 120, bottom: 120, left: 80, right: 0 },
          verticalAlign: VerticalAlign.TOP,
          children: [
            new Paragraph({
              spacing: { after: 60 },
              children: [new TextRun({
                text: "Next Step Title",
                font: "Arial",
                size: 24,
                bold: true,
                color: BRAND.black,
              })],
            }),
            new Paragraph({
              children: [new TextRun({
                text: "Description of what happens next.",
                font: "Arial",
                size: 22,
                color: BRAND.muted,
              })],
            }),
          ],
        }),
      ],
    }),
    // Step 3 (last — no bottom border)
    new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          width: { size: 800, type: WidthType.DXA },
          margins: { top: 120, bottom: 120, left: 0, right: 80 },
          verticalAlign: VerticalAlign.TOP,
          children: [new Paragraph({
            children: [new TextRun({
              text: "03",
              font: "Arial",
              size: 28,
              bold: true,
              color: BRAND.red,
            })],
          })],
        }),
        new TableCell({
          borders: noBorders,
          width: { size: 8560, type: WidthType.DXA },
          margins: { top: 120, bottom: 120, left: 80, right: 0 },
          verticalAlign: VerticalAlign.TOP,
          children: [
            new Paragraph({
              spacing: { after: 60 },
              children: [new TextRun({
                text: "Final Step Title",
                font: "Arial",
                size: 24,
                bold: true,
                color: BRAND.black,
              })],
            }),
            new Paragraph({
              children: [new TextRun({
                text: "Description of the final step.",
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

Red step numbers are the visual signature, matching the slides design system. Use zero-padded numbers (`01`, `02`, etc.) for alignment. Remove the bottom border on the last row for a clean finish. Each step has a bold title and muted description.
