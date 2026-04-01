# Numbered List

Circled numbers with title + description. Good for rules, methodology steps, or criteria.

Use inside a Two-Column layout on the right side. Apply `spot-group` on the container and `spot-item` on each item.

## HTML

```html
<div class="rule-list spot-group">
    <div class="rule-item spot-item reveal s2">
        <div class="ri-icon">1</div>
        <div>
            <div class="ri-title">Rule Title</div>
            <div class="ri-desc">Description of this rule or criterion and how it applies.</div>
        </div>
    </div>
    <div class="rule-item spot-item reveal s3">
        <div class="ri-icon">2</div>
        <div>
            <div class="ri-title">Another Rule</div>
            <div class="ri-desc">Further explanation of this point.</div>
        </div>
    </div>
    <!-- more items... -->
</div>
```

## CSS

```css
.rule-list {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.rule-item {
    display: grid;
    grid-template-columns: 28px 1fr;
    gap: 1rem;
    padding: 1.2em 0;
    border-bottom: 1px solid var(--border);
    align-items: start;
}

.rule-item:last-child { border-bottom: none; }

.rule-item .ri-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    background: var(--brand-white);
    border: 1px solid var(--border);
    color: var(--brand-red);
}

/* On alt (gray) slides, icon background stays white */
.slide.alt .rule-item .ri-icon { background: var(--brand-white); }

.rule-item .ri-title {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--brand-black);
    margin-bottom: 0.2em;
}

.rule-item .ri-desc {
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--brand-muted);
    line-height: 1.6;
}
```
