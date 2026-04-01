# Stat Callouts

Large numbers with supporting labels. Good for KPIs, summary metrics, or score breakdowns. Arrange in a row or grid.

## HTML

```html
<div class="stat-row reveal s3">
    <div class="stat-item">
        <div class="stat-value">94%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-item">
        <div class="stat-value accent">3</div>
        <div class="stat-label">Critical Issues</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">B+</div>
        <div class="stat-label">Overall Grade</div>
    </div>
</div>
```

## CSS

```css
.stat-row {
    display: flex;
    gap: 3rem;
    margin: 2vh 0;
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-family: var(--font-heading);
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    color: var(--brand-navy);
    line-height: 1.1;
}

.stat-value.accent { color: var(--brand-red); }

.stat-label {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--brand-muted);
    margin-top: 0.5em;
}
```
