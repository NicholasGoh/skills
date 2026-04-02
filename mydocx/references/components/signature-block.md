# Signature Block

Author sign-off area with horizontal rule, name, title, and date. Used at the end of memos, letters, proposals, and formal documents.

## JavaScript

```javascript
// Horizontal rule
new Paragraph({
  spacing: { before: 600 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: BRAND.border, space: 1 } },
}),

// Spacer
new Paragraph({ spacing: { before: 400 } }),

// Author name
new Paragraph({
  spacing: { after: 60 },
  children: [new TextRun({
    text: "Author Name",
    font: "Arial",
    size: 24,
    bold: true,
    color: BRAND.navy,
  })],
}),

// Title
new Paragraph({
  spacing: { after: 60 },
  children: [new TextRun({
    text: "Title, Department",
    font: "Arial",
    size: 22,
    color: BRAND.muted,
  })],
}),

// Date
new Paragraph({
  children: [new TextRun({
    text: "January 15, 2026",
    font: "Arial",
    size: 22,
    color: BRAND.muted,
  })],
}),
```

For multiple signatories, use a Two-Column Layout table with each signatory in a column.

**Variant: Approval block** (with signature line for wet signatures):
```javascript
new Paragraph({
  spacing: { before: 600, after: 200 },
  children: [new TextRun({
    text: "APPROVED BY",
    font: "Arial",
    size: 16,
    bold: true,
    color: BRAND.muted,
    characterSpacing: 120,
  })],
}),
new Paragraph({
  spacing: { after: 60 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border, space: 1 } },
  children: [new TextRun({
    text: " ",
    size: 22,
  })],
}),
new Paragraph({
  spacing: { before: 80, after: 200 },
  tabStops: [{ type: TabStopType.LEFT, position: 5040 }],
  children: [
    new TextRun({ text: "Name: ________________", font: "Arial", size: 22, color: BRAND.muted }),
    new TextRun({ text: "\tDate: ________________", font: "Arial", size: 22, color: BRAND.muted }),
  ],
}),
```

**Variant: Compact sign-off** (for memos, no rule):
```javascript
new Paragraph({
  spacing: { before: 400, after: 60 },
  children: [
    new TextRun({ text: "Author Name", font: "Arial", size: 22, bold: true, color: BRAND.navy }),
    new TextRun({ text: "  |  ", font: "Arial", size: 22, color: BRAND.border }),
    new TextRun({ text: "Title, Department", font: "Arial", size: 22, color: BRAND.muted }),
  ],
}),
```
