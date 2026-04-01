# Deprioritised / Secondary Content

For secondary or deprioritised items shown in a sidebar or aside. Muted styling signals lower importance.

## HTML

```html
<div class="depri-sidebar">
    <div class="ds-title">Section Title</div>
    <div class="depri-item">
        <div class="di-name">Item Name</div>
        <div class="di-reason">Reason this is deprioritised or note</div>
    </div>
    <div class="depri-item">
        <div class="di-name">Another Item</div>
        <div class="di-reason">Another reason</div>
    </div>
    <div class="depri-source">Source: <a href="#" class="ref-link">Reference Link</a></div>
</div>
```

## CSS

```css
.depri-sidebar {
    padding-top: 0.5em;
}

.depri-sidebar .ds-title {
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--brand-muted);
    margin-bottom: 1.5em;
}

.depri-item {
    padding: 0.8em 0;
    border-bottom: 1px solid var(--border);
}

.depri-item:last-child { border-bottom: none; }

.depri-item .di-name {
    font-size: 0.82rem;
    font-weight: 400;
    color: var(--brand-muted);
    margin-bottom: 0.2em;
}

.depri-item .di-reason {
    font-size: 0.72rem;
    font-weight: 300;
    font-style: italic;
    color: var(--brand-grey-100);
    line-height: 1.5;
}

.depri-source {
    margin-top: 2em;
    font-size: 0.65rem;
    color: var(--brand-grey-100);
    letter-spacing: 0.05em;
}
```
