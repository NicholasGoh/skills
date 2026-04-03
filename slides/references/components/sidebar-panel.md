# Sidebar Panel

A light-gray rounded box with a title and labeled rows. Used in title slides for summaries, or anywhere you need a compact reference panel. Rows display as flex: label on the left, pill badge on the right, separated by light borders. Dimmed rows (`.dimmed`) use muted text.

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
