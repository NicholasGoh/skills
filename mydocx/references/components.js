"use strict";
const fs = require("fs");
const {
  Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, AlignmentType, PageOrientation,
  LevelFormat, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageNumber, PageBreak, HeadingLevel,
  TabStopType, TabStopPosition, TableOfContents,
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
  margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
  contentWidth: 9360, // width - left - right
};

// ═══════════════════════════════════════════
// SHARED HELPERS
// ═══════════════════════════════════════════
const thin = { style: BorderStyle.SINGLE, size: 1, color: BRAND.border };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
const none = { style: BorderStyle.NONE, size: 0 };
const noBorders = { top: none, bottom: none, left: none, right: none };
const pad = { top: 80, bottom: 80, left: 120, right: 120 };

function pageProps(opts = {}) {
  const p = { size: { width: PAGE.width, height: PAGE.height }, margin: opts.margin || PAGE.margin };
  if (opts.landscape) p.orientation = PageOrientation.LANDSCAPE;
  return p;
}

function equalWidths(n) {
  const w = Math.floor(PAGE.contentWidth / n);
  const widths = Array(n).fill(w);
  widths[n - 1] = PAGE.contentWidth - w * (n - 1);
  return widths;
}

// ═══════════════════════════════════════════
// ELEMENT BUILDERS
// ═══════════════════════════════════════════
const headingMap = { 1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3 };

function heading(level, text) {
  return new Paragraph({ heading: headingMap[level], children: [new TextRun({ text })] });
}

function body(text, opts = {}) {
  return new Paragraph({
    spacing: opts.spacing,
    alignment: opts.alignment,
    children: [new TextRun({
      text, font: "Arial", size: opts.size || 22,
      bold: opts.bold, italics: opts.italics, color: opts.color || BRAND.black,
    })],
  });
}

function spacer(before = 200) {
  return new Paragraph({ spacing: { before } });
}

function rule(opts = {}) {
  return new Paragraph({
    spacing: opts.spacing || { before: 600 },
    border: { bottom: { style: BorderStyle.SINGLE, size: opts.size || 2, color: opts.color || BRAND.border, space: 1 } },
  });
}

function pageBreakParagraph() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ═══════════════════════════════════════════
// CELL BUILDERS
// ═══════════════════════════════════════════
function hCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: BRAND.navy, type: ShadingType.CLEAR }, margins: pad,
    children: [new Paragraph({ children: [new TextRun({
      text: text.toUpperCase(), font: "Arial", size: 18, bold: true, color: BRAND.white,
    })] })],
  });
}

function dCell(text, width, opts = {}) {
  const cell = {
    borders, width: { size: width, type: WidthType.DXA }, margins: pad,
    children: [new Paragraph({ children: [new TextRun({ text: String(text), size: 22 })] })],
  };
  if (opts.shaded) cell.shading = { fill: BRAND.lightGray, type: ShadingType.CLEAR };
  return new TableCell(cell);
}

function lCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: BRAND.lightGray, type: ShadingType.CLEAR }, margins: pad,
    children: [new Paragraph({ children: [new TextRun({
      text: text.toUpperCase(), font: "Arial", size: 16, bold: true, color: BRAND.muted, characterSpacing: 60,
    })] })],
  });
}

// ═══════════════════════════════════════════
// COMPONENT: Cover Page
// ═══════════════════════════════════════════
function coverPage({ title, subtitle, date, author, org } = {}) {
  const children = [spacer(4000)];
  if (org) {
    children.push(new Paragraph({
      spacing: { after: 400 },
      children: [new TextRun({
        text: org.toUpperCase(), font: "Arial", size: 20, bold: true,
        color: BRAND.muted, characterSpacing: 120,
      })],
    }));
  }
  children.push(
    new Paragraph({
      spacing: { after: 400 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BRAND.red, space: 1 } },
    }),
    new Paragraph({
      spacing: { after: 200 },
      children: [new TextRun({
        text: title || "Untitled Document", font: "Arial", size: 72, bold: true, color: BRAND.navy,
      })],
    }),
  );
  children.push(subtitle
    ? new Paragraph({
        spacing: { after: 3000 },
        children: [new TextRun({ text: subtitle, font: "Arial", size: 28, color: BRAND.muted })],
      })
    : spacer(3000)
  );
  if (author) children.push(body(`Prepared by ${author}`, { color: BRAND.muted }));
  if (date) children.push(body(date, { color: BRAND.muted }));
  children.push(pageBreakParagraph());
  return { properties: { page: pageProps() }, children };
}

