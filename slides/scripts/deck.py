# /// script
# requires-python = ">=3.11"
# dependencies = ["beautifulsoup4"]
# ///
"""Inspect and edit assembled slide presentations.

Usage:
    deck.py overview <file.html>
    deck.py extract  <file.html> <slide-num>
    deck.py replace  <file.html> <slide-num> <new-slide.html> [--in-place | -o out.html]
    deck.py delete   <file.html> <slide-num>                  [--in-place | -o out.html]
    deck.py insert   <file.html> <position>  <new-slide.html> [--in-place | -o out.html]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Tag

# Maps a CSS class found inside a slide to the component file basename
# used by assemble.sh.  Order doesn't matter; we check all of them.
COMPONENT_MARKERS: dict[str, str] = {
    "title-grid": "title-slide",
    "content-grid": "two-column-sidebar",
    "rule-item": "numbered-list",
    "grade-card": "grade-rating-cards",
    "flow-step": "flow-steps",
    "principle-list": "principle-checklist",
    "risk-card": "risk-feature-cards",
    "bench-table": "data-table",
    "icon-card": "icon-cards",
    "sidebar": "sidebar-panel",
    "stat-row": "stat-callouts",
    "depri-sidebar": "deprioritised-content",
    "chat-container": "chat-evidence",
}

# Default :root palette from template.html.  Only brand-relevant
# variables are listed; layout vars like --slide-padding are skipped.
DEFAULT_PALETTE: dict[str, str] = {
    "--brand-navy": "#1A1F5D",
    "--brand-red": "#E10B0A",
    "--brand-dark-red": "#C20202",
    "--brand-red-50": "#FCE7E7",
    "--brand-black": "#262626",
    "--brand-muted": "#686879",
    "--brand-light-gray": "#F6F6F6",
    "--brand-white": "#FFFFFF",
    "--bg-header": "#EFF2FF",
}


# ---------------------------------------------------------------------------
# BS4 helpers (used by overview for semantic parsing)
# ---------------------------------------------------------------------------

def parse_deck(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def find_slides(soup: BeautifulSoup) -> list[Tag]:
    return soup.find_all("section", class_="slide")


def detect_components(slide: Tag) -> list[str]:
    found: list[str] = []
    for css_class, name in COMPONENT_MARKERS.items():
        if slide.find(class_=css_class):
            found.append(name)
    return found


def get_heading(slide: Tag) -> str | None:
    for tag in ("h1", "h2"):
        el = slide.find(tag)
        if el:
            return el.get_text(" ", strip=True)
    return None


def get_section_label(slide: Tag) -> str | None:
    el = slide.find(class_="section-label")
    return el.get_text(strip=True) if el else None


def get_slide_bg(slide: Tag) -> str:
    classes = slide.get("class", [])
    return "gray" if "alt" in classes else "white"


def extract_grades_from_slide(slide: Tag) -> list[str]:
    """Find grade pills (.pill.grade-*) on a slide."""
    grades: list[str] = []
    for pill in slide.find_all(class_="pill"):
        for cls in pill.get("class", []):
            if cls.startswith("grade-"):
                letter = cls.removeprefix("grade-").upper()
                if letter != "NA":
                    grades.append(letter)
    return grades


def build_principle_grade_map(soup: BeautifulSoup) -> dict[str, str]:
    """Parse title slide sidebar for principle name -> grade letter mapping.

    Looks for .p-row elements containing .p-label + .pill.grade-*.
    """
    grade_map: dict[str, str] = {}
    for row in soup.select(".p-row"):
        label_el = row.find(class_="p-label")
        if not label_el:
            continue
        label_text = label_el.get_text(strip=True)
        if label_text.lower() == "aggregate":
            continue
        for pill in row.find_all(class_="pill"):
            for cls in pill.get("class", []):
                if cls.startswith("grade-"):
                    letter = cls.removeprefix("grade-").upper()
                    if letter != "NA":
                        grade_map[label_text] = letter
    return grade_map


def format_grade(grades: list[str]) -> str:
    if not grades:
        return ""
    if len(grades) == 1:
        return grades[0]
    # Two grades: show as arrow (old -> new)
    return f"{grades[0]}>{grades[1]}"


def detect_palette_overrides(soup: BeautifulSoup) -> dict[str, tuple[str, str]]:
    """Return {var_name: (default, actual)} for any overridden palette vars."""
    style = soup.find("style")
    if not style or not style.string:
        return {}
    overrides: dict[str, tuple[str, str]] = {}
    for match in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+);", style.string):
        var, val = match.group(1), match.group(2).strip()
        if var in DEFAULT_PALETTE and val.upper() != DEFAULT_PALETTE[var].upper():
            overrides[var] = (DEFAULT_PALETTE[var], val)
    return overrides


# ---------------------------------------------------------------------------
# String-based slide boundary detection (preserves original HTML exactly)
# ---------------------------------------------------------------------------

_SLIDE_OPEN = re.compile(r'<section\s[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>')


def find_slide_spans(html: str) -> list[tuple[int, int]]:
    """Return (start, end) byte offsets for each <section class="slide ...">...</section>.

    Uses a simple depth counter since slides don't nest.
    """
    spans: list[tuple[int, int]] = []
    for m in _SLIDE_OPEN.finditer(html):
        start = m.start()
        # Walk forward counting <section> / </section> to find the matching close
        depth = 1
        pos = m.end()
        while depth > 0 and pos < len(html):
            next_open = html.find("<section", pos)
            next_close = html.find("</section>", pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 8
            else:
                depth -= 1
                if depth == 0:
                    end = next_close + len("</section>")
                    spans.append((start, end))
                pos = next_close + 10
    return spans


def renumber_html(html: str) -> str:
    """Fix slide ids and slide-num spans after insert/delete."""
    spans = find_slide_spans(html)
    total = len(spans)
    padded_total = f"{total:02d}"

    # Work backwards so earlier offsets stay valid
    for i, (start, end) in reversed(list(enumerate(spans, 1))):
        section = html[start:end]
        # Update id="slide-N"
        section = re.sub(r'id="slide-\d+"', f'id="slide-{i}"', section, count=1)
        # Update slide-num text
        section = re.sub(
            r'(<span\s+class="slide-num">)\s*\d+\s*/\s*\d+\s*(</span>)',
            rf"\g<1>{i:02d} / {padded_total}\2",
            section,
            count=1,
        )
        html = html[:start] + section + html[end:]
    return html


def write_str_output(html: str, args: argparse.Namespace) -> None:
    if getattr(args, "in_place", False):
        Path(args.file).write_text(html, encoding="utf-8")
    elif getattr(args, "output", None):
        Path(args.output).write_text(html, encoding="utf-8")
    else:
        sys.stdout.write(html)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_overview(args: argparse.Namespace) -> None:
    path = Path(args.file)
    soup = parse_deck(path)
    slides = find_slides(soup)
    title_el = soup.find("title")
    title = title_el.get_text(strip=True) if title_el else "(untitled)"

    overrides = detect_palette_overrides(soup)
    palette_str = "default palette"
    if overrides:
        parts = [f"{k}: {v[0]}->{v[1]}" for k, v in overrides.items()]
        palette_str = ", ".join(parts)

    principle_grades = build_principle_grade_map(soup)

    print(f'{path.name} \u2014 "{title}" \u2014 {len(slides)} slides \u2014 {palette_str}')
    print()

    rows: list[tuple[str, str, str, str, str, str]] = []
    for i, slide in enumerate(slides, 1):
        num = str(i)
        bg = get_slide_bg(slide)
        heading = get_heading(slide) or ""
        label = get_section_label(slide) or ""
        comps = ", ".join(detect_components(slide))

        # Grade: only show for evidence slides (chat-based findings).
        is_evidence = bool(
            slide.find(class_="chat-container")
            or slide.find(class_="evidence-grid")
        )
        grade_str = ""
        if is_evidence:
            grades = extract_grades_from_slide(slide)
            grade_str = format_grade(grades)
            if not grade_str and label and label in principle_grades:
                grade_str = principle_grades[label]

        rows.append((num, bg, heading, label, comps, grade_str))

    h_num, h_bg, h_head, h_label, h_comp, h_grade = "#", "BG", "Heading", "Label", "Components", "Grade"
    w_num = max(len(h_num), max((len(r[0]) for r in rows), default=1))
    w_bg = max(len(h_bg), 5)
    w_head = max(len(h_head), max((len(r[2]) for r in rows), default=7))
    w_label = max(len(h_label), max((len(r[3]) for r in rows), default=5))
    w_comp = max(len(h_comp), max((len(r[4]) for r in rows), default=10))

    def fmt(n: str, bg: str, head: str, lab: str, comp: str, grade: str) -> str:
        return f" {n:>{w_num}}  {bg:<{w_bg}}  {head:<{w_head}}  {lab:<{w_label}}  {comp:<{w_comp}}  {grade}"

    print(fmt(h_num, h_bg, h_head, h_label, h_comp, h_grade))
    for row in rows:
        print(fmt(*row))


def cmd_extract(args: argparse.Namespace) -> None:
    html = Path(args.file).read_text(encoding="utf-8")
    spans = find_slide_spans(html)
    idx = args.slide_num - 1
    if idx < 0 or idx >= len(spans):
        print(f"Error: slide {args.slide_num} out of range (1-{len(spans)})", file=sys.stderr)
        sys.exit(1)
    start, end = spans[idx]
    sys.stdout.write(html[start:end])
    sys.stdout.write("\n")


def cmd_replace(args: argparse.Namespace) -> None:
    html = Path(args.file).read_text(encoding="utf-8")
    spans = find_slide_spans(html)
    idx = args.slide_num - 1
    if idx < 0 or idx >= len(spans):
        print(f"Error: slide {args.slide_num} out of range (1-{len(spans)})", file=sys.stderr)
        sys.exit(1)

    new_slide = Path(args.new_slide).read_text(encoding="utf-8").strip()
    start, end = spans[idx]
    html = html[:start] + new_slide + html[end:]
    html = renumber_html(html)
    write_str_output(html, args)


def cmd_delete(args: argparse.Namespace) -> None:
    html = Path(args.file).read_text(encoding="utf-8")
    spans = find_slide_spans(html)
    idx = args.slide_num - 1
    if idx < 0 or idx >= len(spans):
        print(f"Error: slide {args.slide_num} out of range (1-{len(spans)})", file=sys.stderr)
        sys.exit(1)

    start, end = spans[idx]
    # Also remove surrounding whitespace/newlines
    while start > 0 and html[start - 1] in " \t":
        start -= 1
    while end < len(html) and html[end] in "\r\n":
        end += 1
    html = html[:start] + html[end:]
    html = renumber_html(html)
    write_str_output(html, args)


def cmd_insert(args: argparse.Namespace) -> None:
    html = Path(args.file).read_text(encoding="utf-8")
    spans = find_slide_spans(html)
    pos = args.position  # 1-indexed; insert before this position

    new_slide = Path(args.new_slide).read_text(encoding="utf-8").strip()

    if not spans:
        print("Error: no slides found in deck", file=sys.stderr)
        sys.exit(1)

    if pos > len(spans):
        # Append after last slide
        _, last_end = spans[-1]
        html = html[:last_end] + "\n\n    " + new_slide + html[last_end:]
    else:
        idx = max(pos - 1, 0)
        ins_point = spans[idx][0]
        html = html[:ins_point] + new_slide + "\n\n    " + html[ins_point:]

    html = renumber_html(html)
    write_str_output(html, args)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deck.py",
        description="Inspect and edit assembled slide presentations.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # overview
    p_ov = sub.add_parser("overview", help="Show deck structure")
    p_ov.add_argument("file", help="Path to assembled HTML file")

    # extract
    p_ex = sub.add_parser("extract", help="Extract a single slide's HTML")
    p_ex.add_argument("file", help="Path to assembled HTML file")
    p_ex.add_argument("slide_num", type=int, help="Slide number (1-indexed)")

    # replace
    p_rp = sub.add_parser("replace", help="Replace a slide")
    p_rp.add_argument("file", help="Path to assembled HTML file")
    p_rp.add_argument("slide_num", type=int, help="Slide number to replace")
    p_rp.add_argument("new_slide", help="Path to HTML file with replacement slide")
    p_rp.add_argument("--in-place", action="store_true")
    p_rp.add_argument("-o", "--output", help="Write to this file instead of stdout")

    # delete
    p_dl = sub.add_parser("delete", help="Delete a slide")
    p_dl.add_argument("file", help="Path to assembled HTML file")
    p_dl.add_argument("slide_num", type=int, help="Slide number to delete")
    p_dl.add_argument("--in-place", action="store_true")
    p_dl.add_argument("-o", "--output", help="Write to this file instead of stdout")

    # insert
    p_in = sub.add_parser("insert", help="Insert a slide before a position")
    p_in.add_argument("file", help="Path to assembled HTML file")
    p_in.add_argument("position", type=int, help="Insert before this position (1-indexed)")
    p_in.add_argument("new_slide", help="Path to HTML file with new slide")
    p_in.add_argument("--in-place", action="store_true")
    p_in.add_argument("-o", "--output", help="Write to this file instead of stdout")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    dispatch = {
        "overview": cmd_overview,
        "extract": cmd_extract,
        "replace": cmd_replace,
        "delete": cmd_delete,
        "insert": cmd_insert,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
