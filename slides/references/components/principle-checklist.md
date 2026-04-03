# Principle / Checklist

Numbered rows with status pills. Good for feature lists, governance principles, requirements, or any list where items have a status/category. Three-column grid: 2-digit number, item name, and status pill. Active items have red numbers; inactive ones are muted.

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
