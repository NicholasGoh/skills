# Numbered List

Circled numbers with title + description. Good for rules, methodology steps, or criteria. Each item shows a small red-numbered circle (28px) on the left, title + description on the right, with light borders between rows.

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
