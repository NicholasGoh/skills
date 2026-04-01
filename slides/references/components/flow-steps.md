# Flow Steps

Numbered process with red-accented step numbers. Good for workflows, timelines, or sequential processes.

## HTML

```html
<div class="flow-steps spot-group">
    <div class="flow-step spot-item reveal s2">
        <div class="fs-num">1</div>
        <div>
            <div class="fs-title">First Step</div>
            <div class="fs-desc">Description of what happens in this step.</div>
        </div>
    </div>
    <div class="flow-step spot-item reveal s3">
        <div class="fs-num">2</div>
        <div>
            <div class="fs-title">Second Step</div>
            <div class="fs-desc">Description of what happens next.</div>
        </div>
    </div>
    <!-- more steps... -->
</div>
```

## CSS

```css
.flow-steps {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.flow-step {
    display: grid;
    grid-template-columns: 40px 1fr;
    gap: 1rem;
    padding: 1.2em 0;
    border-bottom: 1px solid var(--border);
    align-items: start;
}

.flow-step:last-child { border-bottom: none; }

.flow-step .fs-num {
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--brand-red);
    background: var(--brand-white);
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border);
}

.flow-step .fs-title {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--brand-black);
    margin-bottom: 0.2em;
}

.flow-step .fs-desc {
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--brand-muted);
    line-height: 1.6;
}
```
