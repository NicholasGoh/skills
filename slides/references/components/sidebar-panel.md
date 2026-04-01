# Sidebar Panel

A light-gray rounded box with a title and labeled rows. Used in title slides for summaries, or anywhere you need a compact reference panel.

## HTML

```html
<div class="sidebar spot-group">
    <div class="sidebar-title">Panel Title</div>
    <div class="p-row spot-row">
        <span class="p-label">Item Name</span>
        <span class="pill primary">Status</span>
    </div>
    <div class="p-row spot-row">
        <span class="p-label">Another Item</span>
        <span class="pill accent">Urgent</span>
    </div>
    <div class="p-row dimmed spot-row">
        <span class="p-label">Inactive Item</span>
        <span class="pill muted">Deferred</span>
    </div>
</div>
```

## CSS

```css
.sidebar {
    background: var(--brand-light-gray);
    border-radius: 10px;
    padding: 2em 1.8em;
}

.sidebar-title {
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--brand-muted);
    margin-bottom: 1.5em;
}

.p-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.65em 0;
    border-bottom: 1px solid var(--border);
}

.p-row:last-child { border-bottom: none; }

.p-row .p-label {
    font-size: 0.8rem;
    font-weight: 400;
    color: var(--brand-black);
}

.p-row.dimmed .p-label { color: var(--brand-muted); }
```
