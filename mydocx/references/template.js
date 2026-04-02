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

// ═══════════════════════════════════════════
// DESIGN TOKENS
// ═══════════════════════════════════════════
const BRAND = {
  navy:      "1A1F5D",
  red:       "E10B0A",
  darkRed:   "C20202",
  red50:     "FCE7E7",
  black:     "262626",
  muted:     "686879",
  lightGray: "F6F6F6",
  white:     "FFFFFF",
  border:    "ECECF0",
  headerBg:  "EFF2FF",
};

const PAGE = {
  width: 12240,       // US Letter 8.5"
  height: 15840,      // US Letter 11"
  margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }, // 1" all sides
  contentWidth: 9360, // width - left margin - right margin
};

// ═══════════════════════════════════════════
// SHARED HELPERS
// ═══════════════════════════════════════════
const thin = { style: BorderStyle.SINGLE, size: 1, color: BRAND.border };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
const none = { style: BorderStyle.NONE, size: 0 };
const noBorders = { top: none, bottom: none, left: none, right: none };
const pad = { top: 80, bottom: 80, left: 120, right: 120 };

// ═══════════════════════════════════════════
// DOCUMENT
// ═══════════════════════════════════════════
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22, color: BRAND.black },
        paragraph: { spacing: { after: 200, line: 276 } },
      },
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { font: "Arial", size: 56, bold: true, color: BRAND.navy },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 },
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { font: "Arial", size: 36, bold: true, color: BRAND.navy },
        paragraph: { spacing: { before: 280, after: 200 }, outlineLevel: 1 },
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { font: "Arial", size: 28, bold: true, color: BRAND.black },
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

// ═══════════════════════════════════════════
// OUTPUT
// ═══════════════════════════════════════════
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("DOCUMENT_FILENAME", buffer);
  console.log("Created DOCUMENT_FILENAME");
});