// ═══════════════════════════════════════════
// COMPONENT: Table of Contents
// ═══════════════════════════════════════════
function toc({ depth } = {}) {
  return {
    properties: { page: pageProps() },
    children: [
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun({ text: "Contents", bold: true, color: BRAND.navy })],
      }),
      new TableOfContents("Table of Contents", {
        hyperlink: true, headingStyleRange: `1-${depth || 3}`,
      }),
      pageBreakParagraph(),
    ],
  };
}

// ═══════════════════════════════════════════
// COMPONENT: Executive Summary
// ═══════════════════════════════════════════
function executiveSummary(paragraphs, opts = {}) {
  const variants = {
    info:    { border: BRAND.navy, bg: BRAND.headerBg },
    warning: { border: BRAND.red,  bg: BRAND.red50 },
    neutral: { border: BRAND.muted, bg: BRAND.lightGray },
  };
  const v = variants[opts.variant || "info"];
  const items = Array.isArray(paragraphs) ? paragraphs : [paragraphs];
  const cellChildren = items.map((t, i) =>
    typeof t !== "string" ? t : new Paragraph({
      spacing: i < items.length - 1 ? { after: 120 } : undefined,
      children: [new TextRun({
        text: t, font: "Arial", size: 22,
        color: i === 0 ? BRAND.black : BRAND.muted,
      })],
    })
  );
  return [
    heading(2, opts.title || "Executive Summary"),
    new Table({
      width: { size: PAGE.contentWidth, type: WidthType.DXA },
      columnWidths: [PAGE.contentWidth],
      rows: [new TableRow({
        children: [new TableCell({
          borders: { top: thin, bottom: thin, right: thin,
            left: { style: BorderStyle.SINGLE, size: 6, color: v.border } },
          shading: { fill: v.bg, type: ShadingType.CLEAR },
          margins: { top: 160, bottom: 160, left: 200, right: 200 },
          width: { size: PAGE.contentWidth, type: WidthType.DXA },
          children: cellChildren,
        })],
      })],
    }),
  ];
}

// ═══════════════════════════════════════════
// COMPONENT: Data Table
// ═══════════════════════════════════════════
function dataTable(headers, rows, opts = {}) {
  const n = headers.length;
  const widths = opts.columnWidths || equalWidths(n);
  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((text, i) =>
      opts.lightHeader
        ? new TableCell({
            borders, width: { size: widths[i], type: WidthType.DXA },
            shading: { fill: BRAND.lightGray, type: ShadingType.CLEAR }, margins: pad,
            children: [new Paragraph({
              children: [new TextRun({ text, font: "Arial", size: 18, bold: true, color: BRAND.black })],
            })],
          })
        : hCell(text, widths[i])
    ),
  });
  const dataRows = rows.map((row, ri) =>
    new TableRow({
      children: row.map((text, ci) => dCell(String(text), widths[ci], { shaded: ri % 2 === 1 })),
    })
  );
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA },
    columnWidths: widths,
    rows: [headerRow, ...dataRows],
  });
}

// ═══════════════════════════════════════════
// COMPONENT: Bullet List
// ═══════════════════════════════════════════
function bulletList(items) {
  return items.map((item, i) => {
    const last = i === items.length - 1;
    if (typeof item === "string") {
      return new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: last ? 200 : 80 },
        children: [new TextRun({ text: item, size: 22 })],
      });
    }
    return new Paragraph({
      numbering: { reference: "bullets", level: 0 },
      spacing: { after: last ? 200 : 80 },
      children: [
        new TextRun({ text: `${item.lead}: `, size: 22, bold: true }),
        new TextRun({ text: item.text, size: 22 }),
      ],
    });
  });
}

// ═══════════════════════════════════════════
// COMPONENT: Numbered List
// ═══════════════════════════════════════════
function numberedList(items) {
  return items.map((item, i) => new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    spacing: { after: i === items.length - 1 ? 200 : 80 },
    children: [new TextRun({ text: typeof item === "string" ? item : item.text, size: 22 })],
  }));
}

