---
name: mydocx
description: >
  Build polished Word documents (.docx) with a minimalist corporate design system.
  Use this skill whenever the user asks to create a Word document, report, memo,
  proposal, letter, or any professional document delivered as .docx. Also trigger
  for editing existing .docx files, working with tracked changes or comments,
  extracting content, or converting documents. If the user mentions "Word doc",
  ".docx", or wants a formatted deliverable as a Word file, this is the skill to use.
  Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated
  to document generation.
---

# Word Documents

Build professional .docx files that feel premium: clean typography, restrained color, thoughtful spacing, and consistent structure. Every document uses the docx-js library and a unified design system for a cohesive corporate look. Single script, no build step, generates a valid .docx that opens in Word, Google Docs, or any compatible reader.

## Design Philosophy

The aesthetic is **minimalist corporate**: not clip-art-heavy, not plain. Think of a well-designed annual report, not a default Word template. The design earns trust through restraint.

Key principles:
- **Navy + red accent palette.** Navy (#1A1F5D) for headings and emphasis. Red (#E10B0A) sparingly for callout borders, accent rules, and status indicators. Everything else is grayscale.
- **Clean typography.** Arial throughout for universal cross-platform support. Bold headings with generous size hierarchy (28pt, 18pt, 14pt). Body at 11pt with comfortable 1.15x line spacing.
- **Generous whitespace.** Consistent paragraph spacing (before/after), 1-inch margins, breathing room between sections. Let the content stand on its own.
- **Structured hierarchy.** Clear heading levels with outline support for TOC generation. Purposeful use of borders and shading for grouping, not decoration.
- **DXA precision.** All dimensions in DXA units (1440 = 1 inch) for pixel-perfect consistency across readers. Never use percentages for table widths.
- **No dashes in prose.** Never use em dashes, en dashes, or double hyphens in document text. These are hallmarks of generic AI writing. Restructure sentences instead: use periods, commas, colons, semicolons, or parentheses. Hyphens in compound modifiers (e.g. "two-column") are fine.

## How to Build a Document

### Step 1: Read the template

Read `references/template.js` in this skill directory. It contains the document shell (styles, page setup, numbering config) and the Packer output. Design tokens and component functions live in `references/components.js` (copied alongside the template, not read into context). The template has `/* __SECTIONS__ */` and `DOCUMENT_FILENAME` markers for content insertion.

### Step 2: Plan the document structure

Decide on sections and what each covers. Typical structures:
- **Report** (8-15 pages): Cover, TOC, executive summary, 3-5 content sections, appendix
- **Memo** (1-3 pages): Header block, body sections, action items
- **Proposal** (5-10 pages): Cover, summary, scope, timeline, pricing, terms
- Keep each section focused on ONE topic. If you're cramming, split it.

### Step 3: Pick components

Read `references/components/index.md` for the component API. Each function handles borders, shading, spacing, and colors automatically. You pass content; the design system is applied.

Common document patterns:
- **Formal report**: coverPage + toc + executiveSummary + dataTable + keyMetrics
- **Process document**: headerFooter + flowSteps + checklist + callout
- **Proposal**: coverPage + twoColumn + dataTable + signatureBlock
- **Memo**: headerFooter + bulletList + callout + signatureBlock

### Step 4: Assemble and output

Do NOT regenerate the template or components from memory. Copy the files directly:

1. **Copy both files**:
   ```bash
   cp <skill-dir>/references/template.js <output-dir>/create_doc.js
   cp <skill-dir>/references/components.js <output-dir>/components.js
   ```
2. **Filename**: replace `DOCUMENT_FILENAME` with the actual output filename (e.g., `report.docx`)
3. **Sections**: replace `/* __SECTIONS__ */` with section content using `C.` component calls
4. **Run**: `node create_doc.js`
5. **Validate**: `python <skill-dir>/scripts/office/validate.py <output>.docx`

Use `C.section(children, opts)` to build content sections. It auto-flattens children, so array-returning functions (executiveSummary, bulletList, numberedList, imageBlock, signatureBlock) work without `...spread`. For raw docx-js alongside component calls, all docx classes are available in the template scope.

After generating, open or convert to verify layout. If validation flags issues, unpack, fix, and repack (see Editing below).

## Adapting the Color Palette

Update the `BRAND` object in `components.js` to change the design system globally:

- `navy`: Primary heading color
- `red`: Action/emphasis accent (callout borders, status indicators, step numbers)
- `darkRed`: Darker variant for strong emphasis or warning labels
- `red50`: Light tint for warning callout backgrounds
- `muted`: Secondary text color (captions, labels, descriptions)
- `lightGray`: Shading for table headers, alternating rows, neutral callouts
- `headerBg`: Light tint for executive summary backgrounds and info callouts

When changing the palette, keep the contrast ratio between heading color and white background above 4.5:1 for readability.

## Typography Reference

| Role | Font | Size (half-pt) | Display |
|------|------|----------------|---------|
| H1 / Title | Arial Bold | 56 | 28pt |
| H2 / Section | Arial Bold | 36 | 18pt |
| H3 / Subsection | Arial Bold | 28 | 14pt |
| Body | Arial | 22 | 11pt |
| Small / Caption | Arial | 18 | 9pt |
| Label | Arial Bold | 16 | 8pt, uppercase |

All sizes in docx-js are **half-points** (multiply pt by 2). Line spacing 276 = 1.15x.

## Key Details

- docx-js defaults to A4; always set US Letter (12240 x 15840 DXA) explicitly.
- Tables need dual widths: `columnWidths` on the table AND `width` on each cell.
- Use `ShadingType.CLEAR` for table shading (SOLID produces black backgrounds).
- `PageBreak` must be inside a `Paragraph` (standalone creates invalid XML).
- Never use `\n` in text; use separate `Paragraph` elements.
- Never use unicode bullets inline; use `LevelFormat.BULLET` with numbering config.
- Include `outlineLevel` on heading paragraph styles for TOC generation.
- TOC requires `HeadingLevel` only (no custom styles on heading paragraphs).
- Never use tables as horizontal rules; cells have minimum height. Use `border.bottom` on a Paragraph instead.
- Landscape: pass portrait dimensions and set `orientation: PageOrientation.LANDSCAPE` (docx-js swaps internally).
- After creation, validate: `python scripts/office/validate.py <file>.docx`

---

## Editing Existing Documents

Three-step workflow: unpack the ZIP, edit the XML, repack. Read `references/xml-editing.md` for detailed XML patterns (tracked changes, comments, images, schema compliance).

### Step 1: Unpack
```bash
python scripts/office/unpack.py document.docx unpacked/
```
Extracts XML, pretty-prints, merges adjacent runs, converts smart quotes to XML entities. Use `--merge-runs false` to skip run merging.

### Step 2: Edit XML

Edit files in `unpacked/word/` using the Edit tool directly (not Python scripts). Use "Claude" as the tracked changes author unless specified otherwise.

Smart quotes in new content:
| Entity | Character |
|--------|-----------|
| `&#x2018;` | ' (left single) |
| `&#x2019;` | ' (right single / apostrophe) |
| `&#x201C;` | " (left double) |
| `&#x201D;` | " (right double) |

For comments, use `comment.py`:
```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"
```
Then add markers to document.xml (see `references/xml-editing.md` for placement).

### Step 3: Pack
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
Validates with auto-repair, condenses XML, creates the .docx. Use `--validate false` to skip validation.

Auto-repair fixes: `durableId` overflow, missing `xml:space="preserve"` on whitespace text.
Auto-repair does not fix: malformed XML, invalid nesting, missing relationships, schema violations.

## Reading Content

```bash
# Text extraction with tracked changes
pandoc --track-changes=all document.docx -o output.md

# Raw XML access
python scripts/office/unpack.py document.docx unpacked/
```

## Converting

```bash
# Legacy .doc to .docx
python scripts/office/soffice.py --headless --convert-to docx document.doc

# .docx to PDF, then to images
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

## Accepting Tracked Changes

```bash
python scripts/accept_changes.py input.docx output.docx
```
Requires LibreOffice. Produces a clean document with all tracked changes accepted.

## Dependencies

- **docx**: `npm install -g docx` (document creation)
- **pandoc**: Text extraction
- **LibreOffice**: PDF conversion, tracked change acceptance (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- **Poppler**: `pdftoppm` for images
