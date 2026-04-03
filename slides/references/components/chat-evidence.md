# Chat Evidence

A chat-like interface for presenting conversational evidence: user/AI message pairs with optional status annotations and summary callouts. Good for showing test transcripts, failure reproductions, security findings, or any evidence best presented as a dialogue. Renders as a rounded, scrollable container with alternating left/right aligned message bubbles (28px circle avatars, rounded bubble with light borders).

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