// ═══════════════════════════════════════════
// COMPONENT: Callout Box
// ═══════════════════════════════════════════
function callout(text, opts = {}) {
  const types = {
    info:    { border: BRAND.navy,  bg: BRAND.headerBg,  color: BRAND.navy,    label: "NOTE" },
    warning: { border: BRAND.red,   bg: BRAND.red50,     color: BRAND.darkRed, label: "WARNING" },
    tip:     { border: BRAND.muted, bg: BRAND.lightGray, color: BRAND.muted,   label: "TIP" },
  };
  const t = types[opts.type || "info"];
  const lbl = opts.label !== undefined ? opts.label : t.label;
  const cellChildren = [];
  if (lbl) {
    cellChildren.push(new Paragraph({
      spacing: { after: 80 },
      children: [new TextRun({
        text: lbl.toUpperCase(), font: "Arial", size: 16,
        bold: true, color: t.color, characterSpacing: 60,
      })],
    }));
  }
  cellChildren.push(new Paragraph({
    children: [new TextRun({ text, font: "Arial", size: 22, color: BRAND.black })],
  }));
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA },
    columnWidths: [PAGE.contentWidth],
    rows: [new TableRow({
      children: [new TableCell({
        borders: { top: thin, bottom: thin, right: thin,
          left: { style: BorderStyle.SINGLE, size: 8, color: t.border } },
        shading: { fill: t.bg, type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 200, right: 200 },
        width: { size: PAGE.contentWidth, type: WidthType.DXA },
        children: cellChildren,
      })],
    })],
  });
}

// ═══════════════════════════════════════════
// COMPONENT: Key Metrics
// ═══════════════════════════════════════════
function keyMetrics(metrics) {
  const widths = equalWidths(metrics.length);
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA },
    columnWidths: widths,
    rows: [new TableRow({
      children: metrics.map((m, i) => new TableCell({
        borders: noBorders,
        width: { size: widths[i], type: WidthType.DXA },
        margins: { top: 120, bottom: 120, left: 120, right: 120 },
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER, spacing: { after: 40 },
            children: [new TextRun({
              text: m.value, font: "Arial", size: 48, bold: true,
              color: BRAND[m.color] || m.color || BRAND.navy,
            })],
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: m.label.toUpperCase(), font: "Arial", size: 16,
              bold: true, color: BRAND.muted, characterSpacing: 60,
            })],
          }),
        ],
      })),
    })],
  });
}

// ═══════════════════════════════════════════
// COMPONENT: Flow Steps
// ═══════════════════════════════════════════
function flowSteps(steps) {
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA },
    columnWidths: [800, 8560],
    rows: steps.map((s, i) => {
      const last = i === steps.length - 1;
      const num = s.number || String(i + 1).padStart(2, "0");
      const bb = last ? none : { style: BorderStyle.SINGLE, size: 1, color: BRAND.border };
      return new TableRow({
        children: [
          new TableCell({
            borders: { ...noBorders, bottom: bb },
            width: { size: 800, type: WidthType.DXA },
            margins: { top: 120, bottom: 120, left: 0, right: 80 },
            verticalAlign: VerticalAlign.TOP,
            children: [new Paragraph({
              children: [new TextRun({
                text: num, font: "Arial", size: 28, bold: true, color: BRAND.red,
              })],
            })],
          }),
          new TableCell({
            borders: { ...noBorders, bottom: bb },
            width: { size: 8560, type: WidthType.DXA },
            margins: { top: 120, bottom: 120, left: 80, right: 0 },
            verticalAlign: VerticalAlign.TOP,
            children: [
              new Paragraph({
                spacing: { after: 60 },
                children: [new TextRun({
                  text: s.title, font: "Arial", size: 24, bold: true, color: BRAND.black,
                })],
              }),
              new Paragraph({
                children: [new TextRun({
                  text: s.description, font: "Arial", size: 22, color: BRAND.muted,
                })],
              }),
            ],
          }),
        ],
      });
    }),
  });
}

