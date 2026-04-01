---
name: slides
description: >
  Build polished, scroll-snap HTML slide presentations with a minimalist corporate design system.
  Use this skill whenever the user asks to create a presentation, slide deck, pitch deck, report deck,
  or any content that should be delivered as full-viewport scrollable slides. Also trigger when the user
  asks for "slides about X", "present this as slides", "make this into a deck", or wants to turn research,
  analysis, or proposals into a visual presentation format. If the user references an existing HTML
  presentation and wants a new one in the same style, this is the skill to use.
---

# Slides

Build single-file HTML presentations that feel premium: clean typography, restrained color, smooth scroll-snap transitions, and subtle interactive highlights. Every presentation is self-contained — one `.html` file, no build step, opens in any browser.

## Design Philosophy

The aesthetic is **minimalist corporate** — not flashy, not sterile. Think: a well-designed annual report, not a startup pitch deck. The design earns trust through restraint.

Key principles:
- **Navy + red accent palette.** Navy (#1A1F5D) is the primary brand color for headings and emphasis. Red (#E10B0A) is used sparingly — progress bar, active states, numbered icons, danger/risk tags. Everything else is grayscale.
- **Light typographic weight.** Body text uses font-weight 300 (DM Sans). This creates a refined, airy feel. Headings use Figtree at 600-700 for contrast.
- **Generous whitespace.** Slides use clamp-based padding that scales with viewport. Content maxes out at 1060px. Let the content breathe.
- **Two-column grids.** Most slides use a sidebar (description/context) + main content area layout. The sidebar is typically 280-300px fixed, the content area takes the rest. This creates a consistent reading rhythm.
- **Alternating slide backgrounds.** White and light gray (#F6F6F6) alternate to give visual separation without borders.
- **Staggered reveal.** Elements fade up (14px translateY) as each slide enters view. Stagger delays from 0.1s to 0.7s (classes `s1` through `s7`) create a choreographed entrance.
- **Spotlight hover.** When a user hovers over a group of items, siblings dim to 35% opacity and the hovered item stays at full opacity. This focuses attention without tooltips or modals. There are four variants for different component types.

## How to Build a Presentation

### Step 1: Read the template

Read `references/template.html` in this skill directory. It contains the complete CSS design system (tokens, engine, shared components) and the JS presentation controller. The template has a `<!-- SLIDES GO HERE -->` marker where slide sections are inserted.

### Step 2: Plan the slide structure

Decide how many slides and what each one covers. Typical structures:
- **6-8 slides** for a focused topic (overview, 4-6 content slides, next steps)
- **8-12 slides** for a comprehensive report
- Keep each slide to ONE idea. If you're cramming, split it.

Every slide follows this shell:
```html
<section class="slide" id="slide-N">  <!-- add class "alt" for gray background -->
    <div class="slide-inner">
        <!-- content here -->
    </div>
    <span class="slide-num">0N / TOTAL</span>
</section>
```

Alternate `class="slide"` (white) and `class="slide alt"` (gray) for visual rhythm.

### Step 3: Pick components

Read `references/components.md` for the full catalog. Each component includes its HTML structure and any CSS that needs to be added to the `<style>` block. The template's engine CSS handles the framework; component CSS handles the specific layouts.

Common slide patterns:
- **Title slide**: 2-column with heading + sidebar summary
- **List/process slide**: 2-column with section label + numbered items or cards
- **Table slide**: Full-width header + data table
- **Card grid slide**: 2-column with description + card stack

### Step 4: Apply reveal classes

Every element that should animate in gets `class="reveal sN"` where N is the stagger order (1-7). Typically:
- Section labels get `s1`
- Headings get `s2`
- Description text gets `s3`
- Content items get `s2` through `s7` (staggered)

### Step 5: Apply spotlight classes

Add interactive hover focus to groups of related items. Choose the appropriate variant:
- **`.spot-group` + `.spot-item`**: For generic lists (rules, steps, grades). Apply `spot-group` to the container, `spot-item` to each child.
- **`.spot-table`**: For data tables. Apply to the `<table>` element. Rows auto-highlight.
- **`.spot-card`**: For side-by-side or stacked cards. Apply to each card. Uses `:has()` for sibling dimming + subtle elevation.
- **`.spot-group` + `.spot-row`**: For sidebar-style tight rows. Subtle background on hover.

### Step 6: Assemble and output

Copy the template, insert all slide sections, add any component-specific CSS to the `<style>` block (after the engine CSS), and update the total slide count in the `slide-num` spans.

## Adapting the Color Palette

If the user provides brand colors or you need a different palette, update the CSS custom properties in `:root`. The design system references these variables everywhere, so changing them propagates globally:

- `--brand-navy`: Primary heading/accent color
- `--brand-red`: Action/emphasis accent
- `--brand-dark-red`: Darker variant for hover/active
- `--brand-red-50`: Light tint for tag backgrounds
- `--brand-muted`: Secondary text color
- `--brand-light-gray`: Alternate slide background
- `--bg-header`: Light tint matching the primary color (used for pill backgrounds, table header hover)

When changing the palette, also update `--bg-header` to be a light tint of whatever replaces navy, and `--brand-red-50` to a light tint of whatever replaces red.

## Typography Reference

| Role | Font | Weight | Size pattern |
|------|------|--------|-------------|
| h1 | Figtree | 700 | clamp(2rem, 4vw, 3rem) |
| h2 | Figtree | 600 | clamp(1.6rem, 3vw, 2.4rem) |
| h3 | Figtree | 600 | clamp(0.85rem, 1.2vw, 0.95rem) |
| Body/desc | DM Sans | 300 | clamp(0.85rem, 1.2vw, 0.95rem) |
| Labels | Figtree | 500-600 | 0.6-0.65rem, uppercase, tracked |
| Pills | inherit | 500 | 0.6rem, uppercase |

## Key Details

- The Google Fonts link loads both Figtree (400-700) and DM Sans (300-500, italic). Include it in the `<head>`.
- All slides use `scroll-snap-align: start` and the HTML element uses `scroll-snap-type: y mandatory` for slide-to-slide snapping.
- The JS controller auto-generates nav dots from slide headings, handles keyboard (arrows + space), mouse wheel (throttled), and touch navigation.
- Include `@media (prefers-reduced-motion: reduce)` rules — the template already has them.
- Responsive: all grids collapse to single column at 900px. Nav dots and keyboard hint hide on mobile.
