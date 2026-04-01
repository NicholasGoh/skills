# Principle / Checklist

Numbered rows with status pills. Good for feature lists, governance principles, requirements, or any list where items have a status/category.

## HTML

```html
<div class="principle-list spot-group">
    <div class="pl-item active spot-item reveal s2">
        <div class="pl-num">01</div>
        <div class="pl-name">Active Item Name</div>
        <span class="pill primary">Active</span>
    </div>
    <div class="pl-item inactive spot-item reveal s3">
        <div class="pl-num">02</div>
        <div class="pl-name">Inactive Item Name</div>
        <span class="pill muted">Skipped</span>
    </div>
    <!-- more items... -->
</div>
```

## CSS

```css
.principle-list {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.pl-item {
    display: grid;
    grid-template-columns: 32px 1fr auto;
    gap: 0.8rem;
    padding: 0.75em 0;
    border-bottom: 1px solid var(--border);
    align-items: center;
}

.pl-item:last-child { border-bottom: none; }

.pl-item .pl-num {
    font-family: var(--font-heading);
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--brand-muted);
    text-align: center;
}

.pl-item.active .pl-num { color: var(--brand-red); }

.pl-item .pl-name {
    font-size: 0.82rem;
    font-weight: 400;
    color: var(--brand-black);
}

.pl-item.inactive .pl-name { color: var(--brand-muted); }
```
