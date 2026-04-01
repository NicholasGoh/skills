# Risk / Feature Cards

Bordered cards with a tag, title, description, and optional pill row. Uses `.spot-card` for sibling-dim hover. Good for risks, features, highlights, or callouts.

## HTML

```html
<div>
    <div class="risk-card spot-card reveal s4">
        <div class="rc-header">
            <span class="rc-tag">Label 1</span>
            <span class="rc-title">Card Title</span>
        </div>
        <div class="rc-desc">Description of this item and why it matters.</div>
        <div class="rc-maps">
            <span class="rc-pill">Related A</span>
            <span class="rc-pill">Related B</span>
        </div>
    </div>

    <div class="risk-card spot-card reveal s5">
        <div class="rc-header">
            <span class="rc-tag">Label 2</span>
            <span class="rc-title">Another Card</span>
        </div>
        <div class="rc-desc">Another description.</div>
        <div class="rc-maps">
            <span class="rc-pill">Related C</span>
        </div>
    </div>
</div>
```

## CSS

```css
.risk-card {
    background: var(--brand-white);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.4em 1.3em;
    margin-bottom: 1rem;
}

.risk-card .rc-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.6em;
}

.risk-card .rc-tag {
    font-family: var(--font-heading);
    font-size: 0.6rem;
    font-weight: 600;
    color: var(--brand-dark-red);
    background: var(--brand-red-50);
    padding: 0.25em 0.5em;
    border-radius: 3px;
}

.risk-card .rc-title {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--brand-black);
}

.risk-card .rc-desc {
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--brand-muted);
    line-height: 1.6;
    margin-bottom: 0.6em;
}

.risk-card .rc-maps {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
}

.risk-card .rc-pill {
    font-size: 0.58rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    color: var(--brand-navy);
    background: var(--bg-header);
    padding: 0.25em 0.5em;
    border-radius: 3px;
}
```
