#!/usr/bin/env node
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, AlignmentType, PageOrientation,
  LevelFormat, ExternalHyperlink, InternalHyperlink, Bookmark,
  FootnoteReferenceRun, PositionalTab, PositionalTabAlignment,
  PositionalTabRelativeTo, PositionalTabLeader, TabStopType,
  TabStopPosition, Column, SectionType, TableOfContents, HeadingLevel,
  BorderStyle, WidthType, ShadingType, VerticalAlign, PageNumber, PageBreak,
} = require("docx");
const C = require("./components");

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22, color: C.BRAND.black },
        paragraph: { spacing: { after: 200, line: 276 } },
      },
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { font: "Arial", size: 56, bold: true, color: C.BRAND.navy },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 },
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { font: "Arial", size: 36, bold: true, color: C.BRAND.navy },
        paragraph: { spacing: { before: 280, after: 200 }, outlineLevel: 1 },
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { font: "Arial", size: 28, bold: true, color: C.BRAND.black },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 2 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
    ],
  },
  sections: [
    /* __SECTIONS__ */
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("DOCUMENT_FILENAME", buffer);
  console.log("Created DOCUMENT_FILENAME");
});
