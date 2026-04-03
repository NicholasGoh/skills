# Risk / Feature Cards

Bordered cards with a tag, title, description, and optional pill row. Uses `.spot-card` for sibling-dim hover. Good for risks, features, highlights, or callouts. Rounded bordered cards with a red tag pill + bold title in the header, muted description, and optional navy pills at the bottom.

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
