# Icon Cards

Cards with a colored icon square, title, and bullet list. Uses container hover dimming. Good for action items, plans, or categorized feature sets.

## HTML

```html
<div class="icon-cards">
    <div class="icon-card reveal s3">
        <div class="icon-card-header">
            <div class="icon-card-icon primary">&#9741;</div>
            <div class="icon-card-title">Card Title</div>
        </div>
        <ul>
            <li>First bullet point</li>
            <li>Second bullet point</li>
            <li>Third bullet point</li>
        </ul>
    </div>

    <div class="icon-card reveal s4">
        <div class="icon-card-header">
            <div class="icon-card-icon accent">&#9834;</div>
            <div class="icon-card-title">Another Card</div>
        </div>
        <ul>
            <li>Item one</li>
            <li>Item two</li>
        </ul>
    </div>
</div>
```

## CSS

```css
.icon-cards {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

.icon-card {
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    background: var(--brand-white);
    transition: border-color 0.25s ease, box-shadow 0.25s ease, opacity 0.25s ease;
}

.icon-card:hover {
    border-color: var(--brand-navy);
    box-shadow: 0 3px 12px rgba(26, 31, 93, 0.07);
}

.icon-cards:hover .icon-card:not(:hover) {
    opacity: 0.4;
}

.icon-card-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.6rem;
}

.icon-card-icon {
    width: 28px;
    height: 28px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    flex-shrink: 0;
}

.icon-card-icon.primary { background: var(--bg-header); color: var(--brand-navy); }
.icon-card-icon.accent { background: var(--brand-red-50); color: var(--brand-dark-red); }
.icon-card-icon.success { background: #E8F5E9; color: #2E7D32; }

.icon-card-title {
    font-family: var(--font-heading);
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--brand-navy);
}

.icon-card ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.icon-card li {
    font-size: 0.75rem;
    color: var(--brand-muted);
    line-height: 1.6;
    padding-left: 1em;
    position: relative;
}

.icon-card li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.55em;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: var(--brand-grey-100);
}
```
