# Title Slide

The opening slide. Two-column: left has tag line, h1, subtitle, and optional legend/method row. Right has a sidebar summary panel.

## HTML

```html
<section class="slide" id="slide-1">
    <div class="slide-inner">
        <div class="title-grid slide-grid">
            <div>
                <div class="tag-line reveal s1">
                    <span class="dot"></span>
                    <span class="text">CATEGORY LABEL</span>
                </div>
                <h1 class="reveal s2">Main<br>Heading</h1>
                <p class="title-subtitle desc reveal s3">Brief description of what this presentation covers and its scope.</p>

                <!-- Optional: method/legend row -->
                <div class="method-row reveal s4">
                    <div class="method-item">
                        <div class="icon primary"></div>
                        <div>
                            <div class="m-label">Category A</div>
                            <div class="m-desc">Short description</div>
                        </div>
                    </div>
                    <div class="method-item">
                        <div class="icon accent"></div>
                        <div>
                            <div class="m-label">Category B</div>
                            <div class="m-desc">Short description</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sidebar (see Sidebar Panel component) -->
            <div class="sidebar reveal s5 spot-group">
                <div class="sidebar-title">Summary</div>
                <!-- sidebar rows here -->
            </div>
        </div>
    </div>
    <span class="slide-num">01 / TOTAL</span>
</section>
```

## CSS

```css
.title-grid {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 4rem;
    align-items: center;
}

.title-subtitle {
    max-width: 460px;
    margin-bottom: 3vh;
}

.method-row {
    display: flex;
    gap: 1.5rem;
}

.method-item {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
}

.method-item .icon {
    width: 8px;
    height: 8px;
    border-radius: 2px;
    flex-shrink: 0;
    margin-top: 2px;
}

.method-item .icon.primary { background: var(--brand-navy); }
.method-item .icon.accent { background: var(--brand-red); }

.method-item .m-label {
    font-size: 0.75rem;
    color: var(--brand-black);
    font-weight: 500;
}

.method-item .m-desc {
    font-size: 0.7rem;
    color: var(--brand-muted);
    font-weight: 300;
}
```
