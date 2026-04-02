# Chat Evidence

A chat-like interface for presenting conversational evidence: user/AI message pairs with optional status annotations and summary callouts. Good for showing test transcripts, failure reproductions, security findings, or any evidence best presented as a dialogue.

Use inside a Two-Column layout on the right side, or full-width via an evidence grid. Multiple chat containers can sit side-by-side in a 2-column evidence grid, or span the full width with `grid-column: 1 / -1`.

## Core Structure

Each chat container holds a sequence of messages. Messages alternate between `user` and `ai` roles. An optional divider labels the conversation topic.

### Avatars

Avatar text is flexible: use short labels like `U` / `AI`, or variant labels like `V0` / `V1` when comparing prompt variations.

### Status Indicators

AI bubbles can carry a left-border color to signal status:
- **Success** (green via `--brand-navy`): correct or expected response
- **Warning** (amber): degraded or uncertain response
- **Error** (red via `--brand-red`): incorrect, unauthorized, or failed response

A small mono-font status label inside the bubble reinforces the signal (e.g., `BOUNDARY CROSSED`, `NO ACCESS CHECK`).

### Trace Steps

For AI responses that involve reasoning or multi-step logic, use `.trace-step` blocks inside the bubble to show intermediate steps (tool calls, SQL queries, API lookups, etc.).

### Summary Callouts

After a message sequence, an optional summary callout box explains the finding. Use it to spell out the implication of the conversation above.

## HTML

### Basic chat container with divider

```html
<div class="chat-container">
    <div class="chat-divider">Conversation Topic</div>

    <div class="chat-message user">
        <div class="chat-avatar user-avatar">U</div>
        <div class="chat-bubble">User's question or prompt goes here.</div>
    </div>

    <div class="chat-message ai">
        <div class="chat-avatar ai-avatar">AI</div>
        <div class="chat-bubble">
            AI response text here.
        </div>
    </div>
</div>
```

### AI bubble with status border and label

```html
<div class="chat-message ai">
    <div class="chat-avatar ai-avatar">AI</div>
    <div class="chat-bubble chat-status-error">
        <span class="chat-status-label chat-label-error">BOUNDARY CROSSED</span>
        Response containing the error or unauthorized data.
    </div>
</div>
```

Status variants:
- `.chat-status-success` + `.chat-label-success`: left border green, label green
- `.chat-status-warn` + `.chat-label-warn`: left border amber, label amber
- `.chat-status-error` + `.chat-label-error`: left border red, label red
- `.chat-status-error.chat-status-severe`: red border + light red background for critical failures

### AI bubble with trace step

```html
<div class="chat-message ai">
    <div class="chat-avatar ai-avatar">AI</div>
    <div class="chat-bubble">
        Summary of the response.
        <div class="chat-trace">
            <span class="chat-trace-label">SQL Query</span>
            SELECT revenue FROM accounts WHERE id = 42
        </div>
    </div>
</div>
```

### Summary callout after messages

```html
<div class="chat-callout chat-callout-error">
    <div class="chat-callout-label">SECURITY IMPACT</div>
    <div class="chat-callout-body">
        Explanation of what the conversation above demonstrates and why it matters.
    </div>
</div>
```

Callout variants: `.chat-callout-error` (red), `.chat-callout-warn` (amber), `.chat-callout-info` (navy).

### Evidence grid: multiple chats side by side

```html
<div class="evidence-grid">
    <div class="chat-container">
        <div class="chat-divider">Example 1</div>
        <!-- messages... -->
    </div>
    <div class="chat-container">
        <div class="chat-divider">Example 2</div>
        <!-- messages... -->
    </div>
</div>
```

For a full-width chat inside an evidence grid:
```html
<div class="evidence-grid">
    <div class="chat-container" style="grid-column: 1 / -1;">
        <!-- messages... -->
    </div>
</div>
```

### Value highlights inside bubbles

Use inline spans for emphasis:
- `<span class="chat-val-highlight">x%</span>`: navy highlight for correct/notable values
- `<span class="chat-val-error">$xMM</span>`: red for erroneous values
- `<span class="chat-val-conflict">conflicting value</span>`: red background pill for contradictions

## CSS