// ═══════════════════════════════════════════
// COMPONENT: Two-Column Layout
// ═══════════════════════════════════════════
function twoColumn(left, right, opts = {}) {
  const widths = opts.widths || [4560, 4800];
  function toChildren(content) {
    if (typeof content === "string") return [body(content)];
    if (Array.isArray(content)) return content.map(c => typeof c === "string" ? body(c) : c);
    return [content];
  }
  const rows = [];
  if (opts.leftHeader || opts.rightHeader) {
    rows.push(new TableRow({
      children: [
        new TableCell({
          borders: { ...noBorders, bottom: { style: BorderStyle.SINGLE, size: 2, color: BRAND.navy } },
          width: { size: widths[0], type: WidthType.DXA },
          margins: { top: 80, bottom: 120, left: 0, right: 200 },
          children: [new Paragraph({
            children: [new TextRun({
              text: (opts.leftHeader || "").toUpperCase(), font: "Arial", size: 18,
              bold: true, color: BRAND.navy, characterSpacing: 60,
            })],
          })],
        }),
        new TableCell({
          borders: { ...noBorders, bottom: { style: BorderStyle.SINGLE, size: 2, color: BRAND.navy } },
          width: { size: widths[1], type: WidthType.DXA },
          margins: { top: 80, bottom: 120, left: 200, right: 0 },
          children: [new Paragraph({
            children: [new TextRun({
              text: (opts.rightHeader || "").toUpperCase(), font: "Arial", size: 18,
              bold: true, color: BRAND.navy, characterSpacing: 60,
            })],
          })],
        }),
      ],
    }));
  }
  rows.push(new TableRow({
    children: [
      new TableCell({
        borders: noBorders, width: { size: widths[0], type: WidthType.DXA },
        margins: { top: 160, bottom: 120, left: 0, right: 200 },
        children: toChildren(left),
      }),
      new TableCell({
        borders: noBorders, width: { size: widths[1], type: WidthType.DXA },
        margins: { top: 160, bottom: 120, left: 200, right: 0 },
        children: toChildren(right),
      }),
    ],
  }));
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA },
    columnWidths: widths, rows,
  });
}

// ═══════════════════════════════════════════
// COMPONENT: Image Block
// ═══════════════════════════════════════════
function imageBlock(imagePath, opts = {}) {
  const imgType = opts.type || imagePath.split(".").pop().toLowerCase();
  const elements = [
    new Paragraph({
      alignment: opts.alignment || AlignmentType.CENTER,
      spacing: { before: 200, after: 80 },
      children: [new ImageRun({
        type: imgType,
        data: fs.readFileSync(imagePath),
        transformation: { width: opts.width || 468, height: opts.height || 300 },
        altText: {
          title: opts.title || "Image",
          description: opts.alt || opts.title || "Image",
          name: opts.name || "image",
        },
      })],
    }),
  ];
  if (opts.caption) {
    elements.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [new TextRun({
        text: opts.caption, font: "Arial", size: 18, italics: true, color: BRAND.muted,
      })],
    }));
  }
  return elements;
}

// ═══════════════════════════════════════════
// COMPONENT: Checklist
// ═══════════════════════════════════════════
function checklist(items) {
  const styles = {
    done: { fill: "E8F5E9", color: "2E7D32", label: "DONE" },
    todo: { fill: BRAND.headerBg, color: BRAND.navy, label: "TODO" },
    risk: { fill: BRAND.red50, color: BRAND.darkRed, label: "RISK" },
    na:   { fill: BRAND.lightGray, color: BRAND.muted, label: "N/A" },
  };
  return new Table({
    width: { size: PAGE.contentWidth, type: WidthType.DXA },
    columnWidths: [1200, 8160],
    rows: [
      new TableRow({
        tableHeader: true,
        children: [lCell("Status", 1200), lCell("Item", 8160)],
      }),
      ...items.map(item => {
        const s = styles[item.status] || styles.todo;
        return new TableRow({
          children: [
            new TableCell({
              borders, width: { size: 1200, type: WidthType.DXA },
              shading: { fill: s.fill, type: ShadingType.CLEAR }, margins: pad,
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({
                  text: item.label || s.label, font: "Arial", size: 16, bold: true, color: s.color,
                })],
              })],
            }),
            new TableCell({
              borders, width: { size: 8160, type: WidthType.DXA }, margins: pad,
              children: [new Paragraph({
                children: [new TextRun({ text: item.text, size: 22 })],
              })],
            }),
          ],
        });
      }),
    ],
  });
}

