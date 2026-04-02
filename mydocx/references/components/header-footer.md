# Header Footer

Running header with document title and footer with page numbers. Added to the section's `properties` object, not the `children` array. Most formal documents should include these.

## JavaScript

Add `headers` and `footers` alongside `page` in the section properties:

```javascript
{
  properties: {
    page: {
      size: { width: PAGE.width, height: PAGE.height },
      margin: PAGE.margin,
    },
  },
  headers: {
    default: new Header({
      children: [
        new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: BRAND.navy, space: 4 } },
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
          children: [
            new TextRun({
              text: "Document Title",
              font: "Arial",
              size: 18,
              color: BRAND.navy,
            }),
            new TextRun({
              text: "\tOrganization Name",
              font: "Arial",
              size: 16,
              color: BRAND.muted,
            }),
          ],
        }),
      ],
    }),
  },
  footers: {
    default: new Footer({
      children: [
        new Paragraph({
          border: { top: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border, space: 4 } },
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
          children: [
            new TextRun({
              text: "Confidential",
              font: "Arial",
              size: 16,
              color: BRAND.muted,
            }),
            new TextRun({
              children: ["\tPage ", PageNumber.CURRENT],
              font: "Arial",
              size: 16,
              color: BRAND.muted,
            }),
          ],
        }),
      ],
    }),
  },
  children: [
    // Section content here
  ],
}
```

The header uses a navy bottom border for visual weight. The footer uses a light top border and right-aligned page number via tab stop. Both use the design system colors. Never use tables for headers/footers (cells have minimum height); use tab stops for alignment.

**Variant: No header on cover page**

Use `titlePage: true` in section properties and provide a `first` header that's empty:
```javascript
properties: {
  titlePage: true,
  page: { /* ... */ },
},
headers: {
  default: new Header({ children: [/* normal header */] }),
  first: new Header({ children: [] }),
},
footers: {
  default: new Footer({ children: [/* normal footer */] }),
  first: new Footer({ children: [] }),
},
```

**Variant: Centered footer** (no confidential label):
```javascript
footers: {
  default: new Footer({
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({
          children: [PageNumber.CURRENT],
          font: "Arial",
          size: 16,
          color: BRAND.muted,
        })],
      }),
    ],
  }),
},
```
