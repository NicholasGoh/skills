# Grade / Rating Cards

Rows with a prominent letter/grade/icon and description. Good for rating scales, status levels, or categorized items. Each row shows a large colored letter grade (52px) on the left, title + description on the right. Grade colors: `.a`=green, `.b`=blue, `.c`=gold, `.d`=orange, `.f`=red, `.na`=gray.

## HTML

```html
<div class="grade-cards spot-group">
    <div class="grade-card spot-item reveal s2">
        <div class="gc-letter a">A</div>
        <div>
            <div class="gc-title">Excellent</div>
            <div class="gc-desc">Fully meets all requirements, no issues</div>
        </div>
    </div>
    <div class="grade-card spot-item reveal s3">
        <div class="gc-letter b">B</div>
        <div>
            <div class="gc-title">Good</div>
            <div class="gc-desc">Meets requirements with minor improvements needed</div>
        </div>
    </div>
    <!-- more grades... -->
</div>
```
