#!/usr/bin/env python3
"""Grade all eval outputs against assertions by parsing the HTML."""

import json
import os
import re
from pathlib import Path

ITER_DIR = Path(__file__).parent

def read_html(path):
    """Read HTML file and return contents."""
    html_path = path / "outputs" / "presentation.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8", errors="replace")
    return ""

def check_assertion(assertion_id, html):
    """Check a single assertion against HTML content. Returns (passed, evidence)."""
    html_lower = html.lower()

    if assertion_id == "uses-figtree-dm-sans":
        has_figtree = "figtree" in html_lower
        has_dm_sans = "dm sans" in html_lower or "dm+sans" in html_lower
        passed = has_figtree and has_dm_sans
        evidence = f"Figtree: {'found' if has_figtree else 'missing'}, DM Sans: {'found' if has_dm_sans else 'missing'}"
        return passed, evidence

    elif assertion_id == "has-brand-navy":
        # Check for navy color in CSS
        has_navy = bool(re.search(r'#1a1f5d|#1A1F5D', html))
        # Also check for similar dark blues if exact match not found
        if not has_navy:
            has_navy = bool(re.search(r'brand-navy|--navy', html_lower))
        evidence = f"Navy (#1A1F5D or --brand-navy): {'found' if has_navy else 'not found'}"
        return has_navy, evidence

    elif assertion_id == "has-scroll-snap":
        has_snap = "scroll-snap-type" in html_lower
        evidence = f"scroll-snap-type: {'found' if has_snap else 'not found'}"
        return has_snap, evidence

    elif assertion_id == "has-reveal-animations":
        has_reveal_class = bool(re.search(r'class="[^"]*reveal', html))
        has_stagger = bool(re.search(r'\bs[1-7]\b', html)) or bool(re.search(r'transition-delay', html_lower))
        passed = has_reveal_class and has_stagger
        evidence = f"reveal class: {'found' if has_reveal_class else 'missing'}, stagger delays: {'found' if has_stagger else 'missing'}"
        return passed, evidence

    elif assertion_id == "has-spotlight-hover":
        has_spot = bool(re.search(r'spot-group|spot-item|spot-table|spot-card|spot-row', html_lower))
        # Also check for the opacity dimming pattern
        has_dim = bool(re.search(r'opacity:\s*0\.3[0-5]', html_lower))
        passed = has_spot or has_dim
        evidence = f"spotlight classes: {'found' if has_spot else 'missing'}, dim pattern: {'found' if has_dim else 'missing'}"
        return passed, evidence

    elif assertion_id == "has-progress-bar":
        has_progress = "progress-bar" in html_lower or "progress_bar" in html_lower
        evidence = f"progress bar: {'found' if has_progress else 'not found'}"
        return has_progress, evidence

    elif assertion_id == "has-nav-dots":
        has_dots = "nav-dot" in html_lower or "nav_dot" in html_lower or "nav-dots" in html_lower
        evidence = f"nav dots: {'found' if has_dots else 'not found'}"
        return has_dots, evidence

    elif assertion_id == "content-accuracy":
        # This varies per eval - return basic content check
        return True, "Content check requires eval-specific logic (checked separately)"

    elif assertion_id == "min-slides":
        # Count slide sections
        slide_count = len(re.findall(r'class="slide[\s"]', html))
        if slide_count == 0:
            # Try other patterns
            slide_count = len(re.findall(r'<section[^>]*>', html))
        passed = slide_count >= 5
        evidence = f"Found {slide_count} slides (minimum 5 required)"
        return passed, evidence

    elif assertion_id == "light-font-weight":
        has_300 = "font-weight: 300" in html_lower or "font-weight:300" in html_lower
        evidence = f"font-weight 300: {'found' if has_300 else 'not found'}"
        return has_300, evidence

    return False, "Unknown assertion"


def check_content_accuracy(eval_name, html):
    """Eval-specific content accuracy checks."""
    html_lower = html.lower()

    if eval_name == "quarterly-business-review":
        checks = {
            "$4.2M": "4.2m" in html_lower or "$4.2m" in html_lower or "4.2 m" in html_lower,
            "18%": "18%" in html,
            "2 products": bool(re.search(r'2\s*(new\s*)?product', html_lower)),
            "3 risks": bool(re.search(r'supply chain|competitor|talent retention', html_lower)),
            "APAC": "apac" in html_lower,
        }
    elif eval_name == "microservices-migration":
        checks = {
            "auth service": "auth" in html_lower,
            "billing service": "billing" in html_lower,
            "notifications": "notification" in html_lower,
            "search service": "search" in html_lower,
            "content service": "content" in html_lower,
            "analytics service": "analytics" in html_lower,
            "Django": "django" in html_lower,
        }
    elif eval_name == "employee-onboarding":
        checks = {
            "Engineering": "engineering" in html_lower,
            "Product": "product" in html_lower,
            "Design": "design" in html_lower,
            "Sales": "sales" in html_lower,
            "Slack": "slack" in html_lower,
            "Linear": "linear" in html_lower,
            "GitHub": "github" in html_lower,
            "Figma": "figma" in html_lower,
        }
    else:
        return True, "Unknown eval"

    found = [k for k, v in checks.items() if v]
    missing = [k for k, v in checks.items() if not v]
    passed = len(missing) == 0
    evidence = f"Found: {', '.join(found)}" + (f". Missing: {', '.join(missing)}" if missing else "")
    return passed, evidence


def grade_run(eval_dir, run_type, eval_name):
    """Grade a single run."""
    run_dir = eval_dir / run_type
    html = read_html(run_dir)

    if not html:
        return {"error": f"No presentation.html found in {run_dir}/outputs/"}

    # Load assertions from eval metadata
    meta_path = eval_dir / "eval_metadata.json"
    with open(meta_path) as f:
        meta = json.load(f)

    expectations = []
    total_passed = 0

    for assertion in meta["assertions"]:
        if assertion["id"] == "content-accuracy":
            passed, evidence = check_content_accuracy(eval_name, html)
        else:
            passed, evidence = check_assertion(assertion["id"], html)

        expectations.append({
            "text": assertion["text"],
            "passed": passed,
            "evidence": evidence
        })
        if passed:
            total_passed += 1

    result = {
        "eval_id": meta["eval_id"],
        "eval_name": eval_name,
        "run_type": run_type,
        "pass_rate": total_passed / len(expectations) if expectations else 0,
        "passed": total_passed,
        "total": len(expectations),
        "expectations": expectations
    }

    # Save grading.json
    grading_path = run_dir / "grading.json"
    with open(grading_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


def main():
    evals = [
        ("eval-1-qbr", "quarterly-business-review"),
        ("eval-2-microservices", "microservices-migration"),
        ("eval-3-onboarding", "employee-onboarding"),
    ]

    all_results = []

    for eval_dir_name, eval_name in evals:
        eval_dir = ITER_DIR / eval_dir_name
        for run_type in ["with_skill", "without_skill"]:
            result = grade_run(eval_dir, run_type, eval_name)
            all_results.append(result)
            status = f"{result.get('passed', '?')}/{result.get('total', '?')}"
            print(f"{eval_dir_name}/{run_type}: {status} assertions passed")

    print("\n--- Summary ---")
    for r in all_results:
        name = f"{r.get('eval_name', '?')}/{r.get('run_type', '?')}"
        print(f"  {name}: {r.get('pass_rate', 0):.0%} ({r.get('passed', 0)}/{r.get('total', 0)})")


if __name__ == "__main__":
    main()
