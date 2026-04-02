# Table of Contents

Auto-generated table of contents from heading levels. Requires heading paragraphs to use `HeadingLevel` (not custom styles). The TOC displays "Update this field" in Word until the user presses F9 or right-clicks to update.

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
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      children: [new TextRun({ text: "Contents", bold: true, color: BRAND.navy })],
    }),
    new TableOfContents("Table of Contents", {
      hyperlink: true,
      headingStyleRange: "1-3",
    }),
    new Paragraph({ children: [new PageBreak()] }),
  ],
}
```

The `headingStyleRange` controls depth: `"1-2"` for H1 and H2 only, `"1-3"` for three levels. All heading paragraphs in the document must use the built-in `HeadingLevel.HEADING_1`, `HEADING_2`, etc. for the TOC to index them. Custom paragraph styles won't be picked up.

For documents without a cover page, this can be the first section. For documents with a cover page, this is typically the second section.
