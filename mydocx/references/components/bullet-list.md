# Bullet List

Properly formatted bullet or numbered lists using the template's numbering config. Never use unicode bullet characters inline; they render inconsistently across readers.

## JavaScript

**Bullet list:**
```javascript
new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [new TextRun({ text: "First item in the list", size: 22 })],
}),
new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [new TextRun({ text: "Second item with more detail", size: 22 })],
}),
new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 200 },
  children: [new TextRun({ text: "Final item (restore normal after-spacing on last)", size: 22 })],
}),
```

**Numbered list:**
```javascript
new Paragraph({
  numbering: { reference: "numbers", level: 0 },
  spacing: { after: 80 },
  children: [new TextRun({ text: "First step in the process", size: 22 })],
}),
new Paragraph({
  numbering: { reference: "numbers", level: 0 },
  spacing: { after: 80 },
  children: [new TextRun({ text: "Second step", size: 22 })],
}),
new Paragraph({
  numbering: { reference: "numbers", level: 0 },
  spacing: { after: 200 },
  children: [new TextRun({ text: "Third step", size: 22 })],
}),
```

The `"bullets"` and `"numbers"` references are defined in the template's numbering config. Each reference creates an independent numbering sequence: same reference continues (1, 2, 3 then 4, 5, 6), different reference restarts (1, 2, 3 then 1, 2, 3).

**Restarting numbering:** Add a second reference to the template's `numbering.config`:
```javascript
{ reference: "numbers2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
  alignment: AlignmentType.LEFT,
  style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
```

**Bold lead-in text:**
```javascript
new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [
    new TextRun({ text: "Key term: ", size: 22, bold: true }),
    new TextRun({ text: "Explanation of the term follows here.", size: 22 }),
  ],
}),
```

**Nested lists:** Add deeper levels to the numbering config:
```javascript
{ level: 1, format: LevelFormat.BULLET, text: "\u25E6", // open bullet
  alignment: AlignmentType.LEFT,
  style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
```
Then use `level: 1` in the paragraph's numbering reference.