```css
/* ---- Chat Evidence ---- */

.chat-container {
    background: var(--brand-light-gray);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: 65vh;
    overflow-y: auto;
    overscroll-behavior: contain;
}

/* On alt (gray) slides, chat background stays white for contrast */
.slide.alt .chat-container { background: var(--brand-white); }

.chat-message {
    display: flex;
    gap: 0.6rem;
    max-width: 85%;
    align-items: flex-start;
}

.chat-message.user { align-self: flex-end; flex-direction: row-reverse; }
.chat-message.ai { align-self: flex-start; }

.chat-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-heading);
    font-size: 0.6rem;
    font-weight: 600;
    flex-shrink: 0;
    margin-top: 2px;
}

.chat-avatar.user-avatar {
    background: var(--bg-header);
    color: var(--brand-navy);
    border: 1px solid var(--brand-grey-50);
}

.chat-avatar.ai-avatar {
    background: var(--brand-red-50);
    color: var(--brand-red);
    border: 1px solid var(--brand-red-50);
}

.chat-bubble {
    padding: 0.6rem 0.9rem;
    border-radius: 12px;
    font-size: 0.8rem;
    line-height: 1.5;
    color: var(--brand-black);
}

.chat-message.user .chat-bubble {
    background: var(--bg-header);
    border: 1px solid var(--brand-grey-50);
    border-top-right-radius: 4px;
}

.chat-message.ai .chat-bubble {
    background: var(--brand-white);
    border: 1px solid var(--border);
    color: var(--brand-muted);
    border-top-left-radius: 4px;
}

/* On alt slides, AI bubbles use light gray to stand out from the white container */
.slide.alt .chat-message.ai .chat-bubble {
    background: var(--brand-light-gray);
}

/* ---- Status borders ---- */

.chat-status-success { border-left: 2px solid var(--brand-navy); }
.chat-status-warn { border-left: 2px solid #D97706; }
.chat-status-error { border-left: 2px solid var(--brand-red); }
.chat-status-error.chat-status-severe {
    border-left: 2px solid var(--brand-red);
    background: var(--brand-red-50);
}

.chat-status-label {
    display: block;
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.2rem;
}

.chat-label-success { color: var(--brand-navy); }
.chat-label-warn { color: #D97706; }
.chat-label-error { color: var(--brand-red); }

/* ---- Trace steps ---- */

.chat-trace {
    margin-top: 0.4rem;
    padding: 0.3rem 0.5rem;
    background: var(--brand-light-gray);
    border-left: 2px solid var(--brand-navy);
    border-radius: 0 4px 4px 0;
    font-family: 'DM Sans', monospace;
    font-size: 0.7rem;
    color: var(--brand-muted);
}

.chat-trace-label {
    color: var(--brand-navy);
    font-weight: 500;
    display: block;
    margin-bottom: 0.15rem;
}

/* ---- Value highlights ---- */

.chat-val-highlight { color: var(--brand-navy); font-weight: 500; }
.chat-val-error { color: var(--brand-red); font-weight: 500; }
.chat-val-conflict {
    background: var(--brand-red-50);
    padding: 0.1rem 0.35rem;
    border-radius: 3px;
    color: var(--brand-red);
    font-weight: 500;
}

/* ---- Divider ---- */

.chat-divider {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--brand-muted);
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.chat-divider::before,
.chat-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ---- Summary callouts ---- */

.chat-callout {
    margin-top: 1rem;
    padding: 0.75rem;
    border-radius: 6px;
}

.chat-callout-error {
    background: var(--brand-red-50);
    border-left: 3px solid var(--brand-red);
}

.chat-callout-warn {
    background: #FEF3C7;
    border-left: 3px solid #D97706;
}

.chat-callout-info {
    background: var(--bg-header);
    border-left: 3px solid var(--brand-navy);
}

.chat-callout-label {
    font-family: var(--font-heading);
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.25rem;
}

.chat-callout-error .chat-callout-label { color: var(--brand-red); }
.chat-callout-warn .chat-callout-label { color: #D97706; }
.chat-callout-info .chat-callout-label { color: var(--brand-navy); }

.chat-callout-body {
    font-size: 0.8rem;
    font-weight: 300;
    color: var(--brand-muted);
    line-height: 1.6;
}

/* ---- Evidence grid ---- */

.evidence-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-top: 1.5rem;
}

@media (max-width: 900px) {
    .evidence-grid { grid-template-columns: 1fr; }
}
```
