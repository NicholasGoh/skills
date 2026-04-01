# Grade / Rating Cards

Rows with a prominent letter/grade/icon and description. Good for rating scales, status levels, or categorized items.

## HTML

```html
<div class="grade-cards spot-group">
    <div class="grade-card spot-item reveal s2">
        <div class="gc-letter a">A</div>
        <div>
            <div class="gc-title">Excellent</div>
            <div class="gc-desc">Fully meets all requirements, no issues</div>
        </div>
    </div>
    <div class="grade-card spot-item reveal s3">
        <div class="gc-letter b">B</div>
        <div>
            <div class="gc-title">Good</div>
            <div class="gc-desc">Meets requirements with minor improvements needed</div>
        </div>
    </div>
    <!-- more grades... -->
</div>
```

## CSS

```css
.grade-cards {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.grade-card {
    display: grid;
    grid-template-columns: 52px 1fr;
    gap: 1rem;
    padding: 1.1em 0;
    border-bottom: 1px solid var(--border);
    align-items: baseline;
}

.grade-card:last-child { border-bottom: none; }

.grade-card .gc-letter {
    font-family: var(--font-heading);
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
}

/* Color each grade — adjust these to match your rating scheme */
.grade-card .gc-letter.a { color: #16a34a; }
.grade-card .gc-letter.b { color: #2563eb; }
.grade-card .gc-letter.c { color: #ca8a04; }
.grade-card .gc-letter.d { color: #ea580c; }
.grade-card .gc-letter.f { color: var(--brand-red); }
.grade-card .gc-letter.na { color: var(--brand-grey-100); }

.grade-card .gc-title {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--brand-black);
}

.grade-card .gc-desc {
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--brand-muted);
    line-height: 1.5;
    margin-top: 0.15em;
}
```
