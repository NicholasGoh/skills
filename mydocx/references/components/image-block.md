# Image Block

Image with caption paragraph. Supports PNG, JPG, GIF, BMP, and SVG. Always include alt text for accessibility.

## JavaScript

```javascript
// Image (centered)
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 200, after: 80 },
  children: [new ImageRun({
    type: "png",  // Required: png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("path/to/image.png"),
    transformation: { width: 500, height: 300 },  // Points
    altText: {
      title: "Image Title",
      description: "Detailed description for screen readers",
      name: "image-name",
    },
  })],
}),

// Caption
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [new TextRun({
    text: "Figure 1: Description of what the image shows",
    font: "Arial",
    size: 18,
    italics: true,
    color: BRAND.muted,
  })],
}),
```

The `type` parameter is required; docx-js will produce invalid XML without it. The `transformation` dimensions are in **points** (not DXA). For full-width images on US Letter with 1" margins, use `width: 468` (6.5 inches x 72 points/inch).

All three `altText` fields (`title`, `description`, `name`) are required by docx-js.

**Variant: Left-aligned with wrap text:**
```javascript
new Paragraph({
  alignment: AlignmentType.LEFT,
  spacing: { before: 200, after: 120 },
  children: [new ImageRun({
    type: "jpg",
    data: fs.readFileSync("photo.jpg"),
    transformation: { width: 300, height: 200 },
    altText: { title: "Photo", description: "Description", name: "photo" },
  })],
}),
```

**Sizing guide:**
| Width | Approximate display |
|-------|-------------------|
| 468 pt | Full content width (6.5") |
| 324 pt | Two-thirds width (4.5") |
| 234 pt | Half width (3.25") |
| 144 pt | Thumbnail (2") |
