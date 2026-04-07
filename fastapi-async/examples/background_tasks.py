"""
background_tasks.py
===================
Three ways to run work "in the background" in FastAPI, and when to use each.

1. BackgroundTasks  — runs AFTER the response is sent (fire-and-forget)
2. create_task      — runs NOW on the event loop, concurrent with current request
3. gather           — runs multiple coroutines concurrently, waits for ALL results

Run this file to see the timing behavior of each approach.
"""

import asyncio
import time

import uvicorn
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


# ─── Simulated work ──────────────────────────────────────────────────────────

async def send_email(to: str):
    """Simulate sending an email (async IO)."""
    print(f"  [email] Sending to {to}...")
    await asyncio.sleep(1)
    print(f"  [email] Sent to {to}")


async def log_event(event: str):
    """Simulate logging to an external service."""
    print(f"  [log] Recording: {event}...")
    await asyncio.sleep(0.5)
    print(f"  [log] Recorded: {event}")


async def update_analytics(page: str):
    """Simulate an analytics write."""
    print(f"  [analytics] Updating for {page}...")
    await asyncio.sleep(0.3)
    print(f"  [analytics] Updated for {page}")


def sync_audit_log(action: str):
    """Sync function — BackgroundTasks handles both sync and async callables."""
    print(f"  [audit] Writing: {action}...")
    time.sleep(0.5)
    print(f"  [audit] Written: {action}")


# ─── 1. BackgroundTasks — fire and forget, runs AFTER response ───────────────

@app.post("/signup")
async def signup(email: str, bg: BackgroundTasks):
    """
    BackgroundTasks: the response is sent IMMEDIATELY, then the email
    task runs. The client doesn't wait for the email to be sent.

    Use for: notifications, cleanup, non-critical logging.
    """
    bg.add_task(send_email, email)             # async callable — OK
    bg.add_task(sync_audit_log, "user_signup")  # sync callable — also OK
    return {"status": "created", "email": email}


@app.post("/signup-multiple")
async def signup_with_multiple_tasks(email: str, bg: BackgroundTasks):
    """
    You can add multiple background tasks — they run sequentially
    in the order they were added, AFTER the response.
    """
    bg.add_task(send_email, email)
    bg.add_task(log_event, "signup")
    bg.add_task(update_analytics, "/signup")
    return {"status": "created"}


# ─── 2. create_task — runs NOW, concurrent with current request ──────────────

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """
    create_task: schedules a coroutine on the event loop IMMEDIATELY.
    The logging runs concurrently while we fetch the item.
    The response includes the item — it does NOT wait for the log.

    Use for: fire-and-forget work that should start right away.
    """
    asyncio.create_task(log_event(f"viewed item {item_id}"))  # starts NOW

    # Simulate fetching item from DB
    await asyncio.sleep(0.5)
    return {"item_id": item_id, "name": f"Widget {item_id}"}


# ─── 3. gather — run multiple things concurrently, wait for ALL ──────────────

@app.get("/dashboard")
async def dashboard():
    """
    gather: runs multiple coroutines concurrently and waits for all results.
    Total time ≈ max(individual times), not sum.

    Use for: parallel data fetching where you need all results before responding.
    """
    email_count, events, analytics = await asyncio.gather(
        _fetch_email_count(),
        _fetch_recent_events(),
        _fetch_analytics_summary(),
    )
    return {
        "emails": email_count,
        "events": events,
        "analytics": analytics,
    }


async def _fetch_email_count() -> int:
    await asyncio.sleep(0.3)
    return 42


async def _fetch_recent_events() -> list[str]:
    await asyncio.sleep(0.5)
    return ["login", "purchase", "logout"]


async def _fetch_analytics_summary() -> dict:
    await asyncio.sleep(0.4)
    return {"visits": 1200, "conversions": 45}


# ─── Comparison: BackgroundTasks vs create_task vs gather ────────────────────

# ┌──────────────────┬────────────────────┬──────────────────────────────────┐
# │ Approach         │ When it runs       │ Best for                         │
# ├──────────────────┼────────────────────┼──────────────────────────────────┤
# │ BackgroundTasks  │ AFTER response     │ Emails, cleanup, audit logs      │
# │ create_task      │ NOW (fire & forget)│ Non-critical logging, metrics    │
# │ gather           │ NOW (wait for all) │ Parallel data fetching           │
# └──────────────────┴────────────────────┴──────────────────────────────────┘
#
# Key differences:
# - BackgroundTasks: client gets response fast; work happens after
# - create_task: work starts immediately but you don't await it
# - gather: work runs in parallel, you WAIT for all results before responding


# ─── Demonstration ───────────────────────────────────────────────────────────

async def _demo():
    """Show timing differences between the three approaches."""

    # 1. Sequential (baseline)
    print("1. Sequential (baseline):")
    start = time.perf_counter()
    await send_email("a@test.com")
    await log_event("demo")
    await update_analytics("/demo")
    print(f"   Total: {time.perf_counter() - start:.2f}s\n")

    # 2. gather (concurrent, wait for all)
    print("2. gather (concurrent, wait for all):")
    start = time.perf_counter()
    await asyncio.gather(
        send_email("b@test.com"),
        log_event("demo"),
        update_analytics("/demo"),
    )
    print(f"   Total: {time.perf_counter() - start:.2f}s\n")

    # 3. create_task (fire and forget)
    print("3. create_task (fire and forget):")
    start = time.perf_counter()
    asyncio.create_task(send_email("c@test.com"))
    asyncio.create_task(log_event("demo"))
    print(f"   Returned immediately: {time.perf_counter() - start:.4f}s")
    await asyncio.sleep(1.5)  # let tasks finish
    print(f"   After waiting for tasks: {time.perf_counter() - start:.2f}s\n")


if __name__ == "__main__":
    print("=== BackgroundTasks vs create_task vs gather ===\n")
    asyncio.run(_demo())

    print("=== Starting FastAPI server ===")
    uvicorn.run(app, host="0.0.0.0", port=8000)