// ═══════════════════════════════════════════
// COMPONENT: Signature Block
// ═══════════════════════════════════════════
function signatureBlock({ name, title: sigTitle, date, variant } = {}) {
  if (variant === "compact") {
    return [new Paragraph({
      spacing: { before: 400, after: 60 },
      children: [
        new TextRun({ text: name, font: "Arial", size: 22, bold: true, color: BRAND.navy }),
        new TextRun({ text: "  |  ", font: "Arial", size: 22, color: BRAND.border }),
        new TextRun({ text: sigTitle || "", font: "Arial", size: 22, color: BRAND.muted }),
      ],
    })];
  }
  if (variant === "approval") {
    return [
      new Paragraph({
        spacing: { before: 600, after: 200 },
        children: [new TextRun({
          text: "APPROVED BY", font: "Arial", size: 16, bold: true,
          color: BRAND.muted, characterSpacing: 120,
        })],
      }),
      new Paragraph({
        spacing: { after: 60 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border, space: 1 } },
        children: [new TextRun({ text: " ", size: 22 })],
      }),
      new Paragraph({
        spacing: { before: 80, after: 200 },
        tabStops: [{ type: TabStopType.LEFT, position: 5040 }],
        children: [
          new TextRun({ text: "Name: ________________", font: "Arial", size: 22, color: BRAND.muted }),
          new TextRun({ text: "\tDate: ________________", font: "Arial", size: 22, color: BRAND.muted }),
        ],
      }),
    ];
  }
  const els = [
    rule(),
    spacer(400),
    new Paragraph({
      spacing: { after: 60 },
      children: [new TextRun({
        text: name || "Author Name", font: "Arial", size: 24, bold: true, color: BRAND.navy,
      })],
    }),
  ];
  if (sigTitle) els.push(new Paragraph({
    spacing: { after: 60 },
    children: [new TextRun({ text: sigTitle, font: "Arial", size: 22, color: BRAND.muted })],
  }));
  if (date) els.push(new Paragraph({
    children: [new TextRun({ text: date, font: "Arial", size: 22, color: BRAND.muted })],
  }));
  return els;
}

// ═══════════════════════════════════════════
// COMPONENT: Header & Footer
// ═══════════════════════════════════════════
function headerFooter({ title: docTitle, org, confidential, noFirstPage } = {}) {
  const result = {
    headers: {
      default: new Header({
        children: [new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: BRAND.navy, space: 4 } },
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
          children: [
            new TextRun({ text: docTitle || "Document", font: "Arial", size: 18, color: BRAND.navy }),
            ...(org ? [new TextRun({ text: `\t${org}`, font: "Arial", size: 16, color: BRAND.muted })] : []),
          ],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          border: { top: { style: BorderStyle.SINGLE, size: 1, color: BRAND.border, space: 4 } },
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
          children: [
            ...(confidential !== false ? [new TextRun({
              text: typeof confidential === "string" ? confidential : "Confidential",
              font: "Arial", size: 16, color: BRAND.muted,
            })] : []),
            new TextRun({
              children: [confidential !== false ? "\tPage " : "Page ", PageNumber.CURRENT],
              font: "Arial", size: 16, color: BRAND.muted,
            }),
          ],
        })],
      }),
    },
  };
  if (noFirstPage) {
    result.titlePage = true;
    result.headers.first = new Header({ children: [] });
    result.footers.first = new Footer({ children: [] });
  }
  return result;
}

// ═══════════════════════════════════════════
// SECTION HELPER
// ═══════════════════════════════════════════
function section(children, opts = {}) {
  const sec = {
    properties: { page: pageProps(opts) },
    children: children.flat(),
  };
  if (opts.headerFooter) {
    const hf = opts.headerFooter.headers ? opts.headerFooter : headerFooter(opts.headerFooter);
    sec.headers = hf.headers;
    sec.footers = hf.footers;
    if (hf.titlePage) sec.properties.titlePage = true;
  }
  return sec;
}

// ═══════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════
module.exports = {
  BRAND, PAGE,
  thin, borders, none, noBorders, pad, pageProps, equalWidths,
  heading, body, spacer, rule, pageBreak: pageBreakParagraph,
  hCell, dCell, lCell,
  coverPage, toc, executiveSummary, dataTable,
  bulletList, numberedList, callout, keyMetrics,
  flowSteps, twoColumn, imageBlock, checklist,
  signatureBlock, headerFooter, section,
};
