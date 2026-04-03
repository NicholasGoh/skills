# Icon Cards

Cards with a colored icon square, title, and bullet list. Uses container hover dimming (non-hovered cards dim). Good for action items, plans, or categorized feature sets. Stacked bordered cards, each with a small colored icon square (`.primary`=navy, `.accent`=red, `.success`=green), bold title, and bullet list.

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
