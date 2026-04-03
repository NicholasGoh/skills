# Title Slide

The opening slide. Two-column grid: main content (1fr) + sidebar (340px). Left has tag line (red dot + uppercase category label), h1 heading, subtitle, and optional legend/method row with colored dot icons. Right has a sidebar summary panel (see Sidebar Panel component).

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
