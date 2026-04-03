#!/usr/bin/env bash
# assemble.sh - Assemble a slide presentation from template + components + slide HTML
#
# Usage:
#   assemble.sh <output.html> <title> <slides-file> [component-name ...]
#
# Example:
#   assemble.sh ./presentation.html "Q1 Review" /tmp/slides.html \
#       title-slide two-column-sidebar flow-steps stat-callouts
#
# Component names are basenames without extension (e.g. "flow-steps" not "flow-steps.css").
# The script looks for .css files in references/components/ relative to itself.

set -euo pipefail

if [ $# -lt 3 ]; then
    echo "Usage: assemble.sh <output.html> <title> <slides-file> [component ...]" >&2
    exit 1
fi

OUTPUT="$1"
TITLE="$2"
SLIDES_FILE="$3"
shift 3

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$SKILL_DIR/references/template.html"
COMP_DIR="$SKILL_DIR/references/components"

# 1. Copy template
cp "$TEMPLATE" "$OUTPUT"

# 2. Replace title
sed -i "s/PRESENTATION_TITLE/$TITLE/g" "$OUTPUT"

# 3. Concatenate component CSS and inject at marker
if [ $# -gt 0 ]; then
    CSS_TMP="$(mktemp)"
    for comp in "$@"; do
        css_file="$COMP_DIR/${comp}.css"
        if [ ! -f "$css_file" ]; then
            echo "Warning: $css_file not found, skipping" >&2
            continue
        fi
        cat "$css_file" >> "$CSS_TMP"
        echo "" >> "$CSS_TMP"
    done
    sed -i "/\/\* __COMPONENT_CSS__ \*\//r $CSS_TMP" "$OUTPUT"
    rm -f "$CSS_TMP"
fi

# 4. Inject slide HTML at marker
sed -i "/<!-- __SLIDES__ -->/r $SLIDES_FILE" "$OUTPUT"

# 5. Update slide number totals
TOTAL=$(grep -c '<section class="slide' "$OUTPUT" || true)
PADDED=$(printf "%02d" "$TOTAL")
sed -i "s|/ TOTAL|/ $PADDED|g" "$OUTPUT"

echo "Assembled $OUTPUT ($TOTAL slides)"
