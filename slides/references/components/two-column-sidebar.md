# Two-Column with Sidebar

The standard content slide layout. Left column has section label, h2, and description. Right column has the main content (list, cards, table, etc.). Grid layout: sidebar (300px) + content area (1fr). Wide-left variant (`.content-grid.wide-left`) reverses the proportions for slides where the left description needs more room.

## HTML

```html
<section class="slide alt" id="slide-N">
    <div class="slide-inner">
        <div class="content-grid slide-grid">
            <div>
                <p class="section-label reveal s1">Section Name</p>
                <h2 class="reveal s2">Slide<br>Title</h2>
                <p class="desc reveal s3">Supporting description that provides context for the content on the right.</p>
            </div>

            <div>
                <!-- Content component goes here -->
            </div>
        </div>
    </div>
    <span class="slide-num">0N / TOTAL</span>
</section>
```
