# Cover Page

Full title page for formal documents. Navy title with generous whitespace, organization name at top, red accent rule, and metadata (author, date) at bottom. Fills one page with a trailing page break.

## JavaScript

```javascript
{
  properties: {
    page: {
      size: { width: PAGE.width, height: PAGE.height },
      margin: PAGE.margin,
    },
  },
  children: [
    // Top spacer
    new Paragraph({ spacing: { before: 4000 } }),

    // Organization name
    new Paragraph({
      spacing: { after: 400 },
      children: [new TextRun({
        text: "ORGANIZATION NAME",
        font: "Arial",
        size: 20,
        bold: true,
        color: BRAND.muted,
        characterSpacing: 120,
      })],
    }),

    // Accent rule
    new Paragraph({
      spacing: { after: 400 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BRAND.red, space: 1 } },
    }),

    // Document title
    new Paragraph({
      spacing: { after: 200 },
      children: [new TextRun({
        text: "Document Title",
        font: "Arial",
        size: 72,
        bold: true,
        color: BRAND.navy,
      })],
    }),

    // Subtitle
    new Paragraph({
      spacing: { after: 3000 },
      children: [new TextRun({
        text: "Subtitle or brief description of this document",
        font: "Arial",
        size: 28,
        color: BRAND.muted,
      })],
    }),

    // Author
    new Paragraph({
      children: [new TextRun({
        text: "Prepared by Author Name",
        font: "Arial",
        size: 22,
        color: BRAND.muted,
      })],
    }),

    // Date
    new Paragraph({
      children: [new TextRun({
        text: "January 2026",
        font: "Arial",
        size: 22,
        color: BRAND.muted,
      })],
    }),

    // Page break to content
    new Paragraph({ children: [new PageBreak()] }),
  ],
}
```

Adjust the top spacer `before` value (4000) to shift content vertically. For landscape documents, increase spacers proportionally. The accent rule uses the red from the design system for a subtle brand touch without being heavy.

**Variant: Minimal cover** (no organization line, just title + date):

Remove the organization name and accent rule paragraphs. Increase the top spacer to ~6000 for visual centering.
